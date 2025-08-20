import os
import requests
import google.generativeai as genai
import random # Убедитесь, что импортировали random

# --- ВАШ СПИСОК ПРОФЕССИЙ ---
# Мы переносим его прямо в скрипт для удобства
ALL_PROFESSIONS = [
    "Директор по электронной коммерции", "Руководитель отдела по работе с маркетплейсами",
    "Менеджер по работе с маркетплейсами", "Аккаунт-менеджер маркетплейсов",
    "Контент-менеджер", "Аналитик маркетплейсов", "E-commerce аналитик",
    "Специалист по продвижению на маркетплейсах", "Менеджер по трафику",
    "Специалист по ценообразованию", "Интернет-маркетолог", "Бренд-менеджер",
    "SEO-специалист", "SMM-менеджер", "Руководитель склада", "Начальник отдела логистики",
    "Специалист по фулфилменту", "Специалист по управлению товарными запасами",
    "Кладовщик", "Сборщик заказов", "Специалист по маркировке",
    "Финансовый менеджер / Аналитик", "Бухгалтер", "Менеджер по работе с клиентами",
    "Специалист службы поддержки", "Категорийный менеджер", "Менеджер по закупкам",
    "Юрист", "Менеджер ozon", "Менеджер wildberries", "директор по маркетингу"
]
USED_PROFESSIONS_FILE = "used_professions.txt"

# --- Получаем секреты ---
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')
UNSPLASH_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
GEMINI_KEY = os.getenv('GEMINI_API_KEY')

# ... (функции generate_text_with_gemini, get_random_office_photo, send_to_telegram остаются без изменений) ...
def generate_text_with_gemini(api_key, prompt_text):
    # ... ваш код без изменений ...
def get_random_office_photo(api_key):
    # ... ваш код без изменений ...
def send_to_telegram(text, image_url, attribution=""):
    # ... ваш код без изменений ...

# --- НОВЫЕ ФУНКЦИИ ДЛЯ РАБОТЫ СО СПИСКАМИ ---
def get_used_professions():
    """Читает файл с использованными профессиями."""
    try:
        with open(USED_PROFESSIONS_FILE, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def add_profession_to_used(profession):
    """Добавляет профессию в файл использованных."""
    with open(USED_PROFESSIONS_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{profession}\n")

def clear_used_professions():
    """Очищает файл, когда все профессии использованы."""
    with open(USED_PROFESSIONS_FILE, 'w', encoding='utf-8') as f:
        f.write("")
    print("Все профессии были использованы. Начинаем цикл заново.")

# --- Основной блок выполнения (ОБНОВЛЕННЫЙ) ---
if __name__ == "__main__":
    print("Начинаю процесс публикации...")
    
    # 1. Получаем список доступных профессий
    used_professions = get_used_professions()
    available_professions = list(set(ALL_PROFESSIONS) - used_professions)

    # 2. Если доступных нет, очищаем список использованных и начинаем заново
    if not available_professions:
        clear_used_professions()
        available_professions = ALL_PROFESSIONS

    # 3. Выбираем случайную профессию из доступных
    selected_profession = random.choice(available_professions)
    print(f"Выбрана профессия: {selected_profession}")

    # 4. Читаем базовый промпт из файла
    try:
        with open("prompt.txt", 'r', encoding='utf-8') as f:
            base_prompt = f.read()
    except FileNotFoundError:
        print("Ошибка: Файл prompt.txt не найден.")
        exit(1)

    # 5. Подставляем профессию в промпт
    final_prompt = base_prompt.replace("{selected_profession}", selected_profession)
    
    # 6. Генерируем текст и получаем фото
    generated_text = generate_text_with_gemini(GEMINI_KEY, final_prompt)
    photo_url, photo_attribution = get_random_office_photo(UNSPLASH_KEY)
    
    # 7. Публикуем и обновляем лог
    if generated_text and photo_url:
        send_to_telegram(generated_text, photo_url)
        add_profession_to_used(selected_profession)
        print(f"Профессия '{selected_profession}' добавлена в список использованных.")
    else:
        print("Не удалось получить текст или фото. Публикация отменена.")
