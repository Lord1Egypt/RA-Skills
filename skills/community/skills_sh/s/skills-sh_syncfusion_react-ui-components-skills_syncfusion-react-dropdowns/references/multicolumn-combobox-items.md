# Items and Configuration — Syncfusion React MultiColumn ComboBox

## Table of Contents
- [Setting Initial Selection](#setting-initial-selection)
- [Placeholder and Float Label](#placeholder-and-float-label)
- [Clear Button](#clear-button)
- [Disabled and Read Only States](#disabled-and-read-only-states)
- [Width and Popup Size](#width-and-popup-size)
- [CSS Class Customization](#css-class-customization)
- [HTML Attributes](#html-attributes)
- [Grid Settings](#grid-settings)
- [Programmatic Methods](#programmatic-methods)

---

## Setting Initial Selection

Pre-select an item using `text`, `value`, or `index`.

**By text** (display text of the item):
```tsx
<MultiColumnComboBoxComponent dataSource={empData} fields={fields} text="Michael">
  {/* columns */}
</MultiColumnComboBoxComponent>
```

**By value** (hidden key value):
```tsx
<MultiColumnComboBoxComponent dataSource={empData} fields={fields} value="1015">
  {/* columns */}
</MultiColumnComboBoxComponent>
```

**By index** (zero-based position):
```tsx
<MultiColumnComboBoxComponent dataSource={empData} fields={fields} index={1}>
  {/* columns */}
</MultiColumnComboBoxComponent>
```

Use only one at a time. `text` is most human-readable; `value` is best for forms; `index` is useful for "select first item" patterns.

---

## Placeholder and Float Label

**Placeholder** sets hint text displayed when no item is selected:

```tsx
<MultiColumnComboBoxComponent
  dataSource={empData}
  fields={fields}
  placeholder="Select an employee"
>
  {/* columns */}
</MultiColumnComboBoxComponent>
```

**Float Label** makes the placeholder float above the input instead of disappearing when a value is entered. Requires `placeholder` to be set.

| `floatLabelType` | Behavior |
|-----------------|----------|
| `'Never'` | Placeholder never floats (default) |
| `'Always'` | Label always floats above the input |
| `'Auto'` | Label floats after focus or after entering a value |

```tsx
<MultiColumnComboBoxComponent
  dataSource={empData}
  fields={fields}
  placeholder="Select an employee"
  floatLabelType="Auto"
>
  {/* columns */}
</MultiColumnComboBoxComponent>
```

---

## Clear Button

Show a clear (×) button to reset the selection:

```tsx
<MultiColumnComboBoxComponent
  dataSource={empData}
  fields={fields}
  text="Michael"
  showClearButton={true}
>
  {/* columns */}
</MultiColumnComboBoxComponent>
```

Clicking the clear button resets `value`, `text`, and `index` properties to `null`. Default is `false`.

---

## Disabled and Read Only States

**Disabled** — prevents all interactions:
```tsx
<MultiColumnComboBoxComponent dataSource={empData} fields={fields} text="Michael" disabled={true}>
  {/* columns */}
</MultiColumnComboBoxComponent>
```

**Read Only** — allows viewing but not editing:
```tsx
<MultiColumnComboBoxComponent dataSource={empData} fields={fields} text="Michael" readonly={true}>
  {/* columns */}
</MultiColumnComboBoxComponent>
```

| Property | Default | Effect |
|----------|---------|--------|
| `disabled` | `false` | Fully disables the component |
| `readonly` | `false` | Prevents user input but allows display |

---

## Width and Popup Size

**Component width** (defaults to parent container width):
```tsx
<MultiColumnComboBoxComponent dataSource={empData} fields={fields} width="500px">
  {/* columns */}
</MultiColumnComboBoxComponent>
```

**Popup dimensions:**
```tsx
<MultiColumnComboBoxComponent
  dataSource={empData}
  fields={fields}
  popupWidth="400px"
  popupHeight="400px"
>
  {/* columns */}
</MultiColumnComboBoxComponent>
```

Both `width`, `popupWidth`, and `popupHeight` accept `string` (e.g., `'400px'`) or `number` (in pixels).

---

## CSS Class Customization

Add a custom CSS class to the root element for styling:

```tsx
<MultiColumnComboBoxComponent
  dataSource={empData}
  fields={fields}
  cssClass="e-custom-multi-column"
>
  {/* columns */}
</MultiColumnComboBoxComponent>
```

Then in your CSS:
```css
.e-custom-multi-column .e-input-group {
  border-radius: 8px;
  border-color: #007bff;
}
```

---

## HTML Attributes

Add arbitrary HTML attributes (title, name, data-*, aria-*) to the underlying input element:

```tsx
<MultiColumnComboBoxComponent
  dataSource={empData}
  fields={fields}
  htmlAttributes={{ title: 'Select an employee', 'data-testid': 'emp-select' }}
>
  {/* columns */}
</MultiColumnComboBoxComponent>
```

---

## Grid Settings

Configure the popup grid appearance with `gridSettings`. Uses `GridSettingsModel`.

### Grid Lines

```tsx
// Options: 'Default' | 'Horizontal' | 'Vertical' | 'Both' | 'None'
<MultiColumnComboBoxComponent
  dataSource={empData}
  fields={fields}
  gridSettings={{ gridLines: 'Horizontal' }}
>
  {/* columns */}
</MultiColumnComboBoxComponent>
```

### Row Height

```tsx
<MultiColumnComboBoxComponent
  dataSource={empData}
  fields={fields}
  gridSettings={{ rowHeight: 40 }}
>
  {/* columns */}
</MultiColumnComboBoxComponent>
```

### Alternate Row Styling

```tsx
<MultiColumnComboBoxComponent
  dataSource={empData}
  fields={fields}
  gridSettings={{ enableAltRow: true }}
>
  {/* columns */}
</MultiColumnComboBoxComponent>
```

When `enableAltRow` is `true`, the CSS class `e-altrow` is applied to alternating rows.

**Combined example:**
```tsx
<MultiColumnComboBoxComponent
  dataSource={empData}
  fields={fields}
  gridSettings={{ rowHeight: 40, enableAltRow: true, gridLines: 'Horizontal' }}
>
  {/* columns */}
</MultiColumnComboBoxComponent>
```

---

## Programmatic Methods

Access component methods via a ref:

```tsx
import { MultiColumnComboBoxComponent } from '@syncfusion/ej2-react-multicolumn-combobox';
import * as React from 'react';

function App() {
  const comboRef = React.useRef<MultiColumnComboBoxComponent>(null);

  const handleOpen = () => comboRef.current?.showPopup();
  const handleClose = () => comboRef.current?.hidePopup();
  const handleFocus = () => comboRef.current?.focusIn();
  const handleBlur = () => comboRef.current?.focusOut();
  const handleGetData = () => {
    const data = comboRef.current?.getDataByValue('1003');
    console.log(data);
  };

  return (
    <>
      <MultiColumnComboBoxComponent ref={comboRef} dataSource={empData} fields={fields}>
        {/* columns */}
      </MultiColumnComboBoxComponent>
      <button onClick={handleOpen}>Open Popup</button>
      <button onClick={handleClose}>Close Popup</button>
      <button onClick={handleGetData}>Get Data by Value</button>
    </>
  );
}
```

| Method | Description |
|--------|-------------|
| `showPopup(e?)` | Opens the popup dropdown |
| `hidePopup(e?)` | Closes the popup dropdown |
| `focusIn(e?)` | Sets focus to the component |
| `focusOut(e?)` | Removes focus from the component |
| `getDataByValue(value)` | Returns the data object matching the given value |
| `getItems()` | Returns all rendered list item elements |
| `addItems(items, index?)` | Adds new items to the popup list |
