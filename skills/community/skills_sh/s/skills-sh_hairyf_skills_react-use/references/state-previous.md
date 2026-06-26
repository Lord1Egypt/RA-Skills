---
name: state-previous
description: Return previous state or props with usePrevious hook
---

# usePrevious

React state hook that returns the previous state as described in the [React hooks FAQ](https://reactjs.org/docs/hooks-faq.html#how-to-get-the-previous-props-or-state).

## Usage

```jsx
import {usePrevious} from 'react-use';

const Demo = () => {
  const [count, setCount] = React.useState(0);
  const prevCount = usePrevious(count);

  return (
    <p>
      <button onClick={() => setCount(count + 1)}>+</button>
      <button onClick={() => setCount(count - 1)}>-</button>
      <p>
        Now: {count}, before: {prevCount}
      </p>
    </p>
  );
};
```

## Reference

```ts
const prevState = usePrevious<T>(state: T): T;
```

Returns the previous value of state.

## Key Points

- Tracks previous value
- Returns previous on each render
- Useful for change detection

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/usePrevious.md
-->
