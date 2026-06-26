---
name: state-set-state
description: Create setState method that works like this.setState with useSetState hook
---

# useSetState

React state hook that creates `setState` method which works similar to how `this.setState` works in class components—it merges object changes into current state.

## Usage

```jsx
import {useSetState} from 'react-use';

const Demo = () => {
  const [state, setState] = useSetState({});

  return (
    <div>
      <pre>{JSON.stringify(state, null, 2)}</pre>
      <button onClick={() => setState({hello: 'world'})}>hello</button>
      <button onClick={() => setState({foo: 'bar'})}>foo</button>
      <button 
        onClick={() => {
          setState((prevState) => ({
            count: (prevState.count || 0) + 1,
          }))
        }}
      >
        count
      </button>
    </div>
  );
};
```

## Reference

```js
const [state, setState] = useSetState({cnt: 0});

setState({cnt: state.cnt + 1});
setState((prevState) => ({
  cnt: prevState + 1,
}));
```

Merges partial state updates like class component setState.

## Key Points

- Merges object updates
- Supports function updates
- Familiar API from class components

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useSetState.md
-->
