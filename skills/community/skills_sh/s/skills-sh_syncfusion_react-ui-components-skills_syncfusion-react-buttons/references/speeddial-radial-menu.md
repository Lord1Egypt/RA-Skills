# Radial Menu – Syncfusion React Speed Dial

## Table of Contents
- [Overview](#overview)
- [Enable Radial Mode](#enable-radial-mode)
- [Radial Direction](#radial-direction)
- [Start and End Angle](#start-and-end-angle)
- [Offset](#offset)
- [Combined Example](#combined-example)

---

## Overview

Radial mode displays action items in a circular arc around the Speed Dial button. Configure the layout using the `radialSettings` property with a `RadialSettingsModel`.

**Import:** `RadialSettingsModel` from `@syncfusion/ej2-react-buttons`

`RadialSettingsModel` fields:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `direction` | `RadialDirection` | `'Auto'` | Clockwise, AntiClockwise, or Auto |
| `startAngle` | `number` | `null` | Start angle in degrees (0–360) |
| `endAngle` | `number` | `null` | End angle in degrees (0–360) |
| `offset` | `string` | — | Distance between items and the button (e.g., `'80px'`) |

---

## Enable Radial Mode

Set `mode='Radial'` on the component:

```tsx
import { SpeedDialComponent, SpeedDialItemModel } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  const items: SpeedDialItemModel[] = [
    { iconCss: 'e-icons e-cut' },
    { iconCss: 'e-icons e-copy' },
    { iconCss: 'e-icons e-paste' },
    { iconCss: 'e-icons e-edit' },
    { iconCss: 'e-icons e-save' }
  ];

  return (
    <div>
      <div id="targetElement" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      <SpeedDialComponent id='speeddial' openIconCss='e-icons e-edit' closeIconCss='e-icons e-close'
        items={items} mode='Radial' target="#targetElement" />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

---

## Radial Direction

Control the rotation direction of items using `radialSettings.direction`:

- `'Clockwise'` — Items arc clockwise around the button
- `'AntiClockwise'` — Items arc counter-clockwise
- `'Auto'` — Automatically determined by the component's `position` (default)

```tsx
import { SpeedDialComponent, SpeedDialItemModel, RadialSettingsModel } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  const items: SpeedDialItemModel[] = [
    { iconCss: 'e-icons e-cut' },
    { iconCss: 'e-icons e-copy' },
    { iconCss: 'e-icons e-paste' },
    { iconCss: 'e-icons e-edit' },
    { iconCss: 'e-icons e-save' }
  ];
  const radialSettings: RadialSettingsModel = { direction: 'AntiClockwise' };

  return (
    <SpeedDialComponent id='speeddial' openIconCss='e-icons e-edit' closeIconCss='e-icons e-close'
      items={items} mode='Radial' radialSettings={radialSettings} target="#targetElement" />
  );
}
export default App;
```

---

## Start and End Angle

Define a custom arc span for items using `startAngle` and `endAngle` (degrees, 0–360). When both are unset (`null`), items distribute automatically based on the button's `position`.

```tsx
import { SpeedDialComponent, SpeedDialItemModel, RadialSettingsModel } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  const items: SpeedDialItemModel[] = [
    { iconCss: 'e-icons e-cut' },
    { iconCss: 'e-icons e-copy' },
    { iconCss: 'e-icons e-paste' },
    { iconCss: 'e-icons e-edit' },
    { iconCss: 'e-icons e-save' }
  ];
  const radialSettings: RadialSettingsModel = { direction: 'AntiClockwise', startAngle: 180, endAngle: 360 };

  return (
    <div>
      <div id="targetElement" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      <SpeedDialComponent id='speeddial' openIconCss='e-icons e-edit' closeIconCss='e-icons e-close'
        items={items} mode='Radial' radialSettings={radialSettings} position='MiddleCenter' target="#targetElement" />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

---

## Offset

The `offset` property sets the distance between action items and the Speed Dial button. Use CSS length values like `'80px'`:

```tsx
import { SpeedDialComponent, SpeedDialItemModel, RadialSettingsModel } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  const items: SpeedDialItemModel[] = [
    { iconCss: 'e-icons e-cut' },
    { iconCss: 'e-icons e-copy' },
    { iconCss: 'e-icons e-paste' },
    { iconCss: 'e-icons e-edit' },
    { iconCss: 'e-icons e-save' }
  ];
  const radialSettings: RadialSettingsModel = { offset: '80px' };

  return (
    <SpeedDialComponent id='speeddial' openIconCss='e-icons e-edit' closeIconCss='e-icons e-close'
      items={items} mode='Radial' radialSettings={radialSettings} target="#targetElement" />
  );
}
export default App;
```

---

## Combined Example

Full radial configuration with direction, angles, and offset:

```tsx
import { SpeedDialComponent, SpeedDialItemModel, RadialSettingsModel } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  const items: SpeedDialItemModel[] = [
    { iconCss: 'e-icons e-cut' },
    { iconCss: 'e-icons e-copy' },
    { iconCss: 'e-icons e-paste' },
    { iconCss: 'e-icons e-edit' },
    { iconCss: 'e-icons e-save' }
  ];
  const radialSettings: RadialSettingsModel = {
    offset: '80px',
    direction: 'AntiClockwise',
    startAngle: 90,
    endAngle: 270
  };

  return (
    <div>
      <div id="targetElement" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      <SpeedDialComponent id='speeddial' openIconCss='e-icons e-edit' closeIconCss='e-icons e-close'
        items={items} mode='Radial' position='MiddleRight' radialSettings={radialSettings} target="#targetElement" />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```
