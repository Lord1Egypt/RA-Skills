# v2r Basics

v2r (vue-to-react) is a core Vuact function that converts a Vue component into a React component, so you can use Vue components directly in a React app.

**Use cases**:
- Bring an existing Vue component library into a React project
- Gradually migrate Vue components to React
- Mix React and Vue in the same project

## Vue Component

First, you need a standard Vue component. Here is a simple counter example:
`./counter.vue`:

```vue
<script setup lang="ts">
import { ref } from 'vue';

const count = ref(0);
function incCount() {
  count.value += 1;
}
</script>

<template>
  <div>
    <div>{{ count }}</div>
    <button @click="incCount">inc</button>
  </div>
</template>
```

This Vue component:
- Uses `ref` to manage internal state
- Renders DOM elements and handles click events

## React Usage

Use v2r in a React component:

```tsx
import { v2r } from 'vuact';
import Counter from './counter.vue';

// Convert the Vue component into a React component with v2r
const RCounter = v2r(Counter);

export default function Example() {
  return <RCounter defaultCount={1} className="counter" style={{ height: 100 }} />;
}
```

**Key points**:
1. Import `v2r` and your Vue component
2. Call `v2r(VueComponent)` to get a React component
3. Use it like a normal React component
4. Props interop: React `className` and `style` are automatically transformed into Vue `class` and `style` (auto-adds `px` for unitless values)
