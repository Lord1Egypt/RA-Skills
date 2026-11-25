#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""淘宝标题体检：显示宽度 60 字符（约 30 汉字）、重复词、极限词。"""

import argparse
import re
import sys
import unicodedata


LIMIT_WORDS = r"最好|最佳|最优|最低价|最高级|最强|第一|顶级|国家级|世界级|绝无仅有|独一无二|100%|百分百|绝对安全"
SPECIAL = r"[【】\[\]★☆※→←↑↓]"
STOP_WORDS = ("包邮", "正品", "特价", "促销", "热卖")


def display_width(text):
    width = 0
    for char in text:
        width += 2 if unicodedata.east_asian_width(char) in ("W", "F") else 1
    return width


def main():
    parser = argparse.ArgumentParser(description="淘宝标题体检")
    parser.add_argument("--title", action="append", required=True, help="标题，可重复")
    args = parser.parse_args()

    errors = []
    warnings = []

    for title in args.title:
        width = display_width(title.strip())
        if width > 60:
            errors.append(f"标题「{title}」显示宽度 {width}，超过 60 字符（约 30 汉字）")
        elif width > 54:
            warnings.append(f"标题「{title}」宽度 {width}，接近上限，建议留 2-3 字余量")

        for word in re.findall(LIMIT_WORDS, title):
            errors.append(f"标题含极限词「{word}」")

        for symbol in re.findall(SPECIAL, title):
            warnings.append(f"标题含特殊符号「{symbol}」，建议用空格分隔")

        for word in STOP_WORDS:
            if word in title:
                warnings.append(f"标题含无效服务词「{word}」，浪费字数")

        chunks = re.findall(r"[\u4e00-\u9fff]{2,}", title)
        seen = {}
        for chunk in chunks:
            for size in (2, 3):
                for index in range(len(chunk) - size + 1):
                    token = chunk[index:index + size]
                    if token in ("旗舰", "官方", "专营", "专卖"):
                        continue
                    seen[token] = seen.get(token, 0) + 1
        repeated = [token for token, count in seen.items() if count > 1 and len(token) >= 3]
        if repeated:
            warnings.append("疑似重复词：" + "、".join(repeated[:5]))

    print("=== 淘宝标题体检 ===")
    if errors:
        print("\n[ERROR] 必须修改：")
        for item in errors:
            print(f"- {item}")
    if warnings:
        print("\n[WARN] 建议修改：")
        for item in warnings:
            print(f"- {item}")
    if not errors and not warnings:
        print("\n[OK] 标题基础体检通过。")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
