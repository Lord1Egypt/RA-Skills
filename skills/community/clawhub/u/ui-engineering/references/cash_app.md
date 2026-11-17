---
name: ui-spec-cash-app
description: Detailed engineering specification for implementing Cash App's "Psychedelic", "Weird", and "Gen Z" design system.
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Cash App

## 1. Engineering Context
**Mental Model**: "The Glitch World".
Cash App broke Fintech design. It ignores "trust blue" and "safety grids". It uses Dali-esque surrealism, floating 3D coins, green glitch effects, and massive bold type. It feels like a music video, not a bank.

**Key Traits**:
- **Surreal 3D**: Floating objects that defy gravity.
- **Cash Green**: A radioactive green (`#00D632`).
- **Motion**: Everything floats, twists, or glitches.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS.
- **3D**: `Three.js` / `React Three Fiber` (Required for the floaty elements).
- **Shaders**: Custom GLSL shaders for distortion effects.
- **Type**: `Monument Extended` or similar wide sans.

## 3. Design Tokens

### 3.1 Colors (Radioactive)
- **Bg**: `#000000` (Void Black) or `#00D632` (Cash Green).
- **Text**: `#FFFFFF`.
- **Accent**: `#00D632`.
- **Spectrum**: Eye-searing gradients (Pink, Cyan, Yellow) used in 3D lighting.

### 3.2 Typography
- **Font**: `Agrandir` or `Monument Extended` (Wide, bold grotesque).
- **Size**: Massive. `text-9xl` on desktop.
- **Icons**: Custom surreal icons (Eye, Pyramid, Coin).

## 4. Component Recipes

### The "Floating Hero"
- **Bg**: Black.
- **Foreground**: A phone mockup.
- **Surroundings**: 3D coins, cards, and weird shapes (staircases, pillars) orbiting the phone.
- **Interaction**: Mouse movement creates parallax on all 3D objects.

### The "Glitch Text"
- **Effect**: Text flickers on hover.
- **Mix**: Mix of Upper and Lowercase in weird places.

### The "Download CTA"
- **Style**: Brutalist/Retro.
- **Border**: Thick outlines.
- **App Store Badge**: Custom, monochrome, high contrast.

## 5. Interaction Patterns
- **Scroll Distortion**: As you scroll, the page might warp or separate RGB channels.
- **Infinite Loop**: Background textures that slide forever.
