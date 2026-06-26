---
name: lifecycles-deep-compare-effect
description: useEffect with deep comparison using useDeepCompareEffect hook
---

# useDeepCompareEffect

A modified useEffect hook that is using deep comparison on its dependencies instead of reference equality.

## Usage

```jsx
import {useCounter, useDeepCompareEffect} from 'react-use';

const Demo = () => {
  const [count, {inc: inc}] = useCounter(0);
  const options = { step: 2 };

  useDeepCompareEffect(() => {
    inc(options.step)
  }, [options]);

  return (
    <div>
      <p>useDeepCompareEffect: {count}</p>
    </div>
  );
};
```

## Reference

```ts
useDeepCompareEffect(effect: () => void | (() => void | undefined), deps: any[]);
```

Same signature as `useEffect`, but uses deep equality for dependency comparison.

## Key Points

- Deep compares dependencies
- Useful when dependencies are objects/arrays
- Prevents unnecessary effect runs

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useDeepCompareEffect.md
-->
