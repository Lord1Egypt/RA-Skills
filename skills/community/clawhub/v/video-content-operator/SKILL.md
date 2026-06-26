---
name: video-content-operator
description: Use when a user wants help deciding what video/social content to make, how to package it for different platforms, which source materials or ideas are worth using, or what the next content move should be. This skill is for creator operating decisions above editing execution. It should be used for requests like: plan this week's content, decide which clips are worth turning into posts, package an idea for Xiaohongshu/Shorts/YouTube, generate draft content directions, compare angles, recommend the next post, or analyze a creator's current content situation. Before giving recommendations, first understand the user's current state: who they are, which platforms they are already using, what kinds of content they usually publish, and what problem they are trying to solve. In OpenClaw main sessions, proactively use memory files to understand the user before making recommendations. Do NOT use this skill for pure execution when the user already knows exactly what to edit; defer actual editing to sparki-video-editor or other execution tools.
---

# Video Content Operator

This skill sits **above** video editing.

Its job is to help the user decide:
- what content to make
- what source material is worth using
- how to package it
- which platform/version to optimize for
- what the next content move should be

It is **not** the video renderer itself.
If the user already knows exactly what to edit and only needs execution, use `sparki-video-editor` or the execution tool directly instead.

## Core idea

Treat this as a **content operating layer**, not just an editing helper.

Minimum loop:
1. understand the creator's current state
2. clarify the real goal
3. evaluate candidate materials / ideas
4. recommend one best content direction
5. generate 1-3 draft content packages
6. recommend next action
7. if approved, hand off execution cleanly

## First step: understand the creator before advising

Do **not** jump into content advice without first understanding the user's current situation.

You should first determine:
- who this creator is
- what they are trying to build
- which platforms they already use
- what content they usually publish
- what their current bottleneck is

### In OpenClaw main sessions

If you are in the user's main/private session, proactively use available memory/context before asking questions.

Look for signals about:
- mission / positioning
- current product or business
- current content channels
- recurring themes or pillars
- preferred tone
- previous strategy discussions

Do not ask questions that memory already answers.

### Ask only what is still decision-critical

After checking memory/context, only ask for missing information that materially changes the recommendation.

Good examples:
- "Right now, are you optimizing more for trust, growth, or conversion?"
- "Which platform matters most in the next 2 weeks?"
- "Are these materials for personal brand, product marketing, or both?"

Bad examples:
- asking who they are when you already know
- asking which platforms they use when memory/context already says it
- asking broad open-ended questions that do not affect the next decision

## When to use this skill

Use this skill when the user asks things like:
- "Help me decide what content to make"
- "Which of these materials are worth turning into content?"
- "Package this for Xiaohongshu / Shorts / YouTube"
- "Give me draft directions, not just editing"
- "What should I post next?"
- "Turn these notes/materials into a content package"
- "Analyze my current content situation"
- "I want help operating my content, not just producing one video"

Do **not** use this skill when the request is only:
- "剪这个视频"
- "add captions"
- "turn this file into a 30s reel"
- any other pure execution request with already-decided edit intent

## Required output structure

Unless the user explicitly asks for something else, produce output in this structure:

### 1. Current state
- who the creator is
- current platforms/content pattern
- current bottleneck

### 2. Operating goal
- one sentence on the real goal right now

### 3. Best content direction
- what to make now
- why this is the best move

### 4. Recommended source material
- which assets/ideas to use
- which to ignore for now

### 5. Draft packages
Provide 1-3 options. For each option include:
- angle
- hook
- structure
- platform fit
- title/caption direction
- why this option exists

### 6. Next action
Choose one:
- refine
- execute with editing tool
- hold
- collect better material

Keep it concise. Only include information that changes the decision.

## First-principles rules

- Do not assume the user already knows the correct content goal.
- If the goal is unclear, stop and resolve the goal first.
- If the user asks for a path that is not the shortest path, say so and suggest the shorter one.
- Optimize for creator outcome, not surface polish.
- Prefer one strong content recommendation over many weak ones.
- Separate **decision** from **execution**.
- Advice should be based on creator context, not generic platform clichés.

## Operating questions

Before recommending content directions, anchor on these questions:
- Who is this creator, really?
- What are they trying to build right now?
- Which platform matters most right now?
- What is the real goal: trust, growth, conversion, proof, or documentation?
- What is the strongest available source material?
- Why now?
- Is this content better as insight, story, demo, commentary, or proof?

If any of these are unclear and materially affect the answer, ask briefly before proceeding.

## Platform framing

Use these defaults unless the user says otherwise:
- **Xiaohongshu**: emotional clarity, personal relevance, first-screen clarity
- **Shorts / Reels / TikTok**: fast hook, high compression, obvious contrast
- **YouTube**: stronger narrative arc, more context, more explicit thesis

Do not overfit to stereotypes. Use them only as starting priors.

## Draft package format

When generating draft options, keep each one structured like this:

- **Angle**: what this piece is really about
- **Hook**: opening line / opening moment
- **Structure**: 3-5 beat outline
- **Platform fit**: where it belongs first
- **Packaging**: title / caption direction
- **Why this works**: one short reason

## Hand-off to execution

If the user approves one direction and wants the content made, hand off cleanly to the right execution layer.

When handing off to `sparki-video-editor` or another video execution tool, convert the chosen package into an execution brief with:
- selected source materials
- target platform
- target duration
- edit mode
- preferred style or prompt
- any constraints to preserve

Suggested hand-off shape:
- Goal: ...
- Source material: ...
- Platform: ...
- Duration: ...
- Style/prompt: ...
- Must preserve: ...

## Scripts

### `scripts/extract_creator_context.py`
Use this first when you are in an OpenClaw workspace and need a fast draft of creator state from local memory files.

It extracts a lightweight JSON context from:
- `MEMORY.md`
- `USER.md`

Use it to avoid asking questions that local context already answers.

Example:
```bash
python3 scripts/extract_creator_context.py --workspace /Users/fischer/.openclaw/workspace
```

### `scripts/content_operator.py`
Use this to turn creator context + goal + materials into a structured operating recommendation package.

Example:
```bash
python3 scripts/content_operator.py --input /path/to/input.json
```

### `scripts/build_execution_brief.py`
Use this after a content package is accepted and you want a clean hand-off to a video execution skill.

Example:
```bash
python3 scripts/build_execution_brief.py --input /path/to/operator-output.json
```

## References

If you need more structure, read:
- `references/mvp.md` for MVP scope and boundaries
- `references/mvp-spec.md` for product/spec framing
- `references/output-examples.md` for example responses and hand-off patterns
- `references/input-schema.md` for JSON input shape
- `references/implementation-notes.md` for current implementation status
ts/content_operator.py --input /path/to/input.json
```

### `scripts/build_execution_brief.py`
Use this after a content package is accepted and you want a clean hand-off to a video execution skill.

Example:
```bash
python3 scripts/build_execution_brief.py --input /path/to/operator-output.json
```

## References

If you need more structure, read:
- `references/mvp.md` for MVP scope and boundaries
- `references/output-examples.md` for example responses and hand-off patterns
- `references/input-schema.md` for JSON input shape
- `references/implementation-notes.md` for current implementation status
