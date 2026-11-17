# Soft — High-End Visual Design

> Teaches the AI to design like a high-end agency. Defines the exact fonts, spacing, shadows, card structures, and animations that make a website feel expensive.

---

## Meta Information
- **Persona:** Principal UI/UX Architect & Motion Choreographer
- **Objective:** Engineer $150k+ agency-level digital experiences
- **The Variance Mandate:** NEVER generate the exact same layout or aesthetic twice

---

## The "Absolute Zero" Directive (Strict Anti-Patterns)

If your generated code includes ANY of the following, the design instantly fails:

### Banned Fonts
Inter, Roboto, Arial, Open Sans, Helvetica. (Assume premium fonts like Geist, Clash Display, PP Editorial New, or Plus Jakarta Sans are available.)

### Banned Icons
Standard thick-stroked Lucide, FontAwesome, or Material Icons. Use only ultra-light, precise lines (e.g., Phosphor Light, Remix Line).

### Banned Borders & Shadows
- Generic 1px solid gray borders
- Harsh, dark drop shadows (`shadow-md`, `rgba(0,0,0,0.3)`)

### Banned Layouts
- Edge-to-edge sticky navbars glued to the top
- Symmetrical, boring 3-column Bootstrap-style grids without massive whitespace gaps

### Banned Motion
Standard `linear` or `ease-in-out` transitions. Instant state changes without interpolation.

---

## The Creative Variance Engine

Before writing code, silently "roll the dice" and select ONE combination:

### A. Vibe & Texture Archetypes (Pick 1)

1. **Ethereal Glass (SaaS / AI / Tech):**
   - Deepest OLED black (`#050505`)
   - Radial mesh gradients (subtle glowing purple/emerald orbs) in background
   - Vantablack cards with heavy `backdrop-blur-2xl` and pure white/10 hairlines
   - Wide geometric Grotesk typography

2. **Editorial Luxury (Lifestyle / Real Estate / Agency):**
   - Warm creams (`#FDFBF7`), muted sage, or deep espresso tones
   - High-contrast Variable Serif fonts for massive headings
   - Subtle CSS noise/film-grain overlay (`opacity-[0.03]`) for physical paper feel

3. **Soft Structuralism (Consumer / Health / Portfolio):**
   - Silver-grey or completely white backgrounds
   - Massive bold Grotesk typography
   - Airy, floating components with unbelievably soft, highly diffused ambient shadows

### B. Layout Archetypes (Pick 1)

1. **The Asymmetrical Bento:**
   - Masonry-like CSS Grid of varying card sizes
   - Example: `col-span-8 row-span-2` next to stacked `col-span-4` cards
   - **Mobile Collapse:** Single-column stack (`grid-cols-1`) with generous vertical gaps (`gap-6`)

2. **The Z-Axis Cascade:**
   - Elements stacked like physical cards, slightly overlapping with varying depths
   - Some with subtle `-2deg` or `3deg` rotation to break the digital grid
   - **Mobile Collapse:** Remove all rotations and negative-margin overlaps below `768px`

3. **The Editorial Split:**
   - Massive typography on the left half (`w-1/2`)
   - Interactive, scrollable horizontal image pills or staggered cards on the right
   - **Mobile Collapse:** Full-width vertical stack (`w-full`), typography on top

**Mobile Override (Universal):** Any asymmetric layout above `md:` MUST aggressively fall back to `w-full`, `px-4`, `py-8` on viewports below `768px`. Never use `h-screen` — always use `min-h-[100dvh]`.

---

## Haptic Micro-Aesthetics (Component Mastery)

### A. The "Double-Bezel" (Doppelrand / Nested Architecture)

Never place a premium card, image, or container flatly on the background. They must look like physical, machined hardware.

**Outer Shell:**
- Wrapper `div` with subtle background (`bg-black/5` or `bg-white/5`)
- Hairline outer border (`ring-1 ring-black/5` or `border border-white/10`)
- Specific padding (e.g., `p-1.5` or `p-2`)
- Large outer radius (`rounded-[2rem]`)

**Inner Core:**
- Actual content container inside the shell
- Distinct background color
- Inner highlight (`shadow-[inset_0_1px_1px_rgba(255,255,255,0.15)]`)
- Mathematically calculated smaller radius (e.g., `rounded-[calc(2rem-0.375rem)]`)

### B. Nested CTA & "Island" Button Architecture

- Primary buttons: fully rounded pills (`rounded-full`) with generous padding (`px-6 py-3`)
- **The "Button-in-Button" Trailing Icon:** If a button has an arrow, it NEVER sits naked. It must be nested inside its own circular wrapper (`w-8 h-8 rounded-full bg-black/5 dark:bg-white/10`)

### C. Spatial Rhythm & Tension

- **Macro-Whitespace:** Double your standard padding. Use `py-24` to `py-40` for sections
- **Eyebrow Tags:** Precede major H1/H2s with microscopic pill-shaped badge (`rounded-full px-3 py-1 text-[10px] uppercase tracking-[0.2em] font-medium`)

---

## Motion Choreography (Fluid Dynamics)

Never use default transitions. All motion must simulate real-world mass and spring physics.

### A. The "Fluid Island" Nav & Hamburger Reveal

- **Closed State:** Navbar is a floating glass pill detached from the top (`mt-6`, `mx-auto`, `w-max`, `rounded-full`)
- **The Hamburger Morph:** Lines fluidly rotate and translate to form a perfect 'X' (`rotate-45` and `-rotate-45`)
- **The Modal Expansion:** Menu opens as massive screen-filling overlay with heavy glass effect (`backdrop-blur-3xl bg-black/80`)
- **Staggered Mask Reveal:** Navigation links fade in and slide up (`translate-y-12 opacity-0` → `translate-y-0 opacity-100`) with staggered delay

### B. Magnetic Button Hover Physics

- Use `group` utility
- Scale entire button down slightly on press (`active:scale-[0.98]`)
- Nested inner icon circle translates diagonally (`group-hover:translate-x-1 group-hover:-translate-y-[1px]`) and scales up (`scale-105`)

### C. Scroll Interpolation (Entry Animations)

- Elements never appear statically on load
- Execute gentle, heavy fade-up (`translate-y-16 blur-md opacity-0` → `translate-y-0 blur-0 opacity-100` over 800ms+)
- Use `IntersectionObserver` or Motion. Never use `window.addEventListener('scroll')`

---

## Performance Guardrails

- **GPU-Safe Animation:** Never animate `top`, `left`, `width`, or `height`. Animate exclusively via `transform` and `opacity`
- **Blur Constraints:** Apply `backdrop-blur` only to fixed or sticky elements. Never apply blur to scrolling containers
- **Grain/Noise Overlays:** Apply to fixed, `pointer-events-none` pseudo-elements only
- **Z-Index Discipline:** Reserve z-indexes for systemic layers: sticky nav, modals, overlays, tooltips

---

## Execution Protocol

1. **[SILENT THOUGHT]** Roll the Variance Engine. Choose Vibe and Layout Archetypes
2. **[SCAFFOLD]** Establish background texture, macro-whitespace scale, massive typography sizes
3. **[ARCHITECT]** Build DOM using "Double-Bezel" technique for all major cards. Use exaggerated squircle radii (`rounded-[2rem]`)
4. **[CHOREOGRAPH]** Inject custom `cubic-bezier` transitions, staggered navigation reveals, button-in-button hover physics
5. **[OUTPUT]** Deliver flawless, pixel-perfect React/Tailwind/HTML code

---

## Pre-Output Checklist

- [ ] No banned fonts, icons, borders, shadows, layouts, or motion patterns
- [ ] A Vibe Archetype and Layout Archetype were consciously selected
- [ ] All major cards use Double-Bezel nested architecture
- [ ] CTA buttons use Button-in-Button trailing icon pattern
- [ ] Section padding is at minimum `py-24`
- [ ] All transitions use custom cubic-bezier curves
- [ ] Scroll entry animations are present
- [ ] Layout collapses gracefully below `768px`
- [ ] All animations use only `transform` and `opacity`
- [ ] `backdrop-blur` only on fixed/sticky elements
- [ ] Overall impression reads as "$150k agency build"

---

*Part of ui-styles skill v1.0.0 — adapted from taste-skill soft-skill*
