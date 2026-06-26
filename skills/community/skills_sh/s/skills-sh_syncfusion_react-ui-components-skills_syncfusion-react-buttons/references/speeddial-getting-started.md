# Getting Started – Syncfusion React Speed Dial

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [CSS Setup](#css-setup)
- [Basic Speed Dial](#basic-speed-dial)
- [Target Element](#target-element)
- [Minimal Working Example](#minimal-working-example)

---

## Prerequisites

- React 16.8+, Node.js 14+
- Vite (recommended) or Create React App

Create a Vite React project:

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm run dev
```

---

## Installation

Install the Syncfusion buttons package, which includes the SpeedDial component:

```bash
npm install @syncfusion/ej2-react-buttons --save
```

---

## CSS Setup

Add theme CSS imports in `src/App.css`:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
```

Import `App.css` in `src/App.tsx`:

```tsx
import './App.css';
```

---

## Basic Speed Dial

The minimal `SpeedDialComponent` requires an `id`. Add `items` to populate the expandable action menu:

```tsx
import { SpeedDialComponent, SpeedDialItemModel } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import './App.css';

function App() {
  const items: SpeedDialItemModel[] = [
    { text: 'Cut' },
    { text: 'Copy' },
    { text: 'Paste' }
  ];

  return (
    <div id="targetElement" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}>
      <SpeedDialComponent id='speeddial' items={items} content='Edit' target="#targetElement" />
    </div>
  );
}
export default App;
```

---

## Target Element

The `target` property anchors the SpeedDial to a specific container. Without `target`, the component positions relative to the browser viewport.

**Important:** The target element must have `position: relative` for correct placement.

```tsx
// The SpeedDial positions itself inside #targetElement
<div id="targetElement" style={{ position: 'relative', minHeight: '350px' }}>
  <SpeedDialComponent id='speeddial' content='Edit' items={items} target="#targetElement" />
</div>
```

---

## Minimal Working Example

```tsx
import { SpeedDialComponent, SpeedDialItemModel } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  const items: SpeedDialItemModel[] = [
    { text: 'Cut', iconCss: 'e-icons e-cut' },
    { text: 'Copy', iconCss: 'e-icons e-copy' },
    { text: 'Paste', iconCss: 'e-icons e-paste' }
  ];

  return (
    <div>
      <div id="targetElement" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      <SpeedDialComponent
        id='speeddial'
        content='Edit'
        openIconCss='e-icons e-edit'
        closeIconCss='e-icons e-close'
        items={items}
        target="#targetElement"
      />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

After running `npm run dev`, the Speed Dial button appears at the bottom-right of the target element. Click it to expand the action items.
