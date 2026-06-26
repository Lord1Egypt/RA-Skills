---
name: sensors-hash
description: Track browser's location hash with useHash hook
---

# useHash

React sensor hook that tracks browser's location hash.

## Usage

```jsx
import {useHash} from 'react-use';

const Demo = () => {
  const [hash, setHash] = useHash();

  useMount(() => {
    setHash('#/path/to/page?userId=123');
  });

  return (
    <div>
      <div>window.location.href:</div>
      <div>
        <pre>{window.location.href}</pre>
      </div>
      <div>Edit hash: </div>
      <div>
        <input style={{ width: '100%' }} value={hash} onChange={e => setHash(e.target.value)} />
      </div>
    </div>
  );
};
```

## Reference

```js
const [hash, setHash] = useHash()
```

- **`hash`**: `string` - get current url hash, listens to `hashchange` event
- **`setHash`**: `(newHash: string) => void` - change url hash, invokes this method will trigger `hashchange` event

## Key Points

- Automatically listens to `hashchange` events
- Setting hash programmatically triggers `hashchange` event
- Useful for single-page application routing

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useHash.md
-->
