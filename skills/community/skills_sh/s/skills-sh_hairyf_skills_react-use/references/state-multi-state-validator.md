---
name: state-multi-state-validator
description: Validate multiple states with useMultiStateValidator hook
---

# useMultiStateValidator

Each time any of given states changes - validator function is invoked.

## Usage

```ts
import * as React from 'react';
import { useMultiStateValidator } from 'react-use';

const DemoStateValidator = (s: number[]) => [s.every((num: number) => !(num % 2))] as [boolean];
const Demo = () => {
  const [state1, setState1] = React.useState<number>(1);
  const [state2, setState2] = React.useState<number>(1);
  const [state3, setState3] = React.useState<number>(1);
  const [[isValid]] = useMultiStateValidator([state1, state2, state3], DemoStateValidator);

  return (
    <div>
      <div>Below fields will be valid if all of them is even</div>
      <input type="number" value={state1} onChange={(ev) => setState1(Number(ev.target.value))} />
      <input type="number" value={state2} onChange={(ev) => setState2(Number(ev.target.value))} />
      <input type="number" value={state3} onChange={(ev) => setState3(Number(ev.target.value))} />
      {isValid !== null && <span>{isValid ? 'Valid!' : 'Invalid'}</span>}
    </div>
  );
};
```

## Reference

```ts
const [validity, revalidate] = useMultiStateValidator(
  state: any[] | { [p: string]: any },
  validator: (state, setValidity?)=>[boolean|null, ...any[]],
  initialValidity: any = [undefined]
);
```

- **`state`**: array or object of states to validate
- **`validator`**: function that receives all states

## Key Points

- Validates multiple states together
- Triggers on any state change
- Useful for form validation

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useMultiStateValidator.md
-->
