# Style and Appearance — Syncfusion React RadioButton

## Table of Contents
- [CSS Class Reference](#css-class-reference)
- [Custom Appearance with cssClass](#custom-appearance-with-cssclass)
- [Semantic Color Variants](#semantic-color-variants)
- [Small Size Variant](#small-size-variant)
- [Theme Studio](#theme-studio)

---

## CSS Class Reference

Syncfusion exposes specific CSS classes you can override to customize the RadioButton's visual appearance. Target these selectors in your stylesheet:

| CSS Class / Selector | Purpose |
|----------------------|---------|
| `.e-radio-wrapper` | Container wrapper for the entire RadioButton component |
| `.e-radio` | The hidden `<input type="radio">` element |
| `.e-radio + label` | Label text associated with the RadioButton |
| `.e-radio + label::before` | The outer circle (indicator ring) of the RadioButton |
| `.e-radio + label::after` | The inner filled circle shown when checked |
| `.e-radio:hover + label::before` | Indicator ring on mouse hover |
| `.e-radio:checked + label::before` | Indicator ring when the button is checked |
| `.e-radio:checked + label::after` | Inner circle when the button is checked |
| `.e-radio:focus + label::before` | Indicator ring when focused via keyboard |
| `.e-radio:disabled + label` | Label styling when the button is disabled |
| `.e-radio:disabled + label::before` | Indicator ring when disabled |
| `.e-small` | Applies the compact (small) size variant |

---

## Custom Appearance with cssClass

Use the `cssClass` property to apply one or more custom CSS classes to the RadioButton wrapper. Then define those classes in your stylesheet to override colors, sizes, or borders.

```tsx
import { RadioButtonComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  return (
    <RadioButtonComponent
      label="Custom Style"
      name="custom"
      cssClass="my-radio"
    />
  );
}
export default App;
```

```css
/* Override the outer ring color */
.my-radio .e-radio + label::before {
  border-color: #7b2ff7;
}

/* Override the inner filled circle when checked */
.my-radio .e-radio:checked + label::after {
  background-color: #7b2ff7;
}

/* Override the border when checked */
.my-radio .e-radio:checked + label::before {
  border-color: #7b2ff7;
}
```

---

## Semantic Color Variants

Create named style variants to match your design system. Apply them via `cssClass` and define the CSS rules targeting each variant:

```tsx
import { RadioButtonComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  return (
    <ul>
      <li><RadioButtonComponent label="Primary" cssClass="e-primary"  name="custom" /></li>
      <li><RadioButtonComponent label="Success" cssClass="e-success"  name="custom" /></li>
      <li><RadioButtonComponent label="Info"    cssClass="e-info"     name="custom" checked={true} /></li>
      <li><RadioButtonComponent label="Warning" cssClass="e-warning"  name="custom" /></li>
      <li><RadioButtonComponent label="Danger"  cssClass="e-danger"   name="custom" /></li>
    </ul>
  );
}
export default App;
```

Define the CSS for each variant (example for `e-primary`):

```css
/* Primary variant */
.e-primary .e-radio + label::before {
  border-color: #e3165b;
}
.e-primary .e-radio:checked + label::before {
  border-color: #e3165b;
}
.e-primary .e-radio:checked + label::after {
  background-color: #e3165b;
}

/* Success variant */
.e-success .e-radio + label::before {
  border-color: #4caf50;
}
.e-success .e-radio:checked + label::before {
  border-color: #4caf50;
}
.e-success .e-radio:checked + label::after {
  background-color: #4caf50;
}

/* Info variant */
.e-info .e-radio + label::before {
  border-color: #0378d5;
}
.e-info .e-radio:checked + label::before {
  border-color: #0378d5;
}
.e-info .e-radio:checked + label::after {
  background-color: #0378d5;
}

/* Warning variant */
.e-warning .e-radio + label::before {
  border-color: #ff7f00;
}
.e-warning .e-radio:checked + label::before {
  border-color: #ff7f00;
}
.e-warning .e-radio:checked + label::after {
  background-color: #ff7f00;
}

/* Danger variant */
.e-danger .e-radio + label::before {
  border-color: #f44336;
}
.e-danger .e-radio:checked + label::before {
  border-color: #f44336;
}
.e-danger .e-radio:checked + label::after {
  background-color: #f44336;
}
```

> **Pattern:** Override `label::before` for the ring, `label::after` for the fill. Always update both the unchecked ring and the checked state for full visual consistency.

---

## Small Size Variant

Apply `cssClass="e-small"` to render a compact RadioButton suitable for dense UIs:

```tsx
<RadioButtonComponent label="Small Option" name="size" cssClass="e-small" />
```

Combine with other custom classes:

```tsx
<RadioButtonComponent
  label="Small Primary"
  name="combo"
  cssClass="e-small e-primary"
/>
```

---

## Theme Studio

For global theme customization across all Syncfusion components (not just RadioButton), use [Syncfusion Theme Studio](https://ej2.syncfusion.com/themestudio/?theme=material):

1. Open Theme Studio in your browser
2. Select your base theme (Material, Bootstrap, Fluent, etc.)
3. Adjust colors, sizes, and typography
4. Export and download the generated CSS
5. Replace the default theme import in your project

This approach modifies all Syncfusion components consistently, rather than overriding individual CSS selectors.

---

## See Also

- [label-and-size.md](label-and-size.md) — `cssClass="e-small"` and label positioning
- [features-and-state.md](features-and-state.md) — disabled styling behavior
- [api.md](api.md) — `cssClass` property reference
