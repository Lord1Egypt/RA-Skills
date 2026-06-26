"""
yinian_zwds.py — 一念紫微斗数 AI解盘统一入口
四层架构：基础→进阶→高阶→专业

Author: 崽儿虾 🦞
"""

from typing import Optional, Dict, Any
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from zwds_calc import generate_astrolabe, format_astrolabe, astrolabe_to_json
from deep_reading import full_deep_reading
from decadal import calculate_decadal_sequence
from formats import format_chart_for_telegram, build_tg_menu
from ai_reader import read_astrolabe


def build_reading_report(
    date_str: str,
    hour: int,
    gender: str,
    is_lunar: bool = False,
    school: str = "综合",
    target_year: Optional[int] = None,
    depth: str = "normal",
) -> Dict[str, Any]:
    """
    统一解盘入口
    
    Args:
        depth: "basic" — 仅排盘
               "normal" — 排盘+基础解读
               "deep" — 四层全量解读
    
    Returns:
        {"chart_text", "chart_json", "reading_prompt", "summary"}
    """
    from datetime import datetime
    
    if not target_year:
        target_year = datetime.now().year
    
    # 排盘
    if depth == "basic":
        astro = generate_astrolabe(date_str, hour, gender, is_lunar)
        if not astro:
            return {"success": False, "error": "排盘失败"}
        return {
            "success": True,
            "chart_text": format_astrolabe(astro),
            "chart_json": astrolabe_to_json(astro),
            "reading_prompt": "",
        }
    
    # 全量深度解盘
    deep = full_deep_reading(date_str, hour, gender, is_lunar, target_year)
    if not deep["success"]:
        return {"success": False, "error": deep.get("error")}
    
    astro = generate_astrolabe(date_str, hour, gender, is_lunar)
    chart_text = format_astrolabe(astro) if astro else ""
    
    # 摘要
    summary = _generate_summary(deep, astro)
    
    return {
        "success": True,
        "chart_text": chart_text,
        "chart_json": astrolabe_to_json(astro) if astro else {},
        "reading_prompt": deep["ai_prompt"],
        "summary": summary,
        "timing": deep["timing"],
        "professional": deep["professional"],
    }


def _generate_summary(deep: Dict[str, Any], astro) -> str:
    """生成简短摘要（Telegram友好）"""
    lines = []
    
    timing = deep.get("timing", {})
    d = timing.get("current_decadal")
    if d:
        lines.append(f"📅 当前大限：{d['palace_name']} ({d['age_start']}-{d['age_end']}岁)")
    
    professional = deep.get("professional", {})
    laiyin = professional.get("laiyin_palace")
    if laiyin:
        lines.append(f"🎯 来因宫：{laiyin['palace']}")
    
    patterns = deep.get("advanced", {}).get("patterns", [])
    if patterns:
        names = "、".join(p["name"] for p in patterns)
        lines.append(f"🏆 格局：{names}")
    
    # 命宫主星
    if astro and astro.palaces:
        p0 = astro.palaces[0]
        ms = "、".join(f"{s.name}({s.brightness})" for s in p0.major_stars)
        if ms:
            lines.append(f"⭐ 命宫：{ms}")
    
    return "\n".join(lines)


def format_full_output(data: Dict[str, Any], depth: str = "deep") -> str:
    """完整Telegram/控制台输出"""
    if not data["success"]:
        return f"❌ {data.get('error', '未知错误')}"
    
    lines = []
    lines.append(data["chart_text"])
    lines.append("")
    
    if data.get("summary"):
        lines.append(data["summary"])
        lines.append("")
    
    if data.get("reading_prompt"):
        lines.append("━━━ 📖 AI解盘指令 ━━━")
        lines.append("")
        lines.append(data["reading_prompt"])
    
    return "\n".join(lines)


# 快速测试
if __name__ == "__main__":
    import sys
    
    date = sys.argv[1] if len(sys.argv) > 1 else "1984-6-22"
    hour = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    gender = sys.argv[3] if len(sys.argv) > 3 else "男"
    
    depth = "deep"
    
    result = build_reading_report(date, hour, gender, depth=depth)
    print(format_full_output(result, depth))
    print(f"\n\n📊 Prompt长度: {len(result.get('reading_prompt', ''))} 字")
