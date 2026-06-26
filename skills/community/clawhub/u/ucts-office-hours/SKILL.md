---
name: ucts-office-hours
description: >
  Product strategy session with 6 forcing questions. Reframes the problem,
  challenges premises, generates implementation approaches. Works directly
  in OpenClaw — no Claude Code session needed.
tags: [ucts, planning, product-strategy, office-hours]
---

# UCTS Office Hours

Run a structured product strategy session. This is a conversational skill — talk directly with the user.

## The 6 Forcing Questions

Ask each question. Push back on vague answers. Demand specifics.

### 1. What's the specific pain?
Not hypothetical. Real examples. Who screamed? What broke? When did it last happen?
If the user says "it would be nice to have X" — push: "What happens TODAY without X?"

### 2. Who experiences this most acutely?
Which user persona? How often? What's the cost of the status quo (in time, money, frustration)?
"Everyone" is not an answer. Find the single person who suffers most.

### 3. What's the current workaround?
If there is one, it tells you the actual need. If there isn't, why not?
Workarounds reveal the minimum viable solution.

### 4. What does the 10-star experience look like?
Dream big. If this worked perfectly — magic wand — what would it do?
Then cut: what's the 7-star version? The 5-star? The 3-star MVP?

### 5. What's the narrowest wedge?
The smallest possible thing that proves the concept works. Not the full vision — the first proof.
It should be buildable in one session. If it takes a week, it's too big.

### 6. What's the one metric?
Single number that tells you it's working. Not three metrics. One.
"Users" is not a metric. "Daily active users who complete the core flow" is.

## After the Questions

1. **Challenge the framing.** Push back on what the user SAID they want vs what they ACTUALLY described needing.
2. **Generate 3 approaches** with effort estimates:
   - Quick & dirty (hours)
   - Solid MVP (days)
   - Production-grade (weeks)
3. **Recommend one.** Be opinionated. "Start with approach 1, validate with the metric, then upgrade to approach 2."
4. **If a Claude Code session is needed**, generate the dispatch: `Load UCTS. Run /ucts guide <refined description>`
