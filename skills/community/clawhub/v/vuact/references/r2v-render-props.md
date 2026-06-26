# r2v Render Props and Slots

Use this when you want to pass a React component’s render props and element props from Vue via slots.

## Core Concepts

### Element Props
Element props mean the prop value passed to a React component is already-rendered content (a React Element) or static content. This kind of prop is evaluated immediately and rendered, and the React component can use it directly, for example:
- Display it as normal content
- Process it with `React.cloneElement`
- Iterate it with `React.Children`

### Render Props
Render props mean the prop value passed to a React component is a function. The function is called inside the React component and returns a React element. Benefits:
- Receive internal state/data from the React component as arguments
- Render dynamically based on those arguments
- Enable data sharing and logic reuse between components

## React Component Example: RenderPropsComponent

```tsx
import { useState } from 'react';

export default function Counter({
  title,
  renderTitle,
  children,
}: {
  title?: any;
  renderTitle?: (count: number) => any;
  children?: any;
}) {
  const [count, setCount] = useState(0);

  return (
    <div style={{ marginBottom: 20, border: '1px solid #ddd' }}>
      <button onClick={() => setCount(count + 1)}>count: {count}</button>
      {title}
      {renderTitle?.(count)}
      {typeof children === 'function' ? children(count) : children}
    </div>
  );
}
```

This React component demonstrates three different prop patterns:
- **title**: Element prop — receives and renders static content directly
- **renderTitle**: Render prop — receives a function and calls it with `count`
- **children**: Compatible with both — can be static content or a function

## slotsTransformConfig

`slotsTransformConfig` configures how Vue slots are converted into React props.

### Options

```typescript
interface SlotTransformConfig {
  /**
   * Whether to convert the slot into an element prop (execute the slot immediately).
   *
   * Defaults:
   * - default slot: true (treated as the children element prop)
   * - other slots: false
   *
   * You can also enable it by prefixing the slot name with `element:`.
   */
  elementProp?: boolean;

  /**
   * Whether to transform the slot result into a React element.
   *
   * Default: false
   *
   * Enable this when the React component needs to operate on elements,
   * e.g. using React.Children or React.cloneElement.
   */
  transformVNode?: boolean;
}
```

### Example

```typescript
const VRenderPropsComponent = r2v(RenderPropsComponent, {
  slotsTransformConfig: {
    // Treat the title slot as an element prop
    title: { elementProp: true },
    // The default slot is an element prop by default; disable it here
    default: { elementProp: false },
  },
});
```

## Vue Usage (SFC)

```vue
<script setup lang="ts">
import { r2v } from 'vuact';
import RenderPropsComponent from './render-props';

const VRenderPropsComponent = r2v(RenderPropsComponent);
const VRenderPropsComponent2 = r2v(RenderPropsComponent, {
  slotsTransformConfig: {
    // Treat the title slot as an element prop
    title: { elementProp: true },
    // The default slot is an element prop by default; disable it here
    default: { elementProp: false },
  },
});
</script>

<template>
  <!-- Option 1: Use the element: prefix to treat title as an element prop -->
  <VRenderPropsComponent>
    <template #element:title>
      <div>title</div>
    </template>
  </VRenderPropsComponent>

  <!-- Option 2: Configure slotsTransformConfig to treat title as an element prop -->
  <VRenderPropsComponent2>
    <template #title>
      <div>title2</div>
    </template>
  </VRenderPropsComponent2>

  <!-- renderTitle as a render prop, receiving count -->
  <VRenderPropsComponent>
    <template #renderTitle="count">
      <div>renderTitle {{ count }}</div>
    </template>
  </VRenderPropsComponent>

  <!-- children as static content -->
  <VRenderPropsComponent>
    <div>children</div>
  </VRenderPropsComponent>

  <!-- children as a render prop, receiving count -->
  <VRenderPropsComponent>
    <template #children="count">
      <div>children {{ count }}</div>
    </template>
  </VRenderPropsComponent>

  <!-- Disable default slot elementProp so it becomes a render prop -->
  <VRenderPropsComponent2>
    <template #default="count">
      <div>children {{ count }}</div>
    </template>
  </VRenderPropsComponent2>
</template>
```

## Vue Usage (TSX)

```tsx
import { defineComponent } from 'vue';
import { r2v } from 'vuact';
import RenderPropsComponent from './render-props';

const VRenderPropsComponent = r2v(RenderPropsComponent);
const VRenderPropsComponent2 = r2v(RenderPropsComponent, {
  slotsTransformConfig: {
    title: { elementProp: true },
    default: { elementProp: false },
  },
});

export default defineComponent({
  setup: () => () => [
    <VRenderPropsComponent>
      {{ 'element:title': () => <div>title</div> }}
    </VRenderPropsComponent>,
    <VRenderPropsComponent2>
      {{ title: () => <div>title</div> }}
    </VRenderPropsComponent2>,
    <VRenderPropsComponent>
      {{ renderTitle: (count) => <div>renderTitle {count}</div> }}
    </VRenderPropsComponent>,
    <VRenderPropsComponent>
      <div>children</div>
    </VRenderPropsComponent>,
    <VRenderPropsComponent>
      {{ children: (count) => <div>children {count}</div> }}
    </VRenderPropsComponent>,
    <VRenderPropsComponent2>
      {(count) => <div>children {count}</div>}
    </VRenderPropsComponent2>,
  ],
});
```
