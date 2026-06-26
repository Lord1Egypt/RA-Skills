---
name: sensors-network-state
description: Track browser's network connection state with useNetworkState hook
---

# useNetworkState

Tracks the state of browser's network connection.

As of the standard it is not guaranteed that browser connected to the _Internet_, it only guarantees the network connection.

## Usage

```jsx
import {useNetworkState} from 'react-use';

const Demo = () => {
  const state = useNetworkState();

  return (
    <pre>
      {JSON.stringify(state, null, 2)}
    </pre>
  );
};
```

## Reference

```typescript
interface IUseNetworkState {
  online: boolean | undefined; // Whether browser connected to the network
  previous: boolean | undefined; // Previous value of online property
  since: Date | undefined; // The Date object pointing to the moment when state change occurred
  downlink: number | undefined; // Effective bandwidth estimate in megabits per second
  downlinkMax: number | undefined; // Maximum downlink speed in Mbps
  effectiveType: 'slow-2g' | '2g' | '3g' | '4g' | undefined; // Effective connection type
  rtt: number | undefined; // Estimated effective round-trip time in milliseconds
  saveData: boolean | undefined; // Whether user has set a reduced data usage option
  type: 'bluetooth' | 'cellular' | 'ethernet' | 'none' | 'wifi' | 'wimax' | 'other' | 'unknown' | undefined; // Connection type
}

function useNetworkState(initialState?: IUseNetworkState | (() => IUseNetworkState)): IUseNetworkState;
```

## Key Points

- Tracks comprehensive network information
- Provides connection quality metrics
- Useful for adaptive UI based on connection speed

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useNetworkState.md
-->
