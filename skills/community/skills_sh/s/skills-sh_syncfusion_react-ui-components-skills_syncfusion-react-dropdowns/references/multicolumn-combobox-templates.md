# Templates — Syncfusion React MultiColumn ComboBox

## Table of Contents
- [Item Template](#item-template)
- [Header Template](#header-template)
- [Group Template](#group-template)
- [Footer Template](#footer-template)
- [No Records Template](#no-records-template)
- [Action Failure Template](#action-failure-template)

---

## Item Template

`itemTemplate` customizes each row in the popup list. Use `${FieldName}` syntax to interpolate data values. The template must be a **string** — not a JSX function.

```tsx
import { MultiColumnComboBoxComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-multicolumn-combobox';

function App() {
  const empData = [
    { EmpID: 1001, Name: 'Andrew Fuller', Designation: 'Team Lead', Country: 'England' },
    { EmpID: 1002, Name: 'Robert', Designation: 'Developer', Country: 'USA' },
    { EmpID: 1003, Name: 'Michael', Designation: 'HR', Country: 'Russia' },
    { EmpID: 1004, Name: 'Steven Buchanan', Designation: 'Product Manager', Country: 'Ukraine' },
    { EmpID: 1005, Name: 'Margaret Peacock', Designation: 'Developer', Country: 'Egypt' },
  ];
  const fields = { text: 'Name', value: 'EmpID' };
  // itemTemplate must be a string using ${FieldName} interpolation syntax
  const itemTemplate = "<tr><td class='emp-id'>${EmpID}</td><td class='name'>${Name}</td><td class='city'>${Designation}</td></tr>";

  return (
    <MultiColumnComboBoxComponent
      id="multicolumn"
      dataSource={empData}
      fields={fields}
      itemTemplate={itemTemplate}
    >
      <ColumnsDirective>
        <ColumnDirective field='EmpID' header='Employee ID' width={120} />
        <ColumnDirective field='Name' header='Name' width={100} />
        <ColumnDirective field='Designation' header='Designation' width={120} />
      </ColumnsDirective>
    </MultiColumnComboBoxComponent>
  );
}
```

---

## Header Template

`headerTemplate` is a property on `ColumnDirective` that replaces the default column header text with custom HTML.

```tsx
<ColumnsDirective>
  <ColumnDirective
    field='EmpID'
    headerTemplate='<div class="header"><span>Employee ID</span></div>'
    width={90}
  />
  <ColumnDirective
    field='Name'
    headerTemplate='<div class="header"><span>Employee Name</span></div>'
    width={160}
  />
  <ColumnDirective
    field='Designation'
    headerTemplate='<div class="header"><span>Designation</span></div>'
    width={90}
  />
  <ColumnDirective
    field='Country'
    headerTemplate='<div class="header"><span>Country</span></div>'
    width={80}
  />
</ColumnsDirective>
```

---

## Group Template

`groupTemplate` is a component-level property that customizes the group header rows when `fields.groupBy` is set. The template must be a **string** using `${key}`, `${field}`, and `${count}` tokens.

Available template tokens: `${key}` (group value), `${field}` (field name), `${count}` (item count in group).

```tsx
import { MultiColumnComboBoxComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-multicolumn-combobox';

function App() {
  const data = [
    { OrderID: 10248, CustomerID: 'VINET', OrderDate: new Date(8364186e5), Freight: 32.38 },
    { OrderID: 10249, CustomerID: 'TOMSP', OrderDate: new Date(836505e6), Freight: 11.61 },
    { OrderID: 10250, CustomerID: 'HANAR', OrderDate: new Date(8367642e5), Freight: 65.83 },
    { OrderID: 10251, CustomerID: 'VICTE', OrderDate: new Date(8367642e5), Freight: 41.34 },
    { OrderID: 10252, CustomerID: 'SUPRD', OrderDate: new Date(8368506e5), Freight: 51.3 },
    { OrderID: 10253, CustomerID: 'HANAR', OrderDate: new Date(836937e6), Freight: 58.17 },
  ];
  const fields = { text: 'CustomerID', value: 'OrderID', groupBy: 'CustomerID' };
  // groupTemplate must be a string using ${key}, ${field}, ${count} tokens
  const groupTemplate = '<div class="e-group-temp">Key is: ${key}, Field is: ${field}, Count is: ${count}</div>';

  return (
    <MultiColumnComboBoxComponent
      id="multicolumn"
      dataSource={data}
      fields={fields}
      groupTemplate={groupTemplate}
    >
      <ColumnsDirective>
        <ColumnDirective field='OrderID' header='Order ID' width={120} />
        <ColumnDirective field='CustomerID' header='Customer ID' width={140} />
        <ColumnDirective field='Freight' header='Freight' width={120} />
        <ColumnDirective field='OrderDate' header='Order Date' width={140} />
      </ColumnsDirective>
    </MultiColumnComboBoxComponent>
  );
}
```

---

## Footer Template

`footerTemplate` adds a custom element at the bottom of the popup list. The template must be a **string**.

```tsx
import { MultiColumnComboBoxComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-multicolumn-combobox';

function App() {
  const empData = [
    { EmpID: 1001, Name: 'Andrew Fuller', Designation: 'Team Lead', Country: 'England' },
    { EmpID: 1002, Name: 'Robert', Designation: 'Developer', Country: 'USA' },
    { EmpID: 1003, Name: 'Michael', Designation: 'HR', Country: 'Russia' },
    { EmpID: 1004, Name: 'Steven Buchanan', Designation: 'Product Manager', Country: 'Ukraine' },
    { EmpID: 1005, Name: 'Margaret Peacock', Designation: 'Developer', Country: 'Egypt' },
  ];
  const fields = { text: 'Name', value: 'EmpID' };
  // footerTemplate must be a string
  const footerTemplate = "<span class='foot' style='font-weight: bolder; margin: 0 10px'>Total list of employees: " + empData.length + "</span>";

  return (
    <MultiColumnComboBoxComponent
      id="multicolumn"
      dataSource={empData}
      fields={fields}
      footerTemplate={footerTemplate}
      placeholder="Select an employee"
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

## No Records Template

`noRecordsTemplate` customizes the content shown when no items match the filter or the data source is empty. The template must be a **string**.

```tsx
import { MultiColumnComboBoxComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-multicolumn-combobox';

function App() {
  const fields = { text: 'Name', value: 'EmpID' };
  // noRecordsTemplate must be a string
  const noRecordsTemplate = "<span class='norecord'> NO RECORDS FOUND </span>";

  return (
    <MultiColumnComboBoxComponent
      id="multicolumn"
      dataSource={[]}
      fields={fields}
      noRecordsTemplate={noRecordsTemplate}
      placeholder="Select an employee"
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

Default text is `'No records found'`.

---

## Action Failure Template

`actionFailureTemplate` customizes the popup content when a remote data fetch request fails. The template must be a **string**.

```tsx
import { MultiColumnComboBoxComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-multicolumn-combobox';
import { DataManager, WebApiAdaptor } from '@syncfusion/ej2-data';

function App() {
  const dataSource = new DataManager({
    url: 'url',
    adaptor: new WebApiAdaptor(),
    crossDomain: true
  });
  const fields = { text: 'Name', value: 'EmpID' };
  // actionFailureTemplate must be a string
  const actionFailureTemplate = "<span class='action-failure'> Data fetch get fails</span>";

  return (
    <MultiColumnComboBoxComponent
      id="multicolumn"
      dataSource={dataSource}
      fields={fields}
      popupHeight="230px"
      actionFailureTemplate={actionFailureTemplate}
      placeholder="Select a country"
    >
      <ColumnsDirective>
        <ColumnDirective field='OrderID' header='Order ID' width={120} />
        <ColumnDirective field='CustomerID' header='Customer ID' width={130} />
        <ColumnDirective field='ShipCountry' header='Ship Country' width={120} />
      </ColumnsDirective>
    </MultiColumnComboBoxComponent>
  );
}
```

Default text is `'Request Failed'`.

---

## Template Reference Summary

| Template Property | Scope | Default |
|-------------------|-------|---------|
| `itemTemplate` | Component | null |
| `headerTemplate` | `ColumnDirective` | null |
| `groupTemplate` | Component | null |
| `footerTemplate` | Component | null |
| `noRecordsTemplate` | Component | `'No records found'` |
| `actionFailureTemplate` | Component | `'Request Failed'` |
