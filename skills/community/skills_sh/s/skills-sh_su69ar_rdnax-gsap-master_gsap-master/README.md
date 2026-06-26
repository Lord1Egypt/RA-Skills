# GSAP Master Skill

> **Full GSAP v3 mastery for interactive websites**

A comprehensive AI skill for building production-grade animations with GSAP. Covers core tweens/timelines, all major plugins, React/Next.js patterns, performance optimization, accessibility, and debugging.

**Author:** rdnax  
**Version:** 1.5.0  
**License:** MIT

---

## 📦 What's Included

```
gsap-master/
├── SKILL.md                              # Main skill instructions
├── README.md                             # This file
└── references/
    ├── GSAP_CORE.md          (13KB)      # Core fundamentals
    ├── GSAP_RECIPES.md       (4KB)       # Quick-reference recipes
    ├── UI_INTERACTIONS.md    (20KB)      # UI patterns & micro-interactions
    ├── TEXT_ANIMATIONS.md    (15KB)      # Text animation patterns
    ├── PHYSICS_PLUGINS.md    (8KB)       # Physics2D & PhysicsProps
    ├── NEXTJS_REACT_PATTERNS.md (8KB)    # Framework integration
    ├── GSDEVTOOLS.md         (8KB)       # Debugging UI
    └── DEBUG_CHECKLIST.md    (5KB)       # Troubleshooting guide
```

---

## 🚀 Installation

### For AI Agents (Antigravity/Gemini)

Place the entire `gsap-master/` folder in your skills directory:

```
~/.gemini/antigravity/global_skills/gsap-master/
```

The skill auto-activates when you mention GSAP-related keywords.

### For Manual Reference

Read `SKILL.md` directly or browse the `references/` folder for topic-specific documentation.

---

## 🎯 Activation Keywords

The skill automatically activates on these topics:

| Category | Keywords |
|----------|----------|
| **Core** | GSAP, Tween, Timeline, easing, stagger, keyframes |
| **Scroll** | ScrollTrigger, ScrollSmoother, ScrollTo, pin, scrub, parallax |
| **UI** | Flip, Draggable, magnetic button, cursor follower, carousel |
| **Text** | SplitText, ScrambleText, TextPlugin, typewriter |
| **SVG** | DrawSVG, MorphSVG, MotionPath |
| **Physics** | Physics2D, PhysicsProps, inertia, gravity |
| **Tools** | GSDevTools, debugging, matchMedia, gsap.context |
| **Framework** | React, Next.js, useGSAP, SSR, cleanup |

---

## 📚 Coverage

### GSAP Core
- Primitives: `gsap.to()`, `gsap.from()`, `gsap.fromTo()`, `gsap.set()`
- Timelines with labels and position parameters
- Easing reference (power, elastic, bounce, custom)
- Stagger patterns (grid, random, from center)
- Callbacks and lifecycle hooks
- Utilities: `quickTo`, `quickSetter`, `mapRange`, `clamp`, `snap`
- `gsap.context()` and `gsap.matchMedia()`

### Plugins

| Plugin | Description |
|--------|-------------|
| **ScrollTrigger** | Scroll-based triggering, scrub, pin, snap |
| **ScrollSmoother** | Smooth scrolling + parallax |
| **ScrollTo** | Programmatic scroll navigation |
| **Observer** | Gesture detection (wheel/touch/pointer) |
| **Flip** | FLIP layout transitions |
| **Draggable** | Drag interactions |
| **InertiaPlugin** | Momentum physics |
| **SplitText** | Character/word/line splitting |
| **ScrambleText** | Text scramble effects |
| **TextPlugin** | Text replacement/typing |
| **DrawSVG** | SVG stroke animations |
| **MorphSVG** | Path morphing |
| **MotionPath** | Animate along paths |
| **Physics2D** | 2D projectile physics |
| **PhysicsProps** | Physics for any property |
| **CustomEase** | Custom easing curves |
| **GSDevTools** | Visual debugging UI |

### Framework Integration
- React `useGSAP()` hook
- `gsap.context()` cleanup pattern
- SSR-safe practices
- Responsive `matchMedia()` patterns
- Reduced motion accessibility

---

## 🔧 Usage

### Ask the AI for Animations

```
"Create a hero animation with staggered text reveal"
"Add scroll-triggered parallax to this section"
"Make this button have a magnetic hover effect"
"Implement a draggable carousel with snap"
"Add physics-based confetti explosion"
```

### What the AI Delivers

1. **Motion plan** - Goals, triggers, states, timing
2. **Implementation** - Minimal working code
3. **Architecture** - Timeline structure, labels
4. **Responsive + A11y** - matchMedia + reduced-motion
5. **Performance notes** - quickTo/quickSetter tips
6. **Debug checklist** - How to verify it works

---

## 📖 Reference Files

### GSAP_CORE.md
Core GSAP fundamentals including:
- All primitives and properties
- Easing reference
- Timeline methods and position parameters
- Utilities and helpers

### UI_INTERACTIONS.md
UI patterns including:
- Button/hover effects (shine, glow, 3D tilt)
- Magnetic effects
- Cursor effects (follower, expand, text)
- Draggable patterns (carousel, card stack, sortable)
- Flip layouts (grid toggle, modal, tabs)
- Micro-interactions

### TEXT_ANIMATIONS.md
Text animation patterns:
- SplitText (chars/words/lines)
- Character/word/line animations
- ScrambleText effects
- TextPlugin typing effects
- Scroll-triggered text
- DIY alternatives

### PHYSICS_PLUGINS.md
Physics animations:
- Physics2D (velocity, angle, gravity)
- PhysicsProps (any property)
- Particle effects, confetti

### NEXTJS_REACT_PATTERNS.md
Framework integration:
- `useGSAP()` hook
- `gsap.context()` patterns
- SSR safety
- Cleanup patterns

### GSDEVTOOLS.md
Debugging:
- Configuration options
- Keyboard shortcuts
- Persistence settings
- React integration

### DEBUG_CHECKLIST.md
Troubleshooting:
- Target/selector issues
- CSS conflicts
- Timeline problems
- ScrollTrigger debugging
- Performance issues

---

## ⚡ Quick Examples

### Basic Tween

```js
gsap.to(".box", { x: 200, rotation: 360, duration: 1 });
```

### Timeline Sequence

```js
const tl = gsap.timeline({ defaults: { ease: "power3.out" } });
tl.from(".title", { y: 30, autoAlpha: 0 })
  .from(".content", { y: 20, autoAlpha: 0 }, "<0.2");
```

### Scroll-Triggered

```js
gsap.from(".reveal", {
  y: 50, autoAlpha: 0,
  scrollTrigger: { trigger: ".reveal", start: "top 80%" }
});
```

### React/Next.js

```jsx
"use client";
import { useRef } from "react";
import gsap from "gsap";
import { useGSAP } from "@gsap/react";

export function Animated() {
  const container = useRef(null);
  
  useGSAP(() => {
    gsap.from(".box", { y: 50, autoAlpha: 0 });
  }, { scope: container });
  
  return <div ref={container}><div className="box">Hi</div></div>;
}
```

---

## 🛠 Maintenance

### Updating the Skill

Edit `SKILL.md` to update activation triggers or output rules.

Add new reference files to `references/` and update the references list in `SKILL.md`.

### Version History

| Version | Changes |
|---------|---------|
| 1.5.0 | Added Physics plugins, comprehensive README |
| 1.4.0 | Added GSAP Core, GSDevTools |
| 1.3.0 | Added Text animations |
| 1.2.0 | Added UI interactions |
| 1.1.0 | Full plugin coverage |
| 1.0.0 | Initial release |

---

## 📜 License

MIT License - Free to use and modify.

---

## 🙏 Credits

- **GSAP** by GreenSock - https://gsap.com
- **Skill Author:** rdnax

---

> *"GSAP is currently the best available tool for creating astonishing interactive websites and animation effects."* - Petr Tichy
