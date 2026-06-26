# Columns — Syncfusion React MultiColumn ComboBox

## Table of Contents
- [Overview](#overview)
- [Core Column Properties](#core-column-properties)
- [Text Alignment](#text-alignment)
- [Cell Templates](#cell-templates)
- [Header Templates](#header-templates)
- [Display as Checkbox](#display-as-checkbox)
- [Custom Attributes](#custom-attributes)
- [Format](#format)

---

## Overview

Columns define what data fields appear in the popup grid. Use `ColumnsDirective` as a wrapper and `ColumnDirective` for each column. The `ColumnModel` interface governs all column configuration options.

---

## Core Column Properties

Every column requires `field`. Use `header` and `width` to label and size the column.

```tsx
import { MultiColumnComboBoxComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-multicolumn-combobox';

function App() {
  const empData = [
    { EmpID: 1001, Name: 'Andrew Fuller', Designation: 'Team Lead', Country: 'England' },
    { EmpID: 1002, Name: 'Robert', Designation: 'Developer', Country: 'USA' },
    { EmpID: 1003, Name: 'Michael', Designation: 'HR', Country: 'Russia' },
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

| Property | Type | Description |
|----------|------|-------------|
| `field` | `string` | Data source field to display in this column. **Required.** |
| `header` | `string` | Text shown in the column header. |
| `width` | `number` | Column width in pixels. |

---

## Text Alignment

Use `textAlign` to control the horizontal alignment of column content.

Accepted values: `'Left'` | `'Right'` | `'Center'` | `'Justify'`

```tsx
<ColumnsDirective>
  <ColumnDirective field='EmpID' header='Employee ID' width={90} />
  <ColumnDirective field='Name' header='Name' width={90} textAlign={'Right'} />
  <ColumnDirective field='Designation' header='Designation' width={90} />
  <ColumnDirective field='Country' header='Country' width={70} />
</ColumnsDirective>
```

---

## Cell Templates

Use `template` to fully customize what renders inside each cell. The template string uses `${FieldName}` syntax to interpolate data values.

```tsx
const data = [
  { Name: 'Andrew Fuller', Eimg: 7, Designation: 'Team Lead', Country: 'England', DateofJoining: '12/10/2010' },
  { Name: 'Anne Dodsworth', Eimg: 1, Designation: 'Developer', Country: 'USA', DateofJoining: '10/05/2000' },
];
const fields = { text: 'Name', value: 'Eimg' };

return (
  <MultiColumnComboBoxComponent
    id="multicolumn"
    dataSource={data}
    fields={fields}
    placeholder="Select an employee"
    gridSettings={{ rowHeight: 40 }}
  >
    <ColumnsDirective>
      <ColumnDirective
        field='Eimg'
        header='Photos'
        width={90}
        template='<div><img class="empImage" src="https://ej2.syncfusion.com/demos/src/multicolumn-combobox/Employees/${Eimg}.png" alt="employee"/></div>'
      />
      <ColumnDirective
        field='Name'
        header='Employee Name'
        width={160}
        template='<div class="ename"> ${Name} </div><div class="job"> ${Designation} </div>'
      />
      <ColumnDirective
        field='DateofJoining'
        header='Date of Joining'
        width={165}
        template='<div class="dateOfJoining"> ${DateofJoining} </div>'
      />
      <ColumnDirective field='Country' header='Country' width={100} />
    </ColumnsDirective>
  </MultiColumnComboBoxComponent>
);
```

> When using `template`, set `gridSettings={{ rowHeight: 40 }}` if the template content is taller than the default row height.

---

## Header Templates

Use `headerTemplate` on a `ColumnDirective` to replace the default header text with custom HTML.

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

## Display as Checkbox

Use `displayAsCheckBox={true}` to render a boolean field as a checkbox instead of showing `true`/`false` text.

```tsx
<ColumnsDirective>
  <ColumnDirective field='EmpID' header='Employee ID' width={90} displayAsCheckBox={true} />
  <ColumnDirective field='Name' header='Name' width={90} />
  <ColumnDirective field='Designation' header='Designation' width={90} />
  <ColumnDirective field='Country' header='Country' width={70} />
</ColumnsDirective>
```

> Default value is `false`. Enable this when the column field contains boolean values.

---

## Custom Attributes

Use `customAttributes` to add custom CSS classes or inline styles to all cells in a column.

```tsx
<ColumnsDirective>
  <ColumnDirective field='EmpID' header='Employee ID' width={90} />
  <ColumnDirective
    field='Name'
    header='Name'
    width={90}
    customAttributes={{ class: 'e-custom-multicolumn' }}
  />
  <ColumnDirective field='Designation' header='Designation' width={90} />
  <ColumnDirective field='Country' header='Country' width={70} />
</ColumnsDirective>
```

The object is applied as HTML attributes on each cell element in the column.

---

## Format

Use the `format` property to apply formatting to column data (e.g., numbers, dates).

```tsx
// Number format example
<ColumnDirective field='Freight' header='Freight' width={120} format='C2' />

// Date format example
<ColumnDirective field='OrderDate' header='Order Date' width={140} format={{ type: 'date', skeleton: 'medium' }} />
```

Format strings follow the Internalization library conventions used across Syncfusion EJ2 components.
