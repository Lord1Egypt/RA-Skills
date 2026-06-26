# Style and Accessibility

This reference covers CSS customization of the Uploader component's appearance and its accessibility features (WCAG 2.2, keyboard navigation, screen reader support, RTL).

---

## CSS Selectors Reference

| Selector | Targets |
|----------|---------|
| `.e-upload.e-control-wrapper` | Overall component wrapper |
| `.e-upload .e-file-select-wrap .e-btn` | Browse button |
| `.e-upload .e-upload-actions .e-btn` | Upload / Clear action buttons |
| `.e-upload .e-file-select-wrap .e-file-drop` | Drop area text |
| `.e-upload .e-upload-files .e-upload-file-list` | Individual file list items |
| `.e-upload .e-upload-progress-bar .e-upload-progress` | Progress bar fill |
| `.e-upload .e-file-status` | File status text |
| `.e-upload-drag-hover` | Drop area state when file is dragged over it |

---

## Customizing Wrapper Dimensions

```css
.e-upload.e-control-wrapper,
.e-bigger.e-small .e-upload.e-control-wrapper {
  height: 300px;
  width: 400px;
}
```

---

## Customizing Buttons

Style the Browse, Upload, and Clear buttons:

```css
.e-upload .e-file-select-wrap .e-btn,
.e-upload .e-upload-actions .e-btn,
.e-bigger.e-small .e-upload .e-file-select-wrap .e-btn,
.e-bigger.e-small .e-upload .e-upload-actions .e-btn {
  background-color: #0078d4;
  color: #fff;
  border-radius: 4px;
  font-family: 'Segoe UI', sans-serif;
  height: 36px;
}
```

---

## Customizing the Drop Area Text

```css
.e-upload .e-file-select-wrap .e-file-drop,
.e-bigger.e-small .e-upload .e-file-select-wrap .e-file-drop {
  font-size: 16px;
  color: #555;
}
```

---

## Customizing the File List

```css
/* File list item background */
.e-upload .e-upload-files .e-upload-file-list {
  background-color: #f9f9f9;
  border-radius: 4px;
  margin-bottom: 4px;
}
```

---

## Customizing the Progress Bar

```css
/* Progress bar fill color */
.e-upload .e-upload-progress-bar .e-upload-progress {
  background-color: #28a745;
}

/* Thicker progress bar */
.e-upload .e-upload-progress-bar {
  height: 6px;
  border-radius: 3px;
}
```

---

## Theme Integration

Apply a Syncfusion theme by importing the correct CSS files. All three imports must use the same theme name:

```css
/* Tailwind3 */
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-inputs/styles/tailwind3.css";

/* Bootstrap 5.3 */
@import "../node_modules/@syncfusion/ej2-base/styles/bootstrap5.3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/bootstrap5.3.css";
@import "../node_modules/@syncfusion/ej2-react-inputs/styles/bootstrap5.3.css";

/* Material 3 */
@import "../node_modules/@syncfusion/ej2-base/styles/material3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/material3.css";
@import "../node_modules/@syncfusion/ej2-react-inputs/styles/material3.css";

/* Fluent 2 */
@import "../node_modules/@syncfusion/ej2-base/styles/fluent2.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/fluent2.css";
@import "../node_modules/@syncfusion/ej2-react-inputs/styles/fluent2.css";
```

---

## Accessibility Standards

The Syncfusion React Uploader fully meets:

| Standard | Status |
|----------|--------|
| WCAG 2.2 | ✅ Full compliance |
| Section 508 | ✅ Full compliance |
| ADA | ✅ Full compliance |
| Screen reader support | ✅ Full |
| RTL support | ✅ Full |
| Color contrast | ✅ Full |
| Mobile device support | ✅ Full |
| Keyboard navigation | ✅ Full |
| Axe-core validation | ✅ Passes |
| Accessibility checker | ✅ Passes |

---

## Keyboard Navigation

| Key | Action |
|-----|--------|
| `Tab` | Move focus to the next interactive element |
| `Shift + Tab` | Move focus to the previous element |
| `Enter` | Activate the focused button (Browse, Upload, Clear, Remove) |
| `Esc` | Close the file browser dialog; cancel pending upload |

The component is fully keyboard-operable without a mouse. Users can browse, upload, and remove files entirely from the keyboard.

---

## ARIA Attributes

The Uploader sets appropriate ARIA attributes automatically:
- Browse button: `role="button"` with descriptive `aria-label`
- Progress bar: `role="progressbar"` with `aria-valuenow`, `aria-valuemin`, `aria-valuemax`
- File list: `role="list"` with `role="listitem"` per file

No additional ARIA configuration is required for standard use.

---

## RTL (Right-to-Left) Support

Enable RTL layout with the `enableRtl` prop:

```tsx
<UploaderComponent asyncSettings={asyncSettings} enableRtl={true} />
```

The entire UI layout mirrors for RTL locales. Pair with localization for a complete RTL experience.

---

## See Also

- [Integration & security](./integration-and-security.md) — localization, form support, JWT
- [Template customization](./template-customization.md) — custom file list UI
