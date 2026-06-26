---
name: side-effects-title
description: Set title of the page with useTitle hook
---

# useTitle

React side-effect hook that sets title of the page.

## Usage

```jsx
import {useTitle} from 'react-use';

const Demo = () => {
  useTitle('Hello world!');

  return null;
};
```

## Reference

```ts
useTitle(title: string);
```

- **`title`**: `string` - title to set

## Key Points

- Dynamically changes page title
- Useful for dynamic page titles
- Updates document.title

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useTitle.md
-->
