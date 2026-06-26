---
name: youtube-notes
description: Convert any YouTube video into clean, structured markdown notes — steps, tools, timestamps, and parts lists. Use when a user shares a YouTube link and asks you to summarize it, extract the steps, or take notes on it. Requires a TranscriptAPI.com API key (free tier available). Outputs formatted markdown directly to the user.
homepage: https://transcriptapi.com
metadata: {"openclaw":{"requires":{"env":["TRANSCRIPT_API_KEY"]},"primaryEnv":"TRANSCRIPT_API_KEY"}}
---

# YouTube Notes

Fetches the transcript and description of any YouTube video and turns it into clean, structured markdown notes — tools, steps, timestamp links, and parts lists. No fluff.

Works great for:
- DIY / repair / how-to tutorials (tools, steps, torque specs)
- Educational videos (key points, sections, timestamps)
- Any video you want to reference later without rewatching

---

## Setup

This skill requires a **TranscriptAPI.com** API key (`TRANSCRIPT_API_KEY`). TranscriptAPI handles YouTube's anti-scraping protections via residential proxies. Free tier: 100 transcripts/month, no credit card required.

If the user hasn't provided a key yet, tell them:
> "To fetch YouTube transcripts I need a TranscriptAPI.com API key. It's free — sign up at transcriptapi.com, copy your API key from the dashboard, and paste it here."

Store the key as `TRANSCRIPT_API_KEY` wherever your agent manages credentials.

---

## Workflow

### Step 1 — Extract the Video ID

From any YouTube URL:
- `https://www.youtube.com/watch?v=VIDEO_ID` → `VIDEO_ID` is after `v=`
- `https://youtu.be/VIDEO_ID` → `VIDEO_ID` is the path

### Step 2 — Fetch the Transcript

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/transcript?video_url=VIDEO_ID&format=json&include_timestamp=true&send_metadata=true" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Response includes:
- `transcript[]` — array of `{ text, start, duration }` where `start` is seconds from the beginning
- `metadata.title` — video title
- `metadata.author_name` — channel name

**Error codes:**
- `402` — out of credits. User needs to top up at transcriptapi.com.
- `404` — video not found or no transcript available (private video, no captions).
- `401` — API key invalid or expired. Ask the user to check their key.

### Step 3 — Fetch the Video Description

Use a web fetch on the video URL to get the description — it often contains parts lists, affiliate links, and creator-added timestamps (more reliable than auto-detected ones).

```bash
curl -s "https://www.youtube.com/watch?v=VIDEO_ID" -H "User-Agent: Mozilla/5.0"
```

**Look for:**
- Parts lists and product links
- Tool lists with model numbers or sizes
- Torque specs or measurements
- Timestamps the creator added themselves
- Related guides

### Step 4 — Analyze & Structure

Read the transcript for meaning — auto-generated transcripts have no punctuation. Skip `[Music]` tags, sponsor segments, and outro fluff.

**For tutorial/repair/how-to videos, extract:**
- Tools and materials (with sizes, specs, model numbers)
- Torque specs, measurements, part numbers
- Numbered steps in sequence
- Key moments worth timestamping

**For educational/informational videos, extract:**
- Main topic and key points
- Supporting data and natural section breaks

### Step 5 — Format Timestamp Links

Convert `start` seconds to `M:SS`:
- `minutes = Math.floor(seconds / 60)`
- `secs = String(seconds % 60).padStart(2, '0')`

Format:
```
⏱ Skip to M:SS — https://www.youtube.com/watch?v=VIDEO_ID&t=SECONDS
```

### Step 6 — Output the Notes

Deliver the structured markdown directly to the user. After outputting, ask:

> "Want me to save this somewhere? I can store it in Parchment, Notion, Google Docs, or as a local markdown file — just let me know."

If they say yes, use whatever tools and skills you have available to save it. That's outside the scope of this skill — just hand off the markdown.

---

## Output Templates

### Tutorial / Repair / How-To

```markdown
# VIDEO TITLE

**Source:** https://www.youtube.com/watch?v=VIDEO_ID
**Channel:** AUTHOR_NAME | Est. time: X min (if mentioned)

---

## Tools Needed
- Tool 1 (size/purpose)
- Tool 2

## Parts & Links
- Part Name — https://link.to/part

## Torque Specs / Measurements
- Spec: value

---

## Steps

### 1. Step Name
Clear, concise description of what to do.
⏱ Skip to M:SS — https://www.youtube.com/watch?v=VIDEO_ID&t=SECONDS

### 2. Step Name
...
```

### Educational / Informational

```markdown
# VIDEO TITLE

**Source:** https://www.youtube.com/watch?v=VIDEO_ID
**Channel:** AUTHOR_NAME

---

## Key Points
- Point 1
- Point 2

---

## Notes

### Section Title
Summary of this section.
⏱ Skip to M:SS — https://www.youtube.com/watch?v=VIDEO_ID&t=SECONDS
```

---

## Tips

- Auto-generated transcripts have no punctuation — read for meaning, not literally
- Creator-added timestamps in the description are more meaningful than auto-detected ones
- Skip the outro (brand plugs, subscribe reminders) — it's not useful content
- Keep steps concise — this is a reference card, not a transcript
- 1 TranscriptAPI credit = 1 fetch. Free tier = 100/month.
- Some videos have no transcript (private, no captions). Tell the user and offer to summarize from the title/description only.
