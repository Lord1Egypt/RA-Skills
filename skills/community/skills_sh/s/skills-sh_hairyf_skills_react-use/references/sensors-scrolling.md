---
name: sensors-scrolling
description: Track whether user is scrolling with useScrolling hook
---

# useScrolling

React sensor hook that keeps track of whether the user is scrolling or not.

## Usage

```jsx
import { useScrolling } from "react-use";

const Demo = () => {
  const scrollRef = React.useRef(null);
  const scrolling = useScrolling(scrollRef);

  return (
    <div ref={scrollRef}>
      {<div>{scrolling ? "Scrolling" : "Not scrolling"}</div>}
    </div>
  );
};
```

## Reference

```ts
useScrolling(ref: RefObject<HTMLElement>): boolean;
```

Returns `true` if the element is currently being scrolled, `false` otherwise.

## Key Points

- Simple boolean state for scroll activity
- Useful for showing/hiding UI elements during scroll
- Tracks active scrolling state, not just position

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useScrolling.md
-->
