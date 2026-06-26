---
name: state-toggle
description: Track state of a boolean with useToggle hook
---

# useToggle

React state hook that tracks value of a boolean.

`useBoolean` is an alias for `useToggle`.

## Usage

```jsx
import {useToggle} from 'react-use';

const Demo = () => {
  const [on, toggle] = useToggle(true);

  return (
    <div>
      <div>{on ? 'ON' : 'OFF'}</div>
      <button onClick={toggle}>Toggle</button>
      <button onClick={() => toggle(true)}>set ON</button>
      <button onClick={() => toggle(false)}>set OFF</button>
    </div>
  );
};
```

## Reference

```ts
const [value, toggle] = useToggle(initialValue?: boolean);
```

- **`toggle`**: `(value?: boolean) => void` - toggle function, can accept boolean to set specific value

## Key Points

- Simple boolean state management
- Toggle or set specific value
- `useBoolean` is an alias

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useToggle.md
-->
