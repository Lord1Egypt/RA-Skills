# Getting Started with React Chips

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Adding CSS Reference](#adding-css-reference)
- [Rendering a Single Chip](#rendering-a-single-chip)
- [Rendering a Chip List](#rendering-a-chip-list)
- [Run the Application](#run-the-application)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

- Node.js (LTS recommended)
- A React project created via Vite or Create React App

Create a new Vite React app:
```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm run dev
```

---

## Installation

Install the Syncfusion buttons package, which contains the Chips component:

```bash
npm install @syncfusion/ej2-react-buttons --save
```

> The `--save` flag adds the package to your `package.json` dependencies.

---

## Adding CSS Reference

Add the following CSS imports in `src/App.css`:

```css
@import '../node_modules/@syncfusion/ej2-base/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-react-buttons/styles/tailwind3.css';
```

Then import `App.css` in `src/App.tsx`:

```tsx
import './App.css';
```

> You can replace `tailwind3` with other available themes: `material`, `material3`, `bootstrap5`, `fluent2`, `fabric`.

---

## Rendering a Single Chip

The simplest usage — a single chip with display text:

```tsx
import { ChipListComponent } from '@syncfusion/ej2-react-buttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';
import './App.css';

enableRipple(true);

function App() {
  return (
    <ChipListComponent text="Janet Leverling" />
  );
}
export default App;
```

- `text` — sets the label displayed on the chip.
- `enableRipple(true)` — enables the Material-style ripple effect on interaction.

---

## Rendering a Chip List

To render multiple chips, use `ChipsDirective` and `ChipDirective` as children:

```tsx
import {
  ChipListComponent,
  ChipsDirective,
  ChipDirective
} from '@syncfusion/ej2-react-buttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';
import './App.css';

enableRipple(true);

function App() {
  return (
    <ChipListComponent id="chip-list">
      <ChipsDirective>
        <ChipDirective text="Andrew" />
        <ChipDirective text="Janet" />
        <ChipDirective text="Laura" />
        <ChipDirective text="Margaret" />
      </ChipsDirective>
    </ChipListComponent>
  );
}
export default App;
```

- `ChipListComponent` — the container/wrapper component.
- `ChipsDirective` — holds the collection of chips.
- `ChipDirective` — defines an individual chip item. Accepts all per-chip props (`text`, `cssClass`, `avatarText`, `leadingIconCss`, etc.).

---

## Chips via `chips` Prop (Alternative)

Instead of JSX directives, you can pass data as an array via the `chips` prop:

```tsx
import { ChipListComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

const chipsData = [
  { text: 'React' },
  { text: 'Angular' },
  { text: 'Vue' }
];

function App() {
  return <ChipListComponent id="chip-list" chips={chipsData} />;
}
export default App;
```

- `chips` accepts `string[]`, `number[]`, or `ChipModel[]`.
- `ChipModel` supports: `text`, `cssClass`, `avatarText`, `avatarIconCss`, `leadingIconCss`, `leadingIconUrl`, `trailingIconCss`, `trailingIconUrl`, `enabled`, `htmlAttributes`.

---

## Run the Application

```bash
npm run dev
```

The app will start in development mode and open in the browser. The Chip component is rendered inside the `#chip` or `#root` element depending on your setup.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Chip renders without styles | Verify CSS imports are in `App.css` and `App.css` is imported in `App.tsx` |
| `ChipListComponent` not found | Ensure `@syncfusion/ej2-react-buttons` is installed |
| Ripple not working | Call `enableRipple(true)` before rendering the component |
| Chips not rendering in list | Wrap `ChipDirective` inside `ChipsDirective` inside `ChipListComponent` |
