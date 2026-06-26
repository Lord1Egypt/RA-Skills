---
name: sensors-key-press-event
description: Handle keydown and keyup events with useKeyPressEvent hook
---

# useKeyPressEvent

This hook fires `keydown` and `keyup` callbacks, similar to how `useKey` hook does, but it only triggers each callback once per press cycle. For example, if you press and hold a key, it will fire `keydown` callback only once.

## Usage

```jsx
import React, { useState } from React;
import {useKeyPressEvent} from 'react-use';

const Demo = () => {
  const [count, setCount] = useState(0);

  const increment = () => setCount(count => ++count);
  const decrement = () => setCount(count => --count);
  const reset = () => setCount(count => 0);

  useKeyPressEvent(']', increment, increment);
  useKeyPressEvent('[', decrement, decrement);
  useKeyPressEvent('r', reset);

  return (
    <div>
      <p>
        Try pressing <code>[</code>, <code>]</code>, and <code>r</code> to
        see the count incremented and decremented.</p>
      <p>Count: {count}</p>
    </div>
  );
};
```

## Reference

```js
useKeyPressEvent('<key>', keydown);
useKeyPressEvent('<key>', keydown, keyup);
useKeyPressEvent('<key>', keydown, keyup, useKeyPress);
```

- **`key`**: `string | (event: KeyboardEvent) => boolean` - key to listen for or predicate
- **`keydown`**: `(event: KeyboardEvent) => void` - callback for keydown event
- **`keyup`**: `(event: KeyboardEvent) => void` - optional callback for keyup event
- **`useKeyPress`**: `boolean` - whether to use useKeyPress internally (defaults to true)

## Key Points

- Fires callbacks only once per press cycle (not continuously while held)
- Separate callbacks for keydown and keyup
- Useful for toggle actions or one-time events

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useKeyPressEvent.md
-->
