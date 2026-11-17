---
name: ui-spec-trend-bento
description: Detailed engineering specification for implementing "The Bento Grid" trend (Dribbble 2024, Modular, Soft).
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Dribbble Bento

## 1. Engineering Context
**Mental Model**: "The Lunchbox".
Everything is a distinct, contained module. It is the ultimate responsive layout because every cell is self-contained. It differs from "Apple" by being softer, colorful, and often featuring 3D illustrations inside the cells.

**Key Traits**:
- **Gaps**: Large, consistent gaps (`gap-4` or `gap-6`) are the defining feature.
- **Squircle**: `rounded-2xl` or `rounded-3xl` (Super round corners).
- **No Text Wrapping**: Bento items maximize visual punch, minimizing text.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS (Grid utilities are perfect here).
- **Grid**: `unstable_grid` (CSS Grid `auto-rows` is essential).
- **Motion**: `Framer Motion` (Layout animations when reordering).

## 3. Design Tokens

### 3.1 Colors (Soft Play)
- **Bg Page**: `#F7F7F8` (Off-white) or `#0D0D0D` (Mac Black).
- **Bg Cell**: `#FFFFFF` (White) or `#1C1C1E` (Dark Grey).
- **Gradient**: Cells often have subtle internal gradients (`bg-gradient-to-br from-white to-gray-50`).
- **Shadow**: `shadow-[0_2px_12px_rgba(0,0,0,0.04)]` (Very soft).

### 3.2 Typography
- **Font**: `SF Pro Rounded` or `Nunito` (Rounded types are common).
- **Header**: Large, Heavy weight.
- **Label**: Uppercase, small, tracking wide.

## 4. Component Recipes

### The "Bento Cell"
- **Container**: `bg-white rounded-[24px] p-6 flex flex-col justify-between`.
- **Hover**: Scale `1.02` using `transform-gpu transition-transform`.
- **Internal**: Content must "fill" the cell (Object-cover).

### The "Graph Cell"
- **Bg**: White.
- **Chart**: A smooth area chart with a gradient fill.
- **Data**: "Total Revenue" + "$12,450" (Big Text).
- **Visual**: Chart goes all the way to the bottom edge (Full bleed).

### The "Map Widget"
- **Mask**: `overflow-hidden rounded-[24px]`.
- **Content**: Dark mode map.
- **Overlay**: Glass blur floating user avatar.

## 5. Interaction Patterns
- **Reorder**: Drag and drop (like iOS home screen) is the gold standard interaction.
- **Expand**: Clicking a cell expands it to full screen (`layoutId` animation).
