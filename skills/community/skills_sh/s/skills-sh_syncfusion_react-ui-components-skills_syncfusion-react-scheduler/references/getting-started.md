# Getting Started with React Scheduler

## Table of Contents
- [Overview](#overview)
- [Dependencies](#dependencies)
- [Installation and Configuration](#installation-and-configuration)
- [Adding CSS Themes](#adding-css-themes)
- [Module Injection](#module-injection)
- [Initialize the Scheduler](#initialize-the-scheduler)
- [Populating Appointments](#populating-appointments)
- [Field Mapping](#field-mapping)
- [Setting Date](#setting-date)
- [Setting View](#setting-view)
- [Individual View Customization](#individual-view-customization)

## Overview

The Syncfusion React Scheduler component provides a comprehensive calendar interface for displaying and managing appointments. This guide walks through the essential steps to install, configure, and render your first Scheduler component with data.

## Dependencies

The Scheduler component requires the following npm packages:

```
|-- @syncfusion/ej2-react-schedule
    |-- @syncfusion/ej2-base
    |-- @syncfusion/ej2-data
    |-- @syncfusion/ej2-schedule
        |-- @syncfusion/ej2-compression
        |-- @syncfusion/ej2-excel-export
        |-- @syncfusion/ej2-file-utils
        |-- @syncfusion/ej2-navigations
        |-- @syncfusion/ej2-calendars
          |-- @syncfusion/ej2-inputs
            |-- @syncfusion/ej2-split-buttons
          |-- @syncfusion/ej2-lists
          |-- @syncfusion/ej2-popups
            |-- @syncfusion/ej2-buttons
        |-- @syncfusion/ej2-dropdowns
```

The main package `@syncfusion/ej2-react-schedule` automatically installs all required peer dependencies.

## Installation and Configuration

### Setup for Local Development

**Using Vite (Recommended):**

Vite provides faster development environment, smaller bundle sizes, and optimized builds compared to traditional tools like create-react-app.

**TypeScript Setup:**
```bash
npm create vite@latest my-scheduler-app -- --template react-ts
cd my-scheduler-app
npm install
npm run dev
```

**JavaScript Setup:**
```bash
npm create vite@latest my-scheduler-app -- --template react
cd my-scheduler-app
npm install
npm run dev
```

### Install Scheduler Package

Install the Scheduler component package from npm:

```bash
npm install @syncfusion/ej2-react-schedule --save
```

## Adding CSS Themes

Add the Scheduler component styles to `src/App.css`. The Scheduler requires styles from multiple dependent components:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-calendars/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-dropdowns/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-lists/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-splitbuttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-schedule/styles/tailwind3.css";
```

**Available Themes:**
Replace `tailwind3` with any of the following theme names:
- `material3` - Material Design 3
- `bootstrap5` - Bootstrap 5
- `fluent` - Microsoft Fluent
- `tailwind3` - Tailwind CSS
- `material` - Material Design (legacy)
- `bootstrap` - Bootstrap (legacy)
- `fabric` - Microsoft Fabric

**Import CSS in your component:**

Make sure to import `App.css` in your `src/App.tsx` file:

```tsx
import './App.css';
```

## Module Injection

The Scheduler uses a modular architecture where each view type is maintained as an individual module. You must inject the required view modules to use them in the Scheduler.

**Available View Modules:**

| Module | Description | Import Name |
|--------|-------------|-------------|
| `Day` | Day view with time slots | `Day` |
| `Week` | Week view with 7 days | `Week` |
| `WorkWeek` | Work week view (Monday-Friday) | `WorkWeek` |
| `Month` | Month view with calendar grid | `Month` |
| `Agenda` | List view of appointments | `Agenda` |
| `MonthAgenda` | Month view with agenda list | `MonthAgenda` |
| `TimelineViews` | Timeline Day, Week, Work Week | `TimelineViews` |
| `TimelineMonth` | Timeline month view | `TimelineMonth` |
| `TimelineYear` | Timeline year view | `TimelineYear` |
| `Year` | Year view with calendar | `Year` |

**Injection Syntax:**

```tsx
import { ScheduleComponent, Day, Week, WorkWeek, Month, Agenda, Inject } from '@syncfusion/ej2-react-schedule';

<ScheduleComponent>
  <Inject services={[Day, Week, WorkWeek, Month, Agenda]} />
</ScheduleComponent>
```

**Important:** Only the injected views will be available in the Scheduler. If you don't inject a view module, it won't appear in the view options.

## Initialize the Scheduler

Create a basic Scheduler component in your `App.tsx` file:

```tsx
import * as React from 'react';
import { ScheduleComponent, Day, Week, WorkWeek, Month, Agenda, Inject } from '@syncfusion/ej2-react-schedule';
import './App.css';

const App = () => {
  return (
    <ScheduleComponent height="550px">
      <Inject services={[Day, Week, WorkWeek, Month, Agenda]} />
    </ScheduleComponent>
  );
};

export default App;
```

This renders an empty Scheduler with the default week view. To populate it with data, continue to the next section.

## Populating Appointments

Bind appointment data to the Scheduler using the `eventSettings` prop with a `dataSource` property.

**Basic Example:**

```tsx
import * as React from 'react';
import { ScheduleComponent, Day, Week, WorkWeek, Month, Agenda, Inject } from '@syncfusion/ej2-react-schedule';

const App = () => {
  const appointments = [
    {
      Id: 1,
      Subject: 'Team Meeting',
      StartTime: new Date(2026, 2, 25, 10, 0),
      EndTime: new Date(2026, 2, 25, 11, 30),
      IsAllDay: false
    },
    {
      Id: 2,
      Subject: 'Project Review',
      StartTime: new Date(2026, 2, 26, 14, 0),
      EndTime: new Date(2026, 2, 26, 16, 0),
      IsAllDay: false
    }
  ];

  const eventSettings = { dataSource: appointments };

  return (
    <ScheduleComponent 
      height="550px" 
      selectedDate={new Date(2026, 2, 25)}
      eventSettings={eventSettings}
    >
      <Inject services={[Day, Week, WorkWeek, Month, Agenda]} />
    </ScheduleComponent>
  );
};

export default App;
```

**Default Field Names:**

The Scheduler expects the following default field names in your data:

| Field Name | Type | Description |
|------------|------|-------------|
| `Id` | number/string | Unique identifier for the event |
| `Subject` | string | Event title displayed |
| `StartTime` | Date | Event start date and time |
| `EndTime` | Date | Event end date and time |
| `IsAllDay` | boolean | Whether event is all-day (optional) |
| `Location` | string | Event location (optional) |
| `Description` | string | Event details (optional) |
| `RecurrenceRule` | string | Recurrence pattern (optional) |

## Field Mapping

If your data uses different field names, map them using the `fields` property:

```tsx
import * as React from 'react';
import { ScheduleComponent, Day, Week, WorkWeek, Month, Agenda, Inject } from '@syncfusion/ej2-react-schedule';

const App = () => {
  const appointments = [
    {
      EventId: 1,
      Title: 'Conference Call',
      Start: new Date(2026, 2, 25, 10, 0),
      End: new Date(2026, 2, 25, 11, 0),
      AllDay: false,
      Status: 'Confirmed',
      Priority: 'High'
    }
  ];

  const fieldsMapping = {
    id: 'EventId',
    subject: { name: 'Title' },
    startTime: { name: 'Start' },
    endTime: { name: 'End' },
    isAllDay: { name: 'AllDay' }
  };

  const eventSettings = { 
    dataSource: appointments, 
    fields: fieldsMapping 
  };

  return (
    <ScheduleComponent 
      height="550px" 
      selectedDate={new Date(2026, 2, 25)}
      eventSettings={eventSettings}
    >
      <Inject services={[Day, Week, WorkWeek, Month, Agenda]} />
    </ScheduleComponent>
  );
};

export default App;
```

**Field Mapping Structure:**

```tsx
const fields = {
  id: 'YourIdField',
  subject: { name: 'YourSubjectField' },
  startTime: { name: 'YourStartField' },
  endTime: { name: 'YourEndField' },
  isAllDay: { name: 'YourAllDayField' },
  location: { name: 'YourLocationField' },
  description: { name: 'YourDescriptionField' },
  recurrenceRule: { name: 'YourRecurrenceField' }
};
```

## Setting Date

The Scheduler displays the current system date by default. Use the `selectedDate` prop to set a specific date:

```tsx
import * as React from 'react';
import { ScheduleComponent, Day, Week, Month, Inject } from '@syncfusion/ej2-react-schedule';

const App = () => {
  const appointments = [
    {
      Id: 1,
      Subject: 'Conference',
      StartTime: new Date(2026, 2, 15, 10, 0),
      EndTime: new Date(2026, 2, 15, 11, 0)
    }
  ];

  const eventSettings = { dataSource: appointments };

  return (
    <ScheduleComponent 
      height="550px" 
      selectedDate={new Date(2026, 2, 15)}  // March 15, 2026
      eventSettings={eventSettings}
    >
      <Inject services={[Day, Week, Month]} />
    </ScheduleComponent>
  );
};

export default App;
```

The `selectedDate` determines which date/week/month is initially displayed when the Scheduler loads.

## Setting View

The Scheduler displays the Week view by default. Change the active view using the `currentView` prop:

```tsx
import * as React from 'react';
import { ScheduleComponent, Day, Week, WorkWeek, Month, Agenda, Inject } from '@syncfusion/ej2-react-schedule';

const App = () => {
  return (
    <ScheduleComponent 
      height="550px" 
      currentView="Month"  // Set default view to Month
      selectedDate={new Date(2026, 2, 15)}
    >
      <Inject services={[Day, Week, WorkWeek, Month, Agenda]} />
    </ScheduleComponent>
  );
};

export default App;
```

**Available View Values:**
- `Day`
- `Week`
- `WorkWeek`
- `Month`
- `Year`
- `Agenda`
- `MonthAgenda`
- `TimelineDay`
- `TimelineWeek`
- `TimelineWorkWeek`
- `TimelineMonth`
- `TimelineYear`

**Control Available Views:**

Use `ViewsDirective` to specify which views appear in the header toolbar:

```tsx
import * as React from 'react';
import { 
  ScheduleComponent, 
  Day, 
  Week, 
  Month, 
  Inject,
  ViewsDirective, 
  ViewDirective 
} from '@syncfusion/ej2-react-schedule';

const App = () => {
  return (
    <ScheduleComponent 
      height="550px" 
      currentView="Month"
      selectedDate={new Date(2026, 2, 15)}
    >
      <ViewsDirective>
        <ViewDirective option="Day" />
        <ViewDirective option="Week" />
        <ViewDirective option="Month" />
      </ViewsDirective>
      <Inject services={[Day, Week, Month]} />
    </ScheduleComponent>
  );
};

export default App;
```

Only the views specified in `ViewsDirective` will appear as options in the Scheduler header.

## Individual View Customization

Customize each view independently by passing additional props to `ViewDirective`:

```tsx
import * as React from 'react';
import {
  ScheduleComponent,
  WorkWeek,
  Week,
  Month,
  Inject,
  ViewsDirective,
  ViewDirective
} from '@syncfusion/ej2-react-schedule';

const App = () => {
  const appointments = [
    {
      Id: 1,
      Subject: 'Morning Meeting',
      StartTime: new Date(2026, 2, 17, 9, 0),
      EndTime: new Date(2026, 2, 17, 10, 30)
    }
  ];

  const eventSettings = { dataSource: appointments };

  return (
    <ScheduleComponent
      height="550px"
      selectedDate={new Date(2026, 2, 17)}
      eventSettings={eventSettings}
    >
      <ViewsDirective>
        {/* Work Week: 10 AM to 6 PM */}
        <ViewDirective option="WorkWeek" startHour="10:00" endHour="18:00" />
        
        {/* Week: 7 AM to 3 PM */}
        <ViewDirective option="Week" startHour="07:00" endHour="15:00" />
        
        {/* Month: Hide weekends */}
        <ViewDirective option="Month" showWeekend={false} />
      </ViewsDirective>
      <Inject services={[WorkWeek, Week, Month]} />
    </ScheduleComponent>
  );
};

export default App;
```

**Common View-Specific Props:**

| Prop | Type | Description |
|------|------|-------------|
| `startHour` | string | Start time for day views (e.g., "08:00") |
| `endHour` | string | End time for day views (e.g., "18:00") |
| `timeScale` | object | Timescale configuration (interval, slotCount) |
| `showWeekend` | boolean | Show/hide weekend days (Month view) |
| `interval` | number | Number of days/weeks/months to display |
| `readonly` | boolean | Make specific view read-only |

**Example: Different Working Hours Per View**

```tsx
<ViewsDirective>
  {/* Office hours */}
  <ViewDirective option="WorkWeek" startHour="09:00" endHour="17:00" />
  
  {/* Extended hours for special events */}
  <ViewDirective option="Week" startHour="06:00" endHour="22:00" />
  
  {/* Compact month view without weekends */}
  <ViewDirective option="Month" showWeekend={false} />
</ViewsDirective>
```

This allows you to tailor the Scheduler display for different scheduling scenarios within the same application.
