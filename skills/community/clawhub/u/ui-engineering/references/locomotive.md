---
name: ui-spec-locomotive
description: Detailed engineering specification for implementing "Locomotive Style" (Scrollytelling, Inertia, Brutalism).
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Locomotive

## 1. Engineering Context
**Mental Model**: "The Moving Train".
The scrolling experience is decoupled from the browser's native scroll. It has mass and inertia. Elements move at different speeds (Parallax). The layout is loose, often breaking grid lines to create visual tension.

**Key Traits**:
- **Smooth Scroll**: Native scroll is hijacked (using `Lenis` or `Locomotive Scroll`).
- **Reveal**: Images reveal with curtain effects or scale-up masks.
- **Typography**: Big, bold, mixed alignment.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS / SCSS.
- **Scroll**: `Lenis` (Modern standard) or `Locomotive Scroll`.
- **Motion**: `GSAP` (Greensock) ScrollTrigger.

## 3. Design Tokens

### 3.1 Colors (Editorial)
- **Bg**: `#D1CDC7` (Stone) or `#1A1A1A` (Dark Gray).
- **Text**: `#000000`.
- **Accent**: `#BD3F32` (Rust) or `#E3DCD2` (Paper).

### 3.2 Typography
- **Font**: `Neue Montreal` (Grotesque Sans) or `Editorial New` (Serif).
- **Scale**: `text-[12vw]` (Huge display text).
- **Mix**: Combining Italic Serif and Bold Sans in the same headline.

## 4. Component Recipes

### The "Parallax Image"
- **Wrapper**: `overflow-hidden`.
- **Image**: Scale `1.2`.
- **Effect**: `translateY` based on scroll position (`speed: -0.1`).
- **Reveal**: `clip-path` animation from bottom to top on enter.

### The "Marquee"
- **Content**: Massive text running horizontally.
- **Interaction**: Scroll speed affects marquee speed (`velocity * scroll`).

### The "Sticky Stack"
- **Behavior**: Sections stack on top of each other like cards.
- **Scale**: Previous card scales down (`scale: 0.95`) and fades to black (`brightness: 0.5`).

## 5. Interaction Patterns
- **Cursor**: Custom localized cursor (e.g., becomes "View" circle over images).
- **Transition**: Page transitions are mandatory (Cover screen slide up).
