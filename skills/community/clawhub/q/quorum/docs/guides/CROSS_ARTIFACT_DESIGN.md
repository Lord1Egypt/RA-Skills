# Cross-Artifact Consistency — Design Decisions

**Status:** Fully implemented in v0.5.1  
**Date:** 2026-03-06  
**Roadmap:** Item #6  
**Depends on:** Milestone #2 (multi-file/batch) — shipped in v0.2.0

---

## Implementation Status

**v0.5.1 State:** Fully implemented in reference implementation.

- [x] Relationship manifest schema (quorum-relationships.yaml)
- [x] Multi-locus findings with role annotations
- [x] Source hash (SHA-256) for drift detection
- [x] Phase 2 orchestration with findings-only (not verdicts) passing
- [x] Assessor independence principle enforced in architecture

---

## Design Axiom

> In a judgment system, always trade toward transparency over convenience — transparent scope (explicit declarations), transparent judgment type (separate critics), and transparent evidence basis (annotated loci).

This axiom governs all three architectural decisions below and should be referenced when evaluating future proposals that trade transparency for automation.

---

## Decision 1: Relationship Discovery — Explicit Declaration

**Decision:** Users declare file relationships and their types in a manifest (`quorum-relationships.yaml`). Auto-inference is deferred to a future enhancement that proposes manifest entries for human approval.

**Rationale:**
- Captures *intended* contracts, not just observed references
- Avoids introducing a new failure mode in the trust layer (incorrect inference)
- Provides a clean interface that future auto-inference can populate without replacing
- Manifest is auditable, versionable, reviewable

### Manifest Schema

```yaml
# quorum-relationships.yaml
relationships:
  - type: implements        # code implements a spec
    spec: docs/SPEC.md
    impl: reference-implementation/quorum/pipeline.py

  - type: documents         # docs describe code behavior
    source: reference-implementation/quorum/cli.py
    docs: docs/CONFIG_REFERENCE.md

  - type: delegates         # one artifact defers to another
    from: docs/CODE_HYGIENE_FRAMEWORK.md
    to: docs/SECURITY_CRITIC_FRAMEWORK.md
    scope: "Security (all sub-characteristics)"

  - type: schema_contract   # output of A must match schema expected by B
    producer: quorum/prescreen.py
    consumer: quorum/critics/security.py
    contract: "PreScreenResult model"
```

**Relationship types** imply different consistency checks:
- `implements` → coverage verification (are all spec requirements addressed?)
- `documents` → accuracy verification (does documentation match behavior?)
- `delegates` → boundary verification (is the delegation complete and non-overlapping?)
- `schema_contract` → structural compatibility verification (do types match?)
- `threat_context` → security context injection (feeds roles, trust boundaries, and sensitive operations to the Security Critic for SEC-04 authorization review) ✅

Named roles on both sides (`spec`/`impl`, `source`/`docs`, `producer`/`consumer`) are more self-documenting than generic file lists. The `scope` field on `delegates` supports partial relationships, which is where real-world contracts live.

---

## Decision 2: Critic Architecture — Separate Cross-Consistency Critic

**Decision:** Cross-artifact consistency is a new critic type, not an enhancement to existing single-file critics.

**Rationale:**
- Cross-file checks are a fundamentally different question with different evidence structures, scheduling constraints, and remediation paths
- A separate critic category preserves single-file critic composability
- Keeps verdict semantics unambiguous (single-file verdicts remain single-file)
- Introduces zero regression risk to the existing pipeline

### Pipeline Coordination

The Supervisor coordinates a sequential dependency:

```
Phase 1 (parallel):  single-file critics → per-file findings + verdicts
Phase 2 (sequential): cross-consistency critic → cross-file findings + verdict
```

**Critical data flow contract:** The cross-consistency critic receives single-file **findings** (evidence) but NOT single-file **verdicts** (conclusions). This preserves independent judgment while avoiding redundant reporting.

- **Findings are evidence** — "S303 was flagged in loader.py at line 42"
- **Verdicts are conclusions** — "loader.py PASSED correctness"

If the cross-critic receives verdicts, it will be tempted to defer: "correctness already passed loader.py, so the schema contract is probably fine." That's rubber-stamping, not independent evaluation. The cross-critic must form its own conclusions from its own evaluation of the declared relationships, with awareness of what's already been flagged.

This is the same principle as assessor independence in compliance: share the evidence record so work isn't duplicated, but each assessor forms their own judgment.

---

## Decision 3: Evidence Model — Multi-Locus Findings with Role Annotations

**Decision:** Replace the single file reference in Finding with a list of Locus objects. Per-file findings become the single-locus degenerate case.

### Locus Schema

```python
class Locus(BaseModel):
    """A specific location in a specific file cited as evidence."""
    file: str                    # relative path
    start_line: int              # 1-indexed
    end_line: int                # inclusive
    role: str                    # e.g., "implementation", "specification", "documentation", "producer", "consumer"
    source_hash: str             # SHA-256 of raw file bytes at [start_line:end_line] at evaluation time

class Finding(BaseModel):
    """A single finding, potentially spanning multiple files."""
    id: str
    critic: str
    severity: str                # CRITICAL | HIGH | MEDIUM | LOW | INFO
    category: str
    description: str
    loci: list[Locus]            # >= 1 entry; single-locus = per-file finding
    framework_refs: list[str]    # e.g., ["CWE-683", "ASVS V8.2.*"]
    remediation: str
```

**Key design choices:**

- `role` is what makes a cross-file finding immediately interpretable — "this is the spec side, this is the implementation side"
- `source_hash` hashes the raw file content at the cited line range, NOT the critic's excerpt. Excerpts are LLM-generated paraphrases that vary between runs. Source content is deterministic. This answers "has the cited source changed?" not "did the critic describe it the same way twice?"
- Single-locus findings (the existing behavior) are the degenerate case — no migration needed, existing findings remain valid, new findings gain expressiveness

---

## Implementation Notes on Finding Model

The implementation extends the spec's Finding model with these additional fields for backward
compatibility with single-file critics:
- `evidence: Evidence` — structured evidence object (tool + result + citation)
- `location: Optional[str]` — human-readable location string
- `rubric_criterion: Optional[str]` — rubric criterion ID

These fields are used by Phase 1 critics. Cross-artifact findings use `loci` for precise
multi-file location tracking and `category` for finding classification.

Default values: `loci` defaults to empty list for Phase 1 findings (>= 1 enforced only
for cross-artifact findings). `framework_refs` and `remediation` have empty defaults for
backward compatibility.

**Truncation behavior:** Implementation truncates file content to 30,000 characters
(preserving start and end) for LLM context. When truncation occurs, coverage may be
partial — the critic is evaluating a representative subset of the file.

**Confidence estimation:** Confidence is estimated heuristically based on findings quality
(grounded vs. ungrounded ratio) and relationship count. Phase 1 critics use 0.75 baseline
for clean passes; cross-artifact uses 0.80 baseline. Active findings weight by evidence
grounding ratio.

**Pipeline coordination contract:** `pipeline.py` is responsible for filtering findings
from Phase 1 verdicts before passing to Phase 2. The cross-consistency critic receives
raw findings (evidence), not verdicts (conclusions), to preserve independent judgment.

---

## Notes on Implementation

### What Changes
- `models.py` — Add `Locus`, update `Finding` to use `loci: list[Locus]`
- `pipeline.py` — Add Phase 2 coordination after single-file critics complete
- `cli.py` — Add `--relationships` flag to load manifest
- `output.py` — Render multi-locus findings with file+role annotations
- New: `critics/cross_consistency.py` — the cross-artifact critic
- New: `relationships.py` — manifest loader and relationship type registry

### What Doesn't Change
- Single-file critic behavior (correctness, completeness, security, code hygiene)
- Pre-screen pipeline
- Rubric loading
- Config structure (relationships manifest is a separate file, not embedded in quorum-config.yaml)

---

*Design finalized: 2026-03-06. Approved by Daniel Cervera.*
