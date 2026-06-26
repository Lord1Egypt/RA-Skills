---
name: youtube-intelligence-extractor
description: |
  Extract structured intelligence from YouTube video transcripts for productivity,
  AI prompting, platform engineering, and creative workflows. Use this skill whenever
  the user shares a YouTube URL or video ID and wants to extract value from the content including
  todos, action items, AI prompts, advice, frameworks, tools, quotes, and
  platform/engineering insights. Triggers on: get the transcript, extract ideas from
  this video, pull the todos, what prompts does this use, summarize this YouTube
  video for me, what can I learn from this video, extract the advice, pull
  insights from, or any time a YouTube link is shared with intent to learn or act.
  Also triggers when the user pastes a raw transcript and asks Claude to extract value.
  Do NOT use for podcasts (non-YouTube), general web articles, or when the user only
  wants a basic summary with no actionable extraction.
---

# YouTube Intelligence Extractor

## Overview

This skill turns YouTube video transcripts into structured, actionable intelligence
across four domains that matter to Chibitek Labs: productivity, AI prompting,
platform/systems engineering, and creative building. Instead of passive
consumption, every video becomes a reusable asset — extracted todos, prompts you can
run immediately, frameworks you can apply, and insights mapped to your current work.

After presenting the report, always save it as a markdown file and present it to the
user. This is standing behavior — do not wait to be asked.

## Quick Reference

| Situation | Approach |
|-----------|----------|
| User gives a YouTube URL | Try Method A (Wave Tube fetch) → fallback to Method B (python) → fallback to Method C (manual paste) |
| User pastes raw transcript | Skip fetch, go straight to extraction pipeline |
| Python fetch is IP-blocked | Use Wave Tube web fetch — it works from server environments |
| Video has no captions | Attempt auto-generated captions; if unavailable, notify user |
| User wants one specific domain | Run full pipeline, present only the requested domain |
| User wants everything | Run full pipeline, present all four intelligence reports |
| Very long video (1hr+) | Chunk transcript, process in sections, merge outputs |
| Report is complete | Always save as markdown file and present_files — do not ask |

## Step 1: Fetch the Transcript

### Method A — Wave Tube (preferred — works from server/cloud environments)

Wave Tube mirrors YouTube transcripts and is not IP-blocked. Always try this first.

**URL pattern:** `https://tube.wave.co/[video-slug]-[VIDEO_ID]`

To find the slug: search "[VIDEO_ID] youtube" — the Wave Tube result will appear.
Or web_search for the video title + video ID; Wave Tube typically appears in results.

Use the `web_fetch` tool on the Wave Tube URL. The full transcript appears in the page
body under "## Transcript". Also captures: title, channel, views, duration,
description, and timestamps in the same fetch.

**Why Wave Tube first:** youtube-transcript-api fails with IpBlocked when Claude runs
on cloud infrastructure (AWS/GCP/Azure). Wave Tube is a reliable public mirror that
bypasses this entirely and also provides video metadata in the same fetch.

### Method B — Python (works locally on macOS, fails in server environments)

```bash
pip install youtube-transcript-api --break-system-packages -q
```

```python
from youtube_transcript_api import YouTubeTranscriptApi
import re

def extract_video_id(url):
    patterns = [
        r'(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'(?:embed/)([a-zA-Z0-9_-]{11})',
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return url  # assume it's already a video ID

# IMPORTANT: Use instance method .fetch(), NOT .get_transcript()
# The API changed in v1.0+ — always instantiate first
video_id = extract_video_id("VIDEO_URL_HERE")
transcript = YouTubeTranscriptApi().fetch(video_id)
full_text = " ".join([entry.text for entry in transcript])
print(full_text)
```

**Common mistake:** `YouTubeTranscriptApi.get_transcript()` no longer exists in v1.0+.
Always use `YouTubeTranscriptApi().fetch(video_id)` — instantiated, not class method.

### Method C — Manual paste (always works, zero dependencies)

If both automated methods fail, ask the user to:

1. Go to the YouTube video
2. Click the ... menu → Show transcript
3. Copy all the transcript text
4. Paste it directly into the chat

Then proceed with the extraction pipeline on the pasted text.

## Step 2: Run the Extraction Pipeline

Once you have the transcript text, extract across all four domains. Each domain is
independent — process them cleanly and present them in sequence.

### Domain 1 — Todos & Action Items

Extract concrete, doable actions mentioned or implied in the video.

**Output format:**

```markdown
## ✅ Todos & Action Items
- [ ] [Specific action] — [context, tool, or condition if mentioned]
```

**Rules:**
- Every item must be specific enough to act on without watching the video
- Include tool names, URLs, timeframes where mentioned
- Do NOT include vague advice ("learn more about X") — skip it or make it concrete

### Domain 2 — Advice & Frameworks

Extract principles, mental models, frameworks, and strategic advice that apply
repeatedly — not just one-time instructions.

**Output format:**

```markdown
## 💡 Advice & Frameworks

### [Framework Name]
**The idea:** ...
**Why it matters:** ...
**How to apply it:** ...
```

### Domain 3 — AI Prompts (Extractable & Ready to Use)

Extract any AI prompts, prompt strategies, or prompt patterns mentioned, shown,
or implied. Reconstruct them as runnable prompts — not descriptions of prompts.

**Output format:**

```markdown
## 🤖 AI Prompts & Techniques

### [Technique Name]
**Purpose:** [What this achieves]
**Prompt:**
```
[Full, ready-to-run prompt text in a fenced code block]
```
**Notes:** [Model, context, or usage tips]
```

**Rules:**
- If a prompt is partially shown, reconstruct the most likely complete version
- Format prompts in fenced code blocks so they are easy to copy
- Never just describe a prompt — always write the actual text

### Domain 4 — Platform, Engineering & Creative Insights

Extract anything relevant to systems design, platform architecture, tooling,
development workflows, APIs, infrastructure patterns, or creative production.

**Output format:**

```markdown
## ⚙️ Platform, Engineering & Creative Insights

### [Insight Name]
**Domain:** [Engineering / Platform / Creative / Tooling]
**Insight:** ...
**Application for Chibitek/UAMH:** [How this maps to UAMH, STIKI, Nexus, or OpenClaw]
```

**Rules:**
- Always include the Chibitek/UAMH application note — generic insights are less useful
- If an insight maps to multiple Chibitek systems, name them all

## Step 3: Present the Intelligence Report

### Report Header (always include)

```markdown
# 🎬 Intelligence Report: [VIDEO TITLE]
**Channel:** [Channel Name]
**Published:** [Date] · [Duration] · [View count]
**Topic:** [2-3 word tag]
**Source:** [Full YouTube URL]
**Summary:** [One sentence: what this video teaches and who it's for]

---
```

### Report Footer (always include)

```markdown
## 🏆 Top 3 Immediate Actions
1. [Highest-leverage action from the report]
2. [Second most valuable]
3. [Third]

---
*Extracted by Chibitek Labs YouTube Intelligence Extractor · [Date]*
```

## Step 4: Save the Report (Always — Do Not Wait to Be Asked)

After presenting the report in chat, immediately save it as a markdown file and
present it using present_files. This is standing behavior.

**File naming convention:**
```
intel-[short-slug-from-title].md
```
Example: `intel-openclaw-5-things.md`

**Save location:** `/mnt/user-data/outputs/` (or appropriate workspace output dir)

Every video intelligence report is a reusable asset. Saving automatically means
the output is never lost when the chat session ends.

## Step 5: Update This Skill After Every Improvement

After any run that reveals a better approach, edge case, or new pattern, update
this SKILL.md immediately. Do not wait to be asked. This is standing behavior.

**What counts as an improvement worth capturing:**
- A fetch method that worked better than expected
- A new transcript source discovered
- An output format tweak that made the report cleaner
- A new anti-pattern encountered in the wild
- A domain or extraction type that proved more or less useful than expected

## Common Mistakes (Anti-Patterns)

**Trying Python fetch first in server environments**
The youtube-transcript-api library is always IP-blocked when Claude runs on cloud
infrastructure. Go to Wave Tube first — it is faster and more reliable in this context.

**Using the old class method API**
`YouTubeTranscriptApi.get_transcript()` throws AttributeError in v1.0+.
Use `YouTubeTranscriptApi().fetch(video_id)` — instantiated instance, not class method.

**Summarizing instead of extracting**
Do not write a paragraph about what the video covers. Extract discrete, usable pieces.
A summary is what YouTube's description does. This skill does more.

**Vague action items**
Bad: `- [ ] Learn more about AI prompting`
Good: `- [ ] Try reverse prompting: ask OpenClaw to extract your goals by asking you questions`

**Paraphrasing prompts instead of reconstructing them**
If a speaker reads a prompt aloud or shows it on screen, write the actual prompt text
in a fenced code block — ready to copy and run. Never just describe it.

**Skipping the Chibitek mapping in Domain 4**
Generic engineering insights are half as useful as ones mapped to UAMH, STIKI, or Nexus.
Always close the loop on how the insight applies to Chibitek's current work.

**Not saving the report automatically**
The report is a reusable asset. Save it every time without being asked.

**Not updating the skill after improvements**
If this run taught you something new, update the skill before ending the session.

## Quality Checklist

Before closing out a run, verify:
- [ ] Transcript was fetched (Wave Tube preferred, Python fallback, manual last resort)
- [ ] Report header includes: title, channel, date, duration, views, source URL, summary
- [ ] All four domains are present (unless user requested a subset)
- [ ] Action items are specific and immediately actionable
- [ ] At least one AI prompt is reconstructed as a full, runnable prompt in a code block
- [ ] Every Domain 4 insight has a Chibitek/UAMH application note
- [ ] Top 3 immediate actions are surfaced in the footer
- [ ] Report was saved as a markdown file and presented via present_files
- [ ] Skill was updated if any improvements were discovered this run

## Dependencies

Wave Tube (Method A) requires no installation — use the `web_fetch` tool directly.

```bash
pip install youtube-transcript-api --break-system-packages  # Method B only
pip install yt-dlp --break-system-packages                  # Optional fallback
```

## Chibitek Context Notes

This skill is designed around Erick's four priority domains:
- **Productivity:** todos, systems, habits, workflows
- **AI Prompting:** extractable, runnable, copy-paste-ready prompts
- **Platform Engineering:** architecture, tooling, infra, APIs, agent design
- **Creating:** design, content, product, creative workflows

When insights span multiple domains, list them in all applicable sections.
Always map Domain 4 insights back to UAMH, STIKI, Nexus, or OpenClaw specifically.

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-04-07 | Initial skill created |
| 1.1 | 2026-04-07 | Added Wave Tube as primary fetch method (IP block fix), corrected YouTubeTranscriptApi v1.0+ syntax (.fetch() not .get_transcript()), added auto-save as standing behavior, added skill self-update rule, added changelog |
