---
name: reading-digest
description: Processes the reading backlog weekly and delivers what was worth reading with skip verdicts. Use when a user has saved articles and newsletters accumulating unread.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
metadata:
  openclaw.emoji: "📚"
  openclaw.user-invocable: "true"
  openclaw.category: daily-rhythm
  openclaw.tags: "reading,newsletters,articles,digest,curation,knowledge"
  openclaw.triggers: "reading backlog,process my newsletters,reading digest,too much to read,what should I read,newsletter digest"
  openclaw.requires: '{"config": ["channels"]}'
  openclaw.homepage: https://clawhub.com/skills/reading-digest


# Reading Digest

Everyone has a reading backlog. Saved articles, newsletters, tabs, links.
Most of it never gets read.

Once a week, this skill processes it. You get what was worth your time — in ten minutes.

---

## File structure

```
reading-digest/
  SKILL.md
  queue.md           ← items to process
  config.md          ← sources, delivery, digest style
  archive.md         ← processed items with one-line summaries
```

---

## Sources

The skill pulls from wherever reading accumulates:

- **Newsletter inbox** — scans Gmail for newsletters, processes unread ones
- **Saved links** — Pocket, Readwise, browser bookmarks (if accessible)
- **Shared links** — URLs dropped directly by user
- **Instapaper / Matter** — if connected via MCP
- **Manually added** — `/read add [url]`

---

## Setup flow

### Step 1 — Sources

Check what's connected. Default: Gmail newsletters only (most people have these).
Ask if they use a read-later app.

### Step 2 — Digest style

Three options:
- **Bullets** — headline + one sentence per item. Dense. For people who want coverage.
- **Narrative** — short paragraph per item. More readable. Default.
- **Ideas only** — one key idea per item, no context. For people who read fast.

### Step 3 — Frequency and timing

Default: Friday afternoon (clear the week's backlog before the weekend).
Some people prefer Sunday evening (prep for the week).

### Step 4 — Quality filter

Ask: "What topics do you care about? What can you skip?"
Build a topic filter. Newsletters about topics they don't care about get filed without processing.

### Step 5 — Write config.md

```md
# Reading Digest Config

## Sources
gmail_newsletters: true
pocket: false
manual_queue: true

## Topics I care about
[list from user]

## Topics to skip
[list from user]

## Digest style
narrative

## Delivery
day: Friday
time: 17:00
channel: [CHANNEL]
to: [TARGET]

## Queue limit
max items per digest: 10
if more: save overflow to next week
```

---

## Runtime flow

### 1. Collect this week's reading

Pull from all configured sources.
Apply topic filter — skip items that don't match interests.
Deduplicate.
If more than 10 items: take the 10 most relevant, defer rest.

### 2. Process each item

For each item:
- Fetch full content (web_fetch)
- Extract: main argument, key ideas, notable data or quotes
- Assess: is this worth reading in full, or is the digest enough?
- Rate: skip (nothing new) / skim (one good idea) / read (genuinely worth the full article)

### 3. Build the digest

**📚 Reading Digest — [DATE]**
[N] items · ~[X] minutes to read this digest

---

**[ARTICLE TITLE]** — [SOURCE]
[One sentence: the main point]
[One sentence: why it matters or what's interesting about it]
*The idea:* [one concrete takeaway]
[Read in full →] (link) — or — *Digest is enough.*

---

Repeat for each item.

**Also this week — not worth your time:**
• [ITEM] — [one sentence on why it's skippable]
• [ITEM]

**Deferred to next week:**
[N] items saved for next digest.

---

### 4. Update archive.md

Log each processed item with date and one-line summary.
This builds a searchable record of what's been read.

---

## On-demand processing

`/read [url]` — process a single article immediately, outside the weekly digest.
Returns: main point, key idea, read or skip verdict.

---

## Management commands

- `/read [url]` — process one article now
- `/read add [url]` — add to queue for next digest
- `/read list` — show current queue
- `/read now` — run the digest immediately
- `/read skip [url]` — remove from queue without processing
- `/read topics` — show and update topic filter
- `/read search [query]` — search archive.md for past items

---

## What makes it good

The "skip" verdict is as valuable as the summary.
Knowing something wasn't worth your time — and why — is useful.

The one-idea-per-item format beats full summaries.
Reading is about acquiring ideas, not completing articles.

The archive builds something genuinely valuable over time.
After 6 months it's a searchable personal knowledge base.
