# Accessibility in React Rating Component

## Table of Contents
- [Compliance Summary](#compliance-summary)
- [WAI-ARIA Attributes](#wai-aria-attributes)
- [Keyboard Navigation](#keyboard-navigation)
- [RTL Support](#rtl-support)
- [Ensuring Accessibility](#ensuring-accessibility)

---

## Compliance Summary

The Syncfusion React Rating component meets the following accessibility standards:

| Criteria | Status |
|----------|--------|
| WCAG 2.2 | ✅ Full support |
| Section 508 | ✅ Full support |
| ADA | ✅ Full support |
| Screen Reader Support | ✅ Full support |
| Right-To-Left (RTL) | ✅ Full support |
| Color Contrast | ✅ Full support |
| Mobile Device Support | ✅ Full support |
| Keyboard Navigation | ✅ Full support |
| Accessibility Checker Validation | ✅ Passed |
| Axe-core Validation | ✅ Passed |

---

## WAI-ARIA Attributes

The Rating component follows the [WAI-ARIA slider pattern](https://www.w3.org/WAI/ARIA/apg/patterns/slider/).

| Attribute | Purpose |
|-----------|---------|
| `role="slider"` | Identifies the input as a range slider |
| `role="button"` | Applied to the reset button |
| `aria-label` | Provides an accessible name for the rating |
| `aria-valuemin` | Defines the minimum rating value |
| `aria-valuemax` | Defines the maximum rating value |
| `aria-valuenow` | Reflects the current selected value |
| `aria-hidden` | Applied to the reset button when not interactive |

These are applied automatically — no manual ARIA configuration is needed.

---

## Keyboard Navigation

The Rating component supports full keyboard interaction following the [WAI-ARIA keyboard interaction guidelines](https://www.w3.org/WAI/ARIA/apg/patterns/slider/#keyboardinteraction):

| Key | Action |
|-----|--------|
| `Arrow Up` | Increases the rating value |
| `Arrow Right` | Increases the rating value (decreases in RTL mode) |
| `Arrow Down` | Decreases the rating value |
| `Arrow Left` | Decreases the rating value (increases in RTL mode) |
| `Space` | When the **reset button** is focused, resets to `min` value |

---

## RTL Support

Enable right-to-left layout using `enableRtl={true}`:

```tsx
import { RatingComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div className="wrap">
      <RatingComponent id="rating" value={3} enableRtl={true} />
    </div>
  );
}
export default App;
```

In RTL mode:
- Arrow Right **decreases** the value.
- Arrow Left **increases** the value.
- The component layout is mirrored.

---

## Ensuring Accessibility

Accessibility compliance is verified through automated tools:

- **[accessibility-checker](https://www.npmjs.com/package/accessibility-checker)** — automated WCAG/Section 508 validation.
- **[axe-core](https://www.npmjs.com/package/axe-core)** — browser-based accessibility testing.

The Rating component passes both tools without configuration. To evaluate compliance in your app, run these tools against the page containing the rating component.

---

## Tips

- Always provide a meaningful `aria-label` if the rating context isn't clear from surrounding text.
- Combine `showLabel={true}` with the rating to give screen reader users a text representation of the current value.
- Use `readOnly={true}` (not `disabled={true}`) for display-only ratings to keep them focusable and accessible.
