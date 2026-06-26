# Chip Accessibility

## Table of Contents
- [Standards Compliance](#standards-compliance)
- [WAI-ARIA Attributes](#wai-aria-attributes)
- [Keyboard Interaction](#keyboard-interaction)
- [Screen Reader Support](#screen-reader-support)
- [RTL Support](#rtl-support)
- [Color Contrast](#color-contrast)
- [Ensuring Accessibility](#ensuring-accessibility)

---

## Standards Compliance

The Syncfusion React Chips component is built to meet industry accessibility standards:

| Accessibility Criteria | Support |
|------------------------|---------|
| WCAG 2.2 | Full support |
| Section 508 | Full support |
| ADA | Full support |
| Screen Reader Support | Full support |
| Right-To-Left (RTL) | Full support |
| Color Contrast | Full support |
| Mobile Device Support | Full support |
| Keyboard Navigation | Full support |
| Accessibility Checker Validation | Full support |
| Axe-core Accessibility Validation | Full support |

---

## WAI-ARIA Attributes

The Chips component follows [WAI-ARIA](https://www.w3.org/WAI/ARIA/apg/patterns/) patterns. The following ARIA attributes are automatically applied:

| Attribute | Applied to | Purpose |
|-----------|-----------|---------|
| `role="listbox"` | `ChipListComponent` wrapper | Identifies the container as a listbox for assistive technologies |
| `role="option"` | Individual chips (multi-selection) | Marks selectable chips within the listbox |
| `role="button"` | Single chip used for actions | Identifies a chip that triggers an event |
| `aria-label` | Chip element | Provides an accessible name for the chip |
| `aria-selected` | Selectable chip | Indicates whether the chip is currently selected |
| `aria-disabled` | Disabled chip | Indicates the chip is visible but not operable |
| `aria-multiselectable` | `ChipListComponent` (Multiple mode) | Communicates that multiple chips can be selected |

### Example: Providing Custom aria-label

Use `htmlAttributes` to provide an explicit accessible name:

```tsx
import {
  ChipListComponent,
  ChipsDirective,
  ChipDirective
} from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  return (
    <ChipListComponent
      id="accessible-chips"
      selection="Multiple"
      htmlAttributes={{ 'aria-label': 'Filter by category' }}
    >
      <ChipsDirective>
        <ChipDirective text="React" htmlAttributes={{ 'aria-label': 'React framework' }} />
        <ChipDirective text="Angular" htmlAttributes={{ 'aria-label': 'Angular framework' }} />
        <ChipDirective text="Vue" htmlAttributes={{ 'aria-label': 'Vue framework' }} />
      </ChipsDirective>
    </ChipListComponent>
  );
}
export default App;
```

---

## Keyboard Interaction

The Chips component supports full keyboard navigation following [WAI-ARIA keyboard interaction guidelines](https://www.w3.org/WAI/ARIA/apg/patterns/button/#keyboardinteraction):

| Keyboard Shortcut | Action |
|-------------------|--------|
| `Tab` | Move focus to the chip list |
| `Arrow Left / Right` | Navigate between chips |
| `Enter` or `Space` | Select the focused chip (in Single or Multiple selection mode) |
| `Delete` or `Backspace` | Delete the focused chip (when `enableDelete={true}`) |

### Example: Keyboard-Accessible Deletable Chip List

```tsx
import {
  ChipListComponent,
  ChipsDirective,
  ChipDirective
} from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  return (
    <ChipListComponent
      id="keyboard-chips"
      enableDelete={true}
      selection="Multiple"
    >
      <ChipsDirective>
        <ChipDirective text="JavaScript" />
        <ChipDirective text="TypeScript" />
        <ChipDirective text="Python" />
        <ChipDirective text="Rust" />
      </ChipsDirective>
    </ChipListComponent>
  );
}
export default App;
```

- Keyboard users can navigate chips with arrow keys, select with Enter/Space, and delete with Delete/Backspace.

---

## Screen Reader Support

The Chips component works with popular screen readers (NVDA, JAWS, VoiceOver) because:

- The container is marked as `role="listbox"`.
- Each chip has `role="option"` or `role="button"` depending on context.
- `aria-selected` is updated dynamically when a chip is selected.
- `aria-disabled` is set for disabled chips.
- The `created` event fires when the component is fully initialized.

### Best Practice: Descriptive Labels

Use `htmlAttributes` to add `aria-label` to chips that don't have self-describing text:

```tsx
<ChipDirective
  avatarText="A"
  text="Andrew"
  htmlAttributes={{ 'aria-label': 'Andrew, team member' }}
/>
```

---

## RTL Support

Enable right-to-left rendering for Arabic, Hebrew, and other RTL languages:

```tsx
import {
  ChipListComponent,
  ChipsDirective,
  ChipDirective
} from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  return (
    <ChipListComponent id="rtl-chips" enableRtl={true}>
      <ChipsDirective>
        <ChipDirective text="مرحبا" />
        <ChipDirective text="العالم" />
        <ChipDirective text="React" />
      </ChipsDirective>
    </ChipListComponent>
  );
}
export default App;
```

- `enableRtl={true}` — flips the chip layout, icon positions, and text direction.

---

## Color Contrast

The Syncfusion themes (Material, Tailwind, Bootstrap, Fluent) are designed to meet WCAG 2.2 color contrast requirements (minimum 4.5:1 ratio for normal text).

When customizing chip colors via CSS, verify contrast ratios using tools such as:
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Colour Contrast Analyser](https://www.tpgi.com/color-contrast-checker/)

**Example of accessible custom selection color:**
```css
/* Ensure sufficient contrast on selected chip */
.e-chip-list.e-selection .e-chip.e-active {
  background-color: #1a56db; /* dark blue */
  color: #ffffff;             /* white text — passes AA */
}
```

---

## Ensuring Accessibility

The component's accessibility is validated using:
- [accessibility-checker](https://www.npmjs.com/package/accessibility-checker)
- [axe-core](https://www.npmjs.com/package/axe-core)

To validate your implementation:

```bash
# Run axe-core in your test suite
npm install axe-core --save-dev
```

```ts
import axe from 'axe-core';

axe.run(document.getElementById('chip-list')).then((results) => {
  if (results.violations.length) {
    console.error('Accessibility violations:', results.violations);
  }
});
```

You can also open the [Syncfusion Chips accessibility sample](https://ej2.syncfusion.com/accessibility/chips.html) to evaluate live compliance with accessibility tools.
