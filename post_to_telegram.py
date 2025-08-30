import os
import requests
import google.generativeai as genai
import random

# --- ВАШ СПИСОК ПРОФЕССИЙ ---
ALL_PROFESSIONS = [
    "Директор по электронной коммерции", "Руководитель отдела по работе с маркетплейсами",
    "Менеджер по работе с маркетплейсами", "Аккаунт-менеджер маркетплейсов","Фронтенд-разработчик React", "Бэкенд-разработчик Python",
    "Бэкенд-разработчик Golang", "Фулл-стек разработчик", "Мобильный разработчик (iOS, Android, React Native, Flutter)",
    "DevOps Engineer", "UI/UX дизайнер", "Product Manager",
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

# --- Получаем секреты из переменных окружения GitHub ---
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')
UNSPLASH_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
GEMINI_KEY = os.getenv('GEMINI_API_KEY')

# --- Функция для генерации текста с помощью Gemini ---
def generate_text_with_gemini(api_key, prompt_text):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt_text)
        return response.text.strip()
    except Exception as e:
        print(f"Ошибка при генерации текста через Gemini API: {e}")
        return None

# --- Функция для получения случайного фото с Unsplash ---
def get_random_office_photo(api_key):
    url = "https://api.unsplash.com/photos/random"
    params = {
        "client_id": api_key,
        "query": "office, business, workplace, team, meeting",
        "orientation": "landscape"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        image_url = data['urls']['regular']
        print(f"Найдено фото от {data['user']['name']}.")
        # Возвращаем пустую строку для атрибуции, как вы просили ранее
        return image_url, ""
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к Unsplash API: {e}")
        return None, None

# --- Функция для отправки поста в Telegram ---
def send_to_telegram(text, image_url, attribution=""):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    payload = {"chat_id": CHANNEL_ID, "photo": image_url, "caption": text, "parse_mode": "HTML"}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("Пост успешно отправлен в Telegram!")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке в Telegram: {e}")
        print(f"Ответ от сервера: {response.text}")

# --- Функции для работы со списками профессий ---
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

# --- Основной блок выполнения ---
if __name__ == "__main__":
    print("Начинаю процесс публикации...")
    
    used_professions = get_used_professions()
    available_professions = list(set(ALL_PROFESSIONS) - used_professions)

    if not available_professions:
        clear_used_professions()
        available_professions = ALL_PROFESSIONS

    selected_profession = random.choice(available_professions)
    print(f"Выбрана профессия: {selected_profession}")

    try:
        with open("prompt.txt", 'r', encoding='utf-8') as f:
            base_prompt = f.read()
    except FileNotFoundError:
        print("Ошибка: Файл prompt.txt не найден.")
        exit(1)

    final_prompt = base_prompt.replace("{selected_profession}", selected_profession)
    
    generated_text = generate_text_with_gemini(GEMINI_KEY, final_prompt)
    photo_url, photo_attribution = get_random_office_photo(UNSPLASH_KEY)
    
    if generated_text and photo_url:
        send_to_telegram(generated_text, photo_url)
        add_profession_to_used(selected_profession)
        print(f"Профессия '{selected_profession}' добавлена в список использованных.")
    else:
        print("Не удалось получить текст или фото. Публикация отменена.")
