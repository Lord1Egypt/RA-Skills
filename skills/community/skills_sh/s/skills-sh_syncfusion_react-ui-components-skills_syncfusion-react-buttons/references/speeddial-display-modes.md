# Display Modes – Syncfusion React Speed Dial

## Table of Contents
- [Overview](#overview)
- [Linear Mode (Default)](#linear-mode-default)
- [Linear Direction](#linear-direction)
- [Radial Mode](#radial-mode)

---

## Overview

The `mode` property controls how action items are laid out when the Speed Dial opens:

| Mode | Description |
|------|-------------|
| `Linear` | Items displayed in a straight line (default) |
| `Radial` | Items displayed in a circular/arc pattern |

Choose `Linear` for standard action lists; choose `Radial` for visually distinctive circular menus.

---

## Linear Mode (Default)

Items appear in a single straight line. No additional configuration needed since `Linear` is the default:

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
        items={items} mode='Linear' target="#targetElement" />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

---

## Linear Direction

The `direction` property controls which direction items extend from the button:

| Value | Behavior |
|-------|----------|
| `Up` | Items extend upward |
| `Down` | Items extend downward |
| `Left` | Items extend leftward |
| `Right` | Items extend rightward |
| `Auto` | Automatically chosen based on `position` (default) |

`Auto` prevents items from overflowing off-screen. For example, if the button is at `BottomRight`, items display upward.

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
        items={items} mode='Linear' direction='Left' target="#targetElement" />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

---

## Radial Mode

Set `mode='Radial'` to arrange items in a circular arc around the button. Customize the layout with `radialSettings`.

For full radial configuration (angles, offset, direction), see [radial-menu.md](radial-menu.md).

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
      <SpeedDialComponent id='speeddial' openIconCss='e-icons e-edit' items={items}
        mode='Radial' target="#targetElement" />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```
