# Phase 6 Reference — Performance Tracking

## TOC

- §1 Standalone Trigger Recognition
- §2 6.1 Single Post 24h Tracking
- §3 6.2 Batch Data Collection
- §4 6.3 View New Comments & Reply
- §5 6.4 Generate Report
- §6 Local Storage Structure
- §7 Reply Copy Guidelines

---

## §1 Standalone Trigger Recognition

When entering the Skill, if the user's first message matches the following triggers, **jump directly to the corresponding sub-action** without going through Phase 0–5:

| Trigger | Sub-action |
|---------|------------|
| "track performance" / "see data" / "data collection" | 6.2 Batch collection |
| "view comments" / "any new comments" / "reply comments" | 6.3 Comment reply |
| "generate report" / "performance report" / "view report" | 6.4 Generate report |

Still need to complete Phase 0.2 (read session_state.json) and Phase 0.5 (browser login check) first.

---

## §2 6.1 Single Post 24h Tracking

**Trigger**: automatically scheduled after Phase 5 successful publish, once note_id is captured (execute 24h later).

**Steps**:

```bash
browser-act --session $SESSION navigate "https://creator.xiaohongshu.com/new/home"
browser-act --session $SESSION wait stable
browser-act --session $SESSION network requests --filter "datacenter/note/base" --type xhr,fetch
```

If the page doesn't auto-trigger that request, manually navigate to data center and capture:

```bash
browser-act --session $SESSION navigate "https://creator.xiaohongshu.com/creator/note"
browser-act --session $SESSION wait stable
browser-act --session $SESSION network requests --filter "datacenter/note/base?note_id=<target_note_id>" --type xhr,fetch
```

If there's no request with `note_id` param, construct the request URL directly (API doesn't need XS signature, browser session already has cookies):

```bash
browser-act --session $SESSION eval "
fetch('/api/galaxy/creator/datacenter/note/base?note_id=<note_id>', {
  headers: {'Accept': 'application/json'}
}).then(r=>r.json()).then(d=>JSON.stringify({
  likes: d.data?.like_count,
  collects: d.data?.collect_count,
  comments: d.data?.comment_count,
  views: d.data?.view_count,
  shares: d.data?.share_count
}))
"
```

Extract `like_count / collect_count / comment_count / view_count`, update to the `tracking` field of the corresponding record in `published.json`.

---

## §3 6.2 Batch Data Collection

Read all records from `published.json` where `status=published` and `tracking.last_checked` is over 24h ago (or null), collect each one:

```bash
browser-act --session $SESSION navigate "https://creator.xiaohongshu.com/creator/note"
browser-act --session $SESSION wait stable
browser-act --session $SESSION network requests --filter "note_detail_new" --type xhr,fetch
browser-act --session $SESSION network request <request_id>
```

Response body `data.seven` (last 7 days) contains:

| Field | Meaning |
|-------|---------|
| `view_count` | Total views |
| `like_count` | Total likes |
| `collect_count` | Total collects |
| `comment_count` | Total comments |
| `share_count` | Total shares |
| `rise_fans_count` | New followers gained |

**Precise data for a single note** (query by note_id):

```
GET https://creator.xiaohongshu.com/api/galaxy/creator/datacenter/note/base?note_id=<id>
```

Batch collection flow:
1. Read all records pending update from `published.json`
2. For each record, call the above fetch via eval
3. Update `tracking.likes_latest / collects_latest / comments_latest / views_latest / last_checked`
4. Summarize changes: `delta_likes = latest - 24h_baseline`
5. Print change summary

After collection, output:
```
Data collection complete (<N> notes):

| Title | Likes | Collects | Comments | Views |
|-------|-------|----------|----------|-------|
| <title> | <likes> (+<delta>) | ... | ... | ... |
```

---

## §4 6.3 View New Comments & Reply

**Steps**:

1. Read the URL list of notes published in the last 7 days from `published.json`

2. For each URL:
   ```bash
   browser-act --session $SESSION navigate "https://www.xiaohongshu.com/explore/<note_id>"
   browser-act --session $SESSION wait stable
   browser-act --session $SESSION eval "
   JSON.stringify((window.__INITIAL_STATE__?.comment?.commentMap || {}))
   "
   ```
   Or extract comment list via `get markdown`.

3. Identify **substantive comments** (filter out "great" / "noted" / "saved" type single-word reactions):
   - Question type: contains "how" / "can it" / "does it support"
   - Sharing type: contains "me too" / "tried it" / "encountered this"
   - Help-seeking type: contains "please help" / "don't know how"

4. Draft replies for each substantive comment (see §7 copy guidelines), **show all drafts at once**:

```
Pending replies (<N>):

#1 Note: <title>
  Original comment: <comment_text>
  Draft reply: <draft_reply>

#2 Note: <title>
  ...

✓ all — send all
△ edit <N> <new content> — edit one
✗ skip <N> — skip one
```

5. After user approval, for approved replies:
   ```bash
   browser-act --session $SESSION navigate "<comment_permalink>"
   browser-act --session $SESSION state
   # Find "Reply" button
   browser-act --session $SESSION click <reply_btn_index>
   browser-act --session $SESSION input <textarea_index> "<approved_reply>"
   browser-act --session $SESSION screenshot "workspaces/xhs-posting/<date>/replies/reply_<n>.png"
   browser-act --session $SESSION click <submit_btn_index>
   browser-act --session $SESSION wait stable
   ```

**Gate**: no reply may be sent without user approval.

---

## §5 6.4 Generate Report

Read `workspaces/xhs-posting/tracking/published.json`, generate Markdown report:

```markdown
# Xiaohongshu Operations Report — <YYYY-MM-DD>

## Overview
- Published notes: <N>
- Total views: <sum_views>
- Total likes: <sum_likes>
- Total collects: <sum_collects>
- Average likes/post: <avg_likes>

## Top 5 Best Performing Notes

| Title | Published | Likes | Collects | Comments | Views |
|-------|-----------|-------|----------|----------|-------|
| ... | ... | ... | ... | ... | ... |

## Keyword Performance Comparison

| Keyword | Posts | Avg Likes | Avg Collects |
|---------|-------|-----------|--------------|
| ... | ... | ... | ... |

## Recommendations
- Best posting time: <inferred from data>
- Most effective topic tags: <top 3>
- Recommended keywords for next cycle: <based on performance>
```

Report output path: `workspaces/xhs-posting/reports/report_<YYYY-MM-DD>.md`

---

## §6 Local Storage Structure

All paths are relative to the **user's working directory (CWD)**, not inside the Skill directory:

```
workspaces/xhs-posting/           ← relative to user CWD
├── session_state.json             # account config, last post time
├── config/
│   └── keywords.json              # keyword pool
├── tracking/
│   └── published.json             # all published note records (with tracking fields)
├── reports/
│   └── report_<date>.md           # periodically generated performance reports
└── <YYYY-MM-DD>/
    ├── topics/
    │   ├── TOPICS_<kw>.md         # topic collection report
    │   └── screenshots/           # search screenshots
    ├── selected_topics.json       # user-selected topics
    ├── style_fingerprint.json     # style fingerprint
    ├── drafts/
    │   └── <topic_id>/
    │       ├── draft.md           # draft content (title + body + tags)
    │       ├── pre_publish.png    # pre-publish screenshot
    │       └── meta.json          # publish metadata
    └── replies/
        └── reply_<n>.png          # reply screenshot archive
```

`published.json` array structure:

```json
[
  {
    "note_id": "...",
    "title": "...",
    "url": "https://www.xiaohongshu.com/explore/...",
    "published_at": "2026-04-30 14:30",
    "keyword": "keyword used",
    "source_topic_url": "...",
    "status": "published",
    "tracking": {
      "likes_24h": 5,
      "collects_24h": 2,
      "comments_24h": 1,
      "views_24h": 120,
      "likes_latest": 23,
      "collects_latest": 8,
      "comments_latest": 3,
      "views_latest": 456,
      "last_checked": "2026-05-01 10:00"
    }
  }
]
```

---

## §7 Reply Copy Guidelines

- **Match user's language** (Chinese for XHS audience by default)
- **Non-promotional tone** — like helping a peer in the same field
- **Short**: reply ≤ 3 sentences
- Useful info first: specific command / specific number / product docs link
- **Prohibited**: DM / add WeChat / QR code
- **Allowed**: reference `install_cmd` from session_state.json (if available) / `{product.url}` docs link / specific operation steps
- Don't hype the product — just describe results that can actually be reproduced
- Be honest about bugs / limitations, no defensive deflection
