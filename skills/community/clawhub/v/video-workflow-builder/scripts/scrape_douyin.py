#!/usr/bin/env python3
"""
抓取抖音用户主页账号数据、全部视频指标与评论，生成分析报告。

用法:
    python3 scrape_douyin.py --url https://www.douyin.com/user/MS4w...
    python3 scrape_douyin.py --url https://www.douyin.com/user/MS4w... --session session.json

依赖:
    pip install playwright && playwright install chromium
"""

import argparse
import datetime
import json
import os
import re
import sys
import time


def parse_args():
    parser = argparse.ArgumentParser(description="抓取抖音用户主页数据并生成分析报告")
    parser.add_argument("--url", required=True, help="抖音用户主页 URL")
    parser.add_argument("--session", default="", help="session storage 文件路径（默认自动生成）")
    parser.add_argument("--data-dir", default="", help="输出目录（默认脚本同级 data/）")
    parser.add_argument("--max-comments", type=int, default=20, help="每个视频抓取评论数上限")
    parser.add_argument("--timeout", type=int, default=120, help="扫码登录超时秒数")
    return parser.parse_args()


def resolve_data_dir(script_dir, cli_override):
    if cli_override:
        os.makedirs(cli_override, exist_ok=True)
        return cli_override
    d = os.path.join(script_dir, "data")
    os.makedirs(d, exist_ok=True)
    return d


def launch_browser(session_path=""):
    """启动非 headless Chromium，返回 (p, browser, context, page)。"""
    from playwright.sync_api import sync_playwright
    p = sync_playwright().start()
    browser = p.chromium.launch(
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
        ],
    )
    if session_path and os.path.isfile(session_path):
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            storage_state=session_path,
        )
        print("已加载 session:", session_path)
    else:
        context = browser.new_context(viewport={"width": 1280, "height": 800})
    page = context.new_page()
    return p, browser, context, page


def login_if_needed(page, timeout, session_path):
    """导航到抖音首页，如果需要登录则等待用户扫码。"""
    page.goto("https://www.douyin.com", wait_until="domcontentloaded", timeout=30000)
    time.sleep(3)

    logged_in_selectors = [
        'text=发布视频',
        '[data-e2e="user-avatar"]',
        'img[alt*="头像"]',
    ]
    for sel in logged_in_selectors:
        try:
            if page.locator(sel).first.is_visible(timeout=3000):
                print("[已登录] 检测到登录状态")
                return
        except Exception:
            continue

    print("=" * 50)
    print("请在浏览器中扫码登录抖音")
    print("（%d秒超时，登录后请等待页面跳转到抖音首页）" % timeout)
    print("=" * 50)

    try:
        page.locator('text=登录').first.click(timeout=5000)
    except Exception:
        pass
    time.sleep(2)

    try:
        page.locator('text=扫码登录').first.click(timeout=3000)
    except Exception:
        pass

    start = time.time()
    while time.time() - start < timeout:
        for sel in logged_in_selectors:
            try:
                if page.locator(sel).first.is_visible(timeout=2000):
                    print("[登录成功]")
                    time.sleep(2)
                    return
            except Exception:
                continue
        time.sleep(3)

    raise TimeoutError("扫码登录超时（%d秒），请重新运行" % timeout)


def save_session(context, session_path):
    """保存浏览器 session 到文件。"""
    context.storage_state(path=session_path)
    print("session 已保存:", session_path)


def _parse_count(text):
    """将 '1.2万' / '1234' 解析为整数。"""
    if not text:
        return 0
    text = text.strip().replace(",", "").replace(" ", "")
    if "亿" in text:
        return int(float(text.replace("亿", "")) * 100000000)
    if "万" in text:
        return int(float(text.replace("万", "")) * 10000)
    try:
        return int(text)
    except ValueError:
        return 0


def _wait_for_text(page, selectors, timeout=10000):
    """尝试一组选择器，返回第一个有可见文本的元素文本。"""
    for sel in selectors:
        try:
            el = page.locator(sel).first
            el.wait_for(state="visible", timeout=timeout)
            text = el.inner_text().strip()
            if text:
                return text
        except Exception:
            continue
    return ""


def scrape_account(page, url):
    """导航到用户主页，提取账号级数据。"""
    print("正在抓取主页数据:", url)
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    time.sleep(5)  # 等 JS 渲染完成

    account = {
        "nickname": "",
        "douyin_id": "",
        "avatar_url": "",
        "signature": "",
        "follower_count": 0,
        "following_count": 0,
        "total_likes": 0,
        "video_count": 0,
        "verified_badge": None,
        "url": url,
        "fetched_at": datetime.datetime.now().isoformat(),
    }

    # 昵称
    account["nickname"] = _wait_for_text(page, [
        '[data-e2e="user-info-name"]',
        'h1[class*="name"]',
        '[class*="profile"] h1',
        'span[class*="nickname"]',
    ], timeout=5000)

    # 抖音号
    account["douyin_id"] = _wait_for_text(page, [
        '[data-e2e="user-info-id"]',
        'span[class*="short-id"]',
        'text=/抖音号:.*/',
    ], timeout=3000)
    if account["douyin_id"]:
        account["douyin_id"] = account["douyin_id"].replace("抖音号:", "").replace("抖音号：", "").strip()

    # 简介
    account["signature"] = _wait_for_text(page, [
        '[data-e2e="user-info-desc"]',
        'span[class*="signature"]',
        'p[class*="desc"]',
    ], timeout=3000)

    # 粉丝数、关注数、获赞数 —— 使用通用的统计项选择器
    stat_items = page.locator('[data-e2e="user-info-stats"] span, [class*="stats"] span, [class*="count"]').all()
    stat_texts = []
    for item in stat_items:
        try:
            text = item.inner_text().strip()
            if text:
                stat_texts.append(text)
        except Exception:
            continue

    # 查找"获赞"、"关注"、"粉丝"附近的数字
    # 抖音主页的统计数据通常在一行中显示
    all_text = page.locator('[data-e2e="user-info-stats"], [class*="stats"], [class*="user-info"]').first.inner_text() if page.locator('[data-e2e="user-info-stats"], [class*="stats"], [class*="user-info"]').count() > 0 else ""

    # 用模式匹配提取数字
    follower_match = re.search(r"(\d[\d,.]*[亿万]?)\s*(?:粉丝|获赞)", all_text)
    if not follower_match:
        follower_match = re.search(r"(?:粉丝|获赞)\s*:?\s*(\d[\d,.]*[亿万]?)", all_text)

    # 遍历 stat_texts 按位置推断
    # 典型结构: "获赞 X  关注 Y  粉丝 Z" 或 "X 获赞  Y 关注  Z 粉丝"
    for i, t in enumerate(stat_texts):
        if "获赞" in t or "赞" in t:
            # 数字可能在前面或后面
            num = re.search(r"(\d[\d,.]*[亿万]?)", t)
            if num:
                account["total_likes"] = _parse_count(num.group(1))
        elif "关注" in t:
            num = re.search(r"(\d[\d,.]*[亿万]?)", t)
            if num:
                account["following_count"] = _parse_count(num.group(1))
        elif "粉丝" in t:
            num = re.search(r"(\d[\d,.]*[亿万]?)", t)
            if num:
                account["follower_count"] = _parse_count(num.group(1))

    # 作品数
    video_count_text = _wait_for_text(page, [
        '[data-e2e="user-tab-video"] span',
        'text=/作品.*\d/',
    ], timeout=3000)
    count_match = re.search(r"(\d[\d,.]*[亿万]?)", video_count_text or "")
    if count_match:
        account["video_count"] = _parse_count(count_match.group(1))

    # 认证标识
    try:
        badge = page.locator('[data-e2e="verified-badge"], [class*="verified"], [class*="certify"]').first
        if badge.is_visible(timeout=2000):
            account["verified_badge"] = badge.inner_text().strip()
    except Exception:
        pass

    print("账号: %s (粉丝: %s, 获赞: %s, 作品: %s)" % (
        account["nickname"],
        account["follower_count"],
        account["total_likes"],
        account["video_count"],
    ))
    return account


def collect_video_links(page, expected_count=0):
    """在用户主页滚动加载全部作品，返回视频详情页 URL 列表。"""
    print("正在滚动加载作品列表...")

    # 确保在"作品"Tab
    try:
        page.locator('text=作品').first.click(timeout=3000)
    except Exception:
        pass
    time.sleep(2)

    collected = []
    seen = set()
    scroll_attempts = 0
    max_scrolls = 200  # 安全上限
    last_count = 0
    no_new_count = 0

    while scroll_attempts < max_scrolls:
        # 收集当前页面可见的视频链接
        links = page.locator('a[href*="/video/"]').all()
        for link in links:
            try:
                href = link.get_attribute("href")
                if href and "/video/" in href:
                    full_url = "https://www.douyin.com" + href.split("?")[0] if href.startswith("/") else href.split("?")[0]
                    if full_url not in seen:
                        seen.add(full_url)
                        collected.append(full_url)
            except Exception:
                continue

        # 也尝试通过图片父级链接收集
        img_links = page.locator('img[src*="douyinpic.com"], img[src*="dyci"]').all()
        for img in img_links:
            try:
                parent_a = img.locator("xpath=ancestor::a")
                if parent_a.count() > 0:
                    href = parent_a.first.get_attribute("href")
                    if href and "/video/" in href:
                        full_url = "https://www.douyin.com" + href.split("?")[0] if href.startswith("/") else href.split("?")[0]
                        if full_url not in seen:
                            seen.add(full_url)
                            collected.append(full_url)
            except Exception:
                continue

        current_count = len(collected)
        print("  已收集 %d 个视频链接..." % current_count, end="\r")

        if current_count == last_count:
            no_new_count += 1
        else:
            no_new_count = 0
            last_count = current_count

        # 如果预期数量和收集数量匹配，停止
        if expected_count > 0 and current_count >= expected_count:
            break

        # 连续 5 次无新链接则停止
        if no_new_count >= 5:
            break

        # 向下滚动
        page.evaluate("window.scrollBy(0, 800)")
        time.sleep(1.5)
        scroll_attempts += 1

    print("")
    print("收集完成: %d 个视频链接" % len(collected))
    return collected


def scrape_video(page, video_url):
    """打开视频详情页，提取视频级数据。"""
    video = {
        "video_id": "",
        "url": video_url,
        "title": "",
        "cover_url": "",
        "duration_sec": 0,
        "publish_time": "",
        "views": 0,
        "likes": 0,
        "comments_count": 0,
        "shares": 0,
        "hashtags": [],
        "error": "",
    }

    video_id_match = re.search(r"/video/(\d+)", video_url)
    video["video_id"] = video_id_match.group(1) if video_id_match else video_url.rsplit("/", 1)[-1]

    try:
        page.goto(video_url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(4)  # 等 JS 渲染
    except Exception as e:
        video["error"] = "页面加载失败: %s" % str(e)
        return video

    # 标题 / 描述
    try:
        title_el = page.locator('[data-e2e="video-detail-title"], h1[class*="title"], [class*="video-info"] span, [class*="desc"]').first
        if title_el.is_visible(timeout=5000):
            video["title"] = title_el.inner_text().strip()
    except Exception:
        pass

    # 如果标题没抓到，尝试从页面 title 提取
    if not video["title"]:
        try:
            video["title"] = page.title()
        except Exception:
            pass

    # 发布时间
    try:
        time_el = page.locator('[data-e2e="video-publish-time"], span:has-text("天前"), span:has-text("小时前"), span:has-text("分钟前"), span:has-text("秒前"), span:has-text("年"), span:has-text("月"), [class*="publish"]').first
        if time_el.is_visible(timeout=3000):
            video["publish_time"] = time_el.inner_text().strip()
    except Exception:
        pass

    # 互动数据：点赞、评论、分享
    # 抖音视频详情页的互动数据通常在视频右侧或底部
    action_items = page.locator('[data-e2e="video-action"] span, [class*="action"] span, [class*="interact"] span').all()
    for item in action_items:
        try:
            text = item.inner_text().strip()
        except Exception:
            continue
        num_match = re.search(r"(\d[\d,.]*[亿万]?)", text)
        if not num_match:
            continue
        count = _parse_count(num_match.group(1))
        if "点赞" in text or "赞" in text:
            video["likes"] = count
        elif "评论" in text:
            video["comments_count"] = count
        elif "分享" in text or "转发" in text:
            video["shares"] = count

    # 如果 action_items 方式失败，用全页面文本正则兜底
    full_text = page.inner_text("body") if hasattr(page, "inner_text") else ""
    if not video["likes"] and not video["comments_count"] and full_text:
        for pattern, key in [
            (r"(\d[\d,.]*[亿万]?)\s*赞", "likes"),
            (r"(\d[\d,.]*[亿万]?)\s*评论", "comments_count"),
            (r"(\d[\d,.]*[亿万]?)\s*分享", "shares"),
        ]:
            m = re.search(pattern, full_text)
            if m and not video.get(key):
                video[key] = _parse_count(m.group(1))

    # 播放量 — 通常不在详情页直接显示，需要在主页列表页抓
    # 尝试从页面任何数据显示位置提取
    play_match = re.search(r"(\d[\d,.]*[亿万]?)\s*(?:次播放|播放|观看)", full_text) if full_text else None
    if play_match:
        video["views"] = _parse_count(play_match.group(1))

    # 话题标签
    try:
        hashtag_els = page.locator('a[href*="/hashtag/"], span[class*="hashtag"], span:has-text("#")').all()
        for el in hashtag_els:
            try:
                tag_text = el.inner_text().strip()
                if tag_text and (tag_text.startswith("#") or "hashtag" in str(el.get_attribute("href") or "")):
                    video["hashtags"].append(tag_text.replace("#", "").strip())
            except Exception:
                continue
    except Exception:
        pass

    return video


def scrape_comments(page, max_count=20):
    """在视频详情页抓取 Top N 条评论。"""
    comments = []

    try:
        # 滚动到评论区
        try:
            page.evaluate("window.scrollBy(0, 600)")
            time.sleep(2)
        except Exception:
            pass

        # 尝试多种评论容器选择器
        comment_selectors = [
            '[data-e2e="comment-item"]',
            '[class*="comment-item"]',
            '[class*="CommentItem"]',
            'div:has(> [class*="comment"])',
            # 兜底：查找包含"评论"标题区域之后的列表项
        ]

        comment_els = []
        for sel in comment_selectors:
            els = page.locator(sel).all()
            if els:
                comment_els = els
                break

        if not comment_els:
            # 最终兜底：尝试查找页面中所有类似评论的结构
            # 评论区通常在视频下方
            try:
                comment_els = page.locator('[class*="comment"] > div, [class*="reply"] > div').all()
            except Exception:
                pass

        # 滚动评论区以加载更多
        collected = 0
        scroll_attempts = 0
        while collected < max_count and scroll_attempts < 10:
            if comment_els:
                for el in comment_els[collected : min(len(comment_els), max_count)]:
                    try:
                        text = el.inner_text().strip()
                        if not text or len(text) < 2:
                            continue
                        # 解析评论者昵称（通常在内容上方，用小号字体）
                        lines = text.split("\n")
                        user = lines[0] if lines else ""
                        content = lines[1] if len(lines) > 1 else text

                        # 提取评论点赞数
                        likes = 0
                        likes_match = re.search(r"(\d[\d,.]*[亿万]?)\s*(?:赞|likes?)", content)
                        if likes_match:
                            likes = _parse_count(likes_match.group(1))

                        # 清理内容中的点赞数
                        content = re.sub(r"\d[\d,.]*[亿万]?\s*(?:赞|likes?|回复)", "", content).strip()

                        if content and content != user:
                            comments.append({
                                "user": user[:30],
                                "text": content[:500],
                                "likes": likes,
                                "reply_count": 0,
                                "time": "",
                            })
                            collected += 1
                    except Exception:
                        continue

            if collected >= max_count:
                break

            # 滚动评论区加载更多
            page.evaluate("window.scrollBy(0, 400)")
            time.sleep(2)
            scroll_attempts += 1

            # 重新获取评论元素
            for sel in comment_selectors:
                els = page.locator(sel).all()
                if els:
                    comment_els = els
                    break

        return comments[:max_count]
    except Exception as e:
        print("  ⚠ 评论抓取失败: %s" % str(e)[:80])
        return []


def scrape_videos_batch(page, video_urls, json_path, max_comments=20):
    """批量抓取视频数据，每抓完一个立即写入 JSON 文件（断点续抓）。"""
    # 加载已有数据
    if os.path.isfile(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {"account": {}, "videos": []}

    existing_ids = {v["video_id"] for v in data.get("videos", [])}
    pending_urls = [u for u in video_urls if re.search(r"/video/(\d+)", u).group(1) not in existing_ids if re.search(r"/video/(\d+)", u)]

    print("待抓取: %d 个视频（已跳过 %d 个已有数据）" % (len(pending_urls), len(existing_ids)))

    for i, url in enumerate(pending_urls):
        print("\n[%d/%d] %s" % (i + 1, len(pending_urls), url))
        try:
            video = scrape_video(page, url)
        except Exception as e:
            print("  ⚠ 抓取失败: %s" % str(e)[:80])
            video = {
                "video_id": re.search(r"/video/(\d+)", url).group(1) if re.search(r"/video/(\d+)", url) else url,
                "url": url, "title": "", "cover_url": "", "duration_sec": 0,
                "publish_time": "", "views": 0, "likes": 0, "comments_count": 0,
                "shares": 0, "hashtags": [], "top_comments": [],
                "error": str(e)[:200],
            }

        # 如果有评论需求，追加抓取
        if max_comments > 0 and not video.get("error"):
            video["top_comments"] = scrape_comments(page, max_comments)
        else:
            video["top_comments"] = []

        data["videos"].append(video)

        # 立即刷盘
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print("  点赞: %s | 评论: %s | 分享: %s | 评论抓取: %d条" % (
            video["likes"], video["comments_count"], video["shares"], len(video.get("top_comments", []))
        ))

        # 间隔
        time.sleep(2 + (__import__("random").random() * 1.5))

    return data


def generate_report(account, videos, output_path):
    """生成 Markdown 分析报告。"""
    lines = []
    lines.append("# 抖音账号分析报告")
    lines.append("")
    lines.append("**生成时间**: %s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    lines.append("**主页链接**: %s" % account.get("url", ""))
    lines.append("")
    lines.append("---")
    lines.append("")

    # 1. 账号概览
    lines.append("## 一、账号概览")
    lines.append("")
    lines.append("| 指标 | 数值 |")
    lines.append("|------|------|")
    lines.append("| 昵称 | %s |" % account.get("nickname", "-"))
    lines.append("| 抖音号 | %s |" % account.get("douyin_id", "-"))
    lines.append("| 粉丝数 | %s |" % _format_count(account.get("follower_count", 0)))
    lines.append("| 获赞数 | %s |" % _format_count(account.get("total_likes", 0)))
    lines.append("| 关注数 | %s |" % _format_count(account.get("following_count", 0)))
    lines.append("| 作品数 | %d |" % account.get("video_count", 0))
    if account.get("verified_badge"):
        lines.append("| 认证 | %s |" % account["verified_badge"])
    if account.get("signature"):
        lines.append("| 简介 | %s |" % account["signature"])
    lines.append("")

    # 2. 基础健康度
    lines.append("## 二、基础健康度")
    lines.append("")

    follower_count = account.get("follower_count", 0)
    total_likes = account.get("total_likes", 0)
    video_count = account.get("video_count", 1)

    like_fan_ratio = (total_likes / follower_count) if follower_count > 0 else 0
    lines.append("- **赞粉比**: %.2f (%s获赞/%s粉丝)" % (like_fan_ratio, _format_count(total_likes), _format_count(follower_count)))
    lines.append("  - > 10：互动热度极高")
    lines.append("  - 5~10：良性互动")
    lines.append("  - < 5：互动偏低，需提升内容吸引力")

    avg_likes = sum(v.get("likes", 0) for v in videos) / max(len(videos), 1)
    lines.append("- **平均点赞**: %s / 条" % _format_count(int(avg_likes)))
    lines.append("- **平均评论**: %s / 条" % _format_count(int(sum(v.get("comments_count", 0) for v in videos) / max(len(videos), 1))))
    lines.append("")

    # 3. 视频表现排名
    lines.append("## 三、视频表现 Top 10")
    lines.append("")

    sorted_by_likes = sorted(videos, key=lambda v: v.get("likes", 0), reverse=True)[:10]
    lines.append("### 按点赞排名")
    lines.append("")
    lines.append("| # | 标题 | 点赞 | 评论 | 分享 | 发布时间 |")
    lines.append("|---|---|---|---|---|---|")
    for i, v in enumerate(sorted_by_likes[:10]):
        title = (v.get("title") or v.get("video_id") or "-")[:40]
        lines.append("| %d | %s | %s | %s | %s | %s |" % (
            i + 1, title,
            _format_count(v.get("likes", 0)),
            _format_count(v.get("comments_count", 0)),
            _format_count(v.get("shares", 0)),
            v.get("publish_time", "-"),
        ))
    lines.append("")

    sorted_by_comments = sorted(videos, key=lambda v: v.get("comments_count", 0), reverse=True)[:10]
    lines.append("### 按评论排名")
    lines.append("")
    lines.append("| # | 标题 | 评论 | 点赞 | 发布时间 |")
    lines.append("|---|---|---|---|---|")
    for i, v in enumerate(sorted_by_comments[:10]):
        title = (v.get("title") or v.get("video_id") or "-")[:40]
        lines.append("| %d | %s | %s | %s | %s |" % (
            i + 1, title,
            _format_count(v.get("comments_count", 0)),
            _format_count(v.get("likes", 0)),
            v.get("publish_time", "-"),
        ))
    lines.append("")

    # 4. 内容特征
    lines.append("## 四、内容特征分析")
    lines.append("")

    # 话题标签统计
    tag_counts = {}
    for v in videos:
        for tag in v.get("hashtags", []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    if tag_counts:
        top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        lines.append("### 热门话题标签")
        lines.append("")
        lines.append("| 标签 | 使用次数 |")
        lines.append("|---|---|")
        for tag, count in top_tags:
            lines.append("| #%s | %d |" % (tag, count))
        lines.append("")

    # 发布时间分布
    time_slots = {"凌晨(0-6)": 0, "上午(6-12)": 0, "下午(12-18)": 0, "晚上(18-24)": 0}
    for v in videos:
        pub = v.get("publish_time", "")
        hour_match = re.search(r"(\d{1,2}):\d{2}", pub)
        if hour_match:
            h = int(hour_match.group(1))
            if h < 6:
                time_slots["凌晨(0-6)"] += 1
            elif h < 12:
                time_slots["上午(6-12)"] += 1
            elif h < 18:
                time_slots["下午(12-18)"] += 1
            else:
                time_slots["晚上(18-24)"] += 1

    if sum(time_slots.values()) > 0:
        lines.append("### 发布时间偏好")
        lines.append("")
        for slot, count in time_slots.items():
            lines.append("- **%s**: %d 条" % (slot, count))
        lines.append("")

    # 5. 评论洞察
    lines.append("## 五、评论洞察")
    lines.append("")

    all_comments = []
    for v in videos:
        for c in v.get("top_comments", []):
            all_comments.append(c.get("text", ""))

    if all_comments:
        # 简单高频词统计（2字以上中文词）
        word_counts = {}
        for text in all_comments:
            # 简单分词：按非中文切割，取 2-4 字片段
            cleaned = re.sub(r"[^一-鿿]", " ", text)
            words = cleaned.split()
            for w in words:
                if 2 <= len(w) <= 4:
                    word_counts[w] = word_counts.get(w, 0) + 1
        top_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:20]
        if top_words:
            lines.append("### 评论高频词 Top 20")
            lines.append("")
            lines.append("| 词汇 | 出现次数 |")
            lines.append("|---|---|")
            for word, count in top_words:
                lines.append("| %s | %d |" % (word, count))
            lines.append("")

        # 情感简析（基于关键词）
        positive_keywords = ["好", "棒", "赞", "厉害", "牛", "喜欢", "不错", "支持", "加油", "爱", "优秀",
                             "👍", "🔥", "❤", "😍", "哈哈", "笑", "绝", "神", "顶", "强"]
        negative_keywords = ["差", "垃圾", "不好", "无聊", "失望", "举报", "恶心", "烂",
                             "👎", "踩", "呸", "吐", "无语", "尴尬"]
        pos_count = sum(1 for t in all_comments if any(kw in t for kw in positive_keywords))
        neg_count = sum(1 for t in all_comments if any(kw in t for kw in negative_keywords))
        total_comments = len(all_comments)
        lines.append("### 情感倾向简析")
        lines.append("")
        lines.append("- 正面评论: %d 条 (%.1f%%)" % (pos_count, pos_count / total_comments * 100 if total_comments else 0))
        lines.append("- 负面评论: %d 条 (%.1f%%)" % (neg_count, neg_count / total_comments * 100 if total_comments else 0))
        lines.append("- 中性/其他: %d 条 (%.1f%%)" % (
            total_comments - pos_count - neg_count,
            (total_comments - pos_count - neg_count) / total_comments * 100 if total_comments else 0,
        ))
        lines.append("")

    # 6. 趋势观察
    lines.append("## 六、趋势观察")
    lines.append("")
    if len(videos) >= 10:
        recent = videos[:10]
        early = videos[-10:]
        recent_avg_likes = sum(v.get("likes", 0) for v in recent) / max(len(recent), 1)
        early_avg_likes = sum(v.get("likes", 0) for v in early) / max(len(early), 1)
        recent_avg_comments = sum(v.get("comments_count", 0) for v in recent) / max(len(recent), 1)
        early_avg_comments = sum(v.get("comments_count", 0) for v in early) / max(len(early), 1)

        lines.append("| 对比维度 | 近期10条 | 早期10条 | 变化 |")
        lines.append("|---|---|---|---|")
        lines.append("| 平均点赞 | %s | %s | %s |" % (
            _format_count(int(recent_avg_likes)), _format_count(int(early_avg_likes)),
            _trend_emoji(recent_avg_likes, early_avg_likes),
        ))
        lines.append("| 平均评论 | %s | %s | %s |" % (
            _format_count(int(recent_avg_comments)), _format_count(int(early_avg_comments)),
            _trend_emoji(recent_avg_comments, early_avg_comments),
        ))
        lines.append("")
        lines.append("> %s近期点赞表现%s早期。%s评论互动%s早期。" % (
            "📈" if recent_avg_likes > early_avg_likes else "📉",
            "优于" if recent_avg_likes > early_avg_likes else "低于",
            "📈" if recent_avg_comments > early_avg_comments else "📉",
            "优于" if recent_avg_comments > early_avg_comments else "低于",
        ))
        lines.append("")

    lines.append("---")
    lines.append("*报告由 scrape_douyin.py 自动生成*")

    report = "\n".join(lines)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)
    print("分析报告已生成:", output_path)
    return output_path


def _format_count(n):
    """格式化数字为可读形式。"""
    if n >= 100000000:
        return "%.1f亿" % (n / 100000000)
    if n >= 10000:
        return "%.1f万" % (n / 10000)
    return str(n)


def _trend_emoji(recent, early):
    if recent >= early * 1.2:
        return "📈 上升"
    elif recent <= early * 0.8:
        return "📉 下降"
    else:
        return "➡ 持平"


def main():
    args = parse_args()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = resolve_data_dir(script_dir, args.data_dir)
    session_path = args.session or os.path.join(data_dir, "douyin_session.json")

    p, browser, context, page = launch_browser(session_path)

    try:
        login_if_needed(page, args.timeout, session_path)
        save_session(context, session_path)

        # 提取用户 ID 用于稳定文件名（断点续抓）
        user_id_match = re.search(r"user/([A-Za-z0-9_-]+)", args.url)
        user_slug = user_id_match.group(1)[:20] if user_id_match else datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        json_path = os.path.join(data_dir, "%s-douyin-data.json" % user_slug)
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        report_path = os.path.join(data_dir, "%s-douyin-report.md" % timestamp)

        # 1. 抓取账号数据
        account = scrape_account(page, args.url)

        # 2. 收集视频链接
        video_urls = collect_video_links(page, account.get("video_count", 0))
        print("共收集 %d 个视频" % len(video_urls))

        # 写入初始 JSON (含账号数据，但保留已有视频列表以支持断点续抓)
        existing_videos = []
        if os.path.isfile(json_path):
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    prev = json.load(f)
                    existing_videos = prev.get("videos", [])
            except (json.JSONDecodeError, ValueError):
                pass
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({"account": account, "videos": existing_videos}, f, ensure_ascii=False, indent=2)

        # 3. 批量抓取视频数据 + 评论
        data = scrape_videos_batch(page, video_urls, json_path, max_comments=args.max_comments)

        # 4. 生成分析报告
        generate_report(data["account"], data["videos"], report_path)

        print("")
        print("=" * 50)
        print("抓取完成！")
        print("原始数据: %s" % json_path)
        print("分析报告: %s" % report_path)
        print("=" * 50)

    except KeyboardInterrupt:
        print("\n已中断。下次运行将自动从已有数据继续。")
    except TimeoutError as e:
        print("错误:", e, file=sys.stderr)
        return 1
    except Exception as e:
        print("错误:", e, file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1
    finally:
        context.close()
        browser.close()
        p.stop()

    return 0


if __name__ == "__main__":
    sys.exit(main())
