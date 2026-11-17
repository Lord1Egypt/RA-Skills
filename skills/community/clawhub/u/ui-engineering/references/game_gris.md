---
name: ui-spec-game-gris
description: Detailed engineering specification for implementing "Gris Style" (Watercolor, Ink, Fluid, Art).
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Gris

## 1. Engineering Context
**Mental Model**: "The Living Painting".
The UI is invisible. Interactivity is painted. Buttons are ink blots. Transitions are watercolor bleeds. It is fragile, emotional, and 2D.

**Key Traits**:
- **Watercolor**: Textures are essential. Paper grain, ink spread.
- **Line Art**: Ultra-fine lines (`0.5px`).
- **Flow**: Objects morph into each other (Dress becomes a mountain).

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS.
- **SVG**: Essential for the line art and morphing paths.
- **Filters**: SVG Displacement Maps (Turbulence) for the "ink bleed" effect.

## 3. Design Tokens

### 3.1 Colors (Grief Spectrum)
- **Bg**: `#EAECEE` (Watercolor Paper).
- **Ink**: `#2C3E50` (Dark Blue/Grey).
- **Wash**: `#E74C3C` (Red phase), `#3498DB` (Blue phase), `#2ECC71` (Green phase).
- **Gradient**: No flat colors. Everything is a textured gradient.

### 3.2 Typography
- **Font**: `Playfair Display` or `Cormorant Garamond` (Elegant Serif).
- **Style**: Centered, widely spaced, understated.

## 4. Component Recipes

### The "Ink Button"
- **Shape**: Hand-drawn circle (imperfect).
- **Hover**: An ink drop falls and spreads to fill the circle.
- **Stroke**: Trembling line effect.

### The "Parallax Layers"
- **Back**: Blurred watercolor washes.
- **Mid**: Sharp vector geometry.
- **Front**: Silhouette foreground black.

### The "Morph Text"
- **Transition**: Text dissolves into smoke/ink before disappearing.

## 5. Interaction Patterns
- **Slow**: No fast movements. Everything floats.
- **Silence**: Interactions are quiet or accompanied by cello notes.
