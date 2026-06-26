---
name: sensors-scrollbar-width
description: Detect browser's native scrollbars width with useScrollbarWidth hook
---

# useScrollbarWidth

Hook that will return current browser's scrollbar width. In case hook been called before DOM ready, it will return `undefined` and will cause re-render on first available RAF.

> **_NOTE:_** it does not work (return 0) for mobile devices, because their scrollbar width can not be determined.

## Usage

```jsx
const Demo = () => {
  const sbw = useScrollbarWidth();

  return (
    <div>
      {sbw === undefined ? `DOM is not ready yet, SBW detection delayed` : `Browser's scrollbar width is ${sbw}px`}
    </div>
  );
};
```

## Reference

```typescript
const sbw: number | undefined = useScrollbarWidth();
```

Returns:
- `number | undefined` - scrollbar width in pixels, or `undefined` if DOM is not ready

## Key Points

- Returns `undefined` before DOM is ready
- Returns `0` on mobile devices (scrollbar width cannot be determined)
- Useful for layout calculations that account for scrollbar width

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useScrollbarWidth.md
-->
