"""
formats.py — 一念紫微斗数 格式化输出模块
Telegram / Web / JSON 多端输出

Author: 崽儿虾 🦞
"""

from typing import Dict, Any, Optional
from zwds_calc import AstrolabeResult


def format_chart_for_telegram(data: dict) -> str:
    """Telegram适配格式（纯文本，无表格）"""
    lines = []

    # 头部
    lines.append("🔮 *一念紫微斗数 · 命盘解讀*")
    lines.append("")

    # 命主信息
    fp = " ".join([
        data["four_pillars"]["year"],
        data["four_pillars"]["month"],
        data["four_pillars"]["day"],
        data["four_pillars"]["hour"],
    ]).strip()
    lines.append(f"📅 四柱：{fp}")
    lines.append(f"🐲 生肖：{data['zodiac']}　五行：{data['five_elements']}")

    soul = data["palaces"][data["soul_index"]]
    body = data["palaces"][data["body_index"]]
    lines.append(f"🏠 命宮：{soul['name_cn']}　身宮：{body['name_cn']}")
    lines.append("")

    # 四化
    if data["mutagens"]:
        lines.append("⚡ *生年四化*")
        for m in data["mutagens"]:
            lines.append(f"  · {m['palace']}：{m['star']}化{m['mutagen']}")
        lines.append("")

    # 十二宫
    lines.append("*📋 十二宮星盤*")
    for p in data["palaces"]:
        major = " ".join(
            f"{s['name']}({s['brightness']})" + (f"→{s['mutagen']}" if s['mutagen'] else "")
            for s in p["major_stars"]
        )
        minor = " ".join(s["name"] for s in p["minor_stars"])
        empty = "【空宮】" if p["is_empty"] else ""

        parts = [f"▪ {p['name_cn']}"]
        parts.append(f"({p['heavenly_stem']}{p['earthly_branch']})")
        parts.append(f"：{major or empty}")
        if minor:
            parts.append(f"〔{minor}〕")

        lines.append(" ".join(parts))

    # 三方四正
    if "surrounding_palaces" in data:
        lines.append("")
        lines.append("*🔄 命宮三方四正*")
        lines.append("  " + " · ".join(data["surrounding_palaces"]))

    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━")
    lines.append("📜 *文化参考，理性看待*")

    return "\n".join(lines)


def format_reading_for_telegram(chart_text: str, reading_text: str) -> str:
    """命盘+解读组合输出，适合Telegram长消息"""
    return f"{chart_text}\n\n━━━ 📖 AI解讀 ━━━\n\n{reading_text}"


def format_reading_short(reading_text: str) -> str:
    """精简版解读（去掉系统提示词痕迹）"""
    # 去掉可能包含的系统指令前缀
    lines = reading_text.strip().split("\n")
    clean_lines = []
    for line in lines:
        if line.startswith("【命盘数据】") or \
           line.startswith("请以上面命盘数据为基础") or \
           line.strip().startswith("---") or \
           len(line.strip()) < 3:
            continue
        clean_lines.append(line)
    return "\n".join(clean_lines)


def build_tg_menu() -> str:
    """Telegram 帮助/菜单"""
    return """🔮 *一念紫微斗数* — 使用说明

📝 输入您的出生信息即可排盘：

`/zwds 2000-8-16 6 男`
（阳历 年-月-日 时辰(0-23) 性别）

或指定流派：
`/zwds 2000-8-16 6 男 三合`
`/zwds 2000-8-16 6 女 飞星`
`/zwds 2000-8-16 6 男 占验`
`/zwds 2000-8-16 6 男 综合`（默认）

📅 农历排盘：
`/zwds_lunar 2000-7-17 6 男`

🔍 其他指令：
`/zwds_help` — 本帮助
`/zwds_stars` — 星曜查询
`/zwds_palace 命宫` — 查询指定宫位
`/zwds_about` — 关于一念紫微

📜 *文化参考，理性看待*
"""


def format_palace_detail(palace_data: dict) -> str:
    """格式化宫位详情（供独立查询时用）"""
    lines = [
        f"🏛 *{palace_data['name_cn']}*",
        f"天干地支：{palace_data['heavenly_stem']}{palace_data['earthly_branch']}",
    ]

    if palace_data["major_stars"]:
        lines.append("")
        lines.append("*主星*")
        for s in palace_data["major_stars"]:
            parts = [f"  · {s['name']}"]
            if s["brightness"]:
                parts.append(f"({s['brightness']})")
            if s["mutagen"]:
                parts.append(f"→化{s['mutagen']}")
            lines.append(" ".join(parts))

    if palace_data["minor_stars"]:
        lines.append("")
        lines.append("*辅星*")
        for s in palace_data["minor_stars"]:
            parts = [f"  · {s['name']}"]
            if s["mutagen"]:
                parts.append(f"→化{s['mutagen']}")
            lines.append(" ".join(parts))

    if palace_data["is_empty"]:
        lines.append("")
        lines.append("⚠️ 此宫为空宫，需借对宫星曜参照")

    return "\n".join(lines)


# 星曜百科（精简版）
STAR_ENCYCLOPEDIA = {
    "紫微": "北斗帝星，尊贵之星。喜左辅右弼、天相。主贵气、领导力、体面。陷落时可能好面子、刚愎。",
    "天机": "南斗第三星，智慧之星。主聪明、策划、变动。喜天梁、太阴。陷落时易思虑过度。",
    "太阳": "中天星系主星，光明之星。主贵、发散、公益。庙旺宽宏大量，陷落时劳碌、散财。",
    "武曲": "北斗第六星，财帛主。主财富、决断、刚毅。喜天府、天相。陷落时过于刚硬。",
    "天同": "南斗第四星，福星。主福气、协调、温和。庙旺一生安逸，陷落时懒散拖延。",
    "廉贞": "北斗第五星，次桃花。主是非、权术、文艺。庙旺清正，陷落时易卷入是非。",
    "天府": "南斗主星，财库。主稳定、包容、守成。喜紫微、武曲。陷落时保守有余。",
    "太阴": "中天星系主星，母星。主温柔、美感、财富。庙旺富有情调，陷落时阴郁。",
    "贪狼": "北斗第一星，桃花主。主交际、才艺、欲望。喜武曲、破军。庙旺才艺出众。",
    "巨门": "北斗第二星，暗星。主口才、是非、思辨。喜日、月。陷落时口舌是非。",
    "天相": "南斗第五星，印星。主诚信、公正、辅助。喜紫微、天府。陷落时易偏执。",
    "天梁": "南斗第二星，荫星。主贵、长寿、清高。喜天机、太阳。陷落时孤芳自赏。",
    "七杀": "南斗第一星，将星。主权威、决断、变动。庙旺威震八方，陷落时多事。",
    "破军": "北斗第七星，耗星。主变革、突破、动荡。喜贪狼、七杀。陷落时破耗。",
}


def get_star_info(star_name: str) -> Optional[str]:
    """获取星曜简介"""
    for name, desc in STAR_ENCYCLOPEDIA.items():
        if name == star_name:
            return f"⭐ *{name}*\n{desc}"
    return None
