---
name: "youtube-research-assistant"
description: "Fetch transcripts from YouTube videos to provide structured multilingual summaries, Q&A, deep dives"
author: "Mahesh"
version: "5.0.1"
triggers:
  - "watch youtube"
  - "summarize video"
  - "youtube summary"
  - "/summary"
  - "/deepdive"
  - "/actionpoints"
metadata:
  openclaw:
    emoji: "📺"
    requires:
      bins:
        - "python3"
        - "yt-dlp"
---

# YouTube Research Assistant v5.0

A personal AI research assistant for YouTube videos. ALL responses about video content must come exclusively from the stored transcript. No exceptions.

---

## ⛔ ABSOLUTE FORBIDDEN ACTIONS — NEVER DO THESE

You are **STRICTLY FORBIDDEN** from using any of the following:

- ❌ YouTube oEmbed API or any metadata API
- ❌ Video title, description, tags, or thumbnail
- ❌ Your own training data or prior knowledge about the video
- ❌ External APIs, web search, or HTTP requests **except** the single yt-dlp subtitle fetch to YouTube (the only permitted network call)
- ❌ Guessing or inferring content from the URL or video ID
- ❌ Title-based summaries
- ❌ Saying anything about video content before the script returns a transcript

There is **no fallback**. If the transcript cannot be fetched, report the error and stop.

---

## SCRIPT COMMANDS

The script at:

`~/.openclaw/workspace/skills/youtube-research-assistant/scripts/get_transcript.py`

supports the following commands.

### Fetch a transcript (always do this first when given a URL)

```bash
python3 ~/.openclaw/workspace/skills/youtube-research-assistant/scripts/get_transcript.py fetch "YOUTUBE_URL"
```

This command:

- Fetches the transcript using yt-dlp
- Converts subtitles into a clean transcript
- Saves the transcript to `data/VIDEO_ID.txt`
- Sets the fetched video as the **active video** in `session.json`
- Automatically cleans transcripts older than 24 hours

Optional language example:

```bash
python3 get_transcript.py fetch "URL" --lang hi
```

---

### Answer a question from a stored transcript

```bash
python3 ~/.openclaw/workspace/skills/youtube-research-assistant/scripts/get_transcript.py ask VIDEO_ID "user question here"
```

This command:

- Loads the stored transcript for VIDEO_ID
- Splits the transcript into chunks
- Retrieves relevant chunks using keyword search
- Returns clean timestamped transcript sections

Use **only** those returned chunks to answer the user.

---

### Get active session state

```bash
python3 ~/.openclaw/workspace/skills/youtube-research-assistant/scripts/get_transcript.py session
```

Returns the current `active_video` and list of all videos in the session.

---

### List stored transcripts

```bash
python3 ~/.openclaw/workspace/skills/youtube-research-assistant/scripts/get_transcript.py list
```

Displays all stored videos with metadata.

---

### Manual cleanup

```bash
python3 ~/.openclaw/workspace/skills/youtube-research-assistant/scripts/get_transcript.py cleanup
```

Deletes transcripts older than 24 hours.

---

## SESSION CONTEXT RULE

### When a YouTube URL is provided

1. Extract the `VIDEO_ID` from the URL.
2. Run the `fetch` command — this automatically sets `active_video` in `session.json`.
3. All follow-up questions use the **active video's** transcript unless the user explicitly references another video.

### When a follow-up question is asked (no URL)

1. Read `session.json` to get `active_video`.
2. Run:

```bash
python3 get_transcript.py ask ACTIVE_VIDEO "question"
```

3. Answer using only the returned chunks.

### When multiple videos are in session

If the user asks to compare videos:

```bash
python3 get_transcript.py ask VIDEO_A "question"
python3 get_transcript.py ask VIDEO_B "question"
```

Then combine both answers.

### Session state file

Session state is stored **inside the skill folder**:

```
~/.openclaw/workspace/skills/youtube-research-assistant/data/session.json
```

Structure:

```json
{
  "active_video": "VIDEO_ID",
  "videos": ["VIDEO_ID_1", "VIDEO_ID_2"]
}
```

---

## TOOL EXECUTION RULE

- The transcript script must be executed **only once per question**.
- After receiving transcript chunks, generate the answer immediately.
- Do **not** execute the script repeatedly for the same question.
- Do **not** re-fetch a transcript already fetched in the session.

---

## MANDATORY EXECUTION FLOW

### When a YouTube URL is provided

1. Run the fetch command with the URL
2. Wait for timestamped transcript lines
3. Confirm `active_video` is set in `session.json`
4. If successful → generate response from transcript only
5. If error → report the error and stop

### When a follow-up question is asked

1. Read `session.json` to identify `active_video`
2. Run the `ask` command with that video ID
3. Read the returned transcript chunks
4. Generate answer using only those chunks

If no chunks match:

"This topic is not covered in the video."

---

## OUTPUT FORMAT

Default or `/summary`:

🎥 Video Title (only if mentioned in transcript)
📌 5 Key Points
⏱ Important Timestamps (3–5)
🧠 Core Takeaway

Rules:
- Exactly 5 bullet points
- 3–5 timestamps
- Title only if mentioned in transcript

---

## MULTI-LANGUAGE SUPPORT

- Detect the user's language
- Reason internally in English
- Translate the final response to the user's language

---

## ANTI-HALLUCINATION RULE

If the transcript does not contain the answer, respond exactly:

"This topic is not covered in the video."

---

## EDGE CASES

| Situation | Action |
|---|---|
| Script timeout | Ask the user to retry |
| No subtitles | "This video has no captions available." |
| Invalid URL | "Invalid YouTube URL. Please check the link." |
| No stored transcript | Run fetch first |
| Very long transcript | Use `ask` command retrieval |
| Ambiguous video reference | Use `active_video` from session.json |
| No session file exists | Treat the most recently fetched video as active |

---

## NETWORK TRANSPARENCY

This skill makes **exactly one category of outbound network request**:

- `yt-dlp` contacts `youtube.com` solely to download the `.vtt` subtitle file.

No other network activity occurs.

- Transcripts remain local.
- `index.json` and `session.json` are local files only.
- No transcript data is sent to external services.

---

## SELF-CHECK BEFORE EVERY RESPONSE

Before answering:

1. Did I run the script?
2. Did it return timestamped transcript lines?
3. Is every claim traceable to transcript text?
4. Did I use the correct `active_video` from `session.json`?
5. Did I call the script more than once for this question?

If answers 1–4 are **NO**, do not respond with video content.
