# Events and Interactivity — Syncfusion React DropDownButton

## Table of Contents
- [Handling Item Selection (select)](#handling-item-selection-select)
- [Dynamic Caret Icon (beforeOpen / beforeClose)](#dynamic-caret-icon-beforeopen--beforeclose)
- [Custom Popup Position (open)](#custom-popup-position-open)
- [Disable the Button](#disable-the-button)
- [RTL Support](#rtl-support)
- [Open a Dialog on Item Select](#open-a-dialog-on-item-select)
- [Dynamic Item Management (addItems / removeItems)](#dynamic-item-management-additems--removeitems)
- [Programmatic Toggle (toggle)](#programmatic-toggle-toggle)

---

## Handling Item Selection (select)

The `select` event fires when the user clicks a popup item. The `MenuEventArgs` argument provides `args.item` (the selected `ItemModel`) and `args.element` (the DOM element).

```tsx
import { DropDownButtonComponent, ItemModel, MenuEventArgs } from '@syncfusion/ej2-react-splitbuttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';

enableRipple(true);

function App() {
  const items: ItemModel[] = [
    { text: 'Cut' }, { text: 'Copy' }, { text: 'Paste' },
  ];

  function onSelect(args: MenuEventArgs) {
    console.log('Selected item:', args.item.text);
  }

  return (
    <DropDownButtonComponent items={items} select={onSelect}>
      Clipboard
    </DropDownButtonComponent>
  );
}

export default App;
```

---

## Dynamic Caret Icon (beforeOpen / beforeClose)

Use `beforeOpen` and `beforeClose` to change the caret appearance when the popup opens and closes. Mutate `cssClass` on the component instance via a `ref`.

```tsx
import { DropDownButtonComponent, ItemModel } from '@syncfusion/ej2-react-splitbuttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';

enableRipple(true);

function App() {
  let ddb: DropDownButtonComponent;
  const items: ItemModel[] = [
    { text: 'Cut' }, { text: 'Copy' }, { text: 'Paste' },
  ];

  function beforeOpen() {
    ddb.cssClass = 'e-caret-up'; // Flip caret upward when open
  }

  function beforeClose() {
    ddb.cssClass = ''; // Restore default caret when closed
  }

  return (
    <DropDownButtonComponent
      ref={(scope) => { ddb = scope as DropDownButtonComponent; }}
      items={items}
      beforeOpen={beforeOpen}
      beforeClose={beforeClose}
    >
      Clipboard
    </DropDownButtonComponent>
  );
}

export default App;
```

> `e-caret-up` is a Syncfusion utility class that rotates the arrow icon 180°.

---

## Custom Popup Position (open)

The `open` event fires after the popup is positioned. Use `args.element.parentElement` to access the popup wrapper and adjust `top`/`left` via inline styles.

```tsx
import { DropDownButtonComponent, ItemModel, OpenCloseMenuEventArgs } from '@syncfusion/ej2-react-splitbuttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';

enableRipple(true);

function App() {
  let ddb: DropDownButtonComponent;
  const items: ItemModel[] = [
    { text: 'Cut' }, { text: 'Copy' }, { text: 'Paste' },
  ];

  function onOpen(args: OpenCloseMenuEventArgs) {
    const popup = args.element.parentElement as HTMLElement;
    // Position popup above the button
    popup.style.top =
      ddb.element.getBoundingClientRect().top - popup.offsetHeight + 'px';
  }

  return (
    <DropDownButtonComponent
      ref={(scope) => { ddb = scope as DropDownButtonComponent; }}
      items={items}
      open={onOpen}
      cssClass="e-caret-up"
    >
      Clipboard
    </DropDownButtonComponent>
  );
}

export default App;
```

---

## Disable the Button

Set `disabled={true}` to make the button non-interactive. A disabled button cannot receive focus or trigger events.

```tsx
import { DropDownButtonComponent, ItemModel } from '@syncfusion/ej2-react-splitbuttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';

enableRipple(true);

function App() {
  const items: ItemModel[] = [
    { text: 'Edit' }, { text: 'Delete' },
    { text: 'Mark as Read' }, { text: 'Like Message' },
  ];

  return (
    <DropDownButtonComponent
      items={items}
      iconCss="ddb-icons e-message"
      disabled={true}
    >
      Message
    </DropDownButtonComponent>
  );
}

export default App;
```

To re-enable dynamically, update the `disabled` prop or set `instance.disabled = false` via a ref.

---

## RTL Support

Set `enableRtl={true}` to render the button and popup in right-to-left direction, suitable for Arabic, Hebrew, and similar locales.

```tsx
import { DropDownButtonComponent, ItemModel } from '@syncfusion/ej2-react-splitbuttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';

enableRipple(true);

function App() {
  const items: ItemModel[] = [
    { text: 'Edit' }, { text: 'Delete' },
    { text: 'Mark as Read' }, { text: 'Like Message' },
  ];

  return (
    <DropDownButtonComponent
      items={items}
      iconCss="ddb-icons e-message"
      enableRtl={true}
    >
      Message
    </DropDownButtonComponent>
  );
}

export default App;
```

---

## Open a Dialog on Item Select

Combine the `select` event with a Dialog component to show a modal when a specific item is chosen.

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { DialogComponent } from '@syncfusion/ej2-react-popups';
import { DropDownButtonComponent, ItemModel, MenuEventArgs } from '@syncfusion/ej2-react-splitbuttons';
import * as React from 'react';

enableRipple(true);

function App() {
  let dialog: DialogComponent;
  const position = { X: 100, Y: 100 };

  const alertDlgButtons = [{
    buttonModel: { content: 'Submit', cssClass: 'e-flat', isPrimary: true },
    click: () => { dialog.hide(); },
  }];

  const items: ItemModel[] = [
    { text: 'Archive' }, { text: 'Inbox' }, { text: 'HR Portal' },
    { separator: true },
    { text: 'Other Folder...' }, { text: 'Copy to Folder' },
  ];

  function onSelect(args: MenuEventArgs) {
    if (args.item.text === 'Other Folder...') {
      dialog.show();
    }
  }

  return (
    <div>
      <DialogComponent
        ref={(scope) => { dialog = scope as DialogComponent; }}
        width="250px"
        id="dialog"
        content='Move Items To "Web Team"'
        header="Move Items"
        buttons={alertDlgButtons}
        position={position}
        visible={false}
      />
      <DropDownButtonComponent
        items={items}
        select={onSelect}
        iconCss="ddb-icons e-folder"
        cssClass="e-vertical"
        iconPosition="Top"
      >
        Move
      </DropDownButtonComponent>
    </div>
  );
}

export default App;
```

---

## Dynamic Item Management (addItems / removeItems)

Use the component's methods to add or remove items at runtime via a ref.

```tsx
import { DropDownButtonComponent, ItemModel } from '@syncfusion/ej2-react-splitbuttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';

enableRipple(true);

function App() {
  let ddb: DropDownButtonComponent;
  const items: ItemModel[] = [
    { text: 'Cut' }, { text: 'Copy' }, { text: 'Paste' },
  ];

  function addItem() {
    // Append a new item at the end
    ddb.addItems([{ text: 'Select All' }]);
  }

  function addBeforeItem() {
    // Insert before 'Copy'
    ddb.addItems([{ text: 'Undo' }], 'Copy');
  }

  function removeItem() {
    // Remove by text
    ddb.removeItems(['Paste']);
  }

  return (
    <div>
      <DropDownButtonComponent
        ref={(scope) => { ddb = scope as DropDownButtonComponent; }}
        items={items}
      >
        Clipboard
      </DropDownButtonComponent>
      <button onClick={addItem}>Add item</button>
      <button onClick={addBeforeItem}>Insert before Copy</button>
      <button onClick={removeItem}>Remove Paste</button>
    </div>
  );
}

export default App;
```

**Method signatures:**
- `addItems(items: ItemModel[], text?: string): void` — appends items or inserts before the item matching `text`
- `removeItems(items: string[], isUniqueId?: boolean): void` — removes items by text (or by `id` when `isUniqueId` is `true`)

---

## Programmatic Toggle (toggle)

Call `toggle()` on the component instance to open the popup if closed, or close it if open.

```tsx
function App() {
  let ddb: DropDownButtonComponent;
  const items: ItemModel[] = [
    { text: 'Cut' }, { text: 'Copy' }, { text: 'Paste' },
  ];

  return (
    <div>
      <DropDownButtonComponent
        ref={(scope) => { ddb = scope as DropDownButtonComponent; }}
        items={items}
      >
        Clipboard
      </DropDownButtonComponent>
      <button onClick={() => ddb.toggle()}>Toggle Popup</button>
    </div>
  );
}
```
