---
name: ak-rss-digest
description: Curate a Chinese reading digest from a fixed bundle of RSS and Atom feeds, with a strong preference for AI agent thinking, frontier AI commentary, deep interviews, and non-boring high-signal essays. Use when Codex needs to pull the latest week's posts by default, or a specific day's posts when explicitly requested, summarize them, score each article on a 10-point scale, and output only the posts scoring above 7 in a concise Chinese daily-brief style.
---

# AK RSS Digest

## Overview

Use this skill to build a current reading list from the feed bundle in `references/feeds.opml`.
Default to the most recent 7 days ending on the current date in `Asia/Shanghai`, and narrow to a single day only when the user explicitly asks for it.

## Workflow

1. Run `python3 scripts/fetch_today_feed_items.py --format json` to collect entries from the configured feeds. This defaults to the most recent 7 days.
2. Treat feed-level network failures as non-fatal. Continue with the feeds that succeeded and mention major failures only when they materially reduce coverage.
3. Read the structured output and discard obvious mismatches before opening article pages. Reject items that are clearly raw research papers, release notes, changelogs, benchmark dumps, or narrowly technical implementation logs without broader implications.
4. Open the remaining candidate links when the feed summary is too thin to judge the article well. Skim for thesis, novelty, readability, and whether the piece offers strong perspective rather than just information.
5. Score every serious candidate on the rubric below. Output only items with a score strictly greater than `7.0`.
6. If nothing clears the threshold, say so directly instead of padding the output with mediocre picks.

## Selection Heuristics

Prefer articles with at least one of these traits:

- Fresh thinking about AI agents, agent tooling, agent UX, multi-agent workflows, evaluation, deployment, or failure modes.
- Strong interviews or conversations with operators, founders, researchers, or engineers who reveal how frontier work is actually being done.
- Essays that synthesize a new direction, new constraint, or strategic implication in AI, software, or adjacent technology.
- Pieces that are readable and idea-dense for a general technical audience, not just specialists in one subfield.

Penalize heavily or reject:

- Pure technical papers and paper summaries with little interpretive value.
- Vendor marketing, launch fluff, SEO writing, or obvious news rewrites.
- Narrow implementation diaries that do not connect to broader product, research, or ecosystem questions.
- Dry reference material that is correct but not worth a strong recommendation.

## Scoring Rubric

- `9-10`: Exceptional fit. Strong signal, strong writing, original insight, and clearly valuable for someone tracking AI agents or adjacent frontier shifts.
- `8-8.9`: Good recommendation. Worth reading, clear point of view, and relevant enough to the target taste profile.
- `7-7.9`: Borderline. Useful but not compelling enough for the final digest. Do not output it.
- `5-6.9`: Competent but dry, derivative, too narrow, or not aligned with the target taste profile.
- `<5`: Irrelevant, low-signal, or actively unsuitable.

When scoring, weigh these dimensions:

- Relevance to AI agents, frontier AI, deep operator insight, or adjacent strategic technology discussion.
- Originality of the article's argument or reporting.
- Readability and ability to hold attention.
- Practical usefulness for someone trying to keep up with meaningful new directions.

## Output Format

Write the final answer in Simplified Chinese.
For each article that scores above `7`, include exactly these elements with Chinese labels:

- `标题`: original article title.
- `评分`: `x/10`, use one decimal place when helpful.
- `推荐语`: one or two sentences explaining why this is worth reading.
- `摘要`: exactly two sentences summarizing the article.
- `链接`: canonical article URL.

Use a concise tone that reads like a curated daily brief, not a formal report:

- Prefer short, direct sentences over explanatory padding.
- Lead with why the article is worth the user's time.
- Keep each item compact and scannable.
- Avoid English field names such as `Title`, `Score`, or `Recommendation`.

Use this structure for the final answer:

```markdown
本期从最近一周的 RSS 里筛出几篇值得看的文章，重点偏 AI agent、前沿判断和不太枯燥的深度内容。

- 标题：文章标题
  评分：8.7/10
  推荐语：1-2 句话，先说为什么值得看。
  摘要：严格两句话，讲清核心观点和价值。
  链接：文章链接
```

If nothing qualifies, say so directly in Chinese, for example:

```markdown
这周没有筛到真正值得推荐的文章。现有更新要么偏技术细节，要么信息密度不够，没有过 7 分线。
```

## Resources

- `scripts/fetch_today_feed_items.py`
  Use this script to fetch the configured feeds and return recent entries as structured JSON or Markdown.

- `references/feeds.opml`
  Use this as the source of truth for the feed bundle. Keep the workflow anchored to this file unless the user explicitly asks to change the feed list.

## Command Examples

Fetch the latest week of entries in Shanghai time:

```bash
python3 scripts/fetch_today_feed_items.py --format json
```

Fetch a single day explicitly:

```bash
python3 scripts/fetch_today_feed_items.py --date 2026-03-17 --days 1 --timezone Asia/Shanghai --format json
```

Fetch the latest posts from the past week:

```bash
python3 scripts/fetch_today_feed_items.py --days 7 --limit 30 --format json
```

Inspect a quick Markdown view instead of JSON:

```bash
python3 scripts/fetch_today_feed_items.py --format markdown
```
