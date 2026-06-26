# Accessibility in Syncfusion React Mention

## Overview

The Syncfusion React Mention component is built with full accessibility support. It complies with:

- **WCAG 2.2** (Web Content Accessibility Guidelines)
- **Section 508** (US Federal accessibility standard)
- **ADA** (Americans with Disabilities Act)
- **WAI-ARIA** patterns for combobox-style widgets

## WAI-ARIA Attributes

The Mention component automatically applies the following ARIA attributes:

| Attribute | Purpose |
|-----------|---------|
| `aria-selected` | Marks the currently selected suggestion item |
| `aria-activedescendent` | Points to the ID of the currently focused list item descendant |
| `aria-owns` | Connects the input to its popup list as a child element |

These attributes are managed automatically—no manual ARIA setup is required.

## Keyboard Navigation

Users can navigate the Mention popup entirely by keyboard:

| Key | Action |
|-----|--------|
| `↓` Arrow Down | Select the first item, or move to the next item |
| `↑` Arrow Up | Move to the previous item |
| `Escape` | Close the popup without selecting |
| `Enter` | Select the focused item and close popup |
| `Tab` | If popup is open: insert selected item and close popup. If closed: move focus to the next focusable element |

## Accessibility Compliance

| Criteria | Status |
|----------|--------|
| WCAG 2.2 Support | Full |
| Section 508 Support | Full |
| Screen Reader Support | Full |
| Right-To-Left Support | Full |
| Color Contrast | Full |
| Mobile Device Support | Full |
| Keyboard Navigation | Full |

## Example with Keyboard-Accessible Setup

```tsx
import { MentionComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

function App() {
  const mentionTarget: string = '#mentionElement';
  const userData: { [key: string]: Object }[] = [
    { Name: 'Andrew Fuller', ID: '1' },
    { Name: 'Anne Dodsworth', ID: '2' },
    { Name: 'Janet Leverling', ID: '3' },
    { Name: 'Laura Callahan', ID: '4' },
    { Name: 'Margaret Peacock', ID: '5' },
  ];
  const fields: Object = { text: 'Name' };

  return (
    <div id="mention_default">
      <table>
        <tr>
          <td>
            <label id="comment">Comments</label>
            <div
              id="mentionElement"
              placeholder="Type @ and tag user"
              role="textbox"
              aria-label="Comment input"
            ></div>
          </td>
        </tr>
      </table>
      <MentionComponent
        target={mentionTarget}
        dataSource={userData}
        fields={fields}
      />
    </div>
  );
}

export default App;
```

## RTL Support

Enable right-to-left layout with `enableRtl`:

```tsx
<MentionComponent
  target={mentionTarget}
  dataSource={userData}
  fields={fields}
  enableRtl={true}
/>
```

## State Persistence

Enable component state persistence across page reloads with `enablePersistence`:

```tsx
<MentionComponent
  target={mentionTarget}
  dataSource={userData}
  fields={fields}
  enablePersistence={true}
/>
```

## Gotchas

- The `target` element should have meaningful labels (e.g., `<label>` associated with the editable div, or an `aria-label`) so screen readers can describe it.
- The Mention popup uses ARIA roles compatible with the combobox pattern—screen readers will announce suggestions as the user navigates.
- Color contrast and focus indicators meet WCAG 2.2 AA standards in all built-in Syncfusion themes.
