# Modal vs Modeless Dialog

## Table of Contents
- [Modal Dialog](#modal-dialog)
- [Modeless Dialog](#modeless-dialog)
- [Comparison](#comparison)
- [Choosing the Right Mode](#choosing-the-right-mode)
- [Overlay Customization](#overlay-customization)
- [Focus Management](#focus-management)
- [Examples](#examples)

## Modal Dialog

A **modal dialog** prevents user interaction with the parent application until the dialog is closed. It displays an overlay (backdrop) behind the dialog.

### Basic Modal Example

```jsx
import React, { useRef } from 'react';
import { DialogComponent } from '@syncfusion/ej2-react-popups';
import './App.css';

export default function App() {
  const dialogRef = useRef(null);

  const buttons = [
    {
      buttonModel: { content: 'OK', isPrimary: true, cssClass: 'e-flat' },
      click: () => dialogRef.current?.hide(),
    },
    {
      buttonModel: { content: 'Cancel', cssClass: 'e-flat' },
      click: () => dialogRef.current?.hide(),
    },
  ];

  return (
    <div id="dialog-target" style={{ position: 'relative', height: '500px' }}>
      <h1>Modal Dialog Example</h1>
      <button onClick={() => dialogRef.current?.show()} className="e-btn">
        Open Modal
      </button>

      {/* Modal dialog - user cannot interact with content behind */}
      <DialogComponent
        ref={dialogRef}
        header="Important Decision"
        buttons={buttons}
        isModal={true}
        target="#dialog-target"
        showCloseIcon={true}
      >
        <p>This is a modal dialog. You must respond before continuing.</p>
      </DialogComponent>
    </div>
  );
}
```

### Key Characteristics
- **Overlay visible:** Dark/semi-transparent backdrop blocks interaction
- **Focus trapped:** User cannot access parent content
- **Required response:** Dialog must be closed to continue
- **Blocking behavior:** Parent interaction blocked until dialog closes

### Use Cases
- Confirmation dialogs ("Are you sure?")
- Critical warnings or errors
- Form submission required
- Security confirmations (delete, logout)
- License acceptance

## Modeless Dialog

A **modeless dialog** allows users to interact with the parent application while the dialog is open. No overlay is displayed.

### Basic Modeless Example

```jsx
import React, { useRef } from 'react';
import { DialogComponent } from '@syncfusion/ej2-react-popups';
import './App.css';

export default function App() {
  const dialogRef = useRef(null);

  return (
    <div id="dialog-target" style={{ position: 'relative', height: '500px' }}>
      <h1>Modeless Dialog Example</h1>
      <button onClick={() => dialogRef.current?.show()} className="e-btn">
        Open Modeless
      </button>

      {/* Modeless dialog - user CAN interact with content behind */}
      <DialogComponent
        ref={dialogRef}
        header="Floating Window"
        isModal={false}
        target="#dialog-target"
        showCloseIcon={true}
        allowDragging={true}
        position={{ X: 100, Y: 100 }}
      >
        <p>This is modeless. Click elements in the background while this is open.</p>
      </DialogComponent>
    </div>
  );
}
```

### Key Characteristics
- **No overlay:** Background is fully visible
- **Interaction allowed:** User can click parent content
- **Floating window:** Dialog floats on top like a window
- **Non-blocking:** Dialog doesn't prevent other actions

### Use Cases
- Help/information windows
- Tool palettes or docking windows
- Real-time previews
- Settings that don't require immediate action
- Draggable floating panels
- Chat windows

## Comparison

| Feature | Modal | Modeless |
|---------|-------|----------|
| **Overlay** | Yes (dark backdrop) | No |
| **Parent interaction** | Blocked | Allowed |
| **Close required** | Yes (must respond) | Optional (can ignore) |
| **Use case** | Confirmations, alerts, critical decisions | Tools, helpers, reference windows |
| **Typical behavior** | Dialog focuses attention | Secondary information |
| **Draggable** | Usually not | Commonly yes |
| **Multiple open** | Typically one | Multiple possible |

## Choosing the Right Mode

**Use Modal if:**
- User must make a decision before continuing
- Action is destructive or irreversible
- Requires acknowledgment or consent
- Data entry/form submission needed

**Use Modeless if:**
- Information is supplementary
- User should maintain context with parent
- Tool or palette window
- Help/reference content
- Real-time collaboration or preview needed

### Decision Flowchart

```
Does the user NEED to respond?
├─ YES → Modal (e.g., "Confirm deletion?")
└─ NO → Modeless (e.g., "Tips & Tricks")

Is it a critical action?
├─ YES → Modal (e.g., security warning)
└─ NO → Modeless (e.g., search result)

Can user ignore this?
├─ YES → Modeless (e.g., help window)
└─ NO → Modal (e.g., form submission)
```

## Overlay Customization

### Modal Overlay Styling

```css
/* Change overlay color and opacity */
.e-dlg-overlay {
    background-color: rgba(0, 0, 0, 0.7);
    opacity: 0.8;
}

/* Lighter overlay */
.e-dlg-overlay {
    background-color: rgba(100, 100, 255, 0.3);
}

/* Custom blur effect */
.e-dlg-overlay::before {
    backdrop-filter: blur(2px);
}
```

### Remove Overlay for Custom Styling

```jsx
<DialogComponent
  isModal={true}
  className="custom-modal"
>
  Content
</DialogComponent>
```

```css
.custom-modal ~ .e-dlg-overlay {
    background: none;
}
```

## Focus Management

### Modal - Automatic Focus Trapping

When modal dialog opens, focus is automatically managed:
- Initial focus goes to first focusable element
- Tab/Shift+Tab cycles through dialog elements
- Cannot tab to parent elements
- Focus returns to trigger button on close

```jsx
<DialogComponent
  isModal={true}
  showCloseIcon={true}
>
  <input autoFocus placeholder="Focused on open" />
</DialogComponent>
```

### Initial Focus Element

```jsx
const dialogRef = useRef(null);

const handleOpen = () => {
  dialogRef.current?.show();
  // Move focus to specific element
  setTimeout(() => {
    document.querySelector('.dialog-input')?.focus();
  }, 0);
};

<DialogComponent
  ref={dialogRef}
  open={handleOpen}
>
  <input className="dialog-input" placeholder="Gets focus" />
</DialogComponent>
```

### Modeless - Preserve Parent Focus

In modeless dialogs, focus remains on parent:

```jsx
<DialogComponent
  isModal={false}
  allowDragging={true}
>
  {/* User can click inputs behind this dialog */}
  <p>Reference information</p>
</DialogComponent>
```

## Examples

### Example 1: Confirmation Dialog (Modal)

```jsx
export function ConfirmDialog() {
  const dialogRef = useRef(null);
  const [itemToDelete, setItemToDelete] = useState(null);

  const confirmDelete = (item) => {
    setItemToDelete(item);
    dialogRef.current?.show();
  };

  const handleConfirm = () => {
    console.log('Deleting:', itemToDelete);
    dialogRef.current?.hide();
  };

  const buttons = [
    {
      buttonModel: { content: 'Delete', isPrimary: true, cssClass: 'e-flat e-danger' },
      click: handleConfirm,
    },
    {
      buttonModel: { content: 'Cancel', cssClass: 'e-flat' },
      click: () => dialogRef.current?.hide(),
    },
  ];

  return (
    <div id="dialog-target" style={{ position: 'relative' }}>
      <button onClick={() => confirmDelete('Item 1')}>Delete Item</button>

      <DialogComponent
        ref={dialogRef}
        header="Confirm Deletion"
        buttons={buttons}
        isModal={true}
        target="#dialog-target"
      >
        Are you sure you want to delete <strong>{itemToDelete}</strong>?
      </DialogComponent>
    </div>
  );
}
```

### Example 2: Floating Tool (Modeless)

```jsx
export function FloatingTool() {
  const dialogRef = useRef(null);

  return (
    <div id="dialog-target" style={{ position: 'relative', height: '600px' }}>
      <div style={{ padding: '20px' }}>
        <h1>Main Content Area</h1>
        <p>You can interact with this while the tool window is open</p>
        <input type="text" placeholder="Try typing here" style={{ padding: '8px' }} />
      </div>

      <button onClick={() => dialogRef.current?.show()} className="e-btn">
        Open Tool
      </button>

      <DialogComponent
        ref={dialogRef}
        header="Color Picker"
        isModal={false}
        allowDragging={true}
        enableResize={true}
        resizeHandles={['All']}
        position={{ X: 300, Y: 100 }}
        target="#dialog-target"
        width="250px"
      >
        <div style={{ padding: '10px' }}>
          <input type="color" style={{ width: '100%' }} />
        </div>
      </DialogComponent>
    </div>
  );
}
```

### Example 3: Alert (Modal, Single Button)

```jsx
<DialogComponent
  isModal={true}
  header="Alert"
  buttons={[
    {
      buttonModel: { content: 'OK', isPrimary: true, cssClass: 'e-flat' },
      click: () => dialogRef.current?.hide(),
    },
  ]}
>
  <p>Important update: Your session expires in 5 minutes.</p>
</DialogComponent>
```

## Edge Cases

### Multiple Modal Dialogs

When opening multiple modals, each should have its own target:

```jsx
<div id="dialog-target" style={{ position: 'relative' }}>
  {/* First modal */}
  <DialogComponent
    ref={dialog1Ref}
    isModal={true}
    target="#dialog-target"
    zIndex={2000}
  >
    Parent dialog
    <button onClick={() => dialog2Ref.current?.show()}>Open Child</button>
  </DialogComponent>

  {/* Second modal - higher z-index */}
  <DialogComponent
    ref={dialog2Ref}
    isModal={true}
    target="#dialog-target"
    zIndex={2001}
  >
    Child dialog - appears on top
  </DialogComponent>
</div>
```

### Modeless with Multiple Instances

```jsx
// Each tool window is independent
<DialogComponent isModal={false} position={{ X: 50, Y: 50 }} />
<DialogComponent isModal={false} position={{ X: 350, Y: 50 }} />
<DialogComponent isModal={false} position={{ X: 50, Y: 350 }} />
```

**Next:** Choose another reference topic based on your needs.
