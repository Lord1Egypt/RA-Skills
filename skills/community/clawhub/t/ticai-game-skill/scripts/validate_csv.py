#!/usr/bin/env python3
"""
体彩 CSV 数据校验工具
校验 CSV 格式是否满足 SKILL.md 定义的数据规范。
"""

import csv
import sys
import argparse

LOTTERY_TYPES = {"大乐透", "排列3", "排列5", "七星彩", "竞彩足球", "竞彩篮球"}

DIGITAL_LOTTERIES = {"大乐透", "排列3", "排列5", "七星彩"}


def validate_digital(row, line):
    """校验乐透数字型 CSV 行"""
    errors = []
    lottery = row.get("彩种", "")
    if lottery not in DIGITAL_LOTTERIES:
        errors.append(f"第{line}行: 未知彩种 '{lottery}'")
        return errors

    if "期号" not in row or not row["期号"].strip():
        errors.append(f"第{line}行: 缺少期号")

    vals = []
    for i in range(1, 8):
        key = f"号码{i}"
        if key in row and row[key].strip():
            try:
                v = int(row[key])
                vals.append(v)
                if not (0 <= v <= 35):
                    errors.append(f"第{line}行: {key}={v} 超出范围 0-35")
            except ValueError:
                errors.append(f"第{line}行: {key}='{row[key]}' 不是有效数字")

    if lottery == "大乐透":
        front = [v for v in vals[:5]]
        back = vals[5:7]
        if len(front) != 5 or len([v for v in front if 1 <= v <= 35]) != 5:
            errors.append(f"第{line}行: 前区需5个号码(01-35)")
        if len(back) != 2 or len([v for v in back if 1 <= v <= 12]) != 2:
            errors.append(f"第{line}行: 后区需2个号码(01-12)")
    elif lottery == "排列3":
        if len(vals) != 3 or any(not (0 <= v <= 9) for v in vals):
            errors.append(f"第{line}行: 排列3需3个号码(0-9)")
    elif lottery == "排列5":
        if len(vals) != 5 or any(not (0 <= v <= 9) for v in vals):
            errors.append(f"第{line}行: 排列5需5个号码(0-9)")
    elif lottery == "七星彩":
        if len(vals) != 7 or any(not (0 <= v <= 9) for v in vals):
            errors.append(f"第{line}行: 七星彩需7个号码(0-9)")

    return errors


def validate_file(filepath):
    """校验整个 CSV 文件"""
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        if not reader.fieldnames:
            return ["文件为空或缺少表头"]

        headers = reader.fieldnames
        required = ["彩种", "期号"]
        missing = [h for h in required if h not in headers]
        if missing:
            return [f"缺少必需列: {', '.join(missing)}"]

        all_errors = []
        line = 2
        for row in reader:
            lottery = row.get("彩种", "").strip()
            if not lottery:
                all_errors.append(f"第{line}行: 彩种为空")
            elif lottery in DIGITAL_LOTTERIES:
                errs = validate_digital(row, line)
                all_errors.extend(errs)
            elif lottery not in LOTTERY_TYPES:
                all_errors.append(f"第{line}行: 未知彩种 '{lottery}'")
            line += 1

        return all_errors


def main():
    parser = argparse.ArgumentParser(description="体彩 CSV 数据校验")
    parser.add_argument("file", help="CSV 文件路径")
    args = parser.parse_args()

    try:
        errors = validate_file(args.file)
        if errors:
            print(f"❌ 发现 {len(errors)} 个问题:")
            for e in errors:
                print(f"   {e}")
            sys.exit(1)
        else:
            print("✅ CSV 格式校验通过")
    except FileNotFoundError:
        print(f"❌ 文件不存在: {args.file}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 校验异常: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
