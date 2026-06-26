# Accessibility in Syncfusion React Signature

The Signature component is designed to meet accessibility standards for use with assistive technologies and keyboard-only navigation.

---

## Compliance Overview

| Accessibility Criteria | Support |
|------------------------|---------|
| WCAG 2.2 | ✅ Full |
| Section 508 | ✅ Full |
| Screen Reader Support | ✅ Full |
| Right-To-Left Support | N/A |
| Color Contrast | ✅ Full |
| Mobile Device Support | ✅ Full |
| Keyboard Navigation Support | ✅ Full |
| Accessibility Checker Validation | ✅ Full |
| Axe-core Accessibility Validation | ✅ Full |

---

## Keyboard Interaction

The Signature component supports the following keyboard shortcuts when the canvas has focus:

| Key | Action |
|-----|--------|
| `Ctrl + Z` | Undo the last stroke/action |
| `Ctrl + Y` | Redo the last undone action |
| `Ctrl + S` | Save the signature (triggers `beforeSave` event) |
| `Delete` | Clear all signature strokes from the canvas |

> **Note:** `Ctrl + S` raises the `beforeSave` event, which allows you to customize the file name and type before the download occurs. This event is only triggered via keyboard — not when calling `save()` programmatically.

---

## Screen Reader Support

The Signature canvas is equipped with appropriate ARIA roles and labels so screen readers can announce the component's state and purpose to users who rely on assistive technology.

---

## Mobile Device Support

The component captures input from touch events (finger or stylus), making it fully functional on tablets and touchscreen devices. Pointer events handle both mouse and touch seamlessly.

---

## Ensuring Accessibility

Accessibility compliance is verified using:
- [`accessibility-checker`](https://www.npmjs.com/package/accessibility-checker) — for automated WCAG/Section 508 checks
- [`axe-core`](https://www.npmjs.com/package/axe-core) — for DOM-based accessibility rule validation

These tools are used during automated testing of the component. You can run them against your own pages to verify integration-level compliance.

---

## Best Practices

- Always provide a visible label or heading (e.g., `<h4>Sign here</h4>`) near the signature canvas so keyboard and screen reader users understand the context.
- Do not rely on color alone to communicate instructions — use text labels alongside color-coded controls.
- Ensure sufficient color contrast between `strokeColor` and `backgroundColor` (minimum 3:1 ratio for large UI elements).
- When integrating with a toolbar, make sure toolbar buttons are keyboard-focusable and have descriptive `tooltipText` values.
