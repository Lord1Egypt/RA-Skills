# Getting Started with React Splitter

## Table of Contents
- [Installation](#installation)
- [CSS Import](#css-import)
- [Basic Setup](#basic-setup)
- [First Working Example](#first-working-example)
- [Dependencies](#dependencies)

## Installation

The Splitter component is part of the `@syncfusion/ej2-react-layouts` package. Install it using npm:

```bash
npm install @syncfusion/ej2-react-layouts --save
```

This automatically installs the required dependencies:
- `@syncfusion/ej2-base` - Base utilities
- `@syncfusion/ej2-layouts` - Layout components CSS and logic

### Verify Installation

After installation, verify the package in `package.json`:

```json
{
  "dependencies": {
    "@syncfusion/ej2-react-layouts": "^latest",
    "@syncfusion/ej2-base": "^latest"
  }
}
```

## CSS Import

The Splitter component requires CSS files for styling. Import these in your main component or App.css:

### Tailwind 3 Theme
```css
@import '../../node_modules/@syncfusion/ej2-base/styles/tailwind3.css';
@import '../../node_modules/@syncfusion/ej2-layouts/styles/tailwind3.css';
```

### Bootstrap 5 Theme
```css
@import '../../node_modules/@syncfusion/ej2-base/styles/bootstrap5.css';
@import '../../node_modules/@syncfusion/ej2-layouts/styles/bootstrap5.css';
```

### Material Theme
```css
@import '../../node_modules/@syncfusion/ej2-base/styles/material.css';
@import '../../node_modules/@syncfusion/ej2-layouts/styles/material.css';
```

### Fluent Theme
```css
@import '../../node_modules/@syncfusion/ej2-base/styles/fluent.css';
@import '../../node_modules/@syncfusion/ej2-layouts/styles/fluent.css';
```

**Best Practice:** Import CSS in your main App component (App.tsx/App.jsx) before rendering Splitter.

## Basic Setup

The Splitter requires two child components:
1. **PanesDirective** - Container for all panes
2. **PaneDirective** - Individual pane configuration

### Minimal Structure

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';

function App() {
  return (
    <SplitterComponent>
      <PanesDirective>
        <PaneDirective size='300px'>
          <div>Left Pane</div>
        </PaneDirective>
        <PaneDirective size='300px'>
          <div>Right Pane</div>
        </PaneDirective>
      </PanesDirective>
    </SplitterComponent>
  );
}
```

### Import Statements

```tsx
// Import components
import { 
  PaneDirective, 
  PanesDirective, 
  SplitterComponent 
} from '@syncfusion/ej2-react-layouts';

// Import hooks if needed for refs
import * as React from 'react';
```

## First Working Example

Complete working example with two horizontal panes:

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <div className='App'>
      <h2>React Splitter - Getting Started</h2>
      
      <SplitterComponent orientation='Horizontal'>
        <PanesDirective>
          <PaneDirective size='200px'>
            <div style={{ padding: '20px', backgroundColor: '#f5f5f5' }}>
              <h3>Left Panel</h3>
              <p>This is the left panel with fixed size</p>
            </div>
          </PaneDirective>
          
          <PaneDirective size='300px'>
            <div style={{ padding: '20px', backgroundColor: '#ffffff' }}>
              <h3>Right Panel</h3>
              <p>This panel is resizable. Drag the separator to resize.</p>
            </div>
          </PaneDirective>
        </PanesDirective>
      </SplitterComponent>
    </div>
  );
}

export default App;
```

### CSS for Example

```css
.App {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.e-splitter {
  height: 400px;
  border: 1px solid #ddd;
}

.e-pane {
  overflow: auto;
}
```

## Dependencies

### Required Packages
- `@syncfusion/ej2-react-layouts` - React Splitter component
- `@syncfusion/ej2-base` - Base utilities and styles
- `react` - React library (v16.8+)
- `react-dom` - React DOM library (v16.8+)

### Peer Dependencies
```json
{
  "peerDependencies": {
    "react": ">=16.8.0",
    "react-dom": ">=16.8.0"
  }
}
```

### Compatibility
- **React:** 16.8+ (hooks support required)
- **TypeScript:** 3.5+ (optional, for type definitions)
- **Node:** 12+

## Next Steps

After successful setup:
1. **Configure Panes** - Move to pane-layout-configuration.md to add multiple panes and nested layouts
2. **Adjust Sizing** - Use pane-sizing-and-separation.md for size management
3. **Add Features** - Explore expand-collapse, resize events, and other functionality

## Common Setup Issues

**Issue:** Styles not applying
- **Solution:** Ensure CSS imports are at the top of your App component

**Issue:** Components not recognized
- **Solution:** Verify correct import path: `@syncfusion/ej2-react-layouts`

**Issue:** TypeScript errors
- **Solution:** Install type definitions: `npm install --save-dev @types/react`

**Issue:** Height not rendering
- **Solution:** Set explicit height on parent container: `<div style={{height: '500px'}}>`
