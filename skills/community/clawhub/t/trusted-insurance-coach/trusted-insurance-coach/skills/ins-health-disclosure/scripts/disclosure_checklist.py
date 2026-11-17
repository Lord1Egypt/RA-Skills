#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
disclosure_checklist.py — 投保前核对清单生成器（健康告知陪审）

作用：把"险种 + 角色 + 体况口述"变成一份逐项勾的核对清单。
边界：只做清单，不做判断、不做结论、不评价体况、不推荐产品、不给价格。

用法：
    python3 disclosure_checklist.py --insurance-type 百万医疗 --role 本人 \
        --findings "甲状腺结节; 5年前阑尾炎手术" --output checklist.md

    # 病历/体检报告找不到时（口述降级分支）：
    python3 disclosure_checklist.py --insurance-type 重疾 --role 本人 --mode oral

参数：
    --insurance-type   百万医疗 / 重疾 / 意外 / 定寿（默认：未指定，给通用版）
    --role             本人 / 配偶 / 孩子 / 老人 / 孕妇（默认：本人）
    --findings         体况口述，分号分隔（可为空）
    --mode             full=按材料逐项核对（默认）；oral=口述降级（逐项标【未核实】）
    --output           输出文件路径（默认打印到标准输出）
"""

import argparse
import sys
from datetime import date

# ---------------------------------------------------------------- 材料清单骨架

# 通用：任何险种都要核对的材料
GENERAL_ITEMS = [
    ("近 2-5 年体检报告", "翻'异常汇总/建议复查'页 + 影像与超声结论（结节、息肉、囊肿、占位、磨玻璃影都算）"),
    ("门诊病历 / 电子病历", "看'诊断'栏；医生写了才算，自己觉得不算"),
    ("住院与手术记录", "出院小结最权威；剖腹产、日间手术、内镜治疗都算手术"),
    ("用药记录", "连续服药超过题目天数的都要；用国家医保服务平台 App 查购药记录"),
    ("医保卡使用记录", "有没有不是你自己看病的记录（外借项必查）"),
    ("既往投保与核保史", "是否被拒保/延期/加费/除外过；行业信息共享，瞒不住"),
]

# 按险种追加
BY_INSURANCE_TYPE = {
    "百万医疗": [
        ("全部影像与化验报告原件", "医疗险告知最严，结节分级、大小、随访情况都要能说清"),
        ("随访/复查记录", "医生建议'定期复查'的，把每次复查结果按时间排列"),
    ],
    "重疾": [
        ("病理与确诊材料", "涉及肿瘤类的一律以病理报告为准"),
        ("慢病管理记录", "高血压/糖尿病等的诊断时间、用药与并发症"),
    ],
    "意外": [
        ("职业与实际工作内容", "按实际工作内容填，不是按名片；兼职高风险活动也要说"),
        ("既往伤残与既往理赔", "意外险主要看职业与既往伤残"),
    ],
    "定寿": [
        ("负债与收入情况（用于保额思路）", "保额是通用算法，不是本清单的判断项"),
        ("既往重大病史", "与医疗/重疾口径一致，按题目时间窗"),
    ],
}

# 按角色追加
BY_ROLE = {
    "本人": [],
    "配偶": [],
    "孩子": [
        ("出生证明（孕周、出生体重）", "是否早产（<37周）、低出生体重（<2.5kg）——必须查出证明，不能凭记忆"),
        ("儿童保健手册 / 预防接种证", "发育评估、既往住院与就诊时间线"),
        ("先天性疾病与遗传病相关记录", "按问卷列举如实答，不确定就不编"),
    ],
    "老人": [
        ("慢病随访记录（血压、血糖等）", "老人投保慢病几乎必问，准备近期的复查结果"),
        ("近期住院与手术记录", "时间窗内的一律如实"),
    ],
    "孕妇": [
        ("产检手册（孕周）", "孕周是必问项，'先买了再说'是坑"),
        ("妊娠期并发症记录", "妊娠糖尿病/高血压等，按问卷如实"),
    ],
}

# 体况关键词 → 针对性的核对动作
FINDING_RULES = [
    ("结节", "翻出报告原话：位置、大小（如 3mm）、分级（甲状腺 TI-RADS / 乳腺 BI-RADS）、医生建议；按原话描述"),
    ("磨玻璃", "肺 CT 的'检查结论'与'建议'栏；是否随访、有无变化"),
    ("息肉", "部位、大小、病理结果（有没有做过活检/切除）"),
    ("囊肿", "部位、大小、医生是否建议处理"),
    ("增生", "注意：'增生'与'结节'不是一回事，按报告原话分别描述"),
    ("高血压", "诊断时间、最高值、是否服药、有无并发症"),
    ("糖尿病", "类型、确诊时间、用药、有无并发症"),
    ("手术", "手术时间、术式、出院小结、病理结果（如有）"),
    ("住院", "入院与出院时间、医院名称、出院诊断"),
    ("外借", "医保卡外借：外借时间、对象、大致病种，并准备自证材料"),
    ("拒保", "被拒时间、公司类型、原因、后续复查情况"),
    ("复查", "'被建议复查'本身就是要告知的内容，别因为'后来没事'就不说"),
]


def build_checklist(insurance_type: str, role: str, findings: list, mode: str) -> str:
    is_oral = mode == "oral"
    unverified = "【未核实】" if is_oral else ""
    today = date.today().isoformat()

    lines = []
    lines.append(f"# 投保前核对清单（{'不完整版 · 口述记录' if is_oral else '按材料逐项核对'}）")
    lines.append("")
    lines.append(f"- 生成日期：{today}")
    lines.append(f"- 险种：{insurance_type or '未指定（通用版）'} ｜ 被保人角色：{role}")
    lines.append(f"- 模式：{mode}（{'材料不可得，以下各项为口述记录' if is_oral else '正式投保前按材料逐项核对'}）")
    lines.append("")
    lines.append("> 这份清单只告诉你**去翻什么、看哪个字段**；怎么答由你自己决定，最终以保险公司的核保结论为准。")
    lines.append("> 判断依据只有三样：**你的材料、问卷原文、条款**。不是记忆，也不是销售的口头承诺。")
    lines.append("")

    if is_oral:
        lines.append("## ⚠️ 口述降级说明")
        lines.append("")
        lines.append("你说暂时拿不到病历/体检报告，所以下面是**不完整版清单**，每项标 `【未核实】`。")
        lines.append("**口述内容不能替代材料**——正式投保前必须补齐核对，材料与口述不一致时以材料为准。")
        lines.append("")
        lines.append("### 补打病历的三条途径")
        lines.append("")
        lines.append("1. **医院病案室复印**：带本人身份证（代办需双方身份证 + 委托书）到就诊医院病案室/医务科申请；")
        lines.append("2. **医院公众号 / 小程序 / App**：在'就诊记录 / 报告查询'里调阅电子病历与检查报告；")
        lines.append("3. **区域电子健康档案 + 医保消费记录**：地方健康云类平台查历史就诊；国家医保服务平台 App 查医保消费记录（用来回忆时间线）。")
        lines.append("")

    lines.append("## 一、逐项核对清单")
    lines.append("")
    lines.append("| # | 材料 / 项目 | 看什么（关键字段） | 核对结果 |")
    lines.append("|---|---|---|---|")

    idx = 0
    items = list(GENERAL_ITEMS)
    items += BY_INSURANCE_TYPE.get(insurance_type, [])
    items += BY_ROLE.get(role, [])
    for name, how in items:
        idx += 1
        lines.append(f"| {idx} | {unverified}{name} | {how} | ☐ 已核对 / ☐ 待核对 |")

    findings = [f.strip() for f in findings if f and f.strip()]
    if findings:
        lines.append("")
        lines.append("## 二、针对你提到的体况（逐条找材料）")
        lines.append("")
        for f in findings:
            lines.append(f"### 体况：{f}")
            lines.append("")
            matched = [tip for kw, tip in FINDING_RULES if kw in f]
            if matched:
                for tip in matched:
                    lines.append(f"- {unverified}{tip}")
            else:
                lines.append(f"- {unverified}找到与'{f}'对应的门诊/住院病历或体检报告，抄下**诊断原话 + 时间 + 医生建议**")
            lines.append(f"- {unverified}确认问卷里的**时间窗**（最近 2 年 / 5 年 / 曾经），按题目的窗去翻，别自己扩大或缩小")
            lines.append("")

    lines.append("## 三、答题纪律（答之前再看一遍）")
    lines.append("")
    lines.append("1. **问什么答什么**：没问的不用主动说，问到的一定如实答；")
    lines.append("2. **以材料为准**：'医生说没事''我自己觉得不严重'都不能当作'没有'的依据；")
    lines.append("3. **不代填**：答案只能你自己勾，任何让你'都填否'的说法都别信；")
    lines.append("4. **不确定就走核保**：拿不准的体况走智能核保（匿名，不留记录）或预核保，不凭感觉选；")
    lines.append("5. **留存证据**：把这次核对用的材料与问卷截图存一个文件夹，理赔时就是你最硬的底。")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("> 本文为保险通识教育内容，不构成投保建议；一切以保险条款原文、保险公司核保理赔结论及监管规定为准。")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="投保前核对清单生成器（只做清单，不做判断）")
    parser.add_argument("--insurance-type", default="", help="百万医疗 / 重疾 / 意外 / 定寿")
    parser.add_argument("--role", default="本人", help="本人 / 配偶 / 孩子 / 老人 / 孕妇")
    parser.add_argument("--findings", default="", help="体况口述，分号分隔")
    parser.add_argument("--mode", default="full", choices=["full", "oral"], help="full=按材料核对；oral=口述降级")
    parser.add_argument("--output", default="", help="输出文件路径（默认打印到标准输出）")
    args = parser.parse_args()

    # 角色必须认得，否则会静默漏掉这个角色专属的核对项
    if args.role not in BY_ROLE:
        print(f"[没认出来] 被保人角色「{args.role}」我这边没对上。\n"
              f"  能处理这五种：\n"
              f"    本人 / 配偶 / 孩子 / 老人 / 孕妇\n"
              f"  不确定就填「本人」——本人这套核对项最全，先按这个走不会错。\n"
              f"  例：--role 本人",
              file=sys.stderr)
        return 2

    findings = [x for x in args.findings.replace("，", ";").replace("；", ";").split(";")]
    text = build_checklist(args.insurance_type, args.role, findings, args.mode)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fp:
            fp.write(text)
        print(f"已生成：{args.output}")
    else:
        print(text)


if __name__ == "__main__":
    sys.exit(main())
