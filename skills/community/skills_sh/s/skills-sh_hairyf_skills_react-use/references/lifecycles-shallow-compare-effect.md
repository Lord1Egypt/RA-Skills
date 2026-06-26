---
name: lifecycles-shallow-compare-effect
description: useEffect with shallow comparison using useShallowCompareEffect hook
---

# useShallowCompareEffect

A modified useEffect hook that is using shallow comparison on each of its dependencies instead of reference equality.

## Usage

```jsx
import {useCounter, useShallowCompareEffect} from 'react-use';

const Demo = () => {
  const [count, {inc: inc}] = useCounter(0);
  const options = { step: 2 };

  useShallowCompareEffect(() => {
    inc(options.step)
  }, [options]);

  return (
    <div>
      <p>useShallowCompareEffect: {count}</p>
    </div>
  );
};
```

## Reference

```ts
useShallowCompareEffect(effect: () => void | (() => void | undefined), deps: any[]);
```

Same signature as `useEffect`, but uses shallow equality for dependency comparison.

## Key Points

- Shallow compares dependencies
- More efficient than deep comparison
- Useful for object dependencies

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useShallowCompareEffect.md
-->
