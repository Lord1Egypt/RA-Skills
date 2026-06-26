---
name: newsletter-issue
description: Structures and writes a complete newsletter issue from notes or brain dump. Use when a user has something to say and needs the editorial scaffold to say it well.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
metadata:
  openclaw.emoji: "📨"
  openclaw.user-invocable: "true"
  openclaw.category: content
  openclaw.tags: "newsletter,writing,substack,email,content,publishing"
  openclaw.triggers: "write my newsletter,help with newsletter,newsletter issue,what should I send,newsletter content"
  openclaw.homepage: https://clawhub.com/skills/newsletter-issue


# Newsletter Issue

Most newsletters fail because they're written like obligations.
"It's Thursday, time to send the newsletter."

This skill writes issues that feel like someone actually wanted to write them.

---

## On-demand only

`/newsletter [what's on your mind this week / what you want to share]`
Or: "Help me write this week's newsletter"
Or: share links, notes, a brain dump — the skill structures it.

---

## What makes a good newsletter issue

**One thing, well.**
The best newsletters do one thing per issue.
One idea, explored properly. Or one collection of things, unified by a genuine theme.

Not: five unrelated things crammed together because it's Thursday.

**A voice.**
Newsletters are personal publishing. They should sound like a person.
Not a brand. Not a content marketing piece. A person.

**An ending that earns the read.**
The last paragraph should make the reader glad they read it.
Not a CTA. Not "hit reply and let me know." A genuine close.

---

## Setup (one-time)

Ask once, store in a preferences file:
- What's the newsletter about? What's the topic / domain?
- Who reads it? (helps calibrate tone and depth)
- What's the format? (long essay / short notes / mixed / links with commentary)
- What's the voice? (conversational / precise / dry / warm)
- Length? (short <500 words / medium 500-1000 / long 1000+)

---

## The approach

### Step 1 — What do you have

Accept any input:
- A brain dump
- A list of links
- One idea you've been thinking about
- Notes from the week
- "I want to write about X but don't know where to start"

### Step 2 — Find the spine

The spine is the thing the issue is actually about.
Sometimes the user knows it. Sometimes it's hidden in the brain dump.

One sentence: "This issue is about [X]."

Everything in the issue should connect to the spine.
Anything that doesn't connect gets cut or saved for another issue.

Ask if not clear: "What do you actually want to say this week?"

### Step 3 — Structure

**Subject line / title:**
Specific enough to be interesting. Not so clever that it's confusing.
Good: "The thing nobody tells you about compound interest"
Bad: "Thoughts on money 💭"

**Opening:**
Earns the read in the first two sentences.
A scene, a question, a provocative claim, a specific moment.
Not a preamble. Not "welcome back to the newsletter."

**Body:**
Develop the idea. Or curate the links. Or both.
For curation: each item gets a sentence of genuine commentary — not just the headline.
"This is interesting" is not commentary.
"This surprised me because X" is commentary.

**Close:**
One paragraph. The takeaway, or the question, or the feeling the reader should leave with.
Not a CTA. Not "see you next week."
End on something worth ending on.

**Optional: P.S.**
The P.S. is where you can be more casual, add a personal note, or share something small.
It's the one place that can feel like a text message.

### Step 4 — Write the issue

Match the voice from preferences.
Keep to the length preference.
One draft. Clean. No filler.

---

## Output format

```
SUBJECT LINE: [subject line]

---

[Opening]

[Body]

[Close]

---

P.S. [optional]
```

---

## Curation format (for link-heavy newsletters)

```
**[TITLE / TOPIC]** — [source]
[2-3 sentences of genuine commentary — why you're sharing this, what surprised you, what it means]
[Link]
```

The commentary is the newsletter. The links are the evidence.

---

## Management commands

- `/newsletter [input]` — write an issue
- `/newsletter subject` — generate subject line options
- `/newsletter shorter` — cut to length
- `/newsletter open` — try different openings
- `/newsletter close` — rewrite the ending
- `/newsletter tone [adjustment]` — "more personal", "more precise", "less formal"

---

## What makes it good

Finding the spine before writing anything.
A newsletter issue without a spine is just content.
With a spine, it's a piece of writing.

The commentary rule for curation newsletters.
"Here are some links" is not a newsletter.
"Here are some links and here's why each one is interesting" is.

The ending as a craft element.
Most newsletters end with "that's it for this week."
An ending that earns the read is what makes someone open the next one.
