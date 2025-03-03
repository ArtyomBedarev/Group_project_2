import requests
import pandas as pd
import time
import logging


API_KEY = "de7303c846394ab1bb72f7465b697dd8"
URL = "https://api.rawg.io/api"

inp = "pars_games_unique.csv"
df_original = pd.read_csv(inp)
games_names = df_original["Название"].tolist()

logging.config.fileConfig('logging.conf')

def get_json(url):
    response = requests.get(url)
    logging.info(f"Запрос: {url} | Статус-код: {response.status_code}")
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Ошибка при запросе {url}: статус {response.status_code}")
        return {}

# 1) /stores
stores_url = f"{URL}/stores?key={API_KEY}"
stores_data = get_json(stores_url)
stores_results = stores_data.get("results", [])
store_dict = {store["id"]: store["name"] for store in stores_results}

games_info = []

for name in games_names:
    logging.info(f"Обработка игры: {name}")

    #2) /games?search=...
    search_url = f"{URL}/games?key={API_KEY}&search={name}"
    search_data = get_json(search_url)
    results = search_data.get("results", [])
    if not results:
        logging.warning(f"Игра '{name}' не найдена!")
        continue

    game = results[0]
    game_id = game["id"]
    logging.info(f"Выбрана игра: {game.get('name')} (ID: {game_id})")

    #3) /games/{id}
    detail_url = f"{URL}/games/{game_id}?key={API_KEY}"
    detail_data = get_json(detail_url)

    game_title    = detail_data.get("name", name)
    released      = detail_data.get("released")
    rating        = detail_data.get("rating")
    playtime      = detail_data.get("playtime")
    metacritic    = detail_data.get("metacritic")
    ratings_count = detail_data.get("ratings_count")
    description   = detail_data.get("description_raw", "")[:150]
    publishers    = ", ".join(pub["name"] for pub in detail_data.get("publishers", []))
    developers    = ", ".join(dev["name"] for dev in detail_data.get("developers", []))
    esrb_rating   = detail_data.get("esrb_rating", {}).get("name") if detail_data.get("esrb_rating") else None
    tags          = ", ".join(tag["name"] for tag in detail_data.get("tags", []))
    added         = detail_data.get("added")
    platforms_list = detail_data.get("platforms", [])
    platform_names = [p.get("platform", {}).get("name") for p in platforms_list if p.get("platform", {}).get("name")]

    #4) /games/{id}/achievements
    achievements_url = f"{URL}/games/{game_id}/achievements?key={API_KEY}"
    achievements_data = get_json(achievements_url)
    achievements_count = achievements_data.get("count", 0)

    #5) /games/{id}/stores
    stores_url = f"{URL}/games/{game_id}/stores?key={API_KEY}"
    stores_data = get_json(stores_url)
    stores_results = stores_data.get("results", [])
    store_names = [store_dict[s.get("store_id")] for s in stores_results]]

    #6) /games/{id}/development-team
    dev_team_url = f"{URL}/games/{game_id}/development-team?key={API_KEY}"
    dev_team_data = get_json(dev_team_url)
    dev_team_results = dev_team_data.get("results", [])
    dev_team_count = len(dev_team_results)

    game_info = {
        "ID": game_id,
        "Название": game_title,
        "Дата выхода": released,
        "Рейтинг": rating,
        "Playtime": playtime,
        "Metacritic": metacritic,
        "Оценок": ratings_count,
        "Описание": description,
        "Издатели": publishers,
        "Возрастной рейтинг (ESRB)": esrb_rating,
        "Разработчики": developers,
        "Теги": tags,
        "Популярность (added)": added,
        "Достижения (кол-во)": achievements_count,
        "Платформы": ", ".join(platform_names),
        "Магазины": ", ".join(store_names),
        "Команда разработчиков (кол-во)": dev_team_count
    }

    games_info.append(game_info)

    time.sleep(0.3)


df_api = pd.DataFrame(games_info)
df_merged = pd.merge(df_original, df_api, on="Название", how="left")
df_merged.replace(0, pd.NA, inplace=True)

out_df = "df_itog.csv"
df_merged.to_csv(out_df)
