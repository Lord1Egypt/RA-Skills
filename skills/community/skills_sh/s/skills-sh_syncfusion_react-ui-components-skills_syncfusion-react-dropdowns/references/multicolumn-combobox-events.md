# Events — Syncfusion React MultiColumn ComboBox

## Table of Contents
- [change](#change)
- [select](#select)
- [open](#open)
- [close](#close)
- [filtering](#filtering)
- [actionBegin](#actionbegin)
- [actionComplete](#actioncomplete)
- [actionFailure](#actionfailure)
- [created](#created)

---

## change

Fires when a popup item is selected **or** when the model value is changed by the user. This is the primary event for capturing user selection.

```tsx
import { MultiColumnComboBoxComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-multicolumn-combobox';

function App() {
  const empData = [
    { EmpID: 1001, Name: 'Andrew Fuller', Designation: 'Team Lead', Country: 'England' },
    { EmpID: 1002, Name: 'Robert', Designation: 'Developer', Country: 'USA' },
    { EmpID: 1003, Name: 'Michael', Designation: 'HR', Country: 'Russia' },
  ];
  const fields = { text: 'Name', value: 'EmpID' };

  const onChange = (args: any) => {
    console.log('Value changed:', args.value);
    console.log('Text changed:', args.text);
    console.log('Item data:', args.itemData);
  };

  return (
    <MultiColumnComboBoxComponent
      id="multicolumn"
      dataSource={empData}
      fields={fields}
      text="Michael"
      change={onChange}
    >
      <ColumnsDirective>
        <ColumnDirective field='EmpID' header='Employee ID' width={90} />
        <ColumnDirective field='Name' header='Name' width={90} />
        <ColumnDirective field='Designation' header='Designation' width={90} />
        <ColumnDirective field='Country' header='Country' width={70} />
      </ColumnsDirective>
    </MultiColumnComboBoxComponent>
  );
}
```

---

## select

Fires when a popup item is selected by mouse click, tap, or keyboard navigation. Fires *before* `change`.

```tsx
const onSelect = (args: any) => {
  console.log('Selected item:', args.itemData);
};

<MultiColumnComboBoxComponent
  dataSource={empData}
  fields={fields}
  select={onSelect}
>
  {/* columns */}
</MultiColumnComboBoxComponent>
```

---

## open

Fires when the popup opens.

```tsx
const onOpen = (args: any) => {
  console.log('Popup opened');
};

<MultiColumnComboBoxComponent dataSource={empData} fields={fields} open={onOpen}>
  {/* columns */}
</MultiColumnComboBoxComponent>
```

---

## close

Fires when the popup closes.

```tsx
const onClose = (args: any) => {
  console.log('Popup closed');
};

<MultiColumnComboBoxComponent dataSource={empData} fields={fields} close={onClose}>
  {/* columns */}
</MultiColumnComboBoxComponent>
```

---

## filtering

Fires on every character typed in the component. Use this event for custom filter logic, including server-side filtering.

```tsx
const onFiltering = (args: any) => {
  // args.text: the typed search string
  // For custom filtering, call args.updateData(filteredData) to supply results
  console.log('Filtering with text:', args.text);
};

<MultiColumnComboBoxComponent
  dataSource={empData}
  fields={fields}
  allowFiltering={true}
  filtering={onFiltering}
>
  {/* columns */}
</MultiColumnComboBoxComponent>
```

---

## actionBegin

Fires before fetching data from a remote server. Use to show loading indicators.

```tsx
const onActionBegin = () => {
  console.log('Data fetch started');
};

<MultiColumnComboBoxComponent
  dataSource={remoteDataManager}
  fields={fields}
  actionBegin={onActionBegin}
>
  {/* columns */}
</MultiColumnComboBoxComponent>
```

---

## actionComplete

Fires after data is successfully fetched from a remote server.

```tsx
const onActionComplete = () => {
  console.log('Data fetch completed');
};

<MultiColumnComboBoxComponent
  dataSource={remoteDataManager}
  fields={fields}
  actionComplete={onActionComplete}
>
  {/* columns */}
</MultiColumnComboBoxComponent>
```

---

## actionFailure

Fires when a remote data fetch request fails. Use to display error messages or retry logic.

```tsx
const onActionFailure = () => {
  console.error('Data fetch failed');
};

<MultiColumnComboBoxComponent
  dataSource={remoteDataManager}
  fields={fields}
  actionFailure={onActionFailure}
>
  {/* columns */}
</MultiColumnComboBoxComponent>
```

---

## created

Fires after the component is rendered. Use to perform post-render initialization.

```tsx
const onCreated = () => {
  console.log('Component created and rendered');
};

<MultiColumnComboBoxComponent dataSource={empData} fields={fields} created={onCreated}>
  {/* columns */}
</MultiColumnComboBoxComponent>
```

---

## Event Summary

| Event | When Fired | Argument Type |
|-------|-----------|---------------|
| `change` | Value changes or item selected | `ChangeEventArgs` |
| `select` | Item selected in popup | `SelectEventArgs` |
| `open` | Popup opens | `PopupEventArgs` |
| `close` | Popup closes | `PopupEventArgs` |
| `filtering` | Character typed in input | `FilteringEventArgs` |
| `actionBegin` | Remote fetch starts | `Object` |
| `actionComplete` | Remote fetch succeeds | `Object` |
| `actionFailure` | Remote fetch fails | `Object` |
| `created` | Component rendered | `Event` |
