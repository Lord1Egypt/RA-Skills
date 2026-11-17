#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SGCFX `x/{dir}/3010` 单位工程费用汇总表 —— 双精度反解 + 六段式闭合求解

背景：3010 的字符串层是**碎片**（"费用""[程序]""2.2 其中："…），金额全部存为
IEEE-754 little-endian double，无法靠标签定位字段。因此改用**闭合约束反解**。

用法：
    python3 dbl3010.py dump  <3010 路径>                 # 导出全部候选金额（人工看）
    python3 dbl3010.py solve <含 3010 的目录1> [目录2 …]   # 反解六段式结构
    python3 dbl3010.py rate  <新版 xlsx 导出的 CSV>       # 费率反算（3% / 6.35% / 9%）

反解原理：
    六段式  A 分部分项 + B 措施项目 + C 其他项目 = D 税前建安工程造价
            E 增值税 = D × 9%
            F 最高投标限价合计 = D + E (+ 附加性费用)
    在候选金额集合 S 中找 (A,B,C,D,E) 使 A+B+C=D 且 |D×1.09−E| ≤ 0.02。
"""
import sys, struct, itertools


def doubles(path):
    """扫描文件，返回按偏移排序的、形如 2 位小数的候选金额列表 [(offset, value)]。"""
    b = open(path, 'rb').read()
    out = []
    for i in range(0, max(0, len(b) - 8)):
        v = struct.unpack_from('<d', b, i)[0]
        if 0.005 < v < 1e9 and abs(v - round(v, 2)) < 0.0051:
            if out and i - out[-1][0] < 8:
                continue
            out.append((i, round(v, 2)))
    return out


def _hit(C, S):
    """C 是否落在 S 内，或可表示为 S 中两个数之和。

    必要性：安装类单位工程的「其他项目费」＝ 专业工程暂估价 ＋ 规费，
    并不作为单个 double 存盘（实测 单项工程A安装 53,655.20 + 2,157.90 = 55,813.10）。
    """
    if any(abs(C - x) <= 0.011 for x in S):
        return True
    for x in S:
        if x >= C:
            break
        if any(abs(C - x - y) <= 0.011 for y in S):
            return True
    return False


def solve(pairs):
    """在候选金额中找六段式解，返回 (A,B,C,D,E,F)；pairs 为 [(offset, value)]。

    判别式：
        A + B + C = D                     分部分项 + 措施 + 其他 = 税前建安工程造价
        E ≈ D × 9%                        增值税
        tail = F − D − E                  <0.02（新版，纯增值税）
                                          或 0.1% ≤ tail/E ≤ 2.5%（老版另有附加性费用）
    排序：A/B/C 按在文件中的**首次出现偏移**升序 —— 与 SGCFX 行序一致
    （实测 分部分项 → 措施 → 其他），且强制 A＝三者最大。
    剪枝：0.45D ≤ A，0.015D ≤ B ≤ 0.15D（分部分项与措施的实测占比区间）。
    """
    first = {}
    for off, v in pairs:
        first.setdefault(v, off)
    S = sorted(first)
    for F in sorted(S, reverse=True):
        for D in S:
            if D >= F:
                continue
            E = round(D * 0.09, 2)
            if not any(abs(E - x) <= 0.02 for x in S):
                continue
            tail = F - D - E
            if not (tail <= 0.02 or (E > 0 and 0.001 <= tail / E <= 0.025)):
                continue
            for A in S:
                if A < 0.45 * D or A >= D:
                    continue
                for B in S:
                    if B < 0.05 * A or B > 0.15 * D:
                        continue
                    C = round(D - A - B, 2)
                    if C < 0.5:
                        if abs(D - A - B) > 0.02:
                            continue
                        C = 0.0
                    elif C >= A or not _hit(C, S):
                        continue
                    trio = sorted((A, B, C), key=lambda v: first.get(v, 10**9))
                    if trio[0] != A:
                        continue
                    return (trio[0], trio[1], trio[2], D, E, F)
    return None


def cmd_dump(path):
    for off, v in doubles(path):
        print(f"{off:8d} {v:,.2f}")


def cmd_solve(*dirs):
    for d in dirs:
        r = solve(doubles(d))
        if r:
            A, B, C, D, E, F = r
            print(f"{d}\n  分部分项 {A:>14,.2f}  措施 {B:>13,.2f}  其他 {C:>12,.2f}"
                  f"  税前 {D:>14,.2f}  增值税 {E:>12,.2f}  合计 {F:>14,.2f}")
            print(f"  校验 A+B+C={A+B+C:,.2f} vs D={D:,.2f} "
                  f"{'OK' if abs(A+B+C-D) < 0.02 else 'XX'}")
        else:
            print(f"{d}\n  未解出（可能缺项或存在附加性费用，改用 dump 人工读）")


def cmd_rate(csv_path):
    """对 CSV（列：分部分项,单价措施,总价措施,其中安措,税前,增值税）做费率反算。"""
    import csv as _csv
    bad = 0
    with open(csv_path, encoding='utf-8-sig') as f:
        for row in _csv.DictReader(f):
            try:
                A = float(row['分部分项工程费']); U = float(row['单价措施项目费'])
                G = float(row['总价措施项目费']); P = float(row['其中:安全生产措施费'])
                D = float(row['税前建安工程造价']); T = float(row['增值税'])
            except (KeyError, ValueError):
                continue
            B = A + U
            ok = (abs(B * 0.03 - P) <= 0.03 and abs(B * 0.0635 - G) <= 0.03
                  and abs(D * 0.09 - T) <= 0.03)
            bad += 0 if ok else 1
            print(f"B={B:>13,.2f}  B×3%={B*0.03:>10,.2f}/实{P:>10,.2f}"
                  f"  B×6.35%={B*0.0635:>11,.2f}/实{G:>11,.2f}"
                  f"  D×9%={D*0.09:>11,.2f}/实{T:>11,.2f}  {'OK' if ok else 'XX'}")
    print(f"不符项 {bad} 项")
    print("费率（四川 2025 定额，实证）：总价措施 = (分部分项+单价措施) × 6.35%，"
          "其中安措 3.00%（不可竞争）+ 临时设施 1.58% + 文明施工 0.86% + 环境保护 0.21% + 其余 0.70%")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    cmd, args = sys.argv[1], sys.argv[2:]
    {'dump': cmd_dump, 'solve': cmd_solve, 'rate': cmd_rate}[cmd](*args)
