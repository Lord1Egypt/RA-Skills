#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
recommend_pages.py — 按「项目性质 + 金额」推荐技术标页数

用法:
  python recommend_pages.py --budget 298 --nature simple_svc
  python recommend_pages.py --describe "医院物业服务项目公开招标"
  python recommend_pages.py --budget 1200 --nature it_sys --chars-per-page 1050

输出: 性质、预算、推荐页数(单值)、推荐区间、理由、预算汉字数

性质 key: simple_svc / goods / construct / it_sys / design / opex
中文别名（--describe 走关键词识别）见 NATURES 表。
"""
import sys
import argparse

NATURES = {
    "simple_svc": dict(name="简单服务类", alias=["物业", "保洁", "餐饮", "保安", "绿化", "会务", "租赁", "后勤", "环卫", "养护", "服务"], density=0.13, floor=30, ceil=150),
    "goods":      dict(name="货物/设备采购", alias=["货物", "设备", "采购", "器材", "耗材", "供货", "机电", "产品"], density=0.22, floor=40, ceil=250),
    "construct":  dict(name="工程施工/装修", alias=["施工", "工程", "装修", "修缮", "土建", "安装", "建造"], density=0.28, floor=50, ceil=400),
    "it_sys":     dict(name="信息化/系统集成", alias=["信息化", "系统", "集成", "软件", "平台", "数据", "数字化", "智能", "网络"], density=0.30, floor=45, ceil=350),
    "design":     dict(name="设计/咨询/科研", alias=["设计", "咨询", "科研", "规划", "研究", "方案编制", "评估", "课题"], density=0.25, floor=35, ceil=300),
    "opex":       dict(name="运维/维保/运营", alias=["运维", "维保", "运营", "保养", "托管", "运行维护", "维护"], density=0.15, floor=30, ceil=200),
}


def detect_nature(text):
    best, best_hits = None, 0
    for k, v in NATURES.items():
        hits = sum(1 for a in v["alias"] if a in text)
        if hits > best_hits:
            best, best_hits = k, hits
    return best if best_hits > 0 else None


def recommend(nature_key, budget, cpp=1050.0):
    v = NATURES[nature_key]
    raw = budget * v["density"]
    rec = int(max(v["floor"], min(v["ceil"], round(raw))))
    lo = max(v["floor"], round(rec * 0.8))
    hi = min(v["ceil"], round(rec * 1.2))
    return rec, lo, hi, v, raw


def main(argv=None):
    ap = argparse.ArgumentParser(description="按项目性质+金额推荐技术标页数")
    ap.add_argument("--budget", type=float, default=None, help="项目预算/最高限价（万元）")
    ap.add_argument("--nature", type=str, default=None, help="性质 key: simple_svc/goods/construct/it_sys/design/opex")
    ap.add_argument("--describe", type=str, default=None, help="项目描述文本，自动识别性质")
    ap.add_argument("--chars-per-page", type=float, default=1050.0, help="每页字数基准（仿宋小四公文版式默认1050）")
    args = ap.parse_args(argv)

    nature_key = args.nature
    if not nature_key and args.describe:
        nature_key = detect_nature(args.describe)
    if not nature_key:
        print("ERR -> 未给定 --nature 且无法从 --describe 识别性质；可选: " + "/".join(NATURES.keys()))
        return 1
    if nature_key not in NATURES:
        print("ERR -> 未知 nature: %s；可选: %s" % (nature_key, "/".join(NATURES.keys())))
        return 1

    if not args.budget or args.budget <= 0:
        v = NATURES[nature_key]
        print("=" * 60)
        print("recommend_pages — 页数推荐（无金额，给性质软下限）")
        print("=" * 60)
        print("性质     : %s (%s)" % (v["name"], nature_key))
        print("建议下限 : %d 页（请提供预算以细化推荐）" % v["floor"])
        print("=" * 60)
        return 0

    rec, lo, hi, v, raw = recommend(nature_key, args.budget, args.chars_per_page)
    note = ""
    if raw < v["floor"]:
        note = "（预算偏小，已触软下限 %d 页）" % v["floor"]
    elif raw > v["ceil"]:
        note = "（预算偏大，已封软上限 %d 页，建议分册或聚焦核心方案）" % v["ceil"]
    print("=" * 60)
    print("recommend_pages — 页数推荐")
    print("=" * 60)
    print("性质     : %s (%s)" % (v["name"], nature_key))
    print("预算     : %.0f 万元" % args.budget)
    print("密度系数 : %.2f 页/万元" % v["density"])
    print("推荐页数 : %d 页  %s" % (rec, note))
    print("推荐区间 : %d – %d 页" % (lo, hi))
    print("预算字数 : ≈ %d 字（%d 页 × %.0f 字/页）" % (rec * int(args.chars_per_page), rec, args.chars_per_page))
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
