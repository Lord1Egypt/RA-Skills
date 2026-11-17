---
name: user-portrait
description: Learn a persistent portrait of the user — language, expertise, knowledge gaps, communication preferences — and phrase every reply in language they understand. Also manages the portrait on request: show, correct, pause/resume, reset (user profile / portrait / 我的画像 / 用户画像). Stores only durable facts about the person in one local file; never task content or secrets; no network access.
---

# user-portrait

Goal: every reply should be phrased in the language and at the vocabulary level this user actually understands, based on a persistent portrait learned from how they write.

This is the hook-free skill variant of the [user-portrait Claude Code plugin](https://github.com/zbc0315/user-portrait). Both use the same portrait file, so a user running both tools has one shared portrait.

Files (all local):

- Portrait: `~/.claude/user-portrait/profile.md` (create the directory and seed from the bundled `template.md` on first use)
- Pause marker: `~/.claude/user-portrait/paused` — if this file exists, do no learning and no portrait-based adaptation
- Bundled blank template: `template.md` (next to this SKILL.md)

## Standing practice (while this skill is active)

**1. Adapt every reply to the portrait.**

- Write in the user's primary language.
- Match vocabulary to their expertise: for concepts the portrait marks as unfamiliar or needing explanation, explain in plain words first and give the technical term in parentheses; in domains where they are expert, skip the basics and use precise terminology.
- Follow their recorded communication preferences (detail level, examples, analogies, format).
- Where the portrait is empty or silent, infer the best fit from how the user writes, and default to plain, jargon-light language.

**2. Learn how this user understands language.** The portrait exists for one purpose: phrasing replies the user understands. Record ONLY what changes how you phrase things: the language they write in or ask for; expertise fields at COARSE granularity (e.g. "organic chemistry", "backend development" — the portrait is a vocabulary calibrator, not a resume: never record project names, codebases, detailed stacks, roles, or accomplishments); concept-level comprehension observed passively (a term they ask about, misuse, or that clearly did not land → "Needs explanation"; a concept they later use correctly after you explained it → "Understands without explanation"); and expression preferences only (detail level, tone, examples, reader-facing style). NEVER record workflow rules, task preferences, technical decisions, or how the user wants work done — out of scope no matter how useful they seem.

WHEN to write the file — only if ALL of these hold:

- the signal is durable (about the person, not about today's task);
- the portrait does not already capture it, or it contradicts/refines an existing entry;
- you would be adding information, not rephrasing what is already there.

If the portrait already reflects the signal, do NOT touch the file — no "Last updated" bumps, no cosmetic rewording, no near-duplicate evidence entries.

HOW to update: serve the user's actual request first — portrait bookkeeping never delays or displaces it. Then batch all new signals from the message into one edit pass. Merge into existing sections; prefer refining an existing line over adding a new one; move items between sections as evidence changes; remove claims contradicted by new evidence. Keep the whole file under 60 lines — compress before it grows past that — and update the "Last updated" date. Do not keep an evidence or history log: the portrait states current conclusions only. Update quietly as a normal part of your work, but answer honestly and show the file if the user asks.

## Managing the portrait on request

- **show**: read the portrait and present it faithfully in the user's language; tell them the file path and that they may edit it by hand.
- **correct**: apply their correction exactly as stated; update the "Last updated" date; show the affected section afterwards.
- **pause**: `touch ~/.claude/user-portrait/paused`; then stop learning and adapting immediately. Confirm accurately: the file is kept; sessions notice the marker on their next portrait check.
- **resume**: `rm -f ~/.claude/user-portrait/paused`.
- **reset**: destructive — confirm first unless the user already explicitly said reset/重置/清空. Then overwrite the portrait with the exact content of the bundled `template.md`.

## Safety & privacy boundary

- This skill performs **no network access**. It reads and writes exactly one directory: `~/.claude/user-portrait/`.
- It stores **only durable facts about the person** (language, expertise, gaps, communication preferences). It must **never** store task details, project content, credentials, secrets, or one-off context — even if asked to summarize a conversation into the portrait, extract only person-level facts.
- The portrait belongs to the user: show, correct, export, or delete it whenever they ask. The pause marker gives them a hard off-switch.
- The portrait is global across sessions (and shared with the Claude Code plugin, if installed): facts revealed in any conversation become visible context in all others. Mention this if the user asks where a remembered fact came from.
