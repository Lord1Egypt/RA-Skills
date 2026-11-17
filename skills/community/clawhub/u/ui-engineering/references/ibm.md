---
name: ui-spec-ibm
description: Detailed engineering specification for implementing IBM's Carbon Design System (The Enterprise Standard).
license: Public domain / Fair use for reference
---

# UI Engineering Spec: IBM (Carbon)

## 1. Engineering Context
**Mental Model**: "The Grid System".
Carbon is the "Bauhaus" of digital design. It is strictly grid-based (2x grid). It is rational, modular, and accessible. It is not "fun"; it is "competent". If you are building a complex dashboard, Carbon is the gold standard.

**Key Traits**:
- **The Grid**: Everything aligns to the 16-column grid.
- **Productivity**: High information density. Small fonts (14px).
- **Tokens**: Extensive use of design tokens for theming (White, Gray 10, Gray 90, Black themes).

## 2. Tech Stack Recommendations
- **Styling**: SCSS / Tailwind (Carbon specific config).
- **Icons**: Carbon Icons (16px / 20px / 32px specific sizes).
- **Fonts**: `IBM Plex` (Open Source, excellent Mono/Sans/Serif family).

## 3. Design Tokens

### 3.1 Colors (The Gray 100 Scale)
Carbon themes are built by swapping these tokens.
- **Interactive Blue**: `#0F62FE` (Blue 60 - Primary Action).
- **Focus**: `#0F62FE` (2px solid border).
- **Text Primary**: `#161616` (Gray 100).
- **Text Secondary**: `#525252` (Gray 60).
- **Bg Page**: `#F4F4F4` (Gray 10).
- **Bg Layer**: `#FFFFFF`.

### 3.2 Typography
- **Font**: `IBM Plex Sans`.
- **Mono**: `IBM Plex Mono` (Critical for data/code).
- **Scale**: `12px` (Label), `14px` (Body), `16px` (Title). It feels "small" compared to consumer apps.

## 4. Component Recipes

### The "Data Table" (The King)
- **Header**: Capitalized, 12px, bold.
- **Row**: `h-[48px] border-b border-[#E0E0E0] hover:bg-[#E5E5E5]`.
- **Cell**: Monospaced numbers.
- **Action**: Inline overflow menu (•••).

### The "Primary Button" (Sharp)
- **Shape**: `rounded-none` (Or very small `2px` in v11). Carbon is traditionally sharp.
- **Bg**: `#0F62FE` hover `#0353E9`.
- **Icon**: Right aligned icon (Arrow) is very common.
- **Align**: Text is left-aligned in some variations, but center standard.

### The "Tile"
- **Bg**: `#FFFFFF`.
- **Padding**: `p-4`.
- **Border**: No border, but distinct background contrast.
- **Interaction**: Selectable tiles have a thick gray border on select.

## 5. Interaction Patterns
- **Skeleton Loading**: Carbon pioneered the "Grey shimmer" skeleton state.
- **Progressive Disclosure**: Show high-level data, click to expand row for details.
- **Focus States**: High visibility is mandatory for accessibility.
