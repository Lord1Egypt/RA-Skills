---
name: ui-spec-teen-engineering
description: Detailed engineering specification for implementing Teen Engineering's "Raw", "Industrial", and "Brutalist" design system.
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Teen Engineering

## 1. Engineering Context
**Mental Model**: "The Operator Manual".
Teen Engineering treats the website like a piece of hardware documentation. It uses system fonts, tiny text, raw HTML elements, and high-fidelity technical diagrams. It is "anti-design" in the best way.

**Key Traits**:
- **Tiny Type**: `10px` or `11px` is common. Reading requires focus.
- **Raw HTML**: Default browser inputs, radio buttons are stylized to look raw but pixel-perfect.
- **Technical Grid**: Lines, rulers, measurements visible on screen.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS (heavy use of spacing/border utilities).
- **Fonts**: `Arial`, `Helvetica`, or System Fonts stack. No web fonts needed.
- **3D**: `Three.js` (for interactive product rotation).

## 3. Design Tokens

### 3.1 Colors (Plastic & Metal)
- **Bg**: `#E5E5E5` (Light Grey plastic) or `#FFFFFF`.
- **Text**: `#000000` (100% Black).
- **Accents**: Primary colors only. `#FF0000` (Red), `#0000FF` (Blue) - used for tiny indicators.

### 3.2 Typography
- **Font**: `Arial` / `Inter` / `System-UI`.
- **Size**: `text-[11px]` (Label), `text-[13px]` (Body). Unusually small.
- **Case**: All lowercase or All Uppercase.

## 4. Component Recipes

### The "Spec Table"
- **Layout**: Dense grid.
- **Border**: `border t-1 border-black`.
- **Row**: `flex justify-between py-1 border-b border-black`.
- **Key**: Left aligned, 11px uppercase.
- **Value**: Right aligned, 11px mono.

### The "Raw Button"
- **Appearance**: Looks like a generic HTML button but refined.
- **Bg**: `bg-[#F0F0F0]`.
- **Border**: `border border-black hover:bg-black hover:text-white`.
- **Shape**: `rounded-[2px]` (Sharp but not dangerous).

### The "Product Hero"
- **Image**: Cut-out product on plain white/grey background. No shadows.
- **Scale**: Massive. The product fills the screen.

## 5. Interaction Patterns
- **Click**: Instant state change. No transition.
- **Scroll**: Native scroll. No smoothing.
- **Cursor**: Default pointer.
