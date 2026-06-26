# OpenClaw Usage

## One-Line Positioning

This skill collects Xiaohongshu/Rednote public notes and comments, with a demand-discovery mode for small-scale recent high-interaction data collection.

## Recommended OpenClaw Invocation

Use this skill when the user asks to:

- Run Xiaohongshu demand discovery
- Collect recent high-interaction Xiaohongshu notes and comments
- Mine Xiaohongshu comments for user needs
- Collect `求推荐`, `避雷`, `平替`, or similar demand-keyword data
- Prepare Xiaohongshu comment data for later LLM analysis

Prefer:

```bash
python -m scripts demand-discovery
```

Use `search` for simple keyword search. Use `feed` when the user gives a specific note id and `xsec_token`.

## Common Commands

Login:

```bash
python -m scripts qrcode --headless=false
```

Check login:

```bash
python -m scripts check-login
```

Search:

```bash
python -m scripts search "平替" --sort-by=最多评论 --publish-time=一周内 --limit=10
```

Feed detail with comments:

```bash
python -m scripts feed <feed_id> <xsec_token> --load-comments --max-comments=20
```

## Minimal Demand Discovery Test

```bash
python -m scripts demand-discovery --keywords "求推荐" --posts-per-keyword 1 --search-limit 3 --max-comments 5 --headless=false
```

## Real Collection Command

```bash
python -m scripts demand-discovery
```

Multiple keywords:

```bash
python -m scripts demand-discovery --keywords "求推荐,避雷,平替" --posts-per-keyword 2 --search-limit 5 --max-comments 10 --headless=false
```

Keyword file:

```bash
python -m scripts demand-discovery --keywords-file keywords.txt
```

## Output Files

Default output directory:

```text
data/demand_discovery/<timestamp>/
```

Files:

- `notes_clean.jsonl`: note-level records with status, interaction counts, publish time status, and comment counts
- `comments_clean.jsonl`: cleaned comment-level records with `author_hash`
- `collection_summary.json`: machine-readable totals, filters, errors, and per-keyword stats
- `collector_report.md`: human-readable run summary

## OpenClaw Local Installation

Install the unpacked folder, not the zip file. The root folder must contain `SKILL.md`.

```bash
openclaw skills install "<本地 skill 文件夹路径>" --as xhs-demand
```

Example:

```bash
openclaw skills install "C:\Users\Zev\Documents\Codex\2026-05-09\you-are-codex-i-want-you\xiaohongshu-skill-1.0.2-src" --as xhs-demand
```

Verify:

```bash
openclaw skills list
openclaw skills check
openclaw skills info xhs-demand
```

## Safety Boundaries

- Collect only publicly accessible content.
- Do not bypass login, captcha, rate limits, or risk controls.
- Stop when captcha is triggered and ask the user to handle verification manually.
- Stop when cookies are expired or login is invalid.
- Do not save raw usernames, nicknames, avatars, or profile links.
- Use `author_hash` only for deduplication and structured data.
- Do not call `comment.py`, `interact.py`, or `publish.py` for demand discovery.
- Do not run large high-frequency collections.
- First-version use is limited to learning, research, internal validation, and small-scale collection.

## FAQ

### 未登录怎么办

Run:

```bash
python -m scripts qrcode --headless=false
```

Then check:

```bash
python -m scripts check-login
```

### cookie 失效怎么办

Run QR-code login again. Do not try to bypass login.

### 触发验证码怎么办

Stop the collection. Re-run with visible browser mode only for manual handling:

```bash
python -m scripts qrcode --headless=false
```

Wait before retrying. Do not automate captcha bypass.

### comments_clean.jsonl 为空怎么办

Try a small visible-browser run:

```bash
python -m scripts demand-discovery --keywords "求推荐" --posts-per-keyword 1 --search-limit 3 --max-comments 5 --headless=false
```

Possible causes:

- Comments did not load on the detail page
- Notes had no comments after filtering
- Login expired
- Detail page fields changed
- Batch was too small or keyword had low comment activity

### publish_time_unknown 太多怎么办

Xiaohongshu may have changed detail fields. Inspect a few raw note detail results through the `feed` command, then update the publish-time extraction paths if needed. Unknown publish time notes are kept instead of dropped.

### pc_search 详情失败怎么办

The demand collector uses `pc_search` for search-origin note detail URLs. If it becomes unstable, test the original feed command with the same `feed_id` and `xsec_token`. If the original route is more stable, switch demand discovery detail calls back to `pc_feed` in code.
