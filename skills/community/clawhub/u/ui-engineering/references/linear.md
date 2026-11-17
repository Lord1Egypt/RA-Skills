---
name: ui-spec-linear
description: Detailed engineering specification for implementing Linear's magical, high-performance dark mode design system.
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Linear

## 1. Engineering Context
**Mental Model**: "Magical Utility".
Linear makes productivity rendering feel like a video game. It uses "Glows", "Particles", and "Shimmers" to reward user actions. The dark mode is not just black; it's a deep canvas for lighting effects.

**Key Traits**:
- **Glow**: Radial gradients behind active elements.
- **Borders**: 1px subtle, sometimes shimmering borders.
- **Micro-interactions**: Success states have flair.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS + `clsx`.
- **VFX**: Custom CSS `mask-image` for sparkles, `radial-gradient` for glows.
- **Animation**: Framer Motion (Layout transitions).

## 3. Design Tokens

### 3.1 Colors (The Deep Space)
- **Bg**: `#080808` (Almost pure black)
- **Surface**: `#161618` (Slightly lighter)
- **Border**: `#29292D` (Subtle divider)
- **Primary**: `#5E6AD2` (Indigo)
- **Success**: `#27B074` (Green)
- **Warning**: `#F36D40` (Orange)

### 3.2 Typography
- **Headings**: `Inter` (Medium/SemiBold).
- **Body**: `Inter` (Regular).
- **Spacing**: Linear uses very specific letter-spacing adjustments to make text legible on dark backgrounds.

## 4. Component Recipes

### The "Glow Card"
A background effect that follows the mouse or highlights the card.
- **CSS**:
  ```css
  background: radial-gradient(
    800px circle at var(--mouse-x) var(--mouse-y),
    rgba(255, 255, 255, 0.06),
    transparent 40%
  );
  ```

### The "Shimmer Border"
A border that looks like light is passing through it.
- **Implementation**: Mask a rotating conic gradient with a border-shape.
- **Tailwind**: `border border-transparent bg-origin-border bg-gradient-to-r from-white/10 to-white/0` (Simplified).

### The "Command Menu" (Cmd+K)
- **Backdrop**: `backdrop-blur-[2px] bg-black/50`
- **Modal**: `bg-[#18181A] border border-[#2E2E32] shadow-2xl rounded-lg`

## 5. Interaction Patterns
- **Key-Feel**: Hover states are instant. Active states have a "click" feel (scale down 0.98).
- **Optimistic**: Actions happen locally instantly. Loaders are thin top-bars, not spinners.
