---
name: ui-spec-starbucks
description: Detailed engineering specification for implementing Starbucks' expressive, joyful, and typography-rich design system.
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Starbucks

## 1. Engineering Context
**Mental Model**: "Coffee House Vibes".
Starbucks digital is joyful. Unlike the "cool" tech brands, Starbucks wants to feel "warm" and "energetic". It uses complex patterns, illustrations, and a wide range of greens. It feels like a well-designed menu board.

**Key Traits**:
- **Expression**: Headlines are often serif or expressive script.
- **Green Palette**: Not just one green, but a spectrum (House, Accent, Light).
- **Cards**: Layouts are distinct blocks/tiles, often alternating image/text (Zig-zag).

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS.
- **SVG**: Inline SVGs for pattern backgrounds (Plant leaves, stars).
- **Layout**: CSS Grid is heavy used for the tile layouts.

## 3. Design Tokens

### 3.1 Colors (Greens of the World)
- **Starbucks Green**: `#006241` (The House Green).
- **Accent Green**: `#00754A` (Lighter, used in buttons).
- **Warm Beige**: `#F1F8F6` (Mint cream backgrounds).
- **Cold Brew**: `#1E3932` (Darkest Green/Black).
- **Joy**: `#D4E9E2` (Light festive green).

### 3.2 Typography
- **Headings**: `Sodo Sans` (House geometric) or `Lander` (Serif for expression).
- **Body**: `Sodo Sans`.
- **Style**: Headlines are often tight. Body copy is generous.

## 4. Component Recipes

### The "Reward Star"
- **Shape**: Star icon.
- **Color**: Gold `#CBA258`.
- **Animation**: Fill up animation on progress bar.

### The "Content Tile" (Zig Zag)
- **Container**: `grid grid-cols-1 md:grid-cols-2`.
- **Image Side**: Full bleed image.
- **Text Side**: `bg-[#1E3932] text-white flex flex-col justify-center items-center text-center p-10`.
- **Button**: `border border-white rounded-full px-6 py-2 hover:bg-white/10`.

### The "Pill Button"
- **Bg**: `bg-[#00754A]`.
- **Shape**: `rounded-full`.
- **Text**: `text-white font-bold`.
- **Feedback**: Scale down `0.95` on click.

## 5. Interaction Patterns
- **Accordion**: Nutritional info often hides in smooth accordions.
- **Floating Bar**: "Add to Order" floating bottom bar on mobile.
