import tkinter as tk
from tkinter import ttk
import os
import json
import random
from faker import Faker
from tkinter import messagebox
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

root = tk.Tk()
root.title('Форма информации о пациентах')
root.option_add("*Font", ("Helvetica", 11))

# первый контейнер

frame1 = tk.Frame(root)
frame1.pack(fill="both", expand=True, padx=10, pady=10)

table = ttk.Treeview(frame1, columns=("fio", "age", "gender", "height", "weight", "bmi"), show="headings")

scrollbar = ttk.Scrollbar(frame1, orient="vertical", command=table.yview) 
#листаем скроллбар -> листается таблица

table.configure(yscrollcommand=scrollbar.set) 
#листаем таблицу -> листается скроллбар

table.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", font=("Helvetica", 9), rowheight=25)
style.configure("Treeview.Heading", font=("Helvetica", 10))


# колонки таблицы

table.heading("fio", text="ФИО")
table.heading("age", text="Возраст")
table.heading("gender", text="Пол")
table.heading("height", text="Рост")
table.heading("weight", text="Вес")
table.heading("bmi", text="ИМТ")

table.column("fio", width=350, anchor="w")
table.column("age", width=50, anchor="center")
table.column("gender", width=50, anchor="center")
table.column("height", width=50, anchor="center")
table.column("weight", width=50, anchor="center")
table.column("bmi", width=50, anchor="center")


# второй контейнер (кнопки)

frame2 = tk.Frame(root)
frame2.pack(fill="x", padx=10, pady=10)

b_add = tk.Button(frame2, text="Добавить", command=lambda: open_form())
b_add.pack(side="left", padx=5)
b_edit = tk.Button(frame2, text="Редактировать", command=lambda: edit_selected())
b_edit.pack(side="left", padx=5)
b_stats = tk.Button(frame2, text="Статистика", command=lambda: statistics())
b_stats.pack(side="right", padx=5)


# заполняем таблицу пациентами

filename = "patients.json"
patients = []

def calculate_bmi(weight, height):
    height /= 100
    return round(weight/height**2, 1)

def generate_patients(count=20):
    fake = Faker("ru_RU")
    generated = []

    for _ in range(count):
        gender = random.choice(["М", "Ж"])
        if gender == "М": fio = fake.name_male()
        else: fio = fake.name_female()

        age = random.randint(18, 90)
        height = random.randint(150, 200)
        weight = random.randint(55, 130)
        bmi = calculate_bmi(weight, height)

        patient = {
            "fio": fio,
            "age": age,
            "gender": gender,
            "height": height,
            "weight": weight,
            "bmi": bmi
        }
        generated.append(patient)
    return generated

def save_data():
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(patients, file, ensure_ascii=False, indent=4)

def load_data():
    global patients
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            patients = json.load(file)
    else:
        patients = generate_patients(20)
        save_data()

def update_table():
    for row in table.get_children():
        table.delete(row)
    for p in patients:
        table.insert(
            "",
            tk.END,
            values=(p["fio"], p["age"], p["gender"], p["height"], p["weight"], p["bmi"])
        )

load_data()
update_table()


# работа кнопок

def open_form(edit_index=None): #или передаем число (номер в списке) для редактирования или (None) создаем нового

    form = tk.Toplevel(root)
    form.grab_set() #не дает кликать по главному окну пока это открыто

    l_fio = tk.Label(form, text="ФИО")
    l_age = tk.Label(form, text="Возраст")
    l_gender = tk.Label(form, text="Пол")
    l_height = tk.Label(form, text="Рост")
    l_weight = tk.Label(form, text="Вес")

    e_fio = tk.Entry(form)
    e_age = tk.Entry(form)
    combo_gender = ttk.Combobox(form, values=["М", "Ж"], state="readonly")
    e_height = tk.Entry(form)
    e_weight = tk.Entry(form)

    l_fio.grid(row=0, column=0)
    e_fio.grid(row=0, column=1)
    l_age.grid(row=1, column=0)
    e_age.grid(row=1, column=1)
    l_gender.grid(row=2, column=0)
    combo_gender.grid(row=2, column=1)
    l_height.grid(row=3, column=0)
    e_height.grid(row=3, column=1)
    l_weight.grid(row=4, column=0)
    e_weight.grid(row=4, column=1)

    if edit_index is not None:
        patient = patients[edit_index]
        e_fio.insert(0, patient["fio"])
        e_age.insert(0, patient["age"])
        e_height.insert(0, patient["height"])
        e_weight.insert(0, patient["weight"])
        combo_gender.set(patient["gender"])

    def save():
        fio = e_fio.get().strip()
        age = e_age.get().strip()
        gender = combo_gender.get()
        height = e_height.get().strip()
        weight = e_weight.get().strip()

        if not fio: 
            messagebox.showwarning("Ошибка", "Неверно введено ФИО!")
            return
        if not gender: 
                    messagebox.showwarning("Ошибка", "Не выбран пол!")
                    return

        try:
            age = int(age)
            height = int(height)
            weight = int(weight)
            if age <= 0 or height <= 0 or weight <= 0: raise ValueError
        except ValueError:
            messagebox.showwarning("Ошибка", "Неверно заполнены данные!", parent=form)
            return 

        bmi = calculate_bmi(weight, height)

        new_patient = {
            "fio": fio,
            "age": age,
            "gender": gender,
            "height": height,
            "weight": weight,
            "bmi": bmi
        }

        if edit_index is None:
            patients.append(new_patient)
        else:
            patients[edit_index] = new_patient

        save_data()
        update_table()
        form.destroy()

    btn_save = tk.Button(form, text="Сохранить", command=save)
    btn_save.grid(row=5, column=0, padx=10, pady=10)

    def delete():
        if messagebox.askyesno("Вы уверены?", "Хотите удалить данные о пациенте?"):
            patients.pop(edit_index)

            save_data()
            update_table()
            form.destroy()

    if edit_index is not None:
        btn_del = tk.Button(form, text="Удалить", command=delete)
        btn_del.grid(row=5, column=1, padx=10, pady=10)

def edit_selected():
    selected = table.selection()  #узнаем выделена ли строка в таблице
    if not selected:
        messagebox.showwarning("Внимание", "Выберите пациента в таблице!")
        return

    row_id = selected[0]         # Берём системный ID первой выделенной строки (например, 'I004')
    index = table.index(row_id)   # Превращаем его в обычный порядковый номер (например, 3)
    open_form(index) 


# Сводная статистика

def statistics():
    if not patients:
        messagebox.showwarning("Инфо", "Нет данных для статистики")
        return

    ages = [p["age"] for p in patients]
    bmis = [p["bmi"] for p in patients]
    genders = [p["gender"] for p in patients]
    bmi_m = [p["bmi"] for p in patients if p["gender"] == "М"]
    bmi_f = [p["bmi"] for p in patients if p["gender"] == "Ж"]

    # создаем окно для графиков
    plt.figure("Сводная статистика по пациентам", figsize=(10, 7))

    # --- Распределение по полу
    plt.subplot(2, 2, 1)
    # рисует столбчатую диаграмму
    plt.bar(["Мужчины", "Женщины"], [genders.count("М"), genders.count("Ж")])
    plt.title("Распределение по полу")

    # --- Распределение по возрасту
    plt.subplot(2, 2, 2)
    # разбивает числа на интервалы и строит гистограмму распределения
    plt.hist(ages)
    plt.title("Распределение по возрасту")

    # --- Распределение ИМТ по полу
    plt.subplot(2, 2, 3)
    plt.hist(bmi_m, alpha=0.5, label="Мужчины")
    plt.hist(bmi_f, alpha=0.5, label="Женщины")
    plt.legend()
    plt.title("Распределение ИМТ по полу")

    # --- Зависимость ИМТ от возраста
    plt.subplot(2, 2, 4)
    # ставит точки на координатной плоскости
    plt.scatter(ages, bmis)
    plt.title("Зависимость ИМТ от возраста")

    plt.tight_layout() # раздвигает графики, чтобы заголовки не налезали друг на друга
    plt.show(block=False)


root.mainloop()