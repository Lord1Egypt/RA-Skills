# Getting Started with React Dialog

## Table of Contents
- [Installation](#installation)
- [CSS Imports](#css-imports)
- [Basic Implementation](#basic-implementation)
- [Using DialogComponent with Refs](#using-dialogcomponent-with-refs)
- [Show and Hide Methods](#show-and-hide-methods)
- [Functional Component Pattern](#functional-component-pattern)
- [Initial Visibility](#initial-visibility)

## Installation

Install the required packages from Syncfusion:

```bash
npm install @syncfusion/ej2-react-popups @syncfusion/ej2-base
```

### Package Structure

- `@syncfusion/ej2-react-popups` - React wrapper for popups (includes Dialog)
- `@syncfusion/ej2-base` - Base styles and utilities

## CSS Imports

Import theme CSS in your component. Choose one theme:

**Material Theme (Default):**
```jsx
import '@syncfusion/ej2-base/styles/material.css';
import '@syncfusion/ej2-buttons/styles/material.css';
import '@syncfusion/ej2-popups/styles/material.css';
```

**Bootstrap Theme:**
```jsx
import '@syncfusion/ej2-base/styles/bootstrap.css';
import '@syncfusion/ej2-buttons/styles/bootstrap.css';
import '@syncfusion/ej2-popups/styles/bootstrap.css';
```

**Tailwind Theme:**
```jsx
import '@syncfusion/ej2-base/styles/tailwind.css';
import '@syncfusion/ej2-buttons/styles/tailwind.css';
import '@syncfusion/ej2-popups/styles/tailwind.css';
```

**Note:** Always import base styles first, then component-specific styles.

## Basic Implementation

The simplest Dialog displays content with a header:

```jsx
import React from 'react';
import { DialogComponent } from '@syncfusion/ej2-react-popups';
import '@syncfusion/ej2-base/styles/material.css';
import '@syncfusion/ej2-popups/styles/material.css';

export default function BasicDialog() {
  return (
    <div>
      <DialogComponent 
        header="Welcome" 
        width="400px"
        visible={true}
      >
        <p>This is a simple dialog.</p>
      </DialogComponent>
    </div>
  );
}
```

**Key Properties:**
- `header` - Dialog title (required)
- `width` - Dialog width (default: '330px')
- `visible` - Initial visibility (default: false)
- Children content becomes the dialog body

## Using DialogComponent with Refs

To control dialog visibility programmatically, use refs:

```jsx
import React, { useRef } from 'react';
import { DialogComponent } from '@syncfusion/ej2-react-popups';

export default function ControlledDialog() {
  const dialogRef = useRef(null);

  const handleOpen = () => {
    dialogRef.current?.show();
  };

  const handleClose = () => {
    dialogRef.current?.hide();
  };

  return (
    <div>
      <button onClick={handleOpen} className="e-control e-btn e-primary">
        Open Dialog
      </button>

      <DialogComponent
        ref={dialogRef}
        header="Contact Form"
        width="400px"
        visible={false}
      >
        <p>Email: user@example.com</p>
      </DialogComponent>
    </div>
  );
}
```

**Methods:**
- `show()` - Display the dialog
- `hide()` - Hide the dialog
- Access via `dialogRef.current?.method()`

## Show and Hide Methods

You can control dialog visibility with the ref methods:

```jsx
const dialogRef = useRef(null);

// Show the dialog
const openDialog = () => {
  dialogRef.current?.show();
};

// Hide the dialog
const closeDialog = () => {
  dialogRef.current?.hide();
};

// Toggle visibility
const toggleDialog = () => {
  if (dialogRef.current) {
    // Check if visible by looking at DOM
    const isVisible = dialogRef.current.element?.style.display !== 'none';
    isVisible ? dialogRef.current.hide() : dialogRef.current.show();
  }
};
```

**Important:** Use optional chaining (`?.`) because the ref may not be immediately available.

## Functional Component Pattern

Modern React uses functional components with hooks:

```jsx
import React, { useRef, useState } from 'react';
import { DialogComponent } from '@syncfusion/ej2-react-popups';
import '@syncfusion/ej2-base/styles/material.css';
import '@syncfusion/ej2-popups/styles/material.css';

export default function App() {
  const dialogRef = useRef(null);
  const [formData, setFormData] = useState({ name: '', email: '' });

  const handleOpen = () => {
    dialogRef.current?.show();
  };

  const handleClose = () => {
    setFormData({ name: '', email: '' });
    dialogRef.current?.hide();
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Submitted:', formData);
    handleClose();
  };

  return (
    <div id="dialog-container" style={{ padding: '20px' }}>
      <button onClick={handleOpen} className="e-control e-btn e-primary">
        Open Form
      </button>

      <DialogComponent
        ref={dialogRef}
        header="User Registration"
        width="500px"
        visible={false}
        isModal={true}
        showCloseIcon={true}
        buttons={[
          {
            buttonModel: { content: 'Submit', isPrimary: true },
            click: handleSubmit,
          },
          {
            buttonModel: { content: 'Cancel' },
            click: handleClose,
          },
        ]}
      >
        <form onSubmit={handleSubmit} style={{ padding: '16px' }}>
          <div style={{ marginBottom: '12px' }}>
            <label>Name:</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              style={{ width: '100%', padding: '8px' }}
            />
          </div>
          <div>
            <label>Email:</label>
            <input
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              style={{ width: '100%', padding: '8px' }}
            />
          </div>
        </form>
      </DialogComponent>
    </div>
  );
}
```

## Initial Visibility

Control whether the dialog appears on mount:

```jsx
// Dialog hidden on load
<DialogComponent header="Hidden" visible={false}>
  Content
</DialogComponent>

// Dialog visible on load
<DialogComponent header="Visible" visible={true}>
  Content
</DialogComponent>
```

Use `visible={false}` when you want to show it programmatically with `show()`.

## Complete Working Example

```jsx
import React, { useRef, useState } from 'react';
import { DialogComponent } from '@syncfusion/ej2-react-popups';
import '@syncfusion/ej2-base/styles/material.css';
import '@syncfusion/ej2-buttons/styles/material.css';
import '@syncfusion/ej2-popups/styles/material.css';

export default function App() {
  const dialogRef = useRef(null);
  const [count, setCount] = useState(0);

  const handleOpen = () => {
    dialogRef.current?.show();
  };

  const handleClose = () => {
    dialogRef.current?.hide();
  };

  const handleIncrement = () => {
    setCount(count + 1);
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Dialog Example</h1>
      <p>Counter: {count}</p>

      <button onClick={handleOpen} className="e-control e-btn e-primary">
        Open Dialog
      </button>

      <DialogComponent
        ref={dialogRef}
        header="Counter Dialog"
        width="350px"
        visible={false}
        isModal={true}
        buttons={[
          {
            buttonModel: {
              content: 'Increment',
              isPrimary: true,
              cssClass: 'e-flat',
            },
            click: handleIncrement,
          },
          {
            buttonModel: {
              content: 'Close',
              cssClass: 'e-flat',
            },
            click: handleClose,
          },
        ]}
      >
        <div style={{ padding: '16px' }}>
          <p>Current count: {count}</p>
          <p>Click Increment to add 1</p>
        </div>
      </DialogComponent>
    </div>
  );
}
```

## Common Patterns & Edge Cases

**Pattern: Dialog in a Target Container**
```jsx
<div id="dialog-target" style={{ position: 'relative', height: '400px' }}>
  <DialogComponent
    target="#dialog-target"
    isModal={true}
  >
    Dialog appears within target
  </DialogComponent>
</div>
```

**Edge Case: Ref Not Ready**
```jsx
// Always use optional chaining to safely call methods
dialogRef.current?.show();  // ✓ Safe
dialogRef.current.show();   // ✗ May crash if ref not ready
```

**Edge Case: Dialog Content Doesn't Update**
```jsx
// ✓ Correct: State updates trigger re-render
const [isOpen, setIsOpen] = useState(false);
<DialogComponent visible={isOpen}>Content</DialogComponent>

// ✗ Avoid: Only use refs for show/hide methods
// Use state for visible prop to ensure updates
```
