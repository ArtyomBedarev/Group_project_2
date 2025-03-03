!pip install selenium webdriver-manager
!apt update
!apt install -y google-chrome-stable
!apt update
!apt install -y wget unzip
!wget -O /tmp/google-chrome-stable_current_amd64.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
!dpkg -i /tmp/google-chrome-stable_current_amd64.deb || apt-get -fy install
!google-chrome --version
!wget -O chromedriver-linux64.zip https://storage.googleapis.com/chrome-for-testing-public/133.0.6943.141/linux64/chromedriver-linux64.zip
!unzip chromedriver-linux64.zip
!mv chromedriver-linux64/chromedriver /usr/bin/chromedriver
!chmod +x /usr/bin/chromedriver
import time
import pandas as pd
import logging
import logging.config
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from google.colab import files


# Создаем объект Chrome и настраиваем
chrome_options = Options()
chrome_options.add_argument("--headless")  # Запускаем браузер в фоновом режиме
chrome_options.add_argument("--no-sandbox") # Отключаем sandbox
chrome_options.add_argument("--disable-dev-shm-usage")   # Отключаем использование /dev/shm
chrome_options.binary_location = "/usr/bin/google-chrome" # путь к Chrome

service = Service("/usr/bin/chromedriver")
logging.config.fileConfig('logging.conf')

# Запускаем эмулятор браузера
driver = webdriver.Chrome(service=service, options=chrome_options)
logging.info("Браузер успешно запущен")

url = "https://gg.deals/games/?page={}"

def get_page(page):
    driver.get(url.format(page))
    logging.info(f"Открыта страница {page}")
    time.sleep(2)
    games = []

    # Получаем список карточек игр
    game_cards = driver.find_elements("class name", "game-info-title")

    # Проходим по карточкам, извлекаем инфо
    for card in driver.find_elements("css selector", ".game-info-wrapper"):
        try:

            # Извлекаем название игры
            title = card.find_element("css selector", ".title-inner").text.strip()

            # Извлекаем жанр игры
            genre = card.find_element("css selector", ".genres-tag .value").text.strip()

            # Извлекаем цену игры и убираем "~" перед ценой, если она есть
            price = card.find_element("css selector", ".price-inner.numeric").text.strip().replace("~", "")
            games.append({"Название": title, "Жанр": genre, "Цена": price})
            logging.info(f"Добавлена игра: {title}")
        except:
            logging.error(f"Ошибка при обработке карточки на странице {page}: {e}")
            continue

    return games
all_games = []
max_games = 100
page = 1

while len(all_games) < max_games:
    games = get_page(page)
    all_games.extend(games) # Добавляем игры в общий список
    page += 1
driver.quit()

df = pd.DataFrame(all_games)
df.to_csv("gg_deals_games.csv")
files.download("gg_deals_games.csv")
