---
name: side-effects-error
description: Error dispatcher with useError hook
---

# useError

React side-effect hook that returns an error dispatcher.

## Usage

```jsx
import { useError } from 'react-use';

const Demo = () => {
  const dispatchError = useError();

  const clickHandler = () => {
    dispatchError(new Error('Some error!'));
  };

  return <button onClick={clickHandler}>Click me to throw</button>;
};

// In parent app
const App = () => (
  <ErrorBoundary>
    <Demo />
  </ErrorBoundary>
);
```

## Reference

```js
const dispatchError = useError();
```

- **`dispatchError`**: `(err: Error) => void` - callback to dispatch error

## Key Points

- Dispatches errors to ErrorBoundary
- Useful for programmatic error handling
- Works with React Error Boundaries

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useError.md
-->
