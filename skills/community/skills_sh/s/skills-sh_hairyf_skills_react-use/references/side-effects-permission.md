---
name: side-effects-permission
description: Query permission status for browser APIs with usePermission hook
---

# usePermission

React side-effect hook to query permission status of browser APIs.

## Usage

```jsx
import {usePermission} from 'react-use';

const Demo = () => {
  const state = usePermission({ name: 'microphone' });

  return (
    <pre>
      {JSON.stringify(state, null, 2)}
    </pre>
  );
};
```

## Reference

```ts
usePermission(descriptor: PermissionDescriptor);
```

Returns permission state with:
- `state`: `PermissionState` - 'granted', 'denied', 'prompt', or 'unsupported'
- Other permission-specific properties

## Key Points

- Queries browser permission status
- Supports various permissions (camera, microphone, notifications, etc.)
- Useful for permission-aware UI

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/usePermission.md
-->
