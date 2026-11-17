---
name: ui-spec-active-theory
description: Detailed engineering specification for implementing "Active Theory Style" (Particles, Fluid, Shaders).
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Active Theory

## 1. Engineering Context
**Mental Model**: "The Liquid Screen".
The browser canvas is a fluid medium. Water ripples, particles flow, and glass shatters. It is technically demanding and visually overwhelming (in a good way). It feels like a high-end console menu.

**Key Traits**:
- **Particles**: Everything is made of dots or fluid simulation.
- **Shaders**: Custom GLSL shaders for distortion and post-processing.
- **Navigation**: Often circular or non-linear.

## 2. Tech Stack Recommendations
- **3D**: `Three.js` (Raw or VIA framework).
- **Shaders**: `GLSL` (Essential).
- **Framework**: `React` (for UI layer over the canvas).

## 3. Design Tokens

### 3.1 Colors (Neon Dark)
- **Bg**: `#000000` (Void).
- **Particles**: `#FFFFFF` (White) or Gradient (`#FF00CC` to `#00FFFF`).
- **Glow**: Bloom post-processing is heavily used.

### 3.2 Typography
- **Font**: `Monument Extended` or similar Techno-Sans.
- **Style**: Uppercase, tracked out (`tracking-widest`).
- **Effect**: Text often has a "glitch" or "wave" displacement on hover.

## 4. Component Recipes

### The "Water Ripple"
- **Effect**: Mouse movement creates a trail in a fluid velocity map.
- **Visual**: Distorts the background image or displacement map.

### The "Particle Text"
- **Geometry**: Text is converted to thousands of `Points`.
- **Interaction**: Mouse repels particles (`Explosion` effect) which then reform.

### The "Tunnel Navigation"
- **Camera**: Moves forward through a 3D tunnel of images.
- **Speed**: Controlled by scroll or mouse hold.

## 5. Interaction Patterns
- **Preloader**: A complex visual loading state (Percentage + Visual) is required due to asset weight.
- **Sound**: Ambient audio loops and UI hover "ticks" are standard.
