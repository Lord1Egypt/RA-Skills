# Items – Syncfusion React Speed Dial

## Table of Contents
- [SpeedDialItemModel Fields](#speeddialitemmodel-fields)
- [Icon Only](#icon-only)
- [Text Only](#text-only)
- [Icon with Text](#icon-with-text)
- [Disabled Items](#disabled-items)
- [Item Tooltip](#item-tooltip)
- [Animation](#animation)

---

## SpeedDialItemModel Fields

Each item in the `items` array is a `SpeedDialItemModel` with these fields:

| Field | Type | Description |
|-------|------|-------------|
| `text` | `string` | Text label displayed in the item |
| `iconCss` | `string` | CSS class(es) for the item icon |
| `id` | `string` | Unique identifier, available in event args |
| `title` | `string` | Tooltip text shown on hover |
| `disabled` | `boolean` | Disables the item when `true` |

---

## Icon Only

Use `iconCss` alone for compact icon-only items. Add `title` for hover tooltips since no text is visible:

```tsx
import { SpeedDialComponent, SpeedDialItemModel } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  const items: SpeedDialItemModel[] = [
    { iconCss: 'e-icons e-cut' },
    { iconCss: 'e-icons e-copy' },
    { iconCss: 'e-icons e-paste' }
  ];

  return (
    <div>
      <div id="targetElement" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      <SpeedDialComponent id='speeddial' openIconCss='e-icons e-edit' closeIconCss='e-icons e-close'
        items={items} target="#targetElement" />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

---

## Text Only

Use `text` alone when a purely label-based menu fits the design:

```tsx
import { SpeedDialComponent, SpeedDialItemModel } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  const items: SpeedDialItemModel[] = [
    { text: 'Cut' },
    { text: 'Copy' },
    { text: 'Paste' }
  ];

  return (
    <div>
      <div id="targetElement" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      <SpeedDialComponent id='speeddial' content='Edit' items={items} target="#targetElement" />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

---

## Icon with Text

Combine `iconCss` and `text` for items that display both visual and textual information:

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
      <SpeedDialComponent id='speeddial' openIconCss='e-icons e-edit' closeIconCss='e-icons e-close'
        content='Edit' items={items} target="#targetElement" />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

---

## Disabled Items

Set `disabled: true` on individual items to make them non-interactive. Disabled items appear grayed out:

```tsx
import { SpeedDialComponent, SpeedDialItemModel } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  const items: SpeedDialItemModel[] = [
    { text: 'Cut', disabled: true },   // grayed out, unclickable
    { text: 'Copy' },
    { text: 'Paste' }
  ];

  return (
    <div>
      <div id="targetElement" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      <SpeedDialComponent id='speeddial' content='Edit' items={items} target="#targetElement" />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

---

## Item Tooltip

Use the `title` field on items to show a tooltip on hover. This is especially useful for icon-only items:

```tsx
const items: SpeedDialItemModel[] = [
  { iconCss: 'e-icons e-cut', title: 'Cut' },
  { iconCss: 'e-icons e-copy', title: 'Copy' },
  { iconCss: 'e-icons e-paste', title: 'Paste' }
];
```

---

## Animation

Control item animation with the `animation` property. By default, items use a `Fade` effect. Use `SpeedDialAnimationSettingsModel` to customize `effect`, `duration`, and `delay`:

```tsx
import { SpeedDialComponent, SpeedDialItemModel, SpeedDialAnimationSettingsModel } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  const items: SpeedDialItemModel[] = [
    { text: 'Cut', iconCss: 'e-icons e-cut' },
    { text: 'Copy', iconCss: 'e-icons e-copy' },
    { text: 'Paste', iconCss: 'e-icons e-paste' }
  ];
  const animation: SpeedDialAnimationSettingsModel = { effect: 'Zoom' };

  return (
    <div>
      <div id="targetElement" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      <SpeedDialComponent id='speeddial' openIconCss='e-icons e-edit' closeIconCss='e-icons e-close'
        content='Edit' items={items} animation={animation} target="#targetElement" />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

**Animation defaults:** `{ effect: 'Fade', duration: 400, delay: 0 }`

Use `effect: 'None'` to disable animation entirely.
