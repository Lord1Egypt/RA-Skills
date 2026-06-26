---
name: sensors-idle
description: Track if user on the page is idle with useIdle hook
---

# useIdle

React sensor hook that tracks if user on the page is idle.

## Usage

```jsx
import {useIdle} from 'react-use';

const Demo = () => {
  const isIdle = useIdle(3e3);

  return (
    <div>
      <div>User is idle: {isIdle ? 'Yes 😴' : 'Nope'}</div>
    </div>
  );
};
```

## Reference

```js
useIdle(ms, initialState);
```

- **`ms`**: `number` - time in milliseconds after which to consider user idle, defaults to `60e3` (one minute)
- **`initialState`**: `boolean` - whether to consider user initially idle, defaults to false

## Key Points

- Tracks user activity (mouse movement, keyboard input, etc.)
- Configurable idle timeout
- Useful for showing "Are you still there?" prompts or auto-logout

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useIdle.md
-->
