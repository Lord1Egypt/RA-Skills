# Accessibility — Syncfusion React Tooltip

## Table of Contents
- [Compliance Overview](#compliance-overview)
- [WAI-ARIA Attributes](#wai-aria-attributes)
- [Keyboard Interaction](#keyboard-interaction)
- [Screen Reader Behavior](#screen-reader-behavior)
- [Focus Management](#focus-management)
- [Ensuring Accessibility](#ensuring-accessibility)

---

## Compliance Overview

The Syncfusion React Tooltip component meets the following accessibility standards:

| Accessibility Criteria | Support |
|------------------------|---------|
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | ✅ Full |
| [Section 508](https://www.section508.gov/) | ✅ Full |
| Screen Reader Support | ✅ Full |
| Right-To-Left Support | ✅ Full |
| Color Contrast | ✅ Full |
| Mobile Device Support | ✅ Full |
| Keyboard Navigation | ✅ Full |
| Accessibility Checker Validation | ✅ Full |
| axe-core Validation | ✅ Full |

---

## WAI-ARIA Attributes

The Tooltip follows [WAI-ARIA tooltip pattern](https://www.w3.org/WAI/ARIA/apg/patterns/tooltip/):

| Attribute | Element | Description |
|-----------|---------|-------------|
| `role="tooltip"` | Tooltip popup container | Identifies the element as a tooltip to assistive technologies |
| `aria-describedby` | Target element | Set to the tooltip's generated `id` when the tooltip opens; removed when it closes |
| `aria-hidden` | Tooltip popup | `"true"` when tooltip is hidden; `"false"` when visible |

**Multiple aria-describedby values:**
If the target already has an `aria-describedby` attribute, the tooltip appends its own `id` separated by a space:

```html
<!-- Before tooltip opens -->
<button aria-describedby="my-text">Click me</button>

<!-- After tooltip opens -->
<button aria-describedby="my-text my-tooltip">Click me</button>
```

This preserves existing accessibility relationships while adding the tooltip association.

---

## Keyboard Interaction

| Key | Action |
|-----|--------|
| `Escape` | Closes/dismisses the tooltip |
| `Tab` | Moves focus to the target element → tooltip opens; focus leaves → tooltip closes |

**Rules governing focus-based tooltips:**
- When the tooltip opens because the target received focus, the tooltip closes only when focus moves **away** from the target — not on any intermediate actions.
- When the tooltip opens on mouse hover, it closes only when the mouse **leaves** the target.
- When the tooltip opens on click, it closes only on another click action.

---

## Screen Reader Behavior

When a screen reader user tabs to a target element:
1. The screen reader announces the element's accessible name.
2. The tooltip opens (if `opensOn` includes `Focus` or `Auto`).
3. The `aria-describedby` association causes the screen reader to announce the tooltip content as a description.
4. Focus remains on the target element — the tooltip element itself is not focusable.
5. When focus leaves, the tooltip closes and `aria-describedby` is removed.

---

## Focus Management

The Syncfusion Tooltip is designed to not steal focus:
- The tooltip popup is never in the focus ring.
- Keyboard users navigate as normal; tooltips open/close based on focus events.
- Sticky mode (`isSticky={true}`) does not trap focus — the close icon is reachable by assistive technologies via `aria-hidden="false"` state.

**Accessible tooltip with Focus open mode:**
```tsx
<TooltipComponent
  content="This field requires a valid email address"
  opensOn="Focus"
  target="#emailInput"
  position="RightCenter"
>
  <div>
    <label htmlFor="emailInput">Email</label>
    <input
      id="emailInput"
      type="email"
      aria-label="Email address"
    />
  </div>
</TooltipComponent>
```

---

## Ensuring Accessibility

**Do:**
- Provide meaningful `content` text — avoid icons-only content without text alternatives.
- Use `opensOn="Focus"` or `opensOn="Auto"` for form field hints so keyboard users receive the same information as mouse users.
- Ensure sufficient color contrast between tooltip text and background when using `cssClass` overrides.
- Test with screen readers (NVDA, VoiceOver, JAWS) and keyboard-only navigation.

**Avoid:**
- Putting interactive content (links, buttons) inside non-sticky tooltips — users relying on keyboard navigation cannot reach them.
- Using tooltips as the **only** means to convey critical information — always provide an accessible alternative.
- Disabling `enableHtmlSanitizer` unless content is fully trusted.

**Verify with tools:**
- [axe-core](https://www.npmjs.com/package/axe-core) browser extension
- [accessibility-checker](https://www.npmjs.com/package/accessibility-checker)
- Live sample: https://ej2.syncfusion.com/accessibility/tooltip.html

---

## See Also
- [Customization](customization.md) — `enableRtl` for RTL language support
- [Open Mode](open-mode.md) — `opensOn="Focus"` for keyboard-accessible tooltips
- [API Reference](api.md) — `enableRtl`, `htmlAttributes`, `enableHtmlSanitizer`
