# v2r Slots

Use this when you want to pass values to Vue slots from React via `slot:`-prefixed props.

`./slots.vue`:

```vue
<script setup lang="ts">
import { ref } from 'vue';

const count = ref(0);

function onClick() {
  count.value++;
}
</script>

<template>
  <div :style="{ marginBottom: '20px', border: '1px solid #ddd' }">
    <button @click="onClick">count: {{ count }}</button>
    <slot name="title" :count="count" />
    <slot :count="count" />
  </div>
</template>
```

`./example.tsx`:

```tsx
import { v2r } from 'vuact';
import SlotsComponent from './slots.vue';

const RSlotsComponent = v2r(SlotsComponent);

export default function Example() {
  return [
    <RSlotsComponent slot:title={<div>title</div>} />,
    <RSlotsComponent
      slot:title={({ count }) => <div>renderTitle {count}</div>}
    />,
    <RSlotsComponent>
      <div>children</div>
    </RSlotsComponent>,
    <RSlotsComponent>
      {({ count }) => <div>children {count}</div>}
    </RSlotsComponent>,
  ];
}
```
