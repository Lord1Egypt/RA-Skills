---
name: ui-spec-bruno-simon
description: Detailed engineering specification for implementing Bruno Simon's "Gamified Portfolio" aesthetic (Low Poly, Physics, Play).
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Bruno Simon

## 1. Engineering Context
**Mental Model**: "The Playground".
The website is a game. Navigation is movement. The user is a player. Content is discovered, not read. It uses Low Poly aesthetics and physics (cars, balls, gravity) to make the web feel tactile and joyful.

**Key Traits**:
- **Vehicle Controller**: Navigation is done by driving a car (or avatar).
- **Physics**: Everything has rigid body physics (`cannon.js`).
- **Low Poly**: 3D assets are simple, colourful, and performant.

## 2. Tech Stack Recommendations
- **3D**: `Three.js` + `React Three Fiber`.
- **Physics**: `Cannon.js` or `Rapier` (Modern WASM alternative).
- **Framework**: `React` (for the overlay UI).

## 3. Design Tokens

### 3.1 Colors (Toy Box)
- **Bg**: `#E8F0F7` (Sunny Sky Blue).
- **Ground**: `#FDFDFD`.
- **Accent**: `#E76E65` (Red Brick), `#69C4FF` (Blue Water).
- **Shadow**: Baked lighting (Lightmaps) rather than real-time shadows for performance.

### 3.2 Typography
- **Font**: `Poppins` or `Fredoka One` (Rounded, friendly).
- **Use**: 3D Text geometry floating in the world.

## 4. Component Recipes

### The "Vehicle" (Camera Controller)
- **Model**: Low poly car.
- **Controls**: WASD / Arrow keys.
- **Camera**: Follow camera with smooth damping.

### The "Checkpoint" (Section)
- **Visual**: A glowing 3D gate or platform.
- **Interaction**: Driving through it triggers a modal or UI overlay.
- **Label**: Large 3D text floating above.

### The "Interactive Object"
- **Behavior**: Dynamic bodies (Bowling pins, boxes).
- **Feedback**: Sound effects on collision (Bonk!).

## 5. Interaction Patterns
- **Discoverability**: Hidden areas ("Easter eggs") encourage exploration.
- **Loading Screen**: A mini-game or interactive loader while assets bake.
