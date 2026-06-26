# Getting Started — Syncfusion React DropDownButton

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [CSS Imports](#css-imports)
- [Basic Component](#basic-component)
- [Binding Data Source](#binding-data-source)
- [Run the Application](#run-the-application)

---

## Prerequisites

- React 16.8+
- Node.js 14+

---

## Installation

Create a new React project with Vite (recommended):

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install
```

Install the Syncfusion split-buttons package (which includes DropDownButton):

```bash
npm install @syncfusion/ej2-react-splitbuttons --save
```

---

## CSS Imports

Add the required CSS files in `src/App.css`:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-splitbuttons/styles/tailwind3.css";
```

Import `App.css` in `src/App.tsx`:

```tsx
import './App.css';
```

> Other available themes: `material3`, `bootstrap5`, `fluent2`, `fabric`. Replace `tailwind3` with the desired theme name in all four imports.

---

## Basic Component

Render an empty DropDownButton (no popup items yet):

```tsx
import { DropDownButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';
import './App.css';

enableRipple(true);

function App() {
  return (
    <div>
      <DropDownButtonComponent id="element" />
    </div>
  );
}

export default App;
```

`enableRipple(true)` adds a Material-style ripple effect on click. Call it once at the application entry point.

---

## Binding Data Source

Populate the popup using the `items` prop with an array of `ItemModel` objects. Each item requires at minimum a `text` property:

```tsx
import { DropDownButtonComponent, ItemModel } from '@syncfusion/ej2-react-splitbuttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';
import './App.css';

enableRipple(true);

function App() {
  const items: ItemModel[] = [
    { text: 'Cut' },
    { text: 'Copy' },
    { text: 'Paste' },
  ];

  return (
    <div>
      <DropDownButtonComponent id="element" items={items}>
        Clipboard
      </DropDownButtonComponent>
    </div>
  );
}

export default App;
```

**ItemModel fields commonly used:**

| Field | Type | Description |
|-------|------|-------------|
| `text` | `string` | Label displayed in the popup |
| `iconCss` | `string` | CSS class(es) for an icon |
| `url` | `string` | Navigation URL for the item |
| `separator` | `boolean` | Renders a horizontal divider |
| `disabled` | `boolean` | Disables a specific item |
| `id` | `string` | Unique identifier for the item |

---

## Run the Application

```bash
npm run dev
```

Open the URL shown in the terminal (typically `http://localhost:5173`). The DropDownButton renders with a caret; clicking it opens the popup with the configured items.
