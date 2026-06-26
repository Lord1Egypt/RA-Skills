---
name: "playwright-in-sandbox"
description: "Primary Playwright governance skill for sandbox browser verification and deterministic end-to-end authoring or rewrite work."
---

# Playwright In Sandbox

This is the primary Playwright skill for sandbox browser verification and deterministic end-to-end coverage.

Use it in two explicit modes:

1. **Interactive Sandbox Mode** as final browser verification after a task's implementation is in a plausibly correct state.
2. **Deterministic E2E Mode** before finishing a task when the changed flow should be protected by durable regression coverage.

This skill is intentionally generic. It should work for:

- task-level screenshot-driven verification after an agent has implemented UI work and needs browser proof
- formal Playwright E2E authoring or rewrite work in downstream application repos
- task flows where a final browser verification should happen before the task is considered complete

Do not use this skill for backend-only work, one-off page operations that do not justify browser automation, or broad failure storms before you understand the workflow inventory and root causes.

## Core Workflow

1. Write a brief QA inventory before touching the browser.
2. Decide the mode first: Interactive Sandbox Mode or Deterministic E2E Mode.
3. Start or confirm the app in a persistent session.
4. Implement the change and get the functionality into a plausibly correct state before using Playwright as signoff.
5. Run the changed flow interactively and inspect screenshots as evidence, not just DOM state.
6. Record the contracts you learned:
   - route-ready signals
   - modal open and close signals
   - action-enabled conditions
   - save-complete signals
   - durable `data-testid` or semantic selectors
7. If the flow is bug-fix, workflow, regression-critical, or meaningfully changed, graduate it into deterministic E2E coverage.
8. If interactive proof shows the product behavior is wrong, fix the product code or the data contract. Do not make a bad behavior look green by weakening the test.
9. Before finishing the task, ensure the changed flow has both:
   - successful interactive proof
   - durable E2E coverage or an explicit rationale why it stays interactive-only

## Common Rules

These rules apply to both Interactive Sandbox Mode and Deterministic E2E Mode.

- Interactive verification is a post-change signoff step. Do not treat it as random mid-task poking while the implementation is still half-built.
- If the browser proves the product behavior is wrong, fix the functionality or the underlying data contract. Do not invent clever ways to make the test green around a bug.
- Use the repo's canonical E2E database contract strictly. If the repo standard is `e2e.db`, use `e2e.db`. If `e2e.db` is missing and the repo expects one, create or provision `e2e.db` and keep using that contract. Do not silently fall back to the normal application database.
- Prefer querying the canonical E2E database or seeded business data to derive expected values, statuses, assignments, and aggregates. When the repo uses `better-sqlite3`, it is acceptable to inspect the DB directly to confirm the real expected value before asserting the UI.
- Prefer selectors in this order:
  1. explicit `id`, `data-*`, `data-testid`, or other owned semantic contracts
  2. accessible role plus stable accessible name
  3. label/control association
  4. stable URL, pathname, or query contract
  5. text-only selectors only when the text itself is the product contract
  6. CSS, XPath, or DOM-order selectors only for deliberate structure checks
- Remove stale screenshots, traces, and temporary artifacts from failed or superseded runs before signoff.
- If the repo has a maintained full-suite run, nightly QA run, or automated health check, keep visibility on whether it actually ran and whether it stayed green. Targeted checks do not replace suite health forever.
- Some migrated or one-off client applications may temporarily need broader migration-verification coverage than a typical greenfield app. That is allowed, but the quality bar stays the same: deterministic selectors, owned data, real user contracts, and no fake greens.

## Mode Selection

### Use Interactive Sandbox Mode when

- the implementation is already in a plausibly correct state
- you need final browser proof that the changed flow really works for a user
- you need screenshot evidence to judge whether the UI is actually correct
- you need to learn or confirm readiness gates, modal behavior, or durable selectors before writing or updating automated coverage

### Use Deterministic E2E Mode when

- the change fixes a bug
- the task creates or materially changes a user workflow
- the flow is business-critical or likely to regress
- legacy Playwright coverage is being rewritten, consolidated, or retired
- the task should not be considered complete without regression protection

### Stay in Interactive Mode only when

- the change is exploratory or temporary
- the flow is not durable enough yet to encode as regression coverage
- the task does not meaningfully change a maintained workflow
- a migrated or one-off app needs a temporary verification pass that is not yet stable enough to convert into durable E2E coverage

If you choose not to graduate to committed E2E coverage, be explicit about why.

## Shared Environment Contract

- Prefer `127.0.0.1` over `localhost` unless the repo defines something else explicitly.
- Use the repo's explicit server contract first. If the repo does not define one, `4444` is the common sandbox default.
- In sandbox environments, Playwright browsers may live under `/ms-playwright`; do not assume the default cache path.
- In sandbox environments, launch Chromium explicitly in headless mode: `chromium.launch({ headless: true })`.
- Confirm the Playwright browser path when there is any doubt about the runtime payload:

```bash
echo "$PLAYWRIGHT_BROWSERS_PATH"
ls -al /ms-playwright
```

- Before `page.goto(...)`, verify the target port is actually listening and the app responds.
- For standard runs, use the repo's canonical E2E database contract. If the repo standard is `e2e.db`, always use `e2e.db`.
- If the repo expects `e2e.db` and it is missing, create or provision `e2e.db` before running tests.
- Only use alternate DB names or paths when the repo explicitly supports isolated validation lanes and you are intentionally isolating worker runs.
- Keep interactive artifacts separate from committed regression assets.
  - scratch scripts and screenshots belong in temp or dedicated artifact folders
  - committed regression coverage belongs in `tests/e2e/` or the repo's formal test location
- Remove stale screenshots, traces, and temporary artifacts from failed or superseded runs before signoff.
- When running multiple rewrite or validation lanes in parallel, isolate runtime resources:
  - port
  - database or seed state
  - output folder
  - screenshots and traces

## Interactive Sandbox Mode

Use this mode to prove a changed user flow works right now after the implementation is done enough to verify.

Interactive mode is not permission to poke until something happens to pass once. Use it after implementing the change and after you believe the functionality should work, then use the browser as final visual and functional verification of the real user flow.

### QA Inventory

Build the inventory from three sources:

- the user's requested requirements
- the user-visible behavior you implemented or changed
- the claims you expect to make in the final response

Anything that appears in any of those three sources must map to at least one QA check before signoff.

List:

- the user-visible claims you intend to sign off on
- every meaningful control, mode switch, or implemented interactive behavior
- the state changes or view changes each control can cause
- at least two exploratory or off-happy-path probes

### Desktop Verification Script

Set `TARGET_URL` to the app you are debugging. Prefer `127.0.0.1` over `localhost`.

```javascript
import { chromium } from "playwright";

const TARGET_URL = "http://127.0.0.1:4444";
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 1600, height: 900 },
});
const page = await context.newPage();

try {
  await page.goto(TARGET_URL, { waitUntil: "domcontentloaded" });
  console.log("Loaded:", await page.title());

  // Add the task-specific interactions and assertions here.

  await page.screenshot({ path: "playwright-desktop.png", type: "png" });
} finally {
  await context.close().catch(() => {});
  await browser.close().catch(() => {});
}
```

### Mobile Verification Script

Use a separate mobile script when the task affects responsive layout or touch behavior.

```javascript
import { chromium } from "playwright";

const TARGET_URL = "http://127.0.0.1:4444";
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 390, height: 844 },
  isMobile: true,
  hasTouch: true,
});
const page = await context.newPage();

try {
  await page.goto(TARGET_URL, { waitUntil: "domcontentloaded" });
  console.log("Loaded mobile:", await page.title());

  // Add the task-specific interactions and assertions here.

  await page.screenshot({ path: "playwright-mobile.png", type: "png" });
} finally {
  await context.close().catch(() => {});
  await browser.close().catch(() => {});
}
```

### Iteration Model

- Use one standalone Node.js verification script per focused flow.
- After code changes, rerun the verification script from a clean process instead of trying to preserve state across runs.
- Keep each script narrow: one changed flow, its main assertions, and its screenshot artifacts.
- If desktop and mobile both matter, run separate scripts or separate invocations.
- Screenshot review is part of the contract. Do not sign off from DOM assertions alone.

### Interactive Checklists

#### Session Loop

- write the QA inventory
- make the code change
- run the Playwright verification script for the current flow as final browser verification
- rerun functional QA with real user input
- rerun visual QA separately
- capture final artifacts only after the UI is in the state you are actually evaluating
- record the selectors and readiness gates you would trust in formal E2E

#### Functional QA

- Use real user controls for signoff: keyboard, mouse, click, touch, or equivalent Playwright input APIs.
- Verify at least one end-to-end critical flow.
- Confirm the visible result of that flow, not just internal state.
- Work through the shared QA inventory rather than ad hoc spot checks.
- Cover every obvious visible control at least once before signoff, not only the happy path.
- After the scripted checks pass, do a short exploratory pass using normal input.
- `page.evaluate(...)` may inspect or stage state, but it does not count as signoff input.

#### Visual QA

- Treat visual QA as separate from functional QA.
- Verify each visible claim explicitly in the state where it matters.
- Inspect the initial viewport before scrolling.
- Inspect the densest realistic state you can reach during QA.
- Look for clipping, overflow, distortion, weak contrast, broken layering, awkward motion, and stale overlays.
- If the UI only "works" because a hidden blocker was not noticed, the flow is not ready for signoff.

#### Interactive Signoff

- the functional path passed with normal user input
- the visual pass covered the whole relevant interface
- the viewport-fit checks passed for the intended initial view
- the final screenshots match the claims being signed off on
- the exploratory pass is called out in the final response
- the durable selectors and readiness gates are written down for E2E authoring
- stale screenshots or temporary artifacts from failed iterations are removed

## Deterministic E2E Mode

Use this mode when you are authoring or rewriting real Playwright regression coverage.

The job is to protect real functionality. If the app behavior is wrong, fix the app. Do not preserve a bug by adjusting the test around it.

### Workflow

1. Start from what interactive validation already proved.
2. Translate the learned UI contracts into durable automated checks.
3. Keep each spec focused on one workflow family or one coherent user journey.
4. Make each test own or explicitly receive its setup.
5. Prefer canonical seeded data or database-backed expectations for values, statuses, and aggregates instead of magic literals the test does not own.
6. Validate the changed flow before deleting or consolidating legacy coverage.
7. If rewriting a brittle suite, map every removed scenario to one of:
   - retained
   - consolidated with justification
   - intentionally obsolete with rationale
   - quarantined with explicit explanation

### Selector Hierarchy

Do not build durable tests on incidental text, generic combobox patterns, visual styling, or unstable overlay-sensitive DOM structure if a better contract exists.
Text-only selectors are a last resort unless the text itself is the true product contract.

### Waiting and Readiness Rules

- Do not default to `waitForLoadState("networkidle")`.
- For navigation, wait on URL change plus a page-ready sentinel, or response contract plus a ready sentinel.
- For dialogs, wait on explicit open-state before interaction and close-state before the next dependent step.
- For saves, wait on an observable save-complete contract.
- For async controls, assert what makes the control enabled before clicking it.
- For flows with overlays, drawers, or command palettes, prove they are closed before interacting with the next surface.
- If an interaction fails because another surface still owns focus or pointer events, fix the readiness model instead of layering retries forever.

### Navigation and Assertion Rules

- Assert behavior, not implementation.
- Prefer user-visible outcomes over internal implementation details.
- When numeric values, statuses, roster assignments, or aggregates come from seeded business data, derive the expected value from the test-owned setup or canonical DB contract first, then assert the UI matches it.
- Use text assertions only when the text itself is the contract.
- Avoid broad page-level text matching when the real contract lives in a specific card, section, dialog, or row.
- Do not keep multiple redundant assertions for the same workflow outcome just to make a spec feel thorough.
- Do not make a failing test green by broadening selectors, weakening expectations, or accepting the current bug unless that weaker contract is the real intended product behavior.

### Hard Bans

- default `networkidle` as the primary readiness strategy
- `page.evaluate(...)` to assert behavior the UI can expose directly
- giant omnibus specs spanning multiple workflows
- generic selectors like `button[role="combobox"]` as the primary contract
- silently reusing leftover state from prior tests
- deleting or consolidating legacy tests before the workflow mapping is explicit

## Failure Convergence Protocol

When many tests fail, do not patch them one by one by default.

1. Cluster failures by root cause first.
   - auth or bootstrap
   - stale server or shared port contention
   - modal or overlay state
   - selector contract gaps
   - readiness gaps
   - data or setup nondeterminism
   - obsolete workflow assumptions
2. Fix shared contracts before individual tests.
3. If the spec shape is wrong, stop patching and rewrite that workflow family.
4. If a spec keeps re-breaking because it mixes too many workflows, retire the omnibus and split it.

## Rewrite Governance

- Coverage loss must be explicit, never accidental.
- Every removed legacy assertion must have a mapped replacement or a written obsolescence rationale.
- Prefer meaningful consolidation over duplicative green checks, but do not silently reduce user-journey coverage.
- Leave quarantined `fixme` coverage only when:
  - the behavior is genuinely blocked
  - the quarantine is explicit
  - the rest of the family can still move forward safely
- Keep formal E2E assets in committed test directories and exploratory scripts or screenshots out of those directories.

## Parallel Rewrite Validation

Parallel rewrite work is allowed, but only when ownership and runtime isolation are real.

- Parallelize by workflow family or disjoint file ownership.
- Do not let multiple workers edit the same omnibus spec or shared helper without explicit ownership.
- If workers validate in parallel, isolate:
  - port
  - database or seed path
  - output folder
  - screenshots, traces, and artifacts
- If runtime isolation is not available, serialize Playwright validation even if rewrite coding stays parallel.

## Full-Suite Freshness

- Keep targeted validation fast, but do not let the maintained full-suite contract rot.
- If the repo or automation stack supports daily, nightly, or pre-release full-suite runs, treat that as part of quality visibility.
- If automated agents are expected to keep QA green, there should be observable evidence that they ran, what they ran, and whether they stayed green.
- A passing targeted spec is not a substitute for maintaining the broader suite over time.

## Dev Server

For local web debugging, keep the app running in a persistent TTY session. Do not rely on one-shot background commands from a short-lived shell.

Use the repo's documented startup flow first. If there is no explicit contract, the common sandbox pattern is:

```bash
pnpm run build
PORT=4444 pnpm run start
```

Before `page.goto(...)`, verify the target port is listening and the app responds.

After interactive verification is complete, stop the server process you started so the sandbox stays clean for the rest of the task.

## Common Failure Modes

- The browser flow passes only because an overlay or modal blocker was never actually closed.
- A test proves the DOM changed but does not prove the user-visible flow works.
- A spec uses the wrong roster, seed data, or identity assumptions and ends up "testing" fake state.
- A test is made green by adapting to the current bug instead of fixing the app or data contract.
- A test hard-codes display text, counts, or values that should have been derived from the test-owned DB or seed state.
- A worker rewrites files in parallel but validation still shares one fixed port and one mutable database.
- A suite looks green because duplicate tests were kept rather than properly consolidated.
- A large omnibus spec keeps hiding unique coverage because nobody mapped which extracted spec now owns each workflow.

## Signoff Expectations

- Interactive proof exists for the changed flow.
- If the flow matters for regression, durable E2E coverage exists too.
- The browser evidence matches the claims being made in the final response.
- The selectors, waits, and assertions are tied to real UI contracts.
- Any skipped, quarantined, consolidated, or retired coverage is called out explicitly.
