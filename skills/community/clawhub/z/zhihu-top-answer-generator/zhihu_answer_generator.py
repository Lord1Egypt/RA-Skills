# 知乎高赞回答生成器 - 核心生成逻辑
import json
import random
from datetime import datetime

STYLES = {
    "cold_start": {
        "name": "冷启动（新手适用）",
        "hook_type": "共情+数据",
        "description": "适合0-100粉新手，快速获得基础点赞"
    },
    "debate": {
        "name": "争议性观点",
        "hook_type": "反常识+冲突",
        "description": "容易引发讨论，传播快但有风险"
    },
    "professional": {
        "name": "专业深度",
        "hook_type": "权威背书+系统框架",
        "description": "涨粉慢但精准，铁粉质量高"
    }
}

HOOK_TEMPLATES = [
    "作为XX年经验的从业者，我先说几个反常识的真相：",
    "看完这5000字，你可能会颠覆对XX的认知。",
    "大多数人都在犯的XX错误，我用XX万学费换来的教训。",
    "我在XX行业待了XX年，发现一个残酷的事实：",
    "不废话，先上数据：XX%的XX人都不知道这件事。",
    "作为XX（权威身份），我要说一句得罪人的话："
]

GOLDEN_ENDINGS = [
    "记住：真正的门槛，是开始之后的坚持。",
    "评论区告诉我，你现在卡在哪一步？",
    "如果这篇回答对你有帮助，点个赞，我会持续更新。",
    "收藏之前先看三遍，这是最快的学习方法。",
    "你的认知，决定你的选择；你的选择，决定你的命运。"
]

TAG_POOL = [
    "职场", "成长", "副业", "赚钱", "人际关系", 
    "自我提升", "心理学", "学习方法", "效率", "情绪管理",
    "创业", "职场晋升", "沟通技巧", "时间管理", "职业规划"
]

PUBLISH_TIMES = {
    "morning": {"time": "07:30-08:30", "suitable": ["职场", "成长", "学习方法"]},
    "noon": {"time": "12:00-13:00", "suitable": ["情感", "生活"]},
    "evening": {"time": "20:00-22:00", "suitable": ["职场", "创业", "赚钱", "副业"]},
    "late_night": {"time": "22:00-23:30", "suitable": ["情感", "心理", "深度思考"]}
}

def generate_zhihu_answer(topic: str, style: str = "cold_start", word_count: int = 1000):
    """生成知乎高赞回答"""
    
    style_info = STYLES.get(style, STYLES["cold_start"])
    
    # 生成开篇钩子
    hook = random.choice(HOOK_TEMPLATES)
    
    # 生成正文段落
    sections = []
    if word_count >= 500:
        sections.append({
            "title": "一、先说背景",
            "content": f"我研究这个话题已经XX时间，接触过XX个案例。\n"
                       f"今天把我总结出的核心方法论分享给你，建议先收藏再往下看。"
        })
    if word_count >= 1000:
        sections.append({
            "title": "二、具体怎么做（3步框架）",
            "content": "**第一步：XX**\n"
                      "这是最关键的一步，决定了后续80%的效果。\n\n"
                      "**第二步：XX**\n"
                      "很多人卡在这里，我踩过坑，你直接绕过去。\n\n"
                      "**第三步：XX**\n"
                      "这个方法让我在XX个月内实现了XX的突破。"
        })
    if word_count >= 2000:
        sections.append({
            "title": "三、常见的3个坑",
            "content": "1. **XX坑**：以为XX，其实XX\n"
                      "2. **XX坑**：做了XX，却忽略了XX\n"
                      "3. **XX坑**：XX是错的，XX才是对的"
        })
    
    # 生成金句收尾
    golden_ending = random.choice(GOLDEN_ENDINGS)
    
    # 生成标签
    selected_tags = random.sample(TAG_POOL, min(10, len(TAG_POOL)))
    
    # 推荐发布时间
    best_time = random.choice(list(PUBLISH_TIMES.keys()))
    time_info = PUBLISH_TIMES[best_time]
    
    return {
        "status": "success",
        "topic": topic,
        "style": style_info,
        "word_count": word_count,
        "answer": {
            "hook": hook,
            "sections": sections,
            "golden_ending": golden_ending,
            "tags": selected_tags,
            "publish_time": time_info,
            "full_text": f"{hook}\n\n" + 
                        "\n\n".join([f"{s['title']}\n{s['content']}" for s in sections]) +
                        f"\n\n{golden_ending}"
        }
    }

if __name__ == "__main__":
    result = generate_zhihu_answer(
        topic="如何通过副业月入过万？",
        style="debate",
        word_count=1500
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
