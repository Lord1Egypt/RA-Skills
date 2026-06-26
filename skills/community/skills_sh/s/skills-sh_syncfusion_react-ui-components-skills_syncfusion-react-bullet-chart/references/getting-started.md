# Getting Started with React Bullet Chart

This guide covers everything you need to install, configure, and create your first Syncfusion React Bullet Chart component.

## Table of contents

- [Dependencies](#dependencies)
- [Installation and Configuration](#installation-and-configuration)
- [Add Bullet Chart to Your Project](#add-bullet-chart-to-your-project)
- [Module Injection](#module-injection)
- [Bullet Chart with Data](#bullet-chart-with-data)
- [Adding a Title](#adding-a-title)
- [Adding Ranges](#adding-ranges)
- [Enabling Tooltips](#enabling-tooltips)
- [Complete Working Example](#complete-working-example)
- [Common Issues and Solutions](#common-issues-and-solutions)
- [Next Steps](#next-steps)

## Dependencies

The Bullet Chart component requires the following packages:

```
|-- @syncfusion/ej2-react-charts
    |-- @syncfusion/ej2-base
    |-- @syncfusion/ej2-data
    |-- @syncfusion/ej2-charts
    |-- @syncfusion/ej2-react-base
    |-- @syncfusion/ej2-pdf-export
    |-- @syncfusion/ej2-file-utils
    |-- @syncfusion/ej2-compression
    |-- @syncfusion/ej2-svg-base
```

These dependencies are automatically installed when you install the main package.

## Installation and Configuration

### Using Vite (Recommended)

Vite provides a faster development environment, smaller bundle sizes, and optimized builds compared to traditional tools.

**Create a new React application:**

```bash
npm create vite@latest my-app
```

This command will prompt you for project settings. Select React as the framework.

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

### Using Create React App (Alternative)

If you prefer create-react-app, you can use it as an alternative setup method. Refer to the official Syncfusion documentation for create-react-app specific instructions.

### Install Syncfusion Bullet Chart Package

All Syncfusion Essential JS 2 packages are published in the npmjs.com public registry. Install the Bullet Chart package:

```bash
npm install @syncfusion/ej2-react-charts --save
```

The `--save` flag includes the Bullet Chart package in the dependencies section of package.json.

## Add Bullet Chart to Your Project

### Basic Component Setup

Add the Bullet Chart component to `src/App.tsx` or `src/App.jsx`:

**TypeScript:**
```tsx
import { BulletChartComponent } from "@syncfusion/ej2-react-charts";
import * as React from "react";
import * as ReactDOM from "react-dom";

function App() {
    return <BulletChartComponent />;
}
export default App;

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
```

**JavaScript:**
```jsx
import { BulletChartComponent } from "@syncfusion/ej2-react-charts";
import * as React from "react";
import * as ReactDOM from "react-dom";

function App() {
    return <BulletChartComponent />;
}
export default App;

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
```

### Run the Application

Start the development server:

```bash
npm run dev
```

This compiles your code and serves the application locally, opening it in the browser.

## Module Injection

Bullet Chart features are segregated into individual feature modules. To use a specific feature, you must inject its module into the component.

### BulletTooltip Module

To enable tooltip functionality, inject the `BulletTooltip` module:

**TypeScript:**
```tsx
import * as React from 'react';
import { createRoot } from 'react-dom/client';
import { BulletChartComponent, BulletTooltip, Inject } from "@syncfusion/ej2-react-charts";

function App() {
    return (
      <BulletChartComponent id="bulletChart">
        <Inject services={[BulletTooltip]} />
      </BulletChartComponent>
    );
}
export default App;
createRoot(document.getElementById('charts')).render(<App />);
```

**JavaScript:**
```jsx
import * as React from 'react';
import { createRoot } from 'react-dom/client';
import { BulletChartComponent, BulletTooltip, Inject } from "@syncfusion/ej2-react-charts";

function App() {
    return (
      <BulletChartComponent id="bulletChart">
        <Inject services={[BulletTooltip]} />
      </BulletChartComponent>
    );
}
export default App;
createRoot(document.getElementById('charts')).render(<App />);
```

## Bullet Chart with Data

### Prepare Your Data

Define your data structure with `value` and `target` properties:

**TypeScript:**
```tsx
interface DataPoint {
    value: number;
    target: number;
}

const data: DataPoint[] = [
    { value: 100, target: 80 },
    { value: 200, target: 180 },
    { value: 300, target: 280 },
    { value: 400, target: 380 },
    { value: 500, target: 480 }
];
```

**JavaScript:**
```jsx
const data = [
    { value: 100, target: 80 },
    { value: 200, target: 180 },
    { value: 300, target: 280 },
    { value: 400, target: 380 },
    { value: 500, target: 480 }
];
```

### Bind Data to Component

Map the data to the Bullet Chart using `dataSource`, `valueField`, and `targetField`:

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    minimum={0}
    maximum={600}
    interval={100}
/>
```

**Key Properties:**
- `dataSource`: The data array
- `valueField`: Property name for actual values (e.g., "value")
- `targetField`: Property name for target values (e.g., "target")
- `minimum`: Minimum value of the scale
- `maximum`: Maximum value of the scale
- `interval`: Interval between axis labels

## Adding a Title

Use the `title` property to provide information about the data:

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    title="Sales Performance"
    minimum={0}
    maximum={600}
    interval={100}
/>
```

## Adding Ranges

Ranges provide visual context by dividing the chart into qualitative bands (e.g., poor, satisfactory, good).

### Import Range Directives

```tsx
import { 
    BulletChartComponent, 
    BulletRangeCollectionDirective, 
    BulletRangeDirective 
} from "@syncfusion/ej2-react-charts";
```

### Configure Ranges

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    title="Sales Performance"
    minimum={0}
    maximum={600}
    interval={100}
>
    <BulletRangeCollectionDirective>
        <BulletRangeDirective end={200} color="red" />
        <BulletRangeDirective end={400} color="yellow" />
        <BulletRangeDirective end={600} color="green" />
    </BulletRangeCollectionDirective>
</BulletChartComponent>
```

Each `BulletRangeDirective` defines:
- `end`: The ending point of the range
- `color`: The color for that range (poor=red, satisfactory=yellow, good=green)

## Enabling Tooltips

Tooltips display important summary information when hovering over bars.

### Enable Tooltip

Set the `enable` property to `true` in the `tooltip` object and inject the `BulletTooltip` module:

```tsx
import { 
    BulletChartComponent, 
    BulletRangeCollectionDirective, 
    BulletRangeDirective,
    BulletTooltip,
    Inject
} from "@syncfusion/ej2-react-charts";

function App() {
    const data = [
        { value: 270, target: 250 }
    ];

    return (
        <BulletChartComponent
            id="bulletChart"
            dataSource={data}
            valueField="value"
            targetField="target"
            title="Revenue"
            minimum={0}
            maximum={300}
            interval={50}
            tooltip={{ enable: true }}
        >
            <BulletRangeCollectionDirective>
                <BulletRangeDirective end={150} color="red" />
                <BulletRangeDirective end={250} color="yellow" />
                <BulletRangeDirective end={300} color="green" />
            </BulletRangeCollectionDirective>
            <Inject services={[BulletTooltip]} />
        </BulletChartComponent>
    );
}
```

## Complete Working Example

Here's a complete example combining all features:

```tsx
import { 
    BulletChartComponent, 
    BulletRangeCollectionDirective, 
    BulletRangeDirective,
    BulletTooltip,
    Inject
} from "@syncfusion/ej2-react-charts";
import * as React from "react";

function App() {
    const data = [
        { value: 270, target: 250 }
    ];

    return (
        <div style={{ padding: '20px' }}>
            <BulletChartComponent
                id="bulletChart"
                dataSource={data}
                valueField="value"
                targetField="target"
                title="Revenue (in thousands)"
                subtitle="Q1 2024"
                minimum={0}
                maximum={300}
                interval={50}
                tooltip={{ enable: true }}
                width="80%"
                height="100px"
            >
                <BulletRangeCollectionDirective>
                    <BulletRangeDirective end={150} color="#CC0000" />
                    <BulletRangeDirective end={250} color="#FFC107" />
                    <BulletRangeDirective end={300} color="#4CAF50" />
                </BulletRangeCollectionDirective>
                <Inject services={[BulletTooltip]} />
            </BulletChartComponent>
        </div>
    );
}

export default App;
```

## Common Issues and Solutions

**Issue: Chart not rendering**
- Verify that @syncfusion/ej2-react-charts is installed
- Check that you've imported BulletChartComponent correctly
- Ensure the component has a unique `id` prop

**Issue: Data not displaying**
- Verify `dataSource` contains valid data
- Check that `valueField` and `targetField` match your data properties
- Ensure `minimum` and `maximum` encompass your data range

**Issue: Tooltips not working**
- Confirm you've imported and injected the `BulletTooltip` module
- Set `tooltip.enable` to `true`
- Check that the tooltip object is properly configured

**Issue: Ranges not visible**
- Import `BulletRangeCollectionDirective` and `BulletRangeDirective`
- Set `end` values in ascending order
- Verify `end` values are within `minimum` and `maximum` bounds

## Next Steps

Now that you have a basic Bullet Chart running, explore:
- Customizing value bar appearance (types, colors, borders)
- Configuring comparative bar (target) types and styles
- Adding data labels to show exact values
- Customizing axis labels, tick marks, and formatting
- Implementing animations and themes
- Ensuring accessibility compliance
