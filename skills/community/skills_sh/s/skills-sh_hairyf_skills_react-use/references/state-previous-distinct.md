---
name: state-previous-distinct
description: Like usePrevious but with predicate to determine if previous should update
---

# usePreviousDistinct

Just like `usePrevious` but it will only update once the value actually changes. This is important when other hooks are involved and you aren't just interested in the previous props version, but want to know the previous distinct value.

## Usage

```jsx
import {usePreviousDistinct, useCounter} from 'react-use';

const Demo = () => {
  const [count, { inc: relatedInc }] = useCounter(0);
  const [unrelatedCount, { inc }] = useCounter(0);
  const prevCount = usePreviousDistinct(count);

  return (
    <p>
      Now: {count}, before: {prevCount}
      <button onClick={() => relatedInc()}>Increment</button>
      Unrelated: {unrelatedCount}
      <button onClick={() => inc()}>Increment Unrelated</button>
    </p>
  );
};
```

## Reference

```ts
const prevState = usePreviousDistinct<T>(state: T, compare?: (prev: T | undefined, next: T) => boolean): T;
```

- **`compare`**: optional custom comparison function

## Key Points

- Only updates when value actually changes
- Supports custom comparison
- Useful for distinct value tracking

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/usePreviousDistinct.md
-->
