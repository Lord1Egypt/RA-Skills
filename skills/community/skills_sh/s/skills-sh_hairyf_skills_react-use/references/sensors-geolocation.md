---
name: sensors-geolocation
description: Track user's geographic location with useGeolocation hook
---

# useGeolocation

React sensor hook that tracks user's geographic location. This hook accepts [position options](https://developer.mozilla.org/docs/Web/API/PositionOptions).

## Usage

```jsx
import {useGeolocation} from 'react-use';

const Demo = () => {
  const state = useGeolocation();

  return (
    <pre>
      {JSON.stringify(state, null, 2)}
    </pre>
  );
};
```

## Reference

```ts
useGeolocation(options: PositionOptions)
```

The hook returns a state object with:
- `loading`: boolean - whether location is being fetched
- `accuracy`: number - accuracy of the position
- `altitude`: number | null - altitude in meters
- `altitudeAccuracy`: number | null - altitude accuracy in meters
- `heading`: number | null - heading in degrees
- `latitude`: number | null - latitude in decimal degrees
- `longitude`: number | null - longitude in decimal degrees
- `speed`: number | null - speed in meters per second
- `timestamp`: number - timestamp of the position
- `error`: GeolocationPositionError | null - error if geolocation fails

## Key Points

- Requires user permission to access location
- Accepts standard `PositionOptions` (enableHighAccuracy, timeout, maximumAge)
- Returns comprehensive location data including coordinates, altitude, heading, and speed

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useGeolocation.md
-->
