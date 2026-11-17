---
name: ui-spec-vercel
description: Detailed engineering specification for implementing Vercel's developer-centric, monochromatic design system.
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Vercel

## 1. Engineering Context
**Mental Model**: "Infrastructure as Code".
Vercel's design is the visual equivalent of clean code. It is Brutalist in its simplicity but Engineering-grade in its grid system. Black on White. Monospaced dominance. No clutter.

**Key Traits**:
- **Grid**: Visible or implied strict alignment.
- **Contrast**: Extreme (Black #000 vs White #FFF).
- **Typography**: "Geist" is the brand.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS (Vercel uses it heavily).
- **Icons**: Geist Icons (Stroke width 1.5px, sharp corners).
- **Fonts**: `Geist Sans` & `Geist Mono`.

## 3. Design Tokens

### 3.1 Colors (Geist System)
- **Bg**: `#FFFFFF` (Light), `#000000` (Dark)
- **Surface**: `#FAFAFA` (Light), `#111111` (Dark)
- **Border**: `#EAEAEA` (Light), `#333333` (Dark)
- **Accent**: `#0070F3` (Vercel Blue - Action)
- **Error**: `#EE0000`
- **Success**: `#0070F3` (Vercel uses Blue for success often) or `#7928CA` (Purple).

### 3.2 Typography
- **Heading 1**: `font-weight: 800`, `tracking-tight` (-0.04em)
- **Code**: `font-family: 'Geist Mono'`, `font-size: 0.9em`

## 4. Component Recipes

### The "Deploy Button"
- **Bg**: `bg-[#000000] dark:bg-white`
- **Text**: `text-white dark:text-black`
- **Shape**: `rounded-[6px]` (Sharp but safe)
- **Height**: `h-[40px]` (Standard)
- **Hover**: `hover:bg-[#333333]` (Lighten/Darken slightly)

### The "Card" (Geist Card)
- **Bg**: `bg-white`
- **Border**: `border border-[#EAEAEA]`
- **Hover**: `hover:border-black hover:shadow-lg transition-all`
- **Content**: Often contains a mono-spaced snippet.

### The "Status Badge"
- **Size**: `10px` circle.
- **Colors**:
    - Ready: `bg-[#0070F3]` (Blue)
    - Error: `bg-[#EE0000]` (Red)
    - Queued: `bg-[#999999]` (Gray)

## 5. Interaction Patterns
- **Snappy**: 150ms transitions. Start fast, end fast.
- **Skeleton**: Use shimmering skeletons for loading states to mimic data structure.
