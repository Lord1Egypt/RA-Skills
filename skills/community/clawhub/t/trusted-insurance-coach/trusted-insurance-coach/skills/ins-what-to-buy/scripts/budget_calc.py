#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
budget_calc.py — 家庭保费预算试算表（买什么）

输入家庭年收入、月刚性支出、已有年缴保费，输出一张能带走的试算表。
客户给不出精确数字时用 --mode rough，只输出区间与档位感（宁粗不错）。

    - 保费预算区间  = 年收入 × 5%-10%
    - 应急金预留    = 月刚性支出 × 3-6
    - 剩余可配空间  = 预算区间 − 已有年缴保费（为负 → 先体检，不加保）
    - 警戒线        = 年收入 × 15%-20%

用法：
    python3 budget_calc.py --income 30 --expense 12000 --existing 8000
    python3 budget_calc.py --income 20 --income2 15 --expense 12000   # 两口子都挣钱
    python3 budget_calc.py --income 20-40 --mode rough --output budget.md
    python3 budget_calc.py --income 30 --expense 12000 --existing 0 --output budget.md

退出码：0 = 正常；1 = 参数不合法
"""

import argparse
import sys

FOOTER = (
    "> 本文为保险通识教育内容，不构成投保建议；"
    "一切以保险条款原文、保险公司核保理赔结论及监管规定为准。"
)


_CN_DIGIT = {"零": 0, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4,
             "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
_CN_UNIT = {"十": 10, "百": 100, "千": 1000}


def _cn_num(text):
    """把口语中文数字换成阿拉伯数字（只处理 1000 以内，收入/开销场景够用）。

    "十五万" → "15万"     "三十万" → "30万"     "八" → "8"
    "二十五万" → "25万"   "一百二十万" → "120万"
    "二十到四十万" → "20到40万"
    已经只含阿拉伯数字的，原样返回。
    """
    if not text or not any(c in text for c in "零一二两三四五六七八九十百千"):
        return text

    out, i = [], 0
    n = len(text)
    while i < n:
        c = text[i]
        if c not in _CN_DIGIT and c not in _CN_UNIT:
            out.append(c)
            i += 1
            continue
        # 把连续的中文数字段落整体换算
        j = i
        while j < n and (text[j] in _CN_DIGIT or text[j] in _CN_UNIT):
            j += 1
        seg = text[i:j]
        val, cur = 0, 0
        for ch in seg:
            if ch in _CN_DIGIT:
                cur = _CN_DIGIT[ch]
            else:
                unit = _CN_UNIT[ch]
                # "十五"：前面没数字时"十"本身代表 1×10
                if cur == 0:
                    cur = 1
                val += cur * unit
                cur = 0
        val += cur
        out.append(str(val))
        i = j
    return "".join(out)


def parse_income(raw):
    """
    解析年收入，单位统一成元。三种输入都认：
        "30" / "30万" / "30W"   → 30 万
        "20-40"                 → 20~40 万
        "300000" / "300000元"   → 30 万（≥1000 视为已经是元，不再乘万）
    """
    raw = (raw or "").strip().replace(",", "").replace("，", "")
    raw = _cn_num(raw)                     # "三十万""二十五万" → "30万""25万"
    in_yuan = raw.endswith("元")
    raw = raw.replace("万", "").replace("W", "").replace("w", "").replace("元", "").strip()
    if not raw:
        return None

    def _to_yuan(s):
        v = float(s)
        if v <= 0:
            # 收入 0 / 负数不是"没钱"，多半是没填或填错了。
            # 算出一个"0 元 ～ 0 元"的预算是误导，直接让上层报错。
            raise ValueError("income must be positive")
        if in_yuan or v >= 1000:     # 已经是「元」口径
            return int(v)
        return int(v * 10000)        # 「万元」口径

    raw = raw.replace("到", "-").replace("~", "-").replace("—", "-")
    if "-" in raw:
        parts = [p.strip() for p in raw.split("-") if p.strip()]
        if len(parts) == 2:
            try:
                lo, hi = _to_yuan(parts[0]), _to_yuan(parts[1])
            except ValueError:
                return None
            if lo > hi:
                lo, hi = hi, lo
            return lo, hi
        return None
    try:
        v = _to_yuan(raw)
    except ValueError:
        return None
    return v, v


def yuan(n):
    """金额转成人话：≥1 万用「万元」一位小数，其余用「元」。"""
    if n is None:
        return "—"
    if abs(n) >= 10000:
        return "{:.1f} 万".format(n / 10000.0)
    return "{:,.0f} 元".format(n)


def build_table(income, expense, existing, rough, income2=None):
    """income: (low, high) 元；expense: 月支出 元；existing: 元；income2: 配偶年收入 (low, high) 或 None。"""
    lo, hi = income
    if income2:
        lo += income2[0]
        hi += income2[1]
    lines = []
    lines.append("# 你家保费试算表")
    lines.append("")
    lines.append("> 这是一把**尺子**，不是一个目标数字。拿它对一下你家的负债和开销。")
    lines.append("")

    # 应急金
    if expense:
        e3, e6 = expense * 3, expense * 6
        lines.append(
            "- **应急金（先留够，再谈保费）**：月刚性支出 {:,} 元 × 3-6 = **{} ～ {}**".format(
                expense, yuan(e3), yuan(e6)
            )
        )
        if rough:
            lines.append("  - 应急金没留够之前，先把这笔留出来，别急着交保费。")
    else:
        lines.append("- **应急金（先留够，再谈保费）**：你还没说每月固定要花多少，先估一个 3-6 个月的数。")

    # 预算区间
    if rough:
        lines.append(
            "- **保费预算区间**：年收入 × 5%-10%，即 **{} ～ {}**".format(
                yuan(int(lo * 0.05)), yuan(int(hi * 0.10))
            )
        )
        lines.append(
            "- **警戒线**：总保费（你交的钱）超过年收入 15%-20% 就要降档，即 **{} ～ {}** 之外".format(
                yuan(int(lo * 0.15)), yuan(int(hi * 0.20))
            )
        )
    else:
        mid = (lo + hi) // 2
        if income2:
            m1 = (income[0] + income[1]) // 2
            m2 = (income2[0] + income2[1]) // 2
            lines.append(
                "- **保费预算区间**：家庭年收入约 {}（你 {} + 配偶 {}）→ **{} ～ {}**".format(
                    yuan(mid), yuan(m1), yuan(m2), yuan(int(mid * 0.05)), yuan(int(mid * 0.10))
                )
            )
        else:
            lines.append(
                "- **保费预算区间**：年收入约 {} → **{} ～ {}**".format(
                    yuan(mid), yuan(int(mid * 0.05)), yuan(int(mid * 0.10))
                )
            )
        lines.append(
            "- **警戒线**：总保费（你交的钱）超过 **{} ～ {}** 就要降档".format(
                yuan(int(mid * 0.15)), yuan(int(mid * 0.20))
            )
        )

    # 已有支出与剩余空间
    if existing is not None and existing > 0:
        base_lo, base_hi = (int(lo * 0.05), int(hi * 0.10)) if rough else (
            int(((lo + hi) // 2) * 0.05),
            int(((lo + hi) // 2) * 0.10),
        )
        room_lo, room_hi = base_lo - existing, base_hi - existing
        lines.append("- **已有保费支出**：每年 **{}**".format(yuan(existing)))
        if room_lo < 0:
            lines.append(
                "- **剩余可配空间**：**已是负数**——你现在的保费（你交的钱）已经超出经验区间了。"
                "\n  - 下一步：先做**保单体检（把老保单盘一遍）**——同伴 skill `ins-policy-checkup`，"
                "跑 `policy_review.py` 得到全家年缴合计，再回来重算一次；先不谈加保。"
            )
        else:
            lines.append(
                "- **剩余可配空间**：**{} ～ {}**，这是你今年还能拿来加保障的尺子".format(
                    yuan(room_lo), yuan(room_hi)
                )
            )
    else:
        lines.append("- **已有保费支出**：暂未提供（说个大概就行，不追问）")

    lines.append("")
    lines.append("## 降档三招（保费超了怎么用）")
    lines.append("")
    lines.append(
        "1. **保额（出事了最多赔你多少）够就行，不追高**——先砍掉超出经验区间的部分；\n"
        "2. **期限买短**——保到 60 岁（那时孩子大了、房贷还完了）而不是保终身；\n"
        "3. **选消费型**——不出事不退钱，但同样保额（出事了最多赔你多少）便宜很多。"
    )
    lines.append("")
    lines.append("## 你现在可以做的一步")
    lines.append("")
    lines.append(
        "把上面这个「剩余可配空间」的数记住，往下谈配什么、配多少，都拿它当尺子。"
    )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(FOOTER)
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="家庭保费预算试算表")
    ap.add_argument("--income", required=True,
                    help="家庭年收入（万元），支持区间如 20-40；两口子都挣钱时填其中一人")
    ap.add_argument("--income2", default=None,
                    help="配偶年收入（万元），可省略；与 --income 相加为家庭年收入")
    ap.add_argument("--expense", type=int, default=0,
                    help="每月刚性支出（元），可省略")
    ap.add_argument("--existing", type=int, default=None,
                    help="已有保单年缴保费合计（元），可省略")
    ap.add_argument("--mode", choices=["full", "rough"], default="full",
                    help="rough = 客户说不清精确数字，只给区间与档位感")
    ap.add_argument("--output", help="输出到文件（默认打印到屏幕）")
    args = ap.parse_args()

    income = parse_income(args.income)
    if income is None:
        print("[没算出来] 年收入这一项我没读懂。\n"
              "  可以直接说数字，单位是「万」：\n"
              "    --income 30          年收入 30 万\n"
              "    --income 30万        一样的意思\n"
              "    --income 20-40       说不准就报个区间\n"
              "    --income 三十万       写成中文也行\n"
              "  收入填 0 会算不出来——这一项要填真实的年收入。",
              file=sys.stderr)
        return 1

    income2 = None
    if args.income2:
        income2 = parse_income(args.income2)
        if income2 is None:
            print("[没算出来] 配偶收入这一项我没读懂。\n"
                  "  写法和 --income 一样：\n"
                  "    --income2 15        配偶年收入 15 万\n"
                  "    --income2 十五万     中文也行\n"
                  "  不需要就别填这项。",
                  file=sys.stderr)
            return 1

    rough = (args.mode == "rough")
    body = build_table(income, args.expense, args.existing, rough, income2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(body + "\n")
        print("[完成] 试算表已写入 {}".format(args.output))
    else:
        print(body)
    return 0


if __name__ == "__main__":
    sys.exit(main())
