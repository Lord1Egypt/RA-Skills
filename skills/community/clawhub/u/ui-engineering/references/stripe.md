---
name: ui-spec-stripe
description: Detailed engineering specification for implementing Stripe's precision-focused, high-trust design system.
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Stripe

## 1. Engineering Context (The "Why")
**Mental Model**: "Invisible Precision".
Stripe's design is not just "clean"; it is mathematically rigorous. The goal is to build trust through perfection. If a pixel is off, the trust is broken. Animations should feel like physically weighted objects gliding on a frictionless surface.

**Key Traits**:
- **Depth**: Use multiple layers of shadows and subtle translucency.
- **Vibrancy**: Use intentional, highly saturated accent colors against clean backgrounds.
- **Flow**: Interfaces should guide the eye with angled lines and effortless motion.

## 2. Tech Stack Recommendations
To achieve this level of fidelity, use mature and highly controllable libraries.

- **Framework**: React 18+ / Next.js (App Router)
- **Styling**: Tailwind CSS v3 (Extended Config) or Radix UI + CSS Modules.
    - *Why*: You need granular control over spacing and shadows.
- **Animation**: Framer Motion
    - *Why*: Essential for `layoutId` transitions and spring physics.
- **Icons**: Lucide React
    - *Configuration*: `strokeWidth={1.5}`, `size={16}` for UI, `size={20}` for navigational elements.

## 3. Design Tokens (The "Physics")

### 3.1 Colors (Semantic CSS Variables)
Define these in your `:root` or Tailwind `extend` config.

```css
:root {
  /* Surfaces */
  --bg-page: #F6F9FC;       /* Slightly cool gray, never pure white for page bg */
  --bg-surface: #FFFFFF;    /* Pure white for cards */
  --bg-overlay: rgba(255, 255, 255, 0.8); /* Glassmorphism base */

  /* Text - High contrast but soft */
  --text-primary: #0A2540;  /* "Downriver" - Deep navy, almost black */
  --text-secondary: #425466; /* Slate gray, cool tone */
  --text-tertiary: #8898AA; /* Subtle hints */

  /* Actions */
  --brand-accent: #635BFF;  /* "Blurple" - Primary Action */
  --brand-accent-hover: #5851D8;
  --success: #3ECF8E;
  --warning: #F5A623;
  --error: #ED5F74;
}
```

### 3.2 Typography scales
**Font Family**: `Inter` (or `Sohne` if available), falling back to system-ui.
**Characteristics**: Tight tracking for headings, open tracking for small text.

- **Display**: `font-weight: 700`, `letter-spacing: -0.02em`, `line-height: 1.1`
- **Heading**: `font-weight: 600`, `letter-spacing: -0.01em`, `line-height: 1.2`
- **Body**: `font-weight: 400`, `letter-spacing: 0`, `line-height: 1.5`
- **Caption**: `font-weight: 500`, `letter-spacing: 0.02em`, `text-transform: uppercase` (Use sparingly for labels)

### 3.3 Depth & Elevation (The "Stripe Shadow")
Stripe shadows are never single-layer. They are multi-layered to create realistic diffusion.

```css
/* Tailwind config suggestion */
{
  boxShadow: {
    'stripe-sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    'stripe-md': '0 4px 6px -1px rgba(50, 50, 93, 0.25), 0 1px 3px -1px rgba(0, 0, 0, 0.3)',
    'stripe-lg': '0 13px 27px -5px rgba(50, 50, 93, 0.25), 0 8px 16px -8px rgba(0, 0, 0, 0.3)',
    'stripe-float': '0 30px 60px -12px rgba(50, 50, 93, 0.25), 0 18px 36px -18px rgba(0, 0, 0, 0.3)',
  }
}
```

### 3.4 Shapes
- **Corner Radius**: `border-radius: 8px` (Standard), `4px` (Small inputs). Never fully rounded pills unless for specific tags.
- **Slant**: A `7deg` skew is often used for background separations.

## 4. Component Recipes

### The "Stripe Button"
A button that feels substantial and precise.

- **Base**: `bg-[#635BFF] text-white font-medium rounded-[4px] px-4 py-2`
- **Shadow**: `shadow-[0_1px_3px_0_rgba(0,0,0,0.1),0_1px_2px_-1px_rgba(0,0,0,0.1)]`
- **Hover**: `hover:-translate-y-[1px] hover:shadow-[0_4px_6px_-1px_rgba(0,0,0,0.1),0_2px_4px_-1px_rgba(0,0,0,0.06)]` (Slight lift)
- **Active**: `active:translate-y-0 active:shadow-[inset_0_1px_2px_rgba(0,0,0,0.1)]` (Physical depression)
- **Transition**: `transition-all duration-150 ease-[cubic-bezier(0.25,0.1,0.25,1)]`

### The "Glossy Card"
- **Background**: `bg-white`
- **Border**: `border border-slate-100` (Subtle container boundary)
- **Shadow**: `shadow-stripe-md`
- **Interaction**: On hover, lift slightly and increase shadow diffuse radius.

### The "Detailed Input"
- **Background**: `bg-white`
- **Border**: `border border-slate-200`
- **Shadow**: `shadow-sm` (Inner perceived depth)
- **Focus**: `ring-2 ring-[#635BFF] ring-opacity-50 border-[#635BFF]`
- **Typography**: Text should be deeply legible, using `--text-primary`. Placeholder should be `--text-tertiary`.

## 5. Animation Philosophy
Animations should use **spring physics** rather than standard easing curves where possible.
- **Stiffness**: 120
- **Damping**: 20
- **Mass**: 1
- **Result**: A tight, responsive feel that snaps into place without excessive bounce.
