---
name: framer-motion-variants
description: Official Framer Motion skill for animation variants — state machines, orchestrated animations, stagger, repeat, sequencing. Use when building orchestrated animations, animation state machines, staggered entrances, or when asking about Framer Motion variants, transition variants, or choreographed animations.
license: MIT
---

# Framer Motion Variants

## When to Use This Skill

Apply when building multi-step animations, coordinated animations across multiple elements, or when using variants for state-based animation control. Variants are Framer Motion's way of defining reusable animation states that can be choreographed.

**Related skills:** For core animation props use **framer-motion-core**; for React integration use **framer-motion-react**; for scroll-driven variants use **framer-motion-scroll**.

## Defining Variants

Variants are objects that define animation states:

```jsx
const container = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const item = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 }
};

function Component() {
  return (
    <motion.div
      variants={container}
      initial="hidden"
      animate="visible"
    >
      {[1, 2, 3].map(i => (
        <motion.div key={i} variants={item} />
      ))}
    </motion.div>
  );
}
```

## Variant Types

### Static Variants

```jsx
const variants = {
  initial: { opacity: 0 },
  animate: { opacity: 1 },
  exit: { opacity: 0 }
};
```

### Dynamic Variants

```jsx
const variants = {
  animate: (custom) => ({
    x: custom * 100,
    opacity: 1
  })
};
```

## Orchestration

### staggerChildren

Stagger children animations:

```jsx
const container = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2
    }
  }
};
```

### staggerDirection

```jsx
transition: {
  staggerChildren: 0.1,
  staggerDirection: -1  // 1 = forward, -1 = backward
}
```

## Repeating Animations

```jsx
const variants = {
  animate: {
    scale: [1, 1.5, 1],
    transition: {
      duration: 2,
      repeat: Infinity,
      repeatType: "loop"  // "loop" | "reverse" | "mirror"
    }
  }
};
```

### repeatType Options

| Type | Behavior |
|------|----------|
| `"loop"` | Restart from beginning |
| `"reverse"` | Play forward then backward |
| `"mirror"` | Swap states on each repeat |

## Keyframes

Animate through multiple values:

```jsx
<motion.div
  animate={{
    x: [0, 100, -50, 0],
    backgroundColor: ["#ff0000", "#00ff00", "#0000ff"]
  }}
  transition={{
    duration: 2,
    times: [0, 0.3, 0.6, 1]
  }}
/>
```

## State Machine with custom

```jsx
const states = {
  idle: { scale: 1 },
  hovered: { scale: 1.1 },
  pressed: { scale: 0.95 }
};

function Component({ state }) {
  return (
    <motion.div
      variants={states}
      animate={state}
      custom={state}
    />
  );
}
```

## Parent-Child Coordination

```jsx
const container = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      when: "beforeChildren"
    }
  }
};

const child = {
  hidden: { x: -20, opacity: 0 },
  visible: {
    x: 0,
    opacity: 1,
    transition: { duration: 0.3 }
  }
};
```

## Best practices

- ✅ Use **variants** for reusable, coordinated animations.
- ✅ Use **staggerChildren** for list animations.
- ✅ Use **custom** prop to pass dynamic values.
- ✅ Define **exit** variants for AnimatePresence.
- ✅ Use **when** option for parent-child coordination.

## Do Not

- ❌ Mix motion values and variants incorrectly.
- ❌ Forget that variant transitions can be overridden.
- ❌ Use too many variant states (keep to 3-5).
- ❌ Forget to pass `custom` when needed.

### Learn More

https://www.framer.com/motion/animation/
https://www.framer.com/motion/variants/
