# How-To: Autofill, Highlight Search, and Icon Support

## Autofill

The `autofill` property makes the AutoComplete suggest the first matched item inline in the input as the user types. Pressing `Arrow Down` after typing confirms the inline suggestion. If no match is found, nothing is autofilled.

```tsx
import { AutoCompleteComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const sportsData: { [key: string]: Object }[] = [
    { Id: 'Game1', Game: 'Badminton' },
    { Id: 'Game2', Game: 'Basketball' },
    { Id: 'Game3', Game: 'Cricket' },
    { Id: 'Game4', Game: 'Football' },
    { Id: 'Game5', Game: 'Golf' },
    { Id: 'Game6', Game: 'Hockey' },
    { Id: 'Game7', Game: 'Rugby' },
    { Id: 'Game8', Game: 'Snooker' },
  ];
  const fields: object = { value: 'Game' };

  return (
    <AutoCompleteComponent
      id="atcelement"
      dataSource={sportsData}
      fields={fields}
      autofill={true}
      placeholder="Find a game"
    />
  );
}
```

> `autofill` works with `filterType="StartsWith"` for the most natural suggestion experience. When `autofill` is `false` (default), no inline suggestion is shown.

---

## Highlight Search

Enable `highlight={true}` to visually highlight the typed characters within each suggestion in the popup list. The matched text is wrapped in an `<span class="e-highlight">` element which can be styled:

```tsx
import { AutoCompleteComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const sportsData: { [key: string]: Object }[] = [
    { Id: 'Game1', Game: 'Badminton' },
    { Id: 'Game2', Game: 'Basketball' },
    { Id: 'Game3', Game: 'Cricket' },
    { Id: 'Game4', Game: 'Football' },
    { Id: 'Game5', Game: 'Golf' },
    { Id: 'Game6', Game: 'Hockey' },
    { Id: 'Game7', Game: 'Rugby' },
    { Id: 'Game8', Game: 'Snooker' },
  ];
  const fields: object = { value: 'Game' };

  return (
    <AutoCompleteComponent
      id="atcelement"
      dataSource={sportsData}
      fields={fields}
      highlight={true}
      placeholder="Find a game"
    />
  );
}
```

**Customize the highlight appearance:**

```css
.e-highlight {
  font-weight: bold;
  color: #0056b3;
  background-color: #fff3cd;
}
```

---

## Icon Support

Map an icon CSS class column to `fields.iconCss` to render an icon before each list item. The icon CSS class is applied to a `<span>` element prepended to the item text.

```tsx
import { AutoCompleteComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const sortFormatData: { [key: string]: Object }[] = [
    { Class: 'asc-sort',  Type: 'Sort A to Z', Id: '1' },
    { Class: 'dsc-sort',  Type: 'Sort Z to A', Id: '2' },
    { Class: 'filter',    Type: 'Filter',       Id: '3' },
    { Class: 'clear',     Type: 'Clear',        Id: '4' },
  ];

  // iconCss maps to the 'Class' column which contains CSS class names
  const fields: object = { value: 'Type', iconCss: 'Class' };

  return (
    <AutoCompleteComponent
      id="atcelement"
      dataSource={sortFormatData}
      fields={fields}
      placeholder="Find a format"
    />
  );
}
```

**Define the icon styles in your CSS:**

```css
.asc-sort::before  { content: '↑'; margin-right: 8px; }
.dsc-sort::before  { content: '↓'; margin-right: 8px; }
.filter::before    { content: '⊟'; margin-right: 8px; }
.clear::before     { content: '✕'; margin-right: 8px; }
```

> You can use any icon library (Font Awesome, Material Icons, Syncfusion icons) by setting the appropriate class names in the `iconCss` data column.
