---
name: lifecycles-isomorphic-layout-effect
description: useLayoutEffect that works on server with useIsomorphicLayoutEffect hook
---

# useIsomorphicLayoutEffect

`useLayoutEffect` that does not show warning when server-side rendering, see [Alex Reardon's article](https://medium.com/@alexandereardon/uselayouteffect-and-ssr-192986cdcf7a) for more info.

## Usage

```jsx
import {useIsomorphicLayoutEffect} from 'react-use';

const Demo = ({value}) => {
  useIsomorphicLayoutEffect(() => {
    window.console.log(value)
  }, [value]);

  return null;
};
```

## Reference

```ts
useIsomorphicLayoutEffect(effect: EffectCallback, deps?: ReadonlyArray<any> | undefined);
```

Same signature as `useLayoutEffect`, but uses `useEffect` on server.

## Key Points

- No SSR warnings
- Uses `useLayoutEffect` on client, `useEffect` on server
- Useful for SSR applications

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useIsomorphicLayoutEffect.md
-->
