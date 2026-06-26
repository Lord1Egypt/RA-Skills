# Getting Started with React RangeSlider

## Table of Contents
- [Installation](#installation)
- [Setup](#setup)
- [Basic Implementation](#basic-implementation)
- [First Working Example](#first-working-example)
- [Importing CSS Themes](#importing-css-themes)
- [Minimal Configuration](#minimal-configuration)

## Installation

Install the Syncfusion inputs package containing the RangeSlider component:

```bash
npm install @syncfusion/ej2-react-inputs --save
```

The `--save` flag adds the package to your `package.json` dependencies.

### Dependencies

The RangeSlider requires these peer packages (typically already installed):
- `@syncfusion/ej2-base` - Core functionality
- `@syncfusion/ej2-buttons` - Button support (if `showButtons={true}`)
- `@syncfusion/ej2-popups` - Tooltip support

These are automatically installed as dependencies of `@syncfusion/ej2-react-inputs`.

## Setup

### Project Prerequisites

**For new React projects, use Vite (recommended):**

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install
```

**Or use Create React App:**

```bash
npx create-react-app my-app
cd my-app
```

**Or Next.js:**

```bash
npx create-next-app@latest my-app --typescript
cd my-app
```

### Add Syncfusion Inputs Package

In your existing React project:

```bash
npm install @syncfusion/ej2-react-inputs
```

## Importing CSS Themes

Add CSS imports to your main stylesheet or App component. Choose ONE theme:

### Option 1: Import in App.css

Add these lines to `src/App.css`:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-inputs/styles/tailwind3.css";
```

### Option 2: Import in App.tsx

Import directly in your component file:

```tsx
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-buttons/styles/tailwind3.css';
import '@syncfusion/ej2-popups/styles/tailwind3.css';
import '@syncfusion/ej2-react-inputs/styles/tailwind3.css';
```

### Available Themes

Replace `tailwind3` with your chosen theme:
- `material` - Material Design
- `bootstrap5` - Bootstrap 5
- `fluent` - Microsoft Fluent
- `tailwind3` - Tailwind CSS 3
- `fabric` - Microsoft Fabric

## Basic Implementation

### Minimal Code Example

```tsx
import React from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';
import './App.css';

function App() {
  return (
    <div style={{ padding: '20px' }}>
      <h2>Basic Slider</h2>
      <SliderComponent id="slider" value={30} />
    </div>
  );
}

export default App;
```

This creates a horizontal slider with:
- Default value: 30
- Range: 0-100 (defaults)
- No tooltip or ticks visible

### Run Your Project

```bash
npm run dev
```

Then open `http://localhost:5173` (Vite) or `http://localhost:3000` (Create React App) in your browser.

## First Working Example

### Complete Starter Project

Create `src/App.tsx`:

```tsx
import React, { useState } from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';
import '@syncfusion/ej2-base/styles/material.css';
import '@syncfusion/ej2-buttons/styles/material.css';
import '@syncfusion/ej2-popups/styles/material.css';
import '@syncfusion/ej2-react-inputs/styles/material.css';
import './App.css';

function App() {
  const [selectedValue, setSelectedValue] = useState(30);

  return (
    <div className="container">
      <h1>React RangeSlider Example</h1>
      
      <div className="slider-section">
        <h2>Single Value Slider</h2>
        <p>Selected: {selectedValue}</p>
        <SliderComponent
          id="default-slider"
          value={selectedValue}
          change={(e) => setSelectedValue(e.value as number)}
          min={0}
          max={100}
        />
      </div>

      <div className="slider-section">
        <h2>Range Slider (Two Handles)</h2>
        <SliderComponent
          id="range-slider"
          type="Range"
          value={[20, 80]}
          min={0}
          max={100}
          tooltip={{ isVisible: true }}
        />
      </div>

      <div className="slider-section">
        <h2>MinRange Slider</h2>
        <SliderComponent
          id="minrange-slider"
          type="MinRange"
          value={40}
          min={0}
          max={100}
          tooltip={{ isVisible: true }}
        />
      </div>
    </div>
  );
}

export default App;
```

Add styling to `src/App.css`:

```css
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

h1 {
  color: #333;
  text-align: center;
}

.slider-section {
  background: #f5f5f5;
  padding: 20px;
  margin: 20px 0;
  border-radius: 8px;
}

.slider-section h2 {
  font-size: 18px;
  margin-top: 0;
}

.slider-section p {
  color: #666;
  margin: 10px 0;
}

/* Slider container spacing */
.e-slider-container {
  margin: 30px 0;
}
```

Run the project:

```bash
npm run dev
```

You should see three different slider types working.

## Importing CSS Themes

### Complete Theme List

All available themes in Syncfusion:

```tsx
// Material Design Theme
import '@syncfusion/ej2-react-inputs/styles/material.css';

// Material Dark Theme
import '@syncfusion/ej2-react-inputs/styles/material-dark.css';

// Bootstrap 4 Theme
import '@syncfusion/ej2-react-inputs/styles/bootstrap4.css';

// Bootstrap 5 Theme
import '@syncfusion/ej2-react-inputs/styles/bootstrap5.css';

// Bootstrap Dark Theme
import '@syncfusion/ej2-react-inputs/styles/bootstrap-dark.css';

// Fluent Theme
import '@syncfusion/ej2-react-inputs/styles/fluent.css';

// Tailwind CSS 3 Theme
import '@syncfusion/ej2-react-inputs/styles/tailwind3.css';

// Fabric Theme
import '@syncfusion/ej2-react-inputs/styles/fabric.css';

// High Contrast Theme
import '@syncfusion/ej2-react-inputs/styles/highcontrast.css';
```

**Choose based on your design system:**
- Material: Google's Material Design
- Bootstrap: Bootstrap framework
- Fluent: Microsoft Office aesthetic
- Tailwind: Utility-first CSS approach
- Fabric: Microsoft Office Fabric design

## Minimal Configuration

### Simplest Possible Setup

```tsx
import { SliderComponent } from '@syncfusion/ej2-react-inputs';
import '@syncfusion/ej2-react-inputs/styles/material.css';

export default function App() {
  return <SliderComponent id="slider" value={50} />;
}
```

This provides:
- ✅ Working slider component
- ✅ Default styling
- ✅ Range 0-100
- ✅ Initial value 50

### Add Minimum Configuration

```tsx
<SliderComponent
  id="slider"
  value={50}
  min={10}
  max={90}
  step={5}
/>
```

With this you get:
- ✅ Custom range (10-90)
- ✅ Step increments (5 units)
- ✅ User can drag or use keyboard

### Common Starting Props

```tsx
<SliderComponent
  id="slider"                    // Unique ID
  value={50}                     // Initial value
  min={0}                        // Minimum allowed
  max={100}                      // Maximum allowed
  step={1}                       // Increment
  orientation="Horizontal"       // Direction
  change={(e) => console.log(e)} // Value changed
/>
```

## Troubleshooting Setup

### "Module not found" Error

**Problem:** `Cannot find module '@syncfusion/ej2-react-inputs'`

**Solution:**
```bash
npm install @syncfusion/ej2-react-inputs
npm install
```

### Styles Not Applied

**Problem:** Slider renders but has no styling

**Solution:** Ensure CSS imports are at the top of your component or App file:

```tsx
import '@syncfusion/ej2-react-inputs/styles/material.css';
```

### TypeScript Errors

**Problem:** Type errors with SliderComponent

**Solution:** Install type definitions:

```bash
npm install --save-dev @types/react @types/react-dom
```

## Next Steps

1. ✅ You now have a working RangeSlider
2. Read [types-and-orientation.md](types-and-orientation.md) to understand slider types
3. Explore [tooltips-and-ticks.md](tooltips-and-ticks.md) for visual enhancements
4. Check [styling.md](styling.md) for custom appearance
5. Review [accessibility.md](accessibility.md) for screen reader support
