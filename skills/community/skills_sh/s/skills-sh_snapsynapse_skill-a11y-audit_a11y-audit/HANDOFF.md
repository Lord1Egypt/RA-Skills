---
skill_bundle: a11y-audit
file_role: handoff
version: 14
version_date: 2026-05-19
previous_version: 13
change_summary: >
  Recorded executable offline eval validation and the npm run validate
  CI entrypoint.
---

# Accessibility Audit Skill -- Handoff Document

## What This Is

A portable accessibility-audit skill bundle for Claude Code and Codex.
The core workflow lives in `SKILL.md`; platform-specific notes live in
`references/claude-code.md` and `references/codex.md`.

## Current State: v16, self-contained and executable-eval validated

The workflow has been run successfully in Claude Code for eval-1. Codex
eval-1 has been exercised against PAICE2. The bundle now includes
reusable scripts, focused reference files, expanded eval coverage,
sample output artifacts, and a CI template. The direct degraded paths
for Lighthouse-unavailable, runtime URL reconciliation, first-run
context creation, and missing-browser-automation handling have been
validated. The repo now has a deterministic offline eval runner wired to
`npm run validate`, which is also the GitHub Actions validation command.

The three most recent correctness issues are now resolved:

- `discover.js` preserves published sitemap URLs across `robots.txt`,
  sitemap indexes, nested sitemap files, and redirects instead of
  rewriting them onto the runtime origin.
- Representative page selection is deterministic across repeated runs.
- `report.js` delta comparison is page-aware and reports rule movement
  even when total instance counts stay flat.

Those fixes now have runnable local regression fixtures:

- `eval-2` covers context-aware issue planning, standards carry-through,
  configured labels, thresholding, and duplicate skipping in dry-run mode
- `eval-3` covers quick-scan summary behavior without report generation
- `eval-4` covers skipped-Lighthouse markdown and JSON report contracts
- `eval-9` covers cross-origin sitemap preservation
- `eval-10` covers deterministic discovery across repeated runs
- `eval-11` covers page-aware delta reporting

A full audit was run 2026-03-26 against the AI Regulation Reference
(10-page static HTML site, http://127.0.0.1:8081). The audit found
3 rules / 69 instances (color-contrast, landmark-one-main, region),
all of which were remediated to zero violations. This run revealed
four token-efficiency improvements, all now implemented in v10.

### Files in this directory

| File | Purpose |
|------|---------|
| SKILL.md | Portable six-phase audit pipeline (main skill) |
| MANIFEST.yaml | Bundle metadata, dependencies, file inventory |
| CHANGELOG.md | Append-only change history |
| HANDOFF.md | This file -- current state and next steps |
| evals/evals.json | 11 eval cases with passing results recorded for eval-1 through eval-11 where deterministic or prior runtime validation exists |
| evals/run-evals.js | Offline executable eval and validation runner |
| references/claude-code.md | Claude-specific launch and Preview notes |
| references/codex.md | Codex-specific execution notes |
| references/output-contract.md | Markdown/JSON output rules |
| references/issue-trackers.md | Issue creation and deduplication rules |
| references/output-schema.json | Stable JSON output schema |
| references/project-context-template.md | Canonical context-file contract |
| scripts/scan.js | Reusable axe-based scanning helper (--summary flag) |
| scripts/bootstrap-context.js | First-run context bootstrap helper |
| scripts/discover.js | Template-aware page discovery and sampling |
| scripts/report.js | Deterministic report generator for Phases 3+5 |
| scripts/plan-issues.js | Non-destructive issue planning helper |
| assets/sample-output/ | Sample markdown and JSON artifacts |
| assets/ci/github-actions/accessibility-audit.yml | CI workflow starter |
| agents/openai.yaml | Codex UI metadata |

## Where to Put the Skill

- **Upstream (generic):** `/Users/snap/Git/skill-a11y-audit/`
- **Claude install:** `.claude/skills/a11y-audit/` in the target project
- **Codex install:** `$CODEX_HOME/skills/a11y-audit/` or equivalent skill import path
- **Project-specific mutable state:** `.a11y-audit/PROJECT_CONTEXT.md` in the target workspace

## Dependencies

| Dependency | Required? | Check |
|------------|-----------|-------|
| `axe-core` (npm) | Yes | `ls node_modules/axe-core` |
| `puppeteer` or `playwright` (npm) | Yes | `ls node_modules/puppeteer` or `ls node_modules/playwright` |
| `lighthouse` (npm/CLI) | Recommended | `npx lighthouse --version` |
| issue tracker CLI | Phase 6 only | `gh --version`, `glab --version`, or tracker equivalent |

## Known Limitations

1. **No real AT testing.** The skill runs headless Chromium only. Screen
   reader, voice control, and mobile AT testing require manual procedures.
   Phase 4 generates checklists for this.

2. **SPA navigation.** For single-page applications, the scanning script
   navigates via direct URL. Pages that require client-side routing state
   (e.g., post-login pages, multi-step flows) may not render correctly in
   headless mode. The user may need to provide authenticated session
   cookies or skip those routes.

3. **axe-core version coupling.** Results depend on the installed
   axe-core version. Different versions may report different violations.
   The report records the version used.

4. **Lighthouse variance.** Lighthouse scores vary between runs due to
   rendering timing. The skill runs once per page and reports the result;
   it does not average multiple runs.

5. **Lighthouse optionality is real.** Some projects will have
   `axe-core` and browser automation installed but no runnable
   Lighthouse CLI. The skill now treats this as a normal degraded mode
   and requires the report to state the skip reason explicitly.

6. **No CI integration.** The skill runs on demand via an interactive agent. A
   separate GitHub Actions workflow would be needed for continuous
   accessibility monitoring.

7. **Label creation.** Phase 6 assumes GitHub labels already exist. It
   does not create labels. If a label does not exist, `gh issue create`
   will create it automatically, but the label will lack a description
   and color.

8. **Expected URL drift.** Local dev servers may bind to a different
   port than the prompt or context file expects. The skill now updates
   the workspace-local context to the working URL and records the
   mismatch in the report methodology.

9. **Puppeteer-first scanner.** The bundled scanner currently supports
   Puppeteer directly. Playwright remains a documented fallback path in
   the skill, but the helper script has not been expanded to first-class
   Playwright support yet.

10. **Live issue tracker path still pending.** The skill now has
   explicit issue-tracker reference guidance, a non-destructive issue
   planner, and deduplication keys, but the end-to-end authenticated
   ticket creation path has not yet been re-run after the refactor.

## Completed: Token-Efficiency Improvements (v10)

All four improvements from the 2026-03-26 audit are now implemented:

1. **`scripts/report.js`** (~3000 tokens saved): Deterministic report
   generator with hardcoded 50 WCAG 2.1 AA criteria, axe tag mapping,
   violation aggregation, color-contrast detail extraction, and output
   generation per output-contract.md and output-schema.json.
2. **`--summary` flag on scan.js** (~500 tokens saved): Strips node
   detail from passes/inapplicable arrays, adds per-page counts.
3. **Phase 1 condensed** (~500 tokens saved): Replaced ~30-line
   enumeration with ~10 focused lines.
4. **Reference reads removed** (~800 tokens saved): Phase 5 invokes
   report.js directly; agent no longer reads output-contract.md or
   output-schema.json during normal runs.

## Suggested Next Steps

1. Run eval-2 against a real authenticated tracker for full live issue-mode validation
2. Keep `scripts/scan.js` Puppeteer-first unless a Playwright-native project forces expansion
3. Use `scripts/plan-issues.js` as the default dry-run step before any live ticket creation
4. Copy updated skill back to `.claude/skills/a11y-audit/` in target projects
5. Keep new regression fixes covered by `npm run validate` before updating bundle metadata
