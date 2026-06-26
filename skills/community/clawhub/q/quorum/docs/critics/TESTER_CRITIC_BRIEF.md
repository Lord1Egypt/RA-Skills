# Tester Critic — Design Brief

**Status:** Shipped (v0.6.0). L1 deterministic + L2 LLM verification. Wired into pipeline as Phase 3 (v0.7.0). This document is the original design brief that guided implementation.

**Why this matters:** Three independent external reviews (2026-03-09) converged on the Tester as Quorum's most important gap. The Tester shipped in v0.6.0.

**Design principle reminder:** Quorum is the gate, not the road.

---

## What It Does

The Tester is a **finding verifier**, not a traditional critic. It takes other critics' findings as input and independently verifies whether the cited evidence actually exists and supports the claim.

It answers: "The Correctness critic says line 247 of cli.py has an unchecked return value. Is that true?"

## How It's Different

| | Existing Critics | Tester |
|---|---|---|
| Input | The artifact being validated | Other critics' findings |
| Method | LLM judgment against rubric | Deterministic verification + optional LLM |
| Timing | Phase 2 (parallel) | Phase 2.5 (after critics, before Aggregator) |
| Output | Findings with evidence | Verification tags on others' findings |

## Three Verification Levels

### Level 1: Locus Verification (deterministic, zero API cost)
- Extract file:line from finding's locus
- Open file, read the cited line(s)
- Fuzzy match cited evidence against actual content
- **Catches:** hallucinated line numbers, wrong file references, stale loci
- **Shipped:** v0.6.0

### Level 2: Claim Verification (hybrid — deterministic + light LLM)
- Read the code/text surrounding the locus
- One focused LLM call: "Given this excerpt and this claim, is the claim accurate?"
- **Catches:** mischaracterized code, overstated severity, correct line but wrong conclusion
- **Shipped:** v0.6.0

### Level 3: Execution Verification (deterministic, sandboxed)
- For executable claims (regex patterns, import checks, syntax validation): actually run them
- For coverage claims: run coverage analysis
- Requires sandboxing — significant security surface
- **Status:** Deferred, gated behind `--tester-execute`

## Output: Verification Tags

Each finding gets tagged:
- **VERIFIED** — locus confirmed, claim matches reality
- **UNVERIFIED** — locus exists but claim couldn't be confirmed (ambiguous)
- **CONTRADICTED** — locus exists but contradicts the claim

## Aggregator Integration

- VERIFIED findings: accepted at stated severity
- UNVERIFIED findings: severity downgraded by one level (CRITICAL→HIGH, etc.)
- CONTRADICTED findings: dropped entirely with explanation in audit trail
- Conservative defaults: UNVERIFIED means "lower confidence," not "discard"

## Known Hard Problems

1. **Finding parsing** — critics output free-form text. Extracting structured (file, line, claim_type) from unstructured findings is brittle. May need to enforce structured locus format from critics first (prerequisite change).

2. **Line number drift** — if the Fixer modified the file in a re-validation loop, line numbers shift. Tester must handle this (fuzzy line matching, content-based lookup rather than line-number-only).

3. **False negatives on the verifier** — wrongly marking real findings as UNVERIFIED is worse than not having a Tester. Must be conservative.

4. **Cost at scale** — Level 2 adds an LLM call per finding. 50 findings = 50 calls. Need `--verify-findings` opt-in or smart filtering (only verify CRITICAL/HIGH by default).

## Prerequisite Changes

Before building the Tester itself:
1. **Structured locus format** — ensure all critics output findings with parseable `file:line` loci (may already be mostly true via Evidence/Locus Pydantic models — verify)
2. **Finding serialization** — Tester needs to read critic JSON outputs from the run directory. Verify the schema is stable and sufficient.
3. **Pipeline hook point** — the pipeline currently goes critics → aggregator. Need a Phase 2.5 insertion point.

## Build Phases (suggested)

**Phase 1: Foundation (~1 session)**
- Finding parser: extract structured loci from critic JSON outputs
- Level 1 verifier: file read + fuzzy content match
- Unit tests with synthetic findings (known-good and known-bad loci)
- No pipeline integration yet — standalone module

**Phase 2: Integration (~1 session)**
- Wire into pipeline as Phase 2.5
- Aggregator changes to consume verification tags
- Level 2 verifier: light LLM claim checking
- Integration tests against real Quorum run outputs

**Phase 3: Hardening (~0.5 session)**
- Edge cases: line drift, multi-line loci, findings without loci
- Cost controls: `--verify-findings`, severity-based filtering
- Audit trail: verification results in run directory
- Full test suite

## Estimated Scope
- ~1,500 lines of code (verifier + parser + aggregator changes)
- ~500 lines of tests
- ~3 focused sessions, not one marathon

## References
- Three independent external reviews (2026-03-09) converged on the Tester as Quorum's most important gap. The Tester shipped in v0.6.0.
- Current critic architecture: `SPEC.md` §Critics, §Aggregator
- Finding/Evidence/Locus models: `quorum/models.py`
