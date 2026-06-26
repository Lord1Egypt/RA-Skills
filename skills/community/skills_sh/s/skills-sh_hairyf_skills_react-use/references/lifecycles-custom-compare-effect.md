---
name: lifecycles-custom-compare-effect
description: useEffect with custom comparison function using useCustomCompareEffect hook
---

# useCustomCompareEffect

A modified useEffect hook that accepts a comparator which is used for comparison on dependencies instead of reference equality.

## Usage

```jsx
import {useCounter, useCustomCompareEffect} from 'react-use';
import isEqual from 'lodash/isEqual';

const Demo = () => {
  const [count, {inc: inc}] = useCounter(0);
  const options = { step: 2 };

  useCustomCompareEffect(() => {
    inc(options.step)
  }, [options], (prevDeps, nextDeps) => isEqual(prevDeps, nextDeps));

  return (
    <div>
      <p>useCustomCompareEffect with deep comparison: {count}</p>
    </div>
  );
};
```

## Reference

```ts
useCustomCompareEffect(effect: () => void | (() => void | undefined), deps: any[], depsEqual: (prevDeps: any[], nextDeps: any[]) => boolean);
```

- **`depsEqual`**: `(prevDeps: any[], nextDeps: any[]) => boolean` - custom comparison function

## Key Points

- Custom comparison function
- Most flexible comparison option
- Use with libraries like lodash.isEqual

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useCustomCompareEffect.md
-->
