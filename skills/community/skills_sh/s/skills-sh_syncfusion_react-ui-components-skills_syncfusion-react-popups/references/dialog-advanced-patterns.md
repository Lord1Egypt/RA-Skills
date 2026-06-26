# Advanced Patterns

## Table of Contents
- [Nested Dialogs](#nested-dialogs)
- [Dialog with Forms](#dialog-with-forms)
- [AJAX Content Loading](#ajax-content-loading)
- [RTL Support](#rtl-support)
- [Prevent Closing on Backdrop Click](#prevent-closing-on-backdrop-click)
- [Full-Screen Dialogs](#full-screen-dialogs)
- [Utility Functions](#utility-functions)
- [Common Gotchas](#common-gotchas)
- [Performance Tips](#performance-tips)
- [Migration from EJ1](#migration-from-ej1)

## Nested Dialogs

Create child dialogs within parent dialogs:

```jsx
import React, { useRef } from 'react';
import { DialogComponent } from '@syncfusion/ej2-react-popups';
import './App.css';

export function NestedDialogs() {
  const parentRef = useRef(null);
  const childRef = useRef(null);

  const parentButtons = [
    {
      buttonModel: { content: 'Open Child', isPrimary: true, cssClass: 'e-flat' },
      click: () => childRef.current?.show(),
    },
    {
      buttonModel: { content: 'Close', cssClass: 'e-flat' },
      click: () => parentRef.current?.hide(),
    },
  ];

  const childButtons = [
    {
      buttonModel: { content: 'OK', isPrimary: true, cssClass: 'e-flat' },
      click: () => childRef.current?.hide(),
    },
    {
      buttonModel: { content: 'Cancel', cssClass: 'e-flat' },
      click: () => childRef.current?.hide(),
    },
  ];

  return (
    <div id="dialog-target" style={{ position: 'relative', minHeight: '500px' }}>
      <button onClick={() => parentRef.current?.show()} className="e-btn">
        Open Parent Dialog
      </button>

      {/* Parent Dialog */}
      <DialogComponent
        ref={parentRef}
        header="Parent Dialog"
        buttons={parentButtons}
        isModal={true}
        target="#dialog-target"
        showCloseIcon={true}
        zIndex={2000}
      >
        <p>This is the parent dialog.</p>
        <p>Click "Open Child" to show a child dialog on top.</p>
      </DialogComponent>

      {/* Child Dialog - appears on top with higher z-index */}
      <DialogComponent
        ref={childRef}
        header="Child Dialog"
        buttons={childButtons}
        isModal={true}
        target="#dialog-target"
        showCloseIcon={true}
        zIndex={2001}  {/* Higher than parent */}
      >
        <p>This child dialog appears on top of the parent.</p>
        <p>Closing this doesn't close the parent.</p>
      </DialogComponent>
    </div>
  );
}
```

### Multi-Level Nesting

```jsx
// Parent → Child → Grandchild
const grandchildButtons = [
  {
    buttonModel: { content: 'Close', isPrimary: true, cssClass: 'e-flat' },
    click: () => grandchildRef.current?.hide(),
  },
];

<DialogComponent
  ref={grandchildRef}
  header="Grandchild Dialog"
  buttons={grandchildButtons}
  zIndex={2002}  {/* Even higher */}
>
  Third level dialog
</DialogComponent>
```

## Dialog with Forms

### Form Submission

```jsx
export function FormDialog() {
  const dialogRef = useRef(null);
  const [formData, setFormData] = React.useState({
    name: '',
    email: '',
    message: '',
  });

  const handleInputChange = (field, value) => {
    setFormData({ ...formData, [field]: value });
  };

  const handleSubmit = async () => {
    console.log('Submitting:', formData);
    try {
      const response = await fetch('/api/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });
      if (response.ok) {
        alert('Submitted successfully');
        dialogRef.current?.hide();
      }
    } catch (error) {
      alert('Error submitting form');
    }
  };

  const buttons = [
    {
      buttonModel: { content: 'Submit', isPrimary: true, cssClass: 'e-flat' },
      click: handleSubmit,
    },
    {
      buttonModel: { content: 'Cancel', cssClass: 'e-flat' },
      click: () => dialogRef.current?.hide(),
    },
  ];

  return (
    <div id="dialog-target" style={{ position: 'relative' }}>
      <button onClick={() => dialogRef.current?.show()} className="e-btn">
        Open Form
      </button>

      <DialogComponent
        ref={dialogRef}
        header="User Information"
        buttons={buttons}
        target="#dialog-target"
        width="400px"
      >
        <form style={{ padding: '20px' }}>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>Name:</label>
            <input
              type="text"
              className="e-input"
              value={formData.name}
              onChange={(e) => handleInputChange('name', e.target.value)}
              placeholder="Enter your name"
              style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
            />
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>Email:</label>
            <input
              type="email"
              className="e-input"
              value={formData.email}
              onChange={(e) => handleInputChange('email', e.target.value)}
              placeholder="Enter your email"
              style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
            />
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>Message:</label>
            <textarea
              className="e-input"
              value={formData.message}
              onChange={(e) => handleInputChange('message', e.target.value)}
              placeholder="Enter your message"
              rows="4"
              style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
            />
          </div>
        </form>
      </DialogComponent>
    </div>
  );
}
```

### Form Validation

```jsx
export function ValidatedFormDialog() {
  const dialogRef = useRef(null);
  const [formData, setFormData] = React.useState({ email: '' });
  const [errors, setErrors] = React.useState({});

  const validateForm = () => {
    const newErrors = {};
    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }
    return newErrors;
  };

  const handleSubmit = () => {
    const newErrors = validateForm();
    if (Object.keys(newErrors).length === 0) {
      console.log('Valid! Submitting:', formData);
      dialogRef.current?.hide();
    } else {
      setErrors(newErrors);
    }
  };

  const buttons = [
    {
      buttonModel: { content: 'Submit', isPrimary: true, cssClass: 'e-flat' },
      click: handleSubmit,
    },
  ];

  return (
    <div id="dialog-target" style={{ position: 'relative' }}>
      <button onClick={() => dialogRef.current?.show()}>Open Form</button>

      <DialogComponent
        ref={dialogRef}
        header="Email Form"
        buttons={buttons}
        target="#dialog-target"
        width="400px"
      >
        <div style={{ padding: '20px' }}>
          <label>Email:</label>
          <input
            type="email"
            className="e-input"
            value={formData.email}
            onChange={(e) => setFormData({ email: e.target.value })}
            style={{
              width: '100%',
              padding: '8px',
              boxSizing: 'border-box',
              borderColor: errors.email ? 'red' : '#ccc',
            }}
          />
          {errors.email && <span style={{ color: 'red' }}>{errors.email}</span>}
        </div>
      </DialogComponent>
    </div>
  );
}
```

## AJAX Content Loading

### Load Content Dynamically

```jsx
export function AjaxDialog() {
  const dialogRef = useRef(null);
  const [content, setContent] = React.useState('Loading...');

  const loadContent = async () => {
    dialogRef.current?.show();
    try {
      const response = await fetch('/api/dialog-content');
      const data = await response.json();
      setContent(data.content);
    } catch (error) {
      setContent('Error loading content');
    }
  };

  return (
    <div id="dialog-target" style={{ position: 'relative' }}>
      <button onClick={loadContent} className="e-btn">
        Load Content
      </button>

      <DialogComponent
        ref={dialogRef}
        header="Dynamic Content"
        target="#dialog-target"
        showCloseIcon={true}
      >
        {content}
      </DialogComponent>
    </div>
  );
}
```

### Load on Dialog Open

```jsx
<DialogComponent
  ref={dialogRef}
  header="Content"
  open={async () => {
    try {
      const response = await fetch('/api/data');
      const data = await response.json();
      setContent(data.message);
    } catch (error) {
      setContent('Error loading');
    }
  }}
>
  {content}
</DialogComponent>
```

## RTL Support

### Enable RTL Direction

```jsx
<div dir="rtl">
  <DialogComponent
    header="حوار"
    isModal={true}
  >
    هذا محتوى باللغة العربية
  </DialogComponent>
</div>
```

### RTL with CSS

```jsx
<DialogComponent
  className="rtl-dialog"
  header="Dialog"
>
  Content
</DialogComponent>
```

```css
.rtl-dialog {
  direction: rtl;
  text-align: right;
}

.rtl-dialog .e-dlg-header {
  flex-direction: row-reverse;
}
```

## Prevent Closing on Backdrop Click

```jsx
export function PreventCloseDialog() {
  const dialogRef = useRef(null);
  const [isSaved, setIsSaved] = React.useState(false);

  const handleBeforeClose = (e) => {
    if (!isSaved) {
      e.cancel = true;
      alert('Please save your changes first');
    }
  };

  const handleSave = () => {
    console.log('Saved');
    setIsSaved(true);
  };

  const buttons = [
    {
      buttonModel: { content: 'Save', isPrimary: true, cssClass: 'e-flat' },
      click: () => {
        handleSave();
        dialogRef.current?.hide();
      },
    },
    {
      buttonModel: { content: 'Discard', cssClass: 'e-flat' },
      click: () => {
        setIsSaved(true);  // Skip validation
        dialogRef.current?.hide();
      },
    },
  ];

  return (
    <div id="dialog-target" style={{ position: 'relative' }}>
      <button onClick={() => dialogRef.current?.show()}>Open</button>

      <DialogComponent
        ref={dialogRef}
        header="Edit"
        buttons={buttons}
        beforeClose={handleBeforeClose}
        showCloseIcon={true}
        isModal={true}
        target="#dialog-target"
      >
        <input placeholder="Make changes" />
      </DialogComponent>
    </div>
  );
}
```

## Full-Screen Dialogs

```jsx
<DialogComponent
  width="100%"
  height="100vh"
  position={{ X: 0, Y: 0 }}
  enableResize={false}
  allowDragging={false}
  header="Full Screen Dialog"
>
  Takes up entire viewport
</DialogComponent>
```

### Full-Screen with Content

```jsx
export function FullScreenDialog() {
  const dialogRef = useRef(null);

  return (
    <div id="dialog-target">
      <button onClick={() => dialogRef.current?.show()}>Full Screen</button>

      <DialogComponent
        ref={dialogRef}
        width="100%"
        height="100%"
        position={{ X: 0, Y: 0 }}
        header="Full Screen Editor"
        enableResize={false}
        allowDragging={false}
        target="#dialog-target"
        buttons={[
          {
            buttonModel: { content: 'Exit', isPrimary: true, cssClass: 'e-flat' },
            click: () => dialogRef.current?.hide(),
          },
        ]}
      >
        <div style={{ padding: '20px', height: 'calc(100% - 100px)', overflow: 'auto' }}>
          <textarea
            style={{ width: '100%', height: '100%', fontSize: '16px' }}
            placeholder="Type here..."
          />
        </div>
      </DialogComponent>
    </div>
  );
}
```

## Utility Functions

### Create Alert Dialog

```jsx
function createAlert(title, message) {
  const alertRef = React.createRef();
  
  return (
    <DialogComponent
      ref={alertRef}
      header={title}
      isModal={true}
      buttons={[
        {
          buttonModel: { content: 'OK', isPrimary: true, cssClass: 'e-flat' },
          click: () => alertRef.current?.hide(),
        },
      ]}
    >
      {message}
    </DialogComponent>
  );
}

// Usage
const alert = createAlert('Warning', 'This action cannot be undone');
```

### Create Confirm Dialog

```jsx
function createConfirm(title, message, onConfirm, onCancel) {
  const confirmRef = React.createRef();
  
  return (
    <DialogComponent
      ref={confirmRef}
      header={title}
      isModal={true}
      buttons={[
        {
          buttonModel: { content: 'OK', isPrimary: true, cssClass: 'e-flat' },
          click: () => {
            onConfirm?.();
            confirmRef.current?.hide();
          },
        },
        {
          buttonModel: { content: 'Cancel', cssClass: 'e-flat' },
          click: () => {
            onCancel?.();
            confirmRef.current?.hide();
          },
        },
      ]}
    >
      {message}
    </DialogComponent>
  );
}
```

### Dialog Registry

```jsx
export const DialogRegistry = {
  dialogs: {},

  register(name, dialogRef) {
    this.dialogs[name] = dialogRef;
  },

  show(name) {
    this.dialogs[name]?.show();
  },

  hide(name) {
    this.dialogs[name]?.hide();
  },

  hideAll() {
    Object.values(this.dialogs).forEach((ref) => ref?.hide());
  },
};

// Usage
DialogRegistry.register('confirm', confirmRef);
DialogRegistry.show('confirm');
DialogRegistry.hideAll();
```

## Common Gotchas

### Issue 1: Dialog Not Showing

```jsx
// ❌ WRONG - No target container
<DialogComponent header="Dialog">Content</DialogComponent>

// ✅ CORRECT - Specify target
<div id="dialog-target" style={{ position: 'relative' }}>
  <DialogComponent target="#dialog-target">Content</DialogComponent>
</div>
```

### Issue 2: CSS Not Loading

```jsx
// ❌ WRONG - Missing theme CSS
import { DialogComponent } from '@syncfusion/ej2-react-popups';

// ✅ CORRECT - Import CSS
import '@syncfusion/ej2-react-popups/styles/tailwind3.css';
import { DialogComponent } from '@syncfusion/ej2-react-popups';
```

### Issue 3: Multiple Opens Not Working

```jsx
// ❌ WRONG - Re-opening without closing
dialogRef.current?.show();
setTimeout(() => dialogRef.current?.show(), 500);

// ✅ CORRECT - Close before reopening
dialogRef.current?.hide();
setTimeout(() => dialogRef.current?.show(), 500);
```

### Issue 4: Z-Index Stacking

```jsx
// ✅ CORRECT - Use different z-indices for nested dialogs
<DialogComponent zIndex={2000}>Parent</DialogComponent>
<DialogComponent zIndex={2001}>Child</DialogComponent>
<DialogComponent zIndex={2002}>Grandchild</DialogComponent>
```

### Issue 5: Dialog Height Not Set Correctly (Height Calculation)

The dialog's `max-height` is calculated based on the height of its **target element**. If the target has no explicit height (or defaults to `document.body` which has zero/auto height), the dialog height will not render correctly.

**Root Cause:** When `target` is not configured, `document.body` is used. If the dialog's height is larger than the body height, the height will not be applied.

```jsx
// ❌ WRONG - body has no explicit height; dialog max-height calculation fails
<DialogComponent height="600px" isModal={true}>
  Content
</DialogComponent>

// ✅ CORRECT - Add min-height to a custom target container
<div id="dialog-target" style={{ position: 'relative', minHeight: '700px' }}>
  <DialogComponent
    target="#dialog-target"
    height="600px"
    isModal={true}
  >
    Content
  </DialogComponent>
</div>

// ✅ CORRECT - When using document.body as target, set CSS for both html and body
```

```css
/* Required when using document.body as the dialog target */
html, body {
  height: 100%;
  margin: 0;
}
```

**Key Rules:**
- Always give the target element an explicit `min-height` or `height`
- When rendering against `document.body`, ensure `html` and `body` both have `height: 100%`
- Using percentage heights on the dialog (e.g., `height="100%"`) requires the target container to have a defined height

## Performance Tips

### Lazy Load Content

```jsx
const [isLoaded, setIsLoaded] = React.useState(false);

const handleOpen = () => {
  if (!isLoaded) {
    // Load heavy content only when needed
    loadHeavyContent().then(() => setIsLoaded(true));
  }
  dialogRef.current?.show();
};

<DialogComponent open={handleOpen}>
  {isLoaded && <HeavyComponent />}
</DialogComponent>
```

### Memoize Dialog Content

```jsx
const DialogContent = React.memo(() => (
  <div>Heavy computation content</div>
));

<DialogComponent>
  <DialogContent />
</DialogComponent>
```

### Avoid Recreating Dialogs

```jsx
// ❌ WRONG - Recreates dialog on every render
const MyComponent = () => {
  return <DialogComponent header="Dialog">Content</DialogComponent>;
};

// ✅ CORRECT - Dialog is stable
const Dialog = () => (
  <DialogComponent header="Dialog">Content</DialogComponent>
);

const MyComponent = () => <Dialog />;
```

## Migration from EJ1

### EJ1 vs EJ2 Properties

| EJ1 | EJ2 | Notes |
|-----|-----|-------|
| `isModal` | `isModal` | Same |
| `title` | `header` | Renamed |
| `content` | `children` or `content` | Use children in React |
| `allowKeyboardInteraction` | `closeOnEscape` | Controls Escape key behavior |
| `showCloseButton` | `showCloseIcon` | Renamed |
| `buttons` | `buttons` | Same structure, different API |
| `position` | `position` | Same |
| `draggable` | `allowDragging` | Renamed |
| `resizable` | `enableResize` | Renamed; use `resizeHandles` for resize options |

### Migration Example

```jsx
// EJ1 Style
// $('#dialog').ejDialog({
//     isModal: true,
//     title: 'Dialog',
//     content: 'Hello',
//     buttons: [{ text: 'OK', click: function() { } }]
// });

// EJ2 Style (React)
import { DialogComponent } from '@syncfusion/ej2-react-popups';

<DialogComponent
  ref={dialogRef}
  isModal={true}
  header="Dialog"
  buttons={[{
    buttonModel: { content: 'OK' },
    click: () => {}
  }]}
>
  Hello
</DialogComponent>
```

**Next:** Choose another reference topic based on your needs.
