---
name: sensors-hover
description: Track mouse hover state with useHover and useHoverDirty hooks
---

# useHover and useHoverDirty

React UI sensor hooks that track if some element is being hovered by a mouse.

- `useHover` accepts a React element or a function that returns one, `useHoverDirty` accepts React ref
- `useHover` sets react `onMouseEnter` and `onMouseLeave` events, `useHoverDirty` sets DOM `onmouseover` and `onmouseout` events

## Usage

```jsx
import {useHover} from 'react-use';

const Demo = () => {
  const element = (hovered) =>
    <div>
      Hover me! {hovered && 'Thanks!'}
    </div>;
  const [hoverable, hovered] = useHover(element);

  return (
    <div>
      {hoverable}
      <div>{hovered ? 'HOVERED' : ''}</div>
    </div>
  );
};
```

## Reference

```js
const [newReactElement, isHovering] = useHover(reactElement);
const [newReactElement, isHovering] = useHover((isHovering) => reactElement);
const isHovering = useHoverDirty(ref);
```

## Key Points

- **useHover**: Returns a new React element with hover handlers attached
- **useHoverDirty**: Works with refs, uses DOM events directly
- Use `useHover` when you want to wrap an element, use `useHoverDirty` when you have a ref

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useHover.md
-->
