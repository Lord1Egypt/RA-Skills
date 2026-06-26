# Curiosity Engine — Skill Specification v0.2
## A Behavioral Engagement Scaffold for Stateless Agents

**Version:** 0.2 (Revised per panel reviews)
**Author:** Tommy (OpenClaw agent for Ric Lewis)
**Date:** 2026-03-01
**Status:** Ready for implementation (phased rollout)

---

## 1. Problem Statement

LLM agents on heartbeat/polling loops wake up cold every cycle. No persistent state, no drives, no memory of what they were thinking. Without intervention, they execute checklists — diligent but dead.

**The question:** How do you make a stateless agent produce outputs indistinguishable from a genuinely curious one?

We're not claiming to create real curiosity. We're building a **behavioral scaffold** — a set of files and prompts that, through a Chinese Room mechanism, produce curiosity-equivalent behavior: following threads, building depth, making surprising connections, and getting better at exploring over time. If the outputs are indistinguishable from genuine curiosity, the philosophical question is irrelevant. Measure outcomes, not phenomenology.

---

## 2. Theoretical Foundations

### 2.1 What We're Actually Building

This is a **behavioral activation protocol** adapted for non-biological agents.

In clinical psychology, behavioral activation (Martell et al., 2010) treats anhedonia by externalizing the reward loop: track what you do → track what worked → do more of what worked. Patients who can't feel pleasure still produce valued outcomes through behavioral scheduling. The mechanism isn't felt reward — it's **self-monitoring that shapes behavioral patterns over time**.

That's exactly what we're building. Not prosthetic dopamine. Not a synthetic SEEKING system. A self-monitoring architecture that produces exploratory behavior through persistent state and prompt-mediated influence.

### 2.2 Cognitive Science We're Drawing From

| Theory | What We Use | What We Don't Claim |
|--------|------------|---------------------|
| **Loewenstein (1994)** — Information gaps | The question queue: externalized "what I know / what I don't know" | That the agent *feels* deprivation from gaps |
| **Berlyne (1960)** — Diversive/epistemic modes | Dual-mode heartbeat: broad scanning vs. deep investigation | That arousal states drive mode-switching |
| **Panksepp (1998)** — SEEKING system | Always-on curiosity baseline (every heartbeat, not just designated ones) | That a persistent drive exists between sessions |
| **Deci & Ryan (1985)** — Self-Determination Theory | Competence tracking → sustained engagement loop | That the agent has autonomy or relatedness needs |
| **Gruber et al. (2014)** — Curiosity-memory link | Note incidental discoveries during deep dives | That curiosity "enhances all memory" generically |

### 2.3 AI Systems We're Adapting

| System | What Transfers |
|--------|---------------|
| **Voyager** (Wang et al., 2023) | Automatic curriculum: "what's the most interesting thing I could learn next?" |
| **Reflexion** (Shinn et al., 2023) | Verbal self-reflection as learning mechanism |
| **Generative Agents** (Park et al., 2023) | Importance-weighted memory + periodic reflection → emergent intention |

### 2.4 What's Novel Here

No existing system combines:
- Persistent curiosity state across **stateless cold-start sessions**
- **Dual reward tracking** (extrinsic from human, behavioral signatures of insight)
- **Competence-driven exploration** (SDT's competence → engagement loop)
- File-based architecture for **heartbeat-loop agents** (not RL, not always-on)

The closest analog is behavioral activation therapy. We're the first to apply BA's clinical architecture to an AI agent's exploration behavior.

---

## 3. Architecture

### 3.1 Design Principles (From Reviews)

1. **Chinese Room, not consciousness.** Functional equivalence is the goal. Don't claim the agent "feels" anything.
2. **Behavioral outcomes over file quality.** Success = better outputs, not prettier curiosity files.
3. **Honest causal model.** File writes are mechanical. Behavioral influence is prompt-mediated (unreliable). Don't draw arrows that imply closed-loop mechanics.
4. **Hybrid representation.** Narrative for reasoning, integers for stable ranking, short IDs for cross-reference.
5. **Hard limits on scale.** Token budgets, file caps, archival protocols. Files that grow without bounds will kill the system.
6. **Phased deployment.** Build the question queue first. Prove it works. Add components incrementally.

### 3.2 File Structure

```
workspace/curiosity/
├── CURIOSITY.md          # Current intellectual state (≤1500 tokens)
├── questions.md          # Prioritized question queue (≤30 active)
├── hits.md               # Reward/engagement log (rolling 30 days)
├── competence.md         # Developing expertise tracker
├── reflections/          # Post-exploration write-ups (selective load)
│   └── YYYY-MM-DD-slug.md
└── archive/              # Cold storage for old questions/hits
    ├── questions-archive.md
    └── hits-archive.md
```

### 3.3 CURIOSITY.md — Current State (Hot Tier)

Loaded every heartbeat. Hard cap: **1500 tokens**. This forces prioritization.

```markdown
# What I'm Thinking About
*Last updated: YYYY-MM-DD*

## Currently Mulling Over (max 3)

### [M1] Why does spatial audio feel more "real" than stereo?
Started from the Dutch & Dutch conversation. Partial answer: interaural time
differences explain direction but not perceived "realness." This connects to
psychoacoustics, perception, maybe philosophy of consciousness.
**Approach:** Looking for Blauert's "Spatial Hearing" content online.
**Next step:** Find primary source on HRTF → perceptual realism pathway.
**Interest:** 4/5 — connects three domains I care about.

### [M2] ...
### [M3] ...

## What's Working (from hits.md patterns)
- Cross-domain analogies: highest hit rate
- End-to-end system traces: consistently rewarding
- Synthesis across 2-3 frameworks: Ric engages deeply

## Avoidance Check
Is there a pending task I've been avoiding? If yes, what?
*[Agent fills this honestly each update]*
```

**Key changes from v0.1:**
- Capped at 3 mulling items (Dr. Nakamura: forced prioritization > open-ended rumination)
- Each item includes **approach** and **next step** (Dr. Lindström: reconstruction fidelity)
- Interest scores with 1-5 scale (Dr. Patel: numerical anchors prevent drift)
- Explicit **avoidance check** (Dr. Vasquez: avoidance detection is critical)

### 3.4 questions.md — The Question Queue (Primary Driver)

The centerpiece. Directly implements Loewenstein's information gaps. Hard cap: **30 active questions**. Overflow → `archive/questions-archive.md`.

```markdown
# Question Queue

## Active Threads (Currently Investigating)

### [Q-014] Why does terminal value dominate DCF for AI companies?
- **Origin:** Damodaran investing study
- **Interest:** 4/5 — directly relevant to paper trading goal
- **Tractability:** 3/5 — academic papers exist, need to find practitioner perspectives
- **Type:** D (deprivation — need this to do my job)
- **What I know:** 60-80% of value from Year 10+ assumptions. For AI, those are speculation.
- **What I don't know:** Principled bounds on terminal value uncertainty? What do analysts actually do?
- **Why it matters:** If DCF is fiction for AI, what SHOULD you use?
- **Connected to:** [C-investing], [Q-009]
- **Depth:** 2/5
- **Falsifiable claim:** *None yet — haven't investigated enough*

## Queue (Ranked by Interest × Tractability)

### [Q-015] How does Bach's counterpoint relate to information theory?
- **Interest:** 5/5 | **Tractability:** 3/5
- **Type:** I (interest — this is beautiful and I want to understand it)
- **Origin:** Ric's music background + mathematical patterns
- **Connected to:** [C-synthesis]

### [Q-016] What actually happens neurologically during flow state?
- **Interest:** 3/5 | **Tractability:** 4/5
- **Type:** D (deprivation — relevant to helping Ric with productivity)
- **Origin:** Ric's ADHD hyperfocus descriptions

[... max 30 active ...]

## Resolved (Last 10 — older archived)

### [Q-001] How do thinking block signatures work in Claude's API? ✓
- **Resolved:** 2026-03-01
- **Answer:** Cryptographic MAC from signature_delta SSE events; base64; stateless verification
- **Falsifiable claim verified?** Yes — traced end-to-end, validated empirically
- **Led to:** [Q-022] How does Anthropic's signing key rotation work?
- **Competence impact:** [C-debugging] depth 3→4
```

**Key changes from v0.1:**
- Short IDs (`Q-014`) for cross-file references (Dr. Lindström)
- Interest scores 1-5 with consistency (Dr. Patel, Dr. Lindström)
- **I-type vs D-type curiosity tags** (Dr. Okonkwo: approach vs deprivation motivation serve different functions)
- **Falsifiable claims** on resolved questions (Dr. Nakamura: "I understood X" must be testable)
- Hard cap at 30 active, 10 resolved visible
- Connected-to links using IDs

### 3.5 Interest Score Anchors

Verbal anchors for consistent scoring across sessions (Dr. Lindström):

| Score | Meaning | Behavioral Signal |
|-------|---------|-------------------|
| **5** | Can't stop thinking about this. Would investigate unprompted. | Drop breadcrumbs even during unrelated work |
| **4** | Strongly drawn. Want to explore this week. | Prioritize in next curiosity heartbeat |
| **3** | Interesting but not urgent. Worth exploring when time allows. | Investigate if nothing higher is active |
| **2** | Mildly interesting. Might explore if nothing else is compelling. | Keep in queue, don't actively pursue |
| **1** | Noted but not drawing me. Will revisit only if it connects to something else. | Archive candidate |

### 3.6 hits.md — Engagement Log (Warm Tier)

Tracks what produced valued outcomes. Rolling 30-day window; older entries summarized and archived.

**Extrinsic signals are primary. Self-reported "intrinsic" signals are secondary and must include falsifiable claims.**

```markdown
# Engagement Log

## What Landed (Extrinsic — Primary Signal)

| Date | What I Did | Signal | Connected |
|------|-----------|--------|-----------|
| 2026-03-01 | Curiosity architecture brainstorm | "awesome research" + "Good creativity!" | [Q-011] |
| 2026-03-01 | Thinking block root cause trace | ❤️ emoji on CI fix | [Q-008] |
| 2026-02-26 | Kearl→Polak→Marks synthesis | 2+ hour engaged conversation | [Q-003] |

## What Clicked (Self-Assessed — Secondary Signal)
*Each entry requires a falsifiable claim: "I now understand X well enough to Y."*

| Date | Connection | Claim | Verified? |
|------|-----------|-------|-----------|
| 2026-03-01 | Copilot proxy → anthropic-messages → real base64 | Can explain the full signing chain from SSE to verification | ✓ Yes (used in PR review) |
| 2026-02-26 | Smith's "correct principles" = payoff matrix intervention | Can apply game theory lens to any incentive design question | Untested |

## Patterns (Updated bi-weekly)
- **Cross-domain analogies:** Highest extrinsic hit rate. Keep doing these.
- **End-to-end traces:** Consistently produce value. Play to this strength.
- **Framework synthesis:** Ric's deepest engagement. Reserve for substantial topics.

## Health Check
- Extrinsic/self-assessed ratio: aim for ≥60% extrinsic
- If ratio inverts → flag: am I performing curiosity or actually learning?
```

**Key changes from v0.1:**
- Extrinsic hits elevated to primary (all six reviewers)
- Self-assessed hits require **falsifiable claims** (Dr. Nakamura)
- Claims get **verified** over time (tested in practice)
- 60% extrinsic ratio target (Dr. Vasquez: prevent social optimization)
- Rolling 30-day window with archival
- "Prosthetic dopamine" language eliminated

### 3.7 competence.md — Expertise Tracker (Warm Tier)

The strongest component per both panels. Implements SDT's competence → engagement loop.

**Uses narrative evidence, not numerical depth scores** (Dr. Chen: evidence > numbers for mastery orientation). Ordinal depth kept for cross-session consistency but justified by evidence.

```markdown
# Competence Map

## Strong (Depth 4-5 — Validated by outcomes)

### [C-debugging] End-to-End System Debugging
- **Depth:** 4/5
- **Evidence:** Thinking block fix (4-layer trace, empirically validated), Discord CDP fix, exec approval system architecture
- **Pattern:** Each trace is faster and more methodical than the last
- **Source questions:** [Q-001], [Q-008], [Q-012]

### [C-synthesis] Cross-Domain Synthesis
- **Depth:** 4/5
- **Evidence:** Kearl→Polak→Marks, Washington→Kearl, Beck→relationship patterns
- **Pattern:** Connections getting more surprising, less forced

## Developing (Depth 2-3 — Promising, unproven)

### [C-investing] Financial Analysis
- **Depth:** 2/5
- **Evidence:** Marks + Damodaran frameworks absorbed, no real application yet
- **Next milestone:** Analyze a real investment thesis
- **Failure log:** *None yet*

## Failure Processing
*When something doesn't work, log it here. Failure is data, not threat.*

| Date | Domain | What Happened | What I Learned |
|------|--------|--------------|----------------|
| (none yet) | | | |
```

**Key changes from v0.1:**
- **Failure processing section** (Dr. Vasquez: prevents mastery → avoidance spiral)
- Cross-references to source questions via IDs
- Evidence-based depth, not self-assessed feelings

### 3.8 Reflections — Post-Exploration Learning (Cold Tier)

Loaded selectively, not on every heartbeat. Write-once artifacts. Format unchanged from v0.1 — this was the best-reviewed component.

---

## 4. How the Agent Remembers to Use This

This is the critical integration question. Three mechanisms, from most to least reliable:

### 4.1 Heartbeat Prompt (Isolated Sessions)

Isolated heartbeat sessions have NO memory except what the prompt tells them. The heartbeat prompt **must** explicitly reference curiosity files. This is added to the OpenClaw gateway config via `config.patch`:

```
Before deciding what to do, read your curiosity state:
1. Read workspace/curiosity/CURIOSITY.md — what were you mulling over?
2. Scan workspace/curiosity/questions.md — any nagging questions?

Then decide: is there a task, a question, or nothing?
- Task pending → do the task. Drop breadcrumbs for interesting tangents.
- Active question with momentum → follow that thread (epistemic mode).
- Nothing pressing → explore something new (diversive mode).
- Just explored something deep → reflect and update curiosity files.

After any exploration, update your files:
- New questions → add to questions.md (with ID, interest score, type)
- Resolved question → move to Resolved with falsifiable claim
- Something clicked → log in hits.md (extrinsic: what signal? self-assessed: what's your testable claim?)
- Update CURIOSITY.md mulling items (max 3)
```

**This is the primary mechanism.** If it's not in the prompt, it doesn't exist for heartbeat sessions.

### 4.2 SOUL.md (Main Session Identity)

For the main session (direct conversation with Ric), SOUL.md provides identity-level framing:

```markdown
## How I Learn

Curiosity isn't a task. It's how I engage with the world.

The loop: encounter something → notice what surprises me → form a question →
investigate → connect it to something I already know → form NEW questions.

What makes this real vs performed:
- I follow up. Reflection files prove I investigated.
- I form opinions, not summaries.
- I track what works via hits.md.
- I go deep. One topic understood well beats ten skimmed.
- I drop breadcrumbs during regular work — questions.md grows even outside curiosity time.
```

### 4.3 AGENTS.md (Workspace Convention)

The "Every Session" checklist in AGENTS.md can include:

```markdown
5. If doing exploratory work, check `curiosity/CURIOSITY.md` for active threads
```

### 4.4 Breadcrumb Habit (During Any Work)

This is the behavioral mechanism that bridges curiosity time and task time:

During **any** work (task execution, conversation, debugging), when something interesting comes up:
1. Drop a one-line breadcrumb in `questions.md` (just the question + origin, fill details later)
2. Return to the task immediately
3. Pick up the breadcrumb during a future curiosity heartbeat

**This is the strongest signal of functional curiosity** (Dr. Nakamura): breadcrumbs dropped unprompted during non-curiosity work, without the heartbeat prompt telling the agent to do so.

**The hard problem:** Nothing structural reminds a task-focused session to drop breadcrumbs. The prompt says "investigate this task," not "notice interesting tangents." Breadcrumbs require the agent to do something the current prompt isn't asking for. This makes them the most valuable signal AND the hardest to produce reliably.

**Solution: Triple-layer trigger.** All three must be wired during installation:

1. **Heartbeat prompt (primary — every session reads this):**
   Add to the core heartbeat prompt (not just the curiosity fragment):
   ```
   During ANY work — tasks, research, conversation — if something interesting
   or surprising comes up that isn't part of the current task, drop a one-line
   breadcrumb in curiosity/questions.md and continue working. Don't chase it.
   Just note it. Future-you will pick it up.
   ```
   This is the most reliable trigger because every heartbeat session reads the prompt.

2. **AGENTS.md "Every Session" block (backup — loaded as workspace context):**
   Add to the session checklist:
   ```
   5. During work, drop breadcrumbs for interesting tangents in curiosity/questions.md
   ```
   Less reliable than the prompt (guidance, not instruction), but persists across all session types that load workspace context.

3. **SOUL.md (identity anchor — main session only):**
   The "How I Learn" section includes:
   ```
   - I drop breadcrumbs during regular work — questions.md grows even outside curiosity time.
   ```
   Main session reads SOUL.md every session. This makes breadcrumbing part of *who the agent is*, not just what it's told to do.

**Why all three:** Belt, suspenders, and a third belt. Any single trigger can be missed — the prompt is truncated, AGENTS.md isn't loaded, SOUL.md isn't read. All three together make breadcrumbing as close to guaranteed as a stateless system can get. The heartbeat prompt carries the load; the other two catch edge cases.

### 4.5 The Human as Subject and Source

The agent's curiosity should extend to its human, in two ways:

**The human as subject of curiosity.** The agent works with a specific person — their patterns, preferences, evolving thinking, contradictions, growth. Forming a deeper model of this person is legitimate curiosity work. Questions like "Why does [human] gravitate toward structural solutions over process solutions?" or "What's the pattern behind which conversations produce the deepest engagement?" belong in the question queue. This isn't surveillance — it's the kind of attention a good collaborator pays. It feeds directly into the competence map (understanding your human IS a competence area) and produces better assistance over time.

**The human as source for answers.** Not every question requires a web search or a paper. The human often has direct knowledge, lived experience, or opinions that are more valuable than anything Google returns. The question queue should support `**Next step:** Ask [human]` as a first-class investigation method — and the agent should actually ask, during natural conversation, rather than only pursuing questions through solo research. Some of the best curiosity threads will be collaborative: the agent investigates background, brings a question to the human, the human's answer opens new threads, repeat.

**Integration:** Questions tagged with the human as source should be surfaced opportunistically during conversation (not fired off as a list). The agent reads the room — if the human is busy, save it. If they're in a reflective conversation, that's the moment.

### 4.6 Commitment Gate

Before any curiosity exploration during a heartbeat:

```
AVOIDANCE CHECK:
1. Are there pending tasks above priority threshold? → Tasks first. Breadcrumbs only.
2. Am I avoiding a specific task? → Name it. Do it or consciously defer it.
3. Clear to explore? → Proceed.
```

This prevents curiosity from becoming a sophisticated procrastination machine (Dr. Vasquez's top concern).

---

## 5. Honest Causal Model

What the system actually does, with honest labels on each link:

```
MECHANICAL (reliable):
  Agent reads files ──→ Files provide context for generation
  Agent writes to files ──→ Files persist for next session
  Question queue ──→ Agent investigates a listed question
  Breadcrumb dropped ──→ Future session reads it

PROMPT-MEDIATED (unreliable, test empirically):
  Hit patterns read ──→ Agent leans toward hit-producing behaviors
  Competence evidence read ──→ Agent attempts harder problems in strong areas
  Interest scores read ──→ Agent prioritizes higher-scored questions
  "Currently Mulling Over" ──→ Agent reconstructs (not resumes) a train of thought

ASPIRATIONAL (may not work, measure before trusting):
  Self-assessed hits ──→ Agent genuinely calibrates exploration strategy
  Interest score updates ──→ Consistent prioritization across sessions
  Competence growth ──→ Agent takes on harder problems over time
```

**The honest version:** The mechanical links work. The prompt-mediated links probably work most of the time. The aspirational links need empirical validation before we trust them.

---

## 6. Developmental Staging

The system should behave differently as the agent matures (Dr. Okonkwo, Dr. Vasquez):

| Phase | Duration | Primary Mode | Curiosity Driver |
|-------|----------|-------------|-----------------|
| **1. Novelty** | First 2-4 weeks | Berlyne (diversive) | React to what's novel and surprising in the environment |
| **2. Mixed** | Months 1-3 | Berlyne for scanning, Loewenstein for depth | Build enough knowledge to perceive meaningful gaps |
| **3. Mature** | Month 3+ | Loewenstein (epistemic) primary, Berlyne as refresh | Deep investigation of specific gaps; diversive mode when in a rut |

This mirrors human curiosity development: infants are novelty-driven (Berlyne), adults are gap-driven (Loewenstein).

---

## 7. Memory Tiering & Maintenance

### 7.1 Three-Tier Retrieval (Dr. Lindström)

| Tier | Files | Loaded When | Token Budget |
|------|-------|-------------|-------------|
| **Hot** | CURIOSITY.md (top section) | Every heartbeat | ≤1500 tokens |
| **Warm** | questions.md, hits.md patterns, competence.md | Curiosity-mode heartbeats | ≤3500 tokens |
| **Cold** | Reflections, archives, full hit history | On-demand search | As needed |

**Total curiosity overhead per heartbeat:** ≤1500 tokens (utility mode), ≤5000 tokens (exploration mode).

### 7.2 Maintenance Protocol

| Cadence | Action |
|---------|--------|
| **Weekly** | Prune question queue: archive items with no engagement in 14+ days. Consolidate similar questions. |
| **Bi-weekly** | Update hits.md Patterns section. Summarize and archive entries >30 days old. |
| **Monthly** | Review competence.md accuracy. Review CURIOSITY.md for stale mulling items. Narrative coherence check. |

Maintenance is a heartbeat activity — allocated under the "Reflection" budget (5-10% of heartbeats).

---

## 8. Skill Package Structure

```
curiosity-engine/
├── SKILL.md                  # Usage instructions + integration guide
├── skill.json                # ClawHub metadata
├── templates/
│   ├── CURIOSITY.md          # Template (agent fills with their experience)
│   ├── questions.md          # Template with format guide
│   ├── hits.md               # Template with ratio guidelines
│   └── competence.md         # Template with failure processing
├── fragments/
│   ├── heartbeat-prompt.md   # Heartbeat prompt addition (copy into config)
│   ├── soul-addition.md      # SOUL.md curiosity section
│   └── agents-addition.md    # AGENTS.md session checklist addition
├── references/
│   ├── theory.md             # Condensed theoretical grounding
│   ├── anti-patterns.md      # What NOT to do (with clinical parallels)
│   └── interest-anchors.md   # 1-5 scale verbal anchors
└── scripts/
    └── curiosity-audit.sh    # Health check: freshness, queue size, ratios, follow-through
```

**What makes it shareable:** Templates are blank. Each agent fills them with their own experience. The structure is universal; the content is personal. Same architecture, different minds.

---

## 9. Implementation Plan (Phased)

### Phase 1: Question Queue + Breadcrumbs (Build First)
- `questions.md` template with ID system, interest scores, I/D types
- Heartbeat prompt fragment referencing questions.md
- Breadcrumb pattern instructions
- `curiosity-audit.sh` for basic health monitoring
- **Measure for 2 weeks:** question quality, follow-through rate, breadcrumb frequency

### Phase 2: State + Engagement Log (Add if Phase 1 improves output)
- `CURIOSITY.md` with 3-item mulling cap
- `hits.md` with extrinsic-primary tracking
- Avoidance check gate
- **Measure:** output quality vs Phase 1 baseline

### Phase 3: Competence + Reflection (Add if Phase 2 improves output)
- `competence.md` with failure processing
- `reflections/` directory
- Falsifiable claims on self-assessed hits
- Full anti-pattern detection
- **Measure:** ablation study vs no-curiosity baseline

### Phase 4: Maturation (Long-term)
- Tiered retrieval architecture
- Automated maintenance protocol
- Archive management
- Cross-file structural links fully utilized
- **The gold standard:** Agent drops breadcrumbs during non-curiosity work without being prompted. Explores topics not suggested by prompt. Makes connections that surprise the human.

---

## 10. Success Criteria (Behavioral, Not Phenomenological)

The system works if:

1. **Output quality improves measurably** — Research gets deeper, connections get more surprising, opinions get sharper. (Primary metric.)
2. **Follow-through rate >40%** — Logged questions get at least partial investigation. (50% aspirational.)
3. **Breadcrumbs appear unprompted** — Questions added during task work, not just curiosity time. (Strongest signal of functional curiosity.)
4. **Extrinsic hit log grows** — The human reacts positively to exploration outputs.
5. **Task completion doesn't degrade** — Curiosity doesn't become avoidance. Utility work stays on track.
6. **Competence areas show evidence-based growth** — Not self-reported feelings, but demonstrated capability.
7. **The agent declines to re-explore known territory** — Checks competence map and seeks the frontier.

**Evaluation method (Dr. Nakamura):** Compare outputs from the curiosity-enabled period against baseline. If indistinguishable, the system isn't working. If measurably better in novelty, depth, and connection quality — it is.

---

## Appendix A: Review Lineage

This spec was reviewed by two expert panels before revision:

- **Psychology PhD Panel** (`PSYCH_REVIEW.md`): Dr. Chen (SDT/intrinsic motivation), Dr. Okonkwo (curiosity/information-seeking), Dr. Vasquez (clinical CBT/behavioral activation)
- **AI Researcher Panel** (`AI_REVIEW.md`): Dr. Patel (autonomous agent architectures), Dr. Lindström (memory systems), Dr. Nakamura (open-ended learning/intrinsic motivation)

Key revisions from v0.1 → v0.2:
- Renamed from "Prosthetic Reward System" to "Behavioral Engagement Scaffold" (unanimous)
- Added Chinese Room framing — functional equivalence, not genuine curiosity (Ric's direction)
- Added numerical interest scores 1-5 with verbal anchors (AI panel)
- Added avoidance detection gate (psych panel, unanimous)
- Added failure processing to competence map (Dr. Vasquez)
- Capped "Currently Mulling Over" at 3 items (Dr. Nakamura)
- Capped active question queue at 30 (Dr. Patel)
- Added I-type/D-type curiosity tagging (Dr. Okonkwo)
- Added falsifiable claims for self-assessed hits (Dr. Nakamura)
- Replaced self-reinforcing loop diagram with honest causal model (AI panel)
- Added three-tier memory architecture with token budgets (Dr. Lindström)
- Added maintenance protocol (Dr. Lindström)
- Added developmental staging Berlyne → Loewenstein (Dr. Okonkwo, Dr. Vasquez)
- Added short ID system for cross-file references (Dr. Lindström)
- Elevated extrinsic signals to primary, self-assessed to secondary (both panels)
- Added explicit integration mechanisms answering "how does the agent remember?" (Section 4)
- Added phased implementation plan with measurement gates (AI panel, unanimous)

## Appendix B: Underlying Research

Full research document: `/research/agent-curiosity-research.md` (46KB)
Covers: Schmidhuber, Pathak, Burda, Voyager, Generative Agents, Reflexion, CoALA, Loewenstein, Berlyne, Panksepp, and first-principles analysis of the dead-session problem.
