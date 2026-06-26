---
name: sensors-key-press
description: Detect when user is pressing a specific key with useKeyPress hook
---

# useKeyPress

React UI sensor hook that detects when the user is pressing a specific key on their keyboard.

## Usage

```jsx
import {useKeyPress} from 'react-use';

const keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'];

const Demo = () => {
  const states = [];
  for (const key of keys) states.push(useKeyPress(key)[0]);

  return (
    <div style={{textAlign: 'center'}}>
      Try pressing numbers
      <br />
      {states.reduce((s, pressed, index) => s + (pressed ? (s ? ' + ' : '') + keys[index] : ''), '')}
    </div>
  );
};
```

## Reference

```js
const isPressed = useKeyPress('a');
const isPressed = useKeyPress((event) => event.key === 'a');
```

Returns an array:
- `[0]`: `boolean` - whether the key is currently pressed
- `[1]`: `KeyboardEvent | null` - the keyboard event (if available)

## Key Points

- Returns boolean state indicating if key is currently pressed
- Can use string key names or predicate functions
- Useful for keyboard shortcuts or game controls

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useKeyPress.md
-->
