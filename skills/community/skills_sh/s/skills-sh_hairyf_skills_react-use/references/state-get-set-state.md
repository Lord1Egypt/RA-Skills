---
name: state-get-set-state
description: Combination of useGetSet and useSetState with useGetSetState hook
---

# useGetSetState

A mix of `useGetSet` and `useSetState`.

## Usage

```jsx
import {useGetSetState} from 'react-use';

const Demo = () => {
  const [get, setState] = useGetSetState({cnt: 0});
  const onClick = () => {
    setTimeout(() => {
      setState({cnt: get().cnt + 1})
    }, 1000);
  };

  return (
    <button onClick={onClick}>Clicked: {get().cnt}</button>
  );
};
```

## Reference

```ts
const [get, setState] = useGetSetState(initialState);
```

- **`get()`**: `() => S` - getter function
- **`setState(partial)`**: `(partial: Partial<S> | ((state: S) => Partial<S>)) => void` - merges state like setState

## Key Points

- Combines getter with object state merging
- Prevents stale closures
- Object state updates

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useGetSetState.md
-->
