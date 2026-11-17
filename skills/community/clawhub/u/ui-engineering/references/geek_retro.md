---
name: ui-spec-geek-retro
description: Detailed engineering specification for implementing "Windows 95 / Vaporwave Style" (Beige, Pixel, Brutalist).
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Retro 95

## 1. Engineering Context
**Mental Model**: "The Desktop OS".
Nostalgia for the GUI era (1995-2000). Beige boxes, distinct 3D bevels (light top-left, dark bottom-right), and pixelated bitmap fonts. It is "un-flat" design.

**Key Traits**:
- **Bevels**: CSS `border-style: outset` or custom box shadows are key.
- **Chicago/Pixel Font**: Text must not be anti-aliased (`font-smooth: never`).
- **Windows**: Content lives in draggable windows with blue title bars.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS + Custom Borders.
- **Font**: `MS Sans Serif` (or `W95FA` webfont).
- **Libraries**: `OpenWindows` CSS or `98.css`.

## 3. Design Tokens

### 3.1 Colors (VGA)
- **Bg Desktop**: `#008080` (Teal).
- **Bg Window**: `#C0C0C0` (Silver).
- **Title Bar**: Gradient `#000080` (Navy) to `#1084D0` (Light Blue).
- **Text**: `#000000`.
- **Highlight**: `#FFFFFF` (Top/Left edges).
- **Shadow**: `#808080` (Bottom/Right edges) + `#000000` (Deep shadow).

### 3.2 Typography
- **Font**: `Pixelated Sans` (11px or 12px fixed size).
- **Sharpness**: Turn off font smoothing via CSS.

## 4. Component Recipes

### The "Window Frame"
- **Outer**: `bg-silver p-1 shadow-outset`.
- **Title Bar**: `bg-gradient-to-r from-blue-800 to-blue-400 text-white px-2 py-1 flex justify-between`.
- **Controls**: Minimize/Maximize/Close buttons are 3D squares with icons.

### The "3D Button"
- **Normal**: `bg-silver border-2 border-white border-b-gray-800 border-r-gray-800 active:border-gray-800 active:border-b-white`.
- **Interaction**: Physically shifts 1px down-right on click.

### The "Start Bar"
- **Position**: Fixed bottom.
- **Style**: Beveled gray bar.
- **Start Button**: Icon (Logo) + Text "Start". Bold bevel.

## 5. Interaction Patterns
- **Draggable**: Windows must be movable (`react-draggable`).
- **Z-Index**: Clicking a window brings it to front.
- **Error Sound**: The classic "Chord" or "Ding" on error.
