#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
claim_checklist.py — 理赔材料清单生成器（理赔怎么办）

作用：把"险种 + 事故类型 + 就医情况"变成一份逐项勾的材料清单 + 时限提醒 + 常见漏项提示。
边界：只做清单与路径，不做结果判断、不承诺赔付、不代写申请书、不代办。

用法：
    python3 claim_checklist.py --insurance-type 百万医疗 --event 住院 --output claim_materials.md

    # 材料暂时不齐（降级分支）：
    python3 claim_checklist.py --insurance-type 重疾 --event 确诊重大疾病 --mode oral

参数：
    --insurance-type   百万医疗 / 重疾 / 意外 / 定寿 / 小额医疗
    --event            住院 / 门诊 / 确诊重大疾病 / 身故 / 伤残 / 意外医疗
    --hospital         就诊医院情况（可选，用于提示医院等级要求）
    --mode             full=完整清单（默认）；oral=材料不齐时的不完整版（逐项标【待补】）
    --output           输出文件路径（默认打印到标准输出）
"""

import argparse
import sys
from datetime import date

# ---------------------------------------------------------------- 清单骨架

GENERAL = [
    ("理赔申请书", "按保险公司格式填写，本人签字（格式与要点可以讲，内容不代写）"),
    ("申请人身份证明", "被保险人（被保障的人）/ 受益人（拿赔款的人）的身份证件"),
    ("领款银行卡", "开户行、户名、账号；户名须与领款人一致"),
    ("保单信息确认", "确认合同有效、在保障期内、本年度保费已交"),
]

BY_EVENT = {
    "住院": [
        ("住院病历 / 出院小结", "出院时向病案室申请，含入院记录、手术记录（如有）"),
        ("诊断证明（盖章）", "通常要求医院盖章，交之前检查一遍"),
        ("发票原件 + 费用总清单", "**报销型医疗险的核心凭证**，缺一不可"),
        ("医保结算单", "医保报销过的必须提供"),
        ("检查 / 检验报告", "影像、化验、病理（如有）"),
    ],
    "门诊": [
        ("门诊病历（每次）", "不能只交最后一次，每次就诊都要"),
        ("发票原件 + 费用明细", "逐次对应"),
        ("检查 / 检验报告", "按就诊时间排列"),
        ("诊断证明", "按保险公司要求提供"),
    ],
    "确诊重大疾病": [
        ("病理报告 / 确诊材料", "肿瘤类必须有病理报告"),
        ("影像与检验报告", "支撑确诊依据"),
        ("出院小结 / 门诊病历", "完整就诊经过"),
        ("诊断证明（盖章）", "注明确诊病种与时间"),
        ("手术记录（如有）", "部分病种以实施约定手术为给付条件"),
    ],
    "身故": [
        ("死亡医学证明", "医疗机构或公安机关出具"),
        ("户籍注销证明", "公安出具"),
        ("丧葬证明（视要求）", "按保险公司要求"),
        ("受益人身份证明 + 关系证明", "户口本、公证书等，按要求提供"),
        ("事故证明（若涉意外）", "如交通事故认定书、警方证明"),
    ],
    "伤残": [
        ("伤残鉴定报告", "**按条款约定的鉴定标准与鉴定机构做**，别随便找一家"),
        ("事故证明", "时间、地点、经过"),
        ("完整就诊材料", "门诊病历、住院记录、影像报告"),
    ],
    "意外医疗": [
        ("事故经过说明", "写清外来的、突发的、非本意的、非疾病的四个特征"),
        ("门诊 / 住院材料", "病历、诊断证明、检查报告"),
        ("发票原件 + 费用清单", "报销型凭证"),
        ("事故证明", "交通事故需认定书，其他情形按保司要求"),
    ],
}

BY_INSURANCE_TYPE = {
    "百万医疗": "报销型（花多少报多少）：注意免赔额（保险公司不赔、你自己先出的部分）与报销比例；不重复赔。",
    "小额医疗": "报销型：注意单次限额与免赔额，通常较低，看条款。",
    "重疾": "给付型：确诊即申请，看条款约定的确诊标准（部分病种需达到约定状态或实施约定手术）。",
    "意外": "意外医疗走报销，身故/伤残走给付；伤残按条款约定的伤残评定标准。",
    "定寿": "身故/全残给付；注意责任免除条款（如合同约定的特定期限内自杀等，以条款为准）。",
}

TIMING = [
    "**报案时限**：出险后尽快报案（多数条款写'及时通知'，部分写明具体天数）——以你的合同约定为准；",
    "**补正期限**：收到补材料通知要在期限内补，并保留补交通知与回执；",
    "**申请时效**：保险金请求权有诉讼时效限制（人寿保险与其他保险期间不同，自知道或应当知道保险事故发生之日起计算）——别卡时效，材料早收早完整；",
    "**结论要书面**：任何结论都要落到书面，拒赔必须写明理由与引用条款。",
]

PITFALLS = [
    "发票原件丢失：报销型理赔的核心凭证，出院结账时就要收齐；",
    "只有发票没有费用总清单：报销型通常两者都要；",
    "诊断证明没盖章：交之前检查一遍；",
    "门诊病历只交最后一次：每次就诊的都要；",
    "提交前没拍照留底：材料寄出去就回不来了；",
    "病历说法出错：跟医生讲症状和经过，不猜病名、不说'我以前就有过'。",
]

REPLENISH = [
    "**医院病案室复印**：带本人身份证（代办需双方身份证 + 委托书）复印住院病案与门诊病历；",
    "**医院公众号 / 小程序 / App**：在'就诊记录 / 报告查询'里调阅电子病历与检查报告，可导出或截图；",
    "**医保消费记录**：国家医保服务平台 App 或本地医保小程序查询（用来核对就诊时间线与医院）。",
]


def build(insurance_type: str, event: str, hospital: str, mode: str) -> str:
    is_oral = mode == "oral"
    tag = "【待补】" if is_oral else ""
    lines = []

    lines.append(f"# 理赔材料清单（{'不完整版 · 材料不齐' if is_oral else '完整版'}）")
    lines.append("")
    lines.append(f"- 生成日期：{date.today().isoformat()}")
    lines.append(f"- 险种：{insurance_type or '未指定'} ｜ 事故类型：{event or '未指定'}")
    if hospital:
        lines.append(f"- 就诊医院：{hospital}（医院等级要求以条款为准，多数为二级及以上公立医院）")
    lines.append("")
    lines.append("> 这份清单是**通用清单**，最终以保险公司给你的材料清单为准。报案时限与审核时限以你的保险合同条款为准。")
    lines.append("")

    if is_oral:
        lines.append("## ⚠️ 材料不齐说明")
        lines.append("")
        lines.append("你说有些材料一时拿不到，所以下面是**不完整版清单**，每项标 `【待补】`。")
        lines.append("补齐材料的三条途径：")
        lines.append("")
        for r in REPLENISH:
            lines.append(f"1. {r}" if r.startswith("**医院病案室") else f"2. {r}" if r.startswith("**医院公众号") else f"3. {r}")
        lines.append("")

    lines.append("## 一、通用必备")
    lines.append("")
    lines.append("| # | 材料 | 要点 | 状态 |")
    lines.append("|---|---|---|---|")
    for i, (name, how) in enumerate(GENERAL, 1):
        lines.append(f"| {i} | {tag}{name} | {how} | ☐ 已收 / ☐ 待补 |")

    items = BY_EVENT.get(event, [])
    if items:
        lines.append("")
        lines.append(f"## 二、{event}专属材料")
        lines.append("")
        lines.append("| # | 材料 | 怎么拿到 | 状态 |")
        lines.append("|---|---|---|---|")
        for i, (name, how) in enumerate(items, 1):
            lines.append(f"| {i} | {tag}{name} | {how} | ☐ 已收 / ☐ 待补 |")

    if insurance_type in BY_INSURANCE_TYPE:
        lines.append("")
        lines.append("## 三、这个险种的特别提示")
        lines.append("")
        lines.append(f"- {BY_INSURANCE_TYPE[insurance_type]}")

    lines.append("")
    lines.append("## 四、时限提醒（以合同约定为准）")
    lines.append("")
    for t in TIMING:
        lines.append(f"- {t}")

    lines.append("")
    lines.append("## 五、最容易漏的几项")
    lines.append("")
    for p in PITFALLS:
        lines.append(f"- {p}")

    lines.append("")
    lines.append("## 六、三条纪律")
    lines.append("")
    lines.append("1. **发票原件**是报销型的命根子，丢了补办极麻烦；")
    lines.append("2. **结论要书面**：拒赔必须写明理由与引用条款，口头答复不作数；")
    lines.append("3. **不伪造、不凑材料**：任何'补一张''这样写就能赔'的说法都是坑。")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("> 本文为保险通识教育内容，不构成投保建议；一切以保险条款原文、保险公司核保理赔结论及监管规定为准。")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="理赔材料清单生成器（只做清单，不做结果判断）")
    parser.add_argument("--insurance-type", default="", help="百万医疗 / 重疾 / 意外 / 定寿 / 小额医疗")
    parser.add_argument("--event", default="", help="住院 / 门诊 / 确诊重大疾病 / 身故 / 伤残 / 意外医疗")
    parser.add_argument("--hospital", default="", help="就诊医院情况（可选）")
    parser.add_argument("--mode", default="full", choices=["full", "oral"])
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    # 事故类型必须认得，否则会静默生成一份"少了专属材料"的清单——那比报错更危险
    if args.event and args.event not in BY_EVENT:
        print(f"[没认出来] 事故类型「{args.event}」我这边没对上。\n"
              f"  能处理这六类：\n"
              f"    住院 / 门诊 / 确诊重大疾病 / 身故 / 伤残 / 意外医疗\n"
              f"  拿不准的话，直接说「发生了什么、在哪、花了多少」，按最接近的那类给清单。\n"
              f"  例：--event 住院",
              file=sys.stderr)
        return 2

    text = build(args.insurance_type, args.event, args.hospital, args.mode)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fp:
            fp.write(text)
        print(f"已生成：{args.output}")
    else:
        print(text)


if __name__ == "__main__":
    sys.exit(main())
