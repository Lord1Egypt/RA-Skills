---
name: ui-spec-things-3
description: Detailed engineering specification for implementing "Things 3 Style" (White Paper, Layers, Delight).
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Things 3

## 1. Engineering Context
**Mental Model**: "The White Stack".
Things 3 looks like perfectly cut pieces of paper stacking on top of each other. It uses "Magic" buttons that morph and extensive whitespace. It defines the "Apple Indie Quality" aesthetic.

**Key Traits**:
- **Paper Layers**: Views are modals that slide up as white sheets.
- **Soft Shadows**: Shadows are diffuse and elegant.
- **Delight**: Checkboxes have satisfying animations (Fill + Scale).

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS.
- **Icons**: `Feather Icons` (Similar stroke width).
- **Motion**: `Framer Motion` (Essential for the sheet stacking).

## 3. Design Tokens

### 3.1 Colors (Clean White)
- **Bg**: `#FFFFFF`.
- **Text**: `#333333` (Not black).
- **Subtext**: `#8E8E93` (Gray).
- **Accent**: `#3A82F7` (System Blue).
- **Separators**: `#E5E5EA`.

### 3.2 Typography
- **Font**: `System UI` (`-apple-system`). Using the native font is crucial.
- **Weight**: Bold Headings, Regular Body.

## 4. Component Recipes

### The "Magic Plus Button"
- **Shape**: Circle `w-14 h-14`.
- **Bg**: Blue.
- **Icon**: White Plus.
- **Interaction**: Draggable. On release, it creates a task *where you dropped it*.

### The "Task Row"
- **Border**: Bottom border `border-gray-100`.
- **Checkbox**: Square rounded `rounded-[4px] border-2 border-gray-300`.
- **Checked State**: Fills blue, scales up, then down (`scale-110` -> `scale-100`).

### The "Sheet Modal"
- **Visual**: A white card that comes from the bottom.
- **Corner**: `rounded-t-[10px]`.
- **Shadow**: Massive soft shadow (`shadow-2xl`).
- **Offset**: Sits 10px below the top of the viewport.

## 5. Interaction Patterns
- **Swipe Actions**: Swipe left to delete/schedule.
- **Drag Reorder**: Items lift up (`shadow-lg`) when dragged.
