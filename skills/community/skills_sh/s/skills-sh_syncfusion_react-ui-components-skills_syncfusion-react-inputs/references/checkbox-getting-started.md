# Getting Started — Syncfusion React CheckBox

Set up a React project and render a basic `CheckBoxComponent` from Syncfusion.

---

## Prerequisites

- Node.js installed
- A React project (Vite recommended)

### Create a new React app with Vite

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

## Install the Package

All Syncfusion EJ2 packages are published on [npmjs.com](https://www.npmjs.com/~syncfusionorg).

```bash
npm install @syncfusion/ej2-react-buttons --save
```

> The `--save` flag adds the package to `dependencies` in `package.json`.

---

## Add CSS References

Import the required CSS files in **`src/App.css`**:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
```

Then import `App.css` in **`src/App.tsx`** (or `App.jsx`):

```tsx
import './App.css';
```

---

## Add CheckBoxComponent

In **`src/App.tsx`**, import and render the component:

```tsx
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <div>
      <CheckBoxComponent label="Default" />
    </div>
  );
}
export default App;
```

---

## Enable Ripple Effect (Optional)

For a Material-style ripple on click, use `enableRipple` from `@syncfusion/ej2-base`:

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import './App.css';

enableRipple(true);

function App() {
  return (
    <CheckBoxComponent label="Default" />
  );
}
export default App;
```

---

## Run the Application

```bash
npm run dev
```

The browser opens with the rendered CheckBox. The output displays a checkbox with the label **"Default"**.

---

## Troubleshooting

- **Styles not applying** — Verify CSS import paths match your `node_modules` location.
- **Component not found** — Ensure `@syncfusion/ej2-react-buttons` is installed and listed in `package.json`.
- **TypeScript errors** — Use `.tsx` extensions and ensure `@types/react` is installed.
