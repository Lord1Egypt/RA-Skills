# API Reference — Syncfusion React CheckBox

Full API reference for `CheckBoxComponent` from `@syncfusion/ej2-react-buttons`.

**Source:** [Official API Documentation](https://ej2.syncfusion.com/react/documentation/api/check-box/index-default)

## Table of Contents
- [Import](#import)
- [Properties](#properties)
- [Methods](#methods)
- [Events](#events)
- [ChangeEventArgs Interface](#changeeventargs-interface)

---

## Import

```tsx
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';
import { ChangeEventArgs } from '@syncfusion/ej2-react-buttons';
```

---

## Properties

### checked
**Type:** `boolean` | **Default:** `false`

Specifies whether the CheckBox is in the checked state. When `true`, a checkmark is displayed in the checkbox frame.

```tsx
<CheckBoxComponent label="Option" checked={true} />
```

---

### cssClass
**Type:** `string` | **Default:** `''`

Defines one or more CSS class names (space-separated) applied to the CheckBox element. Use this to add custom styles or size variants.

```tsx
<CheckBoxComponent label="Small" cssClass="e-small" />
<CheckBoxComponent label="Custom" cssClass="e-primary e-small" />
```

Common built-in values: `'e-small'` (small size)

---

### disabled
**Type:** `boolean` | **Default:** `false`

Specifies whether the CheckBox is in the disabled state. When `true`, the checkbox is non-interactive and visually dimmed. Disabled checkboxes are not included in form submissions.

```tsx
<CheckBoxComponent label="Disabled" disabled={true} />
```

---

### enableHtmlSanitizer
**Type:** `boolean` | **Default:** `true`

Specifies whether to sanitize untrusted HTML strings before rendering them in the CheckBox (e.g., in the `label` property). When `true`, suspected scripts and unsafe HTML are sanitized. Set to `false` only for trusted, controlled content.

```tsx
<CheckBoxComponent label="<b>Bold</b>" enableHtmlSanitizer={false} />
```

---

### enablePersistence
**Type:** `boolean` | **Default:** `false`

Enables persisting the component's state (checked/unchecked) between page reloads using browser `localStorage`.

```tsx
<CheckBoxComponent label="Remember Me" enablePersistence={true} />
```

---

### enableRtl
**Type:** `boolean` | **Default:** `false`

Enables right-to-left rendering of the CheckBox component. When `true`, the layout mirrors for RTL locales (Arabic, Hebrew, etc.).

```tsx
<CheckBoxComponent label="خيار" enableRtl={true} />
```

---

### htmlAttributes
**Type:** `{ [key: string]: string }` | **Default:** `{}`

Adds additional HTML attributes to the underlying `<input>` element. If the same attribute is set both via `htmlAttributes` and a direct property, the property value takes precedence.

```tsx
<CheckBoxComponent
  label="Required field"
  htmlAttributes={{ required: 'required', 'data-id': 'cb-1' }}
/>
```

---

### indeterminate
**Type:** `boolean` | **Default:** `false`

Specifies whether the CheckBox is in the indeterminate state. When `true`, neither fully checked nor unchecked — visually shows a dash. Used for parent checkboxes in hierarchical selections. Cannot be set by user interaction; must be set programmatically.

```tsx
<CheckBoxComponent label="Select All" indeterminate={true} />
```

---

### label
**Type:** `string` | **Default:** `''`

Defines the caption text displayed next to the CheckBox. Eliminates the need for a separate `<label>` HTML element.

```tsx
<CheckBoxComponent label="Accept Terms and Conditions" />
```

---

### labelPosition
**Type:** `'Before' | 'After'` | **Default:** `'After'`

Controls the position of the label relative to the checkbox frame.

- `'After'` — Label appears to the right (default)
- `'Before'` — Label appears to the left

```tsx
<CheckBoxComponent label="Label on Left" labelPosition="Before" />
```

---

### locale
**Type:** `string` | **Default:** `''`

Overrides the global culture and localization value for this component. When empty, inherits the global culture (`'en-US'`).

```tsx
<CheckBoxComponent label="Option" locale="fr-FR" />
```

---

### name
**Type:** `string` | **Default:** `''`

Defines the `name` attribute for the checkbox input element. Used to group checkboxes in a form and to reference form data after submission. Only checked (and non-disabled) checkboxes with a `name` send their `value` on form submit.

```tsx
<CheckBoxComponent name="hobbies" value="reading" label="Reading" />
```

---

### value
**Type:** `string` | **Default:** `''`

Defines the `value` attribute for the checkbox input element. This value is submitted with the form when the checkbox is checked.

```tsx
<CheckBoxComponent name="hobbies" value="reading" label="Reading" checked={true} />
```

---

## Methods

Access methods via a React ref:

```tsx
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  const checkboxRef = React.useRef<CheckBoxComponent>(null);

  return (
    <CheckBoxComponent
      ref={checkboxRef}
      label="Option"
    />
  );
}
```

### click()
**Returns:** `void`

Programmatically triggers a click on the CheckBox element (native method). Toggles the checked state as if the user clicked.

```tsx
checkboxRef.current?.click();
```

---

### destroy()
**Returns:** `void`

Destroys the CheckBox component and cleans up event listeners and DOM modifications.

```tsx
checkboxRef.current?.destroy();
```

---

### focusIn()
**Returns:** `void`

Sets focus to the CheckBox element (native method). Useful for programmatic focus management in forms.

```tsx
checkboxRef.current?.focusIn();
```

---

## Events

### change
**Type:** `EmitType<ChangeEventArgs>`

Triggers when the CheckBox state is changed by user interaction (click or Space key). Provides a `ChangeEventArgs` object.

```tsx
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';
import { ChangeEventArgs } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  const handleChange = (args: ChangeEventArgs) => {
    console.log('New checked state:', args.checked);
  };

  return (
    <CheckBoxComponent label="Toggle" change={handleChange} />
  );
}
export default App;
```

---

### created
**Type:** `EmitType<Event>`

Triggers once the component has finished rendering. Use this for post-render initialization logic.

```tsx
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  const handleCreated = () => {
    console.log('CheckBox component rendered');
  };

  return (
    <CheckBoxComponent label="Option" created={handleCreated} />
  );
}
export default App;
```

---

## ChangeEventArgs Interface

The `change` event callback receives a `ChangeEventArgs` object:

| Property | Type | Description |
|----------|------|-------------|
| `checked` | `boolean` | The new checked state after the change |
| `event` | `Event` | The original DOM event |

```tsx
const handleChange = (args: ChangeEventArgs) => {
  if (args.checked) {
    console.log('Checkbox is now checked');
  } else {
    console.log('Checkbox is now unchecked');
  }
};
```

---

## Quick Reference Table

| API | Type | Default | Category |
|-----|------|---------|----------|
| `checked` | `boolean` | `false` | Property |
| `cssClass` | `string` | `''` | Property |
| `disabled` | `boolean` | `false` | Property |
| `enableHtmlSanitizer` | `boolean` | `true` | Property |
| `enablePersistence` | `boolean` | `false` | Property |
| `enableRtl` | `boolean` | `false` | Property |
| `htmlAttributes` | `object` | `{}` | Property |
| `indeterminate` | `boolean` | `false` | Property |
| `label` | `string` | `''` | Property |
| `labelPosition` | `'Before' \| 'After'` | `'After'` | Property |
| `locale` | `string` | `''` | Property |
| `name` | `string` | `''` | Property |
| `value` | `string` | `''` | Property |
| `click()` | `void` | — | Method |
| `destroy()` | `void` | — | Method |
| `focusIn()` | `void` | — | Method |
| `change` | `ChangeEventArgs` | — | Event |
| `created` | `Event` | — | Event |
