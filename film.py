import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class MovieLibrary:
    def __init__(self, master):
        self.master = master
        master.title("Movie Library")

        # Поля ввода
        self.title_label = tk.Label(master, text="Название:")
        self.title_label.pack()
        self.title_entry = tk.Entry(master)
        self.title_entry.pack()

        self.genre_label = tk.Label(master, text="Жанр:")
        self.genre_label.pack()
        self.genre_entry = tk.Entry(master)
        self.genre_entry.pack()

        self.year_label = tk.Label(master, text="Год выпуска:")
        self.year_label.pack()
        self.year_entry = tk.Entry(master)
        self.year_entry.pack()

        self.rating_label = tk.Label(master, text="Рейтинг (0-10):")
        self.rating_label.pack()
        self.rating_entry = tk.Entry(master)
        self.rating_entry.pack()

        # Кнопка добавления фильма
        self.add_button = tk.Button(master, text="Добавить фильм", command=self.add_movie)
        self.add_button.pack()

        # Таблица для отображения фильмов
        self.tree = ttk.Treeview(master, columns=("Title", "Genre", "Year", "Rating"), show='headings')
        for col in ("Title", "Genre", "Year", "Rating"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack()

        # Фильтрация
        self.filter_label = tk.Label(master, text="Фильтровать по жанру:")
        self.filter_label.pack()
        self.filter_entry = tk.Entry(master)
        self.filter_entry.pack()
        
        self.filter_button = tk.Button(master, text="Применить фильтр", command=self.filter_movies)
        self.filter_button.pack()

        # Загрузка данных
        self.load_movies()

    def add_movie(self):
        title = self.title_entry.get()
        genre = self.genre_entry.get()
        year = self.year_entry.get()
        rating = self.rating_entry.get()

        # Проверка корректности ввода
        if not title or not genre or not year or not rating:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
            return
        
        try:
            year = int(year)
            if year < 1888:  # Первый фильм был снят в 1888 году
                raise ValueError("Год должен быть больше 1888.")
            rating = float(rating)
            if rating < 0 or rating > 10:
                raise ValueError("Рейтинг должен быть от 0 до 10.")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
            return

        movie = {"title": title, "genre": genre, "year": year, "rating": rating}
        
        # Добавление фильма в таблицу
        self.tree.insert("", "end", values=(title, genre, year, rating))
        
        # Сохранение фильма в файл
        self.save_movie(movie)

    def save_movie(self, movie):
        if os.path.exists('movies.json'):
            with open('movies.json', 'r') as f:
                movies = json.load(f)
        else:
            movies = []

        movies.append(movie)

        with open('movies.json', 'w') as f:
            json.dump(movies, f)

    def load_movies(self):
        if os.path.exists('movies.json'):
            with open('movies.json', 'r') as f:
                movies = json.load(f)
                for movie in movies:
                    self.tree.insert("", "end", values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))

    def filter_movies(self):
        genre_filter = self.filter_entry.get().lower()
        
        for item in self.tree.get_children():

            self.tree.delete(item)

        if os.path.exists('movies.json'):
            with open('movies.json', 'r') as f:
                movies = json.load(f)
                for movie in movies:
                    if genre_filter in movie["genre"].lower():
                        self.tree.insert("", "end", values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()
