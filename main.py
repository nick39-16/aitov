import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

DATA_FILE = 'trainings.json'

def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_training():
    date = entry_date.get()
    training_type = combo_type.get()
    duration = entry_duration.get()

    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        messagebox.showerror('Ошибка', 'Дата должна быть в формате ГГГГ-ММ-ДД')
        return

    if not duration.replace('.', '', 1).isdigit() or float(duration) <= 0:
        messagebox.showerror('Ошибка', 'Длительность должна быть положительным числом')
        return

    training = {'date': date, 'type': training_type, 'duration': float(duration)}
    data.append(training)
    save_data(data)
    update_table()
    clear_inputs()

def update_table(filter_type=None, filter_date=None):
    for i in tree.get_children():
        tree.delete(i)
    for t in data:
        if filter_type and t['type'] != filter_type:
            continue
        if filter_date and t['date'] != filter_date:
            continue
        tree.insert('', 'end', values=(t['date'], t['type'], t['duration']))

def filter_trainings():
    t_type = combo_filter_type.get() if combo_filter_type.get() else None
    t_date = entry_filter_date.get() if entry_filter_date.get() else None
    update_table(t_type, t_date)

def clear_inputs():
    entry_date.delete(0, tk.END)
    combo_type.set('')
    entry_duration.delete(0, tk.END)

data = load_data()

root = tk.Tk()
root.title('Training Planner')
root.geometry('800x500')

tab_control = ttk.Notebook(root)
tab_main = ttk.Frame(tab_control)
tab_filter = ttk.Frame(tab_control)
tab_control.add(tab_main, text='Добавить тренировку')
tab_control.add(tab_filter, text='Фильтр')
tab_control.pack(expand=1, fill='both')

# Вкладка "Добавить тренировку"
tk.Label(tab_main, text='Дата (ГГГГ-ММ-ДД):').grid(row=0, column=0, padx=5, pady=5)
entry_date = tk.Entry(tab_main)
entry_date.grid(row=0, column=1, padx=5, pady=5)

tk.Label(tab_main, text='Тип тренировки:').grid(row=1, column=0, padx=5, pady=5)
combo_type = ttk.Combobox(tab_main, values=['Кардио', 'Силовая', 'Растяжка', 'Йога', 'Прочее'])
combo_type.grid(row=1, column=1, padx=5, pady=5)

tk.Label(tab_main, text='Длительность (мин):').grid(row=2, column=0, padx=5, pady=5)
entry_duration = tk.Entry(tab_main)
entry_duration.grid(row=2, column=1, padx=5, pady=5)

btn_add = tk.Button(tab_main, text='Добавить тренировку', command=add_training)
btn_add.grid(row=3, column=0, columnspan=2, pady=10)

tree = ttk.Treeview(tab_main, columns=('Дата', 'Тип', 'Длительность'), show='headings')
tree.heading('Дата', text='Дата')
tree.heading('Тип', text='Тип')
tree.heading('Длительность', text='Длительность (мин)')
tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

# Вкладка "Фильтр"
tk.Label(tab_filter, text='Тип тренировки:').grid(row=0, column=0, padx=5, pady=5)
combo_filter_type = ttk.Combobox(tab_filter, values=['Все', 'Кардио', 'Силовая', 'Растяжка', 'Йога', 'Прочее'])
combo_filter_type.set('Все')
combo_filter_type.grid(row=0, column=1, padx=5, pady=5)

tk.Label(tab_filter, text='Дата (ГГГГ-ММ-ДД):').grid(row=1, column=0, padx=5, pady=5)
entry_filter_date = tk.Entry(tab_filter)
entry_filter_date.grid(row=1, column=1, padx=5, pady=5)

btn_filter = tk.Button(tab_filter, text='Применить фильтр', command=filter_trainings)
btn_filter.grid(row=2, column=0, columnspan=2, pady=10)

update_table()
root.mainloop()
