# Positions – Syncfusion React Floating Action Button

## Table of Contents
- [Overview](#overview)
- [Predefined Positions](#predefined-positions)
- [Positioning with a Target Container](#positioning-with-a-target-container)
- [All Positions Demo](#all-positions-demo)
- [Custom Position](#custom-position)
- [Refreshing Position](#refreshing-position)

---

## Overview

The `position` property controls where the FAB appears. Combined with the `target` property, the FAB positions itself relative to the specified container element. Without a `target`, it positions itself relative to the **browser viewport**.

> **Important:** The target element must have `position: relative` set in its CSS. Otherwise, the FAB walks up the DOM to the nearest relatively-positioned ancestor.

---

## Predefined Positions

The `position` prop accepts one of nine string values:

| Value | Description |
|-------|-------------|
| `'TopLeft'` | Top-left corner of the target/viewport |
| `'TopCenter'` | Top-center of the target/viewport |
| `'TopRight'` | Top-right corner of the target/viewport |
| `'MiddleLeft'` | Middle-left of the target/viewport |
| `'MiddleCenter'` | Center of the target/viewport |
| `'MiddleRight'` | Middle-right of the target/viewport |
| `'BottomLeft'` | Bottom-left corner of the target/viewport |
| `'BottomCenter'` | Bottom-center of the target/viewport |
| `'BottomRight'` | Bottom-right corner of the target/viewport (default) |

Default is `'BottomRight'`.

```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  return (
    // FAB at the bottom-left of the viewport
    <FabComponent id="fab" content="Add" position="BottomLeft" />
  );
}
export default App;
```

---

## Positioning with a Target Container

Provide the `target` prop (a CSS selector string or `HTMLElement`) to position the FAB inside a specific container:

```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  return (
    <div>
      <div id="target" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      <FabComponent id="fab" content="Add" position="BottomRight" target="#target" />
    </div>
  );
}
export default App;
```

---

## All Positions Demo

Render a FAB at each of the nine positions simultaneously:

```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  return (
    <div>
      <div id="target" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      <FabComponent id="fab1" iconCss="fab-icons fab-icon-people" position="TopLeft"      target="#target" />
      <FabComponent id="fab2" iconCss="fab-icons fab-icon-people" position="TopCenter"    target="#target" />
      <FabComponent id="fab3" iconCss="fab-icons fab-icon-people" position="TopRight"     target="#target" />
      <FabComponent id="fab4" iconCss="fab-icons fab-icon-people" position="MiddleLeft"   target="#target" />
      <FabComponent id="fab5" iconCss="fab-icons fab-icon-people" position="MiddleCenter" target="#target" />
      <FabComponent id="fab6" iconCss="fab-icons fab-icon-people" position="MiddleRight"  target="#target" />
      <FabComponent id="fab7" iconCss="fab-icons fab-icon-people" position="BottomLeft"   target="#target" />
      <FabComponent id="fab8" iconCss="fab-icons fab-icon-people" position="BottomCenter" target="#target" />
      <FabComponent id="fab9" iconCss="fab-icons fab-icon-people" position="BottomRight"  target="#target" />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

---

## Custom Position

For layouts that need precise control beyond the nine presets, override the FAB's CSS using the `cssClass` property and target the position offsets in your stylesheet.

```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  return (
    <div>
      <div id="targetElement" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      <FabComponent id="fab" iconCss="e-icons e-edit" cssClass="custom-position" target="#targetElement" />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

Override the position in your CSS:

```css
/* Custom position: 20px from the top and 50% horizontally */
.custom-position {
  top: 20px !important;
  bottom: auto !important;
  left: 50% !important;
  right: auto !important;
  transform: translateX(-50%);
}
```

---

## Refreshing Position

Call the `refreshPosition()` method when the target container resizes dynamically to recalculate and reapply the FAB's position:

```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  const fabRef = React.useRef<FabComponent>(null);

  function handleResize(): void {
    if (fabRef.current) {
      fabRef.current.refreshPosition();
    }
  }

  return (
    <div>
      <div id="target" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      <button onClick={handleResize}>Simulate Resize</button>
      <FabComponent ref={fabRef} id="fab" content="Add" target="#target" />
    </div>
  );
}
export default App;
```
