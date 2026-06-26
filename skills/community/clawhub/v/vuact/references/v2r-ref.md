# v2r Component Ref

Use this when you want to access methods exposed by a Vue component instance from React.

`./counter.vue`:

```vue
<script setup lang="ts">
import { ref } from 'vue';

interface Props {
  defaultCount?: number;
}
const props = withDefaults(defineProps<Props>(), {
  defaultCount: 0,
});

const count = ref(props.defaultCount);

defineExpose({
  incCount: () => {
    count.value++;
  },
});
</script>

<template>
  <div>
    <p>count {{ count }}</p>
  </div>
</template>
```

`./example.tsx`:

```tsx
import { useRef, v2r, type ReactComponentRefType } from 'vuact';
import Counter from './counter.vue';

const RCounter = v2r(Counter);

export default function Example() {
  const counterRef = useRef<ReactComponentRefType<typeof RCounter>>(null);
  return (
    <div>
      <button onClick={() => counterRef.current?.incCount()}>incCount</button>
      <RCounter
        ref={(instance) => {
          counterRef.current = instance;
        }}
        defaultCount={1}
      />
    </div>
  );
}
```
