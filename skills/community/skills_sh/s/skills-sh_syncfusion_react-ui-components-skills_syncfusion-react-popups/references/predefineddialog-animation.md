# Animation in React Predefined Dialogs

## Table of Contents
- [Overview](#overview)
- [Alert Animation](#alert-animation)
- [Confirm Animation](#confirm-animation)
- [Prompt Animation](#prompt-animation)

---

## Overview

Predefined dialogs support open/close animations via the `animationSettings` property.
The `animationSettings` object accepts:
- `effect` — animation effect name (e.g. `'Zoom'`, `'Fade'`, `'FlipXDown'`, etc.)
- `duration` — duration in milliseconds (optional)
- `delay` — delay before animation starts in milliseconds (optional)

Pass `animationSettings` inside the options object of `DialogUtility.alert()` or `DialogUtility.confirm()`.

---

## Alert Animation

```tsx
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { DialogUtility } from '@syncfusion/ej2-react-popups';
import * as React from 'react';

function App() {
  function buttonClick() {
    DialogUtility.alert({
      title: 'Low Battery',
      width: '250px',
      content: '10% of battery remaining',
      animationSettings: { effect: 'Zoom' },
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

## Confirm Animation

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
      animationSettings: { effect: 'Zoom' },
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

## Prompt Animation

```tsx
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { DialogUtility } from '@syncfusion/ej2-react-popups';
import * as React from 'react';

function App() {
  function buttonClick() {
    DialogUtility.confirm({
      title: 'Join Chat Group',
      width: '300px',
      content: '<p>Enter your name:</p> <input type="text" class="e-input" placeholder="Type here.." />',
      animationSettings: { effect: 'Zoom' },
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
