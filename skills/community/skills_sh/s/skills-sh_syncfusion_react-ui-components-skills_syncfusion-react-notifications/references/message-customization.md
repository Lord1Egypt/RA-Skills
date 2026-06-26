# Customization and Templates

## Table of Contents
- [Content Alignment](#content-alignment)
- [Custom Appearance with cssClass](#custom-appearance-with-cssclass)
- [CSS-Only Message Rendering](#css-only-message-rendering)
- [Content Templates](#content-templates)
- [RTL Support](#rtl-support)
- [Persistence](#persistence)

---

## Content Alignment

By default, message content aligns to the left. Use built-in CSS classes via the `cssClass` prop to change alignment:

| CSS Class | Effect |
|-----------|--------|
| *(none)* | Left-aligned (default) |
| `e-content-center` | Center-aligned |
| `e-content-right` | Right-aligned |

```tsx
import { MessageComponent } from '@syncfusion/ej2-react-notifications';

function App() {
  return (
    <div>
      {/* Left (default) */}
      <MessageComponent content="Your license has been activated successfully" severity="Success" />

      {/* Centered */}
      <MessageComponent
        content="The license will expire today"
        cssClass="e-content-center"
        severity="Warning"
      />

      {/* Right-aligned */}
      <MessageComponent
        content="The license key is invalid"
        cssClass="e-content-right"
        severity="Error"
      />
    </div>
  );
}
```

---

## Custom Appearance with cssClass

The `cssClass` prop appends one or more CSS classes to the message's root element. Use this to override default styles, set border-radius, change padding, or apply any custom design:

```tsx
{/* Rounded corners */}
<MessageComponent content="The license will expire today" cssClass="rounded" severity="Warning" />

{/* Square (no border-radius) */}
<MessageComponent content="The license key is invalid" cssClass="square" severity="Error" />
```

```css
/* App.css */
.rounded {
  border-radius: 20px;
}

.square {
  border-radius: 0;
}
```

Multiple classes are space-separated:

```tsx
<MessageComponent cssClass="e-content-center rounded" severity="Info" content="Centered + rounded" />
```

---

## CSS-Only Message Rendering

The Message component can be rendered using pure HTML and CSS without any JavaScript initialization. This is ideal for static content, server-rendered HTML, or lightweight scenarios.

### Structure — Content Only

```html
<div class="e-message" role="alert">
  <div class="e-msg-content">Editing is restricted</div>
</div>
```

### Structure — Content with Severity Icon

```html
<div class="e-message" role="alert">
  <span class="e-msg-icon"></span>
  <div class="e-msg-content">Editing is restricted</div>
</div>
```

### Available Predefined CSS Classes

| Class | Description |
|-------|-------------|
| `e-message` | Root message wrapper (required) |
| `e-msg-icon` | Severity type icon |
| `e-msg-content` | Message content container |
| `e-msg-close-icon` | Close icon |
| `e-info` | Info severity styling |
| `e-success` | Success severity styling |
| `e-warning` | Warning severity styling |
| `e-error` | Error severity styling |
| `e-content-center` | Center-align message content |
| `e-content-right` | Right-align message content |

### Full CSS-Only Example

```html
<div class="e-message" role="alert">
  <span class="e-msg-icon"></span>
  <div class="e-msg-content">Editing is restricted</div>
</div>
<div class="e-message e-info" role="alert">
  <span class="e-msg-icon"></span>
  <div class="e-msg-content">Please read the comments carefully</div>
</div>
<div class="e-message e-success" role="alert">
  <span class="e-msg-icon"></span>
  <div class="e-msg-content">Your message has been sent successfully</div>
</div>
<div class="e-message e-warning" role="alert">
  <span class="e-msg-icon"></span>
  <div class="e-msg-content">There was a problem with your network connection</div>
</div>
<div class="e-message e-error" role="alert">
  <span class="e-msg-icon"></span>
  <div class="e-msg-content">A problem occurred while submitting your data</div>
</div>
```

---

## Content Templates

The `content` prop accepts a string, a JSX element, or a render function — enabling rich, interactive message bodies:

### String Content

```tsx
<MessageComponent content="Simple text message" />
```

### JSX / Function Template

Pass a function that returns JSX to embed HTML structure or React components inside the message:

```tsx
import { useState } from 'react';
import { MessageComponent } from '@syncfusion/ej2-react-notifications';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  const [visible, setVisible] = useState(true);

  const contentTemplate = () => (
    <div>
      <h1>Merged pull request</h1>
      <p>Pull request #41 merged after a successful build</p>
      <ButtonComponent cssClass="e-link" content="View commit" />
      <ButtonComponent cssClass="e-link" content="Dismiss" onClick={() => setVisible(false)} />
    </div>
  );

  return (
    <MessageComponent
      visible={visible}
      content={contentTemplate}
      severity="Success"
      closed={() => setVisible(false)}
    />
  );
}
```

### Children as Content

JSX children are also supported:

```tsx
<MessageComponent severity="Info">
  <strong>Note:</strong> This action cannot be undone.
</MessageComponent>
```

---

## RTL Support

Enable right-to-left text direction for RTL languages (Arabic, Hebrew, etc.) using `enableRtl`:

```tsx
<MessageComponent content="مرحبا بالعالم" severity="Info" enableRtl={true} />
```

---

## Persistence

The `enablePersistence` prop saves the component's state (including `visible`) across page reloads using browser storage:

```tsx
<MessageComponent content="Persistent message" enablePersistence={true} />
```

Use this when you want dismissed messages to stay dismissed after a page reload.
