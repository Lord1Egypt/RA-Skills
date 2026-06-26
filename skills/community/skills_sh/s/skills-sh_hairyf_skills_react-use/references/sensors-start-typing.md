---
name: sensors-start-typing
description: Fire callback when user starts typing with useStartTyping hook
---

# useStartTyping

React sensor hook that fires a callback when user starts typing. Can be used to focus default input field on the page.

## Usage

```jsx
import {useStartTyping} from 'react-use';

const Demo = () => {
  useStartTyping(() => alert('Started typing...'));

  return null;
};
```

## Reference

```ts
useStartTyping(callback: () => void);
```

- **`callback`**: `() => void` - function to call when user starts typing

## Key Points

- Triggers on first keyboard input
- Useful for auto-focusing input fields
- Simple callback-based API

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useStartTyping.md
-->
