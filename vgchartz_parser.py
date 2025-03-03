import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
import logging
import logging.config

logging.config.fileConfig('logging.conf')

url = "https://www.vgchartz.com/games/games.php"
page = requests.get(url)
page

URL = "https://www.vgchartz.com/games/games.php"
PARAMS = {

    "showtotalsales": 1, "showpublisher": 1, "showreleasedate": 1, "showshipped": 1 # 1. продажи игр, #2. издатель игры, #3. дата выхода игры, #4. отправленные игры
} # указываем параметры для запроса, т.е какие данные будут отображаться

# функция которая позволяет получать данные с 1 страницы
def get_page(page):
    params = PARAMS.copy() # забираем словарь прописанных параметров
    params["page"] = page # добавляем номер страницы в параметры запроса
    logging.info(f"Загружаем страницу {page}")
    response = requests.get(URL, params=params) # гет запрос с параметрами
    soup = BeautifulSoup(response.content, 'html') # с помощью beautifulsoup парсим html код
    try:
      
        games = [
            {
                "Название": row.find_all("td")[2].find("a").text.strip(), # Берем название игры
                "Издатель": row.find_all("td")[4].text.strip(), #Берем издателя игры
                "Продажи (млн)": row.find_all("td")[5].text.strip(), # Берем продажи игр
                "Дата выхода": row.find_all("td")[7].text.strip() # Берем дату выхода игры
            }
            for row in soup.find_all("tr")
            if row.get("style") and "height:70px" in row["style"]
        ] # перебираем все строки где есть tr и потом оставляем только строки с играми

        for game in games:
            logging.info(f"Добавлена игра: {game['Название']}") # Логирование выводит название добавленной игры

        return games # возвращает список игр с новой добавленной игрой  

    except Exception as e: 
        logging.error(f"Ошибка на странице {page}: {e}") 
        return []

all_games = [] #создаем пустой список где будем хранить данные
page = 1
while len(all_games) < 60000:
    games = get_page(page)
    all_games.extend(games)
    page += 1

df = pd.DataFrame(all_games)
df.to_csv("vgchartz_games.csv")
