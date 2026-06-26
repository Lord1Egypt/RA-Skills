---
name: content-from-talks
description: Extracts platform-ready posts from talks, podcasts, and long-form writing. Use when a user wants to repurpose existing content without it feeling scraped.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
allowed-tools: web_fetch
metadata:
  openclaw.emoji: "🎙️"
  openclaw.user-invocable: "true"
  openclaw.category: content
  openclaw.tags: "repurpose,content,podcast,talk,linkedin,twitter,newsletter"
  openclaw.triggers: "repurpose this,turn my talk into,content from podcast,extract posts,repurpose content"
  openclaw.homepage: https://clawhub.com/skills/content-from-talks


# Content From Talks

The best content you'll ever make is probably already recorded.
The problem is getting it out.

This skill takes source material — talk, podcast, long essay, video — and extracts posts
that feel written for the destination, not copied from the source.

---

## On-demand only

`/repurpose [paste transcript, share recording link, or paste essay]`
Or: "Turn this talk into posts" / "I did a podcast — what can I share from it?"

---

## The problem with most repurposing

It's too literal.
"Here's a clip from my talk." (The clip starts mid-sentence and needs context.)
"Here are my slides." (Slides without the talk are confusing.)
"Thread of key takeaways from my interview." (The takeaways are all vague.)

The source material has ideas in it. The skill extracts the ideas, not the source.

---

## What this skill does

1. Reads or processes the source material
2. Identifies the discrete ideas worth sharing
3. Rewrites each one for the target platform and format
4. Packages as a set of posts, not a dump

---

## Input types

**Podcast or interview transcript:**
Paste the transcript or key section.
The skill extracts the best ideas and the best lines.

**Talk / presentation:**
Paste the transcript, outline, or slides with notes.
Extracts: the core argument, the surprising data, the best stories, the counterintuitive moments.

**Long-form essay or article:**
Paste the full text.
Extracts: the key insights, the specific examples, the lines worth sharing standalone.

**Video link (YouTube):**
web_fetch the transcript if available.
Process as transcript.

---

## The extraction process

### Step 1 — Read for ideas

Not sentences. Ideas.
What are the discrete, valuable things in this source material?

Rate each idea:
- Strong: interesting, specific, stands alone
- Medium: interesting with context
- Weak: filler, transition, summary of stronger ideas

Extract only Strong ideas for standalone posts.
Medium ideas get grouped or connected to stronger ones.

### Step 2 — Identify the best lines

Every talk or podcast has 3-5 sentences that are genuinely quotable.
Lines that could stand alone. Lines that don't need context.

Find them. They're the quote posts.

### Step 3 — Match to format

For each extracted idea, decide the best format:

- Standalone tweet/post — one sharp insight
- Thread — an idea that needs 4-8 tweets to develop
- LinkedIn post — professional insight with a specific story
- Reel/Short script — idea that works visually or conversationally
- Newsletter excerpt — idea that works in longer prose

### Step 4 — Write for the destination

Rewrite each idea for its format.
Not "as I said in my talk, X."
Not "from my podcast, here's the key insight."
The idea, written fresh for where it's going.

The test: would this feel natural if it appeared on its own, without the reference to the source?

---

## Output format

**From [SOURCE TITLE / TYPE]**
Extracted [N] ideas. Packaged as:

**STANDALONE POSTS ([N]):**
[Post 1] — [Platform]
[Text of post]

[Post 2] — [Platform]
[Text of post]

**QUOTE CARDS ([N]):**
"[Quotable line]"
*Note: works as text graphic*

**THREAD CANDIDATES ([N]):**
[Idea that works as a thread] → `/thread [idea]` to expand

**REEL/SHORT CANDIDATES ([N]):**
[Idea that works on video] → `/reel [idea]` to script

---

## What gets left out

Not everything from a talk or podcast is worth sharing.
The skill doesn't extract:
- Transitions and connective tissue
- Context that only makes sense in the original
- Weaker versions of ideas that are already captured by better ones
- Anything that would need the original source to make sense

Less is more. 5 good posts from a 45-minute talk beats 20 mediocre ones.

---

## Management commands

- `/repurpose [source]` — extract and package
- `/repurpose [source] [platform]` — extract for a specific platform only
- `/repurpose tweet [source]` — standalone tweets only
- `/repurpose thread [source]` — threads only
- `/repurpose linkedin [source]` — LinkedIn posts only
- `/repurpose reel [source]` — video scripts only

---

## What makes it good

The "written for the destination" rule.
Content that reads like it was scraped from a transcript performs worse than
content that was written for where it's going.
Ideas survive the translation. Sentences often don't.

The extraction discipline.
Not everything is worth sharing. The skill's job is to find what is.

The format matching.
A podcast anecdote might become a LinkedIn story.
A counterintuitive data point might become a tweet.
The format should serve the idea, not the other way round.
