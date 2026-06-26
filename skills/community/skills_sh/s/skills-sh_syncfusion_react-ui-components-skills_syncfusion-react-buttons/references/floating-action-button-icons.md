# Icons and Content – Syncfusion React Floating Action Button

## Table of Contents
- [Icon-Only FAB](#icon-only-fab)
- [FAB with Icon and Text](#fab-with-icon-and-text)
- [Icon Position](#icon-position)
- [Tooltip for Icon-Only FAB](#tooltip-for-icon-only-fab)

---

## Icon-Only FAB

Set the `iconCss` property with a CSS class to display an icon-only FAB. The `iconCss` value can reference Syncfusion built-in icons (prefixed with `e-icons`) or any custom icon font class.

```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  return (
    // Icon-only FAB using Syncfusion built-in icon
    <FabComponent id="fab" iconCss="fab-icons fab-icon-people" />
  );
}
export default App;
```

Using a Syncfusion built-in `e-icons` class:

```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  return (
    <FabComponent id="fab" iconCss="e-icons e-edit" />
  );
}
export default App;
```

---

## FAB with Icon and Text

Set both `iconCss` and `content` to display an icon alongside a text label:

```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  return (
    <FabComponent id="fab" iconCss="fab-icons fab-icon-people" content="Contacts" />
  );
}
export default App;
```

Full example with a target container:

```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  return (
    <div>
      <div id="targetElement" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      <FabComponent
        id="fab"
        iconCss="fab-icons fab-icon-people"
        content="Contacts"
        target="#targetElement"
      />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

---

## Icon Position

Control whether the icon appears to the **left** (default) or **right** of the text using the `iconPosition` property.

| Value | Description |
|-------|-------------|
| `'Left'` | Icon appears to the left of the text content (default) |
| `'Right'` | Icon appears to the right of the text content |

```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  return (
    // Icon placed to the right of the text
    <FabComponent id="fab" iconCss="fab-icons fab-icon-people" content="Contacts" iconPosition="Right" />
  );
}
export default App;
```

Full example:

```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  return (
    <div>
      <div id="targetElement" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      <FabComponent
        id="fab"
        iconCss="fab-icons fab-icon-people"
        content="Contacts"
        iconPosition="Right"
        target="#targetElement"
      />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

---

## Tooltip for Icon-Only FAB

Add a `title` attribute on the FAB to show a browser tooltip on hover. This helps users understand the FAB's purpose when no text label is visible:

```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  return (
    <FabComponent
      id="fab"
      iconCss="fab-icons fab-icon-people"
      title="Add Contact"
    />
  );
}
export default App;
```

> **Accessibility note:** For icon-only FABs, also consider setting `aria-label` for screen reader users. The `title` attribute provides a tooltip but is not reliably announced by all screen readers.
