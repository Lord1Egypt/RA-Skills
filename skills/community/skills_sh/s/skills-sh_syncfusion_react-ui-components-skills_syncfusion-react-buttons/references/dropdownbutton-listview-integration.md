# ListView Integration — Syncfusion React DropDownButton

Use the `target` property to replace the DropDownButton's default popup with a Syncfusion `ListViewComponent`. This enables grouped items with category headers, checkboxes, and other ListView features.

## Installation

The ListView component is part of the `@syncfusion/ej2-react-lists` package:

```bash
npm install @syncfusion/ej2-react-lists --save
```

Add the CSS import:

```css
@import "../node_modules/@syncfusion/ej2-lists/styles/tailwind3.css";
```

## Grouped Popup Items with ListView

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { ListViewComponent } from '@syncfusion/ej2-react-lists';
import { DropDownButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import * as React from 'react';

enableRipple(true);

function App() {
  const data: Array<{ [key: string]: string }> = [
    { class: 'data', text: 'Print',         id: 'data1', category: 'Customize Quick Access Toolbar' },
    { class: 'data', text: 'Save As',        id: 'data2', category: 'Customize Quick Access Toolbar' },
    { class: 'data', text: 'Update Folder',  id: 'data3', category: 'Customize Quick Access Toolbar' },
    { class: 'data', text: 'Reply',          id: 'data4', category: 'Customize Quick Access Toolbar' },
  ];

  const field: { [key: string]: string } = { text: 'text', groupBy: 'category' };

  return (
    <div>
      <ListViewComponent
        id="listview"
        dataSource={data}
        fields={field}
        showCheckBox={true}
      />
      <DropDownButtonComponent
        target="#listview"
        iconCss="e-icons e-down"
        cssClass="e-caret-hide"
      />
    </div>
  );
}

export default App;
```

## How it works

- The `target` value (`"#listview"`) points to the ListView's DOM `id`.
- When the DropDownButton is clicked, it renders the referenced element as the popup content instead of a default item list.
- `cssClass="e-caret-hide"` hides the default caret when using a custom target.
- The `items` property on `DropDownButtonComponent` is ignored when `target` is set.

## Gotchas

- The `target` element must exist in the DOM before the DropDownButton renders. Place it above (or as a sibling to) the DropDownButton in the JSX.
- ListView's `groupBy` field must match a property name present in each data item.
- To handle item selection from the ListView, attach an event listener on the `ListViewComponent` (`select` event), not on the `DropDownButtonComponent`.
