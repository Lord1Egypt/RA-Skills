# v2r Event Callbacks

Use this when you want to pass update events from React to a Vue component.

`./counter.vue`:

```vue
<script setup lang="ts">
import { useModel } from 'vue';

interface Props {
  count?: number;
}
const props = withDefaults(defineProps<Props>(), {
  count: 0,
});

defineEmits<{
  'update:count': [d: number];
}>();

const count = useModel(props, 'count');

function onClick() {
  count.value++;
}
</script>

<template>
  <div>
    <p>You clicked {{ count }} times</p>
    <button @click="onClick">Click me</button>
  </div>
</template>
```

`./example.tsx`:

```tsx
import { v2r } from 'vuact';
import { useState } from 'react';
import Counter from './counter.vue';

const RCounter = v2r(Counter);

export default function Example() {
  const [count, setCount] = useState(1);
  return <RCounter count={count} onUpdate:count={setCount} />;
}
```
