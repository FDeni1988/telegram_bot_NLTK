import random
import nltk
import telebot
from dotenv import load_dotenv
import os

# Обязательно выполните эту команду, чтобы NLTK мог работать с токенизацией
nltk.download('popular')

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
load_dotenv()
TOKEN = os.getenv('API_KEY')
bot = telebot.TeleBot(TOKEN)

# Пример JSON структуры
intent_data = {
    "intents": {
        "hello": {
            "examples": ["Привет", "Здравствуйте", "Хай"],
            "responses": ["Прив", "Хеллоу", "Как жизнь?"]
        },
        "bye": {
            "examples": ["Пока", "До свидания", "Увидимся"],
            "responses": ["Чао", "Будь здоров", "Сайонара"]
        },
        "yandex_search": {
            "examples": ["Как пользоваться Яндекс Поиском?", "Что такое Яндекс Поиск?", "Поиск в Яндексе"],
            "responses": [
                "Яндекс Поиск - это поисковая система, которая помогает находить информацию в интернете.",
                "Воспользуйтесь Яндекс Поиском для поиска информации в сети.",
                "Введите запрос в строку поиска Яндекса и получите результаты."
            ]
        },
        "yandex_maps": {
            "examples": ["Как пользоваться Яндекс Картами?", "Что такое Яндекс Карты?", "Маршруты на Яндекс Картах"],
            "responses": [
                "Яндекс Карты помогут вам найти маршруты и адреса.",
                "Используйте Яндекс Карты для навигации и поиска мест.",
                "С помощью Яндекс Карт можно строить маршруты и просматривать пробки."
            ]
        },
        "yandex_mail": {
            "examples": ["Как создать ящик на Яндекс Почте?", "Что такое Яндекс Почта?", "Настройки Яндекс Почты"],
            "responses": [
                "Яндекс Почта- это сервис для отправки и получения электронных писем.",
                "Создайте ящик на Яндекс Почте, чтобы пользоваться почтовыми услугами.",
                "Настройте параметры ящика в Яндекс Почте для удобства использования."
            ]
        },
        "yandex_music": {
            "examples": ["Как слушать музыку на Яндекс Музыке?", "Что такое Яндекс Музыка?", "Подписка на Яндекс Музыку"],
            "responses": [
                "Яндекс Музыка предлагает доступ к огромной библиотеке треков.",
                "Слушайте любимые треки и создавайте плейлисты на Яндекс Музыке.",
                "Оформите подписку на Яндекс Музыку для доступа ко всем функциям."
            ]
        }
    },
    "default_answers": [
        "Извините я тупой",
        "Переформулируйте Ваш вопрос",
        "Я этого еще не знаю"
    ]
}

def cleaner(text):
    """Функция очистки текста."""
    cleaned_text = ''
    for ch in text.lower():
        if ch in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя ':
            cleaned_text += ch
    return cleaned_text

def match(text, example):
    """Гибкая функция сравнения текста."""
    return nltk.edit_distance(text, example) / len(example) < 0.4

def get_intent(text):
    cleaned_text = cleaner(text)
    for intent, data in intent_data["intents"].items():
        for example in data["examples"]:
            cleaned_example = cleaner(example)
            if match(cleaned_text, cleaned_example):
                return intent
    return None

@bot.message_handler(func=lambda message: True)
def respond_to_messages(message):
    # Определяем намерение
    intent = get_intent(message.text)

    if intent:
        responses = intent_data["intents"][intent]["responses"]
        response = random.choice(responses)
    else:
        response = random.choice(intent_data["default_answers"])
    bot.reply_to(message, response)


if __name__ != "__main__":
    pass
else:
    bot.polling()
