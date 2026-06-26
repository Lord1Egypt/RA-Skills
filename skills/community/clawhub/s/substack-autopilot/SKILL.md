---
name: substack-autopilot
description: Automate Substack newsletter article drafting and publishing using OpenClaw native tools. Generate weekly articles from a topic queue, write brand-consistent long-form content, save drafts locally, open Substack in browser for final review, and notify via Telegram. Triggers on: "write this week's Substack", "generate Substack article", "automate newsletter", "draft Substack post", "weekly Substack".
---

# Substack Autopilot

Generate, draft, and prepare weekly Substack articles from a managed topic queue. Keeps a local article log and opens the browser for final human review before publishing.

## File Structure

```
<workspace>/<brand>/substack/
├── article-topics.json     — topic queue (see format below)
├── article-log.json        — published article history
└── article-YYYY-MM-DD.md   — generated draft files
```

## Topic Queue Format (`article-topics.json`)

```json
[
  {
    "id": 1,
    "title": "How Creators Are Losing Money Without Knowing It",
    "subtitle": "Platform fees, algorithm suppression, and what to do about it",
    "angle": "platform-critique",
    "used": false
  }
]
```

**Angle types:** See `references/article-angles.md` for content frameworks per angle.

## Weekly Article Generation Flow

1. **Pick next unused topic** from `article-topics.json` (first where `"used": false`)
2. **Generate article** — use angle framework from `references/article-angles.md`
3. **Quality check** — score ≥ 70/100 before proceeding (see scoring below)
4. **Save draft** to `article-YYYY-MM-DD.md`
5. **Mark topic as used** in `article-topics.json`
6. **Log article** to `article-log.json`
7. **Open browser** to Substack new post editor for final review
8. **Notify via Telegram** — "Draft ready at [path] — please review before publishing"

If all topics are used: notify user to add new topics, then exit.

## Article Quality Scoring (min 70/100)

| Criterion | Weight |
|-----------|--------|
| Hook strength (first paragraph) | 25 pts |
| Value density (actionable insights) | 25 pts |
| Brand consistency | 20 pts |
| CTA clarity | 15 pts |
| Structure / readability | 15 pts |

Rewrite once if below 70. Do not proceed if still failing after rewrite.

## Article Format

```markdown
# [Title]

[Subtitle / hook sentence]

---

[Body: 600–900 words]
[3–5 sections with H2 headers]
[Specific data, examples, or patterns — not vague claims]
[Final CTA: link to brand URL]
```

## Opening Substack in Browser

```
browser open → https://<publication>.substack.com/publish/post/new (profile: user)
```

Wait for editor to load before notifying user. Do not auto-publish — always leave final approval to the human.

## Cron Job Setup

**Recommended schedule:** Weekly, Wednesday UTC 13:00 (Stockholm 14:00)

```
schedule: { "kind": "cron", "expr": "0 13 * * 3", "tz": "UTC" }
sessionTarget: "isolated"
payload.kind: "agentTurn"
timeoutSeconds: 0
```

See `references/cron-prompt-template.md` for a ready-to-use agentTurn prompt.

## Telegram Notifications

- ✅ Draft ready: `"📝 Substack draft saved: [path] — please review and publish"`
- ⚠️ All topics used: `"⚠️ Substack topic queue empty — please add new topics to article-topics.json"`
- ❌ Generation failed: `"❌ Substack draft failed: [error] — manual write needed"`
