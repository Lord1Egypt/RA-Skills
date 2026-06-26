---
name: side-effects-favicon
description: Set favicon of the page with useFavicon hook
---

# useFavicon

React side-effect hook sets the favicon of the page.

## Usage

```jsx
import {useFavicon} from 'react-use';

const Demo = () => {
  useFavicon('https://cdn.sstatic.net/Sites/stackoverflow/img/favicon.ico');

  return null;
};
```

## Reference

```ts
useFavicon(url: string);
```

- **`url`**: `string` - URL of the favicon to set

## Key Points

- Dynamically changes page favicon
- Accepts URL string
- Useful for status indicators

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useFavicon.md
-->
