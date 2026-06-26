---
name: "playwright-interactive-sandbox"
description: "Persistent browser interaction through a normal Node.js Playwright script for fast iterative web UI debugging."
---

## Core Workflow

1. Write a brief QA inventory before testing:
    - Build the inventory from three sources: the user's requested requirements, the user-visible features or behaviors you actually implemented, and the claims you expect to make in the final response.
    - Anything that appears in any of those three sources must map to at least one QA check before signoff.
    - List the user-visible claims you intend to sign off on.
    - List every meaningful user-facing control, mode switch, or implemented interactive behavior.
    - List the state changes or view changes each control or implemented behavior can cause.
    - Use this as the shared coverage list for both functional QA and visual QA.
    - For each claim or control-state pair, note the intended functional check, the specific state where the visual check must happen, and the evidence you expect to capture.
    - If a requirement is visually central but subjective, convert it into an observable QA check instead of leaving it implicit.
    - Add at least 2 exploratory or off-happy-path scenarios that could expose fragile behavior.
2. Start or confirm any required dev server in a persistent TTY session.
3. Write a dedicated Playwright verification script for the changed flow.
4. Run the desktop script first, then add a mobile script if the change affects mobile layouts or touch behavior.
5. After each code change, rerun the verification script from a clean Node.js process.
6. Run functional QA with normal user input.
7. Run a separate visual QA pass.
8. Verify viewport fit and capture the screenshots needed to support your claims.
9. Save screenshot artifacts from the successful run.

## Desktop Verification Script

Set `TARGET_URL` to the app you are debugging. Use port `4444` and prefer `127.0.0.1` over `localhost`.

In this sandbox, Playwright browsers are preinstalled under `/ms-playwright` and `PLAYWRIGHT_BROWSERS_PATH` may already be set to that location. Do not assume the default cache path `~/.cache/ms-playwright`.

In this Debian sandbox, use headless mode for Playwright. Do not spend attempts trying headed mode unless the environment explicitly provides an X server.

In this Debian sandbox, use headless mode for Playwright. Do not spend attempts trying headed mode unless the environment explicitly provides an X server.

In this Debian sandbox, use headless mode for Playwright. Do not spend attempts trying headed mode unless the environment explicitly provides an X server.

```javascript
import { chromium } from 'playwright';

const TARGET_URL = 'http://127.0.0.1:4444';
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
	viewport: { width: 1600, height: 900 }
});
const page = await context.newPage();

try {
	await page.goto(TARGET_URL, { waitUntil: 'domcontentloaded' });
	console.log('Loaded:', await page.title());

	// Add the task-specific interactions and assertions here.

	await page.screenshot({ path: 'playwright-desktop.png', type: 'png' });
} finally {
	await context.close().catch(() => {});
	await browser.close().catch(() => {});
}
```

Use this pattern for the main changed flow. Keep the script focused on the exact behavior you need to verify.

If you want to confirm the Playwright browser path and installed browser payload, you can run:

```bash
echo "$PLAYWRIGHT_BROWSERS_PATH"
ls -al /ms-playwright
```

Example check run:

```bash
node /tmp/playwright-verify-desktop.mjs
```

## Mobile Verification Script

Use a separate mobile script when the task affects responsive layout or touch behavior.

```javascript
import { chromium } from 'playwright';

const TARGET_URL = 'http://127.0.0.1:4444';
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
	viewport: { width: 390, height: 844 },
	isMobile: true,
	hasTouch: true
});
const page = await context.newPage();

try {
	await page.goto(TARGET_URL, { waitUntil: 'domcontentloaded' });
	console.log('Loaded mobile:', await page.title());

	// Add the task-specific interactions and assertions here.

	await page.screenshot({ path: 'playwright-mobile.png', type: 'png' });
} finally {
	await context.close().catch(() => {});
	await browser.close().catch(() => {});
}
```

## Iteration Model

- Use one standalone Node.js script per verification pass.
- After code changes, rerun the verification script from a clean process instead of trying to preserve state across runs.
- Keep each script narrow: one changed flow, its main assertions, and its screenshot artifacts.
- If desktop and mobile both matter, run separate scripts or separate invocations rather than one large stateful script.

## Checklists

### Session Loop

- Write and run the Node.js Playwright verification script for the current validation run.
- Launch the target web app from the current workspace.
- Make the code change.
- Reload or restart using the correct path for that change.
- Update the shared QA inventory if exploration reveals an additional control, state, or visible claim.
- Re-run functional QA.
- Re-run visual QA.
- Capture final artifacts only after the current state is the one you are evaluating.

### Reload Decision

- Renderer-only change: reload the existing page.
- New uncertainty about whether the current script still matches the changed behavior: rerun a clean script instead of guessing.

### Functional QA

- Use real user controls for signoff: keyboard, mouse, click, touch, or equivalent Playwright input APIs.
- Verify at least one end-to-end critical flow.
- Confirm the visible result of that flow, not just internal state.
- For realtime or animation-heavy apps, verify behavior under actual interaction timing.
- Work through the shared QA inventory rather than ad hoc spot checks.
- Cover every obvious visible control at least once before signoff, not only the main happy path.
- For reversible controls or stateful toggles in the inventory, test the full cycle: initial state, changed state, and return to the initial state.
- After the scripted checks pass, do a short exploratory pass using normal input for 30-90 seconds instead of following only the intended path.
- If the exploratory pass reveals a new state, control, or claim, add it to the shared QA inventory and cover it before signoff.
- `page.evaluate(...)` may inspect or stage state, but it does not count as signoff input.

### Visual QA

- Treat visual QA as separate from functional QA.
- Use the same shared QA inventory defined before testing and updated during QA; do not start visual coverage from a different implicit list.
- Restate the user-visible claims and verify each one explicitly; do not assume a functional pass proves a visual claim.
- A user-visible claim is not signed off until it has been inspected in the specific state where it is meant to be perceived.
- Inspect the initial viewport before scrolling.
- Confirm that the initial view visibly supports the interface's primary claims; if a core promised element is not clearly perceptible there, treat that as a bug.
- Inspect all required visible regions, not just the main interaction surface.
- Inspect the states and modes already enumerated in the shared QA inventory, including at least one meaningful post-interaction state when the task is interactive.
- If motion or transitions are part of the experience, inspect at least one in-transition state in addition to the settled endpoints.
- If labels, overlays, annotations, guides, or highlights are meant to track changing content, verify that relationship after the relevant state change.
- For dynamic or interaction-dependent visuals, inspect long enough to judge stability, layering, and readability; do not rely on a single screenshot for signoff.
- For interfaces that can become denser after loading or interaction, inspect the densest realistic state you can reach during QA, not only the empty, loading, or collapsed state.
- If the product has a defined minimum supported viewport or window size, run a separate visual QA pass there; otherwise, choose a smaller but still realistic size and inspect it explicitly.
- Distinguish presence from implementation: if an intended affordance is technically there but not clearly perceptible because of weak contrast, occlusion, clipping, or instability, treat that as a visual failure.
- If any required visible region is clipped, cut off, obscured, or pushed outside the viewport in the state you are evaluating, treat that as a bug even if page-level scroll metrics appear acceptable.
- Look for clipping, overflow, distortion, layout imbalance, inconsistent spacing, alignment problems, illegible text, weak contrast, broken layering, and awkward motion states.
- Judge aesthetic quality as well as correctness. The UI should feel intentional, coherent, and visually pleasing for the task.
- Prefer viewport screenshots for signoff. Use full-page captures only as secondary debugging artifacts, and capture a focused screenshot when a region needs closer inspection.
- If motion makes a screenshot ambiguous, wait briefly for the UI to settle, then capture the image you are actually evaluating.
- Before signoff, explicitly ask: what visible part of this interface have I not yet inspected closely?
- Before signoff, explicitly ask: what visible defect would most likely embarrass this result if the user looked closely?

### Signoff

- The functional path passed with normal user input.
- Coverage is explicit against the shared QA inventory: note which requirements, implemented features, controls, states, and claims were exercised, and call out any intentional exclusions.
- The visual QA pass covered the whole relevant interface.
- Each user-visible claim has a matching visual check and reviewed screenshot artifact from the state and viewport or window size where that claim matters.
- The viewport-fit checks passed for the intended initial view and any required minimum supported viewport size.
- The UI is not just functional; it is visually coherent and not aesthetically weak for the task.
- Functional correctness, viewport fit, and visual quality must each pass on their own; one does not imply the others.
- A short exploratory pass was completed for interactive products, and the response mentions what that pass covered.
- If screenshot review and numeric checks disagreed at any point, the discrepancy was investigated before signoff; visible clipping in screenshots is a failure to resolve, not something metrics can overrule.
- Include a brief negative confirmation of the main defect classes you checked for and did not find.
- Keep the final successful screenshot artifacts needed for evidence, and remove stale or superseded image artifacts from failed or intermediate runs.

## Screenshot Capture

Use normal Playwright screenshots for evidence and debugging.

Desktop screenshot:

```javascript
await page.screenshot({ path: 'playwright-desktop.png', type: 'png' });
```

Mobile screenshot:

```javascript
await mobilePage.screenshot({ path: 'playwright-mobile.png', type: 'png' });
```

Clipped screenshot for a focused region:

```javascript
const clip = await page.locator('[data-testid="target"]').boundingBox();
if (clip) {
	await page.screenshot({ path: 'playwright-target.png', type: 'png', clip });
}
```

Use viewport screenshots for signoff by default. Use full-page screenshots only as secondary debugging artifacts when needed.

## Viewport Fit Checks (Required)

Do not assume a screenshot is acceptable just because the main widget is visible. Before signoff, explicitly verify that the intended initial view matches the product requirement, using both screenshot review and numeric checks.

- Define the intended initial view before signoff. For scrollable pages, this is the above-the-fold experience. For app-like shells, games, editors, dashboards, or tools, this is the full interactive surface plus the controls and status needed to use it.
- Use screenshots as the primary evidence for fit. Numeric checks support the screenshots; they do not overrule visible clipping.
- Signoff fails if any required visible region is clipped, cut off, obscured, or pushed outside the viewport in the intended initial view, even if page-level scroll metrics appear acceptable.
- Scrolling is acceptable when the product is designed to scroll and the initial view still communicates the core experience and exposes the primary call to action or required starting context.
- For fixed-shell interfaces, scrolling is not an acceptable workaround if it is needed to reach part of the primary interactive surface or essential controls.
- Do not rely on document scroll metrics alone. Fixed-height shells, internal panes, and hidden-overflow containers can clip required UI while page-level scroll checks still look clean.
- Check region bounds, not just document bounds. Verify that each required visible region fits within the viewport in the startup state.
- Passing viewport-fit checks only proves that the intended initial view is visible without unintended clipping or scrolling. It does not prove that the UI is visually correct or aesthetically successful.

Web or renderer check:

```javascript
console.log(
	await page.evaluate(() => ({
		innerWidth: window.innerWidth,
		innerHeight: window.innerHeight,
		clientWidth: document.documentElement.clientWidth,
		clientHeight: document.documentElement.clientHeight,
		scrollWidth: document.documentElement.scrollWidth,
		scrollHeight: document.documentElement.scrollHeight,
		canScrollX: document.documentElement.scrollWidth > document.documentElement.clientWidth,
		canScrollY: document.documentElement.scrollHeight > document.documentElement.clientHeight
	}))
);
```

Augment the numeric check with `getBoundingClientRect()` checks for the required visible regions in your specific UI when clipping is a realistic failure mode; document-level metrics alone are not sufficient for fixed shells.

## Dev Server

For local web debugging, keep the app running in a persistent TTY session. Do not rely on one-shot background commands from a short-lived shell.

Build first, then start the built app on port `4444` only:

```bash
pnpm run build
PORT=4444 pnpm run start
```

Before `page.goto(...)`, verify port `4444` is listening and the app responds.
- After interactive verification is complete, stop the server process you started on port `4444` so the sandbox stays clean for the rest of the task.
- `fuser` is not available in this Debian sandbox. Use `ss -ltnp | rg ":4444"` to find the listening PID, then `kill <pid>`, then rerun `ss -ltnp | rg ":4444"` to confirm port `4444` is no longer listening.
- Remove stale or superseded interactive image artifacts after cleanup so only the final successful evidence remains.
- After interactive verification is complete, stop the server process you started on port `4444` so the sandbox stays clean for the rest of the task.
- `fuser` is not available in this Debian sandbox. Use `ss -ltnp | rg ":4444"` to find the listening PID, then `kill <pid>`, then rerun `ss -ltnp | rg ":4444"` to confirm port `4444` is no longer listening.
- After interactive verification is complete, stop the server process you started on port `4444` so the sandbox stays clean for the rest of the task.

## Common Failure Modes

- `Cannot find module 'playwright'`: ensure the `playwright` package is installed in the current workspace and verify the import before running the Node.js script.
- Playwright package is installed but the browser executable seems missing: first verify `echo $PLAYWRIGHT_BROWSERS_PATH` and `ls -al /ms-playwright`. In this sandbox, browsers are expected at `/ms-playwright`, not `~/.cache/ms-playwright`. Only run `npx playwright install chromium` if that directory is actually absent or unusable.
- `page.goto: net::ERR_CONNECTION_REFUSED`: make sure the dev server is still running in a persistent TTY session, recheck the port, and prefer `http://127.0.0.1:<port>`.
- The Node.js process exited or reset unexpectedly: rerun the verification script from a clean process.
