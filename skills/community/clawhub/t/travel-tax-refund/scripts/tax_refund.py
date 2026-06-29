#!/usr/bin/env python3
"""旅行退税指南 - Travel Tax Refund Guide"""

import json
import sys

# ====== 各国退税政策数据库 ======
# 退税率 = 标准VAT税率，实际退税率因退税公司手续费略低
REFUND_DATA = {
    "法国": {
        "vat_rate": 20,
        "actual_refund_rate": "约12-14%",
        "min_purchase": "同一商店同一天满100.01欧元",
        "currency": "EUR",
        "process": [
            "1. 商店购物时出示护照，索取退税单(Tax Free Form)",
            "2. 离境时到海关盖章(需出示商品+退税单+护照+机票)",
            "3. 盖章后到退税柜台拿现金/退信用卡",
            "4. ⚠️ T2航站楼退税柜台排队很长，预留2小时"
        ],
        "tips": "巴黎戴高乐机场有自助退税机(PABLO)，扫描条码即可，比人工快很多",
        "refund_companies": ["Global Blue", "Premier Tax Free", "Tax Free France"],
        "best_for": "奢侈品(Chanel/Dior/LV)退税率最高",
        "note": "12岁以上方可退税；最后目的地为非EU国家才能退税"
    },
    "德国": {
        "vat_rate": 19,
        "actual_refund_rate": "约10-14%",
        "min_purchase": "同一商店满25欧元起",
        "currency": "EUR",
        "process": [
            "1. 购物时索取退税单",
            "2. 离境时海关盖章(法兰克福/慕尼黑机场有自助机)",
            "3. 盖章后退税柜台取现或退卡",
        ],
        "tips": "德国退税门槛低(25欧)，日常消费也能退",
        "refund_companies": ["Global Blue", "Tax Free Germany"],
        "best_for": "双立人/WMF等厨具、Rimowa行李箱",
        "note": "EU内部转机需在最后一个EU机场盖章"
    },
    "意大利": {
        "vat_rate": 22,
        "actual_refund_rate": "约11-15%",
        "min_purchase": "同一商店满154.95欧元",
        "currency": "EUR",
        "process": [
            "1. 购物时出示护照索取退税单",
            "2. 离境时海关盖章(罗马/米兰机场有自助扫描机)",
            "3. 退税柜台取现/退卡",
        ],
        "tips": "米兰/罗马机场退税排队严重，建议提前3小时到",
        "refund_companies": ["Global Blue", "Premier Tax Free", "Tax Free Italy"],
        "best_for": "Gucci/Prada/Fendi等意大利品牌退税率最高",
        "note": "佛罗伦萨The Mall折扣村购物后可直接店内退税"
    },
    "西班牙": {
        "vat_rate": 21,
        "actual_refund_rate": "约12-15%",
        "min_purchase": "同一商店同一天满90.16欧元",
        "currency": "EUR",
        "process": [
            "1. 购物时索取退税单",
            "2. 离境时海关盖章",
            "3. 退税柜台取现/退卡",
        ],
        "tips": "马德里/巴塞罗那机场退税较顺畅",
        "refund_companies": ["Global Blue", "Premier Tax Free"],
        "best_for": "Loewe/Camper/Zara(本土品牌退税率最高)",
        "note": ""
    },
    "英国": {
        "vat_rate": 20,
        "actual_refund_rate": "约10-14%",
        "min_purchase": "同一商店满30英镑",
        "currency": "GBP",
        "process": [
            "1. 购物时索取退税单",
            "2. 离境时海关盖章(希思罗机场有自助机)",
            "3. 退税柜台取现/退卡",
        ],
        "tips": "脱欧后退税政策仍然有效",
        "refund_companies": ["Global Blue"],
        "best_for": "Burberry/Barbour等英国品牌",
        "note": "希思罗T5退税最方便"
    },
    "瑞士": {
        "vat_rate": 8.1,
        "actual_refund_rate": "约3.5-5%",
        "min_purchase": "同一商店满300瑞郎",
        "currency": "CHF",
        "process": [
            "1. 购物时索取退税单",
            "2. 离境时海关盖章",
            "3. 退税柜台取现/退卡",
        ],
        "tips": "瑞士VAT低，退税率也低，但瑞士手表本身不便宜",
        "refund_companies": ["Global Blue"],
        "best_for": "瑞士手表(Longines/Omega/Rolex)、军刀",
        "note": "瑞士非EU成员国，从瑞士去EU国家可在瑞士边境退税"
    },
    "日本": {
        "vat_rate": 10,
        "actual_refund_rate": "约8-10%",
        "min_purchase": "同一商店同一天满5000日元(免税品)",
        "currency": "JPY",
        "process": [
            "1. 购物时出示护照，直接免税！(日本是即时不扣税)",
            "2. 不需要机场退税！商店直接免掉消费税",
            "3. 部分大型商场有专门免税柜台",
        ],
        "tips": "日本最方便——直接免税，不需要机场退税流程！",
        "refund_companies": ["无需退税公司"],
        "best_for": "药妆/电器/服饰/食品(消耗品免税需当天在同一店满5000日元)",
        "note": "消耗品(食品/药妆)和一般品(电器/服饰)分开计算，各需满5000日元"
    },
    "韩国": {
        "vat_rate": 10,
        "actual_refund_rate": "约5-7%",
        "min_purchase": "同一商店满15000韩元",
        "currency": "KRW",
        "process": [
            "1. 购物时索取退税单",
            "2. 仁川机场：先值机→海关盖章→托运→安检→退税柜台",
            "3. 退税柜台取现/退卡/支付宝",
        ],
        "tips": "韩国支持支付宝退税，最方便！明洞/免税店基本都有退税服务",
        "refund_companies": ["Global Blue", "KTIS", "Easy Tax Refund"],
        "best_for": "化妆品/服饰/箱包",
        "note": "韩国免税店购物本身就免税，退税主要针对百货商店/专卖店"
    },
    "泰国": {
        "vat_rate": 7,
        "actual_refund_rate": "约4-5%",
        "min_purchase": "同一商店同一天满2000泰铢，累计满5000泰铢",
        "currency": "THB",
        "process": [
            "1. 商店购物时索取退税单(P.P.10表)",
            "2. 离境时先去海关盖章(在值机前！需出示商品)",
            "3. 过安检后到退税柜台取现(限30000泰铢以内)",
        ],
        "tips": "⚠️ 贵重物品(珠宝/手表)必须随身携带出示给海关",
        "refund_companies": ["VAT Refund for Tourists"],
        "best_for": "珠宝/手工艺品/丝绸",
        "note": "退税手续费100泰铢；超过30000泰铢只能退卡"
    },
    "新加坡": {
        "vat_rate": 9,
        "actual_refund_rate": "约5-6%",
        "min_purchase": "同一商店满100新币",
        "currency": "SGD",
        "process": [
            "1. 购物时索取退税单",
            "2. 樟宜机场使用自助退税机(eTRS)扫描护照+退税单",
            "3. 选择退到信用卡/支付宝/现金",
        ],
        "tips": "樟宜机场eTRS自助退税非常方便，几分钟搞定",
        "refund_companies": ["eTRS (电子退税系统)"],
        "best_for": "电子产品/化妆品/手表",
        "note": "新加坡免税店本身免税，退税针对含税商店"
    },
    "澳大利亚": {
        "vat_rate": 10,
        "actual_refund_rate": "约6-8%",
        "min_purchase": "同一商店同一天满300澳币",
        "currency": "AUD",
        "process": [
            "1. 购物时索取退税单",
            "2. 离境时TRS柜台办理(出示商品+退税单+护照+登机牌)",
            "3. 退税到信用卡/澳大利亚银行账户",
        ],
        "tips": "TRS柜台在安检后，需先值机→托运→安检→TRS柜台",
        "refund_companies": ["TRS (Tourist Refund Scheme)"],
        "best_for": "UGG/保健品/羊毛制品",
        "note": "澳大利亚政府运营TRS，退税率比商业退税公司高"
    },
    "阿联酋": {
        "vat_rate": 5,
        "actual_refund_rate": "约3-4%",
        "min_purchase": "同一商店满250迪拉姆",
        "currency": "AED",
        "process": [
            "1. 购物时索取退税单",
            "2. 迪拜机场使用自助退税机扫描",
            "3. 退税到信用卡/现金",
        ],
        "tips": "迪拜机场自助退税机很方便，但退税率低(因为VAT本身就低)",
        "refund_companies": ["Planet Tax Free"],
        "best_for": "黄金/奢侈品(本身价格就便宜，退税是锦上添花)",
        "note": "迪拜购物节期间折扣力度远大于退税"
    },
    "土耳其": {
        "vat_rate": 20,
        "actual_refund_rate": "约10-14%",
        "min_purchase": "同一商店满100里拉",
        "currency": "TRY",
        "process": [
            "1. 购物时索取退税单",
            "2. 离境时海关盖章(出示商品+退税单)",
            "3. 退税柜台取现/退卡",
        ],
        "tips": "土耳其退税率高(VAT 20%)，值得退！",
        "refund_companies": ["Global Blue"],
        "best_for": "地毯/皮革/陶瓷/珠宝",
        "note": "注意里拉汇率波动大，退税金额以欧元/美元计算更划算"
    },
}

# ====== 通用退税注意事项 ======
REFUND_TIPS = {
    "机场退税": [
        "提前2-3小时到机场，退税排队可能很久",
        "贵重物品(手表/珠宝/奢侈品)随身携带，海关可能查验",
        "先海关盖章→再托运行李(贵重物品随身)",
        "大件物品可先去海关盖章再托运",
        "退税单盖章后有效期通常3个月-5年(因国而异)",
        "保留退税单直到退款到账",
        "部分机场有自助退税机(法国PABLO/韩国kiosk/新加坡eTRS)，更快",
        "退税方式：信用卡(最方便) > 支付宝(韩国/日本支持) > 现金(手续费最高)",
    ],
    "商店购物": [
        "购物时主动说'Tax Free'或'Detaxe'(法语)",
        "随身带护照(原件/照片/复印件均可，原件最保险)",
        "确认退税单信息准确(姓名/护照号/国籍)",
        "同一商店同一天累计达到起退金额即可",
        "部分商店(如巴黎老佛爷)有中文退税服务",
        "免税店(Duty Free)购物不需要退税，已经免税",
        "机场免税店购物不需要退税流程",
    ],
    "海关查验": [
        "商品必须是未使用的(包装完好的新商品)",
        "海关可能要求开箱查验，提前准备好",
        "从EU国家离境：在最后一个EU国家海关盖章",
        "转机情况：直挂行李也可能需要在转机机场盖章",
        "火车/汽车离境也有海关退税点(需提前确认)",
        "未退税的商品理论上不能在境内使用",
    ],
    "避坑指南": [
        "⚠️ 退税公司手续费：Global Blue等会收2-5%手续费",
        "⚠️ 信用卡退税到账需2-6周，别着急",
        "⚠️ 现金退税手续费最高(约3-5欧/笔)，不建议",
        "⚠️ 退税单遗失不补，小心保管",
        "⚠️ 部分国家退税率看似高，实际到手因手续费打折",
        "⚠️ 非EU居民才能退税(EU居民不符合条件)",
        "⚠️ 在EU境内消费使用的商品不能退税",
        "⚠️ 留足退税时间！误机比不退税损失更大",
    ],
}


def match_destination(destination):
    """模糊匹配目的地"""
    if destination in REFUND_DATA:
        return destination
    
    aliases = {
        "东京": "日本", "大阪": "日本", "京都": "日本", "北海道": "日本", "冲绳": "日本",
        "首尔": "韩国", "釜山": "韩国", "济州岛": "韩国",
        "曼谷": "泰国", "普吉岛": "泰国", "清迈": "泰国",
        "新加坡": "新加坡",
        "巴黎": "法国", "尼斯": "法国", "里昂": "法国",
        "柏林": "德国", "慕尼黑": "德国", "法兰克福": "德国",
        "罗马": "意大利", "米兰": "意大利", "威尼斯": "意大利", "佛罗伦萨": "意大利",
        "巴塞罗那": "西班牙", "马德里": "西班牙",
        "伦敦": "英国", "爱丁堡": "英国",
        "苏黎世": "瑞士", "日内瓦": "瑞士", "卢塞恩": "瑞士",
        "悉尼": "澳大利亚", "墨尔本": "澳大利亚",
        "迪拜": "阿联酋", "阿布扎比": "阿联酋",
        "伊斯坦布尔": "土耳其",
        "槟城": "无", "吉隆坡": "无",  # 马来西亚无VAT退税
        "胡志明": "无", "河内": "无",  # 越南退税复杂
        "纽约": "无", "洛杉矶": "无",  # 美国无联邦VAT
    }
    
    return aliases.get(destination, None)


def cmd_refund_policy(params):
    """查询目的地退税政策"""
    destination = params.get("destination", "")
    
    if not destination:
        return {"error": "请提供目的地国家"}
    
    matched = match_destination(destination)
    
    if matched is None or matched == "无":
        # 无法退税的国家
        no_refund_countries = {
            "美国": "美国没有联邦VAT/消费税退税制度。部分州(如路易斯安那)有地方退税试点，但范围有限",
            "马来西亚": "马来西亚无VAT退税制度(有销售税但不对游客退税)",
            "越南": "越南有退税政策但流程复杂，仅限指定商店，实际操作困难",
            "加拿大": "加拿大已取消游客退税制度(2007年起)",
            "中国": "中国有离境退税政策(2015年起)，覆盖20+城市，退税率约9%，但流程较新普及度低",
        }
        
        # 检查别名
        for country, info in no_refund_countries.items():
            if country in destination or destination in country:
                return {
                    "destination": destination,
                    "refund_available": False,
                    "reason": info,
                }
        
        return {
            "destination": destination,
            "refund_available": False,
            "reason": f"暂未收录{destination}的退税政策",
            "general_tip": "大部分有VAT的国家都支持游客退税，建议查询该国海关官网确认"
        }
    
    data = REFUND_DATA[matched]
    
    return {
        "destination": destination,
        "matched_country": matched,
        "refund_available": True,
        "vat_rate": f"{data['vat_rate']}%",
        "actual_refund_rate": data["actual_refund_rate"],
        "min_purchase": data["min_purchase"],
        "currency": data["currency"],
        "process": data["process"],
        "tips": data["tips"],
        "refund_companies": data["refund_companies"],
        "best_for": data["best_for"],
        "note": data["note"],
    }


def cmd_calc_refund(params):
    """计算退税金额"""
    destination = params.get("destination", "")
    amount = params.get("amount", 0)
    currency = params.get("currency", "")
    
    if not destination:
        return {"error": "请提供目的地国家"}
    
    try:
        amount = float(amount)
        if amount <= 0:
            return {"error": "消费金额必须大于0"}
    except (ValueError, TypeError):
        return {"error": "请输入有效的消费金额"}
    
    matched = match_destination(destination)
    
    if not matched or matched == "无":
        return {"error": f"该目的地暂不支持退税计算"}
    
    data = REFUND_DATA[matched]
    vat_rate = data["vat_rate"] / 100.0
    
    # 退税金额 = 消费金额 × VAT率 / (1 + VAT率)
    # 这是标准的VAT计算公式：含税价中的税额
    tax_amount = amount * vat_rate / (1 + vat_rate)
    
    # 退税公司通常收2-5%手续费
    # 实际到手约为税额的60-70%
    actual_refund_low = tax_amount * 0.60
    actual_refund_high = tax_amount * 0.70
    
    # 判断是否达到起退金额
    min_purchase_text = data["min_purchase"]
    min_reached = True  # 简化判断，提示用户确认
    
    result = {
        "destination": matched,
        "purchase_amount": f"{amount:.2f} {data['currency']}",
        "vat_rate": f"{data['vat_rate']}%",
        "tax_amount": f"{tax_amount:.2f} {data['currency']}",
        "estimated_refund": f"{actual_refund_low:.2f} - {actual_refund_high:.2f} {data['currency']}",
        "refund_rate_note": f"实际退税率约为消费额的{data['actual_refund_rate']}(扣除退税公司手续费后)",
        "min_purchase": min_purchase_text,
        "min_purchase_note": "请确认是否达到起退金额",
        "tips": data["tips"],
    }
    
    # 快速换算人民币参考
    currency_to_cny = {
        "EUR": 7.8, "GBP": 9.2, "CHF": 8.2, "JPY": 0.048,
        "KRW": 0.0052, "THB": 0.20, "SGD": 5.4, "AUD": 4.7,
        "AED": 1.93, "TRY": 0.22, "USD": 7.2,
    }
    rate = currency_to_cny.get(data["currency"], 0)
    if rate > 0:
        cny_low = actual_refund_low * rate
        cny_high = actual_refund_high * rate
        result["estimated_refund_cny"] = f"约¥{cny_low:.0f} - ¥{cny_high:.0f}人民币"
    
    return result


def cmd_refund_tips(params):
    """退税注意事项"""
    scenario = params.get("scenario", "")
    
    result = {}
    
    if scenario:
        scenario_map = {
            "机场": "机场退税", "机场退税": "机场退税",
            "商店": "商店购物", "购物": "商店购物",
            "海关": "海关查验", "查验": "海关查验",
            "避坑": "避坑指南", "注意": "避坑指南",
        }
        key = scenario_map.get(scenario, scenario)
        for category, tips in REFUND_TIPS.items():
            if key in category or category in key:
                result[category] = tips
                break
        
        if not result:
            result = REFUND_TIPS
    else:
        result = REFUND_TIPS
    
    # 补充通用流程
    result["通用退税流程"] = [
        "购物 → 索取退税单 → 离境海关盖章 → 退税柜台取款/退卡",
        "日本/韩国免税店：直接免税，无需退税流程",
        "EU国家：在最后一个EU国家离境时统一退税",
    ]
    
    return result


# ====== 主入口 ======
TOOLS = {
    "refund_policy": cmd_refund_policy,
    "calc_refund": cmd_calc_refund,
    "refund_tips": cmd_refund_tips,
}


def main():
    if len(sys.argv) < 3:
        print(json.dumps({"error": "用法: python3 tax_refund.py <tool> '<json_params>'", "tools": list(TOOLS.keys())}, ensure_ascii=False))
        return

    tool = sys.argv[1]
    try:
        params = json.loads(sys.argv[2])
    except json.JSONDecodeError:
        print(json.dumps({"error": "参数JSON解析失败"}, ensure_ascii=False))
        return

    handler = TOOLS.get(tool)
    if not handler:
        print(json.dumps({"error": f"未知工具: {tool}", "tools": list(TOOLS.keys())}, ensure_ascii=False))
        return

    result = handler(params)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
