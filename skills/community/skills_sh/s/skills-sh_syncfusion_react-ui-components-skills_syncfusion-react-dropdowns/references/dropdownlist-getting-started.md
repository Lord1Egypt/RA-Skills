# Getting Started with DropDownList

This file covers installation, project setup, and the minimal working DropDownList implementation.

## Installation

Install the Syncfusion dropdowns package:

```bash
npm install @syncfusion/ej2-react-dropdowns --save
```

## CSS Imports

Add the following CSS imports in `src/App.css`. The `tailwind3` theme is the current default:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-dropdowns/styles/tailwind3.css";
```

Then import `App.css` in `src/App.tsx`:

```tsx
import './App.css';
```

> **Important:** Always use `tailwind3` (not `material` or `bootstrap`) for current Syncfusion projects. Using an outdated theme name will result in missing styles.

## Basic DropDownList

### Functional Component (recommended)

```tsx
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';
import './App.css';

export default function App() {
  const sportsData: string[] = ['Badminton', 'Cricket', 'Football', 'Golf', 'Tennis'];

  return (
    <DropDownListComponent
      id="ddlelement"
      dataSource={sportsData}
      placeholder="Select a game"
    />
  );
}
```

### Class Component

```tsx
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';
import './App.css';

export default class App extends React.Component<{}, {}> {
  private sportsData: string[] = ['Badminton', 'Cricket', 'Football', 'Golf', 'Tennis'];

  public render() {
    return (
      <DropDownListComponent id="ddlelement" dataSource={this.sportsData} placeholder="Select a game" />
    );
  }
}
```

## Binding a Data Source

Pass any array directly to `dataSource`. For JSON objects, also set the `fields` prop to map display text and value:

```tsx
export default function App() {
  const sportsData = [
    { Id: 'game1', Game: 'Badminton' },
    { Id: 'game2', Game: 'Football' },
    { Id: 'game3', Game: 'Tennis' },
  ];
  const fields = { text: 'Game', value: 'Id' };

  return (
    <DropDownListComponent
      id="ddlelement"
      dataSource={sportsData}
      fields={fields}
      placeholder="Select a game"
    />
  );
}
```

## Configuring Popup Height and Width

By default the popup width matches the input element and the height is 300px. Override with `popupHeight` and `popupWidth`:

```tsx
<DropDownListComponent
  id="ddlelement"
  dataSource={sportsData}
  popupHeight="200px"
  popupWidth="250px"
  placeholder="Select a game"
/>
```

## Running the Application

```bash
npm run dev
```

## Project Setup (Vite)

Create a new React + TypeScript project with Vite:

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install @syncfusion/ej2-react-dropdowns --save
npm run dev
```

## See Also

- [Data Binding](data-binding.md) — local arrays, JSON objects, remote data
- [Filtering](filtering.md) — search-as-you-type filtering
- [Grouping & Templates](grouping-and-templates.md) — grouped items, custom templates
