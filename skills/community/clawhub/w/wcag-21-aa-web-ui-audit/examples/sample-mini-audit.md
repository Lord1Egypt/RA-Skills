# Sample Mini Audit (Ecommerce)

## Scope & Assumptions
- Product type: Ecommerce
- Audit mode: Confirmed implementation audit
- Environment: Staging storefront
- Platforms: Desktop + mobile
- Flows in scope: Browse/Search -> Product Detail -> Cart Drawer -> Checkout -> Order Confirmation
- Components in scope: Navigation, cart drawer, checkout form, toast/status updates, date picker
- Evidence handling:
  - Confirmed implementation issue: verified in staging with reproducible steps
  - Design-time risk: identified from checkout redesign mock where runtime behavior is not yet available
- Conformance statement: This report provides accessibility conformance guidance against WCAG 2.1 Level A and Level AA.

## A) Audit Summary (One Page)
- Overall conformance posture: Material gaps in checkout completion and dynamic status announcements.
- Total findings: 5
- Findings by severity: Blocker 1, High 2, Medium 1, Low 1
- Most impacted flow: Checkout
- Most impacted components: Cart drawer, form error states, toast/status messaging
- Complete process risk: Keyboard-only and screen reader users face elevated failure risk between cart and checkout completion.
- Top priorities:
  1. Fix cart drawer keyboard trap and focus handling.
  2. Add robust checkout error prevention and correction guidance.
  3. Implement status message announcements for add-to-cart and save events.

## B) Findings Table

| ID | Flow/Page | Component | WCAG SC (ID • Name • Level) | Severity | Affected Users | Issue Summary | Repro Steps | Expected | Actual | Recommended Fix (Design + Dev) | Verification (Manual + Tool) | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F-001 | Product -> Cart Drawer | Drawer | 2.1.2 • No Keyboard Trap • A; 2.4.3 • Focus Order • A; 2.4.7 • Focus Visible • AA | Blocker | Keyboard-only, Screen reader, Motor | Focus enters drawer but tabs behind overlay and cannot reliably reach close button. | Open product page, add item, open cart drawer, tab forward repeatedly. | Focus stays in drawer and close control is reachable. | Focus escapes to background and return path is unclear. | Design: preserve visible close action placement and focus ring style. Dev: implement managed focus loop, initial focus on drawer title/close, return focus to trigger on close. | Manual keyboard traversal + axe + screen reader smoke check. | Open |
| F-002 | Checkout Payment Step | Form fields and error states | 3.3.1 • Error Identification • A; 3.3.3 • Error Suggestion • AA; 3.3.4 • Error Prevention (Legal, Financial, Data) • AA; 1.4.1 • Use of Color • A | High | Screen reader, Low vision, Cognitive/learning | Card errors are shown as red outlines only with generic message and no correction guidance; no review step before final charge. | Submit invalid card details, observe field errors and final submit behavior. | Errors include field-specific guidance and review/confirm safeguard before charge. | Error text is generic, color-only cue used, and no confirmation step for critical submit. | Design: explicit field-level error copy and review checkpoint pattern. Dev: bind errors via `aria-describedby`, set `aria-invalid`, add pre-submit review confirmation. | Manual form scenario tests + axe checks for ARIA associations. | Open |
| F-003 | Product Detail | Add-to-cart toast | 4.1.3 • Status Messages • AA | High | Screen reader, Cognitive/learning | "Added to cart" toast appears visually but is not announced to assistive technology. | Activate Add to Cart using keyboard with screen reader running. | Status confirmation is announced without forced focus movement. | Visual toast appears only; no live region announcement. | Design: retain concise confirmation copy and timing. Dev: render toast region with `role=status` or `aria-live=polite` and avoid focus steal. | Manual NVDA/VoiceOver check + axe review of live region semantics. | Open |
| F-004 | Checkout Review | Primary action button focus style | 1.4.11 • Non-text Contrast • AA; 2.4.7 • Focus Visible • AA | Medium | Keyboard-only, Low vision, Color vision | Focus indicator on "Place Order" button has insufficient contrast against adjacent background in light theme. | Tab to Place Order button in checkout review step. | Focus ring is clearly visible with sufficient contrast. | Focus style is faint and difficult to detect. | Design: increase focus indicator contrast and thickness token. Dev: update CSS focus style tokens and preserve across themes. | Manual contrast check + visual regression at 200% zoom. | Open |
| F-005 | Checkout Redesign Spec (Design artifact) | Date picker | 2.1.1 • Keyboard • A; 4.1.2 • Name, Role, Value • A | Low | Keyboard-only, Screen reader | Mockups show custom date picker interactions but do not specify keyboard behavior or ARIA states. | Review redesign specification annotations. | Spec defines keyboard model and announced state/value changes. | Accessibility behavior is unspecified in design artifact. | Design: add interaction spec for keyboard navigation and state announcements. Dev: implement ARIA grid/dialog pattern with explicit focus behavior. | Design review checklist + implementation verification when built. | Open |

## C) Per-Flow Notes

### Flow: Browse/Search -> Product Detail
- Keyboard: Core browse path works; product card secondary actions need clearer focus outlines.
- Screen reader: Product links are announced; add-to-cart feedback is missing as status message.
- Zoom/reflow: Product cards wrap acceptably at 320 CSS px.
- Forms/errors: Search field label is present and associated.
- Dynamic updates: Result count updates are not consistently announced.

### Flow: Product Detail -> Cart Drawer
- Keyboard: Drawer focus containment fails (Blocker).
- Screen reader: Drawer title is announced; close control is difficult to reach after focus escapes.
- Zoom/reflow: Drawer remains usable at 200% but focus location is difficult to track.
- Forms/errors: Quantity controls need clearer instructions for keyboard usage.
- Dynamic updates: Quantity update toast also lacks announcement.

### Flow: Checkout -> Confirmation
- Keyboard: Checkout can be navigated, but focus visibility is weak on critical action.
- Screen reader: Error messages are generic and not always tied to fields.
- Zoom/reflow: Billing form reflows, but helper text wraps poorly with custom spacing.
- Forms/errors: Missing detailed correction suggestions and critical-submit error prevention.
- Dynamic updates: Save/payment status messages are visual-only.

## D) Remediation Backlog

### Epic: EPIC-01 Checkout Completion Accessibility
- Priority: P0
- Complete process integrity impact: Restores keyboard and assistive completion from cart through successful order.
- Mapped SC: 2.1.2, 2.4.3, 2.4.7, 3.3.1, 3.3.3, 3.3.4, 1.4.1
- Owner: Frontend + Design Systems
- Target Sprint: Sprint 12
- Dependencies: Design token update for focus styles
- Status: Planned

#### Issue: A11Y-101 Fix cart drawer focus containment
- Acceptance criteria:
  1. Focus enters drawer on open and returns to trigger on close.
  2. Tabbing remains within drawer while open.
  3. Close action is keyboard reachable with visible focus.
- Test steps:
  1. Keyboard-only tab cycle in drawer.
  2. Screen reader open/close smoke test.
  3. Regression on mobile viewport.

#### Issue: A11Y-102 Improve checkout error handling and prevention
- Acceptance criteria:
  1. Field errors identify exact issue and correction.
  2. Errors are associated programmatically to inputs.
  3. Final financial submit includes review/confirm safeguard.
- Test steps:
  1. Submit empty and invalid payment data.
  2. Verify screen reader reads error details.
  3. Verify review step appears before charge.

### Epic: EPIC-02 Dynamic Status and Visual State Clarity
- Priority: P1
- Complete process integrity impact: Reduces silent failures and improves confidence during multi-step actions.
- Mapped SC: 4.1.3, 1.4.11
- Owner: Frontend Platform
- Target Sprint: Sprint 13
- Dependencies: Toast component update
- Status: Planned

#### Issue: A11Y-201 Announce cart and save status updates
- Acceptance criteria:
  1. Add-to-cart and save confirmations are announced through live region semantics.
  2. No unnecessary focus movement occurs.
- Test steps:
  1. Trigger add-to-cart with screen reader running.
  2. Trigger save action and confirm announcement.

## E) Definition of Done (Engineering + QA)
- [ ] Keyboard-only users can complete cart-to-checkout-to-confirmation process.
- [ ] Focus order and visibility are verified across cart drawer and checkout actions.
- [ ] Form errors are specific, programmatically associated, and include correction guidance.
- [ ] Financial submit has error-prevention safeguard (review/confirm/reversible path).
- [ ] Status messages (cart add, save complete) are announced without forced focus changes.
- [ ] Contrast and non-text contrast checks pass for interactive states.
- [ ] All remediated findings have mapped SC evidence and verification notes.
