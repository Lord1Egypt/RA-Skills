# Getting Started with React 3D Circular Chart

This guide walks you through installing, configuring, and creating your first Syncfusion React 3D Circular Chart component from scratch.

## Table of contents

- [Overview](getting-started.md#overview)
- [Dependencies](getting-started.md#dependencies)
- [Installation and Configuration](getting-started.md#installation-and-configuration)
  - [Step 1: Create a React Application](getting-started.md#step-1-create-a-react-application)
  - [Step 2: Install Syncfusion 3D Circular Chart Package](getting-started.md#step-2-install-syncfusion-3d-circular-chart-package)
  - [Step 3: Import CSS Themes](getting-started.md#step-3-import-css-themes)
- [Add 3D Circular Chart to Your Project](getting-started.md#add-3d-circular-chart-to-your-project)
  - [Minimal Example](getting-started.md#minimal-example)
  - [Creating Your First Pie Chart with Data](getting-started.md#creating-your-first-pie-chart-with-data)
- [Customizing the Basic Chart](getting-started.md#customizing-the-basic-chart)
- [Common Patterns](getting-started.md#common-patterns)
- [Troubleshooting](getting-started.md#troubleshooting)
- [Next Steps](getting-started.md#next-steps)
- [Summary](getting-started.md#summary)

## Overview

The 3D Circular Chart component allows you to create visually appealing pie and donut charts with 3D depth. This guide covers everything from installation to rendering your first chart with data.

## Dependencies

The 3D Circular Chart component requires the following packages:

```
|-- @syncfusion/ej2-react-charts
    |-- @syncfusion/ej2-data
    |-- @syncfusion/ej2-react-base
    |-- @syncfusion/ej2-pdf-export
    |-- @syncfusion/ej2-file-utils
    |-- @syncfusion/ej2-compression
    |-- @syncfusion/ej2-svg-base
```

**Good news:** Once you install `@syncfusion/ej2-react-charts`, all other required dependencies are installed automatically.

## Installation and Configuration

### Step 1: Create a React Application

Syncfusion recommends using **Vite** for faster development and optimized builds.

#### Option A: Using Vite (Recommended)

**For TypeScript:**
```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install
```

**For JavaScript:**
```bash
npm create vite@latest my-app -- --template react
cd my-app
npm install
```

**Interactive Setup:**
If you prefer an interactive setup, simply run:
```bash
npm create vite@latest my-app
```

This will prompt you to select:
1. Framework: Choose **React**
2. Variant: Choose **TypeScript** or **JavaScript**

Then navigate to the project and install dependencies:
```bash
cd my-app
npm install
```

#### Option B: Using Create React App

If you prefer Create React App, you can still use it:

```bash
npx create-react-app my-app
cd my-app
```

### Step 2: Install Syncfusion 3D Circular Chart Package

Install the Syncfusion React Charts package from npm:

```bash
npm install @syncfusion/ej2-react-charts --save
```

The `--save` flag adds the package to the **dependencies** section of your `package.json` file.

## Add 3D Circular Chart to Your Project

### Minimal Example

Replace the content of `src/App.tsx` (or `src/App.jsx`) with:

**TypeScript:**
```tsx
import { CircularChart3DComponent } from '@syncfusion/ej2-react-charts';
import * as React from 'react';

function App() {
  return <CircularChart3DComponent />;
}

export default App;
```

**JavaScript:**
```jsx
import { CircularChart3DComponent } from '@syncfusion/ej2-react-charts';
import React from 'react';

function App() {
  return <CircularChart3DComponent />;
}

export default App;
```

### Run the Application

Start the development server:

```bash
npm run dev
```

This compiles your code and opens the application in your browser. You should see an empty 3D Circular Chart component.

## Creating Your First Pie Chart with Data

Now let's add actual data to create a meaningful pie chart.

### Understanding Data Binding

The 3D Circular Chart uses three key properties for data binding:
- **`dataSource`**: Array of data objects
- **`xName`**: Property name for labels (categories)
- **`yName`**: Property name for values

### Complete Working Example

```tsx
import * as ReactDOM from 'react-dom';
import {
    CircularChart3DComponent,
    CircularChart3DSeriesCollectionDirective,
    CircularChart3DSeriesDirective,
    PieSeries3D,
    Inject
  } from '@syncfusion/ej2-react-charts';
  import * as React from 'react';
  
  function App() {
    // Sample data
    const data = [
      { product: 'Laptops', sales: 35 },
      { product: 'Phones', sales: 28 },
      { product: 'Tablets', sales: 20 },
      { product: 'Accessories', sales: 17 }
    ];
  
    return (
      <CircularChart3DComponent
        id="chart"
        title="Product Sales Distribution"
        width="600px"
        height="450px"
      >
        {/* Inject required module */}
        <Inject services={[PieSeries3D]} />
        
        {/* Define series */}
        <CircularChart3DSeriesCollectionDirective>
          <CircularChart3DSeriesDirective
            dataSource={data}
            xName="product"  // Maps to 'product' property
            yName="sales"    // Maps to 'sales' property
          />
        </CircularChart3DSeriesCollectionDirective>
      </CircularChart3DComponent>
    );
  }
  
export default App;
const root = ReactDOM.createRoot(document.getElementById('charts'));
root.render(<App />);
```

### What's Happening?

1. **Import Components**: We import the chart component, series directives, and `PieSeries3D` module
2. **Create Data**: Define an array of objects with labels and values
3. **Inject Module**: Use `<Inject services={[PieSeries3D]} />` to enable pie chart functionality
4. **Map Data**: Use `xName` and `yName` to map data properties to chart axes
5. **Render**: The chart automatically renders as a pie chart by default

### Key Points

- **Default Behavior**: By default, assigning data creates a pie chart (not a donut)
- **Module Injection**: Always inject `PieSeries3D` for pie/donut charts
- **Data Format**: Data can be any array of objects with consistent properties
- **Field Mapping**: `xName` and `yName` must match your data object property names

## Customizing the Basic Chart

### Setting Chart Dimensions

```tsx
<CircularChart3DComponent
  width="800px"
  height="600px"
>
  {/* ... */}
</CircularChart3DComponent>
```

### Setting Chart Radius

By default, the chart uses 80% of the available space. You can customize it:

```tsx
<CircularChart3DSeriesDirective
  dataSource={data}
  xName="product"
  yName="sales"
  radius="70%"  // Custom radius
/>
```

### Adding a Title

```tsx
<CircularChart3DComponent
  title="Sales Analysis 2024"
  subTitle="Quarterly Report"
>
  {/* ... */}
</CircularChart3DComponent>
```

## Common Patterns

### Using External Data (API/JSON)

```tsx
function App() {
  const [chartData, setChartData] = React.useState([]);

  React.useEffect(() => {
    // Fetch data from API
    fetch('/api/sales-data')
      .then(response => response.json())
      .then(data => setChartData(data));
  }, []);

  return (
    <CircularChart3DComponent>
      <Inject services={[PieSeries3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={chartData}
          xName="category"
          yName="value"
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

### Multiple Data Fields

If your data has multiple value fields:

```tsx
const data = [
  { category: 'Q1', revenue: 45000, expenses: 32000 },
  { category: 'Q2', revenue: 52000, expenses: 35000 }
];

// Show revenue
<CircularChart3DSeriesDirective
  dataSource={data}
  xName="category"
  yName="revenue"  // Choose which field to visualize
/>
```

## Troubleshooting

### Chart Not Rendering

**Problem**: Blank screen or console errors

**Solutions**:
1. Verify you installed the package: `npm install @syncfusion/ej2-react-charts`
2. Check CSS import is present in your component
3. Ensure `PieSeries3D` is injected via `<Inject services={[PieSeries3D]} />`
4. Verify `xName` and `yName` match your data object properties exactly

### Module Injection Error

**Problem**: Error like "Module not injected"

**Solution**: Always include the Inject component:
```tsx
<Inject services={[PieSeries3D]} />
```

### Data Not Displaying

**Problem**: Chart renders but shows no data

**Solutions**:
1. Check `xName` and `yName` match your data properties (case-sensitive)
2. Verify `dataSource` is a valid array
3. Ensure data values are numbers, not strings
4. Check browser console for warnings

### TypeScript Errors

**Problem**: Type errors with imports

**Solution**: Ensure you're using correct import names:
```tsx
// Correct
import { CircularChart3DComponent } from '@syncfusion/ej2-react-charts';

// Not: CircularChartComponent or Chart3DComponent
```

## Next Steps

Now that you have a basic 3D Circular Chart running, explore:

- **Pie and Donut Charts**: Create donut charts with inner radius
- **Data Labels**: Add labels to display values on chart slices
- **Legends**: Show legend for better data understanding
- **Tooltips**: Enable interactive tooltips on hover
- **Export**: Export charts as images or PDFs

## Summary

You've learned how to:
- ✅ Install Syncfusion React Charts package
- ✅ Create a React application with Vite or Create React App
- ✅ Import and apply CSS themes
- ✅ Create a basic 3D Circular Chart
- ✅ Bind data using dataSource, xName, and yName
- ✅ Inject required modules (PieSeries3D)
- ✅ Customize chart with title and dimensions

Your 3D Circular Chart is now ready for advanced customization!
