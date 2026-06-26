---
name: state-create-global-state
description: Cross component shared state with createGlobalState
---

# createGlobalState

A React hook that creates a globally shared state.

## Usage

```tsx
const useGlobalValue = createGlobalState<number>(0);

const CompA: FC = () => {
  const [value, setValue] = useGlobalValue();

  return <button onClick={() => setValue(value + 1)}>+</button>;
};

const CompB: FC = () => {
  const [value, setValue] = useGlobalValue();

  return <button onClick={() => setValue(value - 1)}>-</button>;
};

const Demo: FC = () => {
  const [value] = useGlobalValue();
  return (
    <div>
      <p>{value}</p>
      <CompA />
      <CompB />
    </div>
  );
};
```

## Reference

```ts
const useGlobalValue = createGlobalState<T>(initialValue: T | (() => T));
const [value, setValue] = useGlobalValue();
```

Returns a hook that provides global state shared across all components.

## Key Points

- Global state without Context
- Shared across all components
- Supports function initializers

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/createGlobalState.md
-->
