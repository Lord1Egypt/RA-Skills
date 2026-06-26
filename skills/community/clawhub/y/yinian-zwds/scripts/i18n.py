"""
i18n.py — 一念紫微斗数 国际化多语言模块
支持：zh-CN/zh-TW/en-US/ja-JP/ko-KR/vi-VN

Author: 崽儿虾 🦞
"""

from typing import Dict, List, Optional, Tuple

# ============================================================
# 核心词库
# ============================================================

LANGUAGES = {
    "zh-CN": "简体中文",
    "zh-TW": "繁體中文",
    "en-US": "English",
    "ja-JP": "日本語",
    "ko-KR": "한국어",
    "vi-VN": "Tiếng Việt",
}

def lang_code_validate(code: str) -> str:
    """验证并标准化语言代码"""
    mapping = {
        "zh": "zh-CN", "cn": "zh-CN", "zh-cn": "zh-CN",
        "zh-tw": "zh-TW", "tw": "zh-TW",
        "en": "en-US", "en-us": "en-US",
        "ja": "ja-JP", "ja-jp": "ja-JP", "jp": "ja-JP",
        "ko": "ko-KR", "ko-kr": "ko-KR", "kr": "ko-KR",
        "vi": "vi-VN", "vi-vn": "vi-VN", "vn": "vi-VN",
    }
    return mapping.get(code.lower(), code) if "-" not in code else code


# ============================================================
# 宫位翻译
# ============================================================

PALACE_NAMES: Dict[str, Dict[str, str]] = {
    "命宫": {
        "zh-CN": "命宫", "zh-TW": "命宮",
        "en-US": "Life", "ja-JP": "命宮",
        "ko-KR": "명궁", "vi-VN": "Mệnh cung",
    },
    "父母宫": {
        "zh-CN": "父母宫", "zh-TW": "父母宮",
        "en-US": "Parents", "ja-JP": "父母宮",
        "ko-KR": "부모궁", "vi-VN": "Phụ mẫu cung",
    },
    "福德宫": {
        "zh-CN": "福德宫", "zh-TW": "福德宮",
        "en-US": "Spirit", "ja-JP": "福德宮",
        "ko-KR": "복덕궁", "vi-VN": "Phúc đức cung",
    },
    "田宅宫": {
        "zh-CN": "田宅宫", "zh-TW": "田宅宮",
        "en-US": "Property", "ja-JP": "田宅宮",
        "ko-KR": "전택궁", "vi-VN": "Điền trạch cung",
    },
    "官禄宫": {
        "zh-CN": "官禄宫", "zh-TW": "官祿宮",
        "en-US": "Career", "ja-JP": "官禄宮",
        "ko-KR": "관록궁", "vi-VN": "Quan lộc cung",
    },
    "交友宫": {
        "zh-CN": "交友宫", "zh-TW": "交友宮",
        "en-US": "Friends", "ja-JP": "交友宮",
        "ko-KR": "교우궁", "vi-VN": "Giao hữu cung",
    },
    "迁移宫": {
        "zh-CN": "迁移宫", "zh-TW": "遷移宮",
        "en-US": "Travel", "ja-JP": "遷移宮",
        "ko-KR": "천이궁", "vi-VN": "Thiên di cung",
    },
    "疾厄宫": {
        "zh-CN": "疾厄宫", "zh-TW": "疾厄宮",
        "en-US": "Health", "ja-JP": "疾厄宮",
        "ko-KR": "질액궁", "vi-VN": "Tật ách cung",
    },
    "财帛宫": {
        "zh-CN": "财帛宫", "zh-TW": "財帛宮",
        "en-US": "Wealth", "ja-JP": "財帛宮",
        "ko-KR": "재백궁", "vi-VN": "Tài bạch cung",
    },
    "子女宫": {
        "zh-CN": "子女宫", "zh-TW": "子女宮",
        "en-US": "Children", "ja-JP": "子女宮",
        "ko-KR": "자녀궁", "vi-VN": "Tử nữ cung",
    },
    "夫妻宫": {
        "zh-CN": "夫妻宫", "zh-TW": "夫妻宮",
        "en-US": "Marriage", "ja-JP": "夫妻宮",
        "ko-KR": "부처궁", "vi-VN": "Phu thê cung",
    },
    "兄弟宫": {
        "zh-CN": "兄弟宫", "zh-TW": "兄弟宮",
        "en-US": "Siblings", "ja-JP": "兄弟宮",
        "ko-KR": "형제궁", "vi-VN": "Huynh đệ cung",
    },
}

# ============================================================
# 四化翻译
# ============================================================

MUTAGEN_NAMES: Dict[str, Dict[str, str]] = {
    "禄": {"zh-CN": "化禄", "zh-TW": "化祿", "en-US": "Prosperity(Hua-Lu)", "ja-JP": "化禄", "ko-KR": "화록", "vi-VN": "Hóa Lộc"},
    "权": {"zh-CN": "化权", "zh-TW": "化權", "en-US": "Authority(Hua-Quan)", "ja-JP": "化権", "ko-KR": "화권", "vi-VN": "Hóa Quyền"},
    "科": {"zh-CN": "化科", "zh-TW": "化科", "en-US": "Fame(Hua-Ke)", "ja-JP": "化科", "ko-KR": "화과", "vi-VN": "Hóa Khoa"},
    "忌": {"zh-CN": "化忌", "zh-TW": "化忌", "en-US": "Worry(Hua-Ji)", "ja-JP": "化忌", "ko-KR": "화기", "vi-VN": "Hóa Kỵ"},
}

# ============================================================
# 亮度翻译
# ============================================================

BRIGHTNESS: Dict[str, Dict[str, str]] = {
    "庙": {"zh-CN": "庙", "zh-TW": "廟", "en-US": "Temple", "ja-JP": "廟", "ko-KR": "묘", "vi-VN": "Miếu"},
    "旺": {"zh-CN": "旺", "zh-TW": "旺", "en-US": "Prosperous", "ja-JP": "旺", "ko-KR": "왕", "vi-VN": "Vượng"},
    "得": {"zh-CN": "得", "zh-TW": "得", "en-US": "Adequate", "ja-JP": "得", "ko-KR": "득", "vi-VN": "Đắc"},
    "利": {"zh-CN": "利", "zh-TW": "利", "en-US": "Favorable", "ja-JP": "利", "ko-KR": "리", "vi-VN": "Lợi"},
    "平": {"zh-CN": "平", "zh-TW": "平", "en-US": "Flat", "ja-JP": "平", "ko-KR": "평", "vi-VN": "Bình"},
    "陷": {"zh-CN": "陷", "zh-TW": "陷", "en-US": "Weakened", "ja-JP": "陥", "ko-KR": "함", "vi-VN": "Hãm"},
}

# ============================================================
# 主要星曜翻译
# ============================================================

MAJOR_STARS: Dict[str, Dict[str, str]] = {
    "紫微": {"en-US": "Zi Wei (Emperor)", "ja-JP": "紫微", "ko-KR": "자미", "vi-VN": "Tử Vi"},
    "天机": {"en-US": "Tian Ji (Secrets)", "ja-JP": "天機", "ko-KR": "천기", "vi-VN": "Thiên Cơ"},
    "太阳": {"en-US": "Tai Yang (Sun)", "ja-JP": "太陽", "ko-KR": "태양", "vi-VN": "Thái Dương"},
    "武曲": {"en-US": "Wu Qu (Finance)", "ja-JP": "武曲", "ko-KR": "무곡", "vi-VN": "Vũ Khúc"},
    "天同": {"en-US": "Tian Tong (Harmony)", "ja-JP": "天同", "ko-KR": "천동", "vi-VN": "Thiên Đồng"},
    "廉贞": {"en-US": "Lian Zhen (Integrity)", "ja-JP": "廉貞", "ko-KR": "염정", "vi-VN": "Liêm Trinh"},
    "天府": {"en-US": "Tian Fu (Treasury)", "ja-JP": "天府", "ko-KR": "천부", "vi-VN": "Thiên Phủ"},
    "太阴": {"en-US": "Tai Yin (Moon)", "ja-JP": "太陰", "ko-KR": "태음", "vi-VN": "Thái Âm"},
    "贪狼": {"en-US": "Tan Lang (Wolf)", "ja-JP": "貪狼", "ko-KR": "탐랑", "vi-VN": "Tham Lang"},
    "巨门": {"en-US": "Ju Men (Gate)", "ja-JP": "巨門", "ko-KR": "거문", "vi-VN": "Cự Môn"},
    "天相": {"en-US": "Tian Xiang (Minister)", "ja-JP": "天相", "ko-KR": "천상", "vi-VN": "Thiên Tướng"},
    "天梁": {"en-US": "Tian Liang (Blessing)", "ja-JP": "天梁", "ko-KR": "천량", "vi-VN": "Thiên Lương"},
    "七杀": {"en-US": "Qi Sha (7 Killings)", "ja-JP": "七殺", "ko-KR": "칠살", "vi-VN": "Thất Sát"},
    "破军": {"en-US": "Po Jun (Destroyer)", "ja-JP": "破軍", "ko-KR": "파군", "vi-VN": "Phá Quân"},
}

# ============================================================
# 天干地支翻译
# ============================================================

HEAVENLY_STEMS: Dict[str, Dict[str, str]] = {
    "甲": {"en-US": "Jia", "ja-JP": "甲", "ko-KR": "갑", "vi-VN": "Giáp"},
    "乙": {"en-US": "Yi", "ja-JP": "乙", "ko-KR": "을", "vi-VN": "Ất"},
    "丙": {"en-US": "Bing", "ja-JP": "丙", "ko-KR": "병", "vi-VN": "Bính"},
    "丁": {"en-US": "Ding", "ja-JP": "丁", "ko-KR": "정", "vi-VN": "Đinh"},
    "戊": {"en-US": "Wu", "ja-JP": "戊", "ko-KR": "무", "vi-VN": "Mậu"},
    "己": {"en-US": "Ji", "ja-JP": "己", "ko-KR": "기", "vi-VN": "Kỷ"},
    "庚": {"en-US": "Geng", "ja-JP": "庚", "ko-KR": "경", "vi-VN": "Canh"},
    "辛": {"en-US": "Xin", "ja-JP": "辛", "ko-KR": "신", "vi-VN": "Tân"},
    "壬": {"en-US": "Ren", "ja-JP": "壬", "ko-KR": "임", "vi-VN": "Nhâm"},
    "癸": {"en-US": "Gui", "ja-JP": "癸", "ko-KR": "계", "vi-VN": "Quý"},
}

EARTHLY_BRANCHES: Dict[str, Dict[str, str]] = {
    "子": {"en-US": "Zi", "ja-JP": "子", "ko-KR": "자", "vi-VN": "Tý"},
    "丑": {"en-US": "Chou", "ja-JP": "丑", "ko-KR": "축", "vi-VN": "Sửu"},
    "寅": {"en-US": "Yin", "ja-JP": "寅", "ko-KR": "인", "vi-VN": "Dần"},
    "卯": {"en-US": "Mao", "ja-JP": "卯", "ko-KR": "묘", "vi-VN": "Mão"},
    "辰": {"en-US": "Chen", "ja-JP": "辰", "ko-KR": "진", "vi-VN": "Thìn"},
    "巳": {"en-US": "Si", "ja-JP": "巳", "ko-KR": "사", "vi-VN": "Tỵ"},
    "午": {"en-US": "Wu", "ja-JP": "午", "ko-KR": "오", "vi-VN": "Ngọ"},
    "未": {"en-US": "Wei", "ja-JP": "未", "ko-KR": "미", "vi-VN": "Mùi"},
    "申": {"en-US": "Shen", "ja-JP": "申", "ko-KR": "신", "vi-VN": "Thân"},
    "酉": {"en-US": "You", "ja-JP": "酉", "ko-KR": "유", "vi-VN": "Dậu"},
    "戌": {"en-US": "Xu", "ja-JP": "戌", "ko-KR": "술", "vi-VN": "Tuất"},
    "亥": {"en-US": "Hai", "ja-JP": "亥", "ko-KR": "해", "vi-VN": "Hợi"},
}

# ============================================================
# 接口标签翻译
# ============================================================

UI_LABELS: Dict[str, Dict[str, str]] = {
    "title": {
        "zh-CN": "一念紫微斗数", "zh-TW": "一念紫微斗數",
        "en-US": "Yinian ZWDS", "ja-JP": "一念紫微斗数",
        "ko-KR": "일념자미두수", "vi-VN": "Nhất Niệm Tử Vi Đẩu Số",
    },
    "four_pillars": {
        "zh-CN": "四柱", "zh-TW": "四柱",
        "en-US": "Four Pillars", "ja-JP": "四柱",
        "ko-KR": "사주", "vi-VN": "Tứ trụ",
    },
    "zodiac": {
        "zh-CN": "生肖", "zh-TW": "生肖",
        "en-US": "Zodiac", "ja-JP": "生肖",
        "ko-KR": "띠", "vi-VN": "Tuổi",
    },
    "five_elements": {
        "zh-CN": "五行局", "zh-TW": "五行局",
        "en-US": "Element Bureau", "ja-JP": "五行局",
        "ko-KR": "오행국", "vi-VN": "Cục ngũ hành",
    },
    "soul_palace": {
        "zh-CN": "命宫", "zh-TW": "命宮",
        "en-US": "Life Palace", "ja-JP": "命宮",
        "ko-KR": "명궁", "vi-VN": "Mệnh cung",
    },
    "body_palace": {
        "zh-CN": "身宫", "zh-TW": "身宮",
        "en-US": "Body Palace", "ja-JP": "身宮",
        "ko-KR": "신궁", "vi-VN": "Thân cung",
    },
    "mutagens": {
        "zh-CN": "生年四化", "zh-TW": "生年四化",
        "en-US": "Four Transformations", "ja-JP": "生年四化",
        "ko-KR": "사화", "vi-VN": "Tứ hóa",
    },
    "empty_palace": {
        "zh-CN": "空宫", "zh-TW": "空宮",
        "en-US": "Empty Palace", "ja-JP": "空宮",
        "ko-KR": "빈궁", "vi-VN": "Không cung",
    },
    "current_decadal": {
        "zh-CN": "当前大限", "zh-TW": "當前大限",
        "en-US": "Current Decade", "ja-JP": "現在の大限",
        "ko-KR": "현재 대한", "vi-VN": "Đại hạn hiện tại",
    },
    "reading_title": {
        "zh-CN": "AI深度解盘", "zh-TW": "AI深度解盤",
        "en-US": "AI Deep Reading", "ja-JP": "AI深層解釈",
        "ko-KR": "AI 심층 해석", "vi-VN": "Giải mã AI chuyên sâu",
    },
    "yearly_title": {
        "zh-CN": "流年运势", "zh-TW": "流年運勢",
        "en-US": "Yearly Forecast", "ja-JP": "今年の運勢",
        "ko-KR": "연운", "vi-VN": "Vận niên",
    },
    "monthly_title": {
        "zh-CN": "流月运势", "zh-TW": "流月運勢",
        "en-US": "Monthly Forecast", "ja-JP": "今月の運勢",
        "ko-KR": "월운", "vi-VN": "Vận nguyệt",
    },
    "disclaimer": {
        "zh-CN": "📜 文化参考，理性看待", "zh-TW": "📜 文化參考，理性看待",
        "en-US": "📜 For cultural reference only", "ja-JP": "📜 文化的参考として",
        "ko-KR": "📜 문화적 참고 자료입니다", "vi-VN": "📜 Tham khảo văn hóa",
    },
}


# ============================================================
# 翻译函数
# ============================================================

def t(key: str, lang: str = "zh-CN", fallback: str = "en-US") -> str:
    """获取指定语言文本，支持多级key"""
    lang = lang_code_validate(lang)
    
    # UI标签
    if key in UI_LABELS:
        return UI_LABELS[key].get(lang, UI_LABELS[key].get(fallback, key))
    
    # 宫位
    if key in PALACE_NAMES:
        return PALACE_NAMES[key].get(lang, PALACE_NAMES[key].get(fallback, key))
    
    # 四化
    if key in MUTAGEN_NAMES:
        return MUTAGEN_NAMES[key].get(lang, MUTAGEN_NAMES[key].get(fallback, key))
    
    # 亮度
    if key in BRIGHTNESS:
        return BRIGHTNESS[key].get(lang, BRIGHTNESS[key].get(fallback, key))
    
    # 主星
    if key in MAJOR_STARS:
        return MAJOR_STARS[key].get(lang, key)
    
    # 天干
    if key in HEAVENLY_STEMS:
        return HEAVENLY_STEMS[key].get(lang, key)
    
    # 地支
    if key in EARTHLY_BRANCHES:
        return EARTHLY_BRANCHES[key].get(lang, key)
    
    return key


def t_star(name: str, lang: str = "en-US") -> str:
    """星曜名称翻译"""
    return MAJOR_STARS.get(name, {}).get(lang, name)


def t_palace(name: str, lang: str = "en-US") -> str:
    """宫位名称翻译"""
    return PALACE_NAMES.get(name, {}).get(lang, name)


# ============================================================
# 辅助函数
# ============================================================

def format_birth_str(year_stem_branch: str, month_stem_branch: str, lang: str = "zh-CN") -> str:
    """格式化四柱"""
    if lang.startswith("en"):
        # 英文：直接显示拼音
        return f"{year_stem_branch} {month_stem_branch}"
    return f"{year_stem_branch} {month_stem_branch}"


def get_lang_direction(lang: str) -> str:
    """获取文本方向"""
    return "ltr" if lang.startswith("en") else "ltr"


if __name__ == "__main__":
    # 测试
    test_keys = ["命宫", "紫微", "禄", "庙", "甲", "title"]
    for key in test_keys:
        for lang in ["en-US", "ja-JP", "ko-KR", "vi-VN"]:
            val = t(key, lang)
            print(f"  {lang}: {key} → {val}")
        print()
