---
name: sensors-search-param
description: Track browser's location search param with useSearchParam hook
---

# useSearchParam

React sensor hook that tracks browser's location search param.

## Usage

```jsx
import {useSearchParam} from 'react-use';

const Demo = () => {
  const edit = useSearchParam('edit');

  return (
    <div>
      <div>edit: {edit || '🤷‍♂️'}</div>
      <div>
        <button onClick={() => history.pushState({}, '', location.pathname + '?edit=123')}>Edit post 123 (?edit=123)</button>
      </div>
      <div>
      <button onClick={() => history.pushState({}, '', location.pathname + '?edit=999')}>Edit post 999 (?edit=999)</button>
      </div>
      <div>
        <button onClick={() => history.pushState({}, '', location.pathname)}>Close modal</button>
      </div>
    </div>
  );
};
```

## Reference

```js
const value = useSearchParam(paramName);
```

- **`paramName`**: `string` - name of the search parameter to track
- Returns: `string | null` - value of the search parameter or null if not present

## Caveats

When using a hash router, like `react-router`'s `<HashRouter>`, this hook won't be able to read the search parameters as they are considered part of the hash of the URL by browsers.

## Key Points

- Tracks a specific URL search parameter
- Returns null if parameter is not present
- Does not work with hash routers

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useSearchParam.md
-->
