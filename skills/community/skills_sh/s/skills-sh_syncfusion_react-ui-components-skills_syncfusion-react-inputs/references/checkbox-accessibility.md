# Accessibility — Syncfusion React CheckBox

## Table of Contents
- [Compliance Overview](#compliance-overview)
- [WAI-ARIA Attributes](#wai-aria-attributes)
- [Keyboard Interaction](#keyboard-interaction)
- [Right-to-Left (RTL) Support](#right-to-left-rtl-support)
- [Ensuring Accessibility in Your App](#ensuring-accessibility-in-your-app)

---

## Compliance Overview

The Syncfusion React CheckBox component is built to meet major accessibility standards:

| Accessibility Criteria | Support |
|---|---|
| WCAG 2.2 | ✅ Full |
| Section 508 | ✅ Full |
| Screen Reader Support | ✅ Full |
| Right-To-Left Support | ✅ Full |
| Color Contrast | ✅ Full |
| Mobile Device Support | ✅ Full |
| Keyboard Navigation | ✅ Full |
| Accessibility Checker Validation | ✅ Full |
| Axe-core Validation | ✅ Full |

The component follows [WAI-ARIA CheckBox patterns](https://www.w3.org/WAI/ARIA/apg/patterns/checkbox/).

---

## WAI-ARIA Attributes

| Attribute | Purpose |
|---|---|
| `aria-disabled` | Indicates the CheckBox is perceived but disabled — not editable or operable. Applied automatically when `disabled={true}`. |

The CheckBox renders as a native `<input type="checkbox">` element, which provides built-in `role="checkbox"` semantics for screen readers. No additional ARIA role configuration is needed.

---

## Keyboard Interaction

The CheckBox follows the [WAI-ARIA keyboard interaction guidelines](https://www.w3.org/WAI/ARIA/apg/patterns/checkbox/#keyboardinteraction):

| Key | Action |
|-----|--------|
| `Space` | Toggles the checkbox between checked and unchecked when focused |

The checkbox receives focus via standard `Tab` navigation. Focus indicators are visible and meet WCAG contrast requirements.

---

## Right-to-Left (RTL) Support

Enable RTL rendering for languages using right-to-left scripts (Arabic, Hebrew, etc.) by setting `enableRtl={true}`:

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

enableRipple(true);

function App() {
  return (
    <ul>
      <li><CheckBoxComponent label="Default RTL" enableRtl={true} /></li>
      <li><CheckBoxComponent label="Checked RTL" checked={true} enableRtl={true} /></li>
    </ul>
  );
}
export default App;
```

When `enableRtl={true}`:
- The checkbox frame and label flip to right-to-left orientation
- Works in combination with `labelPosition` for full layout control

**Property:** `enableRtl` — `boolean`, defaults to `false`

---

## State Persistence

Use `enablePersistence={true}` to save and restore the checkbox state across page reloads (stored in `localStorage`):

```tsx
<CheckBoxComponent
  label="Remember my preference"
  enablePersistence={true}
/>
```

**Property:** `enablePersistence` — `boolean`, defaults to `false`

---

## Locale

Override the global locale for this component using the `locale` property:

```tsx
<CheckBoxComponent label="Option" locale="fr-FR" />
```

**Property:** `locale` — `string`, defaults to `''` (inherits global culture `'en-US'`)

---

## Ensuring Accessibility in Your App

- Always provide a meaningful `label` — avoid rendering checkboxes without descriptive text
- Use `disabled={true}` instead of hiding checkboxes to communicate non-availability to assistive technologies
- Test with keyboard-only navigation to confirm focus and toggle behavior
- Run accessibility audits using tools like [axe-core](https://www.npmjs.com/package/axe-core) or [accessibility-checker](https://www.npmjs.com/package/accessibility-checker)
- For indeterminate state, communicate the meaning in surrounding UI (e.g., "Some items selected")
