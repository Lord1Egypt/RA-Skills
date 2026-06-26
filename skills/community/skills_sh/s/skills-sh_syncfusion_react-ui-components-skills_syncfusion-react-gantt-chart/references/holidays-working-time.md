# Holidays, Working Time & Timezone

## Table of Contents
- [Holidays](#holidays)
- [Work Week Configuration](#work-week-configuration)
- [Include Weekends in Scheduling](#include-weekends-in-scheduling)
- [Working Time (Daily Hours)](#working-time-daily-hours)
- [Work (Effort-Based Scheduling)](#work-effort-based-scheduling)
- [Timezone](#timezone)
- [Common Pitfalls](#common-pitfalls)

---

## Holidays

Define non-working days that affect task scheduling, durations, and dependency calculations. Requires the `DayMarkers` service injection.

```tsx
import { GanttComponent, Inject, DayMarkers } from '@syncfusion/ej2-react-gantt';

const holidays = [
  // Single-day holiday
  { from: new Date('2024-12-25'), label: 'Christmas Day', cssClass: 'national-holiday' },
  // Multi-day holiday range
  { from: new Date('2024-12-26'), to: new Date('2024-12-27'), label: 'Christmas Break', cssClass: 'company-holiday' },
  // Minimal — label only
  { from: new Date('2025-01-01'), label: 'New Year' },
];

function App() {
  return (
    <GanttComponent
      dataSource={data}
      taskFields={taskFields}
      holidays={holidays}
      height='450px'
    >
      <Inject services={[DayMarkers]} />
    </GanttComponent>
  );
}
```

### Holiday Object Properties

| Property | Type | Required | Description |
|---|---|---|---|
| `from` | Date | ✅ | Start date of the holiday |
| `to` | Date | ❌ | End date (omit for single-day) |
| `label` | string | ❌ | Text shown in the timeline cell |
| `cssClass` | string | ❌ | CSS class applied to the holiday cell |

### Effects on Scheduling

- Task durations exclude holidays — end dates are automatically extended
- Successor tasks shift forward to preserve dependency relationships
- Critical path slack calculations account for holidays
- Resources are treated as unavailable during holiday periods

### Custom Holiday Styling

```css
/* Style the label inside the holiday span */
.national-holiday .e-span-label {
  color: #C0392B;
  font-weight: bold;
}
.company-holiday .e-span-label {
  color: #2980B9;
}
```

---

## Work Week Configuration

Define which days of the week are treated as working days. The default is Monday through Friday.

```tsx
<GanttComponent
  workWeek={['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']}
  dataSource={data}
  taskFields={taskFields}
  height='450px'
/>
```

**Valid day values:** `'Sunday'`, `'Monday'`, `'Tuesday'`, `'Wednesday'`, `'Thursday'`, `'Friday'`, `'Saturday'`

### Example — 6-Day Work Week (Mon–Sat)

```tsx
<GanttComponent
  workWeek={['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']}
  ...
/>
```

---

## Include Weekends in Scheduling

Set `includeWeekend={true}` to treat Saturday and Sunday as working days for task scheduling and duration calculation:

```tsx
<GanttComponent
  includeWeekend={true}
  dataSource={data}
  taskFields={taskFields}
  height='450px'
/>
```

> When `includeWeekend={true}`, weekend days count toward task duration and dependencies shift accordingly.

---

## Working Time (Daily Hours)

Define the daily working hours used for hour-level scheduling and effort calculations:

```tsx
<GanttComponent
  dayWorkingTime={[
    { from: 8, to: 12 },   // 8:00 AM – 12:00 PM
    { from: 13, to: 17 },  // 1:00 PM – 5:00 PM (excludes lunch break)
  ]}
  dataSource={data}
  taskFields={taskFields}
  height='450px'
/>
```

> `from` and `to` are hours in 24-hour format. Default is `[{ from: 8, to: 17 }]` (8 AM to 5 PM).

---

## Work (Effort-Based Scheduling)

Map a `work` field on tasks to enable effort-based scheduling. Work represents the total effort required (in `workUnit`), and duration is calculated based on resource availability.

```tsx
const taskFields = {
  id: 'TaskID',
  name: 'TaskName',
  startDate: 'StartDate',
  duration: 'Duration',
  progress: 'Progress',
  resourceInfo: 'resources',
  work: 'Work',          // total effort field
  parentID: 'ParentID',
};

// workUnit: 'Hour' (default) | 'Day' | 'Minute'
<GanttComponent
  taskFields={taskFields}
  workUnit='Hour'
  dataSource={data}
  height='450px'
>
  <Inject services={[Edit]} />
</GanttComponent>
```

> Mapping `taskFields.work` sets the default task type to **FixedWork** — work hours stay constant when resources or duration change.

### Task Types

| Type | Behavior |
|---|---|
| `FixedWork` | Work stays constant; duration adjusts with resource unit changes |
| `FixedDuration` | Duration stays fixed; work adjusts with resource unit changes |
| `FixedUnit` | Resource units stay constant; duration or work adjusts |

### Data Source Example

```tsx
const data = [
  {
    TaskID: 1,
    TaskName: 'Development',
    StartDate: new Date('04/02/2024'),
    Duration: 5,
    Work: 40,           // 40 hours of effort
    resources: [{ resourceId: 1, unit: 100 }],
    ParentID: null,
  },
];
```

---

## Timezone

Set an IANA timezone string on the Gantt to ensure consistent date display across users in different regions.

```tsx
<GanttComponent
  timezone='UTC'
  timelineSettings={{
    topTier: { unit: 'Day' },
    bottomTier: { unit: 'Hour' },
  }}
  dataSource={data}
  taskFields={taskFields}
  height='450px'
/>
```

> The `timezone` prop has visible effect only when the timeline renders **hours**. Use `timelineViewMode='Hour'` or configure an hourly bottom tier.

### Common Timezone Values

| Value | Description |
|---|---|
| `'UTC'` | Coordinated Universal Time |
| `'America/New_York'` | US Eastern Time |
| `'America/Los_Angeles'` | US Pacific Time |
| `'Europe/London'` | UK Time |
| `'Asia/Kolkata'` | India Standard Time |
| `'Asia/Tokyo'` | Japan Standard Time |

---

## Common Pitfalls

| Issue | Cause | Fix |
|---|---|---|
| Holidays not rendering | `DayMarkers` service not injected | Add `<Inject services={[DayMarkers]} />` |
| Holiday styling not applied | Wrong CSS selector | Target `.{cssClass} .e-span-label` for label text styling |
| Weekend days still blocked | `includeWeekend` not set | Set `includeWeekend={true}` |
| Work field has no effect | `taskFields.work` not mapped | Add `work: 'Work'` to `taskFields` |
| Timezone has no visible effect | Timeline not showing hours | Set `timelineViewMode='Hour'` or configure hourly bottom tier |
| Duration calculation wrong | `dayWorkingTime` not set | Configure `dayWorkingTime` to match actual working hours |
