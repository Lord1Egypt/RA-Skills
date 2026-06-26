---
name: sensors-keyboard-js
description: Detect complex key combinations with useKeyboardJs hook
---

# useKeyboardJs

React UI sensor hook that detects complex key combos like detecting when multiple keys are held down at the same time or requiring them to be held down in a specified order.

Via [KeyboardJS key combos](https://github.com/RobertWHurst/KeyboardJS). Check its documentation for further details on how to make combo strings.

## Usage

```jsx
import useKeyboardJs from 'react-use/lib/useKeyboardJs';

const Demo = () => {
  const [isPressed] = useKeyboardJs('a + b');

  return (
    <div>
      [a + b] pressed: {isPressed ? 'Yes' : 'No'}
    </div>
  );
};
```

## Requirements

Install [`keyboardjs`](https://github.com/RobertWHurst/KeyboardJS) peer dependency:

```bash
npm add keyboardjs
# or
yarn add keyboardjs
```

## Reference

```js
useKeyboardJs(combination: string | string[]): [isPressed: boolean, event?: KeyboardEvent]
```

- **`combination`**: `string | string[]` - key combination string (e.g., 'ctrl + shift + k') or array of combinations
- Returns: `[isPressed: boolean, event?: KeyboardEvent]` - whether combination is pressed and optional event

## Key Points

- Requires `keyboardjs` as peer dependency
- Must import directly: `import useKeyboardJs from 'react-use/lib/useKeyboardJs'`
- Supports complex combinations like 'ctrl + shift + k' or 'a + b + c'
- Useful for keyboard shortcuts and hotkeys

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useKeyboardJs.md
-->
