# CheckBox States — Syncfusion React CheckBox

The `CheckBoxComponent` supports three visual states: **checked**, **unchecked**, and **indeterminate**. A **disabled** state is also available to prevent user interaction.

---

## Checked and Unchecked

Use the `checked` property to control the checked/unchecked state. When `checked={true}`, a checkmark appears in the frame.

```tsx
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  return (
    <ul>
      {/* Checked state */}
      <li><CheckBoxComponent label="Checked State" checked={true} /></li>

      {/* Unchecked state (default) */}
      <li><CheckBoxComponent label="Unchecked State" /></li>
    </ul>
  );
}
export default App;
```

**Property:** `checked` — `boolean`, defaults to `false`

---

## Indeterminate State

Set `indeterminate={true}` to display a partial-selection indicator. This is commonly used for **parent checkboxes** in hierarchical/tree lists where some (but not all) child items are selected.

> The indeterminate state can only be set programmatically — users cannot toggle it directly.

```tsx
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  return (
    <ul>
      <li><CheckBoxComponent label="Checked State" checked={true} /></li>
      <li><CheckBoxComponent label="Unchecked State" /></li>
      <li><CheckBoxComponent label="Indeterminate State" indeterminate={true} /></li>
    </ul>
  );
}
export default App;
```

**Property:** `indeterminate` — `boolean`, defaults to `false`

---

## Disabled State

Set `disabled={true}` to prevent user interaction. A disabled checkbox is visually dimmed and non-interactive. Disabled checkbox values are **not submitted** with forms.

```tsx
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  return (
    <ul>
      <li><CheckBoxComponent label="Active Option" checked={true} /></li>
      <li><CheckBoxComponent label="Disabled Option" disabled={true} /></li>
    </ul>
  );
}
export default App;
```

**Property:** `disabled` — `boolean`, defaults to `false`

---

## All States Together

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

enableRipple(true);

function App() {
  return (
    <ul>
      <li><CheckBoxComponent label="Checked" checked={true} /></li>
      <li><CheckBoxComponent label="Unchecked" /></li>
      <li><CheckBoxComponent label="Indeterminate" indeterminate={true} /></li>
      <li><CheckBoxComponent label="Disabled" disabled={true} /></li>
      <li><CheckBoxComponent label="Disabled + Checked" disabled={true} checked={true} /></li>
    </ul>
  );
}
export default App;
```

---

## Handling State Changes

Use the `change` event to respond when a user toggles the checkbox:

```tsx
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';
import { ChangeEventArgs } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  const onChange = (args: ChangeEventArgs) => {
    console.log('Checked:', args.checked);
  };

  return (
    <CheckBoxComponent label="Toggle Me" change={onChange} />
  );
}
export default App;
```

The `ChangeEventArgs` object provides the `checked` boolean reflecting the new state.

---

## State Summary

| State | Property | Default |
|-------|----------|---------|
| Checked | `checked={true}` | `false` |
| Unchecked | `checked={false}` | — |
| Indeterminate | `indeterminate={true}` | `false` |
| Disabled | `disabled={true}` | `false` |
