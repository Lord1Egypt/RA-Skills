# Views and Navigation

## Table of Contents
- [Overview](#overview)
- [Calendar Views](#calendar-views)
  - [Day View](#day-view)
  - [Week View](#week-view)
  - [Work Week View](#work-week-view)
  - [Month View](#month-view)
  - [Year View](#year-view)
  - [Agenda View](#agenda-view)
  - [Month Agenda View](#month-agenda-view)
- [Timeline Views](#timeline-views)
  - [Timeline Day](#timeline-day)
  - [Timeline Week](#timeline-week)
  - [Timeline Work Week](#timeline-work-week)
  - [Timeline Month](#timeline-month)
  - [Timeline Year](#timeline-year)
- [Setting Active View](#setting-active-view)
- [View Configuration](#view-configuration)
- [Extending View Intervals](#extending-view-intervals)
- [Navigation](#navigation)

## Overview

The Scheduler includes a wide variety of view modes, each with unique configuration options. By default, the `Week` view is active when the Scheduler loads. The available built-in view modes are:

**Calendar Views:**
- Day
- Week
- Work Week
- Month
- Year
- Agenda
- Month-Agenda

**Timeline Views:**
- Timeline Day
- Timeline Week
- Timeline Work Week
- Timeline Month
- Timeline Year

To navigate between views and dates, use the navigation options on the Scheduler header bar. The active view is highlighted by default, and its date range is displayed on the left. Clicking the date range opens a calendar popup to easily select a different date.

## Calendar Views

### Day View

The Day view displays a single day by default with all its appointments displayed vertically along time slots. You can configure it to show multiple days by setting the `interval` property within the corresponding `ViewDirective`.

**Configuring Day View:**

```tsx
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import {
  ScheduleComponent, Day, Inject,
  ViewsDirective, ViewDirective
} from '@syncfusion/ej2-react-schedule';
import { appData } from './datasource';

const App = () => {
  const eventSettings = { dataSource: appData };
  const timeScale = { enable: true, slotCount: 5 };

  return <ScheduleComponent width='100%' height='550px' selectedDate={new Date(2018, 1, 15)}
    eventSettings={eventSettings}>
    <ViewsDirective>
      <ViewDirective option='Day' startHour='09:30' endHour='18:00' timeScale={timeScale} />
    </ViewsDirective>
    <Inject services={[Day]} />
  </ScheduleComponent>
};
const root = ReactDOM.createRoot(document.getElementById('schedule'));
root.render(<App />);
```

The Day view supports all view properties except `allowVirtualScrolling` and `headerRows`.

### Week View

The Week view displays a count of 7 days (from Sunday to Saturday) with all its related appointments. The first day of the week can be changed using the `firstDayOfWeek` property which accepts integer values (Sunday=0, Monday=1, Tuesday=2, and so on). You can navigate to a particular date in day view from the week view by clicking on the appropriate dates on the date header bar.

**Configuring Week View:**

```tsx
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import {
  ScheduleComponent, Day, Week, Inject,
  ViewsDirective, ViewDirective
} from '@syncfusion/ej2-react-schedule';
import { appData } from './datasource';

const App = () => {
  const eventSettings = { dataSource: appData };
  const timeScale = { enable: true, slotCount: 5 };

  return (<ScheduleComponent width='100%' height='550px' selectedDate={new Date(2018, 1, 15)}
    eventSettings={eventSettings}>
    <ViewsDirective>
      <ViewDirective option='Day' interval={2} displayName='2 Days' startHour='09:30' endHour='18:00' timeScale={timeScale} />
      <ViewDirective option='Week' interval={2} displayName='2 Weeks' showWeekend={false} isSelected={true} />
    </ViewsDirective>
    <Inject services={[Day, Week]} />
  </ScheduleComponent>)
};
const root = ReactDOM.createRoot(document.getElementById('schedule'));
root.render(<App />);
```

### Work Week View

The Work Week view displays only the working days of a week (count of 5 days) and its associated appointments. It is possible to customize the working days on the work week view by using the `workDays` property which accepts an array of integer values (Sunday=0, Monday=1, Tuesday=2, and so on). By default, it displays from Monday to Friday (5 days). You can navigate to a particular date in the day view from the work week view by clicking on the appropriate dates in the date header bar.

**Configuring Work Week View:**

```tsx
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import {
  ScheduleComponent, WorkWeek, Inject,
  ViewsDirective, ViewDirective
} from '@syncfusion/ej2-react-schedule';
import { appData } from './datasource';

const App = () => {
  const eventSettings = { dataSource: appData };
  const workDays: number[] = [2, 3, 5];

  return (<ScheduleComponent width='100%' height='550px' selectedDate={new Date(2018, 1, 15)}
    eventSettings={eventSettings}>
    <ViewsDirective>
      <ViewDirective option='WorkWeek' workDays={workDays} />
    </ViewsDirective>
    <Inject services={[WorkWeek]} />
  </ScheduleComponent>)
};
const root = ReactDOM.createRoot(document.getElementById('schedule'));
root.render(<App />);
```

The Day, Week, and Work Week views can display all-day appointments in a separate row with an expand/collapse option.

### Month View

The Month view displays all the days of a particular month with their corresponding appointments. You can navigate to the Day view of a particular date by clicking on its date number in the month cell.

By default, when you create an appointment through Month view, it is considered as created for an entire day. You can explicitly change this behavior by unchecking the `All-day` option from editor window, so that it defaults to the start time duration as 9:00 AM and end time as 9:30 AM.

The `+ more` text indicator appears on each day cell of a Month view when there are multiple appointments. Clicking on it allows you to view the hidden appointments of that day.

**Configuring Month View:**

```tsx
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import {
  ScheduleComponent, Month, Inject,
  ViewsDirective, ViewDirective
} from '@syncfusion/ej2-react-schedule';
import { appData } from './datasource';

const App = () => {
  const eventSettings = { dataSource: appData };

  return (<ScheduleComponent width='100%' height='550px' selectedDate={new Date(2018, 1, 15)}
    eventSettings={eventSettings}>
    <ViewsDirective>
      <ViewDirective option='Month' showWeekNumber={true} readonly={true} />
    </ViewsDirective>
    <Inject services={[Month]} />
  </ScheduleComponent>)
};
const root = ReactDOM.createRoot(document.getElementById('schedule'));
root.render(<App />);
```

### Year View

The Year view displays all the days of a particular year with months and all its related appointments. You can navigate to a particular date in the day view by clicking on the appropriate date text on the year cells.

The Year view supports both `Horizontal` and `Vertical` orientations, which can be configured using the `orientation` property within the views definition.

**Configuring Year View:**

```tsx
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import {
  ScheduleComponent, Year, Inject,
  ViewsDirective, ViewDirective
} from '@syncfusion/ej2-react-schedule';
import { appData } from './datasource';

const App = () => {
  const eventSettings = { dataSource: appData };

  return <ScheduleComponent width='100%' height='550px' selectedDate={new Date(2018, 1, 15)}
    eventSettings={eventSettings}>
    <ViewsDirective>
      <ViewDirective option='Year' showWeekNumber={true} readonly={true} />
    </ViewsDirective>
    <Inject services={[Year]} />
  </ScheduleComponent>
};
const root = ReactDOM.createRoot(document.getElementById('schedule'));
root.render(<App />);
```

The Year view has built-in module support, presenting all months of a year in a calendar format where dates with appointments are highlighted.

### Agenda View

The Agenda view lists appointments in a grid-like format, showing the next 7 days by default. This duration can be customized with the `agendaDaysCount` property. It supports virtual scrolling when the `allowVirtualScrolling` property is enabled. Additionally, the `hideEmptyAgendaDays` property can be used to hide days that have no appointments.

**Configuring Agenda View:**

```tsx
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import {
  ScheduleComponent, Agenda, Inject,
  ViewsDirective, ViewDirective
} from '@syncfusion/ej2-react-schedule';
import { appData } from './datasource';
import { Internationalization } from '@syncfusion/ej2-base';

const App = () => {
  const eventSettings = { dataSource: appData };

  const instance: Internationalization = new Internationalization();
  const getTimeString = (value: Date) => {
    return instance.formatDate(value, { skeleton: 'hm' });
  }
  const eventTemplate = (props): JSX.Element => {
    return (<div className="template-wrap">
      <div className="subject">{props.Subject}</div>
      <div className="time">
        Time: {getTimeString(props.StartTime)} - {getTimeString(props.EndTime)}</div>
    </div>
    );
  }
  return (<ScheduleComponent width='100%' height='550px' agendaDaysCount={3} selectedDate={new Date(2018, 1, 15)}
    eventSettings={eventSettings}>
    <ViewsDirective>
      <ViewDirective option='Agenda' eventTemplate={eventTemplate} allowVirtualScrolling={false} />
    </ViewsDirective>
    <Inject services={[Agenda]} />
  </ScheduleComponent>)
};
const root = ReactDOM.createRoot(document.getElementById('schedule'));
root.render(<App />);
```

For the Agenda view, it is mandatory to set a specific height (in pixels) for the Scheduler component.

### Month Agenda View

The Month Agenda view combines a month calendar with an agenda list. Clicking a date in the calendar displays that day's appointments in the list below. Dates containing appointments are marked with a dot indicator.

**Configuring Month Agenda View:**

```tsx
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import {
  ScheduleComponent, MonthAgenda, Inject,
  ViewsDirective, ViewDirective
} from '@syncfusion/ej2-react-schedule';
import { appData } from './datasource';

const App = () => {
  const eventSettings = { dataSource: appData };
  const workDays: number[] = [1, 2, 3];

  return (<ScheduleComponent width='100%' height='550px' selectedDate={new Date(2018, 1, 14)}
    eventSettings={eventSettings}>
    <ViewsDirective>
      <ViewDirective option='MonthAgenda' showWeekend={false} workDays={workDays} />
    </ViewsDirective>
    <Inject services={[MonthAgenda]} />
  </ScheduleComponent>)
};
const root = ReactDOM.createRoot(document.getElementById('schedule'));
root.render(<App />);
```

## Timeline Views

Timeline views display appointments horizontally along time slots. They are ideal for showing multiple resources or extended time ranges.

### Timeline Day

Similar to the day view, Timeline Day shows a single day with all its appointments where the time slots are displayed horizontally. By default, the cell height adjusts as per the height set to Scheduler. When the number of appointments exceeds the visible area of the cells, the `+ more` text indicator will be displayed at the bottom to denote the presence of additional appointments.

To use Timeline Day view, you must import and inject the `TimelineViews` module from the `ej2-react-schedule` package.

**Configuring Timeline Day:**

```tsx
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import {
  ScheduleComponent, TimelineViews, Inject,
  ViewsDirective, ViewDirective
} from '@syncfusion/ej2-react-schedule';
import { appData } from './datasource';

const App = () => {
  const eventSettings = { dataSource: appData };

  return (<ScheduleComponent width='100%' height='550px' selectedDate={new Date(2018, 1, 15)}
    eventSettings={eventSettings}>
    <ViewsDirective>
      <ViewDirective option='TimelineDay' startHour='10:00' endHour='15:30' />
    </ViewsDirective>
    <Inject services={[TimelineViews]} />
  </ScheduleComponent>)
};
const root = ReactDOM.createRoot(document.getElementById('schedule'));
root.render(<App />);
```

### Timeline Week

Similar to the standard Week view, the Timeline Week view shows 7 days with associated appointments and horizontal time slots.

**Configuring Timeline Week:**

```tsx
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import {
  ScheduleComponent, TimelineViews, Inject,
  ViewsDirective, ViewDirective
} from '@syncfusion/ej2-react-schedule';
import { appData } from './datasource';

const App = () => {
  const eventSettings = { dataSource: appData };

  return <ScheduleComponent width='100%' height='550px' selectedDate={new Date(2018, 1, 15)}
    eventSettings={eventSettings}>
    <ViewsDirective>
      <ViewDirective option='TimelineWeek' timeScale={{ enable: false }} />
    </ViewsDirective>
    <Inject services={[TimelineViews]} />
  </ScheduleComponent>
};
const root = ReactDOM.createRoot(document.getElementById('schedule'));
root.render(<App />);
```

### Timeline Work Week

The Timeline Work Week view displays only the working days with horizontal time slots.

**Configuring Timeline Work Week:**

```tsx
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import {
  ScheduleComponent, TimelineViews, Agenda, Inject,
  ViewsDirective, ViewDirective
} from '@syncfusion/ej2-react-schedule';
import { appData } from './datasource';

const App = () => {
  const eventSettings = { dataSource: appData };
  const workDays: number[] = [2, 3, 5];

  return (<ScheduleComponent width='100%' height='550px' selectedDate={new Date(2018, 1, 15)}
    eventSettings={eventSettings}>
    <ViewsDirective>
      <ViewDirective option='TimelineWorkWeek' interval={3} workDays={workDays} dateFormat='dd-MMM-yyyy' />
      <ViewDirective option='Agenda' />
    </ViewsDirective>
    <Inject services={[TimelineViews, Agenda]} />
  </ScheduleComponent>)
};
const root = ReactDOM.createRoot(document.getElementById('schedule'));
root.render(<App />);
```

Clicking on dates in the header of Timeline Day, Week, and Work Week views navigates to the Agenda view for that day.

### Timeline Month

The Timeline Month view displays the current month days along with its appointments in a horizontal layout. To make use of the Timeline Month view, you must import and inject the `TimelineMonth` module from the `ej2-react-schedule` package.

**Configuring Timeline Month:**

```tsx
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import {
  ScheduleComponent, TimelineMonth, TimelineViews, Inject,
  ViewsDirective, ViewDirective
} from '@syncfusion/ej2-react-schedule';
import { appData } from './datasource';

const App = () => {
  const eventSettings = { dataSource: appData };

  return (<ScheduleComponent width='100%' height='550px' selectedDate={new Date(2018, 1, 15)}
    eventSettings={eventSettings}>
    <ViewsDirective>
      <ViewDirective option='TimelineMonth' showWeekend={false} />
      <ViewDirective option='TimelineDay' />
    </ViewsDirective>
    <Inject services={[TimelineMonth, TimelineViews]} />
  </ScheduleComponent>)
};
const root = ReactDOM.createRoot(document.getElementById('schedule'));
root.render(<App />);
```

Clicking a date in the header of the Timeline Month view navigates to the Timeline Day view.

### Timeline Year

In Timeline Year view, each row depicts a single resource. Whereas in the vertical view, each resource is grouped parallelly as columns. Here, the resource grouping follows the tree-view like hierarchical grouping structure and can contain any level of child resources.

To use the Timeline Year view, import and inject the `TimelineYear` module from the `ej2-react-schedule` package.

**Configuring Timeline Year:**

```tsx
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import {
  ScheduleComponent, TimelineYear, Inject,
  ViewsDirective, ViewDirective
} from '@syncfusion/ej2-react-schedule';
import { appData } from './datasource';

const App = () => {
  const eventSettings = { dataSource: appData };

  return (<ScheduleComponent width='100%' height='550px' selectedDate={new Date(2018, 1, 15)}
    eventSettings={eventSettings}>
    <ViewsDirective>
      <ViewDirective option='TimelineYear' displayName='Horizontal Timeline Year' isSelected={true} />
      <ViewDirective option='TimelineYear' displayName='Vertical Timeline Year' orientation='Vertical'/>
    </ViewsDirective>
    <Inject services={[TimelineYear]} />
  </ScheduleComponent>)
};
const root = ReactDOM.createRoot(document.getElementById('schedule'));
root.render(<App />);
```

**Resource Grouping in Timeline Year:**

```tsx
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import {
  ScheduleComponent, TimelineYear, ViewsDirective, ViewDirective,
  ResourcesDirective, ResourceDirective, Inject, EventSettingsModel, GroupModel
} from '@syncfusion/ej2-react-schedule';
import { resourceData } from './datasource';

const App = () => {
  const eventSettings: EventSettingsModel = { dataSource: resourceData };
  const group: GroupModel = { resources: ['Owners'] };

  const ownerData: Object[] = [
    { OwnerText: 'Nancy', Id: 1, OwnerColor: '#ffaa00' },
    { OwnerText: 'Steven', Id: 2, OwnerColor: '#f8a398' },
    { OwnerText: 'Michael', Id: 3, OwnerColor: '#7499e1' }
  ];

  return (<ScheduleComponent width='100%' height='550px' selectedDate={new Date(2018, 3, 1)} eventSettings={eventSettings} >
    <ViewsDirective>
      <ViewDirective option='TimelineYear' displayName='Horizontal Timeline Year' isSelected={true} group={group} />
      <ViewDirective option='TimelineYear' displayName='Vertical Timeline Year' orientation='Vertical' group={group} />
    </ViewsDirective>
    <ResourcesDirective>
      <ResourceDirective field='OwnerId' title='Owner' name='Owners' allowMultiple={true}
        dataSource={ownerData} textField='OwnerText' idField='Id' colorField='OwnerColor'>
      </ResourceDirective>
    </ResourcesDirective>
    <Inject services={[TimelineYear]} />
  </ScheduleComponent>)
};
const root = ReactDOM.createRoot(document.getElementById('schedule'));
root.render(<App />);
```

**Auto Row Height:**

Timeline Year view supports auto row height. When the `rowAutoHeight` feature is enabled, the row height gets auto-adjusted based on the number of overlapping events occupied in the same time range. If you disable auto row height, the `+ more` text indicator appears on each day cell, clicking on which allows you to view the hidden appointments.

```tsx
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { ScheduleComponent, TimelineYear, Inject, ViewsDirective, ViewDirective, EventSettingsModel } from '@syncfusion/ej2-react-schedule';
import { scheduleData } from './datasource';

const App = () => {
  const eventSettings: EventSettingsModel = { dataSource: scheduleData }

  return (<ScheduleComponent width='100%' height='550px' currentView='Month'
    selectedDate={new Date(2018, 1, 17)} rowAutoHeight={true} eventSettings={eventSettings}>
    <ViewsDirective>
      <ViewDirective option='TimelineYear' displayName='Horizontal Timeline Year' isSelected={true} />
      <ViewDirective option='TimelineYear' displayName='Vertical Timeline Year' orientation='Vertical' />
    </ViewsDirective>
    <Inject services={[TimelineYear]} />
  </ScheduleComponent>)
};
const root = ReactDOM.createRoot(document.getElementById('schedule'));
root.render(<App />);
```

## Setting Active View

The Scheduler displays the `Week` view by default. To change the active view, set the `currentView` property to the desired view name. The applicable view names that the Scheduler accepts are:

- Day
- Week
- WorkWeek
- Month
- Year
- Agenda
- MonthAgenda
- TimelineDay
- TimelineWeek
- TimelineWorkWeek
- TimelineMonth
- TimelineYear

To use these view modes, you must import and inject the corresponding modules. You can also define a specific set of views and configure them individually using the `views` property.

**Example - Configuring Multiple Views:**

```tsx
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import {
  ScheduleComponent, Week, Month, TimelineViews, TimelineMonth, Inject,
  ViewsDirective, ViewDirective
} from '@syncfusion/ej2-react-schedule';
import { appData } from './datasource';

const App = () => {
  const eventSettings = { dataSource: appData }

  return (<ScheduleComponent width='100%' height='550px' selectedDate={new Date(2018, 1, 15)} eventSettings={eventSettings} >
    <ViewsDirective>
      <ViewDirective option='Week' />
      <ViewDirective option='TimelineWeek' />
      <ViewDirective option='Month' />
      <ViewDirective option='TimelineMonth' />
    </ViewsDirective>
    <Inject services={[Week, Month, TimelineViews, TimelineMonth]} />
  </ScheduleComponent>)
};
const root = ReactDOM.createRoot(document.getElementById('schedule'));
root.render(<App />);
```

By default, the Scheduler is configured with Day, Week, Work Week, Month, and Agenda views. Other views, such as Timeline views, can be enabled by injecting their specific modules.

`ViewDirective` and `ViewsDirective` must be imported from the package to define views.

## View Configuration

Each view can be configured with its own set of properties. To apply view-specific settings, define the desired properties within the corresponding `ViewDirective` tag inside the views collection.

**Available View Properties:**

| Property | Type | Description | Applicable Views |
|----------|------|-------------|------------------|
| `option` | View | Accepts the Scheduler view name (Day, Week, Month, etc.) | All views |
| `isSelected` | Boolean | Similar to `currentView`, defines the active view of the Scheduler | All views |
| `dateFormat` | String | Defines the date format for the specific view | All views |
| `readonly` | Boolean | When set to `true`, prevents CRUD actions on the view | All views |
| `resourceHeaderTemplate` | String | Template to customize resource header cells | All views |
| `dateHeaderTemplate` | String | Template to customize date header cells | All views |
| `eventTemplate` | String | Template to customize event backgrounds | All views |
| `showWeekend` | Boolean | When `false`, hides weekend days | All views |
| `group` | GroupModel | Sets different resource grouping options | All views |
| `cellTemplate` | String | Template to customize work cells | All views except Agenda |
| `workDays` | Number[] | Sets the working days on the view | All views except Agenda |
| `displayName` | String | Sets a custom display name for the view | All views except Agenda and Month Agenda |
| `interval` | Number | Customizes views with different sets of days, weeks, or months | All views except Agenda and Month Agenda |
| `startHour` | String | Specifies the start hour for the Scheduler | Day, Week, Work Week, Timeline Day, Timeline Week, Timeline Work Week |
| `endHour` | String | Specifies the end hour for the Scheduler | Day, Week, Work Week, Timeline Day, Timeline Week, Timeline Work Week |
| `timeScale` | TimeScaleModel | Sets different timescale configurations | Day, Week, Work Week, Timeline Day, Timeline Week, Timeline Work Week |
| `showWeekNumber` | Boolean | Shows week number on respective weeks | Day, Week, Work Week, Month |
| `allowVirtualScrolling` | Boolean | Enables or disables virtual scrolling | Agenda and Timeline views |
| `headerRows` | HeaderRowsModel | Defines custom header rows on timeline views | All timeline views |

**Example - View-Specific Configuration:**

```tsx
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import {
  ScheduleComponent, Day, Week, Month, Inject,
  ViewsDirective, ViewDirective
} from '@syncfusion/ej2-react-schedule';
import { appData } from './datasource';

const App = () => {
  const eventSettings = { dataSource: appData }

  return (<ScheduleComponent width='100%' height='550px' selectedDate={new Date(2018, 1, 15)} eventSettings={eventSettings} >
    <ViewsDirective>
      <ViewDirective option='Week' dateFormat='dd-MMM-yyyy' />
      <ViewDirective option='Month' showWeekend={false} readonly={true} />
    </ViewsDirective>
    <Inject services={[Week, Month]} />
  </ScheduleComponent>)
};
const root = ReactDOM.createRoot(document.getElementById('schedule'));
root.render(<App />);
```

In this example, the Week view displays dates in `dd-MMM-yyyy` format, while the Month view hides weekend days and is set to read-only mode.

## Extending View Intervals

You can customize the display of default number of days on different Scheduler view modes. For example, a day view can be extended to display 3 days by setting the `interval` option as 3 for the Day option within the `ViewDirective`. In the same way, you can also display 2 weeks by setting interval 2 for the Week option.

You can provide an alternative display name for such customized views on the Scheduler header bar by setting the appropriate `displayName` property.

**Example - Extended View Intervals:**

```tsx
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import {
  ScheduleComponent, Day, Week, Inject,
  ViewsDirective, ViewDirective
} from '@syncfusion/ej2-react-schedule';
import { appData } from './datasource';

const App = () => {
  const eventSettings = { dataSource: appData };

  return (<ScheduleComponent width='100%' height='550px' selectedDate={new Date(2018, 1, 15)}
    eventSettings={eventSettings}>
    <ViewsDirective>
      <ViewDirective option='Day' interval={3} displayName='3 Days' />
      <ViewDirective option='Week' interval={2} displayName='2 Weeks' />
    </ViewsDirective>
    <Inject services={[Day, Week]} />
  </ScheduleComponent>)
};
const root = ReactDOM.createRoot(document.getElementById('schedule'));
root.render(<App />);
```

View intervals can be extended on all Scheduler view modes except Agenda and Month-Agenda.

## Navigation

The Scheduler provides intuitive navigation options to move between views and dates:

**Header Bar Navigation:**
- The active view is highlighted in the header toolbar
- The current date range is displayed on the left side of the header
- Clicking the date range opens a calendar popup for easy date selection
- Use the previous/next arrows to navigate to adjacent time periods

**View Switching:**
- Click on any view name in the header toolbar to switch to that view
- The view changes immediately while maintaining the current date context
- Use the `isSelected` property to set the default active view

**Date Navigation from Views:**
- **Month View**: Click on a date number to navigate to Day view for that date
- **Year View**: Click on any date text to navigate to Day view for that date
- **Timeline Day/Week/Work Week**: Click on header dates to navigate to Agenda view for that day
- **Timeline Month**: Click on a header date to navigate to Timeline Day view
- **Week/Work Week**: Click on date headers to navigate to Day view

This comprehensive navigation system enables users to efficiently browse through different time periods and view modes while maintaining context of their current position in the schedule.
