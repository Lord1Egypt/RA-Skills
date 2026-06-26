---
name: state-create-reducer
description: Factory of reducer hooks with custom middleware with createReducer
---

# createReducer

Factory for reducer hooks with custom middleware with an identical API as [React's `useReducer`](https://reactjs.org/docs/hooks-reference.html#usereducer). Compatible with [Redux middleware](https://redux.js.org/advanced/middleware).

## Usage

```jsx
import { createReducer } from 'react-use';
import logger from 'redux-logger';
import thunk from 'redux-thunk';

const useThunkReducer = createReducer(thunk, logger);

function reducer(state, action) {
  switch (action.type) {
    case 'increment':
      return { count: state.count + 1 };
    case 'decrement':
      return { count: state.count - 1 };
    default:
      throw new Error();
  }
}

const Demo = () => {
  const [state, dispatch] = useThunkReducer(reducer, { count: 0 });

  return (
    <div>
      <p>count: {state.count}</p>
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
    </div>
  );
};
```

## Reference

```js
const useMiddlewareReducer = createReducer(...middlewares);
```

Returns a hook with same API as `useReducer` but with middleware support.

## Key Points

- Supports Redux middleware
- Compatible with thunk, logger, etc.
- Same API as useReducer

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/createReducer.md
-->
