---
name: sensors-size
description: Track size of HTML element with useSize hook
---

# useSize

React sensor hook that tracks size of an HTML element.

## Usage

```jsx
import {useSize} from 'react-use';

const Demo = () => {
  const [sized, {width, height}] = useSize(
    ({width}) => <div style={{background: 'red'}}>Size me up! ({width}px)</div>,
    { width: 100, height: 100 }
  );

  return (
    <div>
      {sized}
      <div>width: {width}</div>
      <div>height: {height}</div>
    </div>
  );
};
```

## Reference

```js
useSize(element, initialSize);
```

- **`element`**: `ReactElement | (size: {width: number, height: number}) => ReactElement` - sized element or render function
- **`initialSize`**: `{width: number, height: number}` - initial size containing a `width` and `height` key

Returns:
- `[element, size]` - tuple with the sized element and size object

## Related hooks

- `useMeasure` - tracks element dimensions with ResizeObserver

## Key Points

- Uses render prop pattern
- Provides width and height
- Useful for responsive components

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useSize.md
-->
