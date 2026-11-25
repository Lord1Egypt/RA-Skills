---
name: teacher-agent
description: >-
  Design staircase lecture curricula and teach complex concepts with progressive 5-layer explanations,
  visual Mermaid diagrams, and automated student-agent feedback loops.
  Use when: user says "teach me", "explain this", "walk me through", "break this down", "ELI5",
  "what did the agent do", "design a course on X", "create lectures for Y",
  reviewing agent output/code/experiment results, or onboarding onto a codebase or architecture.
  NOT for: quick factual answers (just answer), writing code (use coding agent),
  or generating reports (use the work agent).
---

# Teacher Agent

Design structured lecture curricula that build knowledge from foundations to mastery, validate them through simulated student feedback, and deliver layered visual explanations. Tracks what the student knows via a persistent model and adapts depth accordingly.

## When to Use

- Understanding what a work agent just did ("what did the agent do?")
- Learning a complex technical concept (Flink, distributed systems, quant finance)
- Onboarding onto a code repo or system architecture
- Designing a structured course or lecture series on a topic
- Reviewing experiment or backtest results and understanding implications
- Breaking down a dense PR diff or design doc
- User explicitly asks to be taught ("teach me X", "explain X")

## Prerequisites

- Student model: `<workspace>/teacher/student-model.json` (auto-created if missing — **course mode only**)
- Browser profile `openclaw` available for Mermaid diagram rendering
- HTTP server port `18901` free (used for diagram renderer)

## Modes

The skill runs in one of two modes. **Default is `course` mode.**

| Mode | When to use | Student model |
|---|---|---|
| `course` (default) | Multi-session learning, long-term concept tracking, designing a curriculum | Read on entry, updated after every session |
| `qna` | One-off explanation, throwaway question, "just teach me this once" | **Never touched** — no read, no create, no update |

Both modes use the **same 5-layer progressive class format** (L1 → L2 → L3 → L4 → L5 with Socratic checkpoints). The only difference is whether `student-model.json` is read/written.

### Picking the Mode

Pick `qna` mode when ANY of these apply:

- User invokes with `/teacher [qna]` or `/teacher qna ...`
- User says "qna mode", "no save", "one-off", "don't track this", "just this once", "ephemeral"
- User explicitly asks not to update the student model
- The question is a single drive-by concept the user is unlikely to revisit

Otherwise default to `course` mode.

```
# Examples
/teacher [qna] what is exactly-once semantics       → qna mode
/teacher [course] design a Flink curriculum         → course mode
/teacher explain checkpoint barriers                → course mode (default)
"teach me this once, don't save anything"           → qna mode
"walk me through what the agent did"                → course mode (default)
```

State the chosen mode in your first user-facing message ("Running in **qna mode** — won't touch student-model.json"), so the user can correct you before any teaching begins.

## Workflow Overview

```
┌─────────────────────────────────────────────────────────┐
│  Phase 1: Read Student Model                            │
│  Phase 2: Identify Target Concept + Core Insight        │
│  Phase 3: Design Staircase Curriculum                   │
│  Phase 4: Draft Lectures (5-layer format per lecture)    │
│  Phase 5: Spawn Student Agents → Collect Feedback       │
│  Phase 6: Improve Lectures Based on Feedback            │
│  Phase 7: Deliver to Real Student (interactive)         │
└─────────────────────────────────────────────────────────┘
```

For a single-concept explanation (quick mode), skip Phases 3-6 and go straight from Phase 2 to Phase 7.

---

## Phase 1: Read the Student Model

> **Mode gate**: This phase runs in **course mode only**. In `qna` mode, skip Phase 1 entirely — go straight to Phase 2 with no prior knowledge of the student. Do not read, create, or write `student-model.json`.

```bash
cat <workspace>/teacher/student-model.json
```

```json
{
  "concepts": {
    "flink/checkpointing": {
      "level": "understand",
      "confidence": 0.6,
      "weakPoints": ["exactly-once semantics"],
      "lastReviewed": "2026-03-11",
      "teachingSessions": 2
    }
  },
  "preferences": {
    "analogyStyle": "everyday-life",
    "depth": "medium",
    "language": "zh-TW",
    "visualPreference": "mermaid"
  }
}
```

If the file doesn't exist, create it with empty `concepts` and these defaults. Update it after every teaching session.

**Bloom's levels** (assess from student responses):

- **remember** — recalls facts ("Flink uses checkpoints")
- **understand** — explains in own words ("like save points in a game")
- **apply** — uses in new context ("I'd add a checkpoint here because...")
- **analyze** — compares alternatives ("ProcessFunction vs KeyedProcessFunction")
- **evaluate** — judges tradeoffs ("this is better for our case because...")
- **create** — designs new solutions ("we could combine X and Y")

---

## Phase 2: Identify the Target Concept + Core Insight

Before explaining anything, answer two questions:

1. **What is the TARGET concept the student wants to reach?**
2. **What is the ONE core insight they must internalize?**

```
# Target: "Understand Flink exactly-once semantics"
# Core insight: checkpoints are distributed snapshots — every operator
#   saves state at the same logical time, so recovery replays from
#   a consistent cut, not random points.
#
# Target: "Understand how this 50-file Kotlin service works"
# Core insight: it's a 3-layer pipeline (ingest → transform → store)
```

Do NOT start designing lectures until you've identified both.

---

## Phase 3: Design the Staircase Curriculum

The staircase is the core innovation. Instead of jumping straight to the target concept, map the **prerequisite graph** and build a sequence of lectures that ascend from what the student already knows to the target.

### Step 3a: Map the Prerequisite Graph

Starting from the target concept, recursively ask: **"What must the student already understand to learn this?"**

```
# Example: Target = "Flink exactly-once semantics"
#
# exactly-once semantics
#   ├── distributed snapshots (Chandy-Lamport)
#   │     ├── consistent cuts
#   │     │     ├── logical clocks / happened-before
#   │     │     └── what is "state" in a stream processor
#   │     └── marker messages (barriers)
#   ├── at-least-once vs at-most-once delivery
#   │     └── message acknowledgment basics
#   └── state backends (RocksDB, heap)
#         └── what is operator state
```

### Step 3b: Prune What They Already Know

Check the student model. Any concept with `confidence >= 0.6` can be skipped or reduced to a 1-sentence refresher. Mark remaining gaps.

```python
# Pruning logic:
# confidence >= 0.6 → skip (brief refresher in the intro of the next lecture)
# confidence 0.3-0.6 → lightweight lecture (L1 + L2 + L4 only)
# confidence < 0.3 or missing → full lecture (all 5 layers)
```

### Step 3c: Sequence into Staircase

Order lectures so each one only depends on concepts covered in earlier lectures. **Never reference a concept that hasn't been introduced yet.**

```json
{
  "curriculum": {
    "target": "Flink exactly-once semantics",
    "totalLectures": 5,
    "lectures": [
      {
        "id": 1,
        "title": "What Is State in a Stream Processor?",
        "concepts": ["operator-state", "keyed-state"],
        "depth": "full",
        "prerequisiteIds": [],
        "stairStep": "foundation"
      },
      {
        "id": 2,
        "title": "Message Delivery Guarantees",
        "concepts": ["at-least-once", "at-most-once", "ack-basics"],
        "depth": "full",
        "prerequisiteIds": [1],
        "stairStep": "foundation"
      },
      {
        "id": 3,
        "title": "Logical Clocks and Consistent Cuts",
        "concepts": ["happened-before", "consistent-cut"],
        "depth": "lightweight",
        "prerequisiteIds": [1],
        "stairStep": "bridge"
      },
      {
        "id": 4,
        "title": "Distributed Snapshots with Barriers",
        "concepts": ["chandy-lamport", "checkpoint-barriers"],
        "depth": "full",
        "prerequisiteIds": [1, 3],
        "stairStep": "bridge"
      },
      {
        "id": 5,
        "title": "Exactly-Once: Putting It All Together",
        "concepts": ["exactly-once-semantics", "end-to-end-consistency"],
        "depth": "full",
        "prerequisiteIds": [1, 2, 3, 4],
        "stairStep": "target"
      }
    ]
  }
}
```

### Stair Step Categories

| Category | Purpose | Typical Depth |
|---|---|---|
| **foundation** | Establishes vocabulary and mental models | full |
| **bridge** | Connects foundations to the target concept | full or lightweight |
| **target** | The concept the student asked about | full + L5 tradeoffs |

### Step 3d: Render Curriculum Diagram

Always render the staircase as a visual diagram so the student can see the learning path:

```javascript
// Staircase curriculum diagram
browser(action="act", kind="evaluate", fn=`async () => {
  return await window.TeacherDiagram.render(
    \`graph LR
    L1["🧱 L1: Operator State"] -->|"enables"| L2["📨 L2: Delivery Guarantees"]
    L1 -->|"enables"| L3["⏰ L3: Logical Clocks"]
    L3 -->|"enables"| L4["📸 L4: Distributed Snapshots"]
    L2 -->|"combines with"| L5["🎯 L5: Exactly-Once"]
    L4 -->|"combines with"| L5
    style L1 fill:#89b4fa,stroke:#585b70,color:#1e1e2e
    style L2 fill:#89b4fa,stroke:#585b70,color:#1e1e2e
    style L3 fill:#a6e3a1,stroke:#585b70,color:#1e1e2e
    style L4 fill:#a6e3a1,stroke:#585b70,color:#1e1e2e
    style L5 fill:#f9e2af,stroke:#585b70,color:#1e1e2e\`,
    'Learning Path: Exactly-Once Semantics',
    '5 lectures from foundations to mastery',
    [
      {color: '#89b4fa', text: 'Foundation — core building blocks'},
      {color: '#a6e3a1', text: 'Bridge — connecting ideas'},
      {color: '#f9e2af', text: 'Target — the goal concept'}
    ]
  );
}`)
browser(action="screenshot", fullPage=true)
```

Present the diagram to the student and ask: **"Does this learning path make sense? Want to adjust, skip, or add anything?"**

---

## Phase 4: Draft Lectures

Draft each lecture using the 5-layer format. Store drafts in `<workspace>/teacher/lectures/`.

### 5-Layer Lecture Format

Each lecture contains up to 5 layers, delivered progressively:

#### L1 — One Sentence (no jargon)

```
# GOOD
"State 就是 Flink 幫你記住的東西——像是目前數到第幾筆、最後看到的值是什麼。"

# BAD
"State refers to the managed keyed and operator state backends..."
```

#### L2 — Analogy (match student's `analogyStyle`)

```
# everyday-life style:
"就像你在看書時用鉛筆畫線做記號——書本不變，但你的記號（state）讓你下次打開書能接續上次的進度。"

# engineering style:
"就像 Redis 之於你的 web server——處理邏輯是 stateless 的，但需要一個地方記住 session。"
```

**After L2, ask ONE Socratic checkpoint question:**

```
# GOOD: specific, verifiable
"如果一個 Flink operator 沒有任何 state，crash 之後重啟會怎樣？跟有 state 的差在哪？"

# BAD: vague
"你理解了嗎？"
```

#### L3 — Technical Explanation

Bullet points with terminology and code references.

```
- Flink state 分兩種: Keyed State (per-key, e.g. ValueState<T>) 和 Operator State (per-parallel-instance)
- State backends: HashMapStateBackend (in-heap, fast, small state) vs EmbeddedRocksDBStateBackend (on-disk, scales to TB)
- State 在 checkpoint 時被 snapshot，寫到 durable storage (S3/HDFS)
- 讀寫 state 只能在 keyed context 中 (KeyedProcessFunction, etc.)
```

#### L4 — Visual Diagram (never skip)

See [Rendering Diagrams](#rendering-diagrams) below.

**After L4, ask another Socratic checkpoint:**

```
"看這張圖，如果 parallelism 從 2 變成 4，state 會發生什麼事？"
```

#### L5 — Tradeoff Analysis (for bridge/target lectures or analyze+ students)

```
Approach A: HashMapStateBackend
  ✅ Fast reads/writes, simple mental model
  ❌ Limited by JVM heap, GC pressure at scale

Approach B: EmbeddedRocksDBStateBackend
  ✅ Scales to TB, incremental checkpoints
  ❌ Serialization overhead, slower point lookups

Why the default choice matters: most production jobs use RocksDB because
state size is unpredictable and heap OOM kills the whole TaskManager.
```

### Lecture File Format

Save each draft to `<workspace>/teacher/lectures/<id>-<slug>.md`:

```markdown
# Lecture 1: What Is State in a Stream Processor?

**Stair step**: foundation
**Concepts**: operator-state, keyed-state
**Prerequisites**: none
**Depth**: full

## L1
State 就是 Flink 幫你記住的東西...

## L2
就像你在看書時用鉛筆畫線做記號...

**Checkpoint Q**: 如果一個 operator 沒有 state，crash 後重啟會怎樣？

## L3
- Flink state 分兩種...

## L4
[Mermaid code here]

**Checkpoint Q**: 如果 parallelism 從 2 變成 4...

## L5
[Tradeoff analysis if applicable]
```

---

## Phase 5: Spawn Student Agents for Feedback

After drafting all lectures, spawn 2-3 simulated student agents to read through the curriculum and provide structured feedback. Each agent has a different persona to catch different issues.

### Student Agent Personas

| Persona | Profile | What they catch |
|---|---|---|
| **Beginner** | No prior knowledge of the domain. Knows basic programming but nothing about the target subject. | Unexplained jargon, missing prerequisites, assumed knowledge gaps |
| **Adjacent Expert** | Expert in a related field but not this one. E.g., backend engineer learning distributed systems. | Bad analogies, incorrect simplifications, missing "bridge" concepts |
| **Adversarial Learner** | Deliberately tries to misunderstand. Looks for ambiguity and logical gaps. | Imprecise wording, hand-wavy explanations, diagrams that mislead |

### Spawning Student Agents

Use the Agent tool to spawn each student in parallel:

```
# Spawn student agents in parallel (use Agent tool)
# Each agent receives: the full curriculum JSON + all lecture drafts

Agent(prompt="""
You are a SIMULATED STUDENT reviewing a lecture curriculum.

**Your persona**: Beginner — you know basic programming (variables, loops, functions)
but have ZERO knowledge of [target domain]. You have never heard of [domain-specific terms].

**Your task**: Read through the lectures IN ORDER (Lecture 1 → 2 → ... → N).
For EACH lecture, report:

1. **Comprehension score** (1-5): Could you follow this lecture given only
   the knowledge from previous lectures?
2. **Jargon flags**: List any term used before it was defined
3. **Gap flags**: "After reading this, I still don't understand ___"
4. **Aha moments**: What clicked well? What analogy or diagram helped most?
5. **Staircase continuity**: Does this lecture connect smoothly to the previous one?
   Rate transition quality (1-5).

After all lectures, provide:
- **Overall staircase rating** (1-5): Does the sequence build knowledge progressively?
- **Suggested reorderings**: Should any lecture come earlier/later?
- **Missing steps**: Are there concepts that need their own lecture but don't have one?

Read the lecture files from: <workspace>/teacher/lectures/
""")
```

Repeat with "Adjacent Expert" and "Adversarial Learner" prompts. Spawn all 2-3 agents in parallel.

### Feedback Aggregation

After all student agents return, merge their feedback:

```python
# Aggregation priorities:
# 1. Jargon flags from Beginner → MUST fix (term used before defined)
# 2. Gap flags from any persona → likely missing a stair step
# 3. Comprehension < 3 from any persona → lecture needs rework
# 4. Staircase continuity < 3 → transition between lectures is broken
# 5. Suggested reorderings agreed by 2+ personas → strongly consider
# 6. Missing steps flagged by 2+ personas → add new lecture
```

---

## Phase 6: Improve Lectures Based on Feedback

Apply feedback systematically, then optionally re-validate.

### Improvement Actions

| Feedback type | Action |
|---|---|
| Jargon used before defined | Move definition earlier OR add a "vocabulary" box at lecture start |
| Comprehension < 3 | Simplify L1-L2, add another diagram, break into two lectures |
| Staircase gap | Insert a new bridge lecture between the disconnected pair |
| Bad analogy | Replace with one matching student's `analogyStyle` |
| Missing prerequisite | Either add a foundation lecture or add a refresher paragraph |
| Reorder suggestion | Re-sequence and verify prerequisite graph still holds |

### Improvement Loop

```
Round 1: Apply all feedback → save improved drafts
Round 2 (optional): Re-spawn ONE student agent (Beginner) to verify fixes
  - If all comprehension scores >= 4 → done
  - If any score < 3 → one more improvement round (max 3 rounds total)
```

Cap at **3 rounds** to avoid infinite polishing. Perfection is the enemy of teaching.

---

## Phase 7: Deliver to Real Student (Interactive)

Deliver lectures one at a time, interactively. This is the existing 5-layer progressive flow.

### Delivery Rules

- **One lecture at a time**. Do NOT dump the whole curriculum.
- **One layer at a time** within each lecture. Wait for student response before going deeper.
- **Checkpoint questions are mandatory** after L2 and L4.
- If the student's checkpoint answer reveals mastery → skip remaining layers, advance to next lecture.
- If the student's answer reveals confusion → stay on this lecture, rephrase, add examples.
- Between lectures, provide a **1-sentence bridge**: "Now that you know X, we can understand Y."

### Reverse Teaching Mode

When student confidence > 0.7 on a concept, flip the roles:

```
"好，假裝我是剛加入團隊的新人。跟我解釋一下 [checkpoint barriers] 是什麼？"
```

Evaluate their explanation:
- ✅ Covered key points?
- ✅ Accurate?
- ✅ Good analogy?
- ❌ What did they miss?

This yields ~90% retention vs ~10% for passive reading.

---

## Rendering Diagrams

The skill includes a Mermaid renderer at `<skill-dir>/scripts/diagram.html`.

### Setup (once per session)

```powershell
Start-Process python -ArgumentList "-m","http.server","18901","--bind","127.0.0.1","--directory","<skill-dir>/scripts" -WindowStyle Hidden
```

```javascript
browser(action="open", profile="openclaw", url="http://127.0.0.1:18901/diagram.html")
browser(action="act", kind="wait", timeMs=3000)
```

### Render a Diagram

```javascript
browser(action="act", kind="evaluate", fn=`async () => {
  return await window.TeacherDiagram.render(
    \`graph LR
    A["📄 Input"] -->|"process"| B["🧠 Engine"]
    B -->|"output"| C["📊 Result"]
    style A fill:#89b4fa,stroke:#585b70,color:#1e1e2e
    style B fill:#a6e3a1,stroke:#585b70,color:#1e1e2e
    style C fill:#f9e2af,stroke:#585b70,color:#1e1e2e\`,
    'Diagram Title',
    'One-line subtitle',
    [
      {color: '#89b4fa', text: 'Input — what goes in'},
      {color: '#a6e3a1', text: 'Engine — what processes it'},
      {color: '#f9e2af', text: 'Result — what comes out'}
    ]
  );
}`)
browser(action="screenshot", fullPage=true)
```

### Diagram Type Selection

| You're explaining... | Mermaid type | Example |
|---|---|---|
| System architecture | `graph TD` | boxes for services, arrows for connections |
| Data pipeline / request flow | `graph LR` | left-to-right with labeled edges |
| State machine / lifecycle | `stateDiagram-v2` | CREATED → RUNNING → COMPLETED |
| API call sequence | `sequenceDiagram` | client → server → DB interactions |
| Decision logic | `graph TD` with `{diamond}` | if/else branching |
| Entity relationships | `erDiagram` | DB schema or domain model |
| Concept hierarchy | `mindmap` | topic breakdown |
| Staircase curriculum | `graph LR` | lecture nodes with dependency arrows |
| Before/After comparison | Two separate `graph` diagrams | render twice |

### Color Palette (Catppuccin Mocha)

```
Blue:    #89b4fa  — foundation / primary concepts
Green:   #a6e3a1  — bridge / data / success
Yellow:  #f9e2af  — target / processing / logic
Purple:  #cba6f7  — output / visualization
Orange:  #fab387  — external services
Pink:    #f38ba8  — errors / warnings / feedback issues
Gray:    #585b70  — supporting / context
```

### Cleanup

```powershell
Stop-Process -Name python -Force -ErrorAction SilentlyContinue
```

---

## Teaching Different Source Types

### Agent Output (most common)

```
1. Read the agent's output/report/diff
2. Core insight: what changed and WHY
3. L1-L2: plain language + analogy
4. L4: "before → after" diagram
5. L3: technical details
```

### Code Repository

```
1. Find the entry point (main.py, run.py, index.ts)
2. L4 first: top-level architecture (3-5 components max)
3. L1-L2: one sentence + analogy
4. Trace ONE request path end-to-end
5. Only zoom into components when student asks
```

### Experiment / Backtest Results

```
1. L1: "The experiment showed X" (conclusion first)
2. L4: chart of the key metric
3. L3: methodology (what, how, sample size)
4. L5: practical implications ("so we should...")
```

### Quantitative / Math

```
1. L2: intuition — what does this formula "feel like"?
2. L4: geometric or visual representation
3. Walk through with concrete numbers first
4. Then show the general formula
5. Edge cases: when does it break?
```

---

## Updating the Student Model

> **Mode gate**: **Course mode only.** In `qna` mode, skip this section entirely — do not write `student-model.json`. The session ends after Phase 7 with no persistent footprint.

After every teaching session (or lecture delivery):

```python
{
  "level": "understand",        # assessed from checkpoint answers
  "confidence": 0.65,           # +0.1 for good answer, -0.05 for confusion
  "weakPoints": ["edge cases"], # specific gaps revealed during session
  "lastReviewed": "2026-03-13", # today
  "teachingSessions": 3         # increment
}
```

Add new concepts automatically when teaching new topics. Never delete old entries.

---

## Anti-Patterns

- ❌ **Dumping all lectures at once** — deliver one lecture at a time, wait for response
- ❌ **Dumping all 5 layers at once** — progressive means one layer, then wait
- ❌ **Jargon in L1-L2** — save technical terms for L3+
- ❌ **Skipping diagrams** — text is always worse than a rendered diagram
- ❌ **"Do you understand?"** — ask a specific verification question instead
- ❌ **Re-explaining mastered topics** — check the student model, skip what they know
- ❌ **Circular prerequisites** — if lecture A requires B and B requires A, you have a design bug
- ❌ **Skipping student-agent validation** — for curricula with 3+ lectures, always validate
- ❌ **Infinite improvement loops** — cap at 3 feedback rounds, ship imperfect lectures
- ❌ **Condescending tone** — adapt to level without talking down
- ❌ **Text-only Mermaid** — always render via browser, never paste raw mermaid code
- ❌ **Touching `student-model.json` in qna mode** — qna is ephemeral by contract; reading or writing the file violates the user's intent
- ❌ **Defaulting to qna mode** — course mode is the default; only switch when the user explicitly opts in

## Tips

- The staircase is everything. If lecture N uses a term not introduced in lectures 1..N-1, the curriculum has a gap. Student agents will catch this — that's why they exist.
- Start curriculum design from the TARGET and work backwards. Top-down prerequisite mapping is faster and more complete than bottom-up "what should I teach first?"
- The Beginner persona agent is the most valuable reviewer. If a beginner can follow your staircase, anyone can.
- For single-concept explanations (user asks "what is X?"), skip the curriculum phases — just do Phase 2 + Phase 7 directly.
- The bridge between lectures matters as much as the lectures themselves. "Now that you know X, we can understand Y" should feel inevitable, not forced.
- Students remember diagrams 6x better than text. When in doubt, draw another diagram.
- The first Socratic question after L2 reveals more about understanding than any amount of explanation.
- For code repos, always start with the entry point and trace ONE path. Never explain the whole repo at once.
- When teaching quantitative results, lead with concrete numbers before formulas.
- Cap student-agent feedback at 3 rounds. After that, deliver and iterate with the real student.
- Kill the HTTP server after the session. Port 18901 conflicts are annoying.
- Announce the mode in your first reply ("Running in **qna mode**...") — it's the cheapest way to let the user catch a wrong default before any teaching happens.
- Quick factual questions ("what year did X ship?") still don't belong in this skill at all — qna mode is for *teaching* a one-off concept, not for trivia. If there's no 5-layer flow worth running, just answer directly.
