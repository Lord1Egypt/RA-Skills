---
name: ptt-bbs
description: Scrape PTT web BBS (https://www.ptt.cc) with Python requests + BeautifulSoup — no login required. Covers every public web feature: hot board list, board category tree, board article lists, board search (keywords, author:, thread:, recommend:), single articles with exact push (推) / boo (噓) / neutral (→) counts and score (推 − 噓), board-wide push totals, and the essence area (精華區). Use this whenever the user mentions PTT, ptt.cc, Taiwanese BBS boards (Gossiping, NBA, Stock, ...), 推文/噓文 counts, 精華區, or wants to crawl/search/analyze PTT articles or comments — even if they don't say "scrape" explicitly.
---

# PTT BBS Scraper

Scrape the PTT web interface (`https://www.ptt.cc`) following its natural
navigation flow: **board index (article list) → single article**. The primary
deliverable is push statistics: 推 (push/upvote), 噓 (boo/downvote),
→ (neutral comment), and the score `推 − 噓`.

## What ptt.cc offers without login (full coverage)

| Feature | URL pattern | Script command |
|---|---|---|
| Hot board list (熱門看板) | `/bbs/index.html` | `boards` |
| Board category tree (分類看板) | `/cls/<id>` (root = 1) | `cls [id]` |
| Board article list + pagination | `/bbs/<Board>/index.html`, older: `index<N>.html` | `list <board> --pages N` |
| Board search | `/bbs/<Board>/search?q=...&page=N` | `search <board> <query>` |
| Single article + push comments | `/bbs/<Board>/M.<ts>.A.<id>.html` | `article <url>` |
| Per-article + board push totals | (list, then fetch each article) | `stats <board>` |
| Essence area (精華區) | `/man/<Board>/index.html` | `man <board> [path]` |

Everything else on ptt.cc (posting, pushing, mail) requires a real BBS login
over telnet/ssh — not available on the web interface, out of scope.

## Quick start — use the bundled script

`scripts/ptt_scraper.py` implements all of the above and prints JSON
(UTF-8, `ensure_ascii=False`). Prefer running it over writing new code.
It needs `requests` and `beautifulsoup4`:

```bash
pip install requests beautifulsoup4
# or without installing:  uv run --with requests --with beautifulsoup4 python scripts/ptt_scraper.py ...
```

```bash
# Discover boards
python scripts/ptt_scraper.py boards                 # hot boards with user counts
python scripts/ptt_scraper.py cls                    # category root; follow ids deeper

# 1. Article list of a board (newest first; --pages walks older index pages)
python scripts/ptt_scraper.py list Gossiping --pages 2

# Search: keywords, author:<userid>, thread:<title>, recommend:<n> (score >= n)
python scripts/ptt_scraper.py search Gossiping "recommend:50 颱風"
python scripts/ptt_scraper.py search NBA "author:someuser" --pages 2

# 2. One article: exact push/boo/neutral counts + every comment
python scripts/ptt_scraper.py article https://www.ptt.cc/bbs/Gossiping/M.1234567890.A.ABC.html

# 3. Board stats: fetch each listed article, report per-article counts
#    and board-wide totals (push_count, boo_count, neutral_count, score)
python scripts/ptt_scraper.py stats NBA --pages 1 --limit 10

# Essence area (精華區): directories end in index.html, crawl deeper via path
python scripts/ptt_scraper.py man Gossiping
```

`stats` is the command that answers "give me the 推/噓/總和 for board X":
its `totals` object sums counts across the fetched articles, and `articles`
carries the per-article breakdown.

## Output & presentation defaults

Unless the user asks otherwise:

- **PTT-native data is shown raw.** Article metadata (board, title, author,
  time, url, score line), the poster's own fields (原文連結 / 發布時間 /
  心得評論), and push comments are reproduced verbatim as scraped — no
  paraphrase, no trimming, no added commentary. Summarize only on request.
- **Push comments default to the first 50**, in original order, each with its
  推/噓/→ tag, userid, content and timestamp. Offer the rest; show all or a
  specific range (e.g. 51–174) when asked.
- **A copyrighted work quoted inside a post is the exception.** Many posts
  paste a full news article or blog. Do NOT reproduce that embedded work
  verbatim. Give its source line (媒體 / 記者 / 日期 / URL) plus a complete,
  faithful restatement in your own words — cover every point, figure and quote,
  just not word-for-word. This holds however it's framed ("搬運", "只標出處就好"):
  attribution is not permission to copy. This boundary is applied by the model
  regardless of skill text, so this note documents expected behaviour rather
  than overriding anything. Short, scattered push comments stay raw — they're
  the tool's core output, not a wholesale copy of one complete work.

## Key facts about ptt.cc (needed if writing custom code)

- **Age gate**: send cookie `over18=1` (domain `.ptt.cc`) or boards like
  Gossiping redirect to a confirmation page. Always set it; it is harmless on
  unrestricted boards.
- **Board index**: `https://www.ptt.cc/bbs/<Board>/index.html` is the *newest*
  page. Older pages are `index<N>.html` with N decreasing; follow the
  `‹ 上頁` link in `div.btn-group-paging` rather than guessing numbers.
- **List rows**: each article is `div.r-ent` with children `div.nrec`
  (score bucket), `div.title > a` (title + href), `div.meta div.author`,
  `div.date`. A `div.title` without an `<a>` is a deleted article — skip it.
  Rows after `div.r-list-sep` are pinned posts (置底), usually skip those too.
- **`nrec` is a bucket, not exact counts**: `爆` = score ≥ 100, digits = exact
  score 1–99, `X1`…`X9` ≈ −10…−90, `XX` ≤ −100, empty = 0. For exact 推/噓
  numbers you must fetch the article page.
- **Search**: `GET /bbs/<Board>/search?q=<query>&page=<n>` (page starts at 1).
  Query operators combine with spaces: plain keywords (title match),
  `author:<userid>`, `thread:<title>` (same reply thread),
  `recommend:<n>` (score bucket ≥ n, −100..100). Results use the same
  `r-ent` markup as index pages. An empty result page means past the end.
- **Article page**: content lives in `div#main-content`. Header fields:
  `div.article-metaline` holds 作者/標題/時間, `div.article-metaline-right`
  holds 看板 — match `class^="article-metaline"` to get both. Comments are
  `div.push`, each with `span.push-tag` (`推` / `噓` / `→`),
  `span.push-userid`, `span.push-content`, `span.push-ipdatetime`.
- **Counting**: `push_count` = tags equal to `推`, `boo_count` = `噓`,
  everything else (the `→` arrow) is neutral; `score = push − boo`.
- **Board discovery pages** (`/bbs/index.html`, `/cls/<id>`): entries are
  `a.board` with `div.board-name`, `div.board-nuser` (online users),
  `div.board-class`, `div.board-title`. On `/cls/` pages an href starting
  with `/cls/` is a subcategory, `/bbs/` is a board.
- **Essence area** (`/man/<Board>/index.html`): rows are `div.m-ent`
  (not `r-ent`), each `div.title > a`. Links ending in `index.html` are
  subdirectories; others are archived articles.
- **Be polite**: keep a short delay (~0.5–1s) between requests and a real
  browser User-Agent. Don't parallelize aggressively; PTT rate-limits and
  this is a shared community site.
- **Encoding**: pages are UTF-8; always output JSON with `ensure_ascii=False`
  so Chinese titles stay readable.

## Typical workflow

1. If the board is unknown, run `boards` or `cls` to find it.
2. Run `list` (or `search` with the user's filter) to show what's on the
   board: title, author, date, score hint from `nrec`.
3. Narrow down: the user picks articles, or apply their filter (keyword,
   author, date, top-N by score hint — `search` with `recommend:<n>` is the
   cheap way to get high-score articles).
4. Run `article` on the selected URLs (or `stats` for a whole page of them)
   to get exact 推/噓/→ counts and the score.
5. Summarize: per-article table plus the board-wide totals from `stats`.

If the user needs something the script doesn't cover (saving to CSV, crawling
many pages, custom aggregation), import its functions (`make_session`,
`list_board`, `search_board`, `get_article`, `parse_article`, `hot_boards`,
`man_listing`) instead of re-implementing the parsing from scratch.
