---
name: a11y-audit
description: >
  Run accessibility audits on web projects combining automated scanning
  (axe-core, Lighthouse) with WCAG 2.1 AA compliance mapping, manual check
  guidance, and structured reporting. Output is configurable: markdown
  report only, markdown plus machine-readable JSON, or markdown plus issue
  tracker integration. Use this skill whenever the user mentions
  "accessibility audit", "a11y audit", "WCAG audit", "accessibility check",
  "compliance scan", or asks to check a web project for accessibility
  issues. Also trigger when the user wants to verify WCAG conformance or
  map findings to a specific standard (CAN-ASC-6.2, EN 301 549, ADA/AODA).
metadata:
  skill_bundle: a11y-audit
  file_role: skill
  version: 14
  version_date: 2026-05-31
  previous_version: 13
  change_summary: >
    Documented same-origin discovery defaults, cross-origin sitemap
    opt-in, and fixed Puppeteer-only scanner dependency behavior.
---

# Accessibility Audit

## Architecture

This skill operates as a single layer. It reads the project environment,
runs automated accessibility tools, maps findings to compliance standards,
and produces output in a configurable format. No external skill dependency
is required.

Store project-specific audit state in the target workspace, not in the
installed skill directory. Default path:
`.a11y-audit/PROJECT_CONTEXT.md` at the workspace root. When that file
exists, use it for project-specific configuration: output mode,
additional compliance standards, issue tracker settings, route lists,
color palettes, and cross-references to existing documentation. When
absent, use WCAG 2.1 AA as the sole standard, `markdown` as the output
mode, and generic defaults for everything else.

Use `references/project-context-template.md` as the canonical schema for
that file, including minimal and `markdown+issues` examples.

Prefer bundled helpers over ad hoc generation when they fit:

- `scripts/bootstrap-context.js` creates a workspace-local
  `.a11y-audit/PROJECT_CONTEXT.md` from simple inputs.
- `scripts/scan.js` runs reusable axe-based scans and records optional
  Lighthouse execution intent. Use `--summary` to reduce output size
  (keeps full violation detail, strips node data from passes/inapplicable).
- `scripts/report.js` generates the markdown report and JSON data file
  from scan.js output. Handles WCAG compliance matrix, violation
  aggregation, and color-contrast detail extraction deterministically.
- `scripts/discover.js` identifies template groups on large sites and
  selects representative pages for scanning. Reads sitemap.xml first,
  falls back to HTML navigation crawl. Outputs a scan plan with
  template groups and a ready-to-use URL list for scan.js. Discovery is
  same-origin by default; use `--allow-cross-origin-sitemaps` only after
  the user approves sitemap-declared cross-origin targets.

### Dependencies

scan.js requires `axe-core` and `puppeteer`. It resolves these in order:

1. **Skill-local** `deps/` directory (sibling to `scripts/`)
2. **Target project** `node_modules/` (and common workspace subdirs)
3. **Global** npm modules

If not found anywhere, scan.js **auto-installs** both packages to the
skill-local `deps/` directory. This means the skill works against any
project without requiring the target to have accessibility tooling
installed. The `deps/` directory is gitignored.

Because `scan.js` may auto-install missing dependencies, agents should
ask before invoking scan.js when the target workspace does not already
provide `axe-core` and the chosen browser automation package.

The bundled scanner supports Puppeteer only. Treat `--browser` as a
fixed option, not a user-controlled package installer.

### Platform-Specific References

- If running in Claude Code, read `references/claude-code.md` for
  `.claude/launch.json` handling and Preview tool usage.
- If running in Codex, read `references/codex.md` for workspace-local
  state handling and execution assumptions.
- `references/output-contract.md` and `references/output-schema.json`
  are encoded in `scripts/report.js`. Read them only when modifying the
  report script.
- Read `references/issue-trackers.md` only when `output_mode` is
  `markdown+issues`.
- If the user wants to operationalize recurring audits in CI, start from
  `assets/ci/github-actions/accessibility-audit.yml`.
- Prefer `scripts/plan-issues.js` before live ticket creation when you
  need a safe review and deduplication pass.

**The skill does not modify source code.** It is an auditor, not a fixer.
Findings are reported with remediation guidance; the user decides what to
act on.

### Output Modes

The skill supports three output modes, configured via the `output_mode`
field in `.a11y-audit/PROJECT_CONTEXT.md`:

| Mode | Output | Use Case |
|------|--------|----------|
| `markdown` | Markdown report only | Human review, documentation |
| `markdown+json` | Markdown report + JSON data file | CI integration, dashboards, trend tracking |
| `markdown+issues` | Markdown report + issue tracker tickets | Active remediation workflow |

On first run, if no `output_mode` is set in
`.a11y-audit/PROJECT_CONTEXT.md`, ask the user which mode they prefer
and persist their choice by appending an `## Output Configuration`
section to that file. If no context file exists, create it at the
default path following `references/project-context-template.md`. Prefer
`scripts/bootstrap-context.js` for first-run context creation when a
simple generated file is sufficient.

The `markdown+json` mode writes a companion file alongside the report:
`audit-YYYY-MM-DD.json` containing the raw axe-core results, Lighthouse
scores, and the compliance matrix as structured data. This file is
machine-readable and can be consumed by CI pipelines, dashboards, or
trend-tracking tools.

The `markdown+issues` mode requires additional configuration in the
context file (see Phase 6).

---

## Pipeline

An accessibility audit moves through six phases. Each phase produces data
the next phase consumes. Phases 1-4 always run. Phase 5 produces output
based on the configured output mode. Phase 6 runs only in
`markdown+issues` mode and requires explicit user confirmation.

The user can request a partial run. Common patterns:
- "Quick scan": Phases 1-2 only, results summarized in conversation
- "Full audit": Phases 1-5, output per configured mode
- "Audit with issues": Phases 1-6, report plus tracker tickets

### Phase 1 -- Environment Discovery

**Purpose:** Understand the project before scanning.

1. Read `.a11y-audit/PROJECT_CONTEXT.md` if it exists (standards, routes,
   output mode, labels). If absent, create it via
   `scripts/bootstrap-context.js` or from
   `references/project-context-template.md`.
2. Read `package.json` for tech stack, existing a11y tooling, and
   available browser automation (`puppeteer` / `playwright`).
3. Build a scannable URL list from router config or HTML file glob.
   For sites with many pages (>15 routes), prefer `scripts/discover.js`
   to classify pages into template groups and select representatives.
   Review the scan plan with the user before proceeding to Phase 2.
4. Confirm a dev server is reachable. Check `.claude/launch.json` and
   platform-specific references for launch hints. If the app starts on a
   different URL than expected, switch to the live URL, record the
   mismatch, and update the context file.
5. Ask before installing any missing dependencies.

**Output:** Structured summary reported to the user before proceeding.

### Phase 2 -- Automated Scanning

**Purpose:** Run automated accessibility checks against live pages.

**Prerequisite:** A running dev server (or production URL provided by
the user).

#### axe-core Scanning

Prefer the bundled `scripts/scan.js` before writing a throwaway scan
script. Use an ad hoc script only when the workspace needs behavior that
the bundled script does not yet support.

The reusable scanner should:

1. Imports `puppeteer` and `axe-core`
2. Launches a headless browser
3. For each target URL:
   a. Navigates to the page
   b. Waits for network idle (`waitUntil: 'networkidle0'`)
   c. Injects axe-core: reads the axe-core source file from
      `node_modules/axe-core/axe.min.js` and injects it via
      `page.evaluate()`
   d. Runs the audit: `page.evaluate(() => axe.run())`
   e. Collects the results JSON
4. Closes the browser
5. Writes raw results to JSON

Example invocation:

```bash
node a11y-audit/scripts/scan.js \
  --root . \
  --urls http://127.0.0.1:3000/,http://127.0.0.1:3000/about \
  --output /tmp/a11y-scan.json \
  --summary
```

**Adapt to the project.** If dependencies live in a frontend
subdirectory, point `--root` at the workspace root; the bundled script
already checks common frontend paths. If that still fails, fall back to
an ad hoc script or run from the frontend directory directly.

**Common mistake:** Do not use `require()` in an ES module project. Check
`package.json` for `"type": "module"`. If present, use `import` syntax
and the `__dirname` workaround in any ad hoc script. If absent,
`require()` is fine.

**Playwright alternative:** If the project uses Playwright instead of
Puppeteer, adapt the script: replace `puppeteer.launch()` with
`chromium.launch()`, use `page.goto()` the same way, and inject
axe-core via `page.evaluate()`. The axe-core injection pattern is
identical. Use whichever browser automation library the project already
has installed.

#### Lighthouse Scanning

Run Lighthouse CLI against each target URL:

```bash
npx lighthouse <url> \
  --output=json \
  --output-path=stdout \
  --only-categories=accessibility \
  --chrome-flags="--headless --no-sandbox" \
  --quiet
```

Parse the JSON output. Extract:
- `categories.accessibility.score` (0-1, multiply by 100)
- `audits` where `score !== 1` (failed or partial audits)
- Each audit's `description` and `details.items`

If Lighthouse is unavailable or fails (common in CI environments), skip
it and note the gap in the report. In the executive summary and
methodology, explicitly say whether Lighthouse was skipped because the
CLI was missing, Chrome launch failed, or another runtime error
occurred. axe-core results alone are sufficient for a valid audit.

#### Scope Control

- Default: scan routes discovered in Phase 1
- If a discover.js scan plan exists, use its `scanList` for `--urls`.
  The report methodology will record the sampling strategy.
- If more than 10 routes exist and no discover plan is available, ask
  the user which to scan or whether to scan all
- The user can provide a specific URL list to override discovery
- For SPAs: navigate via the router, not by reloading the page (some
  routes may not work as direct URLs)

#### Result Structure

For each page, collect:
- `url`: the scanned URL
- `violations`: array of axe violations, each with `id`, `impact`
  (critical/serious/moderate/minor), `description`, `help`, `helpUrl`,
  `tags` (WCAG criteria), `nodes` (affected elements with selectors)
- `passes`: count of passing rules
- `incomplete`: rules that could not be fully evaluated
- `lighthouseScore`: 0-100 (if available)
- `lighthouseAudits`: failed audit details (if available)

### Phase 3 -- Compliance Mapping

**Purpose:** Map automated findings to WCAG 2.1 AA success criteria and
any project-specific standards.

`scripts/report.js` handles the compliance matrix deterministically. It
hardcodes all 50 WCAG 2.1 Level A and AA criteria, maps axe tags to
success criteria, and produces the matrix as part of its markdown and
JSON output. You do not need to build the matrix manually.

If `.a11y-audit/PROJECT_CONTEXT.md` specifies additional standards
(e.g., CAN-ASC-6.2), build a secondary mapping. Cross-reference
automated findings where the standard maps to WCAG criteria. For
requirements that go beyond WCAG (equity, organizational processes,
transparency), note them as manual review items referencing the
project's existing conformance documentation.

### Phase 4 -- Manual Check Guidance

**Purpose:** Generate targeted checklists for what automation cannot
verify, prioritized by the automated findings.

For each WCAG criterion marked "Manual" in the Phase 3 matrix, generate
a testing item. Organize by testing method: Keyboard Navigation, Screen
Reader, Visual Inspection, Cognitive, and Timing/Motion.

**Dynamic prioritization:** Do not produce a static checklist. Use the
Phase 2 results to focus manual effort:

- If axe found color-contrast violations, prioritize visual inspection
  items (SC 1.4.1, 1.4.11, 1.4.10, 1.4.12, 1.4.13)
- If axe found ARIA or landmark violations, prioritize screen reader
  items (SC 1.3.1, 4.1.3, 3.3.1, 3.3.2)
- If axe found heading or structure violations, prioritize keyboard
  navigation items (SC 2.4.3, 2.4.7, 2.1.1)
- If no form-related violations were found, deprioritize form testing
  (SC 3.3.3, 3.3.4) with a note that automated checks passed
- Always include timing items (SC 2.2.1, 2.2.2, 2.3.1) since these
  cannot be automated at all

Each checklist item specifies: the WCAG criterion, what to test, how
to test it, and which pages to focus on (pages where automated issues
were found get priority).

If `.a11y-audit/PROJECT_CONTEXT.md` references an existing testing guide,
cross-link to it rather than duplicating procedures.

### Phase 5 -- Output Generation

**Purpose:** Produce output based on the configured output mode.

Run `scripts/report.js` to generate the markdown report and JSON data
file from the Phase 2 scan output:

```bash
node a11y-audit/scripts/report.js \
  --input /tmp/a11y-scan.json \
  --output-dir docs/accessibility/audits \
  --project-name "Project Name" \
  --runtime-url http://127.0.0.1:3000 \
  --expected-url http://localhost:3000 \
  --discover /tmp/a11y-discover.json
```

Pass `--discover` when a discover.js scan plan was used. This adds a
Sampling Strategy subsection to the report methodology documenting
template groups and coverage ratio.

Pass `--previous <prior-audit.json>` to generate a Delta from Previous
Audit section showing fixed rules, new rules, changed instance counts,
and net progress.

The script produces `audit-YYYY-MM-DD.md` and `audit-YYYY-MM-DD.json`
following the contracts in `references/output-contract.md` and
`references/output-schema.json`. You do not need to read those reference
files unless modifying the report script itself.

After running report.js, review its output and fill in the **Manual
Testing Recommendations** section with the Phase 4 guidance (report.js
leaves a placeholder for this since it requires reasoning about the
specific findings pattern).

`.a11y-audit/PROJECT_CONTEXT.md` can override the output path.

If the user wants a recurring or on-demand CI job, adapt
`assets/ci/github-actions/accessibility-audit.yml` to the target
workspace instead of inventing a workflow from scratch.

### Phase 6 -- Issue Creation (conditional)

**Purpose:** Create issue tracker tickets for findings. Runs only when
the output mode is `markdown+issues`.

**This phase requires explicit user confirmation.** Before creating any
tickets, show the user how many will be created, at what priority levels,
and ask for approval.

Read `references/issue-trackers.md` for tracker configuration,
deduplication, priority mapping, and ticket structure. Use the tracker
settings from `.a11y-audit/PROJECT_CONTEXT.md`.

---

## Verification

After completing an audit, verify these quality checks:

1. **axe results valid**: Compare violation count against a manual
   axe DevTools browser extension run on the same page. Counts should
   match within tolerance (axe versions may differ slightly).

2. **Lighthouse score consistent**: Compare against a manual Chrome
   DevTools Lighthouse run when Lighthouse was actually executed. Should
   be within 5 points.

3. **WCAG matrix complete**: All 50 AA criteria appear in the compliance
   matrix. No criterion is missing.

   Treat the matrix as evidence-oriented status reporting. Do not frame
   it as proof of full conformance, because many WCAG criteria remain
   manual even in a strong automated run.

4. **Report structure**: All required sections present. Tables render
   correctly in a markdown viewer.

5. **JSON validity** (`markdown+json` mode): JSON file parses without
   error. Violation counts match the markdown report.

6. **Issue deduplication** (`markdown+issues` mode): Run the skill
   twice. The second run should create zero duplicate tickets.

7. **Output mode persistence**: After first run, verify the output mode
   is saved to `.a11y-audit/PROJECT_CONTEXT.md` and used automatically
   on next run.

8. **Runtime URL reconciliation**: If the app started on a different
   local URL than expected, verify the report records the mismatch and
   the context file reflects the actual working `base_url`.

---

## What This Skill Does NOT Do

- **Visual regression testing**: does not compare screenshots between
  runs. Use Percy, Chromatic, or BackstopJS for that.
- **PDF accessibility**: does not audit PDF documents for tagged
  structure, reading order, or alternative text.
- **Real device/AT testing**: runs in headless Chromium only. Cannot
  test on real iOS/Android or with real screen readers. Phase 4
  generates manual checklists for this.
- **Code fixes**: reports findings but does not modify source code.
- **VPAT generation**: does not produce Voluntary Product Accessibility
  Templates (specific legal format).
- **Continuous monitoring**: runs on demand, not as a CI pipeline.
  The `markdown+json` output mode provides structured data for building
  CI integrations, but the skill itself does not run in CI.
- **Third-party auditing**: only audits the project's own frontend,
  not embedded third-party services.
