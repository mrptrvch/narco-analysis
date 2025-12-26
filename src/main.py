import requests
import pandas as pd
import json

# Заголовок для обхода блокировки
headers = {'User-Agent': 'Our World In Data data fetch/1.0'}

# рабочий URL на CSV (death rates по типам передозировок)
csv_url = "https://ourworldindata.org/grapher/drug-overdose-death-rates.csv?v=1&csvType=filtered&useColumnShortNames=true&overlay=download-data"

# Скачиваем CSV
response = requests.get(csv_url, headers=headers)

if response.status_code == 200:
    with open("/Users/mac/PycharmProjects/narco-analysis/data/raw/drug_overdoses_raw.csv", "wb") as f:
        f.write(response.content)
    print("CSV файл скачан успешно: drug_overdoses_raw.csv")
else:
    print(f"Ошибка скачивания: {response.status_code}")
    print(response.text[:500])
    exit()

# Читаем CSV
df = pd.read_csv("/Users/mac/PycharmProjects/narco-analysis/data/raw/drug_overdoses_raw.csv")

# Выводим колонки (для проверки)
print("\nКолонки в данных:")
print(df.columns.tolist())

# Колонки со ставками смертности (rates per 100,000)
rate_columns = [
    'Any opioid death rates (CDC WONDER)',
    'Cocaine overdose death rates (CDC WONDER)',
    'Heroin overdose death rates (CDC WONDER)',
    'Synthetic opioids death rates (CDC WONDER)',
    'Prescription Opioids death rates (US CDC WONDER)'
]

# Проверяем наличие колонок
missing_cols = [col for col in rate_columns if col not in df.columns]
if missing_cols:
    print(f"Отсутствуют колонки: {missing_cols}")
    exit()

# Суммируем ставки для общей оценки передозировок
df['Overdose_Death_Rate_Total'] = df[rate_columns].sum(axis=1)

# Переименовываем для удобства
df = df.rename(columns={
    'Entity': 'Country',
    'Year': 'Year'
})

# Фильтруем только страны (убираем World и другие агрегаты; в этих данных в основном USA)
countries = df[~df['Country'].str.contains('World|Income|Europe|Africa|Asia|Americas|Oceania|OECD|WHO', na=False, case=False)]


# Полная история
full_data = countries[['Country', 'Year', 'Overdose_Death_Rate_Total'] + rate_columns].round(2)

full_json = full_data.to_dict(orient='records')
with open("/Users/mac/PycharmProjects/narco-analysis/data/processed/overdose_full_history_rates.json", "w", encoding='utf-8') as f:
    json.dump(full_json, f, indent=4, ensure_ascii=False)

print("Полные исторические данные сохранены в overdose_full_history_rates.json")
print("Готово! Теперь код работает с твоими колонками и суммирует ставки.")