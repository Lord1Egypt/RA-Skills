---
name: lifecycles-lifecycles
description: Call mount and unmount callbacks with useLifecycles hook
---

# useLifecycles

React lifecycle hook that calls `mount` and `unmount` callbacks, when component is mounted and un-mounted, respectively.

## Usage

```jsx
import {useLifecycles} from 'react-use';

const Demo = () => {
  useLifecycles(() => console.log('MOUNTED'), () => console.log('UNMOUNTED'));
  return null;
};
```

## Reference

```js
useLifecycles(mount, unmount);
```

- **`mount`**: `() => void` - callback when component mounts
- **`unmount`**: `() => void` - callback when component unmounts

## Key Points

- Combines mount and unmount callbacks
- Simpler than separate useMount/useUnmount
- Useful for setup/cleanup patterns

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useLifecycles.md
-->
