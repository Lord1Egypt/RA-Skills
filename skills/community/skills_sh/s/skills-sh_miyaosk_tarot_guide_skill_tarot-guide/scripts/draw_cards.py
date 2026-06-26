#!/usr/bin/env python3
"""塔罗牌抽牌脚本 - 生成牌池供用户选择，根据用户选号揭示牌面，附带牌面图片。"""

import argparse
import json
import random
import re
import sys
from pathlib import Path

POOL_SIZE = 78
WIKI_BASE = "https://commons.wikimedia.org/wiki/Special:FilePath"

SPREAD_CONFIG = {
    "single": {
        "count": 1,
        "modes": {
            "daily": ["今日指引"],
            "yesno": ["是或否"],
        },
        "default_mode": "daily",
    },
    "three": {
        "count": 3,
        "modes": {
            "time": ["过去", "现在", "未来"],
            "problem": ["处境", "挑战", "建议"],
            "psyche": ["意识", "潜意识", "指引"],
            "holistic": ["身体", "心理", "灵性"],
            "relationship": ["你", "对方", "关系走向"],
            "choice": ["选项A", "选项B", "建议"],
            "growth": ["该保留的", "该放下的", "该学习的"],
        },
        "default_mode": "time",
    },
    "five": {
        "count": 5,
        "modes": {
            "timeline": ["远过去", "近过去", "现在", "近未来", "远未来"],
            "cross": ["主题", "障碍", "过去影响", "未来趋势", "核心建议"],
            "element": ["火·行动", "水·情感", "风·思维", "土·物质", "灵·指引"],
        },
        "default_mode": "timeline",
    },
}

MAJOR_IMAGE_NAMES = {
    0: "RWS_Tarot_00_Fool.jpg",
    1: "RWS_Tarot_01_Magician.jpg",
    2: "RWS_Tarot_02_High_Priestess.jpg",
    3: "RWS_Tarot_03_Empress.jpg",
    4: "RWS_Tarot_04_Emperor.jpg",
    5: "RWS_Tarot_05_Hierophant.jpg",
    6: "RWS_Tarot_06_Lovers.jpg",
    7: "RWS_Tarot_07_Chariot.jpg",
    8: "RWS_Tarot_08_Strength.jpg",
    9: "RWS_Tarot_09_Hermit.jpg",
    10: "RWS_Tarot_10_Wheel_of_Fortune.jpg",
    11: "RWS_Tarot_11_Justice.jpg",
    12: "RWS_Tarot_12_Hanged_Man.jpg",
    13: "RWS_Tarot_13_Death.jpg",
    14: "RWS_Tarot_14_Temperance.jpg",
    15: "RWS_Tarot_15_Devil.jpg",
    16: "RWS_Tarot_16_Tower.jpg",
    17: "RWS_Tarot_17_Star.jpg",
    18: "RWS_Tarot_18_Moon.jpg",
    19: "RWS_Tarot_19_Sun.jpg",
    20: "RWS_Tarot_20_Judgement.jpg",
    21: "RWS_Tarot_21_World.jpg",
}

SUIT_IMAGE_PREFIX = {
    "wands": "Wands",
    "cups": "Cups",
    "swords": "Swords",
    "pentacles": "Pents",
}

WANDS09_FILENAME = "Tarot_Nine_of_Wands.jpg"


def get_image_url(suit: str, number: int) -> str:
    if suit == "major":
        filename = MAJOR_IMAGE_NAMES[number]
    elif suit == "wands" and number == 9:
        filename = WANDS09_FILENAME
    else:
        prefix = SUIT_IMAGE_PREFIX[suit]
        filename = f"{prefix}{number:02d}.jpg"
    return f"{WIKI_BASE}/{filename}"


def load_cards(json_path: Path) -> list[dict]:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cards = list(data["major_arcana"])
    for suit_cards in data["minor_arcana"].values():
        cards.extend(suit_cards)
    return cards


def parse_picks(raw: str, pool_size: int, count: int) -> tuple[list[int], bool]:
    """从用户输入中提取数字，返回 (选中的索引列表, 是否为用户有效选择)。

    任何分隔符都行，只提取数字。如果数字不合法则随机补位。
    """
    numbers = [int(x) for x in re.findall(r"\d+", raw)]

    valid = [n for n in numbers if 1 <= n <= pool_size]
    seen = set()
    deduped = []
    for n in valid:
        if n not in seen:
            seen.add(n)
            deduped.append(n)

    if len(deduped) == count:
        return [n - 1 for n in deduped], True

    available = [i + 1 for i in range(pool_size) if (i + 1) not in seen]
    random.shuffle(available)
    while len(deduped) < count and available:
        deduped.append(available.pop())

    return [n - 1 for n in deduped], False


def main():
    parser = argparse.ArgumentParser(description="塔罗牌抽牌")
    parser.add_argument(
        "--spread",
        choices=["single", "three", "five"],
        default="single",
        help="牌阵类型: single(1牌), three(3牌), five(5牌)",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default=None,
        help="牌阵模式（如 time, problem, psyche, holistic, relationship, choice, growth, timeline, cross, element, daily, yesno）",
    )
    parser.add_argument(
        "--picks",
        type=str,
        default=None,
        help="用户输入的选牌内容（任意分隔符，脚本自动提取数字）",
    )
    args = parser.parse_args()

    assets_dir = Path(__file__).resolve().parent.parent / "assets"
    json_path = assets_dir / "cards.json"

    if not json_path.exists():
        print(json.dumps({"error": f"找不到牌库文件: {json_path}"}, ensure_ascii=False))
        sys.exit(1)

    cards = load_cards(json_path)
    config = SPREAD_CONFIG[args.spread]
    pool_size = POOL_SIZE
    count = config["count"]

    pool = cards[:]
    random.shuffle(pool)

    user_valid = True
    if args.picks:
        pick_indices, user_valid = parse_picks(args.picks, pool_size, count)
        selected = [pool[i] for i in pick_indices]
        picked_numbers = [i + 1 for i in pick_indices]
    else:
        indices = random.sample(range(pool_size), count)
        selected = [pool[i] for i in indices]
        picked_numbers = [i + 1 for i in indices]
        user_valid = False

    for card in selected:
        card["reversed"] = random.choice([True, False])
        card["orientation"] = "逆位" if card["reversed"] else "正位"

    mode = args.mode or config["default_mode"]
    if mode not in config["modes"]:
        mode = config["default_mode"]
    positions = config["modes"][mode]

    result = {
        "spread": args.spread,
        "mode": mode,
        "pool_size": pool_size,
        "picked_numbers": picked_numbers,
        "user_valid": user_valid,
        "cards": [],
    }

    for i, card in enumerate(selected):
        result["cards"].append({
            "position": positions[i],
            "id": card["id"],
            "name_en": card["name_en"],
            "name_cn": card["name_cn"],
            "suit": card["suit"],
            "number": card["number"],
            "orientation": card["orientation"],
            "reversed": card["reversed"],
            "image_url": get_image_url(card["suit"], card["number"]),
        })

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
