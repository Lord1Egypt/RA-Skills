# How-To Guides — Syncfusion React CheckBox

## Table of Contents
- [Use Name and Value in Form Submission](#use-name-and-value-in-form-submission)
- [Enable Right-to-Left (RTL)](#enable-right-to-left-rtl)
- [Create Customized Checkbox Variants](#create-customized-checkbox-variants)
  - [Color Variants](#color-variants)
  - [Round (Custom Frame) Checkbox](#round-custom-frame-checkbox)
  - [Custom Check Icon](#custom-check-icon)

---

## Use Name and Value in Form Submission

The `name` attribute groups checkboxes in a form. When the form is submitted, only **checked** checkbox values are sent to the server. **Disabled** and **unchecked** checkboxes are excluded from the submission payload.

Retrieve submitted values server-side using the `name` attribute key.

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { ButtonComponent, CheckBoxComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

enableRipple(true);

function App() {
  return (
    <form>
      <ul>
        {/* Checked — will be submitted */}
        <li><CheckBoxComponent name="Sport" value="Cricket" label="Cricket" checked={true} /></li>

        {/* Checked — will be submitted */}
        <li><CheckBoxComponent name="Sport" value="Hockey" label="Hockey" checked={true} /></li>

        {/* Disabled — will NOT be submitted */}
        <li><CheckBoxComponent name="Sport" value="Tennis" label="Tennis" disabled={true} /></li>

        {/* Unchecked — will NOT be submitted */}
        <li><CheckBoxComponent name="Sport" value="Basketball" label="Basketball" /></li>

        <li><ButtonComponent isPrimary={true}>Submit</ButtonComponent></li>
      </ul>
    </form>
  );
}
export default App;
```

**Result:** On submit, only `Sport=Cricket` and `Sport=Hockey` are sent.

- **`name`** — `string`: Groups checkboxes as a form field name
- **`value`** — `string`: The value sent for this checkbox when checked

---

## Enable Right-to-Left (RTL)

Set `enableRtl={true}` to flip the CheckBox layout for RTL locales (Arabic, Hebrew, etc.):

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

enableRipple(true);

function App() {
  return (
    <ul>
      <li><CheckBoxComponent label="Default RTL Checkbox" enableRtl={true} /></li>
    </ul>
  );
}
export default App;
```

The checkbox frame and label render in right-to-left order. Combine with `labelPosition="Before"` for additional control.

---

## Create Customized Checkbox Variants

### Color Variants

Apply semantic color meanings (primary, success, warning, danger, info) by combining `cssClass` with custom CSS:

```tsx
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <ul>
      <li><CheckBoxComponent label="Primary" cssClass="e-primary" checked={true} /></li>
      <li><CheckBoxComponent label="Success" cssClass="e-success" checked={true} /></li>
      <li><CheckBoxComponent label="Info" cssClass="e-info" checked={true} /></li>
      <li><CheckBoxComponent label="Warning" cssClass="e-warning" checked={true} /></li>
      <li><CheckBoxComponent label="Danger" cssClass="e-danger" checked={true} /></li>
    </ul>
  );
}
export default App;
```

Add corresponding CSS for each variant in your stylesheet — see the Style and Appearance reference for the CSS selector patterns.

---

### Round (Custom Frame) Checkbox

Create a circular checkbox frame using `border-radius: 100%`:

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

enableRipple(true);

function App() {
  return (
    <ul>
      <li><CheckBoxComponent label="Buy Groceries" cssClass="e-custom" checked={true} /></li>
      <li><CheckBoxComponent label="Pay Rent" cssClass="e-custom" /></li>
      <li><CheckBoxComponent label="Make Dinner" cssClass="e-custom" /></li>
      <li><CheckBoxComponent label="Finish To-do List Article" cssClass="e-custom" /></li>
    </ul>
  );
}
export default App;
```

**Required CSS:**
```css
.e-checkbox-wrapper.e-custom .e-frame {
  border-radius: 100%;
}
.e-checkbox-wrapper.e-custom .e-frame.e-check {
  border-radius: 100%;
  background-color: #007bff;
  border-color: #007bff;
}
```

---

### Custom Check Icon

Replace the default checkmark with a custom icon using a CSS `::before` pseudo-element:

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

enableRipple(true);

function App() {
  return (
    <ul>
      <li><CheckBoxComponent label="Buy Groceries" cssClass="e-checkicon" checked={true} /></li>
      <li><CheckBoxComponent label="Pay Rent" cssClass="e-checkicon" /></li>
      <li><CheckBoxComponent label="Make Dinner" cssClass="e-checkicon" /></li>
      <li><CheckBoxComponent label="Finish To-do List Article" cssClass="e-checkicon" /></li>
    </ul>
  );
}
export default App;
```

**Required CSS:**
```css
.e-checkbox-wrapper.e-checkicon .e-frame.e-check::before {
  content: '\e7ff'; /* Replace with your icon font unicode */
}
.e-checkbox-wrapper.e-checkicon .e-frame.e-check,
.e-checkbox-wrapper.e-checkicon:hover .e-frame.e-check {
  background-color: #7b1fa2;
  border-color: #7b1fa2;
}
```

---

## Tips

- Multiple custom classes can be combined: `cssClass="e-small e-custom"`
- The `name` and `value` props only affect form submission behavior — they do not change visual appearance
- RTL (`enableRtl`) can be combined with any size or style variant
