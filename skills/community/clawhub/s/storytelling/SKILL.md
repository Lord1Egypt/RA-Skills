---
name: Storytelling
slug: storytelling
version: 1.0.0
homepage: https://clawic.com/skills/storytelling
description: Craft clear, emotionally resonant stories with audience-first framing, narrative arc control, and channel-specific rewrites.
changelog: Initial release with audience framing, story arc diagnostics, and channel-specific rewrite playbooks.
metadata: {"clawdbot":{"emoji":"📖","requires":{"bins":[],"config":["~/storytelling/"]},"os":["darwin","linux","win32"]}}
---

## Setup

On first use, read `setup.md` to align activation behavior, current storytelling goal, and audience context without delaying the immediate task.

## When to Use

User needs to explain, persuade, or teach through narrative and wants a story that is coherent, specific, and emotionally engaging.
Use this skill for product stories, founder narratives, case studies, speeches, long-form writing, and short content adaptations.

## Architecture

Memory lives in `~/storytelling/`. See `memory-template.md` for baseline structure.

```text
~/storytelling/
|-- memory.md                # Audience profile, active narrative goals, and constraints
|-- story-bank.md            # Reusable stories, scenes, and proof points
|-- messaging-pillars.md     # Core themes, promises, and supporting evidence
`-- edit-log.md              # Draft iterations, decisions, and what changed
```

## Quick Reference

Load only the smallest file needed to solve the current bottleneck.

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Memory structure and status model | `memory-template.md` |
| Arc design and narrative sequencing | `story-arc-map.md` |
| Scene construction and detail layering | `scene-design.md` |
| Format-specific adaptations and compression | `rewrite-modes.md` |
| Voice calibration and consistency checks | `voice-consistency.md` |

## Data Storage

Local notes in `~/storytelling/` may include:
- audience assumptions, emotional target, and success criteria
- bank of anecdotes, examples, and proof artifacts
- draft variants, edit decisions, and rejected directions
- reusable hooks, openings, transitions, and closings

## Core Rules

### 1. Anchor Every Story to One Audience Outcome
Define one concrete outcome before drafting:
- understand a complex idea
- believe a claim
- make a decision
- remember a key message

If the desired audience shift is not explicit, the story drifts into pleasant but ineffective prose.

### 2. Build a Causal Arc, Not a Topic List
Force each section to answer one of these transitions:
- context -> tension
- tension -> decision
- decision -> action
- action -> result

If two consecutive sections do not have a causal bridge, add one or remove one section.

### 3. Use Specific Evidence at the Point of Highest Skepticism
Place proof where disbelief is most likely:
- before major claims
- after bold promises
- inside turning points

Evidence can be data, concrete examples, constraints, trade-offs, or observed outcomes. Generic claims without proof collapse trust.

### 4. Control Emotional Pace with Scene Density
Alternate tight scenes and high-level summaries:
- tight scene for empathy and credibility
- summary passage for speed and direction

Overusing scenes slows momentum. Overusing summaries removes emotional impact.

### 5. Separate Drafting from Judgment
Run two explicit passes:
- pass A: generate material without heavy self-editing
- pass B: cut, reorder, and sharpen for clarity

Mixing ideation and critique in one pass usually creates safe, flat narratives.

### 6. Adapt Format Without Losing Core Story Logic
For every channel version, preserve:
- core conflict
- key decision
- core proof
- final implication

Short formats require compression, not simplification into vague slogans.

### 7. End with a Single Clear Action or Reflection
Close with one explicit endpoint:
- what to do next
- what to believe now
- what to watch for

A strong ending turns narrative quality into practical impact.

## Storytelling Traps

- Opening with background before stakes -> audience attention drops before the story starts.
- Adding too many subplots -> the central message becomes untraceable.
- Using abstract adjectives instead of concrete moments -> no mental image, low recall.
- Explaining every detail chronologically -> pacing slows and key turning points disappear.
- Rewriting tone without rechecking logic -> polished text with broken argument flow.
- Ending with broad inspiration only -> no decision, no behavior change, no result.

## Security & Privacy

Data that leaves your machine:
- none by default from this instruction set
- only user-approved outbound requests when the user explicitly asks for external research

Data that stays local:
- storytelling context and iterative notes under `~/storytelling/`
- draft structure choices and narrative experiments

This skill does NOT:
- request secrets, passwords, or private credentials
- make hidden network calls
- perform irreversible actions automatically

## Scope

This skill ONLY:
- structures narrative strategy for clarity, persuasion, and memorability
- improves story logic, evidence placement, pacing, and adaptation
- supports iterative drafting with explicit quality checks

This skill NEVER:
- fabricate facts or testimonials
- claim outcomes that evidence cannot support
- replace domain review when factual or legal accuracy is required

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `writing` - Improve writing quality with clearer structure and stronger revision passes.
- `content-marketing` - Connect stories to audience segments, funnel stages, and distribution plans.
- `storybook` - Create consistent narrative components for UI and product communication flows.
- `history` - Build context-rich historical narratives with chronology and source-aware framing.
- `youtube-video-transcript` - Turn transcript material into tighter narrative scripts and summaries.

## Feedback

- If useful: `clawhub star storytelling`
- Stay updated: `clawhub sync`
