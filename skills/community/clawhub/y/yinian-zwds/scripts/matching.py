"""
matching.py — 一念紫微斗数 合盘匹配引擎
情侣/朋友/事业伙伴合盘分析

Author: 崽儿虾 🦞
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from zwds_calc import generate_astrolabe, astrolabe_to_json
from deep_reading import full_deep_reading
from i18n import t_palace, t_star, t


# ============================================================
# 合盘核心维度
# ============================================================

MATCH_DIMENSIONS = {
    "命宫互看": "Life Palace mutual influence",
    "夫妻宫": "Marriage Palace resonance",
    "四化交集": "Four Transformations intersection",
    "五行互补": "Elemental complement",
    "福德宫": "Spiritual compatibility",
}


def compute_match(
    date1: str, hour1: int, gender1: str,
    date2: str, hour2: int, gender2: str,
) -> Dict[str, Any]:
    """
    两人合盘分析
    
    Returns:
        {
            "success": bool,
            "person_a": {...},  # 命盘数据
            "person_b": {...},  # 命盘数据
            "dimensions": {     # 各维度分析
                "命宫互看": {...},
                "夫妻宫": {...},
                ...
            },
            "score": 65,         # 综合评分 0-100
            "summary": "...",    # AI解盘Prompt
        }
    """
    a = generate_astrolabe(date1, hour1, gender1)
    b = generate_astrolabe(date2, hour2, gender2)
    
    if not a or not b:
        return {"success": False, "error": "排盘失败"}
    
    a_json = astrolabe_to_json(a)
    b_json = astrolabe_to_json(b)
    
    # 各维度分析
    dimensions = {}
    
    # 1. 命宫互看
    dimensions["命宫互看"] = _analyze_life_mutual(a, b, a_json, b_json)
    
    # 2. 夫妻宫
    dimensions["夫妻宫"] = _analyze_marriage(a, b)
    
    # 3. 四化交集
    dimensions["四化交集"] = _analyze_mutagen_intersection(a, b)
    
    # 4. 五行互补
    dimensions["五行互补"] = _analyze_element(a, b)
    
    # 5. 福德宫
    dimensions["福德宫"] = _analyze_spirit(a, b)
    
    # 综合评分
    score = _compute_score(dimensions)
    
    # AI解盘Prompt
    summary = _build_match_prompt(a, b, a_json, b_json, dimensions, score)
    
    return {
        "success": True,
        "person_a": a_json,
        "person_b": b_json,
        "dimensions": dimensions,
        "score": score,
        "score_text": _score_to_text(score),
        "ai_prompt": summary,
    }


def _analyze_life_mutual(
    a, b, a_json: Dict, b_json: Dict
) -> Dict[str, Any]:
    """命宫互看：A的命宫星曜对B的影响"""
    a_soul = a_json["palaces"][0]
    b_soul = b_json["palaces"][0]
    
    a_stars = [s["name"] for s in a_soul["major_stars"]]
    b_stars = [s["name"] for s in b_soul["major_stars"]]
    
    return {
        "a_life_stars": a_stars,
        "b_life_stars": b_stars,
        "analysis": f"A命宫{len(a_stars) and a_stars[0] or '空'} | B命宫{len(b_stars) and b_stars[0] or '空'}",
    }


def _analyze_marriage(a, b) -> Dict[str, Any]:
    """夫妻宫分析"""
    a_marriage = a.palaces[10]  # 夫妻宫在标准序中索引10
    b_marriage = b.palaces[10]
    
    a_ms = [s.name for s in a_marriage.major_stars]
    b_ms = [s.name for s in b_marriage.major_stars]
    
    return {
        "a_marriage_stars": a_ms,
        "b_marriage_stars": b_ms,
        "a_marriage_empty": a_marriage.is_empty,
        "b_marriage_empty": b_marriage.is_empty,
    }


def _analyze_mutagen_intersection(a, b) -> Dict[str, Any]:
    """四化交集分析"""
    a_mut = [(m["star"], m["mutagen"], m["palace"]) for m in a.mutagens if isinstance(m, dict)]
    b_mut = [(m["star"], m["mutagen"], m["palace"]) for m in b.mutagens if isinstance(m, dict)]
    
    # 寻找相同四化的星曜
    common = []
    for s1, m1, p1 in a_mut:
        for s2, m2, p2 in b_mut:
            if s1 == s2 and m1 == m2:
                common.append(f"共同{m1}: {s1}化{m1}")
    
    return {
        "a_mutagens": a_mut,
        "b_mutagens": b_mut,
        "common_transformations": common,
    }


def _analyze_element(a, b) -> Dict[str, Any]:
    """五行互补分析"""
    a_elem = a.five_elements_class or ""
    b_elem = b.five_elements_class or ""
    
    # 五行相生相克
    elem_num = {"水二局": 0, "木三局": 1, "金四局": 2, "土五局": 3, "火六局": 4}
    producing = [(0,1),(1,2),(2,3),(3,4),(4,0)]  # 相生
    destroying = [(0,2),(2,1),(1,3),(3,0),(0,4)]  # 相克
    
    ae = elem_num.get(a_elem, -1)
    be = elem_num.get(b_elem, -1)
    
    relation = "未知"
    if ae >= 0 and be >= 0:
        if (ae, be) in producing:
            relation = "相生（互补）"
        elif (be, ae) in producing:
            relation = "相生（互补）"
        elif (ae, be) in destroying:
            relation = "相克（需调和）"
        elif (be, ae) in destroying:
            relation = "相克（需调和）"
        else:
            relation = "同元素"
    
    return {
        "a_element": a_elem,
        "b_element": b_elem,
        "relationship": relation,
    }


def _analyze_spirit(a, b) -> Dict[str, Any]:
    """福德宫精神层面分析"""
    a_spirit = a.palaces[2]
    b_spirit = b.palaces[2]
    
    a_ms = [s.name for s in a_spirit.major_stars]
    b_ms = [s.name for s in b_spirit.major_stars]
    
    return {
        "a_spirit_stars": a_ms,
        "b_spirit_stars": b_ms,
    }


def _compute_score(dimensions: Dict) -> int:
    """计算综合评分 0-100"""
    score = 60  # 基础分
    
    # 各维度加分/扣分逻辑
    marriage = dimensions.get("夫妻宫", {})
    if not marriage.get("a_marriage_empty") and not marriage.get("b_marriage_empty"):
        score += 10
    
    mutual = dimensions.get("四化交集", {})
    if mutual.get("common_transformations"):
        score += 10
    
    element = dimensions.get("五行互补", {})
    if "相生" in element.get("relationship", ""):
        score += 10
    elif "相克" in element.get("relationship", ""):
        score -= 5
    
    return max(0, min(100, score))


def _score_to_text(score: int) -> str:
    """评分文字描述"""
    if score >= 85:
        return "绝配"
    elif score >= 70:
        return "合拍"
    elif score >= 55:
        return "一般"
    elif score >= 40:
        return "需磨合"
    else:
        return "有挑战"


def _build_match_prompt(
    a, b, a_json: Dict, b_json: Dict,
    dimensions: Dict, score: int,
) -> str:
    """构建合盘AI解盘Prompt"""
    lines = []
    lines.append("【紫微斗数合盘分析】")
    lines.append("")
    
    # 双方信息
    lines.append(f"A：{a.birth_date} 时{a.birth_hour} {a.gender}")
    lines.append(f"  命宫：{a.palaces[0].name_cn}  五行：{a.five_elements_class}")
    lines.append(f"  夫妻宫：{a.palaces[10].name_cn}  主星：{_stars_str(a.palaces[10])}")
    lines.append("")
    
    lines.append(f"B：{b.birth_date} 时{b.birth_hour} {b.gender}")
    lines.append(f"  命宫：{b.palaces[0].name_cn}  五行：{b.five_elements_class}")
    lines.append(f"  夫妻宫：{b.palaces[10].name_cn}  主星：{_stars_str(b.palaces[10])}")
    lines.append("")
    
    # 各维度
    lines.append("【各维度分析】")
    
    e = dimensions.get("五行互补", {})
    lines.append(f"▪ 五行关系：{e.get('a_element')} × {e.get('b_element')} → {e.get('relationship')}")
    
    m = dimensions.get("四化交集", {})
    if m.get("common_transformations"):
        lines.append(f"▪ 四化交集：{'、'.join(m['common_transformations'])}")
    
    lines.append("")
    lines.append(f"综合评分：{score}/100（{_score_to_text(score)}）")
    lines.append("")
    
    lines.append("请从以下角度分析这段关系：")
    lines.append("1. 命宫星曜的互动模式")
    lines.append("2. 夫妻宫的相合程度")
    lines.append("3. 四化连线带来的缘分深度")
    lines.append("4. 五行互补与调和空间")
    lines.append("5. 彼此提供的关键支持领域")
    lines.append("")
    lines.append("📜 文化参考，理性看待")
    
    return "\n".join(lines)


def _stars_str(palace) -> str:
    """宫位主星字符串"""
    return "、".join(f"{s.name}({s.brightness})" for s in palace.major_stars) or "空宫"


# ============================================================
# Telegram格式化输出
# ============================================================

def format_match_for_tg(result: Dict) -> str:
    """合盘结果格式化为Telegram文本"""
    if not result["success"]:
        return f"❌ {result.get('error')}"
    
    a = result["person_a"]
    b = result["person_b"]
    
    lines = []
    lines.append("💞 *紫微斗数 · 合盘匹配*")
    lines.append("")
    
    # 双方基础
    a_fp = a.get("four_pillars", {})
    b_fp = b.get("four_pillars", {})
    a_soul = a.get("palaces", [{}])[0]
    b_soul = b.get("palaces", [{}])[0]
    
    lines.append("*A方*")
    lines.append(f"📅 {a.get('birth_date','')} 五行：{a.get('five_elements','')}")
    lines.append(f"🏠 命宫：{a_soul.get('name_cn','')} 夫妻宫：{a.get('palaces',[{}])[10].get('name_cn','')}")
    lines.append("")
    
    lines.append("*B方*")
    lines.append(f"📅 {b.get('birth_date','')} 五行：{b.get('five_elements','')}")
    lines.append(f"🏠 命宫：{b_soul.get('name_cn','')} 夫妻宫：{b.get('palaces',[{}])[10].get('name_cn','')}")
    lines.append("")
    
    # 评分
    score = result.get("score", 50)
    score_t = result.get("score_text", "")
    score_bar = "▓" * (score // 10) + "░" * (10 - score // 10)
    lines.append(f"*综合契合度*：{score}/100 {score_bar}")
    lines.append(f"评估：{score_t}")
    lines.append("")
    
    # 各维度
    dims = result.get("dimensions", {})
    
    elem = dims.get("五行互补", {})
    lines.append(f"▪ *五行*：{elem.get('a_element')} × {elem.get('b_element')}")
    lines.append(f"  → {elem.get('relationship', '')}")
    
    marriage = dims.get("夫妻宫", {})
    a_marry = "、".join(marriage.get("a_marriage_stars", [])) or "空宫"
    b_marry = "、".join(marriage.get("b_marriage_stars", [])) or "空宫"
    lines.append(f"▪ *夫妻宫*：A-{a_marry} | B-{b_marry}")
    
    mutual = dims.get("四化交集", {})
    if mutual.get("common_transformations"):
        lines.append(f"▪ *四化共鸣*：{'、'.join(mutual['common_transformations'])}")
    
    lines.append("")
    lines.append("📜 文化参考，理性看待")
    
    return "\n".join(lines)


if __name__ == "__main__":
    # 测试合盘
    result = compute_match(
        "1984-6-22", 6, "男",   # 南曦
        "1990-3-15", 8, "女",   # 测试
    )
    
    if result["success"]:
        print(format_match_for_tg(result))
        print()
        print("=" * 40)
        print("AI Prompt:")
        print(result["ai_prompt"])
    else:
        print(f"❌ {result.get('error')}")
