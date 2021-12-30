class Category:

    def __init__(self, name):
        self.ledger = []
        self.name = name

    def deposit(self, amount, descr=''):
        """Add a positive transaction to the ledger."""
        self.ledger.append({"amount": amount, "description": descr})

    def withdraw(self, amount, descr=''):
        """Add a negative transaction to the ledger (if possible)."""
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": descr})
            return True
        return False

    def get_balance(self):
        """Get the current balance in the ledger"""
        return sum(item["amount"] for item in self.ledger)

    def transfer(self, amount, category):
        """Transfer an amount to another ledger (if possible)."""
        if self.check_funds(amount):
            self.ledger.append(
                {"amount": -amount, "description": "Transfer to " + category.name})
            category.deposit(amount, "Transfer from " + self.name)
            return True
        return False

    def check_funds(self, amount):
        """Used to check if withdrawal or transaction is possible."""
        return True if self.get_balance() - amount >= 0 else False

    def __str__(self):
        halfNameLen = round(len(self.name)/2)
        display = '*' * (15 - halfNameLen) + self.name + \
            '*' * (15 - halfNameLen) + '\n'
        for entry in self.ledger:
            descOrig = entry['description']
            descNew = descOrig[:23] if len(descOrig) > 23 else descOrig
            display += descNew
            display += ' ' * (23 - len(descNew))
            amount = "%0.2f" % (entry['amount'])
            display += ' ' * (7 - len(amount))
            display += amount + '\n'

        display += 'Total: ' + str(self.get_balance())
        return display


def create_spend_chart(categories):
    """Prints a chart showing rough percentage of each category's spending"""

    # Store category name and the total of all negative values for each category in new data structure.
    catSum = []
    for cat in categories:
        tmpsum = sum(item['amount']
                     for item in cat.ledger if item['amount'] < 0)
        catSum.append({"category": cat.name, "sum": tmpsum})

    # Calculate the total of all negative values.
    totalsum = sum(item["sum"] for item in catSum)

    # Begin string creation, staring with 'y'-axis and 'bars'
    display = 'Percentage spent by category\n'
    for i in reversed(range(11)):
        display += ' ' * (3 - len(str(i*10))) + str(i*10) + '|'
        for cs in catSum:
            frac = cs["sum"]*10//totalsum*10  # Floor to 10th percent
            if frac >= i*10:
                display += ' o '
            else:
                display += '   '
        display += ' \n'
    display += ' ' * 4 + '-' * len(catSum) * 3 + '-\n'  # 'x'-axis

    # Creating the labels for the 'x'-axis
    display += ' ' * 5
    maxCatLen = max(len(item["category"]) for item in catSum)
    for c in range(maxCatLen):
        for cat in catSum:
            if len(cat["category"]) > c:
                display += cat["category"][c] + '  '
            else:
                display += '   '
        if c < maxCatLen-1:
            display += '\n' + ' ' * 5
    return display
