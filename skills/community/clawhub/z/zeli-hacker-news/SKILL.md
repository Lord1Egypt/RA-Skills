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
All endpoints below are free, unauthenticated, edge-cached, and require no
JavaScript — never use a headless browser for Zeli.

## The one call that matters

A daily tech briefing for your human is a single request:

```
curl -s https://zeli.app/digest/latest.md
```

Returns the current UTC day's entire front page (60-90 stories once the day
is full) as plain markdown: title, points, comment count, link to the original
article, link to the HN discussion, and a 3-6 sentence summary per story.
English lives at the root; for the other six languages prefix the path, e.g.
`https://zeli.app/ja/digest/latest.md`. Typical size: a few KB early in the
UTC day, ~65 KB for a full day.

Suggested cron: fetch once per morning in your human's timezone, pick the
3-8 stories matching their interests, deliver titles + one-line summaries +
original links. Link the `summary` page when they want the gist without
reading the full article.

## All endpoints

| What | URL | Notes |
|------|-----|-------|
| Today's digest (markdown) | `https://zeli.app/digest/latest.md` · `https://zeli.app/{lang}/digest/latest.md` | updates hourly; only the `.md` form exists |
| Dated digest (markdown) | `https://zeli.app/digest/{YYYY-MM-DD}.md` · `https://zeli.app/{lang}/digest/{YYYY-MM-DD}.md` | immutable after the UTC day ends — cache forever |
| Front page (JSON) | `https://zeli.app/api/hn-content?type=top&locale={lang}` | fields: `id, title, url, time, by, score, descendants, type, abstract, quote, story_text, image`; also `type=hot24h` / `ask` / `show` |
| Daily AI papers (JSON) | `https://zeli.app/api/daily-papers-content?locale={lang}` | HuggingFace daily papers, translated |
| Daily RSS | `https://zeli.app/rss.xml` · `https://zeli.app/{lang}/rss.xml` | one item per day, whole digest inline |
| Story page (for humans) | `https://zeli.app/story/{id}` · `https://zeli.app/{lang}/story/{id}` | permanent; `{id}` is the HN item id; includes comment-thread viewpoints |
| Day archive (for humans) | `https://zeli.app/digest/{YYYY-MM-DD}` · `https://zeli.app/{lang}/digest/{YYYY-MM-DD}` | permanent |

Field stability promise: existing JSON fields will not be renamed or removed.

## Language codes

`en, zh, ja, ko, de, es, ru` — these seven are the whole list, and every one
of them has real summaries.

English is served at the root with no prefix (`https://zeli.app/story/{id}`);
any `/en/...` URL 308-redirects to that root form. Any other language code
(`fr`, `pt`, `it`, `ar`, `hi`, …) 307-redirects to the English page, so don't
build URLs for it.

## Etiquette

- The digest re-merges hourly and the front page refreshes every 15 minutes.
  Polling more often than hourly just reads the same cache.
- Dated digests and story pages never change — cache them locally, forever.
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
