#!/usr/bin/env python3
"""
体彩筛选 — 号码分析、条件生成、复式计算与 CSV 统计
"""

import csv, math, random, argparse
from collections import Counter

# ── 彩种配置 ──────────────────────────────────────────────

CONFIG = {
    "大乐透": {
        "f_range": (1, 35), "f_pick": 5,
        "b_range": (1, 12), "b_pick": 2,
        "prime_f": {2,3,5,7,11,13,17,19,23,29,31},
        "prime_b": {2,3,5,7,11},
        "f_mid": 18,
    },
    "排列3":  {"digits": 3, "d_range": (0,9), "prime": {2,3,5,7}},
    "排列5":  {"digits": 5, "d_range": (0,9), "prime": {2,3,5,7}},
    "七星彩":  {"digits": 7, "d_range": (0,9), "prime": {2,3,5,7}},
}

ALL_DIGITAL = {"大乐透", "排列3", "排列5", "七星彩"}


# ── 指标函数 ──────────────────────────────────────────────

def odd_even_ratio(nums):
    o = sum(1 for n in nums if n % 2 == 1)
    return f"{o}:{len(nums)-o}"

def big_small_ratio(nums, mid):
    b = sum(1 for n in nums if n > mid)
    return f"{b}:{len(nums)-b}"

def prime_composite_ratio(nums, primes):
    p = sum(1 for n in nums if n in primes)
    return f"{p}:{len(nums)-p}"

def route012(nums):
    return ":".join(str(sum(1 for n in nums if n % 3 == r)) for r in (0,1,2))

def sum_value(nums):
    return sum(nums)

def span(nums):
    return max(nums) - min(nums)

def consecutive_pairs(nums):
    s = sorted(nums)
    return sum(1 for i in range(len(s)-1) if s[i+1]-s[i] == 1)

def ac_value(nums):
    d = set()
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            d.add(abs(nums[i]-nums[j]))
    return len(d) - (len(nums) - 1)

def comb_count(n, k):
    return math.comb(n, k) if k <= n else 0


# ── 号码分析 ──────────────────────────────────────────────

def analyze_number(nums_str, lottery="大乐透"):
    parts = nums_str.strip().split()
    if lottery == "大乐透":
        sep = parts.index("+") if "+" in parts else -2
        f = list(map(int, parts[:sep])) if sep > 0 else list(map(int, parts[:5]))
        b = list(map(int, parts[sep+1:])) if sep > 0 else list(map(int, parts[5:]))
        cfg = CONFIG["大乐透"]
        return {
            "前区": f, "后区": b,
            "前区奇偶比": odd_even_ratio(f),
            "前区大小比": big_small_ratio(f, cfg["f_mid"]),
            "前区质合比": prime_composite_ratio(f, cfg["prime_f"]),
            "前区和值": sum_value(f),
            "前区跨度": span(f),
            "前区AC值": ac_value(f),
            "前区012路": route012(f),
            "连号组数": consecutive_pairs(f),
            "后区奇偶比": odd_even_ratio(b),
            "后区和值": sum_value(b),
            "后区跨度": span(b),
        }
    else:
        d = list(map(int, parts))
        return {
            "号码": d,
            "和值": sum_value(d),
            "跨度": span(d),
            "奇偶比": odd_even_ratio(d),
            "奇偶形态": "".join("奇" if x%2 else "偶" for x in d),
            "大小形态": "".join("大" if x>4 else "小" for x in d),
        }


# ── 号码生成 ──────────────────────────────────────────────

def gen_dlt(filters=None, count=5):
    cfg = CONFIG["大乐透"]
    fr = range(cfg["f_range"][0], cfg["f_range"][1]+1)
    br = range(cfg["b_range"][0], cfg["b_range"][1]+1)
    res = []
    for _ in range(count * 500):
        f = sorted(random.sample(list(fr), cfg["f_pick"]))
        b = sorted(random.sample(list(br), cfg["b_pick"]))
        if filters:
            ok = True
            if "奇偶比" in filters and odd_even_ratio(f) != filters["奇偶比"]: ok = False
            if "大小比" in filters and big_small_ratio(f, cfg["f_mid"]) != filters["大小比"]: ok = False
            sv = sum_value(f)
            if "和值" in filters and not (filters["和值"][0] <= sv <= filters["和值"][1]): ok = False
            sp = span(f)
            if "跨度" in filters and not (filters["跨度"][0] <= sp <= filters["跨度"][1]): ok = False
            if not ok: continue
        res.append((f, b))
        if len(res) >= count: break
    return res


def gen_digital(lottery, filters=None, count=5):
    cfg = CONFIG[lottery]
    n = cfg["digits"]
    res = []
    for _ in range(count * 200):
        d = [random.randint(cfg["d_range"][0], cfg["d_range"][1]) for _ in range(n)]
        ok = True
        if filters:
            if "奇偶形态" in filters:
                m = "".join("奇" if x%2 else "偶" for x in d)
                if m != filters["奇偶形态"]: ok = False
            if "大小形态" in filters:
                m = "".join("大" if x>4 else "小" for x in d)
                if m != filters["大小形态"]: ok = False
            sv = sum(d)
            if "和值" in filters and not (filters["和值"][0] <= sv <= filters["和值"][1]): ok = False
        if ok:
            res.append(d)
            if len(res) >= count: break
    return res


# ── CSV 解析与分析 ──────────────────────────────────────

def parse_csv(path):
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def analyze_csv(data, lottery="大乐透"):
    freq = Counter()
    back_freq = Counter()
    for row in data:
        nums = [int(row[f"号码{i}"]) for i in range(1, 9) if row.get(f"号码{i}")]
        if lottery == "大乐透":
            for n in nums[:5]: freq[n] += 1
            for n in nums[5:7]: back_freq[n] += 1
        else:
            for n in nums: freq[n] += 1

    result = {"期数": len(data), "号码频率": freq.most_common(10)}
    if lottery == "大乐透":
        result["后区频率"] = back_freq.most_common(6)
        result["遗漏号码"] = sorted([n for n in range(1, 36) if n not in freq])
    return result


# ── 复式计算 ──────────────────────────────────────────────

def calc_dlt_comb(fn, bn, fd=0, bd=0):
    return comb_count(fn, 5-fd) * comb_count(bn, 2-bd)


# ── CLI ───────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="体彩筛选工具")
    sub = ap.add_subparsers(dest="cmd")

    a = sub.add_parser("analyze", help="分析号码指标")
    a.add_argument("nums")
    a.add_argument("--lottery", default="大乐透", choices=list(CONFIG.keys()))

    g = sub.add_parser("generate", help="生成号码")
    g.add_argument("--lottery", default="大乐透", choices=list(CONFIG.keys()))
    g.add_argument("--count", type=int, default=5)
    g.add_argument("--oe", help="奇偶比 如 3:2")
    g.add_argument("--bs", help="大小比 如 2:3")
    g.add_argument("--sum", help="和值范围 如 70-100")
    g.add_argument("--span", help="跨度范围 如 20-28")
    g.add_argument("--oe-shape", help="奇偶形态 如 奇奇偶(排列3/5/七星彩)")
    g.add_argument("--bs-shape", help="大小形态 如 小大大(排列3/5/七星彩)")

    c = sub.add_parser("csv", help="分析 CSV")
    c.add_argument("file")
    c.add_argument("--lottery", default="大乐透", choices=list(CONFIG.keys()))

    m = sub.add_parser("comb", help="复式胆拖计算")
    m.add_argument("--lottery", default="大乐透", choices=list(CONFIG.keys()))
    m.add_argument("--front-num", type=int, default=5)
    m.add_argument("--back-num", type=int, default=2)
    m.add_argument("--front-dan", type=int, default=0)
    m.add_argument("--back-dan", type=int, default=0)

    args = ap.parse_args()

    if args.cmd == "analyze":
        r = analyze_number(args.nums, args.lottery)
        for k, v in r.items():
            print(f"{k}: {v}")

    elif args.cmd == "generate":
        flt = {}
        if args.oe: flt["奇偶比"] = args.oe
        if args.bs: flt["大小比"] = args.bs
        if args.sum:
            lo, hi = map(int, args.sum.split("-"))
            flt["和值"] = (lo, hi)
        if args.span:
            lo, hi = map(int, args.span.split("-"))
            flt["跨度"] = (lo, hi)
        if args.oe_shape: flt["奇偶形态"] = args.oe_shape
        if args.bs_shape: flt["大小形态"] = args.bs_shape

        if args.lottery == "大乐透":
            res = gen_dlt(flt, args.count)
            for i, (f, b) in enumerate(res, 1):
                print(f"参考{i}: {' '.join(f'{n:02d}' for n in f)} + {' '.join(f'{n:02d}' for n in b)}")
            print("\n⚠️ 以上数据仅供统计参考，不构成投注建议。彩票具有随机性，请理性对待。")
        else:
            res = gen_digital(args.lottery, flt, args.count)
            for i, d in enumerate(res, 1):
                print(f"参考{i}: {' '.join(map(str, d))}")
            print("\n⚠️ 以上数据仅供统计参考，不构成投注建议。彩票具有随机性，请理性对待。")
        if not res:
            print("未找到满足条件的号码，请放宽条件")

    elif args.cmd == "csv":
        try:
            data = parse_csv(args.file)
            r = analyze_csv(data, args.lottery)
            print(f"共 {r['期数']} 期数据")
            print("\n号码频率 TOP10:")
            for n, c in r["号码频率"]:
                print(f"  {n:02d}: {c}次")
            if "后区频率" in r:
                print("\n后区频率 TOP6:")
                for n, c in r["后区频率"]:
                    print(f"  {n:02d}: {c}次")
            if "遗漏号码" in r and r["遗漏号码"]:
                print(f"\n遗漏号码: {' '.join(f'{n:02d}' for n in r['遗漏号码'][:10])}")
        except Exception as e:
            print(f"解析失败: {e}")

    elif args.cmd == "comb":
        if args.lottery == "大乐透":
            t = calc_dlt_comb(args.front_num, args.back_num, args.front_dan, args.back_dan)
            print(f"前区{args.front_num}码{'/'+str(args.front_dan)+'胆' if args.front_dan else ''}")
            print(f"后区{args.back_num}码{'/'+str(args.back_dan)+'胆' if args.back_dan else ''}")
            print(f"注数: {t}注  金额: {t*2}元 (追加{t*3}元)")
        else:
            cfg = CONFIG[args.lottery]
            n = cfg["digits"]
            picks = [args.front_num] * n
            t = 1
            for p in picks:
                t *= p
            print(f"{args.lottery} 定位复式: {'×'.join(map(str, picks))} = {t}注")
            print(f"金额: {t*2}元")

    else:
        ap.print_help()


if __name__ == "__main__":
    main()
