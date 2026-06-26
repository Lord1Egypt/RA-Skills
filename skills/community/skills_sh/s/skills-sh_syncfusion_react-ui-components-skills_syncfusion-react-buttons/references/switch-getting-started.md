# Getting Started with Syncfusion React Switch

This guide covers setting up a React project and rendering the Syncfusion Switch component from scratch.

## Prerequisites

- Node.js installed
- A React project (Vite recommended)

## 1. Create a React Application

Using Vite (recommended for faster builds):

```bash
# TypeScript template
npm create vite@latest my-app -- --template react-ts
cd my-app
npm run dev

# JavaScript template
npm create vite@latest my-app -- --template react
cd my-app
npm run dev
```

## 2. Install the Switch Package

The Switch component is part of the `@syncfusion/ej2-react-buttons` package:

```bash
npm install @syncfusion/ej2-react-buttons --save
```

## 3. Add CSS Theme Imports

Add the required CSS files in `src/App.css`:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
```

Then import `App.css` in `src/App.tsx`:

```tsx
import './App.css';
```

> Other available themes: `material3.css`, `bootstrap5.3.css`, `fluent2.css`, `highcontrast.css`. Replace `tailwind3` with the theme name.

## 4. Render a Basic Switch

Add the `SwitchComponent` to `src/App.tsx`:

```tsx
import { SwitchComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <div>
      <SwitchComponent />
    </div>
  );
}
export default App;
```

## 5. Render with Checked State and Ripple

To render the Switch pre-checked with ripple effects enabled:

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { SwitchComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import './App.css';

enableRipple(true);

function App() {
  return (
    <SwitchComponent checked={true} />
  );
}
export default App;
```

## 6. Run the Application

```bash
npm run dev
```

The Switch renders as an interactive toggle in the browser. Clicking it toggles between checked (on) and unchecked (off) states.

## What's Next?

- Configure features like labels, disabled state, and RTL → [features.md](features.md)
- Handle events and call methods programmatically → [events-and-methods.md](events-and-methods.md)
- Apply custom styles and sizes → [style-and-appearance.md](style-and-appearance.md)
- Full API reference → [api.md](api.md)
