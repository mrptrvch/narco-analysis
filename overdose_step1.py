import requests
import pandas as pd
import json
import os

# Актуальный URL на CSV с количеством смертей от drug use disorders (overdoses) по странам и годам
# Источник: Our World in Data / IHME GBD (обновляется регулярно)
csv_url = "https://ourworldindata.org/grapher/data/variables/73477.csv"

# Скачиваем CSV
response = requests.get(csv_url)
if response.status_code == 200:
    with open("drug_overdoses_raw.csv", "wb") as f:
        f.write(response.content)
    print("CSV файл скачан успешно: drug_overdoses_raw.csv")
else:
    print(f"Ошибка скачивания: {response.status_code}")
    exit()

# Читаем CSV с помощью pandas
df = pd.read_csv("drug_overdoses_raw.csv")

# Смотрим колонки
print("\nКолонки в данных:")
print(df.columns.tolist())

# Ключевые колонки: 'entity' (страна), 'year', 'deaths_drug_use_disorders_both_sexes_all_ages_number' (количество смертей)
death_column = 'deaths_drug_use_disorders_both_sexes_all_ages_number'

if death_column not in df.columns:
    print("Колонка с количеством смертей изменилась. Проверьте CSV вручную.")
    exit()

# Переименовываем для удобства
df = df.rename(columns={
    'entity': 'Country',
    'year': 'Year',
    death_column: 'Overdose_Deaths_Count'
})

# Фильтруем только страны (убираем регионы: World, continents, income groups и т.д.)
countries = df[~df['Country'].str.contains('World|Income|Europe|Africa|Asia|Americas|Oceania|OECD', na=False, case=False)]

# Последний доступный год
latest_year = df['Year'].max()
print(f"\nПоследний год в данных: {latest_year}")

# Данные за последний год
latest_data = countries[countries['Year'] == latest_year][['Country', 'Year', 'Overdose_Deaths_Count']]

# Сортируем по убыванию и топ-50 (для полноты)
latest_data = latest_data.sort_values(by='Overdose_Deaths_Count', ascending=False).head(50)
latest_data = latest_data.reset_index(drop=True)
latest_data['Overdose_Deaths_Count'] = latest_data['Overdose_Deaths_Count'].astype(int)  # Для чистоты

# Выводим топ в консоль
print("\nТоп-50 стран по количеству смертей от передозировок/расстройств употребления наркотиков (последний год):")
print(latest_data)

# Сохраняем в JSON (за последний год)
data_to_save = latest_data.to_dict(orient='records')

with open("overdose_statistics.json", "w", encoding='utf-8') as json_file:
    json.dump(data_to_save, json_file, indent=4, ensure_ascii=False)

print("\nДанные за последний год сохранены в overdose_statistics.json")

# Полный исторический датасет по странам
full_data = countries[['Country', 'Year', 'Overdose_Deaths_Count']].copy()
full_data['Overdose_Deaths_Count'] = full_data['Overdose_Deaths_Count'].astype(int)

full_json = full_data.to_dict(orient='records')
with open("overdose_full_history.json", "w", encoding='utf-8') as f:
    json.dump(full_json, f, indent=4, ensure_ascii=False)

print("Полные исторические данные сохранены в overdose_full_history.json")
print("Готово! Теперь всё работает.")