---
skill_bundle: a11y-audit
file_role: reference
version: 19
version_date: 2026-06-04
previous_version: 18
change_summary: >
  Records v2.1.1: sitemap index recursion so --sitemap works against
  large sites whose sitemap.xml is an index of per-section files.
---

# Changelog

## v2.1.1 -- 2026-06-04

- `scripts/scan.js` (v5): `--sitemap` now transparently recurses into
  `<sitemapindex>` documents, following each child `<sitemap><loc>` to
  the leaf URL set. Cycle-protected (50-doc cap), and find/replace runs
  before the child fetch so the rewritten host applies recursively.
  Caught while wiring publedge.org to the composite action — its
  sitemap.xml is a 7-section index, which the previous loader couldn't
  walk.

## v2.1.0 -- 2026-06-03

- Added CI-ready CLI flags to `scripts/scan.js`:
  - `--sitemap <url>` discovers targets from a sitemap.xml at scan time,
    with optional `--sitemap-find` / `--sitemap-replace` host rewriting
    and `--sitemap-exclude <regex>` URL filtering.
  - `--fail-on errors` makes the script exit non-zero (status 2) when
    axe reports any violation, so the scan's exit code carries the gate
    semantic to CI without callers parsing JSON.
- Added a reusable GitHub composite action at
  `.github/actions/scan/action.yml` that wraps the scanner (optional
  http-server, scan, artifact upload). Consumer repos that previously
  hand-rolled `pa11y-ci` now collapse to a few lines invoking this
  action.

## v2.0.1 -- 2026-05-31

- Hardened `scan.js` dependency installation by validating browser
  selection before dependency lookup and invoking `npm install` with argv
  rather than shell interpolation.
- Added bounded discovery fetches, redirect limits, same-origin discovery
  defaults, explicit cross-origin sitemap opt-in, and origin disclosure in
  discovery/report output.
- Escaped target-derived Markdown fields in generated audit reports and
  issue plans to reduce agent-facing instruction injection and table
  breakage from untrusted scan data.
- Documented the repository release, bundle inventory, and assistant
  guide version model.

## Assistant guide v0.3.0 -- 2026-05-24

- Added Level 4 provenance metadata for the GuideCheck
  `assistant-guide.txt` artifact, including a text sidecar manifest URL.
- Prepared the public repository copy at `/assistant-guide.txt` as the
  cross-channel hash anchor for the published guide.
- Tightened action block metadata to satisfy the GuideCheck hosted
  verifier's guide-file checks.

## v16 -- 2026-05-19

- Added `evals/run-evals.js`, a deterministic offline eval runner that
  validates discovery fixtures, issue planning, quick-scan behavior,
  skipped-Lighthouse report contracts, page-aware deltas, dependency
  policy documentation, syntax checks, JSON parsing, YAML parsing, and
  context bootstrap smoke behavior.
- Added fixture coverage for `eval-3` quick-scan behavior and `eval-4`
  skipped-Lighthouse report contract behavior.
- Updated `package.json`, `.github/workflows/validate-skill.yml`, and
  `CONTRIBUTING.md` so `npm run validate` is the single local and CI
  validation entrypoint.
- Updated `SKILL.md` to make the dependency auto-install consent
  boundary explicit before agents invoke `scan.js` in workspaces without
  existing scan dependencies.
- Updated `evals/evals.json` so the human acceptance ledger records the
  deterministic eval-3 fixture and the new eval-4 contract fixture.

## v15 -- 2026-04-23

- Expanded `scripts/plan-issues.js` so the dry-run path now reads
  project context, applies configured severity thresholds, adds priority
  and WCAG labels, records additional standards, and marks duplicates
  from a supplied existing-key index.
- Added runnable fixture coverage for `eval-2`, covering the strongest
  local mitigation path for issue mode short of authenticated live
  tracker writes.
- Updated `references/issue-trackers.md` so the documented safe dry-run
  path matches the richer helper behavior.

## v14 -- 2026-04-23

- Added `evals/run-discover-fixture.js`, a reusable mocked-network
  fixture runner for `discover.js`.
- Added runnable fixture assets for `eval-9` (cross-origin sitemap
  preservation) and `eval-10` (deterministic discovery sampling).
- Validated both discovery fixtures locally so the two discovery-related
  regressions now have in-repo reproduction paths, not just notes in
  `evals/evals.json`.

## v13 -- 2026-04-23

- Discovery now preserves published sitemap URLs instead of rewriting
  them onto the runtime origin. This includes `robots.txt` sitemap
  entries, sitemap indexes, nested sitemap URLs, and redirect targets.
- Discovery sampling is now deterministic. Candidate selection uses
  stable spread indexes and fingerprint ranking now breaks ties by URL,
  eliminating noisy CI diffs across repeated runs.
- `discover.js` is importable without changing CLI behavior, which makes
  mocked-network regression validation possible inside the repo.
- `report.js` delta comparison is now page-aware. A rule that moves
  between pages or template groups with the same instance count is
  reported as changed rather than unchanged.
- Added and validated eval coverage for the resolved issues:
  `eval-9` (cross-origin sitemap preservation), `eval-10`
  (deterministic discovery), and `eval-11` (page-aware delta changes).

## v12 -- 2026-03-26

- **Self-contained dependencies:** scan.js now resolves axe-core and
  puppeteer from skill-local `deps/` → project → global → auto-install.
  The skill works against any project without requiring accessibility
  tooling to be pre-installed.
- **Quick Fixes:** report.js includes actionable one-liner remediation
  hints for ~17 common axe rules, sorted by impact severity.
- **Delta comparison:** `report.js --previous <prior-audit.json>` shows
  fixed rules (strikethrough), new rules, changed instance counts with
  direction arrows, and net totals.
- **Null-label fix:** API enrichment labels no longer show "null" when
  the API manifest lacks count data for an entity type.

## v11 -- 2026-03-26

- **discover.js:** Template-aware page discovery with sitemap-first
  approach. Falls back to HTML navigation crawl if no sitemap exists.
- **DOM fingerprinting:** Loads candidate pages and scores structural
  complexity (tables, details, forms, interactive attrs). Picks the
  most and least complex pages per group instead of alphabetic spread.
- **API entity enrichment:** Reads `/api/v1/index.json` (or similar)
  and annotates groups with entity names/counts (e.g., "25 regulations").
- **Shared template detection:** report.js cross-references per-page
  violation fingerprints with discover groups. Surfaces which template
  groups share identical issues so developers fix the shared template once.
- **No-sitemap fallback validated:** HTML crawl (depth 2) found 132
  pages and all key template groups on AI Regulation Reference.
- **Validated on AI Regulation Reference:** 746 pages → 16 groups →
  22 scanned → 12 serious violations found on templates the previous
  top-level-only scan missed entirely.

## v10 -- 2026-03-26

- **report.js:** New deterministic report generator (`scripts/report.js`)
  handles Phases 3 and 5: WCAG compliance matrix (hardcoded 50 criteria),
  violation aggregation across pages, color-contrast detail extraction,
  markdown report per output-contract.md, and JSON per output-schema.json.
  The LLM no longer builds these manually (~3000 tokens saved).
- **scan.js --summary:** Added `--summary` flag to `scripts/scan.js` that
  keeps full violation detail but strips node data from passes and
  inapplicable arrays, reducing output size (~500 tokens saved).
- **Phase 1 condensed:** Replaced ~30-line framework-by-framework
  enumeration with ~10 focused lines. The agent already knows how to
  discover project structure (~500 tokens saved).
- **Reference reads removed:** Phase 5 now invokes report.js directly.
  The agent no longer reads output-contract.md or output-schema.json
  during normal runs (~800 tokens saved).
- **Phase 4 stays LLM-generated:** Manual check guidance requires
  reasoning about the specific findings pattern and remains the agent's
  responsibility.

## v9 -- 2026-03-03

- **First-run context validation:** Recorded a passing result for eval-6
  by creating a workspace-local context file in `/tmp` with the bundled
  bootstrap helper.
- **Missing-browser-automation validation:** Recorded a passing result
  for eval-7 by exercising the scanner against a workspace with
  `axe-core` present but no Puppeteer dependency, confirming a clear
  blocker message.
- **Issue planning mitigation:** Added `scripts/plan-issues.js` and a
  sample issue plan artifact so `markdown+issues` mode has a safe dry-run
  path before live tracker writes.
- **Validation stance:** Reduced the remaining publish-time runtime gap
  to the live authenticated tracker path rather than the whole issue-mode
  workflow.

## v8 -- 2026-03-03

- **Direct degraded-path validation:** Ran the bundled `scripts/scan.js`
  helper against PAICE2 and recorded passing results for eval-4
  (Lighthouse unavailable but report still generated) and eval-5
  (expected URL wrong but runtime URL reconciled and persisted).
- **Eval results updated:** Added concrete `results` entries for eval-4
  and eval-5 in `evals/evals.json`.
- **CI discoverability:** Updated `SKILL.md` so the GitHub Actions
  starter in `assets/ci/github-actions/accessibility-audit.yml` is part
  of the visible operating guidance rather than a hidden asset.
- **Execution stance:** Kept the bundled scanner Puppeteer-first for
  now. Playwright remains a documented fallback path but is not yet a
  first-class helper implementation.

## v7 -- 2026-03-03

- **Reusable scripts:** Added `scripts/scan.js` for reusable axe-based
  scanning and `scripts/bootstrap-context.js` for first-run workspace
  context creation.
- **Reference decomposition:** Split detailed output rules into
  `references/output-contract.md`, issue creation rules into
  `references/issue-trackers.md`, and the JSON contract into
  `references/output-schema.json`.
- **Eval expansion:** Added explicit eval coverage for missing
  Lighthouse, runtime URL reconciliation, first-run context creation,
  missing browser automation, and issue deduplication.
- **Operational assets:** Added sample markdown/JSON output artifacts and
  a GitHub Actions workflow template for scheduled or on-demand audits.
- **Core skill cleanup:** Updated `SKILL.md` to prefer bundled helpers
  and focused references over repeated inline detail.

## v6 -- 2026-03-03

- **Runtime URL handling:** Updated `SKILL.md` so a local port mismatch
  is treated as a normal adaptation path. The skill now switches to the
  live URL, records the mismatch in methodology, and updates the
  workspace-local `base_url`.
- **Lighthouse degraded mode:** Clarified that missing or failing
  Lighthouse is a documented partial-audit path, not a failure. The
  report must now state the skip reason explicitly in the executive
  summary and methodology.
- **Eval alignment:** Updated `evals/evals.json` so eval-1 allows URL
  reconciliation and Lighthouse-optional execution instead of assuming a
  fixed port and guaranteed Lighthouse score.
- **Handoff update:** Recorded the Codex eval-1 findings from PAICE2 so
  the next session starts from observed runtime behavior rather than
  inferred gaps.

## v5 -- 2026-03-03

- **Configuration contract:** Added
  `references/project-context-template.md` as the canonical schema for
  `.a11y-audit/PROJECT_CONTEXT.md`.
- **Examples:** Included one minimal example and one
  `markdown+issues` example to reduce ambiguity around route lists,
  standards, output paths, and issue-tracker settings.
- **Core skill cleanup:** Updated `SKILL.md` to point to the template as
  the field contract and removed the inline issue-tracker config block.

## v4 -- 2026-03-03

- **Portable core:** Removed the `metadata` block from `SKILL.md` so the
  main skill file uses minimal frontmatter and remains Codex-compatible.
- **Platform branches:** Added `references/claude-code.md` and
  `references/codex.md` so Claude-specific guidance stays explicit
  without leaking into the shared operating path.
- **Workspace state:** Moved mutable project context out of the skill
  install directory. The default path is now
  `.a11y-audit/PROJECT_CONTEXT.md` in the audited workspace.
- **Bundle sync:** Updated `HANDOFF.md`, `evals/evals.json`, and the
  manifest to match the portable layout. Added `agents/openai.yaml` for
  Codex skill-list metadata.

## v3 -- 2026-03-03

- **Output modes:** Replaced hardcoded GitHub Issue creation with three
  configurable output modes: `markdown` (report only), `markdown+json`
  (report + machine-readable JSON), `markdown+issues` (report + issue
  tracker tickets). Mode is stored in PROJECT_CONTEXT.md and persisted
  across runs.
- **Self-configuring:** On first run, if no output_mode is set, the skill
  asks the user to choose and persists the preference. Subsequent runs
  use the saved preference without asking.
- **JSON schema:** Defined structured JSON output format for CI
  integration, dashboards, and trend tracking.
- **Tracker-agnostic:** Issue tracker configuration (GitHub, GitLab,
  Linear, Jira) moved to PROJECT_CONTEXT.md alongside the output mode.
  The skill no longer assumes any specific tracker.
- **Phase rename:** Phase 5 renamed from "Report Generation" to "Output
  Generation". Phase 6 renamed from "Issue Creation (Opt-In)" to "Issue
  Creation (conditional)"; runs only in markdown+issues mode.
- `gh` CLI removed as a top-level dependency; now conditional on
  markdown+issues mode with GitHub tracker selection.

## v2 -- 2026-03-03

- **Token efficiency:** Removed static WCAG 2.1 criteria enumeration
  (57 lines); model generates matrix from its own knowledge. Removed
  hardcoded "no axe coverage" list (15 lines); coverage determined at
  runtime from axe results. Condensed report template from full markdown
  mock (115 lines) to structural spec (30 lines). Condensed issue
  template from full mock (30 lines) to field list (10 lines). Net
  reduction: 632 to 441 lines (~30%).
- **Portability:** Renamed context file from PAICE_CONTEXT.md to
  PROJECT_CONTEXT.md. Added Playwright as alternative to Puppeteer.
  Added multi-tracker support in Phase 6 (GitLab, Linear, Jira).
- **Usefulness:** Added delta/comparison section in report for repeat
  audits (diff new vs. resolved violations). Made Phase 4 manual
  checklists dynamic based on Phase 2 automated findings rather than
  static.
- Validated via eval-1 against PAICE2 (3 pages, Lighthouse 93, 76
  violations, 5 unique rules, report generated successfully).

## v1 -- 2026-03-02

- Bootstrap under skill-provenance system. All files versioned, manifest
  and changelog created.
- SKILL.md v1: Six-phase accessibility audit pipeline
  - Phase 1: Environment Discovery (tech stack, routes, existing tooling)
  - Phase 2: Automated Scanning (axe-core via Puppeteer, Lighthouse CLI)
  - Phase 3: Compliance Mapping (WCAG 2.1 AA matrix, project-specific standards)
  - Phase 4: Manual Check Guidance (checklists by testing method)
  - Phase 5: Report Generation (structured markdown with tables)
  - Phase 6: Issue Creation (opt-in, deduplication via HTML comments)
- WCAG 2.1 AA criteria reference embedded (50 Level A and AA criteria)
- axe-core scanning script template with ES module support
- GitHub Issue template with deduplication key pattern
- evals/evals.json: 3 eval cases defined, pending first run
- HANDOFF.md: Bootstrap context with known limitations
