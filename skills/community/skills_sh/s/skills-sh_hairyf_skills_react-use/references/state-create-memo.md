---
name: state-create-memo
description: Factory of memoized hooks with createMemo
---

# createMemo

Hook factory, receives a function to be memoized, returns a memoized React hook, which receives the same arguments and returns the same result as the original function.

## Usage

```jsx
import {createMemo} from 'react-use';

const fibonacci = n => {
  if (n === 0) return 0;
  if (n === 1) return 1;
  return fibonacci(n - 1) + fibonacci(n - 2);
};

const useMemoFibonacci = createMemo(fibonacci);

const Demo = () => {
  const result = useMemoFibonacci(10);

  return (
    <div>
      fib(10) = {result}
    </div>
  );
};
```

## Reference

```js
const useMemoFn = createMemo(fn);
```

Returns a memoized hook that caches results based on arguments.

## Key Points

- Factory function creates memoized hook
- Caches function results
- Useful for expensive computations

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/createMemo.md
-->
