---
name: smart-router-omni
description: Universal smart routing skill that chooses the best installed skill or skill chain across mixed environments, and automatically applies OpenClaw-aware routing when an OpenClaw workspace or skill inventory is detected. Use when the user asks which skill to use, when multiple skills overlap, when the task spans several phases, or when Codex should inspect local skill metadata and environment signals before choosing a route.
---

# Smart Router Omni

Start broad, then specialize. Default to universal routing, and switch into OpenClaw-aware mode when the environment supports it.

## Load the right reference

- Read `references/scoring-rubric.md` before scoring candidates.
- Read `references/ambiguity-and-fallbacks.md` when confidence is weak or constraints are missing.
- Read `references/environment-detection.md` before deciding whether to stay in universal mode or enter OpenClaw mode.
- Read `references/chain-patterns.md` when the request obviously spans several phases.
- Read `references/research-notes-2026-03.md` when you need the design rationale.

## Workflow

1. Normalize the request into a task card:
   - goal
   - expected artifact
   - domain
   - required actions
   - constraints
   - environment dependencies
2. Detect the environment using `references/environment-detection.md`:
   - universal mode
   - OpenClaw-aware mode
3. Scan visible skill roots conservatively:
   - read `SKILL.md` frontmatter first
   - inspect `agents/openai.yaml` only for shortlisted candidates
4. Apply hard filters before ranking:
   - missing tools
   - missing login or auth
   - wrong output type
   - platform mismatch
   - safety or policy mismatch
5. Score viable candidates with `references/scoring-rubric.md`.
6. If one skill can finish the task, recommend that skill.
7. If the task spans phases, recommend a short chain using `references/chain-patterns.md`.
8. If confidence is low, ask compact clarification questions instead of forcing a route.
9. Output:
   - recommended skill or chain
   - confidence
   - why it won
   - prerequisites
   - fallbacks
   - clarifying questions if needed

## Routing policy

- Prefer explicit capability claims in `description` over name similarity.
- Prefer specialist skills when the task, artifact, and dependencies are clear.
- Prefer workflow skills when the request is end-to-end.
- Prefer the smallest route that can finish the task well.
- In OpenClaw-aware mode, treat browser, publishing, memory, and account-bound skills as dependency-sensitive.
- Abstain and clarify when the top candidates are close.

## Standard output

```md
[Routing Decision]
Mode: universal | openclaw-aware
Request: ...
Recommended skill: ...
Confidence: high | medium | low
Why it fits: ...
Missing checks or prerequisites: ...
Fallbacks: ...
Suggested chain: ...
Clarifying question(s): ...
```

## Guardrails

- Do not rely on a fixed handwritten route table as the primary method.
- Do not read every full `SKILL.md` before shortlisting.
- Do not recommend unavailable skills.
- Do not hide uncertainty when the top candidates are close.
- Do not force one skill when a chain is clearly better.

## Exit condition

Finish with one recommended skill or skill chain, an explicit mode, a confidence level, key reasons, fallbacks, and any blocking unknowns.

---

## Copyright & License

**Copyright (c) 2026 龙虾 (Lobster)**

**All Rights Reserved.**

This skill is proprietary and confidential. The source code, algorithms, documentation, and any accompanying materials are protected by copyright law and international treaties.

**You may NOT:**
- Copy, modify, or distribute the source code or documentation
- Create derivative works based on this skill
- Use this skill as a template or baseline for developing competing products
- Reverse engineer, decompile, or disassemble any components
- Remove or alter any proprietary notices or copyright labels

**You MAY:**
- Install and use this skill in your OpenClaw installation
- Receive updates and support as provided by the author

For licensing inquiries or custom development, contact the author directly.
