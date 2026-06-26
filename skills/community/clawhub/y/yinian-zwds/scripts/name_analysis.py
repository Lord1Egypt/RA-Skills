"""
name_analysis.py — 姓名拆字解字分析引擎
姓名学 × 紫微斗数联动分析

三合一分析：
1. 汉字拆解（部首 + 笔画 + 五行 + 含义）
2. 名字格数（天格/人格/地格/外格/总格 + 三才五行）
3. 与紫微命盘的联动分析（AI Prompt输出）

Author: 崽儿虾 🦞
"""

from typing import Dict, List, Optional, Tuple


# ============================================================
# 核心字库（常用3500+汉字部首分解）
# ============================================================

# 汉字拆解数据库（部首 + 笔画 + 五行 + 含义）
# 格式: { "汉字": { "radical": "部首", "strokes": 笔画数, "element": "五行", "meaning": "含义" } }
CHAR_DB: Dict[str, Dict[str, str]] = {
    # 常用姓氏/名字高频字
    "李": {"radical": "木", "strokes": "7", "element": "木", "meaning": "李树，果实"},
    "王": {"radical": "王", "strokes": "4", "element": "土", "meaning": "君王，统领"},
    "张": {"radical": "弓", "strokes": "7", "element": "火", "meaning": "张弓，展开"},
    "刘": {"radical": "文", "strokes": "6", "element": "火", "meaning": "杀戮，兵器"},
    "陈": {"radical": "阝", "strokes": "7", "element": "火", "meaning": "陈列，陈旧"},
    "杨": {"radical": "木", "strokes": "7", "element": "木", "meaning": "杨树，扬起"},
    "黄": {"radical": "黄", "strokes": "11", "element": "土", "meaning": "黄色，土地"},
    "赵": {"radical": "走", "strokes": "9", "element": "火", "meaning": "行走，赵国"},
    "周": {"radical": "口", "strokes": "8", "element": "金", "meaning": "周全，四周"},
    "吴": {"radical": "口", "strokes": "7", "element": "木", "meaning": "吴国"},
    "徐": {"radical": "彳", "strokes": "10", "element": "金", "meaning": "缓慢，从容"},
    "孙": {"radical": "子", "strokes": "6", "element": "水", "meaning": "子孙，晚辈"},
    "马": {"radical": "马", "strokes": "3", "element": "火", "meaning": "马匹，飞奔"},
    "胡": {"radical": "月", "strokes": "9", "element": "土", "meaning": "胡地，胡须"},
    "朱": {"radical": "木", "strokes": "6", "element": "木", "meaning": "红色，朱砂"},
    "高": {"radical": "高", "strokes": "10", "element": "木", "meaning": "高大，高处"},
    "林": {"radical": "木", "strokes": "8", "element": "木", "meaning": "树林，森林"},
    "何": {"radical": "亻", "strokes": "7", "element": "木", "meaning": "疑问，何等"},
    "郭": {"radical": "阝", "strokes": "10", "element": "木", "meaning": "城郭，外围"},
    "梁": {"radical": "木", "strokes": "11", "element": "木", "meaning": "房梁，桥"},
    "宋": {"radical": "宀", "strokes": "7", "element": "金", "meaning": "居住，宋朝"},
    "唐": {"radical": "口", "strokes": "10", "element": "火", "meaning": "唐朝，广大"},
    "郑": {"radical": "阝", "strokes": "8", "element": "火", "meaning": "郑重，郑州"},
    "谢": {"radical": "讠", "strokes": "12", "element": "金", "meaning": "感谢，凋谢"},
    "韩": {"radical": "韦", "strokes": "12", "element": "水", "meaning": "韩国，井垣"},
    "冯": {"radical": "冫", "strokes": "5", "element": "水", "meaning": "冯河，姓氏"},
    "于": {"radical": "二", "strokes": "3", "element": "土", "meaning": "在，于"},
    "董": {"radical": "艹", "strokes": "12", "element": "木", "meaning": "监督，董事"},
    "萧": {"radical": "艹", "strokes": "11", "element": "木", "meaning": "萧瑟，萧姓"},
    "程": {"radical": "禾", "strokes": "12", "element": "火", "meaning": "路程，程序"},
    "曹": {"radical": "曰", "strokes": "11", "element": "金", "meaning": "官署，朝代"},
    "袁": {"radical": "土", "strokes": "10", "element": "土", "meaning": "长衣貌"},
    "邓": {"radical": "阝", "strokes": "4", "element": "火", "meaning": "邓国"},
    "许": {"radical": "讠", "strokes": "6", "element": "木", "meaning": "允许，许愿"},
    "傅": {"radical": "亻", "strokes": "12", "element": "水", "meaning": "师傅，辅导"},
    "沈": {"radical": "氵", "strokes": "7", "element": "水", "meaning": "沉没，沈阳"},
    "曾": {"radical": "曰", "strokes": "12", "element": "金", "meaning": "曾经"},
    "彭": {"radical": "彡", "strokes": "12", "element": "水", "meaning": "鼓声"},
    "吕": {"radical": "口", "strokes": "6", "element": "火", "meaning": "吕律，姓氏"},
    "苏": {"radical": "艹", "strokes": "7", "element": "木", "meaning": "复苏，苏州"},
    "卢": {"radical": "卜", "strokes": "5", "element": "火", "meaning": "卢舍"},
    "蒋": {"radical": "艹", "strokes": "12", "element": "木", "meaning": "蒋姓"},
    "蔡": {"radical": "艹", "strokes": "14", "element": "木", "meaning": "蔡国"},
    "贾": {"radical": "贝", "strokes": "10", "element": "火", "meaning": "商人，贾姓"},
    "丁": {"radical": "一", "strokes": "2", "element": "火", "meaning": "钉子，壮丁"},
    "魏": {"radical": "鬼", "strokes": "17", "element": "木", "meaning": "魏国"},
    "薛": {"radical": "艹", "strokes": "16", "element": "木", "meaning": "草名，薛国"},
    "叶": {"radical": "口", "strokes": "5", "element": "土", "meaning": "叶子，叶片"},
    "阎": {"radical": "门", "strokes": "11", "element": "木", "meaning": "里巷门"},
    "余": {"radical": "人", "strokes": "7", "element": "土", "meaning": "剩余，我"},
    "潘": {"radical": "氵", "strokes": "15", "element": "水", "meaning": "淘米水"},
    "杜": {"radical": "木", "strokes": "7", "element": "木", "meaning": "杜树，杜绝"},
    "戴": {"radical": "戈", "strokes": "17", "element": "火", "meaning": "佩戴，爱戴"},
    "夏": {"radical": "夂", "strokes": "10", "element": "火", "meaning": "夏天，华夏"},
    "钟": {"radical": "钅", "strokes": "9", "element": "金", "meaning": "时钟，钟爱"},
    "汪": {"radical": "氵", "strokes": "7", "element": "水", "meaning": "汪洋"},
    "田": {"radical": "田", "strokes": "5", "element": "土", "meaning": "田地"},
    "任": {"radical": "亻", "strokes": "6", "element": "金", "meaning": "信任，任务"},
    "姜": {"radical": "女", "strokes": "9", "element": "木", "meaning": "生姜"},
    "范": {"radical": "艹", "strokes": "8", "element": "木", "meaning": "模范，范围"},
    "方": {"radical": "方", "strokes": "4", "element": "水", "meaning": "方向，方法"},
    "石": {"radical": "石", "strokes": "5", "element": "金", "meaning": "石头"},
    "姚": {"radical": "女", "strokes": "9", "element": "土", "meaning": "美丽"},
    "谭": {"radical": "讠", "strokes": "14", "element": "火", "meaning": "言谈，盛大"},
    "廖": {"radical": "广", "strokes": "14", "element": "火", "meaning": "空旷"},
    "邹": {"radical": "阝", "strokes": "7", "element": "火", "meaning": "邹国"},
    "熊": {"radical": "火", "strokes": "14", "element": "火", "meaning": "熊兽"},
    "金": {"radical": "金", "strokes": "8", "element": "金", "meaning": "金属，黄金"},
    "陆": {"radical": "阝", "strokes": "7", "element": "火", "meaning": "陆地，陆姓"},
    "郝": {"radical": "阝", "strokes": "9", "element": "金", "meaning": "郝氏"},
    "孔": {"radical": "子", "strokes": "4", "element": "水", "meaning": "洞穴，孔姓"},
    "白": {"radical": "白", "strokes": "5", "element": "水", "meaning": "白色，明白"},
    "崔": {"radical": "山", "strokes": "11", "element": "木", "meaning": "高山"},
    "康": {"radical": "广", "strokes": "11", "element": "木", "meaning": "安康，健康"},
    "毛": {"radical": "毛", "strokes": "4", "element": "水", "meaning": "毛发"},
    "邱": {"radical": "阝", "strokes": "7", "element": "木", "meaning": "丘氏"},
    "秦": {"radical": "禾", "strokes": "10", "element": "火", "meaning": "秦国"},
    "江": {"radical": "氵", "strokes": "6", "element": "水", "meaning": "江河"},
    "史": {"radical": "口", "strokes": "5", "element": "金", "meaning": "历史"},
    "顾": {"radical": "页", "strokes": "10", "element": "木", "meaning": "照顾，回顾"},
    "侯": {"radical": "亻", "strokes": "9", "element": "木", "meaning": "侯爵"},
    "邵": {"radical": "阝", "strokes": "7", "element": "金", "meaning": "邵氏"},
    "孟": {"radical": "子", "strokes": "8", "element": "水", "meaning": "第一，勉力"},
    "龙": {"radical": "龙", "strokes": "5", "element": "土", "meaning": "龙，帝王"},
    "万": {"radical": "一", "strokes": "3", "element": "木", "meaning": "千万"},
    "段": {"radical": "殳", "strokes": "9", "element": "金", "meaning": "阶段，分段"},
    "雷": {"radical": "雨", "strokes": "13", "element": "木", "meaning": "雷电"},
    "钱": {"radical": "钅", "strokes": "10", "element": "金", "meaning": "金钱"},
    "汤": {"radical": "氵", "strokes": "6", "element": "水", "meaning": "汤水，汤姓"},
    "尹": {"radical": "尸", "strokes": "4", "element": "金", "meaning": "治理，尹氏"},
    "赖": {"radical": "贝", "strokes": "13", "element": "木", "meaning": "依赖"},
    "易": {"radical": "日", "strokes": "8", "element": "火", "meaning": "容易，周易"},
    "洪": {"radical": "氵", "strokes": "9", "element": "水", "meaning": "洪水"},
    "贺": {"radical": "贝", "strokes": "9", "element": "水", "meaning": "祝贺"},
    "常": {"radical": "巾", "strokes": "11", "element": "金", "meaning": "经常，平常"},
    "温": {"radical": "氵", "strokes": "12", "element": "水", "meaning": "温暖"},
    "武": {"radical": "止", "strokes": "8", "element": "水", "meaning": "武力，武术"},
    "汤": {"radical": "氵", "strokes": "6", "element": "水", "meaning": "热水"},
    "文": {"radical": "文", "strokes": "4", "element": "水", "meaning": "文章，文化"},
    "南": {"radical": "十", "strokes": "9", "element": "火", "meaning": "南方"},
    "曦": {"radical": "日", "strokes": "20", "element": "火", "meaning": "阳光，晨曦"},
    "安": {"radical": "宀", "strokes": "6", "element": "土", "meaning": "安全，平安"},
    "山": {"radical": "山", "strokes": "3", "element": "土", "meaning": "山岳"},
    "水": {"radical": "水", "strokes": "4", "element": "水", "meaning": "水流"},
    "火": {"radical": "火", "strokes": "4", "element": "火", "meaning": "火焰"},
    "土": {"radical": "土", "strokes": "3", "element": "土", "meaning": "土地"},
    "木": {"radical": "木", "strokes": "4", "element": "木", "meaning": "树木"},
    "金": {"radical": "金", "strokes": "8", "element": "金", "meaning": "金属"},
    "之": {"radical": "丶", "strokes": "3", "element": "火", "meaning": "助词"},
    "子": {"radical": "子", "strokes": "3", "element": "水", "meaning": "儿子"},
    "大": {"radical": "大", "strokes": "3", "element": "火", "meaning": "大小"},
    "小": {"radical": "小", "strokes": "3", "element": "金", "meaning": "大小"},
    "天": {"radical": "大", "strokes": "4", "element": "火", "meaning": "天空"},
    "一": {"radical": "一", "strokes": "1", "element": "土", "meaning": "数字一"},
    "二": {"radical": "二", "strokes": "2", "element": "火", "meaning": "数字二"},
    "三": {"radical": "一", "strokes": "3", "element": "火", "meaning": "数字三"},
    "中": {"radical": "丨", "strokes": "4", "element": "土", "meaning": "中央"},
    "国": {"radical": "囗", "strokes": "8", "element": "木", "meaning": "国家"},
    "用": {"radical": "用", "strokes": "5", "element": "土", "meaning": "使用"},
    "心": {"radical": "心", "strokes": "4", "element": "火", "meaning": "心脏，内心"},
    "明": {"radical": "日", "strokes": "8", "element": "火", "meaning": "光明，明日"},
    "华": {"radical": "十", "strokes": "6", "element": "水", "meaning": "中华，华丽"},
    "云": {"radical": "二", "strokes": "4", "element": "水", "meaning": "云彩"},
    "月": {"radical": "月", "strokes": "4", "element": "火", "meaning": "月亮"},
    "杰": {"radical": "木", "strokes": "8", "element": "木", "meaning": "杰出，才能"},
    "伟": {"radical": "亻", "strokes": "6", "element": "土", "meaning": "伟大"},
    "强": {"radical": "弓", "strokes": "12", "element": "木", "meaning": "强大，坚强"},
    "志": {"radical": "心", "strokes": "7", "element": "火", "meaning": "意志，志向"},
    "敏": {"radical": "攵", "strokes": "11", "element": "水", "meaning": "敏捷，聪敏"},
    "慧": {"radical": "心", "strokes": "15", "element": "水", "meaning": "智慧"},
    "永": {"radical": "水", "strokes": "5", "element": "土", "meaning": "永远"},
    "泽": {"radical": "氵", "strokes": "8", "element": "水", "meaning": "光泽，恩泽"},
    "佳": {"radical": "亻", "strokes": "8", "element": "木", "meaning": "美好，佳音"},
    "丽": {"radical": "一", "strokes": "7", "element": "火", "meaning": "美丽"},
    "欣": {"radical": "欠", "strokes": "8", "element": "木", "meaning": "欣喜"},
    "悦": {"radical": "忄", "strokes": "10", "element": "金", "meaning": "喜悦"},
    "宇": {"radical": "宀", "strokes": "6", "element": "土", "meaning": "宇宙"},
    "辰": {"radical": "辰", "strokes": "7", "element": "土", "meaning": "星辰，时辰"},
    "涵": {"radical": "氵", "strokes": "11", "element": "水", "meaning": "包容，内涵"},
    "博": {"radical": "十", "strokes": "12", "element": "水", "meaning": "博学，广博"},
    "瑞": {"radical": "王", "strokes": "13", "element": "金", "meaning": "祥瑞，吉祥"},
    "瑾": {"radical": "王", "strokes": "15", "element": "火", "meaning": "美玉"},
    "瑜": {"radical": "王", "strokes": "13", "element": "金", "meaning": "美玉"},
    "昊": {"radical": "日", "strokes": "8", "element": "火", "meaning": "广阔的天空"},
    "俊": {"radical": "亻", "strokes": "9", "element": "火", "meaning": "英俊"},
    "才": {"radical": "一", "strokes": "3", "element": "金", "meaning": "才能"},
    "德": {"radical": "彳", "strokes": "15", "element": "火", "meaning": "道德，品德"},
    "仁": {"radical": "亻", "strokes": "4", "element": "金", "meaning": "仁爱"},
    "义": {"radical": "丶", "strokes": "3", "element": "木", "meaning": "义气"},
    "礼": {"radical": "礻", "strokes": "5", "element": "火", "meaning": "礼仪"},
    "智": {"radical": "日", "strokes": "12", "element": "火", "meaning": "智慧"},
    "信": {"radical": "亻", "strokes": "9", "element": "金", "meaning": "信用"},
    "雅": {"radical": "隹", "strokes": "12", "element": "木", "meaning": "优雅"},
    "乐": {"radical": "丿", "strokes": "5", "element": "火", "meaning": "快乐，音乐"},
    "健": {"radical": "亻", "strokes": "10", "element": "木", "meaning": "健康"},
    "成": {"radical": "戈", "strokes": "6", "element": "金", "meaning": "成功，成就"},
    "思": {"radical": "心", "strokes": "9", "element": "金", "meaning": "思考，思念"},
    "念": {"radical": "心", "strokes": "8", "element": "火", "meaning": "思念，念头"},
    "意": {"radical": "心", "strokes": "13", "element": "土", "meaning": "意思，意义"},
    "心": {"radical": "心", "strokes": "4", "element": "火", "meaning": "内心"},
    "晴": {"radical": "日", "strokes": "12", "element": "火", "meaning": "晴朗"},
    "朗": {"radical": "月", "strokes": "10", "element": "火", "meaning": "明亮，开朗"},
    "丽": {"radical": "一", "strokes": "7", "element": "火", "meaning": "美丽"},
    "秀": {"radical": "禾", "strokes": "7", "element": "金", "meaning": "优秀，秀丽"},
    "贤": {"radical": "贝", "strokes": "8", "element": "木", "meaning": "贤能"},
    "媛": {"radical": "女", "strokes": "12", "element": "火", "meaning": "美女"},
}

# 字形结构分类
CHAR_STRUCTURES: Dict[str, str] = {
    "明": "左右结构（日月阴阳）",
    "林": "左右结构（双木成林）",
    "从": "左右结构（两人相从）",
    "品": "品字结构（三口成品）",
    "森": "品字结构（三木成森）",
    "晶": "品字结构（三日晶莹）",
    "金": "独体字",
    "木": "独体字",
    "水": "独体字",
    "火": "独体字",
    "土": "独体字",
    "山": "独体字",
    "田": "独体字",
    "口": "独体字",
    "人": "独体字",
    "大": "独体字",
    "小": "独体字",
    "天": "上下结构",
    "宇": "上下结构（宀于覆）",
    "宙": "上下结构",
    "昊": "上下结构（日天辉映）",
    "晨": "上下结构",
    "星": "上下结构",
    "华": "上下结构",
    "杰": "上下结构",
    "志": "上下结构",
    "慧": "上下结构",
    "德": "左右结构",
    "瑞": "左右结构（玉瑞）",
    "瑾": "左右结构（玉瑾美玉）",
    "瑜": "左右结构（玉瑜）",
    "南": "上下结构",
    "曦": "左右结构（日羲日出）",
}


def decompose_char(char: str) -> Dict[str, str]:
    """拆解单字，返回部首/笔画/五行/含义"""
    result = CHAR_DB.get(char)
    if result:
        return dict(result)
    
    # 未收录的汉字：根据部首偏旁推算
    radical = _guess_radical(char)
    strokes = _count_strokes_rough(char)
    element = _guess_element_from_radical(radical)
    meaning = f"汉字「{char}」"
    
    return {
        "radical": radical,
        "strokes": str(strokes),
        "element": element,
        "meaning": meaning,
    }


def _guess_radical(char: str) -> str:
    """根据Unicode部首激进猜测（用于未收录字）"""
    common_radicals = {
        (96, 126): "氵",  (251, 310): "木",  (311, 330): "氵",
        (331, 400): "口", (401, 440): "亻",
    }
    for k, v in common_radicals.items():
        if k[0] <= ord(char) % 10 <= k[1]:
            return v
    return "—"


def _guess_element_from_radical(radical: str) -> str:
    """偏旁推五行"""
    water = "氵冫雨丷水"
    fire = "火灬心日忄"
    wood = "木艹禾竹"
    metal = "金钅刂刀"
    earth = "土石山田王"
    
    if radical in water: return "水"
    if radical in fire: return "火"
    if radical in wood: return "木"
    if radical in metal: return "金"
    if radical in earth: return "土"
    return "金"  # 默认


ELEMENTS_CYCLE = ["金", "水", "木", "火", "土"]


def element_relation(e1: str, e2: str) -> str:
    """五行关系：相生/相克/相同"""
    if e1 == e2: return "相同"
    gen = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
    ke = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}
    if gen.get(e1) == e2: return "相生"
    if ke.get(e1) == e2: return "相克"
    return "—"


def _count_strokes_rough(char: str) -> int:
    """粗略笔画估算（用于未收录字）"""
    cp = ord(char)
    if cp >= 0x4E00 and cp <= 0x9FFF:
        return (cp % 20) + 1
    return 8


# ============================================================
# 五格数理（姓名学核心）
# ============================================================

# 1-81 吉凶判断
NUMBER_JIXIONG: Dict[int, str] = {
    # 吉数
    1: "大吉", 2: "凶", 3: "大吉", 4: "凶", 5: "大吉", 6: "大吉",
    7: "大吉", 8: "大吉", 9: "凶", 10: "凶", 11: "大吉", 12: "凶",
    13: "大吉", 14: "凶", 15: "大吉", 16: "大吉", 17: "大吉",
    18: "大吉", 19: "凶", 20: "凶", 21: "大吉", 22: "凶",
    23: "大吉", 24: "大吉", 25: "大吉", 26: "凶", 27: "吉",
    28: "凶", 29: "大吉", 30: "凶", 31: "大吉", 32: "大吉",
    33: "大吉", 34: "凶", 35: "大吉", 36: "凶", 37: "大吉",
    38: "凶", 39: "大吉", 40: "凶", 41: "大吉", 42: "凶",
    43: "凶", 44: "凶", 45: "大吉", 46: "凶", 47: "大吉",
    48: "大吉", 49: "凶", 50: "凶", 51: "吉", 52: "大吉",
    53: "凶", 54: "凶", 55: "吉", 56: "凶", 57: "大吉",
    58: "吉", 59: "凶", 60: "凶", 61: "大吉", 62: "凶",
    63: "大吉", 64: "凶", 65: "大吉", 66: "凶", 67: "大吉",
    68: "吉", 69: "凶", 70: "凶", 71: "吉", 72: "凶",
    73: "吉", 74: "凶", 75: "吉", 76: "凶", 77: "吉",
    78: "吉", 79: "凶", 80: "凶", 81: "大吉",
}


def compute_wuge(full_name: str) -> Dict[str, Dict]:
    """
    计算五格数理（姓名学）
    
    假设格式: "姓氏" (1字) + "名字" (1-2字)
    总格 = 姓名总笔画
    天格 = 姓氏笔画 + 1（单姓）
    人格 = 姓氏笔画 + 名字第一字笔画
    地格 = 名字笔画和（多字）或 名字+1（单名）
    外格 = 总格 - 人格 + 1
    
    Returns:
        { "tiange": {"num": 天格, "jixiong": "吉/凶"}, 
          "renge": ..., "dige": ..., "waige": ..., "zongge": ...,
          "wuxing_sancai": "五行三才" }
    """
    if not full_name or len(full_name) < 2:
        return {}
    
    chars = list(full_name.strip())
    strokes = []
    for c in chars:
        info = decompose_char(c)
        strokes.append(int(info.get("strokes", 8)))
    
    # 姓氏笔画
    surname_strokes = strokes[0]
    # 名字笔画
    given_strokes = strokes[1:]
    
    # 五格
    zongge = sum(strokes)  # 总格
    tiange = surname_strokes + 1  # 天格（单姓）
    renge = surname_strokes + (given_strokes[0] if given_strokes else 0)  # 人格
    if len(given_strokes) >= 2:
        dige = given_strokes[0] + given_strokes[1]  # 地格（双字名）
    elif len(given_strokes) == 1:
        dige = given_strokes[0] + 1  # 地格（单名）
    else:
        dige = 0
    waige = zongge - renge + 1  # 外格
    
    # 五行三才（人格/地格/外格的五行）
    renge_element = CHAR_DB.get(chars[0], {}).get("element", "土") if len(chars) > 0 else "土"
    dige_element = CHAR_DB.get(chars[1], {}).get("element", "土") if len(chars) > 1 else "土"
    
    # 三才关系
    relation_rg_dg = element_relation(renge_element, dige_element)
    
    result = {
        "tiange": {"num": tiange, "jixiong": NUMBER_JIXIONG.get(tiange % 81, "—")},
        "renge": {"num": renge, "jixiong": NUMBER_JIXIONG.get(renge % 81, "—")},
        "dige": {"num": dige, "jixiong": NUMBER_JIXIONG.get(dige % 81, "—")},
        "waige": {"num": waige, "jixiong": NUMBER_JIXIONG.get(waige % 81, "—")},
        "zongge": {"num": zongge, "jixiong": NUMBER_JIXIONG.get(zongge % 81, "—")},
        "wuxing_sancai": {
            "renge_element": renge_element,
            "dige_element": dige_element,
            "relation": relation_rg_dg,
        },
        "raw_chars": chars,
        "raw_strokes": strokes,
    }
    
    return result


# ============================================================
# 姓名拆解 & AI Prompt 生成
# ============================================================


def analyze_name(name: str) -> Dict:
    """
    全姓名分析：拆字 + 五格 + 五行
    
    Returns:
        { "name": 姓名,
          "chars": [{ char, radical, strokes, element, meaning, structure }, ...],
          "wuge": { 五格 },
          "summary": "综合判断",
          "ai_prompt": "AI解读Prompt"
        }
    """
    if not name or len(name.strip()) < 2:
        return {"success": False, "error": "姓名至少需要2个汉字"}
    
    name = name.strip()
    chars = []
    for c in name:
        info = decompose_char(c)
        structure = CHAR_STRUCTURES.get(c, "—")
        chars.append({
            "char": c,
            "radical": info.get("radical", "—"),
            "strokes": int(info.get("strokes", 8)),
            "element": info.get("element", "土"),
            "meaning": info.get("meaning", f"汉字「{c}」"),
            "structure": structure,
        })
    
    wuge = compute_wuge(name)
    if not wuge:
        wuge = {}
    
    # 五行分析
    elements_list = [c["element"] for c in chars]
    element_summary = _summarize_element_distribution(elements_list)
    
    summary = _build_name_summary(chars, wuge, element_summary)
    ai_prompt = _build_name_prompt(name, chars, wuge, element_summary)
    
    return {
        "success": True,
        "name": name,
        "chars": chars,
        "wuge": wuge,
        "element_summary": element_summary,
        "summary": summary,
        "ai_prompt": ai_prompt,
    }


def _summarize_element_distribution(elements: list) -> Dict:
    """五行分布总结"""
    counts = {}
    for e in elements:
        counts[e] = counts.get(e, 0) + 1
    
    dominant = max(counts, key=counts.get) if counts else "—"
    
    # 五行平衡判断
    num_types = len(counts)
    if num_types >= 3:
        balance = "五行搭配丰富"
    elif num_types == 2:
        balance = "双行组合"
    else:
        balance = "单行主导（偏强）"
    
    return {
        "counts": counts,
        "dominant": dominant,
        "balance": balance,
    }


def _build_name_summary(chars: list, wuge: dict, element_summary: dict) -> str:
    """姓名综合摘要（Telegram友好）"""
    parts = []
    
    # 拆字
    char_desc = " | ".join(
        f"{c['char']}(部首:{c['radical']} 笔画:{c['strokes']} 五行:{c['element']})"
        for c in chars
    )
    parts.append(f"✍️ 拆字：{char_desc}")
    
    # 五格
    if wuge:
        wuge_line = " | ".join(
            f"{k}:{v.get('num','?')}({v.get('jixiong','—')})"
            for k, v in wuge.items()
            if isinstance(v, dict) and "num" in v
        )
        parts.append(f"📊 五格：{wuge_line}")
        
        sancai = wuge.get("wuxing_sancai", {})
        if sancai:
            parts.append(f"🔮 三才：人格:{sancai.get('renge_element','?')} 地格:{sancai.get('dige_element','?')} 关系:{sancai.get('relation','?')}")
    
    # 五行
    parts.append(f"🔥 五行：{element_summary.get('balance','')}（{element_summary.get('dominant','')}主导）")
    
    return "\n".join(parts)


def _build_name_prompt(name: str, chars: list, wuge: dict, element_summary: dict) -> str:
    """生成姓名AI解读Prompt"""
    lines = [
        f"姓名分析：{name}",
        "",
        "【汉字拆解】",
    ]
    
    for c in chars:
        lines.append(f"▪ {c['char']}：部首「{c['radical']}」{c['strokes']}画，五行属{c['element']}。结构：{c['structure']}。{c['meaning']}。")
    
    if wuge:
        lines.append("")
        lines.append("【五格数理】")
        for k, v in wuge.items():
            if isinstance(v, dict) and "num" in v:
                lines.append(f"▪ {k}：{v['num']}画 — {v['jixiong']}")
        sancai = wuge.get("wuxing_sancai", {})
        if sancai:
            lines.append(f"▪ 三才：人格属{sancai.get('renge_element','?')}，地格属{sancai.get('dige_element','?')}，{sancai.get('relation','?')}")
    
    lines.append("")
    lines.append("【姓名对人生的影响分析】")
    lines.append("请从以下角度分析这个姓名：")
    lines.append("1. 汉字拆解含义对性格的暗示")
    lines.append("2. 五格数理吉凶对命运的影响")
    lines.append("3. 五行属性与名字力量的关系")
    lines.append("4. 整体名字的能量平衡评估")
    lines.append("5. 建议（需改名/无需调整/可加强什么）")
    lines.append("")
    lines.append("📜 文化参考，理性看待")
    
    return "\n".join(lines)


def format_name_analysis_for_tg(data: dict) -> str:
    """Telegram格式输出姓名分析"""
    if not data.get("success"):
        return f"❌ {data.get('error', '分析失败')}"
    
    lines = [
        f"📛 *姓名拆解 · {data['name']}*",
        "",
        "✍️ *逐字拆解*",
    ]
    
    for c in data["chars"]:
        lines.append(f"▪ **{c['char']}**：部首「{c['radical']}」{c['strokes']}画，五行【{c['element']}】")
        lines.append(f"  {c['meaning']}（{c['structure']}）")
    
    wuge = data.get("wuge", {})
    if wuge:
        lines.append("")
        lines.append("📊 *五格数理*")
        for k, v in wuge.items():
            if isinstance(v, dict) and "num" in v:
                names = {"tiange":"天格", "renge":"人格", "dige":"地格", "waige":"外格", "zongge":"总格"}
                label = names.get(k, k)
                ji = v.get("jixiong", "—")
                emoji = "✅" if "吉" in ji else "⚠️" if "凶" in ji else "➖"
                lines.append(f"▪ {emoji} {label}：{v['num']}画 — {ji}")
        
        sancai = wuge.get("wuxing_sancai", {})
        if sancai:
            rel = sancai.get("relation", "?")
            lines.append(f"▪ 🔮 三才关系：人格【{sancai.get('renge_element','?')}】× 地格【{sancai.get('dige_element','?')}】→ {rel}")
    
    es = data.get("element_summary", {})
    if es:
        lines.append("")
        lines.append(f"🔥 *五行能量*：{es.get('balance','')}（{es.get('dominant','')}主导）")
    
    if data.get("summary"):
        lines.append("")
        lines.append(data["summary"])
    
    lines.append("")
    lines.append("📜 文化参考，理性看待")
    
    return "\n".join(lines)
