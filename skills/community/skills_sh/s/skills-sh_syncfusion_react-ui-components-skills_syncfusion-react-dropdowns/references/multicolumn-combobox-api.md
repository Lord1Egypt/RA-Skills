# API Reference — Syncfusion React MultiColumn ComboBox

Source: https://ej2.syncfusion.com/react/documentation/api/multicolumn-combobox/index-default

---

## Table of Contents
- [Import](#import)
- [Properties](#properties)
- [Methods](#methods)
- [Events](#events)
- [ColumnModel](#columnmodel)
- [GridSettingsModel](#gridsettingsmodel)
- [FieldSettingsModel](#fieldsettingsmodel)

---

## Import

```tsx
import {
  MultiColumnComboBoxComponent,
  ColumnsDirective,
  ColumnDirective,
  SortOrder,
  SortType,
  FilterType,
} from '@syncfusion/ej2-react-multicolumn-combobox';
```

---

## Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `actionFailureTemplate` | `string \| function \| JSX.Element` | `'Request Failed'` | Template shown when a remote request fails |
| `allowFiltering` | `boolean` | `true` | Enables the filter input box in the popup header |
| `allowSorting` | `boolean` | `true` | Enables sorting by clicking column headers |
| `columns` | `ColumnModel[]` | `[]` | Column definitions (use `ColumnsDirective`/`ColumnDirective` in JSX) |
| `cssClass` | `string` | `''` | Custom CSS class added to the root element |
| `dataSource` | `Object[] \| DataManager \| DataResult` | `[]` | Data source for the popup list |
| `disabled` | `boolean` | `false` | Disables the component |
| `enablePersistence` | `boolean` | `false` | Persists component state across page reloads |
| `enableRtl` | `boolean` | `false` | Enables right-to-left layout |
| `enableVirtualization` | `boolean` | `false` | Enables virtual scrolling for large datasets |
| `fields` | `FieldSettingsModel` | `{text:null, value:null, groupBy:null}` | Maps data source fields to component roles |
| `filterType` | `FilterType \| string` | `FilterType.StartsWith` | Filter comparison type (`StartsWith`, `EndsWith`, `Contains`) |
| `floatLabelType` | `FloatLabelType` | `Never` | Floating label behavior (`Never`, `Auto`, `Always`) |
| `footerTemplate` | `string \| function \| JSX.Element` | `null` | Custom template for the popup footer |
| `gridSettings` | `GridSettingsModel` | `{rowHeight:null, gridLines:'Default', enableAltRow:false}` | Grid appearance settings for the popup |
| `groupTemplate` | `string \| function \| JSX.Element` | `null` | Custom template for group headers |
| `htmlAttributes` | `{ [key: string]: string }` | `{}` | Additional HTML attributes applied to the input element |
| `index` | `number \| null` | `null` | Pre-selects an item by zero-based index |
| `itemTemplate` | `string \| function \| JSX.Element` | `null` | Custom template for each popup row |
| `locale` | `string` | `''` | Locale code for localization (e.g., `'fr-BE'`) |
| `noRecordsTemplate` | `string \| function \| JSX.Element` | `'No records found'` | Template shown when no data matches |
| `placeholder` | `string` | `null` | Placeholder text for the input |
| `popupHeight` | `string \| number` | `'300px'` | Height of the popup |
| `popupWidth` | `string \| number` | `'100%'` | Width of the popup |
| `query` | `Query` | `null` | Query object for filtering remote data |
| `readonly` | `boolean` | `false` | Makes the input read-only |
| `showClearButton` | `boolean` | `false` | Shows a clear (×) button when a value is selected |
| `sortOrder` | `SortOrder \| string` | `SortOrder.None` | Initial sort order (`None`, `Ascending`, `Descending`) |
| `sortType` | `SortType \| string` | `SortType.OneColumn` | How many columns can be sorted (`OneColumn`, `MultipleColumns`) |
| `text` | `string` | `null` | Pre-selects an item by its text value |
| `value` | `string` | `null` | Pre-selects an item by its value |
| `width` | `string \| number` | `'100%'` | Width of the component input element |

---

## Methods

Call these via a component ref: `const ref = useRef<MultiColumnComboBoxComponent>(null);`

| Method | Signature | Description |
|--------|-----------|-------------|
| `addItems` | `(items: Object \| Object[], index?: number): void` | Adds new item(s) to the data source at the specified index |
| `focusIn` | `(e?: FocusEvent \| MouseEvent \| KeyboardEvent \| TouchEvent): void` | Focuses the component input |
| `focusOut` | `(e?: MouseEvent \| KeyboardEventArgs): void` | Removes focus from the component |
| `getDataByValue` | `(value: string): {[key:string]:Object}` | Returns the data object matching the given value |
| `getItems` | `(): Element[]` | Returns all rendered popup item DOM elements |
| `hidePopup` | `(e?: MouseEvent \| KeyboardEventArgs \| TouchEvent): void` | Closes the popup programmatically |
| `showPopup` | `(e?: MouseEvent \| KeyboardEventArgs \| TouchEvent, isInputOpen?: boolean): void` | Opens the popup programmatically |

### Method Usage Example

```tsx
import { useRef } from 'react';
import { MultiColumnComboBoxComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-multicolumn-combobox';

function App() {
  const comboRef = useRef<MultiColumnComboBoxComponent>(null);
  const empData = [
    { EmpID: 1001, Name: 'Andrew Fuller', Designation: 'Team Lead', Country: 'England' },
    { EmpID: 1002, Name: 'Robert', Designation: 'Developer', Country: 'USA' },
  ];
  const fields = { text: 'Name', value: 'EmpID' };

  return (
    <>
      <MultiColumnComboBoxComponent
        id="multicolumn"
        ref={comboRef}
        dataSource={empData}
        fields={fields}
      >
        <ColumnsDirective>
          <ColumnDirective field='EmpID' header='Employee ID' width={90} />
          <ColumnDirective field='Name' header='Name' width={90} />
        </ColumnsDirective>
      </MultiColumnComboBoxComponent>
      <button onClick={() => comboRef.current?.showPopup()}>Open Popup</button>
      <button onClick={() => comboRef.current?.hidePopup()}>Close Popup</button>
      <button onClick={() => console.log(comboRef.current?.getDataByValue('1001'))}>Get Data</button>
    </>
  );
}
```

---

## Events

| Event Prop | Argument Type | Description |
|-----------|--------------|-------------|
| `actionBegin` | `EmitType<Object>` | Fires before remote data fetch begins |
| `actionComplete` | `EmitType<Object>` | Fires after remote data fetch completes |
| `actionFailure` | `EmitType<Object>` | Fires when remote data fetch fails |
| `change` | `EmitType<ChangeEventArgs>` | Fires when the selected value changes |
| `close` | `EmitType<PopupEventArgs>` | Fires when the popup closes |
| `created` | `EmitType<Event>` | Fires after the component is first rendered |
| `filtering` | `EmitType<FilteringEventArgs>` | Fires on each filter input keystroke |
| `open` | `EmitType<PopupEventArgs>` | Fires when the popup opens |
| `select` | `EmitType<SelectEventArgs>` | Fires when a popup item is selected |

---

## ColumnModel

Defines the structure of each column in the popup. Used via `ColumnDirective`.

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `field` | `string` | — | Data source field name to display |
| `header` | `string` | — | Column header text |
| `width` | `string \| number` | — | Column width (px or CSS string) |
| `textAlign` | `'Left' \| 'Center' \| 'Right'` | `'Left'` | Horizontal text alignment in cells |
| `template` | `string \| function \| JSX.Element` | — | Custom template for cell content |
| `headerTemplate` | `string \| function \| JSX.Element` | — | Custom template for the header cell |
| `displayAsCheckBox` | `boolean` | `false` | Renders boolean values as checkboxes |
| `customAttributes` | `Object` | — | Custom HTML attributes applied to each cell |
| `format` | `string \| NumberFormatOptions \| DateFormatOptions` | — | Format string for dates and numbers |

---

## GridSettingsModel

Controls the visual appearance of the popup grid.

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `rowHeight` | `number` | `null` | Fixed row height in pixels |
| `gridLines` | `'Default' \| 'None' \| 'Horizontal' \| 'Vertical' \| 'Both'` | `'Default'` | Which grid lines to render |
| `enableAltRow` | `boolean` | `false` | Applies alternating row background colors |

---

## FieldSettingsModel

Maps data source object properties to the component's built-in roles.

| Property | Type | Description |
|----------|------|-------------|
| `text` | `string` | Field name whose value displays in the input after selection |
| `value` | `string` | Field name used as the underlying selected value |
| `groupBy` | `string` | Field name used to group items in the popup |
