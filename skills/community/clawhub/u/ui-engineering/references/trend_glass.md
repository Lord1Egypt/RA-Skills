---
name: ui-spec-trend-glass
description: Detailed engineering specification for implementing "Glass OS" trend (Vision Pro, Spatial UI, Frost).
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Glass OS

## 1. Engineering Context
**Mental Model**: "The HUD".
Heavily influenced by macOS and visionOS. The interface is a set of floating layers of glass. Depth is communicated via shadow and blur intensity, not solid colors. There is barely any "solid" background colors.

**Key Traits**:
- **Translucency**: Everything is `bg-white/10` or `bg-black/20`.
- **Border**: 1px solid white/20 border is mandatory to define edges.
- **Vibrancy**: Use of `backdrop-filter: saturate(180%)` to make colors pop behind the glass.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS.
- **Backdrop**: CSS `backdrop-filter` is the engine.
- **3D**: Often paired with Spline 3D objects floating behind the glass.

## 3. Design Tokens

### 3.1 Colors (Crystal)
- **Bg**: High-res abstract wallpaper (Mesh or dark gradient).
- **Glass Light**: `bg-white/10 border-white/20 text-white`.
- **Glass Dark**: `bg-black/40 border-white/10 text-white`.
- **highlight**: `#FFFFFF`.

### 3.2 Typography
- **Font**: `SF Pro Display` (The Apple feel).
- **Weight**: Thin or Light weights work well on dark glass.

## 4. Component Recipes

### The "Vision Card"
- **Effect**: `bg-white/10 backdrop-blur-2xl border border-white/10 shadow-2xl`.
- **Hover**: `bg-white/20` (Lighting up).
- **Shape**: `rounded-[32px]`.

### The "Depth Dock"
- **Container**: Floating capsule at bottom.
- **Style**: Heavier blur (`backdrop-blur-3xl`) to separate from background.
- **Icons**: Magnification effect on hover.

### The "Shining Border"
- **Technique**: A pseudo-element linear gradient that rotates behind the border mask.
- **Result**: A "light" travels around the edge of the glass card.

## 5. Interaction Patterns
- **Parallax Tilt**: Cards tilt slightly toward the mouse (`vanilla-tilt.js`).
- **Focus**: Active window is clear, inactive ones blur further.
