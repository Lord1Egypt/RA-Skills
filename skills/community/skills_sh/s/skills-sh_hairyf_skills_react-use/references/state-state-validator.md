---
name: state-state-validator
description: Validate state with validator function using useStateValidator hook
---

# useStateValidator

Each time given state changes - validator function is invoked.

## Usage

```ts
import * as React from 'react';
import { useStateValidator } from 'react-use';

const DemoStateValidator = s => [s === '' ? null : (s * 1) % 2 === 0];
const Demo = () => {
  const [state, setState] = React.useState<string | number>(0);
  const [[isValid]] = useStateValidator(state, DemoStateValidator);

  return (
    <div>
      <div>Below field is valid only if number is even</div>
      <input
        type="number"
        value={state}
        onChange={(ev) => setState(ev.target.value)}
      />
      {isValid !== null && <span>{isValid ? 'Valid!' : 'Invalid'}</span>}
    </div>
  );
};
```

## Reference

```ts
const [validity, revalidate] = useStateValidator(
  state: any,
  validator: (state, setValidity?)=>[boolean|null, ...any[]],
  initialValidity: any
);
```

- **`validity`**: `[boolean|null, ...any[]]` - validation result
- **`revalidate`**: `() => void` - manually revalidate
- **`validator`**: function that returns validity array

## Key Points

- Automatic validation on state change
- Supports async validators
- Returns validation result array

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useStateValidator.md
-->
