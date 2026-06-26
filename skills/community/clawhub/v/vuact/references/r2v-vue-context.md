# r2v Vue Context

Use this when you want to provide Vue Context from the Vue side and let a React component read it.

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

`./counter.tsx`:

```tsx
import { inject } from 'vue';
import { counterInjectionKey } from './context';

export default function Counter() {
  const context = inject(counterInjectionKey)!;
  return (
    <div>
      <p>You clicked {context.count.value} times</p>
      <button onClick={() => context.setCount(context.count.value + 1)}>
        Click me
      </button>
    </div>
  );
}
```

`./example.vue`:

```vue
<script setup lang="ts">
import { r2v } from 'vuact';
import { provide, shallowRef } from 'vue';
import { counterInjectionKey, type CounterContext } from './context';
import Counter from './counter';

const VCounter = r2v(Counter);

const counterContext: CounterContext = {
  count: shallowRef(1),
  setCount: (count) => {
    counterContext.count.value = count;
  },
};

provide(counterInjectionKey, counterContext);
</script>

<template>
  <VCounter />
</template>
```
