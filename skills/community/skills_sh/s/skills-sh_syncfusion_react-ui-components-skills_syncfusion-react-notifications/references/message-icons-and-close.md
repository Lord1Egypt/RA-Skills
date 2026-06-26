# Icons and Close Icon

## Table of Contents
- [Severity Icons](#severity-icons)
- [Disabling Severity Icons](#disabling-severity-icons)
- [Custom Severity Icons](#custom-severity-icons)
- [Close Icon](#close-icon)
- [Controlling Visibility with `visible`](#controlling-visibility-with-visible)

---

## Severity Icons

By default, `showIcon` is `true`, meaning each message displays a severity-specific icon on its left edge. The icon changes automatically based on the `severity` prop:

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

---

## Disabling Severity Icons

Set `showIcon={false}` to hide the severity icon for a cleaner, text-only appearance:

```tsx
function App() {
  return (
    <div>
      <MessageComponent content="Editing is restricted" showIcon={false} />
      <MessageComponent content="Please read the comments carefully" severity="Info" showIcon={false} />
      <MessageComponent content="Your message has been sent successfully" severity="Success" showIcon={false} />
      <MessageComponent content="There was a problem with your network connection" severity="Warning" showIcon={false} />
      <MessageComponent content="A problem occurred while submitting your data" severity="Error" showIcon={false} />
    </div>
  );
}
```

---

## Custom Severity Icons

Override the default severity icon by using the `cssClass` prop to apply a custom CSS class, then target the `.e-msg-icon` selector in your stylesheet:

```tsx
<MessageComponent
  id="msg_icon"
  cssClass="custom"
  content="Essential JS 2 is a modern JavaScript UI Controls library."
/>
```

```css
/* App.css — override the icon for messages with cssClass="custom" */
.custom .e-msg-icon::before {
  content: '\e704'; /* your custom icon font character */
  font-family: 'e-icons';
}
```

This allows you to replace default icons with custom icon fonts or images that match your design system.

---

## Close Icon

The close icon lets users dismiss messages interactively. It is hidden by default. Enable it with `showCloseIcon={true}`:

```tsx
import { useState } from 'react';
import { MessageComponent } from '@syncfusion/ej2-react-notifications';

function App() {
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

The `closed` event fires when the user clicks the close icon (or presses Enter/Space while focused on it). Use it to update state so the message doesn't reappear on re-render.

### Restore a Dismissed Message

```tsx
import { useState } from 'react';
import { MessageComponent } from '@syncfusion/ej2-react-notifications';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  const [visible, setVisible] = useState(true);

  return (
    <div>
      {!visible && (
        <ButtonComponent cssClass="e-outline e-primary" onClick={() => setVisible(true)}>
          Show Message
        </ButtonComponent>
      )}
      <MessageComponent
        content="Editing is restricted"
        showCloseIcon={true}
        visible={visible}
        closed={() => setVisible(false)}
      />
    </div>
  );
}
```

---

## Controlling Visibility with `visible`

The `visible` prop shows or hides the entire message without unmounting it. This is useful for toggling messages in response to application state:

```tsx
<MessageComponent
  content="Operation complete"
  severity="Success"
  visible={isOperationDone}
/>
```

- `visible={true}` (default) — message is displayed
- `visible={false}` — message is hidden (but still mounted in the DOM)

### Full Example: Multiple Dismissible Messages

```tsx
import { useState } from 'react';
import { MessageComponent } from '@syncfusion/ej2-react-notifications';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  const [infoVisible, setInfoVisible] = useState(true);
  const [errorVisible, setErrorVisible] = useState(true);

  return (
    <div>
      <MessageComponent
        content="Please read the comments carefully"
        severity="Info"
        showCloseIcon={true}
        visible={infoVisible}
        closed={() => setInfoVisible(false)}
      />
      <MessageComponent
        content="A problem occurred while submitting your data"
        severity="Error"
        showCloseIcon={true}
        visible={errorVisible}
        closed={() => setErrorVisible(false)}
      />
      <ButtonComponent
        cssClass="e-outline e-primary"
        onClick={() => { setInfoVisible(true); setErrorVisible(true); }}
      >
        Reset Messages
      </ButtonComponent>
    </div>
  );
}
```
