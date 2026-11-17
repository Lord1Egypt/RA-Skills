---
name: ui-spec-arc
description: Detailed engineering specification for implementing Arc's soulful, textured, and customizable design system.
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Arc (The Browser Company)

## 1. Engineering Context
**Mental Model**: "Digital Craftsmanship".
Arc feels handmade. It rejects the "flatness" of the web. It embraces texture (grain), organic shapes (irregular borders), and playfulness. It is software with a pulse.

**Key Traits**:
- **Texture**: Grain/Noise is ubiquitous.
- **Squircles**: No hard corners.
- **Translucency**: The desktop wallpaper bleeds through.
- **Play**: Physics-based bouncing, confetti, and color.

## 2. Tech Stack Recommendations
- **Styling**: CSS Modules / Tailwind.
- **Effects**: SVG Filters (for noise), CSS `mix-blend-mode`.
- **Animation**: Framer Motion (Springs are loose and bouncy).

## 3. Design Tokens

### 3.1 Colors (The Boost Palette)
Arc uses **Gradients** as primary colors.
- **Space Gradient**: Linear gradient `to-b` (e.g., `#E0C3FC` to `#8EC5FC`).
- **Surface**: `rgba(255,255,255,0.9)` with backdrop blur.
- **Border**: Often colorful, not gray.

### 3.2 Typography
- **Headings**: `PP Eiko` (Serif, High contrast) or `Inter`.
- **UI**: `SF Pro` / `Inter`.
- **Trait**: Mixes Serif headings with Sans body for a "Editorial" feel.

### 3.3 Texture (The Signature)
You MUST implement the noise layer to get the Arc feel.
```css
.noise-overlay {
  position: absolute;
  inset: 0;
  background-image: url('/noise.png'); /* A static tv noise pattern */
  opacity: 0.04;
  mix-blend-mode: overlay;
  pointer-events: none;
}
```

## 4. Component Recipes

### The "Sidebar" (Translucent)
- **Bg**: `bg-white/70 dark:bg-black/60`
- **Blur**: `backdrop-blur-xl`
- **Border**: `border-r border-black/5`

### The "Squircle Container"
- **Radius**: `rounded-2xl` (approx 16px-20px).
- **Border**: `border border-transparent` (often masked with gradient).
- **Shadow**: Large, colorful diffuse shadows.

### The "Command Bar" (Spotlight)
- **Centering**: Absolute center.
- **Size**: Large and chunky. `h-[60px]`.
- **Shadow**: `shadow-2xl`.
- **Iconography**: Large, friendly icons (24px+).

## 5. Interaction Patterns
- **Overshoot**: When scrolling or opening modals, use a spring curve that overshoots slightly and settles (bouncy).
- **Hover**: Elements scale up (`scale-105`) rather than just changing color.
