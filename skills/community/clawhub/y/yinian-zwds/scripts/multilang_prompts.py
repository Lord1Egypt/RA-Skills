"""
multilang_prompts.py — 一念紫微斗数 多语言Prompt模板
支持中文/英文/日文AI解盘

Author: 崽儿虾 🦞
"""

from typing import Dict, Optional
from i18n import t, t_palace, t_star, lang_code_validate
from zwds_calc import compute_surrounded


# ============================================================
# 多语言系统提示词
# ============================================================

SYSTEM_PROMPTS: Dict[str, str] = {
    "zh-CN": """你是一位精通紫微斗数的顶尖命理师，擅长三派合一综合解读。

【核心能力】
1. 三合派（中州派）：星曜性质 × 亮度 × 三方四正
2. 飞星派（钦天门）：宫干四化脉络 × 自化 × 追禄追忌
3. 占验派（紫云）：太岁入卦 × 特殊格局 × 星曜互涉

【输出要求】
- 严格按照JSON格式输出报告
- 每层用清晰结构
- 使用可能性语气
- 结语标注：📜 文化参考，理性看待""",

    "en-US": """You are a master of Zi Wei Dou Shu (Purple Star Astrology), skilled in the Three-School integrated approach.

【Core Capabilities】
1. San He (Triple Harmony): Star nature × brightness × Four Harmonies
2. Fei Xing (Flying Star): Stem Transformations × Self-transformation chains
3. Zhan Yan (Divination): Tai Sui implantation × Special patterns

【Output Requirements】
- Output in precise JSON format with the structure {"report": {...}}
- Use probabilistic language ("tends to", "may indicate"), never absolutes
- Include cultural context notes
- End with: 📜 For cultural reference only""",

    "ja-JP": """あなたは紫微斗数の達人で、三派統合の解釈を得意としています。

【核心能力】
1. 三合派：星曜の性質 × 光度 × 三方四正
2. 飛星派：宮干四化 × 自化 × 追禄追忌
3. 占験派：太歳入卦 × 特殊格局 × 星曜互渉

【出力要件】
- JSON形式で出力してください
- 可能性を示す表現を使用し、断定的な言い方は避けてください
- 文化的な参考としての見解であることを示してください""",
}

# ============================================================
# 多语言用户提示模板
# ============================================================

def build_multilang_basic_prompt(chart_data: Dict, lang: str = "zh-CN") -> str:
    """多语言基础宫位解读Prompt"""
    lang = lang_code_validate(lang)
    
    if lang == "en-US":
        return _build_en_basic(chart_data)
    elif lang == "ja-JP":
        return _build_ja_basic(chart_data)
    else:
        return _build_zh_basic(chart_data)


def _build_zh_basic(data: Dict) -> str:
    """中文基础解读"""
    lines = []
    lines.append("【十二宫详解】")
    for p in data.get("palaces", []):
        ms = " ".join(
            f"{s['name']}({s['brightness']})" + (f"→{s['mutagen']}" if s.get('mutagen') else "")
            for s in p.get("major_stars", [])
        )
        mins = " ".join(s["name"] for s in p.get("minor_stars", []))
        empty = "【空宫】" if p.get("is_empty") else ""
        sur = compute_surrounded(p["index"])
        sur_names = [data["palaces"][i]["name_cn"] for i in sur]
        lines.append(f"▪ {p['name_cn']}（{p['heavenly_stem']}{p['earthly_branch']}）：{ms or empty}")
        if mins:
            lines.append(f"  辅星：{mins}")
        lines.append(f"  三方四正：{'、'.join(sur_names)}")
        lines.append("")
    return "\n".join(lines)


def _build_en_basic(data: Dict) -> str:
    """英文基础解读"""
    lines = []
    lines.append("【Twelve Palaces Detail】")
    for p in data.get("palaces", []):
        name_en = t_palace(p["name_cn"], "en-US")
        stem_en = p["heavenly_stem"]
        branch_en = p["earthly_branch"]
        
        majors = []
        for s in p.get("major_stars", []):
            star_en = s.get("name_en", t_star(s["name"], "en-US"))
            bright = s["brightness"]
            star_str = f"{star_en} ({bright})"
            if s.get("mutagen"):
                star_str += f" → {s['mutagen']}"
            majors.append(star_str)
        
        minors = [s["name"] for s in p.get("minor_stars", [])]
        empty = "【Empty Palace (borrow from opposite palace)】" if p.get("is_empty") else ""
        
        sur = compute_surrounded(p["index"])
        sur_names = [t_palace(data["palaces"][i]["name_cn"], "en-US") for i in sur]
        
        major_str = "、".join(majors) if majors else empty
        minor_str = "、".join(minors) if minors else ""
        
        lines.append(f"▪ {name_en} ({stem_en}{branch_en}): {major_str}")
        if minor_str:
            lines.append(f"  Minor stars: {minor_str}")
        lines.append(f"  Four Harmonies: {' - '.join(sur_names)}")
        lines.append("")
    return "\n".join(lines)


def _build_ja_basic(data: Dict) -> str:
    """日文基础解读"""
    lines = []
    lines.append("【十二宮詳細】")
    for p in data.get("palaces", []):
        name_ja = t_palace(p["name_cn"], "ja-JP")
        
        majors = []
        for s in p.get("major_stars", []):
            star_ja = t_star(s["name"], "ja-JP")
            star_str = f"{star_ja}({s['brightness']})"
            if s.get("mutagen"):
                star_str += f" → {s['mutagen']}"
            majors.append(star_str)
        
        minors = [t_star(s["name"], "ja-JP") for s in p.get("minor_stars", [])]
        empty = "【空宮】" if p.get("is_empty") else ""
        
        sur = compute_surrounded(p["index"])
        sur_names = [t_palace(data["palaces"][i]["name_cn"], "ja-JP") for i in sur]
        
        major_str = "、".join(majors) if majors else empty
        minor_str = "、".join(minors) if minors else ""
        
        lines.append(f"▪ {name_ja}：{major_str}")
        if minor_str:
            lines.append(f"  副星：{minor_str}")
        lines.append(f"  三方四正：{'、'.join(sur_names)}")
        lines.append("")
    return "\n".join(lines)


# ============================================================
# 完整多语言解盘Prompt拼接
# ============================================================

def build_multilang_deep_prompt(
    chart_data: Dict,
    deep_data: Dict,
    target_year: int,
    lang: str = "zh-CN",
) -> str:
    """根据语言构建完整解盘Prompt"""
    lang = lang_code_validate(lang)
    
    if lang == "en-US":
        return _build_en_full_prompt(chart_data, deep_data, target_year)
    elif lang == "ja-JP":
        return _build_ja_full_prompt(chart_data, deep_data, target_year)
    else:
        return _build_zh_full_prompt(chart_data, deep_data, target_year)


def _build_zh_full_prompt(chart_data: Dict, deep_data: Dict, target_year: int) -> str:
    """中文完整Prompt（复用之前的）"""
    from prompts import build_full_deep_prompt
    return build_full_deep_prompt(chart_data, deep_data, target_year)


def _build_en_full_prompt(chart_data: Dict, deep_data: Dict, target_year: int) -> str:
    """英文完整Prompt"""
    fp = chart_data.get("four_pillars", {})
    timing = deep_data.get("timing", {})
    d = timing.get("current_decadal")
    
    lines = []
    lines.append(f"📅 Subject: {fp.get('year','')} {fp.get('month','')} {fp.get('day','')} {fp.get('hour','')}")
    lines.append(f"🐉 Zodiac: {chart_data.get('zodiac','')}")
    lines.append(f"🏠 Life Palace: {t_palace(chart_data.get('palaces',[{}])[0].get('name_cn',''))}")
    if d:
        lines.append(f"📍 Current Decade: {t_palace(d['palace_name'])} ({d['age_start']}-{d['age_end']} yrs)")
    lines.append("")
    
    # 四化
    if chart_data.get("mutagens"):
        lines.append("【Yearly Transformations】")
        for m in chart_data["mutagens"]:
            lines.append(f"  · {t_palace(m['palace'])}: {t_star(m['star'])} → {m['mutagen']}")
        lines.append("")
    
    # 十二宫
    lines.append("【Layer 1: Palace Detail】")
    lines.append(_build_en_basic(chart_data))
    
    # 格局
    patterns = deep_data.get("advanced", {}).get("patterns", [])
    if patterns:
        lines.append("【Layer 2: Special Patterns】")
        for pt in patterns:
            lines.append(f"  ▪ {pt['name']}: {pt['description']}")
        lines.append("")
    
    # 大限表
    if timing.get("decadal_sequence"):
        lines.append("【Layer 3: Decade Fortune Table】")
        for item in timing["decadal_sequence"]:
            mk = "👉" if item.get("is_current") else "  "
            pn = t_palace(item["palace_name"], "en-US")
            lines.append(f"  {mk} Age {item['age_start']}-{item['age_end']}: {pn}")
        lines.append("")
    
    # 专业层
    prof = deep_data.get("professional", {})
    laiyin = prof.get("laiyin_palace")
    if laiyin:
        lines.append("【Layer 4: Origin Palace】")
        lines.append(f"  Year Stem {laiyin['year_stem']} in {t_palace(laiyin['palace'])}")
        lines.append("")
    
    # 输出指令
    lines.append("=" * 40)
    lines.append("【Output Requirements】")
    lines.append("Please provide a detailed reading in English following this JSON structure:")
    lines.append("""{
  "report": {
    "metadata": { ... },
    "layers": {
      "basic": {"summary": "overall assessment", "palaces": [...]},
      "advanced": {"patterns": [..], "mutagen_analysis": "..."},
      "timing": {"current_decadal": "interpretation", "yearly": "..."},
      "professional": {"origin_analysis": "...", "body_usage": "..."}
    },
    "conclusion": "holistic assessment and suggestions"
  }
}""")
    lines.append("")
    lines.append("📜 For cultural reference only")
    
    return "\n".join(lines)


def _build_ja_full_prompt(chart_data: Dict, deep_data: Dict, target_year: int) -> str:
    """日文完整Prompt"""
    fp = chart_data.get("four_pillars", {})
    timing = deep_data.get("timing", {})
    d = timing.get("current_decadal")
    
    lines = []
    lines.append(f"📅 対象者：{fp.get('year','')} {fp.get('month','')} {fp.get('day','')} {fp.get('hour','')}")
    lines.append(f"🐉 五行：{chart_data.get('five_elements','')}")
    lines.append(f"🏠 命宮：{t_palace(chart_data.get('palaces',[{}])[0].get('name_cn',''), 'ja-JP')}")
    if d:
        d_nm = t_palace(d['palace_name'], 'ja-JP')
        lines.append(f"📍 現在の大限：{d_nm}（{d['age_start']}-{d['age_end']}歳）")
    lines.append("")
    
    # 十二宫
    lines.append("【第一層：十二宮詳細】")
    lines.append(_build_ja_basic(chart_data))
    
    # 格局
    patterns = deep_data.get("advanced", {}).get("patterns", [])
    if patterns:
        lines.append("【第二層：特殊格局】")
        for pt in patterns:
            lines.append(f"  ▪ {pt['name']}：{pt['description']}")
        lines.append("")
    
    # 大限
    if timing.get("decadal_sequence"):
        lines.append("【第三層：十年大運表】")
        for item in timing["decadal_sequence"]:
            mk = "👉" if item.get("is_current") else "  "
            pn = t_palace(item["palace_name"], "ja-JP")
            lines.append(f"  {mk} {item['age_start']}-{item['age_end']}歳 → {pn}")
        lines.append("")
    
    lines.append("=" * 40)
    lines.append("【出力要件】")
    lines.append("日本語で詳細な解釈を提供してください。")
    lines.append("JSON形式で以下の構造に従ってください。")
    lines.append("📜 文化的な参考として")
    
    return "\n".join(lines)


# ============================================================
# 端到端多语言解盘
# ============================================================

def generate_multilang_reading(
    date_str: str,
    hour: int,
    gender: str,
    lang: str = "en-US",
) -> Dict:
    """生成指定语言的完整解盘"""
    from deep_reading import full_deep_reading
    from zwds_calc import generate_astrolabe, astrolabe_to_json
    from datetime import datetime
    
    astro = generate_astrolabe(date_str, hour, gender)
    if not astro:
        return {"success": False, "error": "Chart failed"}
    
    target_year = datetime.now().year
    chart_data = astrolabe_to_json(astro)
    deep = full_deep_reading(date_str, hour, gender, target_year=target_year)
    
    if not deep["success"]:
        return {"success": False, "error": "Deep analysis failed"}
    
    prompt = build_multilang_deep_prompt(chart_data, deep, target_year, lang)
    system_prompt = SYSTEM_PROMPTS.get(lang, SYSTEM_PROMPTS["en-US"])
    
    return {
        "success": True,
        "chart_json": chart_data,
        "deep_data": deep,
        "system_prompt": system_prompt,
        "user_prompt": prompt,
        "language": lang,
    }


if __name__ == "__main__":
    # 测试
    print("=== English Prompt ===")
    r_en = generate_multilang_reading("1984-6-22", 6, "男", "en-US")
    if r_en["success"]:
        print(f"Length: {len(r_en['user_prompt'])} chars")
        print(r_en["user_prompt"][:600])
    
    print("\n\n=== Japanese Prompt ===")
    r_ja = generate_multilang_reading("1984-6-22", 6, "男", "ja-JP")
    if r_ja["success"]:
        print(f"Length: {len(r_ja['user_prompt'])} chars")
        print(r_ja["user_prompt"][:600])
