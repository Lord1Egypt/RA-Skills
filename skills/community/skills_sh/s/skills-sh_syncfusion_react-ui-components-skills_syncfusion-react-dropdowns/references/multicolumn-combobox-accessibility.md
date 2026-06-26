# Accessibility — Syncfusion React MultiColumn ComboBox

## Overview

The MultiColumn ComboBox is built to comply with **WCAG 2.2** and **Section 508** standards by default. Accessibility features include WAI-ARIA attributes, full keyboard navigation, and Right-to-Left (RTL) support.

---

## WCAG Compliance

| Criteria | Conformance Level |
|----------|------------------|
| WCAG 2.2 | A, AA |
| Section 508 | Yes |

---

## WAI-ARIA Attributes

| Attribute | Description |
|-----------|-------------|
| `role="combobox"` | Applied to the input element |
| `aria-expanded` | `true` when popup is open, `false` when closed |
| `aria-selected` | Applied to the active/selected row in the popup |
| `aria-readonly` | Reflects the `readonly` property |
| `aria-disabled` | Reflects the `disabled` property |
| `aria-owns` | Associates the input with the popup listbox element |

These attributes are applied automatically — no manual configuration required.

---

## Keyboard Navigation

| Shortcut | Action |
|----------|--------|
| `Alt` + `Down Arrow` | Open the popup |
| `Alt` + `Up Arrow` | Close the popup |
| `Down Arrow` | Navigate to the next row in the popup |
| `Up Arrow` | Navigate to the previous row in the popup |
| `Page Down` | Scroll down one page in the popup |
| `Page Up` | Scroll up one page in the popup |
| `Enter` | Select the highlighted item |
| `Esc` | Close the popup without selecting |
| `Home` | Navigate to the first item in the popup |
| `End` | Navigate to the last item in the popup |

---

## Right-to-Left (RTL) Support

Set `enableRtl={true}` to flip the component layout for RTL languages (e.g., Arabic, Hebrew).

```tsx
import { MultiColumnComboBoxComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-multicolumn-combobox';

function App() {
  const empData = [
    { EmpID: 1001, Name: 'Andrew Fuller', Designation: 'Team Lead', Country: 'England' },
    { EmpID: 1002, Name: 'Robert', Designation: 'Developer', Country: 'USA' },
    { EmpID: 1003, Name: 'Michael', Designation: 'HR', Country: 'Russia' },
  ];
  const fields = { text: 'Name', value: 'EmpID' };

  return (
    <MultiColumnComboBoxComponent
      id="multicolumn"
      dataSource={empData}
      fields={fields}
      enableRtl={true}
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

## Screen Reader Support

The MultiColumn ComboBox announces:
- The selected item text when an item is chosen
- Popup open/close state via `aria-expanded`
- Item navigation using `aria-selected`

No additional configuration is required for screen reader compatibility.
