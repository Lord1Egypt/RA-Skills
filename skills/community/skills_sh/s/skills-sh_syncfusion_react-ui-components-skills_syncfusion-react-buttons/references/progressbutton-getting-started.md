# Getting Started — React ProgressButton

## Overview

This guide walks through creating a React project and adding the Syncfusion `ProgressButtonComponent`
from `@syncfusion/ej2-react-splitbuttons`.

---

## 1. Create a React application

**Vite (recommended — faster builds, smaller bundles):**

```bash
# JavaScript
npm create vite@latest my-app -- --template react
cd my-app
npm run dev

# TypeScript
npm create vite@latest my-app -- --template react-ts
cd my-app
npm run dev
```

---

## 2. Install the ProgressButton package

```bash
npm install @syncfusion/ej2-react-splitbuttons --save
```

> `--save` adds the package to the `dependencies` section of `package.json`.
>
> The `@syncfusion/ej2-react-splitbuttons` package ships `ProgressButtonComponent` along with
> `SplitButtonComponent`, `DropDownButtonComponent`, and related models.

---

## 3. Add CSS references

Add the following imports to `src/App.css` (or your global stylesheet). Choose the theme
matching your project:

```css
/* Tailwind 3 (default in recent Syncfusion demos) */
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-splitbuttons/styles/tailwind3.css";
```

Then import the stylesheet in `src/App.tsx`:

```tsx
import './App.css';
```

**Other available themes** (replace `tailwind3` with one of):
`material`, `material3`, `bootstrap5`, `fluent`, `highcontrast`

---

## 4. Add the ProgressButton component

`src/App.tsx`:

```tsx
import { ProgressButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <div>
      <ProgressButtonComponent content="Spin Left" />
    </div>
  );
}

export default App;
```

---

## 5. Run the application

```bash
npm run dev
```

Open the URL shown in the terminal (typically `http://localhost:5173`).

---

## See Also

- [Spinner and Progress options](spinner-and-progress.md)
- [API Reference](api.md)
