---
name: state-map
description: Track state of an object with useMap hook
---

# useMap

React state hook that tracks a value of an object.

## Usage

```jsx
import {useMap} from 'react-use';

const Demo = () => {
  const [map, {set, setAll, remove, reset}] = useMap({
    hello: 'there',
  });

  return (
    <div>
      <button onClick={() => set(String(Date.now()), new Date().toJSON())}>
        Add
      </button>
      <button onClick={() => reset()}>
        Reset
      </button>
      <button onClick={() => setAll({ hello: 'new', data: 'data' })}>
        Set new data
      </button>
      <button onClick={() => remove('hello')} disabled={!map.hello}>
        Remove 'hello'
      </button>
      <pre>{JSON.stringify(map, null, 2)}</pre>
    </div>
  );
};
```

## Reference

```ts
const [map, {set, setAll, remove, reset}] = useMap(initialMap?: Record<string, T>);
```

- **`set(key, value)`**: set a key-value pair
- **`setAll(map)`**: replace entire map
- **`remove(key)`**: remove a key
- **`reset()`**: reset to initial value

## Key Points

- Object/Map state management
- Key-value operations
- Useful for keyed state

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useMap.md
-->
