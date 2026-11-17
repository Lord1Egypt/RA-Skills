---
name: ui-spec-procreate
description: Detailed engineering specification for implementing "Procreate Style" (Invisible UI, Gesture First, Dark).
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Procreate

## 1. Engineering Context
**Mental Model**: "The Digital Canvas".
The best UI is no UI. Procreate puts the content (the canvas) first. The UI controls are tiny, semi-transparent, and sit at the edges. They disappear entirely with a 4-finger tap.

**Key Traits**:
- **Obsidian Dark**: The UI is always dark gray to make colors look accurate.
- **Edge Anchoring**: Tools live in the top-right and left sidebar.
- **Popovers**: Menus are small popovers, not full-screen modals.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS.
- **Gestures**: `use-gesture` (React hook for complex multi-touch).
- **Canvas**: `HTML5 Canvas` (The core).

## 3. Design Tokens

### 3.1 Colors (Studio Environment)
- **Bg**: `#121212` (Studio Dark).
- **Tools**: `#2C2C2E` (Toolbars).
- **Active**: `#5A5A5E` (Selected tool).
- **Text**: `#EBETBF` (Off-white).
- **Accent**: `#007AFF` (Apple Blue - rarely used).

### 3.2 Typography
- **Font**: `System UI` (San Francisco).
- **Size**: Small (`text-xs` or `text-sm`). Labels are secondary to Icons.

## 4. Component Recipes

### The "Mobile Toolbar"
- **Position**: Fixed Top.
- **Bg**: `bg-[#1C1C1E]/90 backdrop-blur-md`.
- **Items**: Icons only (Brush, Smudge, Eraser, Layers, Color).
- **Selected**: Highlighted with a brighter gray background.

### The "Slider Sidebar"
- **Position**: Fixed Left (or Right).
- **Width**: `w-12`.
- **Sliders**: Two vertical sliders (Size, Opacity).
- **Interaction**: Drag up/down to adjust value. No visible track until touched.

### The "Color Drop"
- **Visual**: A circle in the top right showing current color.
- **Interaction**: Drag (DnD) the circle onto the canvas to "Flood Fill".

## 5. Interaction Patterns
- **Undo/Redo**: Two-finger tap (Undo), Three-finger tap (Redo). This is the industry standard now.
- **Hiding UI**: 4-finger tap toggles `UI visible` boolean.
