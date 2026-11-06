
import tkinter as tk
from tkinter import ttk

BG_COLOR = "#F4F7FB"
CARD_COLOR = "#FFFFFF"
PRIMARY_COLOR = "#2563EB"
SECONDARY_COLOR = "#1E40AF"
TEXT_COLOR = "#1E293B"
MUTED_COLOR = "#64748B"
BORDER_COLOR = "#DCE3ED"

FONT = "Arial"

def apply_style(root):

    root.configure(bg=BG_COLOR)

    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Treeview",
        background=CARD_COLOR,
        foreground=TEXT_COLOR,
        rowheight=40,
        font=(FONT, 12),
        fieldbackground=CARD_COLOR
    )

    style.configure(
        "Treeview.Heading",
        background=PRIMARY_COLOR,
        foreground="white",
        font=(FONT, 12, "bold"),
        padding=10
    )

    style.map(
        "Treeview",
        background=[("selected", "#BFDBFE")],
        foreground=[("selected", TEXT_COLOR)]
    )

    style.configure(
        "TCombobox",
        padding=8,
        font=(FONT, 12)
    )


def create_label(parent, text, size=14, bold=False):

    return tk.Label(
        parent,
        text=text,
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        font=(FONT, size, "bold" if bold else "normal")
    )


def create_button(parent, text, command, width=16):

    return tk.Button(
        parent,
        text=text,
        command=command,
        width=width,
        height=2,
        bg=PRIMARY_COLOR,
        fg="white",
        activebackground=SECONDARY_COLOR,
        activeforeground="white",
        font=(FONT, 11, "bold"),
        relief="flat",
        cursor="hand2",
        bd=0
    )


def create_entry(parent, width=30):

    return tk.Entry(
        parent,
        width=width,
        font=(FONT, 13),
        bg="white",
        fg=TEXT_COLOR,
        relief="solid",
        bd=1,
        highlightthickness=1,
        highlightbackground=BORDER_COLOR
    )


def create_frame(parent, **kwargs):

    return tk.Frame(
        parent,
        bg=CARD_COLOR,
        **kwargs
    )
