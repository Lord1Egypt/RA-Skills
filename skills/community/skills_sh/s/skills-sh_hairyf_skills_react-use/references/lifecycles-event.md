---
name: lifecycles-event
description: Subscribe to events with useEvent hook
---

# useEvent

React sensor hook that subscribes a `handler` to events.

## Usage

```jsx
import {useEvent, useList} from 'react-use';

const Demo = () => {
  const [list, {push, clear}] = useList();

  const onKeyDown = useCallback(({key}) => {
    if (key === 'r') clear();
    push(key);
  }, []);

  useEvent('keydown', onKeyDown);

  return (
    <div>
      <p>
        Press some keys on your keyboard, <code style={{color: 'tomato'}}>r</code> key resets the list
      </p>
      <pre>
        {JSON.stringify(list, null, 4)}
      </pre>
    </div>
  );
};
```

## Reference

```js
useEvent('keydown', handler)
useEvent('scroll', handler, window, {capture: true})
```

- **`event`**: `string` - event name
- **`handler`**: `(event: Event) => void` - event handler
- **`target`**: `EventTarget` - optional target (defaults to window)
- **`options`**: `AddEventListenerOptions` - optional event options

## Key Points

- Subscribes to DOM events
- Auto-cleans up on unmount
- Supports all standard event options

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useEvent.md
-->
