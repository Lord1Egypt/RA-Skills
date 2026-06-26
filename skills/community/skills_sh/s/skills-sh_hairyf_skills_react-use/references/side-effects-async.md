---
name: side-effects-async
description: Resolve async function with useAsync hook
---

# useAsync

React hook that resolves an `async` function or a function that returns a promise.

## Usage

```jsx
import {useAsync} from 'react-use';

const Demo = ({url}) => {
  const state = useAsync(async () => {
    const response = await fetch(url);
    const result = await response.text();
    return result
  }, [url]);

  return (
    <div>
      {state.loading
        ? <div>Loading...</div>
        : state.error
          ? <div>Error: {state.error.message}</div>
          : <div>Value: {state.value}</div>
      }
    </div>
  );
};
```

## Reference

```ts
useAsync(fn, args?: any[]);
```

Returns state object with:
- `loading`: `boolean` - whether async function is executing
- `error`: `Error | null` - error if execution failed
- `value`: `T | undefined` - result value if successful

## Key Points

- Automatically executes on mount and when dependencies change
- Provides loading, error, and value states
- Useful for data fetching

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useAsync.md
-->
