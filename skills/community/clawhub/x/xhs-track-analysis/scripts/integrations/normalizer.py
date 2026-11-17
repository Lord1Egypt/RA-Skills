# -*- coding: utf-8 -*-
"""
scripts/integrations/normalizer.py
把 NoteRecord 列表统一输出为：CSV + 主表风格 Markdown，
与 scripts/collector 的产物 schema 一致，供 xhs-track-analysis Skill 直接消费。
"""
import csv
import datetime
import os
from source_base import NoteRecord


def to_csv(records, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=[
            "keyword", "sort", "note_id", "url", "title", "author",
            "author_type", "commercialization", "likes", "collects",
            "comments", "comments_saved", "field_scope",
            "completion_state", "captured_at"
        ])
        w.writeheader()
        for r in records:
            w.writerow({
                "keyword": r.keyword, "sort": r.sort, "note_id": r.note_id,
                "url": r.url, "title": r.title, "author": r.author,
                "author_type": r.author_type, "commercialization": r.commercialization,
                "likes": r.likes, "collects": r.collects, "comments": r.comments,
                "comments_saved": r.comments_saved, "field_scope": r.field_scope,
                "completion_state": r.completion_state,
                "captured_at": r.captured_at,
            })


def to_markdown(records, path):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# 数据采集报告（A 方案 · {ts}）\n\n")
        f.write("> 来源：官方/第三方合规数据平台。本文件为**原始资料**摘取，未做判断；\n")
        f.write("> 请交给 xhs-track-analysis Skill 按 methodology 完成分析（含商业化浓度/达人解读/评论四行为）。\n\n")
        f.write(f"共采集 {len(records)} 条笔记（关键词×排序）。\n\n")
        f.write("## 三、采集记录（已合并去重）\n\n")
        f.write("| 关键词 | 排序角度 | note_id | 作者 | 类型 | 商业化浓度 | 赞 | 藏 | 评 | 已存评论 | 范围/状态 | 链接 | 采集时间 |\n")
        f.write("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n")
        for r in records:
            scope_state = f"{r.field_scope}/{r.completion_state}"
            f.write(f"| {r.keyword} | {r.sort} | {r.note_id} | {r.author} | "
                    f"{r.author_type} | {r.commercialization} | {r.likes} | "
                    f"{r.collects} | {r.comments} | {r.comments_saved} | "
                    f"{scope_state} | {r.url} | {r.captured_at} |\n")


def save(records, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = os.path.join(output_dir, f"raw_notes_A_{ts}.csv")
    md_path = os.path.join(output_dir, f"collection_report_A_{ts}.md")
    to_csv(records, csv_path)
    to_markdown(records, md_path)
    return csv_path, md_path
