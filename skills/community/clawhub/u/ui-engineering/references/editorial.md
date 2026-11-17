---
name: ui-spec-editorial
description: Detailed engineering specification for implementing "Editorial Art" aesthetic (Fluid, Broken Grid, Typographic).
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Editorial (Art Direction)

## 1. Engineering Context
**Mental Model**: "The Runway".
This style treats the browser canvas as a magazine spread. It ignores the "Box Model" visually (even if it uses it technically). Images overlap text. Text is gigantic. Scrolling is the primary animation driver (Scrollytelling).

**Key Traits**:
- **Typography as Image**: Fonts are so big they become graphical shapes.
- **Broken Grid**: Elements are intentionally misaligned or overlapping `z-index`.
- **Smooth Scroll**: Native scroll is often hijacked (via Lenis) for smoothness.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS + Custom CSS (for weird positions).
- **Scroll**: `Lenis` (Virtual scroll is essential for this feel).
- **WebGL**: `Three.js` / `React Three Fiber` (distorted images).
- **Animation**: `GSAP` (ScrollTrigger is the industry standard here).

## 3. Design Tokens

### 3.1 Colors (Classic)
- **Bg**: `#F4F0E8` (Warm Paper) or `#1A1A1A` (Charcoal).
- **Text**: `#000000` (Ink).
- **Accent**: Often uses acid colors (Neon Green `#CCFF00`) to contrast with serif fonts.

### 3.2 Typography
- **Heading**: Large Serif (`GT Alpina`, `Ogg`, `Playfair Display`).
- **Size**: `text-8xl` (96px) to `text-[10rem]`.
- **Mix**: Pairing a dainty Serif with a brutalist Sans-Serif / Mono.

## 4. Component Recipes

### The "Parallax Image"
- **Container**: `overflow-hidden`.
- **Image**: Scale `1.2`.
- **Logic**: Translate Y of image `start: -10%, end: 10%` based on scroll position within container.

### The "Marquee" (Ticker)
- **Content**: A huge sentence repeating infinitely horizontally.
- **Motion**: Constant linear velocity.
- **Interaction**: Speeds up or reverses on scroll.

### The "Sticky Section"
- **Layout**: Text stays pinned on the left (`position: sticky`), images scroll on the right.
- **Transition**: Text opacity fades `1 -> 0.2` as new sections arrive.

## 5. Interaction Patterns
- **Cursor**: Custom cursor (large circle or "VIEW" text) that blends with content (`mix-blend-mode: difference`).
- **Preloader**: (Controversial but common here) A percentage counter covering the screen before the "Curtain reveal".
