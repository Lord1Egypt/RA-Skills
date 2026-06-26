# Getting Started with React Linear Gauge

See API Reference: [API Reference](api-reference.md)

## Table of Contents

- [Installation](#installation)
- [Project Setup](#project-setup)
  - [Setup with Vite (Recommended)](#setup-with-vite-recommended)
  - [Setup with Create React App](#setup-with-create-react-app)
- [Basic Component Import](#basic-component-import)
- [CSS Themes](#css-themes)
- [Minimal Working Example](#minimal-working-example)
- [First Gauge with Custom Axis Range](#first-gauge-with-custom-axis-range)
- [Adding Ranges for Visual Zones](#adding-ranges-for-visual-zones)
- [Adding a Title](#adding-a-title)
- [Setting Container Dimensions](#setting-container-dimensions)
- [Running Your Application](#running-your-application)
- [Next Steps](#next-steps)

## Installation

The Linear Gauge component is provided through the `@syncfusion/ej2-react-lineargauge` package. Install it using npm:

```bash
npm install @syncfusion/ej2-react-lineargauge --save
```

This will also automatically install the required dependencies:
- `@syncfusion/ej2-lineargauge` - Core Linear Gauge library
- `@syncfusion/ej2-base` - Base utilities
- `@syncfusion/ej2-svg-base` - SVG rendering engine
- `@syncfusion/ej2-react-base` - React integration

## Project Setup

### Setup with Vite (Recommended)

Vite provides faster development with optimized builds:

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm run dev
```

Then install the Linear Gauge package:
```bash
npm install @syncfusion/ej2-react-lineargauge --save
```

### Setup with Create React App

If using Create React App instead:

```bash
npx create-react-app my-app
cd my-app
npm install @syncfusion/ej2-react-lineargauge --save
```

## Basic Component Import

To use the Linear Gauge, import the required components from the Syncfusion package:

```tsx
import { LinearGaugeComponent, AxesDirective, AxisDirective, 
         PointersDirective, PointerDirective, RangesDirective, RangeDirective } 
  from '@syncfusion/ej2-react-lineargauge';
```

## CSS Themes

Import the appropriate theme CSS file. Syncfusion provides several built-in themes:

```tsx
// Material theme (light)
import '@syncfusion/ej2-lineargauge/styles/material.css';

// Or Bootstrap theme
import '@syncfusion/ej2-lineargauge/styles/bootstrap.css';

// Or Fabric theme
import '@syncfusion/ej2-lineargauge/styles/fabric.css';

// Or Tailwind CSS theme
import '@syncfusion/ej2-lineargauge/styles/tailwind.css';
```

Place the theme import at the top of your `App.tsx` or `main.tsx` file.

## Minimal Working Example

Here's the simplest way to get a Linear Gauge running:

```tsx
import React from 'react';
import { LinearGaugeComponent } from '@syncfusion/ej2-react-lineargauge';

export function App() {
  return <LinearGaugeComponent></LinearGaugeComponent>;
}

export default App;
```

This renders a basic gauge with default settings (0-100 scale, single bar pointer at value 50).

## First Gauge with Custom Axis Range

To set a custom axis range and pointer value:

```tsx
import React from 'react';
import { LinearGaugeComponent, AxesDirective, AxisDirective, 
         PointersDirective, PointerDirective } 
  from '@syncfusion/ej2-react-lineargauge';

export function App() {
  return (
    <LinearGaugeComponent>
      <AxesDirective>
        <AxisDirective minimum={0} maximum={200}>
          <PointersDirective>
            <PointerDirective value={140} />
          </PointersDirective>
        </AxisDirective>
      </AxesDirective>
    </LinearGaugeComponent>
  );
}

export default App;
```

This creates a gauge with:
- Axis range: 0 to 200
- Pointer value: 140

## Adding Ranges for Visual Zones

Ranges highlight different value zones with colors:

```tsx
import React from 'react';
import { LinearGaugeComponent, AxesDirective, AxisDirective, 
         PointersDirective, PointerDirective, RangesDirective, RangeDirective } 
  from '@syncfusion/ej2-react-lineargauge';

export function App() {
  return (
    <LinearGaugeComponent title="Temperature Gauge">
      <AxesDirective>
        <AxisDirective 
          minimum={0} 
          maximum={100}
          labelStyle={{ format: '{value}°C' }}
        >
          <RangesDirective>
            <RangeDirective start={0} end={30} color='#1E90FF' />
            <RangeDirective start={30} end={70} color='#FFA500' />
            <RangeDirective start={70} end={100} color='#FF4500' />
          </RangesDirective>
          
          <PointersDirective>
            <PointerDirective value={55} />
          </PointersDirective>
        </AxisDirective>
      </AxesDirective>
    </LinearGaugeComponent>
  );
}

export default App;
```

This creates:
- Temperature scale from 0-100°C
- Three colored zones: cold (blue), warm (orange), hot (red-orange)
- Pointer at 55°C in the warm zone

## Adding a Title

Display a meaningful heading for your gauge:

```tsx
<LinearGaugeComponent 
  title="Linear Gauge" 
>
  {/* axes, pointers, ranges */}
</LinearGaugeComponent>
```

## Setting Container Dimensions

Control the size of the gauge container:

```tsx
<div style={{ height: '400px', width: '100%' }}>
  <LinearGaugeComponent>
    {/* configuration */}
  </LinearGaugeComponent>
</div>
```

Or set dimensions directly on the component:

```tsx
<LinearGaugeComponent
  width="100%"
  height="400px"
>
  {/* configuration */}
</LinearGaugeComponent>
```

## Running Your Application

Start the development server:

```bash
npm run dev
```

Open your browser and navigate to the local URL (typically `http://localhost:5173` for Vite or `http://localhost:3000` for Create React App).

## Next Steps

- Read **Axis, Ticks & Labels** reference to customize the scale
- Read **Pointer Types** reference to use different pointer visualizations
- Read **Ranges & Annotations** reference to add descriptive elements
- Read **Customization** reference for styling and appearance
