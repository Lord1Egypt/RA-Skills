---
name: personal-brand-review
description: Audits social presence honestly covering what is working, what is not, and what is missing. Use when a user wants a real assessment of how they come across online.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
metadata:
  openclaw.emoji: "🔎"
  openclaw.user-invocable: "true"
  openclaw.category: content
  openclaw.tags: "personal-brand,audit,review,social-media,linkedin,twitter,presence"
  openclaw.triggers: "how does my social look,review my profile,audit my presence,personal brand,how do I come across online"
  openclaw.homepage: https://clawhub.com/skills/personal-brand-review


# Personal Brand Review

Most personal brand advice is about growth.
This skill is about honesty.

What does your current presence actually communicate?
Is it what you want to communicate?
What's the gap?

---

## On-demand only

`/brandreview [your handles / links / paste your recent posts]`
Or: "Review my social presence" / "Tell me honestly how my LinkedIn looks"

---

## What gets reviewed

**Platform presence:**
- Twitter/X, LinkedIn, Instagram, Substack — wherever the user is active
- What's the current state: active, dormant, inconsistent?
- What does the profile itself communicate? (bio, photo, header)

**Content:**
- What topics have you been posting about?
- Is there a clear point of view, or is it scattered?
- What's the strongest content? The weakest?
- What's missing that you probably should be saying?

**Voice:**
- Does the content sound like a person?
- Is the voice consistent or does it shift?
- What's the ratio of performing to actually saying something?

**Audience alignment:**
- Who is currently engaging? Does that match who you want to reach?
- What content gets real engagement vs. performative engagement?

---

## The approach

### Step 1 — Gather what exists

Accept: links to profiles, pasted recent posts, screenshots, or a description.
Use web_fetch to access public profiles if links are provided.

### Step 2 — Assess without flattery

The audit has three sections:

**What's working:**
Specific things that are genuinely good.
Not "great energy" — specific: "The posts where you share [X] get real engagement because..."

**What isn't working:**
Specific things that are weakening the presence.
Not "could improve" — honest: "The LinkedIn posts that start with 'Excited to share' undermine your voice because..."

**What's missing:**
The gap between what you're posting and what would actually represent you well.
Often: an actual point of view. Specific stories. The thing you know that others don't.

### Step 3 — Three recommendations

Not ten. Three.
The three most impactful things to change, start, or stop.
Specific and actionable.

Good recommendations:
- "Stop posting [type of content] — it contradicts the expertise you're trying to establish."
- "You have strong opinions when you talk in person but they don't appear in your posts. Start saying the thing."
- "Your bio says you're [X] but your posts are mostly about [Y] — pick one or explain the connection."

Bad recommendations:
- "Post more consistently."
- "Engage more with your audience."
- "Find your niche."

---

## Output format

**🔎 Brand Review — [NAME]**
*Platforms reviewed: [list]*
*Posts reviewed: [N]*

---

**What's working:**
[Specific observation 1]
[Specific observation 2]

**What isn't working:**
[Specific observation 1]
[Specific observation 2]

**What's missing:**
[The gap — what would make this presence significantly better]

---

**Three recommendations:**

1. [Specific, actionable change]
2. [Specific, actionable change]
3. [Specific, actionable change]

---

**The honest summary:**
[One paragraph. The overall picture. What this presence currently communicates and whether that's right.]

---

## What this skill won't do

Growth hacks. Follower acquisition tactics. Posting frequency optimisation.
Engagement bait recommendations.

This is about whether your presence represents you accurately and well.
That's a different question from how to get more followers.

The two are related — a presence that represents you accurately tends to attract the right people —
but they're not the same question, and mixing them produces bad advice for both.

---

## Management commands

- `/brandreview [input]` — full review
- `/brandreview [platform] [input]` — review one platform only
- `/brandreview bio` — review just the bio/profile
- `/brandreview voice` — review just the voice and tone
- `/brandreview [platform] vs [platform]` — compare consistency across platforms

---

## What makes it good

Specificity and honesty are the whole product.
A review that says "great energy, could post more consistently" is useless.
A review that says "your LinkedIn posts start with the lesson instead of the story, which
makes them read like advice columns rather than actual experience" is useful.

The "what's missing" section is often the most valuable.
It requires the reviewer to understand what the person is trying to do, not just what they're doing.

The honest summary is the thing most people want and don't get.
"This presence currently communicates that you're good at your job but don't have strong opinions.
Is that what you want?" is a useful question.
