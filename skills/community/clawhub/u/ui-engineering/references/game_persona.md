---
name: ui-spec-game-persona
description: Detailed engineering specification for implementing "Persona 5 Style" (Acid Punk, Red/Black, Kinetic).
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Persona 5

## 1. Engineering Context
**Mental Model**: "The Phantom Letter".
The UI is an explosion of punk rebellion. It refuses to be straight. Everything is slanted, jagged, and kinetic. It uses "Ransom Note" typography and distinct black/white/red contrast.

**Key Traits**:
- **Sharps**: No rounded corners. Everything is a jagged shard.
- **Kinetic**: Menus don't just "appear"; they slam into the screen.
- **Contrast**: Pure `#FF0000` Red against Black.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS (`skew-x`, `rotate` utilities).
- **Motion**: `GSAP` (Greensock) for the violent timing curves.
- **SVG**: Heavy use of `clip-path` for jagged container shapes.

## 3. Design Tokens

### 3.1 Colors (Rebellion)
- **Bg**: `#FF0000` (Phantom Red) or `#E60000`.
- **Contrast**: `#000000` (Ink Black) and `#FFFFFF` (Paper White).
- **Pattern**: Halftone dots and starbursts.

### 3.2 Typography
- **Font**: `Slumpdb`, `Earwig Factory` (Ransom style).
- **Main**: `Impact` or `Condensed Sans` (Rotated).
- **Effect**: Letters wobble independently.

## 4. Component Recipes

### The "Shattered Menu"
- **Container**: `transform -skew-x-12`.
- **Item**: Black background with white text. On hover, background slams to Red.
- **Shape**: NOT a rectangle. A polygon with jagged edges (`clip-path`).

### The "Cutout Portrait"
- **Image**: High contrast black/white character portrait.
- **Border**: Thick white outline, like a sticker.
- **Animation**: Slides in from off-screen with motion blur.

### The "All Out Attack" Button
- **Visual**: Explodes on click.
- **Text**: "TAKE YOUR HEART".
- **Bg**: Starburst pattern.

## 5. Interaction Patterns
- **Transition**: Screen "rips" in half to transition pages.
- **Cursor**: A calling card that leaves a trail.
