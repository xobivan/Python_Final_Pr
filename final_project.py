import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import chardet  # Для определения кодировки

# Функция для определения кодировки
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        rawdata = f.read()
    result = chardet.detect(rawdata)
    return result['encoding']

try:
    # Укажите путь к вашему CSV-файлу на локальной машине
    file_path = 'data__1_.csv'

    # Определение кодировки и чтение CSV файла
    detected_encoding = detect_encoding(file_path)
    
    # Пропуск строк, вызывающих ошибки при разборе
    df = pd.read_csv(file_path, encoding=detected_encoding, sep=';', on_bad_lines='skip')
    
    # Вывод первых нескольких строк DataFrame для анализа структуры данных
    print(df.head())

    # Проверка наличия столбца 'Дата создания'
    if 'Дата создания' in df.columns:
        # Преобразование столбца 'Дата создания' в datetime
        df['Дата создания'] = pd.to_datetime(df['Дата создания'], dayfirst=True, errors='coerce')

        # Удаление строк с некорректными датами
        df = df.dropna(subset=['Дата создания'])

        # Извлечение 'Date' и 'Hour' из 'Дата создания'
        df['Date'] = df['Дата создания'].dt.date
        df['Hour'] = df['Дата создания'].dt.hour

        # Создание сводной таблицы
        pivot_table = df.pivot_table(index='Hour', columns='Date', values='ЛД', aggfunc='count', fill_value=0)

        # Построение тепловой карты с помощью Seaborn
        plt.figure(figsize=(12, 8))  # Регулируем размер графика по мере необходимости
        sns.heatmap(pivot_table, annot=True, fmt="d", cmap="YlGnBu", cbar=True)
        plt.title('Количество личных дел, принятых в приёмную комиссию по часам')
        plt.xlabel('Дата')
        plt.ylabel('Час')
        plt.tight_layout()  # Обеспечивает нормальное размещение меток в пределах области графика
        plt.show()
    else:
        print("Столбец 'Дата создания' не найден в наборе данных.")
        # Вывод имен столбцов для проверки
        print("Доступные столбцы:", df.columns)

except Exception as e:
    print(f"Произошла ошибка: {e}")
    # Обработать или сгенерировать ошибку при необходимости