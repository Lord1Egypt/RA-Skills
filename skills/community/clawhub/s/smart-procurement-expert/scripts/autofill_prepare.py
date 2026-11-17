#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧招采专家 · 响应文件内容自动填充管线（autofill prepare）
============================================================
把「招标解析结果 + 结构化内容素材」合成为可直接生成章节初稿 docx 的配置。

端到端链路：
    ① parse_bidding_docx.py  招标文件.docx  → parsed_config.json   （结构与格式）
    ② （人工/LLM）撰写 content.json          （每章的起草正文与图表占位）
    ③ autofill_prepare.py     parsed + content → bid_config.json     （注入 body/chart）
    ④ generate_bid_template.js bid_config.json → 投标文件.docx      （渲染章节初稿）

content.json 结构示例：
{
  "project": { "name": "...", "code": "...", "copyMark": "【正本】" },   # 可选，缺省沿用 parsed
  "chapters": [
    { "match": "公司概况", "body": ["我方成立于...", "..."], "chart": "公司组织架构图" },
    { "match": "施工方案", "body": "采用...工艺。", "chart": {"title":"施工总平图","hint":"CAD 导出"} }
  ]
}

匹配规则：对 parsed 的每个章节，按出现顺序取首个 content 项，其 match 关键词（不区分大小写）
出现在章节标题中即注入；同一 match 仅命中首个匹配章节。未命中章节保留空 body（生成器渲染占位）。

输出：
  - bid_config.json（含注入 body/chart 的 chapters，可直接喂 generate_bid_template.js）
  - 终端打印「已填充 / 未填充」清单，便于查漏补缺

依赖：仅 Python 标准库。
"""

import argparse
import copy
import json
import sys


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def find_content_for(chapter_title, contents):
    """返回首个 match 命中章节标题的 content 项（并标记已用）。"""
    title = (chapter_title or "").lower()
    for item in contents:
        m = (item.get("match") or "").strip().lower()
        if m and m in title:
            return item
    return None


def run(parsed_path, content_path, out_path):
    parsed = load_json(parsed_path)
    content = load_json(content_path)

    contents = content.get("chapters", [])
    used = set()
    filled = []
    unfilled = []

    enriched_chapters = []
    for ch in parsed.get("chapters", []):
        title = ch.get("title", "")
        # 找未使用的、match 命中的 content（每个 match 仅用一次）
        hit = None
        for idx, item in enumerate(contents):
            if idx in used:
                continue
            m = (item.get("match") or "").strip().lower()
            if m and m in (title or "").lower():
                hit = (idx, item)
                break
        new_ch = copy.deepcopy(ch)
        if hit is not None:
            idx, item = hit
            used.add(idx)
            if "body" in item:
                new_ch["body"] = item["body"]
            if "chart" in item:
                new_ch["chart"] = item["chart"]
            filled.append((title, item.get("match")))
        else:
            unfilled.append(title)
        enriched_chapters.append(new_ch)

    # 组装输出配置：以 parsed 为基底，覆盖 chapters，可选覆盖 project
    out_cfg = copy.deepcopy(parsed)
    out_cfg["chapters"] = enriched_chapters
    if content.get("project"):
        out_cfg["project"] = content["project"]

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out_cfg, f, ensure_ascii=False, indent=2)

    # 打印清单
    print(f"[OK] 已生成 {out_path}")
    print(f"\n✅ 已填充章节（{len(filled)}）：")
    for title, m in filled:
        print(f"   · 「{title}」 ← match=\"{m}\"")
    print(f"\n⬜ 未填充章节（{len(unfilled)}，生成后将保留占位，需人工补全）：")
    for title in unfilled:
        print(f"   · 「{title}」")

    unused = [c.get("match") for i, c in enumerate(contents) if i not in used]
    if unused:
        print(f"\n⚠️ content.json 中未匹配到章节的条目（match 关键词需与章节标题一致）：{unused}")
    return out_cfg


def main():
    ap = argparse.ArgumentParser(description="智慧招采专家 · 响应文件内容自动填充")
    ap.add_argument("--parsed", required=True, help="parse_bidding_docx.py 产出的 config.json")
    ap.add_argument("--content", required=True, help="content.json（章节起草正文与图表占位）")
    ap.add_argument("--out", default="bid_config.json", help="输出的 bid_config.json 路径")
    args = ap.parse_args()
    try:
        run(args.parsed, args.content, args.out)
    except Exception as e:
        print(f"[错误] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
