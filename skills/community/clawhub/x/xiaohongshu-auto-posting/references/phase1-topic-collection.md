# Phase 1 Reference — Pain-Point Topic Collection

## TOC

- §1 Keyword Rotation
- §2 XHS Search Execution
- §3 Field Extraction (Listing Pass → Selective Deep)
- §4 Engagement Scoring & Top 5
- §5 Deduplication & Filter Rules
- §6 MD Report Template
- §7 SELECTED_TOPICS Data Structure

---

## §1 Keyword Rotation

Keyword pool at `workspaces/xhs-posting/config/keywords.json`:

```json
{
  "product": "<product name>",
  "keywords": [{"keyword": "<keyword>", "note": "<note>"}],
  "rotation": "sequential",
  "last_index": 0
}
```

Fetch the next keyword:

1. Read `workspaces/xhs-posting/config/keywords.json`
2. `kw = keywords[last_index % len(keywords)]`
3. Show user: `Next keyword: "{kw.keyword}" (#last_index+1 of N)`
4. After user confirms: `last_index = (last_index + 1) % len(keywords)`, write back to `workspaces/xhs-posting/config/keywords.json`
5. User may manually input a keyword (does not advance last_index)

---

## §2 XHS Search Execution

### Search URL

```
https://www.xiaohongshu.com/search_result?keyword=<url-encoded-kw>&source=web_explore_feed
```

The `sort=popularity_descending` URL parameter does not work via POST body — must click the "最热" (Hottest) tab via UI:

```bash
browser-act --session $SESSION navigate "<search_url>"
browser-act --session $SESSION wait stable
# Find "最热" button index from state then click
browser-act --session $SESSION state
browser-act --session $SESSION click <hot_tab_index>
browser-act --session $SESSION wait stable
browser-act --session $SESSION screenshot "workspaces/xhs-posting/<date>/topics/screenshots/search.png"
```

### Capture Structured Data from Network Requests

After searching, capture structured response from network (no need to click into each note):

```bash
browser-act --session $SESSION network requests --filter "search/notes" --type xhr,fetch
browser-act --session $SESSION network request <request_id>
```

Response body `data.items` field reference:

| Field | Meaning |
|-------|---------|
| `id` | Note ID |
| `display_title` / `note_card.display_title` | Note title |
| `note_card.interact_info.liked_count` | Like count |
| `note_card.interact_info.collected_count` | Collect count |
| `note_card.interact_info.comment_count` | Comment count |
| `note_card.desc` | Body excerpt |

Note URL format: `https://www.xiaohongshu.com/explore/<note_id>`

If `search/notes` request doesn't appear (pure SSR case), fall back to:
```bash
browser-act --session $SESSION get markdown
```
Parse note card info from the markdown text.

---

## §3 Field Extraction (Two Steps)

### Step 1 — Listing Pass (from search API response, no click needed)

Parse 10–15 candidate notes' shallow fields from `network request` response JSON:

```yaml
NOTE_<N>:
  note_id: "<id>"
  title: "<display_title>"
  url: "https://www.xiaohongshu.com/explore/<id>"
  likes: <int>
  collects: <int>
  comments: <int>
  snippet: "<desc first 100 chars>"
  posted_at: "<timestamp converted to YYYY-MM-DD>"
```

### Step 2 — Selective Deep (click into Top 5 only)

Navigate to each of the Top 5 and read deep fields from `window.__INITIAL_STATE__`:

```bash
browser-act --session $SESSION navigate "https://www.xiaohongshu.com/explore/<note_id>"
browser-act --session $SESSION wait stable
browser-act --session $SESSION eval "JSON.stringify(window.__INITIAL_STATE__?.note?.noteDetailMap)"
```

Extract from `noteDetailMap[note_id]`:

```yaml
NOTE_<N> (deep):
  key_quote: "<verbatim quote representing the core pain point, ≤120 chars>"
  pain_description: "<1-2 sentences summarizing the user's problem>"
  tools_tried: ["<attempted solution 1>", "..."]
  solved: true | false | "partial"
  tags: ["<topic tag 1>", "..."]    # tagList[].name
  top_comments_theme: "<what readers most ask about, 1 sentence>"
```

`key_quote` must be verbatim from the original post, no paraphrasing. `solved` is determined by whether the body/comments describe a definitive resolution.

If `__INITIAL_STATE__` is empty (React hydration not complete), wait 2s then retry eval; if still failing fall back to `get markdown` to extract from page text.

---

## §4 Engagement Scoring & Top 5

```
score = likes + collects × 2 + comments × 1.5
```

Sort by score descending, apply §5 filters, take top 5 for Step 2.

**Tie-break**: among equal scores, prefer notes whose snippet contains unsolved signals like "don't know how to" / "keeps erroring" / "help needed" / "failed".

---

## §5 Deduplication & Filter Rules

From the 10–15 candidates, skip notes where:

- Title contains obvious ad words ("DM me" / "limited time" / "flash sale" / "recruit" / "group buy" / "click link")
- `posted_at` is more than 3 months ago (XHS content ages fast, author likely inactive)
- `snippet` is empty and `likes < 50` (insufficient content quality)
- `note_id` title has high overlap (Jaccard similarity > 0.6) with titles already in `workspaces/xhs-posting/tracking/published.json`

---

## §6 MD Report Template

Output path: `workspaces/xhs-posting/<YYYY-MM-DD>/topics/TOPICS_<keyword-slug>.md`

```markdown
# Topic Collection Report — <SEARCH_KEYWORD>

- Date: <YYYY-MM-DD>
- Source: Xiaohongshu (site-wide search, sorted by hottest)
- Candidates: <N total> → after filtering <M> → deep-extracted Top 5
- Search URL: <search_url>

## Top 5

### ① [<title>](<url>)
- Engagement: ❤️ <likes> · ⭐ <collects> · 💬 <comments> · Score <score>
- Posted: <posted_at>
- Pain point: <pain_description>
- Key quote: > "<key_quote>"
- Tried: <tools_tried>
- Status: <solved>
- Comment theme: <top_comments_theme>
- Topic tags: <tags>

### ② ...
### ⑤ ...

## Other Candidates (not in Top 5)

| # | Title | Score | URL |
|---|-------|-------|-----|
| 6 | ... | ... | ... |
```

After showing Top 5, ask:

```
These are the Top 5 topics. Which ones do you want to write?
(enter numbers like "1 3"; "all" for all; "skip" to pass today)
>
```

---

## §7 SELECTED_TOPICS Data Structure

Write to `workspaces/xhs-posting/<date>/selected_topics.json`:

```json
[
  {
    "note_id": "...",
    "title": "...",
    "url": "https://www.xiaohongshu.com/explore/...",
    "score": 142,
    "key_quote": "...",
    "pain_description": "...",
    "tools_tried": ["..."],
    "solved": false,
    "tags": ["..."],
    "top_comments_theme": "...",
    "selection_rank": 1,
    "publish_strategy": "immediate"
  }
]
```

`publish_strategy`: `"immediate"` (publish now) or `"draft"` (save draft without publishing)
