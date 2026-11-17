---
name: ui-spec-raycast
description: Detailed engineering specification for implementing Raycast's speed-focused, keyboard-centric design system.
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Raycast

## 1. Engineering Context
**Mental Model**: "Velocity".
Raycast is built for flow state. The UI is designed to be traversed via keyboard, not mouse. Visuals are high-contrast dark mode to reduce eye strain during long coding sessions.

**Key Traits**:
- **Density**: High information density.
- **Focus**: Clear active states (red highlight).
- **Keyboard**: Shortcuts are first-class visual citizens.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS.
- **Logic**: Custom Hooks for Keyboard Management (`useKeyPress`, `useFocus`).
- **Animation**: Instant (0ms) or very fast (100ms) ease-out.

## 3. Design Tokens

### 3.1 Colors (Dark Mode First)
Raycast is natively dark.
- **Bg**: `#151515` (Main)
- **Panel**: `#1F1F1F` (List items, inputs)
- **Border**: `#333333`
- **Accent**: `#FF6363` (The "Raycast Red")
- **Text**: `#FFFFFF` (Primary), `#808080` (Secondary/Comments)

### 3.2 Typography
- **Font**: `Inter` (UI) / `Fira Code` (Code/Snippets).
- **Size**: `13px` or `14px` (Small, precise).

## 4. Component Recipes

### The "Action Panel" (The Root UI)
- **Layout**: Fixed width (`750px`), Fixed height (`450px`).
- **Bg**: `bg-[#191919]/80 backdrop-blur-md`
- **Border**: `border border-white/10 rounded-xl`
- **Shadow**: `shadow-2xl` (Deep black shadow).

### The "List Item" (Active State)
This is the most critical component.
- **Default**: `px-3 py-2 text-gray-400 flex items-center`
- **Active**: `bg-white/10 text-white border-l-2 border-[#FF6363]`
    - *Note*: The red left border is the signature "You are here" marker.

### The "Keyboard Shortcut" Badge
- **Container**: `bg-[#333333] rounded-[4px] px-1.5 py-0.5`
- **Text**: `text-[10px] font-medium text-gray-400 font-mono`

## 5. Interaction Patterns
- **Immediate Response**: No loaders unless absolutely necessary. Optimistic UI updates.
- **Navigation**: Arrow keys for list traversal. `Enter` for action. `Esc` for back.
