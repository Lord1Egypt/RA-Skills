---
name: side-effects-raf-loop
description: Call function inside RAF loop with useRafLoop hook
---

# useRafLoop

This hook calls given function within the RAF loop without re-rendering parent component. Loop stops automatically on component unmount.

Additionally hook provides methods to start/stop loop and check current state.

## Usage

```jsx
import * as React from 'react';
import { useRafLoop, useUpdate } from 'react-use';

const Demo = () => {
  const [ticks, setTicks] = React.useState(0);
  const [lastCall, setLastCall] = React.useState(0);
  const update = useUpdate();

  const [loopStop, loopStart, isActive] = useRafLoop((time) => {
    setTicks(ticks => ticks + 1);
    setLastCall(time);
  });

  return (
    <div>
      <div>RAF triggered: {ticks} (times)</div>
      <div>Last high res timestamp: {lastCall}</div>
      <br />
      <button onClick={() => {
        isActive() ? loopStop() : loopStart();
        update();
      }}>{isActive() ? 'STOP' : 'START'}</button>
    </div>
  );
};
```

## Reference

```ts
const [stopLoop, startLoop, isActive] = useRafLoop(callback: FrameRequestCallback, initiallyActive = true);
```

- **`callback`**: `(time: number) => void` - function to call each RAF tick
- **`initiallyActive`**: `boolean` - whether loop should be started at initial render
- Returns:
  - `stopLoop`: `() => void` - stop loop if it is active
  - `startLoop`: `() => void` - start loop if it was inactive
  - `isActive`: `() => boolean` - true if loop is active

## Key Points

- Does not cause re-renders
- Provides start/stop controls
- Auto-stops on unmount
- Useful for animations and game loops

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useRafLoop.md
-->
