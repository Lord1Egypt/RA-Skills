---
name: ui-spec-aesop
description: Detailed engineering specification for implementing Aesop's "Quiet Luxury" and "Literary Retail" design system.
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Aesop

## 1. Engineering Context
**Mental Model**: "The Library Store".
Aesop is the gold standard for luxury e-commerce. It ignores conversion-rate-optimization trends (big red buttons, urgency). Instead, it favors calm, literary storytelling, muted colors, and intellectual respect for the user. It feels like walking into a spa.

**Key Traits**:
- **Cream & Black**: No white backgrounds. The base is always a warm cream/beige.
- **Literary Typography**: Serif dominance. Product descriptions read like poetry.
- **Grid Structure**: Rigid, modernist grid, often with plenty of negative space.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS.
- **Carousel**: `Swiper.js` (Aesop loves horizontal scrolling product rails).
- **Images**: High-fidelity, un-cropped product photography with transparent backgrounds.

## 3. Design Tokens

### 3.1 Colors (Organic & Earthy)
- **Bg Page**: `#FFFEF2` (Aesop Cream) or `#333333` (Charcoal for some sections).
- **Text Main**: `#333333` (Soft Black).
- **Border**: `#333333` (Thin, 1px borders).
- **Accent**: Muted tones only (Olive, Clay, Slate) extracted from product labels.

### 3.2 Typography
- **Font**: `Suisse Int'l` (Grotesk) and `Zapf Humanist` (Optima-like Serif).
- **Scale**: Body text is often `16px`. Headings are modest.
- **Layout**: Text is often split into two columns (Left: Title, Right: Body).

## 4. Component Recipes

### The "Product Strip"
- **Layout**: Horizontal repeating flex container.
- **Card**: `w-[300px] flex-shrink-0 flex flex-col items-center`.
- **Image**: Centered, no border.
- **Designation**: "Skin Care" (Small sans-serif).
- **Title**: "Parsley Seed Serum" (Serif or Bold Sans).
- **Action**: "Add to your cart - $85.00" (Text link, not a button).

### The "Literary Quote"
- **Bg**: Full width.
- **Content**: A philosophical quote in the center.
- **Style**: Italic Serif, large spacing.

### The "Navigation Bar"
- **Position**: Sticky top.
- **Style**: Minimal text links only. No icons. "Shop", "Read", "Stores", "Search".
- **Bg**: Matching page background (Cream).

## 5. Interaction Patterns
- **Slow Fade**: Page loads are often accompanied by a slow opacity fade-in.
- **Hover**: No motion. Just a subtle underline or text color change. Dignified.
