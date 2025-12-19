# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
import requests
import pandas as pd
import matplotlib.pyplot as plt
import os


# Функция для скачивания файла
def download_file(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Файл {filename} скачан успешно.")
    else:
        print(f"Ошибка скачивания {url}. Код: {response.status_code}")


# URL-адреса ключевых Excel-файлов из UNODC World Drug Report 2025 (открытые данные)
files_to_download = {
    "prevalence_global": "https://www.unodc.org/documents/data-and-analysis/WDR_2025/Annex/1.1_Prevalence_of_drug_use_in_the_general_population_regional_and_global_estimates.xlsx",
    "prevalence_national": "https://www.unodc.org/documents/data-and-analysis/WDR_2025/Annex/1.2_Prevalence_of_drug_use_in_the_general_population_national_data.xlsx",
    "treatment": "https://www.unodc.org/documents/data-and-analysis/WDR_2025/Annex/5.1_Treatment_by_primary_drug_of_use.xlsx"
}

# Скачиваем файлы в текущую папку
for name, url in files_to_download.items():
    download_file(url, f"{name}.xlsx")

# Анализ национальных данных (пример: распространённость употребления наркотиков по странам)
if os.path.exists("prevalence_national.xlsx"):
    # Читаем Excel (предполагаем, что данные в первом листе; если структура изменится, скорректируйте sheet_name)
    df_national = pd.read_excel("prevalence_national.xlsx", sheet_name=0, engine='openpyxl')

    # Очистка и анализ (предполагаем колонки вроде 'Country', 'Drug Type', 'Prevalence (%)' — адаптируйте по реальным данным в файле)
    # Если колонок нет, откройте файл в Excel и посмотрите названия
    if 'Country' in df_national.columns and 'Annual prevalence (%)' in df_national.columns:
        # Топ-10 стран по распространённости (для примера, cannabis)
        df_cannabis = df_national[df_national['Drug Type'] == 'Cannabis']  # Фильтр по типу наркотика
        top_countries = df_cannabis.sort_values(by='Annual prevalence (%)', ascending=False).head(10)

        print("\nТоп-10 стран по распространённости употребления каннабиса:")
        print(top_countries[['Country', 'Annual prevalence (%)']])

        # Визуализация: бар-график
        plt.figure(figsize=(10, 6))
        plt.bar(top_countries['Country'], top_countries['Annual prevalence (%)'])
        plt.xlabel('Страна')
        plt.ylabel('Распространённость (%)')
        plt.title('Топ-10 стран по употреблению каннабиса')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('cannabis_top_countries.png')  # Сохраняет график как изображение
        plt.show()  # Показывает график
    else:
        print("Колонки в файле отличаются. Откройте prevalence_national.xlsx и проверьте структуру данных.")
else:
    print("Файл с национальными данными не скачан.")

# Анализ глобальных данных (пример: региональные оценки)
if os.path.exists("prevalence_global.xlsx"):
    df_global = pd.read_excel("prevalence_global.xlsx", sheet_name=0, engine='openpyxl')

    # Предполагаем колонки 'Region', 'Prevalence (%)'
    if 'Region' in df_global.columns and 'Prevalence (%)' in df_global.columns:
        average_prevalence = df_global['Prevalence (%)'].mean()
        print(f"\nСредняя глобальная распространённость употребления наркотиков: {average_prevalence:.2f}%")

        # График: пирог по регионам
        plt.figure(figsize=(8, 8))
        plt.pie(df_global['Prevalence (%)'], labels=df_global['Region'], autopct='%1.1f%%')
        plt.title('Распределение употребления наркотиков по регионам')
        plt.savefig('global_prevalence_pie.png')
        plt.show()
    else:
        print("Колонки в глобальном файле отличаются. Проверьте файл.")

# Дополнительный анализ: лечение (количество людей на лечении по типам наркотиков)
if os.path.exists("treatment.xlsx"):
    df_treatment = pd.read_excel("treatment.xlsx", sheet_name=0, engine='openpyxl')

    # Предполагаем колонки 'Drug Type', 'Number of People'
    if 'Drug Type' in df_treatment.columns and 'Number of People' in df_treatment.columns:
        treatment_summary = df_treatment.groupby('Drug Type')['Number of People'].sum()
        print("\nКоличество людей на лечении по типам наркотиков:")
        print(treatment_summary)

        # Бар-график
        treatment_summary.plot(kind='bar', figsize=(10, 6))
        plt.xlabel('Тип наркотика')
        plt.ylabel('Количество людей')
        plt.title('Лечение от наркозависимости по типам')
        plt.savefig('treatment_by_drug.png')
        plt.show()
    else:
        print("Колонки в файле лечения отличаются. Проверьте файл.")

print("\nАнализ завершён. Графики сохранены как PNG-файлы. Для более глубокого анализа откройте Excel-файлы вручную.")