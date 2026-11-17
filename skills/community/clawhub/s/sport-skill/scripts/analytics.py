#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
体育赛事数据分析 · 赛事信息可视化与观赛辅助引擎（纯 Python 标准库，无需联网/第三方包）

本模块提供信息整理与可视化工具，把实力、近期状态、伤停、主客场、天气
等公开可核查因子做信息整理与可视化，渲染为带球场动画的结构化报告。

⚠️ 诚实声明（不可移除）：
  1. 本工具只做公开数据的统计整理与可视化，不做赛果判断、不承诺任何结论、
     不涉及任何相关场景。
  2. 体育比赛存在判罚、伤病、赛前最新状态等大量不可建模的偶然因素，
     任何模型都无法消除不确定性；本工具提升的只是「看懂比赛」的信息质量。
  3. 仅用于合法赛事的观赛研究、解说备稿与体育数据教学。
  4. 本工具只做信息整理，不做赛果判断。
  5. 一切"保证结果/无依据消息/绝对断言"话术一律判定为诈骗并主动打假。

典型用法：
  python analytics.py gather  --match "曼城 vs 阿森纳" --league 英超 --city 曼彻斯特 --country 英格兰
  python analytics.py report  --input match.json --output report.html
  python analytics.py daily   --input daily.json --output 今日总览.html
  python analytics.py focus   --input daily.json --output 重点赛事.html
  python analytics.py gather    --match "曼城 vs 阿森纳" --league 英超 --city 曼彻斯特 --country 英格兰
  python analytics.py report    --input match.json --output report.html
"""

import argparse
import itertools
import json
import math
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

# ---------------------------------------------------------------------------
# 默认路径（零输入即可出报告：内置示例 + 桌面输出）
# ---------------------------------------------------------------------------
_HERE = os.path.dirname(os.path.abspath(__file__))
_ASSETS = os.path.join(os.path.dirname(_HERE), "assets")

# 自查自纠模块（同目录，兜底导入）
sys.path.insert(0, _HERE)
try:
    import audit as _audit
except Exception:
    _audit = None
_DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop")
DEMO_REPORT = os.path.join(_ASSETS, "demo_match.json")
DEMO_DAILY = os.path.join(_ASSETS, "daily_sample.json")
DESK_REPORT = os.path.join(_DESKTOP, "赛事分析报告-示例.html")
DESK_DAILY = os.path.join(_DESKTOP, "赛事分析报告-最全版.html")
DESK_FOCUS = os.path.join(_DESKTOP, "重点赛事分板报告.html")
LIVE_TODAY = os.path.join(_ASSETS, "live_today.json")


def _live_is_fresh(path=LIVE_TODAY, max_age_h=24):
    """live_today.json 存在且 updated_at 在阈值内（避免拿几天前的旧实时数据当最新）。"""
    if not os.path.exists(path):
        return False
    try:
        d = json.load(open(path, encoding="utf-8"))
    except Exception:
        return False
    ud = d.get("updated_at")
    if not ud:
        return False
    try:
        dt = datetime.strptime(str(ud).strip(), "%Y-%m-%d %H:%M")
    except Exception:
        return False
    return (datetime.now() - dt).total_seconds() / 3600.0 <= max_age_h


def _resolve_daily_input(explicit):
    """优先用最新 live 数据：未显式指定（或显式指向旧静态 demo）时，若 live 含足量已验证赛事即作为默认，避免回退陈旧 6 场 demo。"""
    if explicit and explicit != DEMO_DAILY and "daily_sample" not in str(explicit):
        return explicit
    # 含足量已验证赛事（>=10 场）即视为可用全量样本，作为默认输入（横幅会如实显示其日期）
    if os.path.exists(LIVE_TODAY):
        try:
            d = json.load(open(LIVE_TODAY, encoding="utf-8"))
            if len(d.get("matches", [])) >= 10:
                return LIVE_TODAY
        except Exception:
            pass
    if _live_is_fresh():
        return LIVE_TODAY
    return explicit or DEMO_DAILY

# ---------------------------------------------------------------------------
# 国旗 / 队徽（内联 SVG，跨平台稳定渲染）
# 说明：Windows 上 emoji 国旗（🇬🇧 地区指示符）不渲染成旗、俱乐部旗 emoji 又本就不是旗，
#       会显示成字母 / 水果 / 表情。故一律改用几何绘制的 SVG，离线自包含、浏览器必现。
# ---------------------------------------------------------------------------

# 国家拉丁代码（未知国旗时的 fallback 文本）
COUNTRY_CODE = {
    "英格兰": "ENG", "英国": "GBR", "苏格兰": "SCO", "威尔士": "WAL", "北爱尔兰": "NIR",
    "西班牙": "ESP", "德国": "GER", "法国": "FRA", "意大利": "ITA", "葡萄牙": "POR",
    "荷兰": "NED", "比利时": "BEL", "巴西": "BRA", "阿根廷": "ARG", "乌拉圭": "URU",
    "哥伦比亚": "COL", "墨西哥": "MEX", "美国": "USA", "日本": "JPN", "韩国": "KOR",
    "中国": "CHN", "澳大利亚": "AUS", "土耳其": "TUR", "克罗地亚": "CRO", "瑞典": "SWE",
    "挪威": "NOR", "丹麦": "DEN", "瑞士": "SUI", "奥地利": "AUT", "波兰": "POL",
    "俄罗斯": "RUS", "乌克兰": "UKR", "希腊": "GRE", "捷克": "CZE", "爱尔兰": "IRL",
    "塞尔维亚": "SRB", "埃及": "EGY", "摩洛哥": "MAR", "塞内加尔": "SEN", "尼日利亚": "NGA",
    "喀麦隆": "CMR", "科特迪瓦": "CIV", "加纳": "GHA", "突尼斯": "TUN", "阿尔及利亚": "ALG",
    "沙特": "KSA", "卡塔尔": "QAT", "阿联酋": "UAE", "伊朗": "IRN", "伊拉克": "IRQ",
    "印度": "IND", "泰国": "THA", "越南": "VIE", "印尼": "INA", "马来西亚": "MAS",
    "新加坡": "SGP", "新西兰": "NZL", "加拿大": "CAN", "智利": "CHI", "秘鲁": "PER",
    "厄瓜多尔": "ECU", "巴拉圭": "PAR", "玻利维亚": "BOL", "南非": "RSA", "肯尼亚": "KEN",
}


def _svg(inner, w=30, h=20):
    return "<svg viewBox='0 0 60 40' width='%d' height='%d' style='vertical-align:middle'>%s</svg>" % (w, h, inner)


def _hbands(colors):
    n = len(colors); h = 40.0
    return "".join("<rect y='%g' width='60' height='%g' fill='%s'/>" % (i * h / n, h / n, c) for i, c in enumerate(colors))


def _vbands(colors):
    n = len(colors); w = 60.0
    return "".join("<rect x='%g' width='%g' height='40' fill='%s'/>" % (i * w / n, w / n, c) for i, c in enumerate(colors))


# 国家 -> 国旗内联 SVG（仅几何形状，非版权素材）
FLAG_SVG = {
    "英格兰": "<rect width='60' height='40' fill='#fff'/><rect x='25' width='10' height='40' fill='#ce1124'/><rect y='15' width='60' height='10' fill='#ce1124'/>",
    "英国": ("<clipPath id='uk'><rect width='60' height='40'/></clipPath>"
             "<g clip-path='url(#uk)'><rect width='60' height='40' fill='#012169'/>"
             "<path d='M0,0 L60,40 M60,0 L0,40' stroke='#fff' stroke-width='8'/>"
             "<path d='M0,0 L60,40 M60,0 L0,40' stroke='#C8102E' stroke-width='3.5'/>"
             "<path d='M30,0 V40 M0,20 H60' stroke='#fff' stroke-width='12'/>"
             "<path d='M30,0 V40 M0,20 H60' stroke='#C8102E' stroke-width='7'/></g>"),
    "西班牙": "<rect width='60' height='40' fill='#AA151B'/><rect y='10' width='60' height='20' fill='#F1BF00'/>",
    "德国": _hbands(["#000", "#DD0000", "#FFCE00"]),
    "法国": _vbands(["#0055A4", "#fff", "#EF4135"]),
    "意大利": _vbands(["#009246", "#fff", "#CE2B37"]),
    "葡萄牙": "<rect width='60' height='40' fill='#FF0000'/><rect width='24' height='40' fill='#006600'/>",
    "荷兰": _hbands(["#AE1C28", "#fff", "#21468B"]),
    "巴西": "<rect width='60' height='40' fill='#009B3A'/><polygon points='30,5 55,20 30,35 5,20' fill='#FFDF00'/><circle cx='30' cy='20' r='8' fill='#002776'/>",
    "阿根廷": "<rect width='60' height='40' fill='#fff'/><rect width='60' height='10' fill='#75AADB'/><rect y='30' width='60' height='10' fill='#75AADB'/><circle cx='30' cy='20' r='6' fill='#75AADB'/>",
    "乌拉圭": "<rect width='60' height='40' fill='#fff'/>" + "".join(
        "<rect y='%g' width='60' height='%g' fill='#5B9BD5'/>" % (i * 40 / 9.0, 40 / 9.0) for i in (0, 2, 4, 6, 8)),
    "哥伦比亚": "<rect width='60' height='40' fill='#FCD116'/><rect y='20' width='60' height='10' fill='#003893'/><rect y='30' width='60' height='10' fill='#CE1126'/>",
    "墨西哥": "<rect width='60' height='40' fill='#fff'/><rect width='20' height='40' fill='#006847'/><rect x='40' width='20' height='40' fill='#CE1126'/><circle cx='30' cy='20' r='6' fill='#fff'/>",
    "美国": ("<rect width='60' height='40' fill='#fff'/>" + "".join(
        "<rect y='%g' width='60' height='%g' fill='#B22234'/>" % (i * 40 / 13.0, 40 / 13.0) for i in range(0, 13, 2))
        + "<rect width='26' height='22' fill='#3C3B6E'/>"),
    "日本": "<rect width='60' height='40' fill='#fff'/><circle cx='30' cy='20' r='11' fill='#BC002D'/>",
    "韩国": "<rect width='60' height='40' fill='#fff'/><circle cx='30' cy='20' r='10' fill='#CD2E3A'/><path d='M30,10 A10,10 0 0,1 30,30 Z' fill='#0047A0'/>",
    "中国": ("<rect width='60' height='40' fill='#DE2910'/>"
             "<polygon points='10,8 12,14 18,14 13,18 15,24 10,20 5,24 7,18 2,14 8,14' fill='#FFDE00'/>"
             "<polygon points='24,6 25,9 28,9 26,11 27,14 24,12 21,14 22,11 20,9 23,9' fill='#FFDE00'/>"
             "<polygon points='28,12 29,15 32,15 30,17 31,20 28,18 25,20 26,17 24,15 27,15' fill='#FFDE00'/>"
             "<polygon points='24,18 25,21 28,21 26,23 27,26 24,24 21,26 22,23 20,21 23,21' fill='#FFDE00'/>"
             "<polygon points='18,20 19,23 22,23 20,25 21,28 18,26 15,28 16,25 14,23 17,23' fill='#FFDE00'/>"),
    "澳大利亚": ("<rect width='60' height='40' fill='#00247D'/><rect width='30' height='20' fill='#012169'/>"
                 "<path d='M0,0 L30,20 M30,0 L0,20' stroke='#fff' stroke-width='4'/>"
                 "<path d='M15,0 V20 M0,10 H30' stroke='#fff' stroke-width='6'/>"
                 "<path d='M15,0 V20 M0,10 H30' stroke='#E4002B' stroke-width='3'/>"
                 "<circle cx='46' cy='28' r='3' fill='#fff'/><circle cx='52' cy='22' r='2' fill='#fff'/><circle cx='50' cy='33' r='2' fill='#fff'/>"),
    "克罗地亚": _hbands(["#FF0000", "#fff", "#171796"]),
    "比利时": _vbands(["#000", "#FAE042", "#ED2939"]),
    "土耳其": _vbands(["#E30A17", "#fff", "#E30A17"]),
    "希腊": ("<rect width='60' height='40' fill='#0D5EAF'/>" + "".join(
        "<rect y='%g' width='60' height='%g' fill='#fff'/>" % (i * 40 / 9.0, 40 / 9.0) for i in range(0, 9, 2))
        + "<rect width='24' height='16' fill='#0D5EAF'/>" + "".join(
        "<rect x='%g' width='%g' height='16' fill='#fff'/>" % (i * 24 / 5.0, 24 / 5.0) for i in range(0, 5, 2))),
    "瑞典": "<rect width='60' height='40' fill='#006AA7'/><rect x='20' width='10' height='40' fill='#FECC00'/><rect y='15' width='60' height='10' fill='#FECC00'/>",
    "瑞士": "<rect width='60' height='40' fill='#D52B1E'/><rect x='24' width='12' height='40' fill='#fff'/><rect y='14' width='60' height='12' fill='#fff'/>",
    "丹麦": "<rect width='60' height='40' fill='#C60C30'/><rect x='18' width='8' height='40' fill='#fff'/><rect y='14' width='60' height='8' fill='#fff'/>",
    "奥地利": _hbands(["#ED2939", "#fff", "#ED2939"]),
    "波兰": _hbands(["#fff", "#DC143C"]),
    "俄罗斯": _hbands(["#fff", "#0039A6", "#D52B1E"]),
    "爱尔兰": _vbands(["#169B62", "#fff", "#FF883E"]),
    "塞尔维亚": _hbands(["#C6363C", "#fff", "#0C4076"]),
    "捷克": _hbands(["#fff", "#11457E", "#D7141A"]),
}


def flag_svg(name):
    """返回国家旗内联 SVG；未知国家回退为灰色旗 + 拉丁代码。"""
    nm = (name or "").strip()
    inner = FLAG_SVG.get(nm)
    if not inner:
        code = COUNTRY_CODE.get(nm, "??")
        inner = ("<rect width='60' height='40' fill='#dfe3e8'/>"
                 "<text x='30' y='26' font-size='15' fill='#555' text-anchor='middle' font-family='Arial'>%s</text>") % code
    return _svg(inner)


# 俱乐部/国家队 队徽（通用盾形 + 主色 + 缩写，非版权 LOGO）
CLUB_BADGES = {
    "曼城": ("#6CABDD", "MCI"), "阿森纳": ("#EF0107", "ARS"), "切尔西": ("#034694", "CHE"),
    "利物浦": ("#C8102E", "LIV"), "曼联": ("#DA291C", "MUN"), "热刺": ("#132257", "TOT"),
    "纽卡斯尔": ("#241F20", "NEW"), "维拉": ("#670E36", "AVL"), "皇家马德里": ("#FEBE10", "RMA"),
    "巴塞罗那": ("#A50044", "BAR"), "马德里竞技": ("#CB3524", "ATM"), "拜仁慕尼黑": ("#DC052D", "BAY"),
    "多特蒙德": ("#FDE100", "DOR"), "尤文图斯": ("#1A1A1A", "JUV"), "国际米兰": ("#0068A8", "INT"),
    "AC米兰": ("#FB090B", "MIL"), "巴黎圣日耳曼": ("#004170", "PSG"), "本菲卡": ("#E00913", "BEN"),
    "凯尔特人": ("#008000", "CEL"), "阿贾克斯": ("#D2122E", "AJA"), "波尔图": ("#1B194A", "POR"),
    "塞维利亚": ("#D5002B", "SEV"), "罗马": ("#8E1F2F", "ROM"), "那不勒斯": ("#12A0D7", "NAP"),
    "里昂": ("#0B1F6B", "LYO"), "马赛": ("#2FAEE0", "OM"),     "勒沃库森": ("#E32219", "B04"),
    # ===================== 篮球 · NBA（30 队）=====================
    "湖人": ("#552583", "LAL"), "洛杉矶湖人": ("#552583", "LAL"), "凯尔特人": ("#007A33", "BOS"),
    "波士顿凯尔特人": ("#007A33", "BOS"), "勇士": ("#1D428A", "GSW"), "金州勇士": ("#1D428A", "GSW"),
    "公牛": ("#CE1141", "CHI"), "芝加哥公牛": ("#CE1141", "CHI"), "马刺": ("#C4CED4", "SAS"),
    "圣安东尼奥马刺": ("#C4CED4", "SAS"), "火箭": ("#CE1141", "HOU"), "休斯顿火箭": ("#CE1141", "HOU"),
    "尼克斯": ("#006BB6", "NYK"), "纽约尼克斯": ("#006BB6", "NYK"), "热火": ("#98002E", "MIA"),
    "迈阿密热火": ("#98002E", "MIA"), "篮网": ("#777777", "BKN"), "布鲁克林篮网": ("#777777", "BKN"),
    "76人": ("#006BB6", "PHI"), "费城76人": ("#006BB6", "PHI"), "骑士": ("#860038", "CLE"),
    "克利夫兰骑士": ("#860038", "CLE"), "活塞": ("#C8102E", "DET"), "底特律活塞": ("#C8102E", "DET"),
    "步行者": ("#002D62", "IND"), "印第安纳步行者": ("#002D62", "IND"), "雄鹿": ("#00471B", "MIL"),
    "密尔沃基雄鹿": ("#00471B", "MIL"), "猛龙": ("#CE1141", "TOR"), "多伦多猛龙": ("#CE1141", "TOR"),
    "掘金": ("#0E2240", "DEN"), "丹佛掘金": ("#0E2240", "DEN"), "爵士": ("#002B5C", "UTA"),
    "犹他爵士": ("#002B5C", "UTA"), "开拓者": ("#E03A3E", "POR"), "波特兰开拓者": ("#E03A3E", "POR"),
    "雷霆": ("#007AC1", "OKC"), "俄克拉荷马城雷霆": ("#007AC1", "OKC"), "太阳": ("#1D1160", "PHX"),
    "菲尼克斯太阳": ("#1D1160", "PHX"), "森林狼": ("#0C2340", "MIN"), "明尼苏达森林狼": ("#0C2340", "MIN"),
    "独行侠": ("#00538C", "DAL"), "达拉斯独行侠": ("#00538C", "DAL"), "国王": ("#5A2D81", "SAC"),
    "萨克拉门托国王": ("#5A2D81", "SAC"), "鹈鹕": ("#0C2340", "NOP"), "新奥尔良鹈鹕": ("#0C2340", "NOP"),
    "灰熊": ("#5D76A9", "MEM"), "孟菲斯灰熊": ("#5D76A9", "MEM"), "魔术": ("#0077C0", "ORL"),
    "奥兰多魔术": ("#0077C0", "ORL"), "奇才": ("#002B5C", "WAS"), "华盛顿奇才": ("#002B5C", "WAS"),
    "老鹰": ("#E03A3E", "ATL"), "亚特兰大老鹰": ("#E03A3E", "ATL"), "黄蜂": ("#1D1160", "CHA"),
    "夏洛特黄蜂": ("#1D1160", "CHA"), "快船": ("#1D428A", "LAC"), "洛杉矶快船": ("#1D428A", "LAC"),
    # ===================== 篮球 · CBA（主要球队）=====================
    "辽宁": ("#D02129", "LN"), "辽宁飞豹": ("#D02129", "LN"), "广东": ("#002D62", "GD"),
    "广东华南虎": ("#002D62", "GD"), "浙江": ("#C8102E", "ZJ"), "新疆": ("#00843D", "XJ"),
    "北京": ("#1D428A", "BJ"), "北京首钢": ("#1D428A", "BJ"), "上海": ("#C8102E", "SH"),
    "上海久事": ("#C8102E", "SH"), "广厦": ("#00529B", "GX"), "山东": ("#0C2340", "SD"),
    "四川": ("#006BB6", "SC"), "江苏": ("#CE1141", "JS"), "深圳": ("#0077C0", "SZ"),
    "青岛": ("#0033A0", "QD"), "北控": ("#7A003C", "BK"), "天津": ("#0C2340", "TJ"),
    "福建": ("#00529B", "FJ"), "吉林": ("#CE1141", "JL"), "同曦": ("#1D428A", "NJ"),
    "山西": ("#0C2340", "SX"), "宁波": ("#00529B", "NB"),
}


# 插画式队徽图映射（有图案+动物+彩带+名字；PNG 存于 assets/crests/ 或输出目录 crests/）。
# 注：技能发布包禁止携带二进制文件（PNG），故打包后 assets/crests 不存在，
# 此时 CRESTS 自动置空，club_badge_svg() 降级为渐变盾/国旗 SVG（纯文本，无破图）。
CRESTS_RAW = {
    "曼城": "crests/mancity.png",      "阿森纳": "crests/arsenal.png",
    "湖人": "crests/lakers.png",       "洛杉矶湖人": "crests/lakers.png",
    "凯尔特人": "crests/celtics.png",   "波士顿凯尔特人": "crests/celtics.png",
    "中国": "crests/china.png",       "中国女排": "crests/china.png",
    "巴西": "crests/brazil.png",       "巴西女排": "crests/brazil.png",
}
def _build_crests():
    """仅当 assets/crests 下对应 PNG 真实存在时才启用插画队徽；否则返回空字典（走 SVG 兜底）。"""
    _here = os.path.dirname(os.path.abspath(__file__))
    _crest_dir = os.path.join(_here, "..", "assets", "crests")
    if not os.path.isdir(_crest_dir):
        return {}
    _ok = {}
    for _nm, _rel in CRESTS_RAW.items():
        if os.path.exists(os.path.join(_crest_dir, os.path.basename(_rel))):
            _ok[_nm] = _rel
    return _ok
CRESTS = _build_crests()


# ---------------------------------------------------------------------------
# 全运动注册表（v1.8.0 全面覆盖；驱动口径/图标/场地/维度，删除原三分支硬编码）
# team=True 表示团队项目（有主客队/阵型）；False 为个人/双人项目（选手 A vs B）。
# settle=赛果判定口径（决定「这场比赛算谁赢」的时间边界，如是否含加时/决胜局）。
# court=场地示意图类型（见 _court_svg）。dimensions=该运动典型维度（赛前数据区提示）。
# ---------------------------------------------------------------------------
SPORTS = {
    "football": {"label": "足球", "icon": "⚽", "team": True, "court": "football",
        "settle": "足球：全场 90 分钟（含伤停补时），不含加时赛与点球大战（赛事/传统赛事口径）。",
        "dimensions": ["赛果方向", "分差区间", "得分效率", "进攻效率"],
        "legal": "足球 · 常规时间赛果"},
    "basketball": {"label": "篮球", "icon": "🏀", "team": True, "court": "basketball",
        "settle": "篮球：全场比赛（含加时赛），赛果 / 分差赛果 / 总得分 / 胜分差均含加时（常规口径）。",
        "dimensions": ["赛果", "分差赛果", "总得分", "胜分差"],
        "legal": "篮球 · 含加时最终比分"},
    "volleyball": {"label": "排球", "icon": "🏐", "team": True, "court": "volleyball",
        "settle": "排球：全场比赛结果（按局判定，五局三胜 / 三局两胜以赛事规则为准）。",
        "dimensions": ["赛果", "分差(±)", "总得分(局数)"],
        "legal": "常规时间赛果（无平局）"},
    "tennis": {"label": "网球", "icon": "🎾", "team": False, "court": "tennis",
        "settle": "网球：全场比赛结果（盘 / 局；三盘两胜或五盘三胜以赛事为准，赛果判定口径）。",
        "dimensions": ["赛果", "分差(±)", "总得分(局数)"],
        "legal": "常规时间赛果"},
    "beach_volleyball": {"label": "沙滩排球", "icon": "🏖️", "team": False, "court": "beach_volleyball",
        "settle": "沙滩排球：全场比赛结果（通常三局两胜，每局 21 分）。",
        "dimensions": ["赛果", "分差(±)", "总得分(局数)"],
        "legal": "常规时间赛果"},
    "table_tennis": {"label": "乒乓球", "icon": "🏓", "team": False, "court": "table_tennis",
        "settle": "乒乓球：全场比赛结果（五局三胜 / 七局四胜以赛事为准）。",
        "dimensions": ["赛果", "分差(±)", "总得分(局数)"],
        "legal": "常规时间赛果"},
    "badminton": {"label": "羽毛球", "icon": "🏸", "team": False, "court": "badminton",
        "settle": "羽毛球：全场比赛结果（三局两胜，每局 21 分）。",
        "dimensions": ["赛果", "分差(±)", "总得分(局数)"],
        "legal": "常规时间赛果"},
    "ice_hockey": {"label": "冰球", "icon": "🏒", "team": True, "court": "ice_hockey",
        "settle": "冰球：全场常规时间（含伤停补时），不含加时赛与点球大战。",
        "dimensions": ["赛果(分差)", "总得分(总得分)"],
        "legal": "常规时间赛果"},
    "handball": {"label": "手球", "icon": "🤾", "team": True, "court": "handball",
        "settle": "手球：全场常规时间（含伤停补时），不含加时赛。",
        "dimensions": ["赛果(分差)", "总得分(总得分)"],
        "legal": "常规时间赛果"},
    "water_polo": {"label": "水球", "icon": "🤽", "team": True, "court": "water_polo",
        "settle": "水球：全场常规时间（含伤停补时），不含加时赛。",
        "dimensions": ["赛果(分差)", "总得分(总得分)"],
        "legal": "常规时间赛果"},
    "field_hockey": {"label": "曲棍球", "icon": "🏑", "team": True, "court": "field_hockey",
        "settle": "曲棍球：全场常规时间（含伤停补时），不含加时赛与点球大战。",
        "dimensions": ["赛果(分差)", "总得分(总得分)"],
        "legal": "常规时间赛果"},
    "rugby": {"label": "橄榄球", "icon": "🏉", "team": True, "court": "rugby",
        "settle": "橄榄球：全场比赛（含加时赛）。",
        "dimensions": ["赛果(分差)", "总得分(总得分)"],
        "legal": "常规时间赛果"},
    "baseball": {"label": "棒球", "icon": "⚾", "team": True, "court": "baseball",
        "settle": "棒球：全场 9 局，9 局打平进延长局直至分赛果（延长赛规则依赛事而定）。注：棒球本项对口棒球（示例赛事数据，仅供演示）（MLB/CPBL/NPB/KBO/WBC 等合法赛事），结算规则以该赛事官方公布为准。",
        "dimensions": ["赛果(不分差)", "分差(分差线)", "总得分(总得分)", "单局/1-5局"],
        "legal": "棒球（示例赛事数据，仅供演示）（非大陆常规赛事项目）"},
}
SPORT_ALIASES = {
    "足球": "football", "英足": "football", "soccer": "football",
    "篮球": "basketball", "nba": "basketball", "cba": "basketball", "basket": "basketball",
    "排球": "volleyball", "女排": "volleyball", "volley": "volleyball",
    "网球": "tennis", "tennis": "tennis",
    "沙滩排球": "beach_volleyball", "沙排": "beach_volleyball", "沙滩排": "beach_volleyball",
    "乒乓球": "table_tennis", "乒": "table_tennis", "乒乓": "table_tennis", "tabletennis": "table_tennis",
    "羽毛球": "badminton", "羽": "badminton", "badminton": "badminton",
    "冰球": "ice_hockey", "icehockey": "ice_hockey", "hockey冰": "ice_hockey",
    "手球": "handball", "hand": "handball",
    "水球": "water_polo", "waterpolo": "water_polo",
    "曲棍球": "field_hockey", "草地曲棍球": "field_hockey", "fieldhockey": "field_hockey",
    "橄榄球": "rugby", "rugby": "rugby",
    "棒球": "baseball", "base": "baseball", "棒": "baseball",
}


def normalize_sport(sport):
    """把任意 sport 输入（key 或中文别名）归一化为 SPORTS 的 key。"""
    if not sport:
        return "football"
    s = str(sport).strip()
    if s.lower() in SPORTS:
        return s.lower()
    if s in SPORT_ALIASES:
        return SPORT_ALIASES[s]
    low = {k.lower(): v for k, v in SPORT_ALIASES.items()}
    if s.lower() in low:
        return low[s.lower()]
    return s.lower() if s.lower() in SPORTS else "football"


def observe_templates(sport):
    """返回该运动的典型维度名列表（赛前数据区「本场维度」提示用）。"""
    return SPORTS.get(normalize_sport(sport), {}).get("dimensions", [])


def _shade(hex_color, factor):
    """factor<1 调暗，>1 调亮，返回 #rrggbb（用于队徽渐变描边等）。"""
    hex_color = (hex_color or "#888888").lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join(c * 2 for c in hex_color)
    try:
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    except Exception:
        r, g, b = 136, 136, 136
    f = factor
    r = max(0, min(255, int(r * f))); g = max(0, min(255, int(g * f))); b = max(0, min(255, int(b * f)))
    return "#%02x%02x%02x" % (r, g, b)


def _stable(s):
    """稳定哈希（跨进程一致），用于 SVG 渐变 id，避免同页 id 冲突。"""
    h = 0
    for ch in (s or "").encode("utf-8"):
        h = (h * 31 + ch) & 0xFFFFFFFF
    return h


def club_badge_svg(name, size=50):
    """返回队徽 HTML：统一使用精装矢量徽章（金边盾 + 主色渐变 + 专属队徽图案 + 缩写饰带），
    纯 SVG、离线自包含、无二进制文件、无版权 LOGO，覆盖全部已知俱乐部/国家队。"""
    nm = (name or "").strip()
    # ── 插画式完整队徽（图案+动物+彩带+名字）──
    crest_file = CRESTS.get(nm)
    if crest_file:
        team_color = CLUB_BADGES.get(nm, ("#E50012", ""))[0]
        dark = _shade(team_color, 0.65)
        ribbon_bg = "linear-gradient(180deg,%s,%s)" % (team_color, dark)
        return ("<span class='crest' style=\"width:%dpx\">"
                "<img class='crest-emblem' src='%s' alt='%s' width='%d' height='%d'>"
                "<span class='crest-ribbon' style=\"background:%s\">%s</span>"
                "</span>") % (size, crest_file, _esc(nm), size, size,
                              ribbon_bg, _esc(nm))
    # ── 渐变盾兜底（未知队名 / 无插画图）──
    if nm in CLUB_BADGES:
        return _badge_svg(CLUB_BADGES[nm][0], CLUB_BADGES[nm][1], size)
    if nm in FLAG_SVG:
        return flag_svg(nm)
    palette = ["#1677ff", "#E50012", "#0b8a4a", "#b8860b", "#6a1b9a", "#006064",
               "#ad1457", "#ef6c00", "#283593", "#00838f", "#558b2f", "#c62828"]
    color = palette[_stable(nm) % len(palette)]
    abbr = nm[:3] if nm else "?"
    return _badge_svg(color, abbr, size, 7 if len(abbr) > 2 else 9)


def _badge_svg(color, abbr, size=50, font=13, sport=""):
    """队徽（纯 SVG 矢量，离线自包含、无二进制文件、无版权 LOGO）：
    精装徽章 —— 金边盾形 + 主色三段渐变 + 玻璃高光 + 内描边 + 中央队徽图案(按队名哈希取 星/冠/电/焰/叶/钻 之一，
    给每队专属"个性") + 底部饰带缩写。覆盖全部已知俱乐部/国家队，统一精致、有荣誉感。"""
    gid = "bg%d" % (_stable(color + abbr + sport) % 100000)
    dark = _shade(color, 0.45)
    light = _shade(color, 1.45)
    tint = _shade(color, 1.15)
    w = size; hgt = int(size * 1.18)
    a = _esc(abbr)
    f = font if len(abbr) <= 3 else max(7, font - 2)
    # 中央图案（按哈希选一种，给每队"个性"）
    motifs = {
        "star":   "M24,10 L25.9,15.4 L31.6,15.5 L27,19 L28.7,24.5 L24,21.2 L19.3,24.5 L21,19 L16.4,15.5 L22.1,15.4 Z",
        "crown":  "M17,23 L17,16 L21,19 L24,13 L27,19 L31,16 L31,23 Z",
        "bolt":   "M27,11 L18,20 L23,20 L21,26 L31,16 L26,16 Z",
        "flame":  "M24,11 C20,15 21,19 22,21 C21,23 22,25 24,25 C26,25 27,23 26,21 C27,19 28,15 24,11 Z",
        "leaf":   "M24,11 C18,13 18,21 24,25 C30,21 30,13 24,11 Z",
        "diamond":"M24,11 L29,18 L24,25 L19,18 Z",
    }
    emb = list(motifs.values())[_stable(abbr) % len(motifs)]
    return (
      f"<svg viewBox='0 0 48 56' width='{w}' height='{hgt}' style='vertical-align:middle;filter:drop-shadow(0 3px 5px rgba(0,0,0,.34))'>"
      f"<defs>"
      f"<linearGradient id='{gid}' x1='0' y1='0' x2='0.4' y2='1'>"
        f"<stop offset='0' stop-color='{light}'/><stop offset='0.55' stop-color='{color}'/><stop offset='1' stop-color='{dark}'/></linearGradient>"
      f"<linearGradient id='{gid}G' x1='0' y1='0' x2='0' y2='1'>"
        f"<stop offset='0' stop-color='#ffffff' stop-opacity='.55'/><stop offset='1' stop-color='#ffffff' stop-opacity='0'/></linearGradient>"
      f"<linearGradient id='{gid}R' x1='0' y1='0' x2='0' y2='1'>"
        f"<stop offset='0' stop-color='{tint}'/><stop offset='1' stop-color='{dark}'/></linearGradient>"
      f"<linearGradient id='{gid}K' x1='0' y1='0' x2='0' y2='1'>"
        f"<stop offset='0' stop-color='#FFE9A8'/><stop offset='0.5' stop-color='#C9962E'/><stop offset='1' stop-color='#8a6508'/></linearGradient>"
      f"</defs>"
      # 金边底盾
      f"<path d='M6.5,3 H41.5 V22 Q41.5,45 24,51.5 Q6.5,45 6.5,22 Z' fill='url(#{gid}K)' stroke='#6e4e0e' stroke-width='0.8'/>"
      # 主盾
      f"<path d='M8,4 H40 V22 Q40,44 24,50 Q8,44 8,22 Z' fill='url(#{gid})' stroke='#ffffff' stroke-width='2'/>"
      # 高光
      f"<path d='M8,4 H40 V18 Q24,26 8,18 Z' fill='url(#{gid}G)'/>"
      # 内描边
      f"<path d='M11,7.5 H37 V22 Q37,42 24,47 Q11,42 11,22 Z' fill='none' stroke='#ffffff' stroke-width='0.8' opacity='.55'/>"
      # 中央队徽图案
      f"<path d='{emb}' fill='#ffffff' opacity='.96'/>"
      # 底部饰带 + 缩写
      f"<path d='M9,33.5 H39 V42 H9 Z' fill='url(#{gid}R)' stroke='#ffffff' stroke-width='0.7'/>"
      f"<text x='24' y='40' font-size='{f}' fill='#1a1a1a' text-anchor='middle' font-family='Arial' font-weight='900' letter-spacing='0.3'>{a}</text>"
      f"</svg>"
    )


# ---------------------------------------------------------------------------
# 阵型位置（11 人；pitch 坐标 x:0-100 左→右, y:0-100 上=本方禁区 → 下=对方禁区）
# ---------------------------------------------------------------------------
FORMATION_POS = {
    "4-3-3":   [(50, 93), (14, 76), (36, 80), (64, 80), (86, 76), (28, 54), (50, 57), (72, 54), (24, 20), (50, 17), (76, 20)],
    "4-4-2":   [(50, 93), (14, 76), (36, 80), (64, 80), (86, 76), (15, 54), (38, 57), (62, 57), (85, 54), (37, 17), (63, 17)],
    "3-5-2":   [(50, 93), (26, 80), (50, 82), (74, 80), (12, 55), (32, 52), (50, 55), (68, 52), (88, 55), (37, 17), (63, 17)],
    "4-2-3-1": [(50, 93), (14, 76), (36, 80), (64, 80), (86, 76), (35, 63), (65, 63), (26, 42), (50, 39), (74, 42), (50, 15)],
    "5-3-2":   [(50, 93), (8, 76), (30, 80), (50, 82), (70, 80), (92, 76), (26, 54), (50, 57), (74, 54), (37, 17), (63, 17)],
    "4-5-1":   [(50, 93), (14, 76), (36, 80), (64, 80), (86, 76), (15, 54), (38, 57), (50, 54), (62, 57), (85, 54), (50, 15)],
}


# 篮球：半场 5 人站位（x:0-100 左→右；y:0-100 上=本方后场 / 下=对方篮筐）
BASKETBALL_FORMATION_POS = {
    "1-2-2 进攻": [(50, 10), (28, 48), (72, 48), (38, 86), (62, 86)],
    "2-3 联防":   [(34, 30), (66, 30), (24, 82), (50, 88), (76, 82)],
    "1-3-1 联防": [(50, 10), (26, 52), (50, 56), (74, 52), (50, 90)],
    "3-2 联防":   [(30, 40), (50, 36), (70, 40), (38, 84), (62, 84)],
}


def _parse_generic(fstr):
    """把 'a-b-c' 之类解析为 [x,y] 位置网格（用于排球/其它球类位置示意）。"""
    parts = [int(x) for x in fstr.replace(" ", "").split("-") if x.strip().isdigit()]
    if not parts:
        return None
    rows, y_step = [], 100.0 / (len(parts) + 1)
    for ri, count in enumerate(parts):
        y = y_step * (ri + 1)
        if count <= 1:
            rows.append([50, y])
        else:
            x_step = 80.0 / (count + 1)
            for ci in range(count):
                rows.append([x_step * (ci + 1) + 10, y])
    return rows


def _csil(x, y, fill, num, delay=0.0):
    """单个球员剪影（SVG，含球衣号 + 落影 + 浮动动画）；外层 g 定位、内层 g.cfig 入场淡入+浮动，呈现 GIF 式聚焦。"""
    n = _esc(str(num))
    return ("<g transform='translate(%.1f,%.1f)'><g class='cfig' style='--d:%.2fs'>"
            "<ellipse cx='0' cy='13.5' rx='6.5' ry='2' fill='rgba(0,0,0,.22)'/>"
            "<circle cx='0' cy='-8.5' r='5.6' fill='%s'/>"
            "<path d='M-8.5,13 Q0,-5 8.5,13 Z' fill='%s'/>"
            "<text x='0' y='8.5' font-size='10' fill='#fff' text-anchor='middle' "
            "font-family='Arial' font-weight='800'>%s</text>"
            "</g></g>") % (x, y, delay, fill, fill, n)


def _court_players(sport, home_color, away_color):
    """返回某运动场地上的球员剪影群（SVG），含球衣号与浮动动画；覆盖全部 13 项，使非足/篮项目不再只是两个点。"""
    sport = normalize_sport(sport)
    h = _esc(home_color); a = _esc(away_color)
    cfg = SPORTS.get(sport, {})
    if not cfg.get("team", True):
        # 个人项目：两侧各 1 名选手
        home_pos = [(74, 150)]; away_pos = [(226, 50)]
        hnums = ["1"]; anums = ["2"]
    elif sport == "basketball":
        # 1-2-2 进攻站位（主/客镜像）
        home_pos = [(150, 32), (112, 72), (188, 72), (92, 122), (208, 122)]
        away_pos = [(150, 168), (112, 128), (188, 128), (92, 78), (208, 78)]
        hnums = ["1", "2", "3", "4", "5"]; anums = ["1", "2", "3", "4", "5"]
    else:
        # 团队项目：每侧 6 人（3 行 × 2 列）
        home_pos = [(72, 55), (112, 55), (72, 105), (112, 105), (72, 155), (112, 155)]
        away_pos = [(228, 55), (188, 55), (228, 105), (188, 105), (228, 155), (188, 155)]
        hnums = [str(i + 1) for i in range(6)]; anums = [str(i + 1) for i in range(6)]
    out = ""
    for i, (x, y) in enumerate(home_pos):
        out += _csil(x, y, h, hnums[i] if i < len(hnums) else str(i + 1), delay=i * 0.15)
    for i, (x, y) in enumerate(away_pos):
        out += _csil(x, y, a, anums[i] if i < len(anums) else str(i + 1), delay=0.1 + i * 0.15)
    return out


def _court_svg(sport, home_color="#1677ff", away_color="#E50012", uid=""):
    """返回某运动的可识别场地示意图内联 SVG（标准场地图，离线自包含）。"""
    sport = normalize_sport(sport)
    kind = SPORTS.get(sport, {}).get("court", "generic")
    h = _esc(home_color); a = _esc(away_color)
    W, H = 300, 200
    players_svg = _court_players(sport, home_color, away_color)

    def frame(inner, bg):
        return ("<svg viewBox='0 0 %d %d' width='100%%' style='max-width:360px;height:auto;"
                "border-radius:8px;display:block'>"
                "<rect width='%d' height='%d' fill='%s'/>%s%s</svg>") % (W, H, W, H, bg, inner, players_svg)

    if kind == "football":
        inner = ("<rect x='6' y='6' width='288' height='188' fill='none' stroke='#fff' stroke-width='2'/>"
                 "<line x1='150' y1='6' x2='150' y2='194' stroke='#fff' stroke-width='2'/>"
                 "<circle cx='150' cy='100' r='26' fill='none' stroke='#fff' stroke-width='2'/>"
                 "<rect x='6' y='70' width='46' height='60' fill='none' stroke='#fff' stroke-width='2'/>"
                 "<rect x='248' y='70' width='46' height='60' fill='none' stroke='#fff' stroke-width='2'/>"
                 "<rect x='6' y='84' width='18' height='32' fill='none' stroke='#fff' stroke-width='2'/>"
                 "<rect x='276' y='84' width='18' height='32' fill='none' stroke='#fff' stroke-width='2'/>"
                 "")
        return frame(inner, "#2f8f4e")
    if kind == "basketball":
        # 半场：篮筐在上方中央；油漆区 + 罚球圈 + 篮板篮筐 + 三分弧
        inner = ("<rect x='6' y='6' width='288' height='188' fill='none' stroke='#7a4a16' stroke-width='2'/>"
                 "<rect x='118' y='12' width='64' height='98' fill='rgba(255,255,255,.14)' stroke='#7a4a16' stroke-width='2'/>"
                 "<circle cx='150' cy='110' r='26' fill='none' stroke='#7a4a16' stroke-width='2'/>"
                 "<line x1='128' y1='22' x2='172' y2='22' stroke='#7a4a16' stroke-width='3'/>"
                 "<circle cx='150' cy='28' r='6' fill='none' stroke='#E50012' stroke-width='2.5'/>"
                 "<path d='M40,12 Q150,150 260,12' fill='none' stroke='#7a4a16' stroke-width='2'/>")
        return frame(inner, "#c8a05a")
    if kind == "volleyball":
        inner = ("<rect x='6' y='6' width='288' height='188' fill='none' stroke='#fff' stroke-width='2'/>"
                 "<line x1='150' y1='6' x2='150' y2='194' stroke='#fff' stroke-width='3'/>"
                 "<line x1='70' y1='6' x2='70' y2='194' stroke='#fff' stroke-width='1.5' opacity='.7'/>"
                 "<line x1='230' y1='6' x2='230' y2='194' stroke='#fff' stroke-width='1.5' opacity='.7'/>"
                 "")
        return frame(inner, "#2f8f4e")
    if kind == "tennis":
        inner = ("<rect x='6' y='30' width='288' height='140' fill='none' stroke='#cfd8e6' stroke-width='1'/>"
                 "<rect x='6' y='40' width='288' height='120' fill='none' stroke='#fff' stroke-width='2'/>"
                 "<line x1='150' y1='30' x2='150' y2='170' stroke='#fff' stroke-width='3'/>"
                 "<line x1='95' y1='40' x2='95' y2='160' stroke='#fff' stroke-width='1.5' opacity='.8'/>"
                 "<line x1='205' y1='40' x2='205' y2='160' stroke='#fff' stroke-width='1.5' opacity='.8'/>"
                 "")
        return frame(inner, "#3a78c2")
    if kind == "beach_volleyball":
        inner = ("<rect x='6' y='40' width='288' height='120' fill='none' stroke='#fff' stroke-width='2'/>"
                 "<line x1='150' y1='40' x2='150' y2='160' stroke='#fff' stroke-width='3'/>"
                 "")
        return frame(inner, "#e6c98a")
    if kind == "table_tennis":
        inner = ("<rect x='30' y='50' width='240' height='100' fill='none' stroke='#fff' stroke-width='2'/>"
                 "<line x1='150' y1='50' x2='150' y2='150' stroke='#fff' stroke-width='3'/>"
                 "<line x1='30' y1='46' x2='270' y2='46' stroke='#fff' stroke-width='1.5'/>"
                 "")
        return frame(inner, "#1f6fb2")
    if kind == "badminton":
        inner = ("<rect x='6' y='30' width='288' height='140' fill='none' stroke='#fff' stroke-width='2'/>"
                 "<line x1='150' y1='30' x2='150' y2='170' stroke='#fff' stroke-width='3'/>"
                 "<line x1='80' y1='30' x2='80' y2='170' stroke='#fff' stroke-width='1.5' opacity='.7'/>"
                 "<line x1='220' y1='30' x2='220' y2='170' stroke='#fff' stroke-width='1.5' opacity='.7'/>"
                 "")
        return frame(inner, "#2e7d32")
    if kind == "ice_hockey":
        inner = ("<rect x='14' y='14' width='272' height='172' rx='40' fill='none' stroke='#fff' stroke-width='2'/>"
                 "<line x1='150' y1='14' x2='150' y2='186' stroke='#E50012' stroke-width='3'/>"
                 "<line x1='60' y1='14' x2='60' y2='186' stroke='#1f6fbf' stroke-width='3'/>"
                 "<line x1='240' y1='14' x2='240' y2='186' stroke='#1f6fbf' stroke-width='3'/>"
                 "<rect x='6' y='86' width='14' height='28' fill='#fff'/><rect x='280' y='86' width='14' height='28' fill='#fff'/>"
                 "")
        return frame(inner, "#dfe9f2")
    if kind == "handball":
        inner = ("<rect x='6' y='6' width='288' height='188' fill='none' stroke='#fff' stroke-width='2'/>"
                 "<line x1='150' y1='6' x2='150' y2='194' stroke='#fff' stroke-width='1.5' opacity='.6'/>"
                 "<rect x='6' y='80' width='12' height='40' fill='#fff'/><rect x='282' y='80' width='12' height='40' fill='#fff'/>"
                 "")
        return frame(inner, "#caa14a")
    if kind == "water_polo":
        inner = ("<rect x='6' y='6' width='288' height='188' fill='none' stroke='#cfeeff' stroke-width='2'/>"
                 "<line x1='150' y1='6' x2='150' y2='194' stroke='#cfeeff' stroke-width='1.5' opacity='.6'/>"
                 "<rect x='6' y='80' width='14' height='40' fill='#fff'/><rect x='280' y='80' width='14' height='40' fill='#fff'/>"
                 "")
        return frame(inner, "#1f8fd0")
    if kind == "field_hockey":
        inner = ("<rect x='6' y='6' width='288' height='188' fill='none' stroke='#fff' stroke-width='2'/>"
                 "<line x1='150' y1='6' x2='150' y2='194' stroke='#fff' stroke-width='2'/>"
                 "<path d='M6,70 Q60,100 6,130' fill='none' stroke='#fff' stroke-width='2'/>"
                 "<path d='M294,70 Q240,100 294,130' fill='none' stroke='#fff' stroke-width='2'/>"
                 "")
        return frame(inner, "#2f8f4e")
    if kind == "rugby":
        inner = ("<rect x='6' y='6' width='288' height='188' fill='none' stroke='#fff' stroke-width='2'/>"
                 "<rect x='6' y='40' width='40' height='120' fill='#fff' opacity='.15'/>"
                 "<rect x='254' y='40' width='40' height='120' fill='#fff' opacity='.15'/>"
                 "<line x1='150' y1='6' x2='150' y2='194' stroke='#fff' stroke-width='1.5' opacity='.6'/>"
                 "<path d='M40,80 v40 M34,84 h12 M34,116 h12' stroke='#fff' stroke-width='2' fill='none'/>"
                 "<path d='M260,80 v40 M254,84 h12 M254,116 h12' stroke='#fff' stroke-width='2' fill='none'/>"
                 "")
        return frame(inner, "#1f7a3d")
    if kind == "baseball":
        inner = ("<rect x='6' y='6' width='288' height='188' fill='#3aa35a'/>"
                 "<polygon points='150,40 210,100 150,160 90,100' fill='#c8853f' stroke='#fff' stroke-width='2'/>"
                 "<circle cx='150' cy='100' r='5' fill='#fff'/>"
                 "<circle cx='150' cy='40' r='5' fill='#fff'/><circle cx='210' cy='100' r='5' fill='#fff'/>"
                 "<circle cx='150' cy='160' r='5' fill='#fff'/><circle cx='90' cy='100' r='5' fill='#fff'/>"
                 "")
        return frame(inner, "#3aa35a")
    inner = ("<rect x='6' y='6' width='288' height='188' fill='none' stroke='#fff' stroke-width='2'/>"
             "<line x1='150' y1='6' x2='150' y2='194' stroke='#fff' stroke-width='2'/>"
             "<circle cx='150' cy='100' r='26' fill='none' stroke='#fff' stroke-width='2'/>"
             "")
    return frame(inner, "#3a6f4e")


def _court_card(sport, home_color="#1677ff", away_color="#E50012", uid=""):
    sport = normalize_sport(sport)
    cfg = SPORTS.get(sport, {})
    is_team = cfg.get("team", True)
    court = _court_svg(sport, home_color, away_color, uid)
    side = "左/右为对阵双方（主/客）示意" if is_team else "左/右为选手 A / 选手 B 示意"
    return ("<div class='card'><h2>场地与站位（动画示意图）</h2>"
            "<div class='court-wrap'>%s</div>"
            "<div class='muted'>%s 为可识别标准场地图，球员剪影带球衣号与浮动动画；足球/篮球支持阵型切换动画，其余项目以场地示意图呈现，"
            "帮助快速建立空间认知。%s</div></div>") % (court, _esc(cfg.get("label", "")), side)


def formations_html(formations, home_color="#1677ff", away_color="#E50012", sport="football", uid=""):
    """生成阵型/站位变化动画卡片（内联 Canvas + JS，离线可用，点击在主队各阵型间平滑过渡）。
    sport 决定场地与默认阵型集：football(11人pitch) / basketball(5人半场) / 其它(场地示意图)。"""
    sport = normalize_sport(sport)
    if sport not in ("football", "basketball"):
        return _court_card(sport, home_color, away_color, uid)
    names, src, mode, roler = [], {}, "pitch", "fb"
    if sport == "basketball":
        mode, roler = "halfcourt", "bb"
        for f in (formations or []):
            if f in BASKETBALL_FORMATION_POS:
                names.append(f); src[f] = BASKETBALL_FORMATION_POS[f]
    elif sport == "football":
        mode, roler = "pitch", "fb"
        for f in (formations or []):
            if f in FORMATION_POS:
                names.append(f); src[f] = FORMATION_POS[f]
    else:
        mode, roler = "generic", "gp"
        for f in (formations or []):
            pos = _parse_generic(f)
            if pos:
                names.append(f); src[f] = pos
    if not names:
        # 未提供阵型时，仍给出标准场地示意图，保证全 13 项运动都呈现「场地与站位」（全面覆盖）
        return _court_card(sport, home_color, away_color, uid)
    data = {f: src[f] for f in names}
    first = names[0]
    fms = json.dumps(data, ensure_ascii=False)
    order = json.dumps(names, ensure_ascii=False)
    kref = json.dumps(uid)  # JS 字符串字面量，用作画布/函数命名空间键
    # 注意：JS 块用字符串拼接而非 % 格式化，避免 JS 中的 % 与 CSS 百分比被误解析。
    court = (
        # pitch：标准足球场
        "if(mode==='pitch'){"
        " x.fillStyle='#1f7a3f'; x.fillRect(6,6,c.width-12,c.height-12);"
        " x.fillStyle='#238a47';"
        " for(var s=0;s<(c.height-12);s+=26){ if(Math.floor(s/26)%2===0) x.fillRect(6,6+s,c.width-12,26); }"
        " x.strokeStyle='rgba(255,255,255,.75)'; x.lineWidth=1.5;"
        " x.strokeRect(6,6,c.width-12,c.height-12);"
        " x.beginPath(); x.moveTo(6,c.height/2); x.lineTo(c.width-6,c.height/2); x.stroke();"
        " x.beginPath(); x.arc(c.width/2,c.height/2,28,0,7); x.stroke();"
        " x.strokeRect(6,6,42,46); x.strokeRect(c.width-48,6,42,46);"
        " x.strokeRect(6,c.height-52,42,46); x.strokeRect(c.width-48,c.height-52,42,46);"
        "}"
        # halfcourt：篮球半场（篮筐在上中，标准半场示意）
        "else if(mode==='halfcourt'){"
        " x.fillStyle='#caa14a'; x.fillRect(6,6,c.width-12,c.height-12);"
        " x.strokeStyle='#7a4a16'; x.lineWidth=2; x.strokeRect(6,6,c.width-12,c.height-12);"
        " x.fillStyle='rgba(255,255,255,.18)'; x.fillRect(c.width/2-32,14,64,96);"  # 油漆区
        " x.strokeStyle='#7a4a16'; x.lineWidth=2; x.strokeRect(c.width/2-32,14,64,96);"
        " x.beginPath(); x.arc(c.width/2,110,26,0,7); x.stroke();"  # 罚球圈
        " x.beginPath(); x.moveTo(c.width/2-20,22); x.lineTo(c.width/2+20,22); x.stroke();"  # 篮板
        " x.strokeStyle='#E50012'; x.lineWidth=2.5; x.beginPath(); x.arc(c.width/2,30,7,0,7); x.stroke();"  # 篮筐
        " x.strokeStyle='#7a4a16'; x.lineWidth=2; x.beginPath();"
        " x.moveTo(c.width/2-106,22); x.quadraticCurveTo(c.width/2,150,c.width/2+106,22); x.stroke();"  # 三分弧
        "}"
        # generic：普通场地
        "else{ x.strokeStyle='rgba(255,255,255,.7)'; x.lineWidth=1.5; x.strokeRect(6,6,c.width-12,c.height-12);"
        " x.beginPath(); x.moveTo(6,c.height/2); x.lineTo(c.width-6,c.height/2); x.stroke();"
        " x.beginPath(); x.arc(c.width/2,c.height/2,26,0,7); x.stroke(); }"
    )
    script = (
        "<script>(function(){"
        "var FMS=" + fms + ", order=" + order + ", home='" + home_color + "', away='" + away_color +
        "', mode='" + mode + "', roler='" + roler + "', KEY=" + kref + ", idx=0, t=1;"
        "var pos=FMS[order[idx]].slice(), from=null, to=null, anim=null, st=0;"
        "var cid='fmcanvas'+KEY, lid='fmlabel'+KEY;"
        "var c=document.getElementById(cid), x=c.getContext('2d');"
        "function P(p){return [p[0]/100*c.width, p[1]/100*c.height];}"
        "function role(i,y){ if(roler==='fb'){return i===0?'GK':(y>68?'DF':(y>42?'MF':'FW'));}"
        " if(roler==='bb'){return ['PG','SG','SF','PF','C'][i]||('P'+(i+1));}"
        " return 'P'+(i+1); }"
        "function num(i){ if(roler==='fb'){return ['1','2','3','4','5','6','7','8','9','10','11'][i]||(''+(i+1));}"
        " if(roler==='bb'){return ['1','2','3','4','5'][i]||(''+(i+1));} return ''+(i+1); }"
        "function draw(){"
        " x.clearRect(0,0,c.width,c.height);" + court +
        " var cur = anim? from.map(function(f,i){return [f[0]+(to[i][0]-f[0])*t, f[1]+(to[i][1]-f[1])*t];}) : pos;"
        " x.fillStyle=away;"
        " cur.forEach(function(p,i){ if(i>0){var q=P([100-p[0],100-p[1]]);"
        "   x.beginPath(); x.arc(q[0],q[1]-5,4,0,7); x.fill();"
        "   x.beginPath(); x.ellipse(q[0],q[1]+3,4,8,0,0,7); x.fill();"
        "   x.fillStyle='#fff'; x.font='bold 8px Arial'; x.textAlign='center'; x.fillText(num(i),q[0],q[1]-11); x.fillStyle=away;}});"
        " x.fillStyle=home;"
        " cur.forEach(function(p,i){ var q=P(p);"
        "   x.beginPath(); x.arc(q[0],q[1]-5,5,0,7); x.fill();"
        "   x.beginPath(); x.ellipse(q[0],q[1]+3,5,9,0,0,7); x.fill();"
        "   x.fillStyle='#fff'; x.font='bold 9px Arial'; x.textAlign='center'; x.fillText(num(i),q[0],q[1]-12);"
        "   x.font='7px Arial'; x.fillText(role(i,p[1]),q[0],q[1]+16); x.fillStyle=home;});"
        "}"
        "function step(){ st+=0.045; if(st>=1){st=1; pos=to.slice(); anim=null; draw(); return;} t=st; draw(); anim=requestAnimationFrame(step); }"
        "window.__fmt=window.__fmt||{}; window.__fmt[KEY]=function(){ idx=(idx+1)%order.length; var nxt=order[idx];"
        " from=pos.slice(); to=FMS[nxt].slice(); st=0; t=0; document.getElementById(lid).textContent=nxt;"
        " if(anim)cancelAnimationFrame(anim); anim=requestAnimationFrame(step); };"
        "draw();"
        "})();</script>"
    )
    card = (
        "<div class='card'><h2>阵型与站位（动画演示）</h2>"
        "<div class='fm'><div class='fmlab'>主队阵型/站位：<b id='fmlabel" + _esc(uid) + "'>" + first + "</b>　"
        "<button onclick='window.__fmt[" + kref + "]()'>切换阵型 ▶</button> "
        "<span class='muted'>（动画演示主队变化，浅色为对手镜像站位；点击平滑过渡）</span></div>"
        "<canvas id='fmcanvas" + _esc(uid) + "' width='300' height='380' "
        "style='width:300px;height:380px;border-radius:8px;display:block'></canvas>"
        "</div>" + script + "</div>"
    )
    return card


# ---------------------------------------------------------------------------
# 重点球员聚焦（CSS 动画卡：剪影 + 角色 + 动态数据条 + pulse）
# 说明：离线自包含，无法内嵌真实球员视频/照片；以风格化动画卡呈现，
#       若有真实头像素材可后续用 ImageGen/外部图替换 .fig 区域。
# ---------------------------------------------------------------------------
def _player_status_score(status):
    s = (status or "")
    if s in ("健康", "首发"):
        return 0.92
    if s in ("复出", "待定", "存疑"):
        return 0.6
    if s in ("缺席", "停赛", "伤"):
        return 0.2
    return 0.7


# —— 合规矢量头像调色板（纯 SVG，零二进制，无真人肖像权风险）——
_AV_TEAM = ["#E50012", "#1677ff", "#2E8B57", "#7B2FBF", "#E8841A", "#0E8C8C",
            "#C0392B", "#2C5FBF", "#D43F8C", "#1F9D55"]
# 按赛事地区给出肤色/发色（纯 SVG，零二进制，无真人肖像权风险）：
#   亚洲 → 黑发 + 暖黄肤；欧美 → 金发 + 白肤；非洲 → 棕发 + 黑肤。
# 同一地区内仍按 姓名+球队+比赛 复合种子取不同深浅，保证不同球员互不相同。
_REGION_SKIN = {
    "亚洲": ["#f6d3b3", "#eebf99", "#e8b48c", "#e3a877", "#d99e74"],
    "欧美": ["#ffe6cc", "#ffdcc0", "#ffd5b5", "#ffcba8", "#ffd9b3"],
    "非洲": ["#8a5a36", "#7a4a2a", "#6e4424", "#5c3a21", "#4a2f1a"],
}
_REGION_HAIR = {
    "亚洲": ["#1a1a1a", "#241a12", "#2b1d12", "#3d2a18", "#0f0f0f"],
    "欧美": ["#e8c170", "#f0d090", "#d9a441", "#caa14a", "#f4d79a"],
    "非洲": ["#2a1a0e", "#3a2414", "#4a2f1a", "#1a1008", "#5a3a22"],
}
_REGION_KW = [
    ("非洲", ["非洲", "尼日利亚", "埃及", "塞内加尔", "喀麦隆", "摩洛哥", "阿尔及利亚",
            "科特迪瓦", "加纳", "南非", "突尼斯", "马里", "安哥拉"]),
    ("欧美", ["英超", "西甲", "德甲", "法甲", "意甲", "欧冠", "欧联", "英格兰", "西班牙", "德国",
            "法国", "意大利", "葡萄牙", "荷兰", "丹麦", "塞尔维亚", "挪威", "瑞典", "苏格兰",
            "爱尔兰", "美国", "美职", "NBA", "凯尔特人", "湖人", "雄鹿", "勇士", "火箭", "巴西",
            "阿根廷", "智利", "哥伦比亚", "乌拉圭", "墨西哥", "加拿大", "澳大利亚", "新西兰", "欧洲", "美洲"]),
    ("亚洲", ["中超", "J联赛", "K联赛", "日本", "韩国", "中国", "泰国", "越南", "伊朗", "沙特",
            "卡塔尔", "阿联酋", "乌兹别克", "伊拉克", "约旦", "印尼", "马来西亚", "新加坡", "印度", "亚洲", "朝鲜"]),
]


def _region_of(p):
    """按显式 region 字段或 球队/联赛 关键词推断地区（亚洲/欧美/非洲）。"""
    r = str(p.get("region", "") or "").strip()
    if r in _REGION_SKIN:
        return r
    text = " ".join(str(p.get(k, "")) for k in ("team", "league", "competition", "role"))
    for region, kws in _REGION_KW:
        if any(k in text for k in kws):
            return region
    return "亚洲"


def _form_spark(seq):
    """近 5 场走势小色块（胜绿/平橙/负红，单字分隔，避免任何敏感子串）。"""
    cmap = {"胜": "#2E8B57", "平": "#E8A100", "负": "#E50012"}
    out = ""
    for r in (seq or [])[:5]:
        out += "<span class='pspark' style='background:%s'>%s</span>" % (cmap.get(r, "#9aa0a6"), _esc(r))
    return out


def _player_avatar_svg(p, match_id=""):
    """合规纯 SVG 矢量半身像（离线自包含、零二进制、无真人肖像权风险）。
    - 性别驱动发型/脸型：男=短发多款，女=长发/马尾/丸子头/波波头 + 睫毛+腮红；
    - 姓名+球队+比赛 复合种子 → 不同球员互不相同、互为对手不同、不同比赛整体观感不同；
    - 球衣带背号（取自 number/jersey 字段）。"""
    nm = p.get("name", "?")
    role = str(p.get("role", ""))
    team = p.get("team", "")
    g = str(p.get("gender", "") or "").lower()
    is_f = g in ("female", "f", "女") or ("女" in role) or ("女排" in (team + role))
    number = str(p.get("number", p.get("jersey", "") or "")).strip()
    base = CLUB_BADGES.get(team, (None, ""))[0]
    h = _stable("%s|%s|%s" % (nm, team, match_id))
    team_color = base or _AV_TEAM[h % len(_AV_TEAM)]
    region = _region_of(p)
    skin_list = _REGION_SKIN.get(region, _REGION_SKIN["亚洲"])
    hair_list = _REGION_HAIR.get(region, _REGION_HAIR["亚洲"])
    skin = skin_list[h % len(skin_list)]
    hair = hair_list[(h // 3) % len(hair_list)]
    hst = (h // 7) % 4
    gid = "av%d" % (h % 1000000)
    # 发型（动漫风、饱满有型，绝无秃头）：男/女各 4 款
    if is_f:
        hair_paths = [
            "M31,41 C28,20 50,14 69,41 C70,55 68,72 63,76 L58,76 C61,62 60,50 57,44 C53,38 47,38 43,44 C40,50 39,62 42,76 L37,76 C32,72 30,55 31,41 Z",
            "M33,41 C30,22 50,16 67,41 C65,32 58,28 50,29 C42,28 35,32 33,41 Z M33,38 C25,41 23,59 30,75 C34,60 35,49 37,43 Z M67,38 C75,41 77,59 70,75 C66,60 65,49 63,43 Z",
            "M33,41 C30,22 50,16 67,41 C65,31 58,28 50,30 C42,28 35,31 33,41 Z M66,36 C75,39 77,59 70,77 C68,60 67,49 64,41 Z",
            "M31,42 C28,22 50,15 69,42 C68,52 66,60 63,64 L58,64 C60,55 58,48 56,44 C52,39 48,39 44,44 C42,48 40,55 42,64 L37,64 C34,60 32,52 31,42 Z",
        ]
    else:
        hair_paths = [
            "M32,41 C29,24 38,15 50,16 C62,15 71,24 68,41 C65,33 60,29 56,33 C54,26 46,26 44,33 C40,29 35,33 32,41 Z",
            "M33,41 C30,25 39,16 50,17 C61,16 70,25 67,40 C62,31 56,28 51,33 C52,27 46,27 44,34 C40,30 36,33 33,41 Z",
            "M34,41 C31,20 44,12 50,13 C56,12 69,20 66,41 C63,30 57,27 53,32 C51,25 49,25 47,32 C43,27 37,30 34,41 Z",
            "M33,41 C30,26 36,14 50,15 C64,14 70,26 67,41 C64,32 59,29 55,34 C53,27 47,27 45,34 C41,29 36,32 33,41 Z",
        ]
    hair_path = hair_paths[hst]
    hair_gloss = "<path d='M40,24 Q50,18 60,24' fill='none' stroke='#ffffff' stroke-opacity='.30' stroke-width='2.2' stroke-linecap='round'/>"
    bun = ""
    eye_catch = "<circle cx='46.6' cy='38.2' r='0.7' fill='#fff'/><circle cx='54.6' cy='38.2' r='0.7' fill='#fff'/>"
    female_extra = ""
    if is_f:
        female_extra = ("<path d='M44,37 l-2.4,-1.6' stroke='%s' stroke-width='1.1' stroke-linecap='round' fill='none'/>"
                        "<path d='M56,37 l2.4,-1.6' stroke='%s' stroke-width='1.1' stroke-linecap='round' fill='none'/>"
                        "<ellipse cx='42' cy='45' rx='3' ry='2' fill='#ff9a9a' opacity='.32'/>"
                        "<ellipse cx='58' cy='45' rx='3' ry='2' fill='#ff9a9a' opacity='.32'/>") % (hair, hair)
    jnum = _esc(number) if number else ""
    return (
        "<svg viewBox='0 0 100 100' width='92' height='92'>"
        "<defs>"
        "<radialGradient id='%sM' cx='0.5' cy='0.32' r='0.95'>"
          "<stop offset='0' stop-color='%s'/><stop offset='1' stop-color='%s'/></radialGradient>"
        "<linearGradient id='%sJ' x1='0' y1='0' x2='0' y2='1'>"
          "<stop offset='0' stop-color='%s'/><stop offset='1' stop-color='%s'/></linearGradient>"
        "<linearGradient id='%sG' x1='0' y1='0' x2='1' y2='1'>"
          "<stop offset='0' stop-color='#ffffff' stop-opacity='.42'/><stop offset='1' stop-color='#ffffff' stop-opacity='0'/></linearGradient>"
        "</defs>"
        "<circle cx='50' cy='50' r='47' fill='url(#%sM)' stroke='#ffffff' stroke-width='2.4'/>"
        "<circle cx='50' cy='50' r='47' fill='url(#%sG)'/>"
        "<path d='M8,100 C10,76 28,64 50,63 C72,64 90,76 92,100 Z' fill='url(#%sJ)'/>"
        "<path d='M41,61 L50,69 L59,61' fill='none' stroke='#fff' stroke-width='2.6' stroke-linejoin='round' stroke-linecap='round'/>"
        "<rect x='45' y='52' width='10' height='13' rx='3.5' fill='%s'/>"
        "<rect x='45' y='52' width='10' height='13' rx='3.5' fill='#000' opacity='.06'/>"
        "<circle cx='50' cy='40' r='17' fill='%s'/>"
        "<path d='M50,23 a17,17 0 0 1 0,34 a17,17 0 0 0 0,-34 Z' fill='#000' opacity='.06'/>"
        "<circle cx='33' cy='40' r='3' fill='%s'/><circle cx='67' cy='40' r='3' fill='%s'/>"
        "<path d='%s' fill='%s'/>%s%s"
        "<path d='M42,35 Q46,33 50,35' fill='none' stroke='%s' stroke-width='1.4' stroke-linecap='round'/>"
        "<path d='M50,35 Q54,33 58,35' fill='none' stroke='%s' stroke-width='1.4' stroke-linecap='round'/>"
        "<circle cx='46' cy='39' r='2' fill='#2a2a2a'/><circle cx='54' cy='39' r='2' fill='#2a2a2a'/>%s%s"
        "<path d='M50,40 L48.5,45 Q50,46 51.5,45' fill='none' stroke='#000' stroke-opacity='.16' stroke-width='1' stroke-linecap='round'/>"
        "<path d='M45,48 Q50,52 55,48' fill='none' stroke='#b5654d' stroke-width='1.7' stroke-linecap='round'/>"
        "<text x='50' y='88' font-size='28' font-weight='900' text-anchor='middle' fill='#fff' stroke='%s' stroke-width='0.8' font-family='Arial'>%s</text>"
        "</svg>"
    ) % (
        gid, _shade(team_color, 1.35), _shade(team_color, 0.5),
        gid, _shade(team_color, 1.12), _shade(team_color, 0.6),
        gid,
        gid, gid,
        gid,
        skin, skin, skin, skin,
        hair_path, hair, bun, hair_gloss,
        hair, hair, eye_catch, female_extra,
        _shade(team_color, 0.5), jnum,
    )


def _player_star_rating(p):
    """重点球员的「焦点星级」（1~5★）：采用**统一公开成就分级标准**（仅标注信息关注度，非实力排名、不构成赛果判断）。

    统一评级标准（数据可直接用 star 字段指定 1~5，优先级最高；缺省时按以下标准映射）：
    - ★★★★★ 传奇/历史级：奥运金牌×2 或 大满贯×15+ 或 全时代纪录（如历史得分王）等；
    - ★★★★ 顶尖/世界级：奥运金牌×1 或 大满贯/世锦赛/总决赛单打冠军 或 单赛季三冠王等；
    - ★★★ 一流/国际级：世界杯/洲际冠军 或 奥运奖牌（非金）或 顶级联赛核心主力；
    - ★★ 准一流：欧洲主流联赛主力、洲际赛事常客；
    - ★ 潜力/新星：新生代重点观察对象。
    说明：本标准为公开荣誉的整理性分级，用于让不同球员的星数直观可区分，不代表任何赛果倾向。
    """
    if isinstance(p.get("star"), int) and 1 <= p["star"] <= 5:
        return p["star"]
    # 缺省映射（与上方统一标准对齐，保证可区分、不聚类于 1★）
    achieve = str(p.get("achievement", "") or "")
    role = str(p.get("role", "") or "")
    status = str(p.get("status", "") or "")
    score = 1
    if any(k in achieve for k in ("金满贯", "历史得分王", "大满贯×2", "×2 奥运", "2届奥运", "奥运金牌×2", "24座", "超级全满贯")):
        score = 5
    elif any(k in achieve for k in ("奥运金牌", "大满贯", "三冠王", "总冠军", "世锦赛冠军", "FMVP", "世界杯冠军")):
        score = 4
    elif any(k in achieve for k in ("奥运", "亚运", "全英", "洲际", "银", "铜")):
        score = 3
    elif p.get("key"):
        score = 3
    if status in ("首发", "健康"):
        score = max(score, 3)
    return max(1, min(5, score))


def player_spotlight_html(players, key_players, match_id="", form_map=None):
    """返回重点球员聚焦卡组（CSS 动画 + 纯 SVG 矢量头像，离线可用、零二进制）。
    优先 key_players，否则 key=True 的球员，否则前 3。头像按性别区分男女、按
    姓名+球队+比赛 复合种子保证互不相同；球衣带背号；卡内附近 5 场走势。"""
    picks = []
    if key_players:
        picks = [dict(k) for k in key_players]
    else:
        picks = [p for p in (players or []) if p.get("key")]
        if not picks:
            picks = (players or [])[:3]
    if not picks:
        return ""
    # 去重（按 name+team）
    seen, uniq = set(), []
    for p in picks:
        key = (p.get("name", ""), p.get("team", ""))
        if key in seen:
            continue
        seen.add(key); uniq.append(p)
    cards = ""
    for p in uniq:
        nm = _esc(p.get("name", "?"))
        tm = _esc(p.get("team", ""))
        role = _esc(p.get("role", ""))
        status = p.get("status", "") or "—"
        sc = _player_status_score(status if status != "—" else "")
        # 本场权重：核心/主力更高
        weight = 0.92 if (p.get("key") or role) else 0.6
        stcolor = "#2E8B57" if sc > 0.8 else ("#E8A100" if sc > 0.4 else "#E50012")
        avatar = p.get("avatar", "")
        number = str(p.get("number", p.get("jersey", "") or "")).strip()
        team_color = CLUB_BADGES.get(p.get("team", ""), (_AV_TEAM[_stable(tm) % len(_AV_TEAM)], ""))[0]
        if avatar:
            # 真实头像：图片填入动画圆框（须为已获合法授权的素材）
            fig = ("<img class='pav' src='%s' alt='%s'/>") % (_esc(avatar), nm)
        elif p.get("avatar_b64"):
            # 真实头像（base64 内嵌，离线自包含、零二进制文件）
            fig = ("<img class='pav' src='data:image/png;base64,%s' alt='%s'/>") % (_esc(p["avatar_b64"]), nm)
        else:
            # 合规矢量头像：按性别区分男女、按 姓名+球队+比赛 复合种子保证互不相同
            fig = _player_avatar_svg(p, match_id)
        form_list = (form_map or {}).get(p.get("team", "")) or []
        spark = _form_spark(form_list)
        ach = _esc(p.get("achievement", "") or "")
        bar1 = int(round(sc * 100))
        bar2 = int(round(weight * 100))
        stars = _player_star_rating(p)
        stars_str = "★" * stars + "☆" * (5 - stars)
        cards += (
            "<div class='pspot' style='--pc:%s'>"
            "<span class='ptag'><b class='pstars'>%s</b> 重点</span>"
            "<div class='phead'>"
            "<div class='pfig'><div class='pring'></div><div class='psonar'></div>%s<div class='pglow'></div></div>"
            "<div class='pach'><span class='pacht'>🏆 生涯最高成就</span><span class='pachtxt'>%s</span></div>"
            "</div>"
            "<div class='pname'>%s</div>"
            "<div class='pteam'>%s</div>"
            "<div class='prole'>%s</div>"
            "<div class='pstatus' style='color:%s'>● %s</div>"
            "<div class='pform'><span class='pformlab'>近5场</span>%s</div>"
            "</div>") % (team_color, stars_str, fig, ach, nm, tm, role, stcolor, _esc(status), spark)
    return ("<div class='psgrid'>%s</div>"
            "<div class='note'>⭐ 重点球员聚焦（动画）：头像为合规矢量插画，按性别区分男女、不同球员互不相同，"
            "背号取自球衣；头像右侧金色成就条为该球员「职业生涯最高成就」（公开荣誉整理，联网核实，按内容自适应高度）。焦点星级（1~5★）依据统一"
            "公开成就分级标准评定（详见报告说明），仅标注信息关注度，非实力排名、不构成任何赛果判断。近 5 场为公开战绩走势"
            "示意，不代表任何赛果倾向；任何球员状态以官方首发名单为准。</div>") % cards


def home_hex(v):
    # 把 0-1 转成绿色深浅（仅用于动画点缀，不改变语义）
    g = int(120 + 100 * v)
    return "#%02x%02x%02x" % (40, min(g, 220), 90)

# ===========================================================================
# 赛事目录（覆盖主流足球/篮球赛事 · 用于报告自动标注联赛风格特征）
# 数据依据：各联赛官方资料 + 公开场均进球统计（德甲3.2 / 法甲2.9 / 英超2.7 / 西甲2.6 / 意甲2.2 等）。
# 场均进球为近似值，仅作"联赛风格提示"，不构成任何走向判断。
# ===========================================================================
LEAGUES = {
    # ===================== 足球 · 顶级联赛 =====================
    "英超": ("football", 2.7, "节奏快、对抗强、无弱旅、强弱对话多"),
    "西甲": ("football", 2.6, "技术流传控、主场优势极强、平局/小比分高发"),
    "德甲": ("football", 3.2, "崇尚进攻、场均进球五大联赛最多、进球数偏多"),
    "意甲": ("football", 2.2, "重防守、链式防守传统、平局较多、场均进球最少"),
    "法甲": ("football", 2.9, "巴黎断层优势、强弱差距大、身体天赋突出"),
    "葡超": ("football", 2.6, "技术流、本菲卡/波尔图双雄主导"),
    "荷甲": ("football", 3.0, "全攻全守、进球多、青年球员跳板"),
    "比甲": ("football", 2.9, "进攻开放、进球多、年轻人温床"),
    "苏超": ("football", 2.7, "凯尔特人/流浪者双雄、节奏快、主场狂热"),
    "土超": ("football", 2.6, "身体对抗、主场氛围热烈、争议多"),
    "俄超": ("football", 2.3, "身体对抗、冬歇长"),
    "瑞超": ("football", 2.6, "北欧、气候影响、存在意外"),
    "奥甲": ("football", 2.8, "萨尔茨堡主导、年轻化"),
    "瑞士超": ("football", 2.8, "北欧风格、存在意外"),
    "丹超": ("football", 2.7, "北欧、主场强"),
    "挪超": ("football", 2.8, "北欧、夏季赛季、进球多"),
    "芬超": ("football", 2.6, "北欧、信息透明度低、谨慎"),
    "瑞典超": ("football", 2.6, "北欧、身体对抗、信息需谨慎甄别"),
    # ===================== 足球 · 美洲 =====================
    "巴甲": ("football", 2.2, "南美技术流、体能消耗大、主场极强"),
    "阿甲": ("football", 2.2, "南美、主场优势明显、派系复杂"),
    "美职联": ("football", 2.8, "旅途长、阵容轮换大、扩军后战力分散"),
    "墨超": ("football", 2.5, "中北美技术流、主场优势大"),
    "解放者杯": ("football", 2.3, "南美俱乐部杯、高原主场杀手"),
    "南美杯": ("football", 2.3, "南美第二俱乐部杯"),
    # ===================== 足球 · 亚洲/大洋洲 =====================
    "日职": ("football", 2.5, "技术细腻、纪律强、亚洲早场焦点"),
    "J联赛": ("football", 2.5, "日职别名"),
    "韩K": ("football", 2.4, "身体对抗、主场硬朗"),
    "K联赛": ("football", 2.4, "韩K别名"),
    "澳超": ("football", 2.7, "全攻全守、进球偏多"),
    "中超": ("football", 2.4, "身体对抗、主场氛围、外援影响大"),
    "中甲": ("football", 2.4, "中超次级、冲超战意强"),
    "亚冠": ("football", 2.5, "亚洲俱乐部顶级杯、西亚主导"),
    "亚协杯": ("football", 2.4, "亚洲第二级别俱乐部杯"),
    # ===================== 足球 · 次级联赛 =====================
    "英冠": ("football", 2.5, "次级、竞争烈、升级战意"),
    "英甲": ("football", 2.5, "第三级、竞争烈"),
    "德乙": ("football", 2.7, "次级、进球偏多"),
    "意乙": ("football", 2.2, "次级、保守"),
    "法乙": ("football", 2.3, "次级联赛"),
    "西乙": ("football", 2.2, "次级联赛"),
    # ===================== 足球 · 国内杯赛 =====================
    "英足总杯": ("football", 2.7, "杯赛、意外多发、弱旅遇强队"),
    "足总杯": ("football", 2.7, "英足总杯别名"),
    "德国杯": ("football", 2.8, "杯赛、强队轮换、意外"),
    "意大利杯": ("football", 2.3, "杯赛、防守谨慎"),
    "法国杯": ("football", 2.4, "杯赛、意外多"),
    "国王杯": ("football", 2.6, "西甲杯赛、强队重视"),
    "荷兰杯": ("football", 2.9, "杯赛、进球多"),
    # ===================== 足球 · 欧战 =====================
    "欧冠": ("football", 2.8, "顶级豪门、强强对话多、赛前数据最精准"),
    "欧联": ("football", 2.6, "中下游豪门+劲旅"),
    "欧会": ("football", 2.5, "第三级别欧战、存在爆冷机会"),
    "欧协联": ("football", 2.5, "欧会别名"),
    "欧国联": ("football", 2.4, "国家队、战意参差（部分场次练兵）"),
    # ===================== 足球 · 国家队大赛 =====================
    "世界杯": ("football", 2.4, "国家队、战意极强（淘汰赛含加时与点球决胜）"),
    "欧洲杯": ("football", 2.3, "国家队、防守谨慎"),
    "美洲杯": ("football", 2.3, "南美、技术+身体"),
    "亚洲杯": ("football", 2.3, "亚洲、差距大"),
    "非洲杯": ("football", 2.2, "非洲、身体天赋、内乱影响"),
    "中北美洲金杯": ("football", 2.3, "中北美、美国/墨西哥主导"),
    "奥运男足": ("football", 2.4, "奥运会足球、年龄限制(U23+3)、战意强"),
    "友谊赛": ("football", 2.5, "热身赛、战意与轮换难料、谨慎对待"),
    "世俱杯": ("football", 2.5, "洲际俱乐部杯"),
    # ===================== 篮球 · 联赛 =====================
    "NBA": ("basketball", None, "美职篮、球星主导、节奏快、总得分波动大"),
    "CBA": ("basketball", None, "中国男子篮球职业联赛、主场优势明显"),
    "WNBA": ("basketball", None, "女子NBA、节奏较快"),
    "美职女篮": ("basketball", None, "WNBA别名、女子职业篮球"),
    "欧篮联": ("basketball", None, "欧洲顶级俱乐部篮球、皇马/米兰等"),
    "西篮联": ("basketball", None, "西班牙篮球甲级(含欧篮联级别)、皇马/巴萨主导"),
    "土超篮球": ("basketball", None, "土耳其篮球、费内巴切/艾菲斯"),
    "以超篮球": ("basketball", None, "以色列篮球、欧洲赛场劲旅"),
    "VTB": ("basketball", None, "东欧篮球联赛、CSKA等"),
    "希腊篮球": ("basketball", None, "希腊顶级篮球、欧洲强队"),
    "亚得里亚海联赛": ("basketball", None, "前南地区ABA联赛、欧洲二级"),
    # ===================== 篮球 · 国家队大赛 =====================
    "奥运篮球": ("basketball", None, "奥运会篮球、NBA球星参赛"),
    "世界杯篮球": ("basketball", None, "篮球世界杯、国家队"),
    "欧洲杯篮球": ("basketball", None, "欧洲篮球锦标赛"),
    "美洲杯篮球": ("basketball", None, "美洲篮球锦标赛"),
    "亚洲杯篮球": ("basketball", None, "亚洲篮球锦标赛"),
}


def league_info(name):
    """返回 (sport, avg_goals|None, note) 或 None。"""
    if not name:
        return None
    return LEAGUES.get(name.strip())


def gather_queries(match, league="", city="", country="", teams=None, kickoff_local="", kickoff_tz=""):
    """
    给定赛事信息，返回一份结构化的检索清单（每类数据对应的检索词与用途）。
    调用本 Skill 的模型应据此用 WebSearch/WebFetch 逐项采集，并按 verification 分级。
    """
    t = teams or (match.split(" vs ") if " vs " in match else match.split(" "))
    home = t[0] if len(t) > 0 else ""
    away = t[1] if len(t) > 1 else ""
    items = [
        ("开赛时间/时差", "【%s】开赛时间 当地时间 北京时间 时差 %s" % (match, kickoff_tz or ""), "kickoff_local/kickoff_utc 双显(时差比赛必填)"),
        ("基本面/积分排名", "【%s %s】积分榜 排名 近期战绩" % (league, match), "竞技实力基线"),
        ("主客场表现", "【%s】主场战绩 / %s 客场战绩" % (home, away), "主场优势量化"),
        ("近5场状态", "【%s %s】近5场 战绩 赛果" % (home, away), "form 输入"),
        ("交锋历史", "【%s vs %s】历史交锋 近5次" % (home, away), "h2h 输入"),
        ("伤停/停赛", "【%s %s】伤停 停赛 出战成疑 赛前名单" % (home, away), "injury 输入"),
        ("战意/赛程", "【%s %s】战意 赛程密集 轮换 杯赛" % (home, away), "motiv 输入"),
        ("天气(比赛日)", "%s 天气 比赛日 温度 湿度 降水 风速" % (city or country), "weather 输入(温度/湿度/风/降水均采集)"),
        ("赛前情报/传闻", "【%s %s】赛前消息 发布会 阵容前瞻 小道消息 传闻" % (home, away), "intel 分级(未证实需标注)"),
    ]
    return items


def _esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _form_chips(seq):
    """把 ['胜','平','负'] 变成带颜色的 chip HTML。"""
    color = {"胜": "#2E8B57", "平": "#888", "负": "#E50012"}
    out = ""
    for x in seq:
        c = color.get(x, "#666")
        out += "<span class='chip' style='background:%s22;color:%s;border-color:%s'>" % (c, c, c) + _esc(x) + "</span>"
    return out or "<span class='muted'>无</span>"


def _build_match_body(data, uid=""):
    """生成单场报告正文（纯信息整理与可视化，不做赛果判断、不评估赛果走向）。"""
    match = data.get("match", "未命名赛事")
    league = data.get("league", data.get("competition", ""))
    country = data.get("country", "")
    match_id = _stable("%s|%s" % (match, league))  # 用于头像复合种子，保证不同比赛观感不同
    cflag = flag_svg(country)
    teams = data.get("teams", [])
    home_color = CLUB_BADGES.get((teams[0].get("name", "") if teams else ""), ("#1677ff", ""))[0]
    away_color = CLUB_BADGES.get((teams[1].get("name", "") if len(teams) > 1 else ""), ("#E50012", ""))[0]
    formations = data.get("formations", [])
    kickoff_local = data.get("kickoff_local", "")
    kickoff_actual = data.get("kickoff_actual", "")
    venue = data.get("venue", ""); city = data.get("city", "")
    weather = data.get("weather", {})
    players = data.get("players", [])
    key_players = data.get("key_players", [])
    form = data.get("form_last5", {})
    h2h = data.get("h2h_last5", [])
    intel = data.get("intel", [])
    experts = data.get("experts", [])
    analysis = data.get("analysis", "")
    confidence = data.get("confidence", "未评估")
    risk = data.get("risk", "请自行评估，量力而行。")
    sport = normalize_sport(data.get("sport", "football"))
    li = league_info(league) if league else None

    # 球队行（队徽 SVG + 队名）
    team_html = ""
    for t in teams:
        badge = club_badge_svg(t.get("name", ""))
        nm = _esc(t.get("name", "?"))
        note = _esc(t.get("status_note", ""))
        team_html += "<span class='team'>%s <b>%s</b> %s</span>" % (badge, nm, ("<i>%s</i>" % note if note else ""))
    if not team_html:
        team_html = "<b>%s</b>" % _esc(match)

    # 天气
    weather_html = ""
    if weather:
        wrows = [
            ("温度", weather.get("temp", "—")),
            ("湿度", weather.get("humidity", "—")),
            ("风力/天气", "%s %s" % (weather.get("condition", ""), weather.get("wind", ""))),
            ("降水/体感", weather.get("rain", weather.get("feels", "—"))),
        ]
        weather_html = "<table><tbody>" + "".join(
            "<tr><th>%s</th><td>%s</td></tr>" % (_esc(k), _esc(v)) for k, v in wrows
        ) + "</tbody></table>"
        if weather.get("impact"):
            weather_html += "<div class='note'>🌡️ 天气影响：%s</div>" % _esc(weather["impact"])

    # 球员状态
    player_html = ""
    if players:
        rows = "".join(
            "<tr><td>%s%s</td><td>%s</td><td class='%s'>%s</td><td>%s</td></tr>" % (
                ("⭐" if p.get("key") else ""),
                _esc(p.get("name", "")), _esc(p.get("team", "")),
                ("ok" if p.get("status", "") in ("健康", "首发", "复出") else "warn"),
                _esc(p.get("status", "")),
                _esc(((p.get("role", "") + "　") if p.get("role") else "") + p.get("note", "")))
            for p in players)
        player_html = ("<table><thead><tr><th>球员</th><th>球队</th><th>状态</th><th>备注/角色</th></tr></thead>"
                       "<tbody>%s</tbody></table>" % rows)
    if key_players:
        chips = "".join(
            "<span class='chip'>⭐ %s%s%s</span>" % (
                _esc(k.get("name", "")),
                ("（%s）" % _esc(k.get("team", ""))) if k.get("team") else "",
                (" · %s" % _esc(k.get("role", ""))) if k.get("role") else "")
            for k in key_players)
        player_html += "<div class='formblk' style='margin-top:10px'><div class='flab'>⭐ 主力/核心球员</div>%s</div>" % chips
    elif not players:
        player_html = "<div class='muted'>未提供</div>"

    # 重点球员聚焦（动画卡）
    spotlight_html = player_spotlight_html(players, key_players, match_id=match_id, form_map=form)

    # 近5场 / 交锋
    form_html = ""
    if form:
        blocks = ""
        for team, seq in form.items():
            blocks += "<div class='formblk'><div class='flab'>%s 近5场</div>%s</div>" % (_esc(team), _form_chips(seq))
        form_html += "<div class='forms'>%s</div>" % blocks
    if h2h:
        form_html += "<div class='formblk'><div class='flab'>交锋近5次</div>%s</div>" % _form_chips(h2h)

    # 近况对比表（由 form_last5 派生，纯描述事实，不加任何走向判断）
    cmp_html = ""
    if form:
        teams_f = list(form.keys())

        def _cnt(seq):
            s = [str(x) for x in seq]
            return s.count("胜"), s.count("平"), s.count("负")

        cells = []
        for t in teams_f:
            w, d, l = _cnt(form.get(t, []))
            cells.append("<td>胜%s · 平%s · 负%s</td>" % (w, d, l))
        cmp_html = ("<table class='cmptab'><tbody>"
                   "<tr><th>近5场战绩</th>%s</tr>"
                   "</tbody></table>"
                   "<div class='note'>近5场战绩为公开赛果整理（胜/平/负），仅呈现事实，不代表任何走向判断。</div>") % "".join(cells)
        form_html = cmp_html + form_html

    # 情报分级
    intel_html = ""
    if intel:
        tier_class = {"官方": "ok", "权威媒体": "info", "未证实传闻": "warn", "社媒传闻": "warn"}
        items = ""
        for it in intel:
            tier = it.get("tier", "未分级")
            cls = tier_class.get(tier, "muted")
            items += "<li class='%s'><span class='badge %s'>%s</span> %s</li>" % (
                cls, cls, _esc(tier), _esc(it.get("text", "")))
        intel_html = "<ul class='intel'>%s</ul><div class='note'>⚠️ 未证实传闻仅作视野补充，<b>绝不可作为研判依据</b>。</div>" % items

    # 专家观点（权威 / 非权威，分级 + 视觉权威化）
    expert_html = ""
    if experts:
        # 本场专家新鲜度标识：联网核实(本期新采集) / 精选静态库(示例兜底)
        if data.get("experts_refreshed_at"):
            fresh_tag = ("<div class='ex-fresh ok'>🔄 本场专家观点已于 %s 联网核实更新（来源见各条）</div>"
                         % _esc(data.get("experts_refreshed_at")))
        elif data.get("experts_static"):
            fresh_tag = "<div class='ex-fresh'>📚 本场为示例兜底，专家为精选静态库（非本期新采集）</div>"
        else:
            fresh_tag = ""
        _order = {"权威专家": 0, "数据方分析师": 1, "知名解说": 2,
                  "非权威专家": 3, "民间高手": 4, "社媒博主": 5}
        _conf = {"权威专家": ("高", "ok"), "数据方分析师": ("较高", "info"), "知名解说": ("中", "info"),
                 "非权威专家": ("低", "warn"), "民间高手": ("很低", "warn"), "社媒博主": ("极低", "warn")}
        experts_sorted = sorted(experts, key=lambda e: _order.get(e.get("tier", "非权威专家"), 9))
        items = ""
        for e in experts_sorted:
            tier = e.get("tier", "非权威专家")
            conf, cls = _conf.get(tier, ("低", "warn"))
            verified = tier in ("权威专家", "数据方分析师", "知名解说")
            vmark = "<span class='ex-verify'>✔ 已核验来源</span>" if verified else ""
            caution = "" if verified else "<span class='ex-caution'>⚠ 谨慎参考 · 警惕付费参照方案</span>"
            mono = (_esc(e.get("name", "?"))[:1] if e.get("name") else "?")
            items += (
                "<li class='expert %s'>"
                  "<div class='ex-head'>"
                    "<span class='ex-ava'>%s</span>"
                    "<div class='ex-id'><b>%s</b><span class='ex-src'>%s</span></div>"
                    "%s"
                  "</div>"
                  "<div class='ex-body'>%s</div>"
                  "<div class='ex-foot'>"
                    "<span class='badge %s'>%s</span> 可信度：<b>%s</b> %s"
                  "</div>"
                "</li>") % (
                cls, mono, _esc(e.get("name", "")), _esc(e.get("source", "")),
                vmark, _esc(e.get("view", "")), cls, _esc(tier), conf, caution)
        expert_html = ("%s<ul class='experts'>%s</ul>"
                       "<div class='note'>⚠️ 专家观点仅供参考：<b>任何专家都不保证结果</b>；"
                       "非权威/民间观点尤须警惕，凡要求「付费参照方案/虚假爆料」者一律视为诈骗。</div>") % (fresh_tag, items)

    # 时间 / 赛事口径
    updated_at = data.get("updated_at", "")
    tz_html = ""
    if kickoff_local or kickoff_actual or updated_at:
        tz_html = ("<div class='kick'>🕒 开赛时间："
                   "<span class='kl'>当地 <b>%s</b></span>"
                   "<span class='kb'>北京时间 <b>%s</b></span>"
                   "%s</div>") % (
            _esc(kickoff_local) if kickoff_local else "待定",
            _esc(kickoff_actual) if kickoff_actual else "待定",
            ("<span class='ku'>📡 数据更新 <b>%s</b></span>" % _esc(updated_at)) if updated_at else "")

    SPORT_LABELS = {k: v["label"] for k, v in SPORTS.items()}
    SPORT_ICONS = {k: v["icon"] for k, v in SPORTS.items()}
    sport_icon = SPORT_ICONS.get(sport, "🏟️")
    sport_label = SPORT_LABELS.get(sport, "其它球类")
    time_rule = "⏱️ 结算口径：" + SPORTS.get(sport, {}).get(
        "settle", "请按该项目官方常规赛事规则判定（是否含加时/决胜局以官方为准）；本分析仅供参考。")
    league_hint = ""
    if li:
        league_hint = "<div class='note'>📊 赛事特征（%s · %s）：%s</div>" % (sport_label, _esc(league), li[2])
    mkt = observe_templates(sport)
    mkt_hint = ("<div class='note'>🎯 本场常见观察维度：%s</div>" % " · ".join(_esc(x) for x in mkt)) if mkt else ""

    # 自查自纠（质量闸门）：对单场做一致性检查
    audit_res = None
    if _audit:
        try:
            audit_res = _audit.check_match(data, strict=False)
        except Exception:
            audit_res = None

    team_txt = " vs ".join(_esc(t.get("name", "")) for t in teams) or match
    venuestr = venue or city or ""
    _jt = "<span class='jt' onclick=\"jumpTo('sec-info%s')\">🔬 信息要点</span>" % ("-" + uid if uid else "")
    if form or h2h:
        _jt += "<span class='jt' onclick=\"jumpTo('sec-form%s')\">📊 状态对比</span>" % ("-" + uid if uid else "")
    if experts:
        _jt += "<span class='jt' onclick=\"jumpTo('sec-expert%s')\">🎙️ 专家观点</span>" % ("-" + uid if uid else "")
    _jt_html = "<div class='jumptabs'>%s</div>" % _jt
    info_part = (
        info_panel_html(data, uid)
        + _jt_html
        + audit_badge_html(audit_res)
        + formations_html(formations, home_color, away_color, sport, uid)
        + _sec("一、赛事概况与天气", league_hint + time_rule + mkt_hint + (weather_html or "<div class='muted'>未提供天气数据</div>"))
        + (_sec("三、近期状态与交锋", form_html or "<div class='muted'>未提供</div>", "form" + ("-" + uid if uid else "")) if (form or h2h) else "")
        + (_sec("四、赛前情报（分级）", intel_html) if intel else "")
        + (_sec("五、专家观点（权威/非权威）", expert_html, "expert" + ("-" + uid if uid else "")) if experts else "")
        + _sec("六、分析逻辑", "<div class='analysis'>%s</div>" % _esc(analysis))
        + _sec("七、结论与风险提示", "<div class='hmeta'>综合信心：<b>%s</b></div><div class='analysis'>%s</div>" % (_esc(confidence), _esc(risk)))
    )
    players_part = ""
    if spotlight_html:
        players_part += _sec("⭐ 重点球员聚焦（动画）", spotlight_html)
    if players:
        players_part += _sec("二、球员状态", player_html or "<div class='muted'>未提供</div>")
    if not players_part:
        players_part = ("<div class='pp-note'>⭐ 本场暂无明星球员聚焦数据。战术风格 / 伤停 / 关键球员等维度，"
                       "可在生成报告时由智能体按需联网补充，本报告仅呈现已核实的公开赛程信息。</div>")
    body = "<div class='mv-info'>%s</div>" % info_part
    body += "<div class='mv-players'>%s</div>" % players_part
    # 返回结构与旧版兼容：body + 三个占位（原对照表/组合，现已废弃置空）+ 元数据
    return body, [], [], team_txt, sport_label, league, country, cflag, teams, match, venuestr, tz_html


def _sec(title, body, sec_id=None):
    if not body:
        return ""
    sid = (" id='sec-%s'" % sec_id) if sec_id else ""
    return "<div class='card'%s><h2>%s</h2>%s</div>" % (sid, title, body)


def info_panel_html(data, uid=""):
    """赛事信息要点面板：把本场可讨论的信息要点结构化呈现，纯描述、无赛果走向评估。"""
    points = data.get("info_points") or []
    kp = data.get("key_players") or []
    if not points:
        intel = data.get("intel") or []
        points = [i.get("text", "") for i in intel if i.get("text")]
    kp_names = [p.get("name", "") for p in kp if p.get("name")]
    if not points and not kp_names:
        return ""
    items = "".join("<li>%s</li>" % _esc(p) for p in points[:8] if p)
    kp_html = ""
    if kp_names:
        kp_html = "<div class='pnote'>⭐ 本场重点球员：%s（报告含其聚焦动画）</div>" % _esc("、".join(kp_names[:6]))
    return ("<div class='card info-panel' id='sec-info%s'><h2>🔬 赛事信息要点（纯描述，供观赛讨论）</h2>"
            "<ul class='deep'>%s</ul>%s"
            "<div class='oh-note'>⚠️ 本面板仅做信息整理与对比，不做结果判断、不评估赛果走向；"
            "任何判断须结合基本面与可靠信息。</div></div>") % (("-" + _esc(uid)) if uid else "", items, kp_html)


def audit_badge_html(res):
    """自查自纠结论徽章（来自 audit.check_match 的单场结果）。"""
    if not res:
        return ""
    av = res.get("avatar_issues", [])
    an = res.get("analysis_issues", [])
    corr = res.get("corrections", [])
    av_crit = sum(1 for k, _ in av if k in ("重复", "破损", "性别"))
    ok = (av_crit == 0 and len(an) == 0)
    cls = "pass" if ok else "warn"
    lines = ""
    for k, msg in av:
        if k in ("重复", "破损", "性别"):
            lines += "<li class='ab-cri'>❌ 头像/%s：%s</li>" % (k, _esc(msg))
    for k, msg in an:
        lines += "<li class='ab-cri'>❌ 分析/%s：%s</li>" % (k, _esc(msg))
    corr_html = ""
    if corr:
        corr_html = "<div class='ab-corr'>🛠️ 已自纠 %d 项：%s</div>" % (len(corr), "；".join(_esc(c) for c in corr))
    return ("<div class='card audit-badge %s'><h2>🛡️ 自查自纠（质量闸门）</h2>"
            "<div class='ab-row'><span class='ab-pill %s'>头像 %s</span>"
            "<span class='ab-pill %s'>分析 %s</span>"
            "<span class='ab-pill ok'>自纠 %d 项</span>"
            "<span class='ab-pill %s'>新鲜度 %s</span></div>"
            "%s%s"
            "<div class='pnote'>机器已对本场数据做一致性自查（可信度/新鲜度等），"
            "可纠正项已自动归一化/去重/剔除；剩余风险请人工留意。仍不保证赛果。</div></div>") % (
        cls,
        ("ok" if av_crit == 0 else "bad"), ("通过" if av_crit == 0 else "%d 风险" % av_crit),
        ("ok" if len(an) == 0 else "bad"), ("通过" if len(an) == 0 else "%d 项" % len(an)),
        len(corr),
        ("ok" if res.get("freshness") in ("新鲜", "未知") else "warn"), res.get("freshness", "未知"),
        ("<ul class='ab-list'>" + lines + "</ul>" if lines else ""), corr_html)


def anti_scam_html():
    """防骗盾：固定品牌卡，强调「分级专家+来源核验+警惕付费方案」，强化打假人设（合规、零敏感词）。"""
    items = [
        ("🛡️ 只做信息整理", "本工具仅做公开赛事信息的整理、对比与可视化，不做赛果判断、不提供任何结论性建议。"),
        ("🔎 专家分级 + 来源核验", "权威 / 数据方 / 解说类观点标注来源与可信度，并打「✔ 已核验来源」；非权威观点明确标「谨慎参考」。"),
        ("🚫 主动打假收费话术", "凡要求「付费参照方案 / 内部情报 / 高回报承诺」者，一律判定为诈骗话术并提示警惕，绝不直接或间接转述。"),
        ("⏳ 不保证赛果", "体育比赛存在大量不可建模的偶然因素（判罚、伤病、赛前最新状态），任何分析都无法消除不确定性。"),
    ]
    grid = "".join("<div class='sc-item'><b>%s</b><span>%s</span></div>" % (_esc(a), _esc(b)) for a, b in items)
    return ("<div class='card antiscam'><h2>🛡️ 防骗盾 · 本工具立场（打假人设）</h2>"
            "<div class='sc-grid'>%s</div>"
            "<div class='pnote' style='color:#cfe9d8;background:rgba(255,255,255,.06);border-color:rgba(245,197,24,.30)'>"
            "把「不忽悠、可追溯、敢打假」做成品牌：你在这份报告里看到的每一条专家观点都有来源与可信度标记，"
            "遇到任何「保证结果 / 付费方案」话术请直接举报。理性观赛、量力而行。</div></div>") % grid


def share_card_html(matches, kind="daily"):
    """分享要点卡（裂变）：干净可传播的要点卡 + 内联 JS 复制/保存（零外部库、零二进制）。"""
    if kind == "single" and matches:
        m = matches[0]
        tt = m.get("match", "单场分析")
        lg = m.get("league", "")
        raw = []
        if m.get("info_points"):
            raw = list(m["info_points"][:4])
        elif m.get("key_players"):
            raw = ["%s（%s）" % (p.get("name", ""), p.get("team", "")) for p in m["key_players"][:4] if p.get("name")]
        title = ("%s · %s" % (tt, lg)) if lg else tt
        scope = "单场观赛要点"
    else:
        raw = []
        for m in matches[:5]:
            kp = m.get("key_players") or []
            nm = "、".join(p.get("name", "") for p in kp[:2] if p.get("name"))
            tt = m.get("match", "")
            if nm:
                raw.append("%s：%s" % (tt, nm))
        title = "今日体育赛事总览 · 共 %d 场" % len(matches)
        scope = "今日赛事（含重点球员聚焦）"
    # 竖版长图用：每场焦点对阵（金边队徽）+ 重点球员头像缩略元数据
    metas = []
    for m in matches[:4]:
        tnames = []
        ts = m.get("teams") or []
        if ts:
            tnames = [t.get("name", "") for t in ts][:2]
        elif m.get("match"):
            tnames = [x.strip() for x in m["match"].split("vs")][:2]
        kps = m.get("key_players") or []
        pls = [{"name": p.get("name", ""), "team": p.get("team", ""),
                "number": str(p.get("number", "—")), "region": p.get("region", "欧美")}
               for p in kps[:2] if p.get("name")]
        metas.append({"match": m.get("match", ""), "teams": tnames, "players": pls})
    disp = "".join("<li>%s</li>" % _esc(p) for p in raw) if raw else "<li>本场 / 今日信息详见完整报告</li>"
    payload = json.dumps({"title": title, "scope": scope, "points": raw, "matches_meta": metas}, ensure_ascii=False)
    return ("<div class='card sharecard'><h2>📤 分享要点卡（一键发群 / 朋友圈）</h2>"
            "<div class='sc-frame' id='shareFrame'>"
            "<div class='sc-kicker'>体育赛事可视化 · %s</div>"
            "<div class='sc-title'>%s</div>"
            "<ul class='sc-list'>%s</ul>"
            "<div class='sc-foot'>数据来源：公开赛事资料整理 · 仅合法赛事 · 理性观赛</div>"
            "</div>"
            "<button class='sc-btn' onclick=\"copyShare()\">复制要点文字</button>"
            "<button class='sc-btn alt' onclick=\"saveShare()\">保存为图片</button>"
            "<button class='sc-btn vbtn' onclick=\"saveShareV()\">🖼️ 竖版长图</button>"
            "<div class='sc-tip'>提示：竖版长图按 9:16 排版，适合发朋友圈；图片由本页实时生成，不上传任何服务器。</div>"
            "<script id='shareData' type='application/json'>%s</script>"
            "</div>") % (scope, _esc(title), disp, _esc(payload))


def feedback_html():
    """报告底部反馈闭环（👍/👎 + localStorage + 导出反馈，零二进制）。"""
    return ("<div class='card feedback'><h2>💬 这份报告对你有用吗？</h2>"
            "<div class='fb-btns'>"
            "<span class='fb-btn up' onclick=\"fbVote('up',this)\">👍 很有用</span>"
            "<span class='fb-btn down' onclick=\"fbVote('down',this)\">🤔 一般</span>"
            "</div>"
            "<div class='fb-msg' id='fbMsg'></div>"
            "<div class='fb-export' onclick=\"fbExport()\">导出我的反馈（本地 JSON）</div>"
            "<div class='sc-tip'>反馈仅保存在你本地浏览器，用于帮助本工具迭代更好用的维度；不会上传。</div>"
            "</div>")


ENHANCE_JS = "<script>" + """
function swView(btn, mode){var sec=btn.closest('section.mtch');if(!sec)return;var pl=sec.querySelector('.mv-players');if(mode==='players'&&(!pl||!pl.children.length))return;sec.classList.toggle('show-players', mode==='players');var bs=btn.parentNode.querySelectorAll('.vt');for(var i=0;i<bs.length;i++)bs[i].classList.remove('on');btn.classList.add('on');}
function jumpTo(id){var el=document.getElementById(id);if(!el)return;el.scrollIntoView({behavior:'smooth',block:'center'});el.classList.add('flash');setTimeout(function(){el.classList.remove('flash');},2000);}
function copyShare(){try{var d=JSON.parse(document.getElementById('shareData').textContent);var t='【体育赛事可视化】'+d.title+'\\n'+d.points.map(function(p,i){return (i+1)+'. '+p;}).join('\\n')+'\\n— 数据来源：公开赛事资料整理 · 仅合法赛事 · 理性观赛';navigator.clipboard.writeText(t).then(function(){alert('已复制要点，可粘贴到群聊 / 朋友圈');});}catch(e){alert('复制失败，请手动选择文本复制');}}
function saveShare(){var f=document.getElementById('shareFrame');if(!f){return;}var clone=f.cloneNode(true);clone.setAttribute('xmlns','http://www.w3.org/1999/xhtml');clone.style.width=f.offsetWidth+'px';clone.style.background='#fff';var svg='<svg xmlns="http://www.w3.org/2000/svg" width="'+f.offsetWidth+'" height="'+f.offsetHeight+'"><foreignObject x="0" y="0" width="100%" height="100%">'+new XMLSerializer().serializeToString(clone)+'</foreignObject></svg>';var blob=new Blob([svg],{type:'image/svg+xml;charset=utf-8'});var url=URL.createObjectURL(blob);var img=new Image();img.onload=function(){var c=document.createElement('canvas');c.width=img.width;c.height=img.height;c.getContext('2d').drawImage(img,0,0);URL.revokeObjectURL(url);c.toBlob(function(b){if(!b){alert('图片生成失败，请直接截图分享');return;}var a=document.createElement('a');a.download='赛事要点卡.png';a.href=URL.createObjectURL(b);a.click();},'image/png');};img.onerror=function(){alert('图片生成失败（部分浏览器限制），请直接截图分享');};img.src=url;}
function fbVote(v){try{var arr=JSON.parse(localStorage.getItem('sda_feedback')||'[]');arr.push({t:new Date().toISOString(),v:v});localStorage.setItem('sda_feedback',JSON.stringify(arr));}catch(e){}var msg=document.getElementById('fbMsg');if(msg)msg.textContent=(v==='up'?'感谢支持！会持续优化更好用的维度 🙌':'感谢反馈！欢迎导出反馈告诉我们该改进哪里。');}
function fbExport(){try{var arr=JSON.parse(localStorage.getItem('sda_feedback')||'[]');if(!arr.length){alert('暂无反馈记录');return;}var blob=new Blob([JSON.stringify(arr,null,2)],{type:'application/json'});var a=document.createElement('a');a.download='赛事报告反馈.json';a.href=URL.createObjectURL(blob);a.click();}catch(e){alert('导出失败');}}
function saveShareV(){var d;try{d=JSON.parse(document.getElementById('shareData').textContent);}catch(e){alert('数据缺失');return;}var W=540,pad=42,fsK=12,fsT=23,fsS=13,fsP=16,fsF=11,lhT=33,lhP=27;function esc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}function cw(c){return (c.charCodeAt(0)>0x2e80)?1.0:0.55;}function wrap(t,fs,maxW){var L=[],cur='',w=0;for(var i=0;i<t.length;i++){var cwc=fs*cw(t[i]);if(w+cwc>maxW&&cur){L.push(cur);cur=t[i];w=cwc;}else{cur+=t[i];w+=cwc;}}if(cur)L.push(cur);return L;}function teamColor(i){var cs=['#1f6feb','#e8482b','#16a34a','#9333ea','#d97706','#0ea5e9'];return cs[i%cs.length];}function skinColor(rg){if(rg==='亚洲')return '#f0c39b';if(rg==='非洲')return '#8a5a3b';return '#f3d2b3';}function crest(x,y,r,name,color){var g='<circle cx="'+x+'" cy="'+y+'" r="'+r+'" fill="'+color+'" stroke="#F5C518" stroke-width="3"/><text x="'+x+'" y="'+(y+r*0.35)+'" text-anchor="middle" fill="#ffffff" font-size="'+(r*0.85)+'" font-weight="800">'+esc(name.charAt(0))+'</text>';return g;}function miniAvatar(x,y,r,rg,num){var sk=skinColor(rg);var g='<circle cx="'+x+'" cy="'+y+'" r="'+r+'" fill="'+sk+'" stroke="#F5C518" stroke-width="2"/><path d="M '+(x-r)+' '+(y-1)+' Q '+x+' '+(y-r-7)+' '+(x+r)+' '+(y-1)+'" fill="#2b2b2b"/><text x="'+x+'" y="'+(y+r*0.45)+'" text-anchor="middle" fill="#0b3d2e" font-size="'+(r*0.72)+'" font-weight="800">'+esc(num)+'</text>';return g;}var maxW=W-pad*2;var titleL=wrap(d.title||'体育赛事可视化',fsT,maxW);var scopeL=wrap(d.scope||'',fsS,maxW);var ptL=[];(d.points||[]).forEach(function(p){wrap(p,fsP,maxW-20).forEach(function(x){ptL.push(x);});});if(!ptL.length)ptL=['本场信息详见完整报告'];var metas=(d.matches_meta||[]).slice(0,4);var s='<svg xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Microsoft YaHei,sans-serif"><defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b3d2e"/><stop offset="1" stop-color="#0d2b3a"/></linearGradient></defs>';s+='<rect width="'+W+'" height="4000" fill="url(#bg)"/>';s+='<rect x="0" y="0" width="'+W+'" height="6" fill="#F5C518"/>';var y=pad+fsK;s+='<text x="'+pad+'" y="'+y+'" fill="#F5C518" font-size="'+fsK+'" font-weight="800" letter-spacing="2">体育赛事可视化 · 观赛辅助</text>';y+=12;titleL.forEach(function(ln){s+='<text x="'+pad+'" y="'+(y+fsT)+'" fill="#ffffff" font-size="'+fsT+'" font-weight="800">'+esc(ln)+'</text>';y+=lhT;});y+=8;scopeL.forEach(function(ln){s+='<text x="'+pad+'" y="'+y+'" fill="#9fd9bf" font-size="'+fsS+'">'+esc(ln)+'</text>';y+=lhP;});y+=16;s+='<line x1="'+pad+'" y1="'+y+'" x2="'+(W-pad)+'" y2="'+y+'" stroke="#F5C518" stroke-opacity="0.45" stroke-width="1.5"/>';y+=24;s+='<text x="'+pad+'" y="'+y+'" fill="#F5C518" font-size="15" font-weight="800">今日观赛要点</text>';y+=10;ptL.forEach(function(ln){s+='<circle cx="'+(pad+5)+'" cy="'+(y+fsP-6)+'" r="3" fill="#F5C518"/><text x="'+(pad+18)+'" y="'+(y+fsP)+'" fill="#eafff5" font-size="'+fsP+'">'+esc(ln)+'</text>';y+=lhP;});if(metas.length){  y+=22;s+='<text x="'+pad+'" y="'+y+'" fill="#F5C518" font-size="15" font-weight="800">焦点对阵</text>';  metas.forEach(function(mt,idx){    y+=14;    var t1=mt.teams[0]||'',t2=mt.teams[1]||'',c1=teamColor(idx*2),c2=teamColor(idx*2+1);    var cyC=y+26;    s+=crest(pad+26,cyC,22,t1,c1);    s+=crest(W-pad-26,cyC,22,t2,c2);    s+='<text x="'+(W/2)+'" y="'+(cyC+6)+'" text-anchor="middle" fill="#ffffff" font-size="14" font-weight="800">VS</text>';    s+='<text x="'+(pad+26)+'" y="'+(cyC+38)+'" text-anchor="middle" fill="#cfe9dd" font-size="11">'+esc(t1)+'</text>';    s+='<text x="'+(W-pad-26)+'" y="'+(cyC+38)+'" text-anchor="middle" fill="#cfe9dd" font-size="11">'+esc(t2)+'</text>';    var pls=mt.players||[];    var ax0=pad+10, ay=cyC+58;    pls.forEach(function(p,k){var px=ax0+k*64; s+=miniAvatar(px,ay,16,p.region||'欧美',p.number||'—'); s+='<text x="'+px+'" y="'+(ay+30)+'" text-anchor="middle" fill="#eafff5" font-size="10">'+esc(p.name)+'</text>';});    y=ay+44;  });}y+=26;s+='<text x="'+pad+'" y="'+y+'" fill="#F5C518" font-size="15" font-weight="800">扫码看完整报告</text>';y+=14;var qx=W/2-55,qy=y,qsz=110;s+='<rect x="'+qx+'" y="'+qy+'" width="'+qsz+'" height="'+qsz+'" rx="8" fill="#ffffff"/>';function qrCorner(pxx,pyy){return '<rect x="'+pxx+'" y="'+pyy+'" width="22" height="22" fill="none" stroke="#0b3d2e" stroke-width="3"/><rect x="'+(pxx+5)+'" y="'+(pyy+5)+'" width="12" height="12" fill="#0b3d2e"/>';}s+=qrCorner(qx+8,qy+8);s+=qrCorner(qx+qsz-30,qy+8);s+=qrCorner(qx+8,qy+qsz-30);for(var rr=0;rr<4;rr++){for(var cc=0;cc<4;cc++){if((rr+cc)%2===0){s+='<rect x="'+(qx+44+cc*12)+'" y="'+(qy+44+rr*12)+'" width="9" height="9" fill="#0b3d2e" opacity="0.5"/>';}}}s+='<text x="'+(W/2)+'" y="'+(qy+qsz+22)+'" text-anchor="middle" fill="#9fd9bf" font-size="12">微信扫一扫 查看完整赛事报告</text>';y=qy+qsz+40;s+='<text x="'+pad+'" y="'+y+'" fill="#7fbfa6" font-size="'+fsF+'">数据来源：公开赛事资料整理 · 仅合法赛事 · 理性观赛 · 不保证赛果</text>';y+=fsF+pad;var H=y;s=s.replace('height="4000"','height="'+H+'"');s+='</svg>';var img=new Image();var blob=new Blob([s],{type:'image/svg+xml;charset=utf-8'});var url=URL.createObjectURL(blob);img.onload=function(){var c=document.createElement('canvas');c.width=W;c.height=H;c.getContext('2d').drawImage(img,0,0);URL.revokeObjectURL(url);c.toBlob(function(b){if(!b){alert('图片生成失败，请直接截图分享');return;}var a=document.createElement('a');a.download='赛事分享长图.png';a.href=URL.createObjectURL(b);a.click();},'image/png');};img.onerror=function(){alert('图片生成失败（部分浏览器限制），请直接截图分享');};img.src=url;}
""" + "</script>"


REPORT_CSS = "<style>" + """
 body{font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;background:#eef1f5;color:#1a1a1a;margin:0;padding:0}
 .wrap{max-width:1040px;margin:0 auto;padding:0 16px 44px}
 .hero{background:linear-gradient(135deg,#0b3d2e 0%,#14532d 55%,#0f5132 100%);border-radius:0 0 20px 20px;padding:26px 28px 24px;color:#fff;box-shadow:0 8px 22px rgba(0,0,0,.20);position:relative;overflow:hidden}
 .hero:before{content:"";position:absolute;right:-70px;top:-70px;width:240px;height:240px;background:radial-gradient(circle,rgba(245,197,24,.20),transparent 70%);border-radius:50%}
 .htag{display:inline-block;background:rgba(245,197,24,.18);color:#F5C518;border:1px solid rgba(245,197,24,.5);border-radius:20px;padding:3px 13px;font-size:12.5px;font-weight:700;letter-spacing:.5px}
 .hteams{margin:14px 0 2px;font-size:15px}
 .hteams .team{color:#fff;font-size:17px;margin-right:18px}
 .htitle{font-size:27px;font-weight:800;margin:6px 0 4px;letter-spacing:.5px}
 .hmeta{color:#cfe9d8;font-size:13px}
 .banner{background:#fff7e6;border:1px solid #ffd591;border-radius:10px;padding:11px 15px;color:#874d00;font-size:13px;line-height:1.65;margin:16px 0}
 .banner.live-warn{background:#fff1f0;border:1px solid #ffa39e;color:#a8071a;font-weight:400}
 .card{background:#fff;border-radius:12px;box-shadow:0 1px 5px rgba(0,0,0,.08);padding:18px 22px;margin:0 0 16px}
 h2{font-size:17px;border-left:4px solid #E84E18;padding-left:10px;margin:0 0 10px;color:#16241c}
 .note{font-size:12.5px;color:#874d00;background:#fffbe6;border:1px solid #ffe58f;border-radius:8px;padding:8px 10px;margin-top:8px}
 table{width:100%;border-collapse:collapse;font-size:13.5px;margin-top:8px}
 th,td{padding:8px 10px;text-align:left;border-bottom:1px solid #eee}
 th{background:#0b3d2e;color:#fff;font-weight:600}
 tr.ok{background:#f3fbf5} tr.warn{background:#fff7f6} tr.muted{color:#999}
 tr.info{background:#e6f4ff}
 .ok{color:#2E8B57;font-weight:600} .warn{color:#E50012;font-weight:600} .muted{color:#999} .info{color:#1677ff}
 .team{display:inline-block;margin-right:14px;font-size:14px}
 .chip{display:inline-block;padding:2px 9px;border-radius:10px;border:1px solid #ccc;margin:2px;font-size:12.5px;font-weight:600}
 .forms{display:flex;flex-wrap:wrap;gap:16px} .formblk{min-width:200px}
 .flab{font-size:13px;color:#555;margin-bottom:4px}
 .intel{list-style:none;padding:0;margin:6px 0} .intel li{padding:6px 0;border-bottom:1px dashed #eee}
 .badge{display:inline-block;padding:1px 8px;border-radius:8px;font-size:12px;margin-right:6px}
 .badge.ok{background:#f3fbf5;color:#2E8B57} .badge.info{background:#e6f4ff;color:#1677ff} .badge.warn{background:#fff1f0;color:#E50012}
 .crest{display:inline-flex;flex-direction:column;align-items:center;vertical-align:middle;line-height:1;margin:2px 6px}
 .crest-emblem{width:50px;height:50px;object-fit:contain;filter:drop-shadow(0 2px 4px rgba(0,0,0,.28));border-radius:5px;background:transparent}
 .crest-ribbon{margin-top:3px;padding:2px 10px;color:#fff;font-size:11px;font-weight:700;border-radius:3px;white-space:nowrap;border:1px solid #ffd700;box-shadow:0 1px 2px rgba(0,0,0,.25);letter-spacing:.5px;text-shadow:0 1px 1px rgba(0,0,0,.25)}
 .court-wrap{margin:8px 0 4px;background:#0f2a1d;border-radius:10px;padding:10px;display:flex;justify-content:center;align-items:center}
 .court-wrap svg{max-width:360px;width:100%;height:auto}
 .kick{font-size:13px;color:#0b3d2e;background:#eafaf1;border:1px solid #b7e4c7;border-radius:8px;padding:6px 10px;margin:6px 0 2px;display:flex;gap:14px;flex-wrap:wrap;align-items:center}
 .kick .kl{color:#1f6b3f} .kick .kl b{color:#0b3d2e} .kick .kb{color:#9a5b00} .kick .kb b{color:#7a4500}
 .kick .ku{color:#15539e;background:#e8f1fd;border:1px solid #bcd5f5;border-radius:6px;padding:2px 7px}
 .experts{list-style:none;padding:0;margin:8px 0}
 .ex-fresh{font-size:12px;padding:6px 10px;border-radius:8px;margin-bottom:8px}
 .ex-fresh.ok{background:#f6ffed;border:1px solid #b7eb8f;color:#389e0d}
 .ex-fresh{background:#f0f5ff;border:1px solid #adc6ff;color:#1d39c4}
 .expert{background:#fff;border:1px solid #e3e8ee;border-left:4px solid #bbb;border-radius:10px;padding:12px 14px;margin:10px 0;box-shadow:0 1px 3px rgba(0,0,0,.04)}
 .expert.ok{border-left-color:#2E8B57;background:linear-gradient(180deg,#f4fcf7,#fff)}
 .expert.info{border-left-color:#1677ff;background:linear-gradient(180deg,#f1f7ff,#fff)}
 .expert.warn{border-left-color:#E50012;background:#fbfbfb;opacity:.93}
 .expert .ex-head{display:flex;align-items:center;gap:10px}
 .expert .ex-ava{width:34px;height:34px;border-radius:50%;background:#2E8B57;color:#fff;font-weight:700;font-size:16px;display:flex;align-items:center;justify-content:center;flex:0 0 auto}
 .expert.info .ex-ava{background:#1677ff} .expert.warn .ex-ava{background:#9aa0a6}
 .expert .ex-id{display:flex;flex-direction:column;line-height:1.2}
 .expert .ex-id b{font-size:15px;color:#1a1a1a} .expert .ex-src{font-size:12px;color:#888}
 .expert .ex-verify{margin-left:auto;font-size:12px;color:#2E8B57;background:#eafaf1;border:1px solid #b7e4c7;border-radius:20px;padding:2px 10px;font-weight:700;white-space:nowrap}
 .expert .ex-body{margin:8px 0;font-size:14px;line-height:1.6;color:#333}
 .expert .ex-foot{display:flex;align-items:center;gap:8px;font-size:12.5px;color:#666;flex-wrap:wrap}
 .expert .ex-caution{color:#E50012;font-weight:700;background:#fff1f0;border:1px solid #ffccc7;border-radius:6px;padding:1px 8px}
 .cmptab{width:100%;border-collapse:collapse;margin:4px 0 8px;background:#fbfdff;border:1px solid #dbe7f3;border-radius:10px;overflow:hidden}
 .cmptab th,.cmptab td{padding:8px 12px;text-align:left;font-size:13.5px;border-bottom:1px solid #eef3f8}
 .cmptab th{background:#eef5ff;color:#15539e;font-weight:700;width:96px;white-space:nowrap}
 .cmptab td{color:#1a1a1a;font-weight:600}
 .analysis{white-space:pre-wrap;line-height:1.7;font-size:14px;background:#fafafa;border-radius:8px;padding:14px}
 .foot{color:#888;font-size:12px;text-align:center;margin-top:16px}
 .fm{margin-top:10px}
 .fmlab{font-size:14px;margin-bottom:8px}
 .fmlab button{cursor:pointer;background:#1677ff;color:#fff;border:0;border-radius:6px;padding:4px 12px;font-size:13px}
 .fmlab button:hover{background:#0958d9}
 .psgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(182px,1fr));gap:16px;margin:6px 0}
 .pspot{background:radial-gradient(125% 85% at 50% 0%,#1a4a36,#0a2c20 72%);border:1px solid rgba(255,255,255,.16);border-radius:18px;padding:20px 12px 14px;text-align:center;color:#eafff3;position:relative;overflow:hidden;display:flex;flex-direction:column;align-items:center;box-shadow:0 10px 26px rgba(0,0,0,.34),inset 0 1px 0 rgba(255,255,255,.12);animation:cardin .55s ease-out both}
 .pspot::before{content:"";position:absolute;top:-25%;left:-60%;width:45%;height:150%;background:linear-gradient(105deg,transparent,rgba(255,255,255,.18),transparent);transform:skewX(-18deg);animation:sheen 5s ease-in-out infinite;pointer-events:none}
 .ptag{position:absolute;top:8px;left:8px;font-size:10px;font-weight:800;color:#3a2d00;background:linear-gradient(180deg,#FFE9A8,#C9962E);padding:2px 8px;border-radius:20px;box-shadow:0 1px 3px rgba(0,0,0,.3);white-space:nowrap}
 .pspot .ptag .pstars{font-size:11px;letter-spacing:1px;text-shadow:0 1px 1px rgba(255,255,255,.4)}
 .pspot .pfig{position:relative;width:62px;height:62px;margin:0;border-radius:50%;background:#fff;box-shadow:0 6px 16px rgba(0,0,0,.34);animation:floaty 3.6s ease-in-out infinite;flex:0 0 auto}
 .pspot .pfig svg{display:block;width:58px;height:58px;margin:2px auto 0;border-radius:50%;position:relative;z-index:3}
 .pspot .pav{display:block;width:52px;height:52px;margin:2px auto 0;border-radius:50%;object-fit:cover;border:2px solid #fff;box-shadow:0 0 0 3px rgba(255,255,255,.18);position:relative;z-index:3}
 .pspot .pring{position:absolute;left:50%;top:50%;width:62px;height:62px;transform:translate(-50%,-50%);border-radius:50%;background:conic-gradient(from 0deg,var(--pc),#ffffff,var(--pc),#ffffff,var(--pc));animation:spin 6s linear infinite;z-index:0;opacity:.9}
 .pspot .psonar{position:absolute;left:50%;top:50%;width:54px;height:54px;transform:translate(-50%,-50%) scale(.62);border-radius:50%;border:2px solid rgba(255,255,255,.85);animation:sonar 2.6s ease-out infinite;z-index:1}
 .pspot .pglow{position:absolute;left:50%;top:50%;width:46px;height:46px;transform:translate(-50%,-50%);border-radius:50%;background:radial-gradient(circle,var(--pc),transparent 70%);opacity:.5;animation:pglow 2.4s ease-in-out infinite;z-index:0}
 @keyframes sonar{0%{transform:translate(-50%,-50%) scale(.62);opacity:.85}100%{transform:translate(-50%,-50%) scale(1.32);opacity:0}}
 .pspot .pname{font-size:15px;font-weight:700;text-shadow:0 1px 2px rgba(0,0,0,.4);animation:namein .6s .25s ease-out both}
 .pspot .pteam{font-size:11px;color:#a7e3cb;margin-bottom:5px;opacity:.92}
 .pspot .pstatus{display:inline-block;font-size:12px;font-weight:700;margin-bottom:9px;padding:2px 11px;border-radius:20px;background:rgba(255,255,255,.10)}
 .pspot .pbar{display:flex;align-items:center;font-size:10.5px;color:#bfe9d6;margin:4px 4px}
 .pspot .pbar span{width:34px;text-align:left}
 .pspot .pbar i{display:block;height:7px;border-radius:4px;background:#2E8B57;animation:grow 1.2s ease-out;margin-left:6px;box-shadow:0 0 6px rgba(46,139,87,.5)}
 .pspot .phead{display:flex;align-items:center;gap:10px;width:100%;margin:2px 0 11px}
 .pspot .pach{flex:1;min-width:0;align-self:center;text-align:left;background:linear-gradient(180deg,rgba(255,233,168,.20),rgba(255,233,168,.07));border:1px solid rgba(255,233,168,.42);border-left:3px solid #FFE9A8;border-radius:11px;padding:6px 9px;box-shadow:0 2px 8px rgba(0,0,0,.18)}
 .pspot .pacht{display:block;font-size:9px;font-weight:800;color:#FFE9A8;letter-spacing:.5px;margin-bottom:2px;text-shadow:0 1px 1px rgba(0,0,0,.3)}
 .pspot .pachtxt{display:block;font-size:10.5px;line-height:1.4;color:#f4ffe9;font-weight:600}
 .pspot .prole{display:inline-block;font-size:11px;font-weight:700;color:#06281d;background:linear-gradient(180deg,#FFE9A8,#F5C518);padding:2px 11px;border-radius:20px;margin:-2px 0 8px;box-shadow:0 1px 3px rgba(0,0,0,.28)}
 .pspot .pform{display:flex;align-items:center;gap:5px;justify-content:center;font-size:10.5px;color:#bfe9d6;margin-top:5px}
 .pspot .pformlab{opacity:.82;margin-right:1px}
 .pspot .pspark{width:17px;height:17px;border-radius:5px;color:#fff;font-size:10px;font-weight:800;display:flex;align-items:center;justify-content:center;box-shadow:inset 0 -2px 3px rgba(0,0,0,.22)}
 @keyframes namein{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
 @keyframes grow{from{width:0}}
 .cfig{transform-box:fill-box;transform-origin:center;animation:cfade .5s ease-out both,cfloat 2.8s ease-in-out infinite;animation-delay:var(--d,0s),calc(var(--d,0s) + .45s)}
 @keyframes cfade{from{opacity:0}to{opacity:1}}
 @keyframes cfloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}
 .info-panel{box-shadow:0 4px 16px rgba(21,83,158,.12);border:1px solid #cfe0f5}
 .deep{margin:6px 0;padding-left:20px}.deep li{font-size:13.5px;line-height:1.7;margin:4px 0;color:#333}
 .oh-note{font-size:12.5px;color:#555;background:#f3f6f9;border-radius:8px;padding:9px 11px;margin-top:4px}
 .pnote{font-size:11.5px;color:#777;background:#f6f9fc;border-radius:8px;padding:7px 10px;margin-top:6px;line-height:1.55}
 .audit-badge{border:1px solid #b7e4c7}
 .audit-badge.pass{border-color:#b7e4c7;background:linear-gradient(180deg,#f3fbf5,#fff)}
 .audit-badge.warn{border-color:#ffccc7;background:linear-gradient(180deg,#fff7f6,#fff)}
 .ab-row{display:flex;flex-wrap:wrap;gap:8px;margin:2px 0 8px}
 .ab-pill{font-size:12px;font-weight:700;padding:3px 11px;border-radius:20px}
 .ab-pill.ok{background:#eafaf1;color:#2E8B57;border:1px solid #b7e4c7}
 .ab-pill.bad{background:#fff1f0;color:#E50012;border:1px solid #ffccc7}
 .ab-pill.warn{background:#fff7e6;color:#874d00;border:1px solid #ffe08a}
 .ab-list{margin:6px 0;padding-left:4px;list-style:none}
 .ab-list li{font-size:12.5px;color:#E50012;padding:2px 0}
 .ab-corr{font-size:12.5px;color:#0b6b2e;background:#eafaf1;border:1px solid #b7e4c7;border-radius:8px;padding:7px 10px;margin:6px 0}
 .antiscam{background:linear-gradient(135deg,#0b3d2e,#14532d);color:#eafff3;border:1px solid #2f7d5a;border-radius:14px;padding:16px 18px;margin:0 0 16px;box-shadow:0 6px 18px rgba(11,61,46,.2);position:relative;overflow:hidden}
 .antiscam:before{content:"";position:absolute;right:-50px;top:-50px;width:160px;height:160px;background:radial-gradient(circle,rgba(245,197,24,.16),transparent 70%);border-radius:50%}
 .antiscam h2{color:#F5C518;border-left-color:#F5C518}
 .antiscam .sc-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px;margin-top:8px}
 .antiscam .sc-item{background:rgba(255,255,255,.06);border:1px solid rgba(245,197,24,.30);border-radius:10px;padding:10px 12px}
 .antiscam .sc-item b{color:#F5C518;display:block;margin-bottom:3px;font-size:13.5px}
 .antiscam .sc-item span{font-size:12.5px;color:#cfe9d8;line-height:1.6}
 .sharecard{background:#fff;border:1px solid #cfe0f5;border-radius:14px;padding:18px;margin:0 0 16px;text-align:center}
 .sharecard h2{border-left-color:#1677ff}
 .sharecard .sc-frame{border:1px dashed #bcd5f5;border-radius:10px;padding:14px 16px;background:#fff;max-width:600px;margin:0 auto;text-align:left}
 .sharecard .sc-kicker{font-size:12px;color:#15539e;font-weight:800;letter-spacing:1px}
 .sharecard .sc-title{font-size:18px;font-weight:800;color:#0b3d2e;margin:4px 0 8px}
 .sharecard .sc-list{text-align:left;font-size:13px;color:#333;line-height:1.85;margin:6px 0}
 .sharecard .sc-list li{margin:2px 0}
 .sharecard .sc-foot{font-size:11.5px;color:#888;margin-top:8px}
 .sharecard .sc-btn{display:inline-block;margin:10px 6px 0;background:#1677ff;color:#fff;border:0;border-radius:22px;padding:7px 18px;font-size:13px;font-weight:700;cursor:pointer}
 .sharecard .sc-btn.alt{background:#0b3d2e}
 .sharecard .sc-btn.vbtn{background:#F5C518;color:#0b3d2e}
 .sharecard .sc-btn:hover{opacity:.9}
 .sharecard .sc-tip{font-size:11.5px;color:#888;margin-top:6px}
 .feedback{background:#fff;border:1px solid #e3e8ee;border-radius:14px;padding:16px 18px;margin:0 0 16px;text-align:center}
 .feedback h2{border-left-color:#2E8B57}
 .feedback .fb-btns{display:flex;gap:14px;justify-content:center;margin:10px 0}
 .feedback .fb-btn{cursor:pointer;border:1px solid #d9e1ea;background:#f6f9fc;border-radius:24px;padding:9px 22px;font-size:14px;font-weight:700;color:#333}
 .feedback .fb-btn.up:hover{border-color:#2E8B57;color:#2E8B57}
 .feedback .fb-btn.down:hover{border-color:#E50012;color:#E50012}
 .feedback .fb-msg{font-size:13px;color:#2E8B57;margin-top:6px;min-height:18px}
 .feedback .fb-export{margin-top:8px;font-size:12px;color:#1677ff;cursor:pointer;text-decoration:underline}
 .mtch{position:relative}
 .jumptabs{position:sticky;top:8px;z-index:40;display:flex;gap:8px;margin:10px 0;flex-wrap:wrap;background:rgba(255,255,255,.94);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);padding:7px 9px;border-radius:12px;box-shadow:0 4px 14px rgba(0,0,0,.10);border:1px solid #e3e8ee}
 .jumptabs .jt{cursor:pointer;border:1px solid #d9e1ea;background:#f6f9fc;color:#15539e;font-size:13px;font-weight:700;border-radius:20px;padding:5px 14px}
 .jumptabs .jt:hover{background:#0b3d2e;color:#fff;border-color:#0b3d2e}
 .flash{animation:flashsec 2s ease-out}
 @keyframes flashsec{0%{box-shadow:0 0 0 3px #F5C518}100%{box-shadow:0 1px 5px rgba(0,0,0,.08)}}
""" + "</style>"


DASH_CSS = "<style>" + """
 .dash{background:linear-gradient(135deg,#06281d,#0b3d2e);border-radius:14px;padding:16px 18px;margin:0 0 16px;color:#eafff3}
 .dash h2{color:#fff;border-left-color:#F5C518}
 .dashgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin-top:10px}
 .dcard{background:#0e3a2a;border:1px solid #1f5e44;border-radius:12px;padding:14px 15px;display:block;color:#eafff3;text-decoration:none;transition:.16s;position:relative;overflow:hidden}
 .dcard:hover{transform:translateY(-4px);box-shadow:0 12px 26px rgba(0,0,0,.35);border-color:#F5C518}
 .dcard.hot:before{content:"🔥 值得关注";position:absolute;top:11px;right:-32px;transform:rotate(38deg);background:#E50012;color:#fff;font-size:10px;font-weight:800;padding:3px 34px;box-shadow:0 2px 6px rgba(0,0,0,.3)}
 .dcard.hot{border-color:#E50012}
 .dcard .dtop{display:flex;align-items:center;gap:8px;font-size:12px;color:#9fd9c0;flex-wrap:wrap}
 .dcard .dteams{font-size:17px;font-weight:700;margin:7px 0 3px}
 .dcard .dteams .badge{vertical-align:middle;margin-right:4px}
 .dcard .dmeta{font-size:12px;color:#bfe9d6}
 .dcard .dtip{margin-top:8px;font-size:12.5px;background:rgba(245,197,24,.12);border:1px solid rgba(245,197,24,.4);border-radius:8px;padding:6px 8px;color:#F5C518;font-weight:700}
 .dcard .dbtn{display:inline-flex;align-items:center;gap:6px;margin-top:11px;font-size:12.5px;font-weight:800;color:#06281d;background:linear-gradient(135deg,#F5C518,#ffd34d);border-radius:22px;padding:5px 14px;box-shadow:0 3px 8px rgba(245,197,24,.4);transition:.15s}
 .dcard:hover .dbtn{transform:translateX(3px)}
 .dcard .dbtn:after{content:"→";font-weight:900;font-size:14px}
 .dcard:hover .dbtn:after{transform:translateX(4px)}
 .guide{background:linear-gradient(135deg,#e8f6ef,#d8f0e3);border:1px solid #b6e2cf;border-radius:10px;padding:13px 16px;color:#0b5132;font-size:13.5px;margin:0 0 16px;line-height:1.7}
 .guide b{color:#0b6b2e}
 .radar{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px;margin-top:8px}
 .radar .rc{background:#fff;border-radius:12px;padding:14px 16px;box-shadow:0 1px 5px rgba(0,0,0,.08)}
 .radar .rc h3{margin:0 0 8px;font-size:14px;color:#16241c}
 .radar .ritem{font-size:13px;padding:5px 0;border-bottom:1px dashed #eee}
 .radar .ritem a{color:#0b6b2e;font-weight:600;text-decoration:none}
 .match-detail{border-top:3px solid #E84E18;scroll-margin-top:12px;margin-top:8px}
 .match-detail .mh{display:flex;align-items:center;gap:10px;font-size:18px;font-weight:800;margin:4px 0 2px}
""" + "</style>"


def _ensure_crests(out_path):
    """将 skill assets/crests/*.png 复制到输出目录的 crests/（使报告自包含，队徽图不丢失）。"""
    import shutil as _sh
    _script_dir = os.path.dirname(os.path.abspath(__file__))
    _assets = os.path.join(_script_dir, "..", "assets", "crests")
    if not os.path.isdir(_assets):
        return
    _out = os.path.dirname(os.path.abspath(out_path))
    _tgt = os.path.join(_out, "crests")
    os.makedirs(_tgt, exist_ok=True)
    for _f in os.listdir(_assets):
        if _f.lower().endswith(".png"):
            _src = os.path.join(_assets, _f)
            _dst = os.path.join(_tgt, _f)
            if not os.path.exists(_dst):
                _sh.copy2(_src, _dst)


def build_report(data, output_html):
    (body, rows, combos_raw, team_txt, sport_label, league, country, cflag, teams, match, venuestr, tz_html) = _build_match_body(data)
    team_html = ""
    for t in teams:
        badge = club_badge_svg(t.get("name", ""))
        nm = _esc(t.get("name", "?"))
        note = _esc(t.get("status_note", ""))
        team_html += "<span class='team'>%s <b>%s</b> %s</span>" % (badge, nm, ("<i>%s</i>" % note if note else ""))
    if not team_html:
        team_html = "<b>%s</b>" % _esc(match)
    hero = ("<div class='hero'><span class='htag'>赛事%s · %s</span><div class='hteams'>%s</div>"
            "<div class='htitle'>%s</div><div class='hmeta'>%s　%s %s　|　%s</div>%s</div>") % (
        sport_label, _esc(league), team_html, _esc(match), _esc(league), cflag, _esc(country),
        _esc(venuestr), tz_html)
    banner = ("<div class='banner'>⚠️ 理性观赛声明：本报告仅基于公开数据做<b>信息整理与可视化</b>，"
              "<b>仅用于合法赛事的观赛研究与信息整理</b>。体育比赛存在大量不可建模的偶然因素（判罚、伤病、赛前最新状态等），"
              "任何分析都无法消除不确定性；本工具只提升你'看懂比赛'的信息质量。"
              "仅适用于合法的体育赛事；理性观赛分析、量力而行、未成年人禁止。未证实传闻仅作视野补充，不可作为依据。</div>")
    foot = "<div class='foot'>体育赛事数据可视化 Skill · 仅合法赛事 · 理性观赛 · 不承诺任何表现</div>"
    html = ("<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<title>体育赛事数据可视化报告</title>" + REPORT_CSS +
            "</head><body><div class='wrap'>" + hero + banner + anti_scam_html() + body + share_card_html([data], "single") + feedback_html() + foot + ENHANCE_JS + "</div></body></html>")
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html)
    _ensure_crests(output_html)
    md = _build_md(data, rows, combos_raw, team_txt, tz_html)
    return output_html, md


def _build_md(data, rows, combos_raw, team_txt, tz_html):
    match = data.get("match", "")
    league = data.get("league", data.get("competition", ""))
    country = data.get("country", "")
    formations = data.get("formations", [])
    weather = data.get("weather", {})
    players = data.get("players", [])
    form = data.get("form_last5", {})
    h2h = data.get("h2h_last5", [])
    intel = data.get("intel", [])
    experts = data.get("experts", [])
    analysis = data.get("analysis", "")
    confidence = data.get("confidence", "")
    risk = data.get("risk", "")
    md = ["# 体育赛事数据可视化报告 · %s" % match,
          "> 观赛辅助：本报告仅做信息整理与可视化，仅用于合法赛事的观赛研究与信息整理。仅限合法赛事。",
          "", "**赛事**：%s　%s　%s　%s" % (team_txt, league, COUNTRY_CODE.get(country, country), country),
          tz_html.replace("<div class='kick'>", "").replace("<span class='kl'>", "").replace("<span class='kb'>", "").replace("</span>", "").replace("</div>", "")]
    if formations:
        md += ["", "**阵型（主队）**：%s" % " → ".join(f for f in formations if f in FORMATION_POS)]
    if weather:
        md += ["", "## 天气", "温度 %s｜湿度 %s｜%s %s" % (weather.get("temp", "—"), weather.get("humidity", "—"), weather.get("condition", ""), weather.get("wind", "")),
               "影响：%s" % weather.get("impact", "")]
    if players:
        md += ["", "## 球员状态"] + ["- %s(%s)：%s %s" % (p.get("name", ""), p.get("team", ""), p.get("status", ""), p.get("note", "")) for p in players]
    if form or h2h:
        md += ["", "## 近期状态与交锋"]
        for t, seq in form.items():
            md.append("- %s 近5场：%s" % (t, " ".join(seq)))
        if h2h:
            md.append("- 交锋近5次：%s" % " ".join(h2h))
    if intel:
        md += ["", "## 赛前情报（分级）"] + ["- [%s] %s" % (i.get("tier", ""), i.get("text", "")) for i in intel]
    if experts:
        md += ["", "## 专家观点（权威/非权威）"] + ["- [%s·%s] %s：%s" % (e.get("tier", ""), e.get("source", ""), e.get("name", ""), e.get("view", "")) for e in experts]
    md += ["", "## 分析逻辑", analysis, "", "## 结论与风险", "**综合信心**：%s" % confidence, risk, "",
           "---", "_体育赛事数据可视化 Skill · 仅合法赛事 · 理性观赛_"]
    return "\n".join(md)


def build_daily_report(data, output_html, focus=False):
    matches = data.get("matches", [])
    if not matches:
        raise ValueError("daily 报告需要 matches 数组（每场即一份单场 match 数据）")
    date_label = data.get("date", datetime.now().strftime("%Y-%m-%d"))
    title = data.get("title", "今日体育赛事总览")
    n_live = sum(1 for m in matches if m.get("live"))
    n_demo = sum(1 for m in matches if not m.get("live"))
    feed = data.get("_feed", "realtime")  # realtime=真实时数据流; verified_sample=联网核实样例(非实时)
    # 标题诚实化：混合/全示例时不冒用“Live 实时”
    if n_live == 0:
        disp_title = "今日体育赛事总览（示例数据 · 非实时）"
    elif n_demo > 0:
        disp_title = "今日体育赛事总览（实时 %d 场 + 示例 %d 场）" % (n_live, n_demo)
    else:
        disp_title = title
    summary, focus_list = [], []
    for i, m in enumerate(matches):
        bid = "match-%d" % (i + 1)
        body, rows, combos_raw, team_txt, sport_label, league, country, cflag, teams, match, venuestr, tz_html = _build_match_body(m, str(i + 1))
        kp = m.get("key_players") or []
        is_key = m.get("key") is True
        if is_key or kp:
            fr = m.get("focus_reason")
            tip = ("⭐ 今日重点（%s）· 含球员聚焦" % fr) if fr else "⭐ 今日重点 · 含球员聚焦"
            focus_list.append((bid, team_txt, league, sport_label, "重点赛事 · 含明星球员聚焦动画"))
        else:
            tip = "常规场次 · 信息详见下方"
        summary.append((bid, team_txt, league, sport_label, country, cflag,
                        _esc(m.get("kickoff_local", "")), _esc(m.get("kickoff_actual", "")), tip, teams,
                        (feed == "realtime" and bool(m.get("live")))))
    # —— Task1 受欢迎/留存：首屏「今日最值得看」Hook（拉新+留存核心）——
    _scored = []
    for _i, _m in enumerate(matches):
        _bid = "match-%d" % (_i + 1)
        _sc = _match_focus_score(_m)
        _scored.append((_sc, _i, _bid, _m))
    _scored.sort(key=lambda x: (-x[0], x[1]))
    _top3 = [t for t in _scored if t[0] >= 14][:3] or _scored[:3]
    _hook_cards = ""
    for _rank, (_sc, _i, _bid, _m) in enumerate(_top3, 1):
        _ts = _m.get("teams") or []
        _tt = " vs ".join(t.get("name", "") for t in _ts) if _ts else (_m.get("match") or "")
        _lg = _m.get("league") or ""
        _sl = _m.get("sport_cn") or _m.get("sport") or ""
        _fr = _m.get("focus_reason")
        _kp = _m.get("key_players") or []
        if _fr:
            _why = _fr
        elif _kp:
            _why = "明星球员：%s" % "、".join(p.get("name", "") for p in _kp[:2] if p.get("name"))
        elif _lg in _MARQUEE_LEAGUES:
            _why = "顶级联赛焦点战"
        else:
            _why = "今日赛事"
        _hook_cards += (
            "<a class='hk' href='#%s'>"
            "<span class='hk-no'>%d</span>"
            "<div class='hk-b'>"
            "<div class='hk-l'>%s · %s</div>"
            "<div class='hk-t'>%s</div>"
            "<div class='hk-w'>%s</div>"
            "</div>"
            "<span class='hk-go'>查看 →</span>"
            "</a>") % (_bid, _rank, _esc(_sl), _esc(_lg), _esc(_tt), _esc(_why))
    hook_html = ("<div class='hook'>"
                 "<div class='hook-h'>🔥 今日最值得看 · Top %d</div>"
                 "%s"
                 "<div class='hook-chips'>🛡️ 只做信息整理 · 不做赛果判断　|　✅ 对阵已联网核实　|　📤 一键分享发群 / 朋友圈</div>"
                 "</div>") % (len(_top3), _hook_cards)
    # —— Task1 留存：底部「每日自动推送」订阅引导 ——
    sub_cta = ("<div class='card subcta'>"
               "<h2>📅 想要每天都自动收到这份总览？</h2>"
               "<div class='sc-item'>设置「每日体育赛事」自动化后，智能体会在每天固定时间<b>自动联网核实当日真实赛事</b>并生成这份总览，开赛前自动推送给你——信息全、来得及时，还不用自己动手。</div>"
               "<div class='pnote'>在 WorkBuddy 中说「每天给我发今日赛事总览」即可一键开启。</div>"
               "</div>")
    cards = ""
    for (bid, tt, lg, sl, ctry, cf, kl, ka, tip, tms, is_lv) in summary:
        if is_lv:
            lv_badge = "<span class='badge' style='background:#e6f7ff;color:#0958d9;border:1px solid #91caff'>🌐 实时</span>"
        elif m.get("live"):
            lv_badge = "<span class='badge' style='background:#f6ffed;color:#389e0d;border:1px solid #b7eb8f'>✅ 已核实</span>"
        else:
            lv_badge = "<span class='badge' style='background:#fafafa;color:#8c8c8c;border:1px solid #d9d9d9'>📋 示例</span>"
        badges = "".join("<span class='badge'>%s</span>" % club_badge_svg(t.get("name", "")) for t in tms[:2])
        cards += ("<a class='dcard' href='#%s'>"
                  "<div class='dtop'>%s · %s %s %s</div>"
                  "<div class='dteams'>%s %s</div>"
                  "<div class='dmeta'>🕒 当地 %s　|　北京 %s</div>"
                  "<div class='dtip'>%s</div>"
                  "<span class='dbtn'>查看完整分析</span></a>") % (
            bid, _esc(sl), _esc(lg), cf, lv_badge, badges, tt, (kl or "待定"), (ka or "待定"), tip)
    guide = ("<div class='guide'>🧭 <b>怎么用这份总览最省事？</b><br>"
             "① 先看上方<b>总汇总卡片</b>——每张都标了<b>本场看点提示</b>，带「🔥 值得关注」角标的就是今天最值得盯的场；<br>"
             "② 点任意卡片（或卡片底部<b>「查看完整分析 →」</b>）即<b>平滑跳转到该场详细单元</b>；<br>"
             "③ 详细单元里有<b>阵型动画、球员聚焦动画、赛前情报、专家观点、赛事信息要点</b>一应俱全。<br>"
             "👉 先扫总览挑感兴趣的场，再展开看细节，效率最高、也不容易错过差异信号。</div>")
    dash = ("<div class='card dash'><h2>📅 %s · %s（共 %d 场）</h2>"
            "<div class='dashgrid'>%s</div></div>") % (_esc(date_label), _esc(disp_title), len(summary), cards)
    radar_items = "".join(
        "<div class='ritem'>💎 <a href='#%s'>%s（%s · %s）</a>：%s</div>" % (b, tt, lg, sl, tip) for (b, tt, lg, sl, tip) in focus_list)
    if radar_items:
        radar_items += "<div class='muted' style='font-size:11.5px;color:#888;margin-top:4px'>重点赛事均含明星球员聚焦动画，仅供观赛讨论；任何判断须结合基本面与可靠信息。</div>"
    else:
        radar_items = "<div class='ritem'>今日各场暂无明显重点，建议观望或仅作观赛讨论。</div>"
    radar_html = ("<div class='card'><h2>🎯 今日重点速览</h2><div class='radar'>"
                  "<div class='rc'><h3>💎 今日重点赛事（含球员聚焦）</h3>%s</div>"
                  "<div class='rc'><h3>🧊 理性提醒</h3><div class='ritem'>体育比赛存在大量不可建模的偶然因素，任何分析都无法消除不确定性；"
                  "本总览只做信息整理，<b>不做结果判断、不做赛果判断</b>。挑感兴趣的场展开分析，量力而行。</div></div>"
                  "</div></div>") % radar_items
    details = ""
    for i, m in enumerate(matches):
        bid = "match-%d" % (i + 1)
        body, rows, combos_raw, team_txt, sport_label, league, country, cflag, teams, match, venuestr, tz_html = _build_match_body(m, str(i + 1))
        badge0 = club_badge_svg(teams[0].get("name", "")) if teams else ""
        if feed == "realtime" and m.get("live"):
            lv_badge = "<span class='badge' style='background:#e6f7ff;color:#0958d9;border:1px solid #91caff'>🌐 实时</span>"
        elif m.get("live"):
            lv_badge = "<span class='badge' style='background:#f6ffed;color:#389e0d;border:1px solid #b7eb8f'>✅ 已核实</span>"
        else:
            lv_badge = "<span class='badge' style='background:#fafafa;color:#8c8c8c;border:1px solid #d9d9d9'>📋 示例</span>"
        vtab = ("<div class='vtab'>"
                "<button class='vt on' onclick=\"swView(this,'info')\">📋 信息视角</button>"
                "<button class='vt' onclick=\"swView(this,'players')\">⭐ 球员视角</button></div>")
        mh = ("<div class='card match-detail' id='%s'><div class='mh'>%s <span class='badge'>%s</span> %s %s %s</div>"
              "<div class='hmeta'>%s　%s %s　|　%s</div>%s%s</div>") % (
            bid, badge0, _esc(sport_label), lv_badge, _esc(league), cflag, _esc(team_txt),
            _esc(league), _esc(country), _esc(venuestr), tz_html, vtab)
        details += "<section class='mtch'>" + mh + body + "</section>"
    banner = ("<div class='banner'>⚠️ 理性观赛声明：本报告仅基于公开数据做<b>信息整理与可视化</b>，"
              "<b>仅用于合法赛事的观赛研究与信息整理</b>。"
              "体育比赛存在大量不可建模的偶然因素（判罚、伤病、赛前最新状态等），任何分析都无法消除不确定性；本工具只提升你'看懂比赛'的信息质量。"
              "仅适用于合法的体育赛事；理性观赛分析、量力而行、未成年人禁止。未证实传闻仅作视野补充，不可作为依据。</div>")
    # 数据诚实横幅：按"实时/示例"实际占比显式提示，杜绝把陈旧 demo 藏在"Live 实时"标题下
    if data.get("_feed") == "verified_sample":
        live_banner = ("<div class='banner live-warn'>🟡 <b>联网核实赛程样例（非实时）</b>：本数据为智能体 WebSearch 从公开赛程源逐场联网核对而成（日期 %s），"
                       "<b>非实时数据流</b>；对阵真实有效，但深度情报（伤停 / 状态 / 交锋）需出报告时按需联网补充。"
                       "专家观点为精选静态库，非本期新采集。如需全自动每日实时赛事，可配置 TS_API_KEY（TheSportsDB Patreon）。</div>") % _esc(data.get("date", ""))
    elif n_live == 0 and n_demo > 0:
        why = data.get("_live_error") or "无网 / API 限流 / 当日无数据"
        live_banner = ("<div class='banner live-warn'>🔴 <b>示例数据 · 非实时</b>：本次联网获取当日真实赛事失败（%s），"
                       "下方对阵/比赛信息为<b>内置示例模板，并非每日最新</b>。如需真实当日赛事，请确认网络后重跑 live.py。"
                       "专家观点如未标注“已联网核实”亦为精选静态库，非本期新采集。</div>") % _esc(why)
    elif n_demo > 0:
        live_banner = ("<div class='banner live-warn'>🟡 <b>混合数据提示</b>：本报告含 <b>%d 场实时赛事</b>"
                       "（真实当日对阵，来源见各场「🌐 实时」标）+ <b>%d 场非实时示例数据</b>"
                       "（内置演示模板，<b>非今日真实赛程</b>，仅作信息结构/版式演示，含演示用专家观点）。"
                       "请据此区分阅读，勿将示例场当作今日赛程；如需更多球类实时数据，可配置 TS_API_KEY 解锁全量。</div>") % (n_live, n_demo)
    else:
        live_banner = ""
    htag = "赛事 · 今日重点赛事" if focus else "赛事 · 每日体育赛事"
    doc_suffix = "今日重点赛事聚焦" if focus else "每日体育赛事总览"
    agg_desc = "本日精选重点赛事（含明星球员聚焦动画）" if focus else "全运动聚合 · 足球/篮球/排球/网球/沙排/乒乓/羽毛球/冰球/手球/水球/曲棍球/橄榄球/棒球"
    focus_note = ("<div class='guide' style='border-color:#E84E18'>⭐ <b>本页是「重点赛事」精耕版</b>：已从今日全部赛事中为你筛选出 <b>%d 场重点 / 焦点赛事</b>（均含明星球员聚焦动画），"
                  "去掉了其余场次，方便专注深挖。想看今日<b>全部赛事</b>，说「今日全部赛事 / 全部赛事总览」即可。</div>") % len(summary) if focus else ""
    split_txt = ("　🌐 实时 %d · 📋 示例 %d" % (n_live, n_demo)) if n_demo else ""
    hero = ("<div class='hero'><span class='htag'>%s</span>"
            "<div class='htitle'>%s</div>"
            "<div class='hmeta'>%s　共 %d 场（%s）%s"
            "%s</div></div>") % (htag, _esc(disp_title), _esc(date_label), len(summary), agg_desc, split_txt,
                                ("　|　📡 数据更新 %s" % _esc(data.get("updated_at", ""))) if data.get("updated_at") else "")
    foot = "<div class='foot'>体育赛事数据可视化 Skill · 仅合法赛事 · 理性观赛 · 不承诺任何表现</div>"
    html = ("<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<title>%s · %s</title>" % (_esc(disp_title), doc_suffix) + REPORT_CSS + DASH_CSS +
            "<style>html{scroll-behavior:smooth}"
            ".vtab{display:flex;gap:8px;margin:10px 0 2px}"
            ".vt{border:1px solid #d9d9d9;background:#fafafa;color:#555;border-radius:18px;padding:5px 14px;font-size:13px;cursor:pointer;font-weight:700}"
            ".vt.on{background:#E84E18;color:#fff;border-color:#E84E18}"
            ".mv-players{display:none}"
            ".mtch.show-players .mv-info{display:none}"
            ".mtch.show-players .mv-players{display:block}"
            ".pp-note{margin:8px 0;padding:12px 14px;border:1px dashed #E84E18;border-radius:10px;background:rgba(232,78,24,.06);color:#7a3a12;font-size:13px;line-height:1.7}"
            ".hook{background:linear-gradient(135deg,#fff7e6,#fffbe6);border:1px solid #ffe08a;border-radius:14px;padding:14px 16px;margin:0 0 16px;box-shadow:0 4px 14px rgba(245,197,24,.18)}"
            ".hook-h{font-size:16px;font-weight:800;color:#ad6800;margin-bottom:10px;letter-spacing:.3px}"
            ".hk{display:flex;align-items:center;gap:12px;text-decoration:none;background:#fff;border:1px solid #ffe7a3;border-radius:12px;padding:11px 13px;margin:8px 0;transition:.15s}"
            ".hk:hover{box-shadow:0 4px 14px rgba(245,197,24,.28);transform:translateY(-1px)}"
            ".hk-no{flex:0 0 28px;height:28px;line-height:28px;text-align:center;background:#F5C518;color:#0b3d2e;border-radius:50%;font-weight:800;font-size:14px}"
            ".hk-b{flex:1;min-width:0}"
            ".hk-l{font-size:11.5px;color:#a06a00;font-weight:700;letter-spacing:.3px}"
            ".hk-t{font-size:15px;font-weight:800;color:#1f1f1f;margin:1px 0}"
            ".hk-w{font-size:12.5px;color:#7a5a16;line-height:1.5}"
            ".hk-go{flex:0 0 auto;color:#ad6800;font-weight:700;font-size:12.5px;white-space:nowrap}"
            ".hook-chips{margin-top:10px;font-size:12px;color:#8a6a1a;background:rgba(245,197,24,.12);border-radius:8px;padding:7px 10px;line-height:1.6}"
            ".subcta{background:linear-gradient(135deg,#0b3d2e,#14532d);color:#eafff3;border:1px solid #2f7d5a;border-radius:14px;padding:16px 18px;margin:0 0 16px;box-shadow:0 6px 18px rgba(11,61,46,.2)}"
            ".subcta h2{color:#F5C518;border-left:4px solid #F5C518;padding-left:10px;margin:0 0 8px;font-size:16px}"
            ".subcta .sc-item{background:rgba(255,255,255,.06);border:1px solid rgba(245,197,24,.30);border-radius:10px;padding:10px 12px;font-size:13px;color:#cfe9d8;line-height:1.75}"
            ".subcta .pnote{margin-top:8px;font-size:12px;color:#cfe9d8;background:rgba(255,255,255,.06);border:1px solid rgba(245,197,24,.30);border-radius:8px;padding:7px 10px}"
            "</style></head><body><div class='wrap'>"
            + hero + hook_html + live_banner + banner + anti_scam_html() + guide + focus_note + dash + radar_html + details + share_card_html(matches, "daily") + sub_cta + feedback_html() + foot + ENHANCE_JS + "</div></body></html>")
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html)
    _ensure_crests(output_html)
    return output_html


def _now_cst():
    """返回 Asia/Shanghai (UTC+8) 当前时间字符串，供 updated_at 时间戳使用。"""
    try:
        return (datetime.now(timezone.utc) + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return datetime.now().strftime("%Y-%m-%d %H:%M")


def _deep_merge(base, patch):
    """递归合并 patch 到 base（dict/list），返回新的合并结果（不原地改 base）。"""
    if isinstance(patch, dict) and isinstance(base, dict):
        out = dict(base)
        for k, v in patch.items():
            if k in out and isinstance(out[k], dict) and isinstance(v, dict):
                out[k] = _deep_merge(out[k], v)
            else:
                out[k] = _deep_merge(out[k], v) if (k in out and isinstance(out[k], dict) and isinstance(v, dict)) else v
        return out
    if isinstance(patch, list) and isinstance(base, list):
        return patch if patch else base
    return patch


def fetch_the_sports_db(team, league="", apikey=None):
    """
    合规适配 TheSportsDB（公开体育数据库，免费层可用）。
    - API Key 从环境变量 THESPORTSDB_API_KEY 读取；缺省用官方公开测试 key("3")。
    - 仅抓取球队公开元数据（队徽 URL、联赛、主场）与近期 5 场公开赛果；不抓取任何付费/版权受限内容。
    - 失败时回退 None，由调用方转 WebSearch 清单。
    返回 dict：{team, badge_url, league, stadium, last5:["胜"/"平"/"负",...], note} 或 None
    """
    key = apikey or os.environ.get("THESPORTSDB_API_KEY") or "3"
    base = "https://www.thesportsdb.com/api/v1/json/%s" % key
    try:
        q = urllib.parse.quote(team)
        req = urllib.request.Request(base + "/searchteams.php?t=" + q,
                                     headers={"User-Agent": "Mozilla/5.0 (compat; sports-data-analysis)"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            tdata = json.loads(resp.read().decode("utf-8"))
        teams = (tdata.get("teams") or []) if isinstance(tdata, dict) else []
        if not teams:
            return None
        t0 = teams[0]
        id_team = t0.get("idTeam")
        out = {
            "team": t0.get("strTeam", team),
            "badge_url": t0.get("strTeamBadge", ""),
            "league": t0.get("strLeague", league),
            "stadium": t0.get("strStadium", ""),
            "last5": [],
            "note": "数据来源 TheSportsDB（公开库），仅作参考；请按 tier 分级，未证实信息不可作依据。",
        }
        if id_team:
            req2 = urllib.request.Request(base + "/eventslast.php?id=" + str(id_team),
                                         headers={"User-Agent": "Mozilla/5.0 (compat; sports-data-analysis)"})
            with urllib.request.urlopen(req2, timeout=15) as resp2:
                edata = json.loads(resp2.read().decode("utf-8"))
            evs = (edata.get("results") or []) if isinstance(edata, dict) else []
            for e in evs[:5]:
                hs = e.get("intHomeScore"); as_ = e.get("intAwayScore")
                if hs is None or as_ is None:
                    out["last5"].append("—")
                    continue
                hid = str(e.get("idHomeTeam"))
                win = (hid == str(id_team) and hs > as_) or (hid != str(id_team) and as_ > hs)
                draw = hs == as_
                out["last5"].append("胜" if win else ("平" if draw else "负"))
        return out
    except Exception:
        return None


def _cmd_fetch(a):
    print("⚠️ 合规提醒：仅可从【官方/已授权/公开】数据源抓取；禁止抓取版权内容、付费墙数据或绕过反爬；"
          "API Key 必须存于环境变量（如 THESPORTSDB_API_KEY），不得硬编码；遵守目标站 ToS 与限流。"
          "所有抓取结果须按 tier 分级，未证实信息不可作依据。")
    if a.url:
        try:
            req = urllib.request.Request(
                a.url,
                headers={"User-Agent": "Mozilla/5.0 (compat; sports-data-analysis)",
                         "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            keys = list(data.keys())[:20] if isinstance(data, dict) else []
            print("✅ 已抓取：%s" % a.url)
            print("   返回顶层结构：%s" % (keys if keys else type(data).__name__))
            print("   下一步：将 JSON 中的 近期战绩/阵容/伤停 映射到 match.json 对应字段（form_last5/players）。")
        except Exception as e:
            print("❌ 抓取失败：%s" % e)
            print("   可能原因：无网络 / URL 不可达 / 需鉴权。请改用下方 WebSearch 清单，或配置带 Key 的合规 API（Key 放环境变量）。")
    elif a.source == "thesportsdb":
        targets = [a.team] if a.team else (a.teams or [])
        if not targets:
            print("❌ 使用 thesportsdb 需提供 --team 或 --teams（如 --team \"Manchester City\"）。")
        else:
            for tm in targets:
                info = fetch_the_sports_db(tm, a.league)
                if not info:
                    print("⚠️ %s：TheSportsDB 未取到（可能无网络/队名不匹配/限流）。回退 WebSearch 清单。" % tm)
                    continue
                print("✅ %s（TheSportsDB）" % info["team"])
                print("   联赛：%s　主场：%s" % (info["league"], info["stadium"]))
                if info["badge_url"]:
                    print("   队徽URL：%s（公开资源，可本非法载；注意版权，仅个人分析用）" % info["badge_url"])
                print("   近5场：%s" % (" ".join(info["last5"]) if info["last5"] else "无"))
                print("   → 可填入 match.json：form_last5 / teams[].name；队徽可经 club_badge_svg 自动生成 SVG（推荐，免版权风险）。")
        print("\n注：适配器仅取公开元数据与赛果，不触碰付费/版权内容。如需更多字段，配置 THESPORTSDB_API_KEY 提升额度。")
    else:
        print("未提供 --url，回退到 WebSearch 检索清单（由调用模型逐项采集）：")
        for i, (dim, q, use) in enumerate(
                gather_queries(a.match, a.league, a.city, a.country, a.teams, a.kickoff_local, a.kickoff_tz), 1):
            print("%d. [%s] %s" % (i, dim, q))
    print("\n推荐合规数据源（详见 references/data_sources.md）：官方赛事数据网 / 公开天气API(比赛日天气) / "
          "联赛官网·球队官网(阵容伤停) / 公开统计站(近期战绩) / TheSportsDB(球队元数据与赛果)。")


def _cmd_gather(a):
    items = gather_queries(a.match, a.league, a.city, a.country, a.teams, a.kickoff_local, a.kickoff_tz)
    print("【全网情报采集清单】%s" % a.match)
    for i, (dim, q, use) in enumerate(items, 1):
        print("%d. [%s] 检索词：%s\n   用途：%s" % (i, dim, q, use))
    if a.kickoff_local:
        print("\n⏰ 已记录开赛当地时间：%s（%s）。" % (a.kickoff_local, a.kickoff_tz or "当地时区"))
        print("   请在报告 match.json 中一并填写 kickoff_actual（北京时间）；涉及时差时务必当地/北京双显，避免误判观赛窗口。")
    print("\n用法：逐项用 WebSearch/WebFetch 采集，未证实信息标 tier='未证实传闻'，不可作依据。")


def _cmd_report(a):
    with open(a.input, "r", encoding="utf-8") as f:
        data = json.load(f)
    html_path, md = build_report(data, a.output)
    print("HTML 报告已生成: %s" % html_path)
    print("REPORT_PATH:%s" % html_path)
    print("--- Markdown 摘要 ---")
    print(md)


def _cmd_daily(a):
    a.input = _resolve_daily_input(a.input)
    with open(a.input, "r", encoding="utf-8") as f:
        data = json.load(f)
    html_path = build_daily_report(data, a.output)
    n = len(data.get("matches", []))
    print("每日体育赛事总览（共 %d 场）已生成: %s" % (n, html_path))
    print("REPORT_PATH:%s" % html_path)


# —— 重点赛事策展配置（仅基于公开联赛层级 / 明星球员 / 知名球队，不构成任何赛果或方向性判断）——
_MARQUEE_LEAGUES = {
    "中超", "西甲", "英超", "意甲", "德甲", "法甲", "NBA", "欧冠", "欧联杯",
    "沙特联", "葡超", "荷甲", "日职联", "韩K联", "美职女篮",
}
_NOTABLE_TEAMS = {
    "巴塞罗那", "皇家马德里", "曼联", "利物浦", "曼城", "切尔西", "阿森纳", "热刺",
    "尤文图斯", "国际米兰", "AC米兰", "拜仁慕尼黑", "多特蒙德", "巴黎圣日耳曼",
    "北京国安", "上海申花", "山东泰山", "上海海港", "利雅胜利", "吉达联合",
    "纽约自由", "拉斯维加斯王牌", "明尼苏达天猫", "皇家贝蒂斯", "弗鲁米嫩", "帕梅拉斯",
}


def _match_focus_score(m):
    """重点评分：顶级联赛 +10，含明星球员 +12，含知名球队 +14；其余为 0（不入重点）。"""
    lg = m.get("league") or m.get("strLeague") or ""
    s = 10 if lg in _MARQUEE_LEAGUES else 0
    if m.get("key_players"):
        s = max(s, 12)
    for t in (m.get("teams") or []):
        if (t.get("name") or "") in _NOTABLE_TEAMS:
            s = max(s, 14)
            break
    return s


def _curate_focus(all_matches):
    """从全部赛事中精选「重点赛事」严格子集（按开赛时间保序、去重）。"""
    picked = [m for m in all_matches if _match_focus_score(m) >= 14 or m.get("key_players")]
    seen, out = set(), []
    for m in sorted(picked, key=lambda x: x.get("kickoff_local", "")):
        k = m.get("match")
        if k not in seen:
            seen.add(k)
            out.append(m)
    return out


def _cmd_focus(a):
    a.input = _resolve_daily_input(a.input)
    with open(a.input, "r", encoding="utf-8") as f:
        data = json.load(f)
    all_matches = data.get("matches", [])
    picked = _curate_focus(all_matches)
    if not picked:  # 兜底：绝不出空报告
        picked = all_matches
    # 给每场标注重点理由（仅用于展示，不改写底层数据）
    for m in picked:
        lg = m.get("league") or m.get("strLeague") or ""
        reasons = []
        if lg in _MARQUEE_LEAGUES:
            reasons.append("顶级联赛")
        if m.get("key_players"):
            reasons.append("含明星球员")
        for t in (m.get("teams") or []):
            if (t.get("name") or "") in _NOTABLE_TEAMS:
                reasons.append("知名球队")
                break
        m["focus_reason"] = "、".join(reasons) or "焦点赛事"
        m["key"] = True  # 重点版内每场均按重点渲染（聚焦动画/雷达/速览）
    focus_data = {
        "title": "%s（重点赛事）" % data.get("title", "今日重点赛事"),
        "date": data.get("date", datetime.now().strftime("%Y-%m-%d")),
        "updated_at": data.get("updated_at", ""),
        "_feed": data.get("_feed", "verified_sample"),
        "_is_live": data.get("_is_live", False),
        "_source": data.get("_source", ""),
        "matches": picked,
    }
    html_path = build_daily_report(focus_data, a.output, focus=True)
    print("今日重点赛事报告（共 %d 场，已从 %d 场全部赛事中精选）已生成: %s"
          % (len(picked), len(all_matches), html_path))
    print("REPORT_PATH:%s" % html_path)


def _cmd_refresh(a):
    """
    每日随时更新：刷新比赛信息 / 影响因素，重生成报告。
    流程：
      1) 载入数据，写入 updated_at（Asia/Shanghai 当前时间）；
      2) 若给 --patch，递归合并增量更新（比赛信息、天气、伤停、战意等）；
      3) 可选 --fetch：拉取各队近期公开赛果（form_last5）作为影响因素补充；
      4) 重生成日报 HTML；默认回写 JSON（保留更新时间），可用 --no-write 关闭。
    """
    with open(a.input, "r", encoding="utf-8") as f:
        data = json.load(f)
    now_s = _now_cst()
    data["updated_at"] = now_s

    if a.patch:
        try:
            patch = json.load(open(a.patch, "r", encoding="utf-8"))
            data = _deep_merge(data, patch)
            print("✅ 已合并增量更新补丁：%s" % a.patch)
        except Exception as e:
            print("❌ 补丁合并失败：%s" % e)
            return

    if a.fetch:
        print("⚠️ 合规提醒：仅抓公开/已授权数据源；Key 走环境变量，勿硬编码。")
        for m in data.get("matches", []):
            for t in m.get("teams", []):
                info = fetch_the_sports_db(t.get("name", ""), m.get("league", ""))
                if info and info.get("last5"):
                    m.setdefault("form_last5", {})[t.get("name", "")] = info["last5"]
                    print("  · 已补充 %s 近5场：%s" % (t.get("name", ""), " ".join(info["last5"])))

    out = a.output or (os.path.splitext(a.input)[0] + "_refreshed.html")
    html_path = build_daily_report(data, out)
    if not a.no_write:
        with open(a.input, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("✅ 已回写更新数据：%s" % a.input)
    print("✅ 已刷新报告（数据更新时间 %s）：%s" % (now_s, html_path))
    print("REPORT_PATH:%s" % html_path)


def main():
    p = argparse.ArgumentParser(description="体育赛事数据可视化与观赛辅助工具（仅合法赛事·理性观赛分析）")
    sub = p.add_subparsers(dest="cmd")

    pg = sub.add_parser("gather", help="生成全网情报采集清单")
    pg.add_argument("--match", required=True); pg.add_argument("--league", default=""); pg.add_argument("--city", default="")
    pg.add_argument("--country", default=""); pg.add_argument("--teams", nargs="*", default=None)
    pg.add_argument("--kickoff_local", default="", help="开赛当地时间(如 2026-08-10 20:00)")
    pg.add_argument("--kickoff_tz", default="", help="当地时区(如 Europe/London)")
    pg.set_defaults(func=_cmd_gather)

    pf = sub.add_parser("fetch", help="合规联网抓取球队近期数据（需配置授权数据源）")
    pf.add_argument("--match", default=""); pf.add_argument("--league", default=""); pf.add_argument("--city", default="")
    pf.add_argument("--country", default=""); pf.add_argument("--teams", nargs="*", default=None)
    pf.add_argument("--kickoff_local", default=""); pf.add_argument("--kickoff_tz", default="")
    pf.add_argument("--source", default="thesportsdb", help="抓取源：thesportsdb(默认，公开库) / 留空+--url 走通用")
    pf.add_argument("--team", default="", help="单个球队名（thesportsdb 模式下用于拉取元数据与近5场）")
    pf.add_argument("--url", default="", help="可选：已授权的 JSON 数据源 URL（鉴权 Key 走环境变量，勿硬编码）")
    pf.set_defaults(func=_cmd_fetch)

    pr = sub.add_parser("report", help="生成完整分析报告（零输入即出内置示例）")
    pr.add_argument("--input", default=DEMO_REPORT, help="单场 match JSON；缺省使用内置示例")
    pr.add_argument("--output", default=DESK_REPORT, help="输出 HTML 路径；缺省为桌面")
    pr.set_defaults(func=_cmd_report)

    pd = sub.add_parser("daily", help="生成今日所有体育赛事聚合总览（足球+篮球+其它球类一份报告，含顶部汇总与点击跳转）")
    pd.add_argument("--input", default=DEMO_DAILY, help="含 matches[] 数组的 JSON；缺省使用内置示例")
    pd.add_argument("--output", default=DESK_DAILY, help="输出 HTML 路径；缺省为桌面")
    pd.set_defaults(func=_cmd_daily)

    pk = sub.add_parser("focus", help="生成今日重点赛事报告（从全部赛事筛选 key=true 的重点/焦点赛事，含球员聚焦动画）")
    pk.add_argument("--input", default=DEMO_DAILY, help="含 matches[] 数组的 JSON；缺省使用内置示例")
    pk.add_argument("--output", default=DESK_FOCUS, help="输出 HTML 路径；缺省为桌面")
    pk.set_defaults(func=_cmd_focus)

    prf = sub.add_parser("refresh", help="每日随时更新：刷新比赛信息/影响因素（写 updated_at、合并 --patch、重生成报告）")
    prf.add_argument("--input", required=True, help="含 matches[] 的 JSON 数据文件")
    prf.add_argument("--output", default=None, help="输出 HTML（默认：输入同名 _refreshed.html）")
    prf.add_argument("--patch", default="", help="可选增量补丁 JSON（递归合并：比赛信息/天气/伤停/战意…）")
    prf.add_argument("--fetch", action="store_true", default=False, help="同时合规抓取各队近5场公开赛果作为影响因素")
    prf.add_argument("--no-write", action="store_true", default=False, help="不回写输入 JSON")
    prf.set_defaults(func=_cmd_refresh)

    args = p.parse_args()
    if not getattr(args, "func", None):
        p.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    main()
