# Style and Appearance — Syncfusion React CheckBox

## Table of Contents
- [CSS Class Overrides](#css-class-overrides)
- [Color Variants with cssClass](#color-variants-with-cssclass)
- [Custom Frame Shape](#custom-frame-shape)
- [Custom Check Icon](#custom-check-icon)
- [Theme Studio](#theme-studio)

---

## CSS Class Overrides

Customize the CheckBox appearance by overriding its default CSS classes. Use the `cssClass` property to apply a class, then define styles in your CSS file.

The following table lists the available CSS selectors:

| CSS Selector | Purpose |
|---|---|
| `.e-checkbox-wrapper .e-frame` | Styles the checkbox frame |
| `.e-checkbox-wrapper:hover .e-frame` | Styles the frame on hover |
| `.e-checkbox-wrapper .e-label` | Styles the checkbox label |
| `.e-checkbox-wrapper:hover .e-label` | Styles the label on hover |
| `.e-checkbox-wrapper .e-frame.e-check` | Styles the checked frame |
| `.e-checkbox-wrapper:hover .e-frame.e-check` | Styles the checked frame on hover |
| `.e-checkbox-wrapper .e-frame.e-indeterminate` | Styles the indeterminate frame |
| `.e-checkbox-wrapper.e-disabled .e-frame` | Styles the disabled frame |
| `.e-checkbox-wrapper .e-ripple` | Styles the ripple effect |

---

## Color Variants with cssClass

Apply semantic color variants by combining `cssClass` with custom CSS rules. The example below creates primary, success, info, warning, and danger checkboxes:

**Component (App.tsx):**
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

**CSS (App.css) — example override for primary:**
```css
/* Primary */
.e-checkbox-wrapper.e-primary .e-frame.e-check,
.e-checkbox-wrapper.e-primary:hover .e-frame.e-check {
  background-color: #e3165b;
  border-color: #e3165b;
}

/* Success */
.e-checkbox-wrapper.e-success .e-frame.e-check,
.e-checkbox-wrapper.e-success:hover .e-frame.e-check {
  background-color: #4caf50;
  border-color: #4caf50;
}

/* Warning */
.e-checkbox-wrapper.e-warning .e-frame.e-check,
.e-checkbox-wrapper.e-warning:hover .e-frame.e-check {
  background-color: #ff9800;
  border-color: #ff9800;
}

/* Danger */
.e-checkbox-wrapper.e-danger .e-frame.e-check,
.e-checkbox-wrapper.e-danger:hover .e-frame.e-check {
  background-color: #f44336;
  border-color: #f44336;
}
```

---

## Custom Frame Shape

Create round (circular) checkboxes by setting `border-radius: 100%` on the frame via a custom CSS class:

**Component:**
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
    </ul>
  );
}
export default App;
```

**CSS:**
```css
/* Round frame */
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

## Custom Check Icon

Replace the default checkmark icon with a custom icon using CSS content override:

**Component:**
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
    </ul>
  );
}
export default App;
```

**CSS:**
```css
/* Custom check icon using a star symbol */
.e-checkbox-wrapper.e-checkicon .e-frame.e-check::before {
  content: '\e7ff';  /* Replace with desired icon unicode */
}
.e-checkbox-wrapper.e-checkicon:hover .e-frame.e-check,
.e-checkbox-wrapper.e-checkicon .e-frame.e-check {
  background-color: #7b1fa2;
  border-color: #7b1fa2;
}
```

---

## Theme Studio

For comprehensive custom theming, use the [Syncfusion Theme Studio](https://ej2.syncfusion.com/themestudio/?theme=material) to generate a custom CSS file. Import the generated CSS instead of the default theme to apply it across all Syncfusion components.

---

## Tips

- Multiple CSS classes can be combined: `cssClass="e-small e-primary"`
- The `cssClass` property is the recommended way to scope styles to specific checkbox instances
- Avoid modifying Syncfusion's default CSS files directly; override via your own stylesheet with higher specificity
