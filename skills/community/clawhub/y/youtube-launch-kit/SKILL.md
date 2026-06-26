---
slug: youtube-launch-kit
name: YouTube Launch Kit
description: Turn a video topic, rough notes, or transcript into a complete YouTube launch package. Outputs two title variants, a keyword-optimized description with timestamped chapters, 10 tags, a pinned comment, a discussion seed (also known as first comment prompt or first pinned comment), an optional thumbnail prompt, and an optional 3-tweet promo set. Use when a creator pastes a video topic, outline, notes, or transcript and asks for a title, description, tags, launch copy, pinned comment, first comment prompt, discussion seed, thumbnail idea, or promo tweets for YouTube.
version: 1.0.0
license: MIT
tags:
  - youtube
  - content-creation
  - creator-tools
  - marketing
  - seo
  - video
  - launch-kit
metadata:
  openclaw:
    requires:
      env: []
      bins: []
---

# YouTube Launch Kit

Turn a video concept or recording into a complete launch package — titles, description, chapters, tags, pinned comment, discussion seed, and optional promo assets. One paste in, full launch out.

## When to use this skill

Trigger this skill when the user:
- Pastes a video topic, rough notes, or outline and asks for a title, description, or tags
- Shares a transcript and wants launch copy generated from it
- Says "write my YouTube description," "optimize my title," "what tags should I use," "write my pinned comment," "write a first comment prompt," "write a discussion seed," "give me a thumbnail prompt," or "help me launch this video"
- Asks for a full YouTube launch package or upload checklist
- Wants promo tweets or social copy for a YouTube video

Do NOT trigger for:
- Channel strategy or long-term content planning — out of scope
- Video editing notes or scripting (pre-production writing, not launch copy)
- Analytics review or performance diagnosis — separate skill

---

## Step 1 — Identify input state and collect what's missing

Determine which of three input states the user is in. Do not ask clarifying questions beyond what's listed below.

### State A: Topic + notes/outline (primary)
User has a concept and rough structure but hasn't recorded yet.

**Required:**
1. Video topic (one sentence describing what the video covers)
2. Notes or outline — bullet points, rough section order, key points to hit, anything they've planned

**Optional (use if provided, don't ask twice):**
3. Target audience (e.g., "beginners," "freelance designers," "new parents")
4. Channel niche or name
5. Tone — educational, entertaining, motivational, tutorial-focused (default: educational/tutorial)

If notes are missing and only a topic is provided, proceed as **State C** and note the limitation.

### State B: Transcript (fallback)
User has already recorded and has a transcript from auto-captions, Whisper, or another source.

**Required:** The transcript text (full or partial — work with what's provided)

**Optional:** Target audience, channel niche, tone

From the transcript: extract real chapter structure, pull exact phrases for keyword-dense copy, and use the creator's own language in the description and pinned comment.

### State C: Topic only (edge case)
User has a topic but no notes and no transcript.

Proceed with title variants, tags, description intro paragraph, and a structural chapter scaffold. State explicitly once: *"Chapter timestamps are structural placeholders — fill in the actual times after recording."* Do not repeat this caveat.

---

## Step 2 — Generate the launch package

Deliver all core deliverables in a single response, clearly labeled with H2 headers. Never skip a core deliverable. Offer optional deliverables at the end.

---

### Title Variants (2)

Produce exactly two variants. Label them by intent, not by letter/number.

**Curiosity-framed:** Withhold one key detail or tease the outcome. Front-load the most compelling word or phrase. Drives browse traffic (suggested videos, homepage feed).

**Clarity-framed:** Direct, keyword-forward, searchable. Lead with the primary keyword. Drives search traffic.

Rules:
- Maximum 60 characters each (YouTube truncates beyond this in most surfaces)
- No manufactured urgency ("You WON'T believe...") unless the video genuinely delivers a surprise
- No all-caps words
- No trailing ellipsis in the clarity variant

---

### Description

Structure in this exact order:

**Opening paragraph (first 150–200 characters):**
Keyword-dense, hooks the viewer and states the video's premise. This is what appears above-the-fold in search results and what YouTube's algorithm indexes most heavily. Must contain the primary keyword naturally — do not stuff.

**Body (2–3 sentences):**
Expand on what the viewer will get. Written in the creator's voice. Specific, not generic ("You'll learn the exact 3-step process I use" > "This video covers a lot of useful tips").

**Timestamped chapters:**
Minimum 4 chapters. First chapter must be at `0:00`. Labels must be content-specific — never use "Intro," "Part 1," "Outro," or "Conclusion" as standalone labels.

- **State A/C inputs:** Use structural timestamps in `0:00 / XX:XX` placeholder format. The creator fills in actual times post-recording.
- **State B (transcript):** Derive timestamps from transcript structure. Use actual minute markers where inferable.

**CTA section:**
One subscribe prompt + one resource link placeholder `[LINK]`. Keep brief — two lines maximum.

---

### Tags (10)

Apply the tag formula exactly:
- **2 broad tags** — high-volume, category-level (e.g., `productivity`, `YouTube`)
- **5 niche tags** — specific to the topic and audience (e.g., `notion for beginners`, `youtube growth tips`)
- **3 long-tail tags** — exact-phrase searches a viewer would type (e.g., `how to organize your notion workspace`, `youtube tags for small channels`)

First tag must exactly match or closely mirror the chosen title — this is YouTube's strongest tag-to-title relevance signal.

Present tags as a comma-separated list, ready to paste into the YouTube tag field.

---

### Pinned Comment

50–80 words. Written in the creator's voice, intended to be pinned to the top of the comments.

Purpose: sticky reference — chapters, key resources, corrections, or links mentioned in the video. Not an engagement play; that's the discussion seed.

Format: lead with a chapter list or the most valuable resource, then link placeholders. Example structure:
> ⏱ Chapters are in the description — jump to whatever's most useful.
> 🔗 [Resource name]: [LINK]
> 🔗 [Resource name]: [LINK]

---

### Discussion Seed

20–40 words. A question the creator posts as their first comment to seed early replies.

Rules:
- Must be specific to this video's content — never "What did you think?" or "Let me know in the comments!"
- Framed in first person from the creator's voice
- Asks something the viewer can answer from their own experience, not just by recapping the video
- Also called "first comment prompt" or "first pinned comment" in other frameworks — same output, different name

---

### Optional Deliverables

After delivering the five core outputs above, offer both of the following once. Generate whichever ones the user requests (or both if they asked upfront):

**Thumbnail Prompt (optional)**
A Midjourney or DALL-E compatible image prompt for the video thumbnail. Format:
- Subject description (person, object, or scene)
- Visual style (photo-realistic, illustrated, bold graphic, etc.)
- Text overlay suggestion (short phrase, ≤5 words, high contrast)
- Aspect ratio: 16:9

**Promo Tweet Set (optional)**
3 tweets, each ≤280 characters. Sequence:
1. **Announcement** — just published, what the video is about, link placeholder `[YOUTUBE_LINK]`
2. **Hook** — the most interesting insight, counterintuitive point, or moment from the video
3. **CTA** — subscriber-directed, drives watch + subscribe

Do not auto-generate optional deliverables unless asked. Offer them at the end of the core package.

---

## Step 3 — SEO rules

### Rules-based layer (apply to every output)

These signals are derived from known YouTube algorithm behavior — apply them without exception:

1. **Description opening:** First 100–150 characters do the most indexing work. Primary keyword must appear here, naturally integrated.
2. **Title-tag alignment:** First tag mirrors the winning title. No exceptions.
3. **Tag formula:** Enforced as written above — 2 broad, 5 niche, 3 long-tail. Padding beyond 10 provides no ranking benefit and dilutes relevance.
4. **Chapter labels:** YouTube uses chapter titles as secondary index signals. Descriptive labels outperform generic ones.
5. **Title length:** 60-character ceiling. Titles truncated in search results lose click-through rate.

### LLM knowledge layer

Keyword selection and semantic variation draw on training knowledge of what searches well in a given niche. This works reliably for evergreen topics across most creator categories.

**Honest ceiling — state this once in every session, do not repeat:**

> *"Keyword recommendations reflect training knowledge, not live search data. For trending topics or highly competitive niches, validate tags with TubeBuddy or VidIQ after running this skill."*

No external API key is required and none should be suggested as mandatory. TubeBuddy/VidIQ are validation tools, not prerequisites.

---

## Step 4 — Style guardrails

- **Never invent content.** Do not include facts, statistics, claims, or timestamps not present in the input. If the notes don't mention a specific number, don't write one.
- **No generic chapter labels.** "Intro," "Main Content," "Part 2," "Conclusion" are banned as standalone labels.
- **No "like and subscribe" in the pinned comment.** Creators know to ask; including it reads as template filler.
- **Match the creator's voice.** If the notes use casual language, the description uses casual language. Don't formalize input that wasn't formal.
- **Curiosity title must deliver.** If the video input doesn't support the curiosity framing, use the clarity variant as the recommended title and note why.
- **Description body is specific, not hype.** "You'll learn the exact method" > "This video is packed with tips."

---

## Step 5 — Follow-up offers

After delivering the package, offer once:

- "Want a version of either title tuned for a different audience or tone?"
- "Want the thumbnail prompt or promo tweet set?"
- "If you have a transcript, I can regenerate with accurate chapter timestamps."

Do not auto-regenerate unless asked.
