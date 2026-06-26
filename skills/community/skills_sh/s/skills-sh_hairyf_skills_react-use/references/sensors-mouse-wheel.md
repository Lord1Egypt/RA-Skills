---
name: sensors-mouse-wheel
description: Get deltaY of mouse scrolled with useMouseWheel hook
---

# useMouseWheel

React Hook to get deltaY of mouse scrolled in window.

## Usage

```jsx
import { useMouseWheel } from 'react-use';

const Demo = () => {
  const mouseWheel = useMouseWheel()
  return (
    <>
      <h3>delta Y Scrolled: {mouseWheel}</h3>
    </>
  );
};
```

## Reference

```ts
const deltaY: number = useMouseWheel();
```

Returns the cumulative deltaY value of mouse wheel scrolling.

## Key Points

- Tracks vertical scroll delta
- Useful for custom scroll interactions
- Accumulates scroll values

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useMouseWheel.md
-->
