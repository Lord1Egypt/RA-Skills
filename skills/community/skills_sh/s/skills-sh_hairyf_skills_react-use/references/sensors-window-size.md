---
name: sensors-window-size
description: Track dimensions of browser window with useWindowSize hook
---

# useWindowSize

React sensor hook that tracks dimensions of the browser window.

## Usage

```jsx
import {useWindowSize} from 'react-use';

const Demo = () => {
  const {width, height} = useWindowSize();

  return (
    <div>
      <div>width: {width}</div>
      <div>height: {height}</div>
    </div>
  );
};
```

## Reference

```js
useWindowSize(options);
```

Options:
- `initialWidth` - Initial width value for non-browser environments
- `initialHeight` - Initial height value for non-browser environments
- `onChange` - Callback function triggered when the window size changes

Returns an object with:
- `width`: `number` - window width
- `height`: `number` - window height

## Related hooks

- `useSize` - tracks element size
- `useMeasure` - tracks element dimensions with ResizeObserver

## Key Points

- Tracks window dimensions
- Useful for responsive layouts
- Supports SSR with initial values

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useWindowSize.md
-->
