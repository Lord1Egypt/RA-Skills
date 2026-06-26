---
name: state-set
description: Track state of a Set with useSet hook
---

# useSet

React state hook that tracks a [Set](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set).

## Usage

```jsx
import {useSet} from 'react-use';

const Demo = () => {
  const [set, { add, has, remove, toggle, reset, clear }] = useSet(new Set(['hello']));

  return (
    <div>
      <button onClick={() => add(String(Date.now()))}>Add</button>
      <button onClick={() => reset()}>Reset</button>
      <button onClick={() => clear()}>Clear</button>
      <button onClick={() => remove('hello')} disabled={!has('hello')}>
        Remove 'hello'
      </button>
      <button onClick={() => toggle('hello')}>Toggle hello</button>
      <pre>{JSON.stringify(Array.from(set), null, 2)}</pre>
    </div>
  );
};
```

## Reference

```ts
const [set, { add, has, remove, toggle, reset, clear }] = useSet(initialSet?: Set<T>);
```

- **`add(value)`**: add value to set
- **`has(value)`**: check if value exists
- **`remove(value)`**: remove value
- **`toggle(value)`**: toggle value presence
- **`reset()`**: reset to initial set
- **`clear()`**: empty the set

## Key Points

- Set data structure management
- Unique value collection
- Toggle functionality

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useSet.md
-->
