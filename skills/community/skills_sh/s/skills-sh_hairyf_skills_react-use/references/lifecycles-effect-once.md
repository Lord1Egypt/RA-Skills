---
name: lifecycles-effect-once
description: Modified useEffect that only runs once with useEffectOnce hook
---

# useEffectOnce

React lifecycle hook that runs an effect only once.

## Usage

```jsx
import {useEffectOnce} from 'react-use';

const Demo = () => {
  useEffectOnce(() => {
    console.log('Running effect once on mount')

    return () => {
      console.log('Running clean-up of effect on unmount')
    }
  });

  return null;
};
```

## Reference

```js
useEffectOnce(effect: EffectCallback);
```

- **`effect`**: `EffectCallback` - effect function with optional cleanup

## Key Points

- Runs effect only on mount
- Cleanup runs on unmount
- Useful for one-time setup

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useEffectOnce.md
-->
