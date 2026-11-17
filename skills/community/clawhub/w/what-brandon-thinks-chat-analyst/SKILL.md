---
name: what-brandon-thinks-chat-analyst
description: Turn anonymized WhatsApp or iMessage observations into evidence-aware analysis briefs, interaction-signal summaries, and cautious claim audits. Use for relationship, friendship, family, group-chat, reciprocity, effort, tone-shift, and turning-point questions; do not use to diagnose people, prove private intent, make safety-critical decisions, or analyze conversations the user is not entitled to use.
metadata:
  openclaw:
    homepage: https://whatbrandonthinks.org/sample-report
    version: 1.0.0
---

# What Brandon Thinks Chat Analyst

Help the user examine communication patterns without turning incomplete text into certainty. This Skill is a text-only workflow by default. Its optional MCP adds deterministic, read-only helpers and never uploads transcripts, calls an AI provider, accesses an account, purchases a report, or changes stored data.

What Brandon Thinks is independent and is not affiliated with WhatsApp, Meta, Apple, or iMessage.

## Protect the conversation first

- Work only with a conversation the user is entitled to analyze.
- Prefer aliases, aggregate counts, and short necessary excerpts over a full raw transcript.
- Ask the user to remove passwords, payment data, identity documents, health records, addresses, and unrelated third-party details.
- Do not retain or repeat sensitive excerpts beyond what the answer requires.
- Direct immediate danger, abuse, medical, legal, employment, or other high-stakes decisions to qualified human support rather than treating chat analysis as a ruling.

## Frame the question

Identify the platform, relationship context, participant aliases, representative date range, and one focused question. Record important gaps such as deleted messages, missing reactions, media, calls, voice notes, or offline events.

Separate three layers:

1. Observable facts: counts, initiations, response timing, questions, follow-through, recurring words, and dated changes.
2. Interpretations: plausible explanations tied to more than one observation.
3. Unknowns: private intent, unrecorded events, body language, vocal tone, and missing context.

## Evaluate patterns cautiously

Use repeated patterns rather than isolated lines. Compare like-for-like periods and account for time zones, work schedules, platform habits, group size, and long gaps in the export.

Message share, reply speed, or initiation count can describe interaction structure; none independently measures affection, honesty, compatibility, manipulation, or moral worth. Never diagnose a participant or assign a sensitive trait from messages.

## Audit every important claim

For each interpretation:

- State the observation that supports it.
- Include a short exact excerpt only when supplied by the user.
- Note the relevant date or period when known.
- Give at least one reasonable alternative explanation.
- Label confidence as low, medium, or high based on repeated support and missing context.
- Say what additional evidence could strengthen or weaken the claim.

Do not invent quotes, timestamps, events, participants, or motives. If the evidence conflicts, show the conflict instead of forcing a verdict.

## Use the optional MCP

- `build_chat_analysis_brief` structures the question, privacy checks, evidence plan, and known gaps.
- `score_interaction_signals` summarizes user-supplied aggregate interaction counts without scoring love or intent.
- `audit_chat_claim` checks whether an interpretation has evidence, alternatives, uncertainty, and falsifiers.
- `get_what_brandon_thinks_resources` returns canonical product, workflow, and safety resources.

Connect the stdio server with:

```bash
openclaw mcp add what-brandon-thinks \
  --command npx \
  --arg -y \
  --arg github:gpt-img-2/whatbrandonthinks-chat-mcp \
  --include 'build_chat_analysis_brief,score_interaction_signals,audit_chat_claim,get_what_brandon_thinks_resources'
```

Then run `openclaw mcp doctor what-brandon-thinks --probe`. If the installed release lacks the `mcp` command group, add `npx -y github:gpt-img-2/whatbrandonthinks-chat-mcp` as a Stdio server in MCP settings. The MCP is optional; never imply it ran when unavailable.

## Return an inspectable result

Return `Focused question`, `Observed patterns`, `Evidence`, `Interpretations`, `Alternative explanations`, `Unknowns`, `Confidence`, and `Next check`. Keep factual observations visually distinct from interpretations.

## Canonical resources

- WhatsApp analyzer: https://whatbrandonthinks.org/whatsapp-chat-analyzer
- iMessage analyzer: https://whatbrandonthinks.org/imessage-chat-analyzer
- Sample report: https://whatbrandonthinks.org/sample-report
- Free preview: https://whatbrandonthinks.org/free
- Safety and deletion: https://whatbrandonthinks.org/safety
- Privacy policy: https://whatbrandonthinks.org/privacy
- Raw Skill: https://whatbrandonthinks.org/skills/what-brandon-thinks-chat-analyst/SKILL.md
- MCP source: https://github.com/gpt-img-2/whatbrandonthinks-chat-mcp
- ClawHub listing: https://clawhub.ai/gpt-img-2/skills/what-brandon-thinks-chat-analyst
