# Getting Started — Syncfusion React ColorPicker

## Table of Contents
- [Prerequisites](#prerequisites)
- [Create a React Application](#create-a-react-application)
- [Install the Package](#install-the-package)
- [Add CSS References](#add-css-references)
- [Add the ColorPicker Component](#add-the-colorpicker-component)
- [Run the Application](#run-the-application)

---

## Prerequisites

- Node.js (LTS recommended)
- A React project using Vite or Create React App

---

## Create a React Application

**Using Vite (recommended):**

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

**Using Create React App:**

```bash
npx create-react-app my-app --template typescript
cd my-app
npm start
```

---

## Install the Package

All Syncfusion EJ2 packages are published on npmjs.com under the `@syncfusion` org.

```bash
npm install @syncfusion/ej2-react-inputs --save
```

The `--save` flag ensures the package is added to `dependencies` in `package.json`.

---

## Add CSS References

Add the following imports in `src/App.css`. These cover the ColorPicker and all its dependencies (buttons, popups, split buttons):

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-inputs/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-splitbuttons/styles/tailwind3.css";
```

Then import `App.css` in `src/App.tsx`:

```tsx
import './App.css';
```

> The order of CSS imports matters — base styles must come before component styles.

---

## Add the ColorPicker Component

Place the following in `src/App.tsx`:

```tsx
import { ColorPickerComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <div id="container">
      <div className="wrap">
        <h4>Choose Color</h4>
        <ColorPickerComponent id="color-picker" />
      </div>
    </div>
  );
}
export default App;
```

This renders a SplitButton. Clicking it opens the ColorPicker popup with the Picker (HSV) panel and Apply/Cancel buttons.

---

## Run the Application

```bash
npm run dev   # Vite
# or
npm start     # Create React App
```

Open the URL shown in the terminal (e.g., `http://localhost:5173`).

---

## What Renders by Default

- A **SplitButton** showing the currently selected color
- Clicking opens a popup with the **Picker** (HSV gradient + hue/opacity sliders)
- Default color: `#008000ff` (green, fully opaque)
- **Apply** button confirms the selection; **Cancel** discards it
- A **mode switcher** button toggles between Picker and Palette views

To change any of this behavior, see `references/modes-and-value.md` (modes/inline), `references/ui-customization.md` (hiding buttons), or `references/palette-features.md` (palette customization).
