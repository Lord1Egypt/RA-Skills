---
name: state-first-mount-state
description: Check if current render is first with useFirstMountState hook
---

# useFirstMountState

Returns `true` if component is just mounted (on first render) and `false` otherwise.

## Usage

```typescript jsx
import * as React from 'react';
import { useFirstMountState } from 'react-use';

const Demo = () => {
  const isFirstMount = useFirstMountState();
  const update = useUpdate();

  return (
    <div>
      <span>This component is just mounted: {isFirstMount ? 'YES' : 'NO'}</span>
      <br />
      <button onClick={update}>re-render</button>
    </div>
  );
};
```

## Reference

```typescript
const isFirstMount: boolean = useFirstMountState();
```

Returns `true` only on first render.

## Key Points

- Simple boolean flag
- `true` only on mount
- Useful for conditional logic

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useFirstMountState.md
-->
