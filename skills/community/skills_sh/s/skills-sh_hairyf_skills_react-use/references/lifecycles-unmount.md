---
name: lifecycles-unmount
description: Call unmount callbacks with useUnmount hook
---

# useUnmount

React lifecycle hook that calls a function when the component will unmount. Use `useLifecycles` if you need both a mount and unmount function.

## Usage

```jsx
import {useUnmount} from 'react-use';

const Demo = () => {
  useUnmount(() => alert('UNMOUNTED'));
  return null;
};
```

## Reference

```ts
useUnmount(fn: () => void | undefined);
```

- **`fn`**: `() => void | undefined` - callback function

## Key Points

- Calls callback on unmount only
- Simple unmount-only hook
- Useful for cleanup

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useUnmount.md
-->
