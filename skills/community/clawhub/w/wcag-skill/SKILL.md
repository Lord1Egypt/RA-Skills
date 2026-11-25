---
name: wcag-skill
description: "Build, audit, and repair web content against WCAG 2.2. Use when: (1) creating accessible HTML/CSS/JS, (2) remediating accessibility defects, (3) running reproducible automated audits, (4) preparing WCAG 2.2 AAA evidence and human-test records, or (5) running the optional AI-WCAG-Gauntlet benchmark. For benchmarks, require an unscored preflight of tag coverage, W3C, axe, Pa11y, and QualWeb before the first scored run."
allowed-tools: Bash, Read, Write, Edit, Env
metadata:
  version: 2.0.36
  openclaw:
    requires:
      bins:
        - node
        - npm
        - python3
        - curl
        - java
    envVars:
      - name: AXE_CHROME_PATH
        required: false
        description: Explicit Chrome/Chromium binary path for scripts/a11y-audit.sh when auto-detection fails.
      - name: AXE_CHROMEDRIVER_PATH
        required: false
        description: Explicit Chromedriver binary path for scripts/a11y-audit.sh when auto-detection fails.
      - name: AXE_CHROME_EXTRA_ARGS
        required: false
        description: Space-separated Chrome flags for scripts/a11y-audit.sh. Set to an empty string to keep the Chrome sandbox enabled when CI=true.
      - name: CI
        required: false
        description: When "true" and AXE_CHROME_EXTRA_ARGS is unset, scripts/a11y-audit.sh disables the Chrome sandbox for hosted CI runners.
      - name: NODE_OPTIONS
        required: false
        description: Read and extended by scripts/a11y-audit-limited.sh with a Node heap limit.
      - name: ULIMIT_PERCENT
        required: false
        description: Percentage of available memory used for ulimit -v by scripts/a11y-audit-limited.sh (default 90).
      - name: ULIMIT_MIN_MB
        required: false
        description: Minimum ulimit -v value in MB for scripts/a11y-audit-limited.sh (default 1536).
      - name: NODE_PERCENT
        required: false
        description: Percentage of available memory used for the Node heap by scripts/a11y-audit-limited.sh (default 30).
      - name: NODE_MIN_MB
        required: false
        description: Minimum Node heap in MB for scripts/a11y-audit-limited.sh (default 256).
      - name: WCAG_TEST_URL
        required: false
        description: Page URL for templates/playwright-state.spec.ts (default http://127.0.0.1:8000/).
    install:
      - kind: node
        package: "@axe-core/cli"
        bins: [axe]
      - kind: node
        package: pa11y
        bins: [pa11y]
      - kind: node
        package: "@qualweb/cli"
        bins: [qw]
      - kind: node
        package: vnu-jar
        bins: [vnu]
      - kind: node
        package: chromedriver
        bins: [chromedriver]
    homepage: https://github.com/turbolego/wcag-skill
---

# WCAG 2.2 Accessibility

Use this skill to build or audit web content. Prefer native HTML, test through
HTTP, and treat automated output as evidence—not proof of conformance.

## Choose the scope first

1. Inventory every route, breakpoint, interactive state, overlay, error path,
   media item, authentication step, and third-party component in scope.
2. Set the target: `baseline`, `AA`, or `AAA`.
3. For an AAA target, read **all three** references before implementation:
   - [`references/validator-workflow.md`](references/validator-workflow.md)
   - [`references/aaa-evidence-matrix.md`](references/aaa-evidence-matrix.md)
   - [`references/manual-test-protocol.md`](references/manual-test-protocol.md)

> Do not say “WCAG AAA compliant” from automated results. Level AAA requires
> every applicable A, AA, and AAA success criterion for the full page and any
> complete process. Record an explicit evidence row or non-applicability
> rationale for each criterion.

## Capabilities and boundaries

The `allowed-tools` frontmatter declares the agent-facing tools and the
`shell` and `env` capabilities used by this skill. It does not set the host's
shell-execution policy, sandbox commands, constrain file paths, or restrict
network access.

| Script | Commands run | Reads | Writes | Network |
|---|---|---|---|---|
| `scripts/a11y-audit.sh <url> [out-dir]` | `axe`, `pa11y`, `node` (QualWeb CLI), `vnu` via Java, `curl`, `npm root -g`, Chrome/Chromium, Chromedriver | Environment variables in the frontmatter; installed tool paths | `out-dir` (default `a11y-reports/`): four JSON reports, `fetched-page.html`, and a Chrome wrapper script when extra Chrome flags apply | Loads the target URL, its redirects, and subresources in a browser; fetches the page with `curl` |
| `scripts/a11y-audit-limited.sh` | `free`, `awk`, `cat`, `ulimit`, then `scripts/a11y-audit.sh` | `/proc/meminfo`, cgroup memory files, memory-limit variables, `NODE_OPTIONS` | Same as `a11y-audit.sh`, relative to the skill root | Same as `a11y-audit.sh` |
| `scripts/run-w3c-validator.mjs <input> <output> [url]` | `vnu` | The input HTML file | The output JSON file | None |
| `scripts/check-wcag-412.py <html>` | None | The input HTML file | Standard output only | None |
| `scripts/check-legacy-markup.py <html-or-directory> [...]` | None | HTML files provided on the command line and `resources/legacy_tags.json` | Standard output only | None |
| `benchmark/scripts/check-tag-coverage.py <html> [tags.json]` | None | The input HTML, obsolete-tag list, and (in benchmark mode) required-tag list | Standard output only | None |
| `templates/playwright-state.spec.ts` | Playwright browser | `WCAG_TEST_URL` | Playwright output | Loads `WCAG_TEST_URL` |

Boundaries:

- No script requires or reads credentials, tokens, or secrets. Release tooling
  that uses a publishing token is excluded from the skill bundle.
- Audit only URLs you are authorized to test. Prefer loopback or staging hosts;
  the browser tools follow redirects and load third-party subresources.
- Use a dedicated output directory. Do not pass sensitive files as HTML inputs
  or sensitive paths as output destinations; scripts overwrite outputs.
- Keep the Chrome sandbox enabled outside isolated CI. In CI, the audit wrapper
  disables it unless `AXE_CHROME_EXTRA_ARGS` is set (an empty value keeps it on).
- Verify execution restrictions in the host runtime; the skill manifest cannot
  establish them. On OpenClaw, `openclaw approvals get` and
  `openclaw exec-policy show` report configured/effective execution policy.
  Use the host's allowlist, approval policy, or sandbox, and verify that it
  applies to the actual execution host.
- Shell use is limited to running the listed local audit tools; scripts do not
  install packages, modify system settings, or persist beyond their outputs.

## Build accessible by default

- Use one `<main>`, a meaningful `<title>`, one clear `<h1>`, and landmarks
  only where their semantics help orientation. Use `<section>` for a meaningful
  thematic grouping; give it an accessible heading when that improves its name.
  Use `<div>` for visual grouping alone.
- Use real `<a>`, `<button>`, `<input>`, `<select>`, `<textarea>`, and native
  disclosure/dialog patterns before inventing ARIA widgets. Never put a
  focusable element inside `aria-hidden="true"` content.
- Give informative images equivalent text; use `alt=""` only for decorative
  images. Provide the relevant captions, transcript, audio description, or
  media alternative for media.
- Label every form control, group related controls with `<fieldset><legend>`,
  use appropriate input types and `autocomplete`, preserve entered data after
  recoverable errors, and identify errors in text as well as colour.
- Keep DOM order aligned with reading and Tab order. Provide a mechanism to
  bypass repeated blocks where applicable (such as a skip link), visible focus,
  keyboard operation, and no keyboard trap.
- Do not communicate status, errors, required fields, or instructions by colour,
  position, shape, or sound alone. Respect `prefers-reduced-motion`.
- Ensure pointer targets are at least 24×24 CSS px (AA) or 44×44 CSS px (AAA) unless an exception applies.
- Ensure all functionality that uses dragging can also be achieved by a single
  pointer without dragging (AA), unless dragging is essential or the
  functionality is determined by the user agent and not modified by the
  author.
- Ensure keyboard focus is visible when operated by keyboard (AA, WCAG 2.2 SC
  2.4.7 Focus Visible).
- Meet WCAG 2.2 SC 1.4.11 Non-text Contrast (AA): visual information needed to
  identify applicable UI components and states, and parts of graphics needed
  to understand content, has at least 3:1 contrast against adjacent colors,
  subject to the criterion's exceptions.
- Meet WCAG 2.2 SC 2.4.11 Focus Not Obscured (Minimum, AA): when a component
  receives keyboard focus, it is not entirely hidden by author-created content.
- For WCAG 4.1.2, inventory interactive components and dynamic states. Use
  [`scripts/check-wcag-412.py`](scripts/check-wcag-412.py) as a source-markup
  candidate check, then verify rendered name, role, value, and state. Any
  user-triggered state change requires a before/after interaction test; axe,
  Pa11y, QualWeb, and a static inventory alone cannot establish that it works.
  Follow [`references/dynamic-state-test-protocol.md`](references/dynamic-state-test-protocol.md)
  and record `DYNAMIC TEST REQUIRED` until the transition is tested.
- Prevent legacy presentation markup, layout tables, div-based layouts that
  disrupt reading order, low-contrast text, unnamed image links, and unlabelled
  controls. Follow the repair workflow below for existing pages.

## Legacy markup repair

Preserve visible content, link destinations and fragment targets, language,
and behavior while replacing obsolete markup. Do not remove content just to
silence a checker. See [`references/legacy-markup-repair.md`](references/legacy-markup-repair.md)
for a worked example and verification checklist.

| Legacy pattern | Repair |
|---|---|
| `<font>` and presentational `color`/`size` | Semantic text or `<span>` plus CSS; test contrast against the actual background. |
| `<center>`, `<basefont>` | CSS alignment and root font styles; assess page structure separately. |
| `<marquee>`, `<blink>` | Preserve the information as static content by default and remove motion/blinking. If automatically moving content lasts more than five seconds alongside other content, provide pause/stop/hide controls unless an exception applies (SC 2.2.2); reduced-motion preferences do not replace required controls. A live region is only for genuinely dynamic updates. |
| Layout `<table>` | CSS grid/flex; retain real data tables with appropriate headers and `scope`. |
| Absolutely positioned div clusters | Assess the actual reading order and purpose of each region; use appropriate landmarks without turning every `div` into one. Positioning alone is not an accessibility failure. |
| Image-only link without a name | Give the image purpose-based `alt` text. Prefer visible link text when available; use `aria-label` only when native naming is unsuitable. |
| Unlabelled search input | Prefer an explicit visible `<label for>`; wrapping labels and `<fieldset><legend>` for related controls are also appropriate. Do not substitute placeholders for labels. |

Use the numeric contrast targets below: AA is 4.5:1 normal and 3:1 large
text (SC 1.4.3); AAA is 7:1 normal and 4.5:1 large text (SC 1.4.6),
subject to each criterion's exceptions. Check actual rendered colors.

```bash
python3 scripts/check-legacy-markup.py path/to/page.html
```

This static source inventory reports obsolete elements with file names and
line numbers as warnings, not WCAG failures. It does not detect presentation
attributes, layout tables, contrast, names, CSS-generated content, or
script-rendered markup. Inspect rendered pages and states; run the normal
audit and manual tests. Landmarks can aid navigation, but the axe `region` rule
is a best-practice check rather than a WCAG success criterion. Use landmarks
for regions with a meaningful purpose; nested `<header>` and `<footer>`
elements do not always expose banner/contentinfo landmarks.

## Low-memory audit guardrail (script-level)

When running on hosts with <2 GB RAM or in containers, use `scripts/a11y-audit-limited.sh`. Never delete this script (see PR #12 rejection rule below).

The wrapper determines and applies its memory budget in this order:

1. Read `MemAvailable` and `MemTotal` from `/proc/meminfo`. If `MemAvailable` is unavailable, use the `available` field from `free -m`.
2. Read the cgroup v1 limit from `memory.limit_in_bytes`. Ignore the unlimited sentinel (`9223372036854775807`).
3. Independently read the cgroup v2 limit from `memory.max` (`if`, not `elif`), even if v1 returned a valid limit. Ignore `max`, which means unlimited.
4. Use only positive numeric cgroup limits. Cap any cgroup limit greater than the host's `MemTotal` from `/proc/meminfo` at `MemTotal`, and use the smallest available value among host available memory and the valid cgroup limits. In containers, verify the guardrail against the cgroup quota instead of relying on host memory alone.
5. Apply `ulimit -v` and `NODE_OPTIONS` using `ULIMIT_PERCENT`/`ULIMIT_MIN_MB` and `NODE_PERCENT`/`NODE_MIN_MB`, respectively, with sensible defaults. Neither limit may exceed the available budget. If `ulimit -v` fails, exit with an explicit error.

In extremely constrained environments (<512MB available), you may need to explicitly set `NODE_OPTIONS="--max-old-space-size=256"` before running the audit wrapper.

- See also [`references/pil-logo-grid.md`](references/pil-logo-grid.md) for the PIL circular-logo layout pattern used when updating grid images.

## CI workflow maintenance

Keep GitHub Actions workflows (`.github/workflows/*.yml`) in sync with the pinned tool versions in `package.json`.
When the Chrome version on the runner changes, the `Align chromedriver to the installed Chrome major version` step must use a reliable version extraction: `chrome_major=$(/opt/hostedtoolcache/setup-chrome/chromium/stable/x64/chrome --version 2>/dev/null | grep -oE '[0-9]+' | head -1)`.
This prevents `npm error ETARGET` when requesting a non‑existent chromedriver version.

Run `npm ci` in a clean environment before each release and whenever `package.json` or the lockfile changes to verify that the pinned dependencies install without errors on the target Node version (>=22).
If you encounter heap-limit errors, increase the Node old space via `NODE_OPTIONS` (e.g., `NODE_OPTIONS="--max-old-space-size=512"`) before running `npm ci`.

## CI / audit environment notes

- `vnu-jar` requires Java 17 or newer; CI runners with older Java will throw `UnsupportedClassVersionError`. Set `JAVA_HOME` to a Java 17+ installation when needed.
- `vnu` writes temporary files to `/dev/shm`. On CI runners with small shared-memory partitions, add `_JAVA_OPTIONS="-Xshare:off -Djava.io.tmpdir=/tmp -Xmx256m"` to redirect temp storage to disk and cap heap.
- The `scripts/run-w3c-validator.mjs` script must be able to parse vnu output that may include warning messages; it now combines stdout and stderr and extracts a JSON object if necessary.
  If no valid JSON object can be extracted from vnu output, write an error record to the output file with the raw stderr text and exit non-zero. Do not write an empty report.


## Use the right numeric target

| Requirement | Baseline / AA minimum | AAA target |
|---|---:|---:|
| Normal text contrast | 4.5:1 | 7:1 |
| Large text contrast | 3:1 | 4.5:1 |
| UI component / state contrast (SC 1.4.11 Non-text Contrast) | At least 3:1 against adjacent colors, subject to exceptions | Same AA requirement |
| Focus Appearance (SC 2.4.13, AAA) | No 2.4.13 requirement at AA | Indicator area at least as large as a two-CSS-pixel-thick perimeter of the unfocused component; at least 3:1 contrast between the same pixels in focused and unfocused states |
| Pointer target (SC 2.5.8 AA / SC 2.5.5 AAA) | 24×24 CSS px, subject to SC 2.5.8 exceptions | 44×44 CSS px, subject to SC 2.5.5 exceptions |
| Dragging movements (SC 2.5.7) | Provide a single-pointer alternative that does not require dragging, unless an exception applies | Same AA requirement |

For AAA, WCAG 2.2 SC 2.4.12 Focus Not Obscured (Enhanced, AAA) requires that no
part of a focused component is hidden by author-created content. SC 2.4.13
Focus Appearance (AAA) requires an indicator area at least as large as a
two-CSS-pixel-thick perimeter of the unfocused component and at least 3:1
contrast between the same pixels in focused and unfocused states, subject to
the criterion's exceptions. These are AAA requirements, not AA requirements;
the stronger focus appearance may be used as an optional recommendation for AA
projects.

## Audit → triage → fix → verify


1. Install the tools listed in the frontmatter and make Chrome/Chromium plus a
   matching Chromedriver available. Set `AXE_CHROME_PATH` and
   `AXE_CHROMEDRIVER_PATH` when auto-detection is insufficient.
   If either binary still cannot be found or their major versions differ,
   stop the audit and do not record any automated results. Report each missing
   binary and its configured path, or report both paths and major versions
   if they do not match.
   In low-memory environments (e.g., <2GB RAM), consider using the headless
   shell and limiting memory via `NODE_OPTIONS` and `ulimit -v`; see
   `scripts/a11y-audit-limited.sh` for an example.

2. Serve the site over HTTP. Run the reproducible wrapper in
   [`references/validator-workflow.md`](references/validator-workflow.md).

3. Triage structural and markup errors first, then semantic, visual, operable,
   and understandable issues. Deduplicate findings across tools; retain raw
   JSON reports.

4. Fix one coherent group of issues, rerun the audit, and record the result.
   Review every `incomplete`, `cantTell`, warning, and false-positive decision.

5. For AAA, complete the mandatory manual protocol and evidence matrix before
   any conformance statement.

### WCAG 4.1.2 dynamic-state check

Run the source-markup inventory as a prompt for review, not as a conformance
result:

```bash
python3 scripts/check-wcag-412.py path/to/page.html
```

Inspect every reported component in the rendered page. For each stateful
component, test the initial state, activate it with the supported input, and
verify both the programmatic state and the corresponding UI change. Include
keyboard activation and assistive-technology review for custom widgets or
announcements whose meaning depends on context.

## Report precisely

For each finding, report the route/state, relevant success criterion, affected
selector or component, user impact, exact change, validation method, and retest
result. Say “no automated findings” when that is all the tools establish.

## Optional benchmark extension

The AI-WCAG-Gauntlet tag-coverage experiment is **not** a production
accessibility gate. Use it only when the task explicitly requests benchmark
scoring. Read [`benchmark/README.md`](benchmark/README.md) before setup,
generation, or either test suite. It requires a complete, unscored preflight of
tag coverage, W3C, axe, Pa11y, and QualWeb before the first official scored
run; preflight findings must be fixed and all five checks rerun before scoring.
Preflight reports and browser profiles stay in OS temporary storage and never
increment the benchmark counter. The official suite is still mandatory after
the preflight is clean; if it fails, follow its scored-iteration loop. Never
use a scored test-suite run as a preflight.

Write an original candidate for the assigned task. Reference templates are
validator smoke-test material only and must not be copied into scored
submissions. The benchmark extension's
[legacy-repair task](https://github.com/turbolego/AI-WCAG-Gauntlet/blob/main/BENCHMARK.md#legacy-repair-task)
retains all 113 required tags and adds preservation and legacy checks to the
validator loop; a production repair does not require benchmark tag coverage.
