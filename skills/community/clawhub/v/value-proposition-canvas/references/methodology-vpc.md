- `legible-agent-output` (this repo) — applies to every user-facing string the agent emits during the workshop.
---
title: Value Proposition Canvas — Methodology
version: 2.0
created: 2026-07-09
updated: 2026-07-09
status: accepted
parent_skill: value-proposition-canvas
major_change: "v2.0 brings back the full Value Map (Pain Relievers, Gain Creators, Products & Services) as Phase 2 with three substeps and explicit user acceptance gates between every step. Adds number rules (1-2 main Jobs + 3-5 supporting, 3-5 Pains, 3-5 Gains). Tables are the primary output format. Adds Phase 2.5: agent asks which prioritization framework to use next (default: Kano) and explains how it works. UVP drafting remains out of scope. One segment or persona at a time, sequentially."
---

# Methodology: Value Proposition Canvas

## How to read this file

**The SKILL.md is the source of truth for the skill's scope and workflow.** This file is reference material — long-form background reading the agent consults when needed, organized in layers and appendices.

As of v2.0, the skill covers the **full VPC** through Phase 1 (Customer Profile) and Phase 2 (Value Map, in three substeps), with a final Phase 2.5 (prioritization framework selection). The skill ends at "framework selected, ready for Kano". UVP drafting is **out of scope** (the user writes it after Kano).

The methodology file is organized as **six layers** plus Section 0 (Research Methods / GOOB), Section 6 (the Gold Standard `vpc-result.md` template), and two appendices. The agent must respect **progressive disclosure** (Hutchby, 2001; echoed in agent design literature as *context-on-demand*): load one layer, run that step, gate the next layer behind user confirmation. Do not dump all six layers in one message. The workshop is a conversation, not a document.

The in-scope sections for v2.0:

- Section 0 (Research Methods / GOOB) — Use Case 2 research plan, evidence quality levels, **0.7 Soft Rigor**, **0.8 Context Window Management**.
- Layer 1 (Job Extraction from Evidence) — 1-2 main + 3-5 supporting Jobs.
- Layer 2 (Pain Extraction from Evidence) — 3-5 Pains.
- Layer 3 (Outcome Test for Gains) — 3-5 Gains, with the two Osterwalder rules.
- Layer 4 (Pain Relievers mapping) — 1:1 with Pains, in Phase 2.1.
- Layer 5 (Gain Creators mapping) — 1:1 with Gains, in Phase 2.3.
- Layer 6 (Products & Services bundling) — 1-3 bundle items, in Phase 2.5.
- Layer 7 (Prioritization Framework Selection) — Kano default, in Phase 2.5 (the final gate).
- Section 6 (Gold Standard `vpc-result.md` template) — full v2.0 template with both phases.

The methodology file does **not** include the legacy v1.0/v1.1 layers (workshop-from-scratch Socratic extraction, full Value Map with Muda elimination, Fit Verdict, UVP drafting). Those were v1.x scope and are no longer in v2.0.

## Purpose of this file

This file is loaded **on demand** by the parent `SKILL.md`. The parent skill stays compact; this file holds the long-form procedure the agent consults when it actually runs the workshop.

The content is organized as **six layers** plus Section 0, Section 6, and two appendices. The agent must respect **progressive disclosure**: load one layer, run that step, gate the next layer behind user confirmation.

The gates between layers are:

| From → To | Gate condition |
|---|---|
| Start → Section 0 | Persona-or-segment question answered. Agent does nothing until user answers. |
| Section 0 → Phase 1 | Sufficient evidence base. If not, switch to Use Case 2 (research plan) and halt. |
| Phase 1 → Phase 2 (gates) | (a) Number rules met: 1-2 main Jobs + 3-5 supporting, 3-5 Pains, 3-5 Gains. (b) Every Job/Pain/Gain has a verbatim source quote. (c) Hypotheses (1/5 support) labeled. (d) Rows sorted by frequency/importance. (e) **User has explicitly accepted Phase 1.** |
| Phase 2.1 → 2.3 (gate) | (a) Pain Relievers 1:1 with locked Pains (no orphans). (b) Each has a one-sentence mechanism. (c) **User has explicitly accepted the Pain Relievers table.** |
| Phase 2.3 → 2.5 (gate) | (a) Gain Creators 1:1 with locked Gains (no orphans). (b) Multi-tag allowed (feature can be both PR and GC). (c) **User has explicitly accepted the Gain Creators table.** |
| Phase 2.5 → 2.7 (gate) | (a) Products & Services is the bundle, not a list of features. (b) 1-3 bundle items. (c) Each has a delivery mechanism and a contract. (d) **User has explicitly accepted the Products & Services table.** |
| Phase 2.7 → Done (gate) | **User has explicitly chosen a prioritization framework** (default: Kano, with explanation). |
| Done | `vpc-result.md` artifact saved with full v2.0 template (Customer Profile + Value Map + Framework Selection). |

If any gate is not met, **halt**. Apply Confidence Gating from `socratic-dialogue`. Do not skip ahead to be helpful. The agent must not move forward without explicit user acceptance.

---

## Section 0 — Research Methods (GOOB) and the Evidence Base

### 0.1 Why this section is first

The VPC is a hypothesis-testing tool, not a hypothesis-generating tool. The user comes in with beliefs about the customer; the workshop's job is to surface, test, and either lock or reject those beliefs against evidence. Without an evidence base, the workshop produces a canvas full of hallucinations. **Do not start the workshop without naming the evidence source for every claim.** The Socratic Pause is the discipline that enforces this; GOOB is the discipline that builds the base in the first place.

### 0.2 GOOB — Get Out Of the Building

Steve Blank's GOOB principle (*The Four Steps to the Epiphany*, 2013) is the operating system for VPC research. The principle: *customers do not say what they want; they reveal what they want through observed behavior.* Survey says "I want X"; behavior says "I pay for Y". The VPC is anchored on the latter.

A workshop participant who has not gone out of the building is operating on assumption. The agent should ask, in Layer 0 (before Layer 1):

> *"Which of the following have you actually done with at least three real customers from this segment: interviewed them, observed them, sent them a survey, read their forum complaints, read their support tickets, or analyzed their competitor reviews?"*

If the answer is "none", halt. Direct the user to do at least one of these before resuming. Do not invent a Customer Profile from speculation.

### 0.3 Acceptable evidence-collection methods

The agent should encourage the user to draw from any of:

- **Customer interviews.** In-depth, open-ended, 30–60 minutes. Listen for the *why*, not the *what*. Ask "tell me about the last time you..." rather than "do you want X?".
- **Surveys and questionnaires.** Useful for breadth, weak for depth. Use to validate, not to discover. Sample size: at least 30 responses per segment for any quantitative claim.
- **Observation and ethnographic studies.** Watch the customer do the job in their natural environment. The things they do *without thinking* are the real jobs.
- **Social media and forum mining.** Reddit, X, Hacker News, niche forums. Look for the complaints people make *voluntarily* — these are unprompted pains.
- **Competitor analysis and reviews.** Read the 1- and 2-star reviews of competitors. These are gold for unaddressed pains.
- **Empathy mapping.** A four-quadrant map (says / thinks / does / feels) for a representative customer. Useful for early-stage personas.
- **Card sorting.** Have customers rank the candidate pains and gains by intensity. The ranking reveals which ones are dominant and which are decoration.

The agent should ask the user to name *which* methods were used for *which* claim. A pain anchored to a forum quote is acceptable evidence; a pain anchored to "I imagine they would say..." is not.

### 0.4 Evidence quality levels

Not all evidence is equal. The agent should weight evidence by proximity to the customer:

| Level | Type | Strength |
|---|---|---|
| 1 | Direct customer interview (transcript) | Strongest |
| 2 | Customer observation / ethnographic note | Strong |
| 3 | Forum / social media complaint (unprompted) | Strong |
| 4 | Survey response (n ≥ 30) | Moderate |
| 5 | Competitor review / 1-star complaint | Moderate (validates the pain, not the segment size) |
| 6 | Analyst report (Gartner, Forrester) | Weak for jobs, moderate for sizing |
| 7 | Founder / team intuition | Weakest — must be labeled "hypothesis" |

If the user's evidence base is mostly Level 7, the workshop is in trouble. The agent should say so plainly and direct the user to do at least one Level 1–3 method before resuming.

### 0.7 Soft rigor — the Hypothesis discipline

The "no quote = no entry" rule is methodologically correct, but the agent must apply it with **softness**, not as a hard wall. A user intuition is a real signal; it is just unvalidated. The agent's job is to label and test it, not to punish it.

This discipline exists to solve a real risk: if the agent applies rigor as a wall, the user gets frustrated and abandons the workshop. If the agent applies rigor as a guidepost, the user stays engaged while the canvas stays honest.

**The four-step discipline:**

1. **Accept the user's intuition.** The agent says *"That sounds like a real Pain. Let's add it as a hypothesis and see what evidence confirms it."* The intuition is honored, not rejected.

2. **Label the field explicitly.** The field is marked `Hypothesis (0/N support)` in the table. The user can see it is not deleted — it is parked for testing. The label is **visible**, not hidden.

3. **Suggest a verification path.** The agent asks: *"What would change your mind about this Pain? What would you need to see in the next 2-3 interviews to lock it?"* The user gets a concrete next step, not a moral judgment.

4. **Do not punish the user.** The agent's tone is curious and inviting, not corrective. *"I do not have evidence for this yet"* is fine. *"This is not a real Pain"* is a failure of the agent.

**Example — bad response (rigor as wall):**

> User: *"Pain: developers don't read specs."*
> Bad agent: *"No source quote. Cannot add to canvas. Provide a verbatim interview quote or this entry is rejected."*

The user feels dismissed. The agent has applied a rule correctly but killed the conversation.

**Example — good response (rigor as guidepost):**

> User: *"Pain: developers don't read specs."*
> Good agent: *"This sounds right intuitively. Adding it as a hypothesis with 0/N support. To lock it, we'd need at least one transcript where a developer (or the persona) says verbatim 'I don't read the spec' or 'the spec is unread'. Can you point me to an interview where this came up? If not, this stays a hypothesis and we test it in the next round of research."*

The user gets:
- Their intuition is honored.
- The label makes the gap visible.
- A concrete path to lock the field.
- No moral judgment on the lack of evidence.

**When to escalate to a hard stop:**

The soft-rigor discipline applies to **field-level** claims (a Pain without a quote, a Gain without evidence). It does not apply to **canvas-level** claims:

- If the user has zero evidence base (no transcripts, no persona docs, no observation notes), the agent **does** halt. The soft-rigor discipline cannot save a canvas with nothing to anchor to. The agent offers Use Case 2 (the research plan) and waits.
- If the user asks the agent to invent a fake persona to feed the canvas, the agent **does** refuse. A hallucinated persona is a hallucination with a name.

These two cases are the only hard stops. Everything else is a soft guidepost.

**What the agent must never do:**

- "I cannot add this. Provide evidence or remove." (dismissive)
- "This is not a real Pain." (corrective)
- "You need to do more research before we can continue." (gatekeeping)
- "The interview data does not support this." (corrective without offering a path)

**What the agent must always do:**

- "Adding as hypothesis. What evidence would lock it?" (inviting)
- "I do not have verbatim support for this yet. What do you remember from the interviews?" (curious)
- "Let's keep this on the canvas as a hypothesis and see if more interviews confirm it." (patient)
- "Here is a path to validate this in the next round of research." (constructive)

The skill is a tool for the user, not a gatekeeper. Rigor is a guide, not a wall.

### 0.8 Context window management and chunked extraction

A 5-7 transcript evidence base is roughly 25,000-50,000 tokens. The skill content (SKILL.md ~23 KB + methodology ~60 KB if loaded) is another 20,000 tokens. The user messages and the running canvas add more. Total: at or beyond the practical context window of most models.

The skill has a **chunked extraction** pattern. The default strategy depends on the evidence base size:

| Evidence base size | Strategy | Notes |
|---|---|---|
| **1-3 transcripts** (small) | Single pass | Read the full evidence in one go. Extract Jobs, Pains, Gains. |
| **4-6 transcripts** (medium) | Chunked extraction | Process one transcript at a time. Accumulate findings into a running canvas. The user validates between chunks. |
| **7+ transcripts or 50+ tickets** (large) | Pre-summarized chunks | The user (or an upstream tool) pre-summarizes each transcript into 200-300 words with key verbatim quotes preserved. The agent reads the summaries + the preserved quotes. |
| **100+ items** (huge) | Parallel sub-agents | Dispatch one sub-agent per cluster of evidence (e.g., one per persona segment). Each sub-agent returns structured output. The parent agent consolidates. |

**The chunked extraction pattern (for medium evidence):**

1. The agent announces the strategy at the start: *"I will process your 6 transcripts one at a time. After each, I will post an incremental canvas update. After the last, I will deduplicate and rank. This preserves verbatim fidelity. Confirm?"*

2. The agent reads transcript #1, extracts Jobs/Pains/Gains with verbatim quotes, posts the partial canvas.

3. The user validates: *"Add Pain P3, drop J2, keep G1."*

4. The agent reads transcript #2, extracts new items, marks duplicates (e.g., "J1 already exists, but this transcript adds verbatim quote X"), posts the merged canvas.

5. The user validates again.

6. Continue until all transcripts are processed.

7. The agent runs the final ranking, lock, and feature brainstorm.

**Critical rules for chunked extraction:**

1. **Verbatim quotes are never summarized away.** The agent preserves the original phrasing, even if it costs tokens. A summarized quote is a hallucinated quote. If the agent cannot fit a full quote in the running canvas, it keeps the full quote in a separate notes section, not in the canvas table.

2. **Source attribution is preserved per chunk.** Each field has a source list. After all chunks are processed, the source counts are aggregated (e.g., "G1 has 4/5 support, with verbatim quotes from interviews #1, #2, #4, #5").

3. **The user validates between chunks.** This is not optional. Without the between-chunk validation, the agent accumulates errors and the final canvas is harder to fix.

4. **The agent deduplicates at the end, not during.** Two transcripts may describe the same Job with different wording. The agent keeps both verbatim quotes and merges the field at the end, not during. Premature deduplication loses nuance.

5. **The agent announces duplicates explicitly.** When the agent notices that two Pains are similar, it says: *"P2 from transcript #1 and P5 from transcript #3 are both about slow code. They may be the same Pain. I will keep both verbatim quotes and merge in the final synthesis. Confirm?"*

**The pre-summarized chunk pattern (for large evidence):**

When the evidence is too large for chunked extraction (e.g., 7+ transcripts or 50+ support tickets), the agent asks the user to pre-summarize.

> *"I cannot process 8 full transcripts in a single context window with rigor. Please pre-summarize each transcript to 200-300 words, preserving the verbatim quotes that you think are most important. Paste the summaries, and I will work from those."*

The user (or an upstream tool like a transcript-summarization skill) produces the pre-summaries. The pre-summary is **not** the evidence — it is a pointer to the evidence. The agent's job is to read the pre-summary, request the full transcript for any field that needs verbatim verification, and post the canvas with the verbatim quotes it now has.

**The parallel sub-agent pattern (for huge evidence):**

When the evidence is 100+ items, the agent dispatches sub-agents. Each sub-agent takes a cluster of evidence (e.g., all transcripts for one persona segment) and returns a structured Customer Profile for that cluster. The parent agent consolidates.

This pattern requires the parent agent to have explicit orchestration logic. It is a v1.2 stretch goal, not a v1.2 default.

**What the agent must never do (context window discipline):**

- **Summarize a verbatim quote to fit the canvas.** A summarized quote is a hallucinated quote.
- **Skip transcripts to fit the window.** The user has chosen to bring the evidence; the agent processes it all.
- **Guess at the content of a transcript it has not read.** If a transcript is referenced but the agent has not processed it, the agent says so plainly.
- **Process transcripts in parallel silently.** The user must see the chunked extraction in action; silent parallel processing hides the validation step.

**Default behavior:**

If the user brings more than 6 transcripts without pre-summarizing, the agent announces the chunked strategy and starts. The agent does not refuse. The agent does not ask the user to pre-summarize all of them first. The agent processes one at a time, validates with the user, processes the next. This is the soft-rigor discipline applied to the context window problem.

---

## Layer 1 — Job Extraction from Evidence (Customer Jobs)

### 1.1 Purpose

Extract the persona's Jobs from the user's evidence base — without inventing. The dominant job is the canvas's center of gravity; if it is wrong, every downstream field is wrong. But the Jobs are *in the data*, not in the agent's prior. The agent's job is to surface them faithfully, not to Socratically extract them from a vague idea (that is the workshop-from-scratch mode, which is a fallback only).

This layer composes the **listening discipline** from Section 0.4 (evidence quality levels) and a small Socratic validation step from `socratic-dialogue` to catch extraction errors. The Socratic engine is used to **validate**, not to **extract**.

### 1.2 Step-by-step

#### Step 1.1 — Read the evidence for Job signals

For each interview transcript, persona doc, or other evidence source, the agent scans for the verbatim signals from the listening guide (Section 0.5 in `examples/research-collection.md`):

| VPC field | Verbatim signals to listen for |
|---|---|
| **Job (functional)** | "I need to...", "My job is to...", "I'm trying to..." |
| **Job (social)** | "I want my team to see me as...", "I want to be known for..." |
| **Job (emotional)** | "I want to feel...", "I hate feeling like..." |

The agent does **not** paraphrase. The agent extracts the verbatim quote and tags it with the source (interview #, persona, line range if available).

#### Step 1.2 — Cluster the Job signals

The agent clusters the verbatim signals into 3-5 candidate Jobs. Each Job:

- Has a **one-sentence name** (functional, social, or emotional).
- Has a **source count** (e.g., 3/5 interviews mentioned this Job explicitly).
- Has **verbatim source quotes** attached (the agent keeps the strongest 1-3 quotes).

If a Job has only 1/5 support, the agent labels it `Hypothesis` and includes it. The user decides whether to keep, drop, or expand the evidence.

#### Step 1.3 — Rank the Jobs

The agent ranks the Jobs by source count and richness. The top Job is the **dominant Job** — the one the persona talks about most, with the most vivid quotes. The agent does not impose an external ranking; the ranking is anchored to the evidence.

#### Step 1.4 — Socratic validation (small dose, not extraction)

The agent does **not** Socratically extract a Job from a vague idea (that is workshop-from-scratch mode). The agent does apply a small dose of Socratic validation to catch extraction errors:

> *"Job 2 ('Be seen as a credible technical partner by the dev team') has 3/5 support, but the quotes are from the same persona archetype. Is this Job generalizable beyond the archetype, or is it a persona-specific signal that should stay in a persona-level canvas, not a segment-level canvas?"*

This is **validation**, not **extraction**. The Socratic engine is used to check the agent's work, not to invent the work.

#### Step 1.5 — Faithfulness Check

The agent runs a self-attack on the Job list:

- Is the dominant Job actually observable, or is it a designer projection?
- Does the dominant Job have at least 2/5 source support?
- Are any Jobs synonyms of each other (should be merged)?
- Does the Job list include Jobs that no source quote supports (hallucinations)?

If hallucinations are found, the agent **removes** them. The user must confirm the final list.

### 1.3 Output format

Each Job is recorded as a row in the Customer Profile:

| # | Job (one sentence) | Type (F / S / E) | Source count | Verbatim source quote(s) | Status |
|---|---|---|---|---|---|
| J1 | ... | Functional | 5/5 | "[quote 1]" — Interview #2 / "[quote 2]" — Interview #4 | Locked |
| J2 | ... | Social | 3/5 | "[quote 1]" — Interview #1 | Locked |
| J3 | ... | Emotional | 1/5 | "[quote 1]" — Interview #5 | Hypothesis (1/5) |

The agent does not invent Jobs. A Job without a source quote is rejected. A hypothesis with 1/5 support is kept, not promoted.

### 1.4 Job Story format (optional)

The Job Story format (Patton, *User Story Mapping*; refined by Alan Klement, *When Coffee and Kale Compete*) is **optional in ingestion mode**. The user has transcripts; the dominant Job is the one with the most source quotes. The agent does not force a Job Story reformatting unless the user asks for it (some users want the Job Story for downstream Story Mapping).

If the user wants the Job Story, the format is:

```
When [situation / motivation]
I want [need / direction of effort]
so I can [outcome / measurable change].
```

The agent must reject any Job Story that fails the Structural Test:
- "When" must name a situation the user finds themselves in, not a screen they visit.
- "I want" must be a direction (reduce / increase / know / feel), not a noun (button, picker, modal).
- "So I can" must be a measurable or visible change, not a deliverable name.

### 1.5 Layer 1 gate

Proceed to Layer 2 only if:
- The user has committed to a Customer Profile Job list (3+ Jobs, with at least one dominant Job).
- Every Job has at least one verbatim source quote.
- Hypotheses (1/5 support) are labeled, not promoted to locked.
- The user has explicitly confirmed the Job list.

---

## Layer 2 — Pain Extraction from Evidence (Customer Pains)

### 2.1 Purpose

Extract the persona's Pains from the user's evidence base — without inventing. Distinguish *scratched-knee* pains (minor, infrequent, workable around) from *broken-leg* pains (severe, frequent, currently unresolved). Every Pain that lands on the canvas must be anchored to a verbatim source quote. A Pain without a quote is a hallucination.

This layer composes the Pain-Driven Design pattern (Hunt, 2016) and the listening discipline from Section 0.4. The Socratic engine is used for **validation**, not extraction.

### 2.2 Step-by-step

#### Step 2.1 — Read the evidence for Pain signals

For each transcript, the agent scans for the verbatim Pain signals from the listening guide:

| VPC field | Verbatim signals |
|---|---|
| **Pain (operational)** | "I waste X hours on...", "Every time I do X, I have to..." |
| **Pain (strategic)** | "I'm worried that...", "What if..." |
| **Pain (social)** | "It's embarrassing when...", "I don't want my team to think I..." |

The agent extracts the verbatim quote and tags it with the source.

#### Step 2.2 — Cluster the Pain signals

The agent clusters the verbatim signals into 3-5 candidate Pains. Each Pain:

- Has a **one-sentence name**.
- Has a **source count** (e.g., 3/5 interviews).
- Has **verbatim source quotes** attached.

If a Pain has only 1/5 support, the agent labels it `Hypothesis` and includes it.

#### Step 2.3 — Broken-Leg Test (severity + frequency + workaround cost)

For each candidate Pain, the agent assesses:

1. **Severity.** If this pain happened once a week, would the customer pay to make it stop? (Yes → severity ≥ 4. No → severity ≤ 2.)
2. **Frequency.** How often does this pain occur? (Daily, weekly, monthly, per release, per quarter.)
3. **Workaround cost.** What does the customer currently do to escape this pain? (No workaround → high. Cheap workaround → low. Expensive, ugly workaround → high.)

A real broken-leg pain scores high on all three. A scratched-knee pain scores low on at least one.

The agent uses the **verbatim source quotes** to score, not its own prior. If the user has a quote like "I would pay $50/month to never have to do this again", severity is 5. If the user has only "this is mildly annoying", severity is 2.

Reject any candidate that fails the Broken-Leg Test. Do not negotiate. *"It would be nice to solve this"* is a feature request, not a Pain.

#### Step 2.4 — Socratic validation (small dose)

The agent applies a small dose of Socratic validation to catch extraction errors:

> *"Pain #2 ('Developers implement the wrong state because they guess at the Figma file') has 3/5 source support. The quotes are vivid ('they guess, get it wrong, I write a v2 spec within a week'). But is the Pain 'developers guess' or is it 'no machine-readable contract exists'? The first is a symptom; the second is the root cause. Which framing matches the data better?"*

This is **validation**, not **extraction**. The Socratic engine checks the agent's work.

#### Step 2.5 — Tag with Pain category

Osterwalder, Pigneur, and Smith (2014) and the IxDF synthesis identify five canonical Pain categories. Tag every locked Pain with the category that best fits.

| Category | What to ask | Examples |
|---|---|---|
| **Concerns and risks** | What significant worries does the customer have? | Losing money, social embarrassment, losing trust or status, security breach |
| **Dissatisfaction and stress** | What causes frustration or anxiety with current solutions? | UX bugs, slow support, frequent errors, hidden costs |
| **Challenges with current designs** | What problems does the customer face using the existing product? | Missing features, hard-to-use interface, blocked tasks |
| **Barriers to adoption** | What stops the customer from starting or switching? | High initial cost, steep learning curve, fear of migration |
| **Costly or demanding aspects** | What aspects of current solutions take too much? | Excessive time, high monetary cost, significant effort |

A healthy canvas has Pains across at least three categories. A canvas with all Pains in one category (typically "missing features") is usually a feature-list disguised as a value proposition.

#### Step 2.6 — Quantifying Pains (Strategyzer best practice)

The agent pushes the user to make every locked Pain **quantitative** wherever the verbatim quote supports it.

- *Weak:* "The onboarding is too long."
- *Strong:* "Onboarding takes more than 3 steps to first value."
- *Stronger:* "Onboarding takes 7 minutes median, with 40% of users abandoning at step 4."

Quantification gives the agent a yardstick for the feature brainstorm in Layer 4. If the Pain is "7 minutes and 40% abandonment at step 4", the brainstorm should produce features that can be measured in the same units.

If the user cannot quantify a Pain, the Pain stays qualitative. The agent does not invent a number.

#### Step 2.7 — Classify and rank

For each locked Pain, record:

- **Statement** (one sentence)
- **Severity** (1-5)
- **Frequency** (per day / week / month / release)
- **Verbatim source quote** with source reference
- **Workaround cost** (none / cheap / expensive)
- **Category** (IxDF)
- **Quantified unit** (if available)

Rank the locked Pains by `severity × frequency`. The top 1-3 are the **dominant Pains** the feature brainstorm should address. The rest stay on the canvas but get a lower priority tag.

### 2.3 Layer 2 gate

Proceed to Layer 3 only if:
- At least three Pains are locked with verbatim source quotes.
- At least one Pain is rated severity 4 or 5.
- The dominant Pain (highest `severity × frequency`) is identified.
- Every locked Pain is tagged with at least one of the five Pain categories.
- At least three Pains are quantified with a measurable unit (time, count, percentage, cost).
- No "scratched-knee" Pains have slipped through (severity ≤ 2 with no evidence → reject).

---

## Layer 3 — The Outcome Test (Gains verification)

### 3.1 Purpose

The user almost always conflates outputs and outcomes at this stage. "Faster code" is an output. "Ship a feature this morning instead of fighting handoff all day" is the outcome. This layer enforces the distinction rigorously.

The Outcome Test is a five-filter gauntlet. A gain must pass all five filters to land on the canvas.

### 3.2 The five filters

#### Filter 1 — The Difference Filter

> *"If we produce this Gain successfully, what is the specific difference it makes in the user's life or the business's bottom line?"*

If the user cannot articulate the difference, the gain is just a relabeled output. Reject and reframe.

#### Filter 2 — Solution-in-Disguise Deconstruction

> *"If I gave you exactly what you asked for, but [the deeper problem] remained, has the Gain been produced?"*

The deeper problem is whatever survives the user's own Elenchus. If the user claims the gain is "the team has documentation" and the team still gets stuck in handoff because the documentation is wrong, the gain has not been produced.

#### Filter 3 — Three-Level Outcome Verification (Gothelf & Seiden, *Lean UX*)

A complete gain must address all three levels:

- **Functional.** What task is completed or what capability is gained? ("I can ship a feature without rework.")
- **Emotional.** How does the user feel? ("I feel confident and tech-savvy delivering to the dev team.")
- **Long-term / business.** How does this move the user toward their dream or KPI? ("I can scale my product because handoff is no longer the bottleneck.")

If any level is empty, the gain is incomplete. Push the user to name the missing level explicitly.

#### Filter 4 — The Measurable Change Requirement

> *"Does this Gain result in a 'measurable change in human behavior that drives business results'?"*

Binary gains fail. A gain is not "the spec exists" — it is "the spec reduces rework rate by 40%". If the user offers a binary, ask: *"What changes in their behavior or in your metrics when this Gain is realized?"*

#### Filter 5 — 5 Whys (gain-side root cause)

Just as pains need a root cause, gains do too. A gain that traces back to "more features" or "better documentation" is symptomatic, not causal. Trace each gain to a core benefit: "mitigating the risk of missing a release deadline", "restoring a sense of agency in delivery", "regaining the time lost to coordination tax".

### 3.3 The two Osterwalder rules for gains

These two rules are the single most common source of gain-shape errors. The agent must enforce them explicitly, even if the user has not read Osterwalder.

**Rule A — Gains are not the simple result of the job.**

> "A greater design knowledge" is not a gain for a design professional who wants to learn new design skills — the *result of the job* is that they have new skills. That is the floor. The **gain** is "suggestions of how to continue growth after course completion" — the unexpected positive outcome on top of the result.

The Socratic test: *"If the customer got the result of the job, would they be done? If yes, you have named a result, not a gain. Push deeper."*

**Rule B — Gains are not the inverse of pains.**

> If the pain is "what if I don't learn anything new?", the gain is **not** "learning something new" — that is the absence of the pain. The **gain** is "educational materials tailored to my level and career stage" — a positive outcome the user did not have before.

The Socratic test: *"If you flip the pain from negative to positive, do you have a gain? If yes, you have a restated pain, not a gain. Push for the unexpected positive."*

Both rules push the workshop toward the **Unexpected Gain** category, which is the territory of Value Innovation. A canvas with only Required and Expected gains is feature-competitive. A canvas with at least one Unexpected gain is differentiated.

### 3.4 Gain category (IxDF / Osterwalder synthesis)

Tag every locked gain with the category that best fits. The IxDF synthesis (drawing on Osterwalder, Pigneur, and Smith) identifies six canonical categories.

| Category | What to ask | Examples |
|---|---|---|
| **How current solutions make users happy** | What positive aspects of existing products do users want preserved or amplified? | Special features, good performance, high quality |
| **Positive social results** | How does the user want to be perceived? | Looking professional, gaining respect, status |
| **Desired improvements** | What would the user change about existing solutions? | Simpler UI, more features, better support |
| **Success criteria** | How does the user judge success or failure? | Reliability, ROI, measurable outcomes |
| **Time, money, effort savings** | What cuts would make the user happy? | Faster onboarding, cheaper pricing, less manual work |
| **Adoption factors** | What would make the user actually start using the product? | Appealing design, solid guarantees, easy migration |

A healthy canvas has gains across at least three categories. A canvas with all gains in "desired improvements" is a feature list, not a value proposition.

### 3.5 Gain classification

For every locked gain, classify on two axes.

**By expectation (Kano-informed, but light):**

- **Required.** The minimum the customer expects. Absence triggers rejection.
- **Expected.** What the customer assumes is normal. Absence triggers disappointment.
- **Desired.** What would delight but is not expected.
- **Unexpected.** A benefit the customer did not anticipate. This is the territory of Value Innovation (Kim & Mauborgne, 2005).

**By outcome type (Gothelf & Seiden, 2016):**

- **Functional.** Saves time, reduces cost, removes a step.
- **Emotional.** Reduces anxiety, increases status, restores agency.
- **Social.** Strengthens the user's position in a group, network, or hierarchy.

A healthy canvas carries a mix. A value proposition that delivers only functional gains is brittle (any competitor can copy a feature). A value proposition that delivers only emotional gains is vaporware (no substance to retain the customer).

### 3.6 Quantifying gains

A qualitative gain is weak. The agent should push the user to make every locked gain **quantitative** wherever possible.

- *Weak:* "Faster code generation."
- *Strong:* "Code generated in under 30 seconds per component."
- *Stronger:* "Code generation reduced from 8 hours to 30 minutes per component, a 16× speedup."

The unit of the gain must match the unit of the pain it relieves. If the pain is "8 hours per component on Slack", the gain must be measurable in the same unit ("coordination time per component reduced to <1 hour").

### 3.7 The Outcome Test Checklist (gate)

A gain is locked only if it passes all eight items:

- [ ] It is an outcome, not an output (Filter 1).
- [ ] It is not a solution in disguise (Filter 2).
- [ ] All three levels (functional, emotional, long-term) are addressed (Filter 3).
- [ ] It includes a measurable behavioral or business change (Filter 4).
- [ ] It survives a 5 Whys trace to a root benefit (Filter 5).
- [ ] It is not the simple result of the job (Rule A).
- [ ] It is not the inverse of a pain (Rule B).
- [ ] It is classified on three axes: expectation, outcome type, and gain category.
- [ ] It is quantified with a measurable unit.

If any item fails, return the gain to the candidate list. Do not allow it onto the canvas.

### 3.8 Layer 3 gate — Customer Profile is locked

Once all three layers (Jobs, Pains, Gains) are locked, the agent posts the **Solution-First Lock** checkpoint:

> *"Customer Profile is locked.*
> *Dominant job: [X]*
> *Dominant pain: [Y]*
> *Dominant gain: [Z]*
> *No solutions will be accepted on the Value Map that do not address at least one of these three. Proceed?"*

The user must confirm. This is the boundary that prevents the Build Trap (Ries, 2011; Perri, *Escaping the Build Trap*).

---
---

## Layer 4 � Pain Relievers mapping (Phase 2.1)

### 4.1 Purpose

Map every locked Pain in Phase 1 to a **Pain Reliever** � a concrete feature (not a bundle) that eliminates or reduces that specific Pain. The mapping is 1:1, no orphans, with a one-sentence mechanism per Pain Reliever.

**Critical distinction (read this carefully):** Pain Relievers are **features** � concrete capabilities of the bundle. The bundle itself is the **Products & Services** (mapped in Layer 6, Phase 2.5). A common mistake is to confuse the two levels. A Pain Reliever is a feature inside the bundle; the bundle is the offering shape (subscription app + plugin + templates).

### 4.2 Step-by-step

#### Step 4.1 � Read the locked Pains from Phase 1

The agent takes the accepted Pains table from Phase 1. Only the **prioritized** Pains (severity 4-5) are mapped in Phase 2. Pains marked `Hypothesis` or rated below severity 4 are **parked** � they appear in the canvas but are not mapped to Pain Relievers. The user decides whether to leave them parked or add them.

Default rule: the user has 3-5 locked Pains, all severity 4-5. Map all of them. If the user has more than 5, the agent pushes back: "You have [N] Pains. We agreed on 3-5 dominant ones. Which should we keep?"

#### Step 4.2 � Propose one Pain Reliever per Pain

For each locked Pain, the agent proposes **one** Pain Reliever. The proposal is a **feature** with a one-sentence mechanism:

- **Pain Reliever (feature)**: A concrete capability the bundle offers. Named (so it is referenceable). Demonstrable (the user can see it in one screenshot or one paragraph).
- **Mechanism**: One sentence describing **how** the feature eliminates or reduces the Pain. Not what the feature does in general; specifically how it addresses THIS Pain.

**Pain Relievers table:**

| # | Pain addressed | Pain Reliever (feature) | Mechanism | Status |
|---|---|---|---|---|
| R1 | P1: 8 hours per component on Slack | Single-link handoff page | A static page that bundles the Figma frame + spec + test cases, shareable as one URL. Dev reads the page, not the Figma file. | Proposed |
| R2 | P2: 60% rework rate | spec.md generator from Figma | A Figma plugin reads the file and emits a structured markdown spec: states, edge cases, accessibility decisions. | Proposed |
| R3 | P3: 50-page spec unread | spec confidence score | A heuristic score that flags how complete / unambiguous the spec is before the dev picks it up. | Proposed |

The agent posts the table and waits for the gate.

#### Step 4.3 � GATE � explicit user accept

The user can:

- **Accept** ("proceed")
- **Drop** ("drop R2, not feasible")
- **Rephrase** ("rewrite R1, the mechanism is unclear")
- **Add** ("add R4 for P4")
- **Multi-tag note** ("note that R1 and the Gain Creator for G2 will be the same feature � flag as overlap")

The agent does not move to Layer 5 (Gain Creators) until the user explicitly accepts the Pain Relievers table.

### 4.3 1:1 mapping and Muda check

**1:1 mapping:** every locked Pain gets exactly one Pain Reliever. No orphans on either side. If a Pain does not have a Pain Reliever, the user must either:

- Propose a Pain Reliever for it, or
- Mark it explicitly as **out of scope** (which is honest, but means the canvas has a gap � the user must own that).

**Muda check (waste elimination):** each Pain Reliever must address a Pain the user actually has, not a Pain the user *might* have. A Pain Reliever that addresses a hallucinated Pain is muda. The agent catches this:

> Socratic question: *"R3 (spec confidence score) addresses P3 (50-page spec unread). Does the spec actually go unread because there is no confidence signal, or because the dev does not have time to read anything longer than a paragraph? If it is the latter, R3 is muda � the dev would not look at a confidence score either."*

The user accepts, drops, or rephrases based on the Socratic probe.

### 4.4 What this layer does NOT do

- **The agent does not rank Pain Relievers.** Phase 2.1 is mapping, not ranking. No "best", "most aligned", "primary" language. The user cuts.
- **The agent does not draft a UVP.** UVP comes after Kano.
- **The agent does not pick a framework.** Framework selection is in Layer 7.


---

## Layer 5 � Gain Creators mapping (Phase 2.3)

### 5.1 Purpose

Map every locked Gain in Phase 1 to a **Gain Creator** � a concrete feature (not a bundle) that produces that specific Gain. The mapping is 1:1, no orphans, with a one-sentence mechanism per Gain Creator.

**Multi-tag rule:** a single feature can be **both** a Pain Reliever and a Gain Creator. This is allowed and even encouraged � a feature that addresses both a Pain and a Gain is more valuable than one that addresses only one. The agent flags overlaps explicitly.

### 5.2 Step-by-step

#### Step 5.1 � Read the locked Gains from Phase 1

The agent takes the accepted Gains table from Phase 1. Only the **prioritized** Gains (Required, Expected, Desired, or Unexpected) are mapped. Hypotheses are parked.

Default rule: 3-5 locked Gains, all prioritized. Map all of them. If more than 5, push back to 3-5.

#### Step 5.2 � Propose one Gain Creator per Gain

For each locked Gain, the agent proposes **one** Gain Creator. The proposal is a **feature** with a one-sentence mechanism:

- **Gain Creator (feature)**: A concrete capability the bundle offers.
- **Mechanism**: One sentence describing **how** the feature produces THIS Gain.

**Gain Creators table:**

| # | Gain produced | Gain Creator (feature) | Mechanism | Status |
|---|---|---|---|---|
| C1 | G1: ship without rework | spec-driven diff review | When the spec changes, the dev sees a diff against the previous version and implements the diff. | Proposed |
| C2 | G2: send one link with everything | single-link handoff page (overlap with R1) | Same feature as R1 � multi-tag is allowed. | Proposed |
| C3 | G3: recognized as Design Engineer | public portfolio of design decisions | A public page showing the spec + rationale + outcome, as evidence of credible technical work. | Proposed |

The agent posts the table and waits for the gate.

#### Step 5.3 � GATE � explicit user accept

Same discipline as Layer 4. The user accepts, drops, rephrases, or adds. The agent does not move to Layer 6 (Products & Services) until the user accepts the Gain Creators table.

### 5.3 1:1 mapping and overlap flagging

**1:1 mapping:** every locked Gain gets exactly one Gain Creator. No orphans.

**Overlap flagging:** if a feature is both a Pain Reliever (R) and a Gain Creator (C), the agent flags it explicitly in both tables. Overlap is a positive signal � a feature that addresses both a Pain and a Gain is high-value.

**Muda check:** same as Layer 4. A Gain Creator that does not produce a real Gain is muda.

### 5.4 What this layer does NOT do

- **The agent does not rank Gain Creators.** Phase 2.3 is mapping, not ranking.
- **The agent does not pick a framework.** Framework selection is in Layer 7.
- **The agent does not draft a UVP.** UVP comes after Kano.


---

## Layer 6 � Products & Services bundling (Phase 2.5)

### 6.1 Purpose

Define the **Products & Services** � the **bundle**, not a list of features. The bundle is the physical shape of the offering: what the customer acquires, how it is delivered, what the contract is.

**Critical distinction (read this carefully):** Pain Relievers and Gain Creators are **features** � they live inside the bundle. The bundle is the **vehicle**: a SaaS app, a Figma plugin, a pack of templates, a consulting engagement, a hardware device, a subscription. The agent must not conflate the two levels. A common error is to list every Pain Reliever and Gain Creator as a separate "product" � that produces 12+ "products", which is a feature list disguised as a bundle.

### 6.2 Step-by-step

#### Step 6.1 � Propose 1-3 bundle items

The agent proposes **1-3 bundle items** that together support the Customer Jobs. The bundle is named precisely. Each item has a delivery mechanism and a contract.

**Bundle items table:**

| # | Bundle item | What the customer receives | Type (tangible / digital / intangible) | Contract | Jobs supported |
|---|---|---|---|---|---|
| S1 | spec.md generator | A Figma plugin + a code-side parser that emits a structured `spec.md` per component | Digital | License (per seat, annual) | J1, J2 |
| S2 | single-link handoff page | A web app that bundles design + spec + states + test cases + a11y into a shareable URL | Digital | Free tier + Pro subscription | J1, J3 |
| S3 | spec.md templates library | A pack of pre-built templates per component type (form, modal, list, etc.) | Digital | One-time purchase | J2, J3 |

The agent posts the table and waits for the gate.

#### Step 6.2 � GATE � explicit user accept

The user accepts, drops, rephrases, or adds. The agent does not move to Layer 7 until the user accepts the Products & Services table.

### 6.3 Naming discipline

Each bundle item must be **nameable in one sentence** and **demonstrable in one screenshot or one paragraph**. Reject vague bundles ("a platform", "a solution", "an experience", "a product suite").

**Common mistakes:**

- Listing every Pain Reliever / Gain Creator as a separate "product" ? produces 12+ "products" = feature list, not bundle.
- Naming the bundle as the sum of features ("the spec.md suite") ? nameable, but conflates features with bundle. The bundle is the vehicle (app, plugin, service); the features are inside.
- Bundling everything into one "super product" ? too coarse, cannot be priced or distributed.

### 6.4 What this layer does NOT do

- **The agent does not draft a UVP.** UVP comes after Kano.
- **The agent does not pick a framework.** Framework selection is in Layer 7.


---

## Layer 7 � Prioritization Framework Selection (Phase 2.7)

### 7.1 Purpose

The skill ends at "framework selected, ready for prioritization". The user has Pain Relievers + Gain Creators (= features) from Layers 4 and 5, and a bundle from Layer 6. The user now needs a **prioritization framework** to decide which features to build first.

**Kano Model Strategist** is the default proposed framework, because it specifically identifies the **Attractive (delighter)** features � the differentiators that will eventually drive the user's UVP. The user can choose a different framework if they prefer.

**This is the final gate.** After this layer, the skill ends. UVP drafting is **out of scope** (the user writes it after Kano, using Kano's Attractive features as the differentiators).

### 7.2 Step-by-step

#### Step 7.1 � Propose Kano and explain how it works

The agent asks: "Phase 2 is complete. You have [N] Pain Relievers and [M] Gain Creators. To decide which to build first, you need a prioritization framework. Which framework would you like to use?"

The agent then proposes **Kano Model Strategist** and explains how it works:

> *"Kano Model Strategist (the next skill in this playbook) classifies features into six categories based on customer satisfaction:*
>
> *- **Must-be (basic):** features the customer expects. Absence causes rejection. These are non-negotiable baseline.*
>
> *- **Performance (one-dimensional):** more is better. Customer satisfaction scales linearly. Investment here is rational but not differentiating.*
>
> *- **Attractive (delighters):** unexpected positives. Absence does not cause dissatisfaction; presence causes delight. These are the differentiators that drive your eventual UVP.*
>
> *- **Indifferent:** the customer does not care either way. Skip.*
>
> *- **Reverse:** some customers actively dislike. Cut.*
>
> *- **Questionable:** the data is unclear. Needs more research.*
>
> *Kano is a great default for VPC outputs because it tells you which features are the Attractive ones � the ones that go into your UVP. Run `kano-model-strategist` next."*

#### Step 7.2 � User picks a framework

The user can:

- **Accept Kano** (default).
- **Pick another framework** (RICE, MoSCoW, ICE, Impact/Effort matrix, custom).

The agent records the choice in the artifact. The skill ends.

### 7.3 What the agent does NOT do

- **The agent does not run the prioritization itself.** That is the chosen framework's skill.
- **The agent does not draft a UVP.** UVP comes after Kano, using Kano's Attractive features as the differentiators.
- **The agent does not build a roadmap.** That is downstream of prioritization.


---


### 6.1 Purpose of the template

The skill's output is a **durable, public-safe, version-controllable artifact** named `vpc-result.md` (or `vpc-[persona-slug].md` for multi-persona canvases). This section is the **Gold Standard** the agent must refer to on every workshop.

The v2.0 template contains the **full VPC** � both Phase 1 (Customer Profile) and Phase 2 (Value Map), plus Phase 2.5 (Framework Selection). It does NOT contain a UVP or Fit Verdict. Those are downstream of the framework the user picks.

The template enforces:

- Tables as the primary output format (not paragraphs).
- Number rules: 1-2 main Jobs + 3-5 supporting, 3-5 Pains, 3-5 Gains, 1:1 mapping to Pain Relievers and Gain Creators, 1-3 bundle items.
- Every Job, Pain, Gain, Pain Reliever, Gain Creator, and Bundle item has a verbatim source quote (for Customer Profile items) or a one-sentence mechanism (for Value Map items).
- Hypotheses (1/5 support) are labeled, not promoted to locked.
- Rows are sorted by frequency/importance (dominant at top).
- Multi-tag allowed (a feature can be both a Pain Reliever and a Gain Creator).
- The output is public-safe: no client secrets, no private workspace context.

### 6.2 The file structure
### 6.2 The file structure

```markdown
---
project: [Project Name]
canvas_type: persona | segment
persona_or_segment: [name + one-sentence behavioral profile]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: draft | locked | needs_more_evidence
canvas: value-proposition-canvas v2.1
mode: research_ingestion | research_collection
multi_file_path: [path where vpc-result.md, shadow-backlog.md, value-proposition.md live]
gates_passed:
  - phase_1_accepted: YYYY-MM-DD
  - phase_2_pain_relievers_accepted: YYYY-MM-DD
  - phase_2_gain_creators_accepted: YYYY-MM-DD
  - phase_2_products_services_accepted: YYYY-MM-DD
  - phase_2_5_framework_selected: YYYY-MM-DD
---

## Section 6 — Gold Standard: `vpc-result.md` Template (v2.1)

> **v2.1 note:** this is **File 1 of 3** in the multi-file output structure. See **Section 7** for the full multi-file pattern (`vpc-result.md` + `shadow-backlog.md` starter + `value-proposition.md` + optional `.vpc-results/` directory). The agent creates `vpc-result.md` during the workshop; the agent creates a starter `shadow-backlog.md` at the end; the user writes `value-proposition.md` after Kano.

### 6.1 Purpose of the template

The skill's output is a **durable, public-safe, version-controllable artifact** named `vpc-result.md` (or `vpc-[persona-slug].md` for multi-persona canvases). This section is the **Gold Standard** the agent must refer to on every workshop.

The v2.1 template includes a new frontmatter field `multi_file_path` that records where the related files (`shadow-backlog.md`, `value-proposition.md`) live, so the user can navigate between them.

### 6.2 The file structure

```markdown
# VPC: [Project Name] — [Persona or Segment Name]

> One-line summary of the dominant Job.

## 1. Customer Segment / Persona

**Persona or segment**: [one sentence]

**Behavioral profile**: [workflow, tool stack, suspected pain — the sharpened version, not the demographic]

## 2. Customer Profile (Phase 1, accepted)

### 2.1 Customer Jobs (ranked by importance)

| # | Priority | Customer Job (one sentence) | Type (F / S / E) | Verbatim source quote | Status |
|---|---|---|---|---|---|
| J1 | Main | ... | Functional | "[quote]" — Interview #2 | Locked |
| J2 | Main | ... | Social | "[quote]" — Interview #1 | Locked |
| J3 | Supporting | ... | Emotional | "[quote]" — Interview #5 | Hypothesis (1/5) |

**Number rule:** 1-2 main jobs + 3-5 supporting jobs.

### 2.2 Pains (ranked by severity × frequency)

| # | Priority | Pain (one sentence) | Severity (1-5) | Frequency | IxDF Category | Quantified unit | Verbatim source quote | Status |
|---|---|---|---|---|---|---|---|---|
| P1 | Dominant | ... | 5 | per component | Dissatisfaction | 8 hours per component | "[quote]" — Interview #2 | Locked |
| P2 | Dominant | ... | 5 | per component | Challenge | 60% rework | "[quote]" — Interview #3 | Locked |
| P3 | Secondary | ... | 3 | per release | Dissatisfaction | n/a | "[quote]" — Interview #4 | Hypothesis (1/5) |

**Number rule:** 3-5 Pains.

### 2.3 Gains (ranked by expectation × outcome type)

| # | Priority | Gain (one sentence) | Expectation (Req / Exp / Des / Unexp) | Outcome type (F / E / S) | Verbatim source quote | Status |
|---|---|---|---|---|---|---|
| G1 | Dominant | ... | Required | Functional | "[quote]" — Interview #1 | Locked |
| G2 | Dominant | ... | Desired | Functional | "[quote]" — Interview #2 | Locked |
| G3 | Secondary | ... | Unexpected | Social | "[quote]" — Interview #3 | Hypothesis (1/5) |

**Number rule:** 3-5 Gains.

## 3. Value Map (Phase 2, accepted)

### 3.1 Pain Relievers (mapped 1:1 to Pains)

| # | Pain addressed | Pain Reliever (feature) | Mechanism | Status |
|---|---|---|---|---|
| R1 | P1: 8 hours per component on Slack | Single-link handoff page | A static page that bundles the Figma frame + spec + test cases, shareable as one URL. | Accepted |
| R2 | P2: 60% rework rate | spec.md generator from Figma | A Figma plugin reads the file and emits a structured markdown spec. | Accepted |
| R3 | P3: 50-page spec unread | spec confidence score | A heuristic score that flags how complete / unambiguous the spec is. | Accepted |

**1:1 mapping:** no orphans. Every locked Pain has exactly one Pain Reliever. A Pain Reliever that addresses a hallucinated Pain is muda.

### 3.2 Gain Creators (mapped 1:1 to Gains, multi-tag allowed)

| # | Gain produced | Gain Creator (feature) | Mechanism | Multi-tag | Status |
|---|---|---|---|---|---|
| C1 | G1: ship without rework | spec-driven diff review | When the spec changes, the dev sees a diff against the previous version and implements the diff. | (none) | Accepted |
| C2 | G2: send one link with everything | single-link handoff page | Same feature as R1 — a single feature can address both a Pain and a Gain. | also R1 | Accepted |
| C3 | G3: recognized as Design Engineer | public portfolio of design decisions | A public page showing the spec + rationale + outcome, as evidence of credible technical work. | (none) | Accepted |

**1:1 mapping:** no orphans. Every locked Gain has exactly one Gain Creator. Multi-tag is encouraged.

### 3.3 Products & Services (the bundle)

**Critical distinction:** Products & Services is the **bundle** (the offering shape), NOT a list of features. Pain Relievers and Gain Creators live inside the bundle.

| # | Bundle item | What the customer receives | Type (tangible / digital / intangible) | Contract | Jobs supported |
|---|---|---|---|---|---|
| S1 | spec.md generator | A Figma plugin + a code-side parser that emits a structured `spec.md` per component | Digital | License (per seat, annual) | J1, J2 |
| S2 | single-link handoff page | A web app that bundles design + spec + states + test cases + a11y into a shareable URL | Digital | Free tier + Pro subscription | J1, J3 |
| S3 | spec.md templates library | A pack of pre-built templates per component type (form, modal, list, etc.) | Digital | One-time purchase | J2, J3 |

**Number rule:** 1-3 bundle items. Reject vague bundles ("a platform", "a solution").

## 4. Framework Selection (Phase 2.5, accepted)

The user chose the following prioritization framework for the next step:

| Framework | Category | Use when | Default? |
|---|---|---|---|
| **Kano Model Strategist** | Satisfaction-based classification (Must-be / Performance / Attractive / Indifferent / Reverse / Questionable) | You want to identify the Attractive features that drive your UVP. | **Yes** |
| RICE | Reach × Impact × Confidence / Effort | You have quantitative reach data and need a numeric score. | No |
| MoSCoW | Must / Should / Could / Won't | You need a quick bucketing for release planning. | No |
| ICE | Impact × Confidence / Ease | You need a quick, intuitive score. | No |
| Impact/Effort matrix | 2D plotting | You want a visual prioritization. | No |

**Next step:** run the chosen framework's skill on the Pain Relievers + Gain Creators. For Kano, the next skill is `kano-model-strategist` in this playbook.

## 5. Workshop log

| Phase / Layer | Gate decision | Date | Notes |
|---|---|---|---|
| Persona/segment question | answered | YYYY-MM-DD | [one line] |
| Phase 1 (Jobs) | accepted | YYYY-MM-DD | [dominant Job] |
| Phase 1 (Pains) | accepted | YYYY-MM-DD | [dominant Pain] |
| Phase 1 (Gains) | accepted | YYYY-MM-DD | [dominant Gain] |
| Phase 1 (overall) | accepted | YYYY-MM-DD | [user confirmed] |
| Phase 2.1 (Pain Relievers) | accepted | YYYY-MM-DD | [N] Pain Relievers, no orphans |
| Phase 2.3 (Gain Creators) | accepted | YYYY-MM-DD | [M] Gain Creators, multi-tag flagged |
| Phase 2.5 (Products & Services) | accepted | YYYY-MM-DD | [K] bundle items |
| Phase 2.5 (Framework) | selected | YYYY-MM-DD | [framework name] |

## 6. Evidence log

| Claim | Source | Source type |
|---|---|---|
| [Claim 1] | [file or URL] | [interview / ticket / review / report] |
| [Claim 2] | ... | ... |

## 7. Dalsza lektura / Further reading

The sources that informed this workshop. See Appendix B for full citations.

## 8. Open Questions (take to real customers)

These are the questions the workshop surfaced that the user **should answer with more data, or take to a real customer**. The skill does not gate the workshop on these being answered.

- [ ] Q1: "If our product did not exist, what would you do? Walk me through it."
- [ ] Q2: "How much time or money does this problem cost you per month or per release?"
- [ ] Q3: "What is the most you have ever spent trying to solve this?"
- [ ] Q4: "Can you introduce me to three people who have this exact problem?"
- [ ] Q5: "If we could solve this problem overnight, what would change in your work next Monday?"
- [ ] Q6: [any custom question surfaced during the workshop]

## 9. What the agent did NOT do (Scope Boundary)

The following are **out of scope** for this skill and are the user's responsibility:

- **UVP drafting.** The user writes the UVP after Kano, using Kano's Attractive features as the differentiators. The agent does not draft UVPs.
- **Prioritization.** The user picks the framework in Phase 2.5, then runs the chosen framework's skill. The agent does not run prioritization.
- **Roadmap building.** Downstream of prioritization.
- **One-line marketing copy.** Different skill (copy skill).
- **Pricing, financial modeling, GTM.** Different skills.

## 10. Workshop end

The skill ends here. The user takes:

- Pain Relievers + Gain Creators (= features) → into the chosen framework's skill (e.g., `kano-model-strategist`) for prioritization.
- Bundle (Products & Services) → into product design and pricing.
- UVP → user writes it after Kano, using Kano's Attractive features as the differentiators.
```

### 6.3 How the agent uses the template

1. **At workshop start (Use Case 1).** The agent creates an empty `vpc-result.md` and commits to filling it in as the workshop progresses. The artifact exists, and it has a known structure.
2. **After persona/segment answer.** The agent fills in Section 1 (Customer Segment / Persona) with the user's answer + behavioral profile.
3. **At Phase 1 gate (Jobs accepted).** The agent fills in Section 2.1 (Jobs). The user validates.
4. **At Phase 1 gate (Pains accepted).** The agent fills in Section 2.2 (Pains). The user validates.
5. **At Phase 1 gate (Gains accepted).** The agent fills in Section 2.3 (Gains). The user confirms Phase 1 is locked.
6. **At Phase 2.1 gate (Pain Relievers accepted).** The agent fills in Section 3.1.
7. **At Phase 2.3 gate (Gain Creators accepted).** The agent fills in Section 3.2, with multi-tag flagged.
8. **At Phase 2.5 gate (Products & Services accepted).** The agent fills in Section 3.3.
9. **At Phase 2.5 framework selection gate.** The agent fills in Section 4 with the user's choice.
10. **At workshop end.** The agent creates `shadow-backlog.md` (starter, see Section 7 for template). The agent does **not** create `value-proposition.md` (the user writes it after Kano). The agent fills in Section 5 (Workshop log), Section 6 (Evidence log), Section 7 (Dalsza lektura), Section 8 (Open Questions), Section 9 (Scope Boundary), Section 10 (Workshop end).

### 6.4 The Fixed Parameters discipline

Fixed Parameters are a discipline borrowed from `socratic-dialogue`. A Fixed Parameter is a workshop conclusion that is **locked** for the duration of the project. The agent must:

- **Declare the Fixed Parameter** explicitly when it is set (e.g. "Dominant Pain is now P1: 8 hours per component on Slack").
- **Reference the Fixed Parameter by ID** in subsequent workshop moves (e.g. "the Pain Reliever for the dominant pain (P1) is...").
- **Refuse to silently edit a Fixed Parameter** mid-workshop. If the user wants to change it, the agent posts a Socratic probe: "If we change the dominant Pain from P1 to P3, then the dominant Job ranking must also change, and the Gate condition for Phase 1 must be re-verified. Are we re-opening the workshop from Phase 1, or are we treating this as a new canvas?"

This discipline protects the canvas from the most common failure mode in AI-assisted workshops: **conversational drift** — where the agent agrees to a new claim in minute 30 that contradicts the locked claim from minute 5, and the canvas ends up internally inconsistent.

### 6.5 Template variant: per-persona canvases

If the user runs the skill for multiple personas (one at a time, sequentially), the agent produces **one `vpc-result.md` per persona**, with a file name convention:

```
vpc-result-[persona-slug].md
```

For example, a project with three personas might produce:

```
vpc-result-pat-indie-designer.md
vpc-result-sam-startup-design-lead.md
vpc-result-alex-enterprise-design-engineer.md
```

The agent then produces a **comparison summary** (separate file or appendix) that shows the differences in dominant Job, dominant Pain, dominant Gain, and Pain Relievers / Gain Creators / Products & Services across the three canvases. The comparison is often the most strategically useful artifact: it reveals whether the personas are actually different value propositions or whether they can be served by the same bundle.

### 6.6 Template variant: segment canvas

If the user is designing for a whole segment (multiple personas in one segment), the agent runs the skill once with the source pool being the combined transcripts from all personas in the segment. The output is a single `vpc-result.md` with the segment-level dominant Job / Pain / Gain.

The segment canvas is **synthesized** across personas. Risks:

- The dominant Job / Pain / Gain become the **lowest common denominator**, which is usually a Required gain and never an Unexpected one.
- The segment canvas hides the fact that different personas have different dominance hierarchies.

**Rule of thumb:** a segment canvas is a starting point, not a destination. After producing it, run per-persona canvases for the 2-3 most distinct personas in the segment and compare. The differences are where Value Innovation lives.


### 6.3 How the agent uses the template

1. **At workshop start (Use Case 1).** The agent creates an empty `vpc-result.md` and commits to filling it in as the workshop progresses. The artifact exists, and it has a known structure.
2. **After persona/segment answer.** The agent fills in Section 1 (Customer Segment / Persona) with the user's answer + behavioral profile.
3. **At Phase 1 gate (Jobs accepted).** The agent fills in Section 2.1 (Jobs). The user validates.
4. **At Phase 1 gate (Pains accepted).** The agent fills in Section 2.2 (Pains). The user validates.
5. **At Phase 1 gate (Gains accepted).** The agent fills in Section 2.3 (Gains). The user confirms Phase 1 is locked.
6. **At Phase 2.1 gate (Pain Relievers accepted).** The agent fills in Section 3.1.
7. **At Phase 2.3 gate (Gain Creators accepted).** The agent fills in Section 3.2, with multi-tag flagged.
8. **At Phase 2.5 gate (Products & Services accepted).** The agent fills in Section 3.3.
9. **At Phase 2.5 framework selection gate.** The agent fills in Section 4 with the user's choice.
10. **At workshop end.** The agent fills in Section 5 (Workshop log), Section 6 (Evidence log), Section 7 (Dalsza lektura), Section 8 (Open Questions), Section 9 (Scope Boundary), Section 10 (Workshop end).

### 6.4 The Fixed Parameters discipline

Fixed Parameters are a discipline borrowed from `socratic-dialogue`. A Fixed Parameter is a workshop conclusion that is **locked** for the duration of the project. The agent must:

- **Declare the Fixed Parameter** explicitly when it is set (e.g. "Dominant Pain is now P1: 8 hours per component on Slack").
- **Reference the Fixed Parameter by ID** in subsequent workshop moves (e.g. "the Pain Reliever for the dominant pain (P1) is...").
- **Refuse to silently edit a Fixed Parameter** mid-workshop. If the user wants to change it, the agent posts a Socratic probe: "If we change the dominant Pain from P1 to P3, then the dominant Job ranking must also change, and the Gate condition for Phase 1 must be re-verified. Are we re-opening the workshop from Phase 1, or are we treating this as a new canvas?"

This discipline protects the canvas from the most common failure mode in AI-assisted workshops: **conversational drift** � where the agent agrees to a new claim in minute 30 that contradicts the locked claim from minute 5, and the canvas ends up internally inconsistent.

### 6.5 Template variant: per-persona canvases

If the user runs the skill for multiple personas (one at a time, sequentially), the agent produces **one `vpc-result.md` per persona**, with a file name convention:

```
vpc-result-[persona-slug].md
```

For example, a project with three personas might produce:

```
vpc-result-pat-indie-designer.md
vpc-result-sam-startup-design-lead.md
vpc-result-alex-enterprise-design-engineer.md
```

The agent then produces a **comparison summary** (separate file or appendix) that shows the differences in dominant Job, dominant Pain, dominant Gain, and Pain Relievers / Gain Creators / Products & Services across the three canvases. The comparison is often the most strategically useful artifact: it reveals whether the personas are actually different value propositions or whether they can be served by the same bundle.

### 6.6 Template variant: segment canvas

If the user is designing for a whole segment (multiple personas in one segment), the agent runs the skill once with the source pool being the combined transcripts from all personas in the segment. The output is a single `vpc-result.md` with the segment-level dominant Job / Pain / Gain.

The segment canvas is **synthesized** across personas. Risks:

- The dominant Job / Pain / Gain become the **lowest common denominator**, which is usually a Required gain and never an Unexpected one.
- The segment canvas hides the fact that different personas have different dominance hierarchies.

**Rule of thumb:** a segment canvas is a starting point, not a destination. After producing it, run per-persona canvases for the 2-3 most distinct personas in the segment and compare. The differences are where Value Innovation lives.


---
- `legible-agent-output` (this repo) — applies to every user-facing string the agent emits during the workshop.
- `kano-model-strategist` (this repo) — **the next step** after the skill finishes. The user takes the Feature Brainstorm and classifies the candidates as Must-be / Performance / Attractive / Indifferent / Reverse / Questionable.
## Section 7 — Multi-file Output Structure (v2.1)

### 7.1 Why multi-file

The v2.0 skill produces a workshop output. The v2.1 skill extends this with a **three-file structure** (plus a hidden directory for raw ideas) to prevent knowledge rot and decision paralysis. Each file has a different lifecycle, audience, and update cadence.

The agent asks the user **where to save the three files** at the very start of the workshop (Step 0 in `SKILL.md`). The user can specify a directory path; default is the current working directory.

### 7.2 The three files

| File | Created by | Updated by | Audience | Lifecycle |
|---|---|---|---|---|
| `vpc-result.md` | The agent (during the workshop) | The agent (only at gates, with explicit user accept) | The user + downstream skills (Kano, UVP, roadmap) | Per persona/segment. Old versions archived. |
| `shadow-backlog.md` (starter) | The agent (at end of workshop) | The user (after running Kano) | The user + product/engineering team | Continuous. Features move through prioritization → story map → implementation. |
| `value-proposition.md` | The user (after Kano) | The user (when UVP changes) | The user + team + organization (for alignment) | Strategic. Reviewed periodically (e.g., quarterly). |
| `.vpc-results/` directory (optional) | The user (long-term) | The user | The user | Continuous. Raw feature ideas, not yet validated. |

### 7.3 Template: `vpc-result.md`

The full template is in Section 6. The v2.1 change is the frontmatter — add a `multi_file_path` field so the user can track where the related files live:

```yaml
---
project: [Project Name]
canvas_type: persona | segment
persona_or_segment: [name + one-sentence behavioral profile]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: draft | locked | needs_more_evidence
canvas: value-proposition-canvas v2.1
mode: research_ingestion | research_collection
multi_file_path: [path where vpc-result.md, shadow-backlog.md, value-proposition.md live]
gates_passed:
  - phase_1_accepted: YYYY-MM-DD
  - phase_2_pain_relievers_accepted: YYYY-MM-DD
  - phase_2_gain_creators_accepted: YYYY-MM-DD
  - phase_2_products_services_accepted: YYYY-MM-DD
  - phase_2_5_framework_selected: YYYY-MM-DD
---
```

### 7.4 Template: `shadow-backlog.md` (starter, written by the agent)

The agent writes this file at the end of the workshop, after Phase 2.5 (Framework Selection). The starter contains the Pain Relievers and Gain Creators (= features) **without priorities**. The user (or the chosen framework's skill) fills in the priorities after.

```markdown
---
project: [Project Name]
related_vpc: vpc-result.md
framework_selected: [Kano | RICE | MoSCoW | ICE | custom]
framework_skill: [kano-model-strategist | custom]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: starter | prioritized | in_story_map | implemented | dropped
---

# Shadow Backlog: [Project Name]

> Prioritized features awaiting Story Map inclusion and implementation. Updated by the user after running the prioritization framework on the Pain Relievers + Gain Creators from `vpc-result.md`.

## Features awaiting prioritization

| # | Feature (from vpc-result.md) | Type (PR / GC) | Mechanism | Kano category | Priority | Notes |
|---|---|---|---|---|---|---|
| F1 | [feature name] | PR | [one-sentence mechanism] | [Must-be / Performance / Attractive / Indifferent / Reverse / Questionable] | [P0 / P1 / P2 / P3] | [notes] |
| F2 | [feature name] | GC | [one-sentence mechanism] | ... | ... | ... |
| F3 | [feature name] | PR (multi-tag) | [one-sentence mechanism] | ... | ... | ... |

**Multi-tag note:** if a feature is both a Pain Reliever and a Gain Creator (multi-tag), it appears once with `Type: PR (multi-tag)`. The mechanism column reflects both roles.

## Wildcards (parked)

| # | Wildcard idea | Why parked | Next step |
|---|---|---|---|
| W1 | [wildcard idea] | [why it did not make it into the locked Customer Profile] | [what would unlock it — e.g., more user research, a different segment] |

## Hypotheses (need more evidence)

| # | Hypothesis (from vpc-result.md) | Type (Job / Pain / Gain) | Source count | What evidence would lock it |
|---|---|---|---|---|
| H1 | [hypothesis] | [Job / Pain / Gain] | [1/5] | [specific evidence to gather] |

## Status legend


Each feature can have one of these statuses (updated by the user as features move through the pipeline):

- **starter** — just created, no priorities yet.
- **prioritized** — Kano (or chosen framework) classification done.
- **in_story_map** — moved to the active Story Map, awaiting sprint planning.
- **implemented** — built and shipped.
- **dropped** — killed (with a reason).

## Workflow

1. After the VPC workshop, the agent creates this file with the Pain Relievers + Gain Creators as features. Status: `starter`.
2. The user runs the chosen prioritization framework (e.g., `kano-model-strategist`) on the features.
3. The user updates this file with the framework classifications and priorities. Status: `prioritized`.
4. The user moves prioritized features to the active Story Map for the next sprint. Status: `in_story_map`.
5. The user marks features as `implemented` (shipped) or `dropped` (killed) as the project progresses.

## Why this file matters


`shadow-backlog.md` is the buffer between the workshop and the active Story Map. Without it:

- Validated features get lost in notebooks, Slack threads, or Notion pages.
- The user cannot see which features are validated but not yet prioritized.
- The story map gets polluted with unvalidated ideas.
- Decision paralysis sets in: "Should I build this? Was this validated? Is this prioritized?"

With it:

- The user can see at a glance: what is validated, what is prioritized, what is in flight, what is dropped.
- The Story Map only pulls from `prioritized` features — discipline enforced by file separation.
- Each status transition is a discrete event the user can review.

### 7.5 Template: `value-proposition.md` (written by the USER, not the agent)

The agent does **not** write this file. The user writes it after running the chosen prioritization framework on `shadow-backlog.md` and identifying the Attractive features (the differentiators).

```markdown
---
project: [Project Name]
related_vpc: vpc-result.md
related_shadow_backlog: shadow-backlog.md
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: draft | active | retired
version: [1.0 | 1.1 | 2.0 | etc.]
---

# Value Proposition: [Project Name]

## UVP (Unique Value Proposition)


Our "[product/service]" help(s) "[customer segment]" who want to "[customer's jobs to do / problems to solve]" by "[your verb]" and "[your verb]", unlike "[competing value proposition]."


> [Final UVP, one sentence]

## Why this UVP


[3-5 sentences explaining which features from `shadow-backlog.md` are the Attractive (delighter) features, why they differentiate from the competition, and how they connect to the dominant Job, Pain, and Gain in `vpc-result.md`.]

## The differentiators (Attractive features from Kano)


| # | Feature | Why it is a differentiator |
|---|---|---|
| F1 | [feature name] | [1-2 sentences] |
| F2 | [feature name] | [1-2 sentences] |

## The supporting features (Performance + Must-be)


| # | Feature | Kano category | Why it must ship |
|---|---|---|---|
| F3 | [feature name] | Performance | [1-2 sentences] |
| F4 | [feature name] | Must-be | [1-2 sentences] |

## What we are NOT (explicitly)


- [feature] — out of scope. Why: [reason from `vpc-result.md`].
- [feature] — parked in `shadow-backlog.md` as a wildcard. Why: [reason].

## Review cadence


- [Quarterly | Monthly | per release] review with the team.
- Update this file when the UVP changes materially (segment shift, new competition, new Attractive feature).
- Re-run the VPC workshop if the dominant Job, Pain, or Gain shifts significantly.

## What the agent does NOT do (with this file)


- The agent does **not** write the UVP. UVP drafting is the user's responsibility.
- The agent does **not** update this file on its own. The user updates it.
- The agent does **not** propose changes to this file unless the user asks. The UVP is a strategic document; the agent does not own the strategy.

### 7.6 Template: `.vpc-results/` directory contents (raw feature ideas)

The `.vpc-results/` directory is for raw feature ideas that have **not** been validated through a VPC workshop. The user maintains this directory. The skill does not create or manage it; the skill only references it as a staging area.

**Suggested file format inside `.vpc-results/`:**


```markdown
---
idea: [one-sentence description]
source: [where the idea came from — conversation, note, brainstorm]
created: YYYY-MM-DD
status: raw | in_research | validated | dropped
---

# Raw idea: [one-sentence description]


> [longer description, context, link to source]

## Next step


- [ ] Run the idea through a VPC workshop (multi-file output: vpc-result.md + shadow-backlog.md + value-proposition.md).
- [ ] Drop the idea (reason: [why it does not warrant validation]).
- [ ] Park the idea (reason: [why it is not ready for validation yet]).

```

**Naming convention:** `idea-[slug].md` per idea. One file per raw idea. The user can `ls .vpc-results/` to see all raw ideas at a glance.

**Why this directory exists:** the production backlog (the user's story map, kanban, sprint board) should only contain validated features. Raw ideas pollute the backlog. `.vpc-results/` is the buffer that keeps raw ideas out of the production system until they are validated.

### 7.7 The handoff to Kano (or the chosen framework)

After the workshop, the multi-file output is in place. The user runs the chosen prioritization framework on `shadow-backlog.md`. The most common path:

1. **VPC workshop** (this skill) → `vpc-result.md` + starter `shadow-backlog.md`.
2. **Kano Model Strategist** (next skill in this playbook) → user runs Kano on the features in `shadow-backlog.md`.
3. **User updates `shadow-backlog.md`** with Kano classifications + priorities. Status: `prioritized`.
4. **User writes `value-proposition.md`** using Kano's Attractive features as the differentiators. Status: `draft` → `active` after team review.
5. **User moves prioritized features** from `shadow-backlog.md` to the active Story Map for the next sprint. Status: `in_story_map`.

The agent does not run any of steps 2-5. The user owns the handoff.

### 7.8 What the agent does with the multi-file structure


| File | The agent's role |
|---|---|
| `vpc-result.md` | **Writes during the workshop** at each gate. Updates with explicit user accept. |
| `shadow-backlog.md` (starter) | **Writes once at the end of the workshop** with Pain Relievers + Gain Creators, no priorities. |
| `value-proposition.md` | **Does not write.** The user writes the UVP after Kano. |
| `.vpc-results/` | **Does not create or manage.** The user maintains the raw ideas directory. The agent may suggest parking wildcards there. |

### 7.9 Why this matters (knowledge rot prevention)

The single biggest risk in a VPC-driven product is **knowledge rot**: the VPC becomes a stale artifact no one updates, and the product drifts away from the customer. The multi-file structure prevents rot by:

- **Separating lifecycles.** Each file updates at its own cadence. The VPC updates per persona. The shadow backlog updates per feature. The UVP updates per strategic shift.
- **Separating audiences.** Each file has a different reader. The VPC is for the workshop owner. The shadow backlog is for the product team. The UVP is for the organization.
- **Separating decisions.** Each file captures a different kind of decision. The VPC captures the customer profile. The shadow backlog captures the feature priority. The UVP captures the strategic positioning.

When a decision changes, the user knows which file to update. When a file is stale, the user knows which file to refresh. When a file is not used, the user knows it can be archived.

---

## Appendix A — Socratic Question Library

A working library, organized by layer and purpose. The agent picks the most relevant question for the moment; this is not a script. In v1.2 the Socratic engine is used for **validation**, not extraction — so this library is smaller and more targeted than the legacy v1.0/v1.1 version.

### A.1 Job Extraction (Layer 1)

For validation of extracted Jobs:

- *"Job 2 has 3/5 support. Are the quotes from one persona archetype or several? If one, is it persona-specific, or generalizable?"*
- *"Is the dominant Job actually observable, or is it a designer projection?"*
- *"Are any Jobs synonyms of each other — should they be merged?"*
- *"Job 3 has 1/5 support (Hypothesis). Do you have 2-3 more interviews queued, or do we park it?"*

For workshop-from-scratch fallback (rare in v1.2):

- *"If you could not name a single feature, how would you describe the change you want to cause?"*
- *"What is the 'hole' in the customer's day that your product is the 'drill' for?"*

### A.2 Pain Extraction (Layer 2)

For validation of extracted Pains:

- *"Pain #2 has 3/5 support. The quotes are vivid. But is the Pain 'developers guess' or 'no machine-readable contract exists'? The first is a symptom; the second is the root cause. Which framing matches the data?"*
- *"If this Pain happened once a week, would the customer pay to make it stop? What does the source quote say about willingness to pay?"*
- *"What does the customer currently do to escape this Pain? Is the workaround cheap or expensive?"*
- *"Your competitor report says [X]. Does that contradict the Pain you described, or refine it?"*
- *"Has the Pain been validated by at least three independent sources? If not, mark as Hypothesis."*
- *"This Pain has severity 2 and no quantified unit. Is it a scratched-knee that should be dropped, or a hypothesis that needs more data?"*

For Broken-Leg Test:

- *"Severity, frequency, workaround cost — score 1-5 on each. A real broken-leg Pain scores 4+ on at least two of three."*

### A.3 Outcome Test (Layer 3)

For validation of extracted Gains:

- *"If we produce this Gain successfully, what is the specific difference it makes in the customer's life or your bottom line?"*
- *"If I gave you exactly what you asked for, but the deeper problem remained, has the Gain been produced?"*
- *"What changes in the customer's behavior or your metrics when this Gain is realized?"*
- *"Is this Gain the **result of the job** (Rule A error) or the **inverse of a Pain** (Rule B error)?"*
- *"Trace this Gain back five levels — what is the root benefit, not the symptom?"*
- *"Is this a required, expected, desired, or unexpected gain?"*
- *"Is this gain functional, emotional, or social?"*

### A.4 Feature Brainstorm (Layer 4)

For validation of brainstormed features:

- *"Feature F2 claims to address Pain P4. Does the mechanism actually address the Pain, or does it just rename the problem?"*
- *"What is the Minimum Path to Awesome for this feature — the smallest unit of bundle usage that produces the Gain?"*
- *"Can the customer feel this feature's value in one session, or do they have to wait a quarter?"*
- *"Am I generating features I would generate for any product (generic), or features specific to this Customer Profile?"*
- *"This feature has no clear Pain or Gain it addresses. Is it a wildcard, or is it muda?"*

### A.5 Open Questions (parked for the user)

These are surfaced as **Open Questions** in the artifact, not as gates. The user takes them to real customers.

- *"If our product did not exist, what would you do? Walk me through it."*
- *"How much time or money does this problem cost you per month or per release?"*
- *"What is the most you have ever spent trying to solve this?"*
- *"Can you introduce me to three people who have this exact problem?"*
- *"If we could solve this problem overnight, what would change in your work next Monday?"*

### A.6 Research Plan (Section 0, Use Case 2)

When the user has no data:

- *"What does Pat do in a typical day, in their own workflow?"*
- *"What tool does Pat reach for first when they sit down to design?"*
- *"What does Pat wish was different about their work, even if they have never said it out loud?"*
- *"Who else does Pat talk to about their work (peers, communities, mentors)?"*
- *"What is Pat not doing, that they would do if their life were easier?"*

For interview design:

- *"What question would I ask that the persona cannot answer with a one-word reply? What about with a feature wishlist?"*
- *"What have I forgotten to ask? What would I learn if I shadowed Pat for an hour?"*

---

## Appendix B — Bibliography (Dalsza lektura)

The agent should close every workshop with a one-line note on which sources informed each step. The full list lives here.

### B.1 Foundational canvas and jobs literature

- Osterwalder, A., Pigneur, Y., Smith, A. (2014). *Value Proposition Design*. Wiley. — The VPC itself. Note: Strategyzer has since clarified that Alan Smith is the third co-author of the 2014 edition; earlier printings credited Papadakos.
- Strategyzer (canonical source: https://www.strategyzer.com). — Maintains the official canvas and the Business Model Canvas that VPC extends.
- Interaction Design Foundation (2024). *The Value Proposition Canvas*. — Synthesizes Osterwalder et al. with worked examples (Amazon, IxDF) and is the source for the canonical Pain and Gain categories used in Layer 2 and Layer 3.
- Christensen, C. M., Hall, T., Dillon, K., Duncan, D. S. (2016). *Know Your Customers' Jobs to Be Done*. Harvard Business Review. — JTBD core.
- Ulwick, A. W. (2016). *Jobs to be Done: Theory to Practice*. Idea Bite Press. — Outcome-Driven Innovation.
- Klement, A. (2016). *When Coffee and Kale Compete*. — Job Story format and outcome thinking.
- Patton, J. (2014). *User Story Mapping*. O'Reilly. — Origin of the job-story discipline.

### B.2 Strategy, failure, and innovation

- Kim, W. C., Mauborgne, R. (2005). *Blue Ocean Strategy*. Harvard Business Review Press. — Value Innovation, four actions framework.
- Ries, E. (2011). *The Lean Startup*. Crown Business. — Build Trap, validated learning, MVPs.
- Perri, M. (2018). *Escaping the Build Trap*. O'Reilly. — The modern Build Trap critique.
- Levy, J. (2015). *UX Strategy*. O'Reilly. — UX Strategy core, demand validation, porters-of-progress.
- Christensen, C. M. (1997). *The Innovator's Dilemma*. Harvard Business Review Press. — Why "good" companies fail.
- Blank, S. (2013). *The Four Steps to the Epiphany*. K&S Ranch. — Customer Development, GOOB (Get Out Of the Building). The operating system for VPC research.

### B.3 Lean product and pain-driven design

- Gothelf, J., Seiden, J. (2016). *Lean UX*. O'Reilly. — Three-level outcome (functional / emotional / long-term), collaborative design.
- Hunt, V. (2016). *The Product Taster / Sprint to Market*. — Pain-Driven Design, broken leg vs scratched knee.
- Womack, J. P., Jones, D. T. (1996). *Lean Thinking*. Simon & Schuster. — Muda (waste) elimination.

### B.4 Socratic dialogue and reasoning

- Vlastos, G. (1983, 1994). *Socrates: Ironist and Moral Philosopher.* — The Elenchus as method.
- Seeskin, K. (1987). *Dialogue and Discovery.* — Socratic terminology anchoring.
- Kahneman, D. (2011). *Thinking, Fast and Slow.* Farrar, Straus and Giroux. — System 1/System 2, cognitive strain, substitution (answering an easier question than the one asked), and WYSIATI. Grounds Confidence Gating and the Socratic Pause.
- Kahneman, D., Klein, G. (2009). "Conditions for Intuitive Expertise: A Failure to Disagree." *American Psychologist*, 64(6), 515-526. — Adversarial collaboration; grounds the Adversarial Probing stance.
- Mitchell, D. J., Russo, J. E., Pennington, N. (1989). "Back to the Future: Temporal Perspective in the Explanation of Events." *Journal of Behavioral Decision Making*, 2(1), 25-38. — Origin of "prospective hindsight"; grounds the Faithfulness Check (Focused Self-Query).
- Klein, G. (2007). "Performing a Project Premortem." *Harvard Business Review*. — The pre-mortem technique built on prospective hindsight.
- Torres, T. (2021). *Continuous Discovery Habits.* Product Talk LLC. — Product-discovery adaptation of the pre-mortem technique (not the originating source).
- `socratic-dialogue` skill in this playbook — Socratic engine used for **validation** in v1.2 (Layer 1 validation, Layer 2 Socratic Pause, Layer 3 Outcome Test filters, Layer 4 brainstorm challenge). Not used for extraction in v1.2.

### B.5 Business analysis and requirements

- IIBA (2018). *A Guide to the Business Analysis Body of Knowledge (BABOK) v3*. — Stakeholder analysis, requirements anchoring.
- Wiegers, K., Beatty, J. (2013). *Software Requirements*. Microsoft Press. — Quality of requirements, verifiability.

### B.6 Sales-side validation (for money-shot questions)

- Rackham, N. (1988). *SPIN Selling*. — Implication, need-payoff, money-shot question patterns.
- Weiss, A. (2013). *Value-Based Fees*. Wiley. — Alan Weiss questioning framework, legacy and meaning questions.
- Hopkins, T. (1980). *How to Master the Art of Selling*. — Classic money-shot sequencing.

### B.7 Composed-with skills in this playbook

- `socratic-dialogue` (this repo) — Socratic engine, used for **validation** in v1.2.
- `kano-model-strategist` (this repo) — **the next step** after the skill finishes. The user takes the Feature Brainstorm and classifies the candidates as Must-be / Performance / Attractive / Indifferent / Reverse / Questionable.
- `legible-agent-output` (this repo) — applies to every user-facing string the agent emits during the workshop.
