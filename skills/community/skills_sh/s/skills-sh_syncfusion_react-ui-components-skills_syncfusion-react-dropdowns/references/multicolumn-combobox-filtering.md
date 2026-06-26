# Filtering — Syncfusion React MultiColumn ComboBox

## Overview

The MultiColumn ComboBox includes built-in filtering. When users type in the input, the popup list automatically narrows to matching items. Filtering is enabled by default (`allowFiltering={true}`).

---

## Enabling and Disabling Filtering

Filtering is on by default. Disable it explicitly with `allowFiltering={false}`:

```tsx
// Filtering enabled (default)
<MultiColumnComboBoxComponent dataSource={empData} fields={fields} allowFiltering={true}>
  {/* columns */}
</MultiColumnComboBoxComponent>

// Filtering disabled
<MultiColumnComboBoxComponent dataSource={empData} fields={fields} allowFiltering={false}>
  {/* columns */}
</MultiColumnComboBoxComponent>
```

---

## Changing the Filter Type

Use `filterType` to control how the typed text is matched against item text. The default is `StartsWith`.

| Value | Behavior |
|-------|----------|
| `'StartsWith'` | Items whose text begins with the typed characters |
| `'EndsWith'` | Items whose text ends with the typed characters |
| `'Contains'` | Items whose text contains the typed characters anywhere |

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

  return (
    <MultiColumnComboBoxComponent
      id="multicolumn"
      dataSource={empData}
      fields={fields}
      allowFiltering={true}
      filterType="EndsWith"
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

## Filtering Event

The `filtering` event fires on every character typed in the input. Use it for custom filter logic (e.g., filtering by multiple fields or applying server-side filtering).

```tsx
function App() {
  const empData = [ /* ...data... */ ];
  const fields = { text: 'Name', value: 'EmpID' };

  const onFiltering = (args: any) => {
    // args.text contains the typed value
    // args.updateData() can be used to supply custom filtered results
    console.log('Filter text:', args.text);
  };

  return (
    <MultiColumnComboBoxComponent
      id="multicolumn"
      dataSource={empData}
      fields={fields}
      allowFiltering={true}
      filtering={onFiltering}
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

## Notes

- Filtering applies to the `fields.text` column by default.
- When no items match the filter, the popup shows the `noRecordsTemplate` content.
- For remote data filtering, handle the `filtering` event manually and call `args.updateData()` with filtered results from the server.
