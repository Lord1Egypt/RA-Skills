# Scrolling in Syncfusion React Gantt Chart

## Table of Contents
- [Setting Width and Height](#setting-width-and-height)
- [Responsive Container](#responsive-container)
- [Scroll to a Specific Date](#scroll-to-a-specific-date)
- [Set Vertical Scroll Position](#set-vertical-scroll-position)
- [Common Pitfalls](#common-pitfalls)

---

## Setting Width and Height

Set fixed pixel dimensions on `GanttComponent` to control when scrollbars appear:

```tsx
<GanttComponent
  dataSource={data}
  taskFields={taskFields}
  width='800px'
  height='450px'
/>
```

- **Vertical scrollbar** appears when total row height exceeds the component `height`
- **Horizontal scrollbar** appears when column widths exceed the grid panel width, or when the chart timeline is wider than the chart panel width
- Default for both `width` and `height` is `'auto'`

---

## Responsive Container

Use `'100%'` to make the Gantt fill its parent container and respond to resize:

```tsx
<GanttComponent
  dataSource={data}
  taskFields={taskFields}
  width='100%'
  height='100%'
/>
```

> The parent element **must have an explicit CSS height** for `height='100%'` to work. Without it, the Gantt collapses to zero height.

```css
/* Parent container must define a height */
.gantt-wrapper {
  height: 500px;
  width: 100%;
}
```

---

## Scroll to a Specific Date

Use `scrollToDate()` to programmatically scroll the chart timeline horizontally to a given date:

```tsx
import React, { useRef } from 'react';
import { GanttComponent } from '@syncfusion/ej2-react-gantt';

function App() {
  const ganttRef = useRef<GanttComponent>(null);

  const scrollToDate = () => {
    ganttRef.current?.scrollToDate('04/28/2024');
  };

  return (
    <>
      <button onClick={scrollToDate}>Go to Apr 28</button>
      <GanttComponent
        ref={ganttRef}
        dataSource={data}
        taskFields={taskFields}
        height='450px'
      />
    </>
  );
}
```

**`scrollToDate` signature:**
```tsx
scrollToDate(date: string): void
// date format: 'MM/dd/yyyy'
```

---

## Set Vertical Scroll Position

Use `setScrollTop()` to programmatically jump to a vertical offset (in pixels) in the row area:

```tsx
import React, { useRef } from 'react';
import { GanttComponent } from '@syncfusion/ej2-react-gantt';

function App() {
  const ganttRef = useRef<GanttComponent>(null);

  const scrollDown = () => {
    (ganttRef.current as any).ganttChartModule.scrollObject.setScrollTop(300);
  };

  return (
    <>
      <button onClick={scrollDown}>Scroll Down 300px</button>
      <GanttComponent
        ref={ganttRef}
        dataSource={data}
        taskFields={taskFields}
        height='450px'
      />
    </>
  );
}
```

> `setScrollTop()` is accessed via the internal `ganttChartModule.scrollObject` — cast the ref to `any` when calling it in TypeScript.

---

## Common Pitfalls

| Issue | Cause | Fix |
|---|---|---|
| No scrollbar appearing | `height` set to `'auto'` | Set a fixed pixel height e.g. `height='450px'` |
| `height='100%'` not working | Parent has no CSS height | Add explicit `height` to the parent container |
| `scrollToDate` has no effect | Date format mismatch | Use `'MM/dd/yyyy'` format string |
| Vertical scroll jumps back | Virtual scroll re-renders rows | Scroll after render completes in `dataBound` event |
