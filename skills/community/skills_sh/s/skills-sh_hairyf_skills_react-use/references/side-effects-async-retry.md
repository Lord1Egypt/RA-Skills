---
name: side-effects-async-retry
description: Async function with retry capability using useAsyncRetry hook
---

# useAsyncRetry

Uses `useAsync` with an additional `retry` method to easily retry/refresh the async function.

## Usage

```jsx
import {useAsyncRetry} from 'react-use';

const Demo = ({url}) => {
  const state = useAsyncRetry(async () => {
    const response = await fetch(url);
    const result = await response.text();
    return result;
  }, [url]);

  return (
    <div>
      {state.loading
        ? <div>Loading...</div>
        : state.error
          ? <div>Error: {state.error.message}</div>
          : <div>Value: {state.value}</div>
      }
      {!loading && <button onClick={() => state.retry()}>Start loading</button>}
    </div>
  );
};
```

## Reference

```ts
useAsyncRetry(fn, args?: any[]);
```

Returns state object with additional `retry` method:
- `retry()`: `() => void` - retry the async function

## Key Points

- Extends `useAsync` with retry capability
- Provides `retry()` method to refresh data
- Useful for retry-on-error patterns

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useAsyncRetry.md
-->
