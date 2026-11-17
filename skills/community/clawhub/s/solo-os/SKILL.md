---
name: solo-os
description: >-
  Expert-roundtable decision framework: the AI convenes a panel of experts with
  conflicting stances who cross-examine one issue from several angles and shape it
  into 2–3 candidate options, one recommendation, and the evidence each candidate
  still lacks. The vote shows where the experts lean, not a verdict; the human
  confirms before anything lands. Includes four tables (role / blind / human /
  contrarian) drawing on four sources of cognitive diversity, a three-dimension role-generation spec, a "will forgetting this hurt
  tomorrow?" persistence gate, an optional outside seat (a blind answer from another
  vendor's model), and a four-layer knowledge-immunity model. For solo
  developers and small teams making architecture, priority, and trade-off decisions.
  Invoke explicitly.
---

# Solo OS · roundtable core — an expert-roundtable decision framework for solo developers

> This is the roundtable core of Solo OS — the part of a larger collaboration system that has been cleaned up for public use. More modes will be added as they are made generic.

**Goal**: upgrade "ask the AI for an answer" into "make a panel of experts with conflicting stakes look at the same issue from several angles, in front of you, so the side you would have missed shows up before you decide". The AI is a thinking amplifier, not a ghostwriter — its value is not in producing the one right answer but in putting every load-bearing face of a decision on the table at once.

This framework is distilled from a collaboration system that has run inside a real project for over half a year and produced three-hundred-plus decision records. Every case study below actually happened; only the identifying details have been removed.

---

## Core principles

1. **The AI is a thinking amplifier, not a ghostwriter** — it simulates several experts cross-examining an issue from different angles; it does not hand down a single answer.
2. **The roundtable shapes the options; the human decides** — the table converges the issue into candidates and a recommendation (the vote expresses where the experts lean; it is not a verdict — see "What the roundtable is for" below). Neither the user alone nor the AI alone decides. Nothing lands until the user says "confirm" or "go".
3. **Decisions persist in layers** — once the user confirms a recommendation, run the gate question: "if we forgot this decision tomorrow, would the project get hurt?" The answer decides which layer it sinks into (see "The persistence gate" below).
4. **Fight forgetting proactively** — the moment a discussion's outcome could be lost to the next session, push for it to be written down. Don't wait to be asked.
5. **A clean division of labor** — the human owns direction, creativity, and value judgments; the AI owns rigor, consistency, and actively surfacing contradictions and blind spots across documents. The AI never changes direction on its own and never executes a strategic decision without confirmation.

---

## The roundtable protocol (core loop)

```text
prior-decision scan → frame the issue → debate (cross-examination, not parallel
statements) → vote (each expert's lean, with ratios and reasons recorded) → fact
verification (when the issue asserts facts) → candidates + recommendation + missing
evidence → persistence gate → user confirmation → write-through
```

Minority opinions are recorded too — they are the re-entry points for future reopenings.

### What the roundtable is for: shaping options, not reviewing them

The roundtable handles **questions you have not thought through yet**. It always produces three things:

1. **2–3 candidate options**
2. **One recommendation**
3. **What evidence each candidate still lacks before it can be decided** — name the command to run, the file to read, or the data to wait for

The vote stays, but it means "which way the experts lean", not "what was decided". Every expert at the table is played by the same model and knows exactly the same facts, so they cannot give one another new information — a vote count is not evidence on its own. Once the user confirms a recommendation it lands as usual, and the missing-evidence list is written down with it; a recommendation resting on zero verified facts is marked "unverified" where it lands.

Reach for something else when:

- **You already have a finished artifact and want it picked apart** → a review checklist, item by item
- **You want to know whether a conclusion actually holds** → the outside seat below, or a cross-vendor adversarial review
- **You only want ideas spread out, not converged** → a brainstorm; don't force a recommendation

### Checkpoint 1: prior-decision scan (before framing, before any expert speaks)

Search your decision records, plans, and authorization logs with the issue's keywords. **An issue phrased as "what does X actually mean?" is itself a red flag** — it presumes X is undefined, when X was very likely settled long ago.

- Found a standing decision → **rewrite the issue** as "how do we land that decision", and pin the original text to the table as a hard constraint
- An expert who wants to overturn an old decision must flag it explicitly — "this opinion requires revoking the decision of <date>" — never slip it through as a side effect
- When the implementation disagrees with an authorized design, the default is to fix the implementation, not to re-pick the design

> **Real case (anonymized)**: a five-expert roundtable voted 5:0 to "redefine" a concept — one the project owner had settled, in the opposite direction, three months earlier. Unanimous, well argued, great atmosphere; the whole table was voided. The lesson: post-vote fact checking cannot catch this class of accident, because the error was committed the moment the issue was framed.

### Checkpoint 2: fact verification (after the vote, before persisting)

When the issue involves **factual claims about the current state of things** ("what can the system do", "what does the spec cover"), verify every fact cited in the debate against the source-of-truth documents after the vote. **Unanimity is not verification — a 5:0 may just be five people sharing one blind spot.**

> **Real case (anonymized)**: two enthusiastic roundtables "invented" seven concepts. Checked against the spec afterwards, all seven already existed — several defined in ways that contradicted the table's version. The strength of a consensus says nothing about its truth.

### Vote accounting

When a vote is written down, the ratio must be split by evidence: write `5:0 (2 verified / 3 reasoned)`, never a bare `5:0`.

- **Verified** = the vote's basis was a command actually run, a file actually read, or citable data — and the record names which one. If you can't name it, it isn't verified.
- **Reasoned** = argument only, nothing checked on the spot. **A reasoned vote is not a bad vote** — it just must not hide behind the tally.
- A unanimous vote with zero verification gets a suffix: "unverified".

> **Real case (anonymized)**: an exhaustive scan of three-hundred-plus decision records found that over half recorded vote ratios — and **zero** recorded per-vote evidence. Whether each vote rested on a measurement or a hunch evaporated at the moment of writing, so the question "how much of our decision-making stands on evidence?" had become unanswerable. Start keeping the ledger first; decide whether to build a harder gate once there are samples.

---

## The outside seat: a blind answer from another vendor's model

Every expert at the table is played by the same model, so the whole table can share one blind spot — that vendor's training biases. Unanimity cannot catch this, and neither can more experts from the same model. For architecture-level or otherwise costly-to-reverse issues, add an **outside seat**: a model from a *different* vendor answers the same issue, blind.

1. **Same issue, no conclusions** — give the outside model the issue and the source material; never the table's debate, vote, or conclusion.
2. **Freeze first, then open** — write down the table's vote and conclusion before reading the outside answer. Never revise the original judgment afterwards to look as if the table saw it coming.
3. **No vote** — the outside seat does not vote. Compare its answer point by point and classify each one: missed by the table / factual error (on either side — check it against the source) / a framing the table never considered / a trade-off weighed differently. Where the two disagree, list both. Major omissions are the user's call, not the host model's.
4. **Know what leaves the machine** — the material goes to a third-party provider and cannot be recalled. Strip credentials, configuration values, customer data, and anything you would not post publicly. Give the outside model a copy of the material, never write access to your repository.
5. **Record every run** — including the runs where the outside answer never arrives — so the seat is judged later on real numbers, not impressions.

How you reach the second model is up to you (another vendor's CLI, API, or chat window). This skill installs and runs nothing.

> **Real case (anonymized)**: across the first 26 roundtables run with an outside seat (eight projects), the outside answer arrived 24 times. In 20 of those the user adopted at least one of its new points; in 6 it changed the table's main conclusion in whole or in part; in 3 it found defects that really existed in code or production — one an unauthenticated endpoint that would have exposed stored credentials the day the keys were configured. After that review the seat became standing practice.

---

## Role generation

### Three dimensions

Every role is defined along three independent axes — a job title alone is not a role:

| Dimension | Meaning | Examples |
|-----------|---------|----------|
| Functional role | Which stake it represents | security, performance, cost, UX, compliance |
| Seniority level | Judgment tier, set by issue complexity | L1 senior practitioner → L2 domain authority → L3 world-class |
| Thinking style | Preferred mode of reasoning | analytical, intuitive, divergent, critical |

### Issue complexity → role level (default high; when unsure, go higher)

| Issue tier | Signals | Role level |
|-----------|---------|------------|
| L1 execution | "how do I configure", "fix this for me" | senior engineer — title + stack |
| L2 design (default) | "how should we design", "compare options" | domain authority — title + one or two lines of experience |
| L3 strategy | "should we do this at all", "long-term direction" | field pioneer — title + landmark achievement + thinking paradigm |

Give each role a **concrete experience anchor**; roles that are bare titles converge in debate. "Chief architect" is weaker than "chief architect who has handled consistency under a million concurrent connections" — the latter knows what to be afraid of.

### Mandatory diversity constraints

- Five roles by default; adjust to 3–7 by the number of dimensions in play
- At least one role's thinking style must differ from the majority (guards against authority convergence)
- Functional roles must not overlap — every expert represents an independent load-bearing face

---

## Four tables (four sources of cognitive diversity)

| Table | Diversity source | Fits |
|-------|-----------------|------|
| **Role table** · 角色桌 (default; formerly 1a quick roundtable) | role difference | general "how do we build it" discussions |
| **Blind table** · 盲桌 (formerly 1b split-perspective debate) | information difference (each perspective reads only its own material) | complex issues needing full-surface evaluation |
| **Human table** · 真人桌 (formerly 1c mixed roundtable) | ontological difference (a real human votes at the table) | the user has a stance, or holds private information the AI lacks |
| **Contrarian table** · 反调桌 (formerly 1d role adversarial) | thinking-mode difference (rational pole vs intuitive pole) | "should we", "priority", value-judgment calls, "I'm torn" |

**Smart selection**: the AI recommends a table from the user's wording — "discuss / design" → role table; "should we / is it worth it / I'm torn" → contrarian table; "analyze from multiple angles" → blind table; "I think we should…" → human table. When the recommendation is not the role table, it is a one-line prompt — "Suggest the **contrarian table** (this is a priority trade-off). Reply `role table` / `blind table` / `human table` / `contrarian table` to switch." When talking to the user in Chinese, use these exact names: 角色桌 / 盲桌 / 真人桌 / 反调桌. On a weak consensus (3:2), proactively suggest switching tables.

**The human table's special rule**: the human casts one equal vote, and that vote counts as the confirmation (the human already participated — no second confirmation; the persistence gate still runs), revocable afterwards. Human participation is a spectrum — observer → questioner → participant → director — adjustable at any time.

**The contrarian table's red line**: simulating "an angel investor's perspective" is fine; **simulating a specific real person is not**. Simulated-human roles need a concrete persona (occupation + the dimension they care about), generated fresh for each issue, never reused from a fixed list.

> **Real case (anonymized)**: discussing a registration-agency service, the rational experts unanimously recommended outsourcing. After a "budget-conscious solo developer" persona joined the table, the user followed that thread with one question — and the plan was rewritten as do-it-yourself: ninety percent cheaper for two extra hours of paperwork. Value-judgment issues without someone at the table who hates spending money produce answers that are correct and expensive.

**Legal switches**: the role table can escalate to the human or contrarian table; the blind table can chain into the human table; **blind table + human table are mutually exclusive** — a human's all-knowing view breaks the information isolation.

---

## The persistence gate (where a decision goes)

The user saying "confirm" is not the end of the roundtable — it is the start of the write-through. First, the gate:

```text
"If we forgot this decision tomorrow, would the project get hurt?"
  ├─ yes       → write a formal decision record
  ├─ partially → write a memo
  └─ no        → update the plan document directly; no new decision record
```

Then cascade automatically: scan the affected documents (plan, roadmap, spec, workflow files, indexes) → apply the edits in one batch → output a cascade report (which files changed, how, and what was deliberately left unchanged and why). **A pure preference call ("A over B" with no follow-up action) does not cascade** — over-recording is as harmful as not recording.

> **Real case (anonymized)**: one roundtable spent five rounds constructing an elegant governance regime — ten resolutions, six rules, internally consistent, the whole table satisfied. The user read it and asked one question: "where is the null option?" — had *doing nothing* ever been evaluated? On re-evaluation, "null option plus one small patch" won 5:0 and the entire regime was scrapped. The lesson is now a standing rule: **in any roundtable about whether to build a mechanism, the null option must be a formal candidate.** A methodology is worth most at the moment it catches itself being wrong.

---

## Knowledge persistence: the four-layer immunity model

Lessons produced by roundtables sink into four layers by **enforcement strength**, on the metaphor of an immune system:

```text
L0 barrier        ← hooks / CI gates / lint: technically enforced, depends on no one's memory
L1 innate         ← always-on rules: loaded into every session automatically
L2 adaptive       ← trigger-based technique library: activates on keyword match
L3 memory         ← decision records + archive: low-frequency but traceable
```

**Routing principle: knowledge sinks downward** — whatever can live in L0 must not live in L1; whatever can live in L1 must not live in L2. One line of hook in L0 beats ten lines of rules in L1 beats a paragraph of prompt advice in L2. To route a new lesson:

1. Can it be technically enforced? → L0
2. Could the AI commit this mistake spontaneously, without a user instruction? → it must be an L1 rule (passive defense — never rely on a trigger)
3. High-frequency and high-risk? → L1. Mid-frequency and a keyword trigger suffices? → L2. One-off strategic insight? → L3
4. Is it a complete reusable workflow? → make it a skill of its own

---

## Scope

**Fits**: complex projects maintained by one person or a small team; the AI is the primary collaborator; a documented decision-record habit exists or is wanted.

**Does not fit**: calls you can make in three minutes (the framework costs more than the decision is worth — first ask "is this worth a roundtable?"); pure execution tasks; and **using the roundtable to dodge personal responsibility** — the vote cannot carry the decision for you; the confirmation is always yours.

**Hard constraints**: never make strategic decisions for the user; never ignore existing documents; never skip documentation; high-risk actions (publishing, deletion, anything outward-facing) always wait for explicit confirmation.
