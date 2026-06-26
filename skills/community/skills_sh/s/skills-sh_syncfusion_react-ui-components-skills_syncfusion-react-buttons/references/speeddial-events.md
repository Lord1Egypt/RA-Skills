# Events – Syncfusion React Speed Dial

## Table of Contents
- [Event Overview](#event-overview)
- [clicked](#clicked)
- [created](#created)
- [beforeOpen](#beforeopen)
- [onOpen](#onopen)
- [beforeClose](#beforeclose)
- [onClose](#onclose)
- [beforeItemRender](#beforeitemrender)
- [Cancel Pattern](#cancel-pattern)

---

## Event Overview

| Event | Trigger | Args Type |
|-------|---------|-----------|
| `clicked` | User clicks an action item | `SpeedDialItemEventArgs` |
| `created` | Component finishes rendering | `Event` |
| `beforeOpen` | Before popup opens | `SpeedDialBeforeOpenCloseEventArgs` |
| `onOpen` | After popup opens | `SpeedDialOpenCloseEventArgs` |
| `beforeClose` | Before popup closes | `SpeedDialBeforeOpenCloseEventArgs` |
| `onClose` | After popup closes | `SpeedDialOpenCloseEventArgs` |
| `beforeItemRender` | Before each item renders | `SpeedDialItemEventArgs` |

---

## clicked

Fires when the user clicks any action item. Use `args.item` to identify which item was clicked:

```tsx
import { SpeedDialComponent, SpeedDialItemModel, SpeedDialItemEventArgs } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  const items: SpeedDialItemModel[] = [
    { text: 'Cut' },
    { text: 'Copy' },
    { text: 'Paste' }
  ];

  function itemClick(args: SpeedDialItemEventArgs): void {
    alert(args.item.text + ' is clicked');
  }

  return (
    <div>
      <div id="targetElement" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      <SpeedDialComponent id='speeddial' items={items} content='Edit'
        target='#targetElement' clicked={itemClick} />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

---

## created

Fires after the SpeedDial is fully initialized and rendered. Use this to run setup code that needs the component to exist:

```tsx
import { SpeedDialComponent, SpeedDialItemModel } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  const items: SpeedDialItemModel[] = [
    { text: 'Cut' },
    { text: 'Copy' },
    { text: 'Paste' }
  ];

  function created(): void {
    // Component is ready — run initialization logic here
  }

  return (
    <SpeedDialComponent id='speeddial' items={items} content='Edit' created={created} />
  );
}
export default App;
```

---

## beforeOpen

Fires before the popup opens. Set `args.cancel = true` to prevent the popup from opening:

```tsx
import { SpeedDialComponent, SpeedDialItemModel, SpeedDialBeforeOpenCloseEventArgs } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  const items: SpeedDialItemModel[] = [
    { text: 'Cut' },
    { text: 'Copy' },
    { text: 'Paste' }
  ];

  function beforeOpen(args: SpeedDialBeforeOpenCloseEventArgs): void {
    // Conditionally prevent opening:
    // args.cancel = true;
  }

  return (
    <SpeedDialComponent id='speeddial' items={items} content='Edit' beforeOpen={beforeOpen} />
  );
}
export default App;
```

---

## onOpen

Fires after the popup opens. Use this to track open state or trigger dependent UI changes:

```tsx
import { SpeedDialComponent, SpeedDialItemModel, SpeedDialOpenCloseEventArgs } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  const items: SpeedDialItemModel[] = [
    { text: 'Cut' },
    { text: 'Copy' },
    { text: 'Paste' }
  ];

  function onOpen(args: SpeedDialOpenCloseEventArgs): void {
    console.log('Speed Dial opened');
  }

  return (
    <SpeedDialComponent id='speeddial' items={items} content='Edit' onOpen={onOpen} />
  );
}
export default App;
```

---

## beforeClose

Fires before the popup closes. Set `args.cancel = true` to keep the popup open:

```tsx
import { SpeedDialComponent, SpeedDialItemModel, SpeedDialBeforeOpenCloseEventArgs } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  const items: SpeedDialItemModel[] = [
    { text: 'Cut' },
    { text: 'Copy' },
    { text: 'Paste' }
  ];

  function beforeClose(args: SpeedDialBeforeOpenCloseEventArgs): void {
    // Prevent closing: args.cancel = true;
  }

  return (
    <SpeedDialComponent id='speeddial' items={items} content='Edit' beforeClose={beforeClose} />
  );
}
export default App;
```

---

## onClose

Fires after the popup closes. Use for cleanup or state updates:

```tsx
import { SpeedDialComponent, SpeedDialItemModel, SpeedDialOpenCloseEventArgs } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  const items: SpeedDialItemModel[] = [
    { text: 'Cut' },
    { text: 'Copy' },
    { text: 'Paste' }
  ];

  function onClose(args: SpeedDialOpenCloseEventArgs): void {
    console.log('Speed Dial closed');
  }

  return (
    <SpeedDialComponent id='speeddial' items={items} content='Edit' onClose={onClose} />
  );
}
export default App;
```

---

## beforeItemRender

Fires for each item before it is rendered into the popup. Use this to modify item data or apply conditional styles:

```tsx
import { SpeedDialComponent, SpeedDialItemModel, SpeedDialItemEventArgs } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  const items: SpeedDialItemModel[] = [
    { text: 'Cut' },
    { text: 'Copy' },
    { text: 'Paste' }
  ];

  function beforeItemRender(args: SpeedDialItemEventArgs): void {
    // Access args.item to inspect or modify item data before render
  }

  return (
    <SpeedDialComponent id='speeddial' items={items} content='Edit'
      beforeItemRender={beforeItemRender} />
  );
}
export default App;
```

---

## Cancel Pattern

Both `beforeOpen` and `beforeClose` provide a `cancel` property on their event args. Setting it to `true` stops the action:

```tsx
function beforeOpen(args: SpeedDialBeforeOpenCloseEventArgs): void {
  const isBlocked = true; // your condition
  if (isBlocked) {
    args.cancel = true; // popup will NOT open
  }
}

function beforeClose(args: SpeedDialBeforeOpenCloseEventArgs): void {
  const hasUnsavedWork = true; // your condition
  if (hasUnsavedWork) {
    args.cancel = true; // popup will NOT close
  }
}
```
