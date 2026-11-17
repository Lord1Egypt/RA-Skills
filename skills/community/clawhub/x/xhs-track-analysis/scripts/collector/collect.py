#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
xhs-track-analysis · 受监督有界采集器原型（collect.py）
=====================================================================
⚠️ 合规与责任边界（运行前必读）
---------------------------------------------------------------------
1. 本脚本仅用于**你本人拥有/授权的账号**，在你的浏览器、你本人在场监督下，
   对小红书**公开搜索结果页与公开笔记页**做有限摘取，用于「赛道深度分析」
   的资料准备（即本 Skill 定义的工作：把最慢、最容易漏的资料整理清楚）。
2. 本脚本**不实现任何反爬/风控对抗**：不伪造请求签名（x-s/x-t）、不自动过
   滑块、不伪造设备指纹、不突破登录态私有接口。它只是用普通浏览器把"人手动
   翻页查看"的过程自动化，且全程你可见、可中断。
3. 小红书用户协议可能禁止自动化访问。运行即表示你已知悉并自行承担由此产生的
   账号与合规风险（含《个人信息保护法》项下评论数据处理的合规责任）。本工具作
   者/提供方不承担任何后果。
4. 仅采集公开内容；不采集非公开数据；不对采集数据做超出分析目的的使用。
5. 严格限频、限量与范围（见 config.json）。超出即停止。

运行方式（需先安装）：
    pip install -r requirements.txt
    playwright install chromium
    python3 collect.py config.json
首次会打开浏览器并展示登录二维码，请用手机扫码；扫码后脚本自动开始采集。
=====================================================================
"""

import sys
import json
import time
import csv
import datetime
import os

# playwright 延迟到 main() 导入：未安装时 --help 与配置校验仍可用

# --debug 诊断模式（首次真机运行建议开启，便于定位选择器漂移/页面结构变化）
DEBUG = False
_probed = False


def logd(msg):
    """debug 模式下的诊断日志。"""
    if DEBUG:
        print(f"[DEBUG] {msg}")

# ---------------------------------------------------------------------------
# 免责确认：必须显式键入确认短语才继续
# ---------------------------------------------------------------------------
CONFIRM_PHRASE = "我已知悉并承担合规责任"
DISCLAIMER = """
╔════════════════════════════════════════════════════════════════════════╗
║  受监督有界采集器 · 合规边界                                          ║
║  1) 仅本人/授权账号、本人监督、仅公开页、有限摘取。                    ║
║  2) 不实现任何反爬/签名伪造/风控对抗。                                ║
║  3) 你自行承担账号与法律合规风险。                                    ║
║  4) 仅采集公开内容，不超范围使用。                                    ║
╚════════════════════════════════════════════════════════════════════════╝
"""


def confirm_compliance() -> bool:
    print(DISCLAIMER)
    ans = input(f"请输入确认短语（{CONFIRM_PHRASE}）以继续，其他输入将退出：\n> ").strip()
    return ans == CONFIRM_PHRASE


# ---------------------------------------------------------------------------
# 选择器（XHS 前端会变，集中在此便于维护；运行前按需核对）
# ---------------------------------------------------------------------------
SELECTORS = {
    "search_input": ["input[name='keyword']", "#search-input", "input[placeholder*='搜索']"],
    "search_button": ["button.search-button", "button[type='submit']", ".search-button"],
    "sort_tab": "div.sort-bar div[class*='sort']",   # 按文本匹配 综合/最新/...
    "note_card": ["section.note-item", "div.note-item", "a.cover", ".feeds-container .note-item"],
    "note_title": [".title", ".content", ".note-title", "a.title"],
    "note_author": [".author .name", ".name", ".author-wrapper .name"],
    "note_likes": [".like-wrapper .count", ".like .count", ".count"],
    "note_collects": [".collect-wrapper .count", ".collect .count"],
    "note_comments": [".comment-wrapper .count", ".comment .count"],
    "note_url": "a.cover",
    # 详情页（评论采集时进入）
    "detail_body": [".note-content .content", ".content .note-text", ".note-text"],
    "comment_item": ["div.comment-item", ".comments-container .comment-item", ".comment-item"],
    "comment_content": [".content .note-text", "span.note-text", ".content"],
}

XHS_BASE = "https://www.xiaohongshu.com"


def _first_match(page, selectors, **kwargs):
    """尝试多个候选选择器，返回首个命中的元素。"""
    for sel in selectors:
        try:
            el = page.query_selector(sel, **kwargs)
            if el:
                return el
        except Exception:
            continue
    return None


def probe_selectors(page):
    """debug 模式：统计主要选择器的命中数，帮助定位前端结构变化（选择器漂移）。"""
    probes = {
        "排序标签": [SELECTORS["sort_tab"]],
        "笔记卡片": SELECTORS["note_card"],
        "标题": SELECTORS["note_title"],
        "作者": SELECTORS["note_author"],
        "点赞数": SELECTORS["note_likes"],
        "收藏数": SELECTORS["note_collects"],
        "评论数": SELECTORS["note_comments"],
        "详情正文": SELECTORS["detail_body"],
        "评论条目": SELECTORS["comment_item"],
        "评论内容": SELECTORS["comment_content"],
    }
    for name, sels in probes.items():
        for sel in sels:
            try:
                n = len(page.query_selector_all(sel))
                logd(f"选择器探针 [{name}] {sel!r} → 命中 {n}")
            except Exception as e:
                logd(f"选择器探针 [{name}] {sel!r} → 异常: {e}")


def _text_or(page, selectors, default=""):
    el = _first_match(page, selectors)
    return el.inner_text().strip() if el else default


def login_via_qr(page, timeout=180):
    """打开首页，等待用户扫码登录。通过 web_session cookie 判断是否登录。"""
    print("[登录] 打开小红书首页，请在弹出的浏览器中用手机扫码登录…")
    page.goto(XHS_BASE + "/explore", wait_until="domcontentloaded")
    # 若出现登录二维码弹窗，等待用户在浏览器中扫码
    deadline = time.time() + timeout
    while time.time() < deadline:
        cookies = page.context.cookies()
        if any(c["name"] == "web_session" for c in cookies):
            print("[登录] 检测到 web_session，登录成功。")
            return True
        time.sleep(3)
    print("[登录] 超时未登录，退出。")
    return False


def apply_sort(page, sort_name, cfg):
    """点击排序标签（按文本匹配）。失败则忽略（使用默认综合排序）。"""
    try:
        tabs = page.query_selector_all(SELECTORS["sort_tab"])
        for t in tabs:
            if sort_name in (t.inner_text() or ""):
                t.click()
                time.sleep(1.5)
                return True
    except Exception as e:
        print(f"[排序] 应用「{sort_name}」失败，继续使用当前排序：{e}")
    return False


def parse_count(text):
    """把 '1.2万' / '3.4k' / '1234' 转成整数。"""
    if not text:
        return 0
    text = text.strip().replace(" ", "")
    try:
        if "万" in text:
            return int(float(text.replace("万", "")) * 10000)
        if "w" in text.lower():
            return int(float(text.lower().replace("w", "")) * 10000)
        return int(float(text))
    except Exception:
        return 0


def collect_search(page, keyword, sort_name, cfg):
    """对一个关键词+排序做有限摘取，返回笔记字典列表。"""
    global _probed
    q = "/search_result?keyword=" + keyword
    page.goto(XHS_BASE + q, wait_until="domcontentloaded")
    time.sleep(2)
    apply_sort(page, sort_name, cfg)
    logd(f"[search] 当前页面 {page.url}（关键词={keyword} 排序={sort_name}）")
    if not _probed:
        probe_selectors(page)
        _probed = True

    notes = []
    scrolls = int(cfg.get("scroll_times", 5))
    max_notes = int(cfg.get("max_notes_per_query", 20))
    for i in range(scrolls):
        if len(notes) >= max_notes:
            break
        cards = _all_first_match(page, SELECTORS["note_card"])
        logd(f"[search] 第 {i+1} 轮滚动：可见卡片 {len(cards)} 个，已摘取 {len(notes)} 条")
        for card in cards:
            if len(notes) >= max_notes:
                break
            try:
                title = _text_or(card, SELECTORS["note_title"])
                author = _text_or(card, SELECTORS["note_author"])
                likes = parse_count(_text_or(card, SELECTORS["note_likes"]))
                collects = parse_count(_text_or(card, SELECTORS["note_collects"]))
                comments = parse_count(_text_or(card, SELECTORS["note_comments"]))
                if not title and not author and not likes:
                    logd("[search] 卡片字段全部为空，疑似选择器漂移或页面结构变化")
                href = ""
                try:
                    a = card.query_selector("a.cover") or card.query_selector("a")
                    href = a.get_attribute("href") if a else ""
                except Exception:
                    pass
                note_id = href.rstrip("/").split("/")[-1].split("?")[0] if href else ""
                notes.append({
                    "keyword": keyword,
                    "sort": sort_name,
                    "note_id": note_id,
                    "url": (XHS_BASE + href) if href.startswith("/") else href,
                    "title": title,
                    "author": author,
                    "author_type": "unknown",
                    "commercialization": "unknown",
                    "likes": likes,
                    "collects": collects,
                    "comments": comments,
                    "comments_saved": 0,
                    "field_scope": "visible_list_card",
                    "completion_state": "complete_visible_list_card",
                    "comment_sample": [],
                    "captured_at": datetime.date.today().isoformat(),
                })
            except Exception as e:
                print(f"[摘取] 单卡失败，跳过: {e}")
        # 去重后再滚
        seen = {n["note_id"] for n in notes if n["note_id"]}
        page.mouse.wheel(0, 1200)
        time.sleep(float(cfg.get("delay_sec", 3)))
    # 去重
    uniq = {}
    for n in notes:
        uniq.setdefault(n["note_id"] or n["url"], n)
    return list(uniq.values())


def _all_first_match(page, selectors):
    """返回首个命中的选择器对应的全部元素（用于评论列表）。"""
    for sel in selectors:
        try:
            els = page.query_selector_all(sel)
            if els:
                return els
        except Exception:
            continue
    return []


def collect_detail(page, note, cfg):
    """进入单篇详情页：采正文与前 N 条一级评论，并更新完成状态。

    状态规则（借鉴"数据契约"思想，本地实现）：
      - 评论滚动到当前可见末端（连续 2 次滚动无新增）→ complete_visible_note
      - 评论达到用户设定的正数上限 → partial_comments_limit（非全量，诚实标注）
      - 页面结构变化导致无法定位 → partial_selector_drift
    """
    url = note.get("url", "")
    if not url:
        return
    limit = int(cfg.get("comments_per_note", 10))
    note["completion_state"] = "partial_selector_drift"
    logd(f"[detail] 进入详情页 {url}")
    try:
        page.goto(url, wait_until="domcontentloaded")
        time.sleep(2)
        body = _text_or(page, SELECTORS["detail_body"])
        logd(f"[detail] 正文选择器命中: {'是' if body else '否（检查 detail_body）'}")
        if body:
            note["title"] = body if not note.get("title") else note["title"]
            note["body"] = body[:500]
        comments = []
        stagnant = 0
        last_count = 0
        for i in range(int(cfg.get("comment_scrolls", 5))):
            items = _all_first_match(page, SELECTORS["comment_item"])
            for item in items:
                text = _text_or(item, SELECTORS["comment_content"]).replace("\n", " ")
                if text and text not in comments:
                    comments.append(text)
                if len(comments) >= limit:
                    break
            logd(f"[detail] 评论轮次 {i+1}/{cfg.get('comment_scrolls', 5)}：可见评论条目 {len(items)}，已保存 {len(comments)} 条")
            if len(comments) >= limit:
                note["completion_state"] = "partial_comments_limit"
                logd("[detail] 状态：达到评论上限 → partial_comments_limit")
                break
            if len(comments) == last_count:
                stagnant += 1
            else:
                stagnant = 0
            last_count = len(comments)
            if stagnant >= 2:
                note["completion_state"] = "complete_visible_note"
                logd("[detail] 状态：连续滚动无新增评论 → complete_visible_note")
                break
            page.mouse.wheel(0, 800)
            time.sleep(float(cfg.get("delay_sec", 3)))
        else:
            if note["completion_state"] != "partial_comments_limit":
                note["completion_state"] = "complete_visible_note"
                logd("[detail] 状态：滚动耗尽仍未达上限 → complete_visible_note")
        note["comment_sample"] = comments[:limit]
        note["comments_saved"] = len(comments)
        note["field_scope"] = "detail_opened"
        if not body and not comments:
            # 正文与评论均未定位到：更可能是页面结构变化/登录阻断，而非"已采到末端"
            note["completion_state"] = "partial_selector_drift"
            logd("[detail] 状态：正文与评论均未定位到 → partial_selector_drift")
    except Exception as e:
        print(f"[详情] {url} 采集失败: {e}")
        logd(f"[detail] 采集失败详情: {e!r}")
        note["completion_state"] = "partial_selector_drift"


def save_outputs(all_notes, cfg):
    out_dir = cfg.get("output_dir", "output")
    os.makedirs(out_dir, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    csv_path = os.path.join(out_dir, f"raw_notes_{ts}.csv")
    fields = ["keyword", "sort", "note_id", "url", "title", "author", "author_type",
              "commercialization", "likes", "collects", "comments", "comments_saved",
              "field_scope", "completion_state", "captured_at"]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for n in all_notes:
            w.writerow({k: n.get(k, "") for k in fields})
    print(f"[输出] CSV: {csv_path}（{len(all_notes)} 条）")

    # 主表-风格 Markdown（仅原始资料，判断留给 Skill/人工）
    md_path = os.path.join(out_dir, f"collection_report_{ts}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# 采集报告 · {ts}\n\n")
        f.write("> 本文件为**原始公开资料**摘取，未做商业化浓度/达人解读/评论四行为判断；\n")
        f.write("> 请交给 xhs-track-analysis Skill 按 methodology 完成分析。\n\n")
        f.write(f"共采集 {len(all_notes)} 条笔记（按关键词×排序）。\n\n")
        f.write("## 三、采集记录（每轮一行，已合并去重）\n\n")
        f.write("| 关键词 | 排序角度 | note_id | 作者 | 赞 | 藏 | 评 | 已存评论 | 范围/状态 | 链接 | 采集时间 |\n")
        f.write("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n")
        for n in all_notes:
            scope_state = f"{n['field_scope']}/{n['completion_state']}"
            f.write(f"| {n['keyword']} | {n['sort']} | {n['note_id']} | {n['author']} | "
                    f"{n['likes']} | {n['collects']} | {n['comments']} | {n['comments_saved']} | "
                    f"{scope_state} | {n['url']} | {n['captured_at']} |\n")
        commented = [n for n in all_notes if n.get("comment_sample") or n.get("body")]
        if commented:
            f.write("\n## 评论明细（仅进过详情页的笔记）\n\n")
            for n in commented:
                f.write(f"- **{n['title'][:40]}**（{n['author']}，{n['url']}，状态 {n['completion_state']}）\n")
                if n.get("body"):
                    f.write(f"  - 正文摘要：{n['body'][:200]}\n")
                for c in n["comment_sample"]:
                    f.write(f"  - 评论：{c}\n")
    print(f"[输出] Markdown: {md_path}")


def main():
    global DEBUG
    args = sys.argv[1:]
    if "--debug" in args:
        DEBUG = True
        args = [a for a in args if a != "--debug"]
        print("[debug] 诊断日志已开启（--debug）")
    if args and args[0] in ("--help", "-h"):
        print("用法: python3 collect.py <config.json> [--debug]")
        print("示例: python3 collect.py config.json --debug")
        print("配置字段见 config.example.json：keywords(必填)、sorts、max_notes_per_query、scroll_times、delay_sec、output_dir；")
        print("可选评论采集：enable_comments(true/false)、comment_note_limit(进详情的笔记数)、comments_per_note(每篇最多评论数)、comment_scrolls。")
        print("--debug：输出选择器探针与逐轮采集诊断日志（首次真机运行建议开启）。")
        sys.exit(0)
    if len(args) < 1:
        sys.exit("错误: 缺少 config.json 参数。用法: python3 collect.py <config.json>")
    cfg_path = args[0]
    if not os.path.exists(cfg_path):
        sys.exit(f"错误: 找不到配置文件: {cfg_path}\n提示: 先复制 config.example.json 为 config.json 并填写 keywords。")
    try:
        with open(cfg_path, encoding="utf-8") as f:
            cfg = json.load(f)
    except json.JSONDecodeError as e:
        sys.exit(f"错误: 配置文件不是合法 JSON（第 {e.lineno} 行附近）: {e.msg}")
    except OSError as e:
        sys.exit(f"错误: 读取配置文件失败: {e}")

    keywords = cfg.get("keywords", [])
    if not isinstance(keywords, list) or not keywords:
        sys.exit("错误: 配置缺少 keywords（非空字符串列表）。\n提示: 参考 config.example.json 填写要研究的关键词，如 [\"熟龄肌抗老\", \"抗老面霜\"]。")
    if not all(isinstance(k, str) and k.strip() for k in keywords):
        sys.exit("错误: keywords 中存在空字符串或非字符串项，请检查配置。")

    sorts = cfg.get("sorts", ["综合", "最新", "最多点赞", "最多收藏", "最多评论"])
    if not isinstance(sorts, list) or not sorts:
        sys.exit("错误: 配置 sorts 为空：请至少保留一种排序角度（如「最新」）。")
    if not all(isinstance(s, str) and s.strip() for s in sorts):
        sys.exit("错误: sorts 中存在空字符串或非字符串项，请检查配置。")

    for key in ("max_notes_per_query", "scroll_times", "delay_sec"):
        if key not in cfg:  # 缺省用脚本内置默认值，不校验
            continue
        try:
            val = float(cfg[key])
        except (TypeError, ValueError):
            sys.exit(f"错误: {key} 必须为数字（当前值: {cfg[key]!r}）。")
        if val <= 0:
            sys.exit(f"错误: {key} 必须为正数（当前值: {cfg[key]!r}）。")

    enable_comments = cfg.get("enable_comments", False)
    if not isinstance(enable_comments, bool):
        sys.exit("错误: enable_comments 必须为 true / false。")
    for key in ("comment_note_limit", "comments_per_note", "comment_scrolls"):
        if key not in cfg:
            continue
        try:
            val = int(cfg[key])
        except (TypeError, ValueError):
            sys.exit(f"错误: {key} 必须为整数（当前值: {cfg[key]!r}）。")
        if val <= 0:
            sys.exit(f"错误: {key} 必须为正整数（当前值: {cfg[key]!r}）。")
    if enable_comments and not cfg.get("comments_per_note"):
        sys.exit("错误: enable_comments=true 时需设置 comments_per_note（每篇最多保存的评论数）。")

    output_dir = cfg.get("output_dir", "output")
    if not isinstance(output_dir, str) or not output_dir.strip():
        sys.exit("错误: output_dir 不能为空。")

    if not confirm_compliance():
        sys.exit("未确认合规，已退出。")

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("未安装 playwright。请先: pip install -r requirements.txt && playwright install chromium")

    all_notes = []
    with sync_playwright() as p:
        # headed=True：用户在场监督，可见二维码与页面，可随时中断
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent=("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/124.0 Safari/537.36")
        )
        page = context.new_page()
        if not login_via_qr(page):
            browser.close()
            sys.exit("登录失败。")

        for kw in keywords:
            for s in sorts:
                print(f"[采集] 关键词={kw} 排序={s}")
                try:
                    notes = collect_search(page, kw, s, cfg)
                    all_notes.extend(notes)
                except Exception as e:
                    print(f"[采集] {kw}/{s} 出错跳过: {e}")
                time.sleep(float(cfg.get("delay_sec", 3)))

        # 评论采集（可选）：对高互动笔记进入详情页，采正文与前 N 条一级评论
        if enable_comments:
            limit = int(cfg.get("comment_note_limit", 3))
            candidates = sorted(all_notes, key=lambda n: n["likes"], reverse=True)[:limit]
            print(f"[评论] 对 {len(candidates)} 条高互动笔记进入详情页采集评论…")
            for n in candidates:
                collect_detail(page, n, cfg)
                time.sleep(float(cfg.get("delay_sec", 3)))
        browser.close()

    save_outputs(all_notes, cfg)
    print("[完成] 受监督采集结束。请人工核对并对商业化浓度/达人/评论做判断。")


if __name__ == "__main__":
    main()
