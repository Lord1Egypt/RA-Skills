# Switch Events and Methods

This file covers all events and programmatic methods available on the Syncfusion React Switch component. All APIs listed here are from the official documentation at `https://ej2.syncfusion.com/react/documentation/api/switch/`.

## Table of Contents
- [Events Overview](#events-overview)
- [change Event](#change-event)
- [beforeChange Event](#beforechange-event)
- [created Event](#created-event)
- [Methods Overview](#methods-overview)
- [toggle() Method](#toggle-method)
- [click() Method](#click-method)
- [focusIn() Method](#focusin-method)
- [destroy() Method](#destroy-method)
- [Using ref to Call Methods](#using-ref-to-call-methods)

---

## Events Overview

| Event | Argument Type | When It Fires |
|-------|--------------|---------------|
| `change` | `ChangeEventArgs` | After the user toggles the switch state |
| `beforeChange` | `BeforeChangeEventArgs` | Before the switch state changes (cancellable) |
| `created` | `Event` | Once the component finishes rendering |

---

## change Event

Fires every time the user toggles the Switch state. Use this to react to state changes, update application state, or trigger side effects.

**`ChangeEventArgs` properties:**
- `checked: boolean` — The new checked state after the change
- `event: Event` — The original DOM event
- `name: string` — Event name

```tsx
import { ChangeEventArgs, SwitchComponent } from '@syncfusion/ej2-react-buttons';
import { enableRipple } from '@syncfusion/ej2-base';

enableRipple(true);

function App() {
  function onChange(args: ChangeEventArgs): void {
    console.log('Switch is now:', args.checked ? 'ON' : 'OFF');
  }

  return (
    <SwitchComponent checked={false} change={onChange} />
  );
}
export default App;
```

---

## beforeChange Event

Fires **before** the Switch state changes. This event allows you to intercept, validate, or cancel the state transition. Set `args.cancel = true` to prevent the change.

**`BeforeChangeEventArgs` properties:**
- `cancel: boolean` — Set to `true` to cancel the state change
- `checked: boolean` — The current checked state before the change
- `event: Event` — The original DOM event that triggered the change

### Prevent all state changes
```tsx
import { BeforeChangeEventArgs, SwitchComponent } from '@syncfusion/ej2-react-buttons';
import { enableRipple } from '@syncfusion/ej2-base';

enableRipple(true);

function beforeChange(args: BeforeChangeEventArgs): void {
  // Cancel the state transition unconditionally
  args.cancel = true;
}

function App() {
  return (
    <SwitchComponent checked={true} beforeChange={beforeChange} />
  );
}
export default App;
```

### Conditionally prevent state changes
```tsx
import { BeforeChangeEventArgs, SwitchComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  function beforeChange(args: BeforeChangeEventArgs): void {
    // Prevent turning the switch OFF; allow turning ON
    if (args.checked === true) {
      args.cancel = true;
    }
  }

  return (
    <SwitchComponent checked={false} beforeChange={beforeChange} />
  );
}
```

---

## created Event

Fires once, after the component completes its initial rendering. Use this to perform setup operations that require the component to exist in the DOM.

```tsx
import { SwitchComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  function onCreated(): void {
    console.log('Switch component is ready');
  }

  return (
    <SwitchComponent created={onCreated} checked={false} />
  );
}
```

---

## Methods Overview

| Method | Returns | Description |
|--------|---------|-------------|
| `toggle()` | void | Toggles checked state between on and off |
| `click()` | void | Simulates a native click on the switch element |
| `focusIn()` | void | Sets focus to the switch element |
| `destroy()` | void | Destroys the switch widget and releases resources |

---

## toggle() Method

Programmatically switches the component between checked and unchecked states. Use this when you need external controls (buttons, keyboard shortcuts, data sync) to change the Switch state without direct user interaction.

The `change` event fires after `toggle()` is called.

```tsx
import { SwitchComponent } from '@syncfusion/ej2-react-buttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';

enableRipple(true);

function App() {
  let switchRef: SwitchComponent;

  function onCreated(): void {
    // Toggle the switch programmatically after creation
    switchRef.toggle();
  }

  return (
    <SwitchComponent
      id="switch"
      ref={(scope) => { switchRef = scope as SwitchComponent; }}
      checked={true}
      created={onCreated}
    />
  );
}
export default App;
```

### Toggle via external button
```tsx
import { useRef } from 'react';
import { SwitchComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  const switchRef = useRef<SwitchComponent>(null);

  function handleToggle(): void {
    switchRef.current?.toggle();
  }

  return (
    <>
      <SwitchComponent ref={switchRef} checked={false} />
      <button onClick={handleToggle}>Toggle Switch</button>
    </>
  );
}
```

---

## click() Method

Triggers the Switch's native click behavior programmatically.

```tsx
function App() {
  let switchRef: SwitchComponent;

  function handleClick(): void {
    switchRef.click();
  }

  return (
    <>
      <SwitchComponent ref={(scope) => { switchRef = scope as SwitchComponent; }} />
      <button onClick={handleClick}>Click Switch</button>
    </>
  );
}
```

---

## focusIn() Method

Programmatically sets focus to the Switch component. Use for accessibility workflows where focus needs to move to the switch after a user action.

```tsx
function App() {
  let switchRef: SwitchComponent;

  function focusSwitch(): void {
    switchRef.focusIn();
  }

  return (
    <>
      <SwitchComponent ref={(scope) => { switchRef = scope as SwitchComponent; }} />
      <button onClick={focusSwitch}>Focus Switch</button>
    </>
  );
}
```

---

## destroy() Method

Destroys the Switch widget and cleans up all event listeners and DOM references. Call this during component unmount if managing the Switch lifecycle manually.

```tsx
function App() {
  let switchRef: SwitchComponent;

  function handleDestroy(): void {
    switchRef.destroy();
  }

  return (
    <>
      <SwitchComponent ref={(scope) => { switchRef = scope as SwitchComponent; }} checked={true} />
      <button onClick={handleDestroy}>Destroy Switch</button>
    </>
  );
}
```

---

## Using ref to Call Methods

Access Switch methods using a React `ref`. Two patterns are supported:

**Pattern 1: Callback ref (works in both class and function components)**
```tsx
let switchInstance: SwitchComponent;

<SwitchComponent ref={(scope) => { switchInstance = scope as SwitchComponent; }} />

// Later:
switchInstance.toggle();
```

**Pattern 2: useRef hook (function components)**
```tsx
import { useRef } from 'react';

const switchRef = useRef<SwitchComponent>(null);

<SwitchComponent ref={switchRef} />

// Later:
switchRef.current?.toggle();
```
