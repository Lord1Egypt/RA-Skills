---
name: accessibility
description: 'Accessibility in React TreeGrid - WCAG 2.1 Level AA compliance, keyboard navigation, ARIA attributes, screen reader support, RTL, and localization.'
---

# Accessibility

## Table of Contents
- [WCAG 2.1 Compliance](#wcag-21-compliance)
- [Keyboard Navigation](#keyboard-navigation)
- [ARIA Support](#aria-support)
- [Screen Reader Support](#screen-reader-support)

The Syncfusion React TreeGrid is built with WCAG 2.1 Level AA accessibility standards and provides comprehensive keyboard navigation, ARIA support, and screen reader compatibility.

## WCAG 2.1 Compliance

TreeGrid adheres to Web Content Accessibility Guidelines (WCAG) 2.1 Level AA, ensuring:

- **Perceivable**: Content is visible and distinguishable
- **Operable**: Fully keyboard navigable
- **Understandable**: Clear labels and predictable behavior
- **Robust**: Compatible with assistive technologies

## Keyboard Navigation

TreeGrid provides complete keyboard accessibility without requiring mouse interaction.

### Navigation Keys

**Arrow Keys - Navigation**
```
→ Left/Right: Move between columns (cell selection)
↑ Down: Move between rows
Ctrl + Home: Go to first cell
Ctrl + End: Go to last cell
```

**Page Navigation**
```
Page Up: Move up by visible rows
Page Down: Move down by visible rows
Tab: Move to next focusable element
Shift + Tab: Move to previous focusable element
```

**Expand/Collapse**
```
Right (→): Expand parent row (when focused on tree column)
Left (←): Collapse parent row (when focused on tree column)
Space: Toggle expand/collapse for tree row
```

### Editing Shortcuts

**Cell Editing**
```
F2 or Double-click: Start cell editing
Enter: Save and move to next row
Tab: Save and move to next cell
Shift + Tab: Save and move to previous cell
Escape: Cancel editing
```

**Row Editing**
```
F2: Start row editing
Enter: Save row
Escape: Cancel editing
```

**Batch Editing**
```
Tab: Move to next cell and start editing
Shift + Tab: Move to previous cell
Escape: Cancel current edit
```

### Selection Shortcuts

**Row Selection**
```
Space: Select/deselect current row
Ctrl + Space: Toggle selection for current row
Ctrl + A: Select all rows
Ctrl + Home then Ctrl + Shift + End: Select from first to last
```

**Cell Selection**
```
Space: Select/deselect current cell
Ctrl + C: Copy selected cell content
Ctrl + V: Paste content (if editing enabled)
```

### TreeGrid-Specific Keys

**Hierarchy Navigation**
```
When focus on tree column with expand/collapse icon:
→ Right: Expand children
← Left: Collapse children
↓ Down: Move to first child (if expanded)
↑ Up: Move to parent row
```

### Filtering & Searching

**Filter Interaction**
```
Ctrl + F: Open search box
Enter: Execute search
Escape: Close search
```

**Filter Menu**
```
Alt + Down: Open filter menu
Arrow keys: Navigate filter options
Enter: Apply filter
Escape: Close menu
```

## ARIA Attributes

TreeGrid automatically includes proper ARIA markup for screen readers:

### Grid Structure
```tsx
<div role="grid" aria-label="Data Table">
  <div role="row" aria-level="1">
    <div role="gridcell">Cell Content</div>
  </div>
</div>
```

**Automatic ARIA for TreeGrid:**

- `role="grid"` - Identifies the component as a data grid
- `role="row"` - Each row in the grid
- `role="gridcell"` - Each cell in a row
- `role="columnheader"` - Column header cells
- `aria-rowindex` - Current row position
- `aria-colindex` - Current column position
- `aria-colcount` - Total number of columns
- `aria-rowcount` - Total number of rows
- `aria-expanded` - For tree rows (true/false/undefined)
- `aria-level` - Hierarchy level in tree
- `aria-selected` - For selected rows/cells
- `aria-label` - Column headers and buttons
- `aria-describedby` - Links cells to column descriptions

### Expanded/Collapsed State

TreeGrid automatically updates ARIA attributes for expand/collapse:

```tsx
// Parent row when expanded
<div role="row" aria-expanded="true" aria-level="1">

// Parent row when collapsed
<div role="row" aria-expanded="false" aria-level="1">

// Child rows (automatically marked as children)
<div role="row" aria-level="2" />
<div role="row" aria-level="3" />
```

### Selection ARIA

```tsx
// Row selection
<div role="row" aria-selected="true">

// Cell selection
<div role="gridcell" aria-selected="true">
```

### Edit Mode ARIA

During cell/row editing:
```tsx
<input aria-label="Task Name" aria-required="true" />
```

## Screen Reader Support

TreeGrid works with popular screen readers:

- **NVDA** - Full support
- **JAWS** - Full support
- **VoiceOver** - Full support

### Screen Reader Announcements

**Grid Navigation**
- "Row 1, Column Name, contains Task ID"
- "Expanded, Level 1"
- "1 of 100 rows"

**Row Operations**
- "Expanding row"
- "Collapsing row"
- "Row selected"
- "3 rows selected"

**Editing**
- "Edit mode, Press Enter to save or Escape to cancel"
- "Cell validation failed"

## Globalization & Localization

**RTL Support** - Full right-to-left language support:

```tsx
<TreeGridComponent enableRtl={true}>
  {/* Grid rendered RTL */}
</TreeGridComponent>
```

**Localization** - Translated UI strings for:
- Proper text direction for each language
- Culturally appropriate formatting

```tsx
import { L10n } from '@syncfusion/ej2-base';

L10n.load({
  'es': {
    'treegrid': {
      'Add': 'Añadir',
      'Edit': 'Editar'
    }
  }
});
```