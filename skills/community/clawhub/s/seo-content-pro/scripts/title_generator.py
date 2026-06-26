#!/usr/bin/env python3
"""
AI 标题生成器 - 生成 10 万 + 爆款标题
支持 A/B 测试，生成多个变体
"""

import sys
import json

# 标题模板库
TITLE_TEMPLATES = {
    "how_to": [
        "如何在{time}内{result}（完整指南）",
        "{number}个简单步骤，教你{result}",
        "{result}的终极指南（{year}最新版）",
    ],
    "list": [
        "{number}个{topic}技巧，第{highlight}个太实用了",
        "{number}个{topic}错误，你中了几个？",
        "Top {number}：{topic}最佳实践",
    ],
    "question": [
        "为什么你的{topic}总是失败？原因在这里",
        "{topic}真的有用吗？实测告诉你",
        "如何用{topic}实现{result}？",
    ],
    "secret": [
        "{number}个{topic}秘密，专家不会告诉你",
        "揭秘：{result}背后的真相",
        "{topic}内幕：{number}个不为人知的技巧",
    ],
    "comparison": [
        "{A} vs {B}：哪个更适合你？",
        "{number}个{topic}工具对比，最佳是...",
        "我用{A}和{B}做了{result}，差距惊人",
    ],
}

def generate_titles(topic, result="", number=5, style="all"):
    """生成标题变体"""
    titles = []
    
    if style == "all":
        styles = list(TITLE_TEMPLATES.keys())
    else:
        styles = [style]
    
    for style in styles:
        templates = TITLE_TEMPLATES.get(style, [])
        for template in templates[:number]:
            title = template.format(
                topic=topic,
                result=result or topic,
                number=3,
                time="30 分钟",
                year="2026",
                highlight=3,
                A="工具 A",
                B="工具 B"
            )
            titles.append(title)
    
    return titles[:number]

def score_title(title):
    """简单标题评分（基于长度、关键词等）"""
    score = 0
    
    # 长度评分（理想 20-40 字）
    length = len(title)
    if 20 <= length <= 40:
        score += 30
    elif 15 <= length <= 50:
        score += 20
    else:
        score += 10
    
    # 数字加分
    if any(c.isdigit() for c in title):
        score += 20
    
    # 问题加分
    if "?" in title or "？" in title:
        score += 15
    
    # 情感词加分
    emotion_words = ["终极", "完整", "秘密", "揭秘", "惊人", "实用"]
    if any(word in title for word in emotion_words):
        score += 20
    
    # 括号加分
    if "(" in title or "（" in title:
        score += 15
    
    return min(score, 100)

if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else "SEO 内容写作"
    result = sys.argv[2] if len(sys.argv) > 2 else ""
    number = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    
    titles = generate_titles(topic, result, number)
    
    print(f"=== AI 标题生成器 ===")
    print(f"主题：{topic}")
    print(f"生成数量：{len(titles)}\n")
    
    for i, title in enumerate(titles, 1):
        score = score_title(title)
        print(f"{i}. [{score}分] {title}")
