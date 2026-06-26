# Getting Started — Syncfusion React ButtonGroup

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Adding CSS References](#adding-css-references)
- [Basic ButtonGroup](#basic-buttongroup)
- [Running the Application](#running-the-application)

## Prerequisites

Create a React application using Vite:

```bash
# JavaScript
npm create vite@latest my-app -- --template react
cd my-app
npm run dev

# TypeScript
npm create vite@latest my-app -- --template react-ts
cd my-app
npm run dev
```

## Installation

Install the Syncfusion buttons package:

```bash
npm install @syncfusion/ej2-react-buttons --save
```

For nesting (DropDownButton / SplitButton) or the `createButtonGroup` utility, also install:

```bash
npm install @syncfusion/ej2-react-splitbuttons --save
```

## Adding CSS References

Add the following imports to `src/App.css`:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-splitbuttons/styles/tailwind3.css";
```

Then import the CSS file in `src/App.tsx` (or `src/App.jsx`):

```tsx
import './App.css';
```

## Basic ButtonGroup

The ButtonGroup is a **pure CSS component** — wrap `ButtonComponent` elements inside a `div` with the `e-btn-group` class. No JavaScript initialization is needed for basic usage.

```tsx
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <div className='e-btn-group'>
      <ButtonComponent>HTML</ButtonComponent>
      <ButtonComponent>CSS</ButtonComponent>
      <ButtonComponent>Javascript</ButtonComponent>
    </div>
  );
}
export default App;
```

**Key point:** The `e-btn-group` class on the container is what creates the visual grouping. Each child `ButtonComponent` is styled as a grouped button automatically.

## Running the Application

```bash
npm run dev
```

The development server starts and the ButtonGroup renders in the browser.

## See Also

- For selection behaviors (radio/checkbox), see [selection-and-nesting.md](selection-and-nesting.md)
- For the `createButtonGroup` utility function approach, see [how-to.md](how-to.md)
