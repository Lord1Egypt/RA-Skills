---
name: ui-spec-nio
description: Detailed engineering specification for implementing NIO's progressive luxury and "Blue Sky Coming" design system.
license: Public domain / Fair use for reference
---

# UI Engineering Spec: NIO

## 1. Engineering Context
**Mental Model**: "The Horizon".
NIO's design creates a sense of space. It uses the "Horizon Line" to separate the "Vision" (Sky/Top) from "Action" (Earth/Bottom). It is airy, sophisticated, and quiet. It feels like a high-end EV interior.

**Key Traits**:
- **Horizon Split**: Top 2/3 is airy (Sky), Bottom 1/3 is functional (Earth).
- **Softness**: Everything is soft but structured.
- **Gradients**: Subtle "Dawn" and "Dusk" atmospheric gradients.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS
- **Animation**: `GSAP` or Framer Motion (Slow, elegant tweens).
- **3D**: `Three.js` / `React Three Fiber` (NIO often features 3D car models).

## 3. Design Tokens

### 3.1 Colors (Atmospheric)
- **Sky (Blue)**: `#4E92F9`
- **Earth (Dark)**: `#21272B` (Warm dark gray).
- **Sand**: `#CFAA84` (Interior leather tone).
- **Gradient**: `linear-gradient(180deg, #7247CA 0%, #58379B 100%)` (NIO Purple).
- **White**: `#FFFFFF` (Pure white for typography).

### 3.2 Typography
- **Font**: `Blue Sky Standard` (Custom) -> `Montserrat` (Clean geometric).
- **Heading**: Light weights (`300`), large sizes.
- **Body**: `Open Sans` or `Nio Sans`.

## 4. Component Recipes

### The "Horizon Button"
- **Bg**: `bg-[#4E92F9]`
- **Shape**: `rounded-full` (Capsule).
- **Width**: Often full width (in mobile contexts).
- **Shadow**: `shadow-[0_10px_30px_rgba(78,146,249,0.3)]` (Colored soft shadow).

### The "Card" (Floating)
- **Bg**: `bg-white`
- **Radius**: `rounded-[20px]`.
- **Shadow**: `shadow-xl` (Soft, large diffuse).
- **Content**: Image on top, text below with lots of padding (`p-8`).

### The "Nomi" (Assistant)
- **Visual**: A simple circle or digital face essential to the brand.
- **Animation**: Morphing shapes to indicate listening/thinking.

## 5. Interaction Patterns
- **Parallax**: Background elements move slower than foreground.
- **Fade**: Elements fade in slowly (`duration-700`) rather than popping in.
- **Scroll**: Smooth scroll with momentum.
