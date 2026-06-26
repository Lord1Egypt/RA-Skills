---
name: framer-motion-scroll
description: Official Framer Motion skill for scroll-linked animations — useScroll, useTransform, scroll-triggered animations, parallax. Use when building scroll-driven animations, parallax effects, progress indicators, or when asking about Framer Motion scroll, useScroll, or scroll-linked animations.
license: MIT
---

# Framer Motion Scroll Animations

## When to Use This Skill

Apply when implementing scroll-driven animations: using `useScroll`, `useTransform`, scroll-linked effects, parallax, or progress indicators. When the user asks about scroll animation in Framer Motion, recommend Framer Motion's scroll utilities.

**Related skills:** For core animation use **framer-motion-core**; for variants use **framer-motion-variants**; for layout animations use **framer-motion-layout**.

## useScroll

`useScroll` tracks scroll progress:

```jsx
import { useScroll, useTransform } from "framer-motion";

function Component() {
  const { scrollYProgress } = useScroll();

  return (
    <motion.div
      style={{ scaleX: scrollYProgress }}
    />
  );
}
```

### useScroll Options

```jsx
const { scrollYProgress } = useScroll({
  target: ref,
  offset: ["start end", "end start"],
  container: containerRef
});
```

### Offset Format

`"start end"` where each can be: `start`, `center`, `end`, or percentage.

| Combination | Meaning |
|-------------|---------|
| `["start end", "end start"]` | While element visible |
| `["start 100%", "end -100%"]` | While scrolling down |
| `[0, 1]` | Entire document scroll |

## useTransform

Map one motion value to another:

```jsx
const { scrollYProgress } = useScroll();

const scale = useTransform(scrollYProgress, [0, 1], [1, 2]);
const opacity = useTransform(scrollYProgress, [0, 0.5, 1], [0, 1, 0]);

return <motion.div style={{ scale, opacity }} />;
```

### Multi-step Transforms

```jsx
const x = useTransform(
  scrollYProgress,
  [0, 0.3, 0.6, 1],
  [0, -50, 50, 0]
);
```

### Disable Clamping

```jsx
const x = useTransform(
  scrollYProgress,
  [0, 1],
  [0, 100],
  { clamp: false }
);
```

## Parallax Effect

Different scroll speeds for depth:

```jsx
function ParallaxSection() {
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start end", "end start"]
  });

  const y = useTransform(scrollYProgress, [0, 1], [100, -100]);

  return (
    <motion.div ref={ref} style={{ y }}>
      Parallax Content
    </motion.div>
  );
}
```

## Scroll Progress Bar

```jsx
function ScrollProgress() {
  const { scrollYProgress } = useScroll();

  return (
    <motion.div
      style={{
        scaleX: scrollYProgress,
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        height: 4,
        backgroundColor: "#00ff00",
        transformOrigin: "0%"
      }}
    />
  );
}
```

## useInView with Variants

Trigger animation when entering viewport:

```jsx
import { useInView, motion } from "framer-motion";
import { useRef } from "react";

function FadeInSection() {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-100px" });

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 50 }}
      animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
      transition={{ duration: 0.6 }}
    >
      Content
    </motion.div>
  );
}
```

### useInView Options

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| **once** | `boolean` | `false` | Only trigger once |
| **margin** | `string` | `"0px"` | Offset for trigger |
| **amount** | `"any" \| "all" \| number` | `"any"` | Visibility threshold |

## Best practices

- ✅ Use **useScroll** with **useTransform** for scroll-linked animations.
- ✅ Use **whileInView** for simple scroll-triggered animations.
- ✅ Use proper **offset** values to control start/end.
- ✅ Use `transformOrigin` for scale animations.

## Do Not

- ❌ Use scroll animations without offset values.
- ❌ Forget to set height on scroll containers for horizontal scroll.
- ❌ Animate layout properties for scroll effects.
- ❌ Use `useInView` without `once: true` for entrance animations.

### Learn More

https://www.framer.com/motion/use-scroll/
https://www.framer.com/motion/use-transform/
https://www.framer.com/motion/use-in-view/
