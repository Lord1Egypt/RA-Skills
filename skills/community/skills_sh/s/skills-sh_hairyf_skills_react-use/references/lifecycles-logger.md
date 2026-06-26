---
name: lifecycles-logger
description: Log component lifecycle transitions with useLogger hook
---

# useLogger

React lifecycle hook that console logs parameters as component transitions through lifecycles.

## Usage

```jsx
import {useLogger} from 'react-use';

const Demo = (props) => {
  useLogger('Demo', props);
  return null;
};
```

## Example Output

```
Demo mounted {}
Demo updated {}
Demo unmounted
```

## Reference

```js
useLogger(componentName: string, ...rest);
```

- **`componentName`**: `string` - component name
- **`...rest`**: `any[]` - parameters to log

## Key Points

- Logs mount, update, and unmount events
- Useful for debugging
- Logs component name and props

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useLogger.md
-->
