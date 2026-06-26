# Toast Accessibility

The Syncfusion React Toast component meets WCAG 2.2, Section 508, and ADA standards. Toasts function as live regions so screen readers announce new notifications automatically without requiring focus.

## Compliance Summary

| Accessibility Criteria | Support |
|---|---|
| WCAG 2.2 | ✅ Full |
| Section 508 | ✅ Full |
| Screen Reader (JAWS, NVDA, VoiceOver) | ✅ Full |
| Right-to-Left (RTL) | ✅ Full |
| Color Contrast | ✅ Full |
| Mobile Device | ✅ Full |
| Keyboard Navigation | Not Applicable* |
| Accessibility Checker Validation | ✅ Full |
| Axe-core Validation | ✅ Full |

> *Toast is a passive notification component — keyboard navigation is not applicable because toasts do not require interaction. Action buttons within toasts are keyboard-accessible via standard button focus.

---

## WAI-ARIA Attributes

The Toast implements the [WAI-ARIA Alert pattern](https://www.w3.org/WAI/ARIA/apg/patterns/alert/):

| Attribute | Value | Purpose |
|---|---|---|
| `role` | `"alert"` | Identifies the element as an urgent live region |
| `aria-live` | `"assertive"` | Announces toast content immediately, interrupting other screen reader speech |
| `aria-label` | descriptive string | Provides an accessible name for the toast region |

These attributes are applied automatically by the component — no manual ARIA setup required.

---

## Screen Reader Behavior

When a toast appears:
- Screen readers (JAWS, NVDA, VoiceOver) announce the toast content immediately via the `aria-live="assertive"` region
- Users do not need to focus the toast — announcement is automatic
- Action button labels are read when the button receives focus

---

## RTL Support

Enable right-to-left text direction with `enableRtl`:

```tsx
<ToastComponent
  ref={toast => toastInstance = toast!}
  title="إشعار"
  content="لديك رسالة جديدة"
  enableRtl={true}
  position={{ X: 'Left', Y: 'Bottom' }}
  created={() => toastInstance.show()}
/>
```

RTL affects text direction, icon placement, progress bar direction, and layout alignment. When using RTL, consider changing `position.X` to `'Left'` so the toast appears on the right side of an RTL layout.

---

## Accessibility Best Practices

**Timeout duration:**
Give users enough time to read toast content. For users with cognitive or vision disabilities, consider:
- Increasing `timeOut` beyond 5000ms for text-heavy toasts
- Using `extendedTimeout` so toasts remain while the user hovers/focuses
- Offering `showCloseButton={true}` so users can dismiss at their own pace

**Color contrast:**
The built-in semantic classes (`e-toast-success`, `e-toast-info`, `e-toast-warning`, `e-toast-danger`) are tested for WCAG color contrast compliance. When overriding colors with custom CSS, verify contrast ratios meet WCAG AA (4.5:1 for normal text, 3:1 for large text).

**Audio notifications:**
When adding audio cues (see [toast-services.md](./toast-services.md)), always include the toast text content as an alternative for users with hearing disabilities.

**Reduced motion:**
Respect the `prefers-reduced-motion` media query for users who are sensitive to animations:

```css
@media (prefers-reduced-motion: reduce) {
  .e-toast-container .e-toast {
    animation-duration: 0ms !important;
    transition-duration: 0ms !important;
  }
}
```

## See Also

- [Animation](./animation.md) — reduced motion in animations
- [Configuration](./configuration.md) — `showCloseButton`, `timeOut`
- [API reference](./api.md) — `enableRtl`, `enableHtmlSanitizer`
