# Getting Started with Smith Charts

## Table of Contents
- [Overview](#overview)
- [Dependencies](#dependencies)
- [Installation and Configuration](#installation-and-configuration)
- [Installing Syncfusion Package](#installing-syncfusion-package)
- [Basic Implementation](#basic-implementation)
- [Module Injection](#module-injection)
- [Adding Series](#adding-series)
- [Adding Title](#adding-title)
- [Enabling Markers](#enabling-markers)
- [Enabling Data Labels](#enabling-data-labels)
- [Enabling Legend](#enabling-legend)
- [Enabling Tooltips](#enabling-tooltips)
- [Complete Working Example](#complete-working-example)

## Overview

This guide walks you through creating a simple Smith Chart and demonstrates the basic usage of the Syncfusion React Smith Chart component. Smith Charts are specialized diagrams used in electrical engineering to visualize transmission line parameters, impedance matching, and RF circuit characteristics.

## Dependencies

Below is the list of minimum dependencies required to use the Smith Chart component:

```
|-- @syncfusion/ej2-react-charts
    |-- @syncfusion/ej2-charts
    |-- @syncfusion/ej2-base
    |-- @syncfusion/ej2-data
    |-- @syncfusion/ej2-svg-base
    |-- @syncfusion/ej2-pdf-export
    |-- @syncfusion/ej2-compression
    |-- @syncfusion/ej2-file-utils
    |-- @syncfusion/ej2-react-base
```

## Installation and Configuration

### Using Vite (Recommended)

To easily set up a React application, use the Vite CLI, which provides a faster development environment, smaller bundle sizes, and optimized builds.

**Create a new React application:**

```bash
npm create vite@latest my-app
```

This command will prompt you for a few settings for the new project, such as selecting a framework and a variant.

**For TypeScript environment:**

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm run dev
```

**For JavaScript environment:**

```bash
npm create vite@latest my-app -- --template react
cd my-app
npm run dev
```

### Using create-react-app (Alternative)

If you prefer the traditional approach:

```bash
npx create-react-app my-app
cd my-app
npm start
```

## Installing Syncfusion Package

All Syncfusion Essential JS 2 packages are published in the [`npmjs.com`](https://www.npmjs.com/~syncfusionorg) public registry.

To install the Smith Chart package, use the following command:

```bash
npm install @syncfusion/ej2-react-charts --save
```

The `--save` flag will include the Smith Chart package in the dependencies section of the package.json.

## Basic Implementation

Add the Smith Chart component to `src/App.tsx` (or `src/App.jsx` for JavaScript) using the following code:

```tsx
import * as React from "react";
import { SmithchartComponent } from '@syncfusion/ej2-react-charts';

function App() {
  return <SmithchartComponent></SmithchartComponent>;
}

export default App;
```

Now run the development server:

```bash
npm run dev
```

This will render a basic empty Smith Chart with default settings.

## Module Injection

Smith Chart features are segregated into individual feature-wise modules. To use a particular feature, you need to inject its feature service into the component.

### Available Feature Modules

- **`SmithchartLegend`** - Inject this module to use legend feature
- **`TooltipRender`** - Inject this module to use tooltip feature

Import these modules from the chart package and inject them into the `services` section of the Smith Chart component:

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartLegend, TooltipRender, Inject } from '@syncfusion/ej2-react-charts';

function App() {
  return (
    <SmithchartComponent>
      <Inject services={[SmithchartLegend, TooltipRender]} />
    </SmithchartComponent>
  );
}

export default App;
```

## Adding Series

Smith Chart has two specifications for adding series data:

### Method 1: Using dataSource

Bind a data object directly by specifying `resistance` and `reactance` field names. The series renders from the provided dataSource.

```tsx
import * as React from "react";
import { SmithchartComponent,SmithchartSeriesCollectionDirective , SmithchartSeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const transmissionData = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0, reactance: 0.1 },
    { resistance: 0, reactance: 0.2 },
    { resistance: 0.3, reactance: 0.3 },
    { resistance: 0.5, reactance: 0.4 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <SmithchartComponent id="smithchart">
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective
          dataSource={transmissionData}
          resistance="resistance"
          reactance="reactance"
        />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

### Method 2: Using points

Provide a collection of resistance and reactance value points directly:

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const transmissionPoints = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0, reactance: 0.1 },
    { resistance: 0, reactance: 0.2 },
    { resistance: 0.3, reactance: 0.3 },
    { resistance: 0.5, reactance: 0.4 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <SmithchartComponent id="smithchart">
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective points={transmissionPoints} />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

## Adding Title

You can add a title to the Smith Chart to provide quick information about the data being plotted:

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const transmissionData = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.3, reactance: 0.2 },
    { resistance: 1.0, reactance: 0.4 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      title={{ text: 'Transmission Line Impedance Analysis' }}
    >
      <SmithchartSeriesCollectionDirective>
        <SmithChartSeriesDirective points={transmissionData} />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

## Enabling Markers

You can add markers to data points by setting the `visible` property to `true` in the `marker` object:

```tsx
<SmithChartSeriesDirective
  points={transmissionData}
  marker={{ visible: true }}
/>
```

## Enabling Data Labels

Add data labels to improve readability by setting the `visible` property to `true` in the `dataLabel` object within marker settings:

```tsx
<SmithChartSeriesDirective
  points={transmissionData}
  marker={{
    visible: true,
    dataLabel: { visible: true }
  }}
/>
```

Data labels are arranged smartly to avoid overlapping based on the series configuration.

## Enabling Legend

Enable legend by setting the `visible` property to `true` in `legendSettings` and injecting the `SmithchartLegend` module:

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective, Inject, SmithchartLegend } from '@syncfusion/ej2-react-charts';

function App() {
  const series1Data = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.3, reactance: 0.2 },
    { resistance: 1.0, reactance: 0.4 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      legendSettings={{ visible: true }}
    >
      <Inject services={[SmithchartLegend]} />
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective
          name="Transmission Line 1"
          points={series1Data}
        />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

Customize the series name using the `name` property in SeriesDirective.

## Enabling Tooltips

Enable tooltips by setting the `visible` property to `true` in the `tooltip` object and injecting the `TooltipRender` module:

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective, Inject, TooltipRender } from '@syncfusion/ej2-react-charts';

function App() {
  const transmissionData = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.3, reactance: 0.2 },
    { resistance: 1.0, reactance: 0.4 }
  ];

  return (
    <SmithchartComponent id="smithchart">
      <Inject services={[TooltipRender]} />
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective
          points={transmissionData}
          tooltip={{ visible: true }}
        />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

Tooltips display point information when hovering over data points with the mouse.

## Complete Working Example

Here's a complete example combining all the features:

```tsx
import * as React from 'react';
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective, Inject, SmithchartLegend, TooltipRender } from '@syncfusion/ej2-react-charts';

function App() {
  // First transmission line data
  const transmission1Data = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0, reactance: 0.1 },
    { resistance: 0, reactance: 0.2 },
    { resistance: 0.3, reactance: 0.3 },
    { resistance: 0.5, reactance: 0.4 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  // Second transmission line data
  const transmission2Data = [
    { resistance: 0.1, reactance: 0.1 },
    { resistance: 0.2, reactance: 0.2 },
    { resistance: 0.4, reactance: 0.3 },
    { resistance: 0.6, reactance: 0.4 },
    { resistance: 0.8, reactance: 0.5 },
    { resistance: 1.2, reactance: 0.6 }
  ];

  return (
    <div style={{ padding: '20px' }}>
      <SmithchartComponent
        id="smithchart"
        title={{ text: 'Transmission Line Impedance Analysis' }}
        legendSettings={{ visible: true, position: 'Bottom' }}
      >
        <Inject services={[SmithchartLegend, TooltipRender]} />
        <SmithchartSeriesCollectionDirective>
          <SmithchartSeriesDirective
            name="Transmission Line 1"
            points={transmission1Data}
            marker={{
              visible: true,
              dataLabel: { visible: true }
            }}
            tooltip={{ visible: true }}
          />
          <SmithchartSeriesDirective
            name="Transmission Line 2"
            points={transmission2Data}
            marker={{
              visible: true,
              dataLabel: { visible: true }
            }}
            tooltip={{ visible: true }}
          />
        </SmithchartSeriesCollectionDirective>
      </SmithchartComponent>
    </div>
  );
}

export default App;
```

### CSS Theme Import

**Important:** CSS theme imports are **NOT required** for Smith Chart to function. The component renders and works perfectly without any theme CSS.

Theme CSS is only needed if you want to apply Syncfusion's predefined visual styling. Available theme options are:
- `material.css` - Material Design theme
- `bootstrap.css` - Bootstrap theme
- `fabric.css` - Office Fabric theme
- `bootstrap5.css` - Bootstrap 5 theme
- `tailwind.css` - Tailwind CSS theme
- `fluent.css` - Fluent UI theme

**When CSS imports are optional:**
- Building custom styled components with your own CSS
- Using external CSS frameworks (Bootstrap, Tailwind)
- Keeping bundle size minimal
- The default browser styling is sufficient for your needs

Smith Chart renders with default browser styles without any CSS imports, making it lightweight and flexible for custom styling.

## Next Steps

Now that you have a basic Smith Chart running, you can explore:
- Customizing series appearance (colors, line width, opacity)
- Configuring horizontal and radial axes
- Advanced marker and data label customization
- Legend positioning and styling
- Chart dimensions and responsive sizing
- Print and export functionality
- Accessibility features

Each of these features is covered in detail in the respective reference files.
