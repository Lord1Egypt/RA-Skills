# Getting Started — Syncfusion React RadioButton

This guide covers installing the package, setting up CSS, and rendering your first `RadioButtonComponent`.

---

## Installation

Install the Syncfusion buttons package (includes RadioButton, Button, Checkbox, etc.):

```bash
npm install @syncfusion/ej2-react-buttons --save
```

> The `--save` flag adds the package to your `package.json` dependencies.

---

## CSS Import

Add the required theme styles in `src/App.css`:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
```

Then import `App.css` in `src/App.tsx`:

```tsx
import './App.css';
```

**Available themes:** `material.css`, `bootstrap5.css`, `fluent.css`, `tailwind3.css`, `highcontrast.css`  
Replace `tailwind3` with your preferred theme name.

---

## Project Setup (Vite + React)

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install @syncfusion/ej2-react-buttons --save
npm run dev
```

---

## Basic RadioButton

```tsx
import { RadioButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <div>
      <RadioButtonComponent label="Default" />
    </div>
  );
}
export default App;
```

---

## Grouping Radio Buttons

Use the `name` property to group buttons as mutually exclusive options. Only one button in a group can be selected at a time:

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { RadioButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

enableRipple(true);

function App() {
  return (
    <ul>
      <li><RadioButtonComponent label="Option 1" name="default" /></li>
      <li><RadioButtonComponent label="Option 2" name="default" /></li>
      <li><RadioButtonComponent label="Option 3" name="default" /></li>
    </ul>
  );
}
export default App;
```

> **Why `name` matters:** All `RadioButtonComponent` elements sharing the same `name` value form a mutually exclusive group. Selecting one automatically deselects others in the group.

---

## Enabling Ripple Effect

The ripple animation (Material Design) is enabled via `enableRipple` from `@syncfusion/ej2-base`. Call it once at your app entry point:

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
enableRipple(true);
```

---

## Run the Application

```bash
npm run dev
```

Open the browser at the local URL (typically `http://localhost:5173`).

---

## See Also

- [label-and-size.md](label-and-size.md) — label positioning and size variants
- [features-and-state.md](features-and-state.md) — checked state, disabled, form submission
- [api.md](api.md) — full property/event reference
