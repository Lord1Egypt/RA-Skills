# -*- coding: utf-8 -*-
"""
游戏数值平衡校验脚本 (balance_calc.py)

三个子命令：
  dps     校验伤害/减伤公式，输出各等级实际 DPS 表
  curve   按目标时长反推等级经验曲线，输出每级所需经验与累计时长
  economy 校验经济系统收支，输出各节点盈余/缺口与断档点

设计约束（对应 references/formulas.md）：
  - 仅支持内置公式名（减伤式/乘算式/差值式 及其英文别名），不接受任意表达式，避免注入与歧义
  - 纯标准库，Windows 兼容，stdout 强制 utf-8
  - 报告末尾附带「复算命令」，用户改参数重跑即得同样口径结果

用法示例：
  python balance_calc.py dps --atk 100 --def 50 --lvl 1,10,50,100 --formula 减伤式
  python balance_calc.py curve --target-hours 30 --max-lvl 30 --base 100
  python balance_calc.py economy --income "1:100,10:250,30:900" --cost "5:120,15:400,30:2000"
"""

import sys
import argparse

# 强制 stdout / stderr 为 utf-8（Windows 默认 cp936 会乱码）
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# 内置公式名 -> 内部键
FORMULA_NAMES = {
    "减伤式": "reduce",
    "reduce": "reduce",
    "乘算式": "mul",
    "mul": "mul",
    "差值式": "diff",
    "diff": "diff",
}


def compute_dmg(kind, atk, dfn, coef, floor):
    """按内置公式类型计算单次伤害。"""
    if kind == "reduce":
        # 减伤除法式：攻击收益平滑递减，攻防同涨时伤害趋向恒定
        if atk + dfn <= 0:
            return 0.0
        return atk * atk / (atk + dfn)
    if kind == "mul":
        # 乘算免伤：防御提供百分比减伤，coef 为护甲常数，越小减伤越陡
        return atk * (coef / (dfn + coef))
    if kind == "diff":
        # 差值式：硬减，floor 为伤害下限（按攻击比例）
        raw = atk - dfn
        return max(raw, atk * floor)
    raise ValueError("未知公式类型: %s" % kind)


def parse_levels(text):
    return [int(x.strip()) for x in text.split(",") if x.strip()]


def parse_nodes(text):
    """解析 'lvl:value,lvl:value' 为 {lvl: value} 整数键字典。"""
    out = {}
    for pair in text.split(","):
        pair = pair.strip()
        if not pair:
            continue
        if ":" not in pair:
            raise ValueError("节点格式应为 等级:数值，收到: %s" % pair)
        k, v = pair.split(":", 1)
        out[int(k.strip())] = float(v.strip())
    if not out:
        raise ValueError("节点为空")
    return out


def interp(nodes, lvl):
    """线性插值取某等级的节点值；区间外取最近的已知端点。"""
    keys = sorted(nodes.keys())
    if lvl <= keys[0]:
        return nodes[keys[0]]
    if lvl >= keys[-1]:
        return nodes[keys[-1]]
    for i in range(1, len(keys)):
        if lvl <= keys[i]:
            a, b = keys[i - 1], keys[i]
            t = (lvl - a) / (b - a)
            return nodes[a] + (nodes[b] - nodes[a]) * t
    return nodes[keys[-1]]


def repr_cmd():
    return "python balance_calc.py " + " ".join(sys.argv[1:])


def judge_dps(levels, dps_list):
    """返回判定结论。levels/dps_list 均为按等级升序的列表。"""
    if len(dps_list) < 2:
        return "样本不足，无法判定曲线形态"
    ratio_total = dps_list[-1] / dps_list[0] if dps_list[0] > 0 else float("inf")
    # 断档：任意相邻步增长超过 2.5 倍
    for i in range(1, len(dps_list)):
        if dps_list[i - 1] > 0 and dps_list[i] / dps_list[i - 1] > 2.5:
            return "断档：等级 %d 处 DPS 较上一采样点突增 %.1fx，建议检查成长曲线" % (
                levels[i], dps_list[i] / dps_list[i - 1])
    if ratio_total > 500:
        return "超调：满级 DPS 为 1 级的 %.0fx，后期数值爆炸，建议压低成长系数" % ratio_total
    if ratio_total < 3:
        return "平坦：满级 DPS 仅 1 级的 %.1fx，成长感弱，建议提高攻击成长" % ratio_total
    return "健康：DPS 随等级平滑增长（%.1fx），未见突跳或爆炸" % ratio_total


def cmd_dps(args):
    if args.formula not in FORMULA_NAMES:
        allowed = "、".join(sorted(set(FORMULA_NAMES.keys())))
        sys.stderr.write("错误：--formula 仅支持内置公式名 [%s]，不支持任意表达式\n" % allowed)
        return 2
    kind = FORMULA_NAMES[args.formula]
    levels = parse_levels(args.lvl)
    rows = []
    for lvl in levels:
        atk = args.atk * (1 + (lvl - 1) * args.grow)
        dfn = args.def_ * (1 + (lvl - 1) * args.defgrow)
        dmg = compute_dmg(kind, atk, dfn, args.coef, args.floor)
        dps = dmg * args.aps
        rows.append((lvl, atk, dfn, dmg, dps))
    print("=== DPS 校验报告 ===")
    print("公式类型：%s" % args.formula)
    print("攻击成长/级：%.1f%%  防御成长/级：%.1f%%  攻速：%.2f 次/秒  护甲常数：%.1f  伤害下限：%.0f%%"
          % (args.grow * 100, args.defgrow * 100, args.aps, args.coef, args.floor * 100))
    print()
    print("%-6s %-10s %-10s %-12s %-12s" % ("等级", "攻击", "防御", "单次伤害", "DPS"))
    print("-" * 52)
    dps_vals = []
    for lvl, atk, dfn, dmg, dps in rows:
        print("%-6d %-10.1f %-10.1f %-12.1f %-12.1f" % (lvl, atk, dfn, dmg, dps))
        dps_vals.append(dps)
    print()
    print("判定：%s" % judge_dps(levels, dps_vals))
    print()
    print("复算命令（改参数重跑即得同样口径）：")
    print("  " + repr_cmd())
    return 0


def cmd_curve(args):
    maxlvl = args.max_lvl
    base = args.base
    total_sec = args.target_hours * 3600.0
    if args.curve_type == "exp":
        r = args.rate_exp
        exps = [base * (r ** (L - 1)) for L in range(1, maxlvl + 1)]
    else:  # power
        p = args.power
        exps = [base * (L ** p) for L in range(1, maxlvl + 1)]
    sum_exp = sum(exps)
    rate = sum_exp / total_sec if total_sec > 0 else 1.0  # 经验/秒，使总时长命中目标
    print("=== 等级经验曲线报告 ===")
    print("曲线类型：%s  目标总时长：%.1f 小时  满级：%d  基础经验：%.0f"
          % (args.curve_type, args.target_hours, maxlvl, base))
    print("拟合获取速率：%.1f 经验/秒（使累计时长命中目标）" % rate)
    print()
    print("%-6s %-12s %-14s %-12s %-12s" % ("等级", "本级经验", "累计经验", "本级时长(h)", "累计时长(h)"))
    print("-" * 58)
    cum_exp = 0.0
    cum_sec = 0.0
    per_hours = []
    for L in range(1, maxlvl + 1):
        e = exps[L - 1]
        t_sec = e / rate if rate > 0 else 0.0
        cum_exp += e
        cum_sec += t_sec
        ph = t_sec / 3600.0
        per_hours.append(ph)
        print("%-6d %-12.0f %-14.0f %-12.2f %-12.2f" % (L, e, cum_exp, ph, cum_sec / 3600.0))
    print()
    # 判定平滑度
    verdict = judge_curve(per_hours, args.curve_type)
    print("判定：%s" % verdict)
    print()
    print("复算命令（改参数重跑即得同样口径）：")
    print("  " + repr_cmd())
    return 0


def judge_curve(per_hours, ctype):
    if len(per_hours) < 3:
        return "样本不足，无法判定曲线形态"
    ratios = []
    for i in range(1, len(per_hours)):
        prev = per_hours[i - 1]
        ratios.append(per_hours[i] / prev if prev > 0 else float("inf"))
    if any(rt > 3 for rt in ratios):
        idx = next(i for i, rt in enumerate(ratios) if rt > 3)
        return "断档：等级 %d 本级时长突增 %.1fx，曲线不平滑" % (idx + 2, ratios[idx])
    if any(rt > 2 for rt in ratios):
        return "超调/爆炸：后期本级时长增速超 2x（类型 %s），后期升级极慢" % ctype
    if all(rt < 0.7 for rt in ratios):
        return "平坦：本级时长持续走低，前期升级过快、缺乏成长感"
    return "健康：本级时长平滑变化，曲线可用（类型 %s）" % ctype


def cmd_economy(args):
    income = parse_nodes(args.income)
    cost = parse_nodes(args.cost)
    maxlvl = max(max(income.keys()), max(cost.keys()))
    print("=== 经济系统收支报告 ===")
    print()
    print("%-6s %-12s %-12s %-12s %-14s" % ("等级", "产出/时", "消耗/时", "净收支", "累计净收支"))
    print("-" * 58)
    cum = 0.0
    break_even = None
    deficit_points = []
    for L in range(1, maxlvl + 1):
        inc = interp(income, L)
        cst = interp(cost, L)
        net = inc - cst
        cum += net
        if net < 0:
            deficit_points.append(L)
        if break_even is None and cum >= 0 and L > 1:
            break_even = L
        tag = "盈余" if net >= 0 else "缺口"
        print("%-6d %-12.1f %-12.1f %-12.1f %-14.1f  %s" % (L, inc, cst, net, cum, tag))
    print()
    if deficit_points:
        print("断档点（产出<消耗，玩家在此卡住）：等级 %s" % "、".join(str(x) for x in deficit_points))
    else:
        print("断档点：无（全程产出≥消耗）")
    if break_even is not None:
        print("回本等级：%d（累计净收支首次转正）" % break_even)
    else:
        print("回本等级：未回本（累计净收支始终为负，经济系统入不敷出）")
    verdict = "健康：收支为正且无断档，经济节奏可持续" if not deficit_points else \
              "断档：存在产出低于消耗的等级，需在该节点补产出或削消耗"
    print("判定：%s" % verdict)
    print()
    print("复算命令（改参数重跑即得同样口径）：")
    print("  " + repr_cmd())
    return 0


def build_parser():
    p = argparse.ArgumentParser(
        description="游戏数值平衡校验：dps / curve / economy 三个子命令",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd")

    d = sub.add_parser("dps", help="校验伤害/减伤公式，输出各等级 DPS")
    d.add_argument("--atk", type=float, required=True, help="1 级基础攻击")
    d.add_argument("--def", dest="def_", type=float, required=True, help="1 级基础防御（参数名用 --def）")
    d.add_argument("--lvl", type=str, required=True, help="等级列表，逗号分隔，如 1,10,50,100")
    d.add_argument("--formula", type=str, required=True,
                   help="内置公式名：减伤式 / 乘算式 / 差值式（不支持任意表达式）")
    d.add_argument("--grow", type=float, default=0.08, help="攻击每级成长比例，默认 0.08")
    d.add_argument("--defgrow", type=float, default=0.04, help="防御每级成长比例，默认 0.04")
    d.add_argument("--aps", type=float, default=1.0, help="每秒攻击次数，默认 1.0")
    d.add_argument("--coef", type=float, default=100.0, help="乘算式护甲常数 K，默认 100")
    d.add_argument("--floor", type=float, default=0.1, help="差值式伤害下限（攻击比例），默认 0.1")
    d.set_defaults(func=cmd_dps)

    c = sub.add_parser("curve", help="按目标时长反推等级经验曲线")
    c.add_argument("--target-hours", type=float, required=True, help="到满级的目标总时长（小时）")
    c.add_argument("--max-lvl", type=int, required=True, help="满级等级")
    c.add_argument("--base", type=float, default=100.0, help="1 级所需经验，默认 100")
    c.add_argument("--curve-type", type=str, default="power", choices=["power", "exp"],
                   help="曲线类型：power(幂函数) / exp(指数函数)，默认 power")
    c.add_argument("--power", type=float, default=1.5, help="幂函数指数 p，默认 1.5")
    c.add_argument("--rate-exp", type=float, default=1.08, help="指数函数公比 r，默认 1.08")
    c.set_defaults(func=cmd_curve)

    e = sub.add_parser("economy", help="校验经济系统收支，输出盈余/缺口与断档点")
    e.add_argument("--income", type=str, required=True, help="产出点，等级:数值 逗号分隔，如 1:100,10:250,30:900")
    e.add_argument("--cost", type=str, required=True, help="消耗点，等级:数值 逗号分隔，如 5:120,15:400,30:2000")
    e.set_defaults(func=cmd_economy)
    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    if not getattr(args, "cmd", None):
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
