# Getting Started with Syncfusion React MultiSelect

Setup and first implementation of the `MultiSelectComponent` in a React project.

---

## Installation

Install the dropdowns package (includes MultiSelect, AutoComplete, ComboBox, DropDownList):

```bash
npm install @syncfusion/ej2-react-dropdowns --save
```

## Adding CSS References

Import the following CSS files in `src/App.css`. MultiSelect depends on base, buttons, and inputs styles:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-dropdowns/styles/tailwind3.css";
```

Then import `App.css` in your entry file:

```tsx
import './App.css';
```

> **Available themes:** `material.css`, `bootstrap5.css`, `fluent.css`, `tailwind3.css`, `highcontrast.css`

## Basic Implementation

### Functional Component (recommended)

```tsx
import { MultiSelectComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';
import './App.css';

export default function App() {
  return (
    <MultiSelectComponent id="mtselement" />
  );
}
```

### Class Component

```ts
import { MultiSelectComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';
import './App.css';

export default class App extends React.Component<{}, {}> {
  public render() {
    return (
      <MultiSelectComponent id="mtselement" />
    );
  }
}
```

## Binding a Simple Data Source

Pass an array of strings directly to `dataSource`:

```tsx
export default function App() {
  const sportsData = ['Badminton', 'Cricket', 'Football', 'Golf', 'Tennis'];
  return (
    <MultiSelectComponent
      id="mtselement"
      dataSource={sportsData}
      placeholder="Find a game"
    />
  );
}
```

## Binding Object Data with Field Mapping

When the data source is an array of objects, map fields explicitly:

```tsx
import { MultiSelectComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

export default function App() {
  const sportsData = [
    { id: 'game1', sports: 'Badminton' },
    { id: 'game2', sports: 'Football' },
    { id: 'game3', sports: 'Tennis' },
  ];
  const fields = { text: 'sports', value: 'id' };

  return (
    <MultiSelectComponent
      id="mtselement"
      dataSource={sportsData}
      fields={fields}
      placeholder="Select a game"
    />
  );
}
```

> **Why field mapping?** The component needs to know which property to display (`text`) and which to use as the selection value (`value`). If skipped, selected item remains undefined.

## Configuring the Popup

Customize popup height and width using `popupHeight` and `popupWidth`:

```tsx
<MultiSelectComponent
  id="mtselement"
  dataSource={sportsData}
  popupHeight="250px"
  popupWidth="300px"
  placeholder="Find a game"
/>
```

- Default popup height: `300px`
- Default popup width: matches input width

## Running the App (Vite)

```bash
npm run dev
```

For create-react-app projects:

```bash
npm start
```

## See Also

- [Data Binding](data-binding.md) — remote data, DataManager, OData
- [Selection Modes and Features](selection-and-features.md) — checkboxes, chips, custom values
