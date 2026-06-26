# Getting Started with Syncfusion React Rating

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [CSS Reference](#css-reference)
- [Basic Usage](#basic-usage)
- [Setting Initial Value](#setting-initial-value)
- [Running the Application](#running-the-application)

---

## Prerequisites

Create a React application using Vite:

```bash
# TypeScript
npm create vite@latest my-app -- --template react-ts
cd my-app
npm run dev

# JavaScript
npm create vite@latest my-app -- --template react
cd my-app
npm run dev
```

---

## Installation

Install the Syncfusion inputs package that includes the Rating component:

```bash
npm install @syncfusion/ej2-react-inputs --save
```

> The `--save` flag adds the package to the `dependencies` section of `package.json`.

---

## CSS Reference

Add the required CSS imports to `src/App.css`:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-inputs/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css";
```

Then import `App.css` in `src/App.tsx`:

```tsx
import './App.css';
```

> Three CSS files are needed: `ej2-base` for core styles, `ej2-react-inputs` for rating styles, and `ej2-popups` for tooltip styles.

---

## Basic Usage

Add the `RatingComponent` to `src/App.tsx`:

```tsx
import { RatingComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <RatingComponent id="rating" />
  );
}
export default App;
```

This renders a 5-star rating with no initial selection and a tooltip on hover.

---

## Setting Initial Value

Use the `value` property to set a pre-selected rating:

```tsx
import { RatingComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <div className="wrap">
      <RatingComponent id="rating" value={3} />
    </div>
  );
}
export default App;
```

- `value` is a decimal ranging from `min` (default `0`) to `itemsCount` (default `5`).
- Example: `value={3.5}` with `precision={PrecisionType.Half}` shows a half-star at position 4.

---

## Running the Application

```bash
npm run dev
```

The application opens in your browser. The rating component is interactive by default — click a star to select a rating, hover to see tooltips.

---

## Gotchas

- Always import `App.css` (with the three CSS imports) in your root component or the component will render unstyled.
- The `id` prop is required for the rating component to function correctly.
- `@syncfusion/ej2-popups` CSS is required even if tooltips are disabled, to avoid layout issues.
