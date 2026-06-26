#!/usr/bin/env python3
# 穿衣建议规则引擎（零 API 成本）
import re

def extract_temperature(temp_str):
    """
    从 "8℃～15℃" 提取最高温和最低温
    返回 (low, high)，单位℃
    """
    if not temp_str:
        return None, None
    nums = re.findall(r'-?\d+', temp_str)
    if len(nums) >= 2:
        return int(nums[0]), int(nums[1])
    elif len(nums) == 1:
        return int(nums[0]), int(nums[0])
    return None, None

def generate_dress_advice(weather_data):
    """
    weather_data: dict 含 temp_range, weather, wind
    返回穿衣建议字符串
    """
    temp_range = weather_data.get('temp_range', '')
    weather = weather_data.get('weather', '')
    wind = weather_data.get('wind', '')
    
    low, high = extract_temperature(temp_range)
    if low is None or high is None:
        return "温度数据缺失，建议根据体感穿着。"
    
    # 基础建议（基于最高温）
    advice_parts = []
    if high >= 28:
        advice_parts.append("短袖/短裤")
    elif high >= 22:
        advice_parts.append("长袖T恤")
    elif high >= 15:
        advice_parts.append("长袖衬衫+薄外套")
    elif high >= 8:
        advice_parts.append("毛衣+外套")
    else:
        advice_parts.append("羽绒服/厚棉衣")
    
    # 温差提醒
    if high - low >= 10:
        advice_parts.append("早晚温差大，建议带件外套备用")
    
    # 天气现象
    if any(word in weather for word in ['雨', '雪', '雹']):
        advice_parts.append("有降水，请带伞")
    if '晴' in weather and high >= 20:
        advice_parts.append("紫外线较强，建议防晒")
    
    # 风力
    if '大风' in wind or '级' in wind:
        level_match = re.search(r'(\d+)级', wind)
        if level_match and int(level_match.group(1)) >= 5:
            advice_parts.append("风大，建议戴帽子/围巾")
    
    # 拼接
    if not advice_parts:
        return "建议根据体感穿着。"
    return "，".join(advice_parts) + "。"

if __name__ == "__main__":
    # 测试
    test_data = {
        "temp_range": "8℃～15℃",
        "weather": "多云转晴",
        "wind": "东北风 2级"
    }
    print(generate_dress_advice(test_data))