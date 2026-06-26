# Grouping — Syncfusion React MultiColumn ComboBox

## Overview

The MultiColumn ComboBox supports grouping popup items by a shared category field. Group headers are fixed and update dynamically as you scroll through the list. Configure grouping through the `fields.groupBy` property.

---

## Enabling Grouping

Set `fields.groupBy` to the data property that defines the group category:

```tsx
import { MultiColumnComboBoxComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-multicolumn-combobox';

function App() {
  const empData: { [key: string]: Object }[] = [
    { EmpID: 1001, Name: 'Andrew Fuller', Designation: 'Team Lead', Country: 'England' },
    { EmpID: 1002, Name: 'Robert', Designation: 'Developer', Country: 'USA' },
    { EmpID: 1003, Name: 'Michael', Designation: 'HR', Country: 'Russia' },
    { EmpID: 1004, Name: 'Steven Buchanan', Designation: 'Product Manager', Country: 'Ukraine' },
    { EmpID: 1005, Name: 'Margaret Peacock', Designation: 'Developer', Country: 'Egypt' },
    { EmpID: 1006, Name: 'Janet Leverling', Designation: 'Team Lead', Country: 'Africa' },
  ];
  // Group items by Country
  const fields = { text: 'Name', value: 'EmpID', groupBy: 'Country' };
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

## Custom Group Template

Use `groupTemplate` on the component to customize how each group header displays. The template string can reference `${key}` (group value), `${field}` (group field name), and `${count}` (number of items in group).

```tsx
import { MultiColumnComboBoxComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-multicolumn-combobox';

function App() {
  const data: { [key: string]: Object }[] = [
    { OrderID: 10248, CustomerID: 'VINET', OrderDate: new Date(8364186e5), Freight: 32.38 },
    { OrderID: 10249, CustomerID: 'TOMSP', OrderDate: new Date(836505e6), Freight: 11.61 },
    { OrderID: 10250, CustomerID: 'HANAR', OrderDate: new Date(8367642e5), Freight: 65.83 },
    { OrderID: 10253, CustomerID: 'HANAR', OrderDate: new Date(836937e6), Freight: 58.17 },
  ];
  const fields = { text: 'CustomerID', value: 'OrderID', groupBy: 'CustomerID' };
  const groupTemplate = (data: any) => {
    return (
      <div className="e-group-temp">
        Key is: {data.key}, Field is: {data.field}, Count is: {data.count}
      </div>
    );
  };

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

## Key Points

- Group headers are fixed — they remain visible as users scroll through a group's items.
- Group headers update dynamically based on scroll position.
- Combine `groupBy` with `groupTemplate` for a fully branded group header appearance.
- Sorting and grouping can coexist — items will be sorted within groups.
