"""
tg_bot_handler.py — 一念紫微斗数 Telegram Bot 消息处理器 v2
支持命令：/zwds /read /reading /yearly /monthly /star /help /about

Author: 崽儿虾 🦞
"""

import sys
import os
import re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from zwds_calc import generate_astrolabe, format_astrolabe, astrolabe_to_json
from formats import format_chart_for_telegram, build_tg_menu, get_star_info, STAR_ENCYCLOPEDIA

from ai_engine import (
    full_reading_with_yearly,
    generate_yearly_reading,
    generate_monthly_reading,
)
from ai_reader import create_chart_and_reading, read_astrolabe
from name_analysis import analyze_name, format_name_analysis_for_tg


def parse_birth_input(text: str) -> dict:
    """
    解析用户输入的生辰信息
    
    支持格式:
    /zwds 2000-8-16 6 男
    /zwds 2000-8-16 6 男 综合
    /zwds 2000-8-16 6 男 --deep
    /reading 2000-8-16 6 男
    /yearly 1984-6-22 6 男 2026
    /monthly 1984-6-22 6 男 2026 4
    2000-8-16 6 男
    """
    text = text.strip()
    is_lunar = False
    is_deep = False
    deep_flag = False
    
    # 去掉命令前缀
    for prefix in ["/reading", "/yearly", "/monthly", "/zwds_lunar", "/zwdslunar", "zwds_lunar", "/zwds", "/read"]:
        if text.lower().startswith(prefix.lower()):
            text = text[len(prefix):].strip()
            if "lunar" in prefix:
                is_lunar = True
            break
    
    # 检查 --deep 标志
    if " --deep" in text or " -d" in text:
        is_deep = True
        text = re.sub(r" --deep|-d", "", text)
    
    if not text:
        return {"success": False, "error": "请输入出生信息。格式：年月日 时辰 性别\n例如：2000-8-16 6 男"}
    
    parts = text.split()
    
    # 提取日期
    date_re = re.search(r"(\d{4}[-/]\d{1,2}[-/]\d{1,2})", text)
    if not date_re:
        return {"success": False, "error": "日期格式错误。请使用 YYYY-MM-DD 格式，例如：2000-8-16"}
    
    date_str = date_re.group(1).replace("/", "-")
    
    # 提取时辰
    hour = 12  # 默认午时
    hour_re = re.search(r"(\d{1,2})", text[text.find(date_str) + len(date_str):])
    if hour_re:
        hour = int(hour_re.group(1))
        if hour < 0 or hour > 23:
            return {"success": False, "error": "时辰必须在 0-23 之间"}
    
    # 提取性别
    gender = "男"  # 默认
    if "女" in text or "female" in text.lower() or "f" in text.lower():
        gender = "女"
    
    # 提取流派和deep标记
    school = "综合"
    for s in ["三合", "飞星", "占验", "综合"]:
        if s in text.replace("--deep", "").replace("-d", ""):
            school = s
            break
    
    # 提取姓名（针对 /name 命令或 name= 参数）
    name_str = ""
    name_match = re.search(r'name=([\u4e00-\u9fff]+)', text)
    if name_match:
        name_str = name_match.group(1)
    
    return {
        "success": True,
        "date": date_str,
        "hour": hour,
        "gender": gender,
        "is_lunar": is_lunar,
        "school": school,
        "deep": is_deep,
    }


def handle_zwds_command(text: str) -> str:
    """处理 /zwds 命令：排盘 + 可选AI解盘"""
    parsed = parse_birth_input(text)
    if not parsed["success"]:
        return f"❌ {parsed['error']}\n\n试试 /help 查看使用说明"
    
    # 如果带 --deep 标志，走AI解盘
    if parsed.get("deep"):
        from ai_engine import full_reading_with_yearly
        result = full_reading_with_yearly(
            parsed["date"], parsed["hour"], parsed["gender"], parsed["is_lunar"]
        )
        if result.get("success"):
            return result.get("telegram_text", "")
        return f"❌ 解盘失败: {result.get('error', '未知错误')}"
    
    # 普通排盘
    try:
        result = create_chart_and_reading(
            date_str=parsed["date"],
            hour=parsed["hour"],
            gender=parsed["gender"],
            is_lunar=parsed["is_lunar"],
            school=parsed["school"],
        )
        if not result["success"]:
            return f"❌ 排盘失败：{result['error']}"
        
        chart_tg = format_chart_for_telegram(result["chart_json"])
        
        school_label = {
            "三合": "三合派",
            "飞星": "飞星派",
            "占验": "占验派",
            "综合": "三派合一",
        }.get(parsed["school"], "综合")
        
        output = (
            f"🔮 *一念紫微斗数 · {school_label}*\n"
            f"📅 {parsed['date']} 时{parsed['hour']} {parsed['gender']}\n"
            f"{'（农历' if parsed['is_lunar'] else ''}"
        )
        
        max_chars = 3800
        full_text = f"{chart_tg}\n\n💡 *提示*：/reading 获取AI深度解盘（含流年流月）"
        
        if len(full_text) > max_chars:
            full_text = full_text[:max_chars] + "\n\n⋯ （命盘超出显示限制）"
        
        return full_text
    except Exception as e:
        return f"❌ 处理异常：{str(e)}"


def handle_reading_command(text: str) -> str:
    """处理 /reading 命令：AI完整四层解盘 + 流年流月"""
    parsed = parse_birth_input(text)
    if not parsed["success"]:
        return f"❌ {parsed['error']}"
    
    result = full_reading_with_yearly(
        parsed["date"], parsed["hour"], parsed["gender"], parsed["is_lunar"]
    )
    if result.get("success"):
        return result.get("telegram_text", "")
    return f"❌ 解盘失败: {result.get('error', '未知错误')}"


def handle_yearly_command(text: str) -> str:
    """处理 /yearly 命令：流年运势"""
    parsed = parse_birth_input(text)
    if not parsed["success"]:
        return f"❌ {parsed['error']}"
    
    from datetime import datetime
    target_year = datetime.now().year
    
    # 提取用户指定的年份
    for part in text.split():
        if part.isdigit() and len(part) == 4 and 1900 < int(part) < 2100:
            target_year = int(part)
            break
    
    result = generate_yearly_reading(
        parsed["date"], parsed["hour"], parsed["gender"], target_year
    )
    if result.get("success"):
        lines = []
        lines.append(f"📅 *{target_year}年流年运势*")
        lines.append(f"📍 宫位：{result['palace']}（地支{result['year_branch']}）")
        lines.append(f"📍 大限叠宫：{result['overlay']}")
        lines.append("")
        lines.append(result.get("analysis", ""))
        lines.append("")
        lines.append("📜 文化参考，理性看待")
        return "\n".join(lines)
    return f"❌ 流年分析失败: {result.get('error')}"


def handle_monthly_command(text: str) -> str:
    """处理 /monthly 命令：流月运势"""
    parsed = parse_birth_input(text)
    if not parsed["success"]:
        return f"❌ {parsed['error']}"
    
    from datetime import datetime
    now = datetime.now()
    target_year = now.year
    target_month = now.month
    
    parts = text.split()
    for i, p in enumerate(parts):
        if p.isdigit() and len(p) == 4 and 1900 < int(p) < 2100:
            target_year = int(p)
            if i + 1 < len(parts) and parts[i+1].isdigit() and 1 <= int(parts[i+1]) <= 12:
                target_month = int(parts[i+1])
    
    result = generate_monthly_reading(
        parsed["date"], parsed["hour"], parsed["gender"], target_year, target_month
    )
    if result.get("success"):
        lines = []
        lines.append(f"🌙 *{target_year}年{target_month}月流月运势*")
        lines.append(f"📍 宫位：{result['palace_name']}（地支{result['month_branch']}）")
        lines.append(f"⭐ 星曜：{result['major_stars']}")
        lines.append("")
        lines.append(result.get("analysis", ""))
        lines.append("")
        lines.append("📜 文化参考，理性看待")
        return "\n".join(lines)
    return f"❌ 流月分析失败: {result.get('error')}"


def handle_read_command(chart_json: dict) -> str:
    """处理 /read 命令：用AI解盘（旧版，保留兼容）"""
    if not chart_json or not chart_json.get("palaces"):
        return "❌ 请先排盘（/zwds），再使用 /read 解盘"
    
    prompt = read_astrolabe(chart_json)
    return prompt


def handle_star_command(star_name: str) -> str:
    """处理 /star 命令：查询星曜"""
    if not star_name:
        stars = "、".join(list(STAR_ENCYCLOPEDIA.keys())[:7])
        stars += "\n" + "、".join(list(STAR_ENCYCLOPEDIA.keys())[7:])
        return f"⭐ *星曜百科*\n\n可查询：\n{stars}\n\n使用 /star 星名 查看详情"
    
    info = get_star_info(star_name)
    if info:
        return info
    return f"❌ 未找到星曜「{star_name}」"


def handle_help() -> str:
    """返回帮助文本"""
    return build_tg_menu()


def handle_reading_english(text: str) -> str:
    """处理 /read_en 命令：英文AI解盘"""
    from multilang_prompts import generate_multilang_reading
    
    parsed = parse_birth_input(text)
    if not parsed["success"]:
        return f"❌ {parsed['error']}"
    
    result = generate_multilang_reading(
        parsed["date"], parsed["hour"], parsed["gender"], "en-US"
    )
    
    if result["success"]:
        lines = [
            "🔮 *Yinian ZWDS · English Reading*\n",
            f"📅 Four Pillars: {result['chart_json'].get('four_pillars', {}).get('year','')}\n",
        ]
        lines.append("\n📜 For cultural reference only")
        return "\n".join(lines) + "\n\n(Send this prompt to your AI to get the full English interpretation)"
    return f"❌ {result.get('error')}"


def handle_matching_command(text: str) -> str:
    """处理 /match 命令：合盘匹配"""
    from matching import compute_match, format_match_for_tg
    import re
    
    # 格式：/match 2000-8-16 6 男 / 1995-3-20 8 女
    # 查找两个日期模式
    dates = re.findall(r'(\d{4}[-/]\d{1,2}[-/]\d{1,2}\s+\d{1,2}\s+[男女])', text)
    
    if len(dates) < 2:
        return "❌ 合盘需要两人信息。格式：/match 2000-8-16 6 男 / 1995-3-20 8 女"
    
    p1 = parse_birth_input(dates[0])
    p2 = parse_birth_input(dates[1])
    
    if not p1["success"] or not p2["success"]:
        return f"❌ 格式错误。正确格式：/match 2000-8-16 6 男 / 1995-3-20 8 女"
    
    result = compute_match(
        p1["date"], p1["hour"], p1["gender"],
        p2["date"], p2["hour"], p2["gender"],
    )
    
    return format_match_for_tg(result)


def handle_name_command(name: str) -> str:
    """处理 /name 命令：姓名拆解分析"""
    if not name or len(name.strip()) < 2:
        return "❌ 请输入姓名。格式：/name 张三\n\n示例：/name 南曦"
    
    import re
    if not re.match(r'^[\u4e00-\u9fff]{2,8}$', name.strip()):
        return "❌ 姓名仅支持2-8个中文字符。格式：/name 张三"
    
    result = analyze_name(name.strip())
    return format_name_analysis_for_tg(result)


def handle_daily_command(text: str) -> str:
    """处理 /daily 命令：日运势"""
    from daily_push import generate_daily_fortune, format_daily_for_tg
    
    parsed = parse_birth_input(text)
    if not parsed["success"]:
        return f"❌ {parsed['error']}"
    
    result = generate_daily_fortune(
        parsed["date"], parsed["hour"], parsed["gender"]
    )
    
    if result["success"]:
        lines = [
            f"☀️ *{result['date']} · 日运势*\n",
            f"📍 宫位：{result['palace_name']}（地支{result['day_branch']}）",
            f"⭐ 星曜：{result['major_stars']}",
            f"🔗 大限：{result['decadal']}\n",
            result.get("ai_prompt", "").split("请给出")[0].strip(),
            "",
            "📜 文化参考，理性看待",
        ]
        return "\n".join(lines)
    return f"❌ {result.get('error')}"


def handle_about() -> str:
    """关于"""
    return (
        "🔮 *一念紫微斗数* v2.1\n\n"
        "AI驱动的紫微斗数深度解盘系统，三派合一。\n\n"
        "**命令：**\n"
        "· /zwds YYYY-MM-DD HH 男/女 — 排盘+基础解读\n"
        "· /reading ... — 完整四层AI解盘+流年流月\n"
        "· /match 甲 / 乙 — 合盘匹配（/分隔两人信息）\n"
        "· /yearly ... [年份] — 流年运势\n"
        "· /monthly ... [年份 月份] — 流月运势\n"
        "· /daily ... — 今日运势\n"
        "· /name 姓名 — 姓名拆字解字+五格数理\n"
        "· /read_en ... — 英文版AI解盘\n"
        "· /star 星名 — 查询星曜百科\n"
        "· /help — 帮助 | /about — 关于\n\n"
        "**支持语言：** zh-CN / en-US / ja-JP\n\n"
        "📜 *文化参考，理性看待*"
    )


if __name__ == "__main__":
    # 测试各种命令
    tests = [
        "/help",
        "/about",
        "/star 紫微",
        "/zwds 1984-6-22 6 男",
        "/reading 1984-6-22 6 男",
        "/yearly 1984-6-22 6 男 2026",
        "/monthly 1984-6-22 6 男 2026 4",
    ]
    for t in tests:
        cmd = t.split()[0].lower()
        if "help" in cmd:
            print(f"\n{'='*50}\n{handle_help()[:200]}...")
        elif "about" in cmd:
            print(f"\n{'='*50}\n{handle_about()}")
        elif "star" in cmd:
            name = " ".join(t.split()[1:]) if len(t.split()) > 1 else ""
            print(f"\n{'='*50}\n{handle_star_command(name)[:200]}...")
        elif "reading" in cmd:
            print(f"\n{'='*50}\n{handle_reading_command(t)[:300]}...")
        elif "yearly" in cmd:
            print(f"\n{'='*50}\n{handle_yearly_command(t)[:300]}...")
        elif "monthly" in cmd:
            print(f"\n{'='*50}\n{handle_monthly_command(t)[:300]}...")
        elif "zwds" in cmd:
            print(f"\n{'='*50}\n{handle_zwds_command(t)[:300]}...")
