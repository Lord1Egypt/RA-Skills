#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw 天气查询测试 Skill
功能：接收城市名称，返回当日天气信息
"""
import requests
import json

def handler(event, context):
    """
    OpenClaw 技能入口函数（固定名称 handler）
    :param event: 包含用户输入、设备信息等的字典
    :param context: 运行上下文
    :return: 回复内容（字典格式）
    """
    try:
        # 1. 解析用户输入（提取城市名称）
        user_input = event.get("text", "").strip()
        city = extract_city(user_input)
        
        if not city:
            return {
                "code": 200,
                "data": {
                    "reply": "你可以说「北京天气」「上海今日天气」，我来帮你查询～"
                }
            }
        
        # 2. 调用免费天气接口（测试用）
        weather_data = get_weather(city)
        
        # 3. 构造回复内容
        if weather_data:
            reply = f"{city}今日天气：{weather_data['weather']}，温度{weather_data['temp']}℃，风力{weather_data['wind']}"
        else:
            reply = f"暂时查不到{city}的天气信息哦，换个城市试试吧～"
        
        return {
            "code": 200,
            "data": {
                "reply": reply
            }
        }
    
    except Exception as e:
        # 异常处理（必选，避免技能崩溃）
        return {
            "code": 500,
            "data": {
                "reply": f"技能出错啦：{str(e)}"
            }
        }

def extract_city(input_text):
    """
    从用户输入中提取城市名称（简单版，可扩展）
    示例：输入「北京天气」→ 提取「北京」
    """
    # 常见城市列表（测试用，可扩展）
    cities = ["北京", "上海", "广州", "深圳", "杭州", "成都", "重庆"]
    for city in cities:
        if city in input_text:
            return city
    return None

def get_weather(city):
    """
    调用免费天气接口获取数据（测试用，无密钥）
    """
    try:
        # 免费测试接口（仅供测试，生产环境需替换为正规接口）
        url = f"http://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=5)
        data = json.loads(response.text)
        
        # 提取核心天气信息
        current_weather = data["current_condition"][0]
        return {
            "weather": current_weather["weatherDesc"][0]["value"],
            "temp": current_weather["temp_C"],
            "wind": current_weather["windspeedKmph"] + "km/h"
        }
    except:
        return None

# 本地测试代码（发布前验证功能）
if __name__ == "__main__":
    # 模拟 OpenClaw 传入的 event 参数
    test_event = {
        "text": "北京天气"
    }
    result = handler(test_event, None)
    print("技能回复：", result["data"]["reply"])