---
name: animations-timeout
description: Re-render component after timeout with useTimeout hook
---

# useTimeout

Re-renders the component after a specified number of milliseconds. Provides handles to cancel and/or reset the timeout.

## Usage

```jsx
import { useTimeout } from 'react-use';

function TestComponent(props: { ms?: number } = {}) {
  const ms = props.ms || 5000;
  const [isReady, cancel] = useTimeout(ms);

  return (
    <div>
      { isReady() ? 'I\'m reloaded after timeout' : `I will be reloaded after ${ ms / 1000 }s` }
      { isReady() === false ? <button onClick={ cancel }>Cancel</button> : '' }
    </div>
  );
}
```

## Reference

```ts
const [
    isReady: () => boolean | null,
    cancel: () => void,
    reset: () => void,
] = useTimeout(ms: number = 0);
```

- **`isReady`**: `() => boolean | null` - function returning current timeout state:
  - `false` - pending re-render
  - `true` - re-render performed
  - `null` - re-render cancelled
- **`cancel`**: `() => void` - cancel the timeout
- **`reset`**: `() => void` - reset the timeout

## Key Points

- Re-renders component after timeout
- Provides cancel and reset controls
- Useful for delayed UI updates

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useTimeout.md
-->
