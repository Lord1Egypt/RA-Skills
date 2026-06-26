---
name: design-review
description: "UI and design review: evaluate visual quality, responsive behavior, accessibility, color/contrast, typography, layout consistency, and i18n readiness using browser-based validation against industrial standards."
---

# Design Review

Evaluate your application's visual quality and usability against established design standards. This review catches issues that typically require a trained designer's eye — responsive breakpoints, accessibility compliance, visual hierarchy, spacing consistency, and internationalization readiness.

## When to use

Use `/design-review` when:
- Shipping UI without a designer reviewing it
- Before a launch or demo
- After significant UI changes or redesigns
- Checking accessibility compliance (WCAG 2.1 AA)
- Validating responsive behavior across devices

## Standards Referenced

- **WCAG 2.1 Level AA** — Web Content Accessibility Guidelines
- **Material Design** / **Human Interface Guidelines** — spacing, touch targets, typography scales
- **ISO 9241-110** — Interaction principles (suitability, self-descriptiveness, conformity)
- **APCA** — Advanced Perceptual Contrast Algorithm (next-gen contrast)

## Phase Overview

```
Phase 1: EDUCATE   → Brief context on what we check and why
Phase 2: SCOPE     → Identify pages, breakpoints, and focus areas
Phase 3: ANALYZE   → Browser-based checks with evidence capture
Phase 4: REPORT    → Findings with screenshots, scores, confidence
Phase 5: REMEDIATE → Fix guidance + YAML regression tests
```

---

## Phase 1: Educate

> **Why this matters:** 94% of first impressions are design-related. Poor visual quality erodes trust even when functionality is correct. Accessibility issues affect 15-20% of users and carry legal risk (ADA lawsuits increased 300% since 2018).

This review checks your app against objective, measurable design criteria — not subjective taste. Every finding references a specific standard.

---

## Phase 2: Scope

### Gather context

1. **Auto-detect** — scan the project for:
   - Framework (React, Vue, Next.js, etc.)
   - CSS approach (Tailwind, CSS modules, styled-components, etc.)
   - Design system in use (if any)
   - Route structure → list of pages
   - Existing a11y tooling (eslint-plugin-jsx-a11y, axe-core, etc.)

2. **Ask the user** (one at a time, with auto-detected defaults):
   - **Target URL**: Where is the app running? (auto-detect dev server)
   - **Key pages**: Which pages matter most? (recommend top 3-5 from routes)
   - **Target devices**: Desktop only? Mobile-first? Both? (default: both)
   - **Brand guidelines**: Any specific colors, fonts, or design system? (default: evaluate against general best practices)
   - **Focus areas**: Any known concerns? (optional)

3. **Define breakpoints** to test:
   - Mobile: 375px (iPhone SE), 390px (iPhone 14)
   - Tablet: 768px (iPad)
   - Desktop: 1280px, 1920px
   - (Adjust based on user's target audience)

---

## Phase 3: Analyze

Open a browser session with `new_session` using `record_evidence: true`. For each page in scope, run the following check categories.

### Category A: Responsive Design (RES)

| Check ID | Check | Standard | Method |
|----------|-------|----------|--------|
| RES-01 | Viewport meta tag present | Mobile best practice | Inspect `<meta name="viewport">` |
| RES-02 | No horizontal overflow at any breakpoint | Responsive design | Resize viewport, check for horizontal scrollbar |
| RES-03 | Touch targets ≥ 48x48px on mobile | WCAG 2.5.8 / Material Design | Measure interactive element sizes at mobile breakpoint |
| RES-04 | Text remains readable without zoom at 375px | WCAG 1.4.4 | Check font sizes ≥ 16px for body text on mobile |
| RES-05 | Navigation is accessible at all breakpoints | Usability | Verify nav collapses/adapts, hamburger menu works |
| RES-06 | Images scale appropriately | Responsive images | Check for `srcset`/`sizes` or CSS containment |
| RES-07 | No content truncation without indication | Usability | Check text overflow, ellipsis with tooltip or expand |
| RES-08 | Form inputs are usable on mobile | Usability | Check input sizes, proper input types (tel, email) |

**Browser validation:** For each breakpoint, use `act` to resize the viewport, then `inspect_page` to capture DOM and screenshot. Check for overflow elements, measure sizes via JavaScript.

### Category B: Accessibility (A11Y)

| Check ID | Check | Standard | Method |
|----------|-------|----------|--------|
| A11Y-01 | Color contrast ratio ≥ 4.5:1 (normal text) | WCAG 1.4.3 AA | Extract computed colors, calculate ratio |
| A11Y-02 | Color contrast ratio ≥ 3:1 (large text ≥ 18pt) | WCAG 1.4.3 AA | Same as above for large text |
| A11Y-03 | All images have alt text | WCAG 1.1.1 | Check `<img>` elements for `alt` attribute |
| A11Y-04 | Form inputs have associated labels | WCAG 1.3.1 | Check `<label for="">` or `aria-label` |
| A11Y-05 | Heading hierarchy is logical (h1→h2→h3) | WCAG 1.3.1 | Extract heading levels, check sequence |
| A11Y-06 | Focus is visible on all interactive elements | WCAG 2.4.7 | Tab through elements, check focus ring visibility |
| A11Y-07 | Keyboard navigation works (Tab, Enter, Escape) | WCAG 2.1.1 | Navigate entire page via keyboard |
| A11Y-08 | Skip navigation link present | WCAG 2.4.1 | Check for skip-to-content link |
| A11Y-09 | ARIA roles used correctly | WCAG 4.1.2 | Check for misused/redundant ARIA |
| A11Y-10 | Page has lang attribute | WCAG 3.1.1 | Check `<html lang="">` |
| A11Y-11 | Modal focus trapping works | WCAG 2.4.3 | Open modal, verify Tab stays within |
| A11Y-12 | Error messages are associated with inputs | WCAG 3.3.1 | Check `aria-describedby` or `aria-errormessage` |
| A11Y-13 | Reduced motion respected | WCAG 2.3.3 | Check for `prefers-reduced-motion` media query |
| A11Y-14 | No seizure-inducing content (>3 flashes/sec) | WCAG 2.3.1 | Visual inspection of animations |

**Browser validation:** Use `inspect_page` to extract the DOM. Run JavaScript via `act` to compute contrast ratios, check ARIA attributes, extract heading hierarchy. Use keyboard navigation (Tab, Enter, Escape) to test focus management.

### Category C: Visual Consistency (VIS)

| Check ID | Check | Standard | Method |
|----------|-------|----------|--------|
| VIS-01 | Consistent spacing scale | Design systems | Extract margins/paddings, check for consistent scale (4px/8px grid) |
| VIS-02 | Typography scale is consistent | Typographic hierarchy | Extract font sizes, check for consistent ratio/scale |
| VIS-03 | Color palette is limited and intentional | Design best practice | Extract all used colors, flag if >10 unique non-gray colors |
| VIS-04 | Interactive elements have consistent styling | Consistency | Compare button styles, link styles across pages |
| VIS-05 | Alignment grid is consistent | Layout | Check for misaligned elements that break the visual grid |
| VIS-06 | Loading states exist for async operations | UX best practice | Trigger async actions, verify loading indicators |
| VIS-07 | Empty states are handled | UX best practice | Navigate to pages with no data, check for meaningful empty states |
| VIS-08 | Error states are styled consistently | UX best practice | Trigger validation errors, check styling |
| VIS-09 | Dark mode consistency (if applicable) | Design systems | Toggle dark mode, check for un-themed elements |

**Browser validation:** Use JavaScript to extract computed styles, compare across elements and pages. Screenshot comparison between pages for visual consistency.

### Category D: Typography & Readability (TYP)

| Check ID | Check | Standard | Method |
|----------|-------|----------|--------|
| TYP-01 | Body text 16-20px | Readability research | Extract computed font-size |
| TYP-02 | Line height 1.4-1.6 for body text | Readability | Extract computed line-height |
| TYP-03 | Line length 45-75 characters | Readability (Bringhurst) | Measure character count per line |
| TYP-04 | Font loading strategy (FOUT/FOIT prevention) | Web performance | Check font-display CSS, preload hints |
| TYP-05 | Sufficient hierarchy levels (≥3 distinct sizes) | Typography | Extract and count distinct heading sizes |
| TYP-06 | Text is left-aligned (not justified) for body | Readability | Check text-align for body paragraphs |

### Category E: Internationalization Readiness (I18N)

| Check ID | Check | Standard | Method |
|----------|-------|----------|--------|
| I18N-01 | No hardcoded strings in components | i18n best practice | Scan source code for string literals in JSX/templates |
| I18N-02 | Layout handles text expansion (+30%) | i18n design | Inject longer text strings, check for overflow |
| I18N-03 | RTL layout support (if applicable) | i18n | Toggle `dir="rtl"`, check layout adaptation |
| I18N-04 | Date/number formatting uses locale | i18n | Check for hardcoded date/number formats |
| I18N-05 | Font stack includes CJK/Unicode fallbacks | i18n typography | Check font-family declarations |
| I18N-06 | Icons/images don't contain text | i18n | Visual inspection of image content |

**Browser validation:** Use JavaScript to modify `dir` attribute, inject longer text, change locale settings. Screenshot at each state.

---

## Phase 4: Report

Generate a structured report saved to `shiplight/reports/design-review-{date}.md`:

```markdown
# Design Review Report
**Date:** {date}
**URL:** {url}
**Pages reviewed:** {list}
**Breakpoints tested:** {list}

## Overall Score: {X}/10 | Confidence: {X}%

## Score Breakdown
| Category | Score | Findings |
|----------|-------|----------|
| Responsive (RES) | 7/10 | 2 high, 1 medium |
| Accessibility (A11Y) | 5/10 | 1 critical, 3 high |
| Visual Consistency (VIS) | 8/10 | 1 medium |
| Typography (TYP) | 9/10 | 1 low |
| i18n Readiness (I18N) | 6/10 | 2 medium |

## Findings

### CRITICAL

#### A11Y-01: Insufficient color contrast on primary buttons
- **Standard:** WCAG 1.4.3 AA (minimum 4.5:1)
- **Finding:** Primary button (#4A90D2 on #FFFFFF) has contrast ratio 3.1:1
- **Evidence:** [screenshot with annotation]
- **Pages affected:** All pages with primary CTA
- **Confidence:** 97%

### HIGH
...

### MEDIUM
...

### LOW / INFO
...
```

### Confidence Scoring
- **90-100%**: Browser-validated, measured programmatically (contrast ratio calculated, element size measured)
- **70-89%**: Strong evidence from DOM inspection, screenshot supports finding
- **50-69%**: Heuristic-based, may vary by context (e.g., "spacing looks inconsistent")
- **Below 50%**: Don't report

---

## Phase 5: Remediate

For each finding, provide:

### 1. Fix guidance
```markdown
#### A11Y-01: Insufficient color contrast
**File:** src/components/Button.tsx:23
**Current:** `background: #4A90D2` (contrast 3.1:1 against white)
**Fix:** `background: #2563EB` (contrast 4.8:1 against white) — maintains blue hue, meets AA
**Alternative:** `background: #1D4ED8` (contrast 7.1:1) — meets AAA
```

### 2. YAML regression test
```yaml
- name: a11y-01-button-contrast
  description: Verify primary button meets WCAG AA contrast ratio
  severity: critical
  standard: WCAG-1.4.3-AA
  steps:
    - URL: /
    - VERIFY: Primary action buttons have sufficient color contrast (minimum 4.5:1 ratio for normal text)
      timeout_seconds: 15
```

Save all YAML tests to `shiplight/tests/design-review.test.yaml`.

---

## Tips

- Use `inspect_page` to read the DOM first — it's cheaper than screenshots and provides element indices for `act`.
- For contrast checking, use JavaScript via `act` with `window.getComputedStyle()` to extract actual rendered colors.
- Test keyboard navigation by using `act` with keyboard actions (Tab, Enter, Escape, Arrow keys).
- Run this review at multiple breakpoints — many issues only appear at specific viewport sizes.
- For i18n text expansion testing, use `act` with JavaScript to modify `textContent` to longer strings.
- Close the session with `close_session` and use `generate_html_report` for a shareable evidence report.
