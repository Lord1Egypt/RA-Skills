# Getting Started – Syncfusion React Floating Action Button

## Table of Contents
- [Installation](#installation)
- [CSS Imports](#css-imports)
- [Basic FAB Setup](#basic-fab-setup)
- [Positioning Relative to a Container](#positioning-relative-to-a-container)
- [Click Event](#click-event)
- [Running the Application](#running-the-application)

---

## Installation

The Floating Action Button is part of the `@syncfusion/ej2-react-buttons` package.

```bash
npm install @syncfusion/ej2-react-buttons --save
```

Create a new Vite + React app if needed:

```bash
# TypeScript
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install @syncfusion/ej2-react-buttons --save
npm run dev

# JavaScript
npm create vite@latest my-app -- --template react
cd my-app
npm install @syncfusion/ej2-react-buttons --save
npm run dev
```

---

## CSS Imports

Add theme imports to `src/App.css`:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
```

Import the CSS file in `src/App.tsx`:

```tsx
import './App.css';
```

---

## Basic FAB Setup

The simplest FAB renders with just an `id`. By default it positions itself at the bottom-right of the browser viewport.

```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <FabComponent id="fab" />
  );
}
export default App;
```

Add `content` to display a text label:

```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  return (
    <FabComponent id="fab" content="Add" />
  );
}
export default App;
```

---

## Positioning Relative to a Container

Use the `target` prop to scope FAB positioning inside a container element. The container **must** have `position: relative` set.

```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import { enableRipple } from '@syncfusion/ej2-base';
import * as ReactDom from 'react-dom';

enableRipple(true);

function App() {
  return (
    <div>
      <div
        id="targetElement"
        style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}
      ></div>
      {/* FAB positioned relative to #targetElement */}
      <FabComponent id="fab" content="Add" target="#targetElement" />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

> **Tip:** Without a `target`, the FAB positions itself relative to the browser viewport. The target element must have `position: relative` or the FAB will walk up the DOM to the nearest relatively-positioned ancestor.

---

## Click Event

Handle user interactions using the `onClick` prop:

```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  function onClick(): void {
    alert('Edit is clicked!');
  }

  return (
    <div>
      <div
        id="targetElement"
        style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}
      ></div>
      <FabComponent
        id="fab"
        iconCss="e-icons e-edit"
        content="Edit"
        onClick={onClick}
        target="#targetElement"
      />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

---

## Running the Application

```bash
npm run dev
```

The development server starts and opens the app in your browser.
