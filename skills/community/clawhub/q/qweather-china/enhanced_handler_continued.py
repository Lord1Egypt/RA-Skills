#!/usr/bin/env python3
"""
enhanced_handler.py的续写部分
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_handler import EnhancedWeatherHandler

def generate_detailed_response_continued(self, location, display_name, weather_now, today_forecast, qtype):
    """生成详细回答（续写）"""
    # 这是enhanced_handler.py中generate_detailed_response方法的续写
    
    response = ""
    
    # 湿度建议（续）
    if weather_now.humidity >= 80:
        response += "• 除湿：湿度较高，可能感觉闷热\n"
    elif weather_now.humidity <= 40:
        response += "• 补水：湿度较低，注意补水保湿\n"
    
    response += "\n"
    
    # 空气质量（如果有）
    try:
        air = self.client.get_air_quality(location.name)
        response += "🌫️ 空气质量\n"
        response += "-" * 20 + "\n"
        response += f"• AQI：{air.aqi}（{air.category}）\n"
        response += f"• 主要污染物：{air.primary}\n"
        response += f"• PM2.5：{air.pm2p5} μg/m³\n"
        response += f"• PM10：{air.pm10} μg/m³\n"
        response += f"• 建议：{air.advice}\n\n"
    except:
        pass  # 空气质量API可能不可用
    
    response += "=" * 40 + "\n"
    response += "💬 总结："
    
    # 总结
    summary = []
    if '雨' in weather_now.text or weather_now.precip > 0:
        summary.append("有降水")
    if weather_now.temp <= 10:
        summary.append("温度较低")
    elif weather_now.temp >= 25:
        summary.append("温度较高")
    if weather_now.wind_scale >= 4:
        summary.append("风较大")
    
    if summary:
        response += "今天" + "、".join(summary)
    else:
        response += "今天天气条件良好"
    
    response += "。"
    
    return response

def generate_error_response(self, error, location, display_name):
    """生成错误响应"""
    error_str = str(error)
    
    if "401" in error_str or "认证" in error_str:
        return f"❌ 获取{display_name}天气失败：认证错误\n请检查API配置。"
    elif "404" in error_str or "找不到" in error_str:
        return f"❌ 找不到地点：{display_name}\n请确认城市名称是否正确。"
    elif "网络" in error_str or "连接" in error_str:
        return f"❌ 网络连接失败\n请检查网络后重试。"
    else:
        return f"❌ 获取天气信息失败：{error_str}"

# 测试函数
def test_enhanced_handler():
    """测试增强版处理器"""
    # 从记忆中读取用户城市（北京）
    handler = EnhancedWeatherHandler(memory_city="beijing")
    
    test_queries = [
        "天气怎么样？",
        "要不要带伞？",
        "冷不冷？",
        "热不热？",
        "下雨吗？",
        "风大吗？",
        "湿度怎么样？",
        "北京天气怎么样？",
        "上海要不要带伞？",
        "详细说说天气",
        "北京详细天气",
    ]
    
    print("=" * 60)
    print("增强版天气处理器测试")
    print("=" * 60)
    
    for query in test_queries:
        print(f"\n查询：{query}")
        print("-" * 40)
        response = handler.handle_query(query)
        print(response[:200] + "..." if len(response) > 200 else response)
        print("-" * 40)
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    test_enhanced_handler()