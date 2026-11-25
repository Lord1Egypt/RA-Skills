#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""小红书笔记发布前体检：标题长度、正文、标签、违禁词与导流词。"""

import argparse
import re
import sys


RULES = [
    ("绝对化", r"最好|最佳|最优|最低价|最高级|最强|第一名|国家级|世界级|顶级|绝无仅有|独一无二|100%|百分百|绝对|零风险"),
    ("医疗功效", r"治疗|治愈|根治|抗癌|降血压|降血糖|祛斑|祛痘|美白|减肥|瘦身|排毒"),
    ("金融承诺", r"稳赚|保本|翻倍|暴富|收益保证|年化收益"),
    ("站外导流", r"微信|vx|VX|QQ|手机号|二维码|私信我|加我|主页链接|淘宝店|店铺名"),
    ("诱导互动", r"点赞抽奖|关注抽奖|转发抽奖|集赞|扣1送|评论区扣1"),
    ("虚假背书", r"亲测有效|全网最低|销量第一|央视推荐|明星同款"),
]


def scan(text, label):
    hits = []
    for name, pattern in RULES:
        for match in re.finditer(pattern, text):
            snippet = text[max(0, match.start() - 8): match.end() + 8].replace("\n", " ")
            hits.append((name, match.group(0), snippet))
    return [(label, *hit) for hit in hits]


def main():
    parser = argparse.ArgumentParser(description="小红书笔记体检")
    parser.add_argument("--title", action="append", default=[], help="标题，可重复传入")
    parser.add_argument("--body", default="", help="正文文本")
    parser.add_argument("--body-file", help="从 UTF-8 文件读取正文")
    parser.add_argument("--tags", default="", help="英文逗号分隔的标签")
    args = parser.parse_args()

    if args.body_file:
        with open(args.body_file, "r", encoding="utf-8") as file:
            body = file.read()
    else:
        body = args.body

    tags = [tag.strip().lstrip("#") for tag in args.tags.split(",") if tag.strip()]
    errors = []
    warnings = []
    hits = []

    for title in args.title:
        length = len(title.strip())
        if length > 24:
            errors.append(f"标题「{title}」{length} 字，超过 24 字硬上限")
        elif length > 20:
            warnings.append(f"标题「{title}」{length} 字，建议压到 20 字内")
        hits.extend(scan(title, f"标题「{title}」"))

    body_length = len(re.sub(r"\s", "", body))
    if body_length == 0:
        errors.append("正文为空")
    else:
        if body_length < 300:
            warnings.append(f"正文 {body_length} 字，偏短，建议 500-900 字")
        if body_length > 1200:
            warnings.append(f"正文 {body_length} 字，偏长，建议压到 900 字内")
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n|\n", body) if p.strip()]
        long_paragraphs = [p for p in paragraphs if len(p) > 120]
        if long_paragraphs:
            warnings.append(f"有 {len(long_paragraphs)} 段超过 120 字，建议每段不超过 3 行")
        hits.extend(scan(body, "正文"))

    if len(tags) < 5:
        warnings.append(f"标签 {len(tags)} 个，建议 5-8 个")
    elif len(tags) > 8:
        warnings.append(f"标签 {len(tags)} 个，超过 8 个，建议精简")
    for tag in tags:
        if len(tag) < 2:
            warnings.append(f"标签「{tag}」过短，缺少指向")
        if len(tag) > 14:
            warnings.append(f"标签「{tag}」过长，建议压到 14 字内")
    if len(set(tags)) != len(tags):
        warnings.append("标签有重复")

    print("=== 小红书笔记体检 ===")
    print(f"标题数：{len(args.title)}    正文：{body_length} 字    标签：{len(tags)} 个")
    if errors:
        print("\n[ERROR] 必须修改：")
        for item in errors:
            print(f"- {item}")
    if warnings:
        print("\n[WARN] 建议修改：")
        for item in warnings:
            print(f"- {item}")
    if hits:
        print("\n[RULE] 违禁/风险词：")
        for label, rule, word, snippet in hits:
            print(f"- {label} / {rule}：「{word}」  ...{snippet}...")
    else:
        print("\n[RULE] 未命中内置风险词。平台规则会变化，仍需人工复核。")
    if not errors and not warnings:
        print("\n[OK] 基础体检通过。")

    return 1 if errors or hits else 0


if __name__ == "__main__":
    sys.exit(main())
