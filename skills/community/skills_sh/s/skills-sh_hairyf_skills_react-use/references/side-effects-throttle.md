---
name: side-effects-throttle
description: Throttle a function with useThrottle hook
---

# useThrottle

React hook that throttles a function.

## Usage

```jsx
import {useThrottle} from 'react-use';

const Demo = () => {
  const [value, setValue] = useState('');
  const throttledValue = useThrottle(value, 1000);

  return (
    <div>
      <input value={value} onChange={e => setValue(e.target.value)} />
      <div>Throttled: {throttledValue}</div>
    </div>
  );
};
```

## Reference

```ts
const throttledValue = useThrottle(value, ms);
```

- **`value`**: `T` - value to throttle
- **`ms`**: `number` - throttle delay in milliseconds
- Returns: `T` - throttled value

## Key Points

- Throttles value updates
- Useful for limiting update frequency
- Similar to debounce but different timing

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useThrottle.md
-->
