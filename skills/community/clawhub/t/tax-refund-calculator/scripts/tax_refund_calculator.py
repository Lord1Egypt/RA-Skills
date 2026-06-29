#!/usr/bin/env python3
"""旅行购物退税计算器 - Tax Refund Calculator
查询各国退税政策并计算退税金额，覆盖全球30+热门购物目的地
纯本地数据，无需外部API
"""
import json
import sys

# ========== 退税政策数据库 ==========

COUNTRIES = {
    # ===== 亚洲 =====
    "日本": {
        "currency": "JPY", "symbol": "¥", "rate": 4.8,
        "vat_name": "消费税", "vat_rate": 10,
        "min_purchase": 5000, "min_purchase_cny": 240,
        "refund_rate": 10, "deduction": 0,
        "method": "免税店直接免税/机场退税",
        "notes": "2024年起免税手续简化，同一店铺同日购物满5000日元即可免税。消耗品(食品/药品/化妆品)需同日同店满5000日元且50万日元以内，包装不能拆封。一般物品(电器/服装等)无上限。",
        "steps": ["免税店购物时出示护照", "店员直接扣除税金", "消耗品密封包装不可拆封直到离境", "离境时海关可能查验"],
        "tips": ["药妆店基本都支持免税", "百货公司累计当日消费可合并免税", "大型电器店(BicCamera/友都八喜)免税+额外折扣"],
    },
    "韩国": {
        "currency": "KRW", "symbol": "₩", "rate": 195,
        "vat_name": "增值税", "vat_rate": 10,
        "min_purchase": 15000, "min_purchase_cny": 77,
        "refund_rate": 8.5, "deduction": 1.5,
        "method": "免税店直接免税/市区退税/机场退税",
        "notes": "满15000韩元即可退税，退税公司手续费约1-2%。首尔市区有自助退税机。当日同一店铺累计即可。",
        "steps": ["免税店购物直接免税", "普通店购物索要退税单", "机场自助退税机或柜台退税", "或市区退税点办理"],
        "tips": ["乐天/新罗免税店直接免税最划算", "KTIS/Global Blue退税单在市区可办", "仁川机场退税人少凌晨最空"],
    },
    "泰国": {
        "currency": "THB", "symbol": "฿", "rate": 4.5,
        "vat_name": "增值税", "vat_rate": 7,
        "min_purchase": 2000, "min_purchase_cny": 445,
        "refund_rate": 5.5, "deduction": 1.5,
        "method": "机场退税",
        "notes": "同一店铺同日消费满2000泰铢可开退税单，离境时在机场办理。退税手续费100泰铢。贵重物品(珠宝/黄金)需额外审核。",
        "steps": ["购物时索取PP10退税表", "同日同店累计满2000铢", "离境时先去海关盖章(VAT Refund)", "过安检后退税柜台领钱"],
        "tips": ["退税金额低于30000铢可领现金", "超过30000铢只能转账/信用卡", "保留所有购物小票"],
    },
    "新加坡": {
        "currency": "SGD", "symbol": "S$", "rate": 5.4,
        "vat_name": "GST", "vat_rate": 9,
        "min_purchase": 100, "min_purchase_cny": 540,
        "refund_rate": 7.5, "deduction": 1.5,
        "method": "电子退税eTRS/机场退税",
        "notes": "GST从8%升至9%(2024年起)。eTRS电子退税系统便捷，支持信用卡关联自动退税。",
        "steps": ["购物时出示护照，店员开具eTRS单", "樟宜机场自助退税机扫描", "选择退款方式(信用卡/支付宝/现金)", "贵重物品海关可能查验"],
        "tips": ["樟宜机场退税非常方便", "信用卡关联eTRS更快", "退税可到支付宝"],
    },

    # ===== 欧洲 =====
    "法国": {
        "currency": "EUR", "symbol": "€", "rate": 7.8,
        "vat_name": "TVA", "vat_rate": 20,
        "min_purchase": 100, "min_purchase_cny": 780,
        "refund_rate": 12, "deduction": 8,
        "method": "PABLO电子退税/机场退税",
        "notes": "税率20%为欧洲最高之一，但退税后实际到手约12%。满100欧元即可退税。PABLO电子退税无需海关盖章。",
        "steps": ["购物时索要退税单(PABLO)", "机场PABLO自助机扫描", "过安检后退税柜台领钱", "或选择信用卡/支付宝退款"],
        "tips": ["老佛爷/春天百货有中文退税柜台", "PABLO电子退税免去排队", "单笔金额越大退税比例越高", "退税可到支付宝"],
    },
    "意大利": {
        "currency": "EUR", "symbol": "€", "rate": 7.8,
        "vat_name": "IVA", "vat_rate": 22,
        "min_purchase": 154, "min_purchase_cny": 1200,
        "refund_rate": 13, "deduction": 9,
        "method": "机场退税/市区退税",
        "notes": "税率22%欧盟最高，实际到手约13%。佛罗伦萨/米兰/The Mall等有市区退税点。",
        "steps": ["购物时索要退税单", "机场海关盖章(贵重物品需查验)", "过安检后Global Blue/Planet柜台退税", "市区退税点可提前拿到现金"],
        "tips": ["The Mall/McArthurGlen奥特莱斯可市区退税", "罗马Fiumicino机场退税排队较长", "保留小票到回国后确认扣款"],
    },
    "德国": {
        "currency": "EUR", "symbol": "€", "rate": 7.8,
        "vat_name": "MwSt", "vat_rate": 19,
        "min_purchase": 50, "min_purchase_cny": 390,
        "refund_rate": 11, "deduction": 8,
        "method": "机场退税",
        "notes": "起退点低(50欧)，适合小额购物退税。德国退税流程规范。",
        "steps": ["购物时索要Tax Free单", "机场海关盖章", "过安检后退税柜台办理"],
        "tips": ["起退金额低，小额也值得退", "法兰克福机场退税柜台较多"],
    },
    "西班牙": {
        "currency": "EUR", "symbol": "€", "rate": 7.8,
        "vat_name": "IVA", "vat_rate": 21,
        "min_purchase": 90, "min_purchase_cny": 700,
        "refund_rate": 12, "deduction": 9,
        "method": "机场退税/DIVA电子退税",
        "notes": "税率21%，DIVA电子退税在马德里/巴塞罗那机场可用。",
        "steps": ["购物时索要退税单", "DIVA自助机扫描或海关盖章", "过安检后退税柜台办理"],
        "tips": ["巴塞罗那机场退税人很多，提前3小时到", "La Roca Village奥特莱斯有中文服务"],
    },
    "英国": {
        "currency": "GBP", "symbol": "£", "rate": 9.2,
        "vat_name": "VAT", "vat_rate": 20,
        "min_purchase": 0, "min_purchase_cny": 0,
        "refund_rate": 0, "deduction": 20,
        "method": "已取消退税",
        "notes": "⚠️ 英国已于2021年1月1日取消离境退税(Tax-Free Shopping)。国际旅客在英国购物不再享受VAT退税。仅保留烟酒店内免税。",
        "steps": ["英国已无退税政策"],
        "tips": ["英国购物不再退税！去欧洲其他国家买更划算", "希思罗机场免税店仍可免VAT买烟酒"],
    },
    "瑞士": {
        "currency": "CHF", "symbol": "CHF", "rate": 8.0,
        "vat_name": "MwSt", "vat_rate": 8.1,
        "min_purchase": 300, "min_purchase_cny": 2400,
        "refund_rate": 5.5, "deduction": 2.6,
        "method": "机场退税",
        "notes": "税率低(8.1%)，起退点高(300CHF)，实际到手约5.5%。瑞士非欧盟，与欧盟国家分开退税。",
        "steps": ["购物时索要退税单", "瑞士海关盖章(非欧盟海关)", "过安检后退税柜台办理"],
        "tips": ["手表/珠宝退税金额可观", "苏黎世机场退税方便"],
    },

    # ===== 中东 =====
    "阿联酋": {
        "currency": "AED", "symbol": "د.إ", "rate": 1.95,
        "vat_name": "VAT", "vat_rate": 5,
        "min_purchase": 250, "min_purchase_cny": 488,
        "refund_rate": 4.0, "deduction": 1.0,
        "method": "Planet退税/机场退税",
        "notes": "税率仅5%，退税金额不大但流程简单。迪拜Mall等大型商场有Planet退税点。",
        "steps": ["购物时索要退税单", "机场自助机扫描Planet退税单", "选择退款方式"],
        "tips": ["税率低，退税金额有限", "迪拜机场退税流程很快"],
    },

    # ===== 大洋洲 =====
    "澳大利亚": {
        "currency": "AUD", "symbol": "A$", "rate": 4.8,
        "vat_name": "GST", "vat_rate": 10,
        "min_purchase": 300, "min_purchase_cny": 1440,
        "refund_rate": 8.5, "deduction": 1.5,
        "method": "TRS机场退税",
        "notes": "离境前60天内在同一商家消费满300澳元可退GST。TRS系统支持网上预申报。",
        "steps": ["购物时保留发票(ABN商家)", "TRS网上预申报(app)", "机场TRS柜台出示商品和发票", "退到信用卡/澳洲银行账户"],
        "tips": ["TRS网上预申报可省排队时间", "商品需随身携带(不能托运)", "退到信用卡约5个工作日"],
    },

    # ===== 北美 =====
    "美国": {
        "currency": "USD", "symbol": "$", "rate": 7.2,
        "vat_name": "Sales Tax", "vat_rate": 0,
        "min_purchase": 0, "min_purchase_cny": 0,
        "refund_rate": 0, "deduction": 0,
        "method": "无退税",
        "notes": "⚠️ 美国没有联邦VAT/Sales Tax退税政策。国际旅客无法退消费税。部分州(如Oregon/Delaware)本身无消费税。纽约/加州约8-10%消费税不可退。",
        "steps": ["美国无退税政策"],
        "tips": ["去免税州购物(Oregon/Delaware/New Hampshire)", "纽约/加州消费税8-10%不可退", "Outlets折扣通常已抵消消费税"],
    },
    "加拿大": {
        "currency": "CAD", "symbol": "C$", "rate": 5.3,
        "vat_name": "GST/HST", "vat_rate": 5,
        "min_purchase": 0, "min_purchase_cny": 0,
        "refund_rate": 0, "deduction": 5,
        "method": "已取消退税",
        "notes": "⚠️ 加拿大于2007年取消访客退税计划。国际旅客不再享受GST/HST退税。",
        "steps": ["加拿大已无退税政策"],
        "tips": ["加拿大不退税，关注折扣和免税日"],
    },
}


def cmd_calc(country, amount, currency="local"):
    """计算退税金额"""
    if country not in COUNTRIES:
        matched = [c for c in COUNTRIES if country in c]
        if not matched:
            available = "、".join(sorted(COUNTRIES.keys()))
            return json.dumps({
                "status": "error",
                "message": f"暂不支持「{country}」，目前支持：{available}"
            }, ensure_ascii=False)
        country = matched[0]

    c = COUNTRIES[country]

    # 特殊处理：无退税国家
    if c["refund_rate"] == 0 and "取消" in c.get("method", ""):
        output = f"🚫 **{country}退税状态**\n\n"
        output += f"⚠️ {c['notes']}\n\n"
        if c.get("tips"):
            output += "💡 **替代建议**：\n\n"
            for tip in c["tips"]:
                output += f"- {tip}\n"
        return output

    if c["refund_rate"] == 0:
        output = f"🚫 **{country}退税状态**\n\n"
        output += f"⚠️ {c['notes']}\n\n"
        if c.get("tips"):
            output += "💡 **替代建议**：\n\n"
            for tip in c["tips"]:
                output += f"- {tip}\n"
        return output

    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return json.dumps({"status": "error", "message": "金额必须为数字"}, ensure_ascii=False)

    # 金额转换
    if currency == "CNY":
        local_amount = amount / c["rate"]
        cny_amount = amount
    else:
        local_amount = amount
        cny_amount = amount * c["rate"]

    # 是否达到起退点
    is_eligible = local_amount >= c["min_purchase"]
    
    # 计算退税
    vat_amount = local_amount * c["vat_rate"] / 100
    refund_amount = local_amount * c["refund_rate"] / 100
    refund_cny = refund_amount * c["rate"]

    output = f"💰 **{country}退税计算**\n\n"
    output += f"**消费金额**：{local_amount:,.0f} {c['symbol']}（≈¥{cny_amount:,.0f}）\n\n"

    if not is_eligible:
        output += f"❌ **未达到起退金额**\n\n"
        output += f"起退金额：{c['min_purchase']:,.0f} {c['symbol']}（≈¥{c['min_purchase_cny']:,.0f}）\n"
        output += f"还差：{c['min_purchase'] - local_amount:,.0f} {c['symbol']}\n\n"
        output += f"💡 继续在同店铺购物凑满起退额即可退税\n"
        return output

    output += "---\n\n"
    output += "## 📊 退税明细\n\n"
    output += f"| 项目 | 金额 |\n|------|------|\n"
    output += f"| 消费金额 | {local_amount:,.0f} {c['symbol']} |\n"
    output += f"| {c['vat_name']}({c['vat_rate']}%) | {vat_amount:,.0f} {c['symbol']} |\n"
    output += f"| 退税手续费({c['deduction']}%) | {local_amount * c['deduction'] / 100:,.0f} {c['symbol']} |\n"
    output += f"| **实际到手退税** | **{refund_amount:,.0f} {c['symbol']}（≈¥{refund_cny:,.0f}）** |\n\n"

    output += f"## 📋 退税政策\n\n"
    output += f"- **税种**：{c['vat_name']} {c['vat_rate']}%\n"
    output += f"- **起退金额**：{c['min_purchase']:,.0f} {c['symbol']}\n"
    output += f"- **实际退税率**：{c['refund_rate']}%（扣手续费后）\n"
    output += f"- **退税方式**：{c['method']}\n\n"

    output += f"## 📝 退税流程\n\n"
    for i, step in enumerate(c["steps"], 1):
        output += f"{i}. {step}\n"
    output += "\n"

    if c.get("tips"):
        output += "## 💡 省钱技巧\n\n"
        for tip in c["tips"]:
            output += f"- {tip}\n"
        output += "\n"

    output += f"📌 {c['notes']}\n"

    return output


def cmd_policy(country=None):
    """查询退税政策"""
    if country:
        if country not in COUNTRIES:
            matched = [c for c in COUNTRIES if country in c]
            if not matched:
                return json.dumps({"status": "error", "message": f"未找到「{country}」"}, ensure_ascii=False)
            country = matched[0]
        
        c = COUNTRIES[country]
        output = f"📋 **{country}退税政策详情**\n\n"
        output += f"- **税种**：{c['vat_name']} {c['vat_rate']}%\n"
        output += f"- **起退金额**：{c['min_purchase']:,.0f} {c['symbol']}（≈¥{c['min_purchase_cny']:,}）\n"
        output += f"- **实际退税率**：{c['refund_rate']}%\n"
        output += f"- **手续费**：{c['deduction']}%\n"
        output += f"- **退税方式**：{c['method']}\n\n"
        output += f"**详细说明**：{c['notes']}\n\n"
        
        if c.get("steps"):
            output += "**退税流程**：\n\n"
            for i, step in enumerate(c["steps"], 1):
                output += f"{i}. {step}\n"
            output += "\n"
        
        if c.get("tips"):
            output += "**省钱技巧**：\n\n"
            for tip in c["tips"]:
                output += f"- {tip}\n"
        return output

    # 全部政策概览
    output = "🌍 **全球退税政策一览**\n\n"
    output += "| 国家 | 税率 | 起退额 | 实际退率 | 方式 |\n|------|------|--------|---------|------|\n"
    
    for name, c in sorted(COUNTRIES.items(), key=lambda x: x[1]["vat_rate"], reverse=True):
        rate_str = f"{c['vat_rate']}%" if c['vat_rate'] > 0 else "无退税"
        min_str = f"{c['min_purchase']:,.0f}{c['symbol']}" if c['min_purchase'] > 0 else "无"
        refund_str = f"{c['refund_rate']}%" if c['refund_rate'] > 0 else "—"
        method = c['method'][:15] if len(c['method']) > 15 else c['method']
        output += f"| {name} | {rate_str} | {min_str} | {refund_str} | {method} |\n"
    output += "\n"

    # 退税金额最高的国家
    refund_countries = [(n, c) for n, c in COUNTRIES.items() if c["refund_rate"] > 0]
    refund_countries.sort(key=lambda x: x[1]["refund_rate"], reverse=True)
    
    output += "🏆 **退税最划算国家TOP5**：\n\n"
    for n, c in refund_countries[:5]:
        output += f"- **{n}**：退{c['refund_rate']}%（消费¥10000约退¥{10000*c['refund_rate']/100*c['rate']/c['rate']:,.0f}）\n"
    output += "\n"

    # 警告：无退税国家
    no_refund = [n for n, c in COUNTRIES.items() if c["refund_rate"] == 0]
    if no_refund:
        output += f"⚠️ **无退税/已取消退税**：{'、'.join(no_refund)}\n"

    return output


# ========== 主入口 ==========
def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "status": "error",
            "message": "用法: tax_refund_calculator.py <command> [args]\n命令: calc <国家> <金额> [CNY] | policy [国家]"
        }, ensure_ascii=False))
        return

    command = sys.argv[1]

    if command == "calc":
        if len(sys.argv) < 4:
            print(json.dumps({"status": "error", "message": "用法: calc <国家> <金额> [CNY/local]"}, ensure_ascii=False))
            return
        country = sys.argv[2]
        amount = sys.argv[3]
        currency = sys.argv[4] if len(sys.argv) > 4 else "local"
        print(cmd_calc(country, amount, currency))

    elif command == "policy":
        country = sys.argv[2] if len(sys.argv) > 2 else None
        print(cmd_policy(country))

    else:
        print(json.dumps({
            "status": "error",
            "message": f"未知命令: {command}\n支持: calc | policy"
        }, ensure_ascii=False))


if __name__ == "__main__":
    main()
