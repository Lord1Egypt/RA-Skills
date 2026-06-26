---
name: state-counter
description: Track state of a number with useCounter hook
---

# useCounter

React state hook that tracks a numeric value.

`useNumber` is an alias for `useCounter`.

## Usage

```jsx
import {useCounter, useNumber} from 'react-use';

const Demo = () => {
  const [min, { inc: incMin, dec: decMin }] = useCounter(1);
  const [max, { inc: incMax, dec: decMax }] = useCounter(10);
  const [value, { inc, dec, set, reset }] = useCounter(5, max, min);

  return (
    <div>
      <div>
        current: { value } [min: { min }; max: { max }]
      </div>
      <button onClick={ () => inc() }>Increment</button>
      <button onClick={ () => dec() }>Decrement</button>
      <button onClick={ () => inc(5) }>Increment (+5)</button>
      <button onClick={ () => dec(5) }>Decrement (-5)</button>
      <button onClick={ () => set(100) }>Set 100</button>
      <button onClick={ () => reset() }>Reset</button>
    </div>
  );
};
```

## Reference

```ts
const [ current, { inc, dec, get, set, reset } ] = useCounter(initial: number, max: number | null = null, min: number | null = null);
```

- **`inc(delta?: number)`**: increment value
- **`dec(delta?: number)`**: decrement value
- **`set(value: number)`**: set arbitrary value
- **`reset(value?: number)`**: reset to initial value
- **`get()`**: getter for current value

## Key Points

- Supports min/max bounds
- Provides increment/decrement with delta
- `useNumber` is an alias

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useCounter.md
-->
