# v2r Vue Context

Use this when you want to provide Vue Context to a Vue component from the React side.

`./context.ts`:

```ts
import { type InjectionKey, type Ref } from 'vue';

export interface CounterContext {
  count: Ref<number>;
  setCount: (count: number) => void;
}

export const counterInjectionKey: InjectionKey<CounterContext> =
  Symbol('Counter');
```

`./counter.vue`:

```vue
<script setup lang="ts">
import { inject } from 'vue';
import { counterInjectionKey } from './context';

const counterContext = inject(counterInjectionKey)!;
const { count } = counterContext;

function onClick() {
  counterContext.setCount(count.value + 1);
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
import { v2r, VueContextProvider } from 'vuact';
import { useMemo } from 'react';
import { shallowRef } from 'vue';
import Counter from './counter.vue';
import { type CounterContext, counterInjectionKey } from './context';

const RCounter = v2r(Counter);

export default function Example() {
  const counterContext = useMemo(() => {
    const count = shallowRef(1);
    return {
      count,
      setCount: (c) => {
        count.value = c;
      },
    } as CounterContext;
  }, []);

  return (
    <VueContextProvider contextKey={counterInjectionKey} value={counterContext}>
      <RCounter />
    </VueContextProvider>
  );
}
```
