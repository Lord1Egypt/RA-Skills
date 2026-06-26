# Accessibility — Syncfusion React Button

## Table of Contents
1. [Compliance Summary](#compliance-summary)
2. [WAI-ARIA Attributes](#wai-aria-attributes)
3. [Keyboard Interaction](#keyboard-interaction)
4. [Ensuring Accessibility in Your Implementation](#ensuring-accessibility-in-your-implementation)

---

## Compliance Summary

The Syncfusion `ButtonComponent` fully adheres to the following accessibility standards:

| Accessibility Criteria | Support |
|---|---|
| WCAG 2.2 | Full support |
| Section 508 | Full support |
| Screen Reader | Full support |
| Right-To-Left (RTL) | Full support |
| Color Contrast | Full support |
| Mobile Device | Full support |
| Keyboard Navigation | Full support |
| Accessibility Checker (IBM) | Validated |
| axe-core | Validated |

---

## WAI-ARIA Attributes

The `ButtonComponent` follows the [WAI-ARIA Button Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/button/).

| Attribute | Purpose |
|---|---|
| `aria-label` | Provides an accessible name for icon-only buttons that lack visible text |

**Icon-only button — always add `aria-label`:**

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

enableRipple(true);

function App() {
  return (
    <div>
      {/* Icon-only: no visible text — aria-label is required */}
      <ButtonComponent
        cssClass='e-round'
        iconCss='e-icons e-search'
        aria-label='Search'
      />

      {/* Button with text — aria-label is optional; text acts as the accessible name */}
      <ButtonComponent cssClass='e-primary'>
        Save
      </ButtonComponent>
    </div>
  );
}
export default App;
```

> Predefined button styles (e.g., `e-danger`, `e-success`) convey meaning visually only. Rely on descriptive button text or `aria-label` — not color alone — for accessibility.

---

## Keyboard Interaction

The `ButtonComponent` follows the [WAI-ARIA keyboard interaction guidelines](https://www.w3.org/WAI/ARIA/apg/patterns/button/#keyboardinteraction):

| Key | Action |
|---|---|
| `Space` | When the button has focus, triggers the click action and (for toggle buttons) changes the state |
| `Enter` | Activates the button (standard browser behavior for `<button>` elements) |
| `Tab` | Moves focus to the next focusable element |
| `Shift+Tab` | Moves focus to the previous focusable element |

> Ensure disabled buttons use `disabled={true}` (not just visual styling) so they are correctly excluded from the tab order.

---

## Ensuring Accessibility in Your Implementation

Follow these best practices when using `ButtonComponent`:

1. **Always label icon-only buttons.** If a button has no visible text (e.g., a round icon button), pass `aria-label` describing the action:
   ```tsx
   <ButtonComponent cssClass='e-round' iconCss='e-icons e-edit' aria-label='Edit record' />
   ```

2. **Use meaningful button text.** Predefined styles like `e-danger` are visual cues only — screen readers announce the text content, not the style. Use text like "Delete" rather than "Button".

3. **Manage disabled state correctly.** Use the `disabled` prop so the browser excludes the button from the focus order and announces it as unavailable:
   ```tsx
   <ButtonComponent disabled={true}>Submit</ButtonComponent>
   ```

4. **Avoid relying on color alone.** Always combine color styles with descriptive text or icons. For example, a "danger" delete button should say "Delete" — not just be red.

5. **Validate with tooling.** Test your implementation with:
   - [IBM Accessibility Checker](https://www.npmjs.com/package/accessibility-checker)
   - [axe-core](https://www.npmjs.com/package/axe-core)
   - Browser developer tools accessibility panel
   - A screen reader (NVDA, JAWS, VoiceOver)
