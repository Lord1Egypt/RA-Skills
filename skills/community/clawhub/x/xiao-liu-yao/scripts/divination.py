#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小六爻（道家小六壬）测算核心脚本
基于邵一尘前辈道家小六壬体系
包含：三步推算 + 体用生克 + 六道 + 藏干 + 数字特性 + 六煞十二宫
"""

import json
import sys
from datetime import datetime
import zhdate


# ============================================================
# 基础数据
# ============================================================

# 六宫名称
PALACES = ["大安", "留连", "速喜", "赤口", "小吉", "空亡"]

# 时辰对应表
SHICHEN = {
    1: ("子时", "23:00-00:59"),
    2: ("丑时", "01:00-02:59"),
    3: ("寅时", "03:00-04:59"),
    4: ("卯时", "05:00-06:59"),
    5: ("辰时", "07:00-08:59"),
    6: ("巳时", "09:00-10:59"),
    7: ("午时", "11:00-12:59"),
    8: ("未时", "13:00-14:59"),
    9: ("申时", "15:00-16:59"),
    10: ("酉时", "17:00-18:59"),
    11: ("戌时", "19:00-20:59"),
    12: ("亥时", "21:00-22:59"),
}


def get_shichen(hour):
    """根据小时获取时辰编号和名称"""
    if 23 <= hour or hour < 1:
        return 1, "子时", "23:00-00:59"
    elif 1 <= hour < 3:
        return 2, "丑时", "01:00-02:59"
    elif 3 <= hour < 5:
        return 3, "寅时", "03:00-04:59"
    elif 5 <= hour < 7:
        return 4, "卯时", "05:00-06:59"
    elif 7 <= hour < 9:
        return 5, "辰时", "07:00-08:59"
    elif 9 <= hour < 11:
        return 6, "巳时", "09:00-10:59"
    elif 11 <= hour < 13:
        return 7, "午时", "11:00-12:59"
    elif 13 <= hour < 15:
        return 8, "未时", "13:00-14:59"
    elif 15 <= hour < 17:
        return 9, "申时", "15:00-16:59"
    elif 17 <= hour < 19:
        return 10, "酉时", "17:00-18:59"
    elif 19 <= hour < 21:
        return 11, "戌时", "19:00-20:59"
    else:
        return 12, "亥时", "21:00-22:59"


# ============================================================
# 六宫详细属性
# ============================================================

PALACE_DETAIL = {
    "大安": {
        "ji_xiong": "大吉",
        "wu_xing": "木",
        "direction": "东方",
        "color": "青色/绿色",
        "divine_beast": "青龙",
        "liu_dao": "人道",
        "liu_dao_palace": "天权",
        "liu_dao_secondary": "修罗道·天艺",
        "dong_gong": "事业宫",
        "jing_gong": "命宫",
        "cang_gan": "甲(藏丁)",
        "zhi": "寅卯",
        "season": "春季（寅卯辰月）",
        "numbers": [1, 4, 5],
        "numbers_hidden": [7, 13],
        "number_hint": "一、四、五（藏七）",
        "summary": "身不动时，安宁稳定，谋事可成",
        "kou_jue": "大安事事昌，求财在坤方。失物去不远，宅舍保安康。行人身未动，病者主无妨。将军回田野，仔细更推详。",
        "personality_good": "俊秀洒脱，正直大方，仁慈善良，利官近贵",
        "personality_bad": "缺乏主动，懒惰固执，不善变通",
        "lei_xiang": [
            "为事业宫、命宫",
            "主木：竹、树木、花卉、木质物、家具",
            "为震巽：肝胆、四肢、左腿",
            "为风雷：阴天、风和日丽",
            "为家宅：卧室、床、疗养",
            "为尊贵：婚姻合美、关系融洽",
            "为青龙：文凭、文书、财帛、贵人、官贵",
            "为卧龙：铁路、火车",
        ],
    },
    "留连": {
        "ji_xiong": "小凶",
        "wu_xing": "土",
        "direction": "四方·东南/西北/西南/东北",
        "color": "黄黑色",
        "divine_beast": "腾蛇",
        "liu_dao": "修罗道",
        "liu_dao_palace": "天奸",
        "liu_dao_secondary": "佛道·天福",
        "dong_gong": "田宅宫",
        "jing_gong": "奴仆宫",
        "cang_gan": "己(藏丁)",
        "zhi": "辰戌丑未",
        "season": "春夏之交/长夏（辰巳月）",
        "numbers": [2, 7, 8],
        "numbers_hidden": [8, 14],
        "number_hint": "二、七、八（藏八）",
        "summary": "卒未归时，拖延缠绵，事有阻隔",
        "kou_jue": "留连事难成，求谋日未明。官事只宜缓，去者未回程。失物南方见，急讨方心称。更须防口舌，人口且平平。",
        "personality_good": "为人精明，小心谨慎，做事稳重，多愁善感",
        "personality_bad": "优柔寡断，缺少主见，为人多疑，虚言善妒",
        "lei_xiang": [
            "为田宅宫、奴仆宫",
            "主土：田园、沟渠、沼泽地、阴地",
            "为坤艮：脾胃、左臂、思绪",
            "为阴雨天、大雾",
            "为小人、阴人、阴私之事",
            "为慢性病、久病、虚病、邪病",
            "主财帛、钱财",
            "为腾蛇：拖延、凝滞、阻力、陈旧、熟人旧事",
        ],
    },
    "速喜": {
        "ji_xiong": "中吉",
        "wu_xing": "火",
        "direction": "南方",
        "color": "红色",
        "divine_beast": "朱雀",
        "liu_dao": "佛道",
        "liu_dao_palace": "天贵",
        "liu_dao_secondary": "畜生道·天破",
        "dong_gong": "感情宫",
        "jing_gong": "婚姻宫/夫妻宫",
        "cang_gan": "丙(藏辛)",
        "zhi": "巳午",
        "season": "夏季（巳午未月）",
        "numbers": [3, 6, 9],
        "numbers_hidden": [9, 15],
        "number_hint": "三、六、九（藏九）",
        "summary": "人即至时，快速喜庆，时机已到",
        "kou_jue": "速喜喜来临，求财向南行。失物申未午，逢人路上寻。官事有福德，病者无祸侵。田宅六畜吉，行人有信音。",
        "personality_good": "心直口快，能言善变，热情大方，敬老谦让",
        "personality_bad": "性情急燥，喜怒无常，易说是非，奢侈浪费",
        "lei_xiang": [
            "为感情宫、婚姻宫",
            "主火：日、烟火、炉灶、燥物",
            "为离：目、脑、心血、中女",
            "为艳阳天、晴天",
            "主礼：有礼节人、贵人、文书、喜讯、喜鹊",
            "为朱雀：口舌、官司、诉讼、信件、信息",
            "为文化之人",
            "为顺产，病为心脑血管",
        ],
    },
    "赤口": {
        "ji_xiong": "中凶",
        "wu_xing": "金",
        "direction": "西方",
        "color": "银白色",
        "divine_beast": "白虎",
        "liu_dao": "畜生道",
        "liu_dao_palace": "天刃",
        "liu_dao_secondary": "仙道·天寿",
        "dong_gong": "疾厄宫",
        "jing_gong": "兄弟宫",
        "cang_gan": "庚(藏癸)",
        "zhi": "申酉",
        "season": "秋季（申酉戌月）",
        "numbers": [4, 1, 2],
        "numbers_hidden": [10, 16],
        "number_hint": "四、一、二（藏十）",
        "summary": "官事凶时，口舌是非，官讼宜防",
        "kou_jue": "赤口主口舌，官非切宜防。失物速速讨，行人有惊慌。六畜多作怪，病者出西方。更须防咀咒，诚恐染瘟皇。",
        "personality_good": "性格刚强，行事果断，豪爽义气，疾恶如仇",
        "personality_bad": "争强好胜，冒失冲动，专横霸道，常生不平",
        "lei_xiang": [
            "为疾厄宫、兄弟宫",
            "主金：刀、剑、金属物、有口器皿",
            "为兑：少女、喜悦、口、肺、右臂",
            "为官司、伤灾、手术、牙医、损伤",
            "为猛禽、虎狼",
            "春夏为雷雨，秋为霜雹，冬为雪冰",
            "为白虎：凶灾、伤病、横祸、孝服、丧事",
            "为军警、政法之人",
        ],
    },
    "小吉": {
        "ji_xiong": "小吉",
        "wu_xing": "水",
        "direction": "北方",
        "color": "黑色",
        "divine_beast": "六合/玄武",
        "liu_dao": "仙道",
        "liu_dao_palace": "天文",
        "liu_dao_secondary": "鬼道·天驿",
        "dong_gong": "驿马宫/迁移宫",
        "jing_gong": "子女宫",
        "cang_gan": "壬(藏甲)",
        "zhi": "亥子",
        "season": "冬季（亥子丑月）",
        "numbers": [5, 3, 8],
        "numbers_hidden": [11, 17],
        "number_hint": "五、三、八（藏十一）",
        "summary": "人来喜时，小利吉庆，贵人助力",
        "kou_jue": "小吉最吉昌，路上好商量。阴人来报喜，失物在坤方。行人即便至，交关甚是强。凡事皆和合，病者叩穷苍。",
        "personality_good": "聪明伶俐，学识过人，人脉广泛，适应力强",
        "personality_bad": "随心所欲，风流浪漫，投机取巧，为人圆滑",
        "lei_xiang": [
            "为驿马宫/迁移宫、子女宫",
            "主水：小溪、流水、水中物",
            "为坎：肾、生殖器、右腿",
            "主智慧、知识",
            "为出行、行走、水路、旅游、奔波",
            "主桃花、色情、浪漫",
            "为建造、拆迁",
            "为玄武：暗昧不明、隐私、盗窃、小人",
        ],
    },
    "空亡": {
        "ji_xiong": "大凶",
        "wu_xing": "土",
        "direction": "中央",
        "color": "黄色",
        "divine_beast": "勾陈",
        "liu_dao": "鬼道",
        "liu_dao_palace": "天厄",
        "liu_dao_secondary": "人道·天孤",
        "dong_gong": "福德宫",
        "jing_gong": "父母宫",
        "cang_gan": "戊(藏乙)",
        "zhi": "辰戌",
        "season": "冬春之交（丑寅月）",
        "numbers": [6, 5, 10],
        "numbers_hidden": [12, 18],
        "number_hint": "六、五、十（藏十二）",
        "summary": "音信稀时，落空无成，谋事不祥",
        "kou_jue": "空亡事不祥，阴人多乖张。求财无利益，行人有灾殃。失物寻不见，官事有刑伤。病人逢暗鬼，解禳保安康。",
        "personality_good": "诚实守信，心胸宽广，温厚善良，尊师敬老",
        "personality_bad": "性格孤僻，脾气倔强，缺少变通，作事迟钝",
        "lei_xiang": [
            "为福德宫、父母宫",
            "主土：中心、空室、牢房、墓穴、旷野、盆地",
            "土中物、田土损失",
            "为音信渺茫、虚伪、妄想、遗忘",
            "为落空、死亡、精神病",
            "为阴天、多云",
            "为勾陈：虚惊怪异之事、鬼神仙妖",
            "为医巫卜相、僧道、孤寡人",
        ],
    },
}

# 体用五行生克
WU_XING_SK = {
    ("木", "土"): "体克用·小吉",
    ("木", "金"): "用克体·大凶",
    ("木", "水"): "用生体·大吉",
    ("木", "火"): "体生用·小凶",
    ("木", "木"): "体用比助·吉",
    ("火", "金"): "体克用·小吉",
    ("火", "水"): "用克体·大凶",
    ("火", "木"): "用生体·大吉",
    ("火", "土"): "体生用·小凶",
    ("火", "火"): "体用比助·吉",
    ("土", "水"): "体克用·小吉",
    ("土", "木"): "用克体·大凶",
    ("土", "火"): "用生体·大吉",
    ("土", "金"): "体生用·小凶",
    ("土", "土"): "体用比助·吉",
    ("金", "木"): "体克用·小吉",
    ("金", "火"): "用克体·大凶",
    ("金", "土"): "用生体·大吉",
    ("金", "水"): "体生用·小凶",
    ("金", "金"): "体用比助·吉",
    ("水", "火"): "体克用·小吉",
    ("水", "土"): "用克体·大凶",
    ("水", "金"): "用生体·大吉",
    ("水", "木"): "体生用·小凶",
    ("水", "水"): "体用比助·吉",
}

# 时辰五行
SHICHEN_WX = {
    1: "水", 2: "土", 3: "木", 4: "木",
    5: "土", 6: "火", 7: "火", 8: "土",
    9: "金", 10: "金", 11: "土", 12: "水",
}

# 分场景解读
SCENE_READINGS = {
    "求财": {
        "大安": "稳得，宜长线投资，财源稳定",
        "留连": "慢成，需耐心等待，不可急躁",
        "速喜": "立得，短线有利，快速见效",
        "赤口": "破财，防诈骗，有纠纷",
        "小吉": "小财，意外之喜，贵人助财",
        "空亡": "落空，血本无归，求财无利",
    },
    "求职": {
        "大安": "稳录，适合长期岗位",
        "留连": "等待通知，流程冗长",
        "速喜": "当场或快速出结果",
        "赤口": "有竞争，易被挑剔",
        "小吉": "有惊无险，顺利通过",
        "空亡": "无果，简历石沉大海",
    },
    "感情": {
        "大安": "稳定长久，平淡真实",
        "留连": "纠缠不清，复合有望",
        "速喜": "速成，一见钟情",
        "赤口": "争吵分手，防第三者",
        "小吉": "小甜蜜，有贵人撮合",
        "空亡": "无缘，单相思",
    },
    "出行": {
        "大安": "平安顺利，无延误",
        "留连": "延误，改期更佳",
        "速喜": "顺利快捷，当日可成",
        "赤口": "有阻碍，防意外",
        "小吉": "顺利，有小惊喜",
        "空亡": "取消，白跑一趟",
    },
    "健康": {
        "大安": "无大碍，康复慢",
        "留连": "缠绵难愈，需调理",
        "速喜": "速愈，无需担心",
        "赤口": "突发急症，防刀伤",
        "小吉": "小恙，无大碍",
        "空亡": "虚惊一场，无实病",
    },
    "失物": {
        "大安": "在原处，东北方",
        "留连": "未远走，被人留置",
        "速喜": "快速找回，南方",
        "赤口": "被人拿走，西方",
        "小吉": "有线索，能找回",
        "空亡": "难找回，信息缺失",
    },
    "事业": {
        "大安": "职位稳固，稳步发展",
        "留连": "进展缓慢，宜守不宜攻",
        "速喜": "有升迁喜讯，快速变动",
        "赤口": "口舌是非，防小人暗算",
        "小吉": "贵人相助，有惊无险",
        "空亡": "落空，计划难成",
    },
    "考试": {
        "大安": "发挥稳定，成绩尚可",
        "留连": "需加倍努力，进度慢",
        "速喜": "顺利通过，惊喜成绩",
        "赤口": "竞争激烈，谨防差错",
        "小吉": "有贵人相助，顺利",
        "空亡": "发挥不佳，希望落空",
    },
}

# 体用解读
TI_YONG_READINGS = {
    "体克用·小吉": "自身主动努力可成，需付出方能改变局面",
    "体生用·小凶": "付出多而得少，费心费力难得其报",
    "用克体·大凶": "外有阻力，诸事难成，宜退守",
    "用生体·大吉": "外力相助，他方赐福，诸事当成",
    "体用比助·吉": "两相互助，合作相宜，协力共进",
    "体用比劫·凶": "竞力相争，互损互缺，内耗严重",
}


# ============================================================
# 核心算法
# ============================================================

def calculate(dt: datetime):
    """核心推算"""
    # 1. 公历信息
    solar_time = dt.strftime("%Y-%m-%d %H:%M:%S")

    # 2. 农历转换
    zhd = zhdate.ZhDate.from_datetime(dt)
    lunar_year = zhd.lunar_year
    lunar_month = zhd.lunar_month
    lunar_day = zhd.lunar_day
    # 从 chinese() 输出中提取干支年，如 "二零二六年六月初四 丙午年 (马年)"
    chinese_str = zhd.chinese()
    ganzhi_year = chinese_str.split(" ")[1].split("年")[0] if " " in chinese_str else "未知"

    # 3. 时辰
    hour = dt.hour
    shichen_num, shichen_name, shichen_range = get_shichen(hour)

    # 4. 三步推算
    # 月落 = (月数 - 1) % 6
    month_idx = (lunar_month - 1) % 6
    month_palace = PALACES[month_idx]

    # 日落 = (月落 + 日数 - 1) % 6
    day_idx = (month_idx + lunar_day - 1) % 6
    day_palace = PALACES[day_idx]

    # 时落 = (日落 + 时数 - 1) % 6
    hour_idx = (day_idx + shichen_num - 1) % 6
    hour_palace = PALACES[hour_idx]

    # 5. 三盘（天盘=月落, 地盘=日落, 人盘=时落）
    tian_pan = month_palace
    di_pan = day_palace
    ren_pan = hour_palace

    # 6. 体用关系
    ti_wx = PALACE_DETAIL[hour_palace]["wu_xing"]
    yong_wx = SHICHEN_WX[shichen_num]

    ti_yong_key = None
    if ti_wx == yong_wx:
        # 同五行，分比助/比劫
        if ti_wx == "木":
            if lunar_month % 2 == 1:
                ti_yong_key = "体用比助·吉"
            else:
                ti_yong_key = "体用比劫·凶"
        else:
            ti_yong_key = "体用比助·吉"
    else:
        ti_yong_key = WU_XING_SK.get((ti_wx, yong_wx))

    ti_yong_result = {
        "ti_wu_xing": ti_wx,
        "yong_wu_xing": yong_wx,
        "relation": ti_yong_key or "无",
        "reading": TI_YONG_READINGS.get(ti_yong_key or "", ""),
    }

    # 7. 构造结果
    detail = PALACE_DETAIL.get(hour_palace, {})
    result = {
        "solar_time": solar_time,
        "lunar": {
            "year": lunar_year,
            "ganzhi_year": ganzhi_year,
            "month": lunar_month,
            "day": lunar_day,
            "shichen_num": shichen_num,
            "shichen_name": shichen_name,
            "shichen_range": shichen_range,
        },
        "calc_steps": {
            "step1_month": f"从大安起正月，顺数 {lunar_month} 位 → {month_palace}",
            "step2_day": f"从 {month_palace} 起初一，顺数 {lunar_day} 位 → {day_palace}",
            "step3_hour": f"从 {day_palace} 起子时，顺数 {shichen_num} 位（{shichen_name}） → {hour_palace}",
        },
        "san_pan": {
            "tian_pan": tian_pan,
            "tian_pan_meaning": "起因/天时/过去",
            "di_pan": di_pan,
            "di_pan_meaning": "经过/地利/发展",
            "ren_pan": ren_pan,
            "ren_pan_meaning": "结果/人和/当下",
        },
        "ti_yong": ti_yong_result,
        "result": {
            "palace": hour_palace,
            "ji_xiong": detail["ji_xiong"],
            "wu_xing": detail["wu_xing"],
            "direction": detail["direction"],
            "color": detail["color"],
            "divine_beast": detail["divine_beast"],
            "cang_gan": detail["cang_gan"],
            "season": detail["season"],
            "zhi": detail["zhi"],
            "liu_dao": detail["liu_dao"],
            "liu_dao_palace": detail["liu_dao_palace"],
            "liu_dao_secondary": detail["liu_dao_secondary"],
            "dong_gong": detail["dong_gong"],
            "jing_gong": detail["jing_gong"],
            "numbers": detail["numbers"],
            "numbers_hidden": detail["numbers_hidden"],
            "number_hint": detail["number_hint"],
            "summary": detail["summary"],
            "kou_jue": detail["kou_jue"],
            "personality_good": detail["personality_good"],
            "personality_bad": detail["personality_bad"],
            "lei_xiang": detail["lei_xiang"],
        },
        "scene_readings": SCENE_READINGS,
    }

    # 8. 应期推断
    result["ying_qi"] = calculate_yingqi(hour_palace, detail)

    # 9. 三宫具象
    result["san_gong_ju_xiang"] = calculate_sangong_juxiang(tian_pan, di_pan, ren_pan)

    # 10. 六亲推算
    result["liu_qin"] = calculate_liuqin(hour_palace, detail)

    return result


# ============================================================
# 高级分析
# ============================================================

def calculate_yingqi(palace, detail):
    """应期推断"""
    season_map = {
        "大安": "春季（寅卯辰月 / 2-4月）",
        "留连": "长夏/春夏之交（辰巳月 / 4-6月）",
        "速喜": "夏季（巳午未月 / 5-8月）",
        "赤口": "秋季（申酉戌月 / 8-11月）",
        "小吉": "冬季（亥子丑月 / 11-2月）",
        "空亡": "冬春之交（丑寅月 / 1-3月）",
    }
    nums = detail["numbers"]
    hidden = detail["numbers_hidden"]
    return {
        "season": season_map.get(palace, ""),
        "days_weeks": f"{nums[0]}/{hidden[0] if hidden else 'N/A'} 天/周",
        "months": f"{nums[1] if len(nums) > 1 else nums[0]}/{nums[2] if len(nums) > 2 else 'N/A'} 月",
        "hint": "紧急事取天/周，长远事取周/月。用生体加速，用克体延迟。",
    }


def calculate_liuqin(palace, detail):
    """六亲推算（以落宫为'我'）"""
    wx = detail["wu_xing"]
    wx_relations = {
        "木": {"生": "火", "克": "土", "被生": "水", "被克": "金"},
        "火": {"生": "土", "克": "金", "被生": "木", "被克": "水"},
        "土": {"生": "金", "克": "水", "被生": "火", "被克": "木"},
        "金": {"生": "水", "克": "木", "被生": "土", "被克": "火"},
        "水": {"生": "木", "克": "火", "被生": "金", "被克": "土"},
    }
    wx_to_palace = {
        "木": "大安",
        "火": "速喜",
        "金": "赤口",
        "水": "小吉",
        "土": {"阳": "空亡", "阴": "留连"},
    }

    rel = wx_relations.get(wx, {})
    sheng_wx = rel.get("生", "")
    ke_wx = rel.get("克", "")
    beisheng_wx = rel.get("被生", "")
    beike_wx = rel.get("被克", "")

    def wx2palace(w):
        p = wx_to_palace.get(w, "")
        if isinstance(p, dict):
            return p.get("阳", "空亡")
        return p

    return {
        "self": f"{palace}({wx})",
        "子女": wx2palace(sheng_wx),
        "子女_desc": f"我生者：{wx}生{sheng_wx} → {wx2palace(sheng_wx)}",
        "配偶财帛": wx2palace(ke_wx),
        "配偶_desc": f"我克者：{wx}克{ke_wx} → {wx2palace(ke_wx)}",
        "父母贵人": wx2palace(beisheng_wx),
        "父母_desc": f"生我者：{beisheng_wx}生{wx} → {wx2palace(beisheng_wx)}",
        "官鬼上级": wx2palace(beike_wx),
        "官鬼_desc": f"克我者：{beike_wx}克{wx} → {wx2palace(beike_wx)}",
        "兄弟朋友": palace,
        "兄弟_desc": f"同我者：同属{wx} → {palace}",
    }


def calculate_sangong_juxiang(tian, di, ren):
    """三宫具象：将三盘阴阳转八卦"""
    yin_yang_map = {
        "大安": "阳", "速喜": "阳", "小吉": "阳",
        "留连": "阴", "赤口": "阴", "空亡": "阴",
    }
    # 天-人-地 序
    order = f"{yin_yang_map.get(tian, '?')}{yin_yang_map.get(ren, '?')}{yin_yang_map.get(di, '?')}"

    gua_map = {
        "阳阳阳": ("☰", "乾", "创始、强健、领导，天行健君子以自强不息"),
        "阴阴阴": ("☷", "坤", "包容、承载、柔顺，地势坤君子以厚德载物"),
        "阴阴阳": ("☳", "震", "震动、变革、行动，雷厉风行"),
        "阳阴阴": ("☶", "艮", "停止、稳固、等待，知止不殆"),
        "阳阴阳": ("☲", "离", "依附、光明、文采，明两作离"),
        "阴阳阴": ("☵", "坎", "险陷、流动、智慧，水洊至习坎"),
        "阴阳阳": ("☱", "兑", "喜悦、口舌、交流，丽泽兑"),
        "阳阳阴": ("☴", "巽", "渗透、顺从、风行，随风巽"),
    }

    gua_info = gua_map.get(order, ("?", "?", ""))
    return {
        "order": f"天({tian})-人({ren})-地({di})",
        "yin_yang": order,
        "gua_symbol": gua_info[0],
        "gua_name": gua_info[1],
        "gua_meaning": gua_info[2],
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="小六爻测算")
    parser.add_argument("time", nargs="?", help="指定时间 (YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--scene", "-s", help="测算场景: 求财/感情/事业/求职/出行/健康/失物/考试/综合运势")
    parser.add_argument("--question", "-q", help="具体问题描述")
    parser.add_argument("--yingqi", action="store_true", help="输出应期推断")
    parser.add_argument("--liuqin", action="store_true", help="输出六亲推算")
    parser.add_argument("--sangong", action="store_true", help="输出三宫具象")
    parser.add_argument("--all", action="store_true", help="输出所有高级分析")
    parser.add_argument("--raw", action="store_true", help="仅输出核心数据（不含高级分析）")
    args = parser.parse_args()

    if args.time:
        try:
            dt = datetime.strptime(args.time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            dt = datetime.strptime(args.time, "%Y-%m-%d")
    else:
        dt = datetime.now()

    result = calculate(dt)
    result["scene"] = args.scene or ""
    result["question"] = args.question or ""

    # 根据参数过滤输出
    if args.raw:
        # 仅核心数据
        keys_to_remove = {"ying_qi", "san_gong_ju_xiang", "liu_qin", "scene_readings"}
        for k in keys_to_remove:
            result.pop(k, None)
    elif args.all:
        # 保留全部
        pass
    else:
        # 默认：保留但按需标记
        result["advanced_available"] = True

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
