#!/usr/bin/env python3
"""
数据合并工具 — 合并多个CSV、去重、排序、自动识别彩种
"""

import csv, argparse, sys, os
from collections import OrderedDict


COLUMN_MAP = {
    "大乐透": ["彩种", "期号", "开奖日期", "号码1", "号码2", "号码3", "号码4", "号码5", "号码6", "号码7"],
    "排列3":  ["彩种", "期号", "开奖日期", "号码1", "号码2", "号码3"],
    "排列5":  ["彩种", "期号", "开奖日期", "号码1", "号码2", "号码3", "号码4", "号码5"],
    "七星彩": ["彩种", "期号", "开奖日期", "号码1", "号码2", "号码3", "号码4", "号码5", "号码6", "号码7"],
}


def detect_lottery(filepath):
    with open(filepath, encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, [])
    n = len(header)
    if n == 10: return "大乐透" if "号码7" in header else "七星彩"
    if n == 5: return "排列5"
    if n == 3: return "排列3"
    return None


def load_csv(filepath):
    rows = []
    with open(filepath, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            return None, []
        fields = reader.fieldnames
        for r in reader:
            rows.append(r)
    return fields, rows


def key_func(row):
    return (row.get("彩种", ""), row.get("期号", ""), row.get("开奖日期", ""))


def main():
    ap = argparse.ArgumentParser(description="数据合并工具")
    ap.add_argument("files", nargs="+", help="CSV文件路径")
    ap.add_argument("--output", "-o", required=True, help="输出文件")
    ap.add_argument("--dedup", action="store_true", default=True, help="去重(默认)")
    ap.add_argument("--no-dedup", action="store_true", help="不去重")
    ap.add_argument("--lottery", choices=["大乐透","排列3","排列5","七星彩","自动"], default="自动")
    args = ap.parse_args()

    dedup = not args.no_dedup
    all_rows = []
    fieldnames = None
    detected_lottery = args.lottery

    for fp in args.files:
        if not os.path.exists(fp):
            print(f"⚠️ 文件不存在: {fp}")
            continue
        try:
            fields, rows = load_csv(fp)
            if not rows:
                print(f"⚠️ 空文件或格式异常: {fp}")
                continue
            if args.lottery == "自动" and detected_lottery == "自动":
                detected = detect_lottery(fp)
                if detected:
                    detected_lottery = detected
                    print(f"🔍 检测到彩种: {detected_lottery}")
            if fieldnames is None:
                fieldnames = fields
            all_rows.extend(rows)
            print(f"📥 {fp}: {len(rows)} 条")
        except Exception as e:
            print(f"❌ 读取失败 {fp}: {e}")

    if not all_rows:
        print("❌ 没有有效数据")
        return

    # 去重
    total_before = len(all_rows)
    if dedup:
        seen = set()
        unique = []
        for r in all_rows:
            k = key_func(r)
            if k not in seen:
                seen.add(k)
                unique.append(r)
        all_rows = unique
        print(f"🧹 去重: {total_before} → {len(all_rows)} 条 (移除 {total_before - len(all_rows)})")

    # 排序
    standard = COLUMN_MAP.get(detected_lottery if detected_lottery != "自动" else "大乐透")
    if standard:
        all_rows.sort(key=lambda r: (r.get("开奖日期", ""), r.get("期号", "")))
    else:
        all_rows.sort(key=lambda r: r.get("期号", ""))

    # 输出
    with open(args.output, "w", newline="", encoding="utf-8") as f:
        fn = fieldnames if fieldnames else standard
        writer = csv.DictWriter(f, fieldnames=fn)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"✅ 共 {len(all_rows)} 条 → {args.output}")
    print(f"📊 更新统计:")
    print(f"   大乐透: {sum(1 for r in all_rows if r.get('彩种','')=='大乐透')} 期")
    qihao_list = sorted(set(r.get("期号", "") for r in all_rows))
    print(f"   期号范围: {qihao_list[0]} ~ {qihao_list[-1]}")


if __name__ == "__main__":
    main()
