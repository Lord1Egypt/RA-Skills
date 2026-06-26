---
name: sensors-scroll
description: Track scroll position in DOM element with useScroll hook
---

# useScroll

React sensor hook that re-renders when the scroll position in a DOM element changes.

## Usage

```jsx
import {useScroll} from 'react-use';

const Demo = () => {
  const scrollRef = React.useRef(null);
  const {x, y} = useScroll(scrollRef);

  return (
    <div ref={scrollRef}>
      <div>x: {x}</div>
      <div>y: {y}</div>
    </div>
  );
};
```

## Reference

```ts
useScroll(ref: RefObject<HTMLElement>);
```

Returns an object with:
- `x`: `number` - horizontal scroll position
- `y`: `number` - vertical scroll position

## Key Points

- Tracks scroll position of a specific element
- Re-renders on scroll changes
- Useful for scroll-based animations or indicators

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useScroll.md
-->
