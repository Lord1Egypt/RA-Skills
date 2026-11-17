---
name: ui-spec-game-monument
description: Detailed engineering specification for implementing "Monument Valley Style" (Isometric, Pastel, Zen, Impossible).
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Monument Valley

## 1. Engineering Context
**Mental Model**: "The Impossible Object".
The UI is not 2D; it is an isometric object that can be rotated. It uses soft pastels, rigorous geometry, and impossible optical illusions (Penrose steps). It is a "Zen" interface.

**Key Traits**:
- **Isometric**: Fixed camera angle ($35.264^\circ$) is mandatory.
- **No HUD**: The environment *is* the UI.
- **Pastel**: Soft, dreamy color palettes that shift with "levels".

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS.
- **3D**: `Three.js` (Orthographic Camera is essential).
- **Engine**: `React Three Fiber` (Drei).

## 3. Design Tokens

### 3.1 Colors (Dreamscape)
- **Bg**: `#FAD9B8` (Soft Peach) or `#2C3E50` (Deep Blue Night).
- **Structure**: `#E74C3C` (Coral), `#F1C40F` (Yellow).
- **Shadow**: Deep purple shadows (`#8E44AD`) instead of black.
- **Highlight**: No specular highlights. Matte finish only.

### 3.2 Typography
- **Font**: `Varela Round` or `Quicksand`.
- **Style**: Minimal, floating in 3D space, sans-serif.

## 4. Component Recipes

### The "Isometric Card"
- **Geometry**: A thick 3D slab (BoxGeometry).
- **Camera**: Orthographic.
- **Interaction**: Drag to rotate the *entire world* to reveal the back.

### The "Impossible Menu"
- **Visual**: A Penrose Triangle that acts as the navigation.
- **Selection**: Clicking a face of the triangle rotates it to a new state.

### The "Totem Button"
- **Shape**: A yellow rectangular prism with eyes.
- **Behavior**: Draggable. It slides along existing paths.

## 5. Interaction Patterns
- **Rotation**: The core mechanic. Rotating the view connects disconnected paths.
- **Sound**: Musical tones play on every interaction (Procedural audio).
