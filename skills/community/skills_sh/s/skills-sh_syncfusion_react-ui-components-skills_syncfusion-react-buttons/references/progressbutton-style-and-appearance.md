# Style and Appearance — React ProgressButton

## Overview

The `ProgressButtonComponent` appearance is controlled through the `cssClass` prop and by
overriding the component's CSS classes. You can also generate fully custom themes using
[Theme Studio](https://ej2.syncfusion.com/themestudio/?theme=material).

---

## CSS Class Reference

| CSS Class | Purpose |
|---|---|
| `.e-progress-btn` | Root container for the ProgressButton component |
| `.e-progress-btn.e-primary` | Applies primary (blue) styling |
| `.e-progress-btn.e-success` | Applies success (green) styling |
| `.e-progress-btn.e-info` | Applies info (cyan) styling |
| `.e-progress-btn.e-warning` | Applies warning (orange/yellow) styling |
| `.e-progress-btn.e-danger` | Applies danger (red) styling |
| `.e-progress-btn.e-outline` | Applies outline (transparent background, bordered) styling |
| `.e-progress-btn.e-flat` | Applies flat (no shadow/border) styling |
| `.e-progress-btn:hover` | Hover state styling |
| `.e-progress-btn:focus` | Keyboard focus state styling |
| `.e-progress-btn:active` | Pressed / active state styling |
| `.e-progress-btn:disabled` | Disabled state styling |
| `.e-progress-btn .e-progress-wrapper` | Container for the progress bar fill element |
| `.e-progress-btn .e-spinner-pane` | Container for the spinner animation |
| `.e-progress-btn .e-spinner-pane .e-spinner-inner svg .e-path-circle` | SVG circle element inside the spinner |

---

## Built-in cssClass Utilities

Pass these directly to the [`cssClass`](api.md#cssclass--string) prop (space-separated for multiple):

| Class | Effect |
|---|---|
| `e-hide-spinner` | Hides the spinner — shows only the progress fill |
| `e-vertical` | Progress fill moves top-to-bottom instead of left-to-right |
| `e-progress-top` | Progress fill is anchored to the top edge of the button |

```tsx
// Progress bar only (no spinner), vertical fill
<ProgressButtonComponent
  content="Upload"
  enableProgress={true}
  cssClass="e-hide-spinner e-vertical"
  duration={4000}
/>
```

---

## Applying Semantic Styles

```tsx
// Primary
<ProgressButtonComponent content="Submit" cssClass="e-primary" />

// Danger + outline
<ProgressButtonComponent content="Delete" cssClass="e-danger e-outline" />

// Success
<ProgressButtonComponent content="Saved" cssClass="e-success" />
```

---

## Custom CSS Overrides

Override component internals by targeting the classes above from your stylesheet:

```css
/* Custom progress bar colour */
.e-progress-btn .e-progress-wrapper {
  background-color: #6200ea;
}

/* Custom spinner colour */
.e-progress-btn .e-spinner-pane .e-spinner-inner svg .e-path-circle {
  stroke: #fff;
}

/* Rounded corners */
.e-progress-btn {
  border-radius: 24px;
}
```

---

## Reverse Progress (Right-to-Left Fill)

Add a custom class to `cssClass` and override the fill direction:

```tsx
<ProgressButtonComponent
  content="Reverse"
  enableProgress={true}
  cssClass="e-hide-spinner e-reverse-progress"
  duration={4000}
/>
```

```css
/* Override fill direction */
.e-progress-btn.e-reverse-progress .e-progress-wrapper {
  right: 0;
  left: auto;
}
```

---

## Theme Studio

Generate a custom theme at [ej2.syncfusion.com/themestudio](https://ej2.syncfusion.com/themestudio/?theme=material)
and download the generated CSS file for use in your project.

---

## See Also

- [API — cssClass property](api.md#cssclass--string)
- [Customize progress using cssClass](how-to-customize-progress-using-cssclass.md)
