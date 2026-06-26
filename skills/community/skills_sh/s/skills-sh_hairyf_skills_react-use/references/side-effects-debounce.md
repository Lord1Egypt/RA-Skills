---
name: side-effects-debounce
description: Debounce a function with useDebounce hook
---

# useDebounce

React hook that delays invoking a function until after wait milliseconds have elapsed since the last time the debounced function was invoked.

The third argument is the array of values that the debounce depends on, in the same manner as useEffect. The debounce timeout will start when one of the values changes.

## Usage

```jsx
const Demo = () => {
  const [state, setState] = React.useState('Typing stopped');
  const [val, setVal] = React.useState('');
  const [debouncedValue, setDebouncedValue] = React.useState('');

  const [, cancel] = useDebounce(
    () => {
      setState('Typing stopped');
      setDebouncedValue(val);
    },
    2000,
    [val]
  );

  return (
    <div>
      <input
        type="text"
        value={val}
        placeholder="Debounced input"
        onChange={({ currentTarget }) => {
          setState('Waiting for typing to stop...');
          setVal(currentTarget.value);
        }}
      />
      <div>{state}</div>
      <div>
        Debounced value: {debouncedValue}
        <button onClick={cancel}>Cancel debounce</button>
      </div>
    </div>
  );
};
```

## Reference

```ts
const [
    isReady: () => boolean | null,
    cancel: () => void,
] = useDebounce(fn: Function, ms: number, deps: DependencyList = []);
```

- **`fn`**: `Function` - function that will be called
- **`ms`**: `number` - delay in milliseconds
- **`deps`**: `DependencyList` - array of values that the debounce depends on
- **`isReady`**: `() => boolean | null` - function returning current debounce state
- **`cancel`**: `() => void` - cancel the debounce

## Key Points

- Delays function execution
- Resets on dependency changes
- Provides cancel capability
- Useful for search inputs and API calls

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useDebounce.md
-->
