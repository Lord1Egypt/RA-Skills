# Customization

## Table of Contents

- [Overview](#overview)
- [Event Editor Customization](#event-editor-customization)
  - [Default Editor Fields](#default-editor-fields)
  - [Custom Editor Template](#custom-editor-template)
  - [Adding Custom Fields](#adding-custom-fields)
  - [Editor Validation](#editor-validation)
- [Cell Template Customization](#cell-template-customization)
  - [Date Header Template](#date-header-template)
  - [Cell Template](#cell-template)
  - [Month Cell Template](#month-cell-template)
  - [Resource Header Template](#resource-header-template)
- [Event Rendering Templates](#event-rendering-templates)
- [Quick Info Templates](#quick-info-templates)
- [Tooltip Customization](#tooltip-customization)

## Overview

The Syncfusion React Scheduler provides extensive customization options to tailor the appearance and behavior of various components. You can customize editor windows, cell templates, event rendering, quick info popups, and tooltips to match your application's requirements and design standards.

Key customization areas include:
- **Event Editor**: Customize fields, templates, validation, and header/footer sections
- **Cell Templates**: Customize date headers, work cells, month cells, and resource headers
- **Event Templates**: Control how events are rendered on the scheduler
- **Quick Info Popups**: Customize the quick view that appears on cell or event clicks
- **Tooltips**: Customize tooltip appearance and content

## Event Editor Customization

### Default Editor Fields

The Scheduler displays a detailed event editor window when cells or events are double-clicked. The editor contains default fields like Subject, Location, Start Time, End Time, and Description.

**Changing Editor Window Labels**

You can customize field labels using the `fields` option within `eventSettings`:

```tsx
import * as React from 'react';
import { ScheduleComponent, Day, Week, Month, Inject } from '@syncfusion/ej2-react-schedule';

const App = () => {
  const fieldsData = {
    id: 'Id',
    subject: { name: 'Subject', title: 'Event Name' },
    location: { name: 'Location', title: 'Event Location' },
    description: { name: 'Description', title: 'Event Description' },
    startTime: { name: 'StartTime', title: 'Start Duration' },
    endTime: { name: 'EndTime', title: 'End Duration' }
  };
  
  const eventSettings = { 
    dataSource: scheduleData, 
    fields: fieldsData 
  };

  return (
    <ScheduleComponent eventSettings={eventSettings}>
      <Inject services={[Day, Week, Month]} />
    </ScheduleComponent>
  );
};
```

**Changing Header and Footer Button Text**

Customize the editor window header title and footer button text using localization:

```tsx
import { L10n } from '@syncfusion/ej2-base';

L10n.load({
  'en-US': {
    'schedule': {
      'saveButton': 'Add',
      'cancelButton': 'Close',
      'deleteButton': 'Remove',
      'newEvent': 'Add Event',
    },
  }
});
```

**Customizing Time Duration**

Change the default time duration in the editor window by modifying the `duration` property in the `popupOpen` event:

```tsx
const onPopupOpen = (args) => {
  if (args.type === 'Editor') {
    args.duration = 60; // Set to 60 minutes
  }
};

<ScheduleComponent popupOpen={onPopupOpen}>
  {/* ... */}
</ScheduleComponent>
```

**Preventing Editor Display**

Prevent the editor window from opening by setting `cancel` to `true`:

```tsx
const onPopupOpen = (args) => {
  if (args.type === 'Editor') {
    args.cancel = true;
  }
};
```

**Customizing Timezone Collection**

Customize timezone collections in the editor using the `timezoneDataSource` property:

```tsx
<ScheduleComponent 
  timezoneDataSource={[
    { Value: 'Pacific/Niue', Text: 'Niue' },
    { Value: 'Pacific/Honolulu', Text: 'Hawaii Time' },
    { Value: 'Pacific/Tahiti', Text: 'Tahiti' },
  ]}
>
  {/* ... */}
</ScheduleComponent>
```

### Custom Editor Template

Create a fully customized editor window using the `editorTemplate` property:

```tsx
import { DateTimePickerComponent } from '@syncfusion/ej2-react-calendars';
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';

const editorTemplate = (props) => {
  return (
    props !== undefined ? (
      <table className="custom-event-editor" style={{ width: '100%', padding: '5' }}>
        <tbody>
          <tr>
            <td className="e-textlabel">Summary</td>
            <td colSpan={4}>
              <input 
                id="Summary" 
                className="e-field e-input" 
                type="text" 
                name="Subject" 
                style={{ width: '100%' }} 
              />
            </td>
          </tr>
          <tr>
            <td className="e-textlabel">Status</td>
            <td colSpan={4}>
              <DropDownListComponent 
                id="EventType" 
                placeholder='Choose status' 
                data-name="EventType" 
                className="e-field" 
                style={{ width: '100%' }} 
                dataSource={['New', 'Requested', 'Confirmed']} 
                value={props.EventType || null}
              />
            </td>
          </tr>
          <tr>
            <td className="e-textlabel">From</td>
            <td colSpan={4}>
              <DateTimePickerComponent 
                format='dd/MM/yy hh:mm a' 
                id="StartTime" 
                data-name="StartTime" 
                value={new Date(props.startTime || props.StartTime)} 
                className="e-field"
              />
            </td>
          </tr>
          <tr>
            <td className="e-textlabel">To</td>
            <td colSpan={4}>
              <DateTimePickerComponent 
                format='dd/MM/yy hh:mm a' 
                id="EndTime" 
                data-name="EndTime" 
                value={new Date(props.endTime || props.EndTime)} 
                className="e-field"
              />
            </td>
          </tr>
          <tr>
            <td className="e-textlabel">Reason</td>
            <td colSpan={4}>
              <textarea 
                id="Description" 
                className="e-field e-input" 
                name="Description" 
                rows={3} 
                cols={50} 
                style={{ width: '100%', height: '60px', resize: 'vertical' }}
              />
            </td>
          </tr>
        </tbody>
      </table>
    ) : <div></div>
  );
};

<ScheduleComponent editorTemplate={editorTemplate} showQuickInfo={false}>
  {/* ... */}
</ScheduleComponent>
```

> **Note**: Fields with the `e-field` class are processed automatically for DropDownList, DateTimePicker, MultiSelect, DatePicker, CheckBox, and TextBox components.

**Customizing Header and Footer Templates**

Customize the editor header and footer using `editorHeaderTemplate` and `editorFooterTemplate`:

```tsx
const editorHeaderTemplate = (props) => {
  return (
    <div id="event-header">
      {props !== undefined ? 
        (props.Subject ? <div>{props.Subject}</div> : <div>Create New Event</div>) 
        : <div></div>
      }
    </div>
  );
};

const editorFooterTemplate = () => {
  return (
    <div id="event-footer">
      <div id="verify">
        <input type="checkbox" id="check-box" value="unchecked" />
        <label htmlFor="check-box">Verified</label>
      </div>
      <div id="right-button">
        <button id="Save" className="e-control e-btn e-primary" disabled>
          Save
        </button>
        <button id="Cancel" className="e-control e-btn e-primary">
          Cancel
        </button>
      </div>
    </div>
  );
};

<ScheduleComponent 
  editorHeaderTemplate={editorHeaderTemplate}
  editorFooterTemplate={editorFooterTemplate}
>
  {/* ... */}
</ScheduleComponent>
```

### Adding Custom Fields

Add custom fields to the default editor using the `popupOpen` event:

```tsx
import { createElement } from '@syncfusion/ej2-base';
import { DropDownList } from '@syncfusion/ej2-dropdowns';

const onPopupOpen = (args) => {
  if (args.type === 'Editor') {
    if (!args.element.querySelector('.custom-field-row')) {
      let row = createElement('div', { className: 'custom-field-row' });
      let formElement = args.element.querySelector('.e-schedule-form');
      formElement.firstChild.insertBefore(row, formElement.firstChild.firstChild);
      
      let container = createElement('div', { className: 'custom-field-container' });
      let inputEle = createElement('input', {
        className: 'e-field', 
        attrs: { name: 'EventType' }
      });
      container.appendChild(inputEle);
      row.appendChild(container);
      
      let dropDownList = new DropDownList({
        dataSource: [
          { text: 'Public Event', value: 'public-event' },
          { text: 'Maintenance', value: 'maintenance' },
          { text: 'Commercial Event', value: 'commercial-event' }
        ],
        fields: { text: 'text', value: 'value' },
        value: args.data.EventType,
        floatLabelType: 'Always',
        placeholder: 'Event Type'
      });
      dropDownList.appendTo(inputEle);
    }
  }
};
```

**Adding Resource Fields**

Include resource fields with multiple selection support:

```tsx
import { MultiSelectComponent } from '@syncfusion/ej2-react-dropdowns';

const ownerData = [
  { OwnerText: 'Nancy', Id: 1, OwnerColor: '#ffaa00' },
  { OwnerText: 'Steven', Id: 2, OwnerColor: '#f8a398' },
  { OwnerText: 'Michael', Id: 3, OwnerColor: '#7499e1' }
];

const editorTemplate = (props) => {
  return (
    <table className="custom-event-editor">
      <tbody>
        <tr>
          <td className="e-textlabel">Owner</td>
          <td colSpan={4}>
            <MultiSelectComponent 
              className="e-field" 
              placeholder='Choose owner' 
              data-name="OwnerId" 
              dataSource={ownerData} 
              fields={{ text: 'OwnerText', value: 'Id' }} 
              value={props.OwnerId} 
            />
          </td>
        </tr>
        {/* Other fields */}
      </tbody>
    </table>
  );
};
```

**Adding Recurrence Options**

Include recurrence editor in custom template:

```tsx
import { RecurrenceEditorComponent } from '@syncfusion/ej2-react-schedule';

const editorTemplate = (props) => {
  return (
    <table className="custom-event-editor">
      <tbody>
        {/* Other fields */}
        <tr>
          <td className="e-textlabel">Recurrence</td>
          <td colSpan={4}>
            <RecurrenceEditorComponent id="RecurrenceEditor" />
          </td>
        </tr>
      </tbody>
    </table>
  );
};

const onPopupClose = (args) => {
  if (args.type === 'Editor' && args.data) {
    args.data.RecurrenceRule = recurrObject.current.value;
  }
};
```

### Editor Validation

Apply validation rules to editor fields using the `fields` property:

```tsx
const minValidation = (args) => {
  return args['value'].length >= 5;
};

const fieldsData = {
  id: 'Id',
  subject: { 
    name: 'Subject', 
    validation: { required: true } 
  },
  location: { 
    name: 'Location', 
    validation: { required: true } 
  },
  description: {
    name: 'Description', 
    validation: {
      required: true, 
      minLength: [minValidation, 'Need at least 5 letters']
    }
  },
  startTime: { 
    name: 'StartTime', 
    validation: { required: true } 
  },
  endTime: { 
    name: 'EndTime', 
    validation: { required: true } 
  }
};

const eventSettings = { 
  dataSource: scheduleData, 
  fields: fieldsData 
};
```

**Validating Custom Template Fields**

Apply validation to custom template fields:

```tsx
import { FormValidator } from '@syncfusion/ej2-inputs';
import { isNullOrUndefined } from '@syncfusion/ej2-base';

const onPopupOpen = (args) => {
  if (args.type === 'Editor') {
    let statusElement = args.element.querySelector('#EventType');
    if (statusElement) {
      statusElement.setAttribute('name', 'EventType');
    }
    
    if (!isNullOrUndefined(document.getElementById("EventType_Error"))) {
      document.getElementById("EventType_Error").style.display = "none";
    }
    
    let formElement = args.element.querySelector('.e-schedule-form');
    let validator = formElement.ej2_instances[0];
    validator.addRules('EventType', { required: true });
  }
};
```

**Saving Custom Editor Data**

Use the `popupClose` event to save customized editor data:

```tsx
const onPopupClose = (args) => {
  if (args.type === 'Editor' && !isNullOrUndefined(args.data)) {
    let subjectElement = args.element.querySelector('#Summary');
    if (subjectElement) {
      args.data.Subject = subjectElement.value;
    }
    
    let statusElement = args.element.querySelector('#EventType');
    if (statusElement) {
      args.data.EventType = statusElement.value;
    }
    
    args.data.StartTime = startObj.current.value;
    args.data.EndTime = endObj.current.value;
    
    let descriptionElement = args.element.querySelector('#Description');
    if (descriptionElement) {
      args.data.Description = descriptionElement.value;
    }
  }
};
```

**Manually Closing Editor**

Close the editor programmatically using the `closeEditor` method:

```tsx
import { useRef } from 'react';

const scheduleObj = useRef(null);

const onCloseEditor = () => {
  scheduleObj.current.closeEditor();
};

<ScheduleComponent ref={scheduleObj}>
  {/* ... */}
</ScheduleComponent>
```

## Cell Template Customization

### Date Header Template

Cells can be customized in all views using templates or the `renderCell` event.

**Setting Cell Dimensions**

Customize cell height and width using the `cssClass` property:

```tsx
<ScheduleComponent cssClass='schedule-cell-dimension'>
  {/* ... */}
</ScheduleComponent>
```

```css
.schedule-cell-dimension.e-schedule .e-vertical-view .e-time-cells-wrap table td,
.schedule-cell-dimension.e-schedule .e-vertical-view .e-work-cells {
  height: 50px;
}

.schedule-cell-dimension.e-schedule .e-month-view .e-work-cells {
  height: 80px;
}
```

**Checking Cell Availability**

Check if time slots are available using `isSlotAvailable`:

```tsx
import { useRef } from 'react';

const scheduleObj = useRef(null);

const onActionBegin = (args) => {
  if (args.requestType === 'eventCreate' && args.data.length > 0) {
    let eventData = args.data[0];
    let eventField = scheduleObj.current.eventFields;
    let startDate = eventData[eventField.startTime];
    let endDate = eventData[eventField.endTime];
    args.cancel = !scheduleObj.current.isSlotAvailable(startDate, endDate);
  }
};
```

### Cell Template

Customize cell appearance using the `cellTemplate` property:

```tsx
const getWorkCellText = (date) => {
  let weekEnds = [0, 6];
  if (weekEnds.indexOf(date.getDay()) >= 0) {
    return "<img src='weekend-icon.svg' />";
  }
  return '';
};

const cellTemplate = (props) => {
  if (props.type === "workCells") {
    return (
      <div 
        className="templatewrap" 
        dangerouslySetInnerHTML={{ __html: getWorkCellText(props.date) }}
      />
    );
  }
  return <div></div>;
};

<ScheduleComponent cellTemplate={cellTemplate}>
  {/* ... */}
</ScheduleComponent>
```

**Using renderCell Event**

An alternative approach using the `renderCell` event:

```tsx
import { createElement } from '@syncfusion/ej2-base';

const onRenderCell = (args) => {
  if (args.elementType === 'workCells' || args.elementType === 'monthCells') {
    let weekEnds = [0, 6];
    if (weekEnds.indexOf(args.date.getDay()) >= 0) {
      let ele = createElement('div', {
        innerHTML: "<img src='weekend-icon.svg' />",
        className: 'templatewrap'
      });
      args.element.appendChild(ele);
    }
  }
};

<ScheduleComponent renderCell={onRenderCell}>
  {/* ... */}
</ScheduleComponent>
```

**RenderCell Element Types**

The `renderCell` event provides access to different element types:

| Element Type | Description |
|--------------|-------------|
| dateHeader | Header cell rendering |
| monthDay | Header cell in month view |
| resourceHeader | Resource header cell |
| alldayCells | All-day cell rendering |
| emptyCells | Empty cell on header bar |
| resourceGroupCells | Work cells for parent resource |
| workCells | Work cell rendering |
| monthCells | Month cell rendering |
| majorSlot | Major time slot cell |
| minorSlot | Minor time slot cell |
| weekNumberCell | Week number cell |

### Month Cell Template

Customize month cells with specific content:

```tsx
const getMonthCellContent = (date) => {
  if (date.getMonth() === 11 && date.getDate() === 25) {
    return '<img src="christmas.svg" />';
  } else if (date.getMonth() === 0 && date.getDate() === 1) {
    return '<img src="newyear.svg" />';
  }
  return '';
};

const cellTemplate = (props) => {
  if (props.type === "monthCells") {
    return (
      <div 
        className="templatewrap" 
        dangerouslySetInnerHTML={{ __html: getMonthCellContent(props.date) }}
      />
    );
  }
  return <div></div>;
};
```

**Customizing Month Cell Header**

Use `cellHeaderTemplate` to customize month cell headers:

```tsx
import { Internationalization } from '@syncfusion/ej2-base';

const instance = new Internationalization();

const getDateHeaderText = (props) => {
  return (
    <div>
      {instance.formatDate(props.date, { skeleton: "Ed" })}
    </div>
  );
};

<ScheduleComponent cellHeaderTemplate={getDateHeaderText}>
  {/* ... */}
</ScheduleComponent>
```

**Customizing Weekend Cell Background**

Customize weekend cell colors:

```tsx
const onRenderCell = (args) => {
  if (args.elementType === "workCells") {
    if (args.date && (args.date.getDay() === 0 || args.date.getDay() === 6)) {
      args.element.style.background = '#ffdea2';
    }
  }
};
```

For month view, use CSS:

```css
.schedule-cell-customization.e-schedule .e-month-view .e-work-cells:not(.e-work-days) {
  background-color: #f08080;
}
```

**Setting Min/Max Date Range**

Restrict date navigation using `minDate` and `maxDate`:

```tsx
<ScheduleComponent 
  minDate={new Date(2017, 4, 17)}
  maxDate={new Date(2018, 5, 17)}
>
  {/* ... */}
</ScheduleComponent>
```

### Resource Header Template

When using resources, you can customize resource headers using the `resourceHeaderTemplate` within the resource configuration:

```tsx
import { ResourcesDirective, ResourceDirective } from '@syncfusion/ej2-react-schedule';

const resourceHeaderTemplate = (props) => {
  return (
    <div className="resource-header">
      <div className="resource-image">
        <img src={props.resourceData.Image} alt={props.resourceData.Text} />
      </div>
      <div className="resource-name">{props.resourceData.Text}</div>
    </div>
  );
};

<ScheduleComponent>
  <ResourcesDirective>
    <ResourceDirective 
      field='OwnerId' 
      title='Owner' 
      name='Owners' 
      dataSource={ownerData} 
      textField='Text' 
      idField='Id' 
      resourceHeaderTemplate={resourceHeaderTemplate}
    />
  </ResourcesDirective>
  {/* ... */}
</ScheduleComponent>
```

## Event Rendering Templates

Customize how events are rendered on the scheduler using the `eventTemplate` property:

```tsx
const eventTemplate = (props) => {
  return (
    <div className="template-wrap" style={{ background: props.Color }}>
      <div className="subject">{props.Subject}</div>
      <div className="time">
        {props.StartTime.toLocaleString()} - {props.EndTime.toLocaleString()}
      </div>
    </div>
  );
};

<ScheduleComponent eventSettings={{ template: eventTemplate }}>
  {/* ... */}
</ScheduleComponent>
```

## Quick Info Templates

Quick info popups appear on single-clicking cells or events. Customize them using the `quickInfoTemplates` property.

**Disabling Quick Info Popups**

```tsx
<ScheduleComponent showQuickInfo={false}>
  {/* ... */}
</ScheduleComponent>
```

**Opening Quick Info on Multiple Cell Selection**

```tsx
<ScheduleComponent quickInfoOnSelectionEnd={true}>
  {/* ... */}
</ScheduleComponent>
```

**Customizing Quick Info Watermark**

```tsx
L10n.load({
  'en-US': {
    'schedule': {
      'addTitle': 'New Title'
    }
  }
});
```

**Custom Quick Info Templates**

```tsx
import { useRef } from 'react';
import { isNullOrUndefined } from '@syncfusion/ej2-base';

const scheduleObj = useRef(null);

const header = (props) => {
  return (
    <div>
      {props.elementType === "cell" ? (
        <div className="e-cell-header e-popup-header">
          <div className="e-header-icon-wrapper">
            <button 
              id="close" 
              className="e-close e-close-icon e-icons" 
              title="Close"
              onClick={buttonClickActions}
            />
          </div>
        </div>
      ) : (
        <div className="e-event-header e-popup-header">
          <div className="e-header-icon-wrapper">
            <button 
              id="close" 
              className="e-close e-close-icon e-icons" 
              title="CLOSE"
              onClick={buttonClickActions}
            />
          </div>
        </div>
      )}
    </div>
  );
};

const content = (props) => {
  return (
    <div>
      {props.elementType === "cell" ? (
        <div className="e-cell-content e-template">
          <form className="e-schedule-form">
            <div>
              <input 
                className="subject e-field e-input" 
                type="text" 
                name="Subject" 
                placeholder="Title" 
              />
            </div>
            <div>
              <input 
                className="location e-field e-input" 
                type="text" 
                name="Location" 
                placeholder="Location" 
              />
            </div>
          </form>
        </div>
      ) : (
        <div className="e-event-content e-template">
          <div className="e-subject-wrap">
            {props.Subject && <div className="subject">{props.Subject}</div>}
            {props.Location && <div className="location">{props.Location}</div>}
            {props.Description && <div className="description">{props.Description}</div>}
          </div>
        </div>
      )}
    </div>
  );
};

const footer = (props) => {
  return (
    <div>
      {props.elementType === "cell" ? (
        <div className="e-cell-footer">
          <div className="left-button">
            <button 
              id="more-details" 
              className="e-event-details" 
              title="Extra Details"
              onClick={buttonClickActions}
            >
              Extra Details
            </button>
          </div>
          <div className="right-button">
            <button 
              id="add" 
              className="e-event-create" 
              title="Add"
              onClick={buttonClickActions}
            >
              Add
            </button>
          </div>
        </div>
      ) : (
        <div className="e-event-footer">
          <div className="left-button">
            <button 
              id="edit" 
              className="e-event-edit" 
              title="Edit"
              onClick={buttonClickActions}
            >
              Edit
            </button>
            {!isNullOrUndefined(props.RecurrenceRule) && props.RecurrenceRule !== "" && (
              <button 
                id="edit-series" 
                className="e-edit-series" 
                title="Edit Series"
                onClick={buttonClickActions}
              >
                Edit Series
              </button>
            )}
          </div>
          <div className="right-button">
            <button 
              id="delete" 
              className="e-event-delete" 
              title="Delete"
              onClick={buttonClickActions}
            >
              Delete
            </button>
            {!isNullOrUndefined(props.RecurrenceRule) && props.RecurrenceRule !== "" && (
              <button 
                id="delete-series" 
                className="e-delete-series" 
                title="Delete Series"
                onClick={buttonClickActions}
              >
                Delete Series
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

const buttonClickActions = (e) => {
  const action = e.target.id;
  
  switch (action) {
    case "add":
      const cellDetails = scheduleObj.current.getCellDetails(
        scheduleObj.current.getSelectedElements()
      );
      const eventData = scheduleObj.current.eventWindow.getObjectFromFormData(
        "e-quick-popup-wrapper"
      );
      scheduleObj.current.addEvent({
        Subject: eventData.Subject || "Add title",
        StartTime: cellDetails.startTime,
        EndTime: cellDetails.endTime,
        Location: eventData.Location
      });
      break;
    case "edit":
    case "edit-series":
      const event = scheduleObj.current.activeEventData.event;
      const actionType = event.RecurrenceRule ? 
        (action === "edit" ? "EditOccurrence" : "EditSeries") : "Save";
      scheduleObj.current.openEditor(event, actionType);
      break;
    case "delete":
    case "delete-series":
      const deleteEvent = scheduleObj.current.activeEventData.event;
      const deleteType = deleteEvent.RecurrenceRule ? 
        (action === "delete" ? "DeleteOccurrence" : "DeleteSeries") : "Delete";
      scheduleObj.current.deleteEvent(deleteEvent, deleteType);
      break;
    case "more-details":
      const moreDetails = scheduleObj.current.getCellDetails(
        scheduleObj.current.getSelectedElements()
      );
      scheduleObj.current.openEditor(moreDetails, "Add", true);
      break;
  }
  
  scheduleObj.current.closeQuickInfoPopup();
};

const quickInfoTemplates = { 
  header: header, 
  content: content, 
  footer: footer 
};

<ScheduleComponent 
  ref={scheduleObj}
  quickInfoTemplates={quickInfoTemplates}
>
  {/* ... */}
</ScheduleComponent>
```

**Manually Opening Quick Info Popup**

```tsx
const onCellClickButton = () => {
  const cellData = {
    Subject: 'Review Meeting',
    StartTime: new Date(2023, 2, 5, 9, 0, 0),
    EndTime: new Date(2023, 2, 5, 10, 0, 0)
  };
  scheduleObj.current.openQuickInfoPopup(cellData, 'Add');
};

const onEventClickButton = () => {
  const eventData = {
    Id: 1,
    Subject: 'Review Meeting',
    StartTime: new Date(2023, 2, 5, 9, 0, 0),
    EndTime: new Date(2023, 2, 5, 10, 0, 0)
  };
  scheduleObj.current.openQuickInfoPopup(eventData, 'Save');
};
```

**Manually Closing Quick Info Popup**

```tsx
const onCloseQuickInfo = () => {
  scheduleObj.current.closeQuickInfoPopup();
};
```

## Tooltip Customization

Customize tooltips that appear when hovering over events using the `eventRendered` event:

```tsx
import { Tooltip } from '@syncfusion/ej2-popups';

const onEventRendered = (args) => {
  const tooltip = new Tooltip({
    content: `${args.data.Subject}<br/>Start: ${args.data.StartTime.toLocaleString()}<br/>End: ${args.data.EndTime.toLocaleString()}`,
    target: '.e-appointment',
    position: 'TopCenter'
  });
  tooltip.appendTo(args.element);
};

<ScheduleComponent eventRendered={onEventRendered}>
  {/* ... */}
</ScheduleComponent>
```

**More Events Indicator Popup**

When multiple appointments exceed cell height, a "+more" indicator appears. Customize this behavior:

**Preventing More Indicator Popup**

```tsx
const onPopupOpen = (args) => {
  if (args.type === 'EventContainer') {
    args.cancel = true;
  }
};
```

**Customizing More Indicator Popup**

```tsx
import { Internationalization } from '@syncfusion/ej2-base';

const onPopupOpen = (args) => {
  if (args.type === 'EventContainer') {
    let instance = new Internationalization();
    let date = instance.formatDate(args.data.date, { skeleton: 'MMMEd' });
    args.element.querySelector('.e-header-date').innerText = date;
    args.element.querySelector('.e-header-day').innerText = 
      'Event count: ' + args.data.event.length;
  }
};
```

**Preventing More Indicator Popup Display**

```tsx
const onMoreEventsClick = (args) => {
  args.cancel = true;
};

<ScheduleComponent moreEventsClick={onMoreEventsClick}>
  {/* ... */}
</ScheduleComponent>
```

**Navigating to Day View on More Indicator Click**

```tsx
const onMoreEventsClick = (args) => {
  args.isPopupOpen = false;
};

<ScheduleComponent moreEventsClick={onMoreEventsClick}>
  <ViewsDirective>
    <ViewDirective option='Day' />
    <ViewDirective option='Month' />
  </ViewsDirective>
  <Inject services={[Day, Month]} />
</ScheduleComponent>
```

---
