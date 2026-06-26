#!/usr/bin/env python3
"""
QWeather China 使用示例
展示如何在不同场景下使用天气服务
"""

from qweather import QWeatherClient

def example_basic_usage():
    """基础使用示例"""
    print("=== 基础使用示例 ===")
    
    client = QWeatherClient()
    
    # 1. 获取实时天气
    weather = client.get_weather_now("beijing")
    print("1. 北京实时天气:")
    print(weather.format())
    
    # 2. 获取3天预报
    forecasts = client.get_weather_forecast("shanghai", 3)
    print("\n2. 上海3天预报:")
    for forecast in forecasts:
        print(forecast.format())
    
    # 3. 获取生活指数
    indices = client.get_life_indices("guangzhou")
    print("\n3. 广州生活指数 (前5个):")
    for index in indices[:5]:
        print(index.format())

def example_advanced_features():
    """高级功能示例"""
    print("\n=== 高级功能示例 ===")
    
    client = QWeatherClient()
    
    # 多个城市对比
    cities = ["beijing", "shanghai", "guangzhou"]
    
    print("多个城市温度对比:")
    for city in cities:
        weather = client.get_weather_now(city)
        dressing = client.get_dressing_advice(weather.temp)
        print(f"{city.capitalize()}: {weather.temp}°C - {dressing}")

def example_error_handling():
    """错误处理示例"""
    print("\n=== 错误处理示例 ===")
    
    client = QWeatherClient()
    
    try:
        # 尝试获取不存在的城市
        weather = client.get_weather_now("invalid_city")
        print(weather.format())
    except Exception as e:
        print(f"错误处理: {e}")
        print("已自动回退到默认城市(北京)")

def example_integration():
    """集成示例 - 模拟OpenClaw中的使用"""
    print("\n=== OpenClaw集成示例 ===")
    
    class OpenClawWeatherBot:
        def __init__(self):
            self.client = QWeatherClient()
        
        def handle_query(self, query: str):
            """处理用户查询"""
            query_lower = query.lower()
            
            if "天气" in query_lower and "北京" in query_lower:
                return self._get_beijing_weather()
            elif "预报" in query_lower and "上海" in query_lower:
                return self._get_shanghai_forecast()
            elif "指数" in query_lower or "生活" in query_lower:
                return self._get_life_indices("beijing")
            else:
                return "请告诉我你想查询哪个城市的天气信息？"
        
        def _get_beijing_weather(self):
            """获取北京天气"""
            weather = self.client.get_weather_now("beijing")
            dressing = self.client.get_dressing_advice(weather.temp)
            umbrella = self.client.get_umbrella_advice(weather.precip, weather.text)
            
            return f"""
北京当前天气:
{weather.format()}
建议:
{dressing}
{umbrella}
"""
        
        def _get_shanghai_forecast(self):
            """获取上海预报"""
            forecasts = self.client.get_weather_forecast("shanghai", 3)
            result = "上海未来3天预报:\n"
            for forecast in forecasts:
                result += forecast.format() + "\n"
            return result
        
        def _get_life_indices(self, city: str):
            """获取生活指数"""
            indices = self.client.get_life_indices(city)
            result = f"{city.capitalize()}今日生活指数:\n"
            for index in indices[:6]:
                result += index.format() + "\n"
            return result
    
    # 模拟用户查询
    bot = OpenClawWeatherBot()
    
    queries = [
        "北京天气怎么样？",
        "上海未来几天预报",
        "今天的生活指数",
        "广州温度多少？"
    ]
    
    for query in queries[:2]:  # 测试前两个查询
        print(f"\n用户: {query}")
        print(f"助手: {bot.handle_query(query)}")

def example_cli_usage():
    """命令行使用示例"""
    print("\n=== 命令行使用示例 ===")
    print("""
基本命令:
1. 实时天气: python qweather.py now --city beijing
2. 3天预报: python qweather.py forecast --city shanghai --days 3
3. 生活指数: python qweather.py indices --city guangzhou
4. 空气质量: python qweather.py air --city hangzhou
5. 完整报告: python qweather.py full --city chengdu

城市支持:
- 北京 (beijing), 上海 (shanghai), 广州 (guangzhou)
- 深圳 (shenzhen), 杭州 (hangzhou), 成都 (chengdu)
- 或直接使用城市代码: 101010100 (北京)
""")

def main():
    """运行所有示例"""
    print("QWeather China 使用示例集")
    print("=" * 60)
    
    example_basic_usage()
    example_advanced_features()
    example_error_handling()
    example_integration()
    example_cli_usage()
    
    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("数据来源: 中国气象局 · 和风天气")

if __name__ == "__main__":
    main()