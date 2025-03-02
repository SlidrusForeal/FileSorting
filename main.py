import os
import shutil
import logging
import json
from concurrent.futures import ThreadPoolExecutor

# Настройка логирования
logging.basicConfig(
    filename="file_sorting.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Пути
DOWNLOADS_DIR = r"D:\downloads"
TARGET_DIR = os.path.join(DOWNLOADS_DIR, "..", "download-sorting")
CONFIG_FILE = "extensions.json"


# Загружаем конфигурацию расширений из JSON
def load_extensions():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {
        "Картинки": [".jpg", ".png", ".jpeg", ".gif"],
        "Видео": [".mp4", ".mkv"],
        "Музыка": [".mp3", ".wav"],
        "Архивы": [".zip", ".tgz", ".rar", ".tar"],
        "Документы": [".pdf", ".docx", ".csv", ".xlsx", ".pptx", ".doc", ".ppt", ".xls"],
        "Установка": [".msi", ".exe"],
        "Программы": [".py", ".c", ".cpp", ".php", ".C", ".CPP"],
        "Дизайн": [".xd", ".psd"],
        "Другое": []
    }


EXTENSIONS = load_extensions()


# Определяем категорию файла
def get_category(file_name):
    for category, exts in EXTENSIONS.items():
        if any(file_name.lower().endswith(ext) for ext in exts):
            return category
    return "Другое"


# Проверяем, существует ли папка назначения
def ensure_directory(path):
    os.makedirs(path, exist_ok=True)


# Обрабатываем ситуацию, когда файл уже существует
def get_unique_filename(dest_folder, file_name):
    base, ext = os.path.splitext(file_name)
    counter = 1
    new_file = file_name

    while os.path.exists(os.path.join(dest_folder, new_file)):
        new_file = f"{base}_{counter}{ext}"
        counter += 1

    return new_file


# Перемещаем файл
def move_file(file):
    file_path = os.path.join(DOWNLOADS_DIR, file)

    if not os.path.isfile(file_path):
        return

    category = get_category(file)
    dest_folder = os.path.join(TARGET_DIR, category)
    ensure_directory(dest_folder)

    unique_file_name = get_unique_filename(dest_folder, file)

    try:
        shutil.move(file_path, os.path.join(dest_folder, unique_file_name))
        logging.info(f"Перемещен: {file} → {category}")
        print(f"✅ {file} → {category}")
    except Exception as e:
        logging.error(f"Ошибка при перемещении {file}: {e}")
        print(f"❌ Ошибка: {file}")


# Главная функция
def main():
    os.chdir(DOWNLOADS_DIR)
    files = os.listdir()

    # Используем потоки для ускорения сортировки
    with ThreadPoolExecutor() as executor:
        executor.map(move_file, files)


if __name__ == "__main__":
    main()
