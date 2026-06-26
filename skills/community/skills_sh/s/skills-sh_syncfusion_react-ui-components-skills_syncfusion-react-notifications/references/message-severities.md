# Message Severity Levels

Severity communicates the importance and type of information in a message. The Message component uses the `severity` prop to apply distinct icons and color schemes that help users quickly understand the message context.

## Available Severity Levels

| Severity | Value | Use Case |
|----------|-------|----------|
| Normal | `"Normal"` (default) | General information, neutral messages |
| Info | `"Info"` | Informational content, tips, guidance |
| Success | `"Success"` | Confirmation, completed operations, positive outcomes |
| Warning | `"Warning"` | Caution, potential issues, non-critical problems |
| Error | `"Error"` | Critical failures, invalid input, system errors |

## Basic Usage

Set the `severity` prop to one of the five values. When omitted, `Normal` is used:

```tsx
import { MessageComponent } from '@syncfusion/ej2-react-notifications';

function App() {
  return (
    <div>
      <MessageComponent content="Editing is restricted" />
      <MessageComponent content="Please read the comments carefully" severity="Info" />
      <MessageComponent content="Your message has been sent successfully" severity="Success" />
      <MessageComponent content="There was a problem with your network connection" severity="Warning" />
      <MessageComponent content="A problem occurred while submitting your data" severity="Error" />
    </div>
  );
}
```

## Choosing the Right Severity

- **Normal** — Neutral context that doesn't require action (e.g., a read-only notice).
- **Info** — Background information the user should know, but no action required (e.g., a tooltip-style note).
- **Success** — Confirm an action completed correctly (e.g., form submitted, file uploaded).
- **Warning** — Alert the user to something that may become a problem (e.g., session expiring soon, low disk space).
- **Error** — Signal a failure that needs immediate attention (e.g., validation failed, network unreachable).

## Combining Severity with Variant

Severity works independently of the `variant` prop. You can combine any severity with any variant:

```tsx
{/* Filled error — maximum visual emphasis */}
<MessageComponent content="A problem occurred" severity="Error" variant="Filled" />

{/* Outlined success — clear but not overwhelming */}
<MessageComponent content="Changes saved" severity="Success" variant="Outlined" />
```

See `variants.md` for full variant documentation.

## Dynamic Severity

Severity can be controlled dynamically via state:

```tsx
import { useState } from 'react';
import { MessageComponent } from '@syncfusion/ej2-react-notifications';

function StatusMessage({ status }: { status: 'success' | 'error' | 'info' }) {
  const severityMap = { success: 'Success', error: 'Error', info: 'Info' } as const;
  return (
    <MessageComponent
      content={`Status: ${status}`}
      severity={severityMap[status]}
    />
  );
}
```
