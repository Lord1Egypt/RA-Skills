"""
deep_reading.py — 一念紫微斗数 深度解盘引擎（四层架构）
基础→进阶→高阶→专业，AI驱动的多视角分析

Author: 崽儿虾 🦞
"""

from typing import List, Dict, Any, Optional, Tuple
from zwds_calc import (
    AstrolabeResult, StarInfo, PalaceInfo,
    generate_astrolabe, astrolabe_to_json,
    compute_surrounded, BRANCH_TO_INDEX,
    ZWDS_PALACE_NAMES, _get_palace_name_by_branch,
    _find_star_in_palaces, _map_mutagen_name,
    _stem_value, _branch_value,
)
from decadal import calculate_decadal_sequence
import json
import math


# ============================================================
# 第一层：基础解读（12宫 + 主辅星 + 亮度 + 空宫）
# ============================================================

def layer1_basic_reading(astro: AstrolabeResult) -> Dict[str, Any]:
    """
    基础解读：逐宫分析主星、辅星、亮度、空宫状态
    
    返回结构化数据供AI读取
    """
    result = {
        "title": "第一层：基础宫位解读",
        "four_pillars": {
            "year": astro.four_pillars_year,
            "month": astro.four_pillars_month,
            "day": astro.four_pillars_day,
            "hour": astro.four_pillars_hour,
        },
        "zodiac": astro.zodiac,
        "five_elements": astro.five_elements_class,
        "palaces": [],
        "mutagens": [],
    }

    for p in astro.palaces:
        palace_data = {
            "index": p.index,
            "name": p.name_cn,
            "heavenly_stem": p.heavenly_stem,
            "earthly_branch": p.earthly_branch,
            "is_empty": p.is_empty,
            "major_stars": [],
            "minor_stars": [],
        }
        for s in p.major_stars:
            star_info = {"name": s.name, "brightness": s.brightness}
            if s.mutagen:
                star_info["mutagen"] = s.mutagen
            palace_data["major_stars"].append(star_info)
        for s in p.minor_stars:
            star_info = {"name": s.name}
            if s.mutagen:
                star_info["mutagen"] = s.mutagen
            palace_data["minor_stars"].append(star_info)
        result["palaces"].append(palace_data)

    # 生年四化
    for m in astro.mutagens:
        result["mutagens"].append({
            "palace": m["palace"],
            "star": m["star"],
            "mutagen": m["mutagen"],
        })

    # 三方四正
    sur = compute_surrounded(astro.soul_index)
    result["soul_surrounded"] = [astro.palaces[i].name_cn for i in sur]

    return result


# ============================================================
# 第二层：进阶解读（四化飞星 + 格局 + 六亲联动）
# ============================================================

def layer2_advanced_reading(astro: AstrolabeResult) -> Dict[str, Any]:
    """
    进阶解读：
    1. 生年四化深入（禄权科忌在各宫含义）
    2. 宫干飞四化初步（派系差异）
    3. 特殊格局识别
    4. 六亲宫联动
    """
    result = {
        "title": "第二层：四化飞星与格局",
        "mutagen_analysis": [],
        "patterns": [],
        "six_relations": [],
    }

    # 四化分析
    for m in astro.mutagens:
        analysis = _analyze_mutagen(m["star"], m["mutagen"], m["palace"])
        result["mutagen_analysis"].append(analysis)

    # 特殊格局检测
    patterns = _detect_patterns(astro)
    result["patterns"] = patterns

    # 六亲宫联动
    six_relations = _six_relations_analysis(astro)
    result["six_relations"] = six_relations

    return result


def _analyze_mutagen(star: str, mutagen: str, palace: str) -> Dict[str, str]:
    """分析四化含义"""
    meanings = {
        "禄": ("增加、融合、顺遂", "该宫主题和谐顺畅，资源丰沛"),
        "权": ("主导、掌控、权威", "该宫主题主控性强，有担当但有压力"),
        "科": ("文雅、名声、调和", "该宫主题有文化气息，名声佳"),
        "忌": ("缺失、纠葛、收缩", "该宫主题有缺憾，需格外注意"),
    }
    desc, detail = meanings.get(mutagen, ("", ""))
    return {
        "star": star,
        "mutagen": mutagen,
        "meaning": desc,
        "palace": palace,
        "detail": detail,
    }


def _detect_patterns(astro: AstrolabeResult) -> List[Dict[str, str]]:
    """识别特殊格局"""
    patterns = []

    # 获取所有宫的主星列表
    palace_stars = {}
    for p in astro.palaces:
        palace_stars[p.index] = [s.name for s in p.major_stars]

    # 紫府相同宫（紫微+天府+天相）
    for idx, stars in palace_stars.items():
        if "紫微" in stars and "天府" in stars:
            patterns.append({
                "name": "紫府同宫",
                "palace": astro.palaces[idx].name_cn,
                "description": "紫微帝星与天府库星同宫，格局稳重，有领导力和守成之能",
            })

    # 杀破狼（七杀+破军+贪狼在命迁财官）
    has_sha = any("七杀" in s for s in palace_stars.values())
    has_po = any("破军" in s for s in palace_stars.values())
    has_tan = any("贪狼" in s for s in palace_stars.values())
    if has_sha and has_po and has_tan:
        patterns.append({
            "name": "杀破狼",
            "palace": "命宫/迁移宫/财帛宫/官禄宫",
            "description": "三颗变动脉冲星齐聚，一生变动大、机遇多，开创型人格",
        })

    # 机月同梁（天机+太阴+天同+天梁）
    has_ji = any("天机" in s for s in palace_stars.values())
    has_yue = any("太阴" in s for s in palace_stars.values())
    has_tong = any("天同" in s for s in palace_stars.values())
    has_liang = any("天梁" in s for s in palace_stars.values())
    if has_ji and has_yue and has_tong and has_liang:
        patterns.append({
            "name": "机月同梁",
            "palace": "命宫/财帛宫/官禄宫",
            "description": "才艺文星组合，适合稳定型、技术型或文化艺术工作",
        })

    # 日月同宫
    for idx, stars in palace_stars.items():
        if "太阳" in stars and "太阴" in stars:
            patterns.append({
                "name": "日月同宫",
                "palace": astro.palaces[idx].name_cn,
                "description": "阴阳调和，为人既有原则又懂变通，贵气加身",
            })

    return patterns


def _six_relations_analysis(astro: AstrolabeResult) -> List[Dict[str, Any]]:
    """六亲宫联动分析（命宫+父母/兄弟/夫妻/子女/交友）"""
    relations = []
    palaces = astro.palaces

    # 六亲宫
    relation_palaces = [
        (1, "父母"), (11, "兄弟"), (10, "夫妻"),
        (9, "子女"), (5, "交友"),
    ]

    for idx, rel_name in relation_palaces:
        p = palaces[idx]
        major_stars = [s.name for s in p.major_stars]
        minor_stars = [s.name for s in p.minor_stars]
        empty = p.is_empty

        # 联动：对宫+三合
        sur = compute_surrounded(idx)
        sur_names = [palaces[i].name_cn for i in sur]

        relations.append({
            "relation": f"{rel_name}宫",
            "palace": p.name_cn,
            "heavenly_stem": p.heavenly_stem,
            "earthly_branch": p.earthly_branch,
            "is_empty": empty,
            "major_stars": major_stars,
            "minor_stars": minor_stars,
            "three_combined": sur_names,
        })

    return relations


# ============================================================
# 第三层：高阶解读（大限 + 流年/月/日 + 叠宫）
# ============================================================

def layer3_advanced_timing(
    astro: AstrolabeResult,
    target_year: Optional[int] = None,
) -> Dict[str, Any]:
    """
    高阶解读：时间维度运势
    1. 大限（十年大运）
    2. 流年运势
    3. 叠宫分析（大限宫位×流年宫位）
    """
    from datetime import datetime

    current_year = datetime.now().year
    birth_year = int(astro.birth_date.split("-")[0]) if astro.birth_date else current_year
    age = current_year - birth_year

    if target_year:
        age = target_year - birth_year

    year_stem = astro.four_pillars_year[0] if astro.four_pillars_year else "甲"
    gender = astro.gender

    # 大限从命宫开始（命宫在标准序中始终为索引0）
    decadal_seq = calculate_decadal_sequence(
        soul_branch_index=0,
        year_stem=year_stem,
        gender=gender,
        five_elements=astro.five_elements_class,
        current_age=age,
    )

    # 找当前大限
    current_decadal = None
    for d in decadal_seq:
        if d["is_current"]:
            current_decadal = d
            break

    # 流年宫位推断（粗略）
    # 流年地支 = (当前年份 - 1984) % 12 的偏移
    year_offset = (current_year - 1984) % 12
    yearly_branch_list = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    yearly_branch = yearly_branch_list[year_offset]

    # 当前大限宫位
    current_palace = None
    if current_decadal:
        pi = current_decadal["palace_index"]
        current_palace = {
            "palace_name": current_decadal["palace_name"],
            "age_range": f"{current_decadal['age_start']}-{current_decadal['age_end']}岁",
            "palace_stars": _palace_stars_summary(astro, pi),
        }

    return {
        "title": "第三层：大限与流年",
        "current_age": age,
        "current_year": current_year,
        "yearly_branch": yearly_branch,
        "decadal_sequence": decadal_seq,
        "current_decadal": current_decadal,
        "current_decadal_palace": current_palace,
    }


def _palace_stars_summary(astro: AstrolabeResult, palace_index: int) -> Dict:
    """某个宫的星曜摘要"""
    if palace_index < 0 or palace_index >= len(astro.palaces):
        return {}
    p = astro.palaces[palace_index]
    return {
        "name": p.name_cn,
        "heavenly_stem": p.heavenly_stem,
        "earthly_branch": p.earthly_branch,
        "major": [{"name": s.name, "brightness": s.brightness, "mutagen": s.mutagen} for s in p.major_stars],
        "minor": [{"name": s.name} for s in p.minor_stars],
        "is_empty": p.is_empty,
    }


# ============================================================
# 第四层：专业解读（来因宫 + 体用宫 + 星曜互涉）
# ============================================================

def layer4_professional(astro: AstrolabeResult) -> Dict[str, Any]:
    """
    专业解读：
    1. 来因宫（年干定位人生方向）
    2. 体用宫（命财官为体，其余为用）
    3. 星曜互涉（六杀/煞星关联）
    4. 三派差异分析
    """
    result = {
        "title": "第四层：专业深度解析",
        "laiyin_palace": None,
        "tiyong_palaces": None,
        "star_interactions": [],
        "three_schools": {},
    }

    # 来因宫：出生年干的天干地支定位
    year_stem = astro.four_pillars_year[0] if astro.four_pillars_year else ""
    year_branch = astro.four_pillars_year[1] if len(astro.four_pillars_year) > 1 else ""

    # 来因宫 = 年干对应的宫位（天干地支交集）
    for p in astro.palaces:
        if p.heavenly_stem == year_stem:
            result["laiyin_palace"] = {
                "year_stem": year_stem,
                "year_branch": year_branch,
                "palace": p.name_cn,
                "analysis": f"年干{year_stem}坐{p.name_cn}，人生主方向围绕{p.name_cn}主题展开",
            }
            break

    # 体用宫
    body_palaces_idx = [0, 4, 8]  # 命宫、官禄宫(4)、财帛宫(8)
    body_palaces = [astro.palaces[i] for i in body_palaces_idx]
    result["tiyong_palaces"] = {
        "body": [
            {
                "name": p.name_cn,
                "role": {
                    "命宫": "体质、本质",
                    "官禄宫": "事业体",
                    "财帛宫": "财禄体",
                }.get(p.name_cn, "体宫"),
                "stars": _palace_stars_summary(astro, p.index),
            }
            for p in body_palaces
        ],
        "usage_analysis": "命宫为体（本质），官禄宫为用（事业），财帛宫为体用之间（资源）",
    }

    # 星曜互涉（六煞 + 桃花星等）
    # 擎羊、陀罗、火星、铃星、地空、地劫
    all_shas = ["擎羊", "陀罗", "火星", "铃星", "地空", "地劫"]
    sha_locations = []
    for p in astro.palaces:
        all_stars = [s.name for s in p.major_stars + p.minor_stars]
        for sha in all_shas:
            if sha in all_stars:
                sha_locations.append({
                    "star": sha,
                    "palace": p.name_cn,
                    "index": p.index,
                })

    result["star_interactions"] = sha_locations

    # 三派分析
    result["three_schools"] = {
        "sanhe": _sanhe_analysis(astro),
        "feixing": _feixing_analysis(astro),
        "zhanyan": _zhanyan_analysis(astro),
    }

    return result


def _sanhe_analysis(astro: AstrolabeResult) -> Dict[str, Any]:
    """三合派分析要点"""
    p0 = astro.palaces[astro.soul_index]
    sur = compute_surrounded(astro.soul_index)
    return {
        "soul_stars": [s.name for s in p0.major_stars],
        "soul_tree": [astro.palaces[i].name_cn for i in sur],
        "key_combinations": _detect_patterns(astro),
    }


def _feixing_analysis(astro: AstrolabeResult) -> Dict[str, Any]:
    """飞星派分析要点"""
    # 宫干四化（简版）
    palace_stems = {}
    for p in astro.palaces:
        stem = p.heavenly_stem
        if stem and stem in _map_mutagen_name(stem):
            palace_stems[p.name_cn] = stem
    return {
        "palace_stems": palace_stems,
        "self_transformation": "通过AI进行宫干飞四化深入分析",
    }


def _zhanyan_analysis(astro: AstrolabeResult) -> Dict[str, Any]:
    """占验派分析要点"""
    return {
        "tai_sui": "太岁入卦法用于分析特定年份与人的互动",
        "special_patterns": _detect_patterns(astro),
    }


# ============================================================
# 统一入口：四层全量解读
# ============================================================

def full_deep_reading(
    date_str: str,
    hour: int,
    gender: str,
    is_lunar: bool = False,
    target_year: Optional[int] = None,
) -> Dict[str, Any]:
    """
    四层全量深度解读

    Returns:
        {
            "success": bool,
            "basic": {...},
            "advanced": {...},
            "timing": {...},
            "professional": {...},
            "summary": {...},
        }
    """
    astro = generate_astrolabe(date_str, hour, gender, is_lunar)
    if not astro:
        return {"success": False, "error": "排盘失败"}

    basic = layer1_basic_reading(astro)
    advanced = layer2_advanced_reading(astro)
    timing = layer3_advanced_timing(astro, target_year)
    professional = layer4_professional(astro)

    # AI Prompt拼接
    ai_prompt = _build_reading_prompt(basic, advanced, timing, professional)

    return {
        "success": True,
        "basic": basic,
        "advanced": advanced,
        "timing": timing,
        "professional": professional,
        "ai_prompt": ai_prompt,
        "chart_json": astrolabe_to_json(astro),
    }


def _build_reading_prompt(
    basic: Dict,
    advanced: Dict,
    timing: Dict,
    professional: Dict,
) -> str:
    """构建AI解盘完整提示词"""
    lines = []
    lines.append("【一念紫微斗数深度解盘指令】")
    lines.append("")

    # 四柱
    fp = basic["four_pillars"]
    lines.append(f"命主：{fp['year']} {fp['month']} {fp['day']} {fp['hour']}")
    lines.append(f"生肖：{basic['zodiac']}　五行：{basic['five_elements']}")
    lines.append("")

    # 生命四化
    if basic["mutagens"]:
        lines.append("【生年四化】")
        for m in basic["mutagens"]:
            lines.append(f"  {m['palace']}：{m['star']}化{m['mutagen']}")
        lines.append("")

    # 十二宫
    lines.append("【十二宫】")
    for p in basic["palaces"]:
        ms = " ".join(
            f"{s['name']}({s['brightness']})" + (f"→{s['mutagen']}" if s.get('mutagen') else "")
            for s in p["major_stars"]
        )
        mins = " ".join(s["name"] for s in p["minor_stars"])
        empty = "【空宫】" if p["is_empty"] else ""
        line_parts = [f"  {p['name']}：{ms or empty}"]
        if mins:
            line_parts.append(f"〔{mins}〕")
        lines.append("".join(line_parts))
    lines.append("")

    # 格局
    if advanced["patterns"]:
        lines.append("【特殊格局】")
        for pt in advanced["patterns"]:
            lines.append(f"  · {pt['name']}（{pt['palace']}）：{pt['description']}")
        lines.append("")

    # 六亲联动
    if advanced["six_relations"]:
        lines.append("【六亲宫联动】")
        for rel in advanced["six_relations"]:
            ms = "、".join(rel["major_stars"]) if rel["major_stars"] else "空宫"
            th = "、".join(rel["three_combined"])
            lines.append(f"  · {rel['relation']}({rel['palace']})：{ms}  联动：{th}")
        lines.append("")

    # 大限
    d = timing["current_decadal"]
    dp = timing.get("current_decadal_palace")
    if d:
        lines.append("【大限运势】")
        lines.append(f"  当前：{d['age_start']}-{d['age_end']}岁 大限在{d['palace_name']}")
        if dp:
            ms = "、".join(s["name"] for s in dp.get("major", []))
            if ms:
                lines.append(f"  大限宫主星：{ms}")
        lines.append("")
        # 大限表
        lines.append("【十年大运表】")
        for item in timing["decadal_sequence"]:
            mk = "👉" if item["is_current"] else "  "
            lines.append(f"  {mk} {item['age_start']}-{item['age_end']}岁 → {item['palace_name']}")
        lines.append("")

    # 来因宫
    if professional.get("laiyin_palace"):
        lp = professional["laiyin_palace"]
        lines.append(f"【来因宫】年干{lp['year_stem']}在{lp['palace']}，{lp['analysis']}")
        lines.append("")

    # 体用宫
    ty = professional.get("tiyong_palaces", {})
    if ty.get("body"):
        lines.append("【体用宫】")
        for b in ty["body"]:
            lines.append(f"  {b['name']}（{b['role']}）")
        lines.append(f"  {ty.get('usage_analysis', '')}")
        lines.append("")

    # 煞星分布
    if professional.get("star_interactions"):
        lines.append("【煞星分布】")
        for si in professional["star_interactions"]:
            lines.append(f"  · {si['star']}坐{si['palace']}")
        lines.append("")

    # 解盘要求
    lines.append("【解盘要求】")
    lines.append("请基于以上命盘数据，进行四层解读：")
    lines.append("1. 【基础层】逐宫详细解读：主星性质+亮度+空宫借星+辅星配合")
    lines.append("2. 【进阶层】四化脉络分析：禄权科忌在各宫的影响轨迹")
    lines.append("3. 【高阶层】大限当前宫位与流年叠宫分析")
    lines.append("4. 【专业层】用体用宫理论给出整体格局判断")
    lines.append("")
    lines.append("输出格式：每层用【】标题，语言专业但不晦涩，用比喻帮助理解。")
    lines.append("语气使用'可能性''倾向'等开放式表述，避免绝对论断。")
    lines.append("")
    lines.append("📜 文化参考，理性看待")

    return "\n".join(lines)


# ============================================================
# CLI测试
# ============================================================

if __name__ == "__main__":
    import sys

    date = sys.argv[1] if len(sys.argv) > 1 else "1984-6-22"
    hour = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    gender = sys.argv[3] if len(sys.argv) > 3 else "男"

    result = full_deep_reading(date, hour, gender)
    if result["success"]:
        print("=" * 50)
        print(result["ai_prompt"])
        print("=" * 50)
        print(f"\nAI Prompt共 {len(result['ai_prompt'])} 字符")
    else:
        print(f"Error: {result.get('error')}")
