---
name: sensors-media-devices
description: Track connected hardware devices with useMediaDevices hook
---

# useMediaDevices

React sensor hook that tracks connected hardware devices.

## Usage

```jsx
import {useMediaDevices} from 'react-use';

const Demo = () => {
  const state = useMediaDevices();

  return (
    <pre>
      {JSON.stringify(state, null, 2)}
    </pre>
  );
};
```

## Reference

Returns a state object with device information from the MediaDevices API, including:
- Available audio/video input/output devices
- Device capabilities and constraints
- Device IDs and labels

## Key Points

- Uses the MediaDevices API
- Tracks changes to connected devices
- Useful for device selection in media applications

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useMediaDevices.md
-->
