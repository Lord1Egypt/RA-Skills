# API Reference — React Spinner

> Source: `@syncfusion/ej2-react-popups` / `@syncfusion/ej2-popups`  
> Official Docs: [https://ej2.syncfusion.com/react/documentation/spinner/](https://ej2.syncfusion.com/react/documentation/spinner/)

The Syncfusion React Spinner is **not a component class** — it is a set of **utility functions** exported from `@syncfusion/ej2-react-popups`. There is no `SpinnerComponent` class.

## Table of Contents
1. [Import Paths](#import-paths)
2. [createSpinner](#createspinner)
3. [showSpinner](#showspinner)
4. [hideSpinner](#hidespinner)
5. [setSpinner](#setspinner)
6. [SpinnerArgs Interface](#spinnerargs-interface)
7. [SetSpinnerArgs Interface](#setspinnerargs-interface)
8. [SpinnerType Values](#spinnertype-values)
9. [Quick Reference Table](#quick-reference-table)

---

## Import Paths

```ts
// React (recommended)
import {
  createSpinner,
  showSpinner,
  hideSpinner,
  setSpinner
} from '@syncfusion/ej2-react-popups';

// Core JavaScript/TypeScript
import {
  createSpinner,
  showSpinner,
  hideSpinner,
  setSpinner
} from '@syncfusion/ej2-popups';
```

---

## createSpinner

Creates a spinner overlay on the specified target element.

```ts
function createSpinner(args: SpinnerArgs): void;
```

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `args` | `SpinnerArgs` | ✅ Yes | Configuration object. See [SpinnerArgs](#spinnerargs-interface). |

### Example

```tsx
import { createSpinner, showSpinner } from '@syncfusion/ej2-react-popups';
import * as React from 'react';
import { useEffect } from 'react';

function App() {
  useEffect(() => {
    createSpinner({
      target: document.getElementById('container') as HTMLElement
    });
    showSpinner(document.getElementById('container') as HTMLElement);
  }, []);

  return <div id="container" style={{ height: '200px' }} />;
}
```

### With Options

```tsx
createSpinner({
  target: document.getElementById('myDiv') as HTMLElement,
  width: '34px',
  label: 'Loading...',
  cssClass: 'custom-spinner',
  type: 'Bootstrap5'
});
```

---

## showSpinner

Makes the spinner visible on the target element.

```ts
function showSpinner(container: HTMLElement): void;
```

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `container` | `HTMLElement` | ✅ Yes | The DOM element where the spinner was created. |

### Example

```tsx
showSpinner(document.getElementById('container') as HTMLElement);
```

---

## hideSpinner

Hides the spinner on the target element. The spinner is **not destroyed**, only hidden.

```ts
function hideSpinner(container: HTMLElement): void;
```

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `container` | `HTMLElement` | ✅ Yes | The DOM element where the spinner was created. |

### Example

```tsx
hideSpinner(document.getElementById('container') as HTMLElement);
```

---

## setSpinner

Changes spinners globally across the entire page from the application level. Call **before** creating individual spinners to apply a global default.

```ts
function setSpinner(args: SetSpinnerArgs): void;
```

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `args` | `SetSpinnerArgs` | ✅ Yes | Global spinner configuration. See [SetSpinnerArgs](#setspinnerargs-interface). |

### Example

```tsx
import { setSpinner } from '@syncfusion/ej2-react-popups';

// Call before createSpinner calls
setSpinner({ type: 'Bootstrap5', cssClass: 'global-spinner' });
```

---

## SpinnerArgs Interface

Arguments used with `createSpinner()`.

```ts
interface SpinnerArgs {
  target: HTMLElement;
  width?: string | number;
  label?: string;
  cssClass?: string;
  template?: string;
  type?: SpinnerType;
}
```

### Properties

| Property | Type | Required | Default | Description |
|---|---|---|---|---|
| `target` | `HTMLElement` | ✅ Yes | — | The DOM element to render the spinner on. |
| `width` | `string \| number` | ❌ No | theme default | Width (size) of the spinner icon. E.g. `'34px'` or `34`. |
| `label` | `string` | ❌ No | — | Text label displayed alongside the spinner. |
| `cssClass` | `string` | ❌ No | `''` | One or more CSS class names added to the spinner root for custom styling. |
| `template` | `string` | ❌ No | — | Custom HTML string to replace the default spinner animation. |
| `type` | `SpinnerType` | ❌ No | auto (from theme) | Spinner visual style/theme. See [SpinnerType Values](#spinnertype-values). |

### Example with All Properties

```tsx
createSpinner({
  target: document.getElementById('myElement') as HTMLElement,
  width: '50px',
  label: 'Please wait...',
  cssClass: 'e-spin-overlay',
  type: 'Material3'
});
```

---

## SetSpinnerArgs Interface

Arguments used with `setSpinner()` for global spinner configuration.

```ts
interface SetSpinnerArgs {
  template?: string;
  cssClass?: string;
  type?: SpinnerType;
}
```

### Properties

| Property | Type | Required | Description |
|---|---|---|---|
| `template` | `string` | ❌ No | Custom HTML string to replace the default spinner animation globally. |
| `cssClass` | `string` | ❌ No | CSS class(es) added to the spinner root element across all spinners. |
| `type` | `SpinnerType` | ❌ No | Spinner visual theme to apply globally. |

### Example

```tsx
// Apply Bootstrap5 theme globally before any createSpinner calls
setSpinner({ type: 'Bootstrap5' });

// Later create spinners — they pick up the global setting
createSpinner({ target: document.getElementById('div1') as HTMLElement });
createSpinner({ target: document.getElementById('div2') as HTMLElement });
```

---

## SpinnerType Values

The `type` property accepts one of the following string values:

| Value | Description |
|---|---|
| `'Material'` | Google Material Design spinner |
| `'Material3'` | Material Design 3 (You) spinner |
| `'Fabric'` | Microsoft Fabric / Office 365 style |
| `'Bootstrap'` | Bootstrap 3 spinner |
| `'Bootstrap4'` | Bootstrap 4 spinner |
| `'Bootstrap5'` | Bootstrap 5 spinner |
| `'HighContrast'` | High contrast accessibility spinner |
| `'Tailwind'` | Tailwind CSS spinner |
| `'Tailwind3'` | Tailwind CSS v3 spinner |
| `'Fluent'` | Microsoft Fluent Design spinner |
| `'Fluent2'` | Microsoft Fluent Design 2 spinner |

### Usage

```tsx
// Explicit type selection
createSpinner({
  target: document.getElementById('container') as HTMLElement,
  type: 'Fluent2'
});

// Global type for all spinners on the page
setSpinner({ type: 'Bootstrap5' });
```

---

## Quick Reference Table

| Function | Signature | When to Use |
|---|---|---|
| `createSpinner` | `(args: SpinnerArgs) => void` | Initialize a spinner on a DOM element |
| `showSpinner` | `(container: HTMLElement) => void` | Show an existing (hidden) spinner |
| `hideSpinner` | `(container: HTMLElement) => void` | Hide a visible spinner |
| `setSpinner` | `(args: SetSpinnerArgs) => void` | Set global spinner defaults for the whole page |

---

## CSS Theme Imports

```css
/* Tailwind 3 (recommended) */
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-popups/styles/tailwind3.css";

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

> ⚠️ Always import `ej2-base` theme **before** `ej2-react-popups` theme.

---

## Common Gotchas

### ❌ Invalid: SpinnerComponent does not exist
```tsx
// WRONG — there is no class-based SpinnerComponent
import { SpinnerComponent } from '@syncfusion/ej2-react-popups'; // ❌
```

### ✅ Correct: Use utility functions only
```tsx
import { createSpinner, showSpinner, hideSpinner, setSpinner } from '@syncfusion/ej2-react-popups'; // ✅
```

### ❌ Invalid: calling showSpinner before createSpinner
```tsx
showSpinner(el); // ❌ spinner not yet created
createSpinner({ target: el });
```

### ✅ Correct: create before show
```tsx
createSpinner({ target: el }); // ✅ create first
showSpinner(el);               // then show
```

### ❌ Invalid: properties that don't exist
```tsx
// WRONG — these properties do not exist on SpinnerArgs
createSpinner({ target: el, color: '#fff', size: 'large', visible: true }); // ❌
```

### ✅ Valid SpinnerArgs properties only
```tsx
createSpinner({
  target: el,
  width: '34px',    // ✅
  label: 'Loading', // ✅
  cssClass: 'my',   // ✅
  type: 'Fluent2',  // ✅
  template: '<div>' // ✅
});
```
