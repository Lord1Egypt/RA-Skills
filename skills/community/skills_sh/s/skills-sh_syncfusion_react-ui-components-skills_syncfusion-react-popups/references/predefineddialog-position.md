# Position in React Predefined Dialogs

## Table of Contents
- [Overview](#overview)
- [Alert Position](#alert-position)
- [Confirm Position](#confirm-position)
- [Prompt Position](#prompt-position)

---

## Overview

The `position` property accepts a `PositionDataModel` with `X` and `Y` values:

| Key | Values |
|-----|--------|
| `X` | `'left'`, `'center'`, `'right'`, or a numeric pixel offset |
| `Y` | `'top'`, `'center'`, `'bottom'`, or a numeric pixel offset |

Default: `{ X: 'center', Y: 'center' }`.

---

## Alert Position

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
      position: { X: 'center', Y: 'center' },
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

## Confirm Position

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
      position: { X: 'center', Y: 'center' },
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

## Prompt Position

```tsx
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { DialogUtility } from '@syncfusion/ej2-react-popups';
import * as React from 'react';

function App() {
  function buttonClick() {
    DialogUtility.confirm({
      title: 'Join Chat Group',
      width: '300px',
      content: '<p>Enter your name:</p><input type="text" class="e-input" placeholder="Type here.." />',
      position: { X: 'center', Y: 'center' },
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
