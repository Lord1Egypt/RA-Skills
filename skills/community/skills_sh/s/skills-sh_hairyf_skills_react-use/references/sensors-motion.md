---
name: sensors-motion
description: Track device's acceleration sensor motions with useMotion hook
---

# useMotion

React sensor hook that uses device's acceleration sensor to track its motions.

## Usage

```jsx
import {useMotion} from 'react-use';

const Demo = () => {
  const state = useMotion();

  return (
    <pre>
      {JSON.stringify(state, null, 2)}
    </pre>
  );
};
```

## Reference

Returns motion state with acceleration and rotation data from the device's motion sensor.

## Key Points

- Uses device's accelerometer and gyroscope
- Tracks device orientation and movement
- Useful for motion-based interactions and games

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useMotion.md
-->
