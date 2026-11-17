---
name: ui-spec-bytedance
description: Detailed engineering specification for implementing ByteDance's (TikTok) energetic, glitch-pop, full-screen aesthetic.
license: Public domain / Fair use for reference
---

# UI Engineering Spec: ByteDance (TikTok)

## 1. Engineering Context
**Mental Model**: "Immersive Flow".
The design is aggressive and immersive. It removes the "chrome" (UI bars) to let the video fill 100% of the screen. Controls hover *over* the content. Aesthetics are Cyberpunk/Glitch (Cyan + Pink).

**Key Traits**:
- **Full Screen**: No margins. No white space.
- **Overlay UI**: Text shadow is mandatory for readability.
- **Glitch**: The split Cyan/Red vibration effect.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS
- **Media**: Native `<video>` with IntersectionObserver for auto-play.
- **Effects**: CSS `text-shadow` and `mix-blend-mode`.

## 3. Design Tokens

### 3.1 Colors (Cyberpunk)
- **Bg**: `#000000` (Pure Black).
- **Text**: `#FFFFFF`.
- **Accent Red**: `#FE2C55` (TikTok Red).
- **Accent Cyan**: `#25F4EE` (TikTok Cyan).

### 3.2 Typography
- **Font**: `Proxima Nova` -> `Sofia Pro`.
- **Style**: Geometric Sans.
- **Weights**: Heavy Bold for headlines.

## 4. Component Recipes

### The "Glitch Text"
- **CSS**:
  ```css
  .glitch {
    text-shadow: 2px 2px 0px #25F4EE, -2px -2px 0px #FE2C55;
    animation: jitter 0.1s infinite;
  }
  ```

### The "Floating Action Sidebar"
Right-aligned vertical stack of icons over video.
- **Structure**: Flex column.
- **Icon**: White fill, `drop-shadow-md`.
- **Text**: Small white text below icon, `font-weight: 600`.
- **Avatar**: Circle with a "Plus" badge at the bottom that disappears after following.

### The "Music Disc"
Bottom right spinning disc.
- **Animation**: `animate-spin` (linear, infinite, 5s duration).
- **Notes**: Floating music notes rising from the disc (`opacity: 0` -> `1` -> `0`, `translate-y`).

## 5. Interaction Patterns
- **Snap Scroll**: `scroll-snap-type: y mandatory`. One flick = exactly one full video.
- **Double Tap**: Heart animation appears at tap location.
- **Long Press**: "Not Interested" / Actions menu.
