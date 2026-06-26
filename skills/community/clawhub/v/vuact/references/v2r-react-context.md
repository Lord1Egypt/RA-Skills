# v2r React Context

Use this when you want to pass data to a Vue component from React via React Context.

`./context.ts`:

```ts
import { createContext } from 'react';

export const CounterContext = createContext({
  count: 0,
  setCount: (count: number) => {},
});
```

`./counter.vue`:

```vue
<script setup lang="ts">
import { injectContext } from 'vuact';
import { CounterContext } from './context';

const counterContextRef = injectContext(CounterContext);

function onClick() {
  counterContextRef.value.setCount(counterContextRef.value.count + 1);
}
</script>

<template>
  <div>
    <p>You clicked {{ counterContextRef.count }} times</p>
    <button @click="onClick">Click me</button>
  </div>
</template>
```

`./example.tsx`:

```tsx
import { v2r } from 'vuact';
import { useState } from 'react';
import Counter from './counter.vue';
import { CounterContext } from './context';

const RCounter = v2r(Counter);

export default function Example() {
  const [context, setContext] = useState({
    count: 1,
    setCount,
  });

  function setCount(count: number) {
    setContext({
      ...context,
      count,
    });
  }

  return (
    <CounterContext.Provider value={context}>
      <RCounter />
    </CounterContext.Provider>
  );
}
```
