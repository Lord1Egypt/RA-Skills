---
name: ui-design-tips
description: "Apply practical UI/UX design principles to improve user interfaces, landing pages, web apps, and components. Use when asked to review, critique, or improve UI design; suggest design improvements for buttons, forms, headers, cards, menus, color usage, visual hierarchy, pricing pages, or any UI element; apply UX laws (Fitts's Law, Gutenberg Principle, Hick's Law, Jakob's Law, etc.); fix accessibility issues; design better onboarding, error messages, empty states, navigation, micro-interactions, or UX copy; or answer questions about UI/UX best practices. Covers visual hierarchy, CTA optimization, color usage, typography, whitespace, alignment, form design, mobile UX, dangerous actions, empty states, onboarding, UX writing, error handling, trust signals, conversion optimization, and more."
---

# UI Design Tips

Practical UI/UX knowledge distilled from real-world product testing (Jim Raptis / uidesign.tips) plus extended UX principles. Apply these when reviewing or improving any interface.

## Core Philosophy

- **Never leave things to user imagination** — make actions explicit and obvious
- **Use multiple attributes** to distinguish elements (color + icon + size, never color alone)
- **Prioritize the primary action** — dangerous/secondary actions must never compete visually
- **Users hate surprises** — copy and microcopy must eliminate all ambiguity
- **UX > Conversions** — 10 annoyed users outweigh 1 accidental conversion

---

## 1. Visual Hierarchy

The #1 design lever. Everything else builds on this.

**Hacks:**
- Reduce opacity of secondary info (50–70%)
- Bold font-weight for primary content emphasis
- Type scale ×1.25: 40px title → 32px subtitle → 25px H3 → 16px body
- Left-align for LTR readability (not centered)
- Group related elements (proximity = relationship)
- Use size contrast: make primary elements noticeably bigger

**Perfect Header formula:**
1. Strong font-weight on title
2. ×1.25 type scale
3. Lower contrast (opacity ~70%) for subtitle
4. Line-height 1.5–1.7 for body text
5. Left-aligned

---

## 2. CTA & Conversion Optimization

- **Always have a CTA above the fold** — many users never scroll
- **One primary CTA per screen** — multiple competing styles cause decision paralysis
- **Button copy = action verb** — "Start Creating Free" beats "Submit"
- **Eliminate pre-click anxiety** — add "No credit card required" / "Free forever" near the CTA
- **Gutenberg Principle:** Eyes travel Z-path (top-left → top-right → bottom-left → bottom-right). Place CTA at the terminal point (bottom-right)
- **Prompt scrolling** — show a glimpse of the next section to signal there's more
- **Direct attention with media** — people follow lines of sight; point characters toward CTA

---

## 3. Color Usage

- **Brand color = accent only** — highlight 1–2 elements maximum; everything else uses tints/shades
- **Never rely on color alone** — always pair with shape/icon/label (8% of men are color-blind)
- When highlighting pricing plans: use **color + size + elevation (shadow)** — minimum 2 attributes

---

## 4. Pricing Pages

- **Highlight the recommended plan** with ≥2 design attributes: color + shadow + scale
- Example: `transform: scale(1.04)` + distinct border color + box-shadow glow
- This guides users to the popular plan and reduces decision fatigue (Hick's Law)

---

## 5. Layout & Alignment

**Aligning uneven elements:** Set same width for all items using the widest element's width.

**Avoid full-width paragraphs:** Limit to 500–700px. CSS: `max-width: 65ch`

**Padding on rounded cards:** Use double padding on the non-rounded edges (text/icon side)

**Border radius consistency:** Outer radius = 2× Inner radius

---

## 6. Cards & Clickability

- **Make cards obviously clickable** — add explicit CTA button; hover effects alone aren't enough
- Never rely on user experience to infer clickability — state it explicitly

---

## 7. Navigation & Menus

- **Add icons next to every menu item** — visual identification without reading
- **Highlight the active tab** clearly (background change, not just color)
- **Whitespace over dividers** between menu sections — cleaner, less cognitive load
- Only use dividers between major sections
- **Keyboard shortcuts:** Display them next to action buttons (Fitts's Law reduces memory load)
- **Dropdown menus:** Add icons to items for faster visual scanning

---

## 8. Forms & Inputs

- **Placeholder text = guidance**, not label repetition — show format examples
- **Choose correct input type** — number picker for integers, not text field
- **Predefined values** reduce errors (country selectors, date pickers)
- For small integer ranges (cart qty 1–10): use −/+ buttons
- **Social login above email/password** for higher conversion; always provide email fallback
- **Inline validation** — show errors as user types, not only on submit
- **Group related fields** — billing info together, personal info together
- **Progress indicators** for multi-step forms — show "Step 2 of 4"

---

## 9. Dangerous Actions

- **De-emphasize destructive actions** with multiple attributes: ghost style + small font + low opacity + placement at end
- **Always validate deletions** — inline or popup confirmation; never silent deletes
- **Button copy = specific action**: "Delete 'Project Alpha'" beats "Delete" beats "Yes"
- Consider **undo** as an alternative to confirmation dialogs (less friction, same safety)
- Never style a destructive action as a primary button

---

## 10. Empty States

- **Never show a blank screen** — empty states are onboarding opportunities
- Offer **pre-made templates** to let users experience value immediately
- Include: illustration/icon + headline + short description + primary CTA + secondary "learn more" link
- Show **sample content** when possible so users understand what they're working toward

---

## 11. Onboarding & UX Copy

- **Inform users of the next step** — never make them guess
- Eliminate anxiety-triggering words — "Reserve" → "Try Free"; add "Cancel anytime"
- **Microcopy near CTAs** is as important as the button label itself
- **Progress indicators** help users commit to multi-step flows (they've already started)
- Pre-fill forms with smart defaults to reduce friction

---

## 12. Error Messages

- **Specific, not generic** — "Email is already in use" not "Invalid input"
- **Actionable** — tell the user what to do next: "Try a different email or log in instead"
- **Friendly tone** — never blame the user ("You entered..." → "We couldn't find...")
- **Inline, not modal** — show errors near the field that caused them
- **Preserve user input** — never clear the form on error

---

## 13. Avatars & Media

- **Transparent PNG avatars:** Add background color + subtle border matching app background
- **Use media to direct attention** — faces/characters should look toward the CTA
- **Avatar consistency:** Apply the same border/background treatment to all avatars

---

## 14. Mobile UX

- **Hover tooltips don't work on mobile** — add a tappable ❓ icon that shows tooltip on tap
- **Thumb Zone:** Place primary CTAs within easy thumb reach (bottom center / lower areas)
- **Touch targets ≥ 44×44px** — small targets cause misclicks and frustration
- Don't rely on hover states for critical functionality
- **Swipe gestures:** Always provide a visible alternative (swipe to delete = also show a delete button)

---

## 15. Accessibility

- **Never use color as the only differentiator** — add icon, shape, or label
- **Contrast ratio ≥ 4.5:1** for normal text, ≥ 3:1 for large text (WCAG AA)
- **Icon labels** are mandatory on mobile (no hover to discover meaning)
- **Focus states** must be visible — don't remove browser outlines without replacing them
- **Alt text** for all meaningful images

---

## 16. Charts & Data

- **Bar chart** for limited/discrete categories (monthly data, categories)
- **Line chart** for continuous time-series data — don't use for discrete values (introduces false intermediate data)
- Label axes clearly; don't make users guess units

---

## 17. Selected & Interactive States

- **Background color change** is the strongest signal for selected items — more accessible than border alone
- Show selected state at a glance — don't make users search for what they chose
- **Hover states** must be meaningful, not decorative

---

## 18. Trust & Social Proof

- Place trust signals **near the CTA** (not buried in footer)
- Trust signals: "No credit card required" / testimonials / user counts / security badges
- **Social proof proximity** — testimonials directly under the offer they're validating
- Show real numbers ("12,847 users") over vague claims ("thousands of users")

---

## 19. UX Writing Checklist

| ❌ Avoid | ✅ Use instead |
|---------|--------------|
| "Submit" | "Start Free Trial" / "Create My Account" |
| "Yes" / "No" | "Delete Project" / "Keep It" |
| "Error occurred" | "We couldn't save your work. Try again?" |
| "Invalid input" | "Email must include @" |
| "Are you sure?" | "This will permanently delete 'Project Name'" |

---

---

## 20. Micro-Interactions & Button States (from uiverse.io)

Every interactive element needs **3 states minimum:**
1. **Default** — resting appearance
2. **Hover** — `translateY(-2px)` + glow/shadow increase
3. **Active/Press** — `translate(2px, 2px)` reverses lift (feels physical)

**Missing active state = cheap, broken feel.**

**Navigation button pattern:**
- Each item gets its own accent color (icon + text change on hover)
- Icons always visible, label always present (no icon-only nav)

**Button animation timing rules:**
- Under 300ms = fast and responsive
- `ease-out` for entrances, `ease-in` for exits, never `linear` (except spinners)
- Always add `@media (prefers-reduced-motion: reduce)` wrapper

**Loading states:**
- Skeleton screens (shimmer) > spinners for content areas
- Button loading state: inline spinner after label text, `pointer-events: none`

**Neon/glow effects (dark UI):**
```css
/* Focus ring */
.input:focus { box-shadow: 0 0 0 3px rgba(177,79,255,0.2); }
/* Hover intensify */
.btn:hover { box-shadow: 0 0 30px rgba(177,79,255,0.5); }
```

**CSS custom properties for consistent theming:**
```css
:root {
  --accent: #b14fff;
  --accent-rgb: 177, 79, 255;
  --radius: 12px;          /* card outer */
  --radius-sm: 6px;         /* card inner → outer = 2× inner rule */
}
```

For full CSS patterns and component code → `references/micro-interactions.md`

---

---

## 21. Color System by Product Type

Choose palette based on industry psychology — not personal preference:

| Category | Primary | CTA | Background |
|---|---|---|---|
| SaaS / Tech | Blue #2563EB | Orange #F97316 | Light #F8FAFC |
| Gaming / Cyberpunk | Purple #7C3AED | Rose #F43F5E | Dark #0F0F23 |
| AI Products | Purple #7C3AED | Cyan #06B6D4 | Soft #FAF5FF |
| Fintech / Crypto | Gold #F59E0B | Purple #8B5CF6 | Dark #0F172A |
| Healthcare | Cyan #0891B2 | Green #059669 | Light #ECFEFF |
| Creative Agency | Pink #EC4899 | Cyan #06B6D4 | Soft #FDF2F8 |
| E-commerce Luxury | Black #1C1917 | Gold #CA8A04 | Off-white #FAFAF9 |
| Video Streaming | Black #0F0F23 | Red #E11D48 | Pure #000000 |
| Food / Restaurant | Red #DC2626 | Gold #CA8A04 | Warm #FEF2F2 |

**Industry rules:**
- Healthcare/Medical: NEVER neon colors; ALWAYS calm + WCAG AAA
- Finance/Banking: NEVER playful; ALWAYS security badges + dark navy
- Gaming: NEVER minimal; ALWAYS dark mode + neon/3D effects
- Kids: NEVER dark; ALWAYS rounded + bright pastels + large touch targets

Full database (96 product types) → `references/design-systems-pro.md`

---

## 22. UI Style Systems (Choose by Context)

**Glassmorphism** — Modern SaaS, financial, lifestyle
```css
backdrop-filter: blur(15px);
background: rgba(255,255,255,0.15);
border: 1px solid rgba(255,255,255,0.2);
```

**Neubrutalism** — Gen Z brands, creative, startups
```css
border: 3px solid #000;
box-shadow: 5px 5px 0 #000;  /* hard offset, no blur */
/* Hover: translate(-4px, -4px) + box-shadow: 9px 9px 0 #000 */
```

**Bento Grid** (Apple-style) — Dashboards, product features
```css
display: grid;
grid-template-columns: repeat(4, 1fr);
grid-auto-rows: 200px;
gap: 16px;
/* Cards: border-radius: 24px; hover: scale(1.02) */
```

**Cyberpunk** — Gaming, crypto, entertainment
```css
background: #0D0D0D;
color: #00FF00;  /* or #FF00FF / #00FFFF */
text-shadow: 0 0 10px currentColor;
font-family: monospace;
/* Add scanlines via ::before repeating-linear-gradient */
```

**Claymorphism** — Kids, education, SaaS onboarding
```css
border-radius: 16-24px;
border: 3-4px solid rgba(0,0,0,0.1);
box-shadow: inset -2px -2px 8px rgba(255,255,255,0.5), 4px 4px 8px rgba(0,0,0,0.2);
/* Bounce: cubic-bezier(0.34, 1.56, 0.64, 1) */
```

For all 60+ styles → `references/design-systems-pro.md`

---

## 23. Typography Selection Guide

| Vibe | Heading | Body |
|---|---|---|
| Tech Startup | Space Grotesk | DM Sans |
| Gaming / Esports | Russo One | Chakra Petch |
| Cyberpunk / HUD | Share Tech Mono | Fira Code |
| Luxury / Fashion | Cormorant | Montserrat |
| Minimal SaaS | Inter | Inter |
| AI / Modern | Plus Jakarta Sans | Plus Jakarta Sans |
| Wellness | Lora (serif) | Raleway |
| Kids / Education | Baloo 2 | Comic Neue |
| News / Editorial | Newsreader | Roboto |
| Gen Z Bold | Anton | Epilogue |
| Crypto / Web3 | Orbitron | Exo 2 |

Chinese: `Noto Sans SC`
Japanese: `Noto Serif JP` + `Noto Sans JP`

---

## 24. Landing Page Pattern Selection

| Goal | Pattern | Key CTA Rule |
|---|---|---|
| SaaS free trial | Hero + Features + CTA | Video demo + sticky CTA |
| Lead generation | Lead Magnet + Form | ≤3 fields, preview lead magnet |
| Pricing page | 3-tier Pricing | Middle tier = "Most Popular", annual discount 20-30% |
| Brand / storytelling | Scroll Narrative | 5-7 chapters, emotional hooks |
| Event / Webinar | Event Landing | Countdown + limited seats |
| Waitlist | Waitlist Pattern | Countdown + email + social proof count |

**CTA placement rules:**
- Primary CTA: **above fold always**
- Secondary: after testimonials/social proof
- Sticky CTA: in navbar when hero scrolls out of view
- Never > 2 CTA variants visible at once

---

## 25. Design Tokens Template

```css
:root {
  /* Spacing (8px base) */
  --space-4: 16px; --space-8: 32px; --space-12: 48px; --space-16: 64px;

  /* Type Scale (1.25×) */
  --text-base: 16px;  /* body minimum */
  --text-2xl: 24px;   --text-4xl: 36px;  --text-6xl: 60px;

  /* Radius */
  --radius: 12px; --radius-lg: 16px; --radius-xl: 24px;

  /* Elevation */
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.1);
  --shadow-md: 0 10px 20px rgba(0,0,0,0.1);
  --shadow-lg: 0 20px 40px rgba(0,0,0,0.15);
  --shadow-glow: 0 0 30px rgba(var(--accent-rgb), 0.4);

  /* Z-Index */
  --z-1: 10; --z-2: 20; --z-modal: 50; --z-toast: 100;

  /* Animation */
  --duration-fast: 150ms; --duration-normal: 200ms; --duration-slow: 300ms;
  --ease-out: cubic-bezier(0.22, 1, 0.36, 1);
  --spring: cubic-bezier(0.34, 1.56, 0.64, 1);  /* bouncy press */
}
```

---

## Reference Files

- **UX Laws deep-dive:** `references/ux-laws.md`
- **UX Writing patterns:** `references/ux-writing.md`
- **Conversion checklist (40 items):** `references/conversion-checklist.md`
- **CSS micro-interactions & uiverse.io patterns:** `references/micro-interactions.md`
- **Design Systems Pro (color/typography/styles/99 UX issues):** `references/design-systems-pro.md`
