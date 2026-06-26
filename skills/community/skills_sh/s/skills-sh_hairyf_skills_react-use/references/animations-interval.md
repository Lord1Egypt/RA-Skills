---
name: animations-interval
description: Re-render component on set interval with useInterval hook
---

# useInterval

A declarative interval hook based on [Dan Abramov's article on overreacted.io](https://overreacted.io/making-setinterval-declarative-with-react-hooks). The interval can be paused by setting the delay to `null`.

## Usage

```jsx
import * as React from 'react';
import {useInterval} from 'react-use';

const Demo = () => {
  const [count, setCount] = React.useState(0);
  const [delay, setDelay] = React.useState(1000);
  const [isRunning, toggleIsRunning] = useBoolean(true);

  useInterval(
    () => {
      setCount(count + 1);
    },
    isRunning ? delay : null
  );

  return (
    <div>
      <div>
        delay: <input value={delay} onChange={event => setDelay(Number(event.target.value))} />
      </div>
      <h1>count: {count}</h1>
      <div>
        <button onClick={toggleIsRunning}>{isRunning ? 'stop' : 'start'}</button>
      </div>
    </div>
  );
};
```

## Reference

```js
useInterval(callback, delay?: number)
```

- **`callback`**: `() => void` - function to call on each interval
- **`delay`**: `number | null` - delay in milliseconds, set to `null` to pause

## Key Points

- Pause by setting delay to `null`
- Declarative interval management
- Automatically cleans up on unmount

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useInterval.md
-->
