# Toast Timeout and Dismissal

## Table of Contents
- [Automatic Dismissal (timeOut)](#automatic-dismissal-timeout)
- [Extended Timeout on Hover](#extended-timeout-on-hover)
- [Static Persistent Toasts](#static-persistent-toasts)
- [Click-to-Close](#click-to-close)
- [Prevent Swipe-to-Close on Mobile](#prevent-swipe-to-close-on-mobile)

---

## Automatic Dismissal (timeOut)

The `timeOut` property controls how many milliseconds a toast remains visible before auto-dismissing. The default is 5000 ms (5 seconds):

```tsx
<ToastComponent
  ref={toast => toastInstance = toast!}
  title="Auto-dismiss in 3s"
  content="This toast will disappear in 3 seconds"
  timeOut={3000}
  position={{ X: 'Right', Y: 'Bottom' }}
  created={() => toastInstance.show()}
/>
```

You can also override `timeOut` per-call when using `show()`:

```tsx
// Show a toast with a specific timeout for this invocation only
toastInstance.show({ timeOut: 8000 });
```

This allows a single `ToastComponent` to display different messages with different durations.

---

## Extended Timeout on Hover

`extendedTimeout` adds extra display time when a user hovers over the toast — giving them time to read or interact without the toast dismissing mid-interaction. Default is 1000 ms:

```tsx
<ToastComponent
  ref={toast => toastInstance = toast!}
  title="Hover to extend"
  content="I'll stay longer while you hover"
  timeOut={3000}
  extendedTimeout={5000}
  position={{ X: 'Right', Y: 'Bottom' }}
  created={() => toastInstance.show()}
/>
```

When the user stops hovering, the original `timeOut` countdown resumes from where it paused.

---

## Static Persistent Toasts

Set `timeOut={0}` to create a toast that stays on screen until the user explicitly closes it. Combine with `showCloseButton` for full manual control:

```tsx
function App() {
  let toastInstance: ToastComponent;

  const buttons = [
    { model: { content: 'Ignore' } },
    { model: { content: 'Reply' } }
  ];

  return (
    <div>
      <button onClick={() => toastInstance.show({ timeOut: 0 })}>
        Show Persistent Toast
      </button>
      <ToastComponent
        ref={toast => toastInstance = toast!}
        title="Action Required"
        content="Please review the pending changes before proceeding."
        position={{ X: 'Right', Y: 'Bottom' }}
        timeOut={0}
        showCloseButton={true}
        buttons={buttons}
        created={() => toastInstance.show({ timeOut: 0 })}
      />
    </div>
  );
}
```

**When to use:**
- Critical alerts that must not auto-dismiss
- Action-required notifications with response buttons
- Toasts with complex content users need time to read

---

## Click-to-Close

Allow users to close a toast by clicking anywhere on it. Set `e.clickToClose = true` inside the `click` event handler:

```tsx
import { ToastClickEventArgs, ToastComponent } from '@syncfusion/ej2-react-notifications';

function App() {
  let toastInstance: ToastComponent;

  function onClick(e: ToastClickEventArgs): void {
    e.clickToClose = true;
  }

  return (
    <div>
      <button onClick={() => toastInstance.show()}>Show Toast</button>
      <ToastComponent
        ref={toast => toastInstance = toast!}
        title="Click to dismiss"
        content="Click anywhere on this toast to close it"
        position={{ X: 'Right', Y: 'Bottom' }}
        click={onClick}
        created={() => toastInstance.show()}
      />
    </div>
  );
}
```

**Best practice:** Use click-to-close with `timeOut={0}` so the toast does not auto-dismiss before the user can act.

---

## Prevent Swipe-to-Close on Mobile

By default, users can swipe a toast away on mobile devices. To prevent this for critical notifications, cancel swipe actions in the `beforeClose` event:

```tsx
import { ToastComponent } from '@syncfusion/ej2-react-notifications';

function App() {
  let toastInstance: ToastComponent;

  function onBeforeClose(e: any): void {
    if (e.type === 'swipe') {
      e.cancel = true; // Block swipe dismissal only
    }
    // Other close triggers (timeout, close button) proceed normally
  }

  return (
    <div>
      <button onClick={() => toastInstance.show()}>Show Toast</button>
      <ToastComponent
        ref={toast => toastInstance = toast!}
        title="Matt sent you a friend request"
        content="Hey, wanna dress up as wizards and ride our hoverboards?"
        position={{ X: 'Center' }}
        beforeClose={onBeforeClose}
        created={() => toastInstance.show()}
      />
    </div>
  );
}
```

**`e.type` values in `beforeClose`:**
- `'swipe'` — mobile swipe gesture
- `'timeout'` — auto-dismiss due to `timeOut` expiry
- `'close'` — close button clicked

> Checking `e.type === 'swipe'` ensures only swipe dismissal is blocked; timeout and button-close still work normally.

## See Also

- [Configuration options](./configuration.md)
- [API reference](./api.md)
