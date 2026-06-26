---
name: state-state-list
description: Circularly iterate over array with useStateList hook
---

# useStateList

Provides handles for circular iteration over states list. Supports forward and backward iterations and arbitrary position set.

## Usage

```jsx
import { useStateList } from 'react-use';

const stateSet = ['first', 'second', 'third', 'fourth', 'fifth'];

const Demo = () => {
  const { state, prev, next, setStateAt, setState, currentIndex, isFirst, isLast } = useStateList(stateSet);

  return (
    <div>
      <pre>
        {state} [index: {currentIndex}], [isFirst: {isFirst}], [isLast: {isLast}]
      </pre>
      <button onClick={() => prev()}>prev</button>
      <button onClick={() => next()}>next</button>
      <button onClick={() => setStateAt(2)}>set state by index</button>
      <button onClick={() => setState('third')}> set state by value</button>
    </div>
  );
};
```

## Reference

```ts
const { state, currentIndex, prev, next, setStateAt, setState, isFirst, isLast } = useStateList<T>(stateSet: T[] = []);
```

- **`prev()`**: go to previous state (wraps to last)
- **`next()`**: go to next state (wraps to first)
- **`setStateAt(index)`**: set by index (supports negative)
- **`setState(value)`**: set by value
- **`isFirst`**: boolean if first element
- **`isLast`**: boolean if last element

## Key Points

- Circular iteration
- Supports forward/backward navigation
- Index-based and value-based setting

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useStateList.md
-->
