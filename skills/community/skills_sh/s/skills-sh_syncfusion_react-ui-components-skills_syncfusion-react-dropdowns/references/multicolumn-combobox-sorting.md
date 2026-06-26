# Sorting — Syncfusion React MultiColumn ComboBox

## Overview

The MultiColumn ComboBox supports column-based sorting via the popup grid header. Clicking a column header toggles ascending → descending → none. Sorting is enabled by default (`allowSorting={true}`).

---

## Enabling and Disabling Sorting

```tsx
// Sorting enabled (default)
<MultiColumnComboBoxComponent dataSource={empData} fields={fields} allowSorting={true}>
  {/* columns */}
</MultiColumnComboBoxComponent>

// Sorting disabled
<MultiColumnComboBoxComponent dataSource={empData} fields={fields} allowSorting={false}>
  {/* columns */}
</MultiColumnComboBoxComponent>
```

---

## Setting Initial Sort Order

Use `sortOrder` to define the initial sort direction when the component first renders.

| Value | Behavior |
|-------|----------|
| `SortOrder.None` | No initial sorting (default) |
| `SortOrder.Ascending` | Data sorted ascending on load |
| `SortOrder.Descending` | Data sorted descending on load |

```tsx
import { MultiColumnComboBoxComponent, ColumnsDirective, ColumnDirective, SortOrder } from '@syncfusion/ej2-react-multicolumn-combobox';

function App() {
  const empData: { [key: string]: Object }[] = [
    { EmpID: 1001, Name: 'Andrew Fuller', Designation: 'Team Lead', Country: 'England' },
    { EmpID: 1002, Name: 'Robert', Designation: 'Developer', Country: 'USA' },
    { EmpID: 1003, Name: 'Michael', Designation: 'HR', Country: 'Russia' },
    { EmpID: 1004, Name: 'Steven Buchanan', Designation: 'Product Manager', Country: 'Ukraine' },
    { EmpID: 1005, Name: 'Margaret Peacock', Designation: 'Developer', Country: 'Egypt' },
  ];
  const fields = { text: 'Name', value: 'EmpID' };

  return (
    <MultiColumnComboBoxComponent
      id="multicolumn"
      dataSource={empData}
      fields={fields}
      allowSorting={true}
      sortOrder={SortOrder.Descending}
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

## Multi-Column Sorting

By default, only one column can be sorted at a time (`sortType="OneColumn"`). To allow sorting by multiple columns simultaneously, set `sortType="MultipleColumns"`. Users can hold **Ctrl** and click multiple column headers.

```tsx
import { MultiColumnComboBoxComponent, ColumnsDirective, ColumnDirective, SortOrder } from '@syncfusion/ej2-react-multicolumn-combobox';

function App() {
  const empData = [ /* ...data... */ ];
  const fields = { text: 'Name', value: 'EmpID' };

  return (
    <MultiColumnComboBoxComponent
      id="multicolumn"
      dataSource={empData}
      fields={fields}
      allowSorting={true}
      sortOrder={SortOrder.Descending}
      sortType="MultipleColumns"
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

## Summary of Sort Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `allowSorting` | `boolean` | `true` | Enable/disable column sorting |
| `sortOrder` | `SortOrder \| string` | `SortOrder.None` | Initial sort direction |
| `sortType` | `SortType \| string` | `'OneColumn'` | One-column or multi-column sorting |
