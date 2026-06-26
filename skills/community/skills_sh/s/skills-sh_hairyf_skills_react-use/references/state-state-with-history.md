---
name: state-state-with-history
description: Store previous state values with history navigation using useStateWithHistory hook
---

# useStateWithHistory

Stores defined amount of previous state values and provides handles to travel through them.

## Reference

```typescript
const [state, setState, stateHistory] = useStateWithHistory<S = undefined>(
  initialState?: S | (()=>S),
  capacity?: number = 10,
  initialHistory?: S
);
```

- **`state`**, **`setState`**: same as React's `useState`
- **`capacity`**: amount of history entries (default: 10)
- **`stateHistory`**: object with:
  - **`history`**: `S[]` - array of history entries
  - **`position`**: `number` - current position in history
  - **`back(amount?)`**: go back in history
  - **`forward(amount?)`**: go forward in history
  - **`go(position)`**: go to arbitrary position

## Key Points

- Maintains state history
- Navigate forward/backward
- Configurable capacity
- Useful for undo/redo

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useStateWithHistory.md
-->
