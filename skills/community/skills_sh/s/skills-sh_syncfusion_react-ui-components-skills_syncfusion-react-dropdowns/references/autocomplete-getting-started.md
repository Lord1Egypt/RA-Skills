# Getting Started – Syncfusion React AutoComplete

## Table of Contents
- [Installation](#installation)
- [CSS Imports](#css-imports)
- [Basic Component Setup](#basic-component-setup)
- [Binding a Data Source](#binding-a-data-source)
- [Configuring the Popup](#configuring-the-popup)

---

## Installation

Install the Syncfusion React Dropdowns package which contains the AutoComplete component:

```bash
npm install @syncfusion/ej2-react-dropdowns --save
```

Create a new Vite React project if needed:

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm run dev
```

---

## CSS Imports

Add the required CSS imports to your `src/App.css` file. Use the theme that matches your project (e.g., `tailwind3`, `material`, `bootstrap5`):

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-inputs/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-dropdowns/styles/tailwind3.css";
```

Then import `App.css` in `src/App.tsx`:

```ts
import './App.css';
```

---

## Basic Component Setup

### Functional Component

```tsx
import { AutoCompleteComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';
import './App.css';

export default function App() {
  return (
    <AutoCompleteComponent id="atcelement" />
  );
}
```

### Class Component

```tsx
import { AutoCompleteComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';
import './App.css';

export default class App extends React.Component<{}, {}> {
  public render() {
    return (
      <AutoCompleteComponent id="atcelement" />
    );
  }
}
```

---

## Binding a Data Source

After initialization, pass data using the `dataSource` property. The simplest form is an array of strings:

### Functional Component

```tsx
import { AutoCompleteComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

export default function App() {
  const sportsData: string[] = [
    'Badminton', 'Basketball', 'Cricket', 'Football',
    'Golf', 'Gymnastics', 'Hockey', 'Rugby', 'Snooker', 'Tennis'
  ];

  return (
    <AutoCompleteComponent id="atcelement" dataSource={sportsData} placeholder="Find a game" />
  );
}
```

### Class Component

```tsx
import { AutoCompleteComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

export default class App extends React.Component<{}, {}> {
  private sportsData: string[] = [
    'Badminton', 'Basketball', 'Cricket', 'Football',
    'Golf', 'Gymnastics', 'Hockey', 'Rugby', 'Snooker', 'Tennis'
  ];

  public render() {
    return (
      <AutoCompleteComponent id="atcelement" dataSource={this.sportsData} placeholder="Find a game" />
    );
  }
}
```

---

## Configuring the Popup

By default, the popup width adjusts to the input element width and the popup height is `300px`. Customize with `popupHeight` and `popupWidth`:

```tsx
<AutoCompleteComponent
  id="atcelement"
  dataSource={sportsData}
  popupHeight="250px"
  popupWidth="250px"
  placeholder="Find a game"
/>
```

| Property | Type | Default | Description |
|---|---|---|---|
| `popupHeight` | `string \| number` | `'300px'` | Height of the popup list |
| `popupWidth` | `string \| number` | `'100%'` | Width of the popup list |
| `placeholder` | `string` | `null` | Hint text in the input |
| `enabled` | `boolean` | `true` | Enables or disables the component |
| `readonly` | `boolean` | `false` | Makes the input read-only |
| `showClearButton` | `boolean` | `true` | Shows or hides the clear (×) button |
| `showPopupButton` | `boolean` | `false` | Shows or hides the dropdown toggle button |
| `width` | `string \| number` | `'100%'` | Width of the component |
| `zIndex` | `number` | `1000` | z-index of the popup element |
