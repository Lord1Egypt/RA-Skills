# Timeline and Zooming in Syncfusion React Gantt Chart

## Table of Contents
- [Timeline View Modes](#timeline-view-modes)
- [Top Tier and Bottom Tier Configuration](#top-tier-and-bottom-tier-configuration)
- [Combining Timeline Cells](#combining-timeline-cells)
- [Custom Timeline Cell Formatting](#custom-timeline-cell-formatting)
- [Timeline View Dates](#timeline-view-dates)
- [Week Start Day](#week-start-day)
- [Automatic Timescale Update](#automatic-timescale-update)
- [Dynamic Timeline Mode Change](#dynamic-timeline-mode-change)
- [Timeline Cell Tooltip](#timeline-cell-tooltip)
- [Timeline Template](#timeline-template)
- [Timeline Navigation](#timeline-navigation)
- [Zooming](#zooming)
- [Customizing Zooming Levels](#customizing-zooming-levels)
- [Programmatic Zoom Methods](#programmatic-zoom-methods)
- [Timeline Cell Width](#timeline-cell-width)
- [Weekend Highlighting](#weekend-highlighting)

---

## Timeline View Modes

Use `timelineSettings.timelineViewMode` to set overall timeline granularity. When `topTier` and `bottomTier` are both configured, `timelineViewMode` is ignored.

| Mode | Top Tier | Bottom Tier | Best For |
|---|---|---|---|
| `"Minutes"` | Hour | Minutes | Minute-level precision |
| `"Hour"` | Day | Hour | Very short tasks |
| `"Day"` | Week | Day | Day-level planning |
| `"Week"` | Month | Week | Short-to-medium projects |
| `"Month"` | Year | Month | Medium-term planning |
| `"Year"` | Year | Month | Long-range roadmaps |

```tsx
import { TimelineSettingsModel } from '@syncfusion/ej2-gantt';

const timelineSettings: TimelineSettingsModel = { timelineViewMode: 'Week' };

<GanttComponent dataSource={data} taskFields={taskFields} timelineSettings={timelineSettings} height="450px" />
```

---

## Top Tier and Bottom Tier Configuration

Configure each tier independently for full control. Available units: `Month`, `Year`, `Week`, `Day`, `Hour`, `Minutes`.

```tsx
const timelineSettings: TimelineSettingsModel = {
  topTier:    { unit: 'Month', format: 'MMM yyyy', count: 1 },
  bottomTier: { unit: 'Week',  format: 'dd MMM',   count: 1 },
};
```

**Day-Hour example:**
```tsx
const timelineSettings: TimelineSettingsModel = {
  topTier:    { unit: 'Day',  format: 'EEE dd MMM' },
  bottomTier: { unit: 'Hour', format: 'hh a', count: 2 }, // every 2 hours
};
```

---

## Combining Timeline Cells

Use the `count` property on `topTier` and `bottomTier` to merge multiple time units into a single cell:

```tsx
const timelineSettings: TimelineSettingsModel = {
  timelineUnitSize: 100,
  topTier: { unit: 'Year' },
  bottomTier: { unit: 'Month', count: 6 },  // groups 6 months into one cell
};
```

- `topTier.count` — number of top-tier units per cell
- `bottomTier.count` — number of bottom-tier units per cell (e.g. `count: 2` shows every 2 hours/days/weeks)

---

## Custom Timeline Cell Formatting

Use `.format` for date format strings, or `.formatter` for full programmatic control.

**Formatter parameters:** `(date: Date, format: string, tier: string, mode: string)`

| Parameter | Description |
|---|---|
| `date` | Date value of the cell |
| `format` | Date format string for the cell |
| `tier` | `'topTier'` or `'bottomTier'` |
| `mode` | Rendering mode: `'Year'`, `'Month'`, `'Week'`, or `'Day'` |

```tsx
// Quarter-label example using all 4 parameters:
const timelineSettings: TimelineSettingsModel = {
  topTier: {
    unit: 'Month', count: 3,
    formatter: (date: Date, format: string, tier: string, mode: string) => {
      const quarter = 'Q' + (Math.floor(date.getMonth() / 3) + 1);
      return (tier === 'topTier' ? 'T-' : 'B-') + quarter + (mode === 'Month' ? '-M' : '');
    },
  },
  bottomTier: { unit: 'Month', format: 'MMM' },
};

// Simple week-number example:
topTier: {
  unit: 'Week',
  formatter: (date: Date) => `Week ${getWeekNumber(date)}`,
},
```

---

## Timeline View Dates

Use `viewStartDate` / `viewEndDate` in `timelineSettings` to lock the *visible* range independently from the project's scheduling boundaries.

```tsx
const timelineSettings: TimelineSettingsModel = {
  viewStartDate: new Date('04/03/2024'),
  viewEndDate:   new Date('04/30/2024'),
};

<GanttComponent
  timelineSettings={timelineSettings}
  projectStartDate={new Date('03/31/2024')} // scheduling boundary (baseline, critical path, ZoomToFit)
  projectEndDate={new Date('05/13/2024')}
/>
```

| Property | Default | When `auto` |
|---|---|---|
| `viewStartDate` | auto | Uses `projectStartDate` if set, else earliest task start |
| `viewEndDate` | auto | Uses `projectEndDate` if set, else max task end (auto-extended to fill chart) |

> `ZoomToFit` uses `projectStartDate` / `projectEndDate`, not `viewStartDate` / `viewEndDate`.

---

## Week Start Day

Set the first day of the week (0=Sunday default … 6=Saturday). Only applies when timeline shows weeks.

```tsx
const timelineSettings: TimelineSettingsModel = { timelineViewMode: 'Week', weekStartDay: 1 }; // Monday
```

> Also applies when `topTier.unit = 'Week'` and `bottomTier.unit = 'Day'`.

---

## Automatic Timescale Update

By default the timeline auto-extends when tasks are edited beyond the project range. Disable with `updateTimescaleView: false`.

```tsx
const timelineSettings: TimelineSettingsModel = { updateTimescaleView: false };

<GanttComponent timelineSettings={timelineSettings} editSettings={{ allowEditing: true, allowTaskbarEditing: true }}>
  <Inject services={[Edit]} />
</GanttComponent>
```

---

## Dynamic Timeline Mode Change

Update `timelineViewMode` at runtime and call `refresh()`:

```tsx
const ganttRef = React.useRef<GanttComponent>(null);

const changeMode = (mode: string) => {
  (ganttRef.current as any).timelineSettings.timelineViewMode = mode;
  ganttRef.current?.refresh();
};

<GanttComponent ref={ganttRef} ... />
<button onClick={() => changeMode('Month')}>Month View</button>
```

---

## Timeline Cell Tooltip

Show/hide the hover tooltip on timeline cells (default: `true`):

```tsx
const timelineSettings: TimelineSettingsModel = { showTooltip: true };
```

---

## Timeline Template

Customize HTML inside timeline cells using `timelineTemplate`. Context: `{ date, value, tier }`.

| Context Prop | Description |
|---|---|
| `date` | Date value of the cell |
| `value` | Formatted date string to display |
| `tier` | `'topTier'` or `'bottomTier'` |

```tsx
const timelineTemplate = (props: any) => {
  if (props.tier === 'topTier')
    return <div style={{ backgroundColor: '#FBF9F1', fontWeight: 'bold', textAlign: 'center' }}>{props.value}</div>;
  const isWeekend = props.value === 'S';
  return <div style={{ backgroundColor: isWeekend ? '#7BD3EA' : '#E0FBE2', textAlign: 'center' }}>{props.value}</div>;
};

<GanttComponent
  timelineTemplate={timelineTemplate}
  timelineSettings={{ topTier: { unit: 'Week', format: 'dd/MM/yyyy' }, bottomTier: { unit: 'Day', count: 1 }, timelineUnitSize: 100 }}
>
  <Inject services={[DayMarkers]} />
</GanttComponent>
```

---

## Timeline Navigation

Shift the visible timeline range by one unit forward or backward:

```tsx
const ganttRef = React.useRef<GanttComponent>(null);

ganttRef.current?.previousTimeSpan(); // move backward (one week/month depending on view mode)
ganttRef.current?.nextTimeSpan();     // move forward
```

---

## Zooming

Add `ZoomIn`, `ZoomOut`, `ZoomToFit` toolbar items:

```tsx
<GanttComponent toolbar={['ZoomIn', 'ZoomOut', 'ZoomToFit']} ...>
  <Inject services={[Toolbar]} />
</GanttComponent>
```

| Action | Behavior |
|---|---|
| **ZoomIn** | Increases cell width; shifts unit years → months → weeks → days → hours → minutes |
| **ZoomOut** | Decreases cell width; shifts unit minutes → hours → days → weeks → months → years |
| **ZoomToFit** | Fits all project tasks within the visible chart width |

---

## Customizing Zooming Levels

Override the default zoom level progression using the `zoomingLevels` property. Assign an array of `ZoomTimelineSettings` to control how each zoom step looks:

```tsx
import { ZoomTimelineSettings } from '@syncfusion/ej2-gantt';

const customZoomingLevels: ZoomTimelineSettings[] = [
  {
    topTier: { unit: 'Month', format: 'MMM, yy', count: 1 },
    bottomTier: { unit: 'Week', format: 'dd', count: 1 },
    timelineUnitSize: 33, level: 0, timelineViewMode: 'Month',
    weekStartDay: 0, updateTimescaleView: true, showTooltip: true
  },
  {
    topTier: { unit: 'Month', format: 'MMM, yyyy', count: 1 },
    bottomTier: { unit: 'Week', format: 'dd MMM', count: 1 },
    timelineUnitSize: 99, level: 2, timelineViewMode: 'Month',
    weekStartDay: 0, updateTimescaleView: true, showTooltip: true
  },
  {
    topTier: { unit: 'Week', format: 'MMM dd, yyyy', count: 1 },
    bottomTier: { unit: 'Day', format: 'd', count: 1 },
    timelineUnitSize: 33, level: 3, timelineViewMode: 'Week',
    weekStartDay: 0, updateTimescaleView: true, showTooltip: true
  },
  {
    topTier: { unit: 'Day', format: 'E dd yyyy', count: 1 },
    bottomTier: { unit: 'Hour', format: 'hh a', count: 6 },
    timelineUnitSize: 99, level: 6, timelineViewMode: 'Day',
    weekStartDay: 0, updateTimescaleView: true, showTooltip: true
  }
];

// Apply via dataBound (after Gantt initializes):
const ganttRef = React.useRef<GanttComponent>(null);

const onDataBound = () => {
  if (ganttRef.current) {
    ganttRef.current.zoomingLevels = customZoomingLevels;
  }
};

<GanttComponent
  ref={ganttRef}
  toolbar={['ZoomIn', 'ZoomOut', 'ZoomToFit']}
  dataBound={onDataBound}
  ...
/>
```

**`ZoomTimelineSettings` properties:**

| Property | Description |
|---|---|
| `level` | Zero-based index for this zoom level |
| `topTier` | Top tier unit, format, and count |
| `bottomTier` | Bottom tier unit, format, and count |
| `timelineUnitSize` | Cell width in pixels for this level |
| `timelineViewMode` | View mode string for this level |
| `weekStartDay` | Day of week to start (0=Sunday) |
| `updateTimescaleView` | Auto-expand timeline on task edits |
| `showTooltip` | Show cell tooltip for this level |

---

## Programmatic Zoom Methods

Control zoom via a component reference:

```tsx
import { GanttComponent } from '@syncfusion/ej2-react-gantt';
import * as React from 'react';

const ganttRef = React.useRef<GanttComponent>(null);

const zoomIn     = () => ganttRef.current?.zoomIn();
const zoomOut    = () => ganttRef.current?.zoomOut();
const fitProject = () => ganttRef.current?.fitToProject();

function App() {
  return (
    <>
      <button onClick={zoomIn}>Zoom In</button>
      <button onClick={zoomOut}>Zoom Out</button>
      <button onClick={fitProject}>Fit to Project</button>
      <GanttComponent ref={ganttRef} dataSource={data} taskFields={taskFields} height="450px" />
    </>
  );
}
```

---

## Timeline Cell Width

Set the initial width of each timeline cell:

```tsx
const timelineSettings: TimelineSettingsModel = {
  timelineUnitSize: 99,   // pixel width per cell (default: 33)
};
```

Useful when you want to pre-size the chart to show a specific number of units without user zooming.

---

## Weekend Highlighting

There are two distinct ways to handle weekends in the timeline:

### 1. Highlight Weekends (shade with color)

```tsx
<GanttComponent
  highlightWeekends={true}  // shades Sat/Sun columns in the chart area
  ...
/>
```

Applies a background color to weekend columns. Works in all view modes.

### 2. Hide Weekends (remove from timeline)

Use `timelineSettings.showWeekend` to hide weekend columns entirely from the timeline:

```tsx
const timelineSettings: TimelineSettingsModel = {
  showWeekend: false,  // removes Sat/Sun columns from the timeline
};

<GanttComponent
  timelineSettings={timelineSettings}
  workWeek={['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']}
  ...
/>
```

**`showWeekend: false` Limitations:**
- Not compatible with baselines
- Not compatible with manual task mode
- Non-working hours cannot be excluded
- Holidays are not excluded from the timeline when weekends are hidden
