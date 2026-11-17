---
name: ui-spec-nike
description: Detailed engineering specification for implementing Nike's "Podium" design system (Motion, Energy, Bold).
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Nike

## 1. Engineering Context
**Mental Model**: "Kinetic Energy".
Nike's digital presence is built to move. It is not static. Typography is massive and often italicized (forward motion). Layouts are sparse to let high-energy photography dominate. The interface feels like a premium sports car dashboard.

**Key Traits**:
- **Motion First**: Transitions are aggressive (`cubic-bezier(0.16, 1, 0.3, 1)`).
- **Helvetica Dominance**: Heavy reliance on `Helvetica Now`.
- **Monochrome Foundation**: Black and White strictly, allowing product colors to pop.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS.
- **Motion**: `GSAP` (Greensock) is standard for Nike's high-end marketing sites. `Framer Motion` for apps.
- **Video**: Heavy use of background looping video (`<video playsinline autoplay muted loop>`).

## 3. Design Tokens

### 3.1 Colors (The Arena)
- **Bg**: `#FFFFFF` (Retail) or `#111111` (Brand/SNKRS).
- **Text**: `#111111` (Black) or `#F5F5F5` (White).
- **Accent**: `#FA5400` (Nike Orange - Legacy), `#F6F6F6` (Light Gray backgrounds).
- **Sale**: `#D30005` (Red).

### 3.2 Typography
- **Font**: `Helvetica Now Display` / `Trade Gothic` (for campaigns).
- **Weight**: `ExtraBlack` or `Medium` (Avoid Regular).
- **Style**: Text is often uppercase and tightly tracked.

## 4. Component Recipes

### The "Product Wall" (Grid)
- **Grid**: `grid-cols-2 md:grid-cols-3`.
- **Card**: `bg-[#F6F6F6] aspect-[4/5] relative group`.
- **Hover**: Image swap (Lifestyle -> Product isolation).
- **Typography**: Brief, bold titles below the image.

### The "Campaign Hero"
- **Height**: `h-screen`.
- **Content**: Full-bleed video.
- **Text Overlay**: Giant white text, centered, with `mix-blend-mode: difference` (sometimes).
- **Button**: White pill button, black text, hover scale.

### The "SNKRS Button" (Hype)
- **Bg**: Black.
- **Text**: White.
- **Shape**: `rounded-full` (Capsule).
- **State**: Loading state changes text to "Pending..." with a custom spinner.

## 5. Interaction Patterns
- **Parallax**: Subtle vertical parallax on text over images.
- **Cursor**: Custom cursors on campaign sites (e.g., "View" circle).
- **Horizontal Scroll**: Horizontal snapping lists for shoes on mobile (`snap-x snap-mandatory`).
