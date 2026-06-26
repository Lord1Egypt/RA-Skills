"""
daily_push.py — 一念紫微斗数 日运势推送模块
支持每日/每周运势推送，计划用于TG Bot定时发送

Author: 崽儿虾 🦞
"""

from typing import Optional, Dict, Any
from datetime import datetime
from zwds_calc import generate_astrolabe, BRANCH_TO_INDEX
from deep_reading import full_deep_reading
from decadal import calculate_decadal_sequence


# ============================================================
# 日运势（基于流日地支）
# ============================================================

def generate_daily_fortune(
    date_str: str,
    hour: int,
    gender: str,
    target_date: Optional[str] = None,
) -> Dict[str, Any]:
    """
    日运势分析
    
    基于流日地支对应的宫位 + 时辰引动
    
    Args:
        target_date: "YYYY-MM-DD" 格式，默认为今天
    """
    if not target_date:
        target_date = datetime.now().strftime("%Y-%m-%d")
    
    dt = datetime.strptime(target_date, "%Y-%m-%d")
    year = dt.year
    month = dt.month
    day = dt.day
    hour_now = dt.hour
    
    astro = generate_astrolabe(date_str, hour, gender)
    if not astro:
        return {"success": False, "error": "排盘失败"}
    
    deep = full_deep_reading(date_str, hour, gender, target_year=year)
    timing = deep.get("timing", {})
    
    # 流日地支（按60天周期简化）
    day_offset = (dt - datetime(1984, 1, 1)).days
    branch_idx = day_offset % 12
    day_branch_list = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    day_branch = day_branch_list[branch_idx]
    
    # 流日对应标准宫序
    soul_branch = astro.soul_palace_branch or "子"
    soul_iztro_idx = BRANCH_TO_INDEX.get(soul_branch, 10)
    day_iztro_idx = BRANCH_TO_INDEX.get(day_branch, 0)
    palace_idx = (day_iztro_idx - soul_iztro_idx) % 12
    
    palace = astro.palaces[palace_idx] if 0 <= palace_idx < len(astro.palaces) else None
    
    if not palace:
        return {"success": False, "error": "找不到对应宫位"}
    
    majors = [f"{s.name}({s.brightness})" + (f"→{s.mutagen}" if s.mutagen else "") for s in palace.major_stars]
    minors = [s.name for s in palace.minor_stars]
    
    mstr = "、".join(majors) if majors else "空宫"
    mistr = "、".join(minors) if minors else "无辅星"
    
    # 当前时辰引动
    hour_branch_list = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    hour_branch_idx = hour_now // 2 % 12
    hour_branch = hour_branch_list[hour_branch_idx]
    
    d = timing.get("current_decadal", {})
    decadal_info = f"{d['palace_name']}（{d['age_start']}-{d['age_end']}岁）" if d else "未知"
    
    prompt = f"""请简析今日运势（紫微斗数）：

日期：{target_date}
流日地支：{day_branch}
当前时辰：{hour_branch}
当前大限：{decadal_info}

今日宫位：{palace.name_cn}
主星：{mstr}
辅星：{mistr}
{"（空宫借对宫星曜）" if palace.is_empty else ""}

请给出（每条30字以内）：
1. 今日主题
2. 注意事项
3. 有利方向
"""
    
    return {
        "success": True,
        "date": target_date,
        "day_branch": day_branch,
        "hour_branch": hour_branch,
        "palace_name": palace.name_cn,
        "major_stars": mstr,
        "minor_stars": mistr,
        "is_empty": palace.is_empty,
        "ai_prompt": prompt,
        "decadal": d["palace_name"] if d else "",
    }


# ============================================================
# 本周运势
# ============================================================

def generate_weekly_fortune(
    date_str: str,
    hour: int,
    gender: str,
    week_start: Optional[str] = None,
) -> Dict[str, Any]:
    """
    本周运势（7天）
    """
    if not week_start:
        from datetime import timedelta
        today = datetime.now()
        week_start = (today - timedelta(days=today.weekday())).strftime("%Y-%m-%d")
    
    ws = datetime.strptime(week_start, "%Y-%m-%d")
    
    days = []
    for i in range(7):
        d = ws.strftime("%Y-%m-%d")
        day_result = generate_daily_fortune(date_str, hour, gender, d)
        if day_result.get("success"):
            days.append(day_result)
        ws = datetime.fromordinal(ws.toordinal() + 1)
    
    return {
        "success": True,
        "week_start": week_start,
        "days": days,
    }


# ============================================================
# Telegram格式化
# ============================================================

def format_daily_for_tg(result: Dict) -> str:
    """日运势格式化为Telegram"""
    if not result["success"]:
        return f"❌ {result.get('error')}"
    
    lines = []
    lines.append(f"☀️ *{result['date']} · 日运势*")
    lines.append("")
    lines.append(f"📍 宫位：{result['palace_name']}（地支{result['day_branch']}）")
    lines.append(f"⭐ 星曜：{result['major_stars']}")
    lines.append("")
    lines.append("💡 " + result.get("ai_prompt", "").split("请给出")[0].strip())
    lines.append("")
    lines.append("📜 文化参考，理性看待")
    
    return "\n".join(lines)


if __name__ == "__main__":
    print("=== 今日运势 ===")
    r = generate_daily_fortune("1984-6-22", 6, "男")
    if r["success"]:
        print(format_daily_for_tg(r))
        print()
        print("AI Prompt:")
        print(r["ai_prompt"])
