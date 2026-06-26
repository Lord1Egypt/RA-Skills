"""
张雪峰AI Skill 主逻辑
处理用户输入、知识检索、回答生成
"""
import os
import re
import json
from pathlib import Path
from typing import Optional, List, Dict, Any

# 触发关键词
TRIGGER_KEYWORDS = [
    "张雪峰",
    "高考志愿",
    "志愿填报",
    "选专业",
    "专业选择",
    "选大学",
    "院校选择",
    "专业前景",
    "考研",
    "考公",
    "就业方向",
    "职业规划",
    "填志愿",
    "报志愿",
    "高考",
    "大学专业",
    "985",
    "211",
    "一本",
    "二本",
    "专科",
    "医学专业",
    "计算机专业",
    "金融专业",
    "法律专业",
    "师范专业",
    "工科专业",
    "文科专业",
    "理科专业",
]

# 张雪峰风格系统提示词
ZHANG_XUEFENG_SYSTEM_PROMPT = """你是张雪峰风格的AI助手，专门回答高考志愿填报、专业选择、院校分析、职业规划等问题。

【你的风格特点】
1. 说话直白、实在、不绕弯 - 有什么说什么，不客套
2. 有观点、有态度，不模棱两可 - 该支持支持，该反对反对
3. 用大白话讲复杂问题 - 不用专业术语绕人
4. 敢于说真话，不怕得罪人 - 该泼冷水就泼冷水

【回答结构】
1. 先给出明确观点（是/否，好/不好，建议/不建议）
2. 用具体例子或数据支撑观点
3. 给出可操作的建议（具体怎么做）
4. 提醒注意事项或潜在风险

【禁止说的话】
- "这要看个人情况" - 太敷衍
- "每个选择都有利弊" - 废话
- "建议你多方面考虑" - 等于没说
- "follow your heart" - 这不是张雪峰风格

【张雪峰经典语录参考】
- "你要是普通家庭，就别想着搞那些虚的"
- "文科选学校，理科选专业"
- "能上985不上211，能上211不上普通一本"
- "生化环材，四大天坑"
- "金融这行，家里没资源别碰"

记住：家长和学生来问你，是要一个明确的建议，不是要听你说"都行"。"""


def should_trigger(message: str) -> bool:
    """检测是否应该触发本 Skill"""
    message_lower = message.lower()
    for keyword in TRIGGER_KEYWORDS:
        if keyword in message_lower:
            return True
    return False


def extract_intent(message: str) -> Dict[str, Any]:
    """从用户消息中提取意图和关键信息"""
    intent = {
        "raw_message": message,
        "topic": None,
        "major": None,
        "school": None,
        "score_range": None,
        "region": None,
    }

    # 提取专业关键词
    major_keywords = [
        "计算机", "软件工程", "人工智能", "电子", "通信", "机械", "土木",
        "建筑", "医学", "临床", "护理", "金融", "经济", "会计", "法律",
        "法学", "师范", "教育", "英语", "中文", "新闻", "传媒", "设计",
        "艺术", "生物", "化学", "环境", "材料", "数学", "物理", "心理",
        "哲学", "历史", "政治", "地理",
    ]

    for major in major_keywords:
        if major in message:
            intent["major"] = major
            break

    # 提取分数段
    score_patterns = [
        r"(\d+)分", r"(\d+)多分", r"(\d+)左右",
        r"一本线", r"二本线", r"专科线",
        r"985", r"211", r"双一流",
        r"一本", r"二本", r"三本", r"专科",
    ]

    for pattern in score_patterns:
        match = re.search(pattern, message)
        if match:
            intent["score_range"] = match.group(0)
            break

    # 提取地区
    region_keywords = [
        "北京", "上海", "广州", "深圳", "杭州", "南京", "武汉", "成都",
        "西安", "天津", "重庆", "苏州", "青岛", "大连", "厦门", "宁波",
        "山东", "江苏", "浙江", "广东", "河南", "河北", "湖北", "湖南",
        "四川", "陕西", "辽宁", "吉林", "黑龙江", "福建", "安徽", "江西",
    ]

    for region in region_keywords:
        if region in message:
            intent["region"] = region
            break

    # 判断话题类型
    if "专业" in message or intent["major"]:
        intent["topic"] = "major"
    elif "学校" in message or "大学" in message or "院校" in message:
        intent["topic"] = "school"
    elif "考研" in message:
        intent["topic"] = "postgraduate"
    elif "考公" in message or "公务员" in message:
        intent["topic"] = "civil_service"
    elif "就业" in message or "工作" in message:
        intent["topic"] = "career"
    else:
        intent["topic"] = "general"

    return intent


def get_knowledge_base_path() -> Path:
    """获取知识库路径"""
    return Path.home() / ".zhang-xuefeng" / "knowledge_base"


def check_knowledge_base() -> bool:
    """检查知识库是否已激活"""
    kb_path = get_knowledge_base_path()
    index_path = kb_path / "index"
    return index_path.exists() and any(index_path.iterdir())


def handle_message(message: str) -> Optional[str]:
    """
    处理用户消息的主入口
    返回：如果触发，返回增强的系统提示词；如果不触发，返回 None
    """
    if not should_trigger(message):
        return None

    # 检查知识库是否已激活
    if not check_knowledge_base():
        return "⚠️ 知识库未下载，无法回答您的问题。\n\n知识库请到 vdoob.com 下载，安装后即可使用张雪峰AI助手。"

    intent = extract_intent(message)

    # 构建增强的提示词
    enhanced_prompt = f"""{ZHANG_XUEFENG_SYSTEM_PROMPT}

【用户问题】
{message}

【提取的关键信息】
- 话题类型: {intent['topic']}
- 涉及专业: {intent['major'] or '未提及'}
- 分数/层次: {intent['score_range'] or '未提及'}
- 地区偏好: {intent['region'] or '未提及'}

【回答要求】
1. 用张雪峰的风格回答
2. 给出明确观点，不要模棱两可
3. 用大白话，不要说教
4. 如果有风险要直接指出来

请直接回答用户问题：
"""

    return enhanced_prompt


def get_activation_status() -> Dict[str, Any]:
    """获取知识库激活状态"""
    kb_path = get_knowledge_base_path()
    return {
        "activated": check_knowledge_base(),
        "knowledge_base_path": str(kb_path),
        "message": "知识库已激活" if check_knowledge_base() else "知识库未激活，请访问 vdoob.com 购买激活码"
    }


# OpenClaw Skill 入口点
def main():
    """Skill 主入口"""
    print("=" * 50)
    print("张雪峰AI Skill 已加载")
    print("=" * 50)
    print("触发关键词：张雪峰、高考志愿、选专业、院校选择等")
    print("=" * 50)

    status = get_activation_status()
    print(f"知识库状态: {status['message']}")

    return {
        "name": "zhang-xuefeng-ai",
        "version": "1.0.0",
        "trigger_keywords": TRIGGER_KEYWORDS,
        "activated": status["activated"]
    }


if __name__ == "__main__":
    main()
