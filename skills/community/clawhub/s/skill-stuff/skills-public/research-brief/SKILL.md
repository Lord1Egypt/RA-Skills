---
name: research-brief
description: Deep research on any topic with bottom line first, contested claims acknowledged, and sources listed. Use when a user needs to properly understand something.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
allowed-tools: web_search web_fetch
metadata:
  openclaw.emoji: "🔬"
  openclaw.user-invocable: "true"
  openclaw.category: intelligence
  openclaw.tags: "research,briefing,analysis,deep-dive,knowledge,information"
  openclaw.triggers: "research,I need to understand,brief me on,deep dive into,explain,research brief,look into"
  openclaw.homepage: https://clawhub.com/skills/research-brief


# Research Brief

When you need to actually understand something — not just find information about it.

Ask a question. Get a structured briefing. Sources included.
The bottom line is always explicit.

---

## On-demand only

No cron. Triggers on request.

`/research [question or topic]`
Or just ask directly: "Research X for me" / "I need to understand Y"

---

## The output structure

Every research brief has the same five sections.

### 1. Bottom line (first, always)

One paragraph. The answer to the question.
Written assuming the reader already knows the context.
No preamble. No "great question."

Good:
> "The EU AI Act's high-risk classification will apply to most HR screening tools from August 2026, requiring conformity assessments and human oversight documentation. The main compliance burden falls on deployers, not developers — if your company uses third-party AI tools for hiring decisions, you're the regulated party."

Bad:
> "The EU AI Act is a comprehensive regulatory framework that was adopted in... [500 words of background]"

### 2. What's established

What is clearly true, well-evidenced, and not meaningfully contested.
Bullet points. Short. Sources in parentheses.

### 3. What's contested or unclear

Where the evidence is mixed, where experts disagree, where the situation is still developing.
This section earns trust. A brief with no uncertainty is not a brief — it's marketing.

### 4. What's missing

What would you need to know that this research couldn't find?
What questions remain open?
Where would deeper research be needed?

### 5. Sources

List of sources consulted, with a one-line note on each.
Not just URLs — say what each source is and why it was useful or limited.

---

## Research depth levels

The user can specify or the agent infers from the question:

**Quick** — 15-30 minutes of research. Good for "what is X" and "overview of Y."
Surface-level synthesis. 3-5 sources. Suitable for orientation.

**Standard** — 45-90 minutes. Default. Good for decision support.
Multiple angles. 8-12 sources. Identifies key debates.

**Deep** — 2-4 hours. For high-stakes decisions or complex topics.
Primary sources. Expert views. Full landscape.
Flags when something is outside the skill's ability to research properly.

Infer the depth from the question's stakes and complexity.
Ask if genuinely unclear.

---

## Research approach

### Source diversity

Don't rely on a single type of source.
Good research uses a mix of:
- Primary sources (official documents, papers, filings)
- Expert commentary (analysts, practitioners, academics)
- News coverage (for events and timelines)
- Criticism and counterarguments (not just the mainstream view)

### Verification

For key claims: find at least two independent sources.
If a claim appears in only one place and it's important: flag it as unverified.

### Recency check

For fast-moving topics: prioritise sources from the last 6 months.
For evergreen topics: use the best sources regardless of date.

### Honest limits

Some questions can't be properly answered with web research.
If the question requires:
- Proprietary data the agent can't access
- Expertise that requires lived experience
- Local knowledge the agent doesn't have

— say so clearly rather than giving a superficial answer.

---

## Output format

**🔬 Research Brief: [TOPIC]**
*Depth: [quick/standard/deep] · [N] sources · [DATE]*

---

**Bottom line**
[The answer. One paragraph. Directly addresses the question.]

---

**What's established**
• [Fact] — ([source])
• [Fact] — ([source])

---

**What's contested**
• [Debate or uncertainty]
• [Another area of genuine disagreement]

---

**What's missing**
• [Gap in available information]
• [Question that requires further research]

---

**Sources**
1. [Source name] — [URL] — [one sentence: what it is and why it was useful]
2. [Source name] — [URL] — [assessment]

---

## Special modes

**Comparison brief:**
`/research compare [A] vs [B]`
Structured comparison with a recommendation. Same five sections plus a comparison table.

**Update brief:**
`/research update [topic]`
"What's changed since [last research date]?" Only covers new developments.

**Devil's advocate:**
`/research argue against [position]`
Best case against something. Useful for stress-testing a decision.

---

## Management commands

- `/research [question]` — standard brief
- `/research deep [question]` — deep brief
- `/research quick [question]` — quick orientation
- `/research compare [A] vs [B]` — comparison
- `/research update [topic]` — what's changed
- `/research argue against [position]` — steelman the opposition

---

## What makes it good

The bottom line first is non-negotiable.
Research that buries the answer is research optimised for the researcher, not the reader.

The "what's missing" section separates honest research from confident-sounding nonsense.
If there's nothing uncertain or missing, the research wasn't thorough enough.

Source diversity prevents echo chamber research.
One perspective repeated across ten outlets is one perspective, not ten.
