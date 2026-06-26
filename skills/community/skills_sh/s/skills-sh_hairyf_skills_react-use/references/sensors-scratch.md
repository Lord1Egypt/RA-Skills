---
name: sensors-scratch
description: Track mouse click-and-scrub state with useScratch hook
---

# useScratch

React sensor hook that tracks state of mouse "scrubs" (or "scratches").

## Usage

```jsx
import useScratch from 'react-use/lib/useScratch';

const Demo = () => {
  const [ref, state] = useScratch();

  const blockStyle: React.CSSProperties = {
    position: 'relative',
    width: 400,
    height: 400,
    border: '1px solid tomato',
  };

  let { x = 0, y = 0, dx = 0, dy = 0 } = state;
  if (dx < 0) [x, dx] = [x + dx, -dx];
  if (dy < 0) [y, dy] = [y + dy, -dy];

  const rectangleStyle: React.CSSProperties = {
    position: 'absolute',
    left: x,
    top: y,
    width: dx,
    height: dy,
    border: '1px solid tomato',
  };

  return (
    <div ref={ref} style={blockStyle}>
      <pre>{JSON.stringify(state, null, 4)}</pre>
      {state.isScratching && <div style={rectangleStyle} />}
    </div>
  );
};
```

## Reference

```ts
const [ref, state] = useScratch();
```

`state` interface:

```ts
export interface ScratchSensorState {
  isScratching: boolean;
  start?: number;
  end?: number;
  x?: number;
  y?: number;
  dx?: number;
  dy?: number;
  docX?: number;
  docY?: number;
  posX?: number;
  posY?: number;
  elH?: number;
  elW?: number;
  elX?: number;
  elY?: number;
}
```

## Key Points

- Tracks click-and-drag (scratch) gestures
- Provides start/end positions and dimensions
- Useful for selection rectangles or drawing tools

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useScratch.md
-->
