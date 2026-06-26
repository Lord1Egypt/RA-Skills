# Technology Decisions

Rationale behind the technology choices for the website cloner workflow.

## Why Tailwind CSS?

### Arbitrary Values Enable Pixel-Perfect Matching

Tailwind's arbitrary value syntax allows exact values:

```tsx
// Exact hex colors
className="bg-[#1a2b3c] text-[#f5f5f5]"

// Exact pixel values
className="py-[120px] px-[24px] gap-[32px]"

// Exact shadows
className="shadow-[0_4px_24px_rgba(0,0,0,0.1)]"

// Exact border-radius
className="rounded-[16px]"
```

### Benefits over Plain CSS

| Aspect | Tailwind | Plain CSS |
|--------|----------|-----------|
| Colocation | Styles with markup | Separate files |
| Specificity | Flat, no conflicts | Cascade issues |
| Responsiveness | Built-in breakpoints | Manual media queries |
| Consistency | Design system tokens | Ad-hoc values |

### No Build Step for Arbitrary Values

Tailwind's JIT compiler handles arbitrary values automatically. No need to extend the config for one-off clones.

---

## Why motion (not framer-motion)?

### Modern, Lighter Alternative

`motion` is the evolution of framer-motion, designed to be:
- Smaller bundle size
- Simpler API
- Better tree-shaking

### Import Pattern

```tsx
// Correct - motion/react
import { motion } from "motion/react"

// Wrong - framer-motion (legacy)
import { motion } from "framer-motion"
```

### Common Animation Patterns

```tsx
// Fade in on scroll
<motion.div
  initial={{ opacity: 0, y: 20 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true }}
  transition={{ duration: 0.6 }}
>

// Hover effect
<motion.button
  whileHover={{ scale: 1.02 }}
  whileTap={{ scale: 0.98 }}
>

// Stagger children
<motion.div
  initial="hidden"
  whileInView="visible"
  variants={{
    visible: { transition: { staggerChildren: 0.1 } }
  }}
>
```

---

## Why Single Component?

### Focus on Cloning, Not Architecture

When cloning a website, the goal is visual fidelity, not optimal code structure. A single component:

1. **Reduces cognitive overhead** - One file to work with
2. **Simplifies iteration** - QA feedback maps directly to sections
3. **Avoids premature abstraction** - User can refactor later if needed

### Section Comments as Organization

Instead of separate files, use multi-line comments:

```tsx
{/* ============================================
    HERO SECTION
    ============================================ */}
<section className="...">
  {/* Hero content */}
</section>

{/* ============================================
    FEATURES SECTION
    ============================================ */}
<section className="...">
  {/* Features content */}
</section>
```

### Easy to Refactor Later

User can extract sections into components after cloning is complete:

```tsx
// Before (single file)
<HeroSection />  // Extract from comment block

// After (componentized)
import HeroSection from '@/components/HeroSection'
```

---

## Why Auto-Detect Framework?

### Supports User's Existing Setup

Users run `/clone-website` within their existing project. The cloner should:

1. Detect what framework they're using
2. Output to the correct location
3. Use framework-appropriate patterns

### Detection Logic

```bash
# Check package.json
grep '"next"' package.json        → Next.js
grep '"@tanstack/start"' package.json → TanStack Start
grep '"vite"' package.json        → Vite
```

### Framework-Specific Patterns

| Framework | Output Path | Special Handling |
|-----------|-------------|------------------|
| Next.js App Router | `app/clone/page.tsx` | Add `"use client"` directive |
| Next.js Pages | `pages/clone.tsx` | No directive needed |
| TanStack Start | `src/routes/clone.tsx` | Follow TanStack conventions |
| Vite | `src/pages/Clone.tsx` | Standard React |

### Image Components

```tsx
// Next.js
import Image from "next/image"
<Image src="/images/hero.jpg" alt="..." fill className="object-cover" />

// Other frameworks
<img src="/images/hero.jpg" alt="..." className="object-cover w-full h-full" />
```

---

## Why public/ for Assets?

### Standard Convention

All modern frameworks serve static files from `public/`:

```
public/images/logo.png → /images/logo.png
public/videos/bg.mp4   → /videos/bg.mp4
```

### Organized Structure

```
public/
├── images/    # Photos, logos, backgrounds
├── videos/    # Background videos
└── icons/     # SVGs, icons
```

### Benefits

1. **Works across frameworks** - Same structure for Next.js, Vite, etc.
2. **Simple paths** - `/images/logo.png` works everywhere
3. **Persists across iterations** - Assets downloaded once
4. **Easy to manage** - User can add/replace assets

---

## Why Playwright MCP?

### Real Browser Environment

Playwright provides actual browser automation:
- Real CSS rendering
- Real computed styles
- Real hover states
- Real animations

### Key Capabilities

| Capability | Use Case |
|------------|----------|
| `navigate` | Go to original/clone URLs |
| `screenshot` | Capture visual references |
| `evaluate` | Extract computed styles via JS |
| `hover` | Capture hover states |
| `click` | Interact with elements |

### Extracting Computed Styles

```javascript
// Via Playwright evaluate
window.getComputedStyle(element).getPropertyValue('color')
window.getComputedStyle(element).getPropertyValue('font-size')
window.getComputedStyle(element).getPropertyValue('padding')
```

---

## Alternative Approaches Considered

### Why Not HTML/CSS Output?

| HTML/CSS | React/Tailwind |
|----------|----------------|
| Standalone file | Integrates with project |
| Manual deployment | Works with existing build |
| No component reuse | Easy to extend |
| Static only | Can add interactivity |

### Why Not CSS Modules?

| CSS Modules | Tailwind |
|-------------|----------|
| Separate files | Colocated |
| Class name mapping | Direct styling |
| Build step required | JIT compiles |
| Harder to match exact values | Arbitrary values |

### Why Not Styled Components?

| Styled Components | Tailwind |
|-------------------|----------|
| Runtime CSS-in-JS | Zero runtime |
| Template literals | Class utilities |
| Theme configuration | Arbitrary values |
| Learning curve | Familiar CSS concepts |
