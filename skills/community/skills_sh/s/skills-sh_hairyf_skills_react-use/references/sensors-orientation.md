---
name: sensors-orientation
description: Track screen orientation with useOrientation hook
---

# useOrientation

React sensor hook that tracks screen orientation of user's device.

## Usage

```jsx
import {useOrientation} from 'react-use';

const Demo = () => {
  const state = useOrientation();

  return (
    <pre>
      {JSON.stringify(state, null, 2)}
    </pre>
  );
};
```

## Reference

Returns state in the following shape:

```js
{
  angle: 0,
  type: 'landscape-primary'
}
```

- **`angle`**: `number` - orientation angle in degrees
- **`type`**: `string` - orientation type (e.g., 'landscape-primary', 'portrait-primary')

## Key Points

- Tracks device orientation changes
- Provides angle and type information
- Useful for responsive layouts based on orientation

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useOrientation.md
-->
