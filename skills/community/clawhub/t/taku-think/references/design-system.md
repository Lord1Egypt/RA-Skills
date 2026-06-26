# Design System Mode (UI-Heavy Projects)

A sub-mode within Design mode. Only activates when the user says "design system", "brand identity", "visual identity", "design tokens", or the project explicitly needs aesthetic direction. For most backend/CLI/API projects, this section never triggers.

## When to Activate

Trigger this mode when ANY of these are true:

- The user explicitly mentions "design system", "visual identity", "brand", or "design tokens"
- The project is UI-heavy and needs consistent visual language across multiple pages/components
- The user asks "what should this look like?" about a web or mobile project with no existing design system
- A new project needs UI direction before component implementation begins

Do NOT activate when:
- The project already uses an established design system (e.g., Material UI, Ant Design) without customization
- The request is purely backend, CLI, API, or infrastructure

---

## Phase 1: Product Context

Gather foundational context before making any visual decisions.

**Checklist:**

- [ ] **Target audience:** Who are the primary users? (Developers, consumers, enterprise, children, etc.)
- [ ] **Core emotion:** What should users feel? Pick 1-2 from: trust, speed, delight, calm, authority, creativity, warmth
- [ ] **Competitive set:** Identify 3-5 products the user admires or competes with
- [ ] **Anti-patterns:** What visual styles should be avoided? (e.g., "no gradients", "not corporate-looking")
- [ ] **Constraints:** Dark mode required? RTL support? Accessibility level (AA/AAA)? Minimum contrast ratio?
- [ ] **Platform:** Web only? Mobile? Both? Print?

**Output:** 3-5 sentence summary of the product's visual direction.

---

## Phase 2: Competitive Research

For each competitor, extract one actionable insight.

**Checklist:**

- [ ] For each competitor: one thing done well (steal the principle, not the exact implementation)
- [ ] For each competitor: one thing done poorly (avoid the trap)
- [ ] Identify common patterns across competitors (e.g., "all use sans-serif at similar scales")
- [ ] Note any unique differentiator worth adopting

**Output:** A table with columns: Competitor | One good thing | One bad thing | Principle to adopt.

**If web search is available:** Look at the competitor's actual site/app. If not, work from the user's description.

---

## Phase 3: Full Proposal

Present concrete design decisions. No vague language — every choice is specific and implementable.

### Aesthetic Direction

- Name the specific visual language (e.g., "Swiss grid minimalism", "Japanese editorial", "Material-inspired utility")
- Provide 2-3 reference words that anchor the feel
- State what this is NOT (e.g., "not playful, not decorative")

### Typography

**Checklist:**

- [ ] **Primary typeface:** Named specifically (no "system-ui" or "Inter/Roboto" as primary unless the user explicitly chose them)
- [ ] **Secondary typeface:** If applicable (code blocks, captions, etc.)
- [ ] **Size scale:** Define each step (e.g., `xs: 12px, sm: 14px, base: 16px, lg: 18px, xl: 24px, 2xl: 32px, 3xl: 48px, 4xl: 64px`)
- [ ] **Heading/body contrast ratio:** Must be ≥ 1.5x (e.g., heading 24px / body 16px = 1.5x)
- [ ] **Line heights:** Define for body (typically 1.5-1.7) and headings (typically 1.2-1.4)
- [ ] **Font weights used:** List which weights (e.g., regular 400, medium 500, bold 700)

### Color System

**Checklist:**

- [ ] **Primary palette:** 5-8 colors with hex values
- [ ] **Semantic colors:** success, warning, error, info — with hex values
- [ ] **Neutral scale:** 5-7 grays from lightest to darkest — with hex values
- [ ] **Dark mode variants:** At minimum, background, surface, text-primary, text-secondary
- [ ] **Contrast check:** All text/background combinations meet WCAG AA (4.5:1 body, 3:1 large text)
- [ ] **CSS custom properties format:** `--color-primary-500`, `--color-neutral-100`, etc.

### Spacing Scale

**Checklist:**

- [ ] **Base unit:** 4px or 8px (pick one, stay consistent)
- [ ] **Defined scale:** e.g., `4, 8, 12, 16, 24, 32, 48, 64, 96`
- [ ] **Usage mapping:** Which scale values map to which contexts (e.g., `8px = component internal padding, 16px = between components, 32px = between sections`)

### Layout Grid

**Checklist:**

- [ ] **Columns:** Desktop (12), tablet (8), mobile (4) — or whatever the project needs
- [ ] **Gutter width:** In px or rem
- [ ] **Max-width:** Content container max-width
- [ ] **Breakpoints:** Named and in px (e.g., `sm: 640px, md: 768px, lg: 1024px, xl: 1280px`)

### Motion

**Checklist:**

- [ ] **Duration scale:** 3 tiers (e.g., `fast: 150ms, base: 300ms, slow: 500ms`)
- [ ] **Easing curves:** Named curves (e.g., `ease-out: cubic-bezier(0.0, 0, 0.2, 1)`)
- [ ] **prefers-reduced-motion:** All animations respect this media query (reduce or remove motion)

**Output:** Complete design token table with every value specified. No "choose appropriate spacing" — provide the exact scale.

---

## Phase 4: SAFE/RISK Breakdown

Classify every design decision as SAFE or RISK.

| Decision | SAFE/RISK | Rationale |
|----------|-----------|-----------|
| Primary typeface | | |
| Color palette | | |
| Spacing scale | | |
| Grid system | | |
| Motion approach | | |

**Rules:**

- SAFE: Industry-standard, well-tested, low learning curve
- RISK: Unconventional, untested with this audience, requires buy-in
- If 3+ decisions are RISK, simplify. Replace the riskiest RISK with a safer alternative.
- Present the SAFE/RISK table to the user for review before proceeding

---

## Phase 5: Preview (Optional)

If image generation is available, create visual previews:

- [ ] Component showcase: buttons, inputs, cards, navigation at minimum
- [ ] Sample page layout using the grid and spacing system
- [ ] Dark mode variant (if dark mode is required)

If image generation is unavailable: skip this phase entirely. The token table and design decisions are sufficient.

---

## Phase 6: Output

Append a `## Design System` section to DESIGN.md containing:

```markdown
## Design System

### Aesthetic Direction
{direction, reference words}

### Typography
{typeface names, size scale, weights, line heights}

### Colors
{primary, semantic, neutral scales with hex values}
{dark mode variants}

### Spacing
{base unit, scale, usage mapping}

### Layout
{columns, gutters, max-width, breakpoints}

### Motion
{durations, easings, reduced-motion strategy}

### SAFE/RISK Summary
{table from Phase 4}
```

No placeholders. Every value is concrete and implementable.

---

## Known Pitfalls

**Proposing a design system without understanding the product.** A "clean, modern" design system was proposed for an enterprise internal tool used by data entry clerks working 8-hour shifts. The light color scheme and thin typography caused eye strain. The "modern" animations slowed down their workflow.

*Prevention:* Phase 1 (Product Context) must be completed before any visual decisions. The target audience and core emotion determine the direction. "Clean and modern" is not a direction — it's a cliché.

**Copying a competitor wholesale.** "Stripe's design is great, let's do that" produced a design system that looked exactly like Stripe for a children's education platform. The audience mismatch was obvious to everyone except the designer.

*Prevention:* Phase 2 extracts principles, not implementations. "Stripe uses clear visual hierarchy with generous whitespace" is a principle. "Use the same blue as Stripe" is copying.

**Omitting dark mode values.** The design system defined 8 colors for light mode. When dark mode was requested later, every color had to be re-evaluated for contrast against dark backgrounds. Two semantic colors failed WCAG AA in dark mode.

*Prevention:* Phase 3 Color System checklist requires dark mode variants upfront. Define them alongside light mode values, not as an afterthought.

**Token explosion.** The design system defined 48 colors, 12 font sizes, 8 font weights, and 16 spacing values. During implementation, developers couldn't decide which token to use and fell back to hardcoded values.

*Prevention:* Keep token counts small. 5-8 primary colors, 6-8 font sizes, 3-4 weights, 8-10 spacing values. More tokens = more decisions = more inconsistency.
