---
name: wireframing
description: Deep wireframing workflow—problem framing, fidelity choice, flows and edge cases, IA and components, critique and iteration, handoff to design/dev. Use when exploring layouts before visual design or aligning stakeholders quickly.
---

# Wireframing (Deep Workflow)

Wireframes are shared thinking tools—not decoration. The goal is alignment on structure, priority, and flows at low rework cost before pixels and code.

## When to Offer This Workflow

**Trigger conditions:**

- New feature with unclear information architecture or many UI states
- Stakeholders disagree on scope or number of screens
- Fast iteration needed before high-fidelity visual design
- Technical constraints (API shape, permissions) must shape the UI early

**Initial offer:**

Use **six stages**: (1) define intent and fidelity, (2) map users and scenarios, (3) structure and navigation, (4) key screens and states, (5) critique and test, (6) handoff. Ask which tool they use (FigJam, Figma, paper, Excalidraw) and the deadline.

---

## Stage 1: Define Intent & Fidelity

**Goal:** Match fidelity to the question being answered.

### Levels

- **Thumbnail flow**: minutes only—steps and sequence
- **Low-fi boxes**: layout and rough component placement
- **Mid-fi**: realistic copy placeholders and density—still grayscale

### Anti-patterns

- **Too polished too early**—stakeholders anchor on color instead of structure
- **Untitled flows**—reviewers lose context

**Exit condition:** Reviewers know whether to judge flow, layout, or both in this round.

---

## Stage 2: Map Users & Scenarios

**Goal:** One primary user and job-to-be-done per flow; edge cases listed explicitly.

### Activities

- Lightweight personas—only traits that change the UI (permissions, expertise)
- Scenarios as short stories: trigger → actions → success or failure
- Out-of-scope scenarios called out to prevent scope creep in wire review

**Exit condition:** Three to seven scenarios ranked; must-have vs later is clear.

---

## Stage 3: Structure & Navigation

**Goal:** Information architecture before screen-level detail.

### Practices

- Sitemap or nav model: where the feature lives; deep-link expectations
- Naming: labels consistent with the user’s mental model; avoid internal jargon unless users know it
- Decide early if mobile and desktop diverge—don’t let it happen by accident

**Exit condition:** Nav entry points and breadcrumbs sketched.

---

## Stage 4: Key Screens & States

**Goal:** Cover the happy path plus critical empty, loading, error, and permission-denied states.

### Checklist per screen

- One clear primary CTA; secondary actions de-emphasized
- Empty: educate and offer a next step; loading: skeleton vs spinner chosen deliberately
- Error: recovery path; permission denied: why and what to do next

### Annotations

- Numbered callouts for open questions—do not hide ambiguity

**Exit condition:** State matrix for the top three screens (rows = states).

---

## Stage 5: Critique & Test

**Goal:** Structured feedback—not only subjective taste.

### Review script

- Five-minute silent read first
- Round-robin: confusion points and missing paths
- Capture decisions; assign owners for open questions

### Lightweight usability

- Click-through prototype or paper walkthrough with one or two users when risk is high

**Exit condition:** Prioritized change list; open questions tracked.

---

## Stage 6: Handoff

**Goal:** Smooth handoff to visual design and engineering.

### To design

- Grid assumptions, responsive breakpoints, content priority order

### To engineering

- API dependencies; UI states that affect backend behavior (pagination, filters)
- Accessibility notes: focus order, live regions for dynamic updates

### Artifacts

- Link to a single source file; version snapshot or changelog entry when the handoff is formal

---

## Final Review Checklist

- [ ] Fidelity matches review goals
- [ ] Scenarios and edge states covered for critical flows
- [ ] IA and navigation coherent
- [ ] Empty, loading, error, and permission states considered
- [ ] Handoff notes for design and dev

## Tips for Effective Guidance

- Content-first where possible—placeholder lorem ipsum often mis-sizes real copy.
- Label screens and flows; reviewers often join mid-stream.
- Encourage disposable wires—speed beats beauty at this stage.

## Handling Deviations

- **Existing design system**: sketch with component skeletons even at low-fi—reduces surprise later.
- **Tiny UI tweak**: skip the full workflow—a single annotated screen may suffice.
