# Splitter in Syncfusion React Gantt Chart

## Table of Contents
- [Overview](#overview)
- [Position-Based Split](#position-based-split)
- [Column-Based Split](#column-based-split)
- [View Mode](#view-mode)
- [Programmatic Resize](#programmatic-resize)
- [Splitter Events](#splitter-events)
- [Common Pitfalls](#common-pitfalls)

---

## Overview

The Gantt component is divided into two panels — the **TreeGrid** (left, shows task columns) and the **Chart** (right, shows taskbars on a timeline). The splitter controls the width ratio between these two panels.

Configure the splitter via `splitterSettings`:

```tsx
import { GanttComponent } from '@syncfusion/ej2-react-gantt';
import { SplitterSettingsModel } from '@syncfusion/ej2-react-gantt';

<GanttComponent
  splitterSettings={splitterSettings}
  dataSource={data}
  taskFields={taskFields}
  height='450px'
/>
```

---

## Position-Based Split

Set the splitter position as a percentage or pixel value:

```tsx
// 50% width to TreeGrid, 50% to Chart
const splitterSettings: SplitterSettingsModel = {
  position: '50%',
};

// Fixed 300px width to TreeGrid
const splitterSettings: SplitterSettingsModel = {
  position: '300px',
};
```

---

## Column-Based Split

Align the splitter to the right edge of a specific column by index:

```tsx
// Splitter placed at the right edge of the 3rd column (index 2)
const splitterSettings: SplitterSettingsModel = {
  columnIndex: 2,
};
```

> Column indices are 0-based. The splitter snaps to the right edge of the specified column.

---

## View Mode

Control which panel is visible using `view`:

```tsx
// Show both panels (default)
const splitterSettings: SplitterSettingsModel = { view: 'Default' };

// Show only the TreeGrid (hide chart)
const splitterSettings: SplitterSettingsModel = { view: 'Grid' };

// Show only the Chart (hide TreeGrid)
const splitterSettings: SplitterSettingsModel = { view: 'Chart' };
```

| Value | Description |
|---|---|
| `'Default'` | Both TreeGrid and Chart visible |
| `'Grid'` | Only TreeGrid (left panel) visible |
| `'Chart'` | Only Chart (right panel) visible |

---

## Programmatic Resize

Use `setSplitterPosition()` to change the splitter position at runtime:

```tsx
import React, { useRef } from 'react';
import { GanttComponent } from '@syncfusion/ej2-react-gantt';

const ganttRef = useRef<GanttComponent>(null);

// Set as percentage
ganttRef.current?.setSplitterPosition('40%', 'percentage');

// Set as fixed pixel value
ganttRef.current?.setSplitterPosition(300, 'position');
```

### `setSplitterPosition` Signature

```tsx
setSplitterPosition(value: string | number, type: 'percentage' | 'position'): void
```

| Parameter | Type | Description |
|---|---|---|
| `value` | string \| number | The splitter position value |
| `type` | `'percentage'` \| `'position'` | Interpret value as `%` or `px` |

---

## Splitter Events

Three events fire when the user drags the splitter:

| Event | Trigger |
|---|---|
| `splitterResizeStart` | User starts dragging the splitter |
| `splitterResizing` | Fires continuously while dragging |
| `splitterResized` | User releases the splitter |

```tsx
function App() {
  const splitterResizeStart = (args: any) => {
    console.log('Resize started');
  };

  const splitterResizing = (args: any) => {
    console.log('Resizing — current width:', args.newWidth);
  };

  const splitterResized = (args: any) => {
    console.log('Resize complete — new width:', args.newWidth);
  };

  return (
    <GanttComponent
      splitterResizeStart={splitterResizeStart}
      splitterResizing={splitterResizing}
      splitterResized={splitterResized}
      dataSource={data}
      taskFields={taskFields}
      height='450px'
    />
  );
}
```

---

## Common Pitfalls

| Issue | Cause | Fix |
|---|---|---|
| Chart not visible | `view: 'Grid'` set unintentionally | Change `view` to `'Default'` |
| Splitter position ignored | Both `position` and `columnIndex` set | Use only one — `columnIndex` takes priority over `position` |
| `setSplitterPosition` has no effect | Called before component is mounted | Call inside `created` event or after `dataBound` |
