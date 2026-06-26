# Accessibility — React ProgressButton

## Overview

The `ProgressButtonComponent` adheres to accessibility standards including
[ADA](https://www.ada.gov/), [Section 508](https://www.section508.gov/),
[WCAG 2.2](https://www.w3.org/TR/WCAG22/), and [WAI-ARIA roles](https://www.w3.org/TR/wai-aria/#roles).

---

## Compliance Matrix

| Accessibility Criteria | Status |
|---|---|
| WCAG 2.2 Support | ✅ Full |
| Section 508 Support | ✅ Full |
| Screen Reader Support | ✅ Full |
| Right-To-Left (RTL) Support | ✅ Full |
| Color Contrast | ✅ Full |
| Mobile Device Support | ✅ Full |
| Keyboard Navigation Support | ✅ Full |
| Accessibility Checker Validation | ✅ Full |
| Axe-core Accessibility Validation | ✅ Full |

---

## WAI-ARIA Attributes

The ProgressButton implements the following ARIA attributes:

| Attribute | Purpose |
|---|---|
| `aria-label` | Accessible name for icon-only buttons; essential for screen readers |
| `aria-disabled` | Communicates the disabled state to assistive technologies |
| `aria-valuemin` | Minimum progress value (0) exposed to assistive technologies |
| `aria-valuemax` | Maximum progress value (100) exposed to assistive technologies |
| `aria-valuenow` | Current progress percentage communicated to screen readers |

---

## Keyboard Interaction

| Key | Action |
|---|---|
| `Enter` | Starts progress when the button has focus |
| `Space` | Starts progress when the button has focus |
| `Tab` | Moves focus to the next focusable element |
| `Shift + Tab` | Moves focus to the previous focusable element |
| `Escape` | Stops or cancels the current progress operation |

---

## RTL Support

Enable right-to-left rendering by setting the [`enableRtl`](api.md#enablertl--boolean) prop:

```tsx
<ProgressButtonComponent content="Progress" enableRtl={true} />
```

---

## Icon-only Accessible Button

When using an icon-only button (no visible text), provide an `aria-label` via `content` or
a wrapper `aria-label` attribute so screen readers can identify the button:

```tsx
<ProgressButtonComponent
  iconCss="e-icons e-upload"
  content=""
  cssClass="e-icon-btn"
  // Wrap in a div with aria-label if content is empty
/>
```

---

## Ensuring Accessibility

Validate with recommended tools:

- [accessibility-checker](https://www.npmjs.com/package/accessibility-checker) — automated audit
- [axe-core](https://www.npmjs.com/package/axe-core) — browser extension & CI integration

Live sample: https://ej2.syncfusion.com/accessibility/progress-button.html

---

## See Also

- [Accessibility in Syncfusion React components](https://ej2.syncfusion.com/react/documentation/common/accessibility)
- [API Reference](progressbutton-api.md)
