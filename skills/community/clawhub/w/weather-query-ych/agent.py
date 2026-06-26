# agent.py
import requests

def get_weather(city, date):
#https://api.weather.com/v2/turbo/vt1dailyForecast?apiKey=c1ea9f47f6a88b9acb43aba7faf389d4&format=json&geocode=39.93%2C116.40&language=zh-CN&units=m
    api_key = "c1ea9f47f6a88b9acb43aba7faf389d4"
    url = f"https://api.weather.com/v2/{city}/{date}?key={api_key}"
    response = requests.get(url)
    return response.json()

def handle_request(input_text):
    # 解析输入（示例简化）
    city = input_text.split("天气")[0]
    date = "today"  # 实际需更复杂解析
    data = get_weather(city, date)
    return f"院彩华测试: {city}今天{data['weather']}, {data['temp']}℃"