# Getting Started — React OTP Input

## Table of Contents
- [Installation](#installation)
- [CSS Imports](#css-imports)
- [Basic Implementation](#basic-implementation)
- [Setting OTP Length](#setting-otp-length)
- [Setting a Default Value](#setting-a-default-value)
- [Auto Focus on Load](#auto-focus-on-load)
- [Troubleshooting](#troubleshooting)

---

## Installation

The OTP Input component is part of the `@syncfusion/ej2-react-inputs` package.

```bash
npm install @syncfusion/ej2-react-inputs --save
```

**Create a Vite React project (recommended):**
```bash
# TypeScript
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install @syncfusion/ej2-react-inputs --save
npm run dev

# JavaScript
npm create vite@latest my-app -- --template react
cd my-app
npm install @syncfusion/ej2-react-inputs --save
npm run dev
```

---

## CSS Imports

Add theme CSS to your `src/App.css` (or global stylesheet):

```css
/* Tailwind3 theme (recommended) */
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css";
```

Other available themes: `material3`, `bootstrap5`, `fluent2`, `fabric`.

Then import the CSS file in `src/App.tsx`:
```tsx
import './App.css';
```

---

## Basic Implementation

Minimal working example in `src/App.tsx`:

```tsx
import { OtpInputComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <div id="container">
      <OtpInputComponent id="otpinput" />
    </div>
  );
}

export default App;
```

This renders a 4-field numeric OTP input with the default `outlined` style.

---

## Setting OTP Length

Use the `length` property to control how many input fields are rendered. The default is `4`.

```tsx
import { OtpInputComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div id="container">
      {/* 6-digit OTP */}
      <OtpInputComponent id="otpinput" length={6} />
    </div>
  );
}

export default App;
```

> Tip: Use `length={6}` for standard email/SMS OTP codes and `length={4}` for PIN-style inputs.

---

## Setting a Default Value

Pre-fill the OTP input with a value using the `value` property. Accepts both `string` and `number`.

```tsx
import { OtpInputComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div id="container">
      <OtpInputComponent id="otpinput" value={1234} />
    </div>
  );
}

export default App;
```

For text/alphanumeric OTP values, use a string:
```tsx
<OtpInputComponent id="otpinput" type="text" value="AB12" />
```

---

## Auto Focus on Load

Set `autoFocus` to `true` so the first input field receives focus automatically when the component loads:

```tsx
import { OtpInputComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div id="container">
      <OtpInputComponent id="otpinput" autoFocus={true} />
    </div>
  );
}

export default App;
```

> Use `autoFocus` in login/verification flows to streamline UX — the user can start typing immediately without clicking.

---

## Troubleshooting

**Styles not applied:**
- Ensure CSS is imported before rendering the component.
- Verify the correct theme file path in `node_modules/@syncfusion`.

**Component not rendering:**
- Confirm `@syncfusion/ej2-react-inputs` is installed and listed in `package.json`.

**TypeScript errors on props:**
- Import types from `@syncfusion/ej2-react-inputs` (e.g., `OtpFocusEventArgs`, `OtpChangedEventArgs`).

**Value not updating:**
- For controlled usage, bind `value` with React state and handle updates via the `valueChanged` or `input` events.
