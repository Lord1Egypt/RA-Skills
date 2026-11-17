---
name: ui-spec-google
description: Detailed engineering specification for implementing Google's Material Design 3 (Material You) design system.
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Google (Material 3)

## 1. Engineering Context (The "Why")
**Mental Model**: "Personalized Paper".
Material Design 3 is fluid, human, and adaptive. Unlike the "physical" paper of Material 2, MD3 is more emotional. It uses large rounded shapes, "Dynamic Color" extraction from wallpapers, and state layers (opacity) rather than just shadows to indicate interaction.

**Key Traits**:
- **Playful**: Generous curves (Pills, odd shapes).
- **Adaptive**: Colors shift based on user preference.
- **Stateful**: Dedicated state layers for hover/focus/press.

## 2. Tech Stack Recommendations
- **Framework**: React / Next.js
- **Styling**: Tailwind CSS (Requires heavy customization) OR Styled Components.
- **Animation**: Framer Motion (Essential for the "Container Transform" pattern).
- **Icons**: Material Symbols (Google Fonts)
    - *Format*: `font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24`

## 3. Design Tokens (The "Physics")

### 3.1 Colors (Tonal Palettes)
MD3 does not use single hex codes. It uses Tonal Palettes (0-100 luminosity).

```css
:root {
  /* Primary Key Color: Blue #4285F4 */
  --md-sys-color-primary: #0B57D0;
  --md-sys-color-on-primary: #FFFFFF;
  --md-sys-color-primary-container: #D3E3FD;
  --md-sys-color-on-primary-container: #041E49;

  /* Surface */
  --md-sys-color-surface: #FEF7FF;
  --md-sys-color-surface-container-low: #F7F2FA;
  --md-sys-color-surface-container-high: #ECE6F0;

  /* Outline */
  --md-sys-color-outline: #79747E;
}
```

### 3.2 Typography scales
**Font Family**: `Google Sans` (Product) or `Roboto` (System).

- **Display Large**: `57px / 64px / -0.25px`
- **Headline Medium**: `28px / 36px / 0px`
- **Body Large**: `16px / 24px / 0.5px`
- **Label Large** (Buttons): `14px / 20px / 0.1px` (`font-weight: 500`)

### 3.3 Shapes (The "Pill" Standard)
- **Full**: `border-radius: 9999px` (Buttons, Chips, Badges).
- **Large**: `border-radius: 28px` (Dialogs, Large Cards).
- **Medium**: `border-radius: 16px` (Small Cards).
- **None**: MD3 rarely uses squares.

## 4. Component Recipes

### The "Filled Button"
- **Shape**: `rounded-full` (Stadium shape)
- **Bg**: `bg-[var(--md-sys-color-primary)]`
- **Text**: `text-[var(--md-sys-color-on-primary)]`
- **State Layer**: An overlay `<div>` inside usage:
    - `hover:bg-white/8` (8% opacity white overlay)
    - `active:bg-white/12`
- **Ripple**: Material Ripple is mandatory for the atomic feel. Use `react-ripple-click` or similar.

### The "Navigation Bar" (Bottom)
- **Height**: `80px` (Taller than standard iOS 49px).
- **Active Indicator**: A pill shape (`h-[32px] rounded-full`) surrounding the active icon.

### The "Card" (Elevated)
- **Bg**: `bg-[var(--md-sys-color-surface-container-low)]`
- **Shadow**: `shadow-md` (Elevation 1) -> `shadow-lg` (Elevation 2 on hover).
- **Radius**: `rounded-[12px]` or `rounded-[16px]`.

## 5. Interaction Patterns
- **Container Transform**: When a card opens into a full page, it expands seamlessly. Use Framer Motion `layoutId`.
- **Easing**: `cubic-bezier(0.2, 0.0, 0, 1.0)` (Emphasized Decelerate) - starts fast, ends slow.
