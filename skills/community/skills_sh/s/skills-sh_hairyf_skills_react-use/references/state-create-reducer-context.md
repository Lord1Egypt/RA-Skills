---
name: state-create-reducer-context
description: Factory of hooks for sharing reducer state between components with createReducerContext
---

# createReducerContext

Factory for react context hooks that will behave just like [React's `useReducer`](https://reactjs.org/docs/hooks-reference.html#usereducer) except the state will be shared among all components in the provider.

This allows you to have a shared state that any component can update easily.

## Usage

```jsx
import { createReducerContext } from 'react-use';

type Action = 'increment' | 'decrement';

const reducer = (state: number, action: Action) => {
  switch (action) {
    case 'increment':
      return state + 1;
    case 'decrement':
      return state - 1;
    default:
      throw new Error();
  }
};

const [useSharedCounter, SharedCounterProvider] = createReducerContext(reducer, 0);

const ComponentA = () => {
  const [count, dispatch] = useSharedCounter();
  return (
    <p>
      Component A &nbsp;
      <button onClick={() => dispatch('decrement')}>-</button>
      &nbsp;{count}&nbsp;
      <button onClick={() => dispatch('increment')}>+</button>
    </p>
  );
};

const Demo = () => {
  return (
    <SharedCounterProvider>
      <ComponentA />
    </SharedCounterProvider>
  );
};
```

## Reference

```jsx
const [useSharedState, SharedStateProvider] = createReducerContext(reducer, initialState);
```

Returns hook and provider for shared reducer state.

## Key Points

- Shared state via Context
- Reducer pattern
- Provider-based sharing

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/createReducerContext.md
-->
