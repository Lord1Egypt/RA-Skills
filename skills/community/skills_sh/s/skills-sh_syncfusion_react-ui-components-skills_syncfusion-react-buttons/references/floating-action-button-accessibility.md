# Accessibility – Syncfusion React Floating Action Button

## Table of Contents
- [Compliance Overview](#compliance-overview)
- [WAI-ARIA Attributes](#wai-aria-attributes)
- [Keyboard Navigation](#keyboard-navigation)
- [Right-to-Left Support](#right-to-left-support)
- [Screen Reader Guidance](#screen-reader-guidance)
- [Ensuring Accessibility](#ensuring-accessibility)

---

## Compliance Overview

The Syncfusion React Floating Action Button meets the following accessibility standards:

| Accessibility Criteria | Support |
|------------------------|---------|
| WCAG 2.2 | ✅ Full |
| Section 508 | ✅ Full |
| Screen Reader Support | ✅ Full |
| Right-To-Left (RTL) | ✅ Full |
| Color Contrast | ✅ Full |
| Mobile Device Support | ✅ Full |
| Keyboard Navigation | ✅ Full |
| Accessibility Checker Validation | ✅ Full |
| axe-core Validation | ✅ Full |

---

## WAI-ARIA Attributes

The FAB implements [WAI-ARIA button patterns](https://www.w3.org/WAI/ARIA/apg/patterns/button/):

| Attribute | Purpose |
|-----------|---------|
| `aria-label` | Provides an accessible name for icon-only FABs—essential for screen reader users who cannot see the icon |
| `aria-disabled` | Communicates the disabled state to assistive technologies when `disabled={true}` |
| `role="button"` | Defines the semantic button role so assistive technologies announce the element correctly |

**Icon-only FAB accessibility best practice:**

For FABs that have no visible text (`content` is not set), add an `aria-label` directly via `htmlAttributes` or ensure the icon font includes an accessible label. Without this, screen readers may announce only a generic "button":

```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  return (
    <div>
      <div id="target" style={{ position: 'relative', minHeight: '300px' }}></div>
      {/* aria-label ensures screen readers announce "Add new item" */}
      <FabComponent
        id="fab"
        iconCss="e-icons e-plus"
        target="#target"
        content="Add new item"
      />
    </div>
  );
}
export default App;
```

**Disabled FAB:**

```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  return (
    <div>
      <div id="target" style={{ position: 'relative', minHeight: '300px' }}></div>
      {/* aria-disabled="true" is set automatically when disabled={true} */}
      <FabComponent id="fab" iconCss="e-icons e-edit" content="Edit" disabled={true} target="#target" />
    </div>
  );
}
export default App;
```

---

## Keyboard Navigation

The FAB follows [WAI-ARIA keyboard interaction guidelines](https://www.w3.org/WAI/ARIA/apg/patterns/button/#keyboardinteraction):

| Key | Action |
|-----|--------|
| `Enter` | Activates the FAB when it has focus |
| `Space` | Activates the FAB when it has focus |
| `Tab` | Moves focus to the next focusable element |
| `Shift + Tab` | Moves focus to the previous focusable element |
| `Escape` | Closes any open tooltip or popup associated with the FAB |

No additional configuration is required—keyboard navigation is built in.

---

## Right-to-Left Support

Enable RTL layout using the `enableRtl` prop. This mirrors the FAB's icon and text placement for right-to-left languages:

```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  return (
    <div>
      <div id="target" style={{ position: 'relative', minHeight: '350px' }}></div>
      <FabComponent
        id="fab"
        iconCss="e-icons e-edit"
        content="تحرير"
        enableRtl={true}
        target="#target"
      />
    </div>
  );
}
export default App;
```

---

## Screen Reader Guidance

- **Icon-only FABs:** Always provide a `content` to give the FAB a meaningful label. Screen readers rely on text to announce interactive elements.
- **Predefined styles** (`e-danger`, `e-warning`, etc.) are visual-only—use the `content` prop to convey semantic meaning in text.
- **Disabled state:** The `aria-disabled` attribute is automatically applied when `disabled={true}` is set.

---

## Ensuring Accessibility

Validate FAB accessibility using the following tools:

- [`accessibility-checker`](https://www.npmjs.com/package/accessibility-checker) – automated accessibility testing
- [`axe-core`](https://www.npmjs.com/package/axe-core) – accessibility rules engine

Both tools are used by Syncfusion during automated testing of the FAB component.
