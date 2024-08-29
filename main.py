import telebot
from telebot import types
from dotenv import find_dotenv, load_dotenv
import os
import requests

load_dotenv(find_dotenv())

bot = telebot.TeleBot(os.getenv("TOKEN_TELEGRAM"))

def get_clothing_recommendation(temp, humidity, wind_speed, weather, clouds):
    # Определение ключей для каждого параметра
    temp_key = (
        "very_hot" if temp > 25 else
        "hot" if 20 < temp <= 25 else
        "warm" if 15 < temp <= 20 else
        "cool" if 10 < temp <= 15 else
        "cold" if 5 < temp <= 10 else
        "very_cold"
    )
    
    humidity_key = "low_humidity" if humidity <= 40 else "high_humidity"
    wind_key = "low_wind" if wind_speed <= 3 else "high_wind"
    precip_key = "no_precipitation" if weather == "Clear" and clouds == 0 else "precipitation"

    # Таблица соответствия уникальных рекомендаций
    recommendations = {
    ("very_hot", "low_humidity", "low_wind", "no_precipitation"): "Легкая одежда, футболка и шорты. (Температура: >25°C, Влажность: ≤40%, Ветер: ≤3 м/с, Осадки: нет)",
    ("very_hot", "low_humidity", "low_wind", "precipitation"): "Легкая непромокаемая куртка и шорты. (Температура: >25°C, Влажность: ≤40%, Ветер: ≤3 м/с, Осадки: есть)",
    ("very_hot", "low_humidity", "high_wind", "no_precipitation"): "Легкая одежда плюс ветровка, чтобы защититься от ветра. (Температура: >25°C, Влажность: ≤40%, Ветер: >5 м/с, Осадки: нет)",
    ("very_hot", "low_humidity", "high_wind", "precipitation"): "Легкая непромокаемая куртка и шорты. (Температура: >25°C, Влажность: ≤40%, Ветер: >5 м/с, Осадки: есть)",
    ("very_hot", "high_humidity", "low_wind", "no_precipitation"): "Легкая одежда из дышащих тканей, кепка или шляпа для защиты от солнца. (Температура: >25°C, Влажность: >60%, Ветер: ≤3 м/с, Осадки: нет)",
    ("very_hot", "high_humidity", "low_wind", "precipitation"): "Легкая непромокаемая куртка из дышащих тканей. (Температура: >25°C, Влажность: >60%, Ветер: ≤3 м/с, Осадки: есть)",
    ("very_hot", "high_humidity", "high_wind", "no_precipitation"): "Легкая одежда из дышащих тканей, ветровка. (Температура: >25°C, Влажность: >60%, Ветер: >5 м/с, Осадки: нет)",
    ("very_hot", "high_humidity", "high_wind", "precipitation"): "Легкая непромокаемая куртка из дышащих тканей, закрытая обувь. (Температура: >25°C, Влажность: >60%, Ветер: >5 м/с, Осадки: есть)",
    
    ("hot", "low_humidity", "low_wind", "no_precipitation"): "Легкая одежда, футболка и брюки или юбка. (Температура: 20-25°C, Влажность: ≤40%, Ветер: ≤3 м/с, Осадки: нет)",
    ("hot", "low_humidity", "low_wind", "precipitation"): "Непромокаемая легкая куртка, брюки. (Температура: 20-25°C, Влажность: ≤40%, Ветер: ≤3 м/с, Осадки: есть)",
    ("hot", "low_humidity", "high_wind", "no_precipitation"): "Легкая куртка или ветровка, брюки. (Температура: 20-25°C, Влажность: ≤40%, Ветер: >5 м/с, Осадки: нет)",
    ("hot", "low_humidity", "high_wind", "precipitation"): "Непромокаемая легкая куртка, брюки. (Температура: 20-25°C, Влажность: ≤40%, Ветер: >5 м/с, Осадки: есть)",
    ("hot", "high_humidity", "low_wind", "no_precipitation"): "Легкая, дышащая одежда, кроссовки или легкая обувь. (Температура: 20-25°C, Влажность: >60%, Ветер: ≤3 м/с, Осадки: нет)",
    ("hot", "high_humidity", "low_wind", "precipitation"): "Непромокаемая легкая куртка из дышащих тканей, закрытая обувь. (Температура: 20-25°C, Влажность: >60%, Ветер: ≤3 м/с, Осадки: есть)",
    ("hot", "high_humidity", "high_wind", "no_precipitation"): "Легкая куртка, дышащие ткани, закрытая обувь. (Температура: 20-25°C, Влажность: >60%, Ветер: >5 м/с, Осадки: нет)",
    ("hot", "high_humidity", "high_wind", "precipitation"): "Непромокаемая легкая куртка из дышащих тканей, закрытая обувь. (Температура: 20-25°C, Влажность: >60%, Ветер: >5 м/с, Осадки: есть)",
    
    ("warm", "low_humidity", "low_wind", "no_precipitation"): "Легкий свитер или толстовка, брюки или джинсы. (Температура: 15-20°C, Влажность: ≤40%, Ветер: ≤3 м/с, Осадки: нет)",
    ("warm", "low_humidity", "low_wind", "precipitation"): "Легкий свитер и непромокаемая куртка. (Температура: 15-20°C, Влажность: ≤40%, Ветер: ≤3 м/с, Осадки: есть)",
    ("warm", "low_humidity", "high_wind", "no_precipitation"): "Свитер плюс легкая куртка, джинсы. (Температура: 15-20°C, Влажность: ≤40%, Ветер: >5 м/с, Осадки: нет)",
    ("warm", "low_humidity", "high_wind", "precipitation"): "Легкий свитер, непромокаемая куртка. (Температура: 15-20°C, Влажность: ≤40%, Ветер: >5 м/с, Осадки: есть)",
    ("warm", "high_humidity", "low_wind", "no_precipitation"): "Легкие, дышащие ткани, свитер, кроссовки. (Температура: 15-20°C, Влажность: >60%, Ветер: ≤3 м/с, Осадки: нет)",
    ("warm", "high_humidity", "low_wind", "precipitation"): "Легкая непромокаемая куртка, дышащие ткани. (Температура: 15-20°C, Влажность: >60%, Ветер: ≤3 м/с, Осадки: есть)",
    ("warm", "high_humidity", "high_wind", "no_precipitation"): "Легкая куртка, дышащие ткани, закрытая обувь. (Температура: 15-20°C, Влажность: >60%, Ветер: >5 м/с, Осадки: нет)",
    ("warm", "high_humidity", "high_wind", "precipitation"): "Легкая непромокаемая куртка, дышащие ткани. (Температура: 15-20°C, Влажность: >60%, Ветер: >5 м/с, Осадки: есть)",
    
    ("cool", "low_humidity", "low_wind", "no_precipitation"): "Теплый свитер, куртка средней плотности, брюки. (Температура: 10-15°C, Влажность: ≤40%, Ветер: ≤3 м/с, Осадки: нет)",
    ("cool", "low_humidity", "low_wind", "precipitation"): "Плотная непромокаемая куртка, джинсы. (Температура: 10-15°C, Влажность: ≤40%, Ветер: ≤3 м/с, Осадки: есть)",
    ("cool", "low_humidity", "high_wind", "no_precipitation"): "Свитер, плотная куртка, шарф, джинсы. (Температура: 10-15°C, Влажность: ≤40%, Ветер: >5 м/с, Осадки: нет)",
    ("cool", "low_humidity", "high_wind", "precipitation"): "Плотная непромокаемая куртка, утепленные брюки. (Температура: 10-15°C, Влажность: ≤40%, Ветер: >5 м/с, Осадки: есть)",
    ("cool", "high_humidity", "low_wind", "no_precipitation"): "Дышащая одежда, утепленная куртка, закрытая обувь. (Температура: 10-15°C, Влажность: >60%, Ветер: ≤3 м/с, Осадки: нет)",
    ("cool", "high_humidity", "low_wind", "precipitation"): "Утепленная непромокаемая куртка, шарф, закрытая обувь. (Температура: 10-15°C, Влажность: >60%, Ветер: ≤3 м/с, Осадки: есть)",
    ("cool", "high_humidity", "high_wind", "no_precipitation"): "Утепленная куртка, шарф, перчатки. (Температура: 10-15°C, Влажность: >60%, Ветер: >5 м/с, Осадки: нет)",
    ("cool", "high_humidity", "high_wind", "precipitation"): "Плотная непромокаемая куртка, утепленные брюки, шарф. (Температура: 10-15°C, Влажность: >60%, Ветер: >5 м/с, Осадки: есть)",
    
    ("cold", "low_humidity", "low_wind", "no_precipitation"): "Теплая куртка, утепленные брюки, шапка, перчатки. (Температура: 0-10°C, Влажность: ≤40%, Ветер: ≤3 м/с, Осадки: нет)",
    ("cold", "low_humidity", "low_wind", "precipitation"): "Плотная непромокаемая куртка, утепленные брюки, шапка, перчатки. (Температура: 0-10°C, Влажность: ≤40%, Ветер: ≤3 м/с, Осадки: есть)",
    ("cold", "low_humidity", "high_wind", "no_precipitation"): "Теплая куртка, шарф, шапка, перчатки, утепленные брюки. (Температура: 0-10°C, Влажность: ≤40%, Ветер: >5 м/с, Осадки: нет)",
    ("cold", "low_humidity", "high_wind", "precipitation"): "Плотная непромокаемая куртка, утепленные брюки, шапка, перчатки, шарф. (Температура: 0-10°C, Влажность: ≤40%, Ветер: >5 м/с, Осадки: есть)",
    ("cold", "high_humidity", "low_wind", "no_precipitation"): "Теплая куртка, шапка, шарф, утепленная обувь. (Температура: 0-10°C, Влажность: >60%, Ветер: ≤3 м/с, Осадки: нет)",
    ("cold", "high_humidity", "low_wind", "precipitation"): "Плотная непромокаемая куртка, шапка, шарф, утепленные брюки. (Температура: 0-10°C, Влажность: >60%, Ветер: ≤3 м/с, Осадки: есть)",
    ("cold", "high_humidity", "high_wind", "no_precipitation"): "Теплая куртка, шарф, шапка, перчатки, утепленные брюки, ботинки. (Температура: 0-10°C, Влажность: >60%, Ветер: >5 м/с, Осадки: нет)",
    ("cold", "high_humidity", "high_wind", "precipitation"): "Плотная непромокаемая куртка, шапка, шарф, утепленные брюки, ботинки. (Температура: 0-10°C, Влажность: >60%, Ветер: >5 м/с, Осадки: есть)",
    
    ("very_cold", "low_humidity", "low_wind", "no_precipitation"): "Очень теплая куртка, термобелье, утепленные брюки, шапка, перчатки. (Температура: <0°C, Влажность: ≤40%, Ветер: ≤3 м/с, Осадки: нет)",
    ("very_cold", "low_humidity", "low_wind", "precipitation"): "Плотная непромокаемая куртка, термобелье, утепленные брюки, шапка, перчатки. (Температура: <0°C, Влажность: ≤40%, Ветер: ≤3 м/с, Осадки: есть)",
    ("very_cold", "low_humidity", "high_wind", "no_precipitation"): "Очень теплая куртка, шарф, шапка, перчатки, утепленные брюки, ботинки. (Температура: <0°C, Влажность: ≤40%, Ветер: >5 м/с, Осадки: нет)",
    ("very_cold", "low_humidity", "high_wind", "precipitation"): "Плотная непромокаемая куртка, термобелье, утепленные брюки, шапка, перчатки, ботинки. (Температура: <0°C, Влажность: ≤40%, Ветер: >5 м/с, Осадки: есть)",
    ("very_cold", "high_humidity", "low_wind", "no_precipitation"): "Очень теплая куртка, термобелье, утепленные брюки, шапка, перчатки, ботинки. (Температура: <0°C, Влажность: >60%, Ветер: ≤3 м/с, Осадки: нет)",
    ("very_cold", "high_humidity", "low_wind", "precipitation"): "Плотная непромокаемая куртка, термобелье, утепленные брюки, шапка, перчатки, ботинки. (Температура: <0°C, Влажность: >60%, Ветер: ≤3 м/с, Осадки: есть)",
    ("very_cold", "high_humidity", "high_wind", "no_precipitation"): "Очень теплая куртка, шарф, шапка, перчатки, термобелье, утепленные брюки, ботинки. (Температура: <0°C, Влажность: >60%, Ветер: >5 м/с, Осадки: нет)",
    ("very_cold", "high_humidity", "high_wind", "precipitation"): "Плотная непромокаемая куртка, термобелье, утепленные брюки, шапка, перчатки, ботинки. (Температура: <0°C, Влажность: >60%, Ветер: >5 м/с, Осадки: есть)"
    }

    # Получение рекомендации
    return recommendations.get((temp_key, humidity_key, wind_key, precip_key), "Неизвестные параметры")

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Да, посоветовать!", callback_data="Yes")
    markup.add(button)
    bot.send_message(message.chat.id, 'Привет, посоветовать ли вам тип одежды под вашу погоду?', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "Yes")
def yes_call(call):
    bot.answer_callback_query(call.id)
    location_user(call.message)

def location_user(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button = types.KeyboardButton("Отправить мое местоположение!", request_location=True)
    markup.add(button)
    bot.send_message(message.chat.id, "Отправьте пожалуйста свое местоположение!", reply_markup=markup)

@bot.message_handler(content_types=['location'])
def sovet(message):
    #api_key = os.getenv("TOKEN_OPENWEATHERMAP")
    api_key = '0f331e591e302f74220e17a7e99efd79'
    
    # Проверка наличия API ключа
    if not api_key:
        bot.send_message(message.chat.id, "Ошибка: API ключ не найден.")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={message.location.latitude}&lon={message.location.longitude}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            weather_data = response.json()  # Получение данных из ответа
            recomends = get_clothing_recommendation(
                weather_data['main']['temp'], 
                weather_data['main']['humidity'], 
                weather_data['wind']['speed'], 
                weather_data['weather'][0]['main'], 
                weather_data['clouds']['all']
            )
            bot.send_message(message.chat.id, f"Получены данные о погоде: {recomends}")
            bot.send_message(message.chat.id, "Чтобы снова получить рекомендацию просто отправьте данные о геопозиции")
        elif response.status_code == 401:
            bot.send_message(message.chat.id, "Ошибка 401: Неверный API ключ или проблемы с аутентификацией.")
        else:
            bot.send_message(message.chat.id, f"Не удалось получить данные. Код ошибки: {response.status_code}")
    except requests.exceptions.RequestException as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при запросе: {e}")

bot.polling()
