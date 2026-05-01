import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class MovieLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Личная кинотека")
        self.root.geometry("800x500")

        # --- Создание виджетов ---
        self.create_widgets()

        # --- Загрузка данных из файла при запуске ---
        self.load_data()

    def create_widgets(self):
        # --- Поля ввода ---
        tk.Label(self.root, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_title = tk.Entry(self.root, width=30)
        self.entry_title.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

        tk.Label(self.root, text="Жанр:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_genre = tk.Entry(self.root, width=30)
        self.entry_genre.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        tk.Label(self.root, text="Год выпуска:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_year = tk.Entry(self.root, width=10)
        self.entry_year.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.root, text="Рейтинг (0-10):").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.entry_rating = tk.Entry(self.root, width=10)
        self.entry_rating.grid(row=2, column=3, padx=5, pady=5)

        # --- Кнопка добавления ---
        btn_add = tk.Button(self.root, text="Добавить фильм", command=self.add_movie)
        btn_add.grid(row=3, column=0, columnspan=4, pady=10)

        # --- Таблица для вывода фильмов ---
        columns = ("title", "genre", "year", "rating")
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        
        self.tree.heading("title", text="Название")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("year", text="Год")
        self.tree.heading("rating", text="Рейтинг")
        
        self.tree.grid(row=4, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

        # Настройка веса колонок для растягивания
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(4, weight=1)

    def add_movie(self):
        title = self.entry_title.get().strip()
        genre = self.entry_genre.get().strip()
        year = self.entry_year.get().strip()
        rating = self.entry_rating.get().strip()

        # Проверка на пустые поля
        if not title or not genre or not year or not rating:
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return

        # Проверка года (должен быть числом в разумном диапазоне)
        if not year.isdigit() or not (1800 <= int(year) <= 2100):
            messagebox.showerror("Ошибка", "Год должен быть числом от 1800 до 2100!")
            return

        # Проверка рейтинга (должен быть числом от 0 до 10)
        try:
            rating_val = float(rating)
            if not (0 <= rating_val <= 10):
                raise ValueError
            rating = f"{rating_val:.1f}"  # Форматируем для красоты
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10!")
            return

        # Добавление в таблицу
        self.tree.insert("", "end", values=(title, genre, year, rating))
        
        # Очистка полей ввода
        self.clear_entries()

    def clear_entries(self):
        self.entry_title.delete(0, tk.END)
        self.entry_genre.delete(0, tk.END)
        self.entry_year.delete(0, tk.END)
        self.entry_rating.delete(0, tk.END)

    def save_data(self):
        movies = [self.tree.item(i)["values"] for i in self.tree.get_children()]
        
        try:
            with open("movies.json", "w", encoding="utf-8") as f:
                json.dump(movies, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Успех", "Данные сохранены в movies.json")
            return True
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", str(e))
            return False

    def load_data(self):
        if not os.path.exists("movies.json"):
            return

        try:
            with open("movies.json", "r", encoding="utf-8") as f:
                movies = json.load(f)
            
            for movie in movies:
                self.tree.insert("", "end", values=tuple(movie))
                
            messagebox.showinfo("Загрузка", "Данные успешно загружены из movies.json")
            
            # Проверка целостности данных (на случай ручного редактирования JSON)
            for item in self.tree.get_children():
                values = self.tree.item(item)['values']
                if len(values) != 4 or not values[2].isdigit():
                    self.tree.delete(item) # Удаляем некорректные записи

            
                
                
            
            
            
            
            
            
            
            
            
            
            
            
            
            


    def on_closing(self):
        if messagebox.askyesno("Выход", "Сохранить изменения перед выходом?"):
            self.save_data()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibraryApp(root)
    
    # Перехват закрытия окна для сохранения данных
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    root.mainloop()
