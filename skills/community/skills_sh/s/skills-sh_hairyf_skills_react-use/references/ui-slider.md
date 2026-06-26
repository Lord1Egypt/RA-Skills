---
name: ui-slider
description: Provide slide behavior over HTML element with useSlider hook
---

# useSlider

React UI hook that provides slide behavior over any HTML element. Supports both mouse and touch events.

## Usage

```jsx
import {useSlider} from 'react-use';

const Demo = () => {
  const ref = React.useRef(null);
  const {isSliding, value, pos, length} = useSlider(ref);

  return (
    <div>
      <div ref={ref} style={{ position: 'relative' }}>
        <p style={{ textAlign: 'center', color: isSliding ? 'red' : 'green' }}>
          {Math.round(value * 100)}%
        </p>
        <div style={{ position: 'absolute', left: pos }}>🎚</div>
      </div>
    </div>
  );
};
```

## Reference

```ts
const {isSliding, value, pos, length} = useSlider(ref);
```

- **`ref`**: `RefObject<HTMLElement>` - reference to element to slide over
- Returns:
  - `isSliding`: `boolean` - whether user is currently sliding
  - `value`: `number` - normalized value (0-1) based on position
  - `pos`: `number` - absolute position in pixels
  - `length`: `number` - length of the element

## Key Points

- Works with both mouse and touch events
- Provides normalized value (0-1) and absolute position
- Useful for custom slider/range inputs
- Tracks sliding state

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useSlider.md
-->
