#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
policy_review.py — 家庭保单检视表（保单体检）

输入：JSON 文件，或直接传若干张保单（--policy 重复传）。
输出：① 家庭保单检视表（一单一行 + 全家汇总）
      ② 缺口与待办清单（三类缺口 + 三条纪律检查）
      ③ 可直接喂给预算试算的「已有保费支出」数字

单张保单字段（JSON 数组里每个对象）：
    who        谁（被保险人，被保障的人）          必填
    type       险种：百万医疗/重疾/意外/定寿/储蓄/其他  必填
    amount     保额（元）                          可空
    premium    年缴保费（元）                       可空
    pay_years  缴费期（年），"缴至X岁"写字符串       可空
    until      保到什么时候（"保到70岁"/"终身"/"1年"）可空
    due        缴费日（如 "03-15"）                 可空
    phone      报案电话                             可空
    beneficiary 受益人（"名字"/"法定"/空）           可空
    paid_last_year 去年是否扣款成功（true/false/null）可空

用法：
    python3 policy_review.py --input policies.json --output review.md
    python3 policy_review.py --income 30 --input policies.json --output review.md
    python3 policy_review.py --demo                      # 打印内置示例（合成数据）

退出码：0 = 正常；1 = 输入不合法
"""

import argparse
import json
import sys

FOOTER = (
    "> 本文为保险通识教育内容，不构成投保建议；"
    "一切以保险条款原文、保险公司核保理赔结论及监管规定为准。"
)

# 四件套（保障类）
FOUR = ["百万医疗", "意外", "重疾", "定寿"]

ALIASES = {
    "医疗": "百万医疗", "百万医疗险": "百万医疗", "医疗险": "百万医疗", "住院医疗": "百万医疗",
    "重疾险": "重疾", "重大疾病": "重疾", "重大疾病险": "重疾",
    "意外险": "意外", "意外伤害": "意外",
    "定期寿险": "定寿", "寿险": "定寿", "定寿": "定寿",
    "年金": "储蓄", "增额终身寿": "储蓄", "理财": "储蓄", "储蓄型": "储蓄",
}

DEMO = [
    {"who": "本人", "type": "重疾", "amount": 300000, "premium": 6800, "pay_years": "20年",
     "until": "终身", "due": "05-18", "phone": "95XXX", "beneficiary": "法定",
     "paid_last_year": True},
    {"who": "本人", "type": "百万医疗", "amount": 2000000, "premium": 890, "pay_years": "1年",
     "until": "1年", "due": "05-18", "phone": "95XXX", "beneficiary": "",
     "paid_last_year": True},
    {"who": "孩子", "type": "重疾", "amount": 500000, "premium": 2400, "pay_years": "20年",
     "until": "终身", "due": "09-02", "phone": "95XXX", "beneficiary": "法定",
     "paid_last_year": False},
]


def norm_type(t):
    t = (t or "").strip()
    return ALIASES.get(t, t or "其他")


def wan(n):
    """
    金额显示成人话。输入一律按「元」解释，但也容错两种常见写法：
        6800 / "6800" / "6800元"  → 6,800
        "50万" / "50w"            → 50.0 万
        50（保额字段且 < 1000）    → 视为 50 万，避免把 50 万写成 50 元
    """
    if n in (None, "", 0):
        return "—"
    if isinstance(n, str):
        s = n.strip().replace(",", "")
        if s.endswith("万") or s.lower().endswith("w"):
            try:
                return "{:.1f} 万".format(float(s.rstrip("万wW")) )
            except ValueError:
                return n
        s = s.replace("元", "")
        try:
            n = float(s)
        except ValueError:
            return n
    try:
        n = float(n)
    except (TypeError, ValueError):
        return str(n)
    if n >= 10000:
        return "{:.1f} 万".format(n / 10000.0)
    return "{:,.0f}".format(n)


def wan_amount(n):
    """保额专用：数字 < 1000 的按「万元」理解（用户口述保额常说"50 万"就写 50）"""
    if isinstance(n, (int, float)) and 0 < n < 1000:
        n = n * 10000
    return wan(n)


def to_yuan(n):
    """把「6800 / "6800" / "6800元" / "0.68万"」统一成元（int），取不到就返回 0。"""
    if n in (None, ""):
        return 0
    if isinstance(n, (int, float)):
        return int(n)
    s = str(n).strip().replace(",", "").replace("元", "")
    try:
        if s.endswith("万") or s.lower().endswith("w"):
            return int(float(s.rstrip("万wW")) * 10000)
        return int(float(s))
    except ValueError:
        return 0


def build(policies, income=None):
    rows, total = [], 0
    missing = []

    for i, p in enumerate(policies, 1):
        who = (p.get("who") or "未填").strip()
        t = norm_type(p.get("type"))
        amount = p.get("amount")
        premium = p.get("premium")
        total += to_yuan(premium)
        for f in ("amount", "premium", "until", "due", "phone"):
            if p.get(f) in (None, "", 0):
                missing.append((i, who, t, f))
        rows.append([
            who, t, wan_amount(amount), wan(premium),
            p.get("pay_years") or "—",
            p.get("until") or "—",
            p.get("due") or "—",
            p.get("phone") or "—",
            p.get("beneficiary") or "—",
        ])

    out = []
    out.append("# 家庭保单检视表")
    out.append("")
    out.append("> 一单一行。**这张表要交给一个家人**——出事那天，它是全家最有用的一张纸。")
    out.append("")

    # 总判断（结论先行）
    covered = {norm_type(p.get("type")) for p in policies}
    people = {p.get("who") for p in policies if p.get("who")}
    lack = [k for k in FOUR if k not in covered]
    if lack:
        out.append("**总判断**：全家共 {} 张、{} 人，四件套里还缺 **{}** 这几类。".format(
            len(policies), len(people), "、".join(lack)))
    else:
        out.append("**总判断**：全家共 {} 张、{} 人，四件套都有人配上了。".format(
            len(policies), len(people)))
    out.append("")

    # 主表
    head = ["谁", "什么险", "保额（最多赔多少）", "年缴（一年交多少）", "缴费期",
            "到期/保到", "缴费日", "报案电话", "受益人（谁拿钱）"]
    out.append("| " + " | ".join(head) + " |")
    out.append("|" + "---|" * len(head))
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    out.append("| **全家合计** | {} 张 | — | **{}** | — | — | — | — | — |".format(
        len(policies), wan(total)))
    out.append("")

    # 缺口
    out.append("## 缺口与待办")
    out.append("")
    gaps = []
    if lack:
        gaps.append("- **类缺**：{} 这几类还没有。先说清优先级，不必急着补齐。".format(
            "、".join(lack)))
    # 人缺：四件套里只有孩子有、大人没有
    adults = {p.get("who") for p in policies
              if p.get("who") and p.get("who") not in ("孩子", "儿子", "女儿", "子女")}
    kids = {p.get("who") for p in policies
            if p.get("who") in ("孩子", "儿子", "女儿", "子女")}
    if kids and not adults:
        gaps.append("- **人缺**：现在只有孩子的保障，家里赚钱的人一张都没有——**先保赚钱的人**。")
    if not gaps:
        gaps.append("- 没发现整类空缺。")
    out.extend(gaps)
    out.append("")

    # 纪律检查
    out.append("## 三条纪律检查")
    out.append("")
    unpaid = [p for p in policies if p.get("paid_last_year") is False]
    if unpaid:
        names = "、".join("{}({})".format(p.get("who") or "未填", norm_type(p.get("type")))
                         for p in unpaid)
        out.append("- ⚠️ **去年可能没扣款成功**：{}。先去银行流水里搜一下扣款记录；"
                   "真漏了，趁**宽限期（忘交保费后的补救时间）**补上，这段时间内出事通常照样能赔。".format(names))
    else:
        out.append("- ✅ **缴费**：没有标记为漏交的保单（建议每年自己再核一次银行流水）。")

    legal = [p for p in policies if (p.get("beneficiary") or "").strip() == "法定"]
    if legal:
        out.append("- ⚠️ **受益人写的是「法定」**：涉及 {} 张。只写法定，将来按遗产处理，"
                   "**手续更麻烦**；建议改成具体名字。".format(len(legal)))
    else:
        out.append("- ✅ **受益人**：没有只写「法定」的保单。")

    out.append("- **家人知不知道**：把这张表打印一份，交给一个家人，或存一份在手机备忘录里。")
    out.append("")

    # 待补
    if missing:
        out.append("## 需要你回去补的几栏")
        out.append("")
        label = {"amount": "保额（出事了最多赔你多少）", "premium": "年缴保费（你交的钱）",
                 "until": "到期/保到什么时候", "due": "缴费日", "phone": "报案电话"}
        for i, who, t, f in missing[:20]:
            out.append("- 第 {} 张（{} · {}）：缺 **{}**".format(i, who, t, label.get(f, f)))
        out.append("")

    # 喂给预算
    out.append("## 已有保费支出（保费＝你交的钱；可直接用于预算试算）")
    out.append("")
    out.append("全家年缴合计：**{}**（{} 元/年）".format(wan(total), total))
    if income:
        try:
            inc = float(str(income).replace("万", ""))
            ratio = total / (inc * 10000.0)
            out.append("")
            out.append("占家庭年收入（约 {} 万）：**{:.1%}**".format(inc, ratio))
            if ratio > 0.20:
                out.append("")
                out.append("> 已超过 **15%-20% 的警戒线** → **先别加保**，先看这张表里有没有该减的。")
            elif ratio > 0.10:
                out.append("")
                out.append("> 已在经验区间的上沿（5%-10% 之上）→ 加保空间有限，先谈优先级。")
            else:
                out.append("")
                out.append("> 在经验区间内。还有空间可以往上加，但不必加满。")
        except ValueError:
            pass
    out.append("")
    out.append("> 下一步：把这笔「已有保费支出」拿去跑预算试算（买什么 → `budget_calc.py --existing {}`）。".format(total))
    out.append("")

    out.append("## 你现在可以做的一步")
    out.append("")
    out.append("把上面缺的几栏补上，再把这张表**发给一个家人**——这一步做完，体检就算完成了大半。")
    out.append("")
    out.append("---")
    out.append("")
    out.append(FOOTER)
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="家庭保单检视表（保单体检）")
    ap.add_argument("--input", help="JSON 文件：保单数组")
    ap.add_argument("--income", help="家庭年收入（万元），用于计算保费占比")
    ap.add_argument("--output", help="输出到文件（默认打印到屏幕）")
    ap.add_argument("--demo", action="store_true", help="打印内置示例结果（合成数据）")
    args = ap.parse_args()

    if args.demo:
        body = build(DEMO, args.income or "30")
        print(body)
        return 0

    if not args.input:
        print("[还差点东西] 保单体检需要你先把手上每张保单写成一张小卡片。\n"
              "  最简单的办法是先看看成品长什么样：\n"
              "    --demo\n"
              "  想直接算自己家的，把保单写进一个 json 文件，最少填这四样：\n"
              '    [{"who": "本人", "type": "重疾", "amount": 300000, "premium": 6800}]\n'
              "      who     给谁买的（本人 / 配偶 / 孩子 / 老人）\n"
              "      type    什么险（重疾 / 百万医疗 / 意外 / 定寿）\n"
              "      amount  保额，单位元（30 万就写 300000；写 30 也行）\n"
              "      premium 一年交多少，单位元\n"
              "  填好之后这样跑：\n"
              "    --input 我的保单.json\n"
              "  填不全也没关系，缺的那栏会空着提醒你补。",
              file=sys.stderr)
        return 1

    try:
        with open(args.input, encoding="utf-8") as f:
            policies = json.load(f)
    except FileNotFoundError:
        print("[找不到文件] 没有这个文件：{}\n"
              "  多半是路径不对，两个办法：\n"
              "    · 把文件直接拖进这个窗口，会自动填上正确路径\n"
              "    · 或者放到当前目录，用文件名就行：--input 我的保单.json".format(args.input),
              file=sys.stderr)
        return 1
    except IsADirectoryError:
        print("[这是个文件夹] 「{}」是个目录，不是文件。\n"
              "  请指向里面的那个 .json 文件，例如：--input {}/我的保单.json".format(
                  args.input, args.input),
              file=sys.stderr)
        return 1
    except UnicodeDecodeError:
        print("[编码不对] 文件里的中文读不出来。\n"
              "  用记事本打开 → 另存为 → 编码选「UTF-8」→ 保存，再来一次。",
              file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print("[格式不对] 这个文件不是标准的 json，第 {} 行第 {} 列附近出了问题。\n"
              "  小白最常踩的三个坑：\n"
              "    1. 用了中文引号（“”）→ 全部换成英文引号（\"）\n"
              "    2. 两张保单之间有逗号没写 → 要写成 }},{{\n"
              "    3. 最后多了一个逗号 → 删掉最后的 ,\n"
              "  不想折腾的话，直接 --demo 看一份成品，照着改。".format(e.lineno, e.colno),
              file=sys.stderr)
        return 1
    except OSError as e:
        print("[没读进来] 这个文件打不开：{}\n"
              "  如果是权限问题，把它复制到桌面再试一次。".format(e.strerror or e),
              file=sys.stderr)
        return 1

    if not isinstance(policies, list) or not policies:
        print("[格式对不上] 文件读进来了，但里面不是一类保单列表。\n"
              "  最外层应该是方括号，里面每张保单用花括号：\n"
              '    [{"who": "本人", "type": "重疾", "amount": 300000, "premium": 6800},\n'
              '     {"who": "孩子", "type": "意外", "amount": 200000, "premium": 300}]\n'
              "  如果你写的是 {\"policies\": [...]} 这种包了一层，把外层去掉就行。",
              file=sys.stderr)
        return 1

    body = build(policies, args.income)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(body + "\n")
        print("[完成] 保单检视表已写入 {}".format(args.output))
    else:
        print(body)
    return 0


if __name__ == "__main__":
    sys.exit(main())
