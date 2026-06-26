---
name: ui-click-away
description: Trigger callback when user clicks outside target element with useClickAway hook
---

# useClickAway

React UI hook that triggers a callback when user clicks outside the target element.

## Usage

```jsx
import {useClickAway} from 'react-use';

const Demo = () => {
  const ref = useRef(null);
  useClickAway(ref, () => {
    console.log('OUTSIDE CLICKED');
  });

  return (
    <div ref={ref} style={{
      width: 200,
      height: 200,
      background: 'red',
    }} />
  );
};
```

## Reference

```js
useClickAway(ref, onMouseEvent)
useClickAway(ref, onMouseEvent, ['click'])
useClickAway(ref, onMouseEvent, ['mousedown', 'touchstart'])
```

- **`ref`**: `RefObject<HTMLElement>` - reference to target element
- **`onMouseEvent`**: `(event: MouseEvent | TouchEvent) => void` - callback function
- **`events`**: `string[]` - optional array of event types to listen for, defaults to `['click']`

## Key Points

- Triggers when click occurs outside the referenced element
- Supports custom event types (click, mousedown, touchstart, etc.)
- Useful for closing modals, dropdowns, or popovers

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useClickAway.md
-->
