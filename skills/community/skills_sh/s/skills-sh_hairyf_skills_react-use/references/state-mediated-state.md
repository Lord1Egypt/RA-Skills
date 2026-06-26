---
name: state-mediated-state
description: useState with mediation by custom function using useMediatedState hook
---

# useMediatedState

A lot like the standard `useState`, but with mediation process.

## Usage

```ts
import * as React from 'react';
import { useMediatedState } from 'react-use';

const inputMediator = s => s.replace(/[\s]+/g, ' ');
const Demo = () => {
  const [state, setState] = useMediatedState(inputMediator, '');

  return (
    <div>
      <div>You will not be able to enter more than one space</div>
      <input type="text" 
             value={state}
             onChange={(ev) => setState(ev.target.value)}
      />
    </div>
  );
};
```

## Reference

```ts
const [state, setState] = useMediatedState<S=any>(
  mediator: StateMediator<S>,
  initialState?: S
);
```

- **`mediator`**: `(value: S, setState?: (value: S) => void) => S` - function that transforms state
- Supports async mediators (2-arg form)

## Key Points

- Transforms state before setting
- Supports async mediators
- Useful for input sanitization

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useMediatedState.md
-->
