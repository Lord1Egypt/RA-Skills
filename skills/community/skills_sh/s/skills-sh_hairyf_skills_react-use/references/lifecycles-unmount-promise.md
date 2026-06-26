---
name: lifecycles-unmount-promise
description: Track if component is mounted with promise support using useUnmountPromise hook
---

# useUnmountPromise

A life-cycle hook that provides a higher order promise that does not resolve if component un-mounts.

## Usage

```ts
import useUnmountPromise from 'react-use/lib/useUnmountPromise';

const Demo = () => {
  const mounted = useUnmountPromise();
  useEffect(async () => {
    await mounted(someFunction()); // Will not resolve if component un-mounts.
  });
};
```

## Reference

```ts
const mounted = useUnmountPromise();

mounted(promise);
mounted(promise, onError);
```

- **`mounted`**: `(promise: Promise<T>, onError?: (error: Error) => void) => Promise<T>` - wrapper function
- **`onError`**: `(error: Error) => void` - if promise rejects after component is unmounted, `onError` callback is called with the error

## Key Points

- Prevents promise resolution after unmount
- Useful for async operations
- Provides error handling for unmounted components

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useUnmountPromise.md
-->
