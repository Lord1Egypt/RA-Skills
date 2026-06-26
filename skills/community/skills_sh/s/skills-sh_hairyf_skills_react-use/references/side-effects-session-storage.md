---
name: side-effects-session-storage
description: Manage value in sessionStorage with useSessionStorage hook
---

# useSessionStorage

React side-effect hook that manages a single `sessionStorage` key.

## Usage

```jsx
import {useSessionStorage} from 'react-use';

const Demo = () => {
  const [value, setValue] = useSessionStorage('my-key', 'foo');

  return (
    <div>
      <div>Value: {value}</div>
      <button onClick={() => setValue('bar')}>bar</button>
      <button onClick={() => setValue('baz')}>baz</button>
    </div>
  );
};
```

## Reference

```js
useSessionStorage(key);
useSessionStorage(key, initialValue);
useSessionStorage(key, initialValue, raw);
```

- **`key`**: `string` - sessionStorage key to manage
- **`initialValue`**: `T` - initial value to set, if value in sessionStorage is empty
- **`raw`**: `boolean` - if set to `true`, hook will not attempt to JSON serialize stored values

## Key Points

- Similar API to `useLocalStorage`
- Persists only for session (cleared on tab close)
- Automatically serializes/deserializes JSON

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useSessionStorage.md
-->
