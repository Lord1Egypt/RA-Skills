# Getting Started with React Badge

The Syncfusion React Badge is a pure CSS component. There is no React component class — badges are rendered as plain HTML elements styled with CSS modifier classes.

## Installation

Install the notifications package which bundles the Badge component:

```bash
npm install @syncfusion/ej2-react-notifications --save
```

> The `--save` flag records the package in the `dependencies` section of `package.json`.

## Setting Up a React Project

Create a new React + Vite project (recommended):

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

## Adding CSS References

Add the following imports to `src/App.css`:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-notifications/styles/tailwind3.css";
```

Then import `App.css` in `src/App.tsx`:

```tsx
import './App.css';
```

## Adding Your First Badge

Badges attach to any inline element — typically a `<span>` nested inside a heading, button, or container. The only requirement is the base `e-badge` class plus a color variant class:

```tsx
import * as React from "react";
import * as ReactDOM from "react-dom";

function App() {
  return (
    <h1>Badge Component <span className="e-badge e-badge-primary">New</span></h1>
  );
}
export default App;
ReactDOM.render(<App />, document.getElementById("element"));
```

## Running the Application

```bash
npm run dev
```

The browser opens with your badge rendered inline inside the heading.

## Key Points

- **No component import needed** — Badge is CSS-only; just add classes to a `<span>` or `<a>`.
- **Always include `e-badge`** as the base class alongside any modifier class.
- **Parent positioning** — For notification/dot/overlap badges, the parent container should have `position: relative` so the badge positions correctly.
