# Appointments and Events

## Table of Contents
- [Overview](#overview)
- [Event Types](#event-types)
  - [Normal Events](#normal-events)
  - [Spanned Events](#spanned-events)
  - [All-Day Events](#all-day-events)
  - [Recurring Events](#recurring-events)
- [CRUD Operations](#crud-operations)
  - [Creating Events](#creating-events)
  - [Updating Events](#updating-events)
  - [Deleting Events](#deleting-events)
  - [Drag and Drop](#drag-and-drop)
  - [Resize Events](#resize-events)
- [Event Fields](#event-fields)
  - [Built-in Fields](#built-in-fields)
  - [Custom Fields](#custom-fields)
  - [Field Settings](#field-settings)
- [Event Customization](#event-customization)
  - [Using Templates](#using-templates)
  - [Using Event Rendered Event](#using-event-rendered-event)
  - [Using CSS Class](#using-css-class)
- [Advanced Features](#advanced-features)
  - [Block Dates and Times](#block-dates-and-times)
  - [Readonly Events](#readonly-events)
  - [Event Overlapping](#event-overlapping)
  - [Inline Editing](#inline-editing)
  - [Event Tooltips](#event-tooltips)
- [Troubleshooting and Edge Cases](#troubleshooting-and-edge-cases)

## Overview

Appointments (also known as events) are the core data elements in the Scheduler component. They represent scheduled items for specific time periods and can be created, edited, and deleted through various interfaces including the editor window, drag-and-drop, resize actions, or programmatic methods.

The Scheduler categorizes appointments into four main types: normal events (scheduled for specific time intervals), spanned events (lasting more than 24 hours), all-day events (occupying entire days), and recurring events (repeating on regular intervals).

## Event Types

### Normal Events

Normal events represent appointments created for any specific time interval within a day. These are standard single-occurrence events with defined start and end times.

**Creating a normal event:**

```typescript
const data: object[] = [{
  Id: 1,
  Subject: 'Paris',
  StartTime: new Date(2023, 1, 15, 10, 0),
  EndTime: new Date(2023, 1, 15, 12, 30),
}];
const eventSettings: EventSettingsModel = { dataSource: data };

<ScheduleComponent height='550px' selectedDate={new Date(2023, 1, 15)} eventSettings={eventSettings}>
  <Inject services={[Day, Week, WorkWeek, Month, Agenda]} />
</ScheduleComponent>
```

### Spanned Events

Spanned events are appointments created for durations longer than 24 hours. By default, events spanning more than 24 hours are displayed in the all-day row. However, spanned events can be customized to render in different ways.

**Example:** An appointment from November 25, 2018, 11:00 PM to November 26, 2018, 2:00 AM (less than 24 hours but spanning multiple days) will be split and displayed on both days.

**Customizing spanned event rendering:**

Use the `spannedEventPlacement` property to control how spanned events are rendered:

```typescript
const eventSettings: EventSettingsModel = { 
  dataSource: data, 
  spannedEventPlacement: 'TimeSlot' // Renders in work cells instead of all-day row
};
```

### All-Day Events

All-day events represent appointments created for entire days, such as holidays. They are displayed in a separate all-day row below the date header (except in Timeline views, where they appear in the working space area).

**Setting an all-day event:**

Set the `isAllDay` field to `true`:

```typescript
const data: object[] = [{
  Id: 2,
  Subject: 'Holiday',
  StartTime: new Date(2022, 3, 29, 0, 0),
  EndTime: new Date(2022, 3, 30, 0, 0),
  IsAllDay: true,
}];
```

**Hide all-day row using CSS:**

```css
.e-schedule .e-date-header-wrap .e-schedule-table thead {
  display: none;
}
```

**Expanding all-day appointments on load:**

```typescript
const scheduleRef = useRef<ScheduleComponent>(null);

useEffect(() => {
  const allDaySection = scheduleRef.current.element.querySelector('.e-all-day-appointment-section');
  if (allDaySection) {
    allDaySection.click();
  }
}, []);
```

### Recurring Events

Recurring events are appointments scheduled to repeat at regular intervals (daily, weekly, monthly, or yearly) based on a recurrence rule. They are marked with a repeat indicator.

**Creating a recurring event:**

```typescript
const data: object[] = [{
  Id: 2,
  Subject: 'Daily Meeting',
  StartTime: new Date(2018, 1, 15, 10, 0),
  EndTime: new Date(2018, 1, 15, 12, 30),
  RecurrenceRule: 'FREQ=DAILY;INTERVAL=1;COUNT=5',
}];
```

**Recurrence Rule Properties:**

| Property | Purpose | Example |
|----------|---------|---------|
| FREQ | Repeat type (DAILY, WEEKLY, MONTHLY, YEARLY) | FREQ=DAILY;INTERVAL=1 |
| INTERVAL | Interval value between occurrences | FREQ=DAILY;INTERVAL=2 |
| COUNT | Number of occurrences | FREQ=DAILY;INTERVAL=1;COUNT=10 |
| UNTIL | End date in ISO format | FREQ=DAILY;INTERVAL=1;UNTIL=20180530T041343Z |
| BYDAY | Day(s) of week (MO, TU, WE, TH, FR, SA, SU) | FREQ=WEEKLY;INTERVAL=1;BYDAY=MO,WE |
| BYMONTHDAY | Date of month | FREQ=MONTHLY;BYMONTHDAY=3 |
| BYMONTH | Month index | FREQ=YEARLY;BYMONTHDAY=16;BYMONTH=6 |
| BYSETPOS | Week position in month | FREQ=MONTHLY;BYDAY=MO;BYSETPOS=2 |

**Adding exceptions to recurring events:**

Exclude specific dates using the `recurrenceException` field (ISO format without hyphens):

```typescript
const data: object[] = [{
  Id: 1,
  Subject: 'Meeting',
  StartTime: new Date(2018, 0, 28, 10, 0),
  EndTime: new Date(2018, 0, 28, 12, 30),
  RecurrenceRule: 'FREQ=DAILY;INTERVAL=1;COUNT=8',
  RecurrenceException: '20180129T043000Z,20180131T043000Z,20180202T043000Z'
}];
```

**Editing a single occurrence:**

Add the edited occurrence as a new event with a `recurrenceID` field pointing to the parent event's ID:

```typescript
const data: object[] = [
  {
    Id: 1,
    Subject: 'Scrum Meeting',
    StartTime: new Date(2018, 0, 28, 10, 0),
    EndTime: new Date(2018, 0, 28, 12, 30),
    RecurrenceRule: 'FREQ=DAILY;INTERVAL=1;COUNT=8',
    RecurrenceException: '20180130T043000Z'
  },
  {
    Id: 2,
    Subject: 'Scrum Meeting - Edited',
    StartTime: new Date(2018, 0, 30, 9, 0),
    EndTime: new Date(2018, 0, 30, 10, 30),
    RecurrenceID: 1
  }
];
```

**Editing current and following events:**

Enable `editFollowingEvents` property and use `followingID` field:

```typescript
const eventSettings: EventSettingsModel = { 
  dataSource: data, 
  editFollowingEvents: true 
};

const data: object[] = [
  {
    Id: 1,
    Subject: 'Meeting',
    StartTime: new Date(2018, 0, 28, 10, 0),
    EndTime: new Date(2018, 0, 28, 12, 30),
    RecurrenceRule: 'FREQ=DAILY;INTERVAL=1;UNTIL=20180129T043000Z;',
  },
  {
    Id: 2,
    Subject: 'Meeting - Following Edited',
    StartTime: new Date(2018, 0, 30, 10, 0),
    EndTime: new Date(2018, 0, 30, 12, 30),
    RecurrenceRule: 'FREQ=DAILY;INTERVAL=1;UNTIL=20180204T043000Z;',
    FollowingID: 1
  }
];
```

**Recurrence Validation Messages:**

The Scheduler provides built-in validation for recurring appointments:

| Validation Message | Description |
|-------------------|-------------|
| Pattern is not valid | Selected recurrence rule value is invalid |
| Changes will be cancelled | Editing entire series when occurrences are already edited |
| Duration must be shorter | Event duration is longer than the frequency interval |
| Some months have fewer dates | Creating recurring event on 31st for months without 31 days |
| Two occurrences cannot occur on same day | Moving/editing occurrence to date where another occurrence exists |

## CRUD Operations

### Creating Events

Create events using the editor window or the `addEvent` method programmatically.

**Creation using editor window:**

Double-click on Scheduler cells to open the default editor window with fields for Subject, Location, Start/End time, All-day status, Timezone, Description, and recurrence options. Single-click opens a quick popup for entering just the subject.

**Creation using addEvent method:**

Programmatically add single or multiple events:

```typescript
const scheduleObj = useRef<ScheduleComponent>(null);

const addEvents = (): void => {
  const newEvents: Object[] = [
    {
      Id: 1,
      Subject: 'Conference',
      StartTime: new Date(2018, 1, 12, 9, 0),
      EndTime: new Date(2018, 1, 12, 10, 0),
    },
    {
      Id: 2,
      Subject: 'Meeting',
      StartTime: new Date(2018, 1, 15, 10, 0),
      EndTime: new Date(2018, 1, 15, 11, 30),
    }
  ];
  scheduleObj.current.addEvent(newEvents);
};
```

**Validation and restrictions:**

Apply validation rules to event fields:

```typescript
const fields = {
  subject: { name: 'Subject', validation: { required: true } },
  location: {
    name: 'Location', 
    validation: {
      required: true,
      regex: ["^[a-zA-Z0-9- ]*$", 'Special characters not allowed']
    }
  }
};
const eventSettings: EventSettingsModel = { dataSource: data, fields: fields };
```

**Restrict creation on specific conditions:**

Use the `actionBegin` event to prevent creation on weekends:

```typescript
const onActionBegin = (args: ActionEventArgs): void => {
  const weekends: number[] = [0, 6];
  if (args.requestType === 'eventCreate' && 
      weekends.indexOf(args.data[0].StartTime.getDay()) >= 0) {
    args.cancel = true;
  }
};
```

**Server-side insertion:**

```csharp
if (param.action == "insert" || (param.action == "batch" && param.added != null)) {
  var value = (param.action == "insert") ? param.value : param.added[0];
  int intMax = db.ScheduleEventDatas.ToList().Max(p => p.Id) + 1;
  DateTime startTime = Convert.ToDateTime(value.StartTime);
  DateTime endTime = Convert.ToDateTime(value.EndTime);
  ScheduleEventData appointment = new ScheduleEventData() {
    Id = intMax,
    StartTime = startTime.ToLocalTime(),
    EndTime = endTime.ToLocalTime(),
    Subject = value.Subject,
    IsAllDay = value.IsAllDay,
    RecurrenceRule = value.RecurrenceRule
  };
  db.ScheduleEventDatas.InsertOnSubmit(appointment);
  db.SubmitChanges();
}
```

### Updating Events

Edit events through the editor window or use the `saveEvent` method programmatically.

**Update using editor window:**

Double-click on an event to open the editor pre-filled with event details. Modify fields and click Save to update.

**Update using saveEvent method:**

For normal events:

```typescript
const scheduleObj = useRef<ScheduleComponent>(null);

const editEvent = (): void => {
  const eventData = scheduleObj.current.getEventDetails(targetElement);
  eventData.Subject = 'Updated Subject';
  scheduleObj.current.saveEvent(eventData);
};
```

For recurring events (single occurrence):

```typescript
const editOccurrence = (): void => {
  const data = new DataManager(scheduleObj.current.getCurrentViewEvents())
    .executeLocal(new Query().where('RecurrenceID', 'equal', 3));
  data[0].Subject = 'Edited';
  scheduleObj.current.saveEvent(data[0], 'EditOccurrence');
};
```

For recurring events (entire series):

```typescript
const editSeries = (): void => {
  const eventData = { /* modified event */ };
  scheduleObj.current.saveEvent(eventData, 'EditSeries');
};
```

**Server-side update:**

```csharp
if (param.action == "update" || (param.action == "batch" && param.changed != null)) {
  var value = (param.action == "update") ? param.value : param.changed[0];
  var filterData = db.ScheduleEventDatas.Where(c => c.Id == Convert.ToInt32(value.Id));
  if (filterData.Count() > 0) {
    DateTime startTime = Convert.ToDateTime(value.StartTime);
    DateTime endTime = Convert.ToDateTime(value.EndTime);
    ScheduleEventData appointment = db.ScheduleEventDatas.Single(A => A.Id == Convert.ToInt32(value.Id));
    appointment.StartTime = startTime.ToLocalTime();
    appointment.EndTime = endTime.ToLocalTime();
    appointment.Subject = value.Subject;
    appointment.RecurrenceRule = value.RecurrenceRule;
    appointment.RecurrenceException = value.RecurrenceException;
  }
  db.SubmitChanges();
}
```

**Restrict editing based on conditions:**

```typescript
const onActionBegin = (args: ActionEventArgs): void => {
  if (args.requestType === 'eventChange') {
    const weekEnds: number[] = [0, 6];
    const isWeekend = weekEnds.indexOf(args.data.StartTime.getDay()) >= 0;
    const isNonWorkHours = args.data.StartTime.getHours() < 
      parseInt(scheduleObj.current.workHours.start);
    if (isWeekend || isNonWorkHours) {
      args.cancel = true;
    }
  }
};
```

### Deleting Events

Delete events through quick popup, Delete key, or the `deleteEvent` method.

**Deletion methods:**
- Select event and click delete icon in quick popup
- Select event and press Delete key
- Select multiple events and press Delete key
- Open editor and click Delete button (no confirmation)

**Deletion using deleteEvent method:**

For normal events:

```typescript
const deleteEvent = (): void => {
  scheduleObj.current.deleteEvent(4); // Pass event ID
};
```

For recurring events (single occurrence):

```typescript
const deleteOccurrence = (): void => {
  const eventData = { /* occurrence data */ };
  scheduleObj.current.deleteEvent(eventData, 'DeleteOccurrence');
};
```

For recurring events (entire series):

```typescript
const deleteSeries = (): void => {
  const eventData = { /* series data */ };
  scheduleObj.current.deleteEvent(eventData, 'DeleteSeries');
};
```

**Server-side deletion:**

```csharp
if (param.action == "remove" || (param.action == "batch" && param.deleted != null)) {
  if (param.action == "remove") {
    int key = Convert.ToInt32(param.key);
    ScheduleEventData appointment = db.ScheduleEventDatas.Where(c => c.Id == key).FirstOrDefault();
    if (appointment != null) db.ScheduleEventDatas.DeleteOnSubmit(appointment);
  } else {
    foreach (var apps in param.deleted) {
      ScheduleEventData appointment = db.ScheduleEventDatas.Where(c => c.Id == apps.Id).FirstOrDefault();
      if (appointment != null) db.ScheduleEventDatas.DeleteOnSubmit(appointment);
    }
  }
  db.SubmitChanges();
}
```

### Drag and Drop

Enable drag-and-drop to reschedule appointments by injecting the `DragAndDrop` module and setting `allowDragAndDrop` to `true`.

**Enable drag and drop:**

```typescript
<ScheduleComponent allowDragAndDrop={true} eventSettings={eventSettings}>
  <Inject services={[Day, Week, WorkWeek, Month, DragAndDrop]} />
</ScheduleComponent>
```

**Drag multiple appointments:**

Enable `allowMultiDrag` to drag multiple selected events:

```typescript
<ScheduleComponent allowMultiDrag={true} eventSettings={eventSettings}>
  <Inject services={[Day, Week, WorkWeek, Month, DragAndDrop]} />
</ScheduleComponent>
```

**Disable drag action:**

```typescript
<ScheduleComponent allowDragAndDrop={false} eventSettings={eventSettings}>
  <Inject services={[Day, Week, WorkWeek, Month, DragAndDrop]} />
</ScheduleComponent>
```

**Prevent dragging to specific targets:**

```typescript
const onDragStart = (args: DragEventArgs): void => {
  args.excludeSelectors = 'e-header-cells,e-header-day,e-header-date,e-all-day-cells';
};
```

**Control scroll behavior during drag:**

```typescript
const onDragStart = (args: DragEventArgs): void => {
  args.scroll = { enable: false }; // Disable scrolling
  // OR
  args.scroll = { enable: true, scrollBy: 5, timeDelay: 200 }; // Custom scroll speed
};
```

**Set drag time interval:**

```typescript
const onDragStart = (args: DragEventArgs): void => {
  args.interval = 10; // Drag at 10-minute intervals
};
```

**Auto navigation on drag:**

```typescript
const onDragStart = (args: DragEventArgs): void => {
  args.navigation = { enable: true, timeDelay: 4000 };
};
```

**Drag from external source:**

```typescript
const onTreeDragStop = (event: DragAndDropEventArgs): void => {
  const scheduleElement = closest(event.target, '.e-content-wrap');
  if (scheduleElement && event.target.classList.contains('e-work-cells')) {
    const cellData = scheduleObj.current.getCellDetails(event.target);
    const eventData = {
      Subject: externalData.Name,
      StartTime: cellData.startTime,
      EndTime: cellData.endTime,
      IsAllDay: cellData.isAllDay
    };
    scheduleObj.current.addEvent(eventData);
  }
};
```

**Open editor on drag stop:**

```typescript
const onDragStop = (args: DragEventArgs): void => {
  args.cancel = true;
  scheduleObj.current.openEditor(args.data, "Save");
};
```

### Resize Events

Enable appointment resizing by injecting the `Resize` module and setting `allowResizing` to `true`.

**Enable resize:**

```typescript
<ScheduleComponent allowResizing={true} eventSettings={eventSettings}>
  <Inject services={[Day, Week, Month, Resize]} />
</ScheduleComponent>
```

**Disable resize:**

```typescript
<ScheduleComponent allowResizing={false} eventSettings={eventSettings}>
  <Inject services={[Day, Week, Month, Resize]} />
</ScheduleComponent>
```

**Control scroll during resize:**

```typescript
const onResizeStart = (args: ResizeEventArgs): void => {
  args.scroll = { enable: false };
  // OR
  args.scroll = { enable: true, scrollBy: 15 };
};
```

**Set resize time interval:**

```typescript
const onResizeStart = (args: ResizeEventArgs): void => {
  args.interval = 10; // Resize at 10-minute intervals
};
```

## Event Fields

### Built-in Fields

Map event data to Scheduler using these built-in field properties:

| Field | Description | Required |
|-------|-------------|----------|
| id | Unique identifier for the event | Yes (for CRUD) |
| subject | Summary text of the event | No |
| startTime | Event start time | Yes |
| endTime | Event end time | Yes |
| startTimezone | IANA timezone for start time | No |
| endTimezone | IANA timezone for end time | No |
| location | Location text | No |
| description | Event description | No |
| isAllDay | Whether event is all-day | No |
| recurrenceID | Parent event ID for edited occurrences | No |
| recurrenceRule | Recurrence rule string | No |
| recurrenceException | Exception dates in UTC format | No |
| isReadonly | Make event read-only | No |
| isBlock | Block time ranges | No |

### Custom Fields

Add custom fields beyond default fields without needing to map them in `eventSettings`:

```typescript
const data: Object[] = [{
  Id: 2,
  Subject: 'Meeting',
  StartTime: new Date(2018, 1, 15, 10, 0),
  EndTime: new Date(2018, 1, 15, 12, 30),
  Status: 'Completed',
  Priority: 'High'
}];
```

**Custom field sorting:**

Sort overlapping events by custom fields using `sortComparer`:

```typescript
const comparerFun = (args: Record<string, any>[]): Record<string, any>[] => {
  args.sort((event1, event2) => 
    event1.RankId.localeCompare(event2.RankId, undefined, { numeric: true })
  );
  return args;
};

const eventSettings: EventSettingsModel = { 
  dataSource: data, 
  sortComparer: comparerFun 
};
```

### Field Settings

Customize field properties with additional settings:

```typescript
const fieldsData = {
  id: 'TravelId',
  subject: { 
    name: 'TravelSummary', 
    title: 'Summary', 
    default: 'Add Summary' 
  },
  location: { 
    name: 'Source', 
    default: 'USA',
    validation: { required: true }
  },
  startTime: { name: 'DepartureTime' },
  endTime: { name: 'ArrivalTime' }
};

const eventSettings: EventSettingsModel = { 
  dataSource: data, 
  fields: fieldsData 
};
```

## Event Customization

### Using Templates

Customize event appearance using templates:

```typescript
const eventTemplate = (props) => {
  const getTimeString = (value: Date) => {
    return new Internationalization().formatDate(value, { skeleton: 'hm' });
  };
  
  return (
    <div className="template-wrap" style={{ background: props.SecondaryColor }}>
      <div className="subject" style={{ background: props.PrimaryColor }}>
        {props.Subject}
      </div>
      <div className="time" style={{ background: props.PrimaryColor }}>
        Time: {getTimeString(props.StartTime)} - {getTimeString(props.EndTime)}
      </div>
    </div>
  );
};

const eventSettings: EventSettingsModel = { 
  dataSource: data, 
  template: eventTemplate 
};
```

### Using Event Rendered Event

Customize events before rendering using the `eventRendered` event:

```typescript
const onEventRendered = (args: EventRenderedArgs): void => {
  const categoryColor: string = args.data.CategoryColor;
  if (categoryColor) {
    if (scheduleObj.current.currentView === 'Agenda') {
      (args.element.firstChild as HTMLElement).style.borderLeftColor = categoryColor;
    } else {
      args.element.style.backgroundColor = categoryColor;
    }
  }
};
```

### Using CSS Class

Apply custom styles using the `cssClass` property:

```typescript
<ScheduleComponent cssClass='custom-class' eventSettings={eventSettings}>
  <Inject services={[Day, Week, Month]} />
</ScheduleComponent>
```

```css
.custom-class .e-appointment {
  background-color: #ff6347;
  color: white;
}
```

## Advanced Features

### Block Dates and Times

Block specific time ranges by setting the `isBlock` field to `true`:

```typescript
const blockData: Object[] = [{
  Id: 1,
  Subject: 'Blocked Time',
  StartTime: new Date(2018, 1, 15, 9, 30),
  EndTime: new Date(2018, 1, 15, 11, 0),
  IsBlock: true
}];
```

**Block recurring time ranges:**

```typescript
const blockData: Object[] = [{
  Id: 1,
  Subject: 'Lunch Break',
  StartTime: new Date(2018, 1, 15, 12, 0),
  EndTime: new Date(2018, 1, 15, 13, 0),
  RecurrenceRule: 'FREQ=DAILY;INTERVAL=1;COUNT=5',
  IsBlock: true
}];
```

### Readonly Events

Make the entire Scheduler read-only:

```typescript
<ScheduleComponent readonly={true} eventSettings={eventSettings}>
  <Inject services={[Day, Week, Month]} />
</ScheduleComponent>
```

Make specific events read-only:

```typescript
const readOnlyData: Object[] = [{
  Id: 1,
  Subject: 'Past Event',
  StartTime: new Date(2018, 1, 10, 10, 0),
  EndTime: new Date(2018, 1, 10, 12, 0),
  IsReadonly: true
}];
```

**Restrict CRUD on specific time slots:**

```typescript
const onActionBegin = (args: ActionEventArgs): void => {
  if (args.requestType === 'eventCreate') {
    const eventData = args.data[0];
    const startDate = eventData[scheduleObj.current.eventFields.startTime];
    const endDate = eventData[scheduleObj.current.eventFields.endTime];
    args.cancel = !scheduleObj.current.isSlotAvailable(startDate, endDate);
  }
};
```

### Event Overlapping

Prevent overlapping events using the `allowOverlap` property:

```typescript
<ScheduleComponent allowOverlap={false} eventSettings={eventSettings}>
  <Inject services={[Day, Week, Month, Resize, DragAndDrop]} />
</ScheduleComponent>
```

**Check overlaps beyond visible range:**

```typescript
const checkOverlap = (args: ActionEventArgs): Promise<boolean> => {
  return new Promise((resolve) => {
    const eventsToCheck = Array.isArray(args.data) ? args.data : [args.data];
    const overlappingEvents = allEvents.filter(event =>
      eventsToCheck.some(newEvent =>
        new Date(event.StartTime) < newEvent.EndTime &&
        new Date(event.EndTime) > newEvent.StartTime &&
        event.Id !== newEvent.Id
      )
    );
    
    const result = overlappingEvents.length === 0;
    if (!result) {
      const popupArgs: PopupOpenEventArgs = {
        type: 'OverlapAlert',
        data: eventsToCheck,
        overlapEvents: overlappingEvents
      };
      scheduleObj.current.openOverlapAlert(popupArgs);
    }
    resolve(result);
  });
};

const onActionBegin = (args: ActionEventArgs): void => {
  if (args.requestType === 'eventCreate' || args.requestType === 'eventChange') {
    args.promise = checkOverlap(args);
  }
};
```

### Inline Editing

Enable inline editing for quick subject updates:

```typescript
<ScheduleComponent allowInline={true} eventSettings={eventSettings}>
  <Inject services={[Day, Week, Month]} />
</ScheduleComponent>
```

Single-click on a cell to add an event inline, or single-click on an event subject to edit it inline. Press Enter to save.

### Event Tooltips

Enable tooltips for events:

```typescript
const eventSettings: EventSettingsModel = { 
  dataSource: data, 
  enableTooltip: true 
};
```

**Custom tooltip template:**

```typescript
const tooltipTemplate = (props) => {
  return (
    <div className="tooltip-wrap">
      <div className="name">{props.Subject}</div>
      <div className="city">{props.City}</div>
      <div className="time">From: {props.StartTime.toLocaleString()}</div>
      <div className="time">To: {props.EndTime.toLocaleString()}</div>
    </div>
  );
};

const eventSettings: EventSettingsModel = {
  dataSource: data,
  enableTooltip: true,
  tooltipTemplate: tooltipTemplate
};
```

**Prevent tooltip for specific events:**

```typescript
const onTooltipOpen = (args): void => {
  if (args.data.Subject === 'Vacation') {
    args.cancel = true;
  }
};
```

## Troubleshooting and Edge Cases

### Setting Minimum Height for Short Events

Set minimum height for appointments when duration is less than one slot:

```typescript
const onEventRendered = (args: EventRenderedArgs): void => {
  const cellHeight = scheduleObj.current.element.querySelector('.e-work-cells').offsetHeight;
  const duration = (args.data.EndTime.getTime() - args.data.StartTime.getTime()) / (60 * 1000);
  const appHeight = duration * (cellHeight * scheduleObj.current.timeScale.slotCount) / 
                    scheduleObj.current.timeScale.interval;
  args.element.style.height = appHeight + 'px';
};
```

### Appointments Occupying Entire Cell

Make events occupy full cell height without header:

```typescript
const eventSettings: EventSettingsModel = { 
  dataSource: data, 
  enableMaxHeight: true,
  enableIndicator: false // Hide more indicator
};
```

### Limiting Maximum Events Per Row

Limit concurrent events displayed per row (Month and Timeline views):

```typescript
<ViewsDirective>
  <ViewDirective option='Month' maxEventsPerRow={3} />
</ViewsDirective>
```

### Differentiate Past Time Events

Style past events differently:

```typescript
const onEventRendered = (args: EventRenderedArgs): void => {
  if (args.data.EndTime < scheduleObj.current.selectedDate) {
    args.element.classList.add('e-past-app');
  }
};
```

```css
.e-past-app {
  opacity: 0.5;
}
```

### Retrieve Event Details from UI

Get event details from appointment element:

```typescript
const onEventClick = (args: EventClickArgs): void => {
  const event = scheduleObj.current.getEventDetails(args.element);
  console.log('Subject:', event.Subject);
};
```

### Get Current View Events

Retrieve appointments in current view:

```typescript
const getCurrentEvents = (): void => {
  const events = scheduleObj.current.getCurrentViewEvents();
  console.log('Current view events:', events.length);
};
```

### Get All Events

Get entire appointment collection:

```typescript
const getAllEvents = (): void => {
  const events = scheduleObj.current.getEvents();
  console.log('Total events:', events.length);
};
```

### Refresh Events

Refresh events without re-rendering entire Scheduler:

```typescript
scheduleObj.current.refreshEvents();
```

### Appointment Selection

- Mouse click or single tap: Select single appointment
- Ctrl + Click: Select multiple appointments
- Delete key: Delete selected appointments

### Delete Multiple Appointments

Select multiple appointments and press Delete key to remove them all at once. For recurring events, only selected occurrences are deleted, not the entire series.

Use these comprehensive reference patterns to implement robust appointment and event handling in the Syncfusion React Scheduler component. Always validate event data, handle edge cases appropriately, and provide clear user feedback for CRUD operations.