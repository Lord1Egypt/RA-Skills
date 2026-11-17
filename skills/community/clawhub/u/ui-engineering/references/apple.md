---
name: ui-spec-apple
description: Detailed engineering specification for implementing Apple's Human Interface Guidelines (HIG) design system.
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Apple (HIG)

## 1. Engineering Context (The "Why")
**Mental Model**: "Premium Glass".
Apple's design is about content deference. The UI retreats. Materials (Blur) providing context. It is premium, refined, and fluid. The boundary between software and hardware disappears using full-bleed layouts and physics-based gestures.

**Key Traits**:
- **Materials**: Frosted glass (Backdrop Blur) is the defining texture.
- **Fluidity**: 1:1 gesture tracking.
- **Continuity**: Smooth corners (Squircle) and refined typography.

## 2. Tech Stack Recommendations
- **Framework**: React / Next.js
- **Styling**: Tailwind CSS + Custom Utilities (for Squircles and Blurs).
- **Animation**: Framer Motion (Spring Physics are mandatory).
- **Icons**: SF Symbols (Exported as SVG) or Lucide with rounded terminals.

## 3. Design Tokens (The "Physics")

### 3.1 Colors (System Colors)
Apple uses specific semantic colors that adapt to Light/Dark mode automatically.

```css
:root {
  /* Materials */
  --material-regular: rgba(255, 255, 255, 0.8); /* With Backdrop Blur */
  --material-thick: rgba(255, 255, 255, 0.95);
  --material-chrome: rgba(255, 255, 255, 0.5);

  /* Backgrounds */
  --bg-system: #F2F2F7; /* Light Mode Grouped BG */
  --bg-card: #FFFFFF;

  /* Typography */
  --label-primary: #000000;
  --label-secondary: rgba(60, 60, 67, 0.6);
  --label-tertiary: rgba(60, 60, 67, 0.3);

  /* Tints */
  --tint-blue: #007AFF;
}

.dark {
  --bg-system: #000000;
  --bg-card: #1C1C1E;
  --separator: #38383A;
  --label-primary: #FFFFFF;
  --label-secondary: rgba(235, 235, 245, 0.6);
}
```

### 3.2 Typography scales
**Font Family**: `SF Pro Display` (Headings) / `SF Pro Text` (Body).
**Fallback**: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto...`

*Crucial Implementation Detail*: Apple fonts use variable tracking.
- **Large Title** (34px): `tracking-tight` (-0.02em)
- **Body** (17px): `tracking-normal` (-0.01em)
- **Caption** (12px): `tracking-wide` (0.02em) -- Important! Small text needs room.

### 3.3 Surfaces & Blur
The "Frosted Glass" effect is key.
- **CSS**: `backdrop-filter: blur(20px) saturate(180%) bg-white/70`
- **Usage**: Sidebars, Modals, Sticky Headers.

## 4. Component Recipes

### The "Squircle Card"
Apple does not use standard border-radius. They use "Continuous Curvature" (Superellipse).
- **Web Implementation**: Since CSS `border-radius` is imperfect, use `clip-path` for large elements or `mask-image` for complex ones if absolute fidelity is needed.
- **Standard Approximation**: `rounded-[18px]` or `rounded-[22px]`.
- **Bg**: `bg-white dark:bg-[#1C1C1E]`
- **Shadow**: `shadow-sm` (Very subtle, diffuse).

### The "List Item" (Grouped)
- **Container**: `bg-white rounded-[10px] mx-4 overflow-hidden`
- **Item**: `h-[44px] flex items-center px-4 border-b border-[#3C3C43]/20 last:border-0`
- **Text**: `text-[17px] text-[--label-primary]`

### The "Segmented Control"
- **Container**: `bg-[#767680]/12 p-[2px] rounded-lg h-[32px]`
- **Thumb**: `bg-white shadow-sm rounded-[6px] h-full` (Use Framer Motion `layoutId` to slide this thumb).

## 5. Interaction Patterns
- **Scale on Touch**: Distinctive `active:scale-95` or `active:scale-97` on almost all tappable elements.
- **Springs**: Use `type: "spring", stiffness: 300, damping: 30` for snappy but realistic UI movement.
