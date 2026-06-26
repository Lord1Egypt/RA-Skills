# Localization — Syncfusion React MultiColumn ComboBox

## Overview

Localization lets you translate the component's built-in text strings (e.g., "No records found") into any language using the `L10n` class from `@syncfusion/ej2-base`.

---

## Setup

### 1. Import `L10n`

```tsx
import { L10n } from '@syncfusion/ej2-base';
```

### 2. Register Locale Strings

The MultiColumn ComboBox uses the locale key `'multicolumncombobox'`. The only built-in translatable string is `noRecordsTemplate`.

```tsx
L10n.load({
  'fr-BE': {
    'multicolumncombobox': {
      'noRecordsTemplate': 'Aucun enregistrement trouvé',
    },
  },
});
```

### 3. Set the `locale` Property

```tsx
<MultiColumnComboBoxComponent locale="fr-BE" ... />
```

---

## Full Example (French)

```tsx
import { L10n } from '@syncfusion/ej2-base';
import { MultiColumnComboBoxComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-multicolumn-combobox';

L10n.load({
  'fr-BE': {
    'multicolumncombobox': {
      'noRecordsTemplate': 'Aucun enregistrement trouvé',
    },
  },
});

function App() {
  const empData = [
    { EmpID: 1001, Name: 'Andrew Fuller', Designation: 'Team Lead', Country: 'England' },
    { EmpID: 1002, Name: 'Robert', Designation: 'Developer', Country: 'USA' },
  ];
  const fields = { text: 'Name', value: 'EmpID' };

  return (
    <MultiColumnComboBoxComponent
      id="multicolumn"
      dataSource={empData}
      fields={fields}
      locale="fr-BE"
      allowFiltering={true}
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

When the user types a value that yields no matches, the popup will display "Aucun enregistrement trouvé" instead of the default "No records found".

---

## Locale Keys Reference

| Locale Key | Default Value |
|------------|--------------|
| `noRecordsTemplate` | `'No records found'` |

---

## Notes

- `L10n.load()` must be called **before** the component renders, typically at the top of the file or in the app entry point.
- The `locale` property accepts any valid BCP 47 language tag (e.g., `'en-US'`, `'fr-BE'`, `'de'`).
- For additional text customization beyond the locale key (such as custom styling in the no-records message), use the `noRecordsTemplate` prop directly — it accepts JSX:

```tsx
<MultiColumnComboBoxComponent
  noRecordsTemplate={<span>Aucun résultat pour cette recherche</span>}
  ...
/>
```
