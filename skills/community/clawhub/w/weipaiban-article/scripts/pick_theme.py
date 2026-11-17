#!/usr/bin/env python3
"""抽取作品主题与版面语法。

LLM 自行「随机挑」会偏向清单前排。本脚本收拢决策：

- --list：完整清单，不写历史
- --recommend：按 query/category/grammar 打分，输出主推 + 备选，不写历史
- --theme：用户确认后锁定，写历史
- 无参数：兼容旧调用，全库随机（避开最近用过的）并写历史

改动需与 themes/theme-index.md 同步。

用法：

    python3 pick_theme.py --list
    python3 pick_theme.py --recommend --query "小满 茶道"
    python3 pick_theme.py --theme neo-chinese --grammar 叙事流 --category 节气
    python3 pick_theme.py --no-history
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
import time

THEMES = [
    {
        "id": "moyu-green",
        "name": "摸鱼绿",
        "primary": "#059669",
        "accent": "#EAB308",
        "canvas": "#F7FBF8",
        "text": "#3F3F3F",
        "grammars": ["章节流", "卡片流"],
        "categories": ["教育", "科技", "节气", "开学季", "报告", "环保"],
        "keywords": ["教育", "开学", "环保", "科普", "清新", "杂志绿"],
        "avoid": ["电竞", "赛博", "党政", "非遗", "茶道"],
        "oneLiner": "清新杂志感",
        "family": "classic",
        "styleAnchor": "清新杂志摄影，翠绿与暖黄点缀，信息密度偏高，干净纸面",
        "lightingHint": "明亮散射光，轻微纸感",
        "related": ["graphite-minimal", "glassmorphism"],
    },
    {
        "id": "red-white",
        "name": "红白",
        "primary": "#DC2626",
        "accent": "#991B1B",
        "canvas": "#FAF7F5",
        "text": "#3F3F3F",
        "grammars": ["章节流", "叙事流"],
        "categories": ["党政", "建党节", "春节", "人物", "报告", "邀请函"],
        "keywords": ["党政", "建党", "春节", "邀请函", "庄重", "仪式"],
        "avoid": ["电竞", "美妆", "赛博", "手账"],
        "oneLiner": "庄重编辑风",
        "family": "classic",
        "styleAnchor": "庄重编辑摄影，正红克制点睛，暖白纸面，仪式感",
        "lightingHint": "均匀室内光，低对比阴影",
        "related": ["editorial-serif", "olive-journal"],
    },
    {
        "id": "graphite-minimal",
        "name": "石墨极简",
        "primary": "#52525B",
        "accent": "#F97316",
        "canvas": "#FAFAFA",
        "text": "#3F3F3F",
        "grammars": ["章节流", "对照流"],
        "categories": ["科技", "金融", "招聘", "会议", "媒体", "报告"],
        "keywords": ["金融", "招聘", "会议", "商务", "媒体", "灰阶", "极简商务"],
        "avoid": ["节气", "茶道", "电竞", "手账", "美妆"],
        "oneLiner": "理性灰阶",
        "family": "classic",
        "styleAnchor": "理性灰阶，极简商务摄影，冷中性色，暖橙点睛，大留白",
        "lightingHint": "柔和顶光，几乎无色偏",
        "related": ["swiss-minimal", "moyu-green"],
    },
    {
        "id": "zen-whitespace",
        "name": "留白禅意",
        "primary": "#4A5D52",
        "accent": "#C9A961",
        "canvas": "#FAF8F2",
        "text": "#4F5B52",
        "grammars": ["叙事流"],
        "categories": ["文学", "节气", "环保", "医疗健康", "邀请函"],
        "keywords": ["文学", "散文", "禅意", "留白", "医疗", "呼吸感", "母亲节"],
        "avoid": ["电竞", "赛博", "促销", "电商", "大模型"],
        "oneLiner": "东方呼吸感",
        "family": "classic",
        "styleAnchor": "东方留白，墨绿细线与枯叶金点缀，散文呼吸感，宣纸暖白",
        "lightingHint": "窗边柔光，大面积负空间",
        "related": ["neo-chinese", "olive-journal"],
    },
    {
        "id": "olive-journal",
        "name": "橄榄手记",
        "primary": "#1E1F23",
        "accent": "#ED7B2F",
        "canvas": "#FDFDF8",
        "text": "#4D4F46",
        "grammars": ["章节流", "叙事流"],
        "categories": ["报告", "人物", "邀请函", "文学", "毕业季", "节气"],
        "keywords": ["内刊", "毕业", "手记", "人物", "温度"],
        "avoid": ["电竞", "赛博", "促销", "美妆"],
        "oneLiner": "内刊温度",
        "family": "classic",
        "styleAnchor": "内刊手记，米纸底与墨色字，橙色点睛，印刷温度",
        "lightingHint": "台灯暖光，纸面微纹理",
        "related": ["collage-journal", "zen-whitespace"],
    },
    {
        "id": "moyu-ticket",
        "name": "摸鱼票据",
        "primary": "#059669",
        "accent": "#F59E0B",
        "canvas": "#FFFEF7",
        "text": "#3F3F3F",
        "grammars": ["卡片流", "对照流"],
        "categories": ["电商", "餐饮", "娱乐", "邀请函", "测评"],
        "keywords": ["测评", "电商", "餐饮", "娱乐", "门票", "对照"],
        "avoid": ["党政", "非遗", "茶道", "深度报道"],
        "oneLiner": "趣味卡片",
        "family": "classic",
        "styleAnchor": "门票票据拼贴，墨色描边与硬阴影，翠绿编号，趣味信息卡",
        "lightingHint": "平光，边缘清晰，轻微纸票质感",
        "related": ["collage-journal", "moyu-green"],
    },
    {
        "id": "neo-chinese",
        "name": "新中式",
        "primary": "#2C3E38",
        "accent": "#B03A2E",
        "canvas": "#FAF8F2",
        "text": "#33332E",
        "grammars": ["章节流", "叙事流"],
        "categories": ["节气", "文学", "邀请函"],
        "keywords": [
            "文化",
            "茶道",
            "香道",
            "文旅",
            "非遗",
            "诗词",
            "国风",
            "宋式",
            "水墨",
            "博物馆",
            "中式",
            "器物",
        ],
        "avoid": ["电竞", "赛博", "促销", "大模型", "美妆"],
        "oneLiner": "宋式留白 / 水墨淡彩 / 竖排印章",
        "family": "trend",
        "styleAnchor": "宋式宣纸肌理，水墨淡彩，暖墨与朱砂点缀，计白当黑",
        "lightingHint": "侧窗柔光，纸面微纹理，低饱和",
        "related": ["zen-whitespace", "olive-journal"],
    },
    {
        "id": "glassmorphism",
        "name": "弥散光感",
        "primary": "#7C6CBF",
        "accent": "#E88A8A",
        "canvas": "#F3F0F7",
        "text": "#3D3A4A",
        "grammars": ["卡片流"],
        "categories": ["科技", "医疗健康"],
        "keywords": [
            "科技产品",
            "效率工具",
            "美妆",
            "护肤",
            "生活方式",
            "产品发布",
            "设计灵感",
            "职场",
            "轻卡片",
        ],
        "avoid": ["党政", "非遗", "茶道", "电竞"],
        "oneLiner": "半透明浅卡 / 低饱和渐变",
        "family": "trend",
        "styleAnchor": "柔和弥散渐变，雾面玻璃质感，低饱和紫粉与冷灰蓝",
        "lightingHint": "漫射顶光，浅景深，干净高光",
        "related": ["moyu-green", "cyber-dark"],
    },
    {
        "id": "cyber-dark",
        "name": "暗黑霓虹",
        "primary": "#00E5FF",
        "accent": "#FF2D95",
        "canvas": "#141A2E",
        "text": "#B8E8EC",
        "grammars": ["卡片流"],
        "categories": ["科技", "娱乐"],
        "keywords": [
            "AI",
            "大模型",
            "数码",
            "3C",
            "电竞",
            "游戏",
            "赛博",
            "加密",
            "潮流街头",
            "先锋",
            "科幻",
        ],
        "avoid": ["茶道", "非遗", "节气", "党政", "医疗"],
        "oneLiner": "有彩色深底 / 荧光点缀",
        "family": "trend",
        "styleAnchor": "赛博深靛空间，电光青与霓虹粉点缀，冷金属与屏幕高光",
        "lightingHint": "边缘轮廓光，暗部干净，荧光只点不铺",
        "related": ["glassmorphism", "graphite-minimal"],
    },
    {
        "id": "editorial-serif",
        "name": "杂志编辑",
        "primary": "#1A1A2E",
        "accent": "#C4903C",
        "canvas": "#FAF9F5",
        "text": "#2D2D3A",
        "grammars": ["章节流", "叙事流"],
        "categories": ["人物", "文学", "媒体", "报告", "金融"],
        "keywords": [
            "深度报道",
            "专访",
            "文化评论",
            "品牌故事",
            "财经深度",
            "杂志",
            "长文",
        ],
        "avoid": ["促销", "电竞", "手账", "开学"],
        "oneLiner": "衬线大字 / 隐形网格",
        "family": "trend",
        "styleAnchor": "纸质杂志摄影，隐形网格构图，暖白纸与古铜色点缀",
        "lightingHint": "窗边自然光，柔和阴影，印刷纸质感",
        "related": ["olive-journal", "swiss-minimal"],
    },
    {
        "id": "collage-journal",
        "name": "拼贴手账",
        "primary": "#3D3A35",
        "accent": "#D4624A",
        "canvas": "#FBF8F0",
        "text": "#3D3A35",
        "grammars": ["卡片流", "叙事流"],
        "categories": ["文学", "餐饮", "娱乐"],
        "keywords": [
            "旅行",
            "游记",
            "手账",
            "书店",
            "手作",
            "文创",
            "播客",
            "读书",
            "咖啡",
            "烘焙",
            "生活方式",
            "随笔",
        ],
        "avoid": ["党政", "金融", "年报", "电竞", "大模型"],
        "oneLiner": "纸纹拼贴 / 胶带手感",
        "family": "trend",
        "styleAnchor": "牛皮纸与胶带拼贴，胶片颗粒，陶土红与墨棕，手作温度",
        "lightingHint": "桌面自然光，轻微阴影，纸纹可见",
        "related": ["olive-journal", "moyu-ticket"],
    },
    {
        "id": "swiss-minimal",
        "name": "极简黑白",
        "primary": "#111111",
        "accent": "#FF3B30",
        "canvas": "#FAFAFA",
        "text": "#1A1A1A",
        "grammars": ["对照流", "章节流"],
        "categories": ["金融", "媒体", "报告", "会议"],
        "keywords": [
            "时尚",
            "艺术",
            "展览",
            "建筑",
            "年度报告",
            "年报",
            "先锋品牌",
            "瑞士",
            "网格",
        ],
        "avoid": ["手账", "碎片", "开学", "节气", "茶道"],
        "oneLiner": "瑞士国际主义 / 近黑近白网格",
        "family": "trend",
        "styleAnchor": "瑞士国际主义，几何网格，高对比黑白摄影，一点信号红",
        "lightingHint": "硬光、利落阴影、博物馆展陈感",
        "related": ["graphite-minimal", "editorial-serif"],
    },
]

THEME_IDS = [t["id"] for t in THEMES]
THEME_BY_ID = {t["id"]: t for t in THEMES}
GRAMMARS = ["叙事流", "章节流", "卡片流", "对照流"]
GRAMMAR_ALIASES = {"模块化": "卡片流"}

SOLAR_TERMS = [
    "立春",
    "雨水",
    "惊蛰",
    "春分",
    "清明",
    "谷雨",
    "立夏",
    "小满",
    "芒种",
    "夏至",
    "小暑",
    "大暑",
    "立秋",
    "处暑",
    "白露",
    "秋分",
    "寒露",
    "霜降",
    "立冬",
    "小雪",
    "大雪",
    "冬至",
    "小寒",
    "大寒",
]

QUERY_EXPAND: dict[str, list[str]] = {
    "大模型": ["AI", "科技"],
    "llm": ["AI", "大模型"],
    "chatgpt": ["AI", "大模型"],
    "人工智能": ["AI", "大模型"],
    "产品发布": ["科技产品", "产品发布"],
    "独立书店": ["书店", "文创"],
    "手帐": ["手账"],
    "中秋": ["节气", "文化"],
    "端午": ["节气", "文化"],
    "重阳": ["节气"],
}
for _term in SOLAR_TERMS:
    QUERY_EXPAND[_term] = ["节气"]

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_HISTORY_FILE = os.path.expanduser(
    "~/.cache/weipaiban-article/theme-history.jsonl"
)
RECENT_WINDOW = 8
EXCLUDE_RECENT = 2


def load_history(path: str) -> list[dict]:
    if not os.path.isfile(path):
        return []
    records: list[dict] = []
    try:
        with open(path, "r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    item = json.loads(line)
                    if isinstance(item, dict):
                        records.append(item)
                except json.JSONDecodeError:
                    continue
    except OSError:
        return []
    return records[-RECENT_WINDOW:]


def append_history(path: str, record: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def pick_excluding(pool: list[str], recent_values: list[str]) -> str:
    recent = recent_values[-EXCLUDE_RECENT:]
    candidates = [item for item in pool if item not in recent]
    if not candidates:
        candidates = [item for item in pool if item not in recent_values[-1:]] or pool
    return random.choice(candidates)


def normalize_grammar(value: str | None) -> str | None:
    if not value:
        return None
    return GRAMMAR_ALIASES.get(value, value)


def tokenize(text: str) -> list[str]:
    if not text:
        return []
    return [part for part in re.split(r"[\s,，、/|]+", text.strip()) if part]


def expand_query(query: str, category: str | None) -> str:
    parts = [query or ""]
    if category:
        parts.append(category)
    blob = " ".join(parts)
    extras: list[str] = []
    for token, mapped in QUERY_EXPAND.items():
        if token.lower() in blob.lower() or token in blob:
            extras.extend(mapped)
            extras.append(token)
    return " ".join([blob, *extras]).strip()


def catalog_item(theme: dict) -> dict:
    return {
        "id": theme["id"],
        "name": theme["name"],
        "family": theme["family"],
        "oneLiner": theme["oneLiner"],
        "grammars": theme["grammars"],
        "categories": theme["categories"],
        "primary": theme["primary"],
        "accent": theme["accent"],
    }


def theme_file_path(theme_id: str) -> str:
    return os.path.join(SKILL_DIR, "themes", f"theme-{theme_id}.md")


def pick_grammar(theme: dict, grammar: str | None) -> str:
    if grammar and grammar in GRAMMARS:
        return grammar
    return theme["grammars"][0]


def pick_category(theme: dict, category: str | None) -> str | None:
    if category:
        return category
    return theme["categories"][0] if theme["categories"] else None


def score_theme(
    theme: dict,
    haystack: str,
    category: str | None,
    grammar: str | None,
    recent_themes: list[str],
) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []

    if category and category in theme["categories"]:
        score += 3
        reasons.append(f"类目「{category}」")
    else:
        cat_hits = [item for item in theme["categories"] if item and item in haystack]
        if cat_hits:
            score += 3
            reasons.append(f"类目「{cat_hits[0]}」")

    keyword_hits = [item for item in theme["keywords"] if item and item in haystack]
    if theme["name"] in haystack or theme["id"] in haystack:
        keyword_hits.append(theme["name"])
    # unique, keep order
    seen: set[str] = set()
    unique_hits: list[str] = []
    for item in keyword_hits:
        if item not in seen:
            seen.add(item)
            unique_hits.append(item)
    if unique_hits:
        score += 2 + min(len(unique_hits) - 1, 2)
        reasons.append("、".join(unique_hits[:3]))

    if grammar and grammar in theme["grammars"]:
        score += 1
        reasons.append(f"语法「{grammar}」")

    avoid_hits = [item for item in theme["avoid"] if item and item in haystack]
    if avoid_hits:
        score -= 4
        reasons.append(f"避开「{avoid_hits[0]}」")

    if theme["id"] in recent_themes[-EXCLUDE_RECENT:]:
        score -= 2

    return score, reasons


def build_reason(theme: dict, reasons: list[str]) -> str:
    if reasons == ["气质相近"]:
        return f"{theme['oneLiner']}；与主推气质相近"
    positive = [item for item in reasons if not item.startswith("避开")]
    if positive:
        return f"{theme['oneLiner']}；命中" + "、".join(positive[:3])
    return theme["oneLiner"]


def lock_result(theme: dict, grammar: str, category: str | None) -> dict:
    theme_file = theme_file_path(theme["id"])
    return {
        "themeId": theme["id"],
        "themeName": theme["name"],
        "primaryColor": theme["primary"],
        "accentColor": theme["accent"],
        "canvasColor": theme["canvas"],
        "textColor": theme["text"],
        "grammar": grammar,
        "category": category,
        "oneLiner": theme["oneLiner"],
        "family": theme["family"],
        "styleAnchor": theme["styleAnchor"],
        "lightingHint": theme["lightingHint"],
        "themeFile": theme_file,
        "supportNote": (
            f"读 {theme_file} 取标题/分割/卡片形态。"
            "字号与边距服从本技能 references/visual-system.md。"
            "辅助 SVG 画布可选；05 主交互本步不写。"
        ),
    }


def pick_alternatives(
    rec_theme: dict,
    ranked: list[tuple[int, dict, list[str]]],
) -> list[tuple[dict, list[str]]]:
    alts: list[tuple[dict, list[str]]] = []
    used = {rec_theme["id"]}

    for score, theme, reasons in ranked:
        if theme["id"] in used or score <= 0:
            continue
        alts.append((theme, reasons))
        used.add(theme["id"])
        if len(alts) >= 2:
            return alts

    for rel_id in rec_theme.get("related", []):
        if rel_id in used or rel_id not in THEME_BY_ID:
            continue
        alts.append((THEME_BY_ID[rel_id], ["气质相近"]))
        used.add(rel_id)
        if len(alts) >= 2:
            return alts

    for _score, theme, reasons in ranked:
        if theme["id"] in used:
            continue
        alts.append((theme, reasons or ["气质相近"]))
        used.add(theme["id"])
        if len(alts) >= 2:
            break
    return alts


def recommend_payload(
    query: str | None,
    category: str | None,
    grammar: str | None,
    recent_themes: list[str],
) -> dict:
    haystack = expand_query(query or "", category)
    ranked: list[tuple[int, dict, list[str]]] = []
    for theme in THEMES:
        score, reasons = score_theme(theme, haystack, category, grammar, recent_themes)
        ranked.append((score, theme, reasons))
    ranked.sort(key=lambda item: (-item[0], item[1]["id"]))

    top_score = ranked[0][0]
    if top_score <= 0:
        chosen_id = pick_excluding(THEME_IDS, recent_themes)
        rec_theme = THEME_BY_ID[chosen_id]
        rec_reasons: list[str] = []
    else:
        rec_theme = ranked[0][1]
        rec_reasons = ranked[0][2]

    alt_pairs = pick_alternatives(rec_theme, ranked)
    alts = [item[0] for item in alt_pairs]
    alt_reasons = [item[1] for item in alt_pairs]

    def pack(theme: dict, reasons: list[str]) -> dict:
        return {
            "themeId": theme["id"],
            "themeName": theme["name"],
            "oneLiner": theme["oneLiner"],
            "family": theme["family"],
            "grammar": pick_grammar(theme, grammar),
            "reason": build_reason(theme, reasons),
            "themeFile": theme_file_path(theme["id"]),
        }

    return {
        "recommended": pack(rec_theme, rec_reasons),
        "alternatives": [
            pack(theme, reasons) for theme, reasons in zip(alts, alt_reasons)
        ],
        "catalog": [catalog_item(theme) for theme in THEMES],
        "query": query,
        "category": category,
        "grammar": grammar,
    }


def list_payload() -> dict:
    return {
        "catalog": [catalog_item(theme) for theme in THEMES],
        "families": {
            "classic": [theme["id"] for theme in THEMES if theme["family"] == "classic"],
            "trend": [theme["id"] for theme in THEMES if theme["family"] == "trend"],
        },
        "grammars": GRAMMARS,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="抽取作品主题与版面语法")
    parser.add_argument("--theme", help="主题 ID，见 --list")
    parser.add_argument("--grammar", help=f"版面语法，可选：{'/'.join(GRAMMARS)}")
    parser.add_argument("--category", help="内容类目；未知类目当作 query 词，不报错")
    parser.add_argument("--query", help="用户原话或场景描述，供 --recommend 打分")
    parser.add_argument(
        "--list", action="store_true", help="输出完整主题清单，不写历史"
    )
    parser.add_argument(
        "--recommend",
        action="store_true",
        help="输出主推 + 备选 + 清单，不写历史",
    )
    parser.add_argument("--history-file", default=DEFAULT_HISTORY_FILE)
    parser.add_argument("--no-history", action="store_true")
    args = parser.parse_args()

    grammar = normalize_grammar(args.grammar)
    if grammar and grammar not in GRAMMARS:
        print(f"错误：--grammar「{args.grammar}」不在合法语法清单内", file=sys.stderr)
        print(f"合法值：{', '.join(GRAMMARS)}", file=sys.stderr)
        return 2
    if args.theme and args.theme not in THEME_IDS:
        print(f"错误：--theme「{args.theme}」不在合法主题清单内", file=sys.stderr)
        print(f"合法值：{', '.join(THEME_IDS)}", file=sys.stderr)
        return 2

    history = [] if args.no_history else load_history(args.history_file)
    recent_themes = [
        record["themeId"]
        for record in history
        if isinstance(record.get("themeId"), str)
    ]

    if args.list:
        print(json.dumps(list_payload(), ensure_ascii=False, indent=2))
        return 0

    if args.recommend:
        payload = recommend_payload(args.query, args.category, grammar, recent_themes)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    if args.theme:
        theme_id = args.theme
    elif args.category:
        haystack = expand_query(args.query or "", args.category)
        ranked = []
        for theme in THEMES:
            score, _reasons = score_theme(
                theme, haystack, args.category, grammar, recent_themes
            )
            ranked.append((score, theme["id"]))
        ranked.sort(key=lambda item: (-item[0], item[1]))
        if ranked[0][0] > 0:
            theme_id = ranked[0][1]
        else:
            theme_id = pick_excluding(THEME_IDS, recent_themes)
    else:
        theme_id = pick_excluding(THEME_IDS, recent_themes)

    theme = THEME_BY_ID[theme_id]
    chosen_grammar = pick_grammar(theme, grammar)
    chosen_category = pick_category(theme, args.category)
    result = lock_result(theme, chosen_grammar, chosen_category)

    if not args.no_history:
        append_history(
            args.history_file,
            {
                "ts": int(time.time()),
                "themeId": theme_id,
                "grammar": chosen_grammar,
                "category": chosen_category,
            },
        )

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
