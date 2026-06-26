---
name: animations-update
description: Force component re-render with useUpdate hook
---

# useUpdate

React utility hook that returns a function that forces component to re-render when called.

## Usage

```jsx
import {useUpdate} from 'react-use';

const Demo = () => {
  const update = useUpdate();
  return (
    <>
      <div>Time: {Date.now()}</div>
      <button onClick={update}>Update</button>
    </>
  );
};
```

## Reference

```ts
const update = useUpdate();
```

Returns a function that when called, forces the component to re-render.

## Key Points

- Simple utility for manual re-renders
- Useful for testing or forcing updates
- Returns a stable function reference

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useUpdate.md
-->
