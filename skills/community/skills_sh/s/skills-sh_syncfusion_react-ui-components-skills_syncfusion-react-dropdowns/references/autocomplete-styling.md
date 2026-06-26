# Styling and Customization – Syncfusion React AutoComplete

## Table of Contents
- [CSS Class Targets](#css-class-targets)
- [Wrapper Element Appearance](#wrapper-element-appearance)
- [Dropdown Icon Color](#dropdown-icon-color)
- [Focus Color](#focus-color)
- [Outline Theme Focus Color](#outline-theme-focus-color)
- [Disabled Text Color](#disabled-text-color)
- [Float Label Focus Color](#float-label-focus-color)
- [Placeholder Text Color](#placeholder-text-color)
- [Text Selection Color](#text-selection-color)
- [Popup Item Background on Hover and Active](#popup-item-background-on-hover-and-active)
- [Popup Item Appearance](#popup-item-appearance)
- [Mandatory Asterisk for Float Label](#mandatory-asterisk-for-float-label)
- [cssClass Property](#cssclass-property)
- [Float Label Type](#float-label-type)
- [Popup Resize](#popup-resize)

---

## CSS Class Targets

The AutoComplete uses standard Syncfusion CSS class names that can be targeted for styling overrides.

---

## Wrapper Element Appearance

```css
.e-ddl.e-input-group.e-control-wrapper .e-input {
  font-size: 20px;
  font-family: emoji;
  color: #ab3243;
  background: #32a5ab;
}
```

---

## Dropdown Icon Color

```css
.e-ddl.e-input-group .e-input-group-icon,
.e-ddl.e-input-group.e-control-wrapper .e-input-group-icon:hover {
  color: #bb233d;
  font-size: 13px;
}
```

---

## Focus Color

```css
.e-ddl.e-input-group.e-control-wrapper.e-input-focus::before,
.e-ddl.e-input-group.e-control-wrapper.e-input-focus::after {
  background: #c000ff;
}
```

---

## Outline Theme Focus Color

```css
.e-outline.e-input-group.e-input-focus:hover:not(.e-success):not(.e-warning):not(.e-error):not(.e-disabled):not(.e-float-icon-left),
.e-outline.e-input-group.e-input-focus.e-control-wrapper:hover:not(.e-success):not(.e-warning):not(.e-error):not(.e-disabled):not(.e-float-icon-left),
.e-outline.e-input-group.e-input-focus:not(.e-success):not(.e-warning):not(.e-error):not(.e-disabled),
.e-outline.e-input-group.e-control-wrapper.e-input-focus:not(.e-success):not(.e-warning):not(.e-error):not(.e-disabled) {
  border-color: #b1bd15;
  box-shadow: inset 1px 1px #b1bd15, inset -1px 0 #b1bd15, inset 0 -1px #b1bd15;
}
```

---

## Disabled Text Color

```css
.e-input-group.e-control-wrapper .e-input[disabled] {
  -webkit-text-fill-color: #0d9133;
}
```

---

## Float Label Focus Color

```css
.e-float-input.e-input-group:not(.e-float-icon-left) .e-float-line::before,
.e-float-input.e-control-wrapper.e-input-group:not(.e-float-icon-left) .e-float-line::before,
.e-float-input.e-input-group:not(.e-float-icon-left) .e-float-line::after,
.e-float-input.e-control-wrapper.e-input-group:not(.e-float-icon-left) .e-float-line::after {
  background-color: #2319b8;
}

.e-ddl.e-input-group.e-control-wrapper.e-float-input.e-input-focus .e-float-text.e-label-top,
.e-float-input.e-control-wrapper:not(.e-error).e-input-focus input ~ label.e-float-text {
  color: #2319b8;
}
```

---

## Placeholder Text Color

```css
.e-ddl.e-input-group input.e-input::placeholder {
  color: red;
}
```

---

## Text Selection Color

```css
.e-ddl.e-input-group input.e-input::selection {
  color: red;
  background: yellow;
}
```

---

## Popup Item Background on Hover and Active

```css
.e-dropdownbase .e-list-item.e-item-focus,
.e-dropdownbase .e-list-item.e-active,
.e-dropdownbase .e-list-item.e-active.e-hover,
.e-dropdownbase .e-list-item.e-hover {
  background-color: #1f9c99;
  color: #2319b8;
}
```

---

## Popup Item Appearance

```css
.e-dropdownbase .e-list-item,
.e-dropdownbase .e-list-item.e-item-focus {
  background-color: #29c2b8;
  color: #207cd9;
  font-family: emoji;
  min-height: 29px;
}
```

---

## Mandatory Asterisk for Float Label

Add a mandatory asterisk (*) to the float label:

```css
.e-input-group.e-control-wrapper.e-float-input .e-float-text::after {
  content: ' *';
  color: red;
}
```

---

## cssClass Property

Inject a custom CSS class onto the root element to scope styles:

```tsx
<AutoCompleteComponent
  id="atcelement"
  dataSource={sportsData}
  cssClass="custom-autocomplete"
  placeholder="Find a game"
/>
```

```css
.custom-autocomplete .e-input {
  border-radius: 8px;
}
```

---

## Float Label Type

Control float label behavior with `floatLabelType`:

```tsx
<AutoCompleteComponent
  id="atcelement"
  dataSource={sportsData}
  floatLabelType="Auto"   // 'Never' | 'Always' | 'Auto'
  placeholder="Find a game"
/>
```

| Value | Behavior |
|---|---|
| `'Never'` | Label never floats; stays as placeholder |
| `'Always'` | Label always floats above the input |
| `'Auto'` | Label floats when input is focused or has a value |

---

## Popup Resize

Allow users to dynamically resize the suggestion popup by dragging the resize handle in the bottom-right corner:

```tsx
import { AutoCompleteComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const statusData: { [key: string]: Object }[] = [
    { Status: 'Open',    State: false },
    { Status: 'On Hold', State: true  },
    { Status: 'Closed',  State: true  },
    { Status: 'Solved',  State: false },
  ];
  const fields: object = { value: 'Status' };

  return (
    <AutoCompleteComponent
      id="atcelement"
      dataSource={statusData}
      fields={fields}
      allowResize={true}
      placeholder="Select a status"
    />
  );
}
```

> Resized dimensions are retained across sessions. Three resize-related events fire: `resizeStart`, `resizing` (continuous), and `resizeStop`.
