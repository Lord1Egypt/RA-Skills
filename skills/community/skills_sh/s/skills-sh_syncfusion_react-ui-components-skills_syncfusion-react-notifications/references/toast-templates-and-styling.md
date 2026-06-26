# Toast Templates and Styling

## Table of Contents
- [Semantic CSS Class Types](#semantic-css-class-types)
- [Custom Template Property](#custom-template-property)
- [Dynamic Templates per Show Call](#dynamic-templates-per-show-call)
- [CSS Customization](#css-customization)

---

## Semantic CSS Class Types

Apply one of four built-in semantic classes via the `cssClass` property to convey message severity without custom CSS. These classes apply predefined background colors, icons, and text styling:

| `cssClass` Value | Meaning | Example Use |
|---|---|---|
| `'e-toast-success'` | Positive / completed | "File saved successfully" |
| `'e-toast-info'` | Informational | "New message received" |
| `'e-toast-warning'` | Caution / attention required | "Unsaved changes detected" |
| `'e-toast-danger'` | Error / critical issue | "Upload failed" |

```tsx
function App() {
  let toastInstance: ToastComponent;
  const toasts = [
    { title: 'Warning !', content: 'There was a problem with your network connection.', cssClass: 'e-toast-warning' },
    { title: 'Success !', content: 'Your message has been sent successfully.', cssClass: 'e-toast-success' },
    { title: 'Error !', content: 'A problem occurred while submitting your data.', cssClass: 'e-toast-danger' },
    { title: 'Information !', content: 'Please read the comments carefully.', cssClass: 'e-toast-info' },
  ];
  let toastFlag = 0;
  const position = { X: 'Right', Y: 'Bottom' };

  function toastCreated(): void {
    toastInstance.show(toasts[toastFlag]);
    toastFlag++;
  }

  function showNext(): void {
    toastInstance.show(toasts[toastFlag]);
    toastFlag = (toastFlag + 1) % toasts.length;
  }

  return (
    <div>
      <button onClick={showNext}>Show Next Toast</button>
      <ToastComponent
        ref={toast => toastInstance = toast!}
        position={position}
        created={toastCreated}
      />
    </div>
  );
}
```

> **When passing toast config to `show()`**, properties like `cssClass`, `title`, `content` can be overridden per invocation. The component-level `cssClass` acts as the default.

---

## Custom Template Property

Replace the default title+content layout entirely with a custom HTML template using the `template` property. This enables complex layouts, icons, images, and fully branded notifications.

### Template as a function (JSX — recommended for React)

```tsx
function App() {
  let toastInstance: ToastComponent;

  function customTemplate() {
    return (
      <div className="custom-toast">
        <span className="e-icons e-check-circle" />
        <div>
          <strong>Upload complete</strong>
          <p>report_q4.pdf (2.3 MB)</p>
        </div>
      </div>
    );
  }

  return (
    <div>
      <button onClick={() => toastInstance.show()}>Show Toast</button>
      <ToastComponent
        ref={toast => toastInstance = toast!}
        template={customTemplate}
        position={{ X: 'Right', Y: 'Bottom' }}
        extendedTimeout={0}
        timeOut={120000}
        created={() => toastInstance.show()}
      />
    </div>
  );
}
```

### Template as an HTML string

```tsx
const htmlTemplate = `
  <div class="e-custom-toast">
    <h4>Custom Title</h4>
    <p>Custom content with <a href="#">a link</a></p>
  </div>
`;

<ToastComponent
  ref={toast => toastInstance = toast!}
  template={htmlTemplate}
  position={{ X: 'Center', Y: 'Bottom' }}
  created={() => toastInstance.show()}
/>
```

### Template as a DOM element selector

```tsx
// Reference an existing hidden element by ID
<ToastComponent
  ref={toast => toastInstance = toast!}
  template="#templateId"
  position={{ X: 'Right', Y: 'Bottom' }}
  created={() => toastInstance.show()}
/>
```

> When `template` is set, the built-in `title` and `content` props are ignored in rendering — the template takes full precedence.

---

## Dynamic Templates per Show Call

Pass different templates per `show()` invocation to reuse a single Toast instance for varied notification content:

```tsx
function App() {
  let toastInstance: ToastComponent;
  const toasts = [
    { template: '2 new mails received' },
    { template: 'User Guest logged in' },
    { template: 'Ticket has been reserved' },
    { template: '#templateToast' },  // DOM element selector
  ];
  let toastFlag = 0;

  function onClick(e: ToastClickEventArgs): void {
    e.clickToClose = true;
  }

  function showToast(): void {
    toastInstance.show(toasts[toastFlag]);
    toastFlag = (toastFlag + 1) % toasts.length;
  }

  return (
    <div>
      <button onClick={showToast}>Show Next Toast</button>
      <ToastComponent
        ref={toast => toastInstance = toast!}
        position={{ X: 'Right', Y: 'Bottom' }}
        click={onClick}
        created={() => {
          toastInstance.show(toasts[toastFlag]);
          toastFlag++;
        }}
      />
    </div>
  );
}
```

---

## CSS Customization

Use Syncfusion's CSS class selectors to override default toast styling:

### Toast title

```css
.e-toast-container .e-toast .e-toast-message .e-toast-title {
  color: #1a1a1a;
  font-size: 16px;
  font-weight: 600;
}
```

### Toast content body

```css
.e-toast-container .e-toast .e-toast-message .e-toast-content {
  color: #444;
  font-size: 13px;
  font-weight: normal;
}
```

### Toast icon

```css
.e-toast-container .e-toast .e-toast-icon {
  color: #0078d4;
}
```

### Toast background

```css
.e-toast-container .e-toast {
  background-color: #1e1e2e;
  border-radius: 8px;
}
```

### Target only one toast type

```css
/* Override only success toasts */
.e-toast-container .e-toast.e-toast-success {
  background-color: #d4edda;
  border-left: 4px solid #28a745;
}
```

## See Also

- [Toast services](./toast-services.md) — `ToastUtility` predefined types
- [Getting started](./getting-started.md) — CSS import paths
- [API reference](./api.md)
