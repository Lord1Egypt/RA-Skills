#!/usr/bin/env python3
"""
企业微信语音消息 Agent - 语音消息模拟器
用于本地测试意图解析和对话流程
"""

import json
import sys
import argparse
import re
from datetime import datetime, timedelta
import hashlib


def generate_msgid():
    """生成唯一消息ID"""
    timestamp = datetime.now().isoformat()
    return hashlib.md5(timestamp.encode()).hexdigest()[:24]


def simulate_voice_callback(text, userid="test_user"):
    """模拟企业微信语音消息回调"""
    
    # 构建企业微信格式的回调JSON
    callback = {
        "msgid": generate_msgid(),
        "aibotid": "test_aibot",
        "chattype": "single",
        "from": {"userid": userid},
        "response_url": "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=test",
        "msgtype": "voice",
        "voice": {
            "content": text
        },
        "timestamp": int(datetime.now().timestamp())
    }
    
    return callback


def parse_intent(text):
    """意图解析器"""
    
    # 关键词映射表
    intent_keywords = {
        "query_schedule": [
            "日程", "会议", "安排", "行程", "有什么会", "几点开会",
            "日程安排", "会议安排", "什么安排", "下周", "下周有什么"
        ],
        "create_todo": [
            "提醒", "待办", "任务", "别忘了", "记得", "定时提醒",
            "设提醒", "创建待办", "定提醒"
        ],
        "query_weather": [
            "天气", "气温", "下雨", "温度", "穿什么", "热不冷",
            "天气预报", "气温多少"
        ],
        "send_message": [
            "发消息", "告诉", "通知", "转发",
            "发信息", "发微信", "给.*发"
        ],
        "help": [
            "帮助", "能做什么", "怎么用", "功能", "help",
            "你可以做什么", "使用说明"
        ],
        "exit_voice": [
            "退出", "不用了", "谢谢", "结束", "再见", "拜拜",
            "先这样"
        ]
    }
    
    # 匹配意图
    max_score = 0
    best_intent = "custom"
    
    for intent, keywords in intent_keywords.items():
        score = sum(1 for kw in keywords if kw in text.lower())
        if score > max_score:
            max_score = score
            best_intent = intent
    
    # 提取实体
    entities = extract_entities(text)
    
    return {
        "intent": best_intent,
        "confidence": min(max_score * 0.3, 1.0),
        "entities": entities,
        "raw_text": text
    }


def extract_entities(text):
    """实体信息提取"""
    
    entities = {}
    
    # 时间提取
    time_patterns = {
        "今天": 0,
        "明天": 1,
        "后天": 2,
        "大后天": 3
    }
    
    for time_word, offset in time_patterns.items():
        if time_word in text:
            target = datetime.now() + timedelta(days=offset)
            entities["time"] = time_word
            entities["date"] = target.strftime("%Y-%m-%d")
            break
    
    # 日期提取 (MM-DD 格式)
    date_match = re.search(r'(\d{1,2})月(\d{1,2})日', text)
    if date_match:
        month, day = date_match.groups()
        year = datetime.now().year
        entities["date"] = f"{year}-{int(month):02d}-{int(day):02d}"
    
    # 人物提取（简化版）
    person_keywords = ["张三", "李四", "王五", "赵六", "小明", "小红"]
    for person in person_keywords:
        if person in text:
            entities["person"] = person
            break
    
    # 地点提取
    city_keywords = ["北京", "上海", "广州", "深圳", "杭州", "成都"]
    for city in city_keywords:
        if city in text:
            entities["location"] = city
            break
    
    return entities


def generate_reply(intent):
    """根据意图生成回复"""
    
    replies = {
        "query_schedule": "正在查询您{}的日程安排，请稍候...",
        "create_todo": "好的，我来为您创建待办提醒...",
        "query_weather": "正在查询{}天气信息...",
        "send_message": "好的，我来帮您发送消息...",
        "help": (
            "我是您的语音助手，可以帮您：\n"
            "• 查询日程安排（例：\"明天有什么会议\"）\n"
            "• 创建待办提醒（例：\"提醒我下午3点开会\"）\n"
            "• 查询天气（例：\"北京今天天气\"）\n"
            "• 发送消息（例：\"发消息给张三\"）\n"
            "🗣️ 直接用语音告诉我您的需求即可！"
        ),
        "exit_voice": "好的，语音模式已退出，随时可以再次召唤我～",
        "custom": (
            "抱歉，我没有完全理解您的意思 😅\n"
            "请试试以下说法：\n"
            "• \"查一下明天的日程\"\n"
            "• \"提醒我下午3点提交报告\"\n"
            "• \"北京天气怎么样\""
        )
    }
    
    template = replies.get(intent["intent"], replies["custom"])
    
    # 填充实体
    try:
        if intent["intent"] == "query_schedule":
            date = intent["entities"].get("date", "")
            reply = template.format(f"({date})" if date else "")
        elif intent["intent"] == "query_weather":
            location = intent["entities"].get("location", "当地")
            reply = template.format(location)
        else:
            reply = template
    except Exception:
        reply = template
    
    return reply


def main():
    parser = argparse.ArgumentParser(description="企业微信语音消息模拟器")
    parser.add_argument("--text", "-t", required=True, help="语音转写的文本内容")
    parser.add_argument("--userid", "-u", default="test_user", help="用户ID")
    parser.add_argument("--format", "-f", choices=["json", "text"], default="text", help="输出格式")
    
    args = parser.parse_args()
    
    # 生成回调
    callback = simulate_voice_callback(args.text, args.userid)
    
    # 解析意图
    intent = parse_intent(callback["voice"]["content"])
    
    # 生成回复
    reply = generate_reply(intent)
    
    if args.format == "json":
        result = {
            "callback": callback,
            "intent": intent,
            "reply": reply,
            "status": "success"
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 50)
        print("📨 企业微信回调模拟")
        print("=" * 50)
        print(f"\n📝 语音内容：{callback['voice']['content']}")
        print(f"\n🎯 识别意图：{intent['intent']} (置信度: {intent['confidence']:.2f})")
        print(f"📊 实体信息：{json.dumps(intent['entities'], ensure_ascii=False)}")
        print(f"\n💬 助手回复：\n{reply}")
        print("\n" + "=" * 50)


if __name__ == '__main__':
    main()
