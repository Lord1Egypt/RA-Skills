#!/usr/bin/env python3
"""微信读书 Web API 封装 — OpenClaw Skill 专用

Cookie 存储路径: ~/.weread/cookie (纯文本单行)
所有接口返回 JSON，错误时 exit(1) + stderr 输出。
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
import urllib.parse

COOKIE_PATH = os.path.expanduser("~/.weread/cookie")

BASE = "https://weread.qq.com"
HEADERS_COMMON = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/135.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

# ── helpers ──────────────────────────────────────────────────────────

def _die(msg: str):
    print(msg, file=sys.stderr)
    sys.exit(1)

def _load_cookie() -> str:
    if not os.path.exists(COOKIE_PATH):
        _die(f"Cookie 文件不存在: {COOKIE_PATH}\n请先运行 weread_login.py 获取 Cookie。")
    with open(COOKIE_PATH) as f:
        cookie = f.read().strip()
    if not cookie:
        _die("Cookie 文件为空，请重新登录。")
    return cookie

def _request(url: str, method: str = "GET", data: bytes | None = None,
             extra_headers: dict | None = None, cookie: str | None = None) -> dict:
    """统一请求，自动附 Cookie + 时间戳防缓存"""
    if cookie is None:
        cookie = _load_cookie()

    # GET 加时间戳
    if method == "GET":
        sep = "&" if "?" in url else "?"
        url += f"{sep}_={int(time.time() * 1000)}"

    headers = {**HEADERS_COMMON, "Cookie": cookie}
    if extra_headers:
        headers.update(extra_headers)
    if data is not None:
        headers["Content-Type"] = "application/json;charset=UTF-8"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read()
    except urllib.error.HTTPError as e:
        body = e.read()
        try:
            err = json.loads(body)
        except Exception:
            _die(f"HTTP {e.code}: {body[:500]}")
        if err.get("errcode") in (-2012, -2010):
            _die("Cookie 已过期，请重新登录微信读书。")
        _die(f"HTTP {e.code}: {json.dumps(err, ensure_ascii=False)}")
    except Exception as e:
        _die(f"请求失败: {e}")

    result = json.loads(body)
    ec = result.get("errcode") or result.get("errCode")
    if ec and ec != 0:
        if ec in (-2012, -2010):
            _die("Cookie 已过期，请重新登录微信读书。")
        _die(f"API 错误 ({ec}): {result.get('errmsg') or result.get('errMsg') or ''}")
    return result


# ── public API ───────────────────────────────────────────────────────

def get_bookshelf() -> dict:
    """获取完整书架（含进度、书单分组等）"""
    return _request(f"{BASE}/web/shelf/sync")


def get_notebooks() -> list:
    """获取有笔记的书籍列表"""
    data = _request(f"{BASE}/api/user/notebook")
    return data.get("books", [])


def get_book_info(book_id: str) -> dict:
    """获取书籍详情"""
    return _request(f"{BASE}/api/book/info?bookId={urllib.parse.quote(book_id)}")


def get_reading_progress(book_id: str) -> dict:
    """获取阅读进度（当前版本接口）"""
    return _request(f"{BASE}/web/book/getProgress?bookId={urllib.parse.quote(book_id)}")


def get_read_detail(book_id: str) -> dict:
    """获取详细阅读信息（含阅读时长明细、完成日期等）"""
    return _request(
        f"{BASE}/web/book/readinfo?bookId={urllib.parse.quote(book_id)}"
        "&readingDetail=1&readingBookIndex=1&finishedDate=1"
    )


def get_bookmarks(book_id: str) -> list:
    """获取书籍的划线记录"""
    data = _request(f"{BASE}/web/book/bookmarklist?bookId={urllib.parse.quote(book_id)}")
    return data.get("updated", [])


def get_reviews(book_id: str, mine_only: bool = True) -> list:
    """获取书籍的笔记/想法"""
    lt = 4 if not mine_only else 11
    mine = 1 if mine_only else 0
    data = _request(
        f"{BASE}/web/review/list?bookId={urllib.parse.quote(book_id)}"
        f"&listType={lt}&mine={mine}&synckey=0&count=0&listMode=2&maxIdx=0"
    )
    reviews = data.get("reviews", [])
    return [r.get("review", r) for r in reviews]


def get_best_reviews(book_id: str, count: int = 10) -> dict:
    """获取热门书评"""
    return _request(
        f"{BASE}/web/review/list/best?bookId={urllib.parse.quote(book_id)}"
        f"&count={count}&maxIdx=0&synckey=0"
    )


def get_chapter_infos(book_id: str) -> dict:
    """获取章节信息（POST）"""
    payload = json.dumps({"bookIds": [book_id]}).encode()
    headers = {
        "Origin": "https://weread.qq.com",
        "Referer": f"https://weread.qq.com/web/reader/{book_id}",
    }
    data = _request(f"{BASE}/web/book/chapterInfos", method="POST",
                    data=payload, extra_headers=headers)
    # 多种返回格式兼容
    if "data" in data and isinstance(data["data"], list) and data["data"]:
        return data["data"][0].get("updated", [])
    if "updated" in data:
        return data["updated"]
    return data


def verify_cookie(cookie: str | None = None) -> bool:
    """验证 Cookie 是否有效"""
    try:
        result = _request(f"{BASE}/api/user/notebook", cookie=cookie)
        return "books" in result
    except SystemExit:
        return False


# ── CLI 入口 ─────────────────────────────────────────────────────────

def _fmt(seconds: int) -> str:
    h, m = divmod(seconds // 60, 60)
    if h:
        return f"{h}小时{m}分钟" if m else f"{h}小时"
    return f"{m}分钟"


def _print_json(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def main():
    if len(sys.argv) < 2:
        print("用法: weread_api.py <command> [args...]")
        print("命令:")
        print("  shelf                  - 获取书架")
        print("  notebooks              - 获取有笔记的书籍")
        print("  info <bookId>          - 获取书籍详情")
        print("  progress <bookId>      - 获取阅读进度")
        print("  detail <bookId>        - 获取详细阅读信息")
        print("  bookmarks <bookId>     - 获取划线记录")
        print("  reviews <bookId>       - 获取我的笔记/想法")
        print("  best-reviews <bookId>  - 获取热门书评")
        print("  chapters <bookId>      - 获取章节信息")
        print("  search <keyword>       - 搜索书架中的书籍")
        print("  verify                 - 验证 Cookie 是否有效")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "shelf":
        data = get_bookshelf()
        books = data.get("books", [])
        progress_list = data.get("bookProgress", [])
        progress_map = {p["bookId"]: p for p in progress_list}
        summary = []
        for b in books:
            bid = b.get("bookId", "")
            prog = progress_map.get(bid, {})
            summary.append({
                "bookId": bid,
                "title": b.get("title", ""),
                "author": b.get("author", ""),
                "progress": prog.get("progress", 0),
                "readingTime": _fmt(prog.get("readingTime", 0)),
                "finishReading": b.get("finishReading", 0) == 1,
            })
        _print_json({"total": len(summary), "books": summary})

    elif cmd == "notebooks":
        _print_json(get_notebooks())

    elif cmd == "info":
        if len(sys.argv) < 3:
            _die("用法: weread_api.py info <bookId>")
        _print_json(get_book_info(sys.argv[2]))

    elif cmd == "progress":
        if len(sys.argv) < 3:
            _die("用法: weread_api.py progress <bookId>")
        _print_json(get_reading_progress(sys.argv[2]))

    elif cmd == "detail":
        if len(sys.argv) < 3:
            _die("用法: weread_api.py detail <bookId>")
        _print_json(get_read_detail(sys.argv[2]))

    elif cmd == "bookmarks":
        if len(sys.argv) < 3:
            _die("用法: weread_api.py bookmarks <bookId>")
        marks = get_bookmarks(sys.argv[2])
        _print_json({"total": len(marks), "bookmarks": marks})

    elif cmd == "reviews":
        if len(sys.argv) < 3:
            _die("用法: weread_api.py reviews <bookId>")
        reviews = get_reviews(sys.argv[2])
        _print_json({"total": len(reviews), "reviews": reviews})

    elif cmd == "best-reviews":
        if len(sys.argv) < 3:
            _die("用法: weread_api.py best-reviews <bookId>")
        count = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        _print_json(get_best_reviews(sys.argv[2], count))

    elif cmd == "chapters":
        if len(sys.argv) < 3:
            _die("用法: weread_api.py chapters <bookId>")
        _print_json(get_chapter_infos(sys.argv[2]))

    elif cmd == "search":
        if len(sys.argv) < 3:
            _die("用法: weread_api.py search <keyword>")
        keyword = sys.argv[2].lower()
        data = get_bookshelf()
        books = data.get("books", [])
        progress_list = data.get("bookProgress", [])
        progress_map = {p["bookId"]: p for p in progress_list}
        matched = []
        for b in books:
            title = (b.get("title") or "").lower()
            author = (b.get("author") or "").lower()
            if keyword in title or keyword in author:
                bid = b.get("bookId", "")
                prog = progress_map.get(bid, {})
                matched.append({
                    "bookId": bid,
                    "title": b.get("title", ""),
                    "author": b.get("author", ""),
                    "progress": prog.get("progress", 0),
                    "readingTime": _fmt(prog.get("readingTime", 0)),
                    "finishReading": b.get("finishReading", 0) == 1,
                })
        _print_json({"total": len(matched), "keyword": sys.argv[2], "books": matched})

    elif cmd == "verify":
        ok = verify_cookie()
        print("✅ Cookie 有效" if ok else "❌ Cookie 已过期或无效")
        sys.exit(0 if ok else 1)

    else:
        _die(f"未知命令: {cmd}")


if __name__ == "__main__":
    main()
