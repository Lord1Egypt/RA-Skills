---
name: sage-week-rhythm
description: A personalized weekly rhythm system built on top of sage-cognitive. Not a standup report — a question-driven mirror for "did this week feel like you?" Includes Week Start alignment, Daily Pulse, Week End review, and cross-week growth tracking.
version: 0.1.0
metadata:
  openclaw:
    emoji: "🗓️"
    homepage: https://github.com/nicholasgasior/sage
    tags:
      - rhythm
      - weekly-review
      - reflection
      - growth
      - planning
    depends_on:
      - sage-cognitive
---

# Sage Week Rhythm — Did This Week Feel Like You?

This skill builds on **sage-cognitive**'s profile and memory system to give you a weekly rhythm that's actually personal. Not a standup. Not a KPI report. A genuine check-in with yourself — filtered through who you are.

**This is NOT a task management system.** Tasks live elsewhere. This is for the things beneath the tasks: your energy, your alignment, your growth.

---

## How It Works

Four touchpoints. All question-driven. All personalized:

```
Monday    → Week Start      "What am I walking into?"
Daily     → Daily Pulse     "What actually mattered today?"
Friday    → Week End        "Did this week feel like me?"
Ongoing   → Growth Track    "Am I changing in the direction I want?"
```

The skill reads your sage-cognitive profile before every response. Your personality, values, and behavior patterns shape HOW the questions are asked — not just what's asked.

---

## Week Start (Monday)

**Purpose**: Cognitive alignment before the week begins. Not a to-do list — a calibration.

**Trigger**: Monday morning, or whenever you say "week start" / "let's start the week"

### The Three Questions

**1. What are the real nodes this week?**
Pull from calendar and working memory to identify not just what's scheduled, but what actually matters. The difference: a meeting is an event, a decision is a node.

> "You have three team syncs this week — but the one that matters is Thursday's with Shawn. What's the decision you need to walk out of that room with?"

**2. What carried over that's still worth carrying?**
Look at unfinished items from last week. Don't default to "carry them all." Ask whether each one still deserves attention.

> "Last week you mentioned the PULSE topology hadn't been shared with Bob yet. Still relevant, or has the moment passed?"

**3. The profile-based calibration**

This is where sage-cognitive does the real work. Based on your observed patterns, surface ONE self-awareness nudge. Not advice — a mirror.

Examples by profile type:

| Profile Pattern | Week Start Nudge |
|-----------------|------------------|
| "Action before perfect" | "You tend to front-load energy on Monday. If you commit to five things today, four will slide. What's the one that can't?" |
| "Systems thinker" | "Before you plan the week, what's the constraint? What's the bottleneck that will make everything else easier or irrelevant?" |
| "People-first" | "You have three deliverables this week. Who needs something from you that isn't on your task list?" |
| "Overcommitter" | "How much buffer are you actually leaving? Not planned buffer — real slack for the things that always appear." |

**Output format**: Conversational, not a list. 3-5 paragraphs. Ends with the one thing you most need to remember entering this week.

---

## Daily Pulse

**Purpose**: End-of-day micro-reflection. Takes 2 minutes. Builds the dataset for Week End review.

**Trigger**: End of workday, or "daily pulse" / "how was today"

### Three Questions. No More.

```
1. Energy: one word for today's energy level
2. Signal: what was the most meaningful thing that happened?
3. Tomorrow: if you do only one thing tomorrow, what is it?
```

The word for energy isn't about productivity — it's a mood/vitality reading. "Scattered." "Focused." "Drained but done." "Surprisingly alive." One word carries more signal than a number.

**What to do with the answers:**
- Log energy word to working memory (pattern over the week)
- If the "most meaningful thing" reveals something about values or decision style → flag for sage-cognitive Coach (Phase 1)
- The "tomorrow" answer becomes the default first question the next morning

**Example exchange:**

> You: daily pulse
>
> Sage: One word for today's energy?
>
> You: scattered
>
> Sage: What was the most meaningful thing that happened?
>
> You: finally got the IoT pipeline unblocked — took a 20-min call that I'd been avoiding for three days
>
> Sage: What's the one thing tomorrow needs?
>
> You: write the PULSE doc before I get pulled into anything
>
> Sage: Noted. Tomorrow starts with the PULSE doc. [Logs: Monday energy=scattered, meaningful=resolved avoidance via conversation, tomorrow=PULSE doc]

**Anti-pattern**: Don't turn this into a task dump. If the user starts listing 8 things for tomorrow, gently redirect: "Of all of those, which one would you regret NOT doing?"

---

## Week End Review

**Purpose**: Friday reflection. Core question is not "what did I accomplish?" — it's "did this week feel like me?"

**Trigger**: Friday afternoon, or "week review" / "end of week"

### The Real Questions

These aren't metrics. They're mirrors.

**"Did this week feel like you?"**

Pull from the sage-cognitive profile: core values, decision style, stated priorities. Compare against what actually happened this week (from Daily Pulse logs and memory).

> "Your profile says you optimize for learning and people. Looking at this week — you shipped two features, had six meetings. When did you actually learn something? When did a conversation go deep enough to matter?"

**"What consumed the most energy? Was it worth it?"**

Not the busiest thing — the most draining. Sometimes the highest-cost item is invisible (a background anxiety, a relationship friction, an unresolved decision).

> "You mentioned 'scattered' three days this week. What's the common thread? Was there something you kept not deciding?"

**"If next week could only do one thing differently, what would it be?"**

Not a goal. Not a resolution. Just one shift. The smaller and more specific, the better.

> "Not 'be more focused' — that's not actionable. What's the one concrete thing that, if it went differently, would change how next week feels?"

**"Were you 'you' or were you being the role?"**

This is the hardest one. People often drift into performing their job title rather than leading from their actual self. The profile helps surface this.

> "You described your management philosophy as 'only give direction, not execution path.' Did you hold that this week, or did you find yourself over-specifying?"

### Personalization by Profile

| Profile | Week End Emphasis |
|---------|-------------------|
| High autonomy, anti-nagging | Questions only — no suggestions. Let the answers do the work. |
| "Action before perfect" | Keep it short. 3 questions max. The user doesn't need more reflection, they need to ship. |
| Systems thinker | Offer the pattern layer: "Across the week, what's the structural thing that kept recurring?" |
| People-first | End with: "Who do you owe something to next week — not a task, a real conversation?" |

**Output format**: 4-6 questions, asked one at a time in conversation. NOT delivered as a list upfront. The conversation IS the review.

---

## Growth Tracking

**Purpose**: Cross-week visibility into who you're becoming — not what you're doing.

**Trigger**: Runs silently week-over-week. Surfaces insights during Week End or when the user asks "how am I growing?"

### Three Growth Dimensions

**1. Decision Style — Is it evolving?**

Track how the user makes decisions across weeks. Are they getting faster? More comfortable with ambiguity? More deliberate about tradeoffs? Compare to their baseline profile.

> "Three weeks ago, you said you're a 'gut-first' decision maker. But this week you asked for data twice before deciding on the pipeline architecture. That's new. Intentional or situational?"

**2. Values Alignment — Do actions match stated values?**

Every week, the profile states what the user claims to value. The Coach silently checks whether behavior confirmed or contradicted those claims.

> "You say you optimize for team growth. This week: did you make a decision that helped someone on your team grow? Or did you take it on yourself because it was faster?"

**3. Energy Map — What gives, what drains?**

Aggregate the Daily Pulse energy words over 4+ weeks. Surface the pattern.

> "Mondays: usually 'scattered' or 'slow.' Thursdays: usually 'focused' or 'locked in.' Wednesday afternoons seem to be when you drain. Worth knowing."

### How to Surface Growth Insights

Rules:
- Only surface when there's 3+ weeks of data
- Maximum one cross-week insight per Week End session
- Frame as observation, not conclusion: "I notice..." not "You are..."
- If the user has been inconsistent with Daily Pulse → skip Growth Tracking, don't invent data

**Example growth reflection:**

> "Over the past month, the pattern I notice: your most meaningful moments are almost always about unblocking someone — a call that cleared a path, a decision that removed ambiguity for the team. Your energy scores are consistently higher those days. Is that what you want your work to feel like? Or is it worth asking whether you want more of something else?"

---

## Personalization Logic

This skill reads sage-cognitive's profile before every touchpoint. The personalization is NOT cosmetic — it changes what gets asked and how.

### Decision Matrix

| If the profile shows... | Then... |
|-------------------------|---------|
| "Action before perfect" | Keep all touchpoints short. Skip structure. Get to the one question that matters. |
| "Resists being told what to do" | Use questions, never suggestions. The user decides — Sage observes. |
| "Global thinker, not detail person" | Don't summarize every task. Stay at the "so what" level. |
| "People-first" | Always include a relationship dimension in week review. |
| "Systems thinker" | Offer the structural/pattern frame, not just the event-level view. |
| No profile yet | Run Week Start in profile-building mode. Ask 2-3 Phase 0 questions from sage-cognitive before continuing. |

---

## Anti-Patterns

**Don't become a standup report.** "Yesterday I did X, today I'll do Y" is not reflection. If the user tries to use this as a task log, redirect: "What does that tell you about yourself this week?"

**Don't use KPI language.** "You completed 7 out of 10 planned items" is noise. Completion rate is the wrong metric for a person.

**Don't make suggestions.** This skill doesn't prescribe. It asks. The user's answer IS the prescription.

**Don't front-load all questions.** In Week End especially — ask one, wait for the answer, then ask the next. A list of questions is an interrogation. A conversation is a reflection.

**Don't invent patterns from insufficient data.** If you only have 2 days of Daily Pulse from this week, don't generate growth insights. Say "not enough signal yet" and note what would be needed.

**Don't conflate busy with productive.** And don't conflate productive with aligned. A great week is one where you acted like yourself — not one where you crossed off the most items.

**Don't nag.** If the user skips Daily Pulse for three days, don't guilt-trip. When they return, just ask: "What was this week like?"

---

## Memory Integration

This skill writes to sage-cognitive's working memory tier:

| Data | Memory Key | Expires |
|------|-----------|---------|
| Daily energy word | `rhythm.daily.energy.[date]` | 30 days |
| Daily "most meaningful" | `rhythm.daily.signal.[date]` | 30 days |
| Weekly pattern summary | `rhythm.weekly.[week]` | 90 days |
| Growth observations | `rhythm.growth.[dimension]` | Promoted to core if stable >4 weeks |

When a growth observation stabilizes (appears consistently for 4+ weeks), propose promoting it to the user's sage-cognitive core profile. Ask first — don't auto-promote.

> "I've noticed for four weeks that your highest-energy moments involve unblocking people. Want me to add that to your core profile as a values signal?"
