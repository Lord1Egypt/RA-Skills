# Accessibility in React Message

The Syncfusion Message component is built to full accessibility compliance, meeting WCAG 2.2, Section 508, and ADA standards. It is validated using `accessibility-checker` and `axe-core` in continuous testing.

## Compliance Summary

| Accessibility Criteria | Compliance |
|------------------------|------------|
| WCAG 2.2 | Full |
| Section 508 | Full |
| Screen Reader Support | Full |
| Right-To-Left Support | Full |
| Color Contrast | Full |
| Mobile Device Support | Full |
| Keyboard Navigation | Full |
| accessibility-checker Validation | Full |
| axe-core Validation | Full |

## WAI-ARIA Attributes

The Message component implements the [WAI-ARIA alert pattern](https://www.w3.org/WAI/ARIA/apg/patterns/alert/):

| Attribute | Applied To | Purpose |
|-----------|-----------|---------|
| `role="alert"` | Message root element | Announces the message to screen readers immediately on render |
| `aria-label` | Close icon button | Provides an accessible name for the close icon for screen readers |

The `role="alert"` attribute causes screen readers to announce the message content as soon as it appears in the DOM — making it critical for dynamic notifications.

## Keyboard Navigation

Users who rely on keyboard navigation can interact with the close icon:

| Key | Action |
|-----|--------|
| `Tab` / `Shift+Tab` | Move focus to the close icon in the message |
| `Enter` / `Space` | Close the focused message (fires the `closed` event) |

Note: Keyboard interaction applies only when `showCloseIcon={true}`. Messages without a close icon are purely informational and require no keyboard interaction.

## Implementation Notes

### Dismissible Messages

When `showCloseIcon={true}`, the close icon is a focusable button with an `aria-label`. Ensure your `closed` handler updates state to reflect dismissal:

```tsx
import { useState } from 'react';
import { MessageComponent } from '@syncfusion/ej2-react-notifications';

function AccessibleMessage() {
  const [visible, setVisible] = useState(true);

  return (
    <MessageComponent
      content="Your session will expire in 5 minutes"
      severity="Warning"
      showCloseIcon={true}
      visible={visible}
      closed={() => setVisible(false)}
    />
  );
}
```

### Dynamic Messages

Because the Message component uses `role="alert"`, screen readers will automatically announce newly rendered messages. If you're conditionally rendering messages based on user actions (e.g., form submission), the announcement happens without additional ARIA management:

```tsx
{submitError && (
  <MessageComponent
    content="A problem occurred while submitting your data"
    severity="Error"
  />
)}
```

### Color Contrast

All severity color combinations (Normal, Info, Success, Warning, Error) across all variants (Text, Outlined, Filled) meet WCAG 2.2 color contrast requirements for both text and icons.

### RTL Support

Enable right-to-left layout for RTL languages to ensure proper visual ordering for screen readers operating in RTL mode:

```tsx
<MessageComponent content="رسالة تحذير" severity="Warning" enableRtl={true} />
```
