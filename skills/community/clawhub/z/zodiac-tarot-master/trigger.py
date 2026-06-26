#!/usr/bin/env python3
"""
星座占卜师触发器脚本
用于OpenClaw技能触发
"""

import sys
import json
import subprocess

def handle_trigger(args):
    """处理技能触发"""
    
    if not args:
        return display_help()
    
    query = args[0].lower()
    
    # 星座配对触发词
    zodiac_keywords = ["星座", "星座配对", "配对", "匹配度", "zodiac"]
    
    # 塔罗牌占卜触发词
    tarot_keywords = ["塔罗牌", "塔罗", "占卜", "抽牌", "tarot", "card", "fortune", "divination"]
    
    # 判断触发类型
    for keyword in zodiac_keywords:
        if keyword in query:
            return handle_zodiac(query)
    
    for keyword in tarot_keywords:
        if keyword in query:
            return handle_tarot(query)
    
    return display_help()

def handle_zodiac(query):
    """处理星座配对请求"""
    
    # 提取星座名称
    zodiac_names = ["白羊座", "金牛座", "双子座", "巨蟹座", "狮子座", "处女座",
                    "天秤座", "天蝎座", "射手座", "摩羯座", "水瓶座", "双鱼座"]
    
    zodiac1 = None
    zodiac2 = None
    
    # 查找星座名称
    for zodiac in zodiac_names:
        if zodiac in query:
            if zodiac1 is None:
                zodiac1 = zodiac
            elif zodiac2 is None:
                zodiac2 = zodiac
                break
    
    if zodiac1 and zodiac2:
        # 调用星座配对脚本
        result = subprocess.run(["python", "scripts/compatibility.py", zodiac1, zodiac2], 
                                capture_output=True, text=True)
        return result.stdout
    elif zodiac1 and zodiac2 is None:
        # 只有一个星座，需要另一个星座
        return f"""
💕 星座配对 💕
═══════════════════════════════════════════
请输入两个星座进行配对
例如："白羊座和天秤座"

支持的星座：白羊座、金牛座、双子座、巨蟹座、狮子座、
         处女座、天秤座、天蝎座、射手座、摩羯座、
         水瓶座、双鱼座

用法：星座配对：<星座1>和<星座2>
═══════════════════════════════════════════
"""
    else:
        return display_zodiac_help()

def handle_tarot(query):
    """处理塔罗牌占卜请求"""
    
    # 提取占卜主题
    divination_types = {
        "爱情": "love", "感情": "love", "恋爱": "love", "婚姻": "love",
        "事业": "career", "工作": "career", "职业": "career",
        "健康": "health", "身体": "health", "养生": "health",
        "财运": "finance", "金钱": "finance", "财富": "finance",
        "灵性": "spiritual", "修行": "spiritual", "自我": "spiritual",
        "选择": "decision", "决定": "decision", "抉择": "decision"
    }
    
    divination_type = None
    for key, value in divination_types.items():
        if key in query:
            divination_type = value
            break
    
    # 判断牌阵类型
    if "三张" in query or "三张牌" in query or "three" in query:
        spread_type = "three"
    elif "十字" in query or "十字牌阵" in query or "cross" in query:
        spread_type = "cross"
    else:
        spread_type = "single"
    
    # 调用塔罗牌脚本
    cmd_args = ["python", "scripts/tarot.py", spread_type]
    if divination_type:
        cmd_args.append(divination_type)
    
    result = subprocess.run(cmd_args, capture_output=True, text=True)
    
    return result.stdout

def display_help():
    """显示帮助信息"""
    
    return """
💕 星座占卜师 🌌
═══════════════════════════════════════════

📖 功能介绍：
1. 💕 星座配对 - 计算两个星座的爱情匹配度
2. 🎴 塔罗占卜 - 78张塔罗牌占卜系统

✨ 使用示例：

星座配对：
- "星座配对：白羊座和天秤座"
- "双鱼座和巨蟹座配吗？"
- "天蝎座和狮子座的匹配度"

塔罗占卜：
- "帮我抽一张塔罗牌"
- "塔罗占卜：爱情问题"
- "十字牌阵占卜事业"
- "三张牌占卜过去现在未来"

🎯 温馨提示：
- 星座配对重在性格分析，不制造焦虑
- 塔罗牌占卜给出建设性建议
- 所有结果仅供娱乐，不要迷信！
═══════════════════════════════════════════
"""

def display_zodiac_help():
    """显示星座配对帮助"""
    
    return """
💕 星座配对 💕
═══════════════════════════════════════════

✨ 支持的星座：
白羊座、金牛座、双子座、巨蟹座、狮子座、
处女座、天秤座、天蝎座、射手座、摩羯座、
水瓶座、双鱼座

🎯 用法示例：
- "星座配对：白羊座和天秤座"
- "双鱼座和巨蟹座配吗？"
- "天蝎座和狮子座的匹配度"

📊 配对包含：
1. 💖 匹配度评分（0-100分）
2. 🌸 双方性格特点
3. 🔮 元素分析（火土风水）
4. 💌 配对评语
5. ✅ 相处建议

🌈 温馨提示：
星座配对重在性格分析，生活掌握在自己手中
═══════════════════════════════════════════
"""

def main():
    """主函数"""
    result = handle_trigger(sys.argv[1:])
    print(result)

if __name__ == "__main__":
    main()