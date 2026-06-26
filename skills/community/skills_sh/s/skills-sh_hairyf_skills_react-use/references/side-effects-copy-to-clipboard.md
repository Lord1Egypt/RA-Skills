---
name: side-effects-copy-to-clipboard
description: Copy text to clipboard with useCopyToClipboard hook
---

# useCopyToClipboard

Copy text to a user's clipboard.

## Usage

```jsx
const Demo = () => {
  const [text, setText] = React.useState('');
  const [state, copyToClipboard] = useCopyToClipboard();

  return (
    <div>
      <input value={text} onChange={e => setText(e.target.value)} />
      <button type="button" onClick={() => copyToClipboard(text)}>copy text</button>
      {state.error
        ? <p>Unable to copy value: {state.error.message}</p>
        : state.value && <p>Copied {state.value}</p>}
    </div>
  )
}
```

## Reference

```js
const [{value, error, noUserInteraction}, copyToClipboard] = useCopyToClipboard();
```

- **`value`**: `string | undefined` - value that was copied to clipboard
- **`error`**: `Error | undefined` - caught error when trying to copy
- **`noUserInteraction`**: `boolean` - whether user interaction was required
- **`copyToClipboard`**: `(text: string) => void` - function to copy text

## Key Points

- Uses Clipboard API
- Provides error handling
- Tracks copy state
- Useful for copy buttons

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useCopyToClipboard.md
-->
