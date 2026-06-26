---
name: sensors-window-scroll
description: Track Window scroll position with useWindowScroll hook
---

# useWindowScroll

React sensor hook that re-renders on window scroll.

## Usage

```jsx
import {useWindowScroll} from 'react-use';

const Demo = () => {
  const {x, y} = useWindowScroll();

  return (
    <div>
      <div>x: {x}</div>
      <div>y: {y}</div>
    </div>
  );
};
```

## Reference

```ts
useWindowScroll(): { x: number, y: number };
```

Returns an object with:
- `x`: `number` - horizontal scroll position of the window
- `y`: `number` - vertical scroll position of the window

## Key Points

- Tracks window-level scroll position
- Re-renders on scroll changes
- Useful for scroll-based UI effects like sticky headers

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useWindowScroll.md
-->
