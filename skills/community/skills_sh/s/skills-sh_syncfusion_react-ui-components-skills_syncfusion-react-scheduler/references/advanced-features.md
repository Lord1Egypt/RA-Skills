# Advanced Features - React Scheduler

This reference provides comprehensive documentation for advanced features in the Syncfusion React Scheduler component.

## Table of Contents

- [State Persistence](#state-persistence)
- [Exporting](#exporting)
  - [Excel Exporting](#excel-exporting)
  - [ICS File Exporting](#ics-file-exporting)
  - [Importing from ICS Files](#importing-from-ics-files)
  - [Print Functionality](#print-functionality)
- [Clipboard Operations](#clipboard-operations)
  - [Cut, Copy, and Paste Using Keyboard](#cut-copy-and-paste-using-keyboard)
  - [Cut, Copy, and Paste Using Context Menu](#cut-copy-and-paste-using-context-menu)
  - [Modifying Content Before Pasting](#modifying-content-before-pasting)
- [Virtual Scrolling](#virtual-scrolling)
  - [Enabling Virtual Scrolling](#enabling-virtual-scrolling)
  - [Lazy Loading for Appointments](#lazy-loading-for-appointments)
- [Performance Tips](#performance-tips)

---

## State Persistence

State persistence allows the Scheduler to retain the `currentView`, `selectedDate`, and scroll position values in the browser's `localStorage` for state maintenance even if the browser is refreshed or you navigate to another page. This behavior is enabled through the `enablePersistence` property, which is disabled by default.

**Key Points:**
- When set to `true`, the Scheduler's `currentView`, `selectedDate`, and scroll position values are preserved after a page refresh
- The Scheduler `id` is required to enable state persistence

**Implementation:**

```typescript
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import {
  ScheduleComponent, Day, Week, WorkWeek, Month, Inject,
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
      enablePersistence={true}
    >
      <Inject services={[Day, Week, WorkWeek, Month]} />
    </ScheduleComponent>
  );
};

const root = ReactDOM.createRoot(document.getElementById('schedule'));
root.render(<App />);
```

---

## Exporting

The Scheduler supports exporting appointments to Excel, ICS files, and provides print functionality for generating reports and sharing schedules.

### Excel Exporting

The Scheduler enables exporting events to an Excel file using the `exportToExcel` method. By default, it includes all fields mapped in the `eventSettings` property.

**Prerequisites:**
- Import and inject the `ExcelExport` module from `@syncfusion/ej2-schedule`

#### Basic Excel Export

```typescript
import * as ReactDOM from 'react-dom';
import { useRef } from 'react';
import * as React from 'react';
import { ItemModel } from '@syncfusion/ej2-react-navigations';
import {
  ScheduleComponent, ViewDirective, Week, Resize, ExcelExport, ExportOptions,
  ActionEventArgs, ToolbarActionArgs, DragAndDrop, Inject, ViewsDirective, EventSettingsModel
} from '@syncfusion/ej2-react-schedule';
import { scheduleData } from './datasource';

const App = () => {
  const scheduleObj = useRef<ScheduleComponent>(null);
  const eventSettings: EventSettingsModel = { dataSource: scheduleData };

  const onActionBegin = (args: ActionEventArgs & ToolbarActionArgs): void => {
    if (args.requestType === 'toolbarItemRendering') {
      let exportItem: ItemModel = {
        align: 'Right', 
        showTextOn: 'Both', 
        prefixIcon: 'e-icon-schedule-excel-export',
        text: 'Excel Export', 
        cssClass: 'e-excel-export', 
        click: onExportClick
      };
      args.items.push(exportItem);
    }
  }

  const onExportClick = (): void => {
    scheduleObj.current.exportToExcel();
  }

  return (
    <ScheduleComponent 
      cssClass='excel-export' 
      width='100%' 
      height='550px' 
      id='schedule' 
      ref={scheduleObj}
      selectedDate={new Date(2019, 0, 10)} 
      eventSettings={eventSettings}
      actionBegin={onActionBegin}
    >
      <ViewsDirective>
        <ViewDirective option='Week' />
      </ViewsDirective>
      <Inject services={[Week, Resize, DragAndDrop, ExcelExport]} />
    </ScheduleComponent>
  );
};
```

#### Exporting with Custom Fields

To export only specific fields, define the required fields through the `fields` option in `ExportOptions`:

```typescript
const onExportClick = (): void => {
  let exportValues: ExportOptions = {
    fields: ['Id', 'Subject', 'StartTime', 'EndTime', 'Location']
  };
  scheduleObj.current.exportToExcel(exportValues);
}
```

#### Exporting Individual Occurrences of Recurring Series

By default, recurring events are exported as a single record. To export each occurrence separately, set `includeOccurrences` to `true`:

```typescript
const onExportClick = (): void => {
  let exportValues: ExportOptions = { includeOccurrences: true };
  scheduleObj.current.exportToExcel(exportValues);
}
```

#### Exporting Custom Event Data

To export specific events or custom data collections, pass them through the `customData` option:

```typescript
const onExportClick = (): void => {
  let exportValues: ExportOptions = {
    customData: [
      {
        Id: 1,
        Subject: 'Explosion of Betelgeuse Star',
        Location: 'Space Centre USA',
        StartTime: new Date(2019, 0, 6, 9, 30),
        EndTime: new Date(2019, 0, 6, 11, 0),
        CategoryColor: '#1aaa55'
      },
      {
        Id: 2,
        Subject: 'Thule Air Crash Report',
        Location: 'Newyork City',
        StartTime: new Date(2019, 0, 7, 12, 0),
        EndTime: new Date(2019, 0, 7, 14, 0),
        CategoryColor: '#357cd2'
      }
    ]
  };
  scheduleObj.current.exportToExcel(exportValues);
}
```

#### Customizing Column Headers

Use the `fieldsInfo` option to customize header names when exporting:

```typescript
const onExportClick = (): void => {
  let customFields: ExportFieldInfo[] = [
    { name: 'Subject', text: 'Summary' },
    { name: 'StartTime', text: 'First Date' },
    { name: 'EndTime', text: 'Last Date' },
    { name: 'Location', text: 'Place' },
    { name: 'OwnerId', text: 'Owners' }
  ];
  let exportValues: ExportOptions = { fieldsInfo: customFields };
  scheduleObj.current.exportToExcel(exportValues);
}
```

#### Export with Custom File Name

The default exported file name is `Schedule.xlsx`. Customize it using the `fileName` option:

```typescript
const onExportClick = (): void => {
  let exportValues: ExportOptions = { fileName: "SchedulerData" };
  scheduleObj.current.exportToExcel(exportValues);
}
```

#### Excel File Formats

Export to `.xlsx` or `.csv` formats by setting the `exportType` option:

```typescript
const onExportClick = (): void => {
  let exportValues: ExportOptions = { exportType: "csv" };
  scheduleObj.current.exportToExcel(exportValues);
}
```

#### Custom Separator in CSV

Change the default CSV separator (`,`) using the `separator` property:

```typescript
const onExportClick = (): void => {
  let exportValues: ExportOptions = { 
    exportType: 'csv', 
    separator: ';' 
  };
  scheduleObj.current.exportToExcel(exportValues);
}
```

#### Customizing Excel Sheet Before Export

Use the `excelExport` event to customize the Excel sheet before exporting:

```typescript
const onExcelExport = (args: ExcelExportEventArgs) => {
  const worksheet = args.worksheets[0];
  
  // Add custom header
  worksheet.rows.unshift({
    index: 1,
    cells: [{
      index: 1,
      value: 'Sales Report',
      style: {
        bold: true,
        fontSize: 18,
        hAlign: 'Center',
        fill: { color: '#1E90FF' }, 
        color: '#FFFFFF',
      },
      colSpan: worksheet.columns.length,
    }]
  });
  
  // Add custom footer
  worksheet.rows.push({
    index: worksheet.rows.length + 1,
    cells: [{
      index: 1,
      value: 'End of Report',
      style: {
        bold: true,
        fontSize: 14,
        hAlign: 'Center',
        fill: { color: '#FFD700' },
      },
      colSpan: worksheet.columns.length,
    }]
  });
}
```

### ICS File Exporting

You can export Scheduler events to a calendar (.ics) file format, compatible with Google Calendar, Outlook, and other calendar applications.

**Prerequisites:**
- Import and inject the `ICalendarExport` module from `@syncfusion/ej2-schedule`

#### Basic ICS Export

```typescript
import * as ReactDOM from 'react-dom';
import * as React from 'react';
import { useRef } from 'react';
import {
  ScheduleComponent, Day, Week, WorkWeek, Month, Agenda, 
  ICalendarExport, Inject
} from '@syncfusion/ej2-react-schedule';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { scheduleData } from './datasource';

const App = () => {
  const scheduleObj = useRef<ScheduleComponent>(null);
  const eventSettings = { dataSource: scheduleData };

  const onClick = (): void => {
    scheduleObj.current.exportToICalendar();
  }
  
  return (
    <div>
      <ButtonComponent id='ics-export' title='Export' onClick={onClick}>
        Export
      </ButtonComponent>
      <ScheduleComponent 
        ref={scheduleObj} 
        width='100%' 
        height='520px' 
        selectedDate={new Date(2018, 1, 15)} 
        eventSettings={eventSettings}
      >
        <Inject services={[Day, Week, WorkWeek, Month, Agenda, ICalendarExport]} />
      </ScheduleComponent>
    </div>
  );
};
```

#### Exporting with Custom File Name

By default, the calendar is exported as `Calendar.ics`. Customize the file name:

```typescript
const onClick = (): void => {
  scheduleObj.current.exportToICalendar('ScheduleEvents');
}
```

### Importing from ICS Files

Import events from external calendars (ICS files) using the `importICalendar` method, which accepts a blob object of an .ics file.

**Prerequisites:**
- Import and inject the `ICalendarImport` module from `@syncfusion/ej2-schedule`

```typescript
import * as ReactDOM from 'react-dom';
import * as React from 'react';
import { useRef } from 'react';
import {
  ScheduleComponent, Day, Week, WorkWeek, Month, Agenda, 
  ICalendarImport, Inject
} from '@syncfusion/ej2-react-schedule';
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';
import { scheduleData } from './datasource';

const App = () => {
  const scheduleObj = useRef<ScheduleComponent>(null);
  const allowedExtensions: string = '.ics';
  const eventSettings = { dataSource: scheduleData };

  const onSelect = (args): void => {
    scheduleObj.current.importICalendar(args.event.target.files[0]);
  }
  
  return (
    <div>
      <UploaderComponent 
        id='fileUpload' 
        type='file' 
        allowedExtensions={allowedExtensions} 
        cssClass='calendar-import'
        buttons={{ browse: 'Choose file' }} 
        multiple={false} 
        showFileList={false}
        selected={onSelect}
      />
      <ScheduleComponent 
        ref={scheduleObj} 
        width='100%' 
        height='520px' 
        selectedDate={new Date(2018, 1, 15)} 
        eventSettings={eventSettings}
      >
        <Inject services={[Day, Week, WorkWeek, Month, Agenda, ICalendarImport]} />
      </ScheduleComponent>
    </div>
  );
};
```

### Print Functionality

The Scheduler allows printing the scheduler element using the `print` client-side method.

**Prerequisites:**
- Import and inject the `Print` module from `@syncfusion/ej2-react-schedule`

#### Using Print Method Without Options

```typescript
import * as ReactDOM from 'react-dom';
import * as React from 'react';
import { useRef } from 'react';
import { 
  ScheduleComponent, Day, Week, WorkWeek, Month, 
  Print, Inject, ActionEventArgs, ToolbarActionArgs 
} from '@syncfusion/ej2-react-schedule';
import { scheduleData } from './datasource';

const App = () => {
  const scheduleObj = useRef<ScheduleComponent>(null);
  const eventSettings = { dataSource: scheduleData };

  const onActionBegin = (args: ActionEventArgs & ToolbarActionArgs): void => {
    if (args.requestType === 'toolbarItemRendering') {
      let printItem = {
        align: 'Right', 
        showTextOn: 'Both', 
        prefixIcon: 'e-icon-schedule-print',
        text: 'Print', 
        cssClass: 'e-schedule-print', 
        click: onPrintIconClick
      };
      args.items.push(printItem);
    }
  }

  const onPrintIconClick = (): void => {
    scheduleObj.current.print();
  }

  return (
    <ScheduleComponent 
      ref={scheduleObj} 
      width='100%' 
      height='520px' 
      selectedDate={new Date(2018, 1, 15)} 
      eventSettings={eventSettings} 
      actionBegin={onActionBegin}
    >
      <Inject services={[Day, Week, WorkWeek, Month, Print]} />
    </ScheduleComponent>
  );
};
```

#### Using Print Method with Options

Customize the print output by passing print options:

```typescript
const onPrintIconClick = (): void => {
  let printModel: ScheduleModel = {
    agendaDaysCount: 14,
    cssClass: 'e-print-schedule',
    currentView: scheduleObj.current.currentView,
    dateFormat: 'dd-MMM-yyyy',
    enableRtl: false,
    endHour: '18:00',
    firstDayOfWeek: 1,
    height: 'auto',
    readonly: true,
    showHeaderBar: false,
    showTimeIndicator: false,
    startHour: '06:00',
    width: 'auto',
    workDays: [1, 2, 3, 4, 5]
  };
  scheduleObj.current.print(printModel);
}
```

#### Customizing Print Layout

Use the `beforePrint` event to customize the print layout:

```typescript
const onBeforePrint = (args: BeforePrintEventArgs) => {
  // Add custom header
  const headerElement = document.createElement('div');
  headerElement.innerHTML = `
    <h1>Schedule Report</h1>
    <p>Date: ${new Date().toLocaleString()}</p>
  `;
  headerElement.style.backgroundColor = '#4CAF50';
  headerElement.style.color = 'white';
  headerElement.style.padding = '10px';
  args.printElement.insertBefore(headerElement, args.printElement.firstChild);

  // Add custom footer
  const footerElement = document.createElement('div');
  footerElement.textContent = 'Confidential Document';
  args.printElement.appendChild(footerElement);
}
```

---

## Clipboard Operations

The Clipboard functionality in the Syncfusion Scheduler control enhances scheduling efficiency by enabling users to cut, copy, and paste appointments with ease.

**Activation:**
- Set the `allowClipboard` property to `true`
- The `allowKeyboardInteraction` property must also be `true`

### Cut, Copy, and Paste Using Keyboard

The Scheduler supports keyboard shortcuts for clipboard operations:

| Operation | Shortcut  | Description                                                      |
|-----------|-----------|------------------------------------------------------------------|
| Copy      | Ctrl+C    | Duplicate appointments to streamline the scheduling process      |
| Cut       | Ctrl+X    | Move appointments to a new time slot without duplicates          |
| Paste     | Ctrl+V    | Place copied or cut appointments into the desired time slot      |

**Note:** For Mac users, use **Cmd** instead of **Ctrl** for copy, cut, and paste operations.

**Implementation:**

```typescript
import { useRef } from 'react';
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import {
  ScheduleComponent, ViewsDirective, ViewDirective,
  Day, Week, WorkWeek, Month, Agenda, Inject
} from '@syncfusion/ej2-react-schedule';
import { scheduleData } from './datasource';

const App = () => {
  const scheduleObj = useRef<ScheduleComponent>(null);
  const eventSettings = { dataSource: scheduleData };

  return (
    <ScheduleComponent 
      height='550px' 
      ref={scheduleObj} 
      selectedDate={new Date(2024, 1, 15)} 
      eventSettings={eventSettings}
      allowClipboard={true} 
      showQuickInfo={false}
    >
      <ViewsDirective>
        <ViewDirective option='Day' />
        <ViewDirective option='Week' />
        <ViewDirective option='WorkWeek' />
        <ViewDirective option='Month' />
        <ViewDirective option='Agenda' />
      </ViewsDirective>
      <Inject services={[Day, Week, WorkWeek, Month, Agenda]} />
    </ScheduleComponent>
  );
};
```

### Cut, Copy, and Paste Using Context Menu

You can programmatically manage appointments using the public methods `cut`, `copy`, and `paste`:

| Method | Parameters                              | Description                                                      |
|--------|-----------------------------------------|------------------------------------------------------------------|
| `copy` | None                                    | Duplicate the selected appointment for reuse                     |
| `cut`  | None                                    | Remove the selected appointment from its current slot for moving |
| `paste`| targetElement (Scheduler's work-cell)   | Insert the copied or cut appointment into the specified time slot|

**Implementation with Context Menu:**

```typescript
import { useRef } from 'react';
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { closest, isNullOrUndefined, remove } from '@syncfusion/ej2-base';
import {
  ScheduleComponent, ViewsDirective, ViewDirective,
  Day, Week, WorkWeek, Month, Inject
} from '@syncfusion/ej2-react-schedule';
import { 
  BeforeOpenCloseMenuEventArgs, MenuEventArgs, MenuItemModel, 
  ContextMenuComponent 
} from '@syncfusion/ej2-react-navigations';
import { scheduleData } from './datasource';

const App = () => {
  const scheduleObj = useRef<ScheduleComponent>(null);
  const menuObj = useRef<ContextMenuComponent>(null);
  const eventSettings = { dataSource: scheduleData };
  let selectedTarget: Element;
  let targetElement: HTMLElement;
  
  const menuItems: MenuItemModel[] = [
    { text: 'Cut Event', iconCss: 'e-icons e-cut', id: 'Cut' },
    { text: 'Copy Event', iconCss: 'e-icons e-copy', id: 'Copy' },
    { text: 'Paste', iconCss: 'e-icons e-paste', id: 'Paste' }
  ];

  const onContextMenuBeforeOpen = (args: BeforeOpenCloseMenuEventArgs): void => {
    targetElement = args.event.target as HTMLElement;
    selectedTarget = closest(
      targetElement, 
      '.e-appointment,.e-work-cells,.e-all-day-cells,.e-header-cells'
    );
    
    if (isNullOrUndefined(selectedTarget)) {
      args.cancel = true;
      return;
    }
    
    if (selectedTarget.classList.contains('e-appointment')) {
      menuObj.current.showItems(['Cut', 'Copy'], true);
      menuObj.current.hideItems(['Paste'], true);
    } else {
      menuObj.current.showItems(['Paste'], true);
      menuObj.current.hideItems(['Cut', 'Copy'], true);
    }
  }

  const onMenuItemSelect = (args: MenuEventArgs): void => {
    switch (args.item.id) {
      case 'Cut':
        scheduleObj.current.cut([selectedTarget] as HTMLElement[]);
        break;
      case 'Copy':
        scheduleObj.current.copy([selectedTarget] as HTMLElement[]);
        break;
      case 'Paste':
        scheduleObj.current.paste(targetElement);
        break;
    }
  }

  return (
    <div>
      <ScheduleComponent 
        height='550px' 
        ref={scheduleObj} 
        selectedDate={new Date(2024, 1, 15)} 
        eventSettings={eventSettings}
      >
        <ViewsDirective>
          <ViewDirective option='Day' />
          <ViewDirective option='Week' />
          <ViewDirective option='WorkWeek' />
          <ViewDirective option='Month' />
        </ViewsDirective>
        <Inject services={[Day, Week, WorkWeek, Month]} />
      </ScheduleComponent>
      <ContextMenuComponent 
        target='.e-schedule' 
        items={menuItems}
        beforeOpen={onContextMenuBeforeOpen} 
        select={onMenuItemSelect}
        cssClass='schedule-context-menu' 
        ref={menuObj} 
      />
    </div>
  );
};
```

### Modifying Content Before Pasting

Use the `beforePaste` event to modify appointment content before pasting:

```typescript
interface ScheduleData {
  Id: string;
  Subject: string;
  StartTime: string;
  EndTime: string;
  Location: string;
  Description: string;
}

const onBeforePasting = (args: BeforePasteEventArgs) => {
  if (typeof args.data === 'string') {
    const dataArray: string[] = (args.data as string).split('\t');
    const result: ScheduleData = {
      Id: dataArray[0],
      Subject: dataArray[1],
      StartTime: new Date(dataArray[4]).toISOString(),
      EndTime: new Date(new Date(dataArray[4]).getTime() + 60 * 60 * 1000).toISOString(),
      Location: dataArray[2],
      Description: dataArray[3]
    };
    args.data = [result];
  }
}
```

**Example: Copying from Grid to Scheduler**

```typescript
<ScheduleComponent 
  height='550px' 
  ref={scheduleObj} 
  selectedDate={new Date(2024, 1, 15)} 
  eventSettings={eventSettings}
  allowClipboard={true} 
  showQuickInfo={false} 
  beforePaste={onBeforePasting}
>
  <Inject services={[Day, Week, WorkWeek, Month]} />
</ScheduleComponent>
<GridComponent 
  dataSource={gridData} 
  width="40%" 
  height="400px" 
  allowSelection={true}
  ref={gridObj}
>
  <ColumnsDirective>
    <ColumnDirective field="OrderID" headerText="Order ID" width={90} />
    <ColumnDirective field="CustomerID" headerText="Customer ID" width={100} />
    <ColumnDirective field="ShipCity" headerText="Ship City" width={100} />
  </ColumnsDirective>
</GridComponent>
```

---

## Virtual Scrolling

Virtual scrolling support in the Scheduler component enhances performance when working with a substantial number of resources and events. This feature allows large sets of resources and events to load dynamically as users scroll.

### Enabling Virtual Scrolling

Enable virtual scrolling by setting the `allowVirtualScrolling` property to `true` within the specific timeline view settings:

```typescript
import * as ReactDOM from 'react-dom';
import * as React from 'react';
import {
  ScheduleComponent, ViewsDirective, ViewDirective, ResourcesDirective,
  ResourceDirective, TimelineMonth, TimelineYear, Resize, DragAndDrop, 
  Inject, EventSettingsModel, GroupModel
} from '@syncfusion/ej2-react-schedule';

const App = () => {
  const generateStaticEvents = (
    start: Date, 
    resCount: number, 
    overlapCount: number
  ): Object[] => {
    let data: Object[] = [];
    let id: number = 1;
    
    for (let i: number = 0; i < resCount; i++) {
      let randomCollection: number[] = [];
      let random: number = 0;
      
      for (let j: number = 0; j < overlapCount; j++) {
        random = Math.floor(Math.random() * 30);
        random = (random === 0) ? 1 : random;
        
        if (randomCollection.indexOf(random) !== -1 || 
            randomCollection.indexOf(random + 2) !== -1 ||
            randomCollection.indexOf(random - 2) !== -1) {
          random += (Math.max.apply(null, randomCollection) + 10);
        }
        
        for (let k: number = 1; k <= 2; k++) {
          randomCollection.push(random + k);
        }
        
        let startDate: Date = new Date(start.getFullYear(), start.getMonth(), random);
        startDate = new Date(startDate.getTime() + (((random % 10) * 10) * (1000 * 60)));
        let endDate: Date = new Date(startDate.getTime() + ((1440 + 30) * (1000 * 60)));
        
        data.push({
          Id: id,
          Subject: 'Event #' + id,
          StartTime: startDate,
          EndTime: endDate,
          IsAllDay: (id % 10) ? false : true,
          ResourceId: i + 1
        });
        id++;
      }
    }
    return data;
  }
  
  const generateResourceData = (
    startId: number, 
    endId: number, 
    text: string
  ): Object[] => {
    let data: { [key: string]: Object }[] = [];
    let colors: string[] = [
      '#ff8787', '#9775fa', '#748ffc', '#3bc9db', '#69db7c',
      '#fdd835', '#748ffc', '#9775fa', '#df5286', '#7fa900',
      '#fec200', '#5978ee', '#00bdae', '#ea80fc'
    ];
    
    for (let a: number = startId; a <= endId; a++) {
      let n: number = Math.floor(Math.random() * colors.length);
      data.push({
        Id: a,
        Text: text + ' ' + a,
        Color: colors[n]
      });
    }
    return data;
  }
  
  const eventSettings: EventSettingsModel = { 
    dataSource: generateStaticEvents(new Date(2018, 4, 1), 300, 12) 
  };
  const group: GroupModel = { resources: ['Resources'] };

  return (
    <ScheduleComponent 
      cssClass='virtual-scrolling' 
      width='100%'
      height='550px' 
      selectedDate={new Date(2018, 4, 1)}
      eventSettings={eventSettings}
      group={group}
    >
      <ResourcesDirective>
        <ResourceDirective 
          field='ResourceId' 
          title='Resource' 
          name='Resources' 
          allowMultiple={true}
          dataSource={generateResourceData(1, 300, 'Resource')}
          textField='Text' 
          idField='Id' 
          colorField='Color'
        />
      </ResourcesDirective>
      <ViewsDirective>
        <ViewDirective 
          option='TimelineMonth' 
          allowVirtualScrolling={true} 
          isSelected={true} 
        />
        <ViewDirective 
          option='TimelineYear' 
          orientation='Vertical' 
          allowVirtualScrolling={true} 
        />
      </ViewsDirective>
      <Inject services={[TimelineMonth, TimelineYear, Resize, DragAndDrop]} />
    </ScheduleComponent>
  );
}
```

**Note:** Virtual loading of resources and events is not supported in `MonthAgenda`, `Year`, and `TimelineYear` (Horizontal Orientation) views.

### Lazy Loading for Appointments

The lazy loading feature provides an efficient approach for loading appointment data into the Scheduler on-demand. This allows large volumes of appointments to be loaded without performance issues.

**How It Works:**
- Scheduler sends queries to the server to retrieve appointments only for resources currently displayed
- Queries include resource IDs and current date range as a comma-separated string
- Server parses resource IDs to filter and serve only necessary appointments
- Additional appointment data is fetched on-demand as new resources enter the viewport

**Enable lazy loading by setting the `enableLazyLoading` property to `true`:**

```typescript
import * as ReactDOM from 'react-dom';
import * as React from 'react';
import {
  ScheduleComponent, ViewsDirective, ViewDirective, ResourcesDirective,
  ResourceDirective, TimelineMonth, Inject, EventSettingsModel, GroupModel
} from '@syncfusion/ej2-react-schedule';
import { DataManager, WebApiAdaptor } from '@syncfusion/ej2-data';

const App = () => {
  const dataManager: DataManager = new DataManager({
    url: 'url',
    adaptor: new WebApiAdaptor,
    crossDomain: true
  });
  
  const eventSettings: EventSettingsModel = { dataSource: dataManager };
  const group: GroupModel = { resources: ['Resources'] };
  
  const generateResourceData = (
    startId: number, 
    endId: number, 
    text: string
  ): Object[] => {
    let data: { [key: string]: Object }[] = [];
    let colors: string[] = [
      '#ff8787', '#9775fa', '#748ffc', '#3bc9db', '#69db7c',
      '#fdd835', '#748ffc', '#9775fa', '#df5286', '#7fa900',
      '#fec200', '#5978ee', '#00bdae', '#ea80fc'
    ];
    
    for (let a: number = startId; a <= endId; a++) {
      let n: number = Math.floor(Math.random() * colors.length);
      data.push({
        Id: a,
        Text: text + ' ' + a,
        Color: colors[n]
      });
    }
    return data;
  }
  
  return (
    <ScheduleComponent 
      width='100%'
      height='550px' 
      selectedDate={new Date(2023, 3, 1)}
      eventSettings={eventSettings}
      group={group} 
      readonly={true}
    >
      <ResourcesDirective>
        <ResourceDirective 
          field='ResourceId' 
          title='Resource' 
          name='Resources'
          dataSource={generateResourceData(1, 1000, 'Resource')}
          textField='Text' 
          idField='Id' 
          colorField='Color'
        />
      </ResourcesDirective>
      <ViewsDirective>
        <ViewDirective 
          option='TimelineMonth' 
          enableLazyLoading={true} 
          isSelected={true} 
        />
      </ViewsDirective>
      <Inject services={[TimelineMonth]} />
    </ScheduleComponent>
  );
}
```

**Server-Side Implementation (C#):**

```csharp
using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;
using System;
using Microsoft.EntityFrameworkCore;
using System.Linq;
using Microsoft.AspNetCore.OData.Query;

namespace LazyLoadingServices.Controllers
{
    public class VirtualEventDataController : Controller
    {
        private readonly EventsContext dbContext;

        [HttpGet]
        [EnableQuery]
        [Route("api/VirtualEventData")]
        public IActionResult GetData([FromQuery] Params param)
        {
            IQueryable<EventData> query = dbContext.Events;
            
            // Filter the appointment data based on the ResourceId query params
            if (!string.IsNullOrEmpty(param.ResourceId))
            {
                string[] resourceId = param.ResourceId.Split(',');
                query = query.Where(data => resourceId.Contains(data.ResourceId.ToString()));
            }
            
            return Ok(query.ToList());
        }
    }
    
    public class Params
    {
        public DateTime? StartDate { get; set; }
        public DateTime? EndDate { get; set; }
        public string ResourceId { get; set; }
    }
}
```

**Important Notes:**
- This property is effective when large numbers of resources and appointments are bound to the Scheduler
- This property is applicable only when resource grouping is enabled in Scheduler

---

## Performance Tips

When working with advanced features in the Syncfusion React Scheduler, consider these performance optimization tips:

### 1. Virtual Scrolling
- **Use virtual scrolling** for large datasets (300+ resources or 1000+ events)
- Enable `allowVirtualScrolling` in timeline views for better performance
- Combine with `enableLazyLoading` for optimal server-side data retrieval

### 2. Data Management
- **Limit initial data load:** Use lazy loading to fetch data on-demand
- **Optimize queries:** Filter data server-side before sending to the client
- **Use DataManager:** Leverage efficient data binding with remote services
- **Implement caching:** Cache frequently accessed data to reduce server calls

### 3. Event Rendering
- **Reduce event complexity:** Minimize custom templates and complex styling
- **Use event templates wisely:** Keep templates lightweight and avoid heavy computations
- **Limit visible events:** Use date range filters to show only necessary events

### 4. Resource Handling
- **Group resources efficiently:** Avoid unnecessary nested grouping
- **Limit resource count:** Display only essential resources initially
- **Use color coding:** Simplify visual representation instead of complex styles

### 5. Export Operations
- **Export selectively:** Use field filters to export only necessary data
- **Batch exports:** For large datasets, consider server-side export generation
- **Optimize file size:** Exclude unnecessary fields and limit date ranges

### 6. Clipboard Operations
- **Disable when not needed:** Set `allowClipboard` to `false` if not using clipboard features
- **Optimize event handlers:** Keep `beforePaste` event handlers lightweight
- **Batch operations:** Process multiple clipboard operations together

### 7. State Persistence
- **Clear old data:** Periodically clear localStorage to prevent bloat
- **Selective persistence:** Only persist essential state information
- **Monitor storage usage:** Check localStorage size limits in different browsers

### 8. General Optimization
- **Disable unused features:** Only inject required modules and services
- **Optimize view switching:** Minimize data reloading when switching views
- **Use readonly mode:** Enable `readonly` for view-only scenarios
- **Debounce scroll events:** Implement debouncing for scroll-triggered operations
- **Minimize DOM manipulation:** Batch DOM updates when possible

### 9. Network Optimization
- **Use compression:** Enable gzip compression for data transfers
- **Implement pagination:** Load data in chunks rather than all at once
- **Use CDN:** Serve static resources from CDN for faster loading
- **Minimize API calls:** Combine multiple requests where possible

### 10. Browser Considerations
- **Test across browsers:** Ensure performance is acceptable on target browsers
- **Monitor memory usage:** Watch for memory leaks with browser dev tools
- **Profile performance:** Use browser profiling tools to identify bottlenecks
- **Handle edge cases:** Test with maximum expected data volumes

By following these performance tips, you can ensure that your Syncfusion React Scheduler application remains responsive and efficient, even when working with large datasets and complex scheduling scenarios.

---

