
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from datetime import date

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import Calendar

from style import (
    apply_style,
    create_label,
    create_button,
    create_entry,
    create_frame,
    BG_COLOR,
    CARD_COLOR,
    TEXT_COLOR
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "expenses.csv"

DATA_DIR.mkdir(exist_ok=True)

COLUMNS = ["ID", "Date", "Amount", "Category", "Notes"]


def load_data():

    if not DATA_FILE.exists():
        return pd.DataFrame(columns=COLUMNS)

    try:
        data = pd.read_csv(DATA_FILE)

        for column in COLUMNS:
            if column not in data.columns:
                data[column] = None

        data = data[COLUMNS]

        data["ID"] = pd.to_numeric(data["ID"], errors="coerce")
        data["Amount"] = pd.to_numeric(data["Amount"], errors="coerce")

        data = data.dropna(subset=["ID"])
        data["Date"] = data["Date"].astype(str)

        return data.reset_index(drop=True)

    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=COLUMNS)


expenses = load_data()


def save_data():
    expenses.to_csv(DATA_FILE, index=False)


class ExpenseTracker:

    def __init__(self, root):

        self.root = root

        self.root.title("Personal Expense Tracker")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)

        apply_style(root)

        self.create_widgets()
        self.show_month()

    # CREATE GUI

    def create_widgets(self):

        top = create_frame(self.root)
        top.pack(fill="x", padx=20, pady=20)

        # CALENDAR

        calendar_frame = tk.LabelFrame(
            top,
            text="Select Date",
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            font=("Arial", 12, "bold")
        )

        calendar_frame.pack(side="left", padx=10, anchor="n")

        self.cal = Calendar(
            calendar_frame,
            date_pattern="yyyy-mm-dd",
            year=date.today().year,
            month=date.today().month,
            day=date.today().day,
            width=45,
            height=18,
            font=("Arial", 18),
            headersfont=("Arial", 16, "bold")
        )

        self.cal.pack(padx=10, pady=10)

        # INPUT FORM

        form = create_frame(top)

        form.pack(
            side="left",
            fill="y",
            expand=True,
            padx=30,
            anchor="n"
        )

        create_label(
            form,
            "Category",
            16,
            True
        ).pack(pady=5)

        self.category = ttk.Combobox(
            form,
            values=[
                "Food",
                "Bills",
                "Travel",
                "Transport",
                "Shopping",
                "Entertainment",
                "Health",
                "Education",
                "Other"
            ],
            state="readonly",
            width=30,
            font=("Arial", 16)
        )

        self.category.pack(pady=5)
        self.category.set("Food")

        create_label(
            form,
            "Amount",
            16,
            True
        ).pack(pady=10)

        self.amount_entry = create_entry(form)
        self.amount_entry.pack(pady=5)

        create_label(
            form,
            "Notes",
            16,
            True
        ).pack(pady=10)

        self.notes_entry = create_entry(form)
        self.notes_entry.pack(pady=5)

        # BUTTONS

        button_frame = create_frame(form)
        button_frame.pack(pady=15)

        create_button(
            button_frame,
            "Search Date",
            self.search_date
        ).grid(row=0, column=0, padx=5, pady=5)

        create_button(
            button_frame,
            "Show Month",
            self.show_month
        ).grid(row=0, column=1, padx=5, pady=5)

        create_button(
            button_frame,
            "Submit",
            self.add_expense,
            34
        ).grid(row=1, column=0, columnspan=2, pady=10)

        # SPENDING CHART

        chart_frame = tk.LabelFrame(
            top,
            text="Category-wise Spending",
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            font=("Arial", 12, "bold")
        )

        chart_frame.pack(side="right", padx=10, anchor="n")

        self.figure, self.ax = plt.subplots(figsize=(5, 4.5))

        self.figure.patch.set_facecolor(CARD_COLOR)

        self.chart_canvas = FigureCanvasTkAgg(
            self.figure,
            master=chart_frame
        )

        self.chart_canvas.get_tk_widget().pack(
            padx=10,
            pady=10
        )

        # DELETE BUTTON

        delete_frame = create_frame(self.root)

        delete_frame.pack(fill="x", padx=20, pady=5)

        create_button(
            delete_frame,
            "Delete Selected Expense",
            self.delete_expense,
            25
        ).pack(anchor="w", pady=5)

        # EXPENSE HISTORY

        table_frame = tk.LabelFrame(
            self.root,
            text="Expense History",
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            font=("Arial", 14, "bold")
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=COLUMNS,
            show="headings",
            height=15
        )

        widths = {
            "ID": 100,
            "Date": 220,
            "Amount": 180,
            "Category": 250,
            "Notes": 600
        }

        for column in COLUMNS:

            self.table.heading(column, text=column)

            self.table.column(
                column,
                width=widths[column],
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(side="right", fill="y")

    # ADD EXPENSE

    def add_expense(self):

        global expenses

        selected_date = self.cal.get_date()
        category = self.category.get()
        amount_text = self.amount_entry.get().strip()
        notes = self.notes_entry.get().strip()

        if not amount_text:

            messagebox.showerror(
                "Error",
                "Please enter an amount"
            )
            return

        try:

            amount = float(amount_text)

            if amount <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Error",
                "Enter a valid amount greater than zero"
            )
            return

        new_id = (
            1 if expenses.empty
            else int(expenses["ID"].max()) + 1
        )

        new_row = {
            "ID": new_id,
            "Date": selected_date,
            "Amount": amount,
            "Category": category,
            "Notes": notes
        }

        expenses.loc[len(expenses)] = new_row

        save_data()

        self.amount_entry.delete(0, tk.END)
        self.notes_entry.delete(0, tk.END)

        self.show_month()

        messagebox.showinfo(
            "Success",
            "Expense added successfully"
        )

    # DISPLAY EXPENSES

    def display_expenses(self, data):

        for item in self.table.get_children():
            self.table.delete(item)

        for _, row in data.iterrows():

            self.table.insert(
                "",
                tk.END,
                values=[
                    row["ID"],
                    row["Date"],
                    row["Amount"],
                    row["Category"],
                    row["Notes"]
                ]
            )

    # SEARCH DATE

    def search_date(self):

        selected_date = self.cal.get_date()

        if expenses.empty:
            data = expenses.copy()

        else:
            data = expenses[
                expenses["Date"].astype(str) == selected_date
            ]

        self.display_expenses(data)
        self.update_chart(data)

    # SHOW MONTH

    def show_month(self):

        selected_date = self.cal.get_date()
        selected_month = selected_date[:7]

        if expenses.empty:
            data = expenses.copy()

        else:
            data = expenses[
                expenses["Date"].astype(str).str.startswith(
                    selected_month
                )
            ]

        self.display_expenses(data)
        self.update_chart(data)

    # UPDATE CHART

    def update_chart(self, data):

        self.ax.clear()

        if not data.empty:

            category_totals = data.groupby(
                "Category"
            )["Amount"].sum()

            self.ax.pie(
                category_totals,
                labels=category_totals.index,
                autopct="%1.0f%%",
                startangle=90
            )

        else:

            self.ax.text(
                0.5,
                0.5,
                "No Expenses",
                ha="center",
                va="center"
            )

        self.ax.set_title("Spending")

        self.figure.tight_layout()
        self.chart_canvas.draw()

    # DELETE EXPENSE

    def delete_expense(self):

        global expenses

        selected = self.table.selection()

        if not selected:

            messagebox.showwarning(
                "Select Expense",
                "Please select an expense from the table"
            )
            return

        item = self.table.item(selected[0])
        expense_id = item["values"][0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this expense?"
        )

        if not confirm:
            return

        expenses = expenses[
            pd.to_numeric(
                expenses["ID"],
                errors="coerce"
            ) != float(expense_id)
        ]

        expenses.reset_index(drop=True, inplace=True)

        save_data()
        self.show_month()

        messagebox.showinfo(
            "Deleted",
            "Expense deleted successfully"
        )


# RUN APPLICATION

if __name__ == "__main__":

    root = tk.Tk()

    app = ExpenseTracker(root)

    root.mainloop()
