---
name: state-list
description: Track state of an array with useList hook
---

# useList

Tracks an array and provides methods to modify it. To cause component re-render you have to use these methods instead of direct interaction with array - it won't cause re-render.

We can ensure that actions object and actions itself will not mutate or change between renders, so there is no need to add it to useEffect dependencies and safe to pass them down to children.

## Usage

```jsx
import {useList} from 'react-use';

const Demo = () => {
  const [list, { set, push, updateAt, insertAt, update, updateFirst, upsert, sort, filter, removeAt, clear, reset }] = useList([1, 2, 3, 4, 5]);

  return (
    <div>
      <button onClick={() => set([1, 2, 3])}>Set to [1, 2, 3]</button>
      <button onClick={() => push(Date.now())}>Push timestamp</button>
      <button onClick={() => updateAt(1, Date.now())}>Update value at index 1</button>
      <button onClick={() => removeAt(1)}>Remove element at index 1</button>
      <button onClick={() => filter(item => item % 2 === 0)}>Filter even values</button>
      <button onClick={() => sort((a, b) => a - b)}>Sort ascending</button>
      <button onClick={clear}>Clear</button>
      <button onClick={reset}>Reset</button>
      <pre>{JSON.stringify(list, null, 2)}</pre>
    </div>
  );
};
```

## Reference

```ts
const [list, { 
    set, push, updateAt, insertAt, update, updateFirst,
    upsert, sort, filter, removeAt, clear, reset 
}] = useList(array: any[] | ()=> any[]);
```

Provides comprehensive array manipulation methods.

## Key Points

- Immutable array operations
- Stable action references
- Comprehensive array API

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useList.md
-->
