# Getting Started with AppBar

## Table of Contents
- [Installation](#installation)
- [Setup Development Environment](#setup-development-environment)
- [Adding Packages](#adding-packages)
- [CSS Imports](#css-imports)
- [Basic AppBar](#basic-appbar)
- [First Example](#first-example)

## Installation

To use AppBar in your React application, install the required Syncfusion packages from npm.

### Dependencies Required

The AppBar component requires the following packages:

```
@syncfusion/ej2-react-navigations      // Main navigation components
  ├── @syncfusion/ej2-react-base       // Base utilities
  ├── @syncfusion/ej2-navigations      // Navigation core
  │   └── @syncfusion/ej2-base        // Core utilities
  └── @syncfusion/ej2-react-buttons   // Button component (optional, for AppBar content)
```

## Setup Development Environment

### Using Vite (Recommended)

Vite provides faster development builds and smaller bundle sizes:

```bash
npm create vite@latest my-app -- --template react
cd my-app
npm run dev
```

For TypeScript:
```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm run dev
```

### Using Create React App

If you prefer Create React App:

```bash
npx create-react-app my-app
cd my-app
npm start
```

## Adding Packages

Install the required Syncfusion packages:

```bash
npm install @syncfusion/ej2-react-navigations --save
npm install @syncfusion/ej2-react-buttons --save
```

These commands install:
- `ej2-react-navigations`: AppBar, Menu, Sidebar components
- `ej2-react-buttons`: Button component for AppBar content
- All dependencies automatically (ej2-react-base, ej2-base, etc.)

## CSS Imports

Add Syncfusion styles to your main CSS file (`App.css` or `index.css`):

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/tailwind3.css";
```

**Available Theme Options:**
- `tailwind3.css` - Tailwind CSS theme (modern, minimal)
- `bootstrap5.css` - Bootstrap 5 theme (familiar Bootstrap look)
- `material.css` - Material Design theme (Google Material Design)
- `fluent2.css` - Microsoft Fluent 2 theme (Office 365 style)
- `fabric.css` - Fabric (Office 365) theme

Choose one theme that matches your project. Replace `tailwind3` with your preferred theme.

## Basic AppBar

### Minimal Example

The most basic AppBar requires:
1. Import `AppBarComponent` from `@syncfusion/ej2-react-navigations`
2. Import `ButtonComponent` from `@syncfusion/ej2-react-buttons`
3. Render the AppBar with content

```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from "react";

const App = () => {
  return (
    <AppBarComponent colorMode="Primary">
      <ButtonComponent cssClass='e-inherit'>Menu</ButtonComponent>
      <span>My Application</span>
    </AppBarComponent>
  );
}

export default App;
```

### With Icons

Add icons to buttons using the `iconCss` property:

```tsx
<AppBarComponent colorMode="Primary">
  <ButtonComponent cssClass='e-inherit' iconCss='e-icons e-menu'></ButtonComponent>
  <span className="regular">React AppBar</span>
  <div className="e-appbar-spacer"></div>
  <ButtonComponent cssClass='e-inherit' iconCss='e-icons e-setting'></ButtonComponent>
</AppBarComponent>
```

**Common Icons:**
- `e-menu` - Hamburger menu
- `e-home` - Home icon
- `e-setting` - Settings gear
- `e-cut`, `e-copy`, `e-paste` - Edit operations
- `e-bold`, `e-italic`, `e-underline` - Text formatting
- `e-align-left`, `e-align-center`, `e-align-right` - Text alignment

## First Example

Here's a complete working example for a new React app:

**App.tsx:**
```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";
import './App.css';

const App = () => {
  return (
    <div className='control-container'>
      <AppBarComponent colorMode="Primary">
        <ButtonComponent cssClass='e-inherit menu' iconCss='e-icons e-menu'></ButtonComponent>
        <span className="regular">React AppBar</span>
        <div className="e-appbar-spacer"></div>
        <ButtonComponent cssClass='e-inherit login'>FREE TRIAL</ButtonComponent>
      </AppBarComponent>
      
      <div className="appbar-content" style={{ padding: '20px' }}>
        <h2>Welcome to AppBar Demo</h2>
        <p>This is your main content area below the AppBar.</p>
      </div>
    </div>
  );
}

export default App;
```

**App.css:**
```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/tailwind3.css";

.control-container {
  width: 100%;
}

.appbar-content {
  font-family: Arial, sans-serif;
  color: #333;
}
```

### Running the App

Start the development server:

```bash
npm run dev     # If using Vite
# or
npm start       # If using Create React App
```

The app will open in your browser at `url` (Vite) or `url` (Create React App).

### What You Should See

- A blue/primary colored bar at the top
- Menu icon (hamburger) on the left
- "React AppBar" text next to the menu
- Flexible space in the middle
- "FREE TRIAL" button on the right
- Content area below the AppBar

## Next Steps

- **Positioning:** Learn about top, bottom, and sticky positioning in positioning-and-layout.md
- **Styling:** Explore color modes and size modes in size-and-color-modes.md
- **Advanced:** Build complex layouts with menus and sidebars in design-patterns.md
