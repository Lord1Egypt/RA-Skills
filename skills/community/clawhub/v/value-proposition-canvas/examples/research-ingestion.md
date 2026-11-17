---
title: Use Case 1 — Research Ingestion (v2.0)
canvas_side: workflow_example
use_case: user_has_data
pattern: data_to_profile_to_value_map_to_framework
skill: value-proposition-canvas
version: 2.0
created: 2026-07-09
---

# Use Case 1: Research Ingestion — "You have user data, need a full VPC"

## Scenario

You are a product designer. You have spent the last two weeks talking to 5 designers who fit your target audience. Each interview is a 30-minute semi-structured conversation. You have transcripts, messy notes, and a few highlight quotes.

You come to the workshop with:
- 5 transcripts in your project folder.
- A vague product idea in your head (no commitment to a name yet).
- The recognition that the interviews revealed something, but you are not sure what.

The skill runs through **Phase 1 (Customer Profile)** + **Phase 2 (Value Map, three substeps)** + **Phase 2.5 (Framework Selection)**. The output is a fully-mapped VPC table with explicit user acceptance gates between every step. The skill ends at "framework selected, ready for Kano".

This is the **primary use case** of the `value-proposition-canvas` skill. The skill does not invent; it structures.

---

## Step 0 — Output location (HARD WAIT)

Before anything else, the agent asks:

> *"This workshop will produce three files:
> 1. `vpc-result.md` — the workshop source-of-truth
> 2. `shadow-backlog.md` — a starter file with the Pain Relievers + Gain Creators, ready for Kano
> 3. `value-proposition.md` — for your UVP (you write it after Kano, not me)
>
> Where should I save them? (default: current working directory)"*

You answer: *"./project-pat/"*.

The agent confirms: *"Saving to ./project-pat/. Three files: vpc-result.md, shadow-backlog.md, value-proposition.md."*

## Step 1 — First clarifying question (HARD WAIT)

The agent asks:

> *"Are we designing for a specific persona (one user type, named like Pat) or for a whole segment (a category of users like 'indie designers building SaaS')?"*

The agent **does nothing** until the user answers. The agent does not extract, does not probe, does not assume.

You answer: **"Persona. Pat — an indie designer, 3 years experience, ships one product at a time, uses Figma and shadcn, talks to 2-3 engineers per release."**

The agent now knows: one canvas, one Pat. The evidence pool is whatever Pat-similar quotes appear in the transcripts.

---

## Step 2 — Persona sharpening (if needed)

The agent checks the persona is a behavioral profile, not a demographic. It asks 3-5 sharpening questions if needed:

> *"What does Pat do in a typical day, in their own workflow?"*
> *"What tool does Pat reach for first when they sit down to design?"*
> *"What does Pat wish was different about their work, even if they have never said it out loud?"*

You answer. The agent refines the persona:

> **Pat (refined)**: A product designer who ships one product at a time, alone or with 2-3 engineers. Uses Figma for design, shadcn for components, and Slack for everything else. Spends ~40% of their time in the design tool, ~30% explaining the design to engineers, ~20% in meetings about the design, and ~10% on everything else. The 30% "explaining" time is the suspected pain.

---

## Step 3 — Phase 1: Customer Profile

### Step 3.1 — Extract Jobs, Pains, Gains

The agent reads the transcripts and extracts three tables. Every row has a verbatim source quote. Rows are sorted by frequency/importance (dominant at top).

**Number rules applied:** 1-2 main Jobs + 3-5 supporting Jobs; 3-5 Pains; 3-5 Gains.

#### Jobs table

| # | Priority | Customer Job (one sentence) | Type | Verbatim source quote | Status |
|---|---|---|---|---|---|
| J1 | Main | Hand off designs to engineering without rework | Functional | *"I spend 8 hours per component on Slack explaining to the engineer what state I am in."* (Q1) | Locked |
| J2 | Main | Be seen as a credible technical partner by the dev team | Social | *"I write a 50-page Notion doc per release. The engineer reads page 1, then asks me everything else in DMs."* (Q2) | Locked |
| J3 | Supporting | Feel confident the implementation will match the design | Emotional | *"I wish I could just send one link that contains everything — the design, the states, the why, the test cases."* (Q4) | Locked |
| J4 | Supporting | Reduce the time spent explaining (so the time goes to designing) | Functional | *"I spend 8 hours per component on Slack explaining to the engineer what state I am in."* (Q1) | Hypothesis (1/5) |

**Hypothesis flagged:** J4 has only 1/5 source support. Same quote as J1; the agent merged the framing.

#### Pains table

| # | Priority | Pain (one sentence) | Severity | Frequency | IxDF Category | Quantified unit | Verbatim source quote | Status |
|---|---|---|---|---|---|---|---|---|
| P1 | Dominant | 8 hours per component on Slack explaining the Figma file | 5 | per component | Dissatisfaction | 8 hours per component | *"I spend 8 hours per component on Slack explaining to the engineer what state I am in."* (Q1) | Locked |
| P2 | Dominant | 60% rework rate; v2 spec needed within a week | 5 | per component | Challenge | 60% rework | *"When I hand off, the engineer guesses. The implementation is wrong 60% of the time. I write a v2 spec within a week."* (Q3) | Locked |
| P3 | Dominant | AI coding agents hallucinate state behavior | 4 | per component | Challenge | n hallucinations per component | *"The AI coding tool hallucinates state behavior because the spec is just a Figma file."* (Q5) | Locked |
| P4 | Secondary | 50-page Notion spec is unread | 4 | per release | Barrier | 1/50 pages read | *"I write a 50-page Notion doc per release. The engineer reads page 1, then asks me everything else in DMs."* (Q2) | Locked |

#### Gains table

| # | Priority | Gain (one sentence) | Expectation | Outcome type | Verbatim source quote | Status |
|---|---|---|---|---|---|---|
| G1 | Dominant | Ship a component without rework | Required | Functional | *"I wish I could just send one link that contains everything — the design, the states, the why, the test cases."* (Q4) | Locked |
| G2 | Dominant | Send one link that contains design + spec + states + test cases + a11y | Desired | Functional | *"I wish I could just send one link that contains everything — the design, the states, the why, the test cases."* (Q4) | Locked |
| G3 | Dominant | AI coding tool gets it right on the first try | Desired | Functional | *"If the AI coding tool just got it right on the first try, my whole workflow would change. Right now it hallucinates because the spec is just a Figma file."* (Q5) | Locked |
| G4 | Secondary | Be recognized as a credible technical partner | Unexpected | Social | *"The engineer reads page 1, then asks me everything else in DMs. By week 2 the Notion is stale."* (Q2) | Hypothesis (1/5) |

**Osterwalder rules applied:**
- **Rule A** (gains are not the result of the job): "I have learned new design skills" is the result; "send one link" is the gain.
- **Rule B** (gains are not the inverse of pains): "Don't have rework" is the absence of the pain; "ship a component without rework" is the gain.

### Step 3.2 — GATE — explicit user accept

The agent posts the three tables and waits. The user can:
- **Accept** ("looks good, proceed")
- **Add** ("add a Pain I forgot")
- **Drop** ("drop P3, no evidence")
- **Rephrase** ("rewrite P2, the framing is wrong")
- **Mark hypothesis** ("I'm not sure about J4, mark hypothesis")

You respond:

> *"Looks good. Move G4 to Locked — actually the second sentence of Q2 implies the social gain is real. And J4 is the same quote as J1; drop J4, it's a duplicate."*

The agent updates the tables. The Customer Profile is **locked**.

---

## Step 4 — Phase 2: Value Map

### Step 4.0 — GATE

Phase 1 is locked. Phase 2 begins.

### Step 4.1 — Map Pains → Pain Relievers (Phase 2.1)

The agent proposes **one Pain Reliever per locked Pain** (1:1 mapping, no orphans). Pain Relievers are **features**, not bundles.

**Pain Relievers table:**

| # | Pain addressed | Pain Reliever (feature) | Mechanism | Status |
|---|---|---|---|---|
| R1 | P1: 8 hours per component on Slack | Single-link handoff page | A static page that bundles the Figma frame + spec + states + test cases + a11y, shareable as one URL. Dev reads the page, not the Figma file. | Proposed |
| R2 | P2: 60% rework rate | spec.md generator from Figma | A Figma plugin reads the file and emits a structured markdown spec: states, edge cases, accessibility decisions, test cases. | Proposed |
| R3 | P3: AI agents hallucinate | Machine-readable spec schema for AI tools | A JSON Schema derived from spec.md that AI coding agents can consume directly. | Proposed |
| R4 | P4: 50-page spec unread | spec confidence score | A heuristic that flags how complete / unambiguous the spec is before the dev picks it up. | Proposed |

### Step 4.2 — GATE — explicit user accept

You respond:

> *"R3 and R4 are good. But R1 and R2 both feel weak — they describe the feature but not how it eliminates the Pain. R1: 'A static page that bundles...' — how does that eliminate '8 hours on Slack'? The mechanism is: dev reads the page, so the dev doesn't have to ask. Make it concrete. Same for R2: the v2 spec is needed because the engineer guesses. The mechanism is: spec-driven diff review forces the engineer to read the diff before guessing."*

The agent rewrites R1 and R2 with concrete mechanisms. The Pain Relievers table is **locked**.

### Step 4.3 — Map Gains → Gain Creators (Phase 2.3)

The agent proposes **one Gain Creator per locked Gain** (1:1 mapping, no orphans, multi-tag allowed).

**Gain Creators table:**

| # | Gain produced | Gain Creator (feature) | Mechanism | Multi-tag | Status |
|---|---|---|---|---|---|
| C1 | G1: ship without rework | spec-driven diff review | When the spec changes, the dev sees a diff against the previous version and implements the diff. | (none) | Proposed |
| C2 | G2: send one link with everything | single-link handoff page (overlap with R1) | Same feature as R1 — multi-tag is allowed. | also R1 | Proposed |
| C3 | G3: AI tool gets it right | spec schema + AI agent prompt library | A pre-built prompt template that wraps the spec schema and tells the AI agent exactly what to consume. | (none) | Proposed |
| C4 | G4: recognized as credible partner | public portfolio of design decisions | A public page showing the spec + rationale + outcome, as evidence of credible technical work. | (none) | Proposed |

**Multi-tag flagged:** C2 and R1 are the same feature (single-link handoff page). This is allowed and even encouraged — a feature that addresses both a Pain and a Gain is high-value.

### Step 4.4 — GATE — explicit user accept

You respond:

> *"C2 and R1 overlap is correct. C3 prompt library is a good addition. C4 portfolio is good but might be premature — mark it as a wildcard for now, not a committed Gain Creator."*

The agent moves C4 to a Wildcards section, not a committed Gain Creator. The Gain Creators table is **locked**.

### Step 4.5 — Map Jobs → Products & Services (Phase 2.5)

The agent proposes **1-3 bundle items** (the offering shape, not features).

**Critical distinction:** Products & Services is the **bundle** — the physical shape of what the customer acquires. Pain Relievers and Gain Creators are features inside the bundle. The agent must not list every feature as a separate "product".

**Products & Services table:**

| # | Bundle item | What the customer receives | Type | Contract | Jobs supported |
|---|---|---|---|---|---|
| S1 | spec.md generator (Figma plugin + code-side parser) | A Figma plugin + a parser that emits a structured `spec.md` per component (states, edge cases, a11y, test cases) | Digital | License (per seat, annual) | J1, J2 |
| S2 | single-link handoff page | A web app that bundles design + spec + states + test cases + a11y into a shareable URL | Digital | Free tier + Pro subscription | J1, J3 |
| S3 | spec.md templates library | A pack of pre-built templates per component type (form, modal, list, etc.) | Digital | One-time purchase | J2, J3 |

### Step 4.6 — GATE — explicit user accept

You respond:

> *"S1 and S2 are right. S3 is a nice-to-have but might confuse the bundle — drop S3, the templates can be a free marketing asset, not a paid product. Update the bundle to S1 + S2 only."*

The agent drops S3. The Products & Services table is **locked**.

---

## Step 5 — Phase 2.7: Framework Selection (final gate)

The agent asks:

> *"Phase 2 is complete. You have 3 Pain Relievers + 3 committed Gain Creators (= 4 features, with 1 multi-tag overlap) + 1 wildcard + 2 bundle items. To decide which to build first, you need a prioritization framework. Which framework would you like to use?"*

The agent proposes **Kano Model Strategist** as the default and explains how it works:

> *"Kano Model Strategist (the next skill in this playbook) classifies features into six categories based on customer satisfaction:*
>
> *- **Must-be (basic):** features the customer expects. Absence causes rejection. These are non-negotiable baseline.*
> *- **Performance (one-dimensional):** more is better. Customer satisfaction scales linearly. Investment here is rational but not differentiating.*
> *- **Attractive (delighters):** unexpected positives. Absence does not cause dissatisfaction; presence causes delight. These are the differentiators that drive your eventual UVP.*
> *- **Indifferent:** the customer does not care either way. Skip.*
> *- **Reverse:** some customers actively dislike. Cut.*
> *- **Questionable:** the data is unclear. Needs more research.*
>
> *Kano is a great default for VPC outputs because it tells you which features are the Attractive ones — the ones that go into your UVP. Run `kano-model-strategist` next."*

You respond:

> *"Kano. Confirmed."*

The framework is selected. The skill ends.

---

## Step 6 — Workshop end

The skill produces **three files** in `./project-pat/`:

1. `vpc-result.md` — the workshop source-of-truth, with:
   - Customer Profile (locked, all 4 Pains + 4 Gains, with verbatim quotes)
   - Value Map (3 Pain Relievers + 3 Gain Creators + 2 bundle items, 1 multi-tag overlap flagged)
   - Framework selection (Kano)
   - 1 wildcard parked (C4: public portfolio)
   - 1 Open Question (the C3 prompt library prompt template — needs more research)

2. `shadow-backlog.md` (starter, written by the agent) — with the Pain Relievers + Gain Creators (= features) listed as rows, **without priorities**. Status: `starter`. The user (or `kano-model-strategist`) fills in the Kano classifications and priorities next.

3. `value-proposition.md` — **not written by the agent.** The user writes this after Kano, using the Osterwalder formula. Status: `draft` (until the user reviews and updates it).

The agent's parting message:

> *"Workshop complete. I have written `vpc-result.md` and a starter `shadow-backlog.md` to ./project-pat/. After you run Kano on the shadow backlog and identify the Attractive features, write your UVP to `value-proposition.md` using the Osterwalder formula. I will not write the UVP — that is your job."*

The user takes:
- `shadow-backlog.md` → into `kano-model-strategist` for prioritization.
- After Kano → writes `value-proposition.md` using Kano's Attractive features as the differentiators.

---

## What the agent did NOT do (and why this matters)

- **The agent did not draft a UVP.** UVP comes after Kano. The user writes it.
- **The agent did not rank the features.** Phase 2 is mapping, not ranking. The agent proposed Pain Relievers and Gain Creators with mechanisms; it did not declare "best" or "most aligned".
- **The agent did not mix personas or segments.** One Pat, one canvas, sequentially.
- **The agent did not silently drift between phases.** Every step has an explicit accept gate.
- **The agent did not invent.** Every Customer Profile field has a verbatim source quote. Every Value Map item has a one-sentence mechanism.
- **The agent did not over-generate.** 4 Pains + 4 Gains + 3 Pain Relievers + 3 Gain Creators + 2 bundle items. Within the number rules.

---

## Lessons for the agent

1. **The first clarifying question is the same in every workshop.** Persona or segment? Wait for the answer.
2. **One segment or persona at a time.** Sequential, not parallel.
3. **Tables are the primary output format.** Rows are prioritized; columns are fields.
4. **Number rules are not negotiable.** 3-5 Pains, 3-5 Gains, 1-2 main Jobs. If the user has 30 candidate Pains, cluster and prune.
5. **Pain Relievers and Gain Creators are features; Products & Services is the bundle.** Conflating these levels is a common mistake. Watch for it.
6. **Multi-tag is allowed and encouraged.** A feature that addresses both a Pain and a Gain is high-value. Flag overlaps explicitly.
7. **Phase 2 is mapping, not ranking.** No "best", "most aligned", "primary" language. The user cuts.
8. **The agent does not draft a UVP.** UVP is downstream of Kano. The agent's job ends at "framework selected, ready for Kano".
9. **The agent must explain concepts to the user.** When the user asks about Kano, the agent describes how it works. When the user asks about the bundle vs. features, the agent clarifies. The skill is educational, not just procedural.
10. **The collaborative validation gates are non-negotiable.** The agent never auto-locks. The user confirms every step.
