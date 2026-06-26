---
name: side-effects-local-storage
description: Manage value in localStorage with useLocalStorage hook
---

# useLocalStorage

React side-effect hook that manages a single `localStorage` key.

## Usage

```jsx
import { useLocalStorage } from 'react-use';

const Demo = () => {
  const [value, setValue, remove] = useLocalStorage('my-key', 'foo');

  return (
    <div>
      <div>Value: {value}</div>
      <button onClick={() => setValue('bar')}>bar</button>
      <button onClick={() => setValue('baz')}>baz</button>
      <button onClick={() => remove()}>Remove</button>
    </div>
  );
};
```

## Reference

```js
useLocalStorage(key);
useLocalStorage(key, initialValue);
useLocalStorage(key, initialValue, { raw: true });
useLocalStorage(key, initialValue, {
  raw: false,
  serializer: (value: T) => string,
  deserializer: (value: string) => T,
});
```

- **`key`**: `string` - localStorage key to manage
- **`initialValue`**: `T` - initial value to set, if value in localStorage is empty
- **`raw`**: `boolean` - if set to `true`, hook will not attempt to JSON serialize stored values
- **`serializer`**: `(value: T) => string` - custom serializer (defaults to `JSON.stringify`)
- **`deserializer`**: `(value: string) => T` - custom deserializer (defaults to `JSON.parse`)

Returns: `[value, setValue, remove]`

## Key Points

- Automatically serializes/deserializes JSON
- Supports custom serializers
- Provides remove function
- Persists across page reloads

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useLocalStorage.md
-->
