# Описание проекта

## Команда
- Чубукин Кирилл Андреевич
- Хайруллин Дамир Ильнурович
- Бедарев Артем Сергеевич
- Шорин Матвей Юрьевич
- Амельченко Валерий Владимирович
- Гончаров Максим Александрович

## Описание проекта
Проект направлен на сбор, обработку и анализ данных о видеоиграх. Используются методы веб-скрапинга и API-интеграции. Источниками данных являются два веб-сайта и один API:
- **gg.deals** – агрегатор скидок и цен на видеоигры.
- **vgchartz** – источник информации о продажах, издателях и датах выхода игр.
- **RAWG.io API** – предоставляет рейтинги, теги, описание и другие характеристики игр.

## Заказчик
Наш заказчик – молодая игровая студия, планирующая выпускать видеоигры. Перед запуском своего первого проекта студия хочет понять, какие факторы влияют на успешность игр. Им важно знать, какие жанры наиболее прибыльны, какие ценовые стратегии работают лучше, какие издатели добиваются наибольших продаж и что влияет на популярность игры. Полученные данные и анализ помогут студии сформировать стратегию по разработке и продвижению игр, минимизировать риски и увеличить вероятность коммерческого успеха.

## Цель проекта
Создать интегрированную базу данных видеоигр и провести анализ данных (EDA) для выявления ключевых факторов, влияющих на продажи, популярность и рейтинг игр. 

**Целевая переменная**: продажи видеоигр (в миллионах копий).

## Источники и структура данных

### Обработка данных

После выполнения парсинга было получено:
- **gg.deals** – 140 047 записей.
- **vgchartz** – 60 000 записей.

После объединения двух датасетов по названию игры и добавления данных из **RAWG.io API** итоговый датасет содержит **1 161 запись**.

### Работа с пропущенными значениями и дубликатами
- В исходных данных были пропущенные значения, включая цены (426), продажи (55 472), возрастной рейтинг (562) и другие характеристики.
- После объединения в merged_df пропуски обрабатывались с помощью метода `dropna()`, то есть **все строки с пропущенными значениями были удалены**.

### Данные из gg.deals:
- **Название** – название игры (2 пропущенных значения).
- **Жанр** – жанровая принадлежность (без пропусков).
- **Цена** – текущая цена игры (426 пропущенных значений).

### Данные из vgchartz:
- **Название** – название игры (без пропусков).
- **Издатель** – издатель игры (без пропусков).
- **Продажи (млн)** – количество проданных копий (55 472 пропущенных значения).
- **Дата выхода** – дата выхода игры (3 282 пропущенных значения).

### Данные из RAWG.io API (итоговый датасет):
- **Рейтинг** – средний рейтинг игры (115 пропущенных значений).
- **Оценок** – количество отзывов (115 пропущенных значений).
- **Описание** – краткое описание игры (122 пропущенных значений).
- **Издатели** – список издателей (122 пропущенных значений).
- **Возрастной рейтинг** – возрастное ограничение (562 пропущенных значений).
- **Разработчики** – студии-разработчики (124 пропущенных значения).
- **Теги** – ключевые теги, характеризующие игру (128 пропущенных значений).
- **Популярность** – показатель популярности (115 пропущенных значений).
- **Платформы** – список платформ, на которых доступна игра (115 пропущенных значений).
- **Магазины** – платформы, на которых можно купить игру (143 пропущенных значения).
- **Размер Команды** – оценка команды разработчиков (115 пропущенных значений).

**Вывод:** 
На этапе объединения данных значительное количество строк с пропущенными значениями было удалено. Итоговый датасет содержит **1 161 запись** без пропусков, что позволяет проводить анализ без дополнительной обработки данных.

## Exploratory Data Analysis (EDA)
- Анализ распределений продаж, цен, рейтингов.
- Выявление корреляций между факторами.
- Визуализация данных (гистограммы, boxplot, heatmap).

## Используемые технологии
- **Сбор данных**: Requests, BeautifulSoup, Selenium, API.
- **Обработка**: Pandas, NumPy.
- **Анализ и визуализация**: Seaborn, Matplotlib.
- **Версионирование**: GitHub.
- **Логирование**: Logging.

## Репозиторий
Репозиторий содержит полный код проекта, датасеты, визуализации и отчет.


