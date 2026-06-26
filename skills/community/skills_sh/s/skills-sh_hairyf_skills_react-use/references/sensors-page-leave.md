---
name: sensors-page-leave
description: Fire callback when mouse leaves page with usePageLeave hook
---

# usePageLeave

React sensor hook that fires a callback when mouse leaves the page.

## Usage

```jsx
import {usePageLeave} from 'react-use';

const Demo = () => {
  usePageLeave(() => console.log('Page left...'));

  return null;
};
```

## Reference

```ts
usePageLeave(callback: () => void);
```

- **`callback`**: `() => void` - function to call when mouse leaves the page

## Key Points

- Triggers when mouse cursor leaves the viewport
- Useful for showing exit intent modals or saving state
- Simple callback-based API

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/usePageLeave.md
-->
