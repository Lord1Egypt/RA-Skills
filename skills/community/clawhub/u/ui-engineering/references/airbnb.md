---
name: ui-spec-airbnb
description: Detailed engineering specification for implementing Airbnb's warm, photography-first design system.
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Airbnb

## 1. Engineering Context
**Mental Model**: "Modern Hospitality".
Airbnb's design is warm, inclusive, and visual. It frames high-quality photography with generous whitespace and soft shadows. It avoids "tech" aesthetics (no glitches, no neon). It feels like a high-end travel magazine.

**Key Traits**:
- **Photography First**: Images are full-width or large cards.
- **Roundness**: Generous curves (24px+).
- **Shadows**: Soft, elevated shadows.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS
- **Carousel**: Swiper.js (The image slider is core).
- **Maps**: Mapbox GL JS (Custom styed).

## 3. Design Tokens

### 3.1 Colors
- **Brand**: `#FF385C` (Rausch - Pinkish Red)
- **Text**: `#222222` (Mine Shaft - High constrast)
- **Text Secondary**: `#717171` (Gray)
- **Border**: `#DDDDDD` (Light gray dividers)
- **Bg**: `#FFFFFF`

### 3.2 Typography
- **Font**: `Airbnb Cereal` (Circular sans-serif) -> `Circular` -> `Inter`.
- **Weights**: Heavy use of `800` (ExtraBold) for titles vs `400` (Regular) for body.

## 4. Component Recipes

### The "Listing Card"
- **Image**: `aspect-[20/19] rounded-xl object-cover`
- **Typography**:
    - Location: `font-semibold text-[#222222]`
    - Distance: `text-[#717171]`
    - Price: `font-semibold text-black` span `font-normal` (per night).
- **Navigation**: Dot pagination overlay on image.

### The "Search Pill" (Header)
- **Container**: `rounded-full border shadow-sm hover:shadow-md transition-shadow`
- **Layout**: Flex row with dividers `h-[24px] w-[1px] bg-gray-300`.
- **Button**: Brand color circle button with search icon.

### The "Primary Button" (Gradient)
- **Bg**: `bg-gradient-to-r from-[#E61E4D] to-[#E31C5F]` (Subtle internal gradient).
- **Size**: Large, touch-friendly (`48px` or `56px` height).
- **Radius**: `rounded-lg` (8px).

## 5. Interaction Patterns
- **Map Interaction**: Floating pill buttons on map (`transform: translate(-50%)`).
- **Modal**: Bottom sheets on mobile, centered modal with rounded corners on desktop.
