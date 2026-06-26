---
name: frontend-design-ui-ux
version: 3.1.0
description: |
  Produce a distinctive, LOCKED design language plus an implementation-ready UX/UI spec, written to
  `.ulpi/design/`: a per-brief visual identity (palette, type, signature), the design system to build
  on, user flows and states, component briefs, and accessibility constraints. Commits to a bold
  aesthetic direction, bans AI-slop by name, and locks the identity so every screen and future session
  stays consistent. Can visit inspiration links with the browse skill to extract real design DNA. Ends
  with a build handoff that a delegated engineering agent implements. Use for new features, redesigns,
  or design-system work. This is a DESIGN-SPEC skill — it does not write production UI code.
allowed-tools:
  - AskUserQuestion
  - Read
  - Write
  - Skill
argument-hint: "[feature, screen, or design problem] (+ optional inspiration URLs)"
arguments:
  - request
when_to_use: |
  Use when the user wants interface design, flow design, component specification, a design language,
  or design-system work rather than direct implementation. Examples: "design this dashboard", "spec
  the onboarding flow", "give this product a visual identity", "make this look less generic", "design
  it like <url> and <url>". Do not use to write production UI code — hand the spec to an engineer.
effort: high
---

<EXTREMELY-IMPORTANT>
This is a DESIGN-SPEC skill, not an implementation skill. Non-negotiable rules:
1. Do NOT write production UI code from this skill. Produce a spec + a locked design language and DELEGATE
   the build to an engineering agent. We own the design spec; the agent implements it.
2. Commit to ONE distinctive aesthetic identity BEFORE specifying screens, and pass the counterfactual
   default test: if you'd produce this same look for any similar brief, it's a default — change it.
3. Ban AI-slop BY NAME (`references/anti-slop.md`). The slop test gates the work: if someone could say
   "AI made that" with no doubt, it failed.
4. LOCK the design language in `DESIGN.md` and bind every screen to it. Variation within identity,
   NEVER between. Re-read `DESIGN.md` first on every later feature or session.
5. If the user gives inspiration links, VISIT them with the `browse` skill and synthesize — never clone
   a single reference, and never inherit its slop.
6. Run the Design Pre-Flight gate before handoff. If a single box can't be honestly ticked, it is not done.
7. Keep the rigor that sets us apart: state coverage, flows/edge cases, and accessibility — never skip them.
</EXTREMELY-IMPORTANT>

# frontend-design-ui-ux

## Inputs

- `$request`: Feature, page, component, or UX problem to design — plus optional inspiration URLs.

## Goal

Produce a design package that is **distinctive, consistent, and buildable** — a spec a delegated
engineering agent implements directly. All artifacts are written under `.ulpi/design/`:

- `.ulpi/design/DESIGN.md` — the locked design language (identity, palette, type, scales, signature,
  voice, chosen design system). Project-wide; re-read first every session.
- `.ulpi/design/<feature>.md` — the per-feature spec: user flows + states, component specs, and the
  build handoff (target agent + acceptance criteria). Binds to `DESIGN.md`.

## Step 0: Discovery & inputs

Resolve: target users · product goal · device/usage context · existing design-system or brand
constraints · accessibility expectations. Ask once: **"Any reference sites or designs you admire?
Paste 1–4 URLs."**

If the problem is underspecified, ask — but at most a couple of focused questions; never a long
interrogation. **Success criteria**: the problem is framed in user + product terms, and inspiration
links (if any) are collected.

## Step 1: Inspiration intake (optional)

If the user gave links, VISIT each with the `browse` skill, extract its design DNA (type, color, shape,
spacing, layout), and distill a one-line DNA note per site. Synthesize across them — never clone one.
If `browse` is unavailable or a link is unreachable, ask the user to describe the vibe and proceed.

Load `references/inspiration-intake.md`. **Success criteria**: each reference reduced to reusable DNA,
with what to take and what to reject — or cleanly skipped.

## Step 2: Design Read & aesthetic direction

Approach as a design lead who would never ship a templated look. Kill the default-aesthetic reflex
before any tokens:

- Emit a one-line **Design Read** (the feeling + the bet).
- Commit to **one named aesthetic direction** from the menu in `references/anti-slop.md`; justify it
  from the brief (and the inspiration DNA, if any).
- Run the **counterfactual default test**: would this look be your answer for ANY similar brief? If so,
  change it.
- Optionally set taste dials (`design_variance` / `motion_intensity` / `visual_density`, 1–10) and
  **match complexity to the direction** (maximalist → elaborate; minimal → restraint, precision, whitespace).

Load `references/anti-slop.md` for the direction menu, the pattern vocabulary, and the named bans.
**Success criteria**: a committed, brief-specific direction that is not a generic default.

## Step 3: Derive & LOCK the design language → write `.ulpi/design/DESIGN.md`

Decide the **register** (brand vs product) and, for `product`, the **design system** to build on (see
`references/design-system-routing.md`). Then derive and LOCK the identity: palette (OKLCH, tinted
neutrals, 60-30-10, WCAG-checked), type roles paired on a contrast axis, ONE spacing/radius/motion
scale, the **Signature**, and the voice. Write it to `.ulpi/design/DESIGN.md` — the consistency source
of truth every screen binds to.

Load `references/design-language-lock.md` (artifact + lock rules), `references/design-tokens-template.md`
(derivation method), and `references/design-system-routing.md` (brief→system map). **Success criteria**:
a complete, locked `.ulpi/design/DESIGN.md`; no generic default identity.

## Step 4: Model flows and states

Document the primary journey, branching/decisions, and the full state model — loading, empty, partial,
success, error — plus edge cases (refresh, session expiry, back, offline). Write into
`.ulpi/design/<feature>.md`. Use `references/user-flow-template.md`. **Success criteria**: behavior is
covered across states, not just the happy path.

## Step 5: Specify components and interaction rules

For each component define: purpose, variants, props/data, states, interaction feedback, responsive
behavior, and accessibility (ARIA, keyboard, screen-reader, focus). Bind every visual value to
`.ulpi/design/DESIGN.md`; append into the same `.ulpi/design/<feature>.md`. Use
`references/component-spec-template.md`. **Success criteria**: a delegated engineer can build it without
guessing, and nothing drifts from the locked identity.

## Step 6: Design Pre-Flight gate

Run `references/design-preflight.md` end to end — identity lock, anti-slop, state coverage,
accessibility, layout craft, cognitive load, and the scored self-critique. Several items are mechanical
counts. Fix any failing box or any axis scored ≤ 2, state in one line WHAT you changed and WHY
(revise-and-justify), then re-run. **Success criteria**: every box ticked and no critique axis ≤ 2.

## Step 7: Build handoff (delegate the build)

Finalize the delegation brief at the end of `.ulpi/design/<feature>.md`: the target engineering agent,
the chosen `design_system` (+ its setup note), and the acceptance criteria — with the instruction:
*"Implement exactly this spec. Theme the design system with our locked tokens; do NOT redesign or
re-implement its components."* The building is delegated to the agent; this skill never writes the UI.

### Agent Selection

| Criteria | Target Agent |
|----------|-------------|
| Server-side rendering / SEO / App Router / Server Actions | `nextjs-senior-engineer` |
| Pure SPA / client-only / CLI web UI / Electron-Tauri | `react-vite-tailwind-engineer` |
| Static site with no SSR | Either (ask user) |
| Unclear | Ask user |

**Success criteria**: a delegated agent can pick up `.ulpi/design/DESIGN.md` + `.ulpi/design/<feature>.md`
and implement it directly, without redesigning.

## Guardrails

- Do not implement production UI code from this skill; produce the spec and hand off.
- Do not ship a generic default identity — derive palette and type per brief; the slop test gates output.
- Do not let screens drift from `DESIGN.md`: variation within identity, never between.
- Do not clone a single inspiration reference, and never inherit its slop.
- Do not skip accessibility, state coverage, or responsive behavior — they are our edge.
- Do not produce vague design prose when a concrete artifact is needed.
- Do not block if `browse` or an image tool is absent — degrade gracefully and proceed from the brief.

## When To Load References

- `references/inspiration-intake.md` — visiting reference links with `browse` and extracting DNA (Step 1).
- `references/anti-slop.md` — the direction menu, named AI-slop bans, and the slop test (Steps 2, 3, 6).
- `references/design-language-lock.md` — the `DESIGN.md` artifact and the consistency lock rules (Step 3).
- `references/design-system-routing.md` — the brief→design-system map + honesty rule (Step 3, product register).
- `references/design-tokens-template.md` — the per-brief color/type derivation method + neutral scales (Step 3).
- `references/user-flow-template.md` — user journeys and acceptance flows (Step 4).
- `references/component-spec-template.md` — component briefs and interface contracts (Step 5).
- `references/design-preflight.md` — the pre-handoff quality + consistency gate (Step 6).

## Output Contract

Write under `.ulpi/design/` and report:

1. the Design Read + committed aesthetic direction (and inspiration DNA, if any)
2. `.ulpi/design/DESIGN.md` — the locked design language (register, design system, palette, type, scales, signature, voice)
3. `.ulpi/design/<feature>.md` — flows and states
4. — component specs (same file)
5. Pre-Flight result (every box ticked, no critique axis ≤ 2)
6. build handoff — target agent + design system + acceptance criteria ("implement exactly this; do not redesign")
