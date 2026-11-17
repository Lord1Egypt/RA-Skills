---
name: ui-spec-figma
description: Detailed engineering specification for implementing Figma's constructive, geometric design system.
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Figma

## 1. Engineering Context
**Mental Model**: "The Workbench".
Figma's UI is a frame for *your* work. It is intentionally neutral (light gray/dark gray) so it doesn't clash with the canvas. The brand personality comes out in "Selection" and "Creation" colors (vectors, bounding boxes).

**Key Traits**:
- **1px Precision**: Borders are crisp 1px.
- **Selection**: High-contrast blue/purple outlines.
- **Economy**: Very small UI controls (switches, inputs).

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS
- **Canvas Logic**: HTML5 Canvas or SVG for complex drawing areas.
- **Icons**: 1px stroke icons (very thin).

## 3. Design Tokens

### 3.1 Colors
- **Bg App**: `#2C2C2C` (Dark Mode UI) or `#F5F5F5` (Light Mode UI).
- **Bg Canvas**: `#1E1E1E` (Dark) or `#E5E5E5` (Light).
- **Selection**: `#0D99FF` (Figma Blue).
- **Hover**: `#FFFFFF` (10% opacity white overlay).
- **Brand Rainbow**: `#F24E1E` (Red), `#A259FF` (Purple), `#1ABCFE` (Blue), `#0ACF83` (Green).

### 3.2 Typography
- **Font**: `Inter` (The standard for UI).
- **Size**: Extreme use of `11px` and `12px` (Small Labels).
- **Weight**: `Medium` (500) for labels, `Regular` (400) for inputs.

## 4. Component Recipes

### The "Property Input"
Small inputs found in the sidebar.
- **Height**: `28px` (Very compact).
- **Bg**: `transparent` hover `border border-white/10`.
- **Focus**: `border border-[#0D99FF] ring-1 ring-[#0D99FF]`.
- **Interaction**: Drag-to-change value cursor functionality.

### The "Layer Item"
- **State**:
    - Selected: `bg-[#0D99FF] text-white`
    - Hover: `bg-white/5`
- **Icon**: Type icon (Frame, Text, Component) in gray vs white.
- **Indentation**: 16px per depth level.

### The "Toolbar"
- **Location**: Floating at bottom center (new UI) or Top (classic).
- **Shape**: `rounded-xl bg-[#2C2C2C] border border-white/10 shadow-lg`.
- **Items**: Icons only, `w-[40px] h-[40px] flex center`.

## 5. Interaction Patterns
- **Direct Manipulation**: Cursors change to indicate tool (Move, Scale, Rotate).
- **Snapping**: Visual guides (red lines) appear when alignment happens.
