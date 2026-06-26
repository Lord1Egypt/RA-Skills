---
name: framer-motion-gestures
description: Official Framer Motion skill for gesture animations — drag, pan, tap, hover, focus, touch animations. Use when building interactive elements with drag, pan, tap, hover, or touch gestures, or when asking about Framer Motion drag constraints, gesture handlers, or interactive animations.
license: MIT
---

# Framer Motion Gestures

## When to Use This Skill

Apply when implementing gesture-driven animations: drag, pan, tap, hover, focus, or touch interactions. When the user asks about drag-and-drop, interactive elements, or gesture-based UI in Framer Motion.

**Related skills:** For core animation use **framer-motion-core**; for variants use **framer-motion-variants**; for layout animations use **framer-motion-layout**.

## Drag

Enable dragging with the `drag` prop:

```jsx
<motion.div
  drag="x"
  dragConstraints={{ left: -100, right: 100 }}
  whileDrag={{ scale: 1.1, cursor: "grabbing" }}
/>
```

### Drag Props

| Prop | Type | Description |
|------|------|-------------|
| **drag** | `bool \| "x" \| "y"` | Enable drag on axis |
| **dragConstraints** | `object \| RefObject` | Movement constraints |
| **dragMomentum** | `boolean` | Continue momentum after release (default: true) |
| **dragElastic** | `number \| object` | Elasticity of bounds (default: 0) |
| **dragTransition** | `Transition` | Spring config for momentum |
| **whileDrag** | `MotionProps` | Animation while dragging |
| **onDrag** | `function` | Callback during drag |
| **onDragStart** | `function` | Callback when drag starts |
| **onDragEnd** | `function` | Callback when drag ends |

### Drag Constraints

```jsx
<motion.div
  drag
  dragConstraints={{
    left: -100,
    right: 100,
    top: -50,
    bottom: 50
  }}
/>
```

### Ref-based Constraints

```jsx
function Draggable() {
  const constraintsRef = useRef(null);

  return (
    <>
      <motion.div
        ref={constraintsRef}
        style={{
          width: 500,
          height: 500,
          backgroundColor: "#eee"
        }}
      />
      <motion.div
        drag
        dragConstraints={constraintsRef}
      />
    </>
  );
}
```

## Pan

Pan is similar to drag but for pointer/touch:

```jsx
<motion.div
  drag="x"
  onDrag={(e, info) => {
    console.log("Position:", info.point);
    console.log("Velocity:", info.velocity);
  }}
/>
```

### Pan vs Drag

- **Drag**: Mouse/touch with visual feedback, momentum, and constraints
- **Pan**: Lower-level pointer tracking without momentum

## Tap (whileTap)

Animation when pressed:

```jsx
<motion.button
  whileTap={{ scale: 0.95, opacity: 0.8 }}
  whileHover={{ scale: 1.05 }}
>
  Click me
</motion.button>
```

## Hover (whileHover)

Animation on hover:

```jsx
<motion.div
  whileHover={{ scale: 1.1, backgroundColor: "#ff0000" }}
  style={{ width: 100, height: 100, backgroundColor: "#00ff00" }}
/>
```

### onHoverStart / onHoverEnd

```jsx
<motion.div
  onHoverStart={() => console.log("Hover started")}
  onHoverEnd={() => console.log("Hover ended")}
/>
```

## Focus (whileFocus)

Animation when focused (keyboard):

```jsx
<motion.input
  whileFocus={{ scale: 1.05, borderColor: "#00ff00" }}
  style={{ borderWidth: 2 }}
/>
```

## Drag with Spring Physics

```jsx
<motion.div
  drag="x"
  dragConstraints={{ left: -200, right: 200 }}
  dragTransition={{
    type: "spring",
    stiffness: 300,
    damping: 20,
    mass: 1
  }}
/>
```

## Drag Controls with Constraints

```jsx
function DraggableBox() {
  const constraintsRef = useRef(null);

  return (
    <>
      <motion.div
        ref={constraintsRef}
        style={{
          width: 500,
          height: 500,
          backgroundColor: "#f0f0f0"
        }}
      />
      {[1, 2, 3].map(i => (
        <motion.div
          key={i}
          drag
          dragConstraints={constraintsRef}
          dragMomentum={false}
          whileDrag={{ scale: 1.1 }}
        />
      ))}
    </>
  );
}
```

## Swipe Detection

```jsx
function Swipeable() {
  const x = useMotionValue(0);
  const { scrollYProgress } = useScroll();

  const opacity = useTransform(x, [-100, 0, 100], [0, 1, 0]);

  return (
    <motion.div
      style={{ x, opacity }}
      drag="x"
      dragConstraints={{ left: 0, right: 0 }}
      dragElastic={1}
    />
  );
}
```

## Gesture State Info

Callbacks receive `PointInfo` and `DragInfo`:

```jsx
onDrag={(e, info) => {
  info.point      // { x, y } position
  info.velocity   // { x, y } velocity
  info.offset     // { x, y } offset from start
}}
```

## Best practices

- ✅ Use **dragConstraints** to keep elements within bounds.
- ✅ Use **dragElastic** for bounce-back effects.
- ✅ Use **whileDrag** for visual feedback during drag.
- ✅ Use **dragMomentum** for natural continuation.
- ✅ Use **dragTransition** with spring for physics-based drag.
- ✅ Use refs for constraints when dragging within a container.

## Do Not

- ❌ Use `drag` without `dragConstraints` if the element should stay within bounds.
- ❌ Forget that drag events only fire after the pointer moves a threshold.
- ❌ Use excessive `dragElastic` — it can cause visual glitches.
- ❌ Animate conflicting properties during drag (e.g., scale and x).

### Learn More

https://www.framer.com/motion/gestures/
https://www.framer.com/motion/drag/
