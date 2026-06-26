# Switch Style and Appearance

Customize the Syncfusion React Switch's visual appearance by overriding CSS classes or using the `cssClass` property to scope custom styles.

## Table of Contents
- [CSS Class Reference](#css-class-reference)
- [Size Variants](#size-variants)
- [Customize Bar and Handle Shape](#customize-bar-and-handle-shape)
- [Customize Switch Colors](#customize-switch-colors)
- [Theme Studio](#theme-studio)
- [Accessibility and Disabled Styling](#accessibility-and-disabled-styling)

---

## CSS Class Reference

The following CSS classes are available for targeting specific Switch elements:

| CSS Class | Purpose |
|-----------|---------|
| `.e-switch-wrapper` | Main Switch component container |
| `.e-switch` | Core Switch element |
| `.e-switch-inner` | Switch track (bar) in off mode |
| `.e-switch-inner.e-switch-active` | Switch track (bar) in on mode |
| `.e-switch-on` | On state label and styling |
| `.e-switch-handle` | Switch thumb (handle) in off mode |
| `.e-switch-handle.e-switch-active` | Switch thumb (handle) in on mode |
| `.e-switch-wrapper:hover .e-switch-inner` | Track hover state styling |
| `.e-switch-wrapper:hover .e-switch-handle` | Handle hover state styling |
| `.e-switch-wrapper.e-switch-disabled` | Disabled state styling |
| `.e-switch-wrapper.e-disabled` | Alternative disabled state class |
| `.e-switch-label` | Label text styling |
| `.e-switch-wrapper.e-small` | Small size variant |
| `.e-switch-wrapper.e-large` | Large size variant |

---

## Size Variants

The Switch has two built-in sizes. Apply them via the `cssClass` property:

```tsx
// Small size
<SwitchComponent cssClass="e-small" />

// Default size (no extra class needed)
<SwitchComponent />
```

To compare sizes side by side:

```tsx
import { SwitchComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  return (
    <table>
      <tbody>
        <tr>
          <td>Small</td>
          <td><SwitchComponent cssClass="e-small" /></td>
        </tr>
        <tr>
          <td>Default</td>
          <td><SwitchComponent /></td>
        </tr>
      </tbody>
    </table>
  );
}
```

---

## Customize Bar and Handle Shape

Use the `cssClass` property to assign a scoping class, then write CSS rules targeting `.e-switch-inner` and `.e-switch-handle` to reshape them.

```tsx
import { SwitchComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  return (
    <div>
      {/* Square-shaped switch */}
      <label htmlFor="switch1">Square Switch</label>
      <SwitchComponent id="switch1" cssClass="square" />

      {/* Custom bar and handle */}
      <label htmlFor="switch2">Bar and handle</label>
      <SwitchComponent id="switch2" cssClass="custom-switch" checked={true} />

      {/* Handle with text */}
      <label htmlFor="switch3">Handle text</label>
      <SwitchComponent id="switch3" cssClass="handle-text" />
    </div>
  );
}
```

Corresponding CSS (in your stylesheet):

```css
/* Square shape: remove border-radius */
.square .e-switch-inner,
.square .e-switch-handle {
  border-radius: 0;
}

/* Custom bar height and handle size */
.custom-switch .e-switch-inner {
  height: 24px;
  border-radius: 4px;
}
.custom-switch .e-switch-handle {
  width: 20px;
  height: 20px;
  border-radius: 4px;
}

/* Text inside handle */
.handle-text .e-switch-handle::after {
  content: 'OFF';
  font-size: 8px;
}
.handle-text .e-switch-handle.e-switch-active::after {
  content: 'ON';
}
```

---

## Customize Switch Colors

Override the background and border properties of `.e-switch-inner` and `.e-switch-handle` to apply brand colors.

```tsx
import { SwitchComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  return (
    <div>
      <label htmlFor="switch1">Custom color</label>
      <SwitchComponent id="switch1" cssClass="bar-color" />

      <label htmlFor="switch2">Handle color</label>
      <SwitchComponent id="switch2" cssClass="handle-color" checked={true} />

      <label htmlFor="switch3">iOS Switch</label>
      <SwitchComponent id="switch3" cssClass="custom-iOS" checked={true} />
    </div>
  );
}
```

Corresponding CSS:

```css
/* Custom bar color */
.bar-color .e-switch-inner.e-switch-active {
  background-color: #4CAF50;
  border-color: #4CAF50;
}

/* Custom handle color */
.handle-color .e-switch-handle {
  background-color: #FF5722;
}

/* iOS-style */
.custom-iOS .e-switch-inner {
  border-radius: 14px;
}
.custom-iOS .e-switch-inner.e-switch-active {
  background-color: #34C759;
  border-color: #34C759;
}
.custom-iOS .e-switch-handle {
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0,0,0,0.3);
}
```

---

## Theme Studio

Use [Syncfusion Theme Studio](https://ej2.syncfusion.com/themestudio/?theme=material) to visually customize and preview themes for all Syncfusion components, including Switch. Export the generated CSS and include it in your project to apply the custom theme.

---

## Accessibility and Disabled Styling

The disabled state applies `.e-switch-disabled` and `.e-disabled` classes to the wrapper. You can further customize the disabled appearance:

```css
.e-switch-wrapper.e-switch-disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

> Do not rely solely on color to indicate disabled state — ensure sufficient contrast for WCAG compliance.
