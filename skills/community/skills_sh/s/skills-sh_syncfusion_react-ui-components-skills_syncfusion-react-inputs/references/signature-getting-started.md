# Getting Started with Syncfusion React Signature

Set up a basic Signature component in a React application using Vite.

---

## Installation

```bash
npm install @syncfusion/ej2-react-inputs --save
```

The Signature component is part of the `@syncfusion/ej2-react-inputs` package.

---

## CSS Imports

Add the following theme imports to `src/App.css`:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css";
```

Import `App.css` in `src/App.tsx`:

```tsx
import './App.css';
```

---

## Basic Setup

Add the `SignatureComponent` to your application (`src/App.tsx`):

```tsx
import { SignatureComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <div>
      <div id="signature-control">
        <h4>Sign here</h4>
        <SignatureComponent id="signature" />
      </div>
    </div>
  );
}
export default App;
```

---

## Running the Application

```bash
npm run dev
```

This starts the Vite development server. Open the URL shown in the terminal to see the Signature component rendered in the browser.

---

## Project Setup (Vite)

Create a new React + TypeScript project:

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install @syncfusion/ej2-react-inputs --save
npm run dev
```

For a JavaScript project:

```bash
npm create vite@latest my-app -- --template react
cd my-app
npm install @syncfusion/ej2-react-inputs --save
npm run dev
```

---

## Notes

- The component renders a `<canvas>` element and captures strokes via pointer/touch/mouse events.
- No additional configuration is required for basic usage — `id` is the only required prop.
- The component requires a wrapping element with a defined size for the canvas to render correctly in layouts.
