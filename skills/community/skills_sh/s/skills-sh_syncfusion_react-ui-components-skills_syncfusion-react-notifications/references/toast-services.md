# Toast Services and Advanced Patterns

## Table of Contents
- [ToastUtility — Quick Toasts](#toastutility--quick-toasts)
- [ToastUtility with ToastModel](#toastutility-with-toastmodel)
- [Prevent Duplicate Toasts](#prevent-duplicate-toasts)
- [Restrict Maximum Visible Toasts](#restrict-maximum-visible-toasts)
- [Play Audio on Toast Open](#play-audio-on-toast-open)

---

## ToastUtility — Quick Toasts

`ToastUtility.show()` displays a toast without requiring a `ToastComponent` in the JSX tree. Ideal for notifications triggered deep in service logic or utility functions where accessing a component ref is inconvenient.

### Predefined type toasts

Four built-in types apply automatic styling and icons:

```tsx
import { ToastUtility } from '@syncfusion/ej2-react-notifications';

// Information (blue)
ToastUtility.show('Please read the comments carefully', 'Information', 20000);

// Success (green)
ToastUtility.show('Your message has been sent successfully', 'Success', 20000);

// Warning (yellow/orange)
ToastUtility.show('There was a problem with your network connection', 'Warning', 20000);

// Error (red)
ToastUtility.show('A problem occurred while submitting data', 'Error', 20000);
```

**Signature:** `ToastUtility.show(content, type, timeOut)`

| Param | Type | Description |
|---|---|---|
| `content` | `string` | Message text |
| `type` | `'Information'` \| `'Success'` \| `'Error'` \| `'Warning'` | Built-in style variant |
| `timeOut` | `number` | Duration in ms; `0` for persistent |

### Hiding utility toasts

`ToastUtility.show()` returns a Toast object. Call `hide('All')` on it to dismiss:

```tsx
let toastObj: any;

function showInfo() {
  toastObj = ToastUtility.show('Loading your data...', 'Information', 0);
}

function hideAll() {
  toastObj.hide('All');
}
```

---

## ToastUtility with ToastModel

For advanced configuration, pass a full `ToastModel` object instead of type arguments:

```tsx
import { ToastUtility } from '@syncfusion/ej2-react-notifications';

let toastObj: any;

function showAdvancedToast() {
  toastObj = ToastUtility.show({
    title: 'File Uploaded',
    content: 'report_q4.pdf was uploaded successfully',
    timeOut: 20000,
    position: { X: 'Right', Y: 'Bottom' },
    showCloseButton: true,
    click: () => {
      console.log('Toast clicked');
    },
    buttons: [{
      model: { content: 'View File' },
      click: () => {
        toastObj.hide('All');
        // navigate to file...
      }
    }]
  });
}
```

Any property available on `ToastComponent` can be passed here, including `animation`, `cssClass`, `template`, `showProgressBar`, `newestOnTop`, and all events.

---

## Prevent Duplicate Toasts

Use the `beforeOpen` event to detect and cancel toasts with duplicate content or titles, avoiding notification fatigue:

```tsx
import { ToastBeforeOpenArgs, ToastComponent } from '@syncfusion/ej2-react-notifications';

function App() {
  let toastInstance: ToastComponent;

  const toasts = [
    { title: 'Warning !', content: 'Network connection problem.', isOpen: false },
    { title: 'Success !', content: 'Message sent successfully.', isOpen: false },
    { title: 'Error !', content: 'Data submission failed.', isOpen: false },
  ];
  let toastFlag = 0;

  // Mark toast as closed when it hides
  function onClose(e: any): void {
    for (const toast of toasts) {
      if (toast.title === e.options.title) {
        toast.isOpen = false;
      }
    }
  }

  // Cancel if a toast with the same title is already visible
  function onBeforeOpen(e: ToastBeforeOpenArgs): void {
    for (const toast of toasts) {
      if (toast.title === e.options.title) {
        if (toast.isOpen) {
          e.cancel = true; // already showing — block duplicate
        } else {
          toast.isOpen = true; // mark as now open
        }
        return;
      }
    }
  }

  function showNext(): void {
    toastInstance.show(toasts[toastFlag]);
    toastFlag = (toastFlag + 1) % toasts.length;
  }

  return (
    <div>
      <button onClick={showNext}>Show Toast</button>
      <ToastComponent
        ref={toast => toastInstance = toast!}
        position={{ X: 'Center' }}
        beforeOpen={onBeforeOpen}
        close={onClose}
        created={() => {
          toastInstance.show(toasts[toastFlag]);
          toastFlag++;
        }}
      />
    </div>
  );
}
```

**Key events used:**
- `beforeOpen` — fires before the toast is shown; set `e.cancel = true` to block it
- `close` — fires after toast hides; reset the `isOpen` flag so the same toast can show again later

---

## Restrict Maximum Visible Toasts

Cap the number of toasts shown simultaneously to keep the UI clean. Cancel new toasts when the limit is reached using `beforeOpen`:

```tsx
import { ToastBeforeOpenArgs, ToastComponent } from '@syncfusion/ej2-react-notifications';

function App() {
  let toastInstance: ToastComponent;
  const MAX_TOASTS = 3;

  const toasts = [
    { title: 'Warning !', content: 'Network connection problem.' },
    { title: 'Success !', content: 'Message sent successfully.' },
    { title: 'Error !', content: 'Data submission failed.' },
  ];
  let toastFlag = 0;

  function onBeforeOpen(e: ToastBeforeOpenArgs): void {
    // toastInstance.element.childElementCount = currently visible toasts
    if (toastInstance.element.childElementCount >= MAX_TOASTS) {
      e.cancel = true;
    }
  }

  function showNext(): void {
    toastInstance.show(toasts[toastFlag]);
    toastFlag = (toastFlag + 1) % toasts.length;
  }

  return (
    <div>
      <button onClick={showNext}>Show Toast</button>
      <ToastComponent
        ref={toast => toastInstance = toast!}
        position={{ X: 'Right', Y: 'Bottom' }}
        beforeOpen={onBeforeOpen}
        created={() => {
          toastInstance.show(toasts[toastFlag]);
          toastFlag++;
        }}
      />
    </div>
  );
}
```

`toastInstance.element.childElementCount` reflects how many toast elements are currently rendered inside the container — use this to gate new additions.

---

## Play Audio on Toast Open

Enhance notifications with an audio cue using the `beforeOpen` event. Use the browser's `Audio` API to play a sound file:

```tsx
import { ToastComponent } from '@syncfusion/ej2-react-notifications';

function App() {
  let toastInstance: ToastComponent;

  function showToastWithAudio(): void {
    const audio = new Audio('/sounds/notification.mp3');
    audio.play().catch(() => {
      // Browsers may block autoplay; handle gracefully
      console.warn('Audio playback blocked by browser policy');
    });
    toastInstance.show();
  }

  return (
    <div>
      <button onClick={showToastWithAudio}>Show Toast</button>
      <ToastComponent
        ref={toast => toastInstance = toast!}
        title="New message"
        content="You have received a new message"
        position={{ X: 'Right', Y: 'Bottom' }}
        created={() => toastInstance.show()}
      />
    </div>
  );
}
```

> **Accessibility note:** Always provide text-based notification alternatives for users with hearing disabilities. Be aware that browsers have autoplay policies that may require user interaction before audio can play.

## See Also

- [Timeout and dismissal](./timeout-and-dismissal.md)
- [Templates and styling](./templates-and-styling.md)
- [API reference](./api.md)
