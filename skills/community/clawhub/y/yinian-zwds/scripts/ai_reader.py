"""
ai_reader.py — 一念紫微斗数 AI解盘引擎（旧版兼容适配器）
主要流程委托给 ai_engine / deep_reading / prompts_v2

Author: 崽儿虾 🦞
"""

from typing import Optional, Dict, Any, List
from zwds_calc import (
    AstrolabeResult, generate_astrolabe, 
    astrolabe_to_json, format_astrolabe,
    compute_surrounded
)
from deep_reading import full_deep_reading, layer1_basic_reading
from ai_engine import ai_reading


def read_astrolabe(astro_data, school: str = "综合") -> str:
    """使用AI解读命盘，返回结构化提示词（旧版兼容）"""
    if isinstance(astro_data, dict):
        chart_json = astro_data
    else:
        chart_json = astrolabe_to_json(astro_data)
    
    deep = full_deep_reading(
        chart_json.get("birth_date", "1984-6-22"),
        chart_json.get("birth_hour", 6),
        chart_json.get("gender", "男"),
    )
    
    if deep["success"]:
        return deep["ai_prompt"]
    
    # 降级：基础prompt
    palaces_str = ""
    for p in chart_json.get("palaces", []):
        major = " ".join(
            f"{s['name']}({s['brightness']}{'→'+str(s.get('mutagen','')) if s.get('mutagen') else ''})"
            for s in p.get("major_stars", [])
        )
        minor = " ".join(s["name"] for s in p.get("minor_stars", []))
        palaces_str += f"  {p['name_cn']}({p['heavenly_stem']}{p['earthly_branch']}): {major} {'附:'+minor if minor else ''}\n"

    mutagens_str = "\n".join(
        f"  {m['palace']}: {m['star']}化{m['mutagen']}"
        for m in chart_json.get("mutagens", [])
    )

    return f"""请以{school}视角解读以下命盘：

【四柱】
{chart_json.get('four_pillars', {}).get('year','')} {chart_json.get('four_pillars', {}).get('month','')} {chart_json.get('four_pillars', {}).get('day','')} {chart_json.get('four_pillars', {}).get('hour','')}
生肖: {chart_json.get('zodiac','')} 五行局: {chart_json.get('five_elements','')}

【生年四化】
{mutagens_str}

【十二宫】
{palaces_str}

请逐宫解读。📜"""


def create_chart_and_reading(
    date_str: str,
    hour: int,
    gender: str,
    is_lunar: bool = False,
    school: str = "综合",
    language: str = "zh-CN",
) -> dict:
    """排盘 + AI解读（旧版兼容）"""
    astro = generate_astrolabe(date_str, hour, gender, is_lunar)
    if not astro:
        return {"success": False, "error": "排盘失败"}
    
    chart_json = astrolabe_to_json(astro)
    chart_text = format_astrolabe(astro)
    
    prompt = read_astrolabe(chart_json, school)
    
    return {
        "success": True,
        "chart_json": chart_json,
        "chart_text": chart_text,
        "prompt": prompt,
    }
