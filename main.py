import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt


class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        # Expense list to store expenses
        self.expenses = []

        # Creating UI elements
        self.create_widgets()

    def create_widgets(self):
        # Description Label and Entry
        self.desc_label = tk.Label(self.root, text="Description:")
        self.desc_label.grid(row=0, column=0, padx=10, pady=10)

        self.desc_entry = tk.Entry(self.root, width=30)
        self.desc_entry.grid(row=0, column=1, padx=10, pady=10)

        # Amount Label and Entry
        self.amount_label = tk.Label(self.root, text="Amount:")
        self.amount_label.grid(row=1, column=0, padx=10, pady=10)

        self.amount_entry = tk.Entry(self.root, width=30)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=10)

        # Category Label and Dropdown
        self.category_label = tk.Label(self.root, text="Category:")
        self.category_label.grid(row=2, column=0, padx=10, pady=10)

        self.category_options = ["Food", "Transport", "Entertainment", "Utilities", "Other"]
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(self.root, textvariable=self.category_var)
        self.category_dropdown['values'] = self.category_options
        self.category_dropdown.grid(row=2, column=1, padx=10, pady=10)
        self.category_dropdown.current(0)  # Set default category

        # Add Button
        self.add_button = tk.Button(self.root, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Expenses Listbox
        self.expenses_listbox = tk.Listbox(self.root, width=50, height=10)
        self.expenses_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Total Label
        self.total_label = tk.Label(self.root, text="Total: $0.00")
        self.total_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        # View Graph Button
        self.graph_button = tk.Button(self.root, text="View Graph", command=self.view_graph)
        self.graph_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def add_expense(self):
        description = self.desc_entry.get()
        amount = self.amount_entry.get()
        category = self.category_var.get()

        if description == "" or amount == "":
            messagebox.showwarning("Input Error", "Please enter both description and amount")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid amount")
            return

        # Add expense to the list
        self.expenses.append((description, amount, category))

        # Update the listbox and total
        self.update_expenses_listbox()
        self.update_total()

        # Clear the entry fields
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_dropdown.current(0)

    def update_expenses_listbox(self):
        self.expenses_listbox.delete(0, tk.END)
        for desc, amount, category in self.expenses:
            self.expenses_listbox.insert(tk.END, f"{desc}: ${amount:.2f} ({category})")

    def update_total(self):
        total = sum(amount for _, amount, _ in self.expenses)
        self.total_label.config(text=f"Total: ${total:.2f}")

    def view_graph(self):
        if not self.expenses:
            messagebox.showwarning("No Data", "No expenses to display.")
            return

        # Summarize expenses by category
        category_totals = {}
        for _, amount, category in self.expenses:
            if category in category_totals:
                category_totals[category] += amount
            else:
                category_totals[category] = amount

        # Plotting the graph
        categories = list(category_totals.keys())
        totals = list(category_totals.values())

        plt.figure(figsize=(10, 5))
        plt.bar(categories, totals, color='blue')
        plt.xlabel('Categories')
        plt.ylabel('Total Amount ($)')
        plt.title('Expenses by Category')
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
