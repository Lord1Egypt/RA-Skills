---
name: state-get-set
description: Return state getter instead of raw state with useGetSet hook
---

# useGetSet

React state hook that returns state getter function instead of raw state itself, this prevents subtle bugs when state is used in nested functions.

## Usage

```jsx
import {useGetSet} from 'react-use';

const Demo = () => {
  const [get, set] = useGetSet(0);
  const onClick = () => {
    setTimeout(() => {
      set(get() + 1)
    }, 1_000);
  };

  return (
    <button onClick={onClick}>Clicked: {get()}</button>
  );
};
```

## Reference

```ts
const [get, set] = useGetSet(initialValue);
```

- **`get()`**: `() => T` - getter function for current state
- **`set(value)`**: `(value: T) => void` - setter function

## Key Points

- Prevents stale closure bugs
- Always gets latest state
- Useful in async callbacks

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useGetSet.md
-->
