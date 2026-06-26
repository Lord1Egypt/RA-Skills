# Dimension in React Predefined Dialogs

## Table of Contents
- [Overview](#overview)
- [Alert Dimension](#alert-dimension)
- [Confirm Dimension](#confirm-dimension)
- [Prompt Dimension](#prompt-dimension)
- [Max-width and Max-height](#max-width-and-max-height)
- [Min-width and Min-height](#min-width-and-min-height)

---

## Overview

Use `width` and `height` in the options passed to `DialogUtility.alert()` or `DialogUtility.confirm()`
to set the dialog dimensions. Values can be strings (`'250px'`, `'50%'`) or numbers.

For max/min constraints, use the `cssClass` property with custom CSS rules on the class.

---

## Alert Dimension

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
      height: '200px',
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

## Confirm Dimension

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
      height: '200px',
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

## Prompt Dimension

```tsx
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { DialogUtility } from '@syncfusion/ej2-react-popups';
import * as React from 'react';

function App() {
  function buttonClick() {
    DialogUtility.confirm({
      title: 'Join Chat Group',
      content: '<p>Enter your name:</p> <input type="text" class="e-input" placeholder="Type here.." />',
      height: '250px',
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

---

## Max-width and Max-height

To restrict maximum dialog dimensions, set `cssClass` and define `max-width` / `max-height` in CSS for that class.

```tsx
// In App.css or component styles:
// .customClass { max-width: 400px; max-height: 300px; }

DialogUtility.alert({
  title: 'About Syncfusion Succinctly Series',
  content: 'In the Succinctly series, Syncfusion created a robust, free library...',
  cssClass: 'customClass',
});
```

---

## Min-width and Min-height

Similarly, set `min-width` / `min-height` in the CSS class and apply via `cssClass`.

```tsx
// In App.css:
// .customClass { min-width: 200px; min-height: 150px; }

DialogUtility.alert({
  title: 'About Syncfusion Succinctly Series',
  content: 'The Succinctly series was born in 2012...',
  cssClass: 'customClass',
});
```
