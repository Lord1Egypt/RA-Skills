---
name: lifecycles-mount
description: Call mount callbacks with useMount hook
---

# useMount

React lifecycle hook that calls a function after the component is mounted. Use `useLifecycles` if you need both a mount and unmount function.

## Usage

```jsx
import {useMount} from 'react-use';

const Demo = () => {
  useMount(() => alert('MOUNTED'));
  return null;
};
```

## Reference

```ts
useMount(fn: () => void);
```

- **`fn`**: `() => void` - callback function

## Key Points

- Calls callback on mount only
- Simple mount-only hook
- Useful for one-time setup

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useMount.md
-->
