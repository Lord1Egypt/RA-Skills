---
name: animations-raf
description: Re-render component on each requestAnimationFrame with useRaf hook
---

# useRaf

React animation hook that forces component to re-render on each `requestAnimationFrame`, returns percentage of time elapsed.

## Usage

```jsx
import {useRaf} from 'react-use';

const Demo = () => {
  const elapsed = useRaf(5000, 1000);

  return (
    <div>
      Elapsed: {elapsed}
    </div>
  );
};
```

## Reference

```ts
useRaf(ms?: number, delay?: number): number;
```

- **`ms`**: `number` - milliseconds for how long to keep re-rendering component, defaults to `1e12`
- **`delay`**: `number` - delay in milliseconds after which to start re-rendering component, defaults to `0`
- Returns: `number` - percentage of time elapsed (0-1)

## Key Points

- Re-renders on every requestAnimationFrame
- Returns normalized progress (0-1)
- Useful for smooth animations

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useRaf.md
-->
