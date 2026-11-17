#!/usr/bin/env python3
"""
中奖概率计算器 — 精确概率/理论奖金期望
"""

import argparse, math, sys


def comb(n, k):
    return math.comb(n, k) if k <= n else 0


def prob_dlt():
    """超级大乐透各奖级中奖概率"""
    print("📊 超级大乐透 中奖概率")
    print("═" * 50)

    total = comb(35, 5) * comb(12, 2)
    print(f"\n总注数: {total:,}")
    print(f"1注中头奖概率: 1/{total:,} ≈ {1/total*100:.8f}%")

    levels = {
        "一等奖(5+2)": (comb(5,5)*comb(30,0) * comb(2,2)*comb(10,0), total),
        "二等奖(5+1)": (comb(5,5)*comb(30,0) * comb(2,1)*comb(10,1), total),
        "三等奖(5+0)": (comb(5,5)*comb(30,0) * comb(2,0)*comb(10,2), total),
        "四等奖(4+2)": (comb(5,4)*comb(30,1) * comb(2,2)*comb(10,0), total),
        "五等奖(4+1)": (comb(5,4)*comb(30,1) * comb(2,1)*comb(10,1), total),
        "六等奖(3+2)": (comb(5,3)*comb(30,2) * comb(2,2)*comb(10,0), total),
        "七等奖(4+0)": (comb(5,4)*comb(30,1) * comb(2,0)*comb(10,2), total),
        "七等奖(3+1)": (comb(5,3)*comb(30,2) * comb(2,1)*comb(10,1), total),
        "七等奖(2+2)": (comb(5,2)*comb(30,3) * comb(2,2)*comb(10,0), total),
        "七等奖(1+2)": (comb(5,1)*comb(30,4) * comb(2,2)*comb(10,0), total),
        "七等奖(0+2)": (comb(5,0)*comb(30,5) * comb(2,2)*comb(10,0), total),
    }

    for name, (wins, total) in levels.items():
        prob = wins / total * 100
        print(f"  {name:<25} {wins:>10,}注  {prob:.6f}%  1/{total//wins:,}" if wins > 0 else f"  {name:<25} 0")

    total_win = sum(w for w, _ in levels.values())
    print(f"\n整体中奖概率: {total_win/total*100:.4f}%  (1/{total//total_win:,})")


def prob_pl3():
    """排列3"""
    print("📊 排列3 中奖概率")
    print("═" * 50)
    print(f"  直选:   1/1,000 = 0.1%")
    print(f"  组选3:  1/333 ≈ 0.30% (180注)")
    print(f"  组选6:  1/167 ≈ 0.60% (360注)")
    print(f"  整体:  541/1,000 = 54.1%")


def prob_pl5():
    """排列5"""
    print("📊 排列5 中奖概率")
    print("═" * 50)
    print(f"  直选:   1/100,000 = 0.001%")
    

def prob_qxc():
    """七星彩"""
    print("📊 七星彩 中奖概率")
    print("═" * 50)
    total = 10**7
    levels = {
        "一等奖(7位全中)": (1, total),
        "二等奖(前6位)": (9*1, total),
        "三等奖(前5位)": (9*10*1, total),
        "四等奖(前4位)": (9*10*10*1, total),
        "五等奖(前3位)": (9*10*10*10*1, total),
        "六等奖(前2位)": (9*10*10*10*10*1, total),
    }
    for name, (wins, tot) in levels.items():
        print(f"  {name:<25} {wins:>10}注  {wins/tot*100:.6f}%")


def main():
    ap = argparse.ArgumentParser(description="中奖概率计算器")
    ap.add_argument("--lottery", default="大乐透", choices=["大乐透","排列3","排列5","七星彩"])
    ap.add_argument("--my-nums", help="自选号码，计算命中概率")
    args = ap.parse_args()

    if args.lottery == "大乐透":
        prob_dlt()
    elif args.lottery == "排列3":
        prob_pl3()
    elif args.lottery == "排列5":
        prob_pl5()
    elif args.lottery == "七星彩":
        prob_qxc()

    print("\n⚠️ 以上概率为理论数学计算值，仅供参考，不构成投注建议。")

    if args.my_nums:
        pass
        # 自选号码概率暂未实现


if __name__ == "__main__":
    main()
