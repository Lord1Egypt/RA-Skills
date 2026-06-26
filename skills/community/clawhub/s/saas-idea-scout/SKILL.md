---
name: saas-idea-scout
description: >
  Chat-driven SaaS idea discovery and validation pipeline. Generates 8 idea
  seeds conversationally, then fans out 24 sub-agents across 3 phases —
  discovery, critique, and evaluation — to produce scored, ranked PRDs with
  adversarial validation and contextual founder-aware ranking. Key features:
  parallel agentic swarm with self-healing, adversarial critique gauntlet,
  separation of concerns across research/critique/evaluation roles, cron
  watchdog for auto-recovery, and 10-dimension scoring with holistic
  founder-contextual judgment. Use for first-pass validation of product
  opportunities, stress-testing startup ideas, or surfacing promising
  directions before committing to deeper research.
metadata:
  openclaw:
    emoji: "🔭"
    os: ["linux"]
---

# SaaS Idea Scout

## What This Is

A chat-driven pipeline for discovering and stress-testing SaaS product ideas. You talk through your domain and constraints, the agent generates 8 idea seeds, then fans out 24 sub-agents across 3 phases — discovery, critique, and evaluation — to produce scored, ranked PRDs with adversarial validation.

**Key features:**
- **Adversarial critique gauntlet** — Every idea is championed by a research agent, attacked by a critic, and objectively scored by an evaluator, all independently.
- **Parallel agentic swarm** — 24 sub-agents run concurrently in batches of 4, completing a full pipeline in ~30-45 minutes of wall time.
- **Self-healing** — A cron watchdog monitors agent health and a retry escalation ladder recovers from failures automatically.
- **Separation of concerns** — Discovery, critique, and evaluation are handled by independent agents with distinct roles and instructions. No role confusion.
- **Contextual founder ranking** — Phase 5 applies founder-profile awareness to rank ideas by what matters for YOUR specific situation.
- **10-dimension scoring rubric** — Structured, transparent evaluation with dimensional scores and narrative synthesis.

- **5 phases:** Ideation → Discovery → Critique → Evaluation → Judgement
- **8 ideas → 24 sub-agents → contextually ranked top 3**
- **~30-45 minutes wall time**
- **No agent config. No `openclaw.json` changes.** Installs and runs through your chat session.

## When To Use

- "Find SaaS opportunities in [domain]"
- "Quick validation of business ideas in [industry]"
- "Surface promising product directions before deep research"
- "I have a problem space — what products could solve it?"
- "Stress-test these startup ideas"

## Prerequisites

None. Install and run. Works with any OpenClaw setup using the default model. For stronger results, use a capable model — a stronger model with higher thinking produces better research and deeper critiques.

## How It Works

```
Chat Agent (orchestrator + your conversation partner)
  │
  ├─ PHASE 1: IDEATION (conversational, ~5 min)
  │     └─ 4-5 questions → 8 idea seeds → you confirm
  │         └─ Creates .scoutrc on first run (model/thinking preference)
  │
  ├─ PHASE 2: DISCOVERY (8 sub-agents, 2 batches of 4, ~10 min)
  │     ├─ Each agent researches one idea, writes a PRD
  │     └─ Verification: file size + section header checks
  │
  ├─ PHASE 3: CRITIQUE (8 sub-agents, 2 batches of 4, ~8 min)
  │     ├─ Each agent reads one PRD, conducts adversarial research, writes critique
  │     └─ Verification: section header checks → orchestrator merges into dossiers
  │
  ├─ PHASE 4: EVALUATION (8 sub-agents, 2 batches of 4, ~8 min)
  │     ├─ Each agent reads PRD + critique, writes holistic evaluation with scores
  │     └─ Verification: section headers + integrity checks → orchestrator merges
  │
  └─ PHASE 5: JUDGEMENT (in-session, ~5 min)
        ├─ Read all 8 assembled dossiers (PRD + critique + evaluation per idea)
        └─ Contextual holistic ranking → top 3 with narrative justification
```

A cron watchdog spans all spawn phases (Discovery through Evaluation). It is created after Phase 1 and removed after Phase 4 completes. On every wake (completion event or watchdog), the orchestrator runs its verification procedure from its own context — it knows which phase and batch it's in.

---

## Pipeline Operations

### Batch-Verify Pattern

All spawn phases (2-4) follow the same pattern:

1. Send progress message for the batch
2. Spawn up to 4 sub-agents simultaneously (max 4 concurrent, no overlap)
3. `sessions_yield()` to wait for completion or watchdog wake
4. **On every wake**, verify expected output files exist using exec commands
5. If files are missing: identify which agents, re-spawn individually, yield again
6. Repeat until all files for the current batch exist
7. Send batch-complete progress, proceed to next batch

Never proceed to the next batch until ALL files from the current batch are verified.

### Yield and Watchdog Interaction

When the orchestrator yields, it wakes for either:
1. **Sub-agent completion events** — agents finished their work
2. **Cron watchdog fires** — the 7-minute interval elapsed

On EVERY wake (regardless of trigger), unconditionally verify output files. Never assume completion events are authoritative — they can be delayed or dropped.

If all expected files for the current batch exist → proceed.
If files are missing but agents are still running → yield again.
If files are missing and agents are done/stuck → intervene (see re-spawn escalation below).

### Verification Commands

Verification uses section-header grep and file size thresholds, following the pattern established in `saas-idea-discovery/instructions/verify_phase.sh`.

**After Phase 2 (Discovery) — verify all 8 PRDs:**
```bash
for f in <run_dir>/pool/0[1-8]_prd.md; do
  sz=$(stat -c%s "$f" 2>/dev/null || stat -f%z "$f")
  [ "$sz" -gt 2048 ] || { echo "FAIL: $(basename $f) too small ($sz bytes)"; continue; }
  grep -q "^### Problem" "$f" && grep -q "^### Rough Market Size" "$f" \
    && grep -q "^### Initial Score" "$f" \
    && echo "OK: $(basename $f)" \
    || echo "FAIL: $(basename $f) missing required sections"
done
```

**After Phase 3 (Critique) — verify all 8 critiques:**
```bash
for f in <run_dir>/pool/0[1-8]_critique.md; do
  sz=$(stat -c%s "$f" 2>/dev/null || stat -f%z "$f")
  [ "$sz" -gt 512 ] || { echo "FAIL: $(basename $f) too small ($sz bytes)"; continue; }
  grep -q "^### Market & Competitive Risks" "$f" \
    && grep -q "^### Blind Spots" "$f" \
    && echo "OK: $(basename $f)" \
    || echo "FAIL: $(basename $f) missing required sections"
done
```

**After Phase 3, assemble dossiers from PRDs + critiques:**
```bash
for i in 01 02 03 04 05 06 07 08; do
  cat "<run_dir>/pool/${i}_prd.md" \
      "<run_dir>/pool/${i}_critique.md" \
    > "<run_dir>/pool/${i}_dossier.md"
done
```

**After Phase 4 (Evaluation) — verify all 8 evaluations:**
```bash
for f in <run_dir>/pool/0[1-8]_evaluation.md; do
  sz=$(stat -c%s "$f" 2>/dev/null || stat -f%z "$f")
  [ "$sz" -gt 1024 ] || { echo "FAIL: $(basename $f) too small ($sz bytes)"; continue; }
  grep -q "^## Evaluation:" "$f" \
    && grep -q "^### Dimension Scores" "$f" \
    && grep -q "^### Total Score:" "$f" \
    && grep -q "^### Verdict:" "$f" \
    && echo "OK: $(basename $f)" \
    || echo "FAIL: $(basename $f) missing required sections"
done

# Integrity check: Total Score must be within 0-100
for f in <run_dir>/pool/0[1-8]_evaluation.md; do
  score=$(grep "^### Total Score:" "$f" | grep -oE '[0-9]+' | head -1)
  if [ -z "$score" ] || [ "$score" -lt 0 ] || [ "$score" -gt 100 ]; then
    echo "WARNING: $(basename $f) has invalid Total Score: $score"
  fi
done
```

**After Phase 4, assemble final dossiers (PRD + critique + evaluation):**
```bash
for i in 01 02 03 04 05 06 07 08; do
  cat "<run_dir>/pool/${i}_prd.md" \
      "<run_dir>/pool/${i}_critique.md" \
      "<run_dir>/pool/${i}_evaluation.md" \
    > "<run_dir>/pool/${i}_dossier.md"
done
```

**Dossier verification:**
```bash
for f in <run_dir>/pool/0[1-8]_dossier.md; do
  grep -q "^### Problem" "$f" \
    && grep -q "^### Market & Competitive Risks" "$f" \
    && grep -q "^## Evaluation:" "$f" \
    && echo "OK: $(basename $f)" \
    || echo "FAIL: $(basename $f) dossier incomplete"
done
```

### Progress Message Format

Batch boundary:
```
📝 Phase N: <phase name> — <brief status>
   Batch X/Y: <idea 1 slug>, <idea 2 slug>, <idea 3 slug>, <idea 4 slug>.
```

Phase transition:
```
✅ Phase N complete: N/N dossiers updated.
   [Idea 1]: XX/100, [Idea 2]: YY/100, ...
   Starting Phase N+1: <next phase name>.
```

### Re-Spawn Escalation

If a sub-agent fails to produce output, re-spawn with escalating urgency:

1. **First failure:** Re-spawn with normal task brief
2. **Second failure:** `"TWO ATTEMPTS FAILED. Produce even minimal output for <output_file_path>."`
3. **Third failure:** `"FINAL ATTEMPT. Your output must go to <output_file_path>."`
4. If all 3 re-spawns fail: mark the idea as incomplete, note it in Phase 5
   output, proceed with remaining ideas.

For multiple stuck agents (>10 min runtime, no output):
- If 3+ agents stuck simultaneously: skip steering, kill all and re-spawn
- If <3 agents stuck: try steering first, then kill + re-spawn if no improvement within 5 minutes

### SUCCESS/FAILURE Message Format

All sub-agents must end their final message with EXACTLY one of:

```
SUCCESS: <AGENT_TYPE> complete for <idea_name>. <1-line summary>
FAILURE: <AGENT_TYPE> failed for <idea_name>. <reason>
```

Agent types: `PRD`, `CRITIQUE`, `EVALUATION`. This standard format allows the
orchestrator to parse results reliably.

---

## Quick Start: Configure Model and Thinking

On first run, the agent will ask you to choose a model and thinking level for sub-agents. This preference is saved to `saas-scout-runs/.scoutrc` and reused on subsequent runs.

The agent will ask before Phase 1 ideation questions. A stronger model with higher thinking produces better results but increases cost and runtime.

To change your preference later, edit `saas-scout-runs/.scoutrc`:

```json
{
  "model": "deepseek/deepseek-v4-flash",
  "thinking": "low"
}
```

Before each run, read `saas-scout-runs/.scoutrc`. If the model and thinking level is configured this is what all subagents will use. If it is not configured, then configure it with the user's input.

---

## Phase 1: Ideation

This is conversational — you and the agent define the scope together.

If `.scoutrc` does not exist yet, the agent asks for model/thinking preference before the ideation questions below.

### What the Agent Asks

1. **"What domain or industry are we exploring?"**
   Be specific. "Healthcare compliance" is better than "healthcare." "Developer tools for API testing" is better than "dev tools."

2. **"Any constraints?"**
   Revenue targets, regulatory boundaries, technical preferences, geographic focus.
   Examples: "Bootstrappable, no hardware dependencies," "SMB only, under $50/user/month,"
   "Must work in EU with GDPR."

3. **"Who's the target customer?"**
   Specific segments. "Mid-market e-commerce brands with 10-50 employees" beats "businesses."

4. **"What's your founder profile?"**
   This matters for ranking. Options include:
   - Solo bootstrapper, technical (you can build)
   - Solo bootstrapper, non-technical (you need co-founders or no-code)
   - Small funded team (you have capital and GTM resources)
   - Domain expert (you know the problem deeply)
   - First-time founder (lower risk tolerance)

5. **"Any ideas already in mind, or should I generate everything?"**

### What You Get

Eight idea seeds, each 2-4 sentences: product name (slug), problem, solution angle, why now. Review them — swap, refine, or approve all.

Once confirmed, the pipeline starts. Create a run directory at a path like `saas-scout-runs/<YYYY-MM-DD>_<domain>/` and write a `context.md` file with the domain, constraints, customer segments, founder profile, and 8 seeds with their slug names.

---

## Phase 2: Discovery

**Batch rule for ALL spawn phases (2-4):** Verify ALL files from the current batch exist before spawning the next batch. Never overlap batches — max 4 sub-agents at any time.

### Spawn Template

Each discovery agent receives the following task brief. The orchestrator resolves absolute paths for `<skill_dir>`, `<run_dir>`, and the idea's slug name.

```
READ YOUR FULL INSTRUCTIONS AT: <skill_dir>/instructions/discovery.md
Follow that file exactly. This is your source of truth.

You are Discovery Agent for idea "<idea_slug>".

IDEA SEED: [seed text from Phase 1]

DOMAIN CONTEXT:
- Industry: [from Phase 1]
- Constraints: [from Phase 1]
- Target customers: [from Phase 1]
- Founder profile: [from Phase 1]

OUTPUT FILE: <run_dir>/pool/<NN>_prd.md
Write your complete PRD to this file. End the file with a blank line.
```

### Batch 1 (Agents 01-04)

Send a progress message before spawning:
```
📝 Starting Discovery Phase — 8 research agents producing PRDs.
   Batch 1/2: <idea 1>, <idea 2>, <idea 3>, <idea 4>.
```

Spawning all 4 agents at once:

```
sessions_spawn({ task: "<spawn template for #01>", mode: "run", timeoutSeconds: 600 })
sessions_spawn({ task: "<spawn template for #02>", mode: "run", timeoutSeconds: 600 })
sessions_spawn({ task: "<spawn template for #03>", mode: "run", timeoutSeconds: 600 })
sessions_spawn({ task: "<spawn template for #04>", mode: "run", timeoutSeconds: 600 })
```

`sessions_yield()`. On EVERY wake, verify files using commands from Pipeline Operations. If < 4 files: identify missing agent(s), re-spawn individually, yield again. Do NOT proceed to Batch 2 until all 4 files exist.

### Batch 2 (Agents 05-08)

Send batch progress:
```
📝 Discovery Batch 1/2 done (4/8 PRDs).
   Scores so far: [summarize from SUCCESS messages].
   Spawning Batch 2: <idea 5>, <idea 6>, <idea 7>, <idea 8>.
```

Spawn agents 05-08 with the same template, then yield and verify. Expect 8 PRDs.

Do NOT remove the cron watchdog. It stays active through all phases.

Phase-complete progress:
```
✅ Phase 2 complete: 8/8 PRDs written.
   <Idea 1>: XX/100, <Idea 2>: YY/100, ...
   Starting Phase 3: Critique.
```

---

## Phase 3: Critique

### Spawn Template

```
READ YOUR FULL INSTRUCTIONS AT: <skill_dir>/instructions/critic.md
Follow that file exactly. This is your source of truth.

You are Critic Agent for idea "<idea_slug>".

PRD FILE: <run_dir>/pool/<NN>_prd.md
Read this file first before writing.

DOMAIN CONTEXT:
- Industry: [from Phase 1]
- Constraints: [from Phase 1]

OUTPUT FILE: <run_dir>/pool/<NN>_critique.md
Write your complete critique to this file. End the file with a blank line.
```

### Batch 1 (Agents 01-04)

Send progress:
```
⚔️ Phase 3: Critique — Adversarial review of each PRD.
   Batch 1/2: <idea 1>, <idea 2>, <idea 3>, <idea 4>.
```

Spawn agents 01-04, yield, verify 4 critique files exist.

### Batch 2 (Agents 05-08)

Progress:
```
⚔️ Critique Batch 1/2 done (4/8 critiques).
   Spawning Batch 2: <idea 5>, <idea 6>, <idea 7>, <idea 8>.
```

Spawn agents 05-08, yield, verify 8 critique files exist.

When all 8 critiques are verified, assemble the first version of each dossier:

```bash
for i in 01 02 03 04 05 06 07 08; do
  cat "<run_dir>/pool/${i}_prd.md" \
      "<run_dir>/pool/${i}_critique.md" \
    > "<run_dir>/pool/${i}_dossier.md"
done
```

Phase-complete progress:
```
✅ Phase 3 complete: 8/8 critiques written.
   Major risks identified across all ideas. Dossiers assembled.
   Starting Phase 4: Evaluation.
```

---

## Phase 4: Evaluation

### Spawn Template

```
READ YOUR FULL INSTRUCTIONS AT: <skill_dir>/instructions/evaluator.md
Follow that file exactly. This is your source of truth.

You are Evaluator Agent for idea "<idea_slug>".

PRD FILE: <run_dir>/pool/<NN>_prd.md
CRITIQUE FILE: <run_dir>/pool/<NN>_critique.md
Read BOTH files before scoring.

DOMAIN CONTEXT:
- Industry: [from Phase 1]
- Constraints: [from Phase 1]
- Target customers: [from Phase 1]
- Founder profile: [from Phase 1]

OUTPUT FILE: <run_dir>/pool/<NN>_evaluation.md
Write your complete evaluation to this file. End the file with a blank line.
```

### Batch 1 (Agents 01-04)

Send progress:
```
📊 Phase 4: Evaluation — Scoring and synthesizing each idea.
   Batch 1/2: <idea 1>, <idea 2>, <idea 3>, <idea 4>.
```

Spawn agents 01-04, yield, verify 4 evaluation files exist.

### Batch 2 (Agents 05-08)

Progress:
```
📊 Evaluation Batch 1/2 done (4/8 evaluations).
   Spawning Batch 2: <idea 5>, <idea 6>, <idea 7>, <idea 8>.
```

Spawn agents 05-08, yield, verify 8 evaluation files exist.

**Remove the cron watchdog** (if not already removed):

```cron({ action: "remove", jobId: "<saved-job-id>" })```

**Assemble final dossiers:**
```bash
for i in 01 02 03 04 05 06 07 08; do
  cat "<run_dir>/pool/${i}_prd.md" \
      "<run_dir>/pool/${i}_critique.md" \
      "<run_dir>/pool/${i}_evaluation.md" \
    > "<run_dir>/pool/${i}_dossier.md"
done
```

Verify dossiers contain all three sections (see Pipeline Operations).

Phase-complete progress:
```
✅ Phase 4 complete: 8/8 evaluations scored.
   Scores: <Idea 1>: XX <verdict>, <Idea 2>: YY <verdict>, ...
   Cron watchdog removed. Dossiers assembled.
   Starting Phase 5: Judgement.
```

---

## Phase 5: Judgement

All in-session. No more spawns. This phase runs entirely as the chat agent.

### Step 1: Read All Dossiers

Read every dossier file to build a complete picture:
```
read path: <run_dir>/pool/01_dossier.md
read path: <run_dir>/pool/02_dossier.md
...through 08_dossier.md
```

Read efficiently — skim verdicts and scores first, then deep-read the top
3-4 candidates.

### Step 2: Holistic Ranking with Founder Context

Consider the user's founder profile from Phase 1:

- **Solo technical founder:** Weight MVP feasibility and founder fit more heavily.
  Can they build this alone? Does the problem affect them personally?
- **Solo non-technical:** Weight GTM viability and revenue model. Can they reach
  customers without building? Do they need a technical co-founder?
- **Funded team with GTM resources:** Weight market size and competitive positioning.
  Can they use capital to capture a large market before incumbents respond?
- **Domain expert:** Weight differentiation and white space. Does their expertise
  give them an unfair advantage in a specific niche?
- **First-time founder:** Weight MVP feasibility and risk. Is this achievable
  without prior founder experience?

Use the dimension scores as evidence, but apply your own judgment about which dimensions matter most for this specific founder and context.

### Step 3: Present Results

```
🏆 Top 3 SaaS Opportunities: [Domain]

Ranking weighted for: [founder profile with brief explanation]

🥇 #1: [Idea Name] — Raw Score: XX/100 [Verdict]

**What it is:** [2-3 sentence summary]
**Why it won:** [Which dimensions pushed it to the top under this founder's context]
**Key risk to watch:** [Top concern from the critique and evaluation]
**Revenue potential:** [Rough estimate]

🥈 #2: [Idea Name] — Raw Score: YY/100 [Verdict]
[2 sentence summary. Note why it's #2 vs #1.]

🥉 #3: [Idea Name] — Raw Score: ZZ/100 [Verdict]
[2 sentence summary. Key differentiator vs the rest.]

---

### The Rest (4-8)
| # | Idea | Score | Verdict | Why Not Top 3 |
|---|------|-------|---------|---------------|
| 4 | [Name] | XX | [Verdict] | Brief reason |
| 5 | [Name] | XX | [Verdict] | Brief reason |
| 6 | [Name] | XX | [Verdict] | Brief reason |
| 7 | [Name] | XX | [Verdict] | Brief reason |
| 8 | [Name] | XX | [Verdict] | Brief reason |

Full PRDs, critiques, and evaluations saved to: <run_dir>/pool/
```

---

## Cron Watchdog

A single cron watchdog spans all spawn phases (Discovery through Evaluation). It fires every 7 minutes into the orchestrator's session. The orchestrator already knows the pipeline state — the watchdog simply wakes it to check.

### Creating the Watchdog

After Phase 1 completes and the run directory is set up, create the watchdog using the cron tool:

```
cron({
  action: "add",
  job: {
    name: "scout-watchdog",
    schedule: { kind: "every", everyMs: 420000 },
    sessionTarget: "current",
    wakeMode: "now",
    payload: {
      kind: "agentTurn",
      message: "SCOUT WATCHDOG WAKE. Run directory: <run_dir>.\nCheck your sub-agents. Verify expected output files exist.\nRe-spawn any stuck/missing agents as needed."
    },
    delivery: { mode: "none" }
  }
})
```

Capture the returned `id` field. You need this for removal.

### How Yield and Watchdog Interact

When the orchestrator yields, it wakes for either:
1. Sub-agent completion events
2. Cron watchdog fires

On EVERY wake, run the standard verification procedure for the current phase and batch. If all expected files exist → proceed. If files are missing but agents are running → yield again. If files are missing and agents are done → intervene with the re-spawn escalation ladder.

### Removing the Watchdog

After Phase 4 completes and all 8 evaluations are verified, remove the watchdog:

```
cron({ action: "remove", jobId: "<saved-job-id>" })
```

Also remove the watchdog in edge cases (user wants to stop, pipeline aborted).

---

## Edge Cases & Recovery

| Scenario | What to Do |
|----------|-----------|
| Sub-agent fails to produce output | Check SUCCESS/FAILURE message. If no output file: re-spawn that single agent (max 3 attempts, escalating urgency). |
| Multiple agents stalled (>10 min runtime, no output) | If 3+: skip steer, kill all and re-spawn. If <3: try steer first, then kill + re-spawn if no improvement within 5 minutes. |
| Re-spawn fails after 3 attempts | Mark that idea as incomplete. Note the gap in Phase 5 output. Proceed with remaining ideas. |
| User wants to regenerate ideas | Ask: "Regenerate from same domain/constraints, or refine the scope first?" |
| All ideas receive WATCH or SKIP verdicts | Surface honestly: "All 8 ideas received WATCH/SKIP verdicts. This domain may need a different angle or broader scope." |
| Founder profile doesn't match categories | Ask clarifying questions. Use holistic judgment in Phase 5. |
| Watchdog creation fails | Proceed without it. Pipeline still functions on agent completion events. Notify user: "Watchdog setup failed, but the pipeline will continue." |
| Run directory collision | Append counter: `<timestamp>-<domain>-2/`, `-3/`, etc. |
| Tie in Phase 5 ranking | Explain the ambiguity, make a judgment call based on qualitative factors (stronger evidence, clearer GTM path, higher differentiation ceiling). |
| Gateway timeout on spawn | Wait 30 seconds, retry once. If still timing out: generate outputs in-session using the write tool. |
| User wants to stop mid-pipeline | Remove the cron watchdog: `cron({ action: "remove", jobId: "<saved-job-id>" })`. Present whatever output exists. |

---

## File Layout

After a full pipeline run, the run directory contains:

```
<run_dir>/context.md                          # Domain scope, constraints, seeds
<run_dir>/pool/
   01_prd.md         # Discovery agent output (PRD)
   01_critique.md    # Critic agent output
   01_evaluation.md  # Evaluator agent output
   01_dossier.md     # Orchestrator-assembled: PRD + critique + evaluation
   02_*.md ... 08_*.md  # Same pattern for all 8 ideas
```

`saas-scout-runs/.scoutrc` at the parent level stores model/thinking preference.
