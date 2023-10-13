import sqlite3
import tkinter as tk
from tkinter import ttk

# Создаем базу данных
conn = sqlite3.connect('employees.db')
cursor = conn.cursor()

# Создаем таблицу employees с необходимыми полями
cursor.execute('CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, email TEXT, salary REAL)')

# Функция для добавления нового сотрудника
def add_employee():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    salary = float(salary_entry.get())

    cursor.execute('INSERT INTO employees (name, phone, email, salary) VALUES (?, ?, ?, ?)', (name, phone, email, salary))
    conn.commit()

    update_treeview()

# Функция для изменения данных о существующем сотруднике
def edit_employee():
    selected_item = treeview.selection()
    if selected_item:
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        salary = float(salary_entry.get())

        cursor.execute('UPDATE employees SET name=?, phone=?, email=?, salary=? WHERE id=?', (name, phone, email, salary, selected_item[0]))
        conn.commit()

        update_treeview()

# Функция для удаления сотрудника
def delete_employee():
    selected_item = treeview.selection()
    if selected_item:
        cursor.execute('DELETE FROM employees WHERE id=?', (selected_item[0],))
        conn.commit()

        update_treeview()

# Функция для поиска сотрудника по ФИО
def search_employee():
    name = search_entry.get()

    cursor.execute('SELECT * FROM employees WHERE name LIKE ?', ('%' + name + '%',))
    employees = cursor.fetchall()

    treeview.delete(*treeview.get_children())
    for employee in employees:
        treeview.insert('', 'end', values=employee[1:])

# Функция для обновления данных в Treeview
def update_treeview():
    cursor.execute('SELECT * FROM employees')
    employees = cursor.fetchall()

    treeview.delete(*treeview.get_children())
    for employee in employees:
        treeview.insert('', 'end', values=employee[1:])

# Создаем графический интерфейс с помощью tkinter
root = tk.Tk()
root.title('Список сотрудников компании')

# Создаем форму для добавления/изменения сотрудника
form_frame = ttk.LabelFrame(root, text='ФОРМА', padding=10)
form_frame.grid(row=0, column=0, padx=10, pady=10)

name_label = ttk.Label(form_frame, text='ФИО')
name_label.grid(row=0, column=0, sticky='W')

name_entry = ttk.Entry(form_frame)
name_entry.grid(row=0, column=1, padx=5, pady=5)

phone_label = ttk.Label(form_frame, text='Номер телефона')
phone_label.grid(row=1, column=0, sticky='W')

phone_entry = ttk.Entry(form_frame)
phone_entry.grid(row=1, column=1, padx=5, pady=5)

email_label = ttk.Label(form_frame, text='Адрес электронной почты')
email_label.grid(row=2, column=0, sticky='W')

email_entry = ttk.Entry(form_frame)
email_entry.grid(row=2, column=1, padx=5, pady=5)

salary_label = ttk.Label(form_frame, text='Заработная плата')
salary_label.grid(row=3, column=0, sticky='W')

salary_entry = ttk.Entry(form_frame)
salary_entry.grid(row=3, column=1, padx=5, pady=5)

add_button = ttk.Button(form_frame, text='Добавить', command=add_employee)
add_button.grid(row=4, column=0, padx=5, pady=5)

edit_button = ttk.Button(form_frame, text='Изменить', command=edit_employee)
edit_button.grid(row=4, column=1, padx=5, pady=5)

# Создаем форму для удаления/поиска сотрудника
delete_search_frame = ttk.LabelFrame(root, text='УДАЛЕНИЕ/ПОИСК', padding=10)
delete_search_frame.grid(row=0, column=1, padx=10, pady=10)

search_label = ttk.Label(delete_search_frame, text='Поиск по ФИО')
search_label.grid(row=0, column=0, sticky='W')

search_entry = ttk.Entry(delete_search_frame)
search_entry.grid(row=0, column=1, padx=5, pady=5)

search_button = ttk.Button(delete_search_frame, text='Найти', command=search_employee)
search_button.grid(row=1, column=0, padx=5, pady=5)

delete_button = ttk.Button(delete_search_frame, text='Удалить', command=delete_employee)
delete_button.grid(row=1, column=1, padx=5, pady=5)

# Создаем таблицу для вывода данных о сотрудниках
treeview_frame = ttk.Frame(root)
treeview_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

treeview = ttk.Treeview(treeview_frame, columns=('name', 'phone', 'email', 'salary'), show='headings')
treeview.grid(row=0, column=0, sticky='nsew')

treeview.heading('name', text='ФИО')
treeview.heading('phone', text='Номер телефона')
treeview.heading('email', text='Адрес электронной почты')
treeview.heading('salary', text='Заработная плата')

treeview.column('name', width=200)
treeview.column('phone', width=150)
treeview.column('email', width=200)
treeview.column('salary', width=100)

# Добавляем полосу прокрутки
scrollbar = ttk.Scrollbar(treeview_frame, orient="vertical", command=treeview.yview)
treeview.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky='ns')

# Обновляем данные в Treeview
update_treeview()

root.mainloop()

# Закрываем соединение с базой данных
cursor.close()
conn.close()

