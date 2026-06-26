# Conversion & UX Checklist

Use this checklist to audit any landing page, app screen, or flow for quick wins.

## Above the Fold (Hero Section)

- [ ] Clear value proposition visible without scrolling
- [ ] Primary CTA present and prominent above the fold
- [ ] Only ONE primary CTA (no competing actions)
- [ ] Trust signals near the CTA ("No credit card" / "Free forever" / user count)
- [ ] Hero describes the outcome/benefit, not just features
- [ ] Subtitle has lower contrast than headline (not competing)
- [ ] Scroll prompt visible (chevron, partial next section, or animation)
- [ ] Hero image/video directs attention toward the CTA (Gutenberg + gaze direction)

## Visual Hierarchy

- [ ] Title is clearly the largest element
- [ ] Type scale is consistent (×1.25 ratio)
- [ ] Secondary text has reduced opacity (≤70%)
- [ ] Primary action is visually dominant over secondary
- [ ] Related elements are grouped with consistent spacing
- [ ] Left-aligned text blocks (not centered paragraphs)
- [ ] Line width capped at 65ch / 500–700px

## Navigation

- [ ] Active state is obvious (background change, not just color)
- [ ] All nav items have icons + labels (not icons alone)
- [ ] Maximum 7 nav items (Miller's Law)
- [ ] Mobile nav accessible in thumb zone
- [ ] Sections separated by whitespace, not excessive dividers

## CTA Buttons

- [ ] Copy is a specific action verb (not "Submit" / "OK")
- [ ] Primary CTA is visually dominant (size + color + shadow)
- [ ] Dangerous/secondary actions are de-emphasized (ghost/text style)
- [ ] Consistent button styles throughout (same shape, same primary color)
- [ ] CTA placement at Z-pattern terminal point (bottom-right of flow)

## Forms

- [ ] Placeholder shows format example, not just repeating label
- [ ] Correct input types used (number picker for integers, etc.)
- [ ] Social login above email/password
- [ ] Progress bar shown for multi-step forms
- [ ] Inline validation (errors shown per field, not only on submit)
- [ ] Form preserves user input on error
- [ ] Error messages are specific and tell user what to do

## Pricing

- [ ] Recommended plan highlighted with ≥2 attributes (color + size + shadow)
- [ ] "Most popular" / "Best value" badge on recommended plan
- [ ] Price anchoring visible (crossed-out higher price or comparison)
- [ ] Feature comparison clearly differentiates tiers
- [ ] CTA on each plan is specific ("Start Pro Trial" not "Choose Plan")

## Dangerous Actions

- [ ] Delete / destructive actions use ghost/text style (not primary button)
- [ ] Confirmation dialog with specific copy ("Delete 'Project Name'")
- [ ] Undo option offered where technically possible
- [ ] Warning color (red/orange) used sparingly and only for actual danger

## Empty States

- [ ] Empty states have: icon + headline + description + CTA
- [ ] Templates offered instead of blank canvas
- [ ] Empty state CTA leads directly to the creation flow

## Accessibility

- [ ] Color is never the only differentiator
- [ ] All icons have text labels (especially on mobile)
- [ ] Touch targets ≥ 44×44px
- [ ] Focus states visible on all interactive elements
- [ ] Contrast ratio ≥ 4.5:1 for body text
- [ ] Alt text on all meaningful images

## Mobile

- [ ] Primary CTAs in thumb zone (lower half of screen)
- [ ] Hover-only tooltips replaced with tap-reveal ❓ icons
- [ ] No content requiring horizontal scroll (except deliberate carousels)
- [ ] Swipe gestures have visible button fallback

## Trust & Social Proof

- [ ] Trust signals placed adjacent to CTA (not buried)
- [ ] Testimonials specific (name, company, real outcome)
- [ ] Social proof uses real numbers ("12,847 users", not "thousands")
- [ ] Security/privacy indicators near data-sensitive inputs

## UX Copy

- [ ] No generic error messages ("Error occurred")
- [ ] Button copies describe specific actions
- [ ] No double negatives
- [ ] Loading states show estimated time or progress
- [ ] Success states are celebratory and confirm what happened
- [ ] Onboarding copy is encouraging, not clinical

## Scroll & Attention Flow

- [ ] Page prompts scrolling (partial next section visible)
- [ ] Whitespace used to create breathing room and guide eye
- [ ] Visual weight leads user from hero → value props → social proof → CTA
- [ ] Charts use appropriate type (bar for discrete, line for continuous)

---

## Quick Wins (High Impact, Low Effort)

1. Add "No credit card required" under your CTA button
2. Make recommended pricing plan `scale(1.05)` with glow shadow
3. Replace "Submit" with a specific action verb
4. Add icons to all navigation items
5. Cap paragraph width at `max-width: 65ch`
6. Change selected item state to background-color fill (not just border)
7. Make delete buttons ghost style with 70% opacity
8. Add skeleton loading states instead of spinners
9. Show the next section peeking at the bottom of the hero
10. Put trust signals (user count, "free forever") directly below the CTA

---

## Score Your UI (1 point each)

**0–15:** Major issues. Start with hierarchy + CTA copy.
**16–25:** Solid foundation. Focus on conversion details + copy.
**26–35:** Well-designed. Polish accessibility + mobile.
**36–40:** Excellent. Ship it.
