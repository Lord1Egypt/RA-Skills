---
name: sensors-location
description: Track browser's location with useLocation hook
---

# useLocation

React sensor hook that tracks browser's location.

For Internet Explorer you need to [install a polyfill](https://github.com/streamich/react-use/issues/73).

## Usage

```jsx
import {useLocation} from 'react-use';

const Demo = () => {
  const state = useLocation();

  return (
    <pre>
      {JSON.stringify(state, null, 2)}
    </pre>
  );
};
```

## Reference

Returns a location state object with properties like:
- `trigger`: string - what triggered the location change
- `state`: any - state object from history API
- `length`: number - number of entries in history
- `hash`: string - URL hash
- `host`: string - hostname and port
- `hostname`: string - hostname
- `href`: string - full URL
- `origin`: string - origin
- `pathname`: string - pathname
- `port`: string - port
- `protocol`: string - protocol
- `search`: string - search query string

## Key Points

- Requires polyfill for Internet Explorer
- Tracks all location properties
- Useful for routing and navigation logic

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useLocation.md
-->
