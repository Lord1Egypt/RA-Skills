# Templates – Syncfusion React Speed Dial

## Table of Contents
- [Overview](#overview)
- [Item Template](#item-template)
- [Popup Template](#popup-template)

---

## Overview

SpeedDial supports two template properties:

| Property | Scope | Use Case |
|----------|-------|----------|
| `itemTemplate` | Individual items | Custom item layout (badge, image, custom HTML) |
| `popupTemplate` | Entire popup | Fully replace popup content (forms, custom lists) |

Both accept JSX elements returned from a function.

---

## Item Template

Use `itemTemplate` to customize how each action item is rendered. The template function receives the item's data via `props.properties`:

```tsx
import { SpeedDialComponent, SpeedDialItemModel } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  const items: SpeedDialItemModel[] = [
    { iconCss: 'e-icons e-cut', text: 'Cut' },
    { iconCss: 'e-icons e-copy', text: 'Copy' },
    { iconCss: 'e-icons e-paste', text: 'Paste' }
  ];

  function itemTemplate(props: any): JSX.Element {
    const classname: string = "icon " + props.properties.iconCss;
    return (
      <div className="itemlist">
        <span className={classname}></span>
        <span className="text">{props.properties.text}</span>
      </div>
    );
  }

  return (
    <div>
      <div id="targetElement" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      <SpeedDialComponent id='speeddial' openIconCss='e-icons e-edit' content="Edit"
        items={items} itemTemplate={itemTemplate} target="#targetElement" />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

**CSS for the template:**

```css
.itemlist {
  display: flex;
  align-items: center;
  padding: 4px 8px;
}
.itemlist .icon {
  margin-right: 8px;
}
.itemlist .text {
  font-size: 14px;
}
```

> **Note:** Access item data via `props.properties` (not `props` directly) since the template receives the component's internal model.

---

## Popup Template

Use `popupTemplate` to replace the entire popup content with custom HTML. The items array is not rendered — you control all content:

```tsx
import { SpeedDialComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  function popupTemplate(): JSX.Element {
    return (
      <div>
        <div className="speeddial-form">
          <p>Here you can customize your code.</p>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div id="targetElement" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      <SpeedDialComponent id='speeddial' content="Edit" popupTemplate={popupTemplate} target="#targetElement" />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

> When `popupTemplate` is set, the `items` array and `itemTemplate` are not used — the popup renders only the template content.

**CSS for the popup template:**

```css
.speeddial-form {
  padding: 16px;
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}
```
