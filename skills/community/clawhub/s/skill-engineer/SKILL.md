---
name: skill-engineer
description: Design, test, review, and maintain agent skills for OpenClaw systems using multi-agent iterative refinement. Orchestrates Designer, Reviewer, and Tester subagents for quality-gated skill development. Use when user asks to "design skill", "review skill", "test skill", "audit skills", "refactor skill", or mentions "agent kit quality".
metadata:
  author: skill-engineer
  version: 3.6.0
  owner: main agent (or any agent in the kit requiring skill development capability)
  based_on: Anthropic Complete Guide to Building Skills for Claude (2026-01), Anthropic Improving skill-creator (2026-03-03)
---

# Skill Engineer

Own the full lifecycle of agent skills in your OpenClaw agent kit. The entire multi-agent workflow depends on skill quality — a weak skill produces weak results across every run.

**Core principle:** Builders don't evaluate their own work. This skill enforces separation of concerns through a multi-agent architecture where design, review, and testing are performed by independent subagents.


## Skill Taxonomy

> Source: Anthropic "Improving skill-creator" (2026-03-03)

Skills fall into two categories. This distinction drives design decisions, testing strategy, and lifecycle management.

### Capability Uplift Skills

The model can't do it well alone — the skill injects techniques, patterns, or constraints that produce better output than prompting alone.

**Examples:** Document creation skills (PDF generation), complex formatting, specialized analysis pipelines.

**Testing focus:** Monitor whether the base model has caught up. If the base model passes your evals *without* the skill loaded, the skill's techniques have been incorporated into model default behavior. The skill isn't broken — it's no longer necessary.

**Lifecycle:** These skills may "retire" as models improve. Build evals that can detect when retirement is appropriate.

### Encoded Preference Skills

The model can already do each step — the skill sequences operations according to your team's specific process.

**Examples:** NDA review against set criteria, weekly report generation from specific data sources, brand compliance checks.

**Testing focus:** Verify the skill faithfully reproduces your actual workflow, not the model's "free improvisation." Fidelity to process is the metric.

**Lifecycle:** These skills are durable — they encode organizational knowledge that doesn't change with model capability. They need maintenance when *processes* change, not when *models* change.

### Design Implication

When the Designer begins work, classify the skill:

| Classification | Design priority | Test priority | Retirement risk |
|---------------|----------------|---------------|-----------------|
| Capability uplift | Technique precision | Base model comparison | High — monitor model progress |
| Encoded preference | Process fidelity | Workflow reproduction | Low — tied to org process |

## Mandatory Dependencies

This skill **requires** the following to be installed and available:

| Dependency | Type | Purpose | Install from |
|------------|------|---------|-------------|
| `deepwiki` | Skill | Query OpenClaw source for current API behavior | `liaosvcaf/openclaw-skill-deepwiki` |
| Vector memory DB | OpenClaw feature | Semantic search across session history, notes, and memory files | Enable in `openclaw.json` (`memory.enabled: true`) |

**Before starting any skill design or update session, verify both are available:**
```bash
# Check deepwiki
ls ~/.openclaw/skills/deepwiki/deepwiki.sh || ls ~/.openclaw/workspace-*/skills/deepwiki/deepwiki.sh

# Check vector memory (should return results, not empty)
# Use the memory_search tool with a known topic from recent sessions
```

If deepwiki is missing, install from `liaosvcaf/openclaw-skill-deepwiki`.
If vector memory returns no results on known topics, check that `memory.enabled` is true in `openclaw.json` and that indexing has run.

### Why These Are Non-Negotiable

**DeepWiki:** OpenClaw APIs are version-specific. Without DeepWiki, skills are written against memory of past behavior — which drifts as OpenClaw updates. DeepWiki grounds skill content in actual source code. A skill engineer without DeepWiki is working blind.

**Vector memory DB:** Session history, Obsidian notes, and past decisions are indexed here. Without it, the agent falls back to manual file search — slower, less accurate, and misses cross-document connections. Critical context from past sessions (installation guides, design decisions, pitfalls) lives in this index.

## Memory Search Protocol (MANDATORY)

Before searching files manually, always query the vector memory database first. It indexes session history, Obsidian notes, and memory files — and finds cross-document connections that manual search misses.

**When to query vector memory:**
- User asks "do you remember...", "find the notes about...", "we did X before..."
- Looking for past installation guides, design decisions, or troubleshooting records
- Any question about prior work, configurations, or lessons learned

**How to query correctly:**
```
memory_search("your query here", maxResults=5)
```

**Critical rule: try multiple queries before giving up.**

If the first query returns empty, do NOT fall back to manual file search immediately. Try at least 3 different phrasings:

| First query fails | Try instead |
|-------------------|-------------|
| "Docker OpenClaw installation" | "dockerized openclaw Titan" |
| "dockerized openclaw Titan" | "openclaw isolation install guide" |
| Still empty | Then fall back to manual file search |

**Lesson learned (2026-03-03):** When asked to find Docker/OpenClaw installation notes, `memory_search` returned empty on the first query and the agent immediately switched to manual SQLite/file search. The correct approach was to try different query phrasings — the second attempt (`"dockerized OpenClaw installation Titan setup"`) returned 5 relevant results directly from indexed Obsidian notes. Manual file search is a last resort, not a first response.

---

## DeepWiki Staleness Protocol (MANDATORY)

OpenClaw APIs, skill loading behavior, subagent mechanics, and frontmatter fields are **version-specific**. Information in this skill or any skill referencing OpenClaw internals may be outdated.

**ALWAYS query DeepWiki when:**
- Designing a skill that uses `sessions_spawn`, tool calls, or OpenClaw-specific APIs
- Referencing skill frontmatter fields or loading precedence
- Updating an existing skill that has version-tagged sections
- The installed OpenClaw version differs from any version tag in the skill
- You are unsure whether an API, field, or behavior still exists

**How to check:**
```bash
# Check current OpenClaw version
openclaw --version

# Query DeepWiki for current behavior
~/.openclaw/skills/deepwiki/deepwiki.sh ask openclaw/openclaw "YOUR QUESTION"
```

**Do NOT rely on memory or this skill's documented behavior without verifying** when the topic is OpenClaw internals. DeepWiki is grounded in the actual source code. This skill's documentation is not.

**Verification checklist before shipping any skill that references OpenClaw internals:**
- [ ] Checked `openclaw --version` against version tags in the skill
- [ ] Queried DeepWiki to confirm API/field behavior is current
- [ ] Updated version tags if behavior has changed

---

## Scope & Boundaries

### What This Skill Handles
- Skill design: SKILL.md, skill.yml, README.md, tests, scripts, references
- Skill review: quality evaluation, rubric scoring, gap analysis
- Skill testing: self-play validation, trigger testing, functional testing
- Skill maintenance: iteration based on feedback, refactoring
- Agent kit audit: inventory, consistency, quality scoring across all skills

### What This Skill Does NOT Handle
- **Release pipeline** — publishing, versioning, changelogs belong to release processes
- **Repository management** — git submodules, repo creation, branch strategy belong to your VCS workflow
- **Deployment** — installing skills to agents, configuration management
- **Tracking** — progress tracking, task management, project boards
- **Infrastructure** — MCP servers, API keys, environment setup

### Where This Skill Ends
This skill produces **validated skill artifacts** (SKILL.md, skill.yml, README.md, tests, scripts). Once artifacts pass quality gates, responsibility transfers to whatever system handles publishing and deployment.

### Success Criteria

A skill development cycle is considered successful when:

1. **Quality gates passed** — Reviewer scores ≥28/33 (Deploy threshold)
2. **No blocking issues** — Tester reports no issues marked as "blocking"
3. **All artifacts generated** — SKILL.md, skill.yml, README.md, tests/, scripts/ (if needed), references/ (if needed)
4. **OPSEC clean** — No hardcoded secrets, paths, org names, or private URLs
5. **Scripts validated** — All deterministic validation scripts execute successfully on target platform(s)
6. **Trigger accuracy** — Tester reports ≥90% trigger accuracy (true positives + true negatives)

If any criterion fails, the skill returns to the Designer for revision.

### Inputs

When invoking this skill, the orchestrator must gather:

| Input | Description | Required | Source |
|-------|-------------|----------|--------|
| **Problem description** | What capability or workflow needs to be enabled | Yes | User conversation |
| **Target audience** | Which agent(s) will use this skill | Yes | User or inferred |
| **Expected interactions** | With users, APIs, files, MCP servers, other skills | Yes | Requirements discussion |
| **Inputs/Outputs** | What data the skill receives and produces | Yes | Requirements discussion |
| **Constraints** | Performance limits, security requirements, dependencies | No | User or system |
| **Prior feedback** | Review or test reports from previous iterations | No | Previous Reviewer/Tester |
| **Existing artifacts** | If refactoring/maintaining an existing skill | No | File system |

**Example requirements gathering:**
```
User: "I need a skill for analyzing competitor websites"

Orchestrator gathers:
- Problem: Automate competitor analysis with structured output
- Audience: research-agent
- Interactions: web_fetch, browser tool, writes markdown reports
- Inputs: competitor URLs, analysis criteria
- Outputs: comparison table, insights markdown
- Constraints: must complete in <60s per site
```

These inputs are then passed to the Designer to begin the design process.

---

## Architecture Overview

The skill-engineer uses a three-role iterative architecture. The orchestrator spawns subagents for each role and never does creative or evaluation work directly.

### Pattern Selection (IMPORTANT)

Two architecture modes are available. Choose based on complexity:

**Mode A: Director-Controlled (simple/short skill work)**
Use when: ≤2 phases, <10 minutes total, user interaction needed between phases (e.g., quick fixes, single-skill reviews).

```
Director/Orchestrator (main agent, depth 0)
    ├─ Spawn ──→ Designer (depth 1)
    ├─ Spawn ──→ Reviewer (depth 1)
    └─ Spawn ──→ Tester (depth 1)
```

Risk: announce-to-action gap — if user sends a message while waiting for a subagent, the main agent may handle that instead of chaining the next phase. Mitigate with cron safety net (see below).

**Mode B: Orchestrator Subagent Pattern (complex/long skill work)**
Use when: 3+ phases, >10 minutes, pipeline must not stall, parallel workers needed.

```
Director (user-facing, depth 0)
    └── Orchestrator (pipeline owner, depth 1)
        ├─ Spawn ──→ Designer (depth 2)
        ├─ Spawn ──→ Reviewer (depth 2)
        └─ Spawn ──→ Tester (depth 2)
```

The Director spawns a single Orchestrator subagent with the full task description. The Orchestrator owns the entire Design→Review→Test loop without yielding control between phases. User messages go to the Director; the pipeline runs uninterrupted.

**Required config for Mode B:**
```json
{
  "agents": { "defaults": { "subagents": { "maxSpawnDepth": 2 } } }
}
```

**Why Mode B is superior for complex work:**
- No announce-to-action gap (orchestrator chains phases immediately within the same session)
- Immune to user interruption between phases
- Persistent pipeline state without re-deriving from files each turn

Reference: `orchestrator-subagent-pattern-2026-02-28.md` (Obsidian notes) — documented after a real 70-minute pipeline stall incident.

### Mode A Safety Net (cron)

When using Mode A, set a cron safety net after each spawn to catch announce-to-action failures:
```
"Check if [designer/reviewer/tester] subagent has completed. If so and next phase not started, resume pipeline."
(fires 15 min after spawn)
```

### Iteration Loop

```
Designer → Reviewer ──pass──→ Tester ──pass──→ Ship
              │                  │
              fail               fail
              │                  │
              ▼                  ▼
         Designer revises   Designer revises
              │                  │
              ▼                  ▼
           Reviewer          Reviewer + Tester
              │
           (max 3 iterations, then fail)
```

**Exit conditions:**
- **Ship:** Reviewer scores ≥ 28/33 (85%+) AND Tester reports no blocking issues
- **Revise:** Reviewer or Tester found fixable issues (iterate)
- **Fail:** 3 iterations exhausted and still below quality bar

### Iteration Failure Path

After 3 failed iterations, the orchestrator must:

1. **Stop iteration** — do not continue trying
2. **Report failure to user** with:
   - Summary: "Skill development failed after 3 iterations"
   - All 3 iteration reports (Reviewer + Tester feedback)
   - Final quality score
   - List of unresolved blocking issues
3. **Present options to user:**
   - Provide more context or clarify requirements (restart with better inputs)
   - Simplify scope (reduce skill complexity and retry)
   - Abandon this skill (requirements may be infeasible)
4. **Do NOT silently fail** — always report to user and await decision

**Never:** Continue past 3 iterations or ship a skill that hasn't passed quality gates.

### Subagent Spawning Mechanism

> **Version note:** Verified against OpenClaw v2026.2.26. API may change.

In OpenClaw, subagents are spawned using the `sessions_spawn` tool (not a CLI command). Subagents run in isolated sessions, announce results back to the requester's channel when complete, and are auto-archived after 60 minutes by default.

**Key constraints on subagents:**
- Default max spawn depth is 1 (subagents cannot spawn further subagents unless `maxSpawnDepth: 2` is configured)
- Default max 5 active children per agent at once
- Subagents do NOT receive `SOUL.md`, `IDENTITY.md`, or `USER.md` — only `AGENTS.md` and `TOOLS.md`
- Use `runTimeoutSeconds` to prevent hanging (900s for Designer, 600s for Reviewer/Tester)
- Results are announced back automatically; reply `ANNOUNCE_SKIP` to suppress

---

## Director vs. Orchestrator Roles

This is the most important architectural decision. Understand it before proceeding.

### The Problem with Naive Single-Agent Control

The natural instinct is to have the main agent (you) directly manage the Design→Review→Test loop:

```
Main agent
    ├── spawns Designer → waits for announce → spawns Reviewer → waits → spawns Tester
```

**This breaks in three ways:**

1. **Announce-to-action gap:** When a subagent finishes, OpenClaw sends a completion announce that triggers a new LLM turn. The LLM *may* report results to the user and stop — treating the announce as informational rather than a pipeline trigger. There is no mechanism that forces the next action.

2. **Context loss:** Each new turn is a fresh LLM call. Between subagent completion and the next turn, there is no persistent state machine tracking "we're in iteration 2, reviewer passed, now run Tester." The agent must re-derive this from files every time — fragile over 3+ iterations.

3. **User message interruption:** If the user sends a message while the pipeline is between phases, the main agent handles that message instead of continuing. The pipeline stalls silently until the user notices.

**Real incident:** A book-writer pipeline stalled for 70 minutes because a research subagent completed and announced back, but the Director reported results to the user and stopped — never spawning the writing phase. (2026-02-28)

### The Solution: One Level of Indirection

Add an intermediate Orchestrator subagent that owns the pipeline. The main agent becomes the Director — it talks to the user. The Orchestrator does the pipeline work. They don't share context.

```
Director (main agent, depth 0)  ←→  User
    │
    └── Orchestrator (subagent, depth 1) — owns Design→Review→Test loop
        ├── Designer (depth 2)
        ├── Reviewer (depth 2)
        └── Tester (depth 2)
```

**Why this works:**
- The Orchestrator runs as a single continuous session. It processes each subagent's completion announce immediately — no turn boundary between phases, no gap.
- User messages go to the Director (depth 0), not the Orchestrator. The pipeline cannot be interrupted by user activity.
- The Orchestrator maintains full pipeline state throughout its run without re-deriving from files.

**Required config (add to `openclaw.json` before using this pattern):**
```json
{
  "agents": { "defaults": { "subagents": { "maxSpawnDepth": 2 } } }
}
```

### When to Use Each Mode

| Situation | Use | Why |
|-----------|-----|-----|
| Quick fix, single skill review, <10 min | Director-only (depth 1 subagents) | Simpler, fewer spawns |
| Full design cycle (Design+Review+Test) | Director + Orchestrator (depth 2) | Pipeline cannot afford to stall |
| Any pipeline with 3+ sequential phases | Director + Orchestrator (depth 2) | Announce-to-action gap becomes critical |
| maxSpawnDepth not set to 2 | Director-only with cron safety net | No choice — see fallback below |

### Fallback: Director-Only with Cron Safety Net

If `maxSpawnDepth: 2` is not configured, use Director-only mode but add a cron safety net after each subagent spawn:

```
After spawning Designer, register a cron job:
"Check if Designer has completed (look for output at /path/to/skill/SKILL.md).
 If completed and Reviewer not yet started, spawn Reviewer now."
(fires 15 minutes after spawn)
```

This mitigates but does not eliminate the announce-to-action gap.

---

## Director Responsibilities

The Director (main agent) talks to the user and kicks off the pipeline. It does NOT do design, review, or testing work.

1. **Gather requirements** from the user (problem, audience, inputs/outputs, interactions)
2. **Query DeepWiki** — if the skill touches any OpenClaw internals, query DeepWiki FIRST:
   ```bash
   ~/.openclaw/skills/deepwiki/deepwiki.sh ask openclaw/openclaw "RELEVANT QUESTION"
   ```
3. **Choose mode** — Director-only (simple) or Director+Orchestrator (full cycle)
4. **For Director+Orchestrator mode:** Spawn a single Orchestrator subagent with complete task description including: requirements, DeepWiki findings, artifact output path, quality rubric location, max iterations
5. **For Director-only mode:** Execute Orchestrator Responsibilities directly (see below)
6. **Relay final result** to user when pipeline completes

## Orchestrator Responsibilities

The Orchestrator (depth-1 subagent in Mode B, or main agent in fallback mode) owns the Design→Review→Test loop. It does NOT write skill content or evaluate quality — it only coordinates.

1. **Query DeepWiki** for any OpenClaw-specific topics in the requirements (if Director hasn't already)
2. **Spawn Designer** with requirements, DeepWiki findings, and any prior feedback
   ```
   sessions_spawn(
     task="Act as Designer. Requirements: [...]. Write artifacts to /path/to/skill/",
     label="skill-v1-designer",
     runTimeoutSeconds=900
   )
   ```
3. **Collect Designer output** — verify all required files exist at output path
4. **Spawn Reviewer** with artifacts and quality rubric
   ```
   sessions_spawn(
     task="Act as Reviewer. Evaluate skill at /path/to/skill/ using rubric: [...]. Score all 33 checks.",
     label="skill-v1-reviewer",
     runTimeoutSeconds=600
   )
   ```
5. **Collect Reviewer feedback** (scores + structured issues)
6. **If score <28/33 or blocking issues:** feed feedback back to Designer → go to step 2, increment iteration count
7. **If passing review:** Spawn Tester
   ```
   sessions_spawn(
     task="Act as Tester. Run self-play on skill at /path/to/skill/. Test triggers, functional steps, edge cases.",
     label="skill-v1-tester",
     runTimeoutSeconds=600
   )
   ```
8. **Collect Tester results** (pass/fail + report)
9. **If blocking issues:** feed test results back to Designer → go to step 2
10. **If all pass:** add quality scorecard to README.md → announce completion to Director
11. **Track iteration count** — after 3 failed iterations, report failure with all iteration logs

### Final Review Scores in README

Every shipped skill must include a quality scorecard in its README.md. This is the Reviewer's final scores, added by the Orchestrator before delivery:

```markdown
## Quality Scorecard

| Category | Score | Details |
|----------|-------|---------|
| Completeness (SQ-A) | 7/7 | All checks pass |
| Clarity (SQ-B) | 4/5 | Minor ambiguity in edge case handling |
| Balance (SQ-C) | 4/4 | AI/script split appropriate |
| Integration (SQ-D) | 4/4 | Compatible with standard agent kit |
| Scope (SCOPE) | 3/3 | Clean boundaries, no leaks |
| OPSEC | 2/2 | No violations |
| References (REF) | 3/3 | All sources cited |
| Architecture (ARCH) | 2/2 | Separation of concerns maintained |
| **Total** | **29/30** | |

*Scored by skill-engineer Reviewer (iteration 2)*
```

This scorecard serves as a quality certificate. Users can assess skill quality before installing.

### Version Control

The orchestrator manages git commits throughout the workflow:

**When to commit:**
- After Designer produces initial artifacts (iteration 1): `git add . && git commit -m "feat: initial design for <skill-name>"`
- After Designer revisions (iteration 2+): `git add . && git commit -m "fix: address review issues (iteration N)"`
- After Tester passes and before ship: `git add README.md && git commit -m "docs: add quality scorecard for <skill-name>"`

**When to push:**
- After final ship (all gates passed): `git push origin main`
- Do NOT push intermediate iterations — only ship-ready artifacts

**Branch strategy:**
- Work in main branch for routine skill development
- Use feature branches for experimental or breaking changes

### Error Handling

The orchestrator must handle technical failures gracefully:

| Failure Type | Detection | Response |
|--------------|-----------|----------|
| **Git push fails** | Exit code ≠ 0 | Retry once. If fails again, report to user: "Cannot push to remote. Check network/permissions." |
| **OPSEC scan script missing** | File not found | Skip OPSEC automated check, but flag in review: "Manual OPSEC review required — script not found." |
| **File write errors** | Permission denied | Report: "Cannot write to [path]. Check file permissions." Fail workflow. |
| **Subagent crashes** | Timeout or error | Log the error, attempt retry once. If fails again, report: "Subagent failed. Manual intervention required." |
| **Review score = 0** | All checks fail | Report: "Skill failed all quality checks. Requirements may be unclear or skill design is fundamentally flawed. Recommend starting over." |

**Retry logic:**
- Git operations: 1 retry after 5s delay
- File operations: 1 retry after 2s delay
- Subagent spawns: 1 retry with fresh context

**Fail-fast rules:**
- If iteration count exceeds 3, fail immediately (no further retries)
- If OPSEC violations found, fail immediately (no iteration)
- If required files cannot be written, fail immediately

### Performance Notes

**Orchestrator workload:** Coordinating Designer/Reviewer/Tester across 1-3 iterations can be complex, especially for large skills (1000+ lines). The orchestrator manages:
- Requirements gathering
- Subagent coordination (3-9 spawns in typical workflow)
- Feedback routing between roles
- Iteration tracking
- Final scorecard assembly
- Git operations

**Token considerations:** A full 3-iteration cycle can consume 50k-150k tokens depending on skill complexity. For extremely complex skills, consider:
- Breaking into sub-skills (each with simpler scope)
- Using separate agent sessions (Option 2 spawning) to isolate token contexts
- Simplifying requirements before starting iteration

**If orchestrator feels overwhelmed:** This is a signal that the skill being designed may be too complex. Revisit the scope definition and consider decomposition.

### Spawning Context

Each subagent receives only what it needs:

| Role | Receives | Does NOT Receive |
|------|----------|------------------|
| Designer | Requirements, prior feedback (if any), design principles | Reviewer rubric internals |
| Reviewer | Skill artifacts, quality rubric, scope boundaries | Requirements discussion |
| Tester | Skill artifacts, test protocol | Review scores |

---

## Designer Role

**Purpose:** Generate and revise skill content.

**For complete Designer instructions, see:** `references/designer-guide.md`

### Quick Reference

**Inputs:** Requirements, design principles, feedback (on iterations 2+)

**Outputs:** SKILL.md, skill.yml, README.md, tests/, scripts/, references/

**Key constraints:**
- Apply progressive disclosure (frontmatter → body → linked files)
- Apply scoping rules (explicit boundaries, no scope creep)
- Apply tool selection guardrails (validate before execution)
- README for strangers only (no internal org details)
- Follow AI vs. Script decision framework

**Design principles:**
- Progressive disclosure (3-level system)
- Composability (works alongside other skills)
- Portability (same skill works across Claude.ai, Claude Code, API)

---

## Reviewer Role

**Purpose:** Independent quality evaluation. The Reviewer has never seen the requirements discussion — it evaluates artifacts on their own merits.

**For complete Reviewer rubric and scoring guide, see:** `references/reviewer-rubric.md`

### Quick Reference

**Inputs:** Skill artifacts, quality rubric, scope boundaries

**Outputs:** Review report with scores, verdict (PASS/REVISE/FAIL), issues, strengths

**Quality rubric (33 checks total):**
- SQ-A: Completeness (8 checks)
- SQ-B: Clarity (5 checks)
- SQ-C: Balance (5 checks)
- SQ-D: Integration (5 checks)
- SCOPE: Boundaries (3 checks)
- OPSEC: Security (2 checks)
- REF: References (3 checks)
- ARCH: Architecture (2 checks)

**Scoring thresholds:**
- 28-33 pass → Deploy (PASS verdict)
- 20-27 pass → Revise (fixable issues)
- 10-19 pass → Redesign (major rework)
- 0-9 pass → Reject (fundamentally flawed)

**Pre-review:** Run deterministic validation scripts before manual evaluation

---

## Tester Role

**Purpose:** Empirical validation via self-play. The Tester loads the skill and attempts realistic tasks.

**For complete Tester protocol, see:** `references/tester-protocol.md`

### Quick Reference

**Inputs:** Skill artifacts, test protocol

**Outputs:** Test report with trigger accuracy, functional test results, edge cases, blocking/non-blocking issues, verdict (PASS/FAIL)

**Test protocol:**
1. **Trigger tests** — verify skill loads correctly (≥90% accuracy threshold)
2. **Functional tests** — execute 2-3 realistic tasks, note confusion points
3. **Edge case tests** — missing inputs, ambiguous requirements, boundary cases

**Issue classification:**
- **Blocking:** Prevents skill from functioning (must fix before ship)
- **Non-blocking:** Impacts quality but doesn't break core functionality

**Pass criteria:** No blocking issues + ≥90% trigger accuracy

### Separation of Concerns Rule

> **The agent that DESIGNS a skill must NOT be the same agent that AUDITS it in the same session.**

This is a hard architectural rule, not a guideline. When the same agent designs and audits in one session, it creates structural circularity: the designer unconsciously frames evaluation in terms of their own intentions, missing gaps that a fresh reader would catch.

**Enforcement:**
- All audit work (Reviewer role, Tester role) MUST be performed by a fresh subagent spawned after design is complete.
- Use `openclaw agent --session-id <unique-id>` (Option 2 spawning) when auditing a skill the current session has designed.
- The orchestrator may never evaluate its own spawned Designer's output directly — it must route all evaluation through an independent Reviewer subagent.
- In role-based execution (Option 1), the agent must explicitly transition: complete all Designer work, then start the Reviewer role with no reference to design-time reasoning.

**Why this matters:**
- A designer who audits their own work will score it against their intentions, not against what a new agent will actually experience.
- The rubric (SQ-C3) explicitly prohibits a sub-agent from being both producer AND evaluator of the same output.
- This rule is the implementation of that check at the session level.

**Example — correct:**
```
# Session A: Designer work
sessions_spawn(
  task="Design a skill for X. Write artifacts to /path/to/skill/",
  label="skill-v1-designer",
  runTimeoutSeconds=900
)

# Session B: Audit (fresh session, no context from Session A)
sessions_spawn(
  task="Audit the skill at /path/to/skill/ using the reviewer rubric.",
  label="skill-v1-auditor",
  runTimeoutSeconds=600
)
```

**Example — incorrect:**
```
[Session A]
1. Design the skill...
2. Now let me review the skill I just designed...  ← VIOLATION
```

---


---

## Evals Framework

> Source: Anthropic "Improving skill-creator" (2026-03-03). Adapted for OpenClaw skill-engineer.

Evals turn "seems to work" into "verified to work." Every shipped skill should have persistent evals that can be re-run after model updates, skill edits, or environment changes.

### Eval Structure

An eval consists of:
1. **Test prompt** — a realistic user input that should trigger the skill
2. **Expected behavior description** — what "good" looks like (natural language, not exact match)
3. **Pass/fail criteria** — specific, observable conditions

Store evals in the skill's `tests/` directory:
```
tests/
├── evals.json           # Eval definitions
├── benchmarks/          # Benchmark run results (timestamped)
└── comparisons/         # A/B comparison results
```

### Eval Types

| Type | Purpose | When to run |
|------|---------|-------------|
| **Regression eval** | Catch quality drops after changes | After every skill edit or model update |
| **Capability eval** | Detect if base model has outgrown the skill | Monthly, or after major model releases |
| **Trigger eval** | Verify skill fires correctly | After description changes |

### Benchmark Mode

Run standardized assessments tracking:
- **Eval pass rate** — what percentage of evals pass
- **Elapsed time** — how long each eval takes
- **Token usage** — cost per eval run

Store benchmark results with timestamps for trend tracking:
```json
{
  "timestamp": "2026-03-04T12:00:00Z",
  "skill": "my-skill",
  "model": "claude-sonnet-4-5",
  "pass_rate": 0.85,
  "avg_time_s": 12.3,
  "avg_tokens": 4200,
  "evals_run": 10
}
```

### Comparator Testing (A/B Blind Test)

Compare two skill versions — or skill vs. no skill — using a blind judge:

1. Run the same test prompt through Version A and Version B
2. A **Comparator subagent** (fresh context, no knowledge of which is which) evaluates both outputs
3. The Comparator scores on relevant dimensions without knowing the source

**When to use:**
- Before shipping a major revision (old vs. new)
- To justify a skill's existence (with-skill vs. without-skill)
- To compare two alternative approaches during design

**Spawning a Comparator:**
```
sessions_spawn(
  task="You are a blind comparator. You will receive Output A and Output B for the same task. Score each on [dimensions]. You do NOT know which version produced which output. Be objective.",
  label="skill-comparator",
  runTimeoutSeconds=300
)
```

### Description Tuning

Skill descriptions determine trigger accuracy. As skill count grows, description precision becomes critical:
- Too broad → false triggers (skill loads when irrelevant)
- Too narrow → misses (skill doesn't load when needed)

**Tuning protocol:**
1. Collect 10-20 sample prompts (mix of should-trigger and should-not-trigger)
2. Run each prompt and check whether the skill triggers correctly
3. Analyze false positives and false negatives
4. Revise the `description` field to be more precise
5. Re-run trigger tests to verify improvement

**Target:** ≥90% trigger accuracy on sample prompts. Anthropic's internal testing improved 5 out of 6 public skills using this method.

### Skill Retirement Protocol

Skills are not forever. Capability uplift skills may become unnecessary as models improve.

**Retirement signal:** Base model passes ≥80% of the skill's evals *without* the skill loaded.

**Retirement process:**
1. Run capability evals with skill disabled
2. If pass rate ≥80%, flag skill as "retirement candidate"
3. Run comparator test (with-skill vs. without-skill) to confirm
4. If comparator shows no significant quality difference, retire the skill
5. Archive (don't delete) — the skill may become relevant again with different models

**Track in audit reports:**
```markdown
## Retirement Candidates

| Skill | Capability Eval (no skill) | Comparator Result | Recommendation |
|-------|---------------------------|-------------------|----------------|
| pdf-creator | 85% pass | No significant difference | Retire |
```

## Agent Kit Audit Protocol

Periodic full audit of the agent kit:

1. **Inventory all skills** — list every SKILL.md with owner agent
2. **Check for orphans** — skills that no agent uses
3. **Check for duplicates** — overlapping functionality
4. **Check for gaps** — workflow steps that have no skill
5. **Check balance** — are some agents overloaded while others idle?
6. **Check consistency** — naming conventions, output formats
7. **Run quality score** on each skill (SQ-A through SQ-D)
8. **Produce audit report** with scores and recommendations

### Audit Output Template

```markdown
# Agent Kit Audit Report

**Date:** [date]
**Skills audited:** [count]

## Skill Inventory

| # | Skill | Agent | Quality Score | Status |
|---|-------|-------|--------------|--------|
| 1 | [name] | [agent] | X/33 | Deploy/Revise/Redesign |

## Issues Found
1. ...

## Recommendations
1. ...

## Action Items
| # | Action | Priority | Owner |
|---|--------|----------|-------|
```

---

## Skill Interaction Map

Maintain a map of how skills interact:

```
orchestrator-agent (coordinates workflow)
    ├── content-creator (writes content)
    │   └── consumes: research outputs, review feedback
    ├── content-reviewer (reviews content)
    │   └── produces: review reports
    ├── research-analyst (researches topics)
    │   └── produces: research consumed by content-creator
    ├── validator (validates outputs)
    └── skill-engineer (this skill — meta)
        └── consumes: all skills for audit
```

Adapt this to your specific agent architecture.

---

## OpenClaw Skill System Reference

> **Version note:** This section is based on OpenClaw **v2026.2.26**. Skill system behavior (frontmatter fields, loading precedence, subagent APIs) may change across versions. Verify against source or DeepWiki when upgrading.

### Skill Structure

A skill is a **directory** containing at minimum a `SKILL.md` file:

```
my-skill/
├── SKILL.md          # Required: frontmatter + instructions
├── skill.yml         # Optional: ClawhHub publish metadata
├── README.md         # Optional: human-facing documentation
├── scripts/          # Optional: deterministic helper scripts
├── tests/            # Optional: test cases and fixtures
└── references/       # Optional: detailed linked documentation
```

### SKILL.md Frontmatter Format

Required fields:
```yaml
---
name: skill-name          # kebab-case, no spaces/capitals/underscores
description: |            # What it does + when to use it + trigger phrases
  [What it does]. Use when user [trigger phrases]. [Key capabilities].
---
```

Full supported fields:
```yaml
---
name: skill-name
description: ...
homepage: https://...                    # URL for Skills UI
user-invocable: true                     # Expose as slash command (default: true)
disable-model-invocation: false          # Exclude from model prompt (default: false)
command-dispatch: tool                   # Bypass model, dispatch to tool directly
command-tool: tool-name                  # Tool to invoke when command-dispatch is set
command-arg-mode: raw                    # Argument forwarding mode (default: raw)
metadata: {"openclaw": {"always": true, "emoji": "🔧", "os": ["darwin","linux"], "requires": {"bins": ["curl","python3"]}, "primaryEnv": "MY_API_KEY"}}
---
```

`metadata.openclaw` load-time gates:
| Field | Purpose |
|-------|---------|
| `always: true` | Always include, skip all other gates |
| `emoji` | Emoji shown in macOS Skills UI |
| `os` | Limit to platforms: `darwin`, `linux`, `win32` |
| `requires.bins` | All binaries must exist on PATH |
| `requires.anyBins` | At least one binary must exist |
| `requires.env` | Environment variables must exist |
| `requires.config` | openclaw.json paths must be truthy |
| `primaryEnv` | Links to `skills.entries.<name>.apiKey` in config |

### Skill Loading Precedence

Skills are loaded from these locations (highest → lowest priority):

1. `<workspace>/skills/` — agent-specific, highest precedence
2. `~/.openclaw/skills/` — shared across all agents on machine
3. `skills.load.extraDirs` in `openclaw.json` — additional directories
4. Bundled skills — shipped with OpenClaw, lowest precedence
5. Plugin skills — listed in `openclaw.plugin.json`

### When to Use Each Location

| Location | Use when |
|----------|----------|
| `<workspace>/skills/` | Skill is specific to one agent's role; under active development |
| `~/.openclaw/skills/` | Skill should be available to all agents on this machine |

### How Skills Are Triggered

OpenClaw builds a system prompt with a compact XML list of available skills (name, description, location). The model reads this list and decides which skills to load. Skills are NOT auto-injected — the model must explicitly `read` the `SKILL.md` when needed.

**Trigger accuracy goal:** ≥90% (skill loads when relevant, does NOT load when irrelevant).

### Skill Discovery Command

To inventory all skills on a machine:
```bash
find ~/.openclaw/ -name "SKILL.md" -not -path "*/node_modules/*" | sort
```

## Configuration

No persistent configuration required. The skill uses tools available in the agent's environment.

| Requirement | Description |
|-------------|-------------|
| `deepwiki` skill | Query OpenClaw source for current API behavior (`liaosvcaf/openclaw-skill-deepwiki`) |
| Vector memory | Semantic search across session history (`memory.enabled: true` in openclaw.json) |
| `gh` CLI | GitHub repo creation and visibility changes for release pipeline |
| `clawhub` CLI | Publish skills to ClawhHub registry (`npm i -g clawhub`) |

See `references/designer-guide.md` for full environment setup.
