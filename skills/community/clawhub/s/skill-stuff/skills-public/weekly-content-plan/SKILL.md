---
name: weekly-content-plan
description: Plans realistic content for the week based on what the user actually has to say with no filler. Use when a user wants a content plan that reflects reality not a template.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
metadata:
  openclaw.emoji: "📆"
  openclaw.user-invocable: "true"
  openclaw.category: content
  openclaw.tags: "content-planning,calendar,weekly,social-media,linkedin,twitter,strategy"
  openclaw.triggers: "plan my content,what should I post this week,content calendar,weekly content,social media plan"
  openclaw.homepage: https://clawhub.com/skills/weekly-content-plan


# Weekly Content Plan

Most content calendars are filled with content that shouldn't exist.
"Tuesday: motivational quote. Wednesday: engagement question. Thursday: throwback."

This skill plans content you'd actually want to post.

---

## On-demand only

`/contentplan [what's happening this week / what's on your mind]`
Or: "Plan my content for this week"
Or: "What should I post this week?"

---

## The inputs that make the plan

**What happened or is happening:**
Events, launches, projects, decisions, conversations worth sharing.
Things from the week that might be worth a post.

**What you've been thinking about:**
Ideas circling. Problems you're working on. Opinions you've been forming.

**What you're working on:**
Projects, work in progress, things you're building.
"Working in public" content comes from this.

**What you've learned recently:**
From reading, experience, mistakes, conversations.

**What's timely:**
Industry news you have a take on. Conversations happening in your space.

The plan is built from what's real, not from what needs to fill a slot.

---

## The approach

### Step 1 — What do you actually have this week

Ask (or infer from user's input):
- What happened this week worth sharing?
- What are you working on that people might find interesting?
- Any opinions or takes you've been sitting on?
- Anything timely in your space?
- Do you have any existing content (talk, article, podcast) to repurpose?

### Step 2 — Assess the material

For each piece of material: what format fits it best?
- Sharp insight → tweet or LinkedIn post
- Complex idea → thread
- Story or experience → LinkedIn or newsletter
- Process or how-to → short-form video
- Opinion → thread or LinkedIn

### Step 3 — Build the plan

Rules:
- Plan for 3-5 posts per week maximum. Less if the material doesn't support more.
- Quality over frequency, always.
- Each post should have a reason to exist beyond "it's Tuesday."
- If there's nothing worth posting this week: say so. Rest weeks are valid.

Format:
```
CONTENT PLAN — Week of [DATE]

[N] posts this week.

---

[PLATFORM] — [DAY]
[Format: tweet / thread / LinkedIn / reel / newsletter]
Topic: [what it's about]
Why this week: [why now is the right time]
Source: [where the content comes from — your experience, a story, an observation]
Notes: [anything to think about when writing it]
Status: ready to write / needs [X] first

---
```

### Step 4 — Flag what needs doing first

Sometimes the content is clear but needs a piece that doesn't exist yet.
"You mentioned the project launch — write a short summary of what you built first, then post about it."
Note these as pre-work in the plan.

---

## Honest constraints

If the user doesn't have much to say this week: the plan reflects that.
2 posts is fine. 1 post is fine. 0 posts is fine.

A week with three good posts beats a week with seven posts where four are filler.
The skill never recommends filler.

If the user asks for 30 posts a week: explain why that's probably not the right goal for them
unless they're a full-time creator with a team. Then ask what they're actually trying to achieve.

---

## Output includes

For each planned post:
- The platform and format
- The core idea in one sentence
- Why this week (timeliness or relevance)
- What to write from (source material)
- Any notes on approach or angle

It does NOT include:
- Fully drafted posts (use the other skills for that)
- Scheduling recommendations beyond "early week vs late week" general guidance
- Engagement predictions

---

## Management commands

- `/contentplan [input]` — generate this week's plan
- `/contentplan [platform]` — plan for one platform only
- `/contentplan light` — minimal week (1-2 posts)
- `/contentplan write [post from plan]` — draft one post from the plan (routes to appropriate skill)

---

## What makes it good

The "why this week" field.
Content with a reason to exist right now performs better than evergreen content
scheduled because a slot needed filling.
Timeliness and relevance are underrated signals.

The honesty about volume.
Most content advice pushes high frequency because frequency is measurable.
Quality isn't as easily measured. This skill optimises for quality.

The plan as a thinking tool, not a commitment.
The plan clarifies what you have to say. The posts come from the clarity.
