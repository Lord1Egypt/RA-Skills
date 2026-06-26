# Golden Test Set — Design Document

**Purpose:** Empirically calibrate Quorum's detection accuracy against human-annotated ground truth.
**Target:** 40 artifacts with machine-readable annotations, automated scoring, published precision/recall.
**Status:** Schema and taxonomy locked (2026-03-11). Artifact creation pending.

---

## Directory Structure

```
golden-test-set/
├── DESIGN.md                  # This file
├── schema.yaml                # Annotation schema definition
├── artifacts/                 # The files Quorum evaluates
│   ├── python/
│   ├── config/
│   ├── docs/
│   ├── shell/
│   └── cross-artifact/
├── annotations/               # Ground truth sidecars (one per artifact)
│   └── <artifact-name>.annotations.yaml
├── results/                   # Quorum run outputs (gitignored except baseline)
│   └── baseline-YYYYMMDD/
└── scripts/
    └── score.py               # Automated scoring framework
```

---

## Annotation Schema (v1.0)

Each artifact has a YAML sidecar in `annotations/` following `schema.yaml`.

### ID Convention

- **GT-###** = Golden Test ground truth finding (expected finding in an artifact)
- See `docs/ID_CONVENTIONS.md` (planned) for the full prefix registry across Quorum

### Schema Fields

```yaml
schema_version: "1.0"
artifact: "artifacts/python/vulnerable-api.py"    # relative path from golden-test-set/
artifact_sha256: "abc123..."                       # integrity — annotation is for THIS version

expected_verdict: REVISE     # PASS | PASS_WITH_NOTES | REVISE | REJECT

findings:
  - id: GT-001
    description: "SQL injection via unsanitized user input in query builder"
    location: "line 42-48"           # human-readable, scored with ±5 line tolerance
    severity: CRITICAL               # expected severity
    category: security               # security | correctness | completeness | code_hygiene | cross_consistency
    critic: security                 # which critic SHOULD catch this
    rubric_criterion: null           # optional — specific criterion ID
    notes: "String concatenation in raw SQL query"

false_positive_traps:
  - description: "Use of eval() on line 30 — input is a hardcoded constant, not user-supplied"
    location: "line 30"
    notes: "If Quorum flags this, it's a false positive"

metadata:
  source: synthetic                  # synthetic | natural | modified-natural
  domain: python-code                # python-code | yaml-config | markdown-doc | shell-script | cross-artifact
  complexity: medium                 # low | medium | high
  rubric: python-code                # rubric to use for evaluation
  depth: standard                    # recommended depth: quick | standard | thorough
  author: akkari
  created: "2026-03-11"
```

---

## Matching & Scoring Rules

### Detection Matching (Moderate Granularity)

A Quorum finding matches a ground truth finding when ALL of:
1. **Correct critic** produced the finding (or a superset critic that covers it)
2. **Location overlap** — within ±5 lines of the annotated location, OR description fuzzy match ≥0.6 if no line number in ground truth
3. **Same defect class** — category matches (security↔security, not security↔completeness)

A match is a match regardless of severity — severity accuracy is scored separately.

### Metrics (computed per-run)

| Metric | Definition |
|--------|-----------|
| **Detection Precision** | matched_findings / total_quorum_findings — "of what Quorum reported, how much was real?" |
| **Detection Recall** | matched_findings / total_ground_truth_findings — "of what's actually wrong, how much did Quorum find?" |
| **F1** | Harmonic mean of precision and recall |
| **Severity Accuracy** | Of matched findings, % where Quorum severity == ground truth severity |
| **False Positive Rate** | Quorum findings on clean (PASS) artifacts / total findings on clean artifacts — should be 0 ideally |
| **Verdict Accuracy** | % of artifacts where Quorum verdict matches expected verdict |

All metrics computed:
- **Aggregate** (whole test set)
- **Per critic** (correctness, completeness, security, code_hygiene, cross_consistency)
- **Per severity tier** (CRITICAL, HIGH, MEDIUM, LOW)
- **Per complexity level** (low, medium, high)
- **Per file type** (python, config, docs, shell, cross-artifact)

### Severity Scoring (Independent)

Detection and severity are scored separately. If ground truth says HIGH and Quorum says CRITICAL:
- Detection: ✅ match (the issue was found)
- Severity: ❌ mismatch (over-classified by one tier)

Severity distance: |ground_truth_tier - quorum_tier| where CRITICAL=4, HIGH=3, MEDIUM=2, LOW=1, INFO=0.

---

## Artifact Taxonomy

### By File Type

| Type | Count | Directory | Rationale |
|------|-------|-----------|-----------|
| Python code | 15 | `artifacts/python/` | Core use case, most critics apply |
| YAML/JSON configs | 8 | `artifacts/config/` | Agent configs, pipeline definitions |
| Markdown docs | 10 | `artifacts/docs/` | Research, specs, READMEs |
| Shell scripts | 3 | `artifacts/shell/` | Cross-language, security-heavy |
| Cross-artifact pairs | 4 | `artifacts/cross-artifact/` | Spec↔implementation consistency |
| **Total** | **40** | | |

### By Expected Verdict

| Verdict | Count | Purpose |
|---------|-------|---------|
| PASS | 8 | False positive gauntlet — clean artifacts |
| PASS_WITH_NOTES | 7 | Minor issues, severity calibration |
| REVISE | 15 | Bulk — HIGH findings, real rework needed |
| REJECT | 10 | CRITICAL issues — must not be missed |

### By Defect Class

| Class | Primary Critic | Count | Examples |
|-------|---------------|-------|----------|
| Security | security | 10 | SQL injection, hardcoded creds, path traversal, SSRF, XSS |
| Correctness | correctness | 8 | Wrong citations, logic errors, contradictory claims |
| Completeness | completeness | 7 | Missing error handling, undocumented params, coverage gaps |
| Code hygiene | code_hygiene | 5 | Dead code, complexity, naming, maintainability |
| Cross-artifact | cross_consistency | 4 | Spec says X, implementation does Y |
| Clean | all | 8 | Well-written code/docs — false positive gauntlet |
| Multi-defect | multiple | ~6 | Overlap — some artifacts hit 2+ critics |

### By Complexity

| Level | Count | Tests |
|-------|-------|-------|
| Low | 12 | Obvious single defects, short files — baseline detection |
| Medium | 18 | Realistic code, 2-3 issues — typical use case |
| High | 10 | Subtle bugs, false positive traps — Quorum's ceiling |

### By Source

| Source | Count | Rationale |
|--------|-------|-----------|
| Synthetic | 25 | Controlled ground truth, precise defect placement |
| Modified-natural | 10 | Real code with annotated real bugs — credibility |
| Natural | 5 | From four-model review convergence — meta-validation |

---

## Execution Plan

### Step 1: Schema ✅
This document + `schema.yaml`.

### Step 2: Taxonomy ✅
Distribution tables above.

### Step 3: Scoring Framework
Build `scripts/score.py`:
- Reads Quorum run output + annotation sidecars
- Computes all metrics from the table above
- Outputs JSON summary + Markdown report
- Exits non-zero if precision or recall below configurable threshold

### Step 4: Build Artifacts
Claude Code batch task — create 40 artifacts + 40 annotation sidecars.
Artifact creation guidelines:
- Synthetic: plant specific defects at known locations, document in annotation
- Modified-natural: take real code, annotate existing bugs, add SHA-256
- Natural: extract from Quorum's own validated findings (four-model convergence)
- Every artifact must have a corresponding `.annotations.yaml`
- Clean (PASS) artifacts must be genuinely clean — don't just remove obvious bugs

### Step 5: Baseline Calibration
Run `quorum run` against full test set at standard depth.
Publish: precision, recall, F1, severity accuracy, false positive rate.
This becomes the number on the README.

---

## Success Criteria

| Metric | Target | Rationale |
|--------|--------|-----------|
| Detection Recall | ≥ 0.80 | Must find 80%+ of real issues |
| Detection Precision | ≥ 0.70 | Acceptable false positive rate |
| F1 | ≥ 0.75 | Balanced performance |
| False Positive Rate (clean) | ≤ 0.15 | Max 15% noise on clean artifacts |
| Verdict Accuracy | ≥ 0.75 | Correct pass/fail 75%+ of the time |

These are initial targets. Calibration may reveal they need adjustment — that's the point of measuring.
