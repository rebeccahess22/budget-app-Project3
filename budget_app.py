lass Category:
    def __init__(self, category):
        self.category = category
        self.ledger = []

    def __str__(self):
        title = self.category.center(30, '*') + '\n'
        items = ''
        for entry in self.ledger:
            desc = entry['description'][:23].ljust(23)
            amt = f"{entry['amount']:.2f}".rjust(7)
            items += f"{desc}{amt}\n"
        total = f"Total: {self.get_balance():.2f}"
        return title + items + total

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        return sum(entry['amount'] for entry in self.ledger)

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.category}")
            category.deposit(amount, f"Transfer from {self.category}")
            return True
        return False

    def check_funds(self, amount):
        return amount <= self.get_balance()


def create_spend_chart(categories):
    withdrawals = {}
    total_spent = 0

    for cat in categories:
        spent = sum(-entry['amount'] for entry in cat.ledger if entry['amount'] < 0)
        withdrawals[cat.category] = spent
        total_spent += spent

    percentages = {
        category: int((amount / total_spent) * 10) * 10
        for category, amount in withdrawals.items()
    }

    chart = "Percentage spent by category\n"
    for i in range(100, -1, -10):
        chart += str(i).rjust(3) + "|"
        for cat in categories:
            if percentages[cat.category] >= i:
                chart += " o "
            else:
                chart += "   "
        chart += " \n"

    chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"

    # Vertical names
    max_len = max(len(cat.category) for cat in categories)
    for i in range(max_len):
        line = "     "
        for cat in categories:
            if i < len(cat.category):
                line += cat.category[i] + "  "
            else:
                line += "   "
        chart += line.rstrip() + "  \n"  # << two spaces after final category

    return chart.rstrip('\n')

food = Category("Food")
entertainment = Category("Entertainment")
business = Category("Business")

food.deposit(900, "deposit")
food.withdraw(105.55, "groceries")
food.withdraw(33.40, "restaurant")

entertainment.deposit(900, "deposit")
entertainment.withdraw(33.40, "movies")

business.deposit(900, "deposit")
business.withdraw(10.99, "stationery")

print(create_spend_chart([business, food, entertainment]))