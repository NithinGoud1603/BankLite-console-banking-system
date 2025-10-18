import json
from datetime import datetime

# ========================
# Account Class
# ========================
class Account:
    def __init__(self, acc_id, name, balance=0.0):
        self.id = acc_id
        self.name = name
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        if amount <= 0:
            print("❌ Deposit amount must be positive.")
            return
        self.balance += amount
        transaction = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Deposited ₹{amount:.2f}"
        self.transactions.append(transaction)
        print("✅ Deposit successful.")

    def withdraw(self, amount):
        if amount <= 0:
            print("❌ Withdrawal amount must be positive.")
            return
        if amount > self.balance:
            print("❌ Insufficient balance.")
            return
        self.balance -= amount
        transaction = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Withdrawn ₹{amount:.2f}"
        self.transactions.append(transaction)
        print("✅ Withdrawal successful.")

    def get_balance(self):
        print(f"💰 Current Balance for {self.name}: ₹{self.balance:.2f}")

    def get_history(self):
        if not self.transactions:
            print("📜 No transactions yet.")
        else:
            print(f"📜 Transaction History for {self.name}:")
            for txn in self.transactions:
                print("   ", txn)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "balance": self.balance,
            "transactions": self.transactions,
        }

    @classmethod
    def from_dict(cls, data):
        acc = cls(data["id"], data["name"], data["balance"])
        acc.transactions = data["transactions"]
        return acc


# ========================
# Bank Class
# ========================
class Bank:
    def __init__(self):
        self.accounts = []

    def create_account(self, name, initial_deposit=0.0):
        acc_id = len(self.accounts) + 1
        new_acc = Account(acc_id, name, initial_deposit)
        new_acc.transactions.append(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Account created with ₹{initial_deposit:.2f}"
        )
        self.accounts.append(new_acc)
        print(f"🎉 Account created successfully! ID: {acc_id}")

    def find_account_by_id(self, acc_id):
        for acc in self.accounts:
            if acc.id == acc_id:
                return acc
        print("❌ Account not found.")
        return None

    def deposit_to_account(self, acc_id, amount):
        acc = self.find_account_by_id(acc_id)
        if acc:
            acc.deposit(amount)

    def withdraw_from_account(self, acc_id, amount):
        acc = self.find_account_by_id(acc_id)
        if acc:
            acc.withdraw(amount)

    def show_account_details(self, acc_id):
        acc = self.find_account_by_id(acc_id)
        if acc:
            print(f"\n📄 Account Details:")
            print(f"ID: {acc.id}")
            print(f"Name: {acc.name}")
            print(f"Balance: ₹{acc.balance:.2f}")
            acc.get_history()
            print()

    def save_to_file(self, filename="bank.json"):
        data = [acc.to_dict() for acc in self.accounts]
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print("💾 Data saved to bank.json")

    def load_from_file(self, filename="bank.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            self.accounts = [Account.from_dict(acc) for acc in data]
            print("📂 Data loaded from bank.json")
        except FileNotFoundError:
            print("⚠️ No previous data found. Starting fresh.")


# ========================
# Console Menu
# ========================
def main():
    bank = Bank()
    bank.load_from_file()

    while True:
        print("\n===== 🏦 BankLite Console Menu =====")
        print("1. Create Account")
        print("2. Deposit Funds")
        print("3. Withdraw Funds")
        print("4. View Balance")
        print("5. View Transaction History")
        print("6. Save & Exit")

        choice = input("👉 Enter your choice: ")

        if choice == "1":
            name = input("Enter account holder name: ")
            initial = float(input("Enter initial deposit: ₹"))
            bank.create_account(name, initial)

        elif choice == "2":
            acc_id = int(input("Enter Account ID: "))
            amount = float(input("Enter amount to deposit: ₹"))
            bank.deposit_to_account(acc_id, amount)

        elif choice == "3":
            acc_id = int(input("Enter Account ID: "))
            amount = float(input("Enter amount to withdraw: ₹"))
            bank.withdraw_from_account(acc_id, amount)

        elif choice == "4":
            acc_id = int(input("Enter Account ID: "))
            acc = bank.find_account_by_id(acc_id)
            if acc:
                acc.get_balance()

        elif choice == "5":
            acc_id = int(input("Enter Account ID: "))
            acc = bank.find_account_by_id(acc_id)
            if acc:
                acc.get_history()

        elif choice == "6":
            bank.save_to_file()
            print("👋 Thank you for using BankLite!")
            break

        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()