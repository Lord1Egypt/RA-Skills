# Quorum — Architectural Specification

**Version:** 3.0  
**Last Updated:** March 2026  
**Status:** Documented and partially implemented — see §3 for implementation status per component  
**Platform:** Designed for [OpenClaw](https://openclaw.ai) agent systems. Cross-platform compatibility with other agent frameworks is under active exploration — see [MODEL_REQUIREMENTS.md](docs/getting-started/MODEL_REQUIREMENTS.md) for supported models and platforms.

---

## 1. Overview

Quorum is a quality assurance framework with a nine-agent target architecture. Currently, 6 critics are implemented (Correctness, Completeness, Security, Code Hygiene, Cross-Artifact Consistency†, and Tester), with 3 additional critics planned. †Cross-Consistency is activated with the `--relationships` flag. The framework is designed to rigorously evaluate multi-agent systems, configurations, research, code, and operational procedures against domain-specific rubrics. It combines:

- **Parallel specialized critics** (9 agents with distinct expertise)
- **Grounded evidence requirement** (every critique must cite tool-verified proof)
- **Intelligent delegation** (Tomasev et al., 2026 principles)
- **Learning memory** (persistent failure-pattern tracking; recurring patterns auto-promote to mandatory critic checks)
- **Cost-aware depth control** (three execution profiles for different budgets)

Quorum treats validation as infrastructure, not an afterthought.

---

## 2. Design Principles

### 2.1 Multi-Critic Architecture (Reflexion + Replacing Judges with Juries)

A single model reviewing a long prompt generates:
- Single point of failure (one model's blindspots)
- Hand-waving without evidence (LLMs can justify anything)
- ~~No learning across validations~~ → **Solved in v0.5.3:** Learning memory tracks recurring patterns and promotes high-frequency findings to mandatory checks

Quorum's target architecture has **nine specialized agents** — six critics are currently shipped, with three more planned:

**Shipped critics (6):**

1. **Correctness Critic** — Factual accuracy, logical consistency, claim support
2. **Completeness Critic** — Coverage gaps, missing requirements, unaddressed edge cases
3. **Security Critic** — Vulnerability patterns, permission issues, injection risks
4. **Code Hygiene Critic** — ISO 25010 maintainability, naming, complexity metrics
5. **Cross-Artifact Consistency Critic**† — Inter-file consistency (activated with `--relationships`)
6. **Tester Agent** — Finding verification: deterministic checks + LLM claim validation

**Shipped infrastructure agents:**

7. **Fixer Agent** — Proposes and applies fixes for CRITICAL/HIGH findings (optional, 1-2 loops max)
8. **Aggregator** — Merges findings, resolves conflicts, recalibrates confidence
9. **Supervisor** — Manages workflow, checkpoints, final verdict

**Planned critics (not yet built):**

10. **Architecture Critic** — Design coherence, pattern consistency, scalability concerns
11. **Delegation & Coordination Critic** — Span of control, reversibility, bidirectional contracts
12. **Style Critic** — Writing quality, tone consistency, formatting standards

Critics don't vote. The Aggregator synthesizes their findings into a final verdict with explicit confidence levels.

### 2.2 Grounded Evidence Requirement

Every issue **must** include tool-verified evidence:
- Excerpt from the artifact being reviewed
- Tool output (git log, schema parse, grep result, web search, shell execution)
- Citation to the rubric criterion it violates

The Aggregator **rejects ungrounded claims**. This single constraint is what separates useful critique from LLM hand-waving.

Example:
```json
{
  "issue": "Missing model assignment in worker agent",
  "severity": "CRITICAL",
  "evidence": {
    "tool": "grep",
    "result": "workers:\n  - name: researcher\n    // NO 'model' field",
    "citation": "Rubric § 2.4: Every agent must have explicit model assignment"
  }
}
```

### 2.3 Intelligent Delegation (Tomasev et al., 2026)

Quorum delegates to critics using five principles from "Towards an Intelligent Assessment Framework for Delegation in AI":

1. **Bidirectional Contracts** — Each critic receives explicit acceptance criteria and resource guarantees
2. **Five-Axis Monitoring Profiles** — Target (process/outcome) × Observability (direct/event) × Control (active/passive) × Frequency × Transparency
3. **Dynamic Re-Delegation** — If a critic fails, the Supervisor can downgrade to a cheaper model or escalate
4. **Trust as Runtime Primitive** — Critics earn trust through demonstrated competence; monitoring intensity scales with trust
5. **Reversibility-Aware Decisions** — Configuration changes (reversible) require less scrutiny than deployment decisions (irreversible)

### 2.4 Learning Memory

After each validation run, the system captures new failure patterns in `known_issues.json`:

```json
{
  "ML-001": {
    "pattern": "Missing bidirectional contract in spawned agent",
    "severity": "CRITICAL",
    "frequency": 12,
    "first_seen": "2026-01-15",
    "last_seen": "2026-02-18",
    "source_runs": ["run-001", "run-047", "run-089"],
    "meta_lesson": "Automation opportunity: validate-contracts.sh for mandatory pre-flight checks"
  }
}
```

High-frequency patterns automatically promote to mandatory checks in future runs.

### 2.5 Cost-Aware Depth Control

Three execution profiles balance rigor, speed, and cost:

| Depth | Critics | Fix Loops | Runtime | Use Case |
|-------|---------|-----------|---------|----------|
| **quick** | Correctness, Completeness | 0 | 5-10 min | Fast feedback; low stakes |
| **standard** | + Security | 0 | 15-30 min | Most work; default |
| **thorough** | All shipped critics | 1 (apply + re-verify) | 30-60 min | Critical decisions; production |

Pre-screen (10 built-in checks + optional DevSkim SAST, §3.1) runs before LLM critics at all depth levels. Fix loops are implemented (Phase 1.5): the Fixer proposes text replacements for CRITICAL/HIGH findings, applies them, and re-runs critics to verify resolution. Full 9-critic panels are the roadmap target for thorough depth.

### 2.6 Transparency Over Convenience

> *"In a judgment system, always trade toward transparency over convenience."*

This is a standing design axiom. When implementation choices arise — such as whether to pass a verdict or raw findings to the next stage, whether to surface intermediate outputs, or whether to collapse multi-locus findings into a summary — Quorum always chooses the option that preserves traceability and exposes reasoning.

Concrete consequences:
- **Phase 2 receives findings, not verdicts** from Phase 1. The Cross-Artifact critic sees what was discovered, not a collapsed judgment, so it can reason independently.
- **Pre-screen results are always written** to `prescreen.json`, even when all checks pass.
- **Run directories are immutable** — outputs are written once and never modified in place.
- **Aggregator decisions are logged** — every dedup and conflict resolution is recorded, not just the outcome.

---

## 3. Architecture

### 3.1 Pre-Screen Layer *(implemented)*

Before any LLM critic runs, Quorum executes a two-pass deterministic pre-screen against the target artifact.

**Pass 1: Built-in checks** — 10 rule-based regex/parse checks. No API costs, completes in milliseconds.

| Check ID | What It Catches |
|----------|----------------|
| PS-001 | Hardcoded absolute paths (portability risk) |
| PS-002 | Credential patterns (API keys, tokens, passwords) |
| PS-003 | PII patterns (email addresses, SSNs, phone numbers) |
| PS-004 | JSON syntax errors |
| PS-005 | YAML syntax errors |
| PS-006 | Python syntax errors |
| PS-007 | Broken internal links (file references that don't resolve) |
| PS-008 | TODO/FIXME/HACK markers |
| PS-009 | Trailing whitespace and mixed line endings |
| PS-010 | Empty file or effectively-empty file |

**Pass 2: DevSkim SAST** — When [DevSkim](https://github.com/microsoft/DevSkim) is installed, Quorum runs it as a second linter pass. DevSkim catches security patterns that regex checks miss (weak crypto, insecure defaults, known-vulnerable API usage). Results are merged into the same pre-screen evidence block. DevSkim is optional — if not installed, Pass 1 runs alone with no degradation.

Pre-screen results are written to `prescreen.json` in the run directory. If any check has severity `CRITICAL` or `HIGH`, the artifact may be rejected before LLM critics are invoked, depending on depth profile. Pre-screen findings are passed as context to Phase 1 critics.

### 3.2 The Agents: Implemented vs. Specified

```
Supervisor (Orchestrator)
├─ Correctness Critic (Tier 2)      [IMPLEMENTED]
├─ Completeness Critic (Tier 2)     [IMPLEMENTED]
├─ Security Critic (Tier 1)         [IMPLEMENTED] — grounded: OWASP ASVS 5.0, CWE Top 25, NIST SA-11; see docs/critics/SEC02_BUSINESS_LOGIC_VALIDATION.md for business logic workflow
├─ Code Hygiene Critic (Tier 2)     [IMPLEMENTED] — grounded: ISO 25010:2023, CISQ
├─ Cross-Artifact Consistency       [IMPLEMENTED] — Phase 2, separate from BaseCritic
├─ Architecture Critic (Tier 2)     [SPECIFIED, not yet built]
├─ Delegation Critic (Tier 1)       [SPECIFIED, not yet built]
├─ Style Critic (Tier 2)            [SPECIFIED, not yet built]
├─ Tester (Tier 2, tools: grep/web/exec) [IMPLEMENTED] — L1 deterministic + L2 LLM claim verification; see docs/critics/TESTER_CRITIC_BRIEF.md
├─ Fixer (Tier 1, optional)         [IMPLEMENTED — proposal mode + re-validation loops]
├─ Aggregator (Tier 1)              [IMPLEMENTED]
└─ Supervisor (Tier 1, final)       [IMPLEMENTED]
```

Model assignments reflect Tomasev delegation: judgment-heavy roles (Security, Aggregator, Supervisor) use your strongest model (Tier 1); execution-heavy roles use a capable but cost-efficient model (Tier 2). For example, Tier 1 might be Claude Opus or GPT-4, and Tier 2 might be Claude Sonnet or GPT-4o-mini.

### 3.3 Two-Phase Pipeline

```
quorum run --target file --relationships manifest.yaml
  │
  ├─ Pre-Screen (§3.1) → prescreen.json
  │
  ├─ Phase 1: Supervisor dispatches single-file critics (parallel)
  │   ├─ correctness
  │   ├─ completeness
  │   ├─ security (framework-grounded)
  │   └─ code_hygiene (framework-grounded)
  │
  ├─ Phase 2: Cross-Artifact Consistency (if --relationships provided)
  │   └─ Evaluates declared relationships between files
  │       Receives Phase 1 findings (NOT verdicts) as context
  │
  ├─ Aggregator → dedup, resolve conflicts, assign verdict
  │
  └─ Output: PASS / PASS_WITH_NOTES / REVISE / REJECT
```

**Phase coordination contract:** Phase 1 critics produce `Finding` objects with grounded evidence. The Aggregator does not run between phases. Phase 2 receives the raw Phase 1 findings as a serialized list — it can observe what was found, but no intermediate verdict has been assigned. This is required by Design Axiom §2.6: transparency over convenience.

### 3.4 Cross-Artifact Consistency *(Phase 2)*

When `--relationships` is provided, Quorum loads a YAML manifest declaring relationships between files and dispatches the Cross-Artifact Consistency critic.

**Manifest format:**
```yaml
version: "1.0"
relationships:
  - source: src/api_handler.py
    target: docs/api-spec.md
    type: implements
  - source: docs/api-spec.md
    target: src/api_handler.py
    type: documents
  - source: quorum/critics/security.py
    target: quorum/configs/standard.yaml
    type: delegates
  - source: data/output-schema.json
    target: src/pipeline.py
    type: schema_contract
```

**Relationship types:** `implements` | `documents` | `delegates` | `schema_contract`

**Locus model:** Cross-artifact findings use a `Locus` object with two anchor points:

```json
{
  "loci": [
    {
      "file": "src/api_handler.py",
      "role": "source",
      "excerpt": "def get_user(id): ...",
      "source_hash": "sha256:abc123"
    },
    {
      "file": "docs/api-spec.md",
      "role": "target",
      "excerpt": "GET /users/{id} — returns user object",
      "source_hash": "sha256:def456"
    }
  ],
  "relationship_type": "implements",
  "issue": "Handler returns 200 on missing user; spec declares 404",
  "severity": "HIGH"
}
```

`source_hash` pins each finding to the artifact version that was evaluated, enabling reproducibility audits.

**Path safety:** All paths in the manifest are resolved and boundary-checked against the project root. Traversal outside the declared boundary raises an error before evaluation begins.

### 3.5 The Workflow

1. **Intake** — Supervisor receives the artifact (config, research, code), target rubric, and optional relationships manifest
2. **Pre-Screen** — built-in checks + DevSkim SAST run (§3.1); results written to `prescreen.json`
3. **Phase 1 Dispatch** — Supervisor provides each critic with:
   - The artifact excerpt relevant to their domain
   - The rubric criteria they must evaluate
   - Required evidence format
   - Pre-screen results as context
4. **Phase 1 Parallel Execution** — Shipped critics run in parallel (see §3.2)
5. **Phase 2 Dispatch** (if `--relationships`) — Cross-Artifact critic receives:
   - Both artifacts for each declared relationship
   - Phase 1 findings (not verdicts) as context
6. **Aggregation** — Aggregator:
   - Deduplicates issues across all phases and critics
   - Resolves conflicts (if critics disagree, escalates to Supervisor)
   - Recalibrates confidence scores
7. **Verdict** — Supervisor assigns final verdict:
   - **PASS** — No issues or only LOW-severity findings
   - **PASS_WITH_NOTES** — Issues found, all addressable, recommendations provided
   - **REVISE** — HIGH/CRITICAL issues require rework; Supervisor provides guidance
   - **REJECT** — Unfixable architectural problems; restart required
8. **Learning** — System extracts and logs new failure patterns *(implemented in v0.5.3)*

### 3.6 File-Based Artifact Passing

All communication between agents uses file-based artifacts, not in-memory variables:

```
run-manifest.json                   ← Supervisor's execution plan
artifact.yaml                       ← What's being validated
rubric.json                         ← Validation criteria
prescreen.json                      ← Deterministic pre-screen results (PS-001–PS-010)
critics/
├── correctness-findings.json
├── completeness-findings.json
├── security-findings.json
├── code_hygiene-findings.json
└── cross_consistency-findings.json  ← Phase 2 (if --relationships used)
aggregator-synthesis.json           ← Merged findings
known_issues.json                   ← Learning memory (updated)
verdict.json                        ← Final result
report.md                           ← Human-readable summary
```

This enforces:
- Determinism (tool output is reproducible)
- Auditability (every change is logged to a file)
- Parallelism (critics don't block each other)
- Safety (no in-memory prompt injection vectors)

---

## 4. Rubric System

Rubrics define what "good" looks like for a specific artifact type. They're JSON documents with:

```json
{
  "name": "Swarm Configuration Rubric",
  "domain": "multi-agent-systems",
  "version": "2.0",
  "criteria": [
    {
      "id": "CRIT-001",
      "criterion": "Every agent has explicit model assignment",
      "severity": "CRITICAL",
      "evidence_required": "grep output showing 'model: ...' in CONFIG",
      "why": "Without model assignment, the system uses defaults unpredictably"
    },
    {
      "id": "CRIT-002",
      "criterion": "Bidirectional contracts exist for all delegations",
      "severity": "CRITICAL",
      "evidence_required": "Schema parse of contract section showing delegator+delegatee commitments",
      "why": "Tomasev delegation principle: both sides must be protected"
    },
    // ... more criteria
  ]
}
```

Rubrics are:
- **Domain-specific** (research synthesis ≠ code review ≠ config audit)
- **Composable** (build custom rubrics by mixing/extending standard ones)
- **Versionable** (rubrics evolve; track changes)
- **Machine-readable** (Supervisor validates rubric itself before use)

---

## 5. The Learning System

`known_issues.json` is Quorum's "experience memory." After each run:

```json
{
  "ML-001": {
    "pattern": "Missing I/O contracts in spawned agent",
    "severity": "CRITICAL",
    "source_papers": ["Tomasev et al. 2026 § 4.3"],
    "frequency": 12,
    "first_seen": "2026-01-15",
    "last_seen": "2026-02-18",
    "source_runs": ["run-001", "run-047"],
    "automation_opportunity": "Pre-flight tool: validate-contracts.sh checks all agent spawns"
  }
}
```

Rules:
- Patterns with frequency ≥ 10 become **mandatory checks** in future validation runs
- Patterns with frequency ≥ 5 trigger **automation opportunities** (design tools to check this deterministically)
- Patterns go stale after 60 days without recurrence (removed from mandatory list)

This learning architecture is implemented as of v0.5.3. See `quorum issues list|promote|reset` CLI commands and `--no-learning` flag.

---

## 6. Trust & Monitoring

Critics earn trust through demonstrated competence:

```
NEW (1st run)
  → PROBATIONARY (2-4 runs, 70%+ accuracy)
    → ESTABLISHED (5-9 runs, 85%+ accuracy)
      → TRUSTED (10+ runs, 95%+ accuracy)
```

Trust level modifies:
- **Monitoring intensity** — NEW critics get tighter scrutiny (more re-validation)
- **Approval thresholds** — TRUSTED critics can auto-approve LOW findings
- **Resource allocation** — ESTABLISHED/TRUSTED critics get higher token budgets

This follows Tomasev's "trust as runtime primitive" principle.

---

## 7. Cost Model

| Component | Cost | Amortization |
|-----------|------|--------------|
| Per-run setup (Supervisor intake) | $0.02 | 1 run |
| 6 shipped critics (parallel, max 30min; 9 at full build-out) | $0.15-0.45 | 1 run |
| Aggregator synthesis | $0.01 | 1 run |
| Tester tools (grep, git, web, exec) | $0.00 | amortized |
| Learning update (`known_issues.json`) | $0.00 | amortized |
| **Total per run (standard depth)** | **~$0.20-0.50** | **1 run** |

Additional runs on related artifacts reuse critic prompts and tools, amortizing costs further.

---

## 8. Implementation Checklist

Status as of v0.7.3 (reference implementation):

- [x] LLM provider — LiteLLM universal provider (100+ models, any tier combination)
- [x] File-based artifact passing (no in-memory state between agents)
- [x] Pre-screen layer — 10 built-in checks (PS-001–PS-010) + DevSkim SAST integration
- [x] 6 critics implemented — Correctness, Completeness, Security, Code Hygiene, Cross-Artifact Consistency† (`--relationships`), Tester (L1 + L2)
- [x] Rubric system (JSON schema + validator, 3 built-in rubrics: research-synthesis, agent-config, python-code)
- [x] Batch/multi-file validation with `BatchVerdict`
- [x] Aggregator synthesis logic (conflict resolution)
- [x] Verdict assignment logic (PASS/PASS_WITH_NOTES/REVISE/REJECT)
- [x] Depth preset system (quick/standard/thorough YAML configs)
- [x] Path traversal security (boundary enforcement)
- [x] Exit codes (0/1/2)
- [x] Parallel critic dispatch (ThreadPoolExecutor, max 6 critics; batch files max 3)
- [x] Fixer agent — proposal mode + re-validation loops (Phase 1.5; proposes and applies text replacements for CRITICAL/HIGH, then re-runs critics to verify)
- [x] Python code rubric (25 criteria, PC-001–PC-025, auto-detects on .py files)
- [x] Learning memory system (known_issues.json frequency tracking + mandatory check promotion — shipped in v0.5.3)
- [ ] Remaining 3 critics — Architecture, Delegation, Style
- [ ] Trust/monitoring system (per-critic accuracy tracking)

See IMPLEMENTATION.md for a reference walkthrough.

---

## 9. Theoretical Grounding

Quorum is built on these peer-reviewed papers:

| Paper | Contribution |
|-------|--------------|
| Shinn et al. (2023), Reflexion | Iterative self-critique, learning from failures |
| Verga et al. (2024), Replacing Judges with Juries | Multi-critic consensus, conflict resolution |
| Cai et al. (2024), LATM | Tool-making paradigm, deterministic execution |
| Wölflein et al. (2025), ToolMaker | Closed-loop tool generation, autonomous debugging |
| Tomasev et al. (2026), Intelligent AI Delegation | Bidirectional contracts, monitoring profiles, trust primitives |

---

## 10. Known Limitations & Roadmap

### Current Limitations (v3.0)

- Only **6 of 9 critics are implemented** (Architecture, Delegation, Style are specified but not built)
- Rubric panel is **static** (doesn't specialize per artifact type dynamically)
- **No critic-to-critic debate** (relies on Aggregator to resolve conflicts)
- Learning is **frequency-based** only (no semantic deduplication of patterns yet)
- **Confidence calibration** replaced by criteria coverage counts in v0.6.1
- **Trust/monitoring system** is not yet implemented

### Planned

- Remaining critics: Architecture, Delegation, Style
- ~~Re-validation loops~~ → **Shipped in v0.5.3**
- ~~Learning memory~~ → **Shipped in v0.5.3**
- Dynamic critic specialization (spawn domain-specific critics on-demand)
- Critic debate mode (when two critics conflict, run a structured debate)
- Semantic pattern deduplication (group similar issues under one ML pattern)
- Empirical confidence calibration (long-term tracking of verdict accuracy)
- Domain-specific rubric packs (compliance, security, infrastructure)

---

## 11. Getting Started

1. Read [IMPLEMENTATION.md](docs/architecture/IMPLEMENTATION.md) for a reference walkthrough
2. Review [examples/](examples/) for your use case
3. Adapt built-in rubrics or build custom ones (see [RUBRIC_BUILDING_GUIDE.md](docs/guides/RUBRIC_BUILDING_GUIDE.md))
4. Run the tutorial: `quorum run --target examples/sample-research.md --depth quick`

---

**Quorum is a production-oriented, early-stage validation framework.**  
*Architecture is sound and tested, with 6 critics shipped (all callable), learning memory, fix re-validation, batch processing, and the Tester verification layer all production-ready. Trust and monitoring systems are specified but not yet wired.*


---

> ⚖️ **LICENSE** — Not part of the operational specification above.
> This file is part of [Quorum](https://github.com/SharedIntellect/quorum).
> Copyright 2026 SharedIntellect. MIT License.
> See [LICENSE](https://github.com/SharedIntellect/quorum/blob/main/LICENSE) for full terms.
