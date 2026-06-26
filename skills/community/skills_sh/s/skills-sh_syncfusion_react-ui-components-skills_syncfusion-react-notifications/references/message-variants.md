# Message Display Variants

Variants define the visual presentation style of the Message component. Three predefined variants are available, each offering a different design aesthetic. Configure the variant using the `variant` prop.

## Available Variants

| Variant | Value | Description |
|---------|-------|-------------|
| Text | `"Text"` (default) | Subtle styling — light background with colored text. Non-intrusive. |
| Outlined | `"Outlined"` | Colored border with matching text on a transparent background. Balanced emphasis. |
| Filled | `"Filled"` | Bold styling — dark background with contrasting text. High-priority or critical content. |

## Basic Usage

Set the `variant` prop to control the visual style:

```tsx
import { MessageComponent } from '@syncfusion/ej2-react-notifications';

function App() {
  return (
    <div>
      {/* Text (default) — subtle */}
      <MessageComponent content="Editing is restricted" />

      {/* Outlined — clear without a filled background */}
      <MessageComponent content="Editing is restricted" variant="Outlined" />

      {/* Filled — bold, commands attention */}
      <MessageComponent content="Editing is restricted" variant="Filled" />
    </div>
  );
}
```

## Combining Variant with Severity

Every variant works with every severity level. The severity drives the color palette; the variant drives the fill/border style:

```tsx
function App() {
  return (
    <div>
      {/* Filled variants */}
      <MessageComponent content="Editing is restricted" variant="Filled" />
      <MessageComponent content="Please read the comments carefully" severity="Info" variant="Filled" />
      <MessageComponent content="Your message has been sent successfully" severity="Success" variant="Filled" />
      <MessageComponent content="There was a problem with your network connection" severity="Warning" variant="Filled" />
      <MessageComponent content="A problem occurred while submitting your data" severity="Error" variant="Filled" />

      {/* Outlined variants */}
      <MessageComponent content="Editing is restricted" variant="Outlined" />
      <MessageComponent content="Please read the comments carefully" severity="Info" variant="Outlined" />
      <MessageComponent content="Your message has been sent successfully" severity="Success" variant="Outlined" />
      <MessageComponent content="There was a problem with your network connection" severity="Warning" variant="Outlined" />
      <MessageComponent content="A problem occurred while submitting your data" severity="Error" variant="Outlined" />
    </div>
  );
}
```

## When to Use Each Variant

- **Text** — Inline notices, help text, or contextual notes where you don't want the message to dominate the layout.
- **Outlined** — Form validation messages, status cards, or secondary alerts where you want clear visual separation without a heavy background.
- **Filled** — Critical system alerts, banners, or high-priority notifications where the message must stand out immediately.

## Gotcha

The `variant` prop is independent of `severity`. Omitting `variant` defaults to `"Text"` regardless of severity, so a `severity="Error"` message will still use the subtle text style unless `variant="Filled"` is explicitly set.
