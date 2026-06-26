---
name: side-effects-throttle-fn
description: Throttle function calls with useThrottleFn hook
---

# useThrottleFn

React hook that invokes a function and then delays subsequent function calls until after wait milliseconds have elapsed since the last time the throttled function was invoked.

The third argument is the array of values that the throttle depends on, in the same manner as useEffect. The throttle timeout will start when one of the values changes.

## Usage

```jsx
import React, { useState } from 'react';
import { useThrottleFn } from 'react-use';

const Demo = () => {
  const [status, setStatus] = React.useState('Updating stopped');
  const [value, setValue] = React.useState('');
  const [throttledValue, setThrottledValue] = React.useState('');

  useThrottleFn(
    () => {
      setStatus('Waiting for input...');
      setThrottledValue(value);
    },
    2000,
    [value]
  );

  return (
    <div>
      <input
        type="text"
        value={value}
        placeholder="Throttled input"
        onChange={({ currentTarget }) => {
          setStatus('Updating stopped');
          setValue(currentTarget.value);
        }}
      />
      <div>{status}</div>
      <div>Throttled value: {throttledValue}</div>
    </div>
  );
};
```

## Reference

```ts
useThrottleFn(fn, ms: number, args: any[]);
```

- **`fn`**: `Function` - function to throttle
- **`ms`**: `number` - throttle delay in milliseconds
- **`args`**: `any[]` - array of values that the throttle depends on

## Key Points

- Throttles function execution
- Resets on dependency changes
- Useful for limiting API calls or updates

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useThrottleFn.md
-->
