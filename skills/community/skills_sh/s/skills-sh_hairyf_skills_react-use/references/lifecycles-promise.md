---
name: lifecycles-promise
description: Resolve promise only while component is mounted with usePromise hook
---

# usePromise

React Lifecycle hook that returns a helper function for wrapping promises. Promises wrapped with this function will resolve only when component is mounted.

## Usage

```jsx
import {usePromise} from 'react-use';

const Demo = ({promise}) => {
  const mounted = usePromise();
  const [value, setValue] = useState();

  useEffect(() => {
    (async () => {
      const value = await mounted(promise);
      // This line will not execute if <Demo> component gets unmounted.
      setValue(value);
    })();
  });
};
```

## Reference

```ts
const mounted = usePromise();
const value = await mounted(promise);
```

Returns a function that wraps promises to only resolve if component is mounted.

## Key Points

- Prevents state updates after unmount
- Wraps promises safely
- Useful for async data fetching

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/usePromise.md
-->
