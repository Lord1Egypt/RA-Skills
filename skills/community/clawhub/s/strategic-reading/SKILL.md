---
name: strategic-reading
description: "Read a source through the lens of a specific problem. Produces an applied playbook, not a summary."
tags: [reading, analysis, strategy, research, thinking]
---

# Strategic Reading

Read a book, article, paper, transcript, or case study through the lens of a specific strategic problem. Produces an applied playbook that maps the source's insights onto the problem and gives actionable recommendations.

**This is not summarization. This is reading with a mission.**

## Contract

- Requires TWO inputs: source text AND a specific strategic problem or question
- Output is an applied analysis, not a general summary
- Every recommendation has its own passage locator, source claim, and separately labeled applied inference
- Never runs on a source without a clear "what problem does this help with?"

## Evidence for each recommendation

Give every proposed tactic/action a stable ID and its own evidence record:

1. **Passage locator:** identify the source edition/revision or saved snapshot
   and the exact page/section/paragraph, timestamp, or anchored text range.
   A title, homepage, or quote shared across a whole section is insufficient.
   If the text has no locators, preserve an authorized excerpt and assign
   paragraph IDs in that excerpt; label them as assigned IDs, not original
   page numbers. Never invent a page or imply an unseen passage was read.
2. **Source claim:** quote briefly or faithfully paraphrase what that passage
   actually establishes, including its scope and qualifications.
3. **Applied inference:** state the proposed action for the user's problem and
   explain the bridge from the source claim. Label this as your application,
   not something the source prescribed for the user.
4. **Assumptions and limits:** identify what must hold for that bridge to work
   and how the user could check it. Keep an unsupported idea explicitly labeled
   as a hypothesis outside the source-backed recommendation list.

Repeat the locator/claim/inference record for each recommendation, even if two
use the same passage. A section-level quote never covers untraced extra tactics.
Use recommendation IDs in a timing list instead of adding fresh ungrounded
actions there. Distinguish evidence-backed relevance from a guaranteed result.
See [traceable-example.md](references/traceable-example.md) for two independently
traceable recommendations and a fully available fictional source.

## When to use

- You have a strategic problem and a source that might inform it
- An academic paper or book needs to be read for actionable takeaways
- A career, research, or project decision could be informed by external knowledge
- Learning with intent: "I need to understand this SO I can DO that"

## When NOT to use

- Casual reading or general interest — that's a book note, not strategic reading
- Pure fact-finding — use a research skill instead
- First-pass source familiarization — read the source first, then apply

## Phases

1. **Identify the strategic problem.** What specific situation or decision is the user working on? Get this explicit before reading the source.
2. **Read the source.** Extract key frameworks, tactics, observations, and historical patterns.
3. **Map to the problem.** Triage sections for relevance (HIGH / MEDIUM / LOW), with passage locators and accurate source claims. Keep application distinct.
4. **Build the playbook.** Give each recommendation the evidence record above, then organize its ID by timing.
5. **Save if authorized.** Write to the explicitly chosen project/reading destination only when the task authorizes it; otherwise return the playbook in the conversation.

## Output Structure

```
---
title: "{Source Title} — Applied to {Problem}"
type: applied-reading
date: YYYY-MM-DD
source: "{citation}"
problem: "{the strategic question}"
---

# {Source Title} — Applied to {Problem}

> Brief overview: the problem, the relevant source claims, and the proposed application.

## The Core Parallel
How the source's central dynamic maps onto the user's situation.

## Section Triage
For each major section of the source:
- 2-3 sentence summary of what it says
- Relevance to the problem: HIGH / MEDIUM / LOW
- One directly applicable quote or faithful paraphrase with its passage locator

## The Playbook
Repeat for EACH recommendation, including tactics and proposed avoidances:

### R1 — {proposed action}
- **Passage locator:** {source identity/revision + precise location}
- **Source claim:** {what the passage actually says}
- **Applied inference:** {action + why it may fit this problem}
- **Assumptions/limits:** {conditions, uncertainty, and a check}

## Short/Medium/Long-Term Actions
- **Now:** recommendation IDs from the playbook
- **This month:** recommendation IDs from the playbook
- **This quarter:** recommendation IDs from the playbook

## Connections
Related notes, projects, and concepts this analysis touches.
```

## Anti-Patterns

- Producing a generic book summary instead of applied analysis
- Reading without a clear strategic question — get the problem first
- Forgetting to map recommendations back to the source passages
- Writing analysis disconnected from the user's actual situation
- Over-recommending: 2-3 high-impact moves beat 10 low-impact suggestions
