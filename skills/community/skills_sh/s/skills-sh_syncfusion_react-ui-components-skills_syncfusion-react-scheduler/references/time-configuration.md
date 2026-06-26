# Time Configuration

## Table of Contents

1. [Overview](#overview)
2. [Timescale Configuration](#timescale-configuration)
   - [Setting Time Slot Duration](#setting-time-slot-duration)
   - [Customizing Time Cells with Templates](#customizing-time-cells-with-templates)
   - [Hiding the Timescale](#hiding-the-timescale)
   - [Current Time Indicator](#current-time-indicator)
3. [Timezone Management](#timezone-management)
   - [Understanding Date Manipulation](#understanding-date-manipulation)
   - [Scheduler Without Specific Timezone](#scheduler-without-specific-timezone)
   - [Setting Specific Timezone](#setting-specific-timezone)
   - [Display Events with No Time Difference](#display-events-with-no-time-difference)
   - [Assign Specific Timezones to Events](#assign-specific-timezones-to-events)
   - [Customizing Timezone Collection](#customizing-timezone-collection)
   - [Timezone Methods](#timezone-methods)
4. [Working Days and Hours](#working-days-and-hours)
   - [Set Working Days](#set-working-days)
   - [Hiding Weekend Days](#hiding-weekend-days)
   - [Show Week Numbers](#show-week-numbers)
   - [Set Working Hours](#set-working-hours)
   - [Custom Display Hours](#custom-display-hours)
   - [Setting First Day of Week](#setting-first-day-of-week)
   - [Scroll to Specific Time](#scroll-to-specific-time)
5. [Calendar Modes](#calendar-modes)
   - [Gregorian Calendar](#gregorian-calendar)
   - [Islamic Calendar](#islamic-calendar)
6. [Time Format Examples](#time-format-examples)

---

## Overview

The Syncfusion React Scheduler provides comprehensive time configuration options to customize how time is displayed and managed in your scheduling application. This includes:

- **Timescale**: Control time slot intervals and visual appearance
- **Timezone**: Support for single and multiple timezone scenarios
- **Working Days/Hours**: Define business hours and working days
- **Calendar Modes**: Support for Gregorian and Islamic calendars
- **Time Formats**: Flexible time display formatting

These features work together to create a flexible scheduling experience that can adapt to various business requirements and international needs.

---

## Timescale Configuration

Time slots are the cells displayed in the Day, Week, and Work Week views of the Scheduler. The `timeScale` property controls the duration and appearance of these slots.

### Key Properties

- **`enable`**: When `true`, displays appointments accurately against exact time duration. Default: `true`
- **`interval`**: Time duration in minutes for each time axis segment. Default: `60` (1 hour)
- **`slotCount`**: Number of slots to split the interval into. Default: `2` (30-minute slots)

> **Note**: The maximum slots per day is 1000 for Timeline views (TimelineDay, TimelineWeek, TimelineWorkWeek).

### Setting Time Slot Duration

Configure custom time slot durations by combining `interval` and `slotCount`. The following example creates six 10-minute slots per hour:

```tsx
import * as React from 'react';
import {
  ScheduleComponent, Day, Week, WorkWeek, TimelineViews,
  ViewsDirective, ViewDirective, Inject, EventSettingsModel, TimeScaleModel
} from '@syncfusion/ej2-react-schedule';
import { scheduleData } from './datasource';

const App = () => {
  const eventSettings: EventSettingsModel = { dataSource: scheduleData };
  const timeScale: TimeScaleModel = { 
    enable: true, 
    interval: 60, 
    slotCount: 6 
  };

  return (
    <ScheduleComponent 
      width='100%' 
      height='550px'
      selectedDate={new Date(2018, 1, 15)} 
      eventSettings={eventSettings}
      timeScale={timeScale}
    >
      <ViewsDirective>
        <ViewDirective option='Day' />
        <ViewDirective option='Week' />
        <ViewDirective option='WorkWeek' />
        <ViewDirective option='TimelineDay' />
      </ViewsDirective>
      <Inject services={[Day, Week, WorkWeek, TimelineViews]} />
    </ScheduleComponent>
  );
};

export default App;
```

### Customizing Time Cells with Templates

Use templates to customize the appearance of time cells with `majorSlotTemplate` and `minorSlotTemplate`:

```tsx
import * as React from 'react';
import {
  ScheduleComponent, Day, Week, WorkWeek, TimelineViews,
  ViewsDirective, ViewDirective, Inject, EventSettingsModel, TimeScaleModel
} from '@syncfusion/ej2-react-schedule';
import { scheduleData } from './datasource';
import { Internationalization } from '@syncfusion/ej2-base';

const App = () => {
  const eventSettings: EventSettingsModel = { dataSource: scheduleData };
  const instance = new Internationalization();

  const minorSlotTemplate = (props): JSX.Element => {
    return (
      <div style={{ textAlign: 'right', marginRight: '15px' }}>
        {instance.formatDate(props.date, { skeleton: 'ms' }).replace(':00', '')}
      </div>
    );
  };

  const majorSlotTemplate = (props): JSX.Element => {
    return (
      <div>{instance.formatDate(props.date, { skeleton: 'hm' })}</div>
    );
  };

  const timeScale: TimeScaleModel = {
    enable: true, 
    interval: 60, 
    slotCount: 6,
    majorSlotTemplate: majorSlotTemplate,
    minorSlotTemplate: minorSlotTemplate
  };

  return (
    <ScheduleComponent 
      width='100%' 
      height='550px'
      selectedDate={new Date(2018, 1, 15)} 
      eventSettings={eventSettings}
      timeScale={timeScale}
    >
      <ViewsDirective>
        <ViewDirective option='Day' />
        <ViewDirective option='Week' />
        <ViewDirective option='TimelineWeek' />
        <ViewDirective option='WorkWeek' />
      </ViewsDirective>
      <Inject services={[Day, Week, WorkWeek, TimelineViews]} />
    </ScheduleComponent>
  );
};

export default App;
```

### Hiding the Timescale

Disable grid lines by setting `enable` to `false`. All appointments display one below another without time indicators:

```tsx
const timeScale: TimeScaleModel = { enable: false };

<ScheduleComponent 
  width='100%' 
  height='550px'
  selectedDate={new Date(2018, 1, 15)} 
  eventSettings={eventSettings}
  timeScale={timeScale}
>
  {/* Views */}
</ScheduleComponent>
```

### Current Time Indicator

The Scheduler highlights the current time by default. Control this with `showTimeIndicator`:

```tsx
<ScheduleComponent 
  width='100%' 
  height='550px'
  showTimeIndicator={true}  // Default: true
>
  <ViewsDirective>
    <ViewDirective option='Day' />
    <ViewDirective option='Week' />
    <ViewDirective option='TimelineWeek' />
  </ViewsDirective>
  <Inject services={[Day, Week, TimelineViews]} />
</ScheduleComponent>
```

---

## Timezone Management

The Scheduler supports comprehensive timezone management for global scheduling scenarios.

### Understanding Date Manipulation

JavaScript's `new Date()` constructor returns the current date with complete time and timezone information:

```javascript
// Example output:
// Wed Dec 12 2018 05:23:27 GMT+0530 (India Standard Time)
```

### Scheduler Without Specific Timezone

When the `timezone` property is not set, appointments display based on the client's system timezone. The same appointment may appear at different times for users in different timezones.

```tsx
import * as React from 'react';
import {
  ScheduleComponent, Day, Week, WorkWeek, Month, Agenda, Inject, EventSettingsModel
} from '@syncfusion/ej2-react-schedule';

const App = () => {
  const scheduleData: Object[] = [{
    Id: 3,
    Subject: 'Paris',
    StartTime: new Date(2018, 1, 15, 9, 0),
    EndTime: new Date(2018, 1, 15, 10, 0)
  }];
  
  const eventSettings: EventSettingsModel = { dataSource: scheduleData };

  return (
    <ScheduleComponent 
      width='100%' 
      height='550px'
      selectedDate={new Date(2018, 1, 11)} 
      eventSettings={eventSettings}
    >
      <Inject services={[Day, Week, WorkWeek, Month, Agenda]} />
    </ScheduleComponent>
  );
};

export default App;
```

### Setting Specific Timezone

Set a specific timezone using the `timezone` property. Appointments display according to the Scheduler's timezone regardless of the user's system timezone:

```tsx
import * as React from 'react';
import {
  ScheduleComponent, Day, Week, WorkWeek, Month, Agenda, Inject, EventSettingsModel
} from '@syncfusion/ej2-react-schedule';
import { scheduleData } from './datasource';

const App = () => {
  const eventSettings: EventSettingsModel = { dataSource: scheduleData };

  return (
    <ScheduleComponent 
      width='100%' 
      height='550px'
      selectedDate={new Date(2018, 1, 17)} 
      eventSettings={eventSettings}
      timezone='America/New_York'  // Eastern Time UTC-05:00
    >
      <Inject services={[Day, Week, WorkWeek, Month, Agenda]} />
    </ScheduleComponent>
  );
};

export default App;
```

### Display Events with No Time Difference

Setting timezone to `UTC` displays appointments at the same time for all users globally:

```tsx
import * as React from 'react';
import {
  ScheduleComponent, Day, Week, Month, Timezone, Inject,
  ViewsDirective, ViewDirective, EventSettingsModel
} from '@syncfusion/ej2-react-schedule';
import { fifaEventsData } from './datasource';

const App = () => {
  const eventSettings: EventSettingsModel = { dataSource: fifaEventsData };
  let timezone: Timezone = new Timezone();

  const onCreate = (): void => {
    for (let fifaEvent of fifaEventsData) {
      let event: { [key: string]: Object } = fifaEvent as { [key: string]: Object };
      event.StartTime = timezone.removeLocalOffset(event.StartTime as Date);
      event.EndTime = timezone.removeLocalOffset(event.EndTime as Date);
    }
  };

  return (
    <ScheduleComponent 
      width='100%' 
      height='550px'
      selectedDate={new Date(2018, 5, 17)} 
      created={onCreate}
      eventSettings={eventSettings}
      timezone='UTC'
    >
      <ViewsDirective>
        <ViewDirective option='Day' />
        <ViewDirective option='Week' />
        <ViewDirective option='Month' />
      </ViewsDirective>
      <Inject services={[Day, Week, Month]} />
    </ScheduleComponent>
  );
};

export default App;
```

### Assign Specific Timezones to Events

Individual appointments can have their own timezones using `startTimezone` and `endTimezone` properties:

```tsx
import * as React from 'react';
import {
  ScheduleComponent, Day, Week, WorkWeek, Month, Agenda, Inject, EventSettingsModel
} from '@syncfusion/ej2-react-schedule';

const App = () => {
  const scheduleData: Object[] = [{
    Id: 3,
    Subject: 'Paris',
    StartTime: new Date(2018, 1, 15, 10, 0),
    EndTime: new Date(2018, 1, 15, 12, 30),
    StartTimezone: 'Europe/Moscow',
    EndTimezone: 'Europe/Moscow'
  }];

  const eventSettings: EventSettingsModel = { dataSource: scheduleData };

  return (
    <ScheduleComponent 
      width='100%' 
      height='550px'
      selectedDate={new Date(2018, 1, 11)} 
      eventSettings={eventSettings}
    >
      <Inject services={[Day, Week, WorkWeek, Month, Agenda]} />
    </ScheduleComponent>
  );
};

export default App;
```

### Customizing Timezone Collection

Customize the timezone collection shown in the editor window:

```tsx
import * as React from 'react';
import { useEffect } from 'react';
import {
  ScheduleComponent, Day, Week, Month, timezoneData, Inject, EventSettingsModel
} from '@syncfusion/ej2-react-schedule';
import { scheduleData } from './datasource';

const App = () => {
  const eventSettings: EventSettingsModel = { dataSource: scheduleData };

  const timeZones: { [key: string]: Object }[] = [
    { Value: 'America/New_York', Text: '(UTC-05:00) Eastern Time' },
    { Value: 'UTC', Text: 'UTC' },
    { Value: 'Asia/Kolkata', Text: '(UTC+05:30) India Standard Time' }
  ];

  useEffect(() => {
    timezoneData.splice(0, timezoneData.length, ...timeZones as any);
  }, []);

  return (
    <ScheduleComponent 
      width='100%' 
      height='550px'
      selectedDate={new Date(2018, 1, 1)} 
      eventSettings={eventSettings}
    >
      <Inject services={[Day, Week, Month]} />
    </ScheduleComponent>
  );
};

export default App;
```

### Timezone Methods

The Scheduler provides utility methods for timezone operations:

#### offset

Calculates the difference in minutes between a UTC date and a target timezone:

```typescript
let timezone: Timezone = new Timezone();
let date: Date = new Date(2018, 11, 5, 15, 25, 11);
let timeZoneOffset: number = timezone.offset(date, "Europe/Paris");
console.log(timeZoneOffset); // -60
```

**Parameters:**
- `Date` (Date): UTC time as date object
- `Timezone` (String): Target timezone

**Returns:** `number` (offset in minutes)

#### convert

Converts a date from one timezone to another:

```typescript
let timezone: Timezone = new Timezone();
let date: Date = new Date(2018, 11, 5, 15, 25, 11);
let convertedDate: Date = timezone.convert(date, "Europe/Paris", "Asia/Tokyo");
let convertedDate1: Date = timezone.convert(date, 60, -360);
console.log(convertedDate);  // 2018-12-05T08:55:11.000Z
console.log(convertedDate1); // 2018-12-05T16:55:11.000Z
```

**Parameters:**
- `Date` (Date): UTC time as date object
- `fromOffset` (number/string): Source timezone
- `toOffset` (number/string): Target timezone

**Returns:** `Date`

#### add

Adds the time difference between UTC and a timezone to the date:

```typescript
let timezone: Timezone = new Timezone();
let date: Date = new Date(2018, 11, 5, 15, 25, 11);
let convertedDate: Date = timezone.add(date, "Europe/Paris");
console.log(convertedDate); // 2018-12-05T05:25:11.000Z
```

**Parameters:**
- `Date` (Date): UTC time as date object
- `Timezone` (String): Target timezone

**Returns:** `Date`

#### remove

Removes the time difference between UTC and a timezone:

```typescript
let timezone: Timezone = new Timezone();
let date: Date = new Date(2018, 11, 5, 15, 25, 11);
let convertedDate: Date = timezone.remove(date, "Europe/Paris");
console.log(convertedDate); // 2018-12-05T14:25:11.000Z
```

**Parameters:**
- `Date` (Date): UTC time as date object
- `Timezone` (String): Target timezone

**Returns:** `Date`

#### removeLocalOffset

Removes the local timezone offset from a date:

```typescript
let timezone: Timezone = new Timezone();
let date: Date = new Date(2018, 11, 5, 15, 25, 11);
let convertedDate: Date = timezone.removeLocalOffset(date);
console.log(convertedDate); // 2018-12-05T15:25:11.000Z
```

**Parameters:**
- `Date` (Date): UTC time as date object

**Returns:** `Date`

---

## Working Days and Hours

Configure working days, hours, and display options to match your business requirements.

### Set Working Days

By default, Monday through Friday are working days `[1, 2, 3, 4, 5]` (0=Sunday, 1=Monday, etc.). Use the `workDays` property to customize:

```tsx
import * as React from 'react';
import {
  ScheduleComponent, Week, WorkWeek, TimelineViews, Inject,
  ViewsDirective, ViewDirective, EventSettingsModel
} from '@syncfusion/ej2-react-schedule';
import { scheduleData } from './datasource';

const App = () => {
  const eventSettings: EventSettingsModel = { dataSource: scheduleData };
  const workingDays: number[] = [1, 3, 5]; // Monday, Wednesday, Friday

  return (
    <ScheduleComponent 
      width='100%' 
      height='550px'
      selectedDate={new Date(2018, 1, 15)} 
      eventSettings={eventSettings}
      workDays={workingDays}
    >
      <ViewsDirective>
        <ViewDirective option='Week' />
        <ViewDirective option='WorkWeek' />
        <ViewDirective option='TimelineWorkWeek' />
      </ViewsDirective>
      <Inject services={[Week, WorkWeek, TimelineViews]} />
    </ScheduleComponent>
  );
};

export default App;
```

> **Note**: Working hours highlighting applies only to specified working days.

### Hiding Weekend Days

Hide non-working days using `showWeekend`:

```tsx
import * as React from 'react';
import {
  ScheduleComponent, Day, Week, Month, Inject,
  ViewsDirective, ViewDirective, EventSettingsModel
} from '@syncfusion/ej2-react-schedule';
import { scheduleData } from './datasource';

const App = () => {
  const eventSettings: EventSettingsModel = { dataSource: scheduleData };

  return (
    <ScheduleComponent 
      width='100%' 
      height='550px'
      selectedDate={new Date(2018, 1, 15)} 
      eventSettings={eventSettings}
      showWeekend={false}
      workDays={[1, 3, 4, 5]}
    >
      <ViewsDirective>
        <ViewDirective option='Day' />
        <ViewDirective option='Week' />
        <ViewDirective option='Month' />
      </ViewsDirective>
      <Inject services={[Day, Week, Month]} />
    </ScheduleComponent>
  );
};

export default App;
```

### Show Week Numbers

Display week numbers using `showWeekNumber`:

```tsx
import * as React from 'react';
import {
  ScheduleComponent, Day, Week, WorkWeek, Month, Agenda, Inject, EventSettingsModel
} from '@syncfusion/ej2-react-schedule';
import { scheduleData } from './datasource';

const App = () => {
  const eventSettings: EventSettingsModel = { dataSource: scheduleData };

  return (
    <ScheduleComponent 
      width='100%' 
      height='550px'
      selectedDate={new Date(2018, 1, 15)} 
      eventSettings={eventSettings}
      showWeekNumber={true}
      workDays={[1, 3, 4, 5]}
    >
      <Inject services={[Day, Week, Month]} />
    </ScheduleComponent>
  );
};

export default App;
```

#### Week Number Rules

Customize week calculation with `weekRule`:

- **`FirstDay`**: First week starts on the first day of the year
- **`FirstFourDayWeek`**: First week has four or more days
- **`FirstFullWeek`**: First week starts on the first occurrence of the designated first day

```tsx
<ScheduleComponent 
  width='100%' 
  height='550px'
  selectedDate={new Date(2020, 1, 15)} 
  eventSettings={eventSettings}
  showWeekNumber={true}
  weekRule='FirstFourDayWeek'
  workDays={[1, 3, 4, 5]}
>
  <Inject services={[Day, Week, Month]} />
</ScheduleComponent>
```

> **Note**: `weekRule` depends on `firstDayOfWeek` value and requires `showWeekNumber` to be enabled.

### Set Working Hours

Define working hours using the `workHours` property:

```tsx
import * as React from 'react';
import {
  ScheduleComponent, Day, Week, WorkWeek, Inject,
  ViewsDirective, ViewDirective, EventSettingsModel, WorkHoursModel
} from '@syncfusion/ej2-react-schedule';
import { scheduleData } from './datasource';

const App = () => {
  const eventSettings: EventSettingsModel = { dataSource: scheduleData };
  const workHours: WorkHoursModel = {
    highlight: true,
    start: '11:00',
    end: '20:00'
  };

  return (
    <ScheduleComponent 
      width='100%' 
      height='550px'
      selectedDate={new Date(2018, 1, 15)} 
      workHours={workHours}
      eventSettings={eventSettings}
    >
      <ViewsDirective>
        <ViewDirective option='Day' />
        <ViewDirective option='Week' />
        <ViewDirective option='WorkWeek' />
      </ViewsDirective>
      <Inject services={[Day, Week, WorkWeek]} />
    </ScheduleComponent>
  );
};

export default App;
```

**Properties:**
- **`highlight`**: Enable/disable working hours highlighting
- **`start`**: Start time of working hours
- **`end`**: End time of working hours

### Custom Display Hours

Display specific time ranges using `startHour` and `endHour`:

```tsx
import * as React from 'react';
import {
  ScheduleComponent, Day, Week, WorkWeek, Inject,
  ViewsDirective, ViewDirective, EventSettingsModel
} from '@syncfusion/ej2-react-schedule';
import { scheduleData } from './datasource';

const App = () => {
  const eventSettings: EventSettingsModel = { dataSource: scheduleData };

  return (
    <ScheduleComponent 
      width='100%' 
      height='550px'
      selectedDate={new Date(2018, 1, 15)} 
      startHour='07:00'
      endHour='18:00'
      eventSettings={eventSettings}
    >
      <ViewsDirective>
        <ViewDirective option='Day' />
        <ViewDirective option='Week' />
        <ViewDirective option='WorkWeek' />
      </ViewsDirective>
      <Inject services={[Day, Week, WorkWeek]} />
    </ScheduleComponent>
  );
};

export default App;
```

### Setting First Day of Week

Customize the week's start day using `firstDayOfWeek`:

```tsx
import * as React from 'react';
import {
  ScheduleComponent, Week, Month, Inject,
  ViewsDirective, ViewDirective, EventSettingsModel
} from '@syncfusion/ej2-react-schedule';
import { scheduleData } from './datasource';

const App = () => {
  const eventSettings: EventSettingsModel = { dataSource: scheduleData };

  return (
    <ScheduleComponent 
      width='100%' 
      height='550px'
      selectedDate={new Date(2018, 1, 15)} 
      eventSettings={eventSettings}
      firstDayOfWeek={1}  // Monday
    >
      <ViewsDirective>
        <ViewDirective option='Week' />
        <ViewDirective option='Month' />
      </ViewsDirective>
      <Inject services={[Week, Month]} />
    </ScheduleComponent>
  );
};

export default App;
```

### Scroll to Specific Time

Use the `scrollTo` method to programmatically scroll to a specific time:

```tsx
import { useRef } from 'react';
import * as React from 'react';
import { TimePickerComponent, ChangeEventArgs } from '@syncfusion/ej2-react-calendars';
import {
  ScheduleComponent, Day, Week, TimelineViews, Inject, EventSettingsModel,
  ViewsDirective, ViewDirective
} from '@syncfusion/ej2-react-schedule';
import { scheduleData } from './datasource';

const App = () => {
  const scheduleObj = useRef<ScheduleComponent>(null);
  const eventSettings: EventSettingsModel = { dataSource: scheduleData };

  const onChange = (args: ChangeEventArgs): void => {
    scheduleObj.current.scrollTo(args.text);
  };

  return (
    <div>
      <TimePickerComponent 
        width={100} 
        value={new Date(2000, 0, 1, 9)} 
        format='HH:mm'
        change={onChange}
      />
      <ScheduleComponent 
        width='100%' 
        height='550px'
        ref={scheduleObj}
        selectedDate={new Date(2018, 1, 15)} 
        eventSettings={eventSettings}
      >
        <ViewsDirective>
          <ViewDirective option='Day' />
          <ViewDirective option='Week' />
          <ViewDirective option='TimelineDay' />
          <ViewDirective option='TimelineWeek' />
        </ViewsDirective>
        <Inject services={[Day, Week, TimelineViews]} />
      </ScheduleComponent>
    </div>
  );
};

export default App;
```

#### Scroll to Current Time on Load

Automatically scroll to current system time when the Scheduler loads:

```tsx
import { useRef } from 'react';
import * as React from 'react';
import {
  ScheduleComponent, Day, Week, TimelineViews, Inject,
  ViewsDirective, ViewDirective, EventSettingsModel
} from '@syncfusion/ej2-react-schedule';
import { scheduleData } from './datasource';
import { Internationalization } from '@syncfusion/ej2-base';

const App = () => {
  const scheduleObj = useRef<ScheduleComponent>(null);
  const eventSettings: EventSettingsModel = { dataSource: scheduleData };
  const instance: Internationalization = new Internationalization();

  const onCreated = (): void => {
    scheduleObj.current.scrollTo(
      instance.formatDate(new Date(), { skeleton: 'hm' })
    );
  };

  return (
    <ScheduleComponent 
      ref={scheduleObj}
      width='100%' 
      height='550px'
      selectedDate={new Date(2018, 1, 15)} 
      eventSettings={eventSettings}
      created={onCreated}
    >
      <ViewsDirective>
        <ViewDirective option='Day' />
        <ViewDirective option='Week' />
        <ViewDirective option='TimelineWeek' />
      </ViewsDirective>
      <Inject services={[Day, Week, TimelineViews]} />
    </ScheduleComponent>
  );
};

export default App;
```

---

## Calendar Modes

The Scheduler supports both Gregorian and Islamic calendar systems.

### Gregorian Calendar

The default calendar mode. The Gregorian calendar is the most widely adopted solar calendar with 12 months, 28-31 days per month, and 365 days (366 in leap years).

```tsx
<ScheduleComponent 
  width='100%' 
  height='550px'
  calendarMode='Gregorian'  // Default
  eventSettings={eventSettings}
>
  {/* Views */}
</ScheduleComponent>
```

### Islamic Calendar

The Islamic (Hijri) calendar is a lunar calendar with 12 months and 354-355 days per year. Odd months have 30 days, even months have 29 days.

#### Setup Requirements

To use the Islamic calendar, import and inject required modules, then load CLDR data:

```tsx
import * as React from 'react';
import {
  ScheduleComponent, Day, Week, Month, TimelineViews, Inject,
  ViewsDirective, ViewDirective, EventSettingsModel
} from '@syncfusion/ej2-react-schedule';
import { scheduleData } from './datasource';
import { L10n, loadCldr } from '@syncfusion/ej2-base';
import * as localeObj from './locale.json';

// Import CLDR data
import arNumberData from '@syncfusion/ej2-cldr-data/main/ar/numbers.json';
import artimeZoneData from '@syncfusion/ej2-cldr-data/main/ar/timeZoneNames.json';
import arGregorian from '@syncfusion/ej2-cldr-data/main/ar/ca-gregorian.json';
import arIslamic from '@syncfusion/ej2-cldr-data/main/ar/ca-islamic.json';
import arNumberingSystem from '@syncfusion/ej2-cldr-data/supplemental/numberingSystems.json';

// Load CLDR data
loadCldr(arNumberData, artimeZoneData, arGregorian, arIslamic, arNumberingSystem);
L10n.load(localeObj);

const App = () => {
  const eventSettings: EventSettingsModel = { dataSource: scheduleData };

  return (
    <ScheduleComponent 
      height='550px'
      showQuickInfo={false}
      selectedDate={new Date(2018, 1, 15)} 
      locale='ar'
      calendarMode='Islamic'
      eventSettings={eventSettings}
    >
      <ViewsDirective>
        <ViewDirective option='Day' />
        <ViewDirective option='Week' />
        <ViewDirective option='TimelineWorkWeek' />
        <ViewDirective option='Month' />
      </ViewsDirective>
      <Inject services={[Day, Week, Month, TimelineViews]} />
    </ScheduleComponent>
  );
};

export default App;
```

**Required CLDR Files:**
- `numberingSystems.json`
- `ca-gregorian.json`
- `numbers.json`
- `timeZoneNames.json`
- `ca-islamic.json`

> **Note**: The current Islamic year is 1440 AH (approximately September 11, 2018 to August 30, 2019 in Gregorian calendar).

---

## Time Format Examples

### Common Time Format Patterns

The Scheduler uses the Internationalization library for flexible time formatting:

#### 24-Hour Format

```tsx
import { Internationalization } from '@syncfusion/ej2-base';

const instance = new Internationalization();
const formattedTime = instance.formatDate(new Date(), { skeleton: 'Hm' });
// Output: "14:30"
```

#### 12-Hour Format with AM/PM

```tsx
const instance = new Internationalization();
const formattedTime = instance.formatDate(new Date(), { skeleton: 'hm' });
// Output: "2:30 PM"
```

#### Full Date and Time

```tsx
const instance = new Internationalization();
const formattedDateTime = instance.formatDate(
  new Date(), 
  { skeleton: 'full' }
);
// Output: "Monday, March 23, 2026 at 2:30:00 PM GMT+05:30"
```

#### Custom Time Format in Templates

```tsx
const timeTemplate = (props): JSX.Element => {
  const instance = new Internationalization();
  return (
    <div>
      {instance.formatDate(props.date, { 
        skeleton: 'hm',
        type: 'time'
      })}
    </div>
  );
};
```

### Formatting Options

Common skeleton patterns for time formatting:

| Skeleton | Description | Example Output |
|----------|-------------|----------------|
| `h` | Hour (12-hour) | 2 |
| `H` | Hour (24-hour) | 14 |
| `m` | Minute | 30 |
| `s` | Second | 45 |
| `hm` | Hour:Minute (12-hour) | 2:30 PM |
| `Hm` | Hour:Minute (24-hour) | 14:30 |
| `hms` | Hour:Minute:Second (12-hour) | 2:30:45 PM |
| `Hms` | Hour:Minute:Second (24-hour) | 14:30:45 |
| `ms` | Minute:Second | 30:45 |

---

## Best Practices

### Performance Optimization

1. **Limit time slots**: Keep slot count × interval reasonable (max 1000 slots for Timeline views)
2. **Use appropriate intervals**: Match business requirements (e.g., 30-minute slots for meetings)
3. **Minimize template complexity**: Keep slot templates simple for better rendering performance

### Timezone Considerations

1. **Server-side storage**: Always store appointment times in UTC on the server
2. **Client-side display**: Convert to appropriate timezone for display
3. **Cross-timezone meetings**: Use event-specific timezones for international meetings
4. **Timezone updates**: Keep timezone data updated for daylight saving changes

### Working Days Configuration

1. **Match business hours**: Configure working days and hours to match actual business operations
2. **Regional differences**: Consider regional holidays and working patterns
3. **View selection**: Use WorkWeek view for working-days-only display
4. **Visual clarity**: Enable `showWeekend: false` to focus on business days

### Calendar Mode Selection

1. **User preference**: Allow users to select their preferred calendar mode
2. **Locale integration**: Match calendar mode with user locale settings
3. **CLDR data**: Ensure all required CLDR files are loaded for Islamic calendar
4. **Testing**: Test thoroughly with both calendar modes if supporting multiple regions

---

## Summary

The Syncfusion React Scheduler provides comprehensive time configuration capabilities:

- **Timescale**: Customize time slot duration, appearance, and visibility
- **Timezone**: Support for single/multiple timezones with conversion utilities
- **Working Days/Hours**: Define business-specific time ranges and days
- **Calendar Modes**: Support for Gregorian and Islamic calendar systems
- **Time Formats**: Flexible formatting options for internationalization

These features enable you to create a scheduling solution tailored to your specific business requirements and user needs.

---
