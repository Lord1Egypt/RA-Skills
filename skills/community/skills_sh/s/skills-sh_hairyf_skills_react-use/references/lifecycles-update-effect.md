---
name: lifecycles-update-effect
description: Run effect only on updates with useUpdateEffect hook
---

# useUpdateEffect

React effect hook that ignores the first invocation (e.g. on mount). The signature is exactly the same as the `useEffect` hook.

## Usage

```jsx
import React from 'react'
import {useUpdateEffect} from 'react-use';

const Demo = () => {
  const [count, setCount] = React.useState(0);
  
  React.useEffect(() => {
    const interval = setInterval(() => {
      setCount(count => count + 1)
    }, 1000)
    
    return () => {
      clearInterval(interval)
    }
  }, [])
  
  useUpdateEffect(() => {
    console.log('count', count) // will only show 1 and beyond
    
    return () => { // *OPTIONAL*
      // do something on unmount
    }
  }) // you can include deps array if necessary

  return <div>Count: {count}</div>
};
```

## Reference

```ts
useUpdateEffect(effect: EffectCallback, deps?: DependencyList);
```

Same signature as `useEffect`, but skips first execution.

## Key Points

- Ignores first execution (mount)
- Runs only on updates
- Useful for update-only side effects

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useUpdateEffect.md
-->
