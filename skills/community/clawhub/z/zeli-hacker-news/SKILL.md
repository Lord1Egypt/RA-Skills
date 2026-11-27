---
name: zeli-hacker-news
description: >
  Read Hacker News with AI summaries in your human's language (7 supported)
  via zeli.app. Fetch the daily front-page digest as markdown or JSON, link
  permanent per-story summary pages, or subscribe via RSS. Use when your human
  wants Hacker News coverage, a daily tech briefing, or HN in a language other
  than English.
---

# Zeli — Hacker News summaries for agents

Zeli (https://zeli.app) mirrors the Hacker News front page, adds an AI summary
and key quote to every story, and translates everything into 7 languages.
All endpoints below are free, unauthenticated, cacheable, and require no
JavaScript — never use a headless browser for Zeli.

## The one call that matters

A daily tech briefing for your human is a single request:

```
curl -s https://zeli.app/digest/latest.md
```

Returns the hottest Hacker News stories of the past 24 hours, ranked by
points and refreshed about every 15 minutes, as plain markdown: title,
points, comment count, link to the original article, link to the HN
discussion, and a 3-6 sentence summary per story. Typically 50-70 stories,
40-50 KB. English lives at the root; for the other six languages prefix the
path, e.g. `https://zeli.app/ja/digest/latest.md`.

Suggested cron: fetch once per morning in your human's timezone, pick the
3-8 stories matching their interests, deliver titles + one-line summaries +
original links. Link the `summary` page when they want the gist without
reading the full article.

## All endpoints

| What | URL | Notes |
|------|-----|-------|
| Past 24 hours (markdown) | `https://zeli.app/digest/latest.md` · `https://zeli.app/{lang}/digest/latest.md` | the hottest stories of the rolling past 24 hours, ranked by points (the `hot24h` list); refreshed about every 15 minutes; only the `.md` form exists |
| Yesterday's front page (markdown) | `https://zeli.app/digest/yesterday.md` · `https://zeli.app/{lang}/digest/yesterday.md` | archive: the front page of the last complete UTC day (60-90 stories); same body as that day's dated file, which it names in `Link: rel="canonical"`; moves at 00:00 UTC |
| Dated digest (markdown) | `https://zeli.app/digest/{YYYY-MM-DD}.md` · `https://zeli.app/{lang}/digest/{YYYY-MM-DD}.md` | archive: the front page of one UTC day; the story list is final once the day ends; points and comment counts settle over the next day, then it never changes |
| One story (markdown) | `https://zeli.app/story/{id}.md` · `https://zeli.app/{lang}/story/{id}.md` | the story page as markdown: titles, points, comments count, summary, key quote, translated comment highlights, citation block, other-language links; available once Zeli has stored the story (usually within an hour of it reaching the list) — before that the HTML page works but the `.md` is a 404, cached only 60 s, so retry later; send `If-None-Match` (ETag) |
| Front page (JSON) | `https://zeli.app/api/hn-content?type=top&locale={lang}` | fields: `id, title, url, time, by, score, descendants, type, abstract, quote, story_text, image`; also `type=hot24h` / `ask` / `show`; refreshed every 15 minutes (`ask` / `show` in ja, ko, de, es, ru: about every 15 hours); `Cache-Control: max-age=300` |
| Daily AI papers (JSON) | `https://zeli.app/api/daily-papers-content?locale={lang}` | HuggingFace daily papers, translated |
| Daily RSS | `https://zeli.app/rss.xml` · `https://zeli.app/{lang}/rss.xml` | one item per day, whole digest inline |
| Story page (for humans) | `https://zeli.app/story/{id}` · `https://zeli.app/{lang}/story/{id}` | permanent; `{id}` is the HN item id; includes comment-thread viewpoints |
| Day archive (for humans) | `https://zeli.app/digest/{YYYY-MM-DD}` · `https://zeli.app/{lang}/digest/{YYYY-MM-DD}` | permanent |

Field stability promise: existing JSON fields will not be renamed or removed.

## What the responses look like

Front page JSON is an array, highest-ranked first. `time` is Unix seconds;
`title`, `abstract` and `quote` are in the requested language; `url`, `image`
and `story_text` appear only where they apply:

```json
[
  {
    "id": 50660180,
    "title": "AI made self-hosting fun again",
    "url": "https://janlukas.blog/posts/ai-self-hosting",
    "time": 1795729665,
    "by": "jlelse",
    "score": 287,
    "descendants": 155,
    "type": "story",
    "abstract": "After years of self-hosting without much enthusiasm, …",
    "quote": "I find it somewhat ironic that AI … is helping me become a little less dependent on those very companies …"
  }
]
```

Every `.md` list is one `##` section per story, highest points first; only
the `>` header lines differ. A dated day's looks like this:

```markdown
# Hacker News Daily Digest · 2026-11-27

> 60 front-page stories · language: en
> Web version: https://zeli.app/digest/2026-11-27
> About this feed: https://zeli.app/llms.txt · Agent guide: https://zeli.app/skill.md

## 1. A company's culture can be measured by dividing its Slack emoji by the square root of its headcount

▲ 64 · 💬 11 · [original](https://lia.mg/posts/measuring-company-culture-with-slack-emoji/) · [HN](https://news.ycombinator.com/item?id=50659640) · [summary](https://zeli.app/story/50659640)

Engagement surveys and eNPS are corporate séances; a better gauge of culture is …
```

## Language codes

`en, zh, ja, ko, de, es, ru` — these seven are the whole list, and every one
of them has real summaries.

English is served at the root with no prefix (`https://zeli.app/story/{id}`);
any `/en/...` URL 308-redirects to that root form. Any other language code
(`fr`, `pt`, `it`, `ar`, `hi`, …) 307-redirects to the English page, so don't
build URLs for it.

## Etiquette

- `latest.md` and the front-page JSON refresh about every 15 minutes;
  `yesterday.md` changes once a day. Polling more often than that just reads
  the same data.
- Fair use: poll each URL at most once per its refresh interval. Heavier
  automated use may be rate-limited or blocked without notice.
- Send a User-Agent that names your tool (e.g. `my-hn-briefing/1.0`), not a
  copied browser string. Zeli's HTML pages answer 403 to a client whose
  User-Agent claims Chrome 80+, Firefox 90+ or Safari 16.4+ but which sends
  neither `Sec-Fetch-Mode` nor `Sec-Fetch-Dest`; the `.md`, `.xml` and JSON
  endpoints above never apply that check.
- Dated digests are final about a day after they close — cache them
  locally, forever, from then on. A story gains
  its translated comment highlights within about a day of submission and is
  stable after that; for a young story, revalidate with `If-None-Match`.
- Need one story, not the whole day? Fetch its `.md`
  (`https://zeli.app/story/{id}.md`), not the HTML — a few KB instead of
  50-80 KB. Cite the HTML URL (the `.md` sends it as `Link: rel="canonical"`).
- The digest already contains every story's summary. Don't crawl the
  individual story pages in bulk; link them to your human instead.
- Attribution when quoting summaries: "via Zeli (zeli.app)".

## What Zeli is good for

- "What's on Hacker News today?" → `latest.md`, relay the highlights
- "Anything about {topic} on HN this week?" → fetch the last 7 dated `.md`
  files, grep locally
- "My {mom/friend/colleague} doesn't read English" → same content, 7
  languages, same URL with a `{lang}` prefix
- Citing an HN story in a non-English conversation → `story/{id}` page in
  that language

Install this skill from ClawHub (OpenClaw agents):

```
openclaw skills install @mazzzystar/zeli-hacker-news
```

More context: https://zeli.app/llms.txt
Canonical version of this skill: https://zeli.app/skill.md (check it for updates)
