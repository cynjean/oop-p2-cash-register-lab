#!/usr/bin/env python3


class CashRegister:
    """Keep a running total and a history of reversible register actions."""

    def __init__(self, discount=0):
        # Start with empty state; use the property so constructor values are validated.
        self._discount = 0
        self.discount = discount
        self.total = 0
        self.items = []
        self.previous_transactions = []

    @property
    def discount(self):
        """The valid whole-number discount percentage for this register."""
        return self._discount

    @discount.setter
    def discount(self, value):
        # bool is an int subclass, so require the exact int type here.
        if type(value) is int and 0 <= value <= 100:
            self._discount = value
        else:
            print("Not valid discount")

    def add_item(self, item, price, quantity=1):
        """Add an item line, expanding quantity in items and recording one action."""
        line_total = price * quantity
        self.total += line_total
        self.items.extend([item] * quantity)
        self.previous_transactions.append({
            "item": item,
            "price": price,
            "quantity": quantity,
        })

    def apply_discount(self):
        """Reduce the total by the configured percentage and record that adjustment."""
        if not self.previous_transactions:
            print("There is no discount to apply.")
            return

        discount_amount = self.total * self.discount / 100
        self.total -= discount_amount
        # Record the adjustment so void_last_transaction can restore the old total.
        self.previous_transactions.append({
            "type": "discount",
            "amount": discount_amount,
        })
        print(f"After the discount, the total comes to ${self.total:g}.")

    def void_last_transaction(self):
        """Undo the last item line or discount adjustment."""
        if not self.previous_transactions:
            print("There is no transaction to void.")
            return

        transaction = self.previous_transactions.pop()
        if transaction.get("type") == "discount":
            # Undoing a discount adds back the amount previously removed.
            self.total += transaction["amount"]
            return

        quantity = transaction["quantity"]
        self.total -= transaction["price"] * quantity
        # A line may contain repeated item names; remove exactly its quantity from the end.
        del self.items[-quantity:]
