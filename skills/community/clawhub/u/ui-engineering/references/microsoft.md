---
name: ui-spec-microsoft
description: Detailed engineering specification for implementing Microsoft's Fluent Design system.
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Microsoft (Fluent)

## 1. Engineering Context (The "Why")
**Mental Model**: "Natural Light & Layered Depth".
Fluent Design is about material authenticity. It simulates light interacting with materials (Acrylic, Mica). It is productive, grounded, and dense (in a good way). It is less "floaty" than Apple, more "solid" than Google.

**Key Traits**:
- **Light**: Reveal Effects (borders lighting up on hover).
- **Material**: Mica (sampling desktop background) and Acrylic (blur).
- **Scale**: A strict 4px grid.

## 2. Tech Stack Recommendations
- **Framework**: React
- **Styling**: CSS Modules or Tailwind.
- **Special**: Use `framer-motion` for layout transitions, but CSS Grid is key for the 4px alignment.
- **Icons**: Fluent System Icons (Segoe Fluent Icons).
    - *Style*: Thin strokes, straightforward geometry.

## 3. Design Tokens

### 3.1 Colors (Neutral & Brand)
Fluent relies heavily on a "Neutral Palette" for structure.

```css
:root {
  /* Brand */
  --brand-primary: #0078D4; /* Windows Blue */
  --brand-dark: #005A9E;

  /* Neutrals (Light Mode) */
  --neutral-white: #FFFFFF;
  --neutral-gray-10: #FAF9F8;
  --neutral-gray-20: #F3F2F1;
  --neutral-gray-60: #C8C6C4; /* Borders */
  --neutral-gray-160: #323130; /* Text */

  /* Text */
  --text-primary: #201F1E;
  --text-secondary: #605E5C;
}
```

### 3.2 Typography scales
**Font Family**: `Segoe UI Variable` (Text/Display).
**Fallback**: `Segoe UI`, `sans-serif`.

- **Style**: No tracking changes like Apple. Just solid, legible weights.
- **Title**: `28px Bold`
- **Subtitle**: `20px Semibold`
- **Base**: `14px Regular` (Note: Default size is smaller than the web standard 16px. Fluent is information dense).

### 3.3 Surfaces (Materials)
**Mica Material**:
- *Spec*: Opaque, slight tint of user's wallpaper.
- *Web Sim*: `bg-[#F3F3F3] bg-opacity-90 backdrop-blur-xl`.

**Acrylic Material**:
- *Spec*: Translucent, noisy, blurred.
- *Web Sim*: `backdrop-filter: blur(30px) saturate(125%) bg-white/60`.

## 4. Component Recipes

### The "Reveal Hover" Effect (Signature)
A border or background light that follows the mouse cursor.
- **Implementation**: Requires JS to track mouse position on the container.
- **CSS**: use `radial-gradient` masked to the border.
```css
/* Simplified Web Approximation */
.card:hover {
  border-color: rgba(0,0,0,0.4); /* Darkens on hover */
}
/* Ideally use a mouse-tracking glow hook */
```

### The "Command Bar"
- **Container**: `bg-white border-b border-[#E1DFDD] h-[48px] px-2 flex items-center`
- **Item**: `h-[36px] rounded-[4px] px-3 flex items-center hover:bg-[#F3F2F1]`

### The "Corner Radius"
- **Layer**: `rounded-[8px]` (Overlays, Popups)
- **Control**: `rounded-[4px]` (Buttons, Inputs, Checkboxes)
- **Window**: `rounded-[8px]` (Windows 11 style)

## 5. Interaction Patterns
- **Connected Transitions**: Elements don't just fade; they move to their new position.
- **Parallax**: Subtle depth shifting on layered elements (Acrylic backgrounds move slower than content).
