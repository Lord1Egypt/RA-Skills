---
name: state-renders-count
description: Count component renders with useRendersCount hook
---

# useRendersCount

Tracks component's renders count including the first render.

## Usage

```typescript jsx
import * as React from 'react';
import { useRendersCount } from "react-use";  

const Demo = () => {
  const update = useUpdate();
  const rendersCount = useRendersCount();

  return (
    <div>
      <span>Renders count: {rendersCount}</span>
      <br />
      <button onClick={update}>re-render</button>
    </div>
  );
};
```

## Reference

```typescript
const rendersCount: number = useRendersCount();
```

Returns the number of times component has rendered.

## Key Points

- Tracks render count
- Includes first render
- Useful for debugging

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useRendersCount.md
-->
