import sqlite3


class NetflixDAO:
    """Объекты класса создаются с указанием пути до БД"""

    def __init__(self, path):
        self.path = path

    """Функция на создание подключения"""

    def load_data(self):
        with sqlite3.connect(self.path) as connection:
            cursor = connection.cursor()
        return cursor

    """Функция поиска по БД Нужного фильма по названию (title в БД)"""

    def get_movie_by_title(self, m_title):
        cursor = self.load_data()
        query = """
                SELECT title, country, release_year, listed_in, description
                FROM netflix
                WHERE `title` LIKE :sub_title COLLATE NOCASE
                AND netflix.type = 'Movie'
                ORDER BY release_year DESC
                LIMIT 1
        """
        cursor.execute(query, {"sub_title": f"%{m_title}%"})
        result = cursor.fetchall()

        movie_by_title = {
            "title": result[0][0],
            "country": result[0][1],
            "release_year": result[0][2],
            "genre": result[0][3],
            "description": result[0][3]
        }
        return movie_by_title

    """функция получает все фильмы от и до двух указанных годов, выводит 100 самых свежих"""

    def get_movies_by_years(self, year_from, year_to):
        cursor = self.load_data()
        query = """
                SELECT title, release_year
                FROM netflix
                WHERE release_year BETWEEN :year_from AND :year_to
                AND `type` = 'Movie'
                ORDER BY release_year DESC
                LIMIT 100
        """
        cursor.execute(query, {"year_from": f"{year_from}", "year_to": f"{year_to}"})
        result = cursor.fetchall()

        movies_by_years = []

        for movie in result:
            d = {"title": movie[0], "release_year": movie[1]}
            movies_by_years.append(d)

        return movies_by_years

    """Функция возвращает список 100 самых свежих фильмов по рейтингу"""

    def get_movies_by_rating(self, category):

        categories = {
            "children": ("G"),
            "family": ("G", "PG", "PG-13"),
            "adult": ("R", "NC-17")
        }

        cursor = self.load_data()
        query = f"""
                SELECT title, rating, description
                FROM netflix
                WHERE rating IN {categories[category]}
                AND `type` = 'Movie'
                ORDER BY release_year DESC
                LIMIT 100
        """
        cursor.execute(query)
        result = cursor.fetchall()
        movies_by_rating = []
        for movie in result:
            d = {"title": movie[0], "rating": movie[1], "description": movie[2]}
            movies_by_rating.append(d)

        return movies_by_rating


    """Функция возвращает список 100 самых свежих фильмов по жанру"""

    def get_movies_by_genre(self, genre):
        cursor = self.load_data()
        query = """
                SELECT title, description
                FROM netflix
                WHERE listed_in LIKE :genre COLLATE NOCASE
                AND `type` = 'Movie'
                ORDER BY release_year DESC
                LIMIT 10
        """
        cursor.execute(query, {"genre": f"%{genre}%"})
        result = cursor.fetchall()

        movies_by_genre = []
        for movie in result:
            d = {"title": movie[0], "description": movie[1]}
            movies_by_genre.append(d)

        return movies_by_genre

    """
    Функция получает имена двух актеров, сохраняет всех актеров из колонки cast 
    и возвращает список тех, кто играет с ними в паре больше 2 раз
    """

    def get_actors_seen_twice(self, actor_1, actor_2):
        cursor = self.load_data()
        query = """
                SELECT `cast`
                FROM netflix
                WHERE `cast` LIKE :actor_1 COLLATE NOCASE
                AND `cast` LIKE :actor_2 COLLATE NOCASE
        """
        cursor.execute(query, {"actor_1": f'%{actor_1}%', "actor_2": f'%{actor_2}%'})
        result = cursor.fetchall()

        actors_all = []

        # Собираем полный список всех актеров
        for movie in result:
            actors = movie[0].split(", ")
            actors_all.extend(actors)

        # Оставляем тех, кто встречается дважды
        actors_seen_twice = {actor for actor in actors_all if actors_all.count(actor) > 2} - {actor_1, actor_2}

        return actors_seen_twice

    """Функция получает на выходе список названий картин с их описаниями по типу, году выпуска и жанру"""

    def get_movies_by_type_year_genre(self, m_type, m_release_year, m_genre):
        cursor = self.load_data()
        query = """
                SELECT title, description 
                FROM netflix
                WHERE `type` LIKE :m_type
                AND release_year LIKE :m_release_year
                AND listed_in LIKE :m_genre
        """
        cursor.execute(query, {"m_type": f"{m_type}",
                               "m_release_year": f"%{m_release_year}%",
                               "m_genre": f"%{m_genre}%"
                               })
        result = cursor.fetchall()

        return result
