# Getting Started with Syncfusion React Stepper

## Table of Contents
- [Installation](#installation)
- [CSS Setup](#css-setup)
- [Creating Your First Stepper](#creating-your-first-stepper)
- [Running the Application](#running-the-application)
- [Quick Configuration](#quick-configuration)

## Installation

### Step 1: Install via npm

The Stepper component is part of the `@syncfusion/ej2-react-navigations` package. Install it using npm:

```bash
npm install @syncfusion/ej2-react-navigations --save
```

### Step 2: Verify Dependencies

The Stepper component depends on the following packages, which are installed automatically:

- `@syncfusion/ej2-base`
- `@syncfusion/ej2-popups`
- `@syncfusion/ej2-navigations`
- `@syncfusion/ej2-react-base`

You can verify the installation by checking your `package.json`:

```json
{
  "dependencies": {
    "@syncfusion/ej2-react-navigations": "^latest"
  }
}
```

## CSS Setup

### Import Required Styles

Import the necessary CSS files in your main application file (typically `src/App.css` or `src/App.jsx`):

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/tailwind3.css";
```

**Available Themes:**
- `tailwind3.css` (default, modern minimal design)
- `bootstrap5.3.css` (Bootstrap 5 styling)
- `fluent2.css` (Fluent Design System)
- `material3.css` (Material Design 3)

Choose one theme file based on your design preference. Replace `tailwind3.css` with your chosen theme.

### Alternative: CSS Modules

If using CSS modules, import in your component:

```jsx
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-navigations/styles/tailwind3.css';
```

## Creating Your First Stepper

### Basic Example: Simple Checkout Flow

```jsx
import React from 'react';
import { StepperComponent, StepsDirective, StepDirective } from '@syncfusion/ej2-react-navigations';
import './App.css';

function App() {
  return (
    <div className="app-container">
      <h2>Checkout Process</h2>
      <StepperComponent>
        <StepsDirective>
          <StepDirective iconCss="sf-icon-cart" label="Cart" />
          <StepDirective iconCss="sf-icon-transport" label="Delivery" />
          <StepDirective iconCss="sf-icon-payment" label="Payment" />
          <StepDirective iconCss="sf-icon-success" label="Confirmation" />
        </StepsDirective>
      </StepperComponent>
    </div>
  );
}

export default App;
```

### Example with Text Instead of Icons

```jsx
<StepperComponent>
  <StepsDirective>
    <StepDirective text="1" label="Account" />
    <StepDirective text="2" label="Profile" />
    <StepDirective text="3" label="Verification" />
    <StepDirective text="4" label="Complete" />
  </StepsDirective>
</StepperComponent>
```

### Example with Active Step

Set the initial active step using the `activeStep` property:

```jsx
<StepperComponent activeStep={1}>
  <StepsDirective>
    <StepDirective iconCss="sf-icon-cart" label="Cart" />
    <StepDirective iconCss="sf-icon-transport" label="Delivery" />
    <StepDirective iconCss="sf-icon-payment" label="Payment" />
    <StepDirective iconCss="sf-icon-success" label="Confirmation" />
  </StepsDirective>
</StepperComponent>
```

### Property-Based Pattern: Using steps Array

You can also use the `steps` property array instead of `StepsDirective` and `StepDirective`:

```jsx
import React from 'react';
import { StepperComponent } from '@syncfusion/ej2-react-navigations';
import './App.css';

function App() {
  const steps = [
    { iconCss: 'sf-icon-cart', label: 'Cart' },
    { iconCss: 'sf-icon-transport', label: 'Delivery' },
    { iconCss: 'sf-icon-payment', label: 'Payment' },
    { iconCss: 'sf-icon-success', label: 'Confirmation' }
  ];

  return (
    <div className="app-container">
      <h2>Checkout Process</h2>
      <StepperComponent steps={steps} activeStep={0} />
    </div>
  );
}

export default App;
```

## Running the Application

### With Vite (Recommended)

```bash
npm create vite@latest my-app -- --template react
cd my-app
npm install @syncfusion/ej2-react-navigations --save
npm run dev
```

Open `url` in your browser.

### With Create React App

```bash
npx create-react-app my-app
cd my-app
npm install @syncfusion/ej2-react-navigations --save
npm start
```

Open `url` in your browser.

## Quick Configuration

### Horizontal Stepper (Default)

```jsx
<StepperComponent orientation="horizontal">
  {/* steps */}
</StepperComponent>
```

### Vertical Stepper

```jsx
<StepperComponent orientation="vertical">
  {/* steps */}
</StepperComponent>
```

### Linear Navigation (Step-by-Step)

```jsx
<StepperComponent linear={true}>
  {/* Users must complete each step sequentially */}
</StepperComponent>
```

### Readonly Stepper (View-Only)

```jsx
<StepperComponent readOnly={true}>
  {/* Users cannot interact with the stepper */}
</StepperComponent>
```

## Troubleshooting

**Issue: Stepper is not displaying**
- ✅ Verify CSS imports are included in your app
- ✅ Check that `@syncfusion/ej2-react-navigations` is installed
- ✅ Ensure `StepperComponent`, `StepsDirective`, and `StepDirective` are imported

**Issue: Styles look different than expected**
- ✅ Verify you're using the correct theme CSS file
- ✅ Check browser DevTools for CSS conflicts
- ✅ Ensure CSS imports are in the correct order

**Issue: Step icons not showing**
- ✅ Install Syncfusion icon fonts or use custom CSS classes
- ✅ Verify `iconCss` property values are valid CSS class names
- ✅ Add icon CSS files to your imports if using custom icon sets
