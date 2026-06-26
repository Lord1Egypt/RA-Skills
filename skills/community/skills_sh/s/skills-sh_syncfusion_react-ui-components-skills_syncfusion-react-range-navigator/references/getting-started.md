# Getting Started with Range Navigator

This guide covers everything you need to know to install, configure, and create your first Range Navigator component in a React application.

## Table of contents
- [Dependencies](#dependencies)
- [Installation and Configuration](#installation-and-configuration)
  - [Option 1: Using Vite (Recommended)](#option-1-using-vite-recommended)
  - [Option 2: Using Create React App](#option-2-using-create-react-app)
- [Add Range Navigator to the Project](#add-range-navigator-to-the-project)
  - [Import and Add Component](#import-and-add-component)
  - [Update Main Entry File](#update-main-entry-file)
- [Basic Range Navigator Implementation](#basic-range-navigator-implementation)
- [Module Injection](#module-injection)
  - [Available Modules](#available-modules)
  - [How to Inject Modules](#how-to-inject-modules)
- [Populating Range Navigator with Data](#populating-range-navigator-with-data)
  - [Prepare Data](#prepare-data)
  - [Configure Series](#configure-series)
- [Value Type Configuration](#value-type-configuration)
- [Enable Tooltip](#enable-tooltip)
- [Add CSS Stylesheets](#add-css-stylesheets)
- [Complete Example](#complete-example)
- [License Registration](#license-registration)
- [Key Points to Remember](#key-points-to-remember)
- [Next Steps](#next-steps)
- [API Links](#api-links)

## Dependencies

The Range Navigator component requires the following Syncfusion packages:

```
|-- @syncfusion/ej2-react-charts
    |-- @syncfusion/ej2-base
    |-- @syncfusion/ej2-data
    |-- @syncfusion/ej2-pdf-export
    |-- @syncfusion/ej2-file-utils
    |-- @syncfusion/ej2-compression
    |-- @syncfusion/ej2-navigations
    |-- @syncfusion/ej2-calendars
    |-- @syncfusion/ej2-svg-base
```

## Installation and Configuration

### Option 1: Using Vite (Recommended)

Vite provides a faster development environment with smaller bundle sizes and optimized builds.

**Step 1: Create a new React application**

```bash
npm create vite@latest my-app
```

This command will prompt you to select a framework and variant.

**For TypeScript:**
```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm run dev
```

**For JavaScript:**
```bash
npm create vite@latest my-app -- --template react
cd my-app
npm run dev
```

**Step 2: Install Syncfusion Range Navigator package**

All Syncfusion Essential JS 2 packages are published on npmjs.com. Install the package using:

```bash
npm install @syncfusion/ej2-react-charts --save
```

The `--save` flag adds the Range Navigator package to the dependencies section in package.json.

### Option 2: Using Create React App

If you prefer Create React App, you can follow the traditional CRA setup process and install the same `@syncfusion/ej2-react-charts` package.

## Add Range Navigator to the Project

### Step 1: Import and Add Component

Add the Range Navigator component to `src/App.tsx` (or `src/App.jsx` for JavaScript):

**TypeScript Example:**
```tsx
import * as React from 'react';
import { RangeNavigatorComponent } from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";

function App() {
  return (<RangeNavigatorComponent></RangeNavigatorComponent>);
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

### Step 2: Update Main Entry File

Update `src/main.tsx` (or `src/main.jsx`) to render the App component using React 18's createRoot API:

```tsx
import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import './index.css';

const root = createRoot(document.getElementById('root')!);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

### Step 3: Run the Development Server

```bash
npm run dev
```

This compiles your code and serves the application locally in the browser.

## Basic Range Navigator Implementation

Here's a basic Range Navigator without any data:

```tsx
import * as React from 'react';
import { RangeNavigatorComponent } from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";

function App() {
  return (
    <RangeNavigatorComponent 
      id="rangeNavigator"
      valueType="Double"
    >
    </RangeNavigatorComponent>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## Module Injection

Range Navigator components are segregated into individual feature-wise modules. To use a particular feature, inject its feature service in the component.

### Available Modules

- **AreaSeries** - Use area series for data visualization
- **LineSeries** - Use line series for data visualization
- **StepLineSeries** - Use step line series for data visualization
- **DateTime** - Use DateTime axis for time-series data
- **Logarithmic** - Use logarithmic scale for magnitude data
- **RangeTooltip** - Display tooltips on slider interaction
- **PeriodSelector** - Add predefined time period buttons

### How to Inject Modules

Import the required modules from the chart package and inject them using the `Inject` component:

```tsx
// src/App.tsx
import * as React from 'react';
import {
  RangeNavigatorComponent,
  AreaSeries,
  DateTime,
  RangeTooltip,
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";

function App() {
  return (
    <RangeNavigatorComponent id="charts">
      <Inject services={[AreaSeries, DateTime, RangeTooltip ]} />
      <RangenavigatorSeriesCollectionDirective>
        <RangenavigatorSeriesDirective
          // placeholder until data is bound
          dataSource={[]}
          xName="x"
          yName="y"
          type="Area"
        />
      </RangenavigatorSeriesCollectionDirective>
    </RangeNavigatorComponent>
  );
}
export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## Populating Range Navigator with Data

### Step 1: Prepare Data

Create a data array with x and y values:

```tsx
const data = [
  { x: new Date(2018, 0, 1), y: 35 },
  { x: new Date(2018, 1, 1), y: 28 },
  { x: new Date(2018, 2, 1), y: 34 },
  { x: new Date(2018, 3, 1), y: 32 },
  { x: new Date(2018, 4, 1), y: 40 },
  { x: new Date(2018, 5, 1), y: 42 },
  { x: new Date(2018, 6, 1), y: 38 }
];
```

### Step 2: Configure Series

Add a series object to the Range Navigator using the `SeriesCollectionDirective`. Map the JSON fields to series properties:

- **dataSource**: JSON array with data
- **xName**: Field name for x-axis values
- **yName**: Field name for y-axis values
- **type**: Series type (Line, Area, StepLine)

```tsx
// src/App.tsx
import * as React from 'react';
import {
  RangeNavigatorComponent,
  AreaSeries,
  DateTime,
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";

function App() {
  const data = [
    { x: new Date(2018, 0, 1), y: 35 },
    { x: new Date(2018, 1, 1), y: 28 },
    { x: new Date(2018, 2, 1), y: 34 },
    { x: new Date(2018, 3, 1), y: 32 },
    { x: new Date(2018, 4, 1), y: 40 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="DateTime"
      labelFormat="MMM"
    >
      <Inject services={[AreaSeries, DateTime]} />
      <RangenavigatorSeriesCollectionDirective>
        <RangenavigatorSeriesDirective
          dataSource={data}
          xName="x"
          yName="y"
          type="Area"
        />
      </RangenavigatorSeriesCollectionDirective>
    </RangeNavigatorComponent>
  );
}
export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

### Value Type Configuration

Since the JSON contains DateTime data, set the `valueType` property to `'DateTime'`. Available value types:

- **Double** (default): Numeric values
- **DateTime**: Date/time values
- **Logarithmic**: Logarithmic scale

For category data, you would use numeric values with appropriate formatting.

## Enable Tooltip

Tooltips display the selected start and end values when users interact with the range sliders.

### Step 1: Inject RangeTooltip Module

```tsx
import { RangeTooltip } from '@syncfusion/ej2-react-charts';
<Inject services={[AreaSeries, DateTime, RangeTooltip ]} />
```

### Step 2: Enable Tooltip

Set the `enable` property to `true` in the `tooltip` object:

```tsx
// src/App.tsx
import * as React from 'react';
import {
  RangeNavigatorComponent,
  AreaSeries,
  DateTime,
  RangeTooltip,
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";

function App() {
  const data = [
    { x: new Date(2018, 0, 1), y: 35 },
    { x: new Date(2018, 1, 1), y: 28 },
    { x: new Date(2018, 2, 1), y: 34 },
    { x: new Date(2018, 3, 1), y: 32 },
    { x: new Date(2018, 4, 1), y: 40 },
    { x: new Date(2018, 5, 1), y: 42 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="DateTime"
      labelFormat="MMM"
      tooltip={{ enable: true }}
    >
      <Inject services={[AreaSeries, DateTime, RangeTooltip ]} />
      <RangenavigatorSeriesCollectionDirective>
        <RangenavigatorSeriesDirective
          dataSource={data}
          xName="x"
          yName="y"
          type="Area"
        />
      </RangenavigatorSeriesCollectionDirective>
    </RangeNavigatorComponent>
  );
}
export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## Theme Customization

**Available themes (18+ including dark & high contrast):**
- Material, MaterialDark, Material3, Material3Dark
- Fabric, FabricDark
- Bootstrap, BootstrapDark, Bootstrap4, Bootstrap5, Bootstrap5Dark, Bootstrap5.3, Bootstrap5.3Dark
- Tailwind, TailwindDark
- Fluent, FluentDark, Fluent2, Fluent2Dark, Fluent2HighContrast
- HighContrast, HighContrastLight

Switch via the `theme` prop:

```tsx
<RangeNavigatorComponent theme='Material3Dark'>
  {/* Range Navigator content */}
</RangeNavigatorComponent>
```

## Complete Example

Here's a complete working example with all the pieces together:

```tsx
// src/App.tsx
import * as React from 'react';
import {
  RangeNavigatorComponent,
  AreaSeries,
  DateTime,
  RangeTooltip,
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";

function App() {
  const data = [
    { x: new Date(2018, 0, 1), y: 35 },
    { x: new Date(2018, 1, 1), y: 28 },
    { x: new Date(2018, 2, 1), y: 34 },
    { x: new Date(2018, 3, 1), y: 32 },
    { x: new Date(2018, 4, 1), y: 40 },
    { x: new Date(2018, 5, 1), y: 42 },
    { x: new Date(2018, 6, 1), y: 38 },
    { x: new Date(2018, 7, 1), y: 45 },
    { x: new Date(2018, 8, 1), y: 43 },
    { x: new Date(2018, 9, 1), y: 46 },
    { x: new Date(2018, 10, 1), y: 48 },
    { x: new Date(2018, 11, 1), y: 50 }
  ];

  return (
    <div className="App">
      <RangeNavigatorComponent
        id="rangeNavigator"
        valueType="DateTime"
        labelFormat="MMM"
        value={[new Date(2018, 1, 1), new Date(2018, 6, 1)]}
        tooltip={{ enable: true }}
      >
        <Inject services={[AreaSeries, DateTime, RangeTooltip ]} />
        <RangenavigatorSeriesCollectionDirective>
          <RangenavigatorSeriesDirective
            dataSource={data}
            xName="x"
            yName="y"
            type="Area"
          />
        </RangenavigatorSeriesCollectionDirective>
      </RangeNavigatorComponent>
    </div>
  );
}
export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## License Registration

For production applications, register your Syncfusion license key:

```tsx
import { registerLicense } from '@syncfusion/ej2-base';

registerLicense('YOUR_LICENSE_KEY');
```

Place this at the top of your application before any Syncfusion component is rendered. You can obtain a license key from the [Syncfusion website](https://www.syncfusion.com/).

## Key Points to Remember

1. **Install Package**: `npm install @syncfusion/ej2-react-charts`
2. **Import CSS**: Add theme CSS file for styling
3. **Inject Modules**: Use `<Inject services={[...]} />` for required features
4. **Set Value Type**: Configure `valueType` based on your data (Double, DateTime, Logarithmic)
5. **Configure Series**: Map data fields using `dataSource`, `xName`, `yName`
6. **Enable Features**: Configure tooltip, period selector, etc. as needed
7. **Register License**: Use `registerLicense()` for production

## Next Steps

- Configure data binding with numeric, logarithmic, or DateTime data
- Customize series types (Line, Area, StepLine)
- Add period selector for predefined time ranges
- Customize appearance (colors, thumbs, borders)
- Enable tooltips with custom formatting
- Configure labels and grid/tick lines

## API Links

Full Range Navigator API: https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default

Complex items referenced in this guide (see API for details):
- [`valueType`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#valueType), [`value`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#value), [`minimum`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#minimum), [`maximum`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#maximum), [`interval`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#interval), [`intervalType`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#intervalType)
- [`series`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#series), [`dataSource`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#dataSource), [`xName`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#xName), [`yName`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#yName)
- Module injection: [`AreaSeries`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#areaSeriesModule), [`LineSeries`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#lineSeriesModule), [`StepLineSeries`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#stepLineSeriesModule), [`DateTime`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#dateTimeModule), [`Logarithmic`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#logarithmicModule), [`RangeTooltip`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#rangeTooltipModule), [`PeriodSelector`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#periodSelectorModule)

