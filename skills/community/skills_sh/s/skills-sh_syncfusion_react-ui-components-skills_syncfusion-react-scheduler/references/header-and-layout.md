# Header and Layout

## Table of Contents
- [Overview](#overview)
- [Header Bar](#header-bar)
  - [Show or Hide Header Bar](#show-or-hide-header-bar)
  - [Customizing Header Bar Using Template](#customizing-header-bar-using-template)
  - [Customizing Header Bar Using Event](#customizing-header-bar-using-event)
  - [Display View Options in Header Bar Popup](#display-view-options-in-header-bar-popup)
  - [Date Header Customization](#date-header-customization)
  - [Customizing Date Range Text](#customizing-date-range-text)
  - [Customizing Header Indent Cells](#customizing-header-indent-cells)
- [Header Rows](#header-rows)
  - [Available Header Row Types](#available-header-row-types)
  - [Display Year and Month Rows](#display-year-and-month-rows)
  - [Display Week Numbers](#display-week-numbers)
  - [Display Full Year in Timeline](#display-full-year-in-timeline)
  - [Customizing Header Rows with Templates](#customizing-header-rows-with-templates)
- [Dimensions](#dimensions)
  - [Auto Height and Width](#auto-height-and-width)
  - [Height and Width in Pixels](#height-and-width-in-pixels)
  - [Height and Width in Percentages](#height-and-width-in-percentages)
- [Row Auto Height](#row-auto-height)
  - [Calendar Month View](#calendar-month-view-auto-height)
  - [Timeline Views](#timeline-views-auto-height)
  - [Timeline with Multiple Resources](#timeline-with-multiple-resources)
  - [Appointments Occupying Entire Cell](#appointments-occupying-entire-cell)
- [Responsive Layout](#responsive-layout)
- [Mobile Rendering](#mobile-rendering)

## Overview

The Syncfusion React Scheduler provides comprehensive customization options for header and layout features. This includes customizing the header bar, configuring additional header rows for Timeline views, setting dimensions, and enabling row auto-height adjustments. These features allow you to create a flexible and responsive scheduler that adapts to various display requirements and data volumes.

Key layout features include:
- **Header Bar Customization**: Control toolbar visibility, add custom items, and customize date navigation
- **Header Rows**: Add additional temporal rows (Year, Month, Week, Date, Hour) in Timeline views
- **Dimensions Control**: Set scheduler size using auto, pixel, or percentage values
- **Row Auto Height**: Automatically adjust row heights based on appointment count
- **Responsive Design**: Built-in adaptive UI for mobile and desktop experiences

## Header Bar

The header bar is the top section of the Scheduler that contains date navigation, view switchers, and other toolbar items. It can be fully customized to match your application requirements.

### Show or Hide Header Bar

By default, the header bar displays date and view navigation options. You can hide it using the `showHeaderBar` property set to `false` (default is `true`).

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
      showHeaderBar={false} 
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

### Customizing Header Bar Using Template

Add custom items to the Scheduler header bar using the `toolbarItems` property with `ToolbarItemsDirective`. Each item requires a `name` field for default items like `Previous`, `Next`, `Today`, `DateRangeText`, `NewEvent`, and `Views`. Custom items should use `Custom` as the name.

```tsx
import { useRef } from 'react';
import * as React from 'react';
import { 
  ScheduleComponent, EventSettingsModel, ViewsDirective, ViewDirective,
  ResourcesDirective, ResourceDirective, Month, Inject, Resize, 
  DragAndDrop, ToolbarItemsDirective, ToolbarItemDirective 
} from '@syncfusion/ej2-react-schedule';
import { DropDownListComponent, ChangeEventArgs } from '@syncfusion/ej2-react-dropdowns';
import { Predicate, Query } from '@syncfusion/ej2-data';
import { scheduleData } from './datasource';

const App = () => {
  const schedule = useRef<ScheduleComponent>(null);
  const eventSettings: EventSettingsModel = { 
    dataSource: scheduleData, 
    query: new Query().where('OwnerId', 'equal', 1) 
  };
  
  const ownerData: { [key: string]: Object }[] = [
    { OwnerText: 'Margaret', OwnerId: 1, Color: '#ea7a57' },
    { OwnerText: 'Robert', OwnerId: 2, Color: '#df5286' },
    { OwnerText: 'Laura', OwnerId: 3, Color: '#865fcf' }
  ];
  
  const fields: object = { text: 'OwnerText', value: 'OwnerId' };

  const template = () => {
    return (
      <DropDownListComponent 
        id='ddlelement' 
        dataSource={ownerData} 
        fields={fields} 
        value={1} 
        change={OnChange} 
      />
    );
  };

  const OnChange = (args: ChangeEventArgs) => {
    let predicate: Predicate;
    predicate = new Predicate('OwnerId', 'equal', parseInt(args.value as string, 10));
    if (schedule.current) {
      schedule.current.eventSettings.query = new Query().where(predicate);
    }
  };

  return (
    <ScheduleComponent 
      width='100%' 
      height='650px' 
      ref={schedule} 
      selectedDate={new Date(2024, 11, 15)} 
      eventSettings={eventSettings}
    >
      <ResourcesDirective>
        <ResourceDirective 
          field='OwnerId' 
          title='Owner' 
          name='Owners' 
          dataSource={ownerData} 
          textField='OwnerText' 
          idField='OwnerId' 
          colorField='Color'
        />
      </ResourcesDirective>
      <ViewsDirective>
        <ViewDirective option='Month' />
      </ViewsDirective>
      <Inject services={[Month, Resize, DragAndDrop]} />
      <ToolbarItemsDirective>
        <ToolbarItemDirective name='Previous' align='Left' />
        <ToolbarItemDirective name='Next' align='Left' />
        <ToolbarItemDirective name='DateRangeText' align='Left' />
        <ToolbarItemDirective name='Today' align='Right' />
        <ToolbarItemDirective align='Center' template={template} />
      </ToolbarItemsDirective>
    </ScheduleComponent>
  );
};

export default App;
```

### Customizing Header Bar Using Event

Use the `actionBegin` event to add custom items dynamically to the header bar. This example adds a user profile image that displays a popup on click.

```tsx
import { useRef, useEffect } from 'react';
import * as React from 'react';
import {
  ScheduleComponent, ViewsDirective, ViewDirective, Month, Inject,
  ActionEventArgs, ToolbarActionArgs, EventSettingsModel
} from '@syncfusion/ej2-react-schedule';
import { createElement, compile } from '@syncfusion/ej2-base';
import { ItemModel } from '@syncfusion/ej2-react-navigations';
import { Popup } from '@syncfusion/ej2-popups';
import { scheduleData } from './datasource';

const App = () => {
  const schedule = useRef<ScheduleComponent>(null);
  const eventSettings: EventSettingsModel = { dataSource: scheduleData };
  let profilePopup: Popup;
  
  const onActionBegin = (args: ActionEventArgs & ToolbarActionArgs): void => {
    if (args.requestType === 'toolbarItemRendering') {
      const userIconItem: ItemModel = {
        align: 'Right', 
        prefixIcon: 'user-icon', 
        text: 'Nancy', 
        cssClass: 'e-schedule-user-icon'
      };
      args.items.push(userIconItem);
    }
  };

  const onActionComplete = (args: ActionEventArgs): void => {
    const scheduleElement: HTMLElement = document.getElementById('schedule');
    if (args.requestType === 'toolBarItemRendered' && scheduleElement) {
      const userIconEle: HTMLElement = scheduleElement.querySelector('.e-schedule-user-icon');
      if (userIconEle) {
        userIconEle.onclick = () => {
          if (profilePopup) {
            profilePopup.relateTo = userIconEle;
            profilePopup.dataBind();
            profilePopup.element.classList.contains('e-popup-close') 
              ? profilePopup.show() 
              : profilePopup.hide();
          }
        };
      }
    }
  };

  return (
    <ScheduleComponent 
      cssClass='schedule-header-bar' 
      width='100%' 
      height='550px' 
      ref={schedule}
      selectedDate={new Date(2018, 1, 15)} 
      eventSettings={eventSettings}
      actionBegin={onActionBegin} 
      actionComplete={onActionComplete}
    >
      <ViewsDirective>
        <ViewDirective option='Month' />
      </ViewsDirective>
      <Inject services={[Month]} />
    </ScheduleComponent>
  );
};

export default App;
```

### Display View Options in Header Bar Popup

For adaptive UI on mobile devices, move view options to a header bar popup by setting `enableAdaptiveUI` to `true`.

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
      height='500px' 
      selectedDate={new Date(2018, 1, 15)} 
      enableAdaptiveUI={true} 
      eventSettings={eventSettings}
    >
      <Inject services={[Day, Week, WorkWeek, Month, Agenda]} />
    </ScheduleComponent>
  );
};

export default App;
```

### Date Header Customization

Customize date header cells in Day, Week, WorkWeek, and Timeline views using the `dateHeaderTemplate` option.

```tsx
import * as React from 'react';
import { 
  ScheduleComponent, ViewsDirective, ViewDirective, 
  Day, Week, WorkWeek, Inject, TimelineViews 
} from '@syncfusion/ej2-react-schedule';
import { scheduleData } from './datasource';
import { Internationalization } from '@syncfusion/ej2-base';

const App = () => {
  const eventSettings = { dataSource: scheduleData };
  const instance: Internationalization = new Internationalization();
  
  const getDateHeaderText = (value: Date): string => {
    return instance.formatDate(value, { skeleton: 'Ed' });
  };
  
  const getWeather = (value: Date) => {
    const weatherMap = {
      0: '25°C', 1: '18°C', 2: '10°C', 3: '16°C',
      4: '8°C', 5: '27°C', 6: '17°C'
    };
    return `<div class="weather-text">${weatherMap[value.getDay()]}</div>`;
  };
  
  const dateHeaderTemplate = (props): JSX.Element => {
    return (
      <div>
        <div>{getDateHeaderText(props.date)}</div>
        <div 
          className="date-text" 
          dangerouslySetInnerHTML={{ __html: getWeather(props.date) }}
        />
      </div>
    );
  };

  return (
    <ScheduleComponent 
      width='100%' 
      height='550px' 
      cssClass='schedule-date-header-template'
      selectedDate={new Date(2018, 1, 15)} 
      eventSettings={eventSettings}
      dateHeaderTemplate={dateHeaderTemplate}
    >
      <ViewsDirective>
        <ViewDirective option='Day' />
        <ViewDirective option='Week' />
        <ViewDirective option='WorkWeek' />
        <ViewDirective option='TimelineWeek' />
      </ViewsDirective>
      <Inject services={[Day, Week, WorkWeek, TimelineViews]} />
    </ScheduleComponent>
  );
};

export default App;
```

For Month view, use the `renderCell` event to customize date headers:

```tsx
import * as React from 'react';
import { 
  ScheduleComponent, ViewsDirective, ViewDirective, 
  Month, RenderCellEventArgs, Inject 
} from '@syncfusion/ej2-react-schedule';
import { scheduleData } from './datasource';

const App = () => {
  const eventSettings = { dataSource: scheduleData };
  
  const getWeather = (value: Date) => {
    const weatherMap = {
      0: '25°C', 1: '18°C', 2: '10°C', 3: '16°C',
      4: '8°C', 5: '27°C', 6: '17°C'
    };
    return `<div class="weather-text">${weatherMap[value.getDay()]}</div>`;
  };
  
  const onRenderCell = (args: RenderCellEventArgs): void => {
    if (args.elementType === 'monthCells') {
      let ele: Element = document.createElement('div');
      ele.innerHTML = getWeather(args.date);
      args.element.appendChild(ele.firstChild);
    }
  };

  return (
    <ScheduleComponent 
      width='100%' 
      height='550px' 
      cssClass='schedule-date-header-template'
      renderCell={onRenderCell} 
      selectedDate={new Date(2018, 1, 15)} 
      eventSettings={eventSettings}
    >
      <ViewsDirective>
        <ViewDirective option='Month' />
      </ViewsDirective>
      <Inject services={[Month]} />
    </ScheduleComponent>
  );
};

export default App;
```

### Customizing Date Range Text

Customize the date range text displayed in the header bar using the `dateRangeTemplate` option.

```tsx
import * as React from 'react';
import { 
  ScheduleComponent, ViewsDirective, ViewDirective, 
  Day, Week, WorkWeek, Inject, TimelineViews 
} from '@syncfusion/ej2-react-schedule';
import { Internationalization } from '@syncfusion/ej2-base';

const App = () => {
  const instance: Internationalization = new Internationalization();
  
  const getDateRange = (startDate: Date, endDate: Date): string => {
    return instance.formatDate(startDate, { skeleton: 'yMd' }) + 
           ' - ' + 
           instance.formatDate(endDate, { skeleton: 'yMd' });
  };
  
  const dateRangeTemplate = (props): JSX.Element => {
    return <div>{getDateRange(props.startDate, props.endDate)}</div>;
  };

  return (
    <ScheduleComponent 
      width='100%' 
      height='550px'
      dateRangeTemplate={dateRangeTemplate}
    >
      <ViewsDirective>
        <ViewDirective option='Day' />
        <ViewDirective option='Week' />
        <ViewDirective option='WorkWeek' />
        <ViewDirective option='TimelineWeek' />
      </ViewsDirective>
      <Inject services={[Day, Week, WorkWeek, TimelineViews]} />
    </ScheduleComponent>
  );
};

export default App;
```

### Customizing Header Indent Cells

Customize header indent cells in vertical and Timeline views using the `headerIndentTemplate` option.

```tsx
import * as React from 'react';
import {
  Week, TimelineViews, TimelineMonth, Day, ScheduleComponent, GroupModel,
  ViewsDirective, ViewDirective, ResourcesDirective, EventSettingsModel,
  ResourceDirective, Inject
} from '@syncfusion/ej2-react-schedule';
import { resourceData } from './datasource';

const App = () => {
  const eventSettings: EventSettingsModel = { dataSource: resourceData };
  const group: GroupModel = { resources: ['Owners'] };
  const ownerData: object[] = [
    { OwnerText: 'Nancy', Id: 1, OwnerColor: '#ffaa00' },
    { OwnerText: 'Steven', Id: 2, OwnerColor: '#f8a398' },
    { OwnerText: 'Michael', Id: 3, OwnerColor: '#7499e1' }
  ];

  const headerIndentTemplate = () => {
    return (
      <div className='e-resource-text'>
        <div className="text">Resources</div>
      </div>
    );
  };

  return (
    <ScheduleComponent 
      width='100%' 
      height='550px' 
      currentView='Week' 
      headerIndentTemplate={headerIndentTemplate} 
      selectedDate={new Date(2018, 3, 1)} 
      eventSettings={eventSettings} 
      group={group}
    >
      <ViewsDirective>
        <ViewDirective option='Day' />
        <ViewDirective option='Week' />
        <ViewDirective option='TimelineWeek' />
        <ViewDirective option='TimelineMonth' />
      </ViewsDirective>
      <ResourcesDirective>
        <ResourceDirective 
          field='OwnerId' 
          title='Owner' 
          name='Owners' 
          allowMultiple={true} 
          dataSource={ownerData} 
          textField='OwnerText' 
          idField='Id' 
          colorField='OwnerColor'
        />
      </ResourcesDirective>
      <Inject services={[Day, Week, TimelineViews, TimelineMonth]} />
    </ScheduleComponent>
  );
};

export default App;
```

## Header Rows

Timeline views support additional header rows beyond the default date and time headers. You can add Year, Month, Week, Date, and Hour rows using `HeaderRowDirective`.

### Available Header Row Types

The following header row options are available:
- **Year**: Displays year information
- **Month**: Displays month information
- **Week**: Displays week numbers
- **Date**: Displays date information
- **Hour**: Displays hour information (not applicable for Timeline Month view)

**Note**: Import `HeaderRowsDirective` and `HeaderRowDirective` to use this feature.

Example showing all available header rows:

```tsx
import * as React from 'react';
import {
  ScheduleComponent, HeaderRowDirective, HeaderRowsDirective, 
  TimelineViews, Inject, ViewsDirective, ViewDirective
} from '@syncfusion/ej2-react-schedule';
import { scheduleData } from './datasource';

const App = () => {
  const eventSettings = { dataSource: scheduleData };
  
  return (
    <ScheduleComponent 
      width='100%' 
      height='550px' 
      selectedDate={new Date(2018, 11, 31)}
      eventSettings={eventSettings} 
      startHour='09:00' 
      endHour='13:00'
    >
      <HeaderRowsDirective>
        <HeaderRowDirective option='Year' />
        <HeaderRowDirective option='Month' />
        <HeaderRowDirective option='Week' />
        <HeaderRowDirective option='Date' />
        <HeaderRowDirective option='Hour' />
      </HeaderRowsDirective>
      <ViewsDirective>
        <ViewDirective option='TimelineWeek' />
      </ViewsDirective>
      <Inject services={[TimelineViews]} />
    </ScheduleComponent>
  );
};

export default App;
```

### Display Year and Month Rows

Display only year and month header rows in Timeline views:

```tsx
import * as React from 'react';
import {
  ScheduleComponent, HeaderRowDirective, HeaderRowsDirective, 
  TimelineMonth, Inject, ViewsDirective, ViewDirective
} from '@syncfusion/ej2-react-schedule';
import { scheduleData } from './datasource';

const App = () => {
  const eventSettings = { dataSource: scheduleData };

  return (
    <ScheduleComponent 
      width='100%' 
      height='550px' 
      selectedDate={new Date(2018, 11, 31)}
      eventSettings={eventSettings}
    >
      <HeaderRowsDirective>
        <HeaderRowDirective option='Year' />
        <HeaderRowDirective option='Month' />
      </HeaderRowsDirective>
      <ViewsDirective>
        <ViewDirective option='TimelineMonth' interval={24} />
      </ViewsDirective>
      <Inject services={[TimelineMonth]} />
    </ScheduleComponent>
  );
};

export default App;
```

### Display Week Numbers

Display week numbers in a separate header row:

```tsx
import * as React from 'react';
import {
  ScheduleComponent, HeaderRowDirective, HeaderRowsDirective, 
  TimelineMonth, TimelineViews, Inject, ViewsDirective, ViewDirective
} from '@syncfusion/ej2-react-schedule';
import { scheduleData } from './datasource';

const App = () => {
  const eventSettings = { dataSource: scheduleData };

  return (
    <ScheduleComponent 
      width='100%' 
      height='550px' 
      selectedDate={new Date(2018, 11, 31)}
      eventSettings={eventSettings}
    >
      <HeaderRowsDirective>
        <HeaderRowDirective option='Week' />
        <HeaderRowDirective option='Date' />
        <HeaderRowDirective option='Hour' />
      </HeaderRowsDirective>
      <ViewsDirective>
        <ViewDirective option='TimelineMonth' interval={24} />
        <ViewDirective option='TimelineWeek' interval={3} />
        <ViewDirective option='TimelineDay' interval={4} />
      </ViewsDirective>
      <Inject services={[TimelineMonth, TimelineViews]} />
    </ScheduleComponent>
  );
};

export default App;
```

### Display Full Year in Timeline

Display a complete year in Timeline view by setting the `interval` to 12:

```tsx
import * as React from 'react';
import {
  ScheduleComponent, HeaderRowDirective, HeaderRowsDirective, 
  TimelineMonth, Inject, ViewsDirective, ViewDirective
} from '@syncfusion/ej2-react-schedule';
import { eventData } from './datasource';

const App = () => {
  const eventSettings = { dataSource: eventData };

  return (
    <ScheduleComponent 
      width='100%' 
      height='550px' 
      selectedDate={new Date(2018, 0, 1)}
      eventSettings={eventSettings}
    >
      <HeaderRowsDirective>
        <HeaderRowDirective option='Month' />
        <HeaderRowDirective option='Date' />
      </HeaderRowsDirective>
      <ViewsDirective>
        <ViewDirective option='TimelineMonth' interval={12} />
      </ViewsDirective>
      <Inject services={[TimelineMonth]} />
    </ScheduleComponent>
  );
};

export default App;
```

### Customizing Header Rows with Templates

Customize header row text and display images or formatted text using the `template` option:

```tsx
import * as React from 'react';
import {
  ScheduleComponent, getWeekNumber, HeaderRowDirective, HeaderRowsDirective, 
  TimelineMonth, Inject, ViewsDirective, ViewDirective, CellTemplateArgs
} from '@syncfusion/ej2-react-schedule';
import { scheduleData } from './datasource';
import { Internationalization } from '@syncfusion/ej2-base';

const App = () => {
  const eventSettings = { dataSource: scheduleData };
  const instance: Internationalization = new Internationalization();
  
  const getYearDetails = (value: CellTemplateArgs) => {
    return 'Year: ' + instance.formatDate(value.date, { skeleton: 'y' });
  };
  
  const getMonthDetails = (value: CellTemplateArgs) => {
    return 'Month: ' + instance.formatDate(value.date, { skeleton: 'M' });
  };
  
  const getWeekDetails = (value: CellTemplateArgs) => {
    return 'Week ' + getWeekNumber(value.date);
  };
  
  const yearTemplate = (props): JSX.Element => {
    return <span className="year">{getYearDetails(props)}</span>;
  };
  
  const monthTemplate = (props): JSX.Element => {
    return <span className="month">{getMonthDetails(props)}</span>;
  };
  
  const weekTemplate = (props): JSX.Element => {
    return <span className="week">{getWeekDetails(props)}</span>;
  };

  return (
    <ScheduleComponent 
      width='100%' 
      height='550px' 
      selectedDate={new Date(2018, 0, 1)}
      eventSettings={eventSettings}
    >
      <HeaderRowsDirective>
        <HeaderRowDirective option='Year' template={yearTemplate} />
        <HeaderRowDirective option='Month' template={monthTemplate} />
        <HeaderRowDirective option='Week' template={weekTemplate} />
        <HeaderRowDirective option='Date' />
      </HeaderRowsDirective>
      <ViewsDirective>
        <ViewDirective option='TimelineMonth' />
      </ViewsDirective>
      <Inject services={[TimelineMonth]} />
    </ScheduleComponent>
  );
};

export default App;
```

## Dimensions

The Scheduler supports three types of dimension values for controlling height and width: `auto`, `pixel`, and `percentage`.

### Auto Height and Width

When height and width are set to `auto`, the Scheduler attempts to match the dimensions of its parent container. By default, both properties are set to `auto`.

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
      height='auto' 
      width='auto' 
      selectedDate={new Date(2018, 1, 15)} 
      eventSettings={eventSettings}
    >
      <Inject services={[Day, Week, WorkWeek, Month, Agenda]} />
    </ScheduleComponent>
  );
};

export default App;
```

### Height and Width in Pixels

Set exact pixel values for height and width. Values can be numbers (e.g., `500`) or strings with `px` suffix (e.g., `'500px'`).

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
      height='550px' 
      width='650px' 
      selectedDate={new Date(2018, 1, 15)} 
      eventSettings={eventSettings}
    >
      <Inject services={[Day, Week, WorkWeek, Month, Agenda]} />
    </ScheduleComponent>
  );
};

export default App;
```

### Height and Width in Percentages

Use percentage values to make the Scheduler scale relative to its parent container.

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
      height='100%' 
      width='100%' 
      selectedDate={new Date(2018, 1, 15)} 
      eventSettings={eventSettings}
    >
      <Inject services={[Day, Week, WorkWeek, Month, Agenda]} />
    </ScheduleComponent>
  );
};

export default App;
```

## Row Auto Height

The row auto-height feature automatically adjusts row heights in Timeline and Month views based on the number of overlapping appointments, eliminating the `+n more` text indicator.

Enable this feature by setting the `rowAutoHeight` property to `true` (default is `false`).

**Note**: This feature applies only to Timeline views and the calendar Month view.

### Calendar Month View Auto Height

In Month view, the row auto-height feature automatically expands rows to display all appointments.

```tsx
import * as React from 'react';
import {
  ScheduleComponent, Month, Inject,
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
      rowAutoHeight={true}
    >
      <ViewsDirective>
        <ViewDirective option='Month' />
      </ViewsDirective>
      <Inject services={[Month]} />
    </ScheduleComponent>
  );
};

export default App;
```

### Timeline Views Auto Height

Timeline views automatically adjust row heights based on overlapping appointments.

```tsx
import * as React from 'react';
import {
  ScheduleComponent, TimelineViews, Inject, TimelineMonth, Agenda,
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
      rowAutoHeight={true}
    >
      <ViewsDirective>
        <ViewDirective option='TimelineDay' />
        <ViewDirective option='TimelineWeek' />
        <ViewDirective option='TimelineWorkWeek' />
        <ViewDirective option='TimelineMonth' />
        <ViewDirective option='Agenda' />
      </ViewsDirective>
      <Inject services={[TimelineViews, TimelineMonth, Agenda]} />
    </ScheduleComponent>
  );
};

export default App;
```

### Timeline with Multiple Resources

Row auto-height works with Timeline views containing multiple resources.

```tsx
import * as React from 'react';
import {
  TimelineViews, ScheduleComponent, ViewsDirective, ViewDirective,
  ResourcesDirective, ResourceDirective, Inject, Resize, 
  DragAndDrop, EventSettingsModel, GroupModel
} from '@syncfusion/ej2-react-schedule';
import { roomData } from './datasource';

const App = () => {
  const ownerData: Object[] = [
    { text: 'Room A', id: 1, color: '#98AFC7' },
    { text: 'Room B', id: 2, color: '#99c68e' },
    { text: 'Room C', id: 3, color: '#C2B280' },
    { text: 'Room D', id: 4, color: '#3090C7' },
    { text: 'Room E', id: 5, color: '#95b9' },
    { text: 'Room F', id: 6, color: '#95b9c7' },
    { text: 'Room G', id: 7, color: '#deb887' },
    { text: 'Room H', id: 8, color: '#3090C7' },
    { text: 'Room I', id: 9, color: '#98AFC7' },
    { text: 'Room J', id: 10, color: '#778899' }
  ];
  
  const fieldsData = {
    id: 'Id',
    subject: { title: 'Summary', name: 'Subject' },
    location: { title: 'Location', name: 'Location' },
    description: { title: 'Comments', name: 'Description' },
    startTime: { title: 'From', name: 'StartTime' },
    endTime: { title: 'To', name: 'EndTime' }
  };
  
  const eventSettings: EventSettingsModel = { 
    dataSource: roomData, 
    fields: fieldsData 
  };
  
  const group: GroupModel = { 
    enableCompactView: false, 
    resources: ['MeetingRoom'] 
  };

  return (
    <ScheduleComponent 
      width='100%' 
      height='550px' 
      selectedDate={new Date(2018, 7, 1)} 
      rowAutoHeight={true} 
      eventSettings={eventSettings} 
      group={group}
    >
      <ResourcesDirective>
        <ResourceDirective 
          field='RoomId' 
          title='Room Type' 
          name='MeetingRoom' 
          allowMultiple={true}
          dataSource={ownerData} 
          textField='text' 
          idField='id' 
          colorField='color'
        />
      </ResourcesDirective>
      <ViewsDirective>
        <ViewDirective option='TimelineDay' />
        <ViewDirective option='TimelineWeek' />
      </ViewsDirective>
      <Inject services={[TimelineViews, Resize, DragAndDrop]} />
    </ScheduleComponent>
  );
};

export default App;
```

### Appointments Occupying Entire Cell

When `rowAutoHeight` is enabled, appointments have whitespace at the bottom by default. Remove this space by setting `ignoreWhitespace` to `true` in `eventSettings`.

```tsx
import * as React from 'react';
import {
  TimelineViews, TimelineMonth, ScheduleComponent, ViewsDirective, 
  ViewDirective, EventSettingsModel, GroupModel, ResourcesDirective, 
  ResourceDirective, Inject
} from '@syncfusion/ej2-react-schedule';
import { resourceData } from './datasource';

const App = () => {
  const eventSettings: EventSettingsModel = { 
    dataSource: resourceData, 
    ignoreWhitespace: true 
  };
  
  const group: GroupModel = { resources: ['Rooms', 'Owners'] };
  
  const roomData: Object[] = [
    { RoomText: 'ROOM 1', Id: 1, RoomColor: '#cb6bb2' },
    { RoomText: 'ROOM 2', Id: 2, RoomColor: '#56ca85' }
  ];
  
  const ownerData: Object[] = [
    { OwnerText: 'Nancy', Id: 1, GroupId: 1, OwnerColor: '#ffaa00' },
    { OwnerText: 'Steven', Id: 2, GroupId: 2, OwnerColor: '#f8a398' },
    { OwnerText: 'Michael', Id: 3, GroupId: 1, OwnerColor: '#7499e1' }
  ];

  return (
    <ScheduleComponent 
      width='100%' 
      height='550px' 
      currentView='TimelineWeek' 
      rowAutoHeight={true} 
      selectedDate={new Date(2021, 7, 4)} 
      eventSettings={eventSettings} 
      group={group}
    >
      <ViewsDirective>
        <ViewDirective option='TimelineDay' />
        <ViewDirective option='TimelineWeek' />
        <ViewDirective option='TimelineMonth' />
      </ViewsDirective>
      <ResourcesDirective>
        <ResourceDirective 
          field='RoomId' 
          title='Room' 
          name='Rooms'
          dataSource={roomData} 
          textField='RoomText' 
          idField='Id' 
          colorField='RoomColor'
        />
        <ResourceDirective 
          field='OwnerId' 
          title='Owner' 
          name='Owners' 
          allowMultiple={true}
          dataSource={ownerData} 
          textField='OwnerText' 
          idField='Id' 
          groupIDField='GroupId' 
          colorField='OwnerColor'
        />
      </ResourcesDirective>
      <Inject services={[TimelineViews, TimelineMonth]} />
    </ScheduleComponent>
  );
};

export default App;
```

**Note**: The `ignoreWhitespace` property only applies when `rowAutoHeight` is enabled.

## Responsive Layout

The Syncfusion React Scheduler is designed to be fully responsive and adapt to various screen sizes automatically. The component adjusts its layout based on the available viewport dimensions, ensuring optimal user experience across devices.

Key responsive features:
- Automatic resizing when parent container dimensions change
- Percentage-based dimensions for fluid layouts
- Built-in adaptive UI mode for mobile devices
- Touch-friendly interface elements on smaller screens

For responsive applications, consider:
- Using percentage values for width and height
- Enabling `enableAdaptiveUI` for mobile-optimized interface
- Testing on various viewport sizes to ensure proper rendering

## Mobile Rendering

The Scheduler provides an adaptive UI mode specifically optimized for mobile devices. Enable this mode using the `enableAdaptiveUI` property set to `true`.

Mobile-specific optimizations include:
- **Compact Header**: View options move to a popup menu
- **Touch-Friendly Controls**: Larger touch targets for better interaction
- **Optimized Event Display**: Improved event rendering for small screens
- **Simplified Navigation**: Streamlined date navigation controls
- **Responsive Dialogs**: Event editor and quick info popup adapt to screen size

Example with adaptive UI enabled:

```tsx
import * as React from 'react';
import {
  ScheduleComponent, Day, Week, Month, Agenda, Inject, EventSettingsModel
} from '@syncfusion/ej2-react-schedule';
import { scheduleData } from './datasource';

const App = () => {
  const eventSettings: EventSettingsModel = { dataSource: scheduleData };

  return (
    <ScheduleComponent 
      width='100%' 
      height='100%' 
      selectedDate={new Date(2018, 1, 15)} 
      enableAdaptiveUI={true} 
      eventSettings={eventSettings}
    >
      <Inject services={[Day, Week, Month, Agenda]} />
    </ScheduleComponent>
  );
};

export default App;
```

When designing for mobile:
- Enable adaptive UI mode for better mobile experience
- Use touch-friendly event handlers
- Consider viewport limitations when customizing templates
- Test on actual mobile devices or emulators
- Ensure custom toolbar items are touch-accessible

---
