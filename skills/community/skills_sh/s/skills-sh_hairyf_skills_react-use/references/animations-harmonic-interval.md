---
name: animations-harmonic-interval
description: Harmonic interval function that triggers all effects at the same time
---

# useHarmonicIntervalFn

Same as `useInterval` hook, but triggers all effects with the same delay at the same time.

For example, this allows you to create ticking clocks on the page which re-render second counter all at the same time.

## Reference

```js
useHarmonicIntervalFn(fn, delay?: number)
```

- **`fn`**: `() => void` - function to call
- **`delay`**: `number` - delay in milliseconds

## Key Points

- Synchronizes multiple components to update at the same time
- Useful for synchronized clocks or timers
- All instances share the same interval timing

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useHarmonicIntervalFn.md
-->
