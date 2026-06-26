# r2v React Context

Use this when you want to provide React Context to a React component from the Vue side.

`./counter.tsx`:

```tsx
import { createContext, useContext } from 'react';

export const CounterContext = createContext({
  count: 0,
  setCount: (count: number) => {},
});

export default function Counter() {
  const { count, setCount } = useContext(CounterContext);
  return (
    <div>
      <p>You clicked {count} times</p>
      <button onClick={() => setCount(count + 1)}>Click me</button>
    </div>
  );
}
```

`./example.vue`:

```vue
<script setup lang="ts">
import { provideContext, r2v } from 'vuact';
import { shallowRef } from 'vue';
import Counter, { CounterContext } from './counter';

const VCounter = r2v(Counter);

function setCount(count: number) {
  counterContextRef.value = {
    ...counterContextRef.value,
    count,
  };
}

const counterContextRef = shallowRef({
  count: 1,
  setCount,
});

provideContext(CounterContext, counterContextRef);
</script>

<template>
  <VCounter />
</template>
```

`./example.vue.tsx`:

```tsx
import { defineComponent, shallowRef } from 'vue';
import { provideContext, r2v } from 'vuact';
import Counter, { CounterContext } from './counter';

const VCounter = r2v(Counter);

export default defineComponent({
  setup: () => {
    function setCount(count: number) {
      counterContextRef.value = {
        ...counterContextRef.value,
        count,
      };
    }

    const counterContextRef = shallowRef({
      count: 1,
      setCount,
    });

    provideContext(CounterContext, counterContextRef);

    return () => {
      return <VCounter />;
    };
  },
});
```
