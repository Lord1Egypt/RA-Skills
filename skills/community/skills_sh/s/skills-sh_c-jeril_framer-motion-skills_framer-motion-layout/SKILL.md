---
name: framer-motion-layout
description: Official Framer Motion skill for layout animations — shared layout transitions, layoutId, exit animations, AnimatePresence. Use when building shared element transitions, layout animations, reorderable lists, or when asking about Framer Motion layout, layoutId, or shared transitions.
license: MIT
---

# Framer Motion Layout Animations

## When to Use This Skill

Apply when implementing shared element transitions, layout animations for reordering, or coordinated mount/unmount animations. When the user asks about Framer Motion layout animations, layoutId, or AnimatePresence.

**Related skills:** For core animation use **framer-motion-core**; for variants use **framer-motion-variants**; for React integration use **framer-motion-react**.

## Layout Prop

The `layout` prop enables automatic position animations when layout changes:

```jsx
<motion.div layout>
  {items.map(item => (
    <motion.div key={item.id} layout />
  ))}
</motion.div>
```

### Layout Modes

| Mode | Behavior |
|------|----------|
| `true` | Animate position and size |
| `"position"` | Animate only position |
| `"size"` | Animate only size |

```jsx
<motion.div layout="position" />
<motion.div layout="size" />
```

## layoutId for Shared Element Transitions

`layoutId` enables smooth transitions between elements in different components:

### Page Transitions

```jsx
// Page A
function CardA() {
  return <motion.div layoutId="card" />;
}

// Page B
function CardB() {
  return <motion.div layoutId="card" />;
}
```

When CardA unmounts and CardB mounts with the same `layoutId`, Framer Motion animates the element smoothly between positions.

### Modal Overlays

```jsx
function ListItem({ item, onClick }) {
  return (
    <motion.div layoutId={`item-${item.id}`} onClick={onClick}>
      {item.name}
    </motion.div>
  );
}

function Modal({ item }) {
  return (
    <motion.div layoutId={`item-${item.id}`}>
      <h2>{item.name}</h2>
      <p>{item.description}</p>
    </motion.div>
  );
}
```

## AnimatePresence for Layout

AnimatePresence enables exit animations:

```jsx
import { AnimatePresence, motion } from "framer-motion";

function TodoList({ todos }) {
  return (
    <motion.ul>
      <AnimatePresence>
        {todos.map(todo => (
          <motion.li
            key={todo.id}
            layout
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
          />
        ))}
      </AnimatePresence>
    </motion.ul>
  );
}
```

### AnimatePresence Modes

```jsx
<AnimatePresence mode="wait">
  {isOpen && <Modal key="modal" />}
</AnimatePresence>
```

| Mode | Description |
|------|-------------|
| `"sync"` | All animations run simultaneously (default) |
| `"wait"` | Exit completes before enter starts |
| `"popLayout"` | Exiting element removed from layout immediately |

## Reorderable Lists

Combine layout with drag for reorderable lists:

```jsx
function ReorderableList({ items, setItems }) {
  return (
    <AnimatePresence>
      {items.map(item => (
        <motion.div
          key={item.id}
          layout
          drag
          dragConstraints={{ top: 0, bottom: 0 }}
          onDragEnd={({ info, target }) => {
            // Calculate new index and update
          }}
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.8 }}
        />
      ))}
    </AnimatePresence>
  );
}
```

## Shared Layout with Grid

```jsx
function Grid({ items }) {
  return (
    <motion.div
      layout
      style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fill, minmax(100px, 1fr))",
        gap: 10
      }}
    >
      {items.map(item => (
        <motion.div
          key={item.id}
          layout
          style={{
            width: "100%",
            aspectRatio: 1,
            backgroundColor: item.color
          }}
        />
      ))}
    </motion.div>
  );
}
```

## Exit Animations

Elements must have exit states for AnimatePresence:

```jsx
<motion.div
  initial={{ opacity: 0, scale: 0 }}
  animate={{ opacity: 1, scale: 1 }}
  exit={{ opacity: 0, scale: 0 }}
/>
```

### Exit with layout

```jsx
<motion.div
  layout
  exit={{ opacity: 0, x: -100, transition: { duration: 0.3 } }}
/>
```

## Crossfade with layoutId

When multiple elements share a layoutId at the same level:

```jsx
function Toggle() {
  const [showA, setShowA] = useState(true);

  return (
    <AnimatePresence mode="popLayout">
      {showA ? (
        <motion.div
          key="a"
          layoutId="shape"
          style={{ backgroundColor: "red" }}
        />
      ) : (
        <motion.div
          key="b"
          layoutId="shape"
          style={{ backgroundColor: "blue", borderRadius: "50%" }}
        />
      )}
    </AnimatePresence>
  );
}
```

The element smoothly morphs between states including border radius.

## Best practices

- ✅ Use **layoutId** for shared element transitions between routes/pages.
- ✅ Wrap animated lists with **AnimatePresence** for exit animations.
- ✅ Use **layout** prop for automatic position animations.
- ✅ Use **AnimatePresence mode="popLayout"** for smooth reordering.
- ✅ Define **exit** states for components using AnimatePresence.
- ✅ Use **layout** on parent containers when children need to animate position.

## Do Not

- ❌ Forget to wrap conditionally rendered animated components with AnimatePresence.
- ❌ Use the same layoutId on multiple elements at the same level.
- ❌ Forget to define exit states for components that unmount.
- ❌ Use layout animations without proper keys on children.
- ❌ Animate too many layout elements simultaneously — group or stagger.

### Learn More

https://www.framer.com/motion/layout-animations/
https://www.framer.com/motion/animate-presence/
