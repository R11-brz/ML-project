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
    ALLOWED_COLUMNS = ['id', 'title', 'genres', 'release_date', 'budget']
    for p in range(1, 3):
        print(f"--- Загружаю страницу {p} из TMDB ---")
        movies_list = get_movies(p)

        for movie in movies_list:
            details = get_movie_details(movie['id'])
            full_info = {**movie, **details}
            filtered_movie = {key: full_info.get(key) for key in ALLOWED_COLUMNS}
            dataset.append(filtered_movie) #Склеивание словарей
            time.sleep(0.1)

    df = pd.DataFrame(dataset) #Превращаем список словарей в таблицу Pandas

    df.to_csv("data/movies_raw.csv", index=False)

if __name__ == "__main__":
    main()

        