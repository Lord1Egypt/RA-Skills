---
name: ui-doctor
description: >
  Audit and review application UI for IDS compliance, accessibility, usability,
  and cognitive load. Covers component usage validation, WCAG accessibility
  checks, cognitive load assessment, and UX quality evaluation. Use when asked
  to review UI, check accessibility, assess usability, audit IDS compliance,
  or when the user says "review this page", "check a11y", or "is this
  accessible?"
license: Apache-2.0
compatibility: React 18+, TypeScript, @iress-oss/ids-components@beta
metadata:
  author: iress
  version: "1.0"
---

# Skill: UI Doctor

Audit and review application UI for IDS compliance, accessibility, usability, and cognitive load. This skill helps AI agents perform comprehensive UI reviews covering component usage, accessibility (WCAG), usability heuristics (Nielsen's 10), cognitive load, and progressive disclosure — then produce actionable reports with prioritised recommendations.

## When to Use

Activate this skill when the user says things like:

- "Review this page / component / file for accessibility"
- "Check the usability of this UI"
- "Audit this for IDS compliance"
- "This feels like too much cognitive load"
- "Are we following IDS guidelines?"
- "Check for a11y issues"
- "Review this UI"
- "Is this form accessible?"
- "Can you do a UX review?"

Or more generally:

- Reviewing application UI code for IDS compliance
- Validating accessibility (WCAG 2.1 AA)
- Assessing usability and cognitive load
- Evaluating design token usage and consistency
- Generating a UI health report with a compliance score
- Providing recommendations to improve UX, accessibility, and IDS adoption

## Audit Modes

**Default: Quick UX Review.** Use this unless the user specifically asks for accessibility or full compliance. Escalate to a more thorough mode if the quick review reveals significant issues.

### Quick UX Review (default)

Use when the user asks for a general UI review, usability check, or "does this look right?"

1. **Cognitive load & information architecture** — Is the UI overwhelming? Are there too many items, options, or actions visible at once?
2. **Usability heuristics** — Evaluate against Nielsen's 10 (see [audit checklist](references/audit-checklist.md) § Usability Heuristics)
3. **Button hierarchy & layout consistency** — One primary per section, consistent spacing
4. **Quick component scan** — Are obvious raw HTML elements used where IDS components exist?

### Accessibility Review

Use when the user asks about a11y, WCAG, keyboard navigation, or screen reader support.

1. **Form accessibility** — Labels, required indicators, validation messages, id/htmlFor pairing
2. **Keyboard & focus** — Skip links, focus trapping in modals/slideouts, visible focus indicators
3. **Screen reader** — ARIA landmarks, dynamic content announcements, accessible names on interactive elements
4. **Colour & contrast** — WCAG AA contrast ratios, no reliance on colour alone
5. **Cognitive load** — Progressive disclosure, information density (see [audit checklist](references/audit-checklist.md) § Cognitive Load)

### Full Compliance Audit

Use when the user asks for a complete IDS audit or compliance report.

1. Run **all** checklist sections from the [audit checklist](references/audit-checklist.md)
2. Validate component usage against [replacement tables](references/replacement-tables.md)
3. Check design token usage and Provider/CSS setup
4. Evaluate patterns (forms, loading, navigation)
5. Assess usability and cognitive load
6. Generate a full report using the [report template](references/report-template.md)

## Scoped Audits

If the user asks about a **specific file, component, or page**, focus the audit on that scope only. Apply the same checklist items but only to the files in question. Do not scan the entire application unless asked.

Example: "Check the accessibility of `UserProfileForm.tsx`" → run the Accessibility Review mode on that single file.

## Audit Scope

Before starting, determine which files to scan.

### Files to Scan

- All `.tsx`, `.jsx`, `.ts`, `.js` files in `src/` (or the application source directory)
- CSS/SCSS/styled-component files for hardcoded design values
- Application entry point(s) for Provider and CSS import checks

**Important:** Always trace the component tree from the actual mount point (e.g. `main.tsx`, `index.tsx`) before evaluating Provider & Setup. The entry point may not be a route file — it could be a custom element wrapper, a shadow DOM host, or a separate bootstrap file that renders the router. Do not penalise missing Provider/CSS if a parent entry point already handles it.

### Files to Exclude

- **Test files** (`*.test.tsx`, `*.spec.tsx`, `__tests__/`) — test mocks may legitimately use raw HTML
- **Storybook stories** (`*.stories.tsx`) — may intentionally show raw HTML for comparison
- **Config files** (`*.config.ts`, `*.config.js`) — not UI code
- **Type definitions** (`*.d.ts`) — no runtime UI code
- **Third-party code** (`node_modules/`, vendored libraries) — outside application control
- **Build output** (`dist/`, `build/`) — generated code

### Version-Aware Auditing

IDS is currently on **version 6**. When auditing:

- **Check the installed version** — `package.json` for `@iress-oss/ids-components`
- **v6** — Apply all rules as-is
- **v5** — Flag v5-specific patterns as "migration opportunities" (key differences: `IressForm` uses `rules` prop, `react-hook-form` is a peer dependency, form state via `useWatch`/`ref`)
- **Pre-v5** — Flag as requiring major migration; prioritise Provider/CSS setup first
- **Always note the version** in the audit report header

## Audit Process

### 1. Evaluate UX, Accessibility & Cognitive Load

Start with what users experience — assess the UI's usability, accessibility, and information density before checking component compliance.

#### a. Usability Heuristics (Nielsen's 10)

Evaluate the application against all 10 heuristics. Each has IDS-specific guidance in the [audit checklist](references/audit-checklist.md) § Usability Heuristics. Key areas:

1. **Visibility of system status** — Loading states use `IressLoading` (preferred) or `IressSkeleton` (for custom content placeholder patterns); active states visible on tabs, nav, breadcrumbs
2. **Match between system and real world** — Labels use plain language; icons paired with text; status colours follow conventions
3. **User control and freedom** — Modals/slideouts dismissible; destructive actions require confirmation; forms have cancel
4. **Consistency and standards** — All components from IDS; tokens used consistently; same action = same pattern
5. **Error prevention** — Declarative `rules` validation; required fields marked; constraints communicated via `hint`
6. **Recognition rather than recall** — Persistent navigation; visible breadcrumbs; labels always visible (not just placeholders)
7. **Flexibility and efficiency** — Keyboard shortcuts; skip links; searchable selects; autocomplete
8. **Aesthetic and minimalist design** — Clear visual hierarchy; consistent spacing; one primary action per section
9. **Help users recognise/recover from errors** — Human-readable validation; inline errors; `IressValidationSummary` for long forms
10. **Help and documentation** — Hint text; tooltips for non-obvious UI; placeholder supplementary to labels

#### b. Cognitive Load & Information Architecture

Evaluate whether the UI presents too much information or too many choices at once.

- **Item count thresholds** — Menus/dropdowns with >10 items should use `searchable`; long forms (>8 fields) should use `IressForm pattern="long"`; navigation with >7 top-level items should use grouping
- **Progressive disclosure** — Use `IressExpander` or `IressTabSet` to hide secondary content until needed; multi-step flows break complex tasks into stages
- **Information density** — Is the screen overwhelming? Use `IressCard`/`IressPanel` to group related content; use `IressStack` with adequate spacing
- **Batch action safety** — Bulk operations (select-all + delete) need explicit confirmation via `IressModal`; show count of affected items
- **Focus management after state changes** — After modal close, focus returns to trigger; after item deletion, focus moves to next/previous item; after form submission, focus moves to result or error
- **Visual hierarchy** — Primary content is prominent; secondary content is de-emphasised; use `IressText textStyle` to establish hierarchy

#### c. Accessibility (WCAG 2.1 AA)

Check form accessibility, keyboard & focus, screen reader support, and colour/contrast. See [audit checklist](references/audit-checklist.md) § Accessibility for the full list. Key checks:

- All form inputs have labels (via `IressField` or `IressFormField`)
- Skip links present (`IressSkipLink`)
- Focus trapping in modals/slideouts (automatic with IDS)
- ARIA landmarks (`<nav>`, `<main>`, `<aside>`)
- Dynamic content announced to screen readers — choose the right tier:
  - `IressAlert` — persistent, inline status messages (no `aria-live`; already in the reading flow)
  - `IressToaster` — transient notifications demanding attention (`aria-live="assertive"`); avoid overuse
  - Micro animations/interactions with colocated `aria-live="polite"` — for subtle, user-initiated updates (save indicators, count badges, status changes) that don't warrant a toast; place the live region near the component, not globally
- Colour contrast meets WCAG AA; no reliance on colour alone

#### d. Button Hierarchy

- One `mode="primary"` button per logical section
- Destructive actions use `status="danger"`, not custom red styling
- Icon-only buttons include accessible text

#### e. Layout Consistency

- Vertical stacks → `IressStack`; horizontal rows → `IressInline`; grids → `IressRow`/`IressCol`
- Spacing uses token values (0–10) on `gap` prop
- `IressCSSProps` (`m`, `mx`, `p`, `px`) instead of inline styles
- Responsive: `hideFrom`/`hideBelow` props or `useBreakpoint` hook; grid layouts use responsive `span` (e.g. `span={{ xs: 12, md: 6 }}`); mobile view focuses on primary task with secondary content in `IressSlideout` or collapsible sections

### 2. Validate IDS Component Usage

Scan for raw HTML, third-party components, and custom implementations that have IDS equivalents. Use the [replacement tables](references/replacement-tables.md) for the full mapping.

**Quick checks:**

- No raw `<button>`, `<input>`, `<select>`, `<form>`, `<table>` — use IDS equivalents
- No third-party UI library imports (MUI, Ant, Chakra, Bootstrap, Radix, Headless UI) where IDS equivalents exist
- No custom modals, drawers, tabs, tooltips, alerts — use IDS patterns
- No custom loading spinners — use `IressLoading` (preferred) or `IressSkeleton` for custom content placeholder patterns
- Layout divs with flex/grid styles → `IressStack`, `IressInline`, `IressRow`/`IressCol`

**Acceptable exceptions** (do NOT flag): raw elements in test files, third-party widgets the app cannot control, `<input type="hidden">`, custom components wrapping IDS internally. See [replacement tables](references/replacement-tables.md) § Acceptable Exceptions.

### 3. Validate IDS Principles & Setup

#### a. Provider & CSS Setup

- **IressProvider must wrap the application root** — Required for fonts, CSS variables, and theming. `IressProvider` already includes `IressModalProvider`, `IressSlideoutProvider`, `IressToasterProvider`, `IressPopoverProvider`, and `IressIconProvider` — these should not be added separately. Similarly, `IressShadow` includes `IressProvider` internally, so no additional providers are needed when using `IressShadow`.
- **The IDS component CSS must be imported** — `@iress-oss/ids-components/dist/style.css` contains all component styles
- Users only need to install `@iress-oss/ids-components@beta` — the tokens are bundled within the component library and do not need to be installed separately. **IDS v6 is currently in beta**, so the `@beta` tag is required (e.g. `npm install @iress-oss/ids-components@beta`)
- **CSP must allowlist IDS external origins** — If the app enforces a Content Security Policy, `fonts.googleapis.com` and `fonts.gstatic.com` must be in `style-src`/`font-src`. Add `cdn.iress.com` if using legacy Font Awesome icons or `IressTheme`. If using `IressShadow` and inline styles are blocked, add `<meta name="csp-nonce" content="...">` in `<head>`. See the CSP Guide at `node_modules/@iress-oss/ids-components/.ai/guides/get-started-content-security-policy.md` for details (requires `@iress-oss/ids-components` to be installed).
- If using design tokens directly in application code (for custom styling), users should additionally install `@iress-oss/ids-tokens@beta` and import `@iress-oss/ids-tokens/build/css-vars.css`

```typescript
// ✅ Minimum required setup (option A — standard)
import '@iress-oss/ids-components/dist/style.css';
import { IressProvider } from '@iress-oss/ids-components';

function App() {
  return <IressProvider>{/* app content */}</IressProvider>;
}
```

```typescript
// ✅ Minimum required setup (option B — IressShadow)
// IressShadow is a superset of IressProvider — it wraps children in a shadow DOM,
// injects style.css automatically, and provides the IressProvider context.
// No separate IressProvider or CSS import is needed when using IressShadow.
import { IressShadow } from '@iress-oss/ids-components';

function App() {
  return <IressShadow>{/* app content */}</IressShadow>;
}
```

```typescript
// ✅ With direct token usage in application code (optional)
import '@iress-oss/ids-components/dist/style.css';
import '@iress-oss/ids-tokens/build/css-vars.css';
import { IressProvider } from '@iress-oss/ids-components';
import { cssVars } from '@iress-oss/ids-tokens';

function App() {
  return (
    <IressProvider>
      <div style={{ padding: cssVars.spacing[4] }}>{/* app content */}</div>
    </IressProvider>
  );
}
```

```typescript
// ❌ Incorrect — missing component CSS
import { IressProvider } from '@iress-oss/ids-components';
// Components will render without styles!

// ❌ Incorrect — installing tokens separately just for provider setup
yarn add @iress-oss/ids-tokens@beta  // Not needed unless using tokens directly

// ❌ Incorrect — installing without @beta tag (will not resolve to v6)
yarn add @iress-oss/ids-components  // Must use @beta tag
```

#### b. Design Token Usage

- No hardcoded colour hex/rgb — use IDS colour tokens
- No hardcoded pixel spacing — use IDS spacing tokens
- No hardcoded font properties — use IDS typography tokens
- No hardcoded border-radius — use IDS radius tokens

```typescript
// ❌ Hardcoded values
<div style={{ color: '#003271', padding: '16px', borderRadius: '4px' }}>

// ✅ IDS tokens
import { cssVars } from '@iress-oss/ids-tokens';
<div style={{
  color: cssVars.colour.primary.fill,
  padding: cssVars.spacing[4],
  borderRadius: cssVars.radius[1]
}}>
```

#### c. Form & Pattern Compliance

IDS provides patterns that ensure consistent UIs. Validate usage where appropriate.

**Form Pattern (`IressForm`):**

- Use `IressForm` + `IressFormField` for all forms
- `rules` prop for validation; `useWatch` for conditional fields
- `pattern="long"` for forms with >8 fields
- `react-hook-form` as peer dependency

**Loading Pattern (`IressLoading` / `IressSkeleton`):**

- `page`, `component`, `start-up`, `validate`, `long` patterns
- Handles timing thresholds automatically (no indicator <500ms, spinner at 500ms, message at 2s)
- Prefer `IressLoading` for standard loading states — it handles timing, messaging, and accessibility automatically
- `IressSkeleton` is valid for custom content placeholder patterns where you need skeleton screens that mirror the page layout; use `IressLoading` if possible
- When a page reads from a pre-populated cache (e.g. SWR, React Query, or TanStack Query cache populated by a previous page), a separate loading state may be unnecessary — check whether the data source is a cache read vs a fresh fetch before flagging

**Navigation Patterns:**

- `IressDropdownMenu` for filter/action triggers (not inside forms)
- `IressContextualMenu` for row-level actions with `ariaLabel`
- `IressSideNav` for application shell navigation
- `IressBreadcrumbs` for hierarchy navigation

**Error Boundary Pattern:**

React error boundaries catch component crashes and should render IDS components as fallback UI — not custom error pages or raw HTML.

| Error Scope                                 | IDS Component                                          | Why                                                                 |
| ------------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------- |
| Full-page crash (root error boundary)       | `IressModal status="danger"` with retry/reload actions | Blocks interaction, demands attention, provides structured recovery |
| Section/feature crash (scoped boundary)     | `IressAlert status="danger"` as inline fallback        | Persistent, in-context — rest of the page still works               |
| Transient API/network failure (not a crash) | `IressToaster`                                         | Retryable, doesn't block the UI                                     |

- **Do NOT use `IressToaster` for error boundaries** — toasts are transient and dismissible; if the user dismisses it, the broken component tree has no recovery UI
- **`IressModal status="danger"`** is the primary recommendation for root-level error boundaries — use `actions` prop to offer "Retry" or "Reload" buttons
- **`IressAlert status="danger"`** is preferred for scoped boundaries that wrap individual features — shows inline where the broken component was

**Before flagging missing error handling:** Check whether a parent component or layout route already provides an error boundary that covers the file being audited. Error boundaries are an app-wide pattern — a page component does not need its own error/empty state handling if a parent boundary already catches and renders IDS-based fallback UI (e.g. `IressModal status="danger"` with navigation-aware recovery). Only flag if no ancestor provides error handling.

**Shadow DOM Pattern (`IressShadow`):**

- `IressShadow` is a **superset of `IressProvider`** — it creates a shadow root, injects `style.css` into it, and provides the `IressProvider` context automatically. When an app uses `IressShadow` at its entry point, no separate `IressProvider` or CSS import is required.
- Commonly used for microfrontend CSS isolation, but also valid as the sole Provider + CSS setup for any application
- Creates a shadow root on a `<div>` — children are standard React components
- The `slot` attribute is irrelevant; always use React props (`prepend`, `append`, `footer`, etc.)

### 4. Provide Recommendations

Prioritise findings using these levels:

| Priority     | Description                                                                                             | Action                |
| ------------ | ------------------------------------------------------------------------------------------------------- | --------------------- |
| **Critical** | Missing Provider/CSS, raw inputs without labels, missing skip links, forms not using `IressForm`        | Must fix immediately  |
| **High**     | Raw HTML elements with IDS equivalents, custom form handling, a11y failures, high cognitive load issues | Fix in current sprint |
| **Medium**   | Hardcoded tokens, missing IressText, custom layout, missing ARIA landmarks, information density issues  | Plan for next sprint  |
| **Low**      | Missing IressImage, custom badges, minor token inconsistencies, non-critical UX improvements            | Backlog               |

For each finding, provide: (1) what was found, (2) why it matters, (3) how to fix (with before/after code), (4) priority level.

### 5. Generate Compliance Report

Use the [report template](references/report-template.md) to produce a structured report.

## Example Audit Output

### Quick Scan Summary

```
IDS UI Doctor — Quick Scan
================================
Files scanned:     42
Components found:  18 IDS / 7 raw HTML
Patterns used:     3/7 available
Token compliance:  73%
Accessibility:     82%

Top Issues:
  ⚠ 3× raw <button> found (should be IressButton)
  ⚠ 2× hardcoded colours found (#333, #f5f5f5)
  ⚠ 1× <input> without IressField wrapper
  ⚠ 2× custom <form> found (should use IressForm)
  ⚠ 1× custom loading spinner (should use IressLoading)
  ⚠ 1× missing skip link for keyboard navigation
  ✓ IressProvider correctly configured
  ✓ Component CSS imported
  ✓ IressBreadcrumbs used for navigation hierarchy
  ✓ Colour contrast passes WCAG AA
```

## Reference

> **Note:** Component docs, pattern docs, and the manifest are within the package itself.

- **Component docs:** `node_modules/@iress-oss/ids-components/.ai/components/`
- **Pattern docs:** `node_modules/@iress-oss/ids-components/.ai/patterns/`
- **Index (full component list):** `node_modules/@iress-oss/ids-components/.ai/index.json`
- **Token usage skill:** `.agents/skills/token-usage/SKILL.md`
- **Figma mapping skill:** `.agents/skills/figma-to-ids/SKILL.md`
- **UI translation skill:** `.agents/skills/ui-translation/SKILL.md`
- **Storybook and Guidelines:** https://main--691abcc79dfa560a36d0a74f.chromatic.com
- **Common mistakes guide:** `node_modules/@iress-oss/ids-components/.ai/guides/foundations-common-mistakes.md` (requires `@iress-oss/ids-components` to be installed)

## Common Mistakes to Flag in Audits

For the full list of common anti-patterns with code examples, read the Common Mistakes guide at `node_modules/@iress-oss/ids-components/.ai/guides/foundations-common-mistakes.md` (requires `@iress-oss/ids-components` to be installed). When auditing, flag these with the following priorities and audit rules:

### `disabled` attribute on IressButton — **High** priority

**Audit rule:** Search for `disabled` on any `<IressButton`. Every match is a finding.

### Redundant `textStyle` on IressText — **Medium** priority

**Audit rule:** Search for `IressText` with both `element` and `textStyle` where the textStyle matches the element's default styling (e.g. `element="h1" textStyle="typography.heading.1"`).

### Legacy `slot` attributes (v4 pattern) — **High** priority

**Audit rule:** Search for `slot="` inside any `<Iress*>` component. Every match is a finding.
