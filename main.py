import telebot
from telebot import types
from dotenv import find_dotenv, load_dotenv
import os
import requests

load_dotenv(find_dotenv())

bot = telebot.TeleBot(os.getenv("TOKEN_TELEGRAM"))

def get_clothing_recommendation(temp, humidity, wind_speed, weather, clouds):

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

    recommendations = {
    ("very_hot", "low_humidity", "low_wind", "no_precipitation"): "Light clothing, t-shirt, and shorts. (Temperature: >25°C, Humidity: ≤40%, Wind: ≤3 m/s, Precipitation: none)",
    ("very_hot", "low_humidity", "low_wind", "precipitation"): "Light waterproof jacket and shorts. (Temperature: >25°C, Humidity: ≤40%, Wind: ≤3 m/s, Precipitation: yes)",
    ("very_hot", "low_humidity", "high_wind", "no_precipitation"): "Light clothing plus a windbreaker to protect against the wind. (Temperature: >25°C, Humidity: ≤40%, Wind: >5 m/s, Precipitation: none)",
    ("very_hot", "low_humidity", "high_wind", "precipitation"): "Light waterproof jacket and shorts. (Temperature: >25°C, Humidity: ≤40%, Wind: >5 m/s, Precipitation: yes)",
    ("very_hot", "high_humidity", "low_wind", "no_precipitation"): "Light, breathable fabrics, cap or hat for sun protection. (Temperature: >25°C, Humidity: >60%, Wind: ≤3 m/s, Precipitation: none)",
    ("very_hot", "high_humidity", "low_wind", "precipitation"): "Light waterproof jacket made of breathable fabrics. (Temperature: >25°C, Humidity: >60%, Wind: ≤3 m/s, Precipitation: yes)",
    ("very_hot", "high_humidity", "high_wind", "no_precipitation"): "Light, breathable fabrics, windbreaker. (Temperature: >25°C, Humidity: >60%, Wind: >5 m/s, Precipitation: none)",
    ("very_hot", "high_humidity", "high_wind", "precipitation"): "Light waterproof jacket made of breathable fabrics, closed shoes. (Temperature: >25°C, Humidity: >60%, Wind: >5 m/s, Precipitation: yes)",
    
    ("hot", "low_humidity", "low_wind", "no_precipitation"): "Light clothing, t-shirt, and pants or skirt. (Temperature: 20-25°C, Humidity: ≤40%, Wind: ≤3 m/s, Precipitation: none)",
    ("hot", "low_humidity", "low_wind", "precipitation"): "Light waterproof jacket, pants. (Temperature: 20-25°C, Humidity: ≤40%, Wind: ≤3 m/s, Precipitation: yes)",
    ("hot", "low_humidity", "high_wind", "no_precipitation"): "Light jacket or windbreaker, pants. (Temperature: 20-25°C, Humidity: ≤40%, Wind: >5 m/s, Precipitation: none)",
    ("hot", "low_humidity", "high_wind", "precipitation"): "Light waterproof jacket, pants. (Temperature: 20-25°C, Humidity: ≤40%, Wind: >5 m/s, Precipitation: yes)",
    ("hot", "high_humidity", "low_wind", "no_precipitation"): "Light, breathable clothing, sneakers, or light shoes. (Temperature: 20-25°C, Humidity: >60%, Wind: ≤3 m/s, Precipitation: none)",
    ("hot", "high_humidity", "low_wind", "precipitation"): "Light waterproof jacket made of breathable fabrics, closed shoes. (Temperature: 20-25°C, Humidity: >60%, Wind: ≤3 m/s, Precipitation: yes)",
    ("hot", "high_humidity", "high_wind", "no_precipitation"): "Light jacket, breathable fabrics, closed shoes. (Temperature: 20-25°C, Humidity: >60%, Wind: >5 m/s, Precipitation: none)",
    ("hot", "high_humidity", "high_wind", "precipitation"): "Light waterproof jacket made of breathable fabrics, closed shoes. (Temperature: 20-25°C, Humidity: >60%, Wind: >5 m/s, Precipitation: yes)",
    
    ("warm", "low_humidity", "low_wind", "no_precipitation"): "Light sweater or hoodie, pants, or jeans. (Temperature: 15-20°C, Humidity: ≤40%, Wind: ≤3 m/s, Precipitation: none)",
    ("warm", "low_humidity", "low_wind", "precipitation"): "Light sweater and waterproof jacket. (Temperature: 15-20°C, Humidity: ≤40%, Wind: ≤3 m/s, Precipitation: yes)",
    ("warm", "low_humidity", "high_wind", "no_precipitation"): "Sweater plus light jacket, jeans. (Temperature: 15-20°C, Humidity: ≤40%, Wind: >5 m/s, Precipitation: none)",
    ("warm", "low_humidity", "high_wind", "precipitation"): "Light sweater, waterproof jacket. (Temperature: 15-20°C, Humidity: ≤40%, Wind: >5 m/s, Precipitation: yes)",
    ("warm", "high_humidity", "low_wind", "no_precipitation"): "Light, breathable fabrics, sweater, sneakers. (Temperature: 15-20°C, Humidity: >60%, Wind: ≤3 m/s, Precipitation: none)",
    ("warm", "high_humidity", "low_wind", "precipitation"): "Light waterproof jacket, breathable fabrics. (Temperature: 15-20°C, Humidity: >60%, Wind: ≤3 m/s, Precipitation: yes)",
    ("warm", "high_humidity", "high_wind", "no_precipitation"): "Light jacket, breathable fabrics, closed shoes. (Temperature: 15-20°C, Humidity: >60%, Wind: >5 m/s, Precipitation: none)",
    ("warm", "high_humidity", "high_wind", "precipitation"): "Light waterproof jacket, breathable fabrics. (Temperature: 15-20°C, Humidity: >60%, Wind: >5 m/s, Precipitation: yes)",
    
    ("cool", "low_humidity", "low_wind", "no_precipitation"): "Warm sweater, medium-density jacket, pants. (Temperature: 10-15°C, Humidity: ≤40%, Wind: ≤3 m/s, Precipitation: none)",
    ("cool", "low_humidity", "low_wind", "precipitation"): "Thick waterproof jacket, jeans. (Temperature: 10-15°C, Humidity: ≤40%, Wind: ≤3 m/s, Precipitation: yes)",
    ("cool", "low_humidity", "high_wind", "no_precipitation"): "Sweater, thick jacket, scarf, jeans. (Temperature: 10-15°C, Humidity: ≤40%, Wind: >5 m/s, Precipitation: none)",
    ("cool", "low_humidity", "high_wind", "precipitation"): "Thick waterproof jacket, insulated pants. (Temperature: 10-15°C, Humidity: ≤40%, Wind: >5 m/s, Precipitation: yes)",
    ("cool", "high_humidity", "low_wind", "no_precipitation"): "Breathable clothing, insulated jacket, closed shoes. (Temperature: 10-15°C, Humidity: >60%, Wind: ≤3 m/s, Precipitation: none)",
    ("cool", "high_humidity", "low_wind", "precipitation"): "Insulated waterproof jacket, scarf, closed shoes. (Temperature: 10-15°C, Humidity: >60%, Wind: ≤3 m/s, Precipitation: yes)",
    ("cool", "high_humidity", "high_wind", "no_precipitation"): "Insulated jacket, scarf, gloves. (Temperature: 10-15°C, Humidity: >60%, Wind: >5 m/s, Precipitation: none)",
    ("cool", "high_humidity", "high_wind", "precipitation"): "Thick waterproof jacket, insulated pants, scarf. (Temperature: 10-15°C, Humidity: >60%, Wind: >5 m/s, Precipitation: yes)",
    
    ("cold", "low_humidity", "low_wind", "no_precipitation"): "Warm jacket, insulated pants, hat, gloves. (Temperature: 0-10°C, Humidity: ≤40%, Wind: ≤3 m/s, Precipitation: none)",
    ("cold", "low_humidity", "low_wind", "precipitation"): "Thick waterproof jacket, insulated pants, hat, gloves. (Temperature: 0-10°C, Humidity: ≤40%, Wind: ≤3 m/s, Precipitation: yes)",
    ("cold", "low_humidity", "high_wind", "no_precipitation"): "Warm jacket, scarf, hat, gloves, insulated pants. (Temperature: 0-10°C, Humidity: ≤40%, Wind: >5 m/s, Precipitation: none)",
    ("cold", "low_humidity", "high_wind", "precipitation"): "Thick waterproof jacket, insulated pants, hat, scarf, gloves. (Temperature: 0-10°C, Humidity: ≤40%, Wind: >5 m/s, Precipitation: yes)",
    ("cold", "high_humidity", "low_wind", "no_precipitation"): "Insulated jacket, warm hat, scarf, gloves. (Temperature: 0-10°C, Humidity: >60%, Wind: ≤3 m/s, Precipitation: none)",
    ("cold", "high_humidity", "low_wind", "precipitation"): "Thick waterproof jacket, insulated pants, scarf, gloves. (Temperature: 0-10°C, Humidity: >60%, Wind: ≤3 m/s, Precipitation: yes)",
    ("cold", "high_humidity", "high_wind", "no_precipitation"): "Thick insulated jacket, scarf, gloves, hat. (Temperature: 0-10°C, Humidity: >60%, Wind: >5 m/s, Precipitation: none)",
    ("cold", "high_humidity", "high_wind", "precipitation"): "Thick waterproof jacket, scarf, gloves, insulated pants, hat. (Temperature: 0-10°C, Humidity: >60%, Wind: >5 m/s, Precipitation: yes)",
    
    ("very_cold", "low_humidity", "low_wind", "no_precipitation"): "Very thick insulated jacket, snow pants, hat, gloves. (Temperature: <-5°C, Humidity: ≤40%, Wind: ≤3 m/s, Precipitation: none)",
    ("very_cold", "low_humidity", "low_wind", "precipitation"): "Thick waterproof jacket, snow pants, hat, gloves. (Temperature: <-5°C, Humidity: ≤40%, Wind: ≤3 m/s, Precipitation: yes)",
    ("very_cold", "low_humidity", "high_wind", "no_precipitation"): "Thick insulated jacket, scarf, hat, gloves, snow pants. (Temperature: <-5°C, Humidity: ≤40%, Wind: >5 m/s, Precipitation: none)",
    ("very_cold", "low_humidity", "high_wind", "precipitation"): "Thick waterproof jacket, insulated pants, hat, scarf, gloves. (Temperature: <-5°C, Humidity: ≤40%, Wind: >5 m/s, Precipitation: yes)",
    ("very_cold", "high_humidity", "low_wind", "no_precipitation"): "Very thick insulated jacket, warm hat, scarf, gloves. (Temperature: <-5°C, Humidity: >60%, Wind: ≤3 m/s, Precipitation: none)",
    ("very_cold", "high_humidity", "low_wind", "precipitation"): "Thick waterproof jacket, insulated pants, scarf, gloves. (Temperature: <-5°C, Humidity: >60%, Wind: ≤3 m/s, Precipitation: yes)",
    ("very_cold", "high_humidity", "high_wind", "no_precipitation"): "Thick insulated jacket, scarf, gloves, hat, snow pants. (Temperature: <-5°C, Humidity: >60%, Wind: >5 m/s, Precipitation: none)",
    ("very_cold", "high_humidity", "high_wind", "precipitation"): "Thick waterproof jacket, scarf, gloves, insulated pants, hat. (Temperature: <-5°C, Humidity: >60%, Wind: >5 m/s, Precipitation: yes)",
}

    return recommendations.get((temp_key, humidity_key, wind_key, precip_key), "Unknown parameters")

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Yes, I recommend it!", callback_data="Yes")
    markup.add(button)
    bot.send_message(message.chat.id, 'Hi, can I recommend you the type of clothing for your weather?', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "Yes")
def yes_call(call):
    bot.answer_callback_query(call.id)
    location_user(call.message)

def location_user(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button = types.KeyboardButton("Send my location!", request_location=True)
    markup.add(button)
    bot.send_message(message.chat.id, "Please send your location!", reply_markup=markup)

@bot.message_handler(content_types=['location'])
def sovet(message):

    api_key = os.getenv("TOKEN_OPENWEATHERMAP")
    
    if not api_key:
        bot.send_message(message.chat.id, "Error: API key not found.")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={message.location.latitude}&lon={message.location.longitude}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            weather_data = response.json()  
            recomends = get_clothing_recommendation(
                weather_data['main']['temp'], 
                weather_data['main']['humidity'], 
                weather_data['wind']['speed'], 
                weather_data['weather'][0]['main'], 
                weather_data['clouds']['all']
            )
            bot.send_message(message.chat.id, f"Weather data received: {recomends}")
            bot.send_message(message.chat.id, "To get a recommendation again, simply send your location data")
        elif response.status_code == 401:
            bot.send_message(message.chat.id, "Error 401: Invalid API key or authentication problems.")
        else:
            bot.send_message(message.chat.id, f"Failed to retrieve data. Error code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        bot.send_message(message.chat.id, f"An error occurred while making your request: {e}")

bot.polling()
