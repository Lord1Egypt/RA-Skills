---
name: state-create-state-context
description: Factory of hooks for sharing state between components with createStateContext
---

# createStateContext

Factory for react context hooks that will behave just like [React's `useState`](https://reactjs.org/docs/hooks-reference.html#usestate) except the state will be shared among all components in the provider.

This allows you to have a shared state that any component can update easily.

## Usage

```jsx
import { createStateContext } from 'react-use';

const [useSharedText, SharedTextProvider] = createStateContext('');

const ComponentA = () => {
  const [text, setText] = useSharedText();
  return (
    <p>
      Component A:
      <br />
      <input type="text" value={text} onInput={ev => setText(ev.target.value)} />
    </p>
  );
};

const Demo = () => {
  return (
    <SharedTextProvider>
      <ComponentA />
    </SharedTextProvider>
  );
};
```

## Reference

```jsx
const [useSharedState, SharedStateProvider] = createStateContext(initialValue);
```

Returns hook and provider for shared state.

## Key Points

- Shared state via Context
- useState-like API
- Provider-based sharing

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/createStateContext.md
-->
