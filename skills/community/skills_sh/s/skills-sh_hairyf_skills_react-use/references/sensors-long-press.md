---
name: sensors-long-press
description: Fire callback after long pressing with useLongPress hook
---

# useLongPress

React sensor hook that fires a callback after long pressing.

## Usage

```jsx
import { useLongPress } from 'react-use';

const Demo = () => {
  const onLongPress = () => {
    console.log('calls callback after long pressing 300ms');
  };

  const defaultOptions = {
    isPreventDefault: true,
    delay: 300,
  };
  const longPressEvent = useLongPress(onLongPress, defaultOptions);

  return <button {...longPressEvent}>useLongPress</button>;
};
```

## Reference

```ts
const {
  onMouseDown,
  onTouchStart,
  onMouseUp,
  onMouseLeave,
  onTouchEnd
} = useLongPress(
  callback: (e: TouchEvent | MouseEvent) => void,
  options?: {
    isPreventDefault?: true,
    delay?: 300
  }
)
```

- **`callback`**: `(e: TouchEvent | MouseEvent) => void` - callback function
- **`options`**: `object` - optional parameter
  - `isPreventDefault?`: `boolean` - whether to call `event.preventDefault()` of `touchend` event, for preventing ghost click on mobile devices in some cases, defaults to `true`
  - `delay?`: `number` - delay in milliseconds after which to calls provided callback, defaults to `300`

## Key Points

- Works with both mouse and touch events
- Prevents ghost clicks on mobile by default
- Configurable delay before triggering callback
- Returns event handlers to spread on element

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useLongPress.md
-->
