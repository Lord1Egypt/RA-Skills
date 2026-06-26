# Getting Started with React Circular Gauge

This guide covers installation, setup, and creating your first Circular Gauge component.

## Table of contents

- [Installation](#installation)
  - [Step 1: Install the Package](#step-1-install-the-package)
  - [Import CSS Theme](#step-2-import-css-theme)
- [Project Setup](#project-setup)
  - [Using Vite (Recommended)](#using-vite-recommended)
  - [Using Create React App](#using-create-react-app)
  - [Using TypeScript](#using-typescript)
- [Basic Component Initialization](#basic-component-initialization)
  - [Minimal Example](#minimal-example)
  - [Add a Container Height](#add-a-container-height)
- [Working Example: Simple Speedometer](#working-example-simple-speedometer)
- [Common Initialization Issues](#common-initialization-issues)
  - [Issue: Gauge Not Rendering](#issue-gauge-not-rendering)
  - [Issue: CSS Not Applied](#issue-css-not-applied)
  - [Issue: Types Not Found (TypeScript)](#issue-types-not-found-typescript)
- [Next Steps](#next-steps)

---

## Installation

### Step 1: Install the Package

```bash
npm install @syncfusion/ej2-react-circulargauge --save
```

The Circular Gauge package has the following dependencies:
- `@syncfusion/ej2-react-base`
- `@syncfusion/ej2-circulargauge`
- `@syncfusion/ej2-base`
- `@syncfusion/ej2-svg-base`
- `@syncfusion/ej2-paf-export` (for print/export)

All dependencies are installed automatically with npm.

### Step 2: Theme Customizing

**Available themes:**
- `material.css` - Material Design theme (default)
- `fabric.css` - Fabric theme
- `bootstrap.css` - Bootstrap theme
- `bootstrap4.css` - Bootstrap 4 theme
- `fluent.css` - Fluent Design theme
- `highcontrast.css` - High contrast theme

---

## Project Setup

### Using Vite (Recommended)

Vite provides faster development with optimized builds.

```bash
# Create new project
npm create vite@latest my-gauge-app -- --template react-ts

# Install dependencies
cd my-gauge-app
npm install

# Install Circular Gauge
npm install @syncfusion/ej2-react-circulargauge --save

# Start dev server
npm run dev
```

### Using Create React App

```bash
# Create new project
npx create-react-app my-gauge-app

# Install dependencies
cd my-gauge-app

# Install Circular Gauge
npm install @syncfusion/ej2-react-circulargauge --save

# Start dev server
npm start
```

### Using TypeScript

Both Vite and CRA support TypeScript. For Vite:

```bash
npm create vite@latest my-gauge-app -- --template react-ts
```

This provides TypeScript support with proper type definitions for Syncfusion components.

---

## Basic Component Initialization

### Minimal Example

The simplest working Circular Gauge requires the component wrapper and at least one axis:

```tsx
import React from 'react';
import { CircularGaugeComponent, AxesDirective, AxisDirective } 
  from '@syncfusion/ej2-react-circulargauge';

export function App() {
  return (
    <div style={{ height: '500px' }}>
      <CircularGaugeComponent>
        <AxesDirective>
          <AxisDirective />
        </AxesDirective>
      </CircularGaugeComponent>
    </div>
  );
}

export default App;
```

This renders a default circular gauge with:
- Start angle: 200°
- End angle: 160°
- Minimum value: 0
- Maximum value: 100
- Default pointer at value 0

### Add a Container Height

Always wrap the gauge in a container with a defined height:

```tsx
<div style={{ height: '500px', width: '100%' }}>
  <CircularGaugeComponent>
    {/* gauge content */}
  </CircularGaugeComponent>
</div>
```

Without a height, the gauge may not render correctly.

---

## Working Example: Simple Speedometer

Here's a complete working example with installation steps:

```tsx
import React from 'react';
import { CircularGaugeComponent, AxesDirective, AxisDirective,
         PointersDirective, PointerDirective, RangesDirective, RangeDirective }
  from '@syncfusion/ej2-react-circulargauge';

export function App() {
  return (
    <div style={{ height: '600px', width: '100%' }}>
      <CircularGaugeComponent
        title="Speed (km/h)"
        titleStyle={{
          size: '20px',
          color: '#424242'
        }}
        centerX="50%"
        centerY="50%"
      >
        <AxesDirective>
          <AxisDirective
            minimum={0}
            maximum={240}
            startAngle={270}
            endAngle={90}
            lineStyle={{ width: 2, color: '#E0E0E0' }}
            majorTicks={{
              interval: 20,
              width: 2,
              color: '#616161'
            }}
            minorTicks={{
              interval: 4,
              width: 1,
              color: '#9E9E9E'
            }}
            labelStyle={{
              color: '#616161',
              offset: 15
            }}
          >
            {/* Define colored ranges */}
            <RangesDirective>
              <RangeDirective 
                start={0} 
                end={60} 
                color='#30B32D'
                startWidth={10}
                endWidth={10}
              />
              <RangeDirective 
                start={60} 
                end={120} 
                color='#FFDD00'
                startWidth={10}
                endWidth={10}
              />
              <RangeDirective 
                start={120} 
                end={240} 
                color='#F03E3E'
                startWidth={10}
                endWidth={10}
              />
            </RangesDirective>

            {/* Add pointer */}
            <PointersDirective>
              <PointerDirective
                value={85}
                type='Needle'
                radius='80%'
                pointerWidth={5}
                color='#424242'
                cap={{
                  radius: 8,
                  color: '#424242',
                  border: {
                    color: '#ffffff',
                    width: 2
                  }
                }}
                needleTail={{
                  length: '20%',
                  color: '#424242'
                }}
              />
            </PointersDirective>
          </AxisDirective>
        </AxesDirective>
      </CircularGaugeComponent>
    </div>
  );
}

export default App;
```

**Installation steps:**
1. Create React app: `npm create vite@latest my-app -- --template react-ts`
2. Install gauge: `npm install @syncfusion/ej2-react-circulargauge --save`
3. Copy the code above into `src/App.tsx`
4. Run: `npm run dev`
5. Open browser to `http://localhost:5173`

---

## Common Initialization Issues

### Issue: Gauge Not Rendering

**Cause:** Missing container height
```tsx
// ❌ Wrong
<CircularGaugeComponent>
  <AxesDirective>
    <AxisDirective />
  </AxesDirective>
</CircularGaugeComponent>

// ✅ Correct
<div style={{ height: '500px' }}>
  <CircularGaugeComponent>
    <AxesDirective>
      <AxisDirective />
    </AxesDirective>
  </CircularGaugeComponent>
</div>
```

### Issue: Types Not Found (TypeScript)

**Cause:** Missing type definitions
```bash
# Types are included in the package, but ensure proper TypeScript setup
npm install --save-dev typescript @types/react @types/node
```

---

## Next Steps

Also review the API reference: [api-reference.md](api-reference.md)

Once you have the basic gauge working:

1. **Configure axes and pointers** → See [axes-pointers-ranges.md](axes-pointers-ranges.md)
2. **Customize appearance** → See [appearance-dimensions.md](appearance-dimensions.md)
3. **Add interactions** → See [advanced-features.md](advanced-features.md)
4. **View common patterns** → See [common-patterns.md](common-patterns.md)
