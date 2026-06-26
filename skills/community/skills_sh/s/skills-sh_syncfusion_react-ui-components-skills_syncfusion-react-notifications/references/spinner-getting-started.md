# Getting Started — React Spinner

## Table of Contents
- [Installation](#installation)
- [CSS Imports](#css-imports)
- [Basic Spinner Example](#basic-spinner-example)
- [Functional Component Pattern](#functional-component-pattern)
- [Class Component Pattern](#class-component-pattern)
- [Show and Hide Spinner](#show-and-hide-spinner)
- [Spinner with Label](#spinner-with-label)
- [Full-Page Overlay Spinner](#full-page-overlay-spinner)
- [Troubleshooting](#troubleshooting)

---

## Installation

The Spinner is part of the `@syncfusion/ej2-react-popups` package.

```bash
npm install @syncfusion/ej2-react-popups --save
```

> The `--save` flag adds the package as a project dependency in `package.json`.

---

## CSS Imports

Add the required theme CSS to your `src/App.css` file:

```css
/* Tailwind 3 (default / recommended) */
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-popups/styles/tailwind3.css";
```

Other available themes (pick ONE):

```css
/* Material */
@import "../node_modules/@syncfusion/ej2-base/styles/material.css";
@import "../node_modules/@syncfusion/ej2-react-popups/styles/material.css";

/* Bootstrap 5 */
@import "../node_modules/@syncfusion/ej2-base/styles/bootstrap5.css";
@import "../node_modules/@syncfusion/ej2-react-popups/styles/bootstrap5.css";

/* Fluent 2 */
@import "../node_modules/@syncfusion/ej2-base/styles/fluent2.css";
@import "../node_modules/@syncfusion/ej2-react-popups/styles/fluent2.css";
```

> ⚠️ Always import `ej2-base` theme **before** `ej2-react-popups` theme. Import `App.css` in `src/App.tsx`.

---

## Basic Spinner Example

The Spinner is created imperatively using utility functions — not as a JSX component.

```tsx
// src/App.tsx
import { createSpinner, showSpinner } from '@syncfusion/ej2-react-popups';
import * as React from 'react';
import { useEffect } from 'react';
import './App.css';

function App() {
  useEffect(() => {
    // Step 1: Create the spinner on the target element
    createSpinner({
      target: document.getElementById('container') as HTMLElement
    });
    // Step 2: Show the spinner
    showSpinner(document.getElementById('container') as HTMLElement);
  }, []);

  return (
    <div className="control-pane">
      <div
        id="container"
        className="control-section"
        style={{ width: '100%', height: '200px' }}
      />
    </div>
  );
}

export default App;
```

**Key points:**
- `createSpinner` must be called **before** `showSpinner`
- The `target` is a real DOM element (use `document.getElementById` or a `useRef`)
- In functional components, put spinner logic inside `useEffect`

---

## Functional Component Pattern

Using `useRef` for reliable element access:

```tsx
import { createSpinner, showSpinner, hideSpinner } from '@syncfusion/ej2-react-popups';
import * as React from 'react';
import { useEffect, useRef } from 'react';
import './App.css';

function App() {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (containerRef.current) {
      createSpinner({ target: containerRef.current });
      showSpinner(containerRef.current);
    }

    // Cleanup: hide spinner on unmount
    return () => {
      if (containerRef.current) {
        hideSpinner(containerRef.current);
      }
    };
  }, []);

  return (
    <div
      ref={containerRef}
      style={{ width: '300px', height: '200px', position: 'relative' }}
    />
  );
}

export default App;
```

---

## Class Component Pattern

```tsx
import { createSpinner, showSpinner } from '@syncfusion/ej2-react-popups';
import * as React from 'react';
import './App.css';

export default class App extends React.Component {
  componentDidMount() {
    // Create and show spinner after mount
    createSpinner({
      target: document.getElementById('container') as HTMLElement
    });
    showSpinner(document.getElementById('container') as HTMLElement);
  }

  render() {
    return (
      <div className="control-pane">
        <div
          id="container"
          className="control-section col-lg-12 spinner-target"
        />
      </div>
    );
  }
}
```

---

## Show and Hide Spinner

Control spinner visibility using `showSpinner` and `hideSpinner`:

```tsx
import { createSpinner, showSpinner, hideSpinner } from '@syncfusion/ej2-react-popups';
import * as React from 'react';
import { useEffect, useRef, useState } from 'react';
import './App.css';

function LoadingDemo() {
  const containerRef = useRef<HTMLDivElement>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (containerRef.current) {
      // Create spinner once — show/hide separately
      createSpinner({ target: containerRef.current });
    }
  }, []);

  const startLoading = () => {
    setIsLoading(true);
    showSpinner(containerRef.current as HTMLElement);

    // Simulate async work
    setTimeout(() => {
      hideSpinner(containerRef.current as HTMLElement);
      setIsLoading(false);
    }, 3000);
  };

  return (
    <div>
      <button onClick={startLoading} disabled={isLoading}>
        {isLoading ? 'Loading...' : 'Load Data'}
      </button>
      <div
        ref={containerRef}
        style={{ width: '300px', height: '200px', position: 'relative' }}
      />
    </div>
  );
}

export default LoadingDemo;
```

> ✅ `hideSpinner` hides the spinner but does **not** destroy it — you can `showSpinner` again later.

---

## Spinner with Label

Add descriptive text alongside the spinner:

```tsx
import { createSpinner, showSpinner } from '@syncfusion/ej2-react-popups';
import { useEffect, useRef } from 'react';

function LabeledSpinner() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (ref.current) {
      createSpinner({
        target: ref.current,
        label: 'Loading data, please wait...',
        width: '40px'
      });
      showSpinner(ref.current);
    }
  }, []);

  return <div ref={ref} style={{ height: '150px' }} />;
}
```

---

## Full-Page Overlay Spinner

Block the entire page during async operations:

```tsx
import { createSpinner, showSpinner, hideSpinner } from '@syncfusion/ej2-react-popups';
import * as React from 'react';
import { useEffect } from 'react';

function PageOverlaySpinner() {
  useEffect(() => {
    // Use document.body as target for full-page overlay
    createSpinner({
      target: document.body,
      label: 'Loading application...'
    });
    showSpinner(document.body);

    // Hide after initialization completes
    const timer = setTimeout(() => {
      hideSpinner(document.body);
    }, 2000);

    return () => clearTimeout(timer);
  }, []);

  return <div className="app-content">Application content here</div>;
}

export default PageOverlaySpinner;
```

---

## Troubleshooting

### Spinner not appearing
- Ensure `createSpinner` is called **before** `showSpinner`
- Confirm the target element exists in the DOM when `createSpinner` runs (use `useEffect`, not render-time)
- Check that CSS is properly imported in `App.css` and `App.css` is imported in `App.tsx`

### Spinner appears but has no animation
- Verify both `ej2-base` and `ej2-react-popups` CSS are imported
- Ensure `ej2-base` CSS comes **before** `ej2-react-popups` CSS

### TypeScript error on getElementById
- Cast the result: `document.getElementById('id') as HTMLElement`
- Or use `useRef<HTMLDivElement>(null)` and null-check before use

### Spinner stays visible after data loads
- Call `hideSpinner(container)` in the `finally` block of your async operation:
  ```ts
  try {
    await fetchData();
  } finally {
    hideSpinner(containerEl);
  }
  ```

### Cannot import from '@syncfusion/ej2-react-popups'
- Run `npm install @syncfusion/ej2-react-popups --save`
- Verify the package is in `package.json` dependencies
