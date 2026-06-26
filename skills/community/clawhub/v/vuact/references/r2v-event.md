# r2v Event Callbacks

r2v supports two-way event passing between Vue and React components. On the Vue side, you listen with `@event-name`. On the React side, you trigger events by calling callback props like `onEventName`.

**Use cases**:
- A React component needs to send data to its Vue parent
- Two-way binding between Vue and React components
- Handling user interaction events

## React Component Example

First, create a React component that accepts a callback:

```tsx
import { useState } from 'react';

export default function Counter({ count, onUpdateCount }: { count: number; onUpdateCount: (count: number) => void }) {
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => onUpdateCount(count + 1)}>Increment</button>
    </div>
  );
}
```

This React component:
- Accepts `count` as the current value
- Accepts `onUpdateCount` to notify the parent about updates
- Calls `onUpdateCount` with the new value when the button is clicked

## Vue Usage (SFC)

Use r2v in a Vue Single-File Component to handle callbacks:

```vue
<script setup lang="ts">
import { ref } from 'vue';
import { r2v } from 'vuact';
import Counter from './counter';

const VCounter = r2v(Counter);
const count = ref(1);
</script>

<template>
  <!-- Listen to the React component's onUpdateCount via @update-count -->
  <VCounter :count="count" @update-count="count = $event" />
</template>
```

**Event mapping rules**:
- React `onUpdateCount` → Vue `@update-count` (camelCase → kebab-case)
- Callback arguments are available as `$event`

## Vue Usage (TSX)

Use r2v in Vue TSX to handle callbacks:

```tsx
import { defineComponent, ref } from 'vue';
import { r2v } from 'vuact';
import Counter from './counter';

const VCounter = r2v(Counter);

export default defineComponent({
  setup: () => {
    const count = ref(1);
    return () => (
      // In TSX, use onUpdateCount directly (same as React)
      <VCounter count={count.value} onUpdateCount={(c) => (count.value = c)} />
    );
  },
});
```

## v-model Support

Vuact also supports Vue's `v-model` sugar. Vue `v-model` update events are exposed to React components as `onUpdate:xxx`:

```vue
<script setup lang="ts">
import { ref } from 'vue';
import { r2v } from 'vuact';
import Input from './input';

const VInput = r2v(Input);
const value = ref('');
</script>

<template>
  <!-- With v-model, the React component receives value and onUpdate:value -->
  <VInput v-model="value" />
</template>
```

The corresponding React component:

```tsx
export default function Input({ value, onUpdateValue }: { value: string; onUpdateValue: (value: string) => void }) {
  return <input value={value} onChange={(e) => onUpdateValue(e.target.value)} />;
}
```
