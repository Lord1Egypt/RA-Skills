---
name: state-raf-state
description: setState that only updates after requestAnimationFrame with useRafState hook
---

# useRafState

React state hook that only updates state in the callback of [`requestAnimationFrame`](https://developer.mozilla.org/en-US/docs/Web/API/window/requestAnimationFrame).

## Usage

```jsx
import {useRafState, useMount} from 'react-use';

const Demo = () => {
  const [state, setState] = useRafState({
    width: 0,
    height: 0,
  });

  useMount(() => {
    const onResize = () => {
      setState({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    window.addEventListener('resize', onResize);

    return () => {
      window.removeEventListener('resize', onResize);
    };
  });

  return <pre>{JSON.stringify(state, null, 2)}</pre>;
};
```

## Reference

```ts
const [state, setState] = useRafState(initialState);
```

Same API as `useState`, but updates are batched in requestAnimationFrame.

## Key Points

- Updates batched in RAF
- Better performance for frequent updates
- Useful for scroll/resize handlers

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useRafState.md
-->
