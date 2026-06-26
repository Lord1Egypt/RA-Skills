# Draggable Predefined Dialogs (React)

## Table of Contents
- [Overview](#overview)
- [Alert Dragging](#alert-dragging)
- [Confirm Dragging](#confirm-dragging)
- [Prompt Dragging](#prompt-dragging)

---

## Overview

Set `isDraggable: true` in the options object passed to `DialogUtility.alert()` or
`DialogUtility.confirm()` to allow users to drag the dialog by its header.

---

## Alert Dragging

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
      isDraggable: true,
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

## Confirm Dragging

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
      isDraggable: true,
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

## Prompt Dragging

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
      isDraggable: true,
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
