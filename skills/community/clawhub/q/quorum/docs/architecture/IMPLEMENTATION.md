# Implementation Guide — Quorum

This guide walks through building Quorum from the architectural spec. It's structured as a reference walkthrough, not a copy-paste tutorial. The goal is understanding the patterns so you can adapt them to your stack.

> **Implementation Status (v0.7.3):** This guide describes the full target architecture. All 6 critics are shipped and callable: Correctness, Completeness, Security, Code Hygiene, Cross-Artifact Consistency, and Tester. Also shipped: the fixer (proposal mode), parallel execution, batch processing, and pre-screen integration. See `critic-status.yaml` for the authoritative status matrix. Sections below marked 🔜 describe components not yet built (Architecture, Delegation, Style).

---

## Prerequisites

- LLM provider with access to two capability tiers (e.g., Opus-class for judgment, Sonnet-class for execution)
- Tool execution environment (shell, web search, schema validation, git)
- File system access for artifact passing
- ~$0.20-0.50 budget per standard validation run

---

## Phase 1: Core Scaffold

### 1.1 File Structure

Set up the working directory Quorum uses per run:

```
runs/<run-id>/
├── run-manifest.json          ← Supervisor creates this first
├── artifact/                  ← What you're validating
│   └── target.yaml            (or .json, .md, .py, etc.)
├── rubric/
│   └── rubric.json            ← Which criteria to evaluate against
├── critics/
│   ├── correctness.json       ← Each critic writes here
│   ├── security.json
│   ├── completeness.json
│   ├── architecture.json
│   └── delegation.json
├── tester/
│   └── tester-results.json    ← Tester agent writes evidence here
├── fixer/
│   └── fixer-recommendations.json
├── aggregator/
│   └── synthesis.json
├── verdict.json               ← Final output
└── lessons-delta.json         ← New patterns to add to known_issues.json
```

Everything is files. No in-memory state between agents. This enforces determinism, parallelism, and auditability.

### 1.2 The Rubric Format

A rubric is a JSON document defining what "good" looks like:

```json
{
  "name": "Swarm Configuration Rubric",
  "version": "2.0",
  "domain": "multi-agent-systems",
  "criteria": [
    {
      "id": "CRIT-001",
      "criterion": "Every agent has explicit model assignment",
      "severity": "CRITICAL",
      "evidence_type": "tool",
      "evidence_instruction": "Run grep for 'model:' in each agent block. Show full output.",
      "rationale": "Without model assignment, defaults are unpredictable across providers"
    },
    {
      "id": "CRIT-002",
      "criterion": "Bidirectional contracts exist for all agent delegations",
      "severity": "CRITICAL",
      "evidence_type": "schema_parse",
      "evidence_instruction": "Parse delegation sections. Verify both delegator_commitments and delegatee_commitments fields.",
      "rationale": "Tomasev delegation principle: both sides must have explicit commitments"
    }
  ]
}
```

### 1.3 The Issue Format

Every critic must produce issues in this exact format:

```json
{
  "issue_id": "SEC-001",
  "critic": "security",
  "severity": "CRITICAL",
  "criterion_ref": "CRIT-005",
  "location": "agents[2].spawn_pattern",
  "description": "Agent spawns with shell variable interpolation — injection vector",
  "evidence": {
    "type": "grep",
    "output": "spawn: 'run.sh $USER_INPUT'",
    "tool_command": "grep -n 'spawn' config.yaml"
  },
  "recommendation": "Use file-based input passing instead of shell interpolation"
}
```

**If `evidence` is absent or unverifiable, the Aggregator rejects the issue.**

---

## Phase 2: The Nine Agents

### 2.1 Supervisor (Orchestrator)

The Supervisor runs first and last. Its system prompt covers:

**Intake responsibilities:**
- Validate the artifact exists and is parseable
- Load the rubric and confirm it's well-formed
- Assign criteria to critics based on domain expertise
- Write `run-manifest.json` with assignments and timeouts

**Verdict responsibilities:**
- Read `aggregator/synthesis.json`
- Assign PASS / PASS_WITH_NOTES / REVISE / REJECT
- Write `verdict.json` with full reasoning
- Extract lessons and write `lessons-delta.json`

**Key instruction in its system prompt:**
```
You do not write issues yourself. You orchestrate critics who write issues.
Your job is assignment, coordination, and synthesis — not evaluation.
```

### 2.2 The Critics

> ✅ **Shipped:** Correctness, Completeness, Security, Code Hygiene, Cross-Artifact Consistency, Tester
> 🔜 **Planned:** Architecture, Delegation & Coordination, Style

Each critic receives:
1. The relevant portion of the artifact (not the whole thing — reduce noise)
2. The criteria assigned to it
3. The required evidence format
4. The `known_issues.json` entries in its domain (primes pattern recognition)

**Correctness Critic:**
- Checks: factual accuracy, logical consistency, internal contradictions, claim support
- Tools: grep, regex matching, web search for fact verification
- Model tier: Sonnet (systematic, not judgment-heavy)

**Security Critic:**
- Checks: injection vectors, permission scope, credential exposure, trust boundaries
- Tools: grep patterns for known-bad constructs, schema parse for permission fields
- Model tier: Opus (adversarial thinking requires high capability)

**Completeness Critic:**
- Checks: coverage gaps, missing fields, unaddressed requirements, unstated assumptions
- Tools: grep for required fields, diff against rubric checklist
- Model tier: Sonnet

**Architecture Critic:** 🔜
- Checks: design coherence, pattern consistency, scalability, coupling/cohesion
- Tools: dependency analysis, pattern matching against known anti-patterns
- Model tier: Sonnet

**Delegation & Coordination Critic:** 🔜
- Checks: span of control, reversibility profile, bidirectional contracts, cognitive friction, dynamic re-delegation triggers
- Tools: schema parse of contract sections, grep for oversight mechanisms
- Model tier: Opus (requires Tomasev framework knowledge)

### 2.3 The Tester Agent ✅

The Tester doesn't evaluate — it verifies. For each issue raised by critics:

1. Find the claimed evidence location
2. Execute a tool to confirm it
3. Write `CONFIRMED` or `UNCONFIRMED` back to `tester-results.json`

The Aggregator uses tester results to filter ungrounded claims before synthesis.

### 2.4 The Fixer Agent (Optional)

Only activates for CRITICAL/HIGH issues in standard and thorough depth profiles:

```python
if depth in ['standard', 'thorough'] and issue.severity in ['CRITICAL', 'HIGH']:
    fixer.generate_fix(issue)
```

The Fixer writes concrete, applicable recommendations — not vague suggestions. "Replace `$USER_INPUT` with `--input-file /tmp/input.json`" not "avoid shell injection."

Max 2 fix loops. If the Fixer can't resolve an issue after 2 attempts, it escalates to REVISE verdict (human needs to decide).

### 2.5 The Aggregator

The hardest agent to get right. Its job:

1. **Deduplicate** — Multiple critics often find the same issue. Group by `(location, criterion_ref)` and keep the best evidence.
2. **Resolve conflicts** — If Correctness says PASS and Security says FAIL on the same criterion, escalate to Supervisor.
3. **Recalibrate confidence** — An issue confirmed by 3 critics is more confident than one from 1 critic.
4. **Filter ungrounded** — Any issue the Tester marked `UNCONFIRMED` gets downgraded one severity level or dropped.
5. **Synthesize** — Write `aggregator/synthesis.json` with the final merged issue list and overall confidence.

---

## Phase 3: The Learning System

> **Status:** Shipped in v0.5.3. The `known_issues.json` system tracks failure patterns across runs with frequency-based promotion to mandatory checks.

### 3.1 Extracting Lessons

After each run, the Supervisor extracts new patterns:

```python
for issue in verdict.critical_issues:
    if not matches_existing_pattern(issue, known_issues):
        delta.add({
            "pattern": extract_pattern(issue),
            "severity": issue.severity,
            "frequency": 1,
            "first_seen": today(),
            "source_run": run_id
        })
```

### 3.2 Pattern Promotion

```python
for pattern in known_issues:
    if pattern.frequency >= 10:
        pattern.mandatory = True          # Always check this
    if pattern.frequency >= 5:
        pattern.automation_candidate = True  # Design a tool for this
    if pattern.last_seen < 60_days_ago:
        pattern.stale = True              # Remove from mandatory list
```

### 3.3 Pre-Flight Integration

Before each run, the Supervisor loads mandatory patterns:

```python
mandatory = [p for p in known_issues if p.mandatory]
# Add these as explicit criteria to the current run
rubric.criteria.extend(mandatory_to_criteria(mandatory))
```

This is how past failures automatically improve future validation.

---

## Phase 4: Depth Profiles

### 4.1 Quick (5-10 min)

```yaml
critics: [correctness, completeness]
tester: disabled
fixer: disabled
aggregator: simplified (no conflict resolution)
fix_loops: 0
cost_ceiling: $0.20
```

Use for: iterative development, fast feedback loops, low-stakes work.

### 4.2 Standard (15-30 min)

```yaml
critics: [correctness, completeness, security + tester]
fixer: enabled for CRITICAL only
aggregator: full
fix_loops: 1
cost_ceiling: $0.50
```

Use for: most production work, configuration reviews, research validation.

### 4.3 Thorough (45-90 min)

```yaml
critics: [correctness, completeness, security, code_hygiene + tester]
fixer: enabled for CRITICAL + HIGH
aggregator: full + external validator
fix_loops: 2
human_checkpoints: before final verdict
cost_ceiling: $1.50
```

Use for: critical decisions, pre-launch reviews, irreversible actions.

**Note:** Cross-Artifact Consistency is a separate mode activated with the `--relationships` flag — it's additive at any depth, not part of the base critic panels above.

---

## Phase 5: Integration Patterns

### 5.1 CI/CD Integration

```yaml
# .github/workflows/validate.yaml
- name: Validate swarm config
  run: |
    quorum run \
      --target configs/swarm.yaml \
      --depth quick \
      --rubric swarm-config \
      --fail-on CRITICAL
```

### 5.2 Pre-Merge Review

```bash
# Before merging a new agent config
quorum run \
  --target pr-changes/new-agent.yaml \
  --depth standard \
  --rubric agent-config \
  --output pr-review.md
```

### 5.3 Research Synthesis Validation

```bash
# Validate a research report before publishing
quorum run \
  --target research/synthesis.md \
  --depth thorough \
  --rubric research-synthesis \
  --require-evidence web_search
```

---

## Common Pitfalls

### 1. In-Memory State Between Agents
**Wrong:** Passing issue lists as function arguments between critics  
**Right:** Each critic writes to its own file; Aggregator reads all files

### 2. Ungrounded Evidence
**Wrong:** "This looks like an injection risk" (no tool verification)  
**Right:** "grep found `spawn: '$INPUT'` at line 47 of config.yaml (tool output attached)"

### 3. Vague Rubric Criteria
**Wrong:** "The config should be complete"  
**Right:** "Every agent block must contain: name, model, tools, input_contract, output_contract (grep for each field)"

### 4. One-Size Depth
**Wrong:** Running thorough on every config change  
**Right:** Quick for dev iterations, Standard for PR review, Thorough for prod deployment

### 5. Ignoring Learning
**Wrong:** Never checking `known_issues.json`  
**Right:** Mandatory patterns load before every run; automation candidates trigger tool creation

---

## What to Build First

1. **File scaffold** (Phase 1) — Get the directory structure right
2. **Rubric format** (Phase 1) — Pick one domain, write 10 criteria
3. **Supervisor skeleton** (Phase 2) — Just intake + verdict; no critics yet
4. **One critic** (Phase 2) — Start with Correctness (simplest)
5. **Tester** (Phase 2) — Evidence verification loop
6. **Aggregator** (Phase 2) — Deduplication + verdict
7. **All 5 critics** (Phase 2) — Add one at a time
8. **Fixer** (Phase 2) — Only if you need it
9. **Learning system** (Phase 3) — After you have 5+ validation runs worth of data
10. **Depth profiles** (Phase 4) — Tune once the base system works

---

*Quorum is a pattern, not a product. Adapt freely. Contribute back what you learn.*


---

> ⚖️ **LICENSE** — Not part of the operational specification above.
> This file is part of [Quorum](https://github.com/SharedIntellect/quorum).
> Copyright 2026 SharedIntellect. MIT License.
> See [LICENSE](https://github.com/SharedIntellect/quorum/blob/main/LICENSE) for full terms.
