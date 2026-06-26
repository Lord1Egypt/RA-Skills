#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周易占卜工具 - 完整版（含八字 + 起卦）
纯本地实现，无外部依赖
"""

import json
import random
import argparse
from datetime import datetime
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bazi import (
    bazi_pandan, analyze_wuxing, find_yongshen,
    get_da_yun, generate_bazi_report, print_bazi_report
)

# ==================== 64 卦数据 ====================
HEXAGRAMS = {
    1: {"name": "乾为天", "trigrams": "上乾下乾", "judgment": "元亨利贞", "image": "天行健，君子以自强不息"},
    2: {"name": "坤为地", "trigrams": "上坤下坤", "judgment": "元亨，利牝马之贞", "image": "地势坤，君子以厚德载物"},
    3: {"name": "水雷屯", "trigrams": "上坎下震", "judgment": "元亨利贞，勿用有攸往", "image": "云雷屯，君子以经纶"},
    4: {"name": "山水蒙", "trigrams": "上艮下坎", "judgment": "亨。匪我求童蒙，童蒙求我", "image": "山下出泉，蒙；君子以果行育德"},
    5: {"name": "水天需", "trigrams": "上坎下乾", "judgment": "有孚，光亨，贞吉", "image": "云上于天，需；君子以饮食宴乐"},
    6: {"name": "天水讼", "trigrams": "上乾下坎", "judgment": "有孚，窒惕中吉", "image": "天与水违行，讼；君子以作事谋始"},
    7: {"name": "地水师", "trigrams": "上坤下坎", "judgment": "贞，丈人吉无咎", "image": "在地中，师；君子以容民畜众"},
    8: {"name": "水地比", "trigrams": "上坎下坤", "judgment": "吉。原筮元永贞，无咎", "image": "地上有水，比；先王以建万国，亲诸侯"},
    9: {"name": "风天小畜", "trigrams": "上巽下乾", "judgment": "亨。密云不雨，自我西郊", "image": "风行天上，小畜；君子以懿文德"},
    10: {"name": "天泽履", "trigrams": "上乾下兑", "judgment": "履虎尾，不咥人，亨", "image": "上天下泽，履；君子以辨上下，定民志"},
    11: {"name": "地天泰", "trigrams": "上坤下乾", "judgment": "小往大来，吉亨", "image": "天地交，泰；后以财成天地之道"},
    12: {"name": "天地否", "trigrams": "上乾下坤", "judgment": "否之匪人，不利君子贞", "image": "天地不交，否；君子以俭德辟难"},
    13: {"name": "天火同人", "trigrams": "上乾下离", "judgment": "同人于野，亨", "image": "天与火，同人；君子以类族辨物"},
    14: {"name": "火天大有", "trigrams": "上离下乾", "judgment": "元亨", "image": "火上于天，大有；君子以遏恶扬善"},
    15: {"name": "地山谦", "trigrams": "上坤下艮", "judgment": "亨，君子有终", "image": "地中有山，谦；君子以裒多益寡"},
    16: {"name": "雷地豫", "trigrams": "上震下坤", "judgment": "利建侯行师", "image": "雷出地奋，豫；先王以作乐崇德"},
    17: {"name": "泽雷随", "trigrams": "上兑下震", "judgment": "元亨利贞，无咎", "image": "泽中有雷，随；君子以向晦入宴息"},
    18: {"name": "山风蛊", "trigrams": "上艮下巽", "judgment": "元亨，利涉大川", "image": "风落山，蛊；君子以振民育德"},
    19: {"name": "地泽临", "trigrams": "上坤下兑", "judgment": "元亨利贞。至于八月有凶", "image": "泽上有地，临；君子以教思无穷"},
    20: {"name": "风地观", "trigrams": "上巽下坤", "judgment": "盥而不荐，有孚颙若", "image": "风行地上，观；先王以省方观民设教"},
    21: {"name": "火雷噬嗑", "trigrams": "上离下震", "judgment": "亨，利用狱", "image": "雷电噬嗑；先王以明罚敕法"},
    22: {"name": "山火贲", "trigrams": "上艮下离", "judgment": "亨，小利有攸往", "image": "山下有火，贲；君子以明庶政"},
    23: {"name": "山地剥", "trigrams": "上艮下坤", "judgment": "不利有攸往", "image": "山附于地，剥；上以厚下安宅"},
    24: {"name": "地雷复", "trigrams": "上坤下震", "judgment": "亨。出入无疾，朋来无咎", "image": "雷在地中，复；先王以至日闭关"},
    25: {"name": "天雷无妄", "trigrams": "上乾下震", "judgment": "元亨利贞。其匪正有眚", "image": "天下雷行，无妄；先王以茂对时育万物"},
    26: {"name": "山天大畜", "trigrams": "上艮下乾", "judgment": "利贞。不家食吉，利涉大川", "image": "天在山中，大畜；君子以多识前言往行"},
    27: {"name": "山雷颐", "trigrams": "上艮下震", "judgment": "贞吉。观颐，自求口实", "image": "山下有雷，颐；君子以慎言语，节饮食"},
    28: {"name": "泽风大过", "trigrams": "上兑下巽", "judgment": "栋桡，利有攸往，亨", "image": "泽灭木，大过；君子以独立不惧"},
    29: {"name": "坎为水", "trigrams": "上坎下坎", "judgment": "习坎，有孚，维心亨", "image": "水洊至，习坎；君子以常德行习教事"},
    30: {"name": "离为火", "trigrams": "上离下离", "judgment": "利贞，亨。畜犊牛吉", "image": "明两作，离；大人以继明照四方"},
    31: {"name": "泽山咸", "trigrams": "上兑下艮", "judgment": "亨，利贞，取女吉", "image": "山上有泽，咸；君子以虚受人"},
    32: {"name": "雷风恒", "trigrams": "上震下巽", "judgment": "亨，无咎，利贞，利有攸往", "image": "雷风，恒；君子以立不易方"},
    33: {"name": "天山遁", "trigrams": "上乾下艮", "judgment": "亨，小利贞", "image": "天下有山，遁；君子以远小人"},
    34: {"name": "雷天大壮", "trigrams": "上震下乾", "judgment": "利贞", "image": "雷在天上，大壮；君子以非礼弗履"},
    35: {"name": "火地晋", "trigrams": "上离下坤", "judgment": "康侯用锡马蕃庶，昼日三接", "image": "明出地上，晋；君子以自昭明德"},
    36: {"name": "地火明夷", "trigrams": "上坤下离", "judgment": "利艰贞", "image": "明入地中，明夷；君子以莅众用晦而明"},
    37: {"name": "风火家人", "trigrams": "上巽下离", "judgment": "利女贞", "image": "风自火出，家人；君子以言有物而行有恒"},
    38: {"name": "火泽睽", "trigrams": "上离下兑", "judgment": "小事吉", "image": "火动上，泽涌下；君子以同而异"},
    39: {"name": "水山蹇", "trigrams": "上坎下艮", "judgment": "利西南，不利东北；利见大人，贞吉", "image": "山上有水，蹇；君子以反身修德"},
    40: {"name": "雷水解", "trigrams": "上震下坎", "judgment": "利西南。无所往，其来复吉", "image": "雷雨作，解；君子以赦过宥罪"},
    41: {"name": "山泽损", "trigrams": "上艮下兑", "judgment": "有孚，元吉，无咎，可贞，利有攸往", "image": "山下有泽，损；君子以惩忿窒欲"},
    42: {"name": "风雷益", "trigrams": "上巽下震", "judgment": "利有攸往，利涉大川", "image": "风雷，益；君子以见善则迁，有过则改"},
    43: {"name": "泽天夬", "trigrams": "上兑下乾", "judgment": "扬于王庭，孚号有厉", "image": "泽上于天，夬；君子以施禄及下"},
    44: {"name": "天风姤", "trigrams": "上乾下巽", "judgment": "女壮，勿用取女", "image": "天下有风，姤；后以施命诰四方"},
    45: {"name": "泽地萃", "trigrams": "上兑下坤", "judgment": "亨，王假有庙，利见大人", "image": "泽上于地，萃；君子以除戎器，戒不虞"},
    46: {"name": "地风升", "trigrams": "上坤下巽", "judgment": "元亨，用见大人，勿恤，南征吉", "image": "地中生木，升；君子以顺德，积小以高大"},
    47: {"name": "泽水困", "trigrams": "上兑下坎", "judgment": "亨，贞，大人吉，无咎", "image": "泽无水，困；君子以致命遂志"},
    48: {"name": "水风井", "trigrams": "上坎下巽", "judgment": "改邑不改井，无丧无得", "image": "木上有水，井；君子以劳民劝相"},
    49: {"name": "泽火革", "trigrams": "上兑下离", "judgment": "巳日乃孚，元亨利贞，悔亡", "image": "泽中有火，革；君子以治历明时"},
    50: {"name": "火风鼎", "trigrams": "上离下巽", "judgment": "元吉，亨", "image": "木上有火，鼎；君子以正位凝命"},
    51: {"name": "震为雷", "trigrams": "上震下震", "judgment": "亨。震来虩虩，笑言哑哑", "image": "洊雷，震；君子以恐惧修省"},
    52: {"name": "艮为山", "trigrams": "上艮下艮", "judgment": "艮其背，不获其身", "image": "兼山，艮；君子以思不出其位"},
    53: {"name": "风山渐", "trigrams": "上巽下艮", "judgment": "女归吉，利贞", "image": "山上有木，渐；君子以居贤德善俗"},
    54: {"name": "雷泽归妹", "trigrams": "上震下兑", "judgment": "征凶，无攸利", "image": "泽上有雷，归妹；君子以永终知敝"},
    55: {"name": "雷火丰", "trigrams": "上震下离", "judgment": "亨，王假之，勿忧，宜日中", "image": "雷电皆至，丰；君子以折狱致刑"},
    56: {"name": "火山旅", "trigrams": "上离下艮", "judgment": "小亨，旅贞吉", "image": "山上有火，旅；君子以明慎用刑"},
    57: {"name": "巽为风", "trigrams": "上巽下巽", "judgment": "小亨，利有攸往，利见大人", "image": "随风，巽；君子以申命行事"},
    58: {"name": "兑为泽", "trigrams": "上兑下兑", "judgment": "亨，利贞", "image": "丽泽，兑；君子以朋友讲习"},
    59: {"name": "风水涣", "trigrams": "上巽下坎", "judgment": "亨，王假有庙，利涉大川", "image": "风行水上，涣；先王以享于帝立庙"},
    60: {"name": "水泽节", "trigrams": "上坎下兑", "judgment": "亨，苦节不可贞", "image": "泽上有水，节；君子以制数度，议德行"},
    61: {"name": "风泽中孚", "trigrams": "上巽下兑", "judgment": "豚鱼吉，利涉大川，利贞", "image": "泽上有风，中孚；君子以议狱缓死"},
    62: {"name": "雷山小过", "trigrams": "上震下艮", "judgment": "亨，利贞，可小事，不可大事", "image": "山上有雷，小过；君子以行过乎恭"},
    63: {"name": "水火既济", "trigrams": "上坎下离", "judgment": "亨，小利贞，初吉终乱", "image": "水在火上，既济；君子以思患而预防之"},
    64: {"name": "火水未济", "trigrams": "上离下坎", "judgment": "亨，小狐汔济，濡其尾，无攸利", "image": "火在水上，未济；君子以慎辨物居方"}
}

def toss_coins():
    """模拟三枚铜钱抛掷"""
    total = 0
    results = []
    for i in range(3):
        side = random.choice([0, 1])
        value = 3 if side == 0 else 2
        total += value
        results.append(value)
    return total, results

def cast_hexagram():
    """起六爻卦象（从下往上）"""
    lines = []
    line_values = []
    
    print("🎲 开始起卦...")
    print("=" * 50)
    
    for i in range(6):
        line_value, coin_results = toss_coins()
        lines.append(line_value)
        line_values.append({
            "value": line_value,
            "coins": coin_results,
            "type": get_line_type(line_value)
        })
        
        symbol = "⚊" if line_value in [7, 9] else "⚋"
        type_name = ["老阴×", "少阳-", "少阴--", "老阳○"][line_value - 6]
        print(f"第{i+1}爻：{symbol} ({type_name}) - 铜钱组合：{coin_results}")
    
    print("=" * 50)
    return lines, line_values

def get_line_type(value):
    return {6: "老阴（动爻）", 7: "少阳（静爻）", 8: "少阴（静爻）", 9: "老阳（动爻）"}.get(value, "未知")

def hexagram_from_lines(lines):
    """根据六爻计算卦号"""
    binary_str = ""
    for line in lines:
        binary_str += "1" if line in [7, 9] else "0"
    binary_str = binary_str[::-1]
    number = int(binary_str, 2) + 1
    if number < 1 or number > 64:
        number = 1
    return number

def generate_result(question, lines, line_values):
    """生成完整占卜结果"""
    main_number = hexagram_from_lines(lines)
    main_hexagram = HEXAGRAMS.get(main_number, HEXAGRAMS[1])
    
    changing_lines = []
    for i, lv in enumerate(line_values):
        if lv["value"] in [6, 9]:
            changing_lines.append(i + 1)
    
    visual_upper = "".join(["⚊" if l in [7, 9] else "⚋" for l in lines[3:]][::-1])
    visual_lower = "".join(["⚊" if l in [7, 9] else "⚋" for l in lines[:3]][::-1])
    
    result = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "question": question,
        "main_hexagram": {
            "number": main_number,
            "name": main_hexagram["name"],
            "trigrams": main_hexagram["trigrams"],
            "judgment": main_hexagram["judgment"],
            "image": main_hexagram["image"]
        },
        "changing_lines": changing_lines,
        "lines_details": line_values,
        "visual": {
            "upper": visual_upper,
            "lower": visual_lower,
            "combined": f"{visual_upper}{visual_lower}"
        }
    }
    
    if changing_lines:
        new_lines = lines.copy()
        for pos in changing_lines:
            idx = pos - 1
            if new_lines[idx] == 6:
                new_lines[idx] = 9
            elif new_lines[idx] == 9:
                new_lines[idx] = 6
        
        changing_number = hexagram_from_lines(new_lines)
        changing_hexagram = HEXAGRAMS.get(changing_number, HEXAGRAMS[1])
        
        result["changing_hexagram"] = {
            "number": changing_number,
            "name": changing_hexagram["name"],
            "trigrams": changing_hexagram["trigrams"],
            "judgment": changing_hexagram["judgment"],
            "image": changing_hexagram["image"]
        }
    
    return result

def oracle_with_bazi(result, bazi_report=None):
    """AI Oracle 诠释（支持八字结合）"""
    mh = result["main_hexagram"]
    
    print("\n" + "=" * 60)
    print("📖 《周易》综合解读报告")
    print("=" * 60)
    
    print(f"\n🙋‍♀️ 你所问：{result['question']}")
    
    print(f"\n═══════════════ 🎯 本卦信息 ═══════════════")
    print(f"   卦名：{mh['name']} (第{mh['number']}卦)")
    print(f"   卦象：{mh['trigrams']}")
    print(f"   卦辞：{mh['judgment']}")
    print(f"   大象：{mh['image']}")
    
    if result.get("changing_lines"):
        ch = result["changing_hexagram"]
        print(f"\n═══════════════ 🔄 变卦信息 ═══════════════")
        print(f"   变卦：{ch['name']} (第{ch['number']}卦)")
        print(f"   动爻：第{', '.join(map(str, result['changing_lines']))}爻")
    
    # 如果提供了八字信息，进行综合分析
    if bazi_report:
        print(f"\n═══════════════ 📜 八字背景 ═══════════════")
        b = bazi_report["bazi"]
        y = bazi_report["yongshen"]
        
        print(f"   八字：{b['raw']}")
        print(f"   日主：{y['day_master']} ({y['element']})")
        strength_text = "身强" if y['strength'] >= 3 else "身弱"
        print(f"   强弱：{strength_text} ({y['strength']}/8)")
        print(f"   用神建议：{', '.join(y['recommendations'])}")
        
        if bazi_report.get("current_da_yun"):
            cd = bazi_report["current_da_yun"]
            print(f"   当前大运：{cd['gan']}{cd['zhi']} ({bazi_report['current_age']}岁)")
        
        print(f"\n═══════════════ 💡 综合建议 ═══════════════")
        combined_advice = generate_combined_advice(result, bazi_report)
        print(combined_advice)
    
    print(f"\n═══════════════════════════════════════════════════")
    print("✨ 温馨提示：卦象只是指引，最终决策还需结合自身实际情况～")
    print("=" * 60)

def generate_combined_advice(hexagram_result, bazi_report):
    """结合卦象和八字的综合建议"""
    mh = hexagram_result["main_hexagram"]
    y = bazi_report["yongshen"]
    wuxing = bazi_report["wuxing"]
    
    # 提取问题关键词
    question = hexagram_result["question"].lower()
    
    advice_templates = {}
    
    # 事业相关
    if any(k in question for k in ["工作", "事业", "升职", "发展", "创业"]):
        if y['strength'] >= 3:
            advice = f"您的八字显示'{y['day_master']}'日主身强，精力充沛。当前{mh['name']}提醒您 '{mh['judgment']}'。建议发挥优势但注意收敛锋芒，配合流年运势把握机遇。"
        else:
            advice = f"您的日主'{y['day_master']}'偏弱，需要借助外力。{mh['name']}的启示是'{mh['image']}'。建议寻求贵人相助，积累实力再图发展。"
    
    # 感情相关
    elif any(k in question for k in ["感情", "姻缘", "婚姻", "恋爱", "对象"]):
        if y['element'] in ["木", "火"]:
            advice = f"{mh['name']}对于感情的启示：'{mh['judgment']}'。您性格积极热情，但在感情中需要更多耐心和理解。"
        else:
            advice = f"{mh['name']}关于感情的智慧：'{mh['judgment']}'。保持真诚和包容，缘分自然会来。"
    
    # 财运相关
    elif any(k in question for k in ["财运", "投资", "赚钱", "财富", "金钱"]):
        wood_count = wuxing.get("木", 0)
        fire_count = wuxing.get("火", 0)
        if wood_count + fire_count >= 3:
            advice = f"{mh['name']}提示财运方面'{mh['judgment']}'。您八字木火较旺，适合积极进取，但需注意风险把控。"
        else:
            advice = f"根据{mh['name']}的智慧，财运上建议稳中求进。'{mh['image']}'提醒我们量力而行。"
    
    # 健康相关
    elif any(k in question for k in ["健康", "身体", "生病", "吃药"]):
        water_count = wuxing.get("水", 0)
        fire_count = wuxing.get("火", 0)
        if water_count < 2 or fire_count < 2:
            advice = f"{mh['name']}关照身心健康。您八字五行{'水' if water_count<2 else '火'}偏弱，需要注意休息调养，平衡身心。"
        else:
            advice = f"《周易》通过{mh['name']}提示：养生要顺应自然，'{mh['image']}'是重要的生活智慧。"
    
    else:
        # 通用建议
        if y['strength'] >= 4:
            advice = f"您八字日主极强，个性突出。{mh['name']}启示您：'{mh['image']}'。建议在发挥优势的同时，学会审时度势、顺势而为。"
        elif y['strength'] <= 2:
            advice = f"您的八字显示需要借力发力。{mh['name']}告诉我们要'{mh['judgment']}'。积累人脉资源，等待时机成熟会更有利。"
        else:
            advice = f"综合来看，{mh['name']}的核心智慧是'{mh['image']}'。这是一个中正平和的状态，保持初心、稳步前行即可。"
    
    return advice

def print_menu():
    """打印菜单"""
    print("""
╔════════════════════════════════════════════════════════╗
║           🔮  周易占卜系统 · 完整版  🔮              ║
║                                                         ║
║   ① 纯起卦（铜钱法）                                    ║
║   ② 八字 + 起卦综合解读                                 ║
║   ③ 只排八字                                            ║
║   ④ 退出                                               ║
╚════════════════════════════════════════════════════════╝
    """)

def main():
    parser = argparse.ArgumentParser(description="周易占卜工具 - 完整版（含八字 + 起卦）")
    parser.add_argument("--question", "-q", type=str, default="",
                        help="你想问的问题")
    parser.add_argument("--birth-year", type=int, help="出生年份")
    parser.add_argument("--birth-month", type=int, help="出生月份")
    parser.add_argument("--birth-day", type=int, help="出生日期")
    parser.add_argument("--birth-hour", type=int, help="出生时辰（24 小时制）")
    parser.add_argument("--gender", choices=["男", "女"], default="男", help="性别")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式结果")
    parser.add_argument("--mode", choices=["hexagram", "bazi", "both"], default="both",
                        help="模式：纯起卦/只排八字/综合")
    
    args = parser.parse_args()
    
    # 命令行模式
    if args.question:
        bazi_report = None
        
        # 如果提供了八字信息或需要综合模式
        if args.mode in ["both", "bazi"]:
            if args.birth_year and args.birth_month and args.birth_day and args.birth_hour:
                birth_info = {
                    "year": args.birth_year,
                    "month": args.birth_month,
                    "day": args.birth_day,
                    "hour": args.birth_hour,
                    "gender": args.gender
                }
                bazi_report = generate_bazi_report(birth_info)
                if not args.json:
                    print_bazi_report(bazi_report)
            elif args.mode == "both":
                print("提示：提供八字信息可以获得更精准的解读哦～")
                print("      --birth-year --birth-month --birth-day --birth-hour")
                print()
        
        # 起卦
        lines, line_values = cast_hexagram()
        result = generate_result(args.question, lines, line_values)
        
        if args.json:
            output = result
            if bazi_report:
                output["bazi_report"] = bazi_report
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            print(f"\n📊 卦象可视化:")
            print(f"   {result['visual']['upper']} ← 上卦")
            print(f"   {result['visual']['lower']} ← 下卦")
            oracle_with_bazi(result, bazi_report)
        
        return
    
    # 交互模式
    print("\n🔮 ===== 周易占卜系统 =====")
    print("基于铜钱法和传统八字命理的综合推演工具")
    print("请选择模式...\n")
    
    try:
        choice = input("请输入选项 (1-4): ").strip()
        
        if choice == "4":
            print("有缘再会！🙏")
            return
        
        question = input("\n请静心思考，输入您的问题：").strip() or "今年的运势如何？"
        
        bazi_report = None
        
        if choice in ["2", "3"]:
            print("\n请输入出生信息：")
            year = int(input("  出生年份 (如 1990): ") or datetime.now().year)
            month = int(input("  出生月份 (1-12): ") or 1)
            day = int(input("  出生日期 (1-31): ") or 1)
            hour = int(input("  出生时辰 (0-23): ") or 12)
            gender = input("  性别 (男/女): ").strip() or "男"
            
            birth_info = {"year": year, "month": month, "day": day, "hour": hour, "gender": gender}
            bazi_report = generate_bazi_report(birth_info)
            print_bazi_report(bazi_report)
        
        if choice in ["1", "2"]:
            lines, line_values = cast_hexagram()
            result = generate_result(question, lines, line_values)
            oracle_with_bazi(result, bazi_report)
        
    except KeyboardInterrupt:
        print("\n\n再见！愿您平安顺遂～ 🙏")
    except Exception as e:
        print(f"\n发生错误：{e}")

if __name__ == "__main__":
    main()
