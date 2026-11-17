#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""抓取央视《新闻联播》官方文字稿（第一信源，零依赖）

用法: python3 fetch_xwlb.py [YYYYMMDD] [输出目录]
- 指定日期: 直取 day/YYYYMMDD.shtml 日期页（主路径，纯 HTML 无 JS）
- 无日期: 默认取 index.shtml 首屏最新一期（index 改版后大概率拿不到，保留兜底）
- 输出目录: 不传时依次取环境变量 XWLB_OUT、默认 ./data/xwlb（相对当前工作目录）

流程:
1. https://tv.cctv.com/lm/xwlb/day/YYYYMMDD.shtml 取当日全部条目 URL 列表
2. 逐条抓视频页，提取「主要内容」区块中的《央视网消息（新闻联播）》全文
3. 汇总写入 <输出目录>/YYYYMMDD.md

信源说明:
- tv.cctv.com 为央视官网，文字稿与播出内容对齐，置信度 ★★★★★
- 每页 size 约 28KB，抓取间隔 1s，单期 19-26 条，总耗时 <1min
- 当日可用性: 19:00 播出后约 20:00-20:30 全量上线（实测某期 20:22 即 17 条 16 条含全文）
- 部分条目（如领导人会谈类）仅一行标题级简介，无央视网消息正文，
  属正常情况（官即如此），标注 [仅标题] 即可。
"""
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
INDEX = "https://tv.cctv.com/lm/xwlb/index.shtml"
DAY = "https://tv.cctv.com/lm/xwlb/day/{ymd}.shtml"  # index.shtml 已改版为 JS 动态加载（反爬 cookie + 空容器），静态抓取失效；day/ 日期页可直接取当日全部条目


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="ignore")


def clean(t: str) -> str:
    t = t.replace("&ldquo;", "\u201c").replace("&rdquo;", "\u201d")
    t = t.replace("&lsquo;", "\u2018").replace("&rsquo;", "\u2019")
    t = t.replace("&mdash;", "\u2014").replace("&nbsp;", " ").replace("&amp;", "&")
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else None
    outdir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(os.environ.get("XWLB_OUT", "data/xwlb"))
    items = []
    # 路径1（主）: 指定日期时直接抓 day/YYYYMMDD.shtml
    if target:
        try:
            html = fetch(DAY.format(ymd=target))
            items = re.findall(
                r'href="(https?://tv\.cctv\.com/\d{4}/\d{2}/\d{2}/VIDE\w+\.shtml)"[^>]*title="([^"]+)"',
                html,
            )
            if items:
                print(f"[day/{target}] 命中 {len(items)} 个链接")
        except Exception as e:
            print(f"[day/{target}] 抓取失败: {e}")
    # 路径2（fallback/默认无日期）: index.shtml 首屏（改版后大概率拿不到，保留兜底）
    if not items:
        html = fetch(INDEX)
        items = re.findall(
            r'href="(https?://tv\.cctv\.com/\d{4}/\d{2}/\d{2}/VIDE\w+\.shtml)"[^>]*title="([^"]+)"',
            html,
        )
        if target:
            date_pat = f"/{target[:4]}/{target[4:6]}/{target[6:8]}/"
            items = [it for it in items if date_pat in it[0]]
    if not items:
        print("未找到条目：day 页与 index 首页均无结果。可能是当日节目尚未上线")
        sys.exit(1)

    # 去重（同一标题可能有多个分页入口）
    seen, uniq = set(), []
    for u, t in items:
        if t not in seen:
            seen.add(t)
            uniq.append((u, t))
    items = uniq
    # 注意: 开场整期入口条目的 URL 内嵌的是次日日期，产出文件必须以 target 参数命名（脚本已处理）
    date_id = target or "".join(re.search(r"/(\d{4})/(\d{2})/(\d{2})/", items[0][0]).groups())
    print(f"[{date_id}] 共 {len(items)} 条官方条目")

    out_lines = [f"# 新闻联播 {date_id} 官方文字稿", "信源: tv.cctv.com/lm/xwlb（央视官网，★★★★★）", ""]
    ok, brief_only = 0, 0
    for i, (url, title) in enumerate(items, 1):
        title = clean(title).replace("[视频] ", "")
        try:
            page = fetch(url)
        except Exception as e:
            out_lines.append(f"## {i}. {title}\n[抓取失败: {e}]\n")
            continue
        m = re.search(r"(央视网消息|本台消息|记者从[\w\S]{0,30}了解到)[\s\S]{0,6000}?</div>", page)
        if m:
            body = clean(m.group(0).rsplit("</div>", 1)[0])
            ok += 1
        else:
            body = "[仅标题级简介，官方未配文字稿]"
            brief_only += 1
        out_lines.append(f"## {i}. {title}\n来源: {url}\n\n{body}\n")
        time.sleep(1)

    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / f"{date_id}.md"
    out.write_text("\n".join(out_lines), encoding="utf-8")
    print(f"完成: {ok} 条含全文, {brief_only} 条仅标题 -> {out}")


if __name__ == "__main__":
    main()
