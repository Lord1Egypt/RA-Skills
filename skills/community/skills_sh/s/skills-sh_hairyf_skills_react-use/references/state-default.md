---
name: state-default
description: Return default value when state is null or undefined with useDefault hook
---

# useDefault

React state hook that returns the default value when state is null or undefined.

## Usage

```jsx
import {useDefault} from 'react-use';

const Demo = () => {
  const initialUser = { name: 'Marshall' }
  const defaultUser = { name: 'Mathers' }
  const [user, setUser] = useDefault(defaultUser, initialUser);

  return (
    <div>
      <div>User: {user.name}</div>
      <input onChange={e => setUser({ name: e.target.value })} />
      <button onClick={() => setUser(null)}>set to null</button>
    </div>
  );
};
```

## Reference

```ts
const [value, setValue] = useDefault(defaultValue, initialValue);
```

- **`defaultValue`**: `T` - value to use when state is null/undefined
- **`initialValue`**: `T | null | undefined` - initial state value

## Key Points

- Provides fallback for null/undefined
- Always returns non-null value
- Useful for optional props/state

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useDefault.md
-->
