# Getting Started — Syncfusion React Button

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [CSS Imports](#css-imports)
4. [Rendering the Button](#rendering-the-button)
5. [Enabling Ripple Effects](#enabling-ripple-effects)
6. [Click Handling](#click-handling)
7. [Using `ref` to Access the Instance](#using-ref-to-access-the-instance)

---

## Prerequisites

- React 16.8+
- Node.js 14+
- A Vite or Create React App project

Create a new Vite project:
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

## Installation

Install the Syncfusion Button package:

```bash
npm install @syncfusion/ej2-react-buttons --save
```

The `--save` flag adds the package to the `dependencies` section of `package.json`.

---

## CSS Imports

Add the required theme stylesheets to `src/App.css`:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-buttons/styles/tailwind3.css";
```

Import `App.css` in `src/App.tsx`:

```tsx
import './App.css';
```

> **Available themes:** tailwind3, bootstrap5, material3, fluent2. Replace `tailwind3` with your preferred theme name in both import paths.

---

## Rendering the Button

The `ButtonComponent` is the core element. Place it in `src/App.tsx`:

```tsx
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <div>
      <ButtonComponent>Button</ButtonComponent>
    </div>
  );
}
export default App;
```

Button text can be supplied as children **or** via the `content` prop:

```tsx
// Using children
<ButtonComponent>Click Me</ButtonComponent>

// Using the content prop
<ButtonComponent content="Click Me" />
```

---

## Enabling Ripple Effects

Import `enableRipple` from `@syncfusion/ej2-base` and call it **once** before rendering — typically at the top of `App.tsx`:

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import './App.css';

enableRipple(true);   // Call once; applies ripple to all Syncfusion components

function App() {
  return (
    <ButtonComponent cssClass='e-primary'>Save</ButtonComponent>
  );
}
export default App;
```

> Call `enableRipple(true)` before `ReactDOM.render` / `createRoot`. Calling it multiple times is safe but unnecessary.

---

## Click Handling

Handle clicks using the standard React `onClick` prop:

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

enableRipple(true);

function App() {
  function handleClick(): void {
    alert('Button clicked!');
  }

  return (
    <ButtonComponent cssClass='e-primary' onClick={handleClick}>
      Submit
    </ButtonComponent>
  );
}
export default App;
```

---

## Using `ref` to Access the Instance

Use a React `ref` to call imperative methods (`click`, `focusIn`, `destroy`) or access `element`:

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

enableRipple(true);

function App() {
  let btnRef: ButtonComponent | null = null;

  function onCreated(): void {
    // Access the underlying DOM element after component mounts
    if (btnRef && btnRef.element) {
      btnRef.element.setAttribute('title', 'Primary Button');
    }
  }

  return (
    <ButtonComponent
      ref={(scope) => { btnRef = scope; }}
      created={onCreated}
      isPrimary={true}
    >
      Button
    </ButtonComponent>
  );
}
export default App;
```

> The `created` event fires once rendering is complete — use it for post-render DOM operations such as setting `title` attributes.
