# Customization in React Predefined Dialogs

## Table of Contents
- [Overview](#overview)
- [Alert Action Button](#alert-action-button)
- [Confirm Action Buttons](#confirm-action-buttons)
- [Prompt Action Buttons](#prompt-action-buttons)
- [Show or Hide Close Button](#show-or-hide-close-button)
- [Customize Dialog Content](#customize-dialog-content)

---

## Overview

Predefined dialog buttons are customized via:
- `okButton` — customize the OK button (`text`, `icon`, `click`)
- `cancelButton` — customize the Cancel button (`text`, `icon`, `click`)
- `showCloseIcon` — show an × icon in the dialog header (default: `false`)
- `closeOnEscape` — close on Escape key press (default: `false`)
- `content` — supports HTML strings for custom content including input elements

---

## Alert Action Button

Customize the alert OK button label using `okButton: { text: '...' }`.

```tsx
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { DialogUtility } from '@syncfusion/ej2-react-popups';
import * as React from 'react';

function App() {
  function buttonClick() {
    DialogUtility.alert({
      title: 'Low Battery',
      content: '10% of battery remaining',
      width: '250px',
      okButton: { text: 'Dismiss' },
    });
  }
  return (
    <div className="App" id="dialog-target">
      <ButtonComponent id="alertBtn" cssClass="e-danger" onClick={buttonClick}>Alert</ButtonComponent>
    </div>
  );
}
export default App;
```

---

## Confirm Action Buttons

Customize both OK and Cancel labels and add icons using `icon`.

```tsx
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { DialogUtility } from '@syncfusion/ej2-react-popups';
import * as React from 'react';

function App() {
  function buttonClick() {
    DialogUtility.confirm({
      title: 'Delete Multiple Items',
      content: 'Are you sure you want to permanently delete these items?',
      width: '300px',
      okButton: { text: 'Yes', icon: 'e-icons e-check' },
      cancelButton: { text: 'No', icon: 'e-icons e-close' },
    });
  }
  return (
    <div className="App" id="dialog-target">
      <ButtonComponent id="confirmBtn" cssClass="e-success" onClick={buttonClick}>Confirm</ButtonComponent>
    </div>
  );
}
export default App;
```

---

## Prompt Action Buttons

```tsx
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { DialogUtility } from '@syncfusion/ej2-react-popups';
import * as React from 'react';

function App() {
  function buttonClick() {
    DialogUtility.confirm({
      title: 'Join Chat Group',
      content: '<p>Enter your name:</p><input type="text" class="e-input" placeholder="Type here.." />',
      height: '200px',
      okButton: { text: 'Connect' },
      cancelButton: { text: 'Close' },
    });
  }
  return (
    <div className="App" id="dialog-target">
      <ButtonComponent id="promptBtn" isPrimary onClick={buttonClick}>Prompt</ButtonComponent>
    </div>
  );
}
export default App;
```

---

## Show or Hide Close Button

Use `showCloseIcon: true` to show the × icon and `closeOnEscape: true` to allow Escape key to close.

**Alert:**
```tsx
DialogUtility.alert({
  title: 'Low Battery',
  width: '250px',
  content: '10% of battery remaining',
  showCloseIcon: true,
  closeOnEscape: true,
});
```

**Confirm:**
```tsx
DialogUtility.confirm({
  title: 'Delete Multiple Items',
  content: 'Are you sure you want to permanently delete these items?',
  width: '300px',
  showCloseIcon: true,
  closeOnEscape: true,
});
```

**Prompt:**
```tsx
DialogUtility.confirm({
  title: 'Join Chat Group',
  content: '<p>Enter your name:</p> <input type="text" class="e-input" placeholder="Type here.." />',
  width: '300px',
  showCloseIcon: true,
  closeOnEscape: true,
});
```

---

## Customize Dialog Content

Pass an HTML string to `content` to render rich content including input elements.

```tsx
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { DialogUtility } from '@syncfusion/ej2-react-popups';
import * as React from 'react';

function App() {
  function buttonClick() {
    DialogUtility.confirm({
      title: 'Join Chat Group',
      content: '<p>Enter your name:</p><input class="e-input" placeholder="Type here.." />',
      width: '300px',
    });
  }
  return (
    <div className="App" id="dialog-target">
      <ButtonComponent id="promptBtn" isPrimary onClick={buttonClick}>Prompt</ButtonComponent>
    </div>
  );
}
export default App;
```
