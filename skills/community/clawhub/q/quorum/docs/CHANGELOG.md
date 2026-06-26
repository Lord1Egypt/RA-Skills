# Changelog

All notable changes to Quorum will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.7.3] — 2026-03-15

### Fixed — Pre-Existing Code Findings Cleanup

- **`__version__` corrected** — `reference-implementation/quorum/__init__.py` now reads `0.7.3` (was stuck at `0.5.3` since initial release; PyPI showed `0.7.2` but runtime `__version__` did not match)
- **Broad exception handling narrowed** (prescreen.py) — PS-006 `except Exception` narrowed to `(OSError, UnicodeDecodeError)`; external tool integrations (Ruff, DevSkim, Bandit, PSSA) now log with `exc_info=True` for traceback capture on unexpected failures
- **PSScriptAnalyzer security documentation** (prescreen.py) — Added comprehensive `# SECURITY:` comment explaining the PowerShell single-quote injection trust model for `_run_pssa`
- **SPEC.md §2.1 overclaiming fixed** — Numbered agent list now separates shipped critics (6) from planned critics (3) and infrastructure agents; Code Hygiene and Cross-Artifact Consistency added (were missing from list despite being shipped)
- **validate-docs.py hardcoded range removed** — `check_hardcoded_counts` `range(2, 9)` replaced with parameterized bounds derived from manifest total critic count
- **validate-docs.py SRP cleanup** — Extracted `_extract_pyproject_version()` and `_extract_badge_versions()` as pure functions; `main()` refactored to delegate to `validate_docs()` (eliminated duplicated validation loop)
- **Test exception handling** (test_batch_resilience.py) — Broad `except Exception` narrowed to `(json.JSONDecodeError, OSError)` with explanatory comment

---

## [0.7.2] — 2026-03-12

### Documentation — Stale Content Cleanup (PR #18)

- **External reviews removed**: 3 frontier model review files (GPT-5.4, Opus 4.6, Grok 4.20) and ideas-backlog.md deleted — reviews were run against v0.5.3 and no longer reflect current capabilities. `EXTERNAL_REVIEWS.md` replaced with community invitation template.
- **13 stale content findings resolved** across SPEC.md, IMPLEMENTATION.md, CONFIG_REFERENCE.md, TUTORIAL.md, SKILL.md, RUBRIC_BUILDING_GUIDE.md, SECURITY_CRITIC_FRAMEWORK.md, CODE_HYGIENE_FRAMEWORK.md, TESTER_CRITIC_BRIEF.md, and INSTALLATION.md:
  - Tester marked as shipped (was "SPECIFIED, not yet built")
  - Critic counts updated to 6 shipped across all docs
  - Learning memory marked as shipped (v0.5.3) across all docs
  - Confidence scores replaced with coverage language (v0.6.1)
  - Version headers updated to v0.7.2
  - Depth profile critic counts aligned with critic-status.yaml
  - Broken cross-reference paths fixed (TESTER_CRITIC_BRIEF, INSTALLATION)
  - Security and Code Hygiene framework status checklists updated

### Documentation — Docs Restructure & README Rewrite (PR #16)

- **README.md** rewritten: ~400 lines → ~120 lines. Focused on what Quorum is, how to run it, and where to go next. First-person voice preserved.
- **23 docs reorganized** into 6 categorized subdirectories under `docs/`:
  - `getting-started/` — QUICK_START, INSTALLATION, TUTORIAL, FOR_BEGINNERS, MODEL_REQUIREMENTS
  - `architecture/` — IMPLEMENTATION, THE_NINE
  - `critics/` — all critic-specific docs and frameworks
  - `guides/` — RUBRIC_BUILDING_GUIDE, CROSS_ARTIFACT_DESIGN
  - `reviews/` — community and practitioner evaluations
  - `configuration/` — CONFIG_REFERENCE
- **New files:** `docs/getting-started/QUICK_START.md` (zero to running in <5 min), `docs/README.md` (navigation hub)
- All cross-references updated across 30+ files
- `validate-docs.py` exclusion updated to match new `docs/reviews/` path

### Fixed
- 7 broken relative links caused by docs moving one directory deeper (CONFIG_REFERENCE, SPEC, CONTRIBUTING, reference-implementation paths)
- `SKILL.md` frontmatter: "4 independent AI critics" → "6" (matched shipped state)
- `README.md` version badge: v0.7.0 → v0.7.2

---

## [0.7.1] — 2026-03-12

### Fixed — Self-Validation Findings (PR #14)

Ran Quorum self-validation (standard depth) against all shipped artifacts in v0.6.1, Copilot CLI Port, Golden Test Set, and core engine. Fixed **64 findings** across **10 files** — 3 CRITICAL, 16 HIGH, 45 MEDIUM/LOW.

#### Critical Fixes
- **aggregator.py** — INFO-only findings now correctly produce PASS (not PASS_WITH_NOTES), honoring the documented verdict contract
- **pipeline.py** — `resume_batch_validation` now restores original config + relationships_path from manifest (was hardcoding None, causing resumed batches to produce different results than original runs)
- **models.py** — `Locus` now validates `start_line <= end_line` and `_hash_byte_range` raises ValueError on out-of-bounds ranges instead of silently hashing empty bytes

#### High-Impact Fixes
- **Severity normalization** (base.py, cross_consistency.py) — malformed LLM severity strings no longer discard ALL findings for that critic
- **Format-string injection** (cross_consistency.py) — user YAML `scope` field now brace-escaped before `str.format()`
- **Deterministic dedup** (aggregator.py) — findings sorted by severity before greedy matching; output no longer depends on input ordering
- **CancelledError handling** (pipeline.py) — cancelled futures in batch loops no longer crash pipeline
- **Library-safe prescreen** (quorum-prescreen.py) — `run_prescreen()` returns error dicts instead of calling `sys.exit()`

#### Tests
- 879 passed, 0 failures
- 2 tests updated: `test_info_finding_pass_with_notes` and `test_verdict_json_serialization_never_none` (codified buggy behavior; now corrected)

#### Process
- Added mandatory self-validation step to Claude Code task template (`~/.claude/tasks/README.md`)

---

## [0.7.0-port.1] — 2026-03-12

### Added
- **Copilot CLI port** at `ports/copilot-cli/` — Quorum's multi-critic validation framework packaged as a GitHub Copilot CLI skill. Zero infrastructure, zero pip dependencies.
  - `SKILL.md` (414 lines): Orchestrator skill — artifact classification, rubric selection, prescreen gating, critic dispatch, verdict aggregation, report generation.
  - `quorum-prescreen.py` (649 lines): Stdlib-only pre-screen implementing PS-001 through PS-010. PyYAML optional for YAML artifact support.
  - 5 critic `.agent.md` files: Verbatim prompts for correctness, completeness, security, code hygiene, and cross-consistency critics.
  - 3 rubric JSON files: Byte-identical copies from reference implementation (python-code, research-synthesis, agent-config).
  - `README.md`: Install and usage guide.
  - `ARCHITECTURE.md`: Port design rationale and mapping to reference implementation.

### Changed
- `.gitignore`: Removed `ports/` exclusion — ports are now tracked for public release.

## [0.7.0] — 2026-03-12

### Added
- **TesterCritic wired into pipeline as Phase 3** (DEC-020). The Tester verifies other critics' findings after Phase 1 (single-file critics) and Phase 2 (cross-consistency), before the Aggregator produces the verdict.
  - **L1 contradictions auto-excluded**: If a critic cites a file/line that doesn't exist or content that doesn't match, the finding is silently removed from verdict calculation. Preserved in tester output for audit.
  - **L2 contradictions annotated**: If the Tester's LLM judges a claim unsupported by evidence, the finding gets a `[L2-CONTRADICTED]` annotation but remains in the verdict. Human decides.
  - **Depth-based activation**: Quick = skip, Standard = L1 only (zero API cost), Thorough = L1 + L2.
- **Tester stats in run manifest**: `verified`, `unverified`, `contradicted`, `verification_rate`, `runtime_ms`.
- **Verification section in report.md** when tester results are present: table of verified/unverified/contradicted counts with per-finding exclusion details.
- 12 new integration tests (`test_tester_pipeline_integration.py`). Total: 879 passed, 6 skipped.

### Changed
- `AggregatorAgent.run()` accepts optional `tester_result` parameter. Applies DEC-020 policy before deduplication.
- `AggregatedReport` model gains `tester_result` and `l1_excluded_count` fields.
- Verdict reasoning now includes excluded finding count when tester ran.
- Removed unnecessary `asyncio.CancelledError` isinstance guards (CancelledError is BaseException in Python 3.9+, never caught by `except Exception`).

## [0.6.1] — 2026-03-11

### Changed
- **Confidence scores replaced with criteria coverage.** Verdicts now report "Coverage: N% of criteria evaluated" with per-critic criteria counts (`criteria_evaluated` / `criteria_total`) instead of fabricated confidence percentages. The previous formula (`0.5 + ratio × 0.45`) always returned ~0.95 since evidence non-emptiness was already enforced upstream — the number was decorative. Coverage counts are honest and verifiable.
- **Aggregator confidence** now computes total criteria evaluated across all critics rather than averaging per-critic scores with skip penalties and agreement bonuses.
- **Report output** shows "N/M criteria" per file and "Coverage: N% of criteria evaluated" in batch and single-file reports. Fixer proposal confidence (LLM self-assessed) is unchanged — it's a legitimately different concept.
- `CriticResult` model gains `criteria_total` and `criteria_evaluated` fields.

### Fixed
- **SPEC.md** status summary updated to reflect 6 shipped critics (was still showing "4/9" from v0.5.x).
- **IMPLEMENTATION.md** status header updated to v0.6.0 with correct critic count and pointer to `critic-status.yaml` as authoritative source.

### Tooling
- **`validate-docs.py` enhanced**: version consistency checks across all doc files, depth config validation against `critic-status.yaml`, fraction pattern detection (DEC-019: no exposed denominators for critic counts), callable vs shipped distinction.
- **`critic-status.yaml` extended**: `callable` flag (shipped vs invocable in pipeline), `spec_version`, `depth_configs` per depth profile.

## [0.6.0] — 2026-03-10

### Added

#### Tester Critic (Milestone #10) — Critic 6 of 9
- **L1 Deterministic Verification**: checks finding loci exist, line numbers are in range, excerpts match source text, file paths are valid
- **L2 LLM Claim Verification**: language model evaluates whether each finding's claim is substantiated by the cited evidence
- 805 lines of code, 994 lines of tests, 76/76 passing
- Merged via PR #8

#### Shipping Process Infrastructure
- **`critic-status.yaml`** — single source of truth for shipped critic and feature status. All doc references derive from this manifest instead of hardcoding counts
- **`tools/validate-docs.py`** — automated doc validation that reads the manifest, scans all public markdown files for stale critic counts, outdated status markers (🔜/Planned for shipped critics), and roadmap references to shipped features. Exit 0 = clean, exit 1 = findings
- **`SHIPPING.md`** — shipping checklist for humans and agents (including Claude Code) to follow before merging feature PRs to main
- **`.github/workflows/validate-docs.yml`** — CI enforcement: runs `validate-docs.py` on every PR to main. Manual checks have repeatedly failed to catch doc staleness; CI is the reliable gate

#### SEC-07: Self-Validation Convergence Problem
- Documented the iterative self-validation convergence problem observed during PR #8
- Root cause: fresh context per run, fix-induced findings, severity recalibration, no delta awareness
- Five mitigations proposed; interim decision: advisory-only self-validation (CRITICAL-only blocking)
- Self-validation moved to non-required in GitHub branch ruleset

### Changed
- **Cross-Consistency critic** now counted as shipped (critic 5 of 9) in all documentation, with visible note that it requires `--relationships` flag
- Version bump to 0.6.0 across `pyproject.toml`, `critic-status.yaml`, and all docs

### Documentation
- **Full doc sweep**: 10 files updated to reflect 6 shipped critics (was inconsistently 4 or 5 across different files)
- README.md architecture diagram updated: Cross-Consistency and Tester moved to "shipped" row; Style remains in "roadmap"
- SPEC.md status matrix, limitations, and roadmap sections updated (6/9 implemented, 3 remaining)
- CONFIG_REFERENCE.md, TUTORIAL.md, IMPLEMENTATION.md — Tester status markers updated from 🔜 to ✅
- FOR_BEGINNERS.md — critic counts and cost estimates updated
- MODEL_REQUIREMENTS.md — cost estimates updated for 6-critic standard depth
- CROSS_ARTIFACT_DESIGN.md — `threat_context` relationship type marked as shipped
- SEC03_EVIDENCE_INTEGRITY.md — Tester status updated from "planned" to "shipped"
- docs/TESTER_CRITIC_BRIEF.md — design brief for Tester critic

### Roadmap Status
- [x] Tester critic (Milestone #10) — L1 deterministic + L2 LLM verification
- [x] Shipping process infrastructure — manifest, validation script, CI gate, checklist
- [ ] Architecture critic (Milestone #9)
- [ ] Confidence calibration (Milestone #6b)
- [ ] Delegation critic (Milestone #11)
- [ ] Style critic (Milestone #12)
- [ ] **Hardware-backed result protection** (Milestone #18)

---

## [0.5.3] — 2026-03-09

### Added

#### Re-Validation Loops (Milestone #5c)
- **Fix-verify cycle**: Fixer proposes text replacements for CRITICAL/HIGH findings → applies them to a working copy → re-runs only the critics that flagged the originals → compares before/after
- **Delta tracking**: each loop reports `improved`, `unchanged`, or `regressed` with finding counts
- **Loop control**: stops early when all findings clear, no proposals generated, or `max_fix_loops` reached (max 3)
- **CLI flag**: `--fix-loops N` overrides depth profile default; `--depth thorough` defaults to 1 loop
- **Immutable originals**: fixed artifacts saved as `artifact-fixed.txt` in run directory; original file never modified
- Per-loop audit trail: `fix-proposals-loop-N.json` saved for each iteration

#### Learning Memory (Milestone #7)
- **Recurring pattern tracking**: `known_issues.json` stores failure patterns with stable SHA-256 pattern IDs, frequency counts, first/last seen dates
- **Auto-promotion**: patterns seen ≥3 times automatically promoted to mandatory checks
- **Critic injection**: mandatory patterns prepended to critic system prompts as natural language instructions — critics are aware of known recurring issues
- **CLI subcommands**: `quorum issues list` (table view), `quorum issues promote --threshold N`, `quorum issues reset`
- **Run integration**: learning memory loads at start, updates after verdict, stats written to `run-manifest.json`
- **Opt-out**: `--no-learning` flag disables for a run
- Atomic file writes (tmp + rename) to prevent corruption

#### Pre-Screen Expansion (Milestone #15)
- **Ruff S-rules**: Python security linting via `ruff check --select S` (S1xx → MEDIUM, S2xx+ → HIGH)
- **Bandit**: Python security analysis with native severity/confidence mapping; deduplicated with Ruff when both present
- **PSScriptAnalyzer**: PowerShell security rules via `pwsh` — filters to 8 security-relevant rules (AvoidUsingInvokeExpression, AvoidUsingBrokenHashAlgorithms, etc.)
- All three tools follow the DevSkim pattern: detect if installed, run if available, graceful degradation if not
- Pre-screen now has 5 layers: built-in regex (PS-001–010) → DevSkim → Ruff → Bandit → PSScriptAnalyzer

#### Crash-Resilient Batch Validation
- **Progressive manifest**: `batch-manifest.json` updates atomically after each file completes (not just at the end). Tracks `completed_files`, `failed_files`, `status` (running/completed/interrupted)
- **Resume**: `quorum run --resume <batch-dir>` reads manifest, skips completed files, re-validates crashed entries, only pays for remaining work
- **Graceful shutdown**: SIGTERM/SIGINT handler saves all in-flight work with `status='interrupted'` before exiting
- **Progressive report**: `batch-report.md` grows as files complete instead of one big write at the end

#### Cost Tracking and Estimation (Milestone #16)
- **Per-call tracking**: CostTracker records prompt/completion tokens and USD cost for every LLM call via `litellm.completion_cost()`
- **Budget cap**: `--max-cost $10` stops gracefully when cumulative cost exceeds threshold — saves all work collected so far
- **Pre-run estimate**: prints "Estimated cost: $X.XX (Y critic calls across Z files). Proceed? [Y/n]" — auto-skips under $0.50 or with `--yes`
- **Cost report**: CLI output shows per-file cost breakdown; `run-manifest.json` includes full cost summary
- Hardcoded rates for Claude, GPT, Gemini, Mistral families; graceful fallback for unknown models

#### CSV Audit Reports (Milestone #17)
- **`audit-detail.csv`**: one row per file — SHA-256 hash, file size, token estimate, analysis start/end/duration, input/output tokens, tokens/sec, models used, verdict, finding count, cost
- **`audit-summary.csv`**: single aggregate row — totals, avg/median tokens/sec, cost by model (JSON), pass/fail counts
- `--audit-report` flag, auto-enabled at `--depth thorough`
- SHA-256 artifact hashes stored in `run-manifest.json`

### Fixed
- **PSScriptAnalyzer command injection**: single quotes in file paths now escaped before passing to `pwsh -Command`
- **Learning memory save resilience**: `save()` wrapped in try/except to prevent crash on write failure

### Documentation
- **docs/README.md** — new documentation index with categorized links to all framework docs
- **docs/SEC02_BUSINESS_LOGIC_VALIDATION.md** — severity calibration table, shared manifest example, Option C success/failure criteria, depth-level mapping (per Devola's review)
- **SPEC.md** — Security Critic links to SEC-02 workflow; Fixer updated to reflect re-validation loops; learning memory sections updated from "planned" to "shipped"
- **README.md** — updated to v0.5.3: all new features, CLI flags, cost tracking, audit reports, crash resilience

### Roadmap Status
- [x] Re-validation loops (Milestone #5c)
- [x] Learning memory (Milestone #7)
- [x] Pre-screen expansion — Ruff, Bandit, PSScriptAnalyzer (Milestone #15)
- [x] PyPI publish (Milestone #14) — `pip install quorum-validator`
- [x] **Cost tracking and estimation** (Milestone #16) — per-call token counts via LiteLLM, cumulative run cost in manifest, pre-run estimate, `--max-cost` budget cap, cost report in CLI output
- [x] **CSV audit reports** (Milestone #17) — per-file SHA-256, timing, token counts, cost breakdown; aggregate summary with median tokens/sec and cost-by-model
- [x] **Crash-resilient batch validation** — progressive manifest saves, `--resume`, graceful SIGTERM/SIGINT shutdown
- [ ] Architecture critic (Milestone #9)
- [ ] Tester critic (Milestone #10)
- [ ] Confidence calibration (Milestone #6b)
- [ ] Delegation critic (Milestone #11)
- [ ] Style critic (Milestone #12)
- [x] Self-validation graduation (GRAD) — CI gate on PRs to main, standard depth, changed files only, $5 budget cap
- [ ] **Hardware-backed result protection** (Milestone #18) — YubiKey KEK wrapping per-run DEKs, encrypted-at-rest validation results, HMAC tamper evidence over run manifests. For sensitive security assessments where findings themselves are high-value targets. CKMS-aligned (SP 800-130/152 principles applied to the validation pipeline)

---

## [0.5.2] — 2026-03-08

### Added

#### DevSkim Pre-Screen Integration
- **New SAST pass: DevSkim** — second security linter alongside the existing 10 deterministic pre-screen checks (~690 lines)
- Catches patterns that regex-based PS-002 misses; runs as part of the pre-screen phase before LLM critics
- Pre-screen layer now has two passes: deterministic rules (PS-001–PS-010) + DevSkim SAST

#### Structured Output Enforcement
- **New utility: `extract_json_from_response()`** — strips markdown fence wrappers (` ```json `) from critic JSON responses before parsing
- **25 tests** covering fence-wrapped, bare JSON, and malformed inputs
- Prevents critic JSON parse failures when LLM wraps output in markdown blocks

#### threat_context Relationship Type
- **New relationship type: `threat_context`** for `quorum-relationships.yaml` — surfaces threat model context to the SEC-04 (Authorization) critic
- Enables cross-artifact authorization review with declared threat scope

#### Test Suite + CI Pipeline
- **560 tests passing** via pytest — expanded from 524 (0.5.1) to 560 with new structured output tests
- **GitHub Actions CI** — automated on push/PR; `setup-python@v5`, `codecov@v4`

#### Implementation Status Markers
- **`✅ Shipped` / `🔜 Planned` markers** added across framework docs
- Distinguishes shipped capability from roadmap intent at a glance

### Documentation

- **SEC-02 business logic validation workflow** — documents the requirements→critic path for business logic review
- **PowerShell coverage assessment** — honest ~70% coverage disclosure; DevSkim finding documented; confirmed SAST landscape gaps noted
- **PEP framework grounding for Python code rubric** — PC-001–PC-025 criteria now cite PEP 8, PEP 20, PEP 257, PEP 484, PEP 526
- **CODE_HYGIENE_FRAMEWORK.md** — added to public repo

### Fixed

- **Claim discipline audit** — README and SPEC overclaiming corrected; 5 line-level issues resolved; internal docs removed from public repo
- **Internal reference leaks** — removed internal boundary instructions from public SKILL.md and internal references from public repo
- **arXiv citation corrected** — "Council as Judge" → "Replacing Judges with Juries" (Verga et al., 2024)
- **Broken links** — fixed broken links and removed domain-specific roadmap from public repo
- **CI action versions** — bumped `setup-python` to v5, `codecov` to v4
- **Email addresses** — replaced personal emails with `@sharedintellect.com` in `pyproject.toml`
- **Version string sync** — `pyproject.toml` and `__init__.py` aligned to 0.5.1 before this release

### Roadmap Status
- [x] Test suite + CI — 560 tests, GitHub Actions
- [x] Claim discipline audit — completed
- [x] Python rubric framework grounding — PEP citations added
- [x] Pre-screen expansion (Phase 1) — DevSkim integrated
- [ ] Re-validation loops — apply Fixer proposals → re-run critics → verify (Milestone #5c)
- [ ] Architecture critic (Milestone #9)
- [ ] Tester critic (Milestone #10)
- [ ] Confidence calibration (Milestone #6b)
- [ ] **Learning memory** (Milestone #7) — wire up known_issues.json frequency tracking + mandatory check promotion
- [ ] **PyPI publish** (Milestone #14) — `pip install quorum-validator` instead of clone + install (package name finalized as `quorum-validator`)
- [ ] Delegation critic (Milestone #11)
- [ ] Style critic (Milestone #12)
- [ ] Documentation headers adoption (Phase 1–4)
- [ ] Self-validation graduation (GRAD)

---

## [0.5.1] — 2026-03-06

### Added — Parallel Execution, Python Code Rubric, Fixer Agent

#### Parallel Critic Execution
- **Critics run concurrently** via `ThreadPoolExecutor` (max 4 critics in parallel)
- **Batch files run concurrently** (max 3 files processed simultaneously)
- Significant throughput improvement for multi-critic and batch validation runs

#### Python Code Rubric (NEW)
- **New built-in rubric: `python-code`** — 25 criteria (PC-001–PC-025)
- **Auto-detection** — rubric is automatically selected when `--target` is a `.py` file and no rubric is specified
- 3 built-in rubrics now shipped: `research-synthesis`, `agent-config`, `python-code`

#### Fixer Agent (NEW — Phase 1.5)
- **New agent: Fixer** — activates when `max_fix_loops > 0` (thorough depth default: 1)
- **Proposal mode** — proposes concrete text replacements for CRITICAL/HIGH findings
- **Pipeline position:** Phase 1.5, between critic dispatch and cross-artifact consistency
- Re-validation loops (apply proposals → re-run critics → verify) are deferred to a future release

### Self-Validation
- Ran Quorum against itself using the new Python code rubric
- Result: REVISE, 16 findings — pipeline refactor in progress

---

## [0.5.0] — 2026-03-06

### Added — Framework-Grounded Critics

#### Code Hygiene Critic (NEW)
- **New module: `critics/code_hygiene.py`** — evaluates structural code quality
- **Grounded in:** ISO/IEC 25010:2023 (Maintainability + Reliability), ISO/IEC 5055:2021 (CISQ CWE mappings)
- **12 evaluation categories** (CAT-01 through CAT-12): Code Correctness, Error Handling, Resource Management, Complexity & Modularity, Code Duplication, Naming & Documentation, Type Safety, Async & Concurrency, Import Hygiene, Style & Formatting, Portability, Testability
- **6 agentic patterns** (AP-01 through AP-06): Prompt Construction, LLM API Calls, Agent Pipeline Errors, Credential Management, Timeout & Retry, Logging & Observability
- **Two-layer architecture** — deterministic pre-screen rules + LLM judgment for what SAST cannot catch
- **Delegation boundary** — flags security-relevant patterns (eval, exec, credentials) but explicitly delegates security assessment to Security Critic
- **Evidence grounding enforced** — inherits BaseCritic's evidence mandate

#### Security Critic (REVISED — Framework-Grounded Upgrade)
- **Upgraded from ad-hoc to framework-grounded evaluation**
- **Now grounded in:** OWASP ASVS 5.0.0 (17 chapters), CWE Top 25 (2024), NIST SP 800-53 SA-11, ISO/IEC 25010:2023 Security sub-characteristics
- **14 security categories** (SEC-01 through SEC-14): Injection, Input Validation, Authentication, Authorization, Session/Tokens, Cryptography, Secrets, Path Traversal, Deserialization, SSRF, Error/Info Disclosure, Security Logging, Supply Chain, DoS
- **Tiered evaluation model** — Tier 1 (must-evaluate), Tier 2 (should-evaluate), Tier 3 (deep-analysis)
- **Detection capability matrix** — instructs LLM to focus on SAST-blind categories (authorization logic, IDOR, JWT, SSRF, authentication bypass)
- **Finding citation format** — ASVS §section, CWE-ID, SA-11 sub-control references
- **All 6 original focus areas preserved** — context-aware sensitivity, proprietary content, info disclosure, prompt injection, dependency risk, boundary enforcement (enhanced with framework citations)

#### Research Corpus (NEW — 5 Research Documents)
- `docs/research/iso-25010-quality-model.md` — ISO/IEC 25010:2023, 9 characteristics, 40 sub-characteristics, evaluability classification
- `docs/research/cisq-quality-measures.md` — ISO/IEC 5055:2021, 195 weaknesses across 4 dimensions with CWE IDs
- `docs/research/python-static-analysis-taxonomy.md` — Ruff 900+ rules, Pylint 500+ messages, quality dimension coverage matrix
- `docs/research/powershell-static-analysis-taxonomy.md` — PSScriptAnalyzer 69 rules, 6 quality dimensions, agentic patterns
- `docs/research/security-code-review-frameworks.md` — OWASP ASVS 5.0, CWE Top 25, CERT, NIST SA-11 cross-reference

#### Framework Specifications (NEW)
- `docs/CODE_HYGIENE_FRAMEWORK.md` (~50KB) — complete evaluation spec for Code Hygiene Critic
  - All 40 ISO 25010:2023 sub-characteristics mapped with inclusion/exclusion rationale
  - Two-layer architecture per category (deterministic + LLM judgment)
  - CERT applicability note (no official Python/PowerShell standard)
  - Two-critic architecture narrative (delegation boundary)
- `docs/SECURITY_CRITIC_FRAMEWORK.md` (~47KB) — complete evaluation spec for Security Critic
  - Detection capability matrix (40 rows: SAST strength vs. LLM advantage)
  - Python checklist (25 items) + PowerShell checklist (24 items)
  - Minimum viable coverage for SA-11 alignment (Tier 1/2/3)
  - Framework cross-reference: where ASVS/CWE/CERT/SA-11 overlap vs. contribute uniquely
  - Finding citation vocabulary with severity calibration

#### Cross-Artifact Consistency Design (NEW)
- `docs/CROSS_ARTIFACT_DESIGN.md` — architectural decisions for Roadmap item #6
- **Design axiom:** "In a judgment system, always trade toward transparency over convenience"
- **Decision 1:** Explicit relationship declaration via `quorum-relationships.yaml` manifest (auto-inference deferred)
- **Decision 2:** Separate cross-consistency critic type (preserves single-file critic composability)
- **Decision 3:** Multi-locus Finding model with `Locus` objects (role annotations, `source_hash` for drift detection)
- **Data flow contract:** Cross-critic receives single-file findings (evidence) but not verdicts (conclusions) — preserves assessor independence

#### Documentation Standards (NEW)
- `docs/DOCUMENTATION_STANDARDS.md` — universal `@KEY: value` header schema
- Three required keys: `@module`/`@doc`/`@config`/`@script`, `@purpose`, `@version`
- Decision-density heuristic for Strategy A (inline) vs. Strategy B (reference doc)
- Machine-readable `quorum-header-schema.yaml` for pre-screen validation
- Single source of truth: `@relationships` points to manifest, no duplicate declarations

### Fixed — Framework Document Corrections
- **S303 misattributed** to shelve in SEC-09 → corrected to S403 (pickle/shelve import detection)
- **S324 misattributed** to jsonpickle in SEC-09 → corrected to "no dedicated rule — LLM detection"
- **CWE-683 not in CISQ** → removed from CAT-01; CWE-561/570/571 reclassified with correct CISQ dimensions
- **3 missing ISO 25010 sub-characteristics** → added Interoperability, Appropriateness Recognizability, Scalability
- **AP-04/SEC-07 overlap** → delegation note added ("Hygiene flags, Security assesses")
- **CAT-02 child CWEs** → annotated as children of CWE-703 per CISQ conformance model

### Validated
- Framework docs: Validator Swarm PASS (78%) → Correctness re-run ISSUES_FOUND (91% confidence) → all findings fixed
- Code Hygiene Critic: Validator Swarm PASS (95% confidence) — 6/6 checks, 0 findings
- Security Critic revision: Validator Swarm PASS (95% confidence) — 6/6 checks, 0 findings
- Cross-checks: 2/2 passed — no overlap violation, consistent style

### Roadmap Status
- [x] Custom rubric loading (Milestone #1)
- [x] Multi-file / batch validation (Milestone #2)
- [x] Deterministic pre-screen layer (Milestone #3)
- [x] Security critic — framework-grounded (Milestone #4) ← **DONE**
- [x] Code hygiene critic (Milestone #5) ← **DONE**
- [x] Cross-artifact consistency (Milestone #6) ← **DONE**
- [x] Parallel critic execution (Milestone #8) ← **DONE**
- [x] Parallel batch validation (Milestone #8b) ← **DONE**
- [x] Python code rubric — 25 criteria, auto-detect on .py ← **DONE**
- [ ] Fix loops / Fixer agent (Milestone #5b) ← deferred; proposal mode implemented as NEW in [0.5.1], re-validation loops in [0.5.3]
- [ ] **Test suite + CI** (Milestone #13) — pytest smoke tests, import checks, GitHub Actions. Credibility gate: no tests = not production-ready. (Grok + GPT 5.4)
- [ ] **Claim discipline audit** — GPT 5.4 scored 2.5/5 on both README and SPEC. Fix: README ("production-grade"), GitHub org/repo descriptions ("9 critics" + "learning memory"), model table ("not enough" without benchmarks), SPEC §1 framing (nine-agent → target architecture), research citations (Tomasev/ToolMaker = "engineering interpretation of," not "validated by")
- [ ] **Pre-screen expansion** (Milestone #15) — Wire actual SAST tools: `ruff check` (S1xx+), `bandit`, `PSScriptAnalyzer`. Current 10 regex checks become universal fallback. Frameworks reference 80+ rules from research corpus — integrate them.
- [ ] Re-validation loops — apply Fixer proposals → re-run critics → verify (Milestone #5c)
- [ ] Python rubric framework grounding — research swarm for PEP 8/257/484, Python antipatterns literature, map criteria to published sources with citations
- [ ] Architecture critic (Milestone #9)
- [ ] Tester critic (Milestone #10)
- [ ] Confidence calibration (Milestone #6b)
- [ ] **Learning memory** (Milestone #7) — wire up known_issues.json frequency tracking + mandatory check promotion
- [ ] **PyPI publish** (Milestone #14) — `pip install quorum-validator` instead of clone + install (package name finalized as `quorum-validator`)
- [ ] Delegation critic (Milestone #11)
- [ ] Style critic (Milestone #12)
- [ ] Documentation headers adoption (Phase 1–4)
- [ ] Self-validation graduation (GRAD)

---

## [0.2.0] — 2026-03-05

### Added — Parity Milestones #1–#3

#### Milestone #1: Custom Rubric Loading
- **File path rubrics** — `--rubric ./path/to/my-rubric.json` now loads custom rubric files directly
- **Schema flexibility** — rubric loader accepts field aliases: `category`→`severity`, `evidence_instruction`→`evidence_required`, `rationale`→`why`
- **Backwards compatible** — built-in rubric names still work as before
- **Unblocks:** domain-specific rubric development workflows

#### Milestone #2: Multi-File / Batch Validation
- **Directory targets** — `quorum run --target ./docs/` validates all text files in a directory
- **Glob patterns** — `quorum run --target "./**/*.md"` expands wildcards
- **Pattern filter** — `--pattern "*.yaml"` filters directory contents
- **Consolidated verdicts** — `BatchVerdict` aggregates per-file results with worst-case status propagation
- **Batch reports** — per-file summary table + aggregate findings in `batch-report.md` and `batch-verdict.json`
- **Batch run directories** — `quorum-runs/batch-TIMESTAMP/per-file/...` structure
- **Graceful degradation** — one file failing doesn't kill the batch; errors collected and reported separately
- **New models** — `BatchVerdict`, `FileResult` (Pydantic v2)
- **New functions** — `resolve_targets()` (file/dir/glob resolution), `run_batch_validation()`, `print_batch_verdict()`
- **Files changed:** `models.py`, `pipeline.py`, `cli.py`, `output.py`

#### Milestone #2 Security Hardening (Validator Swarm QA)
- **Path traversal guard** — `_validate_path()` with boundary enforcement on all resolved paths
- **Pattern sanitization** — `..` in `--pattern` explicitly rejected
- **Auto-boundary** — directory targets use themselves as boundary; globs use non-glob prefix
- **Path leakage mitigation** — error messages use relative/basename instead of full absolute paths

#### Milestone #3: Deterministic Pre-Screen Layer
- **New module: `prescreen.py`** — runs fast deterministic checks before LLM critics
- **10 checks implemented:**
  - PS-001: Hardcoded absolute paths (regex)
  - PS-002: Potential credentials/secrets (regex + base64 detection)
  - PS-003: PII patterns — email, phone, SSN-like (regex)
  - PS-004: JSON validity (`json.loads()`)
  - PS-005: YAML validity (`yaml.safe_load()`)
  - PS-006: Python syntax (`py_compile.compile()`)
  - PS-007: Broken relative markdown links (regex + file existence)
  - PS-008: TODO/FIXME/HACK/XXX markers
  - PS-009: Trailing whitespace + mixed CRLF/LF line endings
  - PS-010: Empty file detection
- **Evidence injection** — `to_evidence_block()` formats results for LLM critic prompt injection as `pre_verified_evidence[]`
- **Config toggle** — `enable_prescreen: bool` (default: true)
- **Extension-aware** — checks gated by file type; skipped checks marked in evidence
- **Zero new dependencies** — stdlib only
- **Pipeline integration** — pre-screen runs between rubric loading and critic dispatch; results written to `prescreen.json`
- **New models** — `PreScreenCheck`, `PreScreenResult` (Pydantic v2)
- **Files changed:** new `prescreen.py`, updated `models.py`, `config.py`, `pipeline.py`, `agents/supervisor.py`, `output.py`

### Changed
- `--target` CLI option now accepts strings (was `click.Path`) to support directories and globs
- `run-manifest.json` now includes `prescreen_enabled`, prescreen stats, `completed_at`, and `verdict`
- Supervisor `run()` accepts optional `PreScreenResult` for critic evidence enrichment

### Validated
- Milestone #2 validated by Validator Swarm v2.3 (Run #9, standard depth, 6 critics)
  - 19/19 correctness checks passed, 14/14 requirements addressed
  - 3 CRITICAL path traversal findings → resolved in security hardening
  - Final: all acceptance criteria met

### Roadmap Status
- [x] Custom rubric loading (Milestone #1) ← **DONE**
- [x] Multi-file / batch validation (Milestone #2) ← **DONE**
- [x] Deterministic pre-screen layer (Milestone #3) ← **DONE**
- [x] Security critic (Milestone #4) ← **DONE** (revision pending after framework validation)
- [~] Code hygiene critic (Milestone #5) ← **FRAMEWORK COMPLETE**, build pending
- [ ] Cross-artifact consistency (Milestone #6)
- [ ] Confidence calibration (Milestone #6b)
- [ ] Learning memory (Milestone #7)
- [ ] Fix loops (Milestone #5b)
- [ ] Self-validation graduation (GRAD)

### Research & Framework Documents (2026-03-05)
- **5-agent research swarm** covering ISO 25010:2023, CISQ/ISO 5055, Ruff/Pylint, PSScriptAnalyzer, OWASP ASVS 5.0/CWE/CERT/SA-11
- **`docs/CODE_HYGIENE_FRAMEWORK.md`** — 12 evaluation categories + 6 agentic patterns, two-layer architecture, full coverage matrix
- **`docs/SECURITY_CRITIC_FRAMEWORK.md`** — 14 security categories, Python/PowerShell checklists, detection capability matrix
- **Validator swarm: PASS (78% confidence)** — correctness critic timed out, re-run pending for higher confidence
- **4 findings** (1 MEDIUM, 3 LOW): ISO 25010 Safety sub-chars incomplete, grouped scope rows, cross-reference note, CERT limitation note

---

## [0.1.0] — 2026-02-23

### Added — Reference Implementation MVP
- **Working CLI** — `quorum run --target <file> --depth quick|standard|thorough`
- **2 critics** — Correctness and Completeness, both with evidence grounding enforcement
- **LiteLLM universal provider** — supports Anthropic, OpenAI, Mistral, Groq, and 100+ models
- **2 built-in rubrics** — `research-synthesis` (10 criteria) and `agent-config` (10 criteria)
- **Pipeline orchestration** — supervisor → critics → aggregator → verdict (sequential MVP)
- **Deterministic verdict assignment** — PASS / PASS_WITH_NOTES / REVISE / REJECT based on finding severity
- **Deduplication** — SequenceMatcher-based cross-critic finding dedup with source merging
- **Run directories** — timestamped output dirs with manifest, critic JSONs, verdict.json, report.md
- **First-run setup** — interactive config wizard (model tier + depth preference)
- **Example artifacts** — `sample-research.md` (planted contradictions, unsourced claims) and `sample-agent-config.yaml` (6 planted flaws)
- **FOR_BEGINNERS.md** — explains spec-driven AI tools for newcomers
- **Updated README** — real CLI commands, working install instructions

### Tested
- Research synthesis: 10 findings, REJECT verdict, all planted flaws detected, 8 duplicates merged
- Agent config: 12 findings, REJECT verdict, all 6+ planted flaws detected, 4 duplicates merged

### Fixed
- LiteLLM requires full model slugs (`anthropic/claude-sonnet-4-20250514`), not short names

---

## [1.0.0] — Target Release (Not Yet Shipped)

> **Status:** This entry describes the planned full-release architecture. None of the features below are yet implemented. See the Roadmap sections in recent releases for current status.

### Planned
- **9-agent parallel validation architecture** — Correctness, Architecture, Security, Delegation, Completeness, and Style critics, plus Tester, Fixer, and Aggregator
- **Evidence mandate** — every critique requires tool-verified evidence (schema parsing, web search, grep, exec output)
- **Rubric system** — JSON-based rubrics with weighted criteria, evidence types, and severity levels
- **Three depth profiles** — quick (3 critics, ~5 min), standard (6 critics, ~15 min), thorough (all 9, ~45 min)
- **Learning memory** — `known_issues.json` accumulates failure patterns across runs with severity, frequency, and auto-promotion to mandatory checks
- **Tomasev delegation critics** — bidirectional contract evaluation, span-of-control analysis, cognitive friction scoring, dynamic re-delegation triggers
- **Bounded reflection loops** — 1–2 fix rounds on CRITICAL/HIGH issues only, preventing infinite recursion
- **Structured aggregation** — deduplication by location+description, cross-validation of conflicts, confidence recalibration
- **Two-tier model architecture** — judgment-heavy roles on Tier 1 models, execution-heavy roles on Tier 2
- **Example rubrics** — research synthesis and swarm configuration rubrics included
- **Tutorial** — step-by-step walkthrough validating a deliberately broken agent configuration
- **Brand assets** — logo, social previews, README banners (light/dark/transparent)

### Notes
- External evaluation claim ("Grok 4.20 at 9.2–9.5/10") referenced a non-existent model version; removed until verifiable.

## Roadmap

- [ ] Dynamic critic specialization (v1.1)
- [ ] Critic-to-critic debate mode (v1.1)
- [ ] Deterministic domain pre-screen (v1.2)
- [ ] Hard cost ceiling with budget allocation (v1.2)
- [ ] Empirical confidence calibration (v2.0)
- [ ] Single-agent validation rubrics (v1.1)
