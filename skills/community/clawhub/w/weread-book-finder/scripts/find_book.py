#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import sys
import time
import urllib.parse
from pathlib import Path

import re
from playwright.sync_api import sync_playwright

WEREAD_URL = "https://weread.qq.com/"
ZLIB_URL = "https://z-lib.by/"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"


def ensure_parent(path: str):
    os.makedirs(path, exist_ok=True)


def safe_filename(name: str) -> str:
    name = (name or "").strip()
    name = re.sub(r'[\\/:*?"<>|]+', "_", name)
    name = re.sub(r"\s+", " ", name)
    return name[:180].strip(" .") or "book"


def cleanup_profile_locks(profile_dir: str):
    p = Path(profile_dir)
    for name in ["SingletonLock", "SingletonCookie", "SingletonSocket"]:
        f = p / name
        try:
            if f.exists() or f.is_symlink():
                f.unlink()
        except Exception:
            pass


def launch_context(p, profile_dir: str, headed: bool):
    ensure_parent(profile_dir)
    try:
        return p.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=not headed,
            user_agent=UA,
            locale="zh-CN",
            accept_downloads=True,
        )
    except Exception as e:
        # 常见是 profile 残留锁文件。清一下再重试一次。
        if "ProcessSingleton" in str(e) or "Singleton" in str(e):
            cleanup_profile_locks(profile_dir)
            return p.chromium.launch_persistent_context(
                user_data_dir=profile_dir,
                headless=not headed,
                user_agent=UA,
                locale="zh-CN",
                accept_downloads=True,
            )
        raise


def norm_title(s: str) -> str:
    s = s or ""
    s = re.sub(r"\s+", "", s)
    s = re.sub(r"[：:·,，.。!！?？'\"“”‘’()（）\-—_]", "", s)
    return s.lower()


def title_score(query: str, candidate: str) -> int:
    q = norm_title(query)
    c = norm_title(candidate)
    if not q or not c:
        return -1
    if q == c:
        return 100
    if q in c:
        return 80
    if c in q:
        return 70
    overlap = sum(1 for ch in q if ch in c)
    return overlap


def author_score(query_author: str, candidate_author: str) -> int:
    qa = norm_title(query_author)
    ca = norm_title(candidate_author)
    if not qa or not ca:
        return 0
    if qa == ca:
        return 30
    if qa in ca or ca in qa:
        return 20
    overlap = sum(1 for ch in qa if ch in ca)
    return min(overlap, 10)


def parse_query(book_name: str):
    raw = (book_name or "").strip()
    title = raw
    author = ""
    separators = [" / ", "｜", "|", " by ", " - ", " —— ", " — "]
    for sep in separators:
        if sep in raw:
            left, right = raw.split(sep, 1)
            if left.strip() and right.strip():
                title, author = left.strip(), right.strip()
                break
    return title, author


def weread_search_and_open(page, book_name: str):
    query_title, query_author = parse_query(book_name)

    page.goto(WEREAD_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(2500)

    body = page.locator("body").inner_text(timeout=3000)
    if "登录" in body and "我的书架" not in body:
        return {"status": "needs_login", "platform": "weread"}

    search = page.locator("input[placeholder='搜索']")
    if search.count() == 0:
        return {"status": "failed", "platform": "weread", "reason": "search_input_not_found"}

    search.fill(query_title)
    page.keyboard.press("Enter")
    page.wait_for_timeout(3000)

    items = page.locator("a.wr_index_page_mini_bookInfo")
    count = items.count()
    if count == 0:
        return {"status": "not_found", "platform": "weread"}

    candidates = []
    for i in range(min(count, 8)):
        txt = items.nth(i).inner_text(timeout=1000)
        lines = [x.strip() for x in (txt or "").splitlines() if x.strip()]
        title = lines[0] if lines else ""
        author = lines[2] if len(lines) >= 3 else (lines[1] if len(lines) >= 2 else "")
        t_score = title_score(query_title, title)
        a_score = author_score(query_author, author)
        exact = norm_title(query_title) == norm_title(title)
        rank = t_score + a_score + (20 if exact else 0)
        candidates.append({
            "idx": i,
            "title": title,
            "author": author,
            "href": items.nth(i).get_attribute("href"),
            "titleScore": t_score,
            "authorScore": a_score,
            "exactTitle": exact,
            "rank": rank,
        })

    candidates.sort(key=lambda x: (x["rank"], x["exactTitle"], x["titleScore"]), reverse=True)
    best = candidates[0]

    # 标题太歧义时，不要无脑误点；保留候选供调试/人工确认。
    qn = norm_title(query_title)
    bn = norm_title(best["title"])
    ambiguous_short = len(qn) <= 4 and qn != bn and qn in bn and not best["exactTitle"] and best["authorScore"] == 0
    if best["titleScore"] < 2 or ambiguous_short:
        return {
            "status": "not_found",
            "platform": "weread",
            "reason": "no_confident_match",
            "candidates": candidates[:5],
        }

    target = items.nth(best["idx"])
    target.click()
    page.wait_for_timeout(4000)
    return {
        "status": "opened",
        "platform": "weread",
        "url": page.url,
        "href": best.get("href"),
        "match": best["title"],
        "matchAuthor": best["author"],
        "candidates": candidates[:5],
    }


def weread_flow(page, book_name):
    print(f"尝试在微信读书搜索: {book_name}")
    open_res = weread_search_and_open(page, book_name)
    if open_res["status"] != "opened":
        return open_res

    # 微信读书 reader 顶栏会显示加入书架状态。
    added_icon = page.locator(".readerTopBar_addToShelf_icon.added")
    if added_icon.count() > 0:
        return {
            "status": "already_exists",
            "platform": "weread",
            "url": page.url,
            "match": open_res.get("match"),
            "matchAuthor": open_res.get("matchAuthor"),
            "candidates": open_res.get("candidates", []),
        }

    add_btn = page.locator(".readerTopBar_addToShelf")
    if add_btn.count() > 0:
        add_btn.first.click()
        page.wait_for_timeout(2000)
        if page.locator(".readerTopBar_addToShelf_icon.added").count() > 0:
            return {
                "status": "success",
                "platform": "weread",
                "url": page.url,
                "match": open_res.get("match"),
                "matchAuthor": open_res.get("matchAuthor"),
                "candidates": open_res.get("candidates", []),
            }

    # 页面底部有时也会出现“加入书架/去 App 阅读”按钮，作为补充检测。
    if page.locator(".rbb_addShelf").count() > 0:
        txt = page.locator(".rbb_addShelf").first.inner_text(timeout=1000)
        if "加入书架" in txt:
            page.locator(".rbb_addShelf").first.click()
            page.wait_for_timeout(2000)
            if page.locator(".readerTopBar_addToShelf_icon.added").count() > 0:
                return {
                    "status": "success",
                    "platform": "weread",
                    "url": page.url,
                    "match": open_res.get("match"),
                    "matchAuthor": open_res.get("matchAuthor"),
                    "candidates": open_res.get("candidates", []),
                }

    return {
        "status": "failed",
        "platform": "weread",
        "url": page.url,
        "match": open_res.get("match"),
        "reason": "opened_but_add_failed",
    }


def zlib_flow(page, book_name, download_dir):
    print(f"微信读书未命中，尝试在 Z-Library 搜索: {book_name}")
    query_title, query_author = parse_query(book_name)
    ensure_parent(download_dir)
    search_url = f"{ZLIB_URL}s/{urllib.parse.quote(query_title)}"
    page.goto(search_url, wait_until="domcontentloaded")
    page.wait_for_timeout(3000)

    body = page.locator("body").inner_text(timeout=3000)
    if "Log In" in body and "My Library" not in body:
        # Z-Library 搜索页匿名也能看结果，所以这里只是记录，不直接失败。
        pass

    cards = page.locator(".book-item z-bookcard")
    if cards.count() == 0:
        return {"status": "not_found", "platform": "zlib"}

    items = page.locator(".book-item")
    candidates = []
    for i in range(cards.count()):
        card = cards.nth(i)
        lines = [x.strip() for x in items.nth(i).inner_text(timeout=1000).splitlines() if x.strip()]
        title = lines[0] if lines else ""
        author = lines[1] if len(lines) >= 2 else ""
        ext = (card.get_attribute("extension") or "").lower()
        non_pdf = ext != "pdf"
        t_score = title_score(query_title, title)
        a_score = author_score(query_author, author)
        exact = norm_title(query_title) == norm_title(title)
        rank = t_score + a_score + (20 if non_pdf else 0) + (20 if exact else 0)
        candidates.append({
            "idx": i,
            "title": title,
            "author": author,
            "extension": ext,
            "nonPdf": non_pdf,
            "titleScore": t_score,
            "authorScore": a_score,
            "exactTitle": exact,
            "rank": rank,
        })

    candidates.sort(key=lambda x: (x["rank"], x["nonPdf"], x["exactTitle"], x["titleScore"]), reverse=True)
    best = candidates[0]
    qn = norm_title(query_title)
    bn = norm_title(best["title"])
    ambiguous_short = len(qn) <= 4 and qn != bn and qn in bn and not best["exactTitle"] and best["authorScore"] == 0
    if best["titleScore"] < 2 or ambiguous_short:
        return {
            "status": "not_found",
            "platform": "zlib",
            "reason": "no_confident_match",
            "candidates": candidates[:5],
        }

    card = cards.nth(best["idx"])
    title = best["title"]
    href = card.get_attribute("href")
    download_href = card.get_attribute("download")
    extension = (card.get_attribute("extension") or "").lower()

    if not href:
        return {"status": "failed", "platform": "zlib", "reason": "book_href_not_found"}

    page.goto(urllib.parse.urljoin(ZLIB_URL, href), wait_until="domcontentloaded")
    page.wait_for_timeout(2500)

    dl_btn = page.locator("a.addDownloadedBook").first
    if dl_btn.count() == 0 and download_href:
        page.goto(urllib.parse.urljoin(ZLIB_URL, download_href), wait_until="domcontentloaded")
        page.wait_for_timeout(2500)
        dl_btn = page.locator("a.addDownloadedBook").first

    if dl_btn.count() > 0:
        with page.expect_download(timeout=15000) as download_info:
            dl_btn.click()
        download = download_info.value
        ext = extension or Path(download.suggested_filename).suffix.lstrip(".")
        filename = f"{safe_filename(title)}.{ext}" if ext else safe_filename(title)
        path = os.path.join(download_dir, filename)
        download.save_as(path)
        return {
            "status": "success",
            "platform": "zlib",
            "path": path,
            "filename": filename,
            "match": title,
            "matchAuthor": best.get("author"),
            "extension": extension,
            "candidates": candidates[:5],
        }

    return {
        "status": "failed",
        "platform": "zlib",
        "match": title,
        "matchAuthor": best.get("author"),
        "extension": extension,
        "reason": "download_button_not_found",
        "candidates": candidates[:5],
    }


def run(book_name, profile_dir, download_dir, headed=False, login_mode=None):
    with sync_playwright() as p:
        context = launch_context(p, profile_dir, headed)
        page = context.pages[0] if context.pages else context.new_page()

        if login_mode == "weread":
            page.goto(WEREAD_URL)
            print("请手动完成微信读书登录，完成后按回车...")
            input()
            context.close()
            return
        elif login_mode == "zlib":
            page.goto(ZLIB_URL)
            print("请手动完成 Z-Library 登录，完成后按回车...")
            input()
            context.close()
            return

        wr_res = weread_flow(page, book_name)
        if wr_res["status"] in ["success", "already_exists"]:
            print(json.dumps(wr_res, ensure_ascii=False, indent=2))
            context.close()
            return

        z_res = zlib_flow(page, book_name, download_dir)
        print(json.dumps({"weread": wr_res, "zlib": z_res}, ensure_ascii=False, indent=2))
        context.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("book_name", nargs="?")
    parser.add_argument("--profile", default=os.path.expanduser("~/.openclaw/browser-profiles/book-finder"))
    parser.add_argument("--downloads", default=os.path.expanduser("~/Downloads/OpenClaw-Books"))
    parser.add_argument("--headed", action="store_true")
    parser.add_argument("--login", choices=["weread", "zlib"])
    args = parser.parse_args()

    if not args.book_name and not args.login:
        parser.error("需要提供书名，或使用 --login")

    run(args.book_name, args.profile, args.downloads, args.headed, args.login)
