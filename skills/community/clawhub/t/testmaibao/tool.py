import json
import random


class WeatherQueryTool:
    def __init__(self):
        pass

    def get_weather(self, city: str, unit: str = "celsius") -> str:
        """
        模拟获取天气数据的函数。

        Args:
            city (str): 城市名称
            unit (str): 温度单位 ('celsius' or 'fahrenheit')

        Returns:
            str: JSON 格式的天气信息
        """
        # 模拟一些随机天气数据，用于测试
        weather_conditions = ["晴朗", "多云", "小雨", "雷阵雨", "阴天"]
        base_temp = random.randint(15, 35)

        if unit.lower() == "fahrenheit":
            temp_display = f"{base_temp * 9 / 5 + 32:.1f}°F"
        else:
            temp_display = f"{base_temp}°C"

        result = {
            "city": city,
            "temperature": temp_display,
            "description": random.choice(weather_conditions),
            "humidity": f"{random.randint(30, 80)}%",
            "status": "success"
        }

        # 模拟简单的错误处理
        if not city:
            return json.dumps({"status": "error", "message": "City name cannot be empty."})

        return json.dumps(result, ensure_ascii=False)


# 用于直接运行测试
if __name__ == "__main__":
    tool = WeatherQueryTool()
    print(tool.get_weather("北京"))
    print(tool.get_weather("New York", unit="fahrenheit"))