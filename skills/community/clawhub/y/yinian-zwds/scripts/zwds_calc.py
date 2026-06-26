"""
zwds_calc.py — 一念紫微斗数排盘核心引擎
基于 iztro-py v0.3.4

【关键修正 v2】
iztro 的 to_iztro_dict() 返回的 palaces 按地支固定顺序(寅→丑)排列，
并非紫微斗数标准宫序。
必须以 earthlyBranchOfSoulPalace 找到命宫位置，再重排为正确顺序。

紫微斗数标准宫序（命宫为第0宫，按宫位逆时针）：
  0 命宫 1 父母宫 2 福德宫 3 田宅宫
  4 官禄宫 5 交友宫 6 迁移宫 7 疾厄宫
  8 财帛宫 9 子女宫 10 夫妻宫 11 兄弟宫

Author: 崽儿虾 🦞
"""

from iztro_py import astro
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Tuple
import json
import re


# 地支 → 索引映射（寅=0, 卯=1, ..., 丑=11）
BRANCH_TO_INDEX = {
    "寅": 0, "卯": 1, "辰": 2, "巳": 3, "午": 4, "未": 5,
    "申": 6, "酉": 7, "戌": 8, "亥": 9, "子": 10, "丑": 11,
}

INDEX_TO_BRANCH = {v: k for k, v in BRANCH_TO_INDEX.items()}

# 紫微斗数标准宫序（按地支定宫）
# iztro的palaces[0]是寅宫(福德宫)，palaces[10]是子宫(命宫)
# 但宫名本身由iztro的name字段决定，不是由索引决定！

BRIGHTNESS_CN = {
    "miao": "庙", "wang": "旺", "de": "得",
    "li": "利", "xian": "陷", "ping": "平",
}

HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 紫微斗数宫位名（按命宫为0开始逆时针顺序）
ZWDS_PALACE_NAMES = [
    ("命宫", "Life"),
    ("父母宫", "Parents"),
    ("福德宫", "Spirit"),
    ("田宅宫", "Property"),
    ("官禄宫", "Career"),
    ("交友宫", "Friends"),
    ("迁移宫", "Travel"),
    ("疾厄宫", "Health"),
    ("财帛宫", "Wealth"),
    ("子女宫", "Children"),
    ("夫妻宫", "Marriage"),
    ("兄弟宫", "Siblings"),
]

# 命宫在iztro palaces中的固定索引（地支寅=0序，命宫地支=子=10）
# 命宫地支由 earthlyBranchOfSoulPalace 给出
# 但iztro的palace是固定地支排序，所以需要找到命宫在哪
# soul_branch = earthlyBranchOfSoulPalace 的映射值


@dataclass
class StarInfo:
    name: str = ""
    brightness: str = ""
    mutagen: str = ""
    is_major: bool = True


@dataclass
class PalaceInfo:
    index: int = -1
    name_cn: str = ""
    name_en: str = ""
    heavenly_stem: str = ""
    earthly_branch: str = ""
    major_stars: List[StarInfo] = field(default_factory=list)
    minor_stars: List[StarInfo] = field(default_factory=list)
    is_empty: bool = False


@dataclass
class AstrolabeResult:
    birth_date: str = ""
    birth_hour: int = 0
    gender: str = ""
    zodiac: str = ""
    five_elements_class: str = ""
    four_pillars_year: str = ""
    four_pillars_month: str = ""
    four_pillars_day: str = ""
    four_pillars_hour: str = ""
    soul_palace_branch: str = ""
    body_palace_branch: str = ""
    soul_index: int = -1
    body_index: int = -1
    palaces: List[PalaceInfo] = field(default_factory=list)
    mutagens: List[Dict[str, str]] = field(default_factory=list)


def safe_str(val) -> str:
    """安全转字符串"""
    if val is None:
        return ""
    if hasattr(val, 'value'):
        return val.value
    return str(val)


def _stem_value(stem) -> str:
    """天干枚举转中文"""
    s = safe_str(stem)
    for h in HEAVENLY_STEMS:
        if h in s or s.startswith(h):
            return h
    name_map = {
        "jia": "甲", "yi": "乙", "bing": "丙", "ding": "丁", "wu": "戊",
        "ji": "己", "geng": "庚", "xin": "辛", "ren": "壬", "gui": "癸",
        "jiaHeavenly": "甲", "yiHeavenly": "乙", "bingHeavenly": "丙", "dingHeavenly": "丁",
        "wuHeavenly": "戊", "jiHeavenly": "己", "gengHeavenly": "庚", "xinHeavenly": "辛",
        "renHeavenly": "壬", "guiHeavenly": "癸",
    }
    return name_map.get(s, s)


def _branch_value(branch) -> str:
    """地支枚举转中文"""
    s = safe_str(branch)
    for b in EARTHLY_BRANCHES:
        if b in s or s.startswith(b):
            return b
    name_map = {
        "zi": "子", "chou": "丑", "yin": "寅", "mao": "卯",
        "chen": "辰", "si": "巳", "wu": "午", "wei": "未",
        "shen": "申", "you": "酉", "xu": "戌", "hai": "亥",
        "ziEarthly": "子", "chouEarthly": "丑", "yinEarthly": "寅", "maoEarthly": "卯",
        "chenEarthly": "辰", "siEarthly": "巳", "wuEarthly": "午", "weiEarthly": "未",
        "shenEarthly": "申", "youEarthly": "酉", "xuEarthly": "戌", "haiEarthly": "亥",
    }
    return name_map.get(s, s)


def _branch_index(branch_str: str) -> int:
    """地支名称转索引（子=0, 丑=1, ..., 亥=11）"""
    b = _branch_value(branch_str)
    return EARTHLY_BRANCHES.index(b)


def _map_mutagen_name(stem: str) -> Tuple[str, str, str, str]:
    """
    生年天干四化
    返回: (禄星, 权星, 科星, 忌星)
    """
    table = {
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
    return table.get(stem, ("", "", "", ""))


def _find_star_in_palaces(
    star_name: str,
    iztro_palaces: List[dict],
) -> Optional[int]:
    """在iztro的palaces中查找某星曜所在的宫位索引"""
    for i, p in enumerate(iztro_palaces):
        major = p.get("majorStars", [])
        minor = p.get("minorStars", [])
        for s in major + minor:
            if safe_str(s.get("name", "")) == star_name:
                return i
    return None


def compute_surrounded(palace_index: int) -> List[int]:
    """
    三方四正
    
    Args:
        palace_index: 在紫微斗数标准宫序中的索引(0-11)
    
    返回: 包含本宫在内的三方四正索引列表
    """
    return sorted({
        palace_index,
        (palace_index + 6) % 12,  # 对宫
        (palace_index + 4) % 12,  # 三合左
        (palace_index + 8) % 12,  # 三合右
    })


def _get_palace_name_by_branch(
    earth_branch: str,
    iztro_palaces: List[dict],
) -> str:
    """根据地支找到iztro宫殿在命盘中的紫微名称"""
    for p in iztro_palaces:
        if safe_str(p.get("earthlyBranch", "")) == _branch_value(earth_branch):
            return safe_str(p.get("name", ""))
    return ""


def generate_astrolabe(
    date_str: str,
    hour: int,
    gender: str,
    is_lunar: bool = False,
    is_lunar_leap: bool = False,
    language: str = "zh-CN"
) -> Optional[AstrolabeResult]:
    """生成紫微斗数命盘"""
    try:
        if is_lunar:
            result = astro.by_lunar(date_str, hour, gender, is_lunar_leap, True, language)
        else:
            result = astro.by_solar(date_str, hour, gender, True, language)

        if not result:
            return None

        d = result.to_iztro_dict()
        if not d:
            return None

        # ====== 从iztro原始数据中提取基本信息 ======
        raw_palaces = d.get("palaces", [])
        if not raw_palaces:
            return None

        # 获取命宫/身宫的地支
        soul_branch_str = safe_str(d.get("earthlyBranchOfSoulPalace", ""))
        body_branch_str = safe_str(d.get("earthlyBranchOfBodyPalace", ""))

        soul_branch = _branch_value(soul_branch_str)
        body_branch = _branch_value(body_branch_str)

        # 地支映射索引
        earth_branch_to_index = {
            "子": 0, "丑": 1, "寅": 2, "卯": 3,
            "辰": 4, "巳": 5, "午": 6, "未": 7,
            "申": 8, "酉": 9, "戌": 10, "亥": 11,
        }

        # 地支寅→丑在iztro palaces中的索引
        ztro_branch_to_idx = BRANCH_TO_INDEX

        # 命宫在iztro原始palaces中的索引
        # soul_branch是地支名称，iztro palaces按寅→丑顺序
        raw_soul_idx = ztro_branch_to_idx.get(soul_branch, 0)
        raw_body_idx = ztro_branch_to_idx.get(body_branch, 0)

        # ====== 构建 AstrolabeResult ======
        r = AstrolabeResult(
            birth_date=date_str,
            birth_hour=hour,
            gender=gender,
            zodiac=safe_str(d.get("zodiac", "")),
            five_elements_class=safe_str(d.get("fiveElementsClass", "")),
            soul_palace_branch=soul_branch,
            body_palace_branch=body_branch,
        )

        # 四柱
        cdate = getattr(result, "raw_chinese_date", None)
        if cdate:
            r.four_pillars_year = _stem_value(getattr(cdate, 'year_stem', '')) + _branch_value(getattr(cdate, 'year_branch', ''))
            r.four_pillars_month = _stem_value(getattr(cdate, 'month_stem', '')) + _branch_value(getattr(cdate, 'month_branch', ''))
            r.four_pillars_day = _stem_value(getattr(cdate, 'day_stem', '')) + _branch_value(getattr(cdate, 'day_branch', ''))
            r.four_pillars_hour = _stem_value(getattr(cdate, 'time_stem', '')) + _branch_value(getattr(cdate, 'time_branch', ''))

        # ====== 生年四化 ======
        year_stem = r.four_pillars_year[0] if r.four_pillars_year else ""
        if year_stem:
            mutagen_stars = _map_mutagen_name(year_stem)
            mutagen_names = ["禄", "权", "科", "忌"]
            
            for i, star in enumerate(mutagen_stars):
                if not star:
                    continue
                # 找此星曜在哪个宫
                palace_idx = _find_star_in_palaces(star, raw_palaces)
                if palace_idx is not None:
                    # 把iztro索引转回地支，再映射到实际宫名
                    branch_at_idx = INDEX_TO_BRANCH[palace_idx]
                    palace_name = _get_palace_name_by_branch(branch_at_idx, raw_palaces)
                    r.mutagens.append({
                        "palace": palace_name,
                        "star": star,
                        "mutagen": mutagen_names[i],
                    })

        # ====== 解析宫位 ======
        # Iztro palaces按地支寅→丑固定顺序排列
        # 我们需要按紫微斗数标准序（命宫为0，逆时针）重排
        
        soul_branch_index = BRANCH_TO_INDEX.get(soul_branch, 0)
        
        # 紫微斗数标准宫序对应的iztro原始索引
        # 命宫(0) = iztro[soul_branch_index]
        # 父母宫(1) = iztro[(soul_branch_index - 1) % 12]  (逆时针)
        # 福德宫(2) = iztro[(soul_branch_index - 2) % 12]
        # ...
        
        r.soul_index = 0  # 第0宫是命宫
        r.body_index = (raw_body_idx - soul_branch_index) % 12  # 身宫在标准序中的索引
        
        for i in range(12):
            raw_idx = (soul_branch_index + i) % 12  # 逆时针循环（iztro顺时针排寅→丑，命宫到父母宫需要+1）
            raw = raw_palaces[raw_idx]
            
            cn_name, en_name = ZWDS_PALACE_NAMES[i]
            hs = safe_str(raw.get("heavenlyStem", ""))
            eb = safe_str(raw.get("earthlyBranch", ""))

            # 主星
            major_stars = []
            for s in raw.get("majorStars", []):
                star_info = StarInfo(
                    name=safe_str(s.get("name", "")),
                    brightness=safe_str(s.get("brightness", "")),
                    mutagen=safe_str(s.get("mutagen", "")),
                    is_major=True,
                )
                major_stars.append(star_info)

            # 辅星
            minor_stars = []
            for s in raw.get("minorStars", []):
                star_info = StarInfo(
                    name=safe_str(s.get("name", "")),
                    mutagen=safe_str(s.get("mutagen", "")),
                    is_major=False,
                )
                minor_stars.append(star_info)
                
            # 亮度映射中文
            for s in major_stars:
                s.brightness = BRIGHTNESS_CN.get(s.brightness, s.brightness)

            # 四化标注
            # 生年四化的星曜对应四化
            for m in r.mutagens:
                for s in major_stars + minor_stars:
                    if s.name == m["star"]:
                        if not s.mutagen:
                            s.mutagen = m["mutagen"]

            is_empty = len(major_stars) == 0

            palace = PalaceInfo(
                index=i,
                name_cn=cn_name,
                name_en=en_name,
                heavenly_stem=hs,
                earthly_branch=eb,
                major_stars=major_stars,
                minor_stars=minor_stars,
                is_empty=is_empty,
            )
            r.palaces.append(palace)

        return r

    except Exception as e:
        import traceback
        print(f"[zwds_calc] 排盘异常: {e}")
        traceback.print_exc()
        return None


def astrolabe_to_json(astro_result: AstrolabeResult) -> Dict[str, Any]:
    """将 AstrolabeResult 转为 JSON 字典"""
    if not astro_result:
        return {}

    return {
        "birth": {
            "date": astro_result.birth_date,
            "hour": astro_result.birth_hour,
            "gender": astro_result.gender,
        },
        "four_pillars": {
            "year": astro_result.four_pillars_year,
            "month": astro_result.four_pillars_month,
            "day": astro_result.four_pillars_day,
            "hour": astro_result.four_pillars_hour,
        },
        "zodiac": astro_result.zodiac,
        "five_elements": astro_result.five_elements_class,
        "mutagens": astro_result.mutagens,
        "soul_index": astro_result.soul_index,
        "body_index": astro_result.body_index,
        "palaces": [
            {
                "index": p.index,
                "name_cn": p.name_cn,
                "name_en": p.name_en,
                "heavenly_stem": p.heavenly_stem,
                "earthly_branch": p.earthly_branch,
                "is_empty": p.is_empty,
                "major_stars": [
                    {
                        "name": s.name,
                        "brightness": s.brightness,
                        "mutagen": s.mutagen,
                    }
                    for s in p.major_stars
                ],
                "minor_stars": [
                    {
                        "name": s.name,
                        "mutagen": s.mutagen,
                    }
                    for s in p.minor_stars
                ],
            }
            for p in astro_result.palaces
        ],
    }


def format_astrolabe(astro_result: AstrolabeResult) -> str:
    """格式化命盘为可读文本"""
    if not astro_result:
        return "排盘失败"

    lines = []
    lines.append("━━━ 🔮 一念紫微斗数 · 命盘 ━━━")
    lines.append(f"四柱: {astro_result.four_pillars_year} {astro_result.four_pillars_month} {astro_result.four_pillars_day} {astro_result.four_pillars_hour}")
    
    lines.append(f"生肖: {astro_result.zodiac}　　五行局: {astro_result.five_elements_class}")

    soul_name = astro_result.palaces[astro_result.soul_index].name_cn if astro_result.palaces else ""
    body_name = astro_result.palaces[astro_result.body_index].name_cn if astro_result.palaces else ""
    soul_eb = astro_result.palaces[astro_result.soul_index].earthly_branch if astro_result.palaces else ""
    body_eb = astro_result.palaces[astro_result.body_index].earthly_branch if astro_result.palaces else ""
    soul_hs = astro_result.palaces[astro_result.soul_index].heavenly_stem if astro_result.palaces else ""
    body_hs = astro_result.palaces[astro_result.body_index].heavenly_stem if astro_result.palaces else ""
    
    lines.append(f"🏠 命宫: {soul_name}({soul_hs}{soul_eb})")
    lines.append(f"🏠 身宫: {body_name}({body_hs}{body_eb})")
    lines.append("")

    # 四化
    if astro_result.mutagens:
        lines.append("【生年四化】")
        for m in astro_result.mutagens:
            lines.append(f"  {m['palace']}: {m['star']}化{m['mutagen']}")
        lines.append("")

    # 十二宫
    lines.append("【十二宫】")
    for p in astro_result.palaces:
        major = " ".join(
            f"{s.name}({s.brightness})" + (f"→{s.mutagen}" if s.mutagen else "")
            for s in p.major_stars
        )
        minor = " ".join(s.name for s in p.minor_stars)
        empty = "【空宫】" if p.is_empty else ""

        parts = [f"  {p.name_cn} ({p.heavenly_stem}{p.earthly_branch})", ":"]
        parts.extend([f" {major}" if major else f" {empty}"])
        if minor:
            parts.append(f" 〔{minor}〕")
        lines.append("".join(parts))

    # 三方四正
    sur = compute_surrounded(astro_result.soul_index)
    sur_names = [astro_result.palaces[i].name_cn for i in sur]
    lines.append("")
    lines.append("【命宫三方四正】")
    lines.append(f"  {' · '.join(sur_names)}")

    lines.append("")
    lines.append("━ 文化参考，理性看待 ━")

    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    
    # CLI使用
    if len(sys.argv) > 1:
        # 从参数读取
        date_str = sys.argv[sys.argv.index("--date") + 1] if "--date" in sys.argv else "2000-1-1"
        hour = int(sys.argv[sys.argv.index("--hour") + 1]) if "--hour" in sys.argv else 0
        gender = sys.argv[sys.argv.index("--gender") + 1] if "--gender" in sys.argv else "男"
        is_lunar = "--lunar" in sys.argv
    else:
        date_str = "1984-6-22"
        hour = 6
        gender = "男"
        is_lunar = False
    
    r = generate_astrolabe(date_str, hour, gender, is_lunar)
    if r:
        print(format_astrolabe(r))
        print("\n--- JSON ---")
        import json
        print(json.dumps(astrolabe_to_json(r), ensure_ascii=False, indent=2))
    else:
        print("排盘失败")
