---
name: sensors-intersection
description: Track element intersection with viewport using Intersection Observer API
---

# useIntersection

React sensor hook that tracks the changes in the intersection of a target element with an ancestor element or with a top-level document's viewport. Uses the [Intersection Observer API](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API) and returns a [IntersectionObserverEntry](https://developer.mozilla.org/en-US/docs/Web/API/IntersectionObserverEntry).

## Usage

```jsx
import * as React from 'react';
import { useIntersection } from 'react-use';

const Demo = () => {
  const intersectionRef = React.useRef(null);
  const intersection = useIntersection(intersectionRef, {
    root: null,
    rootMargin: '0px',
    threshold: 1
  });

  return (
    <div ref={intersectionRef}>
      {intersection && intersection.intersectionRatio < 1
        ? 'Obscured'
        : 'Fully in view'}
    </div>
  );
};
```

## Reference

```ts
useIntersection(
  ref: RefObject<HTMLElement>,
  options: IntersectionObserverInit,
): IntersectionObserverEntry | null;
```

The `options` parameter accepts standard `IntersectionObserverInit`:
- `root`: Element or null - root element for intersection
- `rootMargin`: string - margin around root
- `threshold`: number | number[] - threshold(s) for intersection

Returns `IntersectionObserverEntry` with properties like:
- `intersectionRatio`: number - ratio of intersection (0 to 1)
- `isIntersecting`: boolean - whether element is intersecting
- `boundingClientRect`: DOMRectReadOnly
- `rootBounds`: DOMRectReadOnly | null

## Key Points

- Uses native Intersection Observer API for performance
- Perfect for lazy loading, infinite scroll, or visibility tracking
- Returns null until first intersection is detected

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useIntersection.md
-->
