---
name: ui-spec-game-nier
description: Detailed engineering specification for implementing "Nier Automata Style" (Beige Industrial, Glitch, CRT).
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Nier: Automata

## 1. Engineering Context
**Mental Model**: "The Android System".
The UI is diegetic—it is the actual operating system of the android you are playing. It is monotone beige, utilitarian, and melancholic. It glitches when the "system" is damaged.

**Key Traits**:
- **Monotone**: 99% of the UI is Beige (`#DAD4BB`).
- **Scanlines**: Subtle CRT grid overlay on everything.
- **System**: Menus are lists of system parameters.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS.
- **Effects**: CSS Filters (Noise, Scanlines).
- **Font**: Monospaced only.

## 3. Design Tokens

### 3.1 Colors (YoRHa Standard)
- **Bg**: `#CDC8B0` (Beige Dark) or `#DAD4BB` (Beige Light).
- **Text**: `#4D4A40` (Dark Mud).
- **Grid**: `#5C5950` (Thin lines).
- **Glitch**: `#FFFFFF` (Digital artifacts).

### 3.2 Typography
- **Font**: `Rodin` (The official font) or `HelvetiPixel` / `Overpass Mono`.
- **Size**: Small, dense, legible.

## 4. Component Recipes

### The "System Menu"
- **Bg**: Patterned Grid (1px dots).
- **List**: Simple text items.
- **Cursor**: A square block that blinks.
- **Selection**: Invert colors (Text becomes Beige, Block becomes Dark).

### The "Loading Boot"
- **Text**: "SYSTEM CHECK..." printing character by character.
- **Log**: Fast scrolling hex code streams.

### The "Map Grid"
- **Style**: Wireframe 3D map.
- **Color**: Beige lines on Beige background (low contrast).

## 5. Interaction Patterns
- **Audio**: Selecting items makes a "blip" sound.
- **Glitch**: On error or hover, the element momentarily shifts pixels (`transform: translate(2px)`).
