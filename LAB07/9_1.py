import csv
from collections import defaultdict

def read_csv_file(filename):
    """чтение csv файла с разделителем ';'"""
    movies = []
    with open(filename, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file, delimiter=';')
        for row in csv_reader:
            # преобразуем числовые поля
            row['Year'] = int(row['Year'])
            row['Rating'] = float(row['Rating'])
            row['Duration'] = int(row['Duration'])
            row['Box_Office'] = int(row['Box_Office'])
            movies.append(row)
    return movies

def print_movies_as_key_value(movies):
    """вывод фильмов в формате 'ключ → значение'"""
    print("=" * 60)
    print("содержимое файла 9.csv:")
    print("=" * 60)
    
    for i, movie in enumerate(movies, 1):
        print(f"\nфильм #{i}:")
        for key, value in movie.items():
            print(f"  {key} → {value}")

def find_min_max_duration(movies):
    """нахождение самого короткого и самого длинного фильма"""
    min_movie = min(movies, key=lambda x: x['Duration'])
    max_movie = max(movies, key=lambda x: x['Duration'])
    return min_movie, max_movie

def calculate_high_rating_revenue(movies):
    """подсчет общих кассовых сборов для фильмов с рейтингом выше 8.0"""
    total_revenue = 0
    high_rated_movies = []
    
    for movie in movies:
        if movie['Rating'] > 8.0:
            total_revenue += movie['Box_Office']
            high_rated_movies.append(movie['Title'])
    
    return total_revenue, high_rated_movies

def calculate_avg_drama_rating(movies):
    """вычисление среднего рейтинга для жанра 'drama'"""
    drama_ratings = []
    
    for movie in movies:
        if movie['Genre'].lower() == 'drama':
            drama_ratings.append(movie['Rating'])
    
    if not drama_ratings:
        return 0, 0
    
    avg_rating = sum(drama_ratings) / len(drama_ratings)
    return avg_rating, len(drama_ratings)

def count_movies_by_genre(movies):
    """подсчет количества фильмов по жанрам"""
    genre_count = defaultdict(int)
    
    for movie in movies:
        genre = movie['Genre']
        genre_count[genre] += 1
    
    return dict(genre_count)

def analyze_movies():
    """основная функция анализа фильмов"""
    # читаем данные из файла
    movies = read_csv_file('9.csv')
    
    # 1. вывод содержимого
    print_movies_as_key_value(movies)
    
    # 2. анализ данных
    print("\n" + "=" * 60)
    print("анализ данных о фильмах:")
    print("=" * 60)
    
    # а) самый короткий и самый длинный фильм
    min_movie, max_movie = find_min_max_duration(movies)
    
    print(f"\n1. самый короткий фильм:")
    print(f"   название: {min_movie['Title']}")
    print(f"   продолжительность: {min_movie['Duration']} мин")
    print(f"   жанр: {min_movie['Genre']}")
    
    print(f"\n2. самый длинный фильм:")
    print(f"   название: {max_movie['Title']}")
    print(f"   продолжительность: {max_movie['Duration']} мин")
    print(f"   жанр: {max_movie['Genre']}")
    
    # б) общие кассовые сборы для фильмов с рейтингом > 8.0
    total_revenue, high_rated_movies = calculate_high_rating_revenue(movies)
    
    print(f"\n3. фильмы с рейтингом выше 8.0:")
    print(f"   количество: {len(high_rated_movies)}")
    print(f"   общие кассовые сборы: ${total_revenue:,}")
    
    # в) средний рейтинг для жанра "drama"
    avg_drama_rating, drama_count = calculate_avg_drama_rating(movies)
    
    print(f"\n4. жанр 'drama':")
    print(f"   количество фильмов: {drama_count}")
    print(f"   средний рейтинг: {avg_drama_rating:.2f}")
    
    # г) количество фильмов по жанрам
    genre_stats = count_movies_by_genre(movies)
    
    print(f"\n5. распределение фильмов по жанрам:")
    for genre, count in sorted(genre_stats.items()):
        print(f"   {genre}: {count} фильм(ов)")
    
    print("\n" + "=" * 60)
    print("анализ завершен!")
    print("=" * 60)

# если файл запущен напрямую
if __name__ == "__main__":
    analyze_movies()