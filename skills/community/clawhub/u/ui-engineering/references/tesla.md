---
name: ui-spec-tesla
description: Detailed engineering specification for implementing Tesla's cinematic, minimalist, product-first design system.
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Tesla

## 1. Engineering Context
**Mental Model**: "Cinematic Window".
Tesla's website dissolves the interface. The car is the interface. The website is just a window. There are almost no "containers" or distinct "sections" - just full-screen panels that snap into place.

**Key Traits**:
- **Scroll Snap**: The entire homepage is a vertical carousel of full-screen sections.
- **Invisible UI**: Buttons are transparent ghosts until needed.
- **Glass**: Frosted glass overlays for specs.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS.
- **Scroll**: `fullpage.js` or CSS Scroll Snap (`scroll-snap-type: y mandatory`).
- **3D**: `Three.js` (Configurators are essential).

## 3. Design Tokens

### 3.1 Colors (Future Industrial)
- **Bg**: Transparent (Video/Image) or `#171A20` (Dark UI).
- **Text**: `#171A20` (Dark) / `#FFFFFF` (Light).
- **Btn Primary**: `#3E6AE1` (Tesla Blue) or `#171A20` (Black/White inverted).
- **Btn Secondary**: `backdrop-blur-md bg-white/10` (Glass).

### 3.2 Typography
- **Font**: `GothamSSm` (Gotham Screen Smart) or `Universal Sans`.
- **Style**: Clean, geometric, wide aperture.
- **Specs**: Data (0-60mph) is displayed large and thin.

## 4. Component Recipes

### The "Full-Screen Section"
- **Container**: `h-screen w-full relative snap-center`.
- **Media**: `absolute inset-0 object-cover`.
- **Content**: `aboslute top-20 w-full text-center flex-col`.
- **Title**: `text-4xl font-medium fade-in-up`.

### The "Ghost Button" group
- **Layout**: Fixed at bottom center of screen.
- **White Button**: `bg-[#F4F4F4]/65 backdrop-blur-sm text-[#393C41] w-[264px] rounded-[4px]`.
- **Dark Button**: `bg-[#171A20]/65 text-white w-[264px] rounded-[4px]`.
- **Spacing**: `gap-6`.

### The "Configurator Option"
- **Shape**: Circle `w-12 h-12`.
- **Fill**: Gradient representing car paint.
- **State**: Selected has a ring around it (`ring-2 ring-blue-500 ring-offset-2`).

## 5. Interaction Patterns
- **Fade In**: Element entry is slow (`duration-1000`) and delayed.
- **Smoothness**: No jagged movements. Everything glides.
