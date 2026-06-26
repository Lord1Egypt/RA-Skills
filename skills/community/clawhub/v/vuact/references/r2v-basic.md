# r2v Basics

r2v (react-to-vue) is a core Vuact function that converts a React component into a Vue component, so you can use React components directly in a Vue app.

**Use cases**:
- Bring an existing React component library into a Vue project
- Gradually migrate React components to Vue
- Mix Vue and React in the same project

## React Component

First, you need a standard React component. Here is a simple counter example:

```tsx
import { useState } from 'react';

export default function Counter({ defaultCount = 0 }: { defaultCount?: number }) {
  const [count, setCount] = useState(defaultCount);
  return (
    <div>
      <p>You clicked {count} times</p>
      <button onClick={() => setCount(count + 1)}>Click me</button>
    </div>
  );
}
```

This React component:
- Accepts `defaultCount` as the initial value
- Uses `useState` to manage internal state
- Renders DOM elements and handles click events

## Vue Usage (SFC)

Use r2v in a Vue Single-File Component (SFC):

```vue
<script setup lang="ts">
import { r2v } from 'vuact';
import Counter from './counter';

// Convert the React component into a Vue component with r2v
const VCounter = r2v(Counter);
</script>

<template>
  <!-- Use the converted component like a normal Vue component -->
  <VCounter :defaultCount="1" class="counter" style="border: 1px solid #ddd" />
</template>
```

**Key points**:
1. Import `r2v` and your React component
2. Call `r2v(ReactComponent)` to get a Vue component
3. Use it in the template like a normal Vue component
4. Props interop: Vue `class`/`style` are automatically transformed into React `className`/`style` object

## Vue Usage (TSX)

If you use TSX in your Vue project:

```tsx
import { defineComponent } from 'vue';
import { r2v } from 'vuact';
import Counter from './counter';

// Convert the React component into a Vue component with r2v
const VCounter = r2v(Counter);

export default defineComponent({
  setup: () => () => <VCounter defaultCount={1} />,
});
```

In TSX, props are passed the same way as in React.
