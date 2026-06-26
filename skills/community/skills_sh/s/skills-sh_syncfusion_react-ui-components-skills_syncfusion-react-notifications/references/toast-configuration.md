# Toast Configuration

## Table of Contents
- [Title and Content](#title-and-content)
- [Close Button](#close-button)
- [Progress Bar](#progress-bar)
- [Stacking Order](#stacking-order)
- [Width and Height](#width-and-height)
- [Action Buttons](#action-buttons)
- [Custom Target Container](#custom-target-container)

---

## Title and Content

Use `title` for the notification headline and `content` for the message body. Both accept plain text, HTML strings, or element references:

```tsx
<ToastComponent
  title="Matt sent you a friend request"
  content="Hey, wanna dress up as wizards and ride our hoverboards?"
  position={{ X: 'Center' }}
  created={() => toastInstance.show()}
  ref={toast => toastInstance = toast!}
/>
```

HTML content in `content` and `title` is sanitized by default (`enableHtmlSanitizer: true`). To allow raw HTML, set `enableHtmlSanitizer={false}` (use with caution in user-generated content contexts).

---

## Close Button

Enable a manual dismiss button so users can close the toast before timeout:

```tsx
<ToastComponent
  ref={toast => toastInstance = toast!}
  title="File Downloading"
  content="<div class='progress'><span style='width: 80%'></span></div>"
  position={{ X: 'Center' }}
  showCloseButton={true}
  created={() => toastInstance.show()}
/>
```

`showCloseButton` defaults to `false`. Pair with `timeOut={0}` for persistent toasts that require explicit user dismissal.

---

## Progress Bar

Display a visual countdown bar showing remaining display time:

```tsx
<ToastComponent
  ref={toast => toastInstance = toast!}
  title="Uploading"
  content="Your file is being uploaded..."
  showProgressBar={true}
  progressDirection="Ltr"
  timeOut={5000}
  position={{ X: 'Right', Y: 'Bottom' }}
  created={() => toastInstance.show()}
/>
```

| Property | Type | Default | Description |
|---|---|---|---|
| `showProgressBar` | boolean | `false` | Enables the progress bar |
| `progressDirection` | `'Ltr'` \| `'Rtl'` | `'Rtl'` | Direction of progress bar fill |

Use `progressDirection="Ltr"` for a left-to-right fill (empties left-to-right), and `"Rtl"` for right-to-left (default, empties right-to-left).

---

## Stacking Order

Control whether new toasts appear above or below existing ones:

```tsx
<ToastComponent
  ref={toast => toastInstance = toast!}
  title="Notification"
  content="New notification received"
  newestOnTop={true}
  position={{ X: 'Center' }}
  created={() => toastInstance.show()}
/>
```

| `newestOnTop` | Behavior |
|---|---|
| `true` (default) | New toasts appear above older ones |
| `false` | New toasts append below existing stack |

---

## Width and Height

Set custom dimensions using pixels, numbers (treated as pixels), or percentages:

```tsx
<ToastComponent
  ref={toast => toastInstance = toast!}
  title="Notification"
  content="Custom sized toast"
  width={400}
  height="auto"
  position={{ X: 'Center', Y: 'Bottom' }}
  created={() => toastInstance.show()}
/>
```

**Defaults:** `width: '300'`, `height: 'auto'`

**Full-width toast:** Set `width="100%"` — toast spans the full container width. The `position.X` value is ignored when width is 100%. Position with `position.Y` only (`'Top'` or `'Bottom'`):

```tsx
<ToastComponent
  ref={toast => toastInstance = toast!}
  content="<div class='e-custom'>System maintenance in 10 minutes</div>"
  width="100%"
  title=""
  position={{ X: 'Center', Y: 'Top' }}
  created={() => toastInstance.show()}
/>
```

> On mobile devices, the default width is `100%` of the page.

---

## Action Buttons

Add interactive buttons to toast notifications using the `buttons` property. Each button is specified with a `model` (Button component props) and an optional click handler:

```tsx
function App() {
  let toastInstance: ToastComponent;

  const buttons = [
    { model: { content: 'Ignore' } },
    { model: { content: 'Reply' } }
  ];

  function contentTemplate() {
    return <p><img src="./avatar.png" alt="user" /></p>;
  }

  return (
    <div>
      <button onClick={() => toastInstance.show()}>Show Toast</button>
      <ToastComponent
        ref={toast => toastInstance = toast!}
        title="Anjolie Stokes"
        content={contentTemplate}
        position={{ X: 'Right', Y: 'Bottom' }}
        width={230}
        height={250}
        buttons={buttons}
        created={() => toastInstance.show()}
      />
    </div>
  );
}
```

**Button model properties** follow the Syncfusion `ButtonModel` interface — set `content`, `cssClass`, `iconCss`, `disabled`, etc.

To handle button clicks:
```tsx
const buttons = [
  {
    model: { content: 'Undo' },
    click: () => {
      console.log('Undo clicked');
      toastInstance.hide('All');
    }
  }
];
```

---

## Custom Target Container

Render toast inside a specific DOM element instead of `document.body`:

```tsx
<ToastComponent
  ref={toast => toastInstance = toast!}
  title="Scoped Alert"
  content="This toast is inside the panel"
  target="#my-panel"
  position={{ X: 'Center', Y: 'Top' }}
  created={() => toastInstance.show()}
/>
```

Toast position (`Left`, `Right`, `Center`, `Top`, `Bottom`) is calculated relative to the target element when `target` is set.

## See Also

- [Positioning](./position.md)
- [Timeout and dismissal](./timeout-and-dismissal.md)
- [API reference](./api.md)
