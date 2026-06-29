#!/usr/bin/env python3
"""
Xiaohongshu Note Booster — Core Generation Script

Generates viral Xiaohongshu notes from structured input.
Usage:
    python3 generate.py --topic "玫瑰精华水" --selling-points "补水保湿,提亮肤色,敏感肌可用" --audience "18-30岁女性" --style "亲切种草" --category beauty

    python3 generate.py --topic "白色阔腿裤" --selling-points "显瘦,垂坠感好,百搭" --audience "通勤女性" --style "亲切种草" --category fashion

    python3 generate.py --help
"""

import argparse
import json
import sys
import random
import datetime
from typing import Optional

# ── Note Generation Templates ────────────────────────────────────────

TITLE_TEMPLATES = {
    "数字型": [
        "{product}的{benefit}个秘密，第{num}个没人告诉你",
        "{num}周用了{product}，{result}简直离谱",
        "花{price}块买{product}，效果堪比{compare}",
    ],
    "痛点型": [
        "别再{pain}了！试试{product}吧",
        "谁还在{problem}？{product}真的救了我",
        "{problem}的姐妹看过来，{product}就是答案",
    ],
    "好奇型": [
        "为什么{group}都在偷偷用{product}？",
        "没人告诉你吗？{product}{benefit}很简单",
        "被问爆了！{product}真的{result}",
    ],
    "情感型": [
        "用了{product}后，我终于{result}了",
        "{product}，{emotion}的救星",
        "真心安利给所有{group}，{product}太值得了",
    ],
    "对比型": [
        "以前{old_state}，现在{new_state}，全靠{product}",
        "{product} VS 其他，区别一目了然",
        "换了{product}才发现，以前都在浪费钱",
    ],
}

# ── Style to Template Mapping (Q1 fix) ──────────────────────────────

STYLE_TEMPLATE_MAP = {
    "亲切种草": ["数字型", "情感型", "对比型"],
    "干货分享": ["数字型", "痛点型", "好奇型"],
    "测评对比": ["对比型", "数字型", "好奇型"],
    "开箱体验": ["好奇型", "情感型", "数字型"],
    "Vlog文案": ["情感型", "好奇型", "数字型"],
    "教程攻略": ["数字型", "痛点型", "情感型"],
}

STYLE_LABEL_MAP = {
    "亲切种草": ["数字型·痛点直击", "情感型·共鸣种草", "对比型·效果冲击"],
    "干货分享": ["数字型·干货分享", "痛点型·解决问题", "好奇型·引人深思"],
    "测评对比": ["对比型·效果对比", "数字型·数字说话", "好奇型·真相揭秘"],
    "开箱体验": ["好奇型·开箱惊喜", "情感型·真实感受", "数字型·开箱实测"],
    "Vlog文案": ["情感型·日常Vlog", "好奇型·生活记录", "数字型·我的日常"],
    "教程攻略": ["数字型·实用教程", "痛点型·手把手教", "情感型·学完真香"],
}

# ── Body Templates ───────────────────────────────────────────────────

def build_body_beauty(topic: str, points: list, audience: str, category: str = None) -> str:
    """Build a beauty/skincare note body."""
    pain = random.choice([
        "熬夜后脸又黄又干😭",
        "换季时候皮肤状态差到不想照镜子😩",
        "素颜完全出不了门，气色差到离谱",
    ])
    product_appear = random.choice([
        f"最近挖到了{topic}，之前完全不知道它这么好用！",
        f"也是被姐妹安利的{topic}，一试就停不下来",
        f"抱着试试的心态入了{topic}，结果真香了",
    ])
    experience = random.choice([
        f"质地像精华一样润，拍两遍脸就软软嫩嫩的",
        f"抹上去凉凉的，嗖一下就吸收了，完全不黏",
        f"味道是淡淡的{random_choice(['玫瑰', '植物', '清新', '果香'])}味，每次用都很治愈",
    ])
    result = random.choice([
        f"坚持了一周，早上照镜子明显感觉脸亮了",
        f"用了三天，化妆都不卡粉了！",
        f"皮肤状态稳定了好多，泛红都少了",
    ])
    skeptic = random.choice([
        f"敏感肌亲测不刺痛，成分很干净",
        f"无酒精无香精，烂脸期用也没问题",
        f"查了成分表，都是温和有效的成分",
    ])
    cta = random.choice([
        f"姐妹们真的可以试试！评论区告诉我你的肤质",
        f"你是什么肤质？评论区聊聊",
        f"已经回购第二瓶了！你们还有什么好推荐？",
    ])

    body = f"""{pain}
{product_appear}
{experience}
{result}
{skeptic}
现在化妆前用它打底，底妆都服帖很多！
{cta}"""
    return body


def build_body_food(topic: str, points: list, audience: str, category: str = "food") -> str:
    """Build a food/restaurant review body."""
    location_hint = f"📍 {random_choice(['藏在巷子里', '商场负一层', '街角不起眼'])}"
    price_note = points[-1] if any("人均" in p for p in points) else "💰 性价比超高"
    highlights = "\n".join([f"✅ {p}" for p in points[:3]])

    # Detect city from topic (B2 fix)
    city = "这里"
    for known_city in KNOWN_CITIES:
        if known_city in topic:
            city = known_city
            break

    # Dynamic inline hashtags based on city/category (B2 fix)
    city_tag = f"#{city}探店" if city != "这里" else "#探店"
    food_tag = "#美食推荐"
    if "烧肉" in topic:
        food_tag = "#日式烧肉"
    elif "火锅" in topic:
        food_tag = "#火锅"
    elif "咖啡" in topic or "奶茶" in topic:
        food_tag = "#咖啡探店"
    elif "甜品" in topic:
        food_tag = "#甜品"

    body = f"""{location_hint}，氛围感已经赢了一半
店内灯光暖黄，很适合约会聊天
说说出品：

{highlights}

服务员很贴心，会帮你掌握火候
整体来说，如果是{'约会' if '约会' in str(points) else '朋友聚会'}来的话，绝对不踩雷！

{price_note}
{city_tag} {food_tag}
💬 有人去过这家吗？评论区聊聊体验"""
    return body


def build_body_fashion(topic: str, points: list, audience: str, category: str = None) -> str:
    """Build a fashion/outfit body."""
    body_type = random_choice(["梨形身材", "小个子", "微胖", "苹果身材"])
    pain_phrases = {
        "梨形身材": "找到一条合适的裤子比找对象还难",
        "小个子": "每次买裤子都要改裤长，心累",
        "微胖": "显瘦又舒适的衣服真的太难淘了",
        "苹果身材": "腰腹有肉的我，选衣服很谨慎",
    }
    pain = pain_phrases.get(body_type, "找到合适的单品真的不容易")

    body = f"""本{body_type}终于找到命定{topic}了！
{pain}😩
但是！这条真的很🉑
{' '.join([f'✅ {p}' for p in points[:3]])}
上班搭衬衫，周末搭背心都好看
已经入了第二条换着穿！

你觉得怎么样？评论区告诉我你的身材焦虑👇"""
    return body


GENERIC_BODIES = {
    "beauty": build_body_beauty,
    "fashion": build_body_fashion,
    "food": build_body_food,
}


# ── Known Cities (B2 fix) ───────────────────────────────────────────

KNOWN_CITIES = [
    "上海", "北京", "广州", "深圳", "杭州", "成都", "重庆", "武汉",
    "西安", "南京", "苏州", "长沙", "天津", "厦门", "青岛", "大连",
    "昆明", "三亚", "丽江", "大理", "珠海", "佛山", "宁波", "郑州",
    "沈阳", "哈尔滨", "海口", "贵阳", "兰州", "桂林", "无锡", "常州",
    "香港", "澳门", "台北",
]


def build_body_generic(topic: str, points: list, audience: str, category: str = None) -> str:
    """Fallback body generator for any category."""
    pain = "最近一直被这个问题困扰😩"
    return f"""{pain}
直到发现了{topic}，真的打开了新世界！
{'、'.join(points[:3])}，每一个都让我很满意
用了一段时间，效果比我预期的还好

还在犹豫的朋友可以放心冲
有问题评论区问我👇"""


# ── Hashtag Generators ──────────────────────────────────────────────

HASHTAG_LIBRARY = {
    "beauty": ["护肤", "美妆", "变美", "素颜", "好皮肤", "敏感肌", "补水保湿",
               "精华水", "成分党", "熬夜护肤", "精简护肤", "护肤品推荐",
               "空瓶记", "我的护肤日常", "安利一个护肤品"],
    "fashion": ["穿搭", "穿搭分享", "显瘦穿搭", "OOTD", "日常穿搭",
                "梨形身材", "小个子穿搭", "通勤穿搭", "阔腿裤", "连衣裙",
                "百搭单品", "基础款", "平价穿搭", "上班穿什么"],
    "food": ["美食", "探店", "美食探店", "我的美食日记", "宝藏店铺",
             "约会餐厅", "氛围感餐厅", "性价比", "魔都美食", "周末去哪儿"],
    "travel": ["旅行", "旅行攻略", "旅游", "周末去哪儿", "小众景点",
               "度假", "民宿", "城市漫步", "周边游"],
    "lifestyle": ["好物分享", "好物推荐", "生活方式", "日常", "家居",
                  "幸福感好物", "提升幸福感", "收纳整理"],
    "digital": ["数码好物", "数码", "好物分享", "生产力工具", "提升效率"],
    "fitness": ["健身", "运动", "减肥", "减脂", "瑜伽", "自律生活"],
    "mom": ["母婴", "育儿", "宝宝", "妈妈", "新手妈妈", "母婴好物"],
    "pet": ["宠物", "猫", "狗", "萌宠", "养猫经验分享", "铲屎官"],
    "education": ["学习", "自律", "读书", "学习打卡", "学习方法"],
}


def pick_hashtags(category: str, topic: str, count: int = 7) -> list:
    """Pick hashtags from the library, always including topic-related tags.

    Extracts topic-level hashtags (not character-level, B1 fix).
    """
    pool = HASHTAG_LIBRARY.get(category, HASHTAG_LIBRARY["lifestyle"])[:]
    random.shuffle(pool)

    # Extract topic-derived hashtags at word level (B1 fix)
    topic_tags = []
    clean_topic = topic.strip()
    if len(clean_topic) >= 2:
        topic_tags.append(clean_topic)

    # Split on common delimiters for multi-word topics
    for sep in [' ', ',', '，', '/', '、', '·']:
        if sep in clean_topic:
            parts = [p.strip() for p in clean_topic.split(sep) if len(p.strip()) >= 2]
            topic_tags.extend(parts)
            break

    # Deduplicate while preserving order
    seen = set()
    unique_tags = []
    for tag in topic_tags:
        if tag not in seen:
            seen.add(tag)
            unique_tags.append(tag)

    selected = (unique_tags[:2] + pool)[:count]
    return selected


# ── Cover Tips ──────────────────────────────────────────────────────

COVER_TIPS = {
    "beauty": [
        {"description": "手拿产品对光拍摄，背景干净桌面",
         "composition": "Top-down flat lay or hand holding product in natural window light",
         "text_overlay": "熬夜脸有救了"},
        {"description": "护肤品空瓶排列，展示使用痕迹",
         "composition": "Flat lay of empty bottles in a row, warm lighting",
         "text_overlay": "空瓶才有说服力"},
    ],
    "fashion": [
        {"description": "全身穿搭照，自然光，突出裤型",
         "composition": "Full-body mirror shot in daylight, phone at chin height",
         "text_overlay": "梨形身材必买"},
        {"description": "上衣+裤子挂在一起展示搭配",
         "composition": "Outfit laid flat on bed or hanging on rack",
         "text_overlay": "通勤一周不重样"},
    ],
    "food": [
        {"description": "烤架上和牛特写，火焰微光",
         "composition": "Close-up of food cooking, steam/mist visible, warm backlight",
         "text_overlay": "人均200吃和牛"},
        {"description": "餐厅环境氛围感照片",
         "composition": "Wide shot of restaurant interior, candlelight on table",
         "text_overlay": "约会氛围感满分"},
    ],
}

DEFAULT_COVER = [
    {"description": "高颜值产品近景特写，配简洁文字",
     "composition": "Close-up hero shot, centered, clean background",
     "text_overlay": "亲测好用"},
    {"description": "使用场景自然抓拍",
     "composition": "Lifestyle candid shot in natural setting",
     "text_overlay": "提升幸福感的好物"},
    {"description": "对比图——左右或上下对比",
     "composition": "Side-by-side before/after split image",
     "text_overlay": "区别一目了然"},
]


def pick_cover(category: str) -> dict:
    tips = COVER_TIPS.get(category, DEFAULT_COVER)
    return random.choice(tips)


# ── Publish Time Suggestions ────────────────────────────────────────

PUBLISH_TIMES = {
    "beauty":    ["20:00-22:00", "12:00-13:00", "21:00-23:00"],
    "fashion":   ["12:00-13:00", "20:00-22:00", "08:00-09:00"],
    "food":      ["17:30-19:00", "11:30-13:00", "20:00-21:30"],
    "travel":    ["20:00-22:00", "10:00-11:00", "14:00-15:00"],
    "lifestyle": ["20:00-22:00", "12:00-13:00", "21:00-22:00"],
    "digital":   ["20:00-22:00", "12:00-13:00", "22:00-23:00"],
    "fitness":   ["06:00-07:00", "19:00-20:00", "21:00-22:00"],
    "mom":       ["13:00-14:00", "21:00-22:00", "10:00-11:00"],
    "pet":       ["20:00-22:00", "12:00-13:00", "19:00-20:00"],
    "education": ["20:00-22:00", "07:00-08:00", "22:00-23:00"],
}


def pick_publish_time(category: str) -> str:
    times = PUBLISH_TIMES.get(category, ["20:00-22:00"])
    return random.choice(times)


# ── Utility ─────────────────────────────────────────────────────────

def random_choice(items):
    return random.choice(items)


def generate_title_variant(topic: str, points: list, style_label: str, variant_index: int) -> str:
    """Generate one title for a note variant."""
    title_pool = TITLE_TEMPLATES.get(style_label, TITLE_TEMPLATES["痛点型"])
    template = random.choice(title_pool)

    replacements = {
        "product": topic,
        "benefit": points[0] if points else "好用",
        "num": str(random.randint(1, 5)),
        "result": random_choice(["效果明显", "变化惊人", "彻底爱上", "停不下来"]),
        "price": random_choice(["19.9", "30", "50", "100", "200", "300"]),
        "compare": random_choice(["大牌", "千元级", "医美", "贵妇品牌"]),
        "pain": random_choice(["乱花钱", "踩雷", "盲目跟风", "无效护肤"]),
        "problem": random_choice(["皮肤暗沉", "脸干到起皮", "妆不持久"]),
        "group": random_choice(["学生党", "上班族", "敏感肌", "成分党"]),
        "emotion": random_choice(["熬夜党", "懒人", "手残党", "吃土女孩"]),
        "old_state": random_choice(["盲目跟风", "乱买一通", "浪费了好多钱"]),
        "new_state": random_choice(["精准种草", "每一分都花对了", "找到了真爱"]),
    }

    title = template.format(**replacements)

    # Add emoji prefix
    emojis = ["💧", "✨", "🔥", "💖", "😱", "🥹", "🆘", "🙏", "🤯", "💯", "🌟", "⚡"]
    emoji = emojis[(variant_index + len(topic)) % len(emojis)]

    # Truncate at word boundary (B3 fix: avoid splitting compound words)
    if len(title) > 25:
        BREAK_CHARS = set(' \t\n\r,.!?;:，。！？；：)）」』》〉“”‘’…—·、（「『《〈的了和在就有都很是也不可以没戴哦')
        # Common 2-char Chinese compounds that should not be split
        COMPOUND_WORDS = {
            "简单", "方法", "推荐", "护肤",
            "保养", "真的", "效果", "明显",
            "变化", "彻底", "不会", "这个",
            "感觉", "喜欢", "需要", "应该",
            "一下", "一点", "一些", "一个",
            "产品", "成分", "品牌", "价格",
            "精华", "面霜", "夺回", "白居",
            "适合", "体验", "感受", "分享",
            "种草", "对比", "测试", "搭配",
            "品质", "版型", "颜色", "口感",
            "环境", "服务", "份量", "特色",
            "探店", "美食", "咖啡", "甜品",
            "火锅", "烧肉", "简直", "收藏",
            "回购", "攻略", "教程", "妆容",
        }
        boundary = -1
        for j in range(min(len(title) - 1, 24), max(19, 0), -1):
            if title[j] in BREAK_CHARS:
                boundary = j + 1
                break
        if boundary > 0:
            title = title[:boundary] + "\u2026"
        else:
            # Check for compound word split at the boundary (B3 improvement)
            if len(title) >= 25 and title[23:25] in COMPOUND_WORDS:
                title = title[:23] + "\u2026"
            elif len(title) >= 25 and title[22:24] in COMPOUND_WORDS:
                title = title[:24] + "\u2026"
            else:
                title = title[:24] + "\u2026"
    return f"{emoji} {title}"


# ── Main Generator ──────────────────────────────────────────────────

def generate_notes(
    topic: str,
    selling_points: Optional[list] = None,
    target_audience: str = "通用人群",
    style: str = "亲切种草",
    category: str = "other",
    count: int = 3,
    include_disclaimer: bool = False,
) -> dict:
    """Generate `count` Xiaohongshu note variants."""

    if selling_points is None or len(selling_points) == 0:
        selling_points = [f"{topic}推荐"]

    points = selling_points[:5]
    body_builder = GENERIC_BODIES.get(category, build_body_generic)

    # Use style-driven template/label selection (Q1 fix)
    style_labels = STYLE_LABEL_MAP.get(style, ["数字型·痛点直击", "情感型·共鸣种草", "对比型·效果冲击"])
    style_keys = STYLE_TEMPLATE_MAP.get(style, ["数字型", "情感型", "对比型"])

    notes = []
    for i in range(count):
        style_label = style_labels[i % len(style_labels)]
        style_key = style_keys[i % len(style_keys)]

        title = generate_title_variant(topic, points, style_key, i)
        body = body_builder(topic, points, target_audience, category=category)

        hashtags = pick_hashtags(category, topic, count=random.randint(6, 9))
        cover = pick_cover(category)
        pub_time = pick_publish_time(category)

        note = {
            "note_number": i + 1,
            "style_label": style_label,
            "title": title,
            "body": body.strip(),
            "hashtags": hashtags,
            "cover_tip": cover,
            "publish_time": pub_time,
        }
        notes.append(note)

    metadata = {
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "total_notes": count,
        "input_topic": topic,
        "style": style,
        "target_audience": target_audience,
    }

    if include_disclaimer:
        metadata["disclaimer"] = (
            "⚠️ 本文内容仅供参考，不构成医疗建议或购买建议。"
            "产品效果因人而异，请根据自身情况理性选择。"
        )

    return {"notes": notes, "metadata": metadata}


# ── CLI Entry Point ────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="📕 Xiaohongshu Note Booster — Generate viral XHS notes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 generate.py --topic "玫瑰精华水" --selling-points "补水保湿,提亮肤色,敏感肌可用" --audience "18-30岁女性" --category beauty
  python3 generate.py --topic "白色阔腿裤" --selling-points "显瘦,垂坠感好,百搭" --audience "通勤女性" --category fashion
  python3 generate.py --topic "上海静安寺日式烧肉" --selling-points "和牛入口即化,环境适合约会,人均200" --category food
  python3 generate.py --topic "MacBook Air M4" --selling-points "轻薄,续航强,性能提升" --audience "学生党" --category digital --include-disclaimer
        """
    )

    parser.add_argument("--topic", required=True, help="Product name, scene, or topic")
    parser.add_argument("--selling-points", help="Comma-separated selling points")
    parser.add_argument("--audience", default="通用人群", help="Target audience")
    parser.add_argument("--style", default="亲切种草",
                        choices=["亲切种草", "干货分享", "测评对比",
                                 "开箱体验", "Vlog文案", "教程攻略"],
                        help="Writing style")
    parser.add_argument("--category", default="other",
                        choices=["beauty", "fashion", "food", "travel",
                                 "lifestyle", "digital", "fitness", "mom",
                                 "pet", "education", "other"],
                        help="Content category")
    parser.add_argument("--count", type=int, default=3, choices=[1, 2, 3, 4, 5],
                        help="Number of note variants")
    parser.add_argument("--include-disclaimer", action="store_true",
                        help="Include compliance disclaimer")
    parser.add_argument("--output", help="Output file path (default: stdout)")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")

    args = parser.parse_args()

    points = [p.strip() for p in args.selling_points.split(",")] if args.selling_points else None

    result = generate_notes(
        topic=args.topic,
        selling_points=points,
        target_audience=args.audience,
        style=args.style,
        category=args.category,
        count=args.count,
        include_disclaimer=args.include_disclaimer,
    )

    output = json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"✅ Notes saved to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    # Deterministic-ish seed for reproducibility
    random.seed()
    main()
