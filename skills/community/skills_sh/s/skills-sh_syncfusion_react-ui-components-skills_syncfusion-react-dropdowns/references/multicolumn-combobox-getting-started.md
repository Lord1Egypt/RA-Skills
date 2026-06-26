# Getting Started — Syncfusion React MultiColumn ComboBox

## Table of Contents
- [Installation](#installation)
- [CSS Imports](#css-imports)
- [Basic Component Setup](#basic-component-setup)
- [Binding Data with Fields and Columns](#binding-data-with-fields-and-columns)
- [Configuring Popup Size](#configuring-popup-size)
- [Functional vs Class Components](#functional-vs-class-components)
- [Troubleshooting](#troubleshooting)

---

## Installation

Create a new React app and install the MultiColumn ComboBox package:

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install @syncfusion/ej2-react-multicolumn-combobox --save
npm run dev
```

For JavaScript (non-TypeScript):
```bash
npm create vite@latest my-app -- --template react
```

---

## CSS Imports

Add the following CSS imports to `src/App.css`:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-grids/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-multicolumn-combobox/styles/tailwind3.css";
```

Then import the CSS file in `src/App.tsx`:
```tsx
import './App.css';
```

> Other themes available: `bootstrap5.css`, `material3.css`, `fluent2.css`, `fabric.css`. Replace `tailwind3` with the desired theme name across all imports.

---

## Basic Component Setup

The minimum required setup: `dataSource`, `fields`, and at least one `ColumnDirective`.

**Functional Component:**

```tsx
import { MultiColumnComboBoxComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-multicolumn-combobox';
import * as React from 'react';
import './App.css';

function App() {
  const empData = [
    { EmpID: 1001, Name: 'Andrew Fuller', Designation: 'Team Lead', Country: 'England' },
    { EmpID: 1002, Name: 'Robert', Designation: 'Developer', Country: 'USA' },
    { EmpID: 1003, Name: 'Michael', Designation: 'HR', Country: 'Russia' },
  ];
  const fields = { text: 'Name', value: 'EmpID' };

  return (
    <MultiColumnComboBoxComponent id="multicolumn" dataSource={empData} fields={fields} placeholder="Select an employee">
      <ColumnsDirective>
        <ColumnDirective field='EmpID' header='Employee ID' width={120} />
        <ColumnDirective field='Name' header='Name' width={120} />
        <ColumnDirective field='Designation' header='Designation' width={120} />
        <ColumnDirective field='Country' header='Country' width={100} />
      </ColumnsDirective>
    </MultiColumnComboBoxComponent>
  );
}
export default App;
```

**Class Component:**

```tsx
import { MultiColumnComboBoxComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-multicolumn-combobox';
import * as React from 'react';
import './App.css';

export default class App extends React.Component<{}, {}> {
  private empData: object[] = [
    { EmpID: 1001, Name: 'Andrew Fuller', Designation: 'Team Lead', Country: 'England' },
    { EmpID: 1002, Name: 'Robert', Designation: 'Developer', Country: 'USA' },
    { EmpID: 1003, Name: 'Michael', Designation: 'HR', Country: 'Russia' },
  ];
  private fields: object = { text: 'Name', value: 'EmpID' };

  public render() {
    return (
      <MultiColumnComboBoxComponent id="multicolumn" dataSource={this.empData} fields={this.fields} placeholder="Select an employee">
        <ColumnsDirective>
          <ColumnDirective field='EmpID' header='Employee ID' width={120} />
          <ColumnDirective field='Name' header='Name' width={120} />
          <ColumnDirective field='Designation' header='Designation' width={120} />
          <ColumnDirective field='Country' header='Country' width={100} />
        </ColumnsDirective>
      </MultiColumnComboBoxComponent>
    );
  }
}
```

---

## Binding Data with Fields and Columns

The `fields` property maps your data's text/value keys. The `ColumnsDirective` and `ColumnDirective` define what columns appear in the popup.

```tsx
// fields: maps which data property shows as display text and which is the hidden value
const fields = { text: 'Name', value: 'EmpID' };

// columns: each ColumnDirective renders one column in the popup grid
<ColumnsDirective>
  <ColumnDirective field='EmpID' header='Employee ID' width={120} />
  <ColumnDirective field='Name' header='Name' width={120} />
  <ColumnDirective field='Designation' header='Designation' width={120} />
</ColumnsDirective>
```

- `fields.text` — the field shown in the input box after selection
- `fields.value` — the hidden value bound to the component
- `ColumnDirective field` — must match a key in your data objects

---

## Configuring Popup Size

The popup defaults to `300px` height and matches the component width. Customize with `popupHeight` and `popupWidth`:

```tsx
<MultiColumnComboBoxComponent
  dataSource={empData}
  fields={fields}
  popupHeight={250}
  popupWidth={500}
  placeholder="Select an employee"
>
  <ColumnsDirective>
    <ColumnDirective field='EmpID' header='Employee ID' width={90} />
    <ColumnDirective field='Name' header='Name' width={90} />
    <ColumnDirective field='Designation' header='Designation' width={90} />
    <ColumnDirective field='Country' header='Country' width={70} />
  </ColumnsDirective>
</MultiColumnComboBoxComponent>
```

Both properties accept `string` (e.g., `'250px'`) or `number` (e.g., `250`).

---

## Functional vs Class Components

Both patterns are supported. Functional components with hooks are generally preferred in modern React.

- **Functional:** Use `const` for data, fields, and event handlers.
- **Class:** Use `private` properties and `this.` references in render.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Popup list renders unstyled | Verify all 5 CSS imports are present in `App.css` |
| Selected text not showing | Check `fields.text` maps to the correct property key in your data |
| No data displays in popup | Confirm `dataSource` is not empty and column `field` values match data keys |
| Component not found error | Run `npm install @syncfusion/ej2-react-multicolumn-combobox --save` |
| TypeScript type errors | Use `{ [key: string]: Object }[]` for typed data arrays |
