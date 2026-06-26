---
name: side-effects-before-unload
description: Show browser alert when user tries to reload or close page with useBeforeUnload hook
---

# useBeforeUnload

React side-effect hook that shows browser alert when user tries to reload or close the page.

## Usage

### Boolean check

```jsx
import {useBeforeUnload} from 'react-use';

const Demo = () => {
  const [dirty, toggleDirty] = useToggle(false);
  useBeforeUnload(dirty, 'You have unsaved changes, are you sure?');

  return (
    <div>
      {dirty && <p>Try to reload or close tab</p>}
      <button onClick={() => toggleDirty()}>{dirty ? 'Disable' : 'Enable'}</button>
    </div>
  );
};
```

### Function check

```jsx
import {useBeforeUnload} from 'react-use';

const Demo = () => {
  const [dirty, toggleDirty] = useToggle(false);
  const dirtyFn = useCallback(() => {
    return dirty;
  }, [dirty]);
  useBeforeUnload(dirtyFn, 'You have unsaved changes, are you sure?');

  return (
    <div>
      {dirty && <p>Try to reload or close tab</p>}
      <button onClick={() => toggleDirty()}>{dirty ? 'Disable' : 'Enable'}</button>
    </div>
  );
};
```

## Reference

```ts
useBeforeUnload(enabled: boolean | (() => boolean), message?: string);
```

- **`enabled`**: `boolean | (() => boolean)` - whether to show alert
- **`message`**: `string` - optional message to show

## Key Points

- Shows browser confirmation dialog
- Supports boolean or function check
- Use function check with refs if value changes often
- Useful for preventing data loss

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useBeforeUnload.md
-->
