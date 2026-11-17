---
name: ui-spec-presentation-scroll
description: Detailed engineering specification for implementing "PPT-style" Full-Page Scrolling and Scrollytelling websites.
license: MIT
---

# UI Engineering Spec: Presentation Scroll (PPT-Style)

## 1. Engineering Context (The "Why")
**Mental Model**: "The Interactive Deck" or "Digital Storytelling".
This style turns a website into a curated, linear journey. Unlike traditional websites where the user controls the scroll freely, this model imposes a structured narrative rhythm. It is ideal for portfolios, product launches, pitch decks, and immersive editorial stories.

**Key Traits**:
- **Snap Physics**: The viewport "snaps" to specific sections, ensuring the user always sees a perfectly framed composition.
- **Cinematic Transitions**: Entering a new section triggers choreographed animations (Fade In, Slide Up, Scale).
- **Minimalist UI**: Controls are often hidden or reduced to simple pagination dots to maximize partial immersion.

## 2. Tech Stack Recommendations
- **Core CSS**: `scroll-snap-type` (The native, lightweight foundation).
- **Logic**: Custom React Hooks for intersection observing (to trigger animations).
- **Libraries** (Choose based on complexity):
    - **Leightweight**: Native CSS + `framer-motion` (for component animations).
    - **Standard**: `fullPage.js` or `swiper.js` (mousewheel control enabled).
    - **High-End**: `Lenis` (Smooth Scroll) + `GSAP ScrollTrigger` (for complex pinned animations).

## 3. Design Tokens (The "Rhythm")

### 3.1 Dimensions
- **Viewport**: Every section MUST be `h-screen` (100vh) or `min-h-screen`.
- **Containers**: Content is usually centered `container mx-auto px-6` or full-bleed for media.

### 3.2 Typography
- **Headings**: Massive. Since there is little text per screen, headings act as visual anchors.
    - `text-6xl md:text-8xl font-bold tracking-tighter`
- **Body**: Concise.
    - `text-xl md:text-2xl text-balance` (Uses `text-wrap: balance` for perfect line lengths).

### 3.3 Navigation (The "Compass")
- **Pagination**: Vertical dots on the right (Desktop) or bottom (Mobile).
- **Progress Bar**: A slim line at the top or bottom indicating total read progress.

## 4. Component Recipes

### The "Slide Section" (Native CSS Snap)
A robust, dependency-free implementation of the snap container.

```tsx
// Tailwind + CSS Native Snap
<div className="h-screen w-full overflow-y-scroll snap-y snap-mandatory scroll-smooth">
  {/* Slide 1 */}
  <section className="h-screen w-full snap-start flex items-center justify-center bg-zinc-950 text-white relative overflow-hidden">
     <div className="z-10 text-center space-y-4">
        <h1 className="text-8xl font-black tracking-tighter animate-in fade-in zoom-in duration-1000">
           The Future.
        </h1>
        <p className="text-2xl text-white/60">Is already here.</p>
     </div>
     {/* Background Video/Image here */}
  </section>

  {/* Slide 2 */}
  <section className="h-screen w-full snap-start flex items-center justify-center bg-white text-black">
      <h2>Slide Two</h2>
  </section>
</div>
```

### The "Scrollytelling Layout" (Sticky)
For when you want text to scroll *over* a fixed background.

```tsx
<div className="relative h-[300vh]"> {/* 3x Height for scroll distance */}
  <div className="sticky top-0 h-screen w-full flex items-center justify-center overflow-hidden">
     {/* The Visual that stays fixed and maybe morphs */}
     <img src="/hero.jpg" className="absolute inset-0 w-full h-full object-cover" />
  </div>
  
  {/* The Text Blocks that scroll over */}
  <div className="relative z-10">
     <div className="h-screen flex items-center justify-center pointer-events-none">
        <h2 className="bg-black/50 p-8 rounded-2xl text-white backdrop-blur-md">
           Contextual Overlay 1
        </h2>
     </div>
     <div className="h-screen flex items-center justify-center pointer-events-none">
         <h2 className="bg-black/50 p-8 rounded-2xl text-white backdrop-blur-md">
           Contextual Overlay 2
        </h2>
     </div>
  </div>
</div>
```

## 5. Interaction Patterns
- **Entrance Animations**: Use `IntersectionObserver` to add a `.visible` class when a slide comes into view.
    - *Example*: Staggered reveal of text lines.
- **Scroll Hijacking (Caution)**: If using libraries like GSAP or Lenis, ensure key commands (Spacebar, Arrows) still work for accessibility.
- **Parallax**: Background moves slower than foreground. `translate-y-[-20%]` on the background image.

## 6. SEO & Accessibility (Crucial for this style)
- **Problem**: Full-page scroll often hides content from spiders if not careful.
- **Fix**: content MUST be in the DOM. Do not `display: none` off-screen sections; just use `opacity: 0` or simply let them exist below the fold.
- **Keyboard**: Ensure users can Arrow Down to snap to the next section.
