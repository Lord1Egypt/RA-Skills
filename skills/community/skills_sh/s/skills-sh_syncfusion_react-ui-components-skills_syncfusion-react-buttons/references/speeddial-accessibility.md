# Accessibility – Syncfusion React Speed Dial

## Table of Contents
- [Compliance Summary](#compliance-summary)
- [WAI-ARIA Attributes](#wai-aria-attributes)
- [Keyboard Navigation](#keyboard-navigation)
- [RTL Support](#rtl-support)
- [Ensuring Accessibility](#ensuring-accessibility)

---

## Compliance Summary

The Speed Dial component adheres to the following accessibility standards:

| Criterion | Support |
|-----------|---------|
| WCAG 2.2 | ✅ Full |
| Section 508 | ✅ Full |
| Screen Reader | ✅ Full |
| Right-To-Left (RTL) | ✅ Full |
| Color Contrast | ✅ Full |
| Mobile Device | ✅ Full |
| Keyboard Navigation | ✅ Full |
| Accessibility Checker Validation | ✅ Full |
| Axe-core Accessibility Validation | ✅ Full |

---

## WAI-ARIA Attributes

The Speed Dial follows [WAI-ARIA menubar patterns](https://www.w3.org/WAI/ARIA/apg/patterns/menubar/):

| Attribute | Purpose |
|-----------|---------|
| `role="menu"` | Defines the popup container as a menu |
| `role="menuitem"` | Defines each action item as a menu item |
| `aria-label` | Provides an accessible name for the button or items |
| `aria-expanded` | `true` when popup is open, `false` when closed |
| `aria-haspopup` | Indicates the button has an associated popup |
| `aria-controls` | References the popup element controlled by the button |
| `aria-disabled` | Marks individual items as disabled when applicable |

These attributes are applied automatically by the component—no manual configuration needed.

---

## Keyboard Navigation

The Speed Dial supports the following keyboard shortcuts:

| Key | Action |
|-----|--------|
| `Enter` | Opens or closes the popup |
| `Space` | Opens or closes the popup |
| `Up Arrow` | Moves focus to the previous action item |
| `Down Arrow` | Moves focus to the next action item |
| `Left Arrow` | Moves focus to the previous action item |
| `Right Arrow` | Moves focus to the next action item |
| `Home` | Moves focus to the first action item |
| `End` | Moves focus to the last action item |
| `Escape` | Closes the popup |

---

## RTL Support

Enable right-to-left layout by setting `enableRtl={true}`. This mirrors the component's visual layout for RTL languages:

```tsx
import { SpeedDialComponent, SpeedDialItemModel } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  const items: SpeedDialItemModel[] = [
    { text: 'Cut', iconCss: 'e-icons e-cut' },
    { text: 'Copy', iconCss: 'e-icons e-copy' },
    { text: 'Paste', iconCss: 'e-icons e-paste' }
  ];

  return (
    <SpeedDialComponent id='speeddial' items={items} content='Edit'
      enableRtl={true} target="#targetElement" />
  );
}
export default App;
```

---

## Ensuring Accessibility

Accessibility compliance is verified during automated testing using:
- [accessibility-checker](https://www.npmjs.com/package/accessibility-checker)
- [axe-core](https://www.npmjs.com/package/axe-core)

**Best practices for developers:**

1. Always provide meaningful `aria-label` on the Speed Dial button when icon-only (`openIconCss` without `content`)
2. Use `title` on icon-only items so screen readers can describe them
3. Ensure the `target` container has sufficient color contrast with the button
4. Test keyboard navigation by tabbing to the button and using arrow keys to navigate items
