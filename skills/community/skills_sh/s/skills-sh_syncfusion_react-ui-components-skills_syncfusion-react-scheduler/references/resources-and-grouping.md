# Resources and Grouping

## Table of Contents

- [Overview](#overview)
- [Resource Fields](#resource-fields)
- [Resource Data Binding](#resource-data-binding)
  - [Local JSON Data](#local-json-data)
  - [Remote Service URL](#remote-service-url)
- [Single Resource Assignment](#single-resource-assignment)
- [Multiple Resource Assignment](#multiple-resource-assignment)
- [Hierarchical Grouping](#hierarchical-grouping)
  - [Multi-level Resources](#multi-level-resources)
  - [One-to-One Grouping](#one-to-one-grouping)
- [Grouping by Resources](#grouping-by-resources)
  - [Vertical Resource View](#vertical-resource-view)
  - [Timeline Resource View](#timeline-resource-view)
- [Grouping by Dates](#grouping-by-dates)
- [Resource Colorization](#resource-colorization)
- [Custom Work Hours Per Resource](#custom-work-hours-per-resource)
  - [Different Work Days](#different-work-days)
  - [Different Work Hours](#different-work-hours)
- [Expandable Groups](#expandable-groups)
- [Additional Features](#additional-features)
  - [Shared Events](#shared-events)
  - [Dynamic Resources](#dynamic-resources)
  - [Resource Header Customization](#resource-header-customization)
  - [Hide Non-Working Days](#hide-non-working-days)

## Overview

The Scheduler supports resources and grouping, allowing multiple resources to share the component. Resources can be displayed in:
- **Vertical hierarchy** (Calendar views)
- **Expandable groups** (Timeline views)

Key capabilities:
- Single or multiple resource assignment to appointments
- Multi-level resource hierarchies
- Grouping by resources or dates
- Custom work hours and days per resource
- Remote and local data binding

## Resource Fields

Configure resources using the `resources` collection with these fields:

| Field | Type | Description |
|-------|------|-------------|
| `field` | String | Maps to the event object's resource field |
| `title` | String | Displays in the event editor window |
| `name` | String | Unique identifier for grouping |
| `allowMultiple` | Boolean | Allows multiple resource selection |
| `dataSource` | Object | Array or DataManager for resource data |
| `query` | Query | External query for data processing |
| `idField` | String | Resource ID field name |
| `textField` | String | Display text field name |
| `colorField` | String | Color field for event styling |
| `groupIDField` | String | Parent resource ID for hierarchical grouping |
| `expandedField` | String | Initial expand/collapse state (timeline views) |
| `startHourField` | String | Custom work start hours |
| `endHourField` | String | Custom work end hours |
| `workDaysField` | String | Custom working days |
| `cssClassField` | String | Custom CSS classes for events |

**Basic Resource Configuration:**

```tsx
import { ResourcesDirective, ResourceDirective } from '@syncfusion/ej2-react-schedule';

<ResourcesDirective>
  <ResourceDirective 
    field='OwnerId' 
    title='Owner' 
    name='Owners' 
    dataSource={ownerData} 
    textField='OwnerText' 
    idField='Id' 
    colorField='OwnerColor'
  />
</ResourcesDirective>
```

## Resource Data Binding

### Local JSON Data

Bind local data directly to the resource `dataSource`:

```tsx
import { useState } from 'react';
import { ScheduleComponent, ResourcesDirective, ResourceDirective } from '@syncfusion/ej2-react-schedule';

const App = () => {
  const [ownerData] = useState([
    { OwnerText: 'Nancy', Id: 1, OwnerColor: '#ffaa00' },
    { OwnerText: 'Steven', Id: 2, OwnerColor: '#f8a398' },
    { OwnerText: 'Michael', Id: 3, OwnerColor: '#7499e1' }
  ]);

  return (
    <ScheduleComponent eventSettings={{ dataSource: resourceData }}>
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
    </ScheduleComponent>
  );
};
```

### Remote Service URL

Use DataManager with adaptors for remote data:

```tsx
import { DataManager, UrlAdaptor } from '@syncfusion/ej2-data';

const ownerData = new DataManager({
  url: 'Home/GetResourceData',
  adaptor: new UrlAdaptor(),
  crossDomain: true
});

<ResourceDirective 
  field='OwnerId' 
  title='Owner' 
  name='Owners' 
  dataSource={ownerData} 
  textField='OwnerText' 
  idField='Id' 
  colorField='OwnerColor'
/>
```

## Single Resource Assignment

Display Scheduler without visible resource grouping, but allow resource assignment in the event editor:

```tsx
const App = () => {
  const ownerData = [
    { OwnerText: 'Nancy', Id: 1, OwnerColor: '#ffaa00' },
    { OwnerText: 'Steven', Id: 2, OwnerColor: '#f8a398' },
    { OwnerText: 'Michael', Id: 3, OwnerColor: '#7499e1' }
  ];

  return (
    <ScheduleComponent eventSettings={{ dataSource: resourceData }}>
      {/* No group property - displays default view */}
      <ResourcesDirective>
        <ResourceDirective 
          field='OwnerId' 
          title='Owner' 
          name='Owners' 
          allowMultiple={false}
          dataSource={ownerData} 
          textField='OwnerText' 
          idField='Id' 
          colorField='OwnerColor'
        />
      </ResourcesDirective>
    </ScheduleComponent>
  );
};
```

Appointments are differentiated by resource colors without grouping UI.

## Multiple Resource Assignment

Enable `allowMultiple` to assign appointments to multiple resources:

```tsx
<ResourceDirective 
  field='OwnerId' 
  title='Owner' 
  name='Owners' 
  allowMultiple={true}  // Enables multiple selection
  dataSource={ownerData} 
  textField='OwnerText' 
  idField='Id' 
  colorField='OwnerColor'
/>
```

When `allowMultiple={true}`:
- Event editor shows multi-select for resources
- Creates multiple appointment instances
- Each instance appears under its respective resource

## Hierarchical Grouping

### Multi-level Resources

Establish parent-child relationships using `groupIDField`:

```tsx
const App = () => {
  const roomData = [
    { RoomText: 'ROOM 1', Id: 1, RoomColor: '#cb6bb2' },
    { RoomText: 'ROOM 2', Id: 2, RoomColor: '#56ca85' }
  ];

  const ownerData = [
    { OwnerText: 'Nancy', Id: 1, GroupId: 1, OwnerColor: '#ffaa00' },
    { OwnerText: 'Steven', Id: 2, GroupId: 2, OwnerColor: '#f8a398' },
    { OwnerText: 'Michael', Id: 3, GroupId: 1, OwnerColor: '#7499e1' }
  ];

  const group = { resources: ['Rooms', 'Owners'] };

  return (
    <ScheduleComponent group={group} eventSettings={{ dataSource: resourceData }}>
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
          groupIDField='GroupId'  // Links to parent Room Id
          colorField='OwnerColor'
        />
      </ResourcesDirective>
    </ScheduleComponent>
  );
};
```

### One-to-One Grouping

Display all child resources against each parent by setting `byGroupID: false`:

```tsx
const group = { 
  byGroupID: false,  // Shows all child resources for each parent
  resources: ['Rooms', 'Owners'] 
};

const ownerData = [
  { OwnerText: 'Nancy', Id: 1, OwnerColor: '#ffaa00' },
  { OwnerText: 'Steven', Id: 2, OwnerColor: '#f8a398' }
];

// Creates matrix: ROOM 1 x Nancy, ROOM 1 x Steven, ROOM 2 x Nancy, ROOM 2 x Steven
```

## Grouping by Resources

### Vertical Resource View

Display resources in columns (calendar views):

```tsx
const App = () => {
  const projectData = [
    { text: 'PROJECT 1', id: 1, color: '#cb6bb2' },
    { text: 'PROJECT 2', id: 2, color: '#56ca85' }
  ];

  const categoryData = [
    { text: 'Development', id: 1, color: '#1aaa55' },
    { text: 'Testing', id: 2, color: '#7fa900' }
  ];

  const group = { 
    byGroupID: false, 
    resources: ['Projects', 'Categories'] 
  };

  return (
    <ScheduleComponent currentView='Month' group={group}>
      <ResourcesDirective>
        <ResourceDirective 
          field='ProjectId' 
          title='Choose Project' 
          name='Projects' 
          dataSource={projectData} 
          textField='text' 
          idField='id' 
          colorField='color'
        />
        <ResourceDirective 
          field='TaskId' 
          title='Category' 
          name='Categories' 
          allowMultiple={true}
          dataSource={categoryData} 
          textField='text' 
          idField='id' 
          colorField='color'
        />
      </ResourcesDirective>
    </ScheduleComponent>
  );
};
```

### Timeline Resource View

Display resources horizontally (timeline views):

```tsx
import { TimelineViews, TimelineMonth } from '@syncfusion/ej2-react-schedule';

const App = () => {
  const group = { resources: ['Rooms', 'Owners'] };

  return (
    <ScheduleComponent 
      currentView='TimelineWeek' 
      group={group}
      eventSettings={{ dataSource: resourceData }}
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
```

## Grouping by Dates

Group resources horizontally under each date (calendar views only):

```tsx
const App = () => {
  const group = { 
    byDate: true,  // Groups resources by date
    resources: ['Owners'] 
  };

  const resourceData = [
    { text: 'Alice', id: 1, color: '#1aaa55' },
    { text: 'Smith', id: 2, color: '#7fa900' }
  ];

  return (
    <ScheduleComponent group={group}>
      <ResourcesDirective>
        <ResourceDirective 
          field='OwnerId' 
          title='Owner' 
          name='Owners' 
          allowMultiple={true}
          dataSource={resourceData} 
          textField='text' 
          idField='id' 
          colorField='color'
        />
      </ResourcesDirective>
      <ViewsDirective>
        <ViewDirective option='Week' />
        <ViewDirective option='Month' />
        <ViewDirective option='Agenda' />
      </ViewsDirective>
    </ScheduleComponent>
  );
};
```

> **Note:** Grouping by date is not applicable in timeline views.

## Resource Colorization

### Default Behavior

Colors from the top-level resource apply to events by default.

### Custom Resource Color Selection

Choose which resource level colors to apply using `resourceColorField`:

```tsx
import { useRef } from 'react';
import { RadioButtonComponent } from '@syncfusion/ej2-react-buttons';

const App = () => {
  const scheduleObj = useRef<ScheduleComponent>(null);
  
  const eventSettings = { 
    dataSource: resourceData, 
    resourceColorField: 'Rooms'  // Use Room colors instead of Owner colors
  };

  const onChange = (args) => {
    scheduleObj.current.eventSettings.resourceColorField = args.value;
  };

  return (
    <div>
      <RadioButtonComponent 
        value='Rooms' 
        name='default' 
        label='Rooms' 
        checked={true} 
        change={onChange} 
      />
      <RadioButtonComponent 
        value='Owners' 
        name='default' 
        label='Owners' 
        change={onChange}
      />
      <ScheduleComponent 
        ref={scheduleObj} 
        eventSettings={eventSettings}
        group={{ resources: ['Rooms', 'Owners'] }}
      >
        <ResourcesDirective>
          <ResourceDirective 
            field='RoomId' 
            title='Room' 
            name='Rooms'
            dataSource={roomData} 
            colorField='RoomColor'
          />
          <ResourceDirective 
            field='OwnerId' 
            title='Owner' 
            name='Owners'
            dataSource={ownerData} 
            colorField='OwnerColor'
          />
        </ResourcesDirective>
      </ScheduleComponent>
    </div>
  );
};
```

> **Note:** The `resourceColorField` value must match a resource `name` value.

## Custom Work Hours Per Resource

### Different Work Days

Customize working days per resource using `workDaysField`:

```tsx
const App = () => {
  const resourceData = [
    { 
      text: 'Will Smith', 
      id: 1, 
      color: '#ea7a57', 
      workDays: [1, 2, 4, 5]  // Monday, Tuesday, Thursday, Friday
    },
    { 
      text: 'Alice', 
      id: 2, 
      color: '#357cd2', 
      workDays: [1, 3, 5]  // Monday, Wednesday, Friday
    },
    { 
      text: 'Robson', 
      id: 3, 
      color: '#7fa900', 
      workDays: [2, 6]  // Tuesday, Saturday
    }
  ];

  return (
    <ScheduleComponent 
      currentView='WorkWeek' 
      group={{ resources: ['Doctors'] }}
    >
      <ResourcesDirective>
        <ResourceDirective 
          field='DoctorId' 
          title='Doctor' 
          name='Doctors' 
          dataSource={resourceData} 
          textField='text' 
          idField='id' 
          colorField='color' 
          workDaysField='workDays'  // Maps to workDays property
        />
      </ResourcesDirective>
    </ScheduleComponent>
  );
};
```

Day indexes: `0` (Sunday) to `6` (Saturday)

> **Note:** Applicable only to calendar views, not timeline views.

### Different Work Hours

Set custom start and end times per resource:

```tsx
const App = () => {
  const resourceData = [
    { 
      text: 'Will Smith', 
      id: 1, 
      startHour: '07:00', 
      endHour: '13:00'  // 7 AM - 1 PM
    },
    { 
      text: 'Alice', 
      id: 2, 
      startHour: '09:00', 
      endHour: '17:00'  // 9 AM - 5 PM
    },
    { 
      text: 'Robson', 
      id: 3, 
      startHour: '08:00', 
      endHour: '16:00'  // 8 AM - 4 PM
    }
  ];

  return (
    <ScheduleComponent group={{ resources: ['Doctors'] }}>
      <ResourcesDirective>
        <ResourceDirective 
          field='DoctorId' 
          title='Doctor' 
          name='Doctors' 
          dataSource={resourceData} 
          startHourField='startHour'  // Maps to startHour property
          endHourField='endHour'  // Maps to endHour property
          workDaysField='workDays'
        />
      </ResourcesDirective>
    </ScheduleComponent>
  );
};
```

Work hours are visually highlighted with active colors on the Scheduler.

## Expandable Groups

Control resource expansion/collapse state in timeline views using `expandedField`:

```tsx
const App = () => {
  const roomData = [
    { 
      RoomText: 'ROOM 1', 
      Id: 1, 
      RoomColor: '#cb6bb2', 
      IsExpand: false  // Initially collapsed
    },
    { 
      RoomText: 'ROOM 2', 
      Id: 2, 
      RoomColor: '#56ca85'  // Expanded by default
    }
  ];

  const ownerData = [
    { OwnerText: 'Nancy', Id: 1, GroupId: 1, OwnerColor: '#ffaa00' },
    { OwnerText: 'Steven', Id: 2, GroupId: 2, OwnerColor: '#f8a398' },
    { OwnerText: 'Michael', Id: 3, GroupId: 1, OwnerColor: '#7499e1' }
  ];

  return (
    <ScheduleComponent 
      currentView='TimelineWeek' 
      group={{ resources: ['Rooms', 'Owners'] }}
    >
      <ResourcesDirective>
        <ResourceDirective 
          field='RoomId' 
          title='Room' 
          name='Rooms'
          dataSource={roomData} 
          expandedField='IsExpand'  // Controls expand/collapse
        />
        <ResourceDirective 
          field='OwnerId' 
          title='Owner' 
          name='Owners'
          dataSource={ownerData} 
          groupIDField='GroupId'
        />
      </ResourcesDirective>
    </ScheduleComponent>
  );
};
```

Default: `true` (expanded)

## Additional Features

### Shared Events

Enable `allowGroupEdit` to edit shared events across all related resource instances:

```tsx
const App = () => {
  const conferenceData = [
    { Text: 'Margaret', Id: 1, Color: '#1aaa55' },
    { Text: 'Robert', Id: 2, Color: '#357cd2' },
    { Text: 'Laura', Id: 3, Color: '#7fa900' }
  ];

  const data = [
    {
      Id: 1,
      Subject: 'Burning Man',
      StartTime: new Date(2018, 5, 1, 15, 0),
      EndTime: new Date(2018, 5, 1, 17, 0),
      ConferenceId: [1, 2, 3]  // Shared across multiple resources
    }
  ];

  const group = { 
    allowGroupEdit: true,  // Enable shared event editing
    resources: ['Conferences'] 
  };

  return (
    <ScheduleComponent group={group} eventSettings={{ dataSource: data }}>
      <ResourcesDirective>
        <ResourceDirective 
          field='ConferenceId' 
          title='Conference' 
          name='Conferences' 
          allowMultiple={true}
          dataSource={conferenceData}
        />
      </ResourcesDirective>
    </ScheduleComponent>
  );
};
```

When enabled:
- Single appointment object maintained
- CRUD actions reflect across all instances
- Resource field holds multiple resource IDs

### Dynamic Resources

Add or remove resources dynamically using `addResource` and `removeResource` methods:

```tsx
import { useRef } from 'react';
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';

const App = () => {
  const scheduleObj = useRef<ScheduleComponent>(null);

  const calendarCollections = [
    { CalendarText: 'My Calendar', CalendarId: 1, CalendarColor: '#c43081' },
    { CalendarText: 'Company', CalendarId: 2, CalendarColor: '#ff7f50' },
    { CalendarText: 'Birthday', CalendarId: 3, CalendarColor: '#AF27CD' }
  ];

  const onChange = (args) => {
    const value = parseInt(args.event.currentTarget.querySelector('input').getAttribute('value'), 10);
    const resourceData = calendarCollections.filter(item => item.CalendarId === value);
    
    if (args.checked) {
      scheduleObj.current.addResource(resourceData[0], 'Calendars', value);
    } else {
      scheduleObj.current.removeResource(value, 'Calendars');
    }
  };

  return (
    <div>
      <CheckBoxComponent value='1' checked={true} label='My Calendar' change={onChange} />
      <CheckBoxComponent value='2' checked={false} label='Company' change={onChange} />
      <CheckBoxComponent value='3' checked={false} label='Birthday' change={onChange} />
      
      <ScheduleComponent 
        ref={scheduleObj} 
        group={{ resources: ['Calendars'] }}
      >
        <ResourcesDirective>
          <ResourceDirective 
            field='CalendarId' 
            title='Calendar' 
            name='Calendars'
            dataSource={[calendarCollections[0]]}
          />
        </ResourcesDirective>
      </ScheduleComponent>
    </div>
  );
};
```

### Resource Header Customization

Customize resource headers with templates:

```tsx
const App = () => {
  const getDoctorName = (value) => {
    return value.resourceData[value.resource.textField];
  };

  const getDoctorLevel = (value) => {
    const name = getDoctorName(value);
    return name === 'Will Smith' ? 'Cardiologist' : 
           name === 'Alice' ? 'Neurologist' : 'Orthopedic Surgeon';
  };

  const resourceHeaderTemplate = (props) => (
    <div className="template-wrap">
      <div className="resource-detail">
        <div className="resource-name">{getDoctorName(props)}</div>
        <div className="resource-designation">{getDoctorLevel(props)}</div>
      </div>
    </div>
  );

  return (
    <ScheduleComponent resourceHeaderTemplate={resourceHeaderTemplate}>
      <ResourcesDirective>
        <ResourceDirective 
          field='DoctorId' 
          name='Doctors' 
          dataSource={resourceData}
        />
      </ResourcesDirective>
    </ScheduleComponent>
  );
};
```

### Hide Non-Working Days

Hide non-working days when grouped by date:

```tsx
const App = () => {
  const resourceData = [
    { text: 'Alice', id: 1, workDays: [1, 2, 3, 4] },
    { text: 'Smith', id: 2, workDays: [2, 3, 5] }
  ];

  const group = { 
    byDate: true, 
    resources: ['Owners'],
    hideNonWorkingDays: true  // Only shows custom work days
  };

  return (
    <ScheduleComponent group={group}>
      <ResourcesDirective>
        <ResourceDirective 
          field='OwnerId' 
          name='Owners' 
          dataSource={resourceData}
          workDaysField='workDays'
        />
      </ResourcesDirective>
    </ScheduleComponent>
  );
};
```

> **Note:** Only applies when `byDate: true` is set.
