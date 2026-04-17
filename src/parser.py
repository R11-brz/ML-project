import requests
import pandas as pd
import time
from config import Config

def get_movies(page_number):
    url = f"{Config.BASE_URL}/discover/movie"
    my_params = {
        'api_key': Config.TMDB_API_KEY,  
        'include_adult': 'false',
        'page': page_number,                
        'language': 'en-US',
        'sort_by': 'popularity.desc' 
    }
    response = requests.get(url, params=my_params) #объект класса response
    if response.status_code == 200: #Код ответа 
        data = response.json() # Превращает JSON в словарь/список
        return data.get('results', [])
    else:
        print(f"Ошибка! Код: {response.status_code}")
        return []


def get_movie_details(movie_id):
    url = f"{Config.BASE_URL}/movie/{movie_id}"

    my_params = {
        'api_key': Config.TMDB_API_KEY,
        'language': 'en-US' 
    }

    try:
        response = requests.get(url, params=my_params)
        if response.status_code == 200:
            data = response.json()
            return {
                'budget': data.get('budget', 0),    # Бюджет
                'revenue': data.get('revenue', 0),  # Сборы
                'runtime': data.get('runtime', 0),  # Длительность в минутах
                'genres': ", ".join([g['name'] for g in data.get('genres', [])])
            }
    except Exception as e:
        print(f"Ошибка на ID {movie_id}: {e}")
    return {'budget': 0, 'revenue': 0, 'runtime': 0, 'genres': ""}

def main():
    dataset = []
    
    for p in range(201, 251):
        print(f"--- Загружаю страницу {p} из TMDB ---")
        movies_list = get_movies(p)

        for movie in movies_list:
            details = get_movie_details(movie['id'])
            full_info = {**movie, **details}
            
            # СОЗДАЕМ СЛОВАРЬ СРАЗУ В НУЖНОМ ФОРМАТЕ
            movie_for_ml = {
                # Базовые признаки
                'id': movie['id'],
                'title': movie['title'],
                'vote_average': movie['vote_average'],  # ЦЕЛЕВАЯ ПЕРЕМЕННАЯ (то, что предсказываем)
                'budget': details.get('budget', 0),
                'revenue': details.get('revenue', 0),
                'runtime': details.get('runtime', 0),
                'popularity': movie.get('popularity', 0),
                'vote_count': movie.get('vote_count', 0),
                
                # ГОД из даты (сразу преобразуем)
                'release_year': int(movie['release_date'][:4]) if movie.get('release_date') else 0,
            }
            
            # ==========================================
            # ОБРАБОТКА ЖАНРОВ - создаем флаги (1 или 0)
            # ==========================================
            genres_str = details.get('genres', '')
            if genres_str:
                genres_list = genres_str.split(', ')
                
                # Флаги для основных жанров
                movie_for_ml['is_Action'] = 1 if 'Action' in genres_list else 0
                movie_for_ml['is_Comedy'] = 1 if 'Comedy' in genres_list else 0
                movie_for_ml['is_Drama'] = 1 if 'Drama' in genres_list else 0
                movie_for_ml['is_Horror'] = 1 if 'Horror' in genres_list else 0
                movie_for_ml['is_Romance'] = 1 if 'Romance' in genres_list else 0
                movie_for_ml['is_Thriller'] = 1 if 'Thriller' in genres_list else 0
                movie_for_ml['is_SciFi'] = 1 if 'Science Fiction' in genres_list else 0
                movie_for_ml['is_Crime'] = 1 if 'Crime' in genres_list else 0
                movie_for_ml['is_Adventure'] = 1 if 'Adventure' in genres_list else 0
                movie_for_ml['is_Family'] = 1 if 'Family' in genres_list else 0
                movie_for_ml['is_Animation'] = 1 if 'Animation' in genres_list else 0
            else:
                # Если жанров нет - все флаги = 0
                movie_for_ml['is_Action'] = 0
                movie_for_ml['is_Comedy'] = 0
                movie_for_ml['is_Drama'] = 0
                movie_for_ml['is_Horror'] = 0
                movie_for_ml['is_Romance'] = 0
                movie_for_ml['is_Thriller'] = 0
                movie_for_ml['is_SciFi'] = 0
                movie_for_ml['is_Crime'] = 0
                movie_for_ml['is_Adventure'] = 0
                movie_for_ml['is_Family'] = 0
                movie_for_ml['is_Animation'] = 0
            
            # ==========================================
            # ОБРАБОТКА ЯЗЫКА - создаем флаги (1 или 0)
            # ==========================================
            lang = movie.get('original_language', 'unknown')
            movie_for_ml['lang_en'] = 1 if lang == 'en' else 0
            movie_for_ml['lang_ru'] = 1 if lang == 'ru' else 0
            movie_for_ml['lang_fr'] = 1 if lang == 'fr' else 0
            movie_for_ml['lang_es'] = 1 if lang == 'es' else 0
            movie_for_ml['lang_de'] = 1 if lang == 'de' else 0
            movie_for_ml['lang_other'] = 1 if lang not in ['en', 'ru', 'fr', 'es', 'de'] else 0
            
            # Добавляем готовый словарь в датасет
            dataset.append(movie_for_ml)
            time.sleep(0.1)

    # Превращаем список словарей в таблицу Pandas
    df = pd.DataFrame(dataset)
    
    # Сохраняем ГОТОВЫЙ файл (уже со всеми dummy-переменными)
    df.to_csv("data/movies_ready_for_ml.csv", index=False)
    
    print(f"\nГОТОВО! Загружено фильмов: {len(df)}")
    print(f"Столбцы в готовой таблице: {list(df.columns)}")
    print("\nПервые 5 строк:")
    print(df.head())
    
    return df

if __name__ == "__main__":
    df = main()