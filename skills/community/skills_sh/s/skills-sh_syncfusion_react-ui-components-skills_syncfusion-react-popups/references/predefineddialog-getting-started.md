# Getting Started with React Predefined Dialogs

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [CSS Reference](#css-reference)
- [Alert Dialog](#alert-dialog)
- [Confirm Dialog](#confirm-dialog)
- [Prompt Dialog](#prompt-dialog)

---

## Overview

Syncfusion Predefined Dialogs are opened using the **`DialogUtility`** utility class from
`@syncfusion/ej2-react-popups`. There is no JSX component tag — all three dialog types (alert,
confirm, prompt) are invoked imperatively.

---

## Installation

```bash
npm install @syncfusion/ej2-react-popups --save
```

---

## CSS Reference

Add the following CSS imports in `src/App.css`:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-buttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-popups/styles/tailwind3.css";
```

Then import `App.css` in `src/App.tsx`.

---

## Alert Dialog

An alert dialog displays a message with an **OK** button. Use `DialogUtility.alert()`.

```tsx
// Functional component
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { DialogUtility } from '@syncfusion/ej2-react-popups';
import * as React from 'react';

let dialogObj: any;

function App() {
  function buttonClick() {
    document.getElementById('statusText')!.style.display = 'none';
    dialogObj = DialogUtility.alert({
      title: 'Low Battery',
      width: '250px',
      content: '10% of battery remaining',
      okButton: { click: alertOkAction },
    });
  }
  function alertOkAction() {
    dialogObj.hide();
    document.getElementById('statusText')!.innerHTML = 'The user closed the Alert dialog.';
    document.getElementById('statusText')!.style.display = 'block';
  }
  return (
    <div className="App" id="dialog-target">
      <ButtonComponent id="alertBtn" cssClass="e-danger" onClick={buttonClick}>Alert</ButtonComponent>
      <span id="statusText"></span>
    </div>
  );
}
export default App;
```

---

## Confirm Dialog

A confirm dialog displays a message with **OK** and **Cancel** buttons. Use `DialogUtility.confirm()`.

```tsx
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { DialogUtility } from '@syncfusion/ej2-react-popups';
import * as React from 'react';

let dialogObj: any;

function App() {
  function buttonClick() {
    document.getElementById('statusText')!.style.display = 'none';
    dialogObj = DialogUtility.confirm({
      title: 'Delete Multiple Items',
      content: 'Are you sure you want to permanently delete these items?',
      width: '300px',
      okButton: { click: confirmOkAction },
      cancelButton: { click: confirmCancelAction },
    });
  }
  function confirmOkAction() {
    dialogObj.hide();
    document.getElementById('statusText')!.innerHTML = 'The user confirmed the dialog box.';
    document.getElementById('statusText')!.style.display = 'block';
  }
  function confirmCancelAction() {
    dialogObj.hide();
    document.getElementById('statusText')!.innerHTML = 'The user canceled the dialog box.';
    document.getElementById('statusText')!.style.display = 'block';
  }
  return (
    <div className="App" id="dialog-target">
      <ButtonComponent id="confirmBtn" cssClass="e-success" onClick={buttonClick}>Confirm</ButtonComponent>
      <span id="statusText"></span>
    </div>
  );
}
export default App;
```

---

## Prompt Dialog

A prompt dialog collects input from the user. Use `DialogUtility.confirm()` with an `<input>` element in `content`.

```tsx
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { DialogUtility } from '@syncfusion/ej2-react-popups';
import * as React from 'react';

let dialogObj: any;

function App() {
  function buttonClick() {
    document.getElementById('statusText')!.style.display = 'none';
    dialogObj = DialogUtility.confirm({
      title: 'Join Chat Group',
      width: '300px',
      content: '<p>Enter your name:</p> <input id="inputEle" type="text" class="e-input" placeholder="Type here.." />',
      okButton: { click: promptOkAction },
      cancelButton: { click: promptCancelAction },
    });
  }
  function promptOkAction() {
    const value = (document.getElementById('inputEle') as HTMLInputElement).value;
    dialogObj.hide();
    document.getElementById('statusText')!.innerHTML =
      value === '' ? 'The user\'s input is returned as ""' : `The user's input is returned as ${value}`;
    document.getElementById('statusText')!.style.display = 'block';
  }
  function promptCancelAction() {
    dialogObj.hide();
    document.getElementById('statusText')!.innerHTML = 'The user canceled the prompt dialog.';
    document.getElementById('statusText')!.style.display = 'block';
  }
  return (
    <div className="App" id="dialog-target">
      <ButtonComponent id="promptBtn" isPrimary onClick={buttonClick}>Prompt</ButtonComponent>
      <span id="statusText"></span>
    </div>
  );
}
export default App;
```

> **Note:** The return value of `DialogUtility.alert()` / `DialogUtility.confirm()` is a dialog instance.
> Call `.hide()` on it to close the dialog programmatically.
