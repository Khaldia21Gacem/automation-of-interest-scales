import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os
from datetime import datetime

def browse_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Excel or CSV Files", "*.xlsx;*.xls;*.csv")])
    if file_path:
        file_label.config(text=f"Selected File: {file_path}")
        clean_data()

def clean_data():
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path, header=None, dtype=str)  # Read as strings to avoid format issues
        else:
            df = pd.read_excel(file_path, header=None, dtype=str)

        df = df[0].str.split("!", expand=True)  # Split column by "!"
        df.replace(r'^\s*$', None, regex=True, inplace=True)  # Convert empty spaces to NaN
        df.dropna(how='all', inplace=True)  # Remove empty rows

        # Fix date formatting in the first column
        def clean_date(value):
            if isinstance(value, str):
                value = value.replace('*', '')  # Remove '*'
                if pd.to_datetime(value, format="%d/%m/%y", errors='coerce') is not pd.NaT:
                    return pd.to_datetime(value, format="%d/%m/%y").strftime("%d/%m/%Y")
            return value

        df.iloc[:, 0] = df.iloc[:, 0].apply(clean_date)  # Apply fix to first column

        # Ensure first column is treated as a date in Excel
        df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0], errors='coerce')

        # Save cleaned file
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        dir_path = os.path.dirname(file_path)
        cleaned_file_path = os.path.join(dir_path, f"cleaned_data_{timestamp}.xlsx")

        with pd.ExcelWriter(cleaned_file_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, header=False)
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']
            date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})
            worksheet.set_column(0, 0, None, date_format)  # Apply date format

        messagebox.showinfo("Success", f"Data cleaning completed!\nSaved at:\n{cleaned_file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

root = tk.Tk()
root.title("Excel File Selector")
root.geometry("800x400")

browse_button = tk.Button(root, text="Browse Excel or CSV File", command=browse_file)
browse_button.pack(pady=10)

file_label = tk.Label(root, text="No file selected")
file_label.pack()

root.mainloop()
