---
name: xiaohongshu-skill
description: Use this skill when the user needs to work with Xiaohongshu/Rednote public content: QR-code login, keyword search, note details, user profiles, explore feed extraction, or small-scale demand discovery collection from recent high-interaction notes and comments. Prefer the demand-discovery command when the user wants to collect recent Xiaohongshu notes/comments for later LLM demand analysis.
user-invokable: true
metadata: {"openclaw": {"emoji": "\ud83d\udcd5", "requires": {"bins": ["python3", "playwright"], "anyBins": ["python3", "python"]}, "os": ["win32", "linux", "darwin"], "install": [{"id": "pip", "kind": "node", "label": "Install Python dependencies", "bins": ["playwright"]}]}}
---

# Xiaohongshu Skill

This is a Python Playwright based OpenClaw skill for Xiaohongshu/Rednote public-content workflows. It reads page data from Xiaohongshu web pages, mainly through `window.__INITIAL_STATE__`, and returns structured JSON.

It includes the original capabilities:

- QR-code login and login status checking
- Keyword search with sort/type/time filters
- Note detail extraction
- Comment loading for note detail pages
- User profile extraction
- Explore feed extraction
- Optional publishing and interaction commands retained from the upstream skill

It also adds:

- **Xiaohongshu Demand Discovery Collector**

The demand discovery mode searches demand-style keywords, collects recent high-interaction notes and comments, cleans the data, removes raw user identity fields, and writes structured files for later LLM demand analysis or product-manager agent workflows.

## What This Skill Is

This skill is a Xiaohongshu content and comment collection tool. The demand discovery collector can:

- Search recent notes using demand-oriented keywords such as `求推荐`, `避雷`, `平替`, `真实测评`, `后悔买`, `踩坑`
- Filter search results to notes from the last week
- Sort by most comments by default
- Visit note detail pages
- Load comments
- Prefer notes published within the recent `--days` window
- Preserve notes whose publish time cannot be parsed as `publish_time_unknown`
- Clean comments by removing empty, duplicate, short-noise, and obvious advertising comments
- Save structured output files for downstream analysis

## What This Skill Is Not

This skill is not:

- A tool for bypassing Xiaohongshu login, captcha, rate limits, or risk controls
- An automatic like/comment/follow/publish bot for demand discovery
- An LLM demand analysis tool
- A product-manager agent
- A complete SaaS product
- An unrestricted high-volume crawler

Use it for learning, research, internal product validation, and small-scale public-content collection.

## When OpenClaw Should Use It

Prefer `demand-discovery` when the user says things like:

- “帮我跑一次小红书需求发现”
- “抓小红书最近几天高互动笔记和评论”
- “用小红书评论区挖用户需求”
- “分析小红书用户在求推荐、避雷、平替里的需求”
- “采集小红书热门笔记评论，后面喂给 LLM 分析”

Use `search` when the user only wants to search a Xiaohongshu keyword:

```bash
python -m scripts search "关键词"
```

Use `feed` when the user provides a concrete note id/link context and wants note detail or comments:

```bash
python -m scripts feed <feed_id> <xsec_token> --load-comments --max-comments=20
```

Use `qrcode` or `check-login` when login state is unknown or expired.

Do not use interaction or publishing commands for demand discovery. The collector itself does not call `comment.py`, `interact.py`, or `publish.py`.

## Installation

Run all commands from the skill root directory.

```bash
pip install -r requirements.txt
playwright install chromium
```

On Linux/WSL, Chromium dependencies may also be required:

```bash
playwright install-deps chromium
```

## Login

First login by QR code:

```bash
python -m scripts qrcode --headless=false
```

Check login status:

```bash
python -m scripts check-login
```

If cookies expire, run the QR-code login again.

## Command Reference

### Search

```bash
python -m scripts search "美食" --sort-by=最新 --note-type=图文 --publish-time=一周内 --limit=10
```

Common search options:

- `--sort-by`: `综合`, `最新`, `最多点赞`, `最多评论`, `最多收藏`
- `--note-type`: `不限`, `视频`, `图文`
- `--publish-time`: `不限`, `一天内`, `一周内`, `半年内`
- `--search-scope`: `不限`, `已看过`, `未看过`, `已关注`
- `--location`: `不限`, `同城`, `附近`
- `--limit`: returned result limit

### Feed Detail

```bash
python -m scripts feed <feed_id> <xsec_token>
python -m scripts feed <feed_id> <xsec_token> --load-comments --max-comments=20
```

### Explore Feed

```bash
python -m scripts explore --limit=20
```

The explore feed exists, but demand discovery should prefer keyword search in the first version.

### User Profile

```bash
python -m scripts user <user_id> [xsec_token]
python -m scripts me
```

## Demand Discovery Collector

Basic command:

```bash
python -m scripts demand-discovery
```

Small-scale test:

```bash
python -m scripts demand-discovery --keywords "求推荐" --posts-per-keyword 1 --search-limit 3 --max-comments 5 --headless=false
```

Specify multiple keywords:

```bash
python -m scripts demand-discovery --keywords "求推荐,避雷,平替" --posts-per-keyword 2 --search-limit 5 --max-comments 10 --headless=false
```

Use a keyword file:

```bash
python -m scripts demand-discovery --keywords-file keywords.txt
```

Important parameters:

- `--keywords`: comma-separated keywords
- `--keywords-file`: UTF-8 text file, one keyword per line
- `--days`: recent-day window for note filtering, default `3`
- `--search-publish-time`: Xiaohongshu search time filter, default `一周内`
- `--sort-by`: default `最多评论`, also supports `最多点赞`
- `--note-type`: default `不限`
- `--posts-per-keyword`: notes saved per keyword, default `3`
- `--search-limit`: search results inspected per keyword, default `8`
- `--max-comments`: valid comments saved per note, default `20`
- `--output-dir`: output directory; default `data/demand_discovery/<timestamp>/`
- `--timezone`: default `Asia/Shanghai`
- `--headless`: `true` or `false`

Default demand keywords:

```text
求推荐
避雷
平替
真实测评
后悔买
踩坑
好用吗
怎么选
值不值得买
学生党
新手必备
替代品
不好用
怎么解决
```

Output files:

- `notes_clean.jsonl`: one note-level record per saved/attempted note
- `comments_clean.jsonl`: cleaned comment-level records
- `collection_summary.json`: machine-readable summary and counters
- `collector_report.md`: human-readable report

The collector uses one browser session per run:

1. `XiaohongshuClient.start()`
2. `LoginAction.check_login_status()`
3. Reused `SearchAction`
4. Reused `FeedDetailAction`
5. `XiaohongshuClient.close()`

## Privacy And Data Safety

Demand discovery output must not save raw Xiaohongshu usernames, nicknames, avatars, or profile links. It writes `author_hash` instead:

```text
sha256("xiaohongshu:" + raw_author_id)
```

The preferred raw author id is `user_id`. If unavailable, the collector may hash another available author field such as nickname or profile link, then discard the original value.

## Safety And Compliance Boundaries

- Collect only publicly accessible content.
- Do not bypass login, captcha, rate limits, or platform risk controls.
- If captcha is triggered, stop and ask the user to handle it manually.
- If login/cookie is invalid, stop and ask the user to log in again.
- Do not save raw usernames, nicknames, avatars, or profile links.
- Use `author_hash` only for deduplication and structured analysis.
- Do not call `comment.py`, `interact.py`, or `publish.py` for demand discovery.
- Do not run large high-frequency collections.
- Keep first-version usage small, conservative, and reviewable.

## Troubleshooting

- Not logged in: run `python -m scripts qrcode --headless=false`
- Cookie expired: login again by QR code
- Captcha triggered: stop collection, wait, and handle verification manually in visible browser mode
- Empty comments output: reduce batch size, test with `--headless=false`, and confirm comments load on the note page
- Too many `publish_time_unknown`: Xiaohongshu may have changed detail fields; inspect raw note detail structure before relying on recent-day filtering
- Detail failures from search results: `demand-discovery` uses `pc_search` as `xsec_source`; if this becomes unstable, test the original `feed` command behavior with `pc_feed`
