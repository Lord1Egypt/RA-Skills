# Common Bug Signatures

A catalog of exact, recurring failure patterns — check against these first, since pattern-matching a known signature is faster and more reliable than re-deriving root cause from scratch every time.

## 1. "Fix applied but symptom unchanged"

**Signature**: a fix was made (or claimed to be made), but re-inspecting the running app shows no visible change at all — not even partially.

**Likely causes, in order of probability**:
1. **Stale dev server / build cache** — the edit was saved but the running process is serving a cached bundle. Check: was the dev server restarted after the edit? For Vite, check if HMR actually picked up the change (a full page reload sometimes reveals what HMR silently failed to apply, especially for changes to config files, Tailwind config, or files outside the normal module graph). For Next.js, check `.next/cache` staleness, especially after config changes — a `rm -rf .next` and rebuild is a legitimate diagnostic step, not just a "last resort" hack.
2. **The edit was applied to the wrong file/component** — especially likely if the codebase has similarly-named components, or a component is re-exported/aliased and the edit landed on an unused copy. Grep for the actual rendered component's import path from the page entry point down, don't assume the file you edited is the one actually rendering.
3. **A more specific CSS rule or later-loaded stylesheet overrides the change** — check computed specificity, not just presence of the new rule. A utility class added to an element does nothing if a more specific selector elsewhere still wins.
4. **Conditional rendering never reaches the changed code path** — the fix is correct for the code as read, but a condition upstream (feature flag, prop default, environment check) means that code path isn't actually exercised in the scenario being tested.

## 2. "Element disappears entirely instead of just its label" (collapse/responsive hiding bugs)

**Signature**: a collapsible element (sidebar nav item, toolbar button) is meant to hide only its text label when space is constrained, but the whole element (icon included) vanishes.

**Likely cause**: the collapse logic conditionally renders the *entire* child tree (`{!collapsed && <NavItem icon label />}`) instead of conditionally rendering only the label portion (`<NavItem icon>{!collapsed && <span>{label}</span>}</NavItem>`), or applies `display: none` to a wrapping element that contains both icon and label instead of scoping the hidden state to the label element specifically.

**Fix pattern**: restructure so the icon is always rendered; only the label's visibility/width is conditional. Add a tooltip (`title` attribute or a proper tooltip component) that activates specifically in the collapsed state, since the label text becomes inaccessible otherwise — this is also an accessibility requirement, not just a nicety (a collapsed nav item with no accessible name violates basic labeling requirements).

## 3. "Child sizing fix doesn't work because of an unfixed parent"

**Signature**: a component was given `w-full`/`flex-grow`/`flex: 1` to make it fill available space, but it still renders narrower than expected, often appearing to only take up part of the viewport with unexplained empty space beside it.

**Likely cause**: an ancestor in the DOM tree has a competing constraint — a fixed `width`, a `max-width` without `mx-auto` centering intent, `display: inline-block`/`inline-flex` (which sizes to content, not available space), or a grid/flex parent that hasn't been told this child should grow (missing `flex-1`/`grow` on the *parent's* flex-item declaration for this child, not just on the child's own root element).

**Fix pattern**: trace every ancestor from the reported element up to the layout root (or at minimum up to the nearest `flex`/`grid` container) and confirm each one either has no competing width constraint or explicitly passes through sizing intent (e.g. a wrapping `<div>` between the flex container and the target element needs its own `flex: 1`/`w-full`, or the fix on the innermost element does nothing). This is the single most common reason a "full-width fix" that looks correct in isolation fails in the actual page.

## 4. "Works in one framework's dev mode, breaks in production build" (or vice versa)

**Signature**: a fix verified in `next dev`/`vite dev` looks correct, but breaks (or a bug that seemed fixed reappears) after `next build && next start` / `vite build && vite preview`.

**Likely cause**: dev-mode-only behavior masking the real issue — unminified/unpurged CSS in dev showing a class that gets purged in production (Tailwind content-path misconfiguration not scanning a file that uses a class dynamically), or hydration mismatches in Next.js that dev mode tolerates more visibly/differently than production. See `references/framework-verification.md` for the specific per-tool checks.

**Fix pattern**: always do a final production-build check for any fix in a project that will be deployed, not just a dev-server check — the two can genuinely diverge.

## 5. "Instruction was clear but the agent implemented something adjacent, not the actual ask"

**Signature**: a fix request specified a precise change (e.g. "main content must flex-grow to fill remaining width"), and the resulting diff makes *some* plausible-looking change, but not the one that addresses the actual reported symptom — the bug persists, sometimes across multiple attempts, sometimes even across a framework/stack change that doesn't touch the actual root cause.

**Likely cause**: this is a capability/discipline gap, not a code bug per se — treat it as a signal to slow down rather than iterate faster. Before making any change, restate in one sentence the exact root cause and the exact file/property that will change, and check that restatement against the original report before touching code. If, after a fix, the same category of bug is reported again for the same component, stop and re-derive the diagnosis from scratch (re-read the actual current state of the file) rather than applying another incremental patch on top of a possibly-wrong prior fix.
