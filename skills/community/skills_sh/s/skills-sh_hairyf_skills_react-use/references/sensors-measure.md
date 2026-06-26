---
name: sensors-measure
description: Track dimensions of HTML element using ResizeObserver with useMeasure hook
---

# useMeasure

React sensor hook that tracks dimensions of an HTML element using the [Resize Observer API](https://developer.mozilla.org/en-US/docs/Web/API/ResizeObserver).

## Usage

```jsx
import { useMeasure } from "react-use";

const Demo = () => {
  const [ref, { x, y, width, height, top, right, bottom, left }] = useMeasure();

  return (
    <div ref={ref}>
      <div>x: {x}</div>	
      <div>y: {y}</div>
      <div>width: {width}</div>
      <div>height: {height}</div>
      <div>top: {top}</div>
      <div>right: {right}</div>
      <div>bottom: {bottom}</div>
      <div>left: {left}</div>
    </div>
  );
};
```

## Reference

```ts
const [ref, bounds] = useMeasure();
```

Returns:
- `ref`: `RefObject<HTMLElement>` - ref to attach to element
- `bounds`: object with `x`, `y`, `width`, `height`, `top`, `right`, `bottom`, `left`

## Browser Support

This hook uses [`ResizeObserver` API][resize-observer]. If you want to support legacy browsers, consider installing [`resize-observer-polyfill`][resize-observer-polyfill] before running your app:

```js
if (!window.ResizeObserver) {
  window.ResizeObserver = (await import('resize-observer-polyfill')).default;
}
```

## Related hooks

- `useSize` - tracks element size with render prop pattern

## Key Points

- Uses ResizeObserver for efficient size tracking
- Provides comprehensive bounding box information
- Requires polyfill for older browsers

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useMeasure.md
-->
