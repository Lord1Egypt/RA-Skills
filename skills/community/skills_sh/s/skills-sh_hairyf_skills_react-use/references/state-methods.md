---
name: state-methods
description: Neat alternative to useReducer with useMethods hook
---

# useMethods

React hook that simplifies the `useReducer` implementation.

## Usage

```jsx
import { useMethods } from 'react-use';

const initialState = {
  count: 0,
};

function createMethods(state) {
  return {
    reset() {
      return initialState;
    },
    increment() {
      return { ...state, count: state.count + 1 };
    },
    decrement() {
      return { ...state, count: state.count - 1 };
    },
  };
}

const Demo = () => {
  const [state, methods] = useMethods(createMethods, initialState);

  return (
    <>
      <p>Count: {state.count}</p>
      <button onClick={methods.decrement}>-</button>
      <button onClick={methods.increment}>+</button>
    </>
  );
};
```

## Reference

```js
const [state, methods] = useMethods(createMethods, initialState);
```

- **`createMethods`**: `(state: S) => { [key: string]: (state: S) => S }` - function that returns methods
- **`initialState`**: `S` - initial state value

## Key Points

- Simpler than useReducer
- Methods return new state
- Cleaner API for state updates

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useMethods.md
-->
