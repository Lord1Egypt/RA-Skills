# Popup Items — Syncfusion React DropDownButton

## Table of Contents
- [Icons on Popup Items](#icons-on-popup-items)
- [Navigation URLs](#navigation-urls)
- [Separators](#separators)
- [Item Templating with beforeItemRender](#item-templating-with-beforeitemrender)
- [Popup Templating with target](#popup-templating-with-target)
- [Underline a Character in Item Text](#underline-a-character-in-item-text)

---

## Icons on Popup Items

Set `iconCss` on each `ItemModel` to add an icon. The icon appears to the left of the item text by default.

```tsx
import { DropDownButtonComponent, ItemModel } from '@syncfusion/ej2-react-splitbuttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';

enableRipple(true);

function App() {
  const items: ItemModel[] = [
    { text: 'Edit',          iconCss: 'ddb-icons e-edit' },
    { text: 'Delete',        iconCss: 'ddb-icons e-delete' },
    { text: 'Mark As Read',  iconCss: 'ddb-icons e-read' },
    { text: 'Like Message',  iconCss: 'ddb-icons e-like' },
  ];

  return (
    <DropDownButtonComponent items={items} iconCss="ddb-icons e-message">
      Message
    </DropDownButtonComponent>
  );
}

export default App;
```

---

## Navigation URLs

Provide a `url` on an `ItemModel` to make the item navigate to a web page. Use the `beforeItemRender` event to set `target="_blank"` on the generated anchor tag.

```tsx
import { DropDownButtonComponent, ItemModel, MenuEventArgs } from '@syncfusion/ej2-react-splitbuttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';

enableRipple(true);

function App() {
  const items: ItemModel[] = [
    { text: 'Flipkart', iconCss: 'e-cart-icon e-link', url: 'https://www.google.co.in/search?q=flipkart' },
    { text: 'Amazon',   iconCss: 'e-cart-icon e-link', url: 'https://www.google.co.in/search?q=amazon' },
    { text: 'Snapdeal', iconCss: 'e-cart-icon e-link', url: 'https://www.google.co.in/search?q=snapdeal' },
  ];

  function itemBeforeEvent(args: MenuEventArgs) {
    args.element.getElementsByTagName('a')[0].setAttribute('target', '_blank');
  }

  return (
    <DropDownButtonComponent
      items={items}
      iconCss="e-cart-icon e-shopping"
      beforeItemRender={itemBeforeEvent}
    >
      Shop By
    </DropDownButtonComponent>
  );
}

export default App;
```

---

## Separators

Add a separator item (`{ separator: true }`) to visually group related popup items with a horizontal line. Separators cannot be selected.

```tsx
import { DropDownButtonComponent, ItemModel } from '@syncfusion/ej2-react-splitbuttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';

enableRipple(true);

function App() {
  const items: ItemModel[] = [
    { text: 'Cut',       iconCss: 'e-db-icons e-cut' },
    { text: 'Copy',      iconCss: 'e-icons e-copy' },
    { text: 'Paste',     iconCss: 'e-db-icons e-paste' },
    { separator: true },
    { text: 'Font',      iconCss: 'e-db-icons e-font' },
    { text: 'Paragraph', iconCss: 'e-db-icons e-paragraph' },
  ];

  return (
    <DropDownButtonComponent items={items} iconCss="e-icons e-edit">
      Clipboard
    </DropDownButtonComponent>
  );
}

export default App;
```

---

## Item Templating with beforeItemRender

The `beforeItemRender` event fires once per popup item during rendering. Use it to inject custom HTML into each item element — useful for rich layouts with descriptions, multiple lines, or custom icons.

```tsx
import { DropDownButtonComponent, ItemModel, MenuEventArgs } from '@syncfusion/ej2-react-splitbuttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';

enableRipple(true);

function App() {
  const items: ItemModel[] = [
    { text: 'Edit' },
    { text: 'Cut' },
  ];

  function itemBeforeEvent(args: MenuEventArgs) {
    if (args.item.text === 'Edit') {
      args.element.innerHTML =
        '<span></span><div><b>Paste Text</b><div>Provides option to paste only the<br>selected text.</div></div>';
      args.element.style.height = '80px';
      args.element.children[0].setAttribute('class', 'e-cm-icons e-pastetext e-align');
      (args.element.children[1] as HTMLElement).setAttribute('class', 'e-div-align');
    } else {
      args.element.innerHTML =
        '<span></span><div><b>Paste Special</b><div>Provides options to paste formulas,<br> values, comments, validations etc...</div></div>';
      args.element.style.height = '80px';
      args.element.children[0].setAttribute('class', 'e-cm-icons e-pastespecial e-align');
      (args.element.children[1] as HTMLElement).setAttribute('class', 'e-div-align');
    }
  }

  return (
    <DropDownButtonComponent
      items={items}
      iconCss="e-ddb-icons e-paste"
      cssClass="e-vertical"
      iconPosition="Top"
      beforeItemRender={itemBeforeEvent}
    >
      Paste
    </DropDownButtonComponent>
  );
}

export default App;
```

> **Tip:** When using `beforeItemRender` for underline, set `args.element.innerHTML` directly. See the [Underline a Character](#underline-a-character-in-item-text) section below.

---

## Popup Templating with target

Replace the entire popup with a custom HTML element by setting the `target` property to the element's selector or element reference. The DropDownButton renders the targeted element inside the popup instead of the default list.

```tsx
import { DropDownButtonComponent, MenuEventArgs } from '@syncfusion/ej2-react-splitbuttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';

enableRipple(true);

function App() {
  function itemBeforeEvent(args: MenuEventArgs) {
    args.element.style.height = '105px';
  }

  return (
    <div>
      {/* Custom popup template */}
      <div id="target">
        <table>
          <caption><b>Insert Table</b></caption>
          <tbody>
            {[...Array(6)].map((_, r) => (
              <tr key={r} className="e-row">
                {[...Array(6)].map((_, c) => <td key={c} className="e-data" />)}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <DropDownButtonComponent
        target="#target"
        iconCss="e-icons e-table"
        iconPosition="Top"
        cssClass="e-vertical"
        beforeItemRender={itemBeforeEvent}
      >
        Table
      </DropDownButtonComponent>
    </div>
  );
}

export default App;
```

> When `target` is set, the `items` property is ignored — the target element is used directly as the popup content.

---

## Underline a Character in Item Text

Use `beforeItemRender` to wrap a specific character in a `<u>` tag for keyboard shortcut hints.

```tsx
import { DropDownButtonComponent, ItemModel, MenuEventArgs } from '@syncfusion/ej2-react-splitbuttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';

enableRipple(true);

function App() {
  const items: ItemModel[] = [
    { text: 'Cut' },
    { text: 'Copy' },
    { text: 'Paste' },
  ];

  function itemRender(args: MenuEventArgs) {
    if (args.item.text === 'Copy') {
      // Underline the first character 'C'
      args.element.innerHTML = '<u>C</u>opy';
    }
  }

  return (
    <DropDownButtonComponent items={items} beforeItemRender={itemRender}>
      Clipboard
    </DropDownButtonComponent>
  );
}

export default App;
```
