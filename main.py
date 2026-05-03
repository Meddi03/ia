import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = "data.json"


class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.root.geometry("800x500")


        self.trainings = []
        self.load_data()


        self.create_input_frame()
        self.create_table()
        self.create_filter_frame()


        self.refresh_table()

    def create_input_frame(self):
        """Форма ввода новой тренировки"""
        frame = tk.LabelFrame(self.root, text="Добавить тренировку", padx=10, pady=10)
        frame.pack(fill="x", padx=10, pady=5)


        tk.Label(frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.date_entry = tk.Entry(frame)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))


        tk.Label(frame, text="Тип тренировки:").grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.type_combobox = ttk.Combobox(frame, values=["Бег", "Велосипед", "Плавание", "Силовая", "Йога"], width=15)
        self.type_combobox.grid(row=0, column=3, padx=5, pady=5)
        self.type_combobox.current(0)


        tk.Label(frame, text="Длительность (мин):").grid(row=0, column=4, sticky="e", padx=5, pady=5)
        self.duration_entry = tk.Entry(frame, width=10)
        self.duration_entry.grid(row=0, column=5, padx=5, pady=5)


        add_btn = tk.Button(frame, text="Добавить тренировку", command=self.add_training, bg="lightgreen")
        add_btn.grid(row=0, column=6, padx=10, pady=5)

    def create_table(self):
        """Таблица с тренировками"""
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("ID", "Дата", "Тип", "Длительность (мин)")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150 if col != "ID" else 40)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_filter_frame(self):
        """Фильтрация"""
        frame = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=5)
        frame.pack(fill="x", padx=10, pady=5)


        tk.Label(frame, text="Фильтр по типу:").pack(side="left", padx=5)
        self.filter_type = ttk.Combobox(frame, values=["Все", "Бег", "Велосипед", "Плавание", "Силовая", "Йога"], width=12)
        self.filter_type.pack(side="left", padx=5)
        self.filter_type.current(0)


        tk.Label(frame, text="Фильтр по дате (ГГГГ-ММ-ДД):").pack(side="left", padx=5)
        self.filter_date = tk.Entry(frame, width=12)
        self.filter_date.pack(side="left", padx=5)


        apply_btn = tk.Button(frame, text="Применить фильтр", command=self.refresh_table, bg="lightblue")
        apply_btn.pack(side="left", padx=5)

        reset_btn = tk.Button(frame, text="Сбросить фильтры", command=self.reset_filters, bg="lightgray")
        reset_btn.pack(side="left", padx=5)

    def add_training(self):
        """Добавление тренировки с проверкой данных"""
        date = self.date_entry.get().strip()
        training_type = self.type_combobox.get()
        duration = self.duration_entry.get().strip()


        if not date or not training_type or not duration:
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты! Используйте ГГГГ-ММ-ДД")
            return

        try:
            duration_val = float(duration)
            if duration_val <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом!")
            return


        new_id = max([t["id"] for t in self.trainings], default=0) + 1
        self.trainings.append({
            "id": new_id,
            "date": date,
            "type": training_type,
            "duration": duration_val
        })

        self.save_data()
        self.refresh_table()


        self.duration_entry.delete(0, tk.END)

        messagebox.showinfo("Успех", "Тренировка добавлена!")

    def refresh_table(self):
        """Обновление таблицы с учётом фильтров"""
        for row in self.tree.get_children():
            self.tree.delete(row)


        filtered = self.trainings

        type_filter = self.filter_type.get()
        if type_filter != "Все":
            filtered = [t for t in filtered if t["type"] == type_filter]

        date_filter = self.filter_date.get().strip()
        if date_filter:
            filtered = [t for t in filtered if t["date"] == date_filter]

        for t in filtered:
            self.tree.insert("", "end", values=(t["id"], t["date"], t["type"], t["duration"]))


    def reset_filters(self):
        """Сброс фильтров"""
        self.filter_type.current(0)
        self.filter_date.delete(0, tk.END)
        self.refresh_table()

    def load_data(self):
        """Загрузка данных из JSON"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.trainings = json.load(f)
            except:
                self.trainings = []
        else:
            self.trainings = []

    def save_data(self):
        """Сохранение данных в JSON"""
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.trainings, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()