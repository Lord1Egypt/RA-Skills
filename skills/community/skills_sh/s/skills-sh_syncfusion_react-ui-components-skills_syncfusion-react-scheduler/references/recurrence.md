# Recurrence Editor

## Table of Contents
- [Overview](#overview)
- [Recurrence Rules (RRULE format)](#recurrence-rules-rrule-format)
- [Recurrence Patterns](#recurrence-patterns)
  - [Daily Pattern](#daily-pattern)
  - [Weekly Pattern](#weekly-pattern)
  - [Monthly Pattern](#monthly-pattern)
  - [Yearly Pattern](#yearly-pattern)
- [Exception Dates](#exception-dates)
- [Editing Recurring Events](#editing-recurring-events)
- [Follow Events](#follow-events)
- [Standalone Recurrence Editor Component](#standalone-recurrence-editor-component)
  - [Customizing Repeat Type Options](#customizing-repeat-type-options)
  - [Customizing End Type Options](#customizing-end-type-options)
  - [Accessing Recurrence Rule String](#accessing-recurrence-rule-string)
  - [Setting Specific Values](#setting-specific-values)
  - [Date Generation](#date-generation)

## Overview

The Recurrence editor is integrated into Scheduler's editor window by default to process the recurrence rule generation for events. It can also be used as an individual component referring from the Scheduler repository to work with recurrence-related processes.

All valid recurrence rule strings defined in the iCalendar specification apply to the recurrence editor.

## Recurrence Rules (RRULE format)

The recurrence rule is generated based on the iCalendar specifications. The generated recurrence rule string is valid for use with the Scheduler event's recurrence rule field.

**Key Components of RRULE:**
- `FREQ`: Frequency (DAILY, WEEKLY, MONTHLY, YEARLY)
- `INTERVAL`: The interval between each frequency iteration
- `COUNT`: Number of occurrences
- `UNTIL`: End date for the recurrence
- `BYDAY`: Days of the week (MO, TU, WE, TH, FR, SA, SU)
- `BYMONTHDAY`: Day of the month
- `BYMONTH`: Month of the year

**Example RRULE:**
```
FREQ=DAILY;INTERVAL=2;COUNT=8
```
This rule means: Repeat every 2 days, 8 times.

## Recurrence Patterns

### Daily Pattern

Daily recurrence allows events to repeat every day or at specified day intervals.

**Example:**
```typescript
// Repeat every day
FREQ=DAILY;INTERVAL=1

// Repeat every 2 days
FREQ=DAILY;INTERVAL=2;COUNT=8
```

### Weekly Pattern

Weekly recurrence allows events to repeat on specific days of the week.

**Example:**
```typescript
// Repeat every week on Monday and Friday
FREQ=WEEKLY;BYDAY=MO,FR;INTERVAL=1

// Repeat every 2 weeks on Wednesday
FREQ=WEEKLY;BYDAY=WE;INTERVAL=2
```

### Monthly Pattern

Monthly recurrence allows events to repeat on specific days of the month or on specific weeks.

**Example:**
```typescript
// Repeat on the 15th day of every month
FREQ=MONTHLY;BYMONTHDAY=15;INTERVAL=1

// Repeat on the first Monday of every month
FREQ=MONTHLY;BYDAY=MO;BYSETPOS=1;INTERVAL=1
```

### Yearly Pattern

Yearly recurrence allows events to repeat annually on specific dates.

**Example:**
```typescript
// Repeat every year on January 15
FREQ=YEARLY;BYMONTH=1;BYMONTHDAY=15;INTERVAL=1
```

## Exception Dates

Exception dates allow you to exclude specific occurrences from a recurring event series. Dates are specified in ISO format and separated by commas.

**Generating dates with exceptions:**
```typescript
import { RecurrenceEditorComponent } from '@syncfusion/ej2-react-schedule';

const recObject = useRef<RecurrenceEditorComponent>(null);

// Generate dates excluding specific dates
let dates = recObject.current.getRecurrenceDates(
  new Date(2018, 0, 7, 10, 0),
  'FREQ=DAILY;INTERVAL=1',
  '20180108T114224Z,20180110T114224Z', // Excluded dates
  4,
  new Date(2018, 0, 7)
);
```

The example above generates dates while excluding January 8, 2018 and January 10, 2018 from the series.

## Editing Recurring Events

When editing recurring events in the Scheduler, the recurrence editor provides options to:

1. **Edit only this event**: Modify the specific occurrence without affecting the series
2. **Edit the series**: Modify all occurrences in the recurring series
3. **Edit following events**: Modify this and all following occurrences

The recurrence editor automatically updates the recurrence rule based on the selected editing option.

## Follow Events

Follow events refer to editing the current and all subsequent occurrences of a recurring event. When you modify a recurring event and select "Edit following events," the Scheduler creates a new recurrence rule starting from that occurrence forward.

## Standalone Recurrence Editor Component

The recurrence editor can be used as a standalone component separate from the Scheduler for advanced recurrence rule handling.

### Customizing Repeat Type Options

By default, the recurrence editor provides five repeat options: Never, Daily, Weekly, Monthly, and Yearly. You can customize it to display only specific options using the `frequencies` property.

```typescript
import { ScheduleComponent, PopupOpenEventArgs } from '@syncfusion/ej2-react-schedule';

const onPopupOpen = (args: PopupOpenEventArgs): void => {
  if (args.type === 'Editor') {
    scheduleObj.current.eventWindow.recurrenceEditor.frequencies = ['none', 'daily', 'weekly'];
  }
}
```

**Available Properties:**

| Property | Type | Description |
|----------|------|-------------|
| firstDayOfWeek | number | Sets the first day of the week |
| startDate | Date | Sets the start date |
| dateformat | string | Sets the specific date format on recurrence editor |
| locale | string | Sets the locale to be applied on recurrence editor |
| cssClass | string | Allows styling with custom class names |
| enableRtl | boolean | Allows recurrence editor to render in RTL mode |
| minDate | Date | Sets the minimum date on recurrence editor |
| maxDate | Date | Sets the maximum date on recurrence editor |
| value | string | Sets the recurrence rule as its output values |
| selectedType | number | Sets the current repeat type to be set on the recurrence editor |

### Customizing End Type Options

By default, the recurrence editor provides three end options: Never, Until, and Count. You can customize it to display only specific options using the `endTypes` property.

```typescript
import { RecurrenceEditorComponent } from '@syncfusion/ej2-react-schedule';

const App = () => {
  const recObject = useRef<RecurrenceEditorComponent>(null);
  
  useEffect(() => {
    recObject.current.endTypes = ['until', 'count'];
  }, []);

  return (
    <div className='content-wrapper recurrence-editor-wrap'>
      <div className='RecurrenceEditor'>
        <RecurrenceEditorComponent id='RecurrenceEditor' ref={recObject}></RecurrenceEditorComponent>
      </div>
    </div>
  );
};
```

### Accessing Recurrence Rule String

The `change` event triggers whenever the recurrence editor fields change. You can access the generated recurrence rule through the `value` property in the event arguments.

```typescript
import { RecurrenceEditorComponent, RecurrenceEditorChangeEventArgs } from '@syncfusion/ej2-react-schedule';

const onChange = (args: RecurrenceEditorChangeEventArgs): void => {
  if (args.value === "") {
    console.log('No rule selected');
  } else {
    console.log('Generated rule:', args.value);
  }
}

return (
  <RecurrenceEditorComponent id='RecurrenceEditor' change={onChange}></RecurrenceEditorComponent>
);
```

### Setting Specific Values

You can display the recurrence editor with specific options loaded initially by providing a rule string through the `setRecurrenceRule` method.

```typescript
import { RecurrenceEditorComponent } from '@syncfusion/ej2-react-schedule';

const App = () => {
  const recObject = useRef<RecurrenceEditorComponent>(null);

  useEffect(() => {
    recObject.current.setRecurrenceRule('FREQ=DAILY;INTERVAL=2;COUNT=8');
  }, []);

  return (
    <RecurrenceEditorComponent id='RecurrenceEditor' ref={recObject}></RecurrenceEditorComponent>
  );
};
```

### Date Generation

You can parse the recurrence rule of an event to generate date instances using the `getRecurrenceDates` method.

**Method Parameters:**

| Field name | Type | Description |
|------------|------|-------------|
| startDate | Date | Appointment start date |
| rule | String | Recurrence rule present in an event object |
| excludeDate | String | Date collection (in ISO format) to be excluded (optional) |
| maximumCount | Number | Number of date count to be generated (optional) |
| viewDate | Date | Current view range's first date (optional) |

**Example:**
```typescript
import { RecurrenceEditorComponent } from '@syncfusion/ej2-react-schedule';

const recObject = useRef<RecurrenceEditorComponent>(null);

let dates = recObject.current.getRecurrenceDates(
  new Date(2018, 0, 7, 10, 0),
  'FREQ=DAILY;INTERVAL=1',
  '20180108T114224Z,20180110T114224Z',
  4,
  new Date(2018, 0, 7)
);
```

**Restricting Date Generation with Count:**

For rules in the "NEVER ENDS" category, you can specify a maximum count to stop date generation:

```typescript
let dates = recObject.current.getRecurrenceDates(
  new Date(2018, 0, 7, 10, 0),
  'FREQ=DAILY;INTERVAL=1',
  null,
  10, // Maximum count of 10 dates
  null
);
```

**Server-Side Date Generation:**

You can also generate recurrence date instances from server-side by manually referring to the `RecurrenceHelper` class.

---
