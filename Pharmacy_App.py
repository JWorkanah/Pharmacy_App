
import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class PharmacyManagementSystem:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Pharmacy Application')
        self.medicines = []  

        self.name_label = tk.Label(self.window, text='Medication')
        self.name_label.grid(column=0, row=0, padx=10, pady=10)

        self.name_entry = tk.Entry(self.window)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.quantity_label = tk.Label(self.window, text='Qty')
        self.quantity_label.grid(column=0, row=1, padx=10, pady=10)

        self.quantity_entry = tk.Entry(self.window)
        self.quantity_entry.grid(row=1, column=1, padx=10, pady=10)

        self.add_button = tk.Button(self.window, text='Add', command=self.add_medicine)
        self.add_button.grid(row=2, column=1, padx=10, pady=10)

        self.update_button = tk.Button(self.window, text='Update', command=self.update_quantity)
        self.update_button.grid(row=2, column=2, padx=10, pady=10)

        self.delete_button = tk.Button(self.window, text='Delete', command=self.delete_medicine)
        self.delete_button.grid(row=2, column=3, padx=10, pady=10)

        self.display_button = tk.Button(self.window, text='Display', command=self.display_medicines)
        self.display_button.grid(row=2, column=4, padx=10, pady=10)

        self.treeview = ttk.Treeview(self.window, columns=('Name', 'Quantity'), show='headings')
        self.treeview.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.treeview.heading('Name', text='Medicine Name')
        self.treeview.heading('Quantity', text='Quantity')

        self.conn = sqlite3.connect('Pharmacy.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS medicines
                               (name TEXT, quantity INTEGER)''')
        self.conn.commit()

    def add_medicine(self):
        name = self.name_entry.get()
        quantity = self.quantity_entry.get()

        if name and quantity:
            self.medicines.append((name, quantity))
            messagebox.showinfo(title='Success', message='Medicine added successfully')
            self.name_entry.delete(0, tk.END)
            self.quantity_entry.delete(0, tk.END)

            self.save_medicine_to_database(name, quantity)
            self.display_medicines()
        else:
            messagebox.showinfo(title='Error', message="Please enter both medicine's name and quantity.")

        self.conn.commit()

    def save_medicine_to_database(self, name, quantity):
        try:
            self.cursor.execute("INSERT INTO medicines (name, quantity) VALUES (?, ?)", (name, quantity))
            self.conn.commit()
        except sqlite3.Error as e:
            messagebox.showinfo("Error", f"Database Error: {e}")

    def update_quantity(self):
        name = self.name_entry.get()
        quantity = self.quantity_entry.get()

        if name and quantity:
            self.update_medicine_in_database(name, quantity)
            self.display_medicines()
        else:
            messagebox.showerror("Error", "Please enter both medicine's name and quantity.")

    def update_medicine_in_database(self, name, quantity):
        try:
            self.cursor.execute("UPDATE medicines SET quantity = ? WHERE name = ?", (quantity, name))
            self.conn.commit()
            messagebox.showinfo("Success", "Quantity updated successfully")
        except sqlite3.Error as e:
            messagebox.showinfo("Error", f"Database Error: {e}")

    def delete_medicine(self):
        name = self.name_entry.get()
        if name:
            self.delete_medicine_from_database(name)
            messagebox.showinfo("Success", "Medicine deleted successfully.")
            self.name_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please enter Medicine name.")

    def delete_medicine_from_database(self, name):
        try:
            self.cursor.execute("DELETE FROM medicines WHERE name = ?", (name,))
            self.conn.commit()
        except sqlite3.Error as e:
            messagebox.showinfo("Error", f"Database Error: {e}")

    def display_medicines(self):
        try:
            self.treeview.delete(*self.treeview.get_children())

            self.cursor.execute("select name, quantity from medicines")
            medicines = self.cursor.fetchall()

            for medicine in medicines:
                self.treeview.insert('', tk.END, values=medicine)

        except sqlite3.Error as e:
            messagebox.showinfo("Error", f"Database Error: {e}")

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def run(self):
        self.window.geometry('600x400')
        self.window.mainloop()

pharmacy_system = PharmacyManagementSystem()
pharmacy_system.run()

