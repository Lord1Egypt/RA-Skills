---
name: core-usage
description: Import patterns and tree-shaking recommendations for react-use
---

# Usage

How to import and use react-use hooks in your React application.

## Import Methods

You can import hooks individually for better tree-shaking:

```js
import useToggle from 'react-use/lib/useToggle'
```

Or use ES6 named imports:

```js
import {useToggle} from 'react-use'
```

## Tree-Shaking with Babel

For optimal bundle size, use `babel-plugin-import` to transform named imports to individual imports:

```json
[
  "import",
  {
    "libraryName": "react-use",
    "camel2DashComponentName": false,
    "customName": (name) => {
      const libraryDirectory = name.startsWith('Use')
        ? 'lib/component'
        : name.startsWith('create')
        ? 'lib/factory'
        : 'lib'
      return `react-use/${libraryDirectory}/${name}`
    }
  },
  "import-react-use"
]
```

## Requirements

- React 16.8.0 or later (for Hooks API support)
- Some hooks may require peer dependencies (check individual hook documentation)

## Key Points

- **Individual imports** are recommended for better tree-shaking
- **Named imports** work but may require additional bundler configuration
- **babel-plugin-import** provides the best of both worlds (named imports with tree-shaking)

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/Usage.md
-->
