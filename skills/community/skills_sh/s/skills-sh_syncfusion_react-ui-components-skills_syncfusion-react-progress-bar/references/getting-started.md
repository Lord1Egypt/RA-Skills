# Getting Started with React Progress Bar

## Table of Contents

- [Installation](#installation)
- [CSS Theme Setup](#css-theme-setup)
- [Basic Implementation](#basic-implementation)
  - [Linear Progress Bar (Default)](#linear-progress-bar-default)
  - [Circular Progress Bar](#circular-progress-bar)
- [TypeScript Setup](#typescript-setup)
- [Project Setup Variations](#project-setup-variations)
  - [Vite + React](#vite--react)
  - [Create React App](#create-react-app)
- [Common Setup Issues](#common-setup-issues)
  - [Issue: Styles Not Applying](#issue-styles-not-applying)
  - [Issue: "Cannot find module" Error](#issue-cannot-find-module-error)
  - [Issue: Circular Progress Bar Not Showing](#issue-circular-progress-bar-not-showing)
- [License Registration (Optional)](#license-registration-optional)
- [Next Steps](#next-steps)
- [Troubleshooting Quick Reference](#troubleshooting-quick-reference)

## Installation

The Syncfusion Progress Bar component is part of the `@syncfusion/ej2-react-progressbar` package. Install it via npm:

```bash
npm install @syncfusion/ej2-react-progressbar --save
```

This will automatically install required dependencies:
- `@syncfusion/ej2-base` - Core utilities
- `@syncfusion/ej2-svg-base` - SVG rendering for circular types
- `@syncfusion/ej2-data` - Data handling

**Theme Selection Guide:**
- **Material** (recommended): Modern, flat design with Material Design principles
- **Bootstrap5**: Latest Bootstrap styling and components
- **Tailwind**: Utility-first CSS framework style  
- **Fluent**: Microsoft Fluent Design System
- **Highcontrast**: Enhanced visibility for accessibility

## Basic Implementation

### Linear Progress Bar (Default)

```tsx
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

function App() {
  return (
    <ProgressBarComponent
      id="linear"
      type="Linear"
      value={75}
      height="60"
      theme="Material"
    />
  );
}

export default App;
```

**What this does:**
- Creates a linear (horizontal) progress bar
- `value={75}` shows 75% completion
- `height="60"` sets the height to 60 pixels
- Default theme: Material

### Circular Progress Bar

```tsx
<ProgressBarComponent
  id="circular"
  type="Circular"
  value={60}
  height="160px"
/>
```

**What this does:**
- Creates a circular (donut) progress bar
- Better for confined spaces
- `height="160px"` defines the diameter
- Value still represents percentage (0-100)

### Semi-Circular Progress Bar

```tsx
<ProgressBarComponent
  id="semicircle"
  type="Semicircle"
  value={75}
  height="160px"
/>
```

**What this does:**
- Creates a semi-circular (half-circle) progress bar
- Useful for dashboard panels and mobile layouts
- Height defines the radius
- Great for space-constrained layouts

## TypeScript Setup

For TypeScript projects, types are included automatically:

```tsx
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';
import { ProgressBarProps } from '@syncfusion/ej2-react-progressbar';

interface AppProps extends ProgressBarProps {}

const App: React.FC<AppProps> = () => {
  return (
    <ProgressBarComponent
      id="progress"
      type="Linear"
      value={50}
    />
  );
};

export default App;
```

## Project Setup Variations

### Vite + React

```bash
npm create vite@latest my-app -- --template react
cd my-app
npm install @syncfusion/ej2-react-progressbar
npm run dev
```

**App.tsx:**
```tsx
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';
import './App.css';

function App() {
  return (
    <div>
      <h1>Progress Bar Example</h1>
      <ProgressBarComponent id="progress" value={40} />
    </div>
  );
}

export default App;
```

### Create React App

```bash
npx create-react-app my-app
cd my-app
npm install @syncfusion/ej2-react-progressbar
npm start
```

**App.js:**
```jsx
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';
import './App.css';

function App() {
  return (
    <div className="App">
      <h1>Progress Bar Example</h1>
      <ProgressBarComponent id="progress" value={40} />
    </div>
  );
}

export default App;
```

## Common Setup Issues

### Issue: Styles Not Applying

**Problem:** Progress bar renders but styling is missing (no colors, distorted shape)

**Solution:** Verify CSS import is at top of file:
```tsx
// ✓ CORRECT - CSS imported first
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

// ✗ WRONG - CSS after component import
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

```

### Issue: "Cannot find module" Error

**Problem:** TypeScript can't find Syncfusion types

**Solution:** Ensure package is installed:
```bash
npm install @syncfusion/ej2-react-progressbar
```

Delete `node_modules` and reinstall if issue persists:
```bash
rm -r node_modules package-lock.json
npm install
```

### Issue: Circular Progress Bar Not Showing

**Problem:** Circular type renders as linear or disappears

**Solution:** Set height for circular type:
```tsx
<ProgressBarComponent
  type="Circular"
  value={50}
  height="150px"  // Required for circular
/>
```

## License Registration (Optional)

If you have Syncfusion license, register it in your root component:

```tsx
import { registerLicense } from '@syncfusion/ej2-base';

// Register license
registerLicense('YOUR_LICENSE_KEY_HERE');

// Component code follows
```

**Without license:** Components work in development with a watermark (shows in evaluation mode)

## Next Steps

- **Types & Shapes:** Ready to explore different progress bar shapes? Read [types-and-shapes.md](types-and-shapes.md)
- **States & Modes:** Want to learn determinate vs. indeterminate? Read [states-and-modes.md](states-and-modes.md)
- **Customization:** Ready to style and customize? Read [customization-and-styling.md](customization-and-styling.md)
- **Advanced:** Learn animations and events? Read [animations-events-accessibility.md](animations-events-accessibility.md)

## Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| Cannot find module | Run `npm install @syncfusion/ej2-react-progressbar` |
| Circular type broken | Add `height` prop with pixel value (e.g., `height="160px"`) |
| Semicircle type not showing | Set `type="Semicircle"` and provide height value |
| Types not recognized | Ensure package version is ≥20.0.0 |
| Build fails | Clear `node_modules` and reinstall: `rm -rf node_modules && npm install` |
| Progress value not displaying | Set `showProgressValue={true}` on the component |
| Animation not working | Ensure animation object is properly configured: `animation={{ enable: true, duration: 2000 }}` |

## Complete Working Example with All Features

```tsx
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

import { useState, useEffect } from 'react';

function App() {
  const [linearProgress, setLinearProgress] = useState(0);
  const [circularProgress, setCircularProgress] = useState(0);
  const [semicircleProgress, setSemicircleProgress] = useState(0);

  useEffect(() => {
    // Simulate progress updates
    const interval = setInterval(() => {
      setLinearProgress(prev => (prev >= 100 ? 0 : prev + 10));
      setCircularProgress(prev => (prev >= 100 ? 0 : prev + 8));
      setSemicircleProgress(prev => (prev >= 100 ? 0 : prev + 12));
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Syncfusion Progress Bar Examples</h1>

      {/* Linear Progress Bar */}
      <section>
        <h2>Linear Progress Bar</h2>
        <ProgressBarComponent
          id="linear"
          type="Linear"
          value={linearProgress}
          height="30"
          showProgressValue={true}
          animation={{ enable: true, duration: 1000, delay: 0 }}
        />
      </section>

      {/* Circular Progress Bar */}
      <section>
        <h2>Circular Progress Bar</h2>
        <ProgressBarComponent
          id="circular"
          type="Circular"
          value={circularProgress}
          height="160px"
          showProgressValue={true}
          animation={{ enable: true, duration: 1000, delay: 0 }}
        />
      </section>

      {/* Semi-Circular Progress Bar */}
      <section>
        <h2>Semi-Circular Progress Bar</h2>
        <ProgressBarComponent
          id="semicircle"
          type="Semicircle"
          value={semicircleProgress}
          height="160px"
          showProgressValue={true}
          animation={{ enable: true, duration: 1000, delay: 0 }}
        />
      </section>

      {/* Indeterminate Progress (Loading Spinner) */}
      <section>
        <h2>Loading Spinner (Indeterminate)</h2>
        <ProgressBarComponent
          id="spinner"
          type="Circular"
          isIndeterminate={true}
          height="100px"
          animation={{ enable: true, duration: 2000 }}
        />
      </section>

      {/* Buffer Progress */}
      <section>
        <h2>Buffer Progress (Streaming)</h2>
        <ProgressBarComponent
          id="buffer"
          type="Linear"
          value={40}
          secondaryProgress={75}
          height="30"
          animation={{ enable: true, duration: 1000 }}
        />
        <p>Actual: 40% | Buffered: 75%</p>
      </section>
    </div>
  );
}

export default App;
```

This example demonstrates all three types of progress bars and key features.
