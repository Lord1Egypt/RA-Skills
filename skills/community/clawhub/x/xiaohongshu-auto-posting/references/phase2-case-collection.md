# Phase 2 Reference — Top Case Collection (Style Reference)

## Overview

Phase 2 **shares the same search results as Phase 1** — only the purpose differs: Phase 1 finds pain-point topics, Phase 2 collects writing styles from high-engagement notes to generate a Style Fingerprint for Phase 4 writing reference.

No additional search requests needed — take the top 3 high-engagement notes directly from Phase 1's search API response.

---

## §1 Case Selection Criteria

From the 10–15 candidates in Phase 1's Listing Pass, select the top 3 that meet:

- `likes + collects >= 200` (sufficient engagement, representative)
- Body has substantive content (not a pure image note, `snippet` not empty)
- Not published by an ad/brand account (regular user perspective is more valuable)

If fewer than 3 candidates qualify, take all that do.

---

## §2 Full-Text Extraction

For each of the selected 3 cases, navigate to the detail page to read full content:

```bash
browser-act --session $SESSION navigate "https://www.xiaohongshu.com/explore/<note_id>"
browser-act --session $SESSION wait stable
browser-act --session $SESSION eval "
(function() {
  const state = window.__INITIAL_STATE__;
  const detail = state?.note?.noteDetailMap;
  if (!detail) return JSON.stringify({error: 'no state'});
  const noteId = Object.keys(detail)[0];
  const note = detail[noteId];
  return JSON.stringify({
    title: note?.noteInfo?.title || '',
    desc: note?.noteInfo?.desc || '',
    tags: (note?.tagInfo?.tagList || []).map(t => t.name),
    likes: note?.interactInfo?.likedCount || 0,
    collects: note?.interactInfo?.collectedCount || 0,
    comments: note?.interactInfo?.commentCount || 0
  });
})()
"
```

---

## §3 Style Fingerprint Analysis

For each case note, analyze the following dimensions:

### 3.1 Title Pattern
- Character count (≤20 hard limit)
- Uses numbers ("3 methods" / "5 minutes")
- Uses question / exclamation ("?" / "!")
- Uses emoji (emoji at start of title)
- Pain-point type vs. how-to type vs. story type

### 3.2 Opening (first 50 chars of body)
- Question hook ("Have you ever encountered…")
- Scene immersion ("Last week when I was working on a project…")
- Conclusion first ("Using this tool saved me 3 hours")
- Number shock ("0 lines of code to achieve…")

### 3.3 Paragraph Structure
- Average paragraph length (XHS recommends 30–60 chars/paragraph)
- Paragraph frequency (blank line after each paragraph)
- Emoji density (0/1/multiple per paragraph)
- List usage (numbered 1. 2. 3. or bullet ·)

### 3.4 Topic Tag Strategy
- Number of tags (target 3–5)
- Tag type combination: generic + scene-specific + category
- Whether high-traffic topics are used (topics with > 100k likes)

### 3.5 Closing CTA
- Question type ("How do you usually handle this problem?")
- Save reminder ("Save this first, you'll definitely need it")
- Follow prompt ("Follow me for more tips")

---

## §4 Style Fingerprint Output Format

Write to `workspaces/xhs-posting/<date>/style_fingerprint.json`:

```json
{
  "generated_at": "<YYYY-MM-DD>",
  "keyword": "<search_keyword>",
  "sample_notes": [
    {
      "note_id": "...",
      "title": "...",
      "likes": 342,
      "collects": 156
    }
  ],
  "fingerprint": {
    "title": {
      "pattern": "pain-point",
      "avg_chars": 16,
      "use_numbers": true,
      "use_emoji": true,
      "example": "<title example extracted from collected case notes>"
    },
    "opening": {
      "style": "scene immersion",
      "example": "<opening example extracted from collected case notes>"
    },
    "body": {
      "avg_para_chars": 45,
      "emoji_density": "1 per paragraph",
      "use_list": true,
      "list_style": "numbered"
    },
    "tags": {
      "count": 4,
      "combo": ["generic", "scene-specific", "category", "brand"],
      "examples": ["<topic tag examples extracted from collected case notes>"]
    },
    "cta": {
      "style": "question + save",
      "example": "<CTA example extracted from collected case notes>"
    }
  }
}
```

---

## §5 Using the Style Fingerprint in Phase 4

Phase 4 writing must read this file and align with the fingerprint:

- Title format aligned with `fingerprint.title.pattern`
- Opening style references `fingerprint.opening.style`
- Paragraph length controlled within `fingerprint.body.avg_para_chars` ± 15 chars
- Topic tag combination references `fingerprint.tags.combo`
- Closing CTA references `fingerprint.cta.style`

Not mechanical copying — fill new topic content within the same style tone.
