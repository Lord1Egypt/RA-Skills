#!/usr/bin/env python3
"""PTT web BBS (https://www.ptt.cc/bbs) scraper.

Workflow: board article list -> single article, extracting push (推),
boo (噓), neutral (→) counts and the total score (推 - 噓).

Uses only `requests` + `BeautifulSoup` (beautifulsoup4).
Sends the `over18=1` cookie so age-gated boards (e.g. Gossiping) work.

Commands (everything ptt.cc offers without login)
--------------------------------------------------
  boards                                      Hot board list (/bbs/index.html).
  cls     [id]                                Board category tree (/cls/<id>);
                                              id defaults to 1 (the root).
  list    <board> [--pages N]                 List articles on a board index.
  search  <board> <query> [--pages N]         Board search. Query supports PTT
                                              operators: plain keywords,
                                              author:<userid>, thread:<title>,
                                              recommend:<n> (score >= n,
                                              -100..100). Operators combine
                                              with spaces.
  article <url-or-path>                       Fetch one article with exact
                                              push/boo counts.
  stats   <board> [--pages N] [--limit M]     List articles, then fetch each
                                              one and report per-article and
                                              board-wide push/boo totals.
  man     <board> [path]                      Essence area (精華區) listing:
                                              /man/<board>/index.html or a
                                              subdirectory path within it.

Examples
--------
  python ptt_scraper.py boards
  python ptt_scraper.py list Gossiping --pages 2
  python ptt_scraper.py search Gossiping "recommend:50 颱風"
  python ptt_scraper.py article https://www.ptt.cc/bbs/Gossiping/M.1700000000.A.ABC.html
  python ptt_scraper.py stats NBA --pages 1 --limit 10
  python ptt_scraper.py man Gossiping

Output is JSON on stdout (UTF-8, ensure_ascii=False).
"""

import argparse
import json
import re
import sys
import time

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.ptt.cc"
# Polite delay between consecutive HTTP requests (seconds).
REQUEST_DELAY = 0.8
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    )
}


def make_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(HEADERS)
    # PTT age-gate: setting this cookie skips the "over 18?" interstitial.
    session.cookies.set("over18", "1", domain=".ptt.cc")
    return session


def fetch_soup(session: requests.Session, url: str, params: dict | None = None) -> BeautifulSoup:
    resp = session.get(url, params=params, timeout=15)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


def parse_nrec(text: str) -> dict:
    """Interpret the push marker shown on board index pages.

    PTT buckets the score on list pages: '爆' means 100+, 'X1'..'XX' mean
    negative buckets (-10 per step, 'XX' is -100 or worse), digits are the
    exact positive score up to 99, empty means 0. This is a *score bucket*,
    not exact push/boo counts — fetch the article for exact numbers.
    """
    text = (text or "").strip()
    if not text:
        return {"marker": "", "score_hint": 0}
    if text == "爆":
        return {"marker": text, "score_hint": 100}
    if text == "XX":
        return {"marker": text, "score_hint": -100}
    if text.startswith("X"):
        try:
            return {"marker": text, "score_hint": -int(text[1:]) * 10}
        except ValueError:
            return {"marker": text, "score_hint": None}
    try:
        return {"marker": text, "score_hint": int(text)}
    except ValueError:
        return {"marker": text, "score_hint": None}


def parse_board_page(soup: BeautifulSoup) -> tuple[list, str | None]:
    """Parse one board index page.

    Returns (articles, prev_page_url). Articles pinned to the bottom of the
    board (置底文) appear after the 'r-list-sep' divider and are skipped.
    """
    articles = []
    main = soup.find("div", class_="r-list-container")
    if main is None:
        main = soup
    for child in main.find_all("div", recursive=False):
        classes = child.get("class") or []
        if "r-list-sep" in classes:
            break  # everything below the separator is a pinned post
        if "r-ent" not in classes:
            continue
        title_div = child.find("div", class_="title")
        link = title_div.find("a") if title_div else None
        if link is None:
            # Deleted article: title exists but no link.
            continue
        nrec = child.find("div", class_="nrec")
        author = child.find("div", class_="author")
        date = child.find("div", class_="date")
        articles.append(
            {
                "title": link.get_text(strip=True),
                "url": BASE_URL + link["href"],
                "author": author.get_text(strip=True) if author else "",
                "date": date.get_text(strip=True) if date else "",
                "nrec": parse_nrec(nrec.get_text() if nrec else ""),
            }
        )

    prev_url = None
    for a in soup.select("div.btn-group-paging a"):
        if "上頁" in a.get_text():
            href = a.get("href")
            if href:
                prev_url = BASE_URL + href
            break
    return articles, prev_url


def list_board(session: requests.Session, board: str, pages: int = 1) -> dict:
    url = f"{BASE_URL}/bbs/{board}/index.html"
    all_articles = []
    for page_no in range(pages):
        soup = fetch_soup(session, url)
        articles, prev_url = parse_board_page(soup)
        all_articles.extend(articles)
        if prev_url is None or page_no == pages - 1:
            break
        url = prev_url
        time.sleep(REQUEST_DELAY)
    return {"board": board, "article_count": len(all_articles), "articles": all_articles}


def parse_board_entries(soup: BeautifulSoup) -> list:
    """Parse board entries (a.board) on /bbs/index.html and /cls/<id> pages."""
    entries = []
    for a in soup.select("a.board"):
        href = a.get("href", "")
        name = a.find("div", class_="board-name")
        nuser = a.find("div", class_="board-nuser")
        cls = a.find("div", class_="board-class")
        title = a.find("div", class_="board-title")
        entries.append(
            {
                "name": name.get_text(strip=True) if name else "",
                "type": "category" if href.startswith("/cls/") else "board",
                "url": BASE_URL + href,
                "nuser": nuser.get_text(strip=True) if nuser else "",
                "class": cls.get_text(strip=True) if cls else "",
                "title": title.get_text(strip=True) if title else "",
            }
        )
    return entries


def hot_boards(session: requests.Session) -> dict:
    soup = fetch_soup(session, f"{BASE_URL}/bbs/index.html")
    boards = parse_board_entries(soup)
    return {"source": "hot-boards", "count": len(boards), "boards": boards}


def board_categories(session: requests.Session, cls_id: int) -> dict:
    soup = fetch_soup(session, f"{BASE_URL}/cls/{cls_id}")
    entries = parse_board_entries(soup)
    return {"source": f"cls/{cls_id}", "count": len(entries), "entries": entries}


def search_board(session: requests.Session, board: str, query: str, pages: int = 1) -> dict:
    """Board search. PTT search operators (combine with spaces in `query`):

    - plain words: title keyword match
    - author:<userid>: articles by that author
    - thread:<title>: all articles in the same reply thread
    - recommend:<n>: score (推-噓 bucket) >= n, n in -100..100
    """
    all_articles = []
    for page in range(1, pages + 1):
        soup = fetch_soup(
            session,
            f"{BASE_URL}/bbs/{board}/search",
            params={"q": query, "page": page},
        )
        articles, _ = parse_board_page(soup)
        if not articles:
            break  # past the last page of results
        all_articles.extend(articles)
        if page < pages:
            time.sleep(REQUEST_DELAY)
    return {
        "board": board,
        "query": query,
        "article_count": len(all_articles),
        "articles": all_articles,
    }


def man_listing(session: requests.Session, board: str, path: str | None) -> dict:
    """List the essence area (精華區). Entries link either to subdirectories
    (crawl deeper by passing their path) or to archived articles."""
    if path:
        path = path if path.startswith("/man/") else f"/man/{board}/{path.lstrip('/')}"
        url = BASE_URL + path
    else:
        url = f"{BASE_URL}/man/{board}/index.html"
    soup = fetch_soup(session, url)
    entries = []
    # Essence-area rows use "m-ent" (not the board index's "r-ent").
    for ent in soup.find_all("div", class_="m-ent"):
        title_div = ent.find("div", class_="title")
        link = title_div.find("a") if title_div else None
        if link is None:
            continue
        href = link["href"]
        entries.append(
            {
                "title": link.get_text(strip=True),
                "url": BASE_URL + href,
                # Directory entries end in index.html; leaves are articles.
                "type": "directory" if href.endswith("index.html") else "article",
            }
        )
    return {"board": board, "url": url, "count": len(entries), "entries": entries}


def parse_article(soup: BeautifulSoup, url: str) -> dict:
    main = soup.find("div", id="main-content")
    if main is None:
        raise ValueError(f"no main-content found at {url} (deleted article?)")

    meta = {}
    # 作者/標題/時間 use class "article-metaline"; 看板 uses
    # "article-metaline-right" — match both.
    for line in main.find_all("div", class_=re.compile(r"^article-metaline")):
        tag = line.find("span", class_="article-meta-tag")
        value = line.find("span", class_="article-meta-value")
        if tag and value:
            meta[tag.get_text(strip=True)] = value.get_text(strip=True)

    push = boo = neutral = 0
    pushes = []
    for div in main.find_all("div", class_="push"):
        tag_span = div.find("span", class_="push-tag")
        if tag_span is None:
            continue
        tag = tag_span.get_text(strip=True)
        if tag == "推":
            push += 1
        elif tag == "噓":
            boo += 1
        else:
            neutral += 1
        userid = div.find("span", class_="push-userid")
        content = div.find("span", class_="push-content")
        ipdatetime = div.find("span", class_="push-ipdatetime")
        pushes.append(
            {
                "tag": tag,
                "userid": userid.get_text(strip=True) if userid else "",
                "content": content.get_text(strip=True).lstrip(": ") if content else "",
                "ipdatetime": ipdatetime.get_text(strip=True) if ipdatetime else "",
            }
        )

    return {
        "url": url,
        "board": meta.get("看板", ""),
        "author": meta.get("作者", ""),
        "title": meta.get("標題", ""),
        "time": meta.get("時間", ""),
        "push_count": push,
        "boo_count": boo,
        "neutral_count": neutral,
        "total_comments": push + boo + neutral,
        "score": push - boo,
        "pushes": pushes,
    }


def get_article(session: requests.Session, url_or_path: str) -> dict:
    url = url_or_path if url_or_path.startswith("http") else BASE_URL + url_or_path
    soup = fetch_soup(session, url)
    return parse_article(soup, url)


def board_stats(session: requests.Session, board: str, pages: int, limit: int | None) -> dict:
    listing = list_board(session, board, pages)
    articles = listing["articles"]
    if limit is not None:
        articles = articles[:limit]

    results = []
    totals = {"push": 0, "boo": 0, "neutral": 0}
    for entry in articles:
        time.sleep(REQUEST_DELAY)
        try:
            art = get_article(session, entry["url"])
        except (requests.RequestException, ValueError) as exc:
            print(f"warning: skipping {entry['url']}: {exc}", file=sys.stderr)
            continue
        art.pop("pushes")  # keep stats output compact
        totals["push"] += art["push_count"]
        totals["boo"] += art["boo_count"]
        totals["neutral"] += art["neutral_count"]
        results.append(art)

    return {
        "board": board,
        "articles_fetched": len(results),
        "totals": {
            "push_count": totals["push"],
            "boo_count": totals["boo"],
            "neutral_count": totals["neutral"],
            "score": totals["push"] - totals["boo"],
        },
        "articles": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="PTT web BBS scraper")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("boards", help="hot board list")

    p_cls = sub.add_parser("cls", help="board category tree")
    p_cls.add_argument("id", type=int, nargs="?", default=1, help="category id (root = 1)")

    p_list = sub.add_parser("list", help="list articles on a board")
    p_list.add_argument("board", help="board name, e.g. Gossiping")
    p_list.add_argument("--pages", type=int, default=1, help="index pages to walk (newest first)")

    p_search = sub.add_parser("search", help="search a board (keywords, author:, thread:, recommend:)")
    p_search.add_argument("board", help="board name, e.g. Gossiping")
    p_search.add_argument("query", help='e.g. "颱風", "author:someone", "recommend:50 颱風"')
    p_search.add_argument("--pages", type=int, default=1, help="result pages to fetch")

    p_man = sub.add_parser("man", help="essence area (精華區) listing")
    p_man.add_argument("board", help="board name, e.g. Gossiping")
    p_man.add_argument("path", nargs="?", default=None, help="subdirectory path within /man/<board>/")

    p_article = sub.add_parser("article", help="fetch one article with push/boo counts")
    p_article.add_argument("url", help="full URL or /bbs/... path")

    p_stats = sub.add_parser("stats", help="per-article and board-wide push/boo totals")
    p_stats.add_argument("board", help="board name, e.g. Gossiping")
    p_stats.add_argument("--pages", type=int, default=1, help="index pages to walk")
    p_stats.add_argument("--limit", type=int, default=None, help="max articles to fetch")

    args = parser.parse_args()
    session = make_session()

    if args.command == "boards":
        result = hot_boards(session)
    elif args.command == "cls":
        result = board_categories(session, args.id)
    elif args.command == "list":
        result = list_board(session, args.board, args.pages)
    elif args.command == "search":
        result = search_board(session, args.board, args.query, args.pages)
    elif args.command == "article":
        result = get_article(session, args.url)
    elif args.command == "man":
        result = man_listing(session, args.board, args.path)
    else:
        result = board_stats(session, args.board, args.pages, args.limit)

    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
