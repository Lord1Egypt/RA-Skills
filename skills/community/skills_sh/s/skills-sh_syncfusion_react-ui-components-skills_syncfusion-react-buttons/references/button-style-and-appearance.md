# Style and Appearance — Syncfusion React Button

## Table of Contents
1. [Available CSS Classes](#available-css-classes)
2. [Overriding Default Styles](#overriding-default-styles)
3. [Custom Theme with Theme Studio](#custom-theme-with-theme-studio)

---

## Available CSS Classes

The following CSS classes are available for customizing and overriding button styles. Apply them via the `cssClass` prop or by targeting the class names in your stylesheets.

| CSS Class | Purpose |
|---|---|
| `.e-btn` | Base button style applied to all `ButtonComponent` instances |
| `.e-btn:hover` | Hover state styling |
| `.e-btn:focus` | Focus state styling (keyboard / tab navigation) |
| `.e-btn:active` | Active (pressed) state styling |
| `.e-primary` | Primary action style |
| `.e-success` | Success / positive action style |
| `.e-info` | Informational action style |
| `.e-warning` | Cautionary action style |
| `.e-danger` | Destructive / negative action style |
| `.e-link` | Hyperlink appearance |
| `.e-flat` | Flat style — no background color |
| `.e-outline` | Outline style — transparent background with border |
| `.e-round` | Circular shape — use with icon-only buttons |
| `.e-small` | Small button size |
| `.e-block` | Full-width (block-level) button |
| `.e-round-corner` | Rounded corners (5px border radius) |

---

## Overriding Default Styles

Override Syncfusion's built-in styles by targeting the class names in your own stylesheet. Place your overrides **after** the Syncfusion CSS imports to ensure specificity.

**Example — change background, text color, size, and corner style for all states:**

```css
/* styles.css — loaded after Syncfusion CSS imports */

/* Default state */
.e-btn.e-custom {
  background-color: #6c5ce7;
  color: #ffffff;
  height: 44px;
  min-width: 120px;
  border-radius: 8px;
  border: none;
  font-weight: 600;
}

/* Hover state */
.e-btn.e-custom:hover {
  background-color: #a29bfe;
  color: #ffffff;
}

/* Focus state */
.e-btn.e-custom:focus {
  background-color: #6c5ce7;
  box-shadow: 0 0 0 3px rgba(108, 92, 231, 0.35);
}

/* Active (pressed) state */
.e-btn.e-custom:active {
  background-color: #4834d4;
}
```

Apply the class in the component:

```tsx
<ButtonComponent cssClass='e-custom'>Custom Button</ButtonComponent>
```

> Use double class selectors (`.e-btn.e-custom`) to increase specificity and reliably override Syncfusion's default rules.

---

## Custom Theme with Theme Studio

For full-scale theme customization across all Syncfusion components, use [Syncfusion Theme Studio](https://ej2.syncfusion.com/themestudio/?theme=material):

1. Open Theme Studio and select your base theme (Material, Bootstrap, Tailwind, Fluent, etc.).
2. Customize global color tokens — these cascade to all components including buttons.
3. Download the generated CSS file.
4. Replace the default Syncfusion CSS import in `App.css` with the downloaded file.

This approach is preferable to manual CSS overrides when building a consistent design system.
