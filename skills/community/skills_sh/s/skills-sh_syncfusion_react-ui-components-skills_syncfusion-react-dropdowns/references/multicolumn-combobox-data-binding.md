# Data Binding — Syncfusion React MultiColumn ComboBox

## Table of Contents
- [Overview](#overview)
- [Fields Mapping](#fields-mapping)
- [Binding Local Data](#binding-local-data)
- [Binding Remote Data](#binding-remote-data)
- [Using Query](#using-query)
- [Supported Data Services](#supported-data-services)

---

## Overview

The MultiColumn ComboBox accepts data through the `dataSource` property. It supports:
- Plain JavaScript object arrays (local data)
- `DataManager` instances (remote or advanced local queries)

The `fields` property maps which data object keys serve as the display text, hidden value, and optional group-by field.

---

## Fields Mapping

```tsx
// Fields map data properties to component roles
const fields = {
  text: 'Name',       // shown in the input box after selection
  value: 'EmpID',     // hidden value stored/returned by the component
  groupBy: 'Country'  // optional: groups items in the popup by this field
};
```

| Field | Type | Description |
|-------|------|-------------|
| `text` | `string` | Property to display as item text in the input |
| `value` | `string` | Property used as the underlying value |
| `groupBy` | `string` | Property used to group list items |

> Map `fields` correctly — an incorrect mapping causes the selected item to appear `undefined`.

---

## Binding Local Data

Pass a plain array of objects to `dataSource`. Each object's keys must include what `fields.text`, `fields.value`, and each `ColumnDirective field` reference.

```tsx
import { MultiColumnComboBoxComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-multicolumn-combobox';

function App() {
  const empData: { [key: string]: Object }[] = [
    { EmpID: 1001, Name: 'Andrew Fuller', Designation: 'Team Lead', Country: 'England' },
    { EmpID: 1002, Name: 'Robert', Designation: 'Developer', Country: 'USA' },
    { EmpID: 1003, Name: 'Michael', Designation: 'HR', Country: 'Russia' },
    { EmpID: 1004, Name: 'Steven Buchanan', Designation: 'Product Manager', Country: 'Ukraine' },
    { EmpID: 1005, Name: 'Margaret Peacock', Designation: 'Developer', Country: 'Egypt' },
  ];
  const fields = { text: 'Name', value: 'EmpID' };
  const text = 'Michael';

  return (
    <MultiColumnComboBoxComponent id="multicolumn" dataSource={empData} fields={fields} text={text}>
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

## Binding Remote Data

Use `DataManager` with an adaptor to fetch data from a REST API. The component will load and display data from the remote service.

```tsx
import { MultiColumnComboBoxComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-multicolumn-combobox';
import { DataManager, WebApiAdaptor } from '@syncfusion/ej2-data';

function App() {
  const dataSource = new DataManager({
    url: 'url',
    adaptor: new WebApiAdaptor(),
    crossDomain: true
  });
  const fields = { text: 'FirstName', value: 'EmployeeID' };

  return (
    <MultiColumnComboBoxComponent
      id="multicolumn"
      dataSource={dataSource}
      fields={fields}
      placeholder="Select a name"
      popupHeight="230px"
    >
      <ColumnsDirective>
        <ColumnDirective field='EmployeeID' header='Employee ID' width={120} />
        <ColumnDirective field='FirstName' header='Name' width={130} />
        <ColumnDirective field='Designation' header='Designation' width={120} />
        <ColumnDirective field='Country' header='Country' width={90} />
      </ColumnsDirective>
    </MultiColumnComboBoxComponent>
  );
}
```

---

## Using Query

Use the `query` property to apply constraints on the data before it is rendered. This works with both local and remote data sources.

```tsx
import { MultiColumnComboBoxComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-multicolumn-combobox';
import { Query } from '@syncfusion/ej2-data';

function App() {
  const empData = [ /* ...data... */ ];
  const fields = { text: 'Name', value: 'EmpID' };
  // Only select specific fields and limit to 7 records
  const query = new Query().select(['Name', 'EmpID', 'Designation', 'Country']).take(7);

  return (
    <MultiColumnComboBoxComponent id="multicolumn" dataSource={empData} fields={fields} query={query}>
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

## Supported Data Services

The `DataManager` supports multiple adaptors for different backends:

| Adaptor | Use Case |
|---------|----------|
| `WebApiAdaptor` | ASP.NET Web API / REST services |
| `ODataAdaptor` | OData v3 services |
| `ODataV4Adaptor` | OData v4 services |
| `JsonAdaptor` | Local JSON array with DataManager features |

```tsx
import { DataManager, ODataV4Adaptor } from '@syncfusion/ej2-data';

const dataSource = new DataManager({
  url: 'url',
  adaptor: new ODataV4Adaptor(),
  crossDomain: true
});
```

> For large remote datasets, combine `DataManager` with `enableVirtualization={true}` for efficient rendering.
