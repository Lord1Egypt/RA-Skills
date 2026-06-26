---
name: sensors-mouse
description: Track mouse position with useMouse and useMouseHovered hooks
---

# useMouse and useMouseHovered

React sensor hooks that re-render on mouse position changes. `useMouse` simply tracks mouse position; `useMouseHovered` allows you to specify extra options:
- `bound` - to bind mouse coordinates within the element
- `whenHovered` - whether to attach `mousemove` event handler only when user hovers over the element

## Usage

```jsx
import {useMouse} from 'react-use';

const Demo = () => {
  const ref = React.useRef(null);
  const {docX, docY, posX, posY, elX, elY, elW, elH} = useMouse(ref);

  return (
    <div ref={ref}>
      <div>Mouse position in document - x:{docX} y:{docY}</div>
      <div>Mouse position in element - x:{elX} y:{elY}</div>
      <div>Element position- x:{posX} y:{posY}</div>
      <div>Element dimensions - {elW}x{elH}</div>
    </div>
  );
};
```

## Reference

```ts
useMouse(ref);
useMouseHovered(ref, {bound: false, whenHovered: false});
```

Returns an object with:
- `docX`, `docY`: mouse position relative to document
- `posX`, `posY`: element position
- `elX`, `elY`: mouse position relative to element
- `elW`, `elH`: element dimensions

## Key Points

- `useMouse` tracks mouse position continuously
- `useMouseHovered` can be optimized to only track when hovering
- Provides both document and element-relative coordinates

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useMouse.md
-->
