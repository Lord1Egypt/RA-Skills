---
name: animations-timeout-fn
description: Call function after timeout with useTimeoutFn hook
---

# useTimeoutFn

Calls given function after specified amount of milliseconds.

Several things about its work:
- does not re-render component
- automatically cancel timeout on unmount
- automatically reset timeout on delay change
- reset function call will cancel previous timeout
- timeout will NOT be reset on function change

## Usage

```jsx
import * as React from 'react';
import { useTimeoutFn } from 'react-use';

const Demo = () => {
  const [state, setState] = React.useState('Not called yet');

  function fn() {
    setState(`called at ${Date.now()}`);
  }

  const [isReady, cancel, reset] = useTimeoutFn(fn, 5000);
  const cancelButtonClick = useCallback(() => {
    if (isReady() === false) {
      cancel();
      setState(`cancelled`);
    } else {
      reset();
      setState('Not called yet');
    }
  }, []);

  return (
    <div>
      <div>{isReady() !== null ? 'Function will be called in 5 seconds' : 'Timer cancelled'}</div>
      <button onClick={cancelButtonClick}> {isReady() === false ? 'cancel' : 'restart'} timeout</button>
      <br />
      <div>Function state: {isReady() === false ? 'Pending' : isReady() ? 'Called' : 'Cancelled'}</div>
      <div>{state}</div>
    </div>
  );
};
```

## Reference

```ts
const [
    isReady: () => boolean | null,
    cancel: () => void,
    reset: () => void,
] = useTimeoutFn(fn: Function, ms: number = 0);
```

- **`fn`**: `Function` - function that will be called
- **`ms`**: `number` - delay in milliseconds
- **`isReady`**: `() => boolean | null` - function returning current timeout state
- **`cancel`**: `() => void` - cancel the timeout
- **`reset`**: `() => void` - reset the timeout

## Key Points

- Does not cause re-renders
- Auto-cancels on unmount
- Auto-resets on delay change
- Useful for delayed function calls

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useTimeoutFn.md
-->
