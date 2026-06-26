# Item Template — Syncfusion React DropDownButton

The `itemTemplate` property lets you define a React render function that replaces the default item rendering for every popup item. Use it when you need rich content (links, icons, formatted text, custom layouts) inside each item.

## Basic itemTemplate Usage

```tsx
import { DropDownButtonComponent, ItemModel } from '@syncfusion/ej2-react-splitbuttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';

enableRipple(true);

function App() {
  const items: ItemModel[] = [
    { text: 'Home',      iconCss: 'e-icons e-home' },
    { text: 'Search',    iconCss: 'e-icons e-search',        url: 'http://www.google.com' },
    { text: 'Yes / No',  iconCss: 'e-icons e-check-box' },
    { text: 'Text',      iconCss: 'e-icons e-caption' },
    { separator: true },
    { text: 'Syncfusion', iconCss: 'e-icons e-mouse-pointer', url: 'http://www.syncfusion.com' },
  ];

  function itemTemplate(data: any): JSX.Element {
    if (data.properties.url) {
      return (
        <div>
          <span className={`e-menu-icon ${data.properties.iconCss}`}></span>
          <span className="custom-class">
            <a href={data.properties.url} target="_blank" rel="noopener noreferrer">
              {data.properties.text}
            </a>
          </span>
        </div>
      );
    }
    return (
      <div>
        <span className={`e-menu-icon ${data.properties.iconCss}`}></span>
        <span className="custom-class">{data.properties.text}</span>
      </div>
    );
  }

  return (
    <DropDownButtonComponent items={items} itemTemplate={itemTemplate}>
      DropDownButton
    </DropDownButtonComponent>
  );
}

export default App;
```

## Key Notes

- `data.properties` exposes the `ItemModel` fields (`text`, `iconCss`, `url`, `id`, etc.).
- The template function is called for every non-separator item.
- Separator items (`{ separator: true }`) are rendered natively and bypass the template.
- `itemTemplate` is a property on `DropDownButtonComponent` — it applies globally to all items. For per-item control, use `beforeItemRender` instead (see `popup-items.md`).

## Comparing itemTemplate vs beforeItemRender

| | `itemTemplate` | `beforeItemRender` |
|---|---|---|
| Approach | React JSX render function | DOM mutation in event handler |
| Style | Declarative (React) | Imperative (direct DOM) |
| Best for | Rich React content, links, custom components | Quick HTML injection, character underline |
| Applies to | All items | Each item individually |
