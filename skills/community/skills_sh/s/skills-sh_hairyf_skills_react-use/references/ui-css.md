---
name: ui-css
description: Dynamically adjust CSS with useCss hook
---

# useCss

React UI hook that changes CSS dynamically. Works like "virtual CSS" — it re-renders only CSS rules that change. It is different from inline styles, because you can use media queries and pseudo selectors.

## Usage

```jsx
import {useCss} from 'react-use';

const Demo = () => {
  const className = useCss({
    color: 'red',
    border: '1px solid red',
    '&:hover': {
      color: 'blue',
    },
  });

  return (
    <div className={className}>
      Hover me!
    </div>
  );
};
```

## Examples

```js
const className = useCss({
  color: 'tomato',
  '&:hover': {
    color: 'orange',
  },
});

const className = useCss({
  svg: {
    fill: 'tomato',
  },
  '.global_class &:hover svg': {
    fill: 'orange',
  },
});

const className = useCss({
  color: 'tomato',
  '@media only screen and (max-width: 600px)': {
    color: 'orange',
    '&:hover': {
      color: 'red',
    }
  },
});
```

## Reference

```ts
const className: string = useCss(styles: CSSObject);
```

- **`styles`**: `CSSObject` - CSS-in-JS object with support for:
  - Regular CSS properties
  - Pseudo-selectors (`&:hover`, `&:focus`, etc.)
  - Media queries (`@media ...`)
  - Nested selectors

## Key Points

- Generates unique class names dynamically
- Supports pseudo-selectors and media queries
- More powerful than inline styles
- Only re-renders changed CSS rules

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useCss.md
-->
