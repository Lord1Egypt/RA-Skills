---
name: sensors-media
description: Track state of CSS media query with useMedia hook
---

# useMedia

React sensor hook that tracks state of a CSS media query.

## Usage

```jsx
import {useMedia} from 'react-use';

const Demo = () => {
  const isWide = useMedia('(min-width: 480px)');

  return (
    <div>
      Screen is wide: {isWide ? 'Yes' : 'No'}
    </div>
  );
};
```

## Reference

```ts
useMedia(query: string, defaultState: boolean = false): boolean;
```

- **`query`**: `string` - CSS media query string
- **`defaultState`**: `boolean` - fallback state for server-side rendering, defaults to `false`
- Returns: `boolean` - whether the media query matches

## Key Points

- The `defaultState` parameter is only used as a fallback for server side rendering
- When server side rendering, it is important to set this parameter because without it the server's initial state will fallback to false, but the client will initialize to the result of the media query
- When React hydrates the server render, it may not match the client's state, which can lead to costly bugs

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useMedia.md
-->
