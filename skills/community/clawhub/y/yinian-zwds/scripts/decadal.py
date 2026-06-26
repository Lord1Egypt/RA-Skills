"""
decadal.py — 大限（十年大运）推算模块

五行局定起运年龄：
水二局 = 2岁起运
木三局 = 3岁起运
金四局 = 4岁起运
土五局 = 5岁起运
火六局 = 6岁起运

顺逆：阳男阴女顺行，阴男阳女逆行

Author: 崽儿虾 🦞
"""

from typing import List, Dict, Any, Optional, Tuple

# 12地支索引
BRANCH_INDEX = {
    "子": 0, "丑": 1, "寅": 2, "卯": 3,
    "辰": 4, "巳": 5, "午": 6, "未": 7,
    "申": 8, "酉": 9, "戌": 10, "亥": 11,
}

INDEX_BRANCH = {v: k for k, v in BRANCH_INDEX.items()}

# 天干阴阳（阳=0, 阴=1）
STEM_YIN_YANG = {
    "甲": 0, "乙": 1, "丙": 0, "丁": 1, "戊": 0,
    "己": 1, "庚": 0, "辛": 1, "壬": 0, "癸": 1,
}

# 五行局 → 起运年龄
FIVE_ELEMENTS_START_AGE = {
    "水二局": 2, "木三局": 3, "金四局": 4,
    "土五局": 5, "火六局": 6,
}

PALACE_NAMES_CN = [
    "命宫", "父母宫", "福德宫", "田宅宫",
    "官禄宫", "交友宫", "迁移宫", "疾厄宫",
    "财帛宫", "子女宫", "夫妻宫", "兄弟宫",
]

# 生年天干四化表
NATAL_MUTAGEN = {
    "甲": ("廉贞", "破军", "武曲", "太阳"),
    "乙": ("天机", "天梁", "紫微", "太阴"),
    "丙": ("天同", "天机", "文昌", "廉贞"),
    "丁": ("太阴", "天同", "天机", "巨门"),
    "戊": ("贪狼", "太阴", "右弼", "天机"),
    "己": ("武曲", "贪狼", "天梁", "文曲"),
    "庚": ("太阳", "武曲", "太阴", "天同"),
    "辛": ("巨门", "太阳", "文曲", "文昌"),
    "壬": ("天梁", "紫微", "左辅", "武曲"),
    "癸": ("破军", "巨门", "太阴", "贪狼"),
}


def calculate_start_age(five_elements: str) -> int:
    """根据五行局计算起运年龄"""
    return FIVE_ELEMENTS_START_AGE.get(five_elements, 4)


def calculate_decadal_sequence(
    soul_branch_index: int,
    year_stem: str,
    gender: str,
    five_elements: str,
    current_age: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """
    推算全部大限序列
    
    Args:
        soul_branch_index: 命宫地支索引 (0-11)
        year_stem: 年干（如"甲"）
        gender: "男"或"女"
        five_elements: 五行局（如"水二局"）
        current_age: 当前年龄（可选的，用于标注当前大限）
    
    Returns:
        [
            {
                "age_start": 2,
                "age_end": 11,
                "palace_index": 0,
                "palace_name": "命宫",
                "heavenly_stem": "庚",
                "earthly_branch": "午",
                "is_current": True/False,
                "mutagen": [...],
            },
            ...
        ]
    """
    start_age = calculate_start_age(five_elements)
    
    # 阳男/阴女 = 顺行，阴男/阳女 = 逆行
    is_yang = STEM_YIN_YANG.get(year_stem, 0) == 0
    is_male = gender == "男"
    is_forward = (is_yang and is_male) or (not is_yang and not is_male)
    
    step = 1 if is_forward else -1
    
    # 水2 木3 金4 土5 火6 → 每个大限步数年数
    step_years = 10  # 固定每大限10年（主流中州派标准）
    
    # 从命宫开始
    seq = []
    palace_idx = soul_branch_index
    
    for i in range(12):
        age_start = start_age + (i * step_years)
        age_end = age_start + step_years - 1
        
        is_current = False
        if current_age is not None:
            is_current = age_start <= current_age <= age_end
        
        seq.append({
            "age_start": age_start,
            "age_end": age_end,
            "palace_index": palace_idx,
            "palace_name": PALACE_NAMES_CN[palace_idx],
            "heavenly_stem": "",
            "earthly_branch": INDEX_BRANCH[palace_idx],
            "is_current": is_current,
        })
        
        palace_idx = (palace_idx + step) % 12
    
    return seq


def get_decadal_stem_branch(
    seq: List[Dict],
    year_stem: str,
    year_branch: str,
    gender: str,
) -> List[Dict]:
    """
    给大限序列赋天干地支
    
    大限天干 = 命宫天干（以五虎遁定）+ 顺/逆排
    """
    is_yang = STEM_YIN_YANG.get(year_stem, 0) == 0
    is_male = gender == "男"
    is_forward = (is_yang and is_male) or (not is_yang and not is_male)
    
    # 第一个大限的干支 = 命宫干支
    # 支是命宫地支，干是命宫天干（需从已知数据获取）
    # 天干递增/递减（顺行加1，逆行减1），地支也同方向
    
    for item in seq:
        pass  # 干支由外部传入
    
    return seq


def format_decadal_table(seq: List[Dict]) -> str:
    """格式化大限表"""
    lines = []
    lines.append("📅 *十年大运表*")
    lines.append("")
    
    for item in seq:
        marker = "👉 " if item.get("is_current") else "   "
        range_str = f"{item['age_start']}-{item['age_end']}岁"
        palace = item["palace_name"]
        
        lines.append(f"{marker}{range_str}  →  {palace}")
    
    lines.append("")
    lines.append("📜 *文化参考，理性看待*")
    
    return "\n".join(lines)


if __name__ == "__main__":
    # 南曦测试（1984甲子年，水二局，命宫午=6，阳男顺行）
    seq = calculate_decadal_sequence(6, "甲", "男", "水二局")
    print(format_decadal_table(seq))
    print()
    for s in seq:
        print(f"  {s['age_start']}-{s['age_end']}岁: {s['palace_name']} {'👈 当前' if s['is_current'] else ''}")
