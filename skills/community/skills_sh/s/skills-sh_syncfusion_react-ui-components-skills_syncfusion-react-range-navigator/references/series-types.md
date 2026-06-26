# Series Types

The Range Navigator supports three types of series for rendering data: Line, Area, and StepLine. Each series type provides a different visual representation of your data.

## Table of contents
- [Line Series](#line-series)
  - [Module Injection](#module-injection)
  - [Basic Line Series Implementation](#basic-line-series-implementation)
  - [Line Series with DateTime Data](#line-series-with-datetime-data)
- [Area Series](#area-series)
  - [Module Injection](#module-injection-1)
  - [Basic Area Series Implementation](#basic-area-series-implementation)
  - [Area Series with DateTime Data](#area-series-with-datetime-data)
- [StepLine Series](#stepline-series)
  - [Module Injection](#module-injection-2)
  - [Basic StepLine Series Implementation](#basic-stepline-series-implementation)
  - [StepLine Series with DateTime Data](#stepline-series-with-datetime-data)
- [Multiple Series](#multiple-series)
- [Series Configuration Properties](#series-configuration-properties)
- [Complete Example with All Series Types](#complete-example-with-all-series-types)
- [Series Type Selection Guide](#series-type-selection-guide)
- [Key Points](#key-points)
- [API Links](#api-links)

## Line Series

Line series is the default series type and renders data as a continuous line connecting data points.

### Module Injection

```tsx
import { LineSeries } from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';
<Inject services={[LineSeries]} />
```

### Basic Line Series Implementation

```tsx
import { 
  RangeNavigatorComponent, 
  LineSeries, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective 
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const data = [
    { x: 0, y: 10 },
    { x: 10, y: 30 },
    { x: 20, y: 25 },
    { x: 30, y: 45 },
    { x: 40, y: 35 },
    { x: 50, y: 55 },
    { x: 60, y: 50 }
  ];

  return (
    <RangeNavigatorComponent id="rangeNavigator">
      <Inject services={[LineSeries]} />
      <RangenavigatorSeriesCollectionDirective>
        <RangenavigatorSeriesDirective
          dataSource={data}
          xName="x"
          yName="y"
          type="Line"
        />
      </RangenavigatorSeriesCollectionDirective>
    </RangeNavigatorComponent>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

### Line Series with DateTime Data

```tsx
import { 
  RangeNavigatorComponent, 
  LineSeries, 
  DateTime, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective 
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const stockData = [
    { date: new Date(2023, 0, 1), price: 100 },
    { date: new Date(2023, 1, 1), price: 110 },
    { date: new Date(2023, 2, 1), price: 105 },
    { date: new Date(2023, 3, 1), price: 115 },
    { date: new Date(2023, 4, 1), price: 120 },
    { date: new Date(2023, 5, 1), price: 125 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="DateTime"
      labelFormat="MMM"
    >
      <Inject services={[LineSeries, DateTime]} />
      <RangenavigatorSeriesCollectionDirective>
        <RangenavigatorSeriesDirective
          dataSource={stockData}
          xName="date"
          yName="price"
          type="Line"
        />
      </RangenavigatorSeriesCollectionDirective>
    </RangeNavigatorComponent>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

**When to Use Line Series:**
- Stock price trends
- Temperature changes over time
- Simple numeric data visualization
- When you need clear data point connections
- Minimal visual emphasis on data ranges

## Area Series

Area series renders data as a filled area under the line, providing visual emphasis on the data range and magnitude.

### Module Injection

```tsx
import { AreaSeries } from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';
<Inject services={[AreaSeries]} />
```

### Basic Area Series Implementation

```tsx
import { 
  RangeNavigatorComponent, 
  AreaSeries, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective 
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const data = [
    { x: 0, y: 10 },
    { x: 10, y: 30 },
    { x: 20, y: 25 },
    { x: 30, y: 45 },
    { x: 40, y: 35 },
    { x: 50, y: 55 },
    { x: 60, y: 50 }
  ];

  return (
    <RangeNavigatorComponent id="rangeNavigator">
      <Inject services={[AreaSeries]} />
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

### Area Series with DateTime Data

```tsx
import { 
  RangeNavigatorComponent, 
  AreaSeries, 
  DateTime, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective 
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const salesData = [
    { month: new Date(2023, 0, 1), sales: 15000 },
    { month: new Date(2023, 1, 1), sales: 18000 },
    { month: new Date(2023, 2, 1), sales: 22000 },
    { month: new Date(2023, 3, 1), sales: 25000 },
    { month: new Date(2023, 4, 1), sales: 28000 },
    { month: new Date(2023, 5, 1), sales: 32000 }
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
          dataSource={salesData}
          xName="month"
          yName="sales"
          type="Area"
        />
      </RangenavigatorSeriesCollectionDirective>
    </RangeNavigatorComponent>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

**When to Use Area Series:**
- Sales volume over time
- Resource utilization charts
- When emphasizing data magnitude
- Highlighting cumulative values
- Financial data visualization (most common for Range Navigator)

## StepLine Series

StepLine series renders data with horizontal and vertical steps, creating a staircase pattern. This is useful for data that changes at specific intervals.

### Module Injection

```tsx
import { StepLineSeries } from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';
<Inject services={[StepLineSeries]} />
```

### Basic StepLine Series Implementation

```tsx
import { 
  RangeNavigatorComponent, 
  StepLineSeries, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective 
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const data = [
    { x: 0, y: 10 },
    { x: 10, y: 30 },
    { x: 20, y: 25 },
    { x: 30, y: 45 },
    { x: 40, y: 35 },
    { x: 50, y: 55 },
    { x: 60, y: 50 }
  ];

  return (
    <RangeNavigatorComponent id="rangeNavigator">
      <Inject services={[StepLineSeries]} />
      <RangenavigatorSeriesCollectionDirective>
        <RangenavigatorSeriesDirective
          dataSource={data}
          xName="x"
          yName="y"
          type="StepLine"
        />
      </RangenavigatorSeriesCollectionDirective>
    </RangeNavigatorComponent>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

### StepLine Series with DateTime Data

```tsx
import { 
  RangeNavigatorComponent, 
  StepLineSeries, 
  DateTime, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective 
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const priceData = [
    { date: new Date(2023, 0, 1), price: 100 },
    { date: new Date(2023, 1, 1), price: 100 },
    { date: new Date(2023, 2, 1), price: 110 },
    { date: new Date(2023, 3, 1), price: 110 },
    { date: new Date(2023, 4, 1), price: 105 },
    { date: new Date(2023, 5, 1), price: 105 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="DateTime"
      labelFormat="MMM"
    >
      <Inject services={[StepLineSeries, DateTime]} />
      <RangenavigatorSeriesCollectionDirective>
        <RangenavigatorSeriesDirective
          dataSource={priceData}
          xName="date"
          yName="price"
          type="StepLine"
        />
      </RangenavigatorSeriesCollectionDirective>
    </RangeNavigatorComponent>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

**When to Use StepLine Series:**
- Price changes that occur at specific intervals
- Binary or discrete state changes
- Fixed pricing tiers
- Inventory levels that change at specific times
- Digital signal representations

## Multiple Series

You can display multiple series in the same Range Navigator for comparing different datasets.

### Multiple Series Example

```tsx
import { 
  RangeNavigatorComponent, 
  AreaSeries, 
  DateTime, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective 
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const series1Data = [
    { x: new Date(2023, 0, 1), y: 100 },
    { x: new Date(2023, 1, 1), y: 110 },
    { x: new Date(2023, 2, 1), y: 105 },
    { x: new Date(2023, 3, 1), y: 115 }
  ];

  const series2Data = [
    { x: new Date(2023, 0, 1), y: 90 },
    { x: new Date(2023, 1, 1), y: 95 },
    { x: new Date(2023, 2, 1), y: 100 },
    { x: new Date(2023, 3, 1), y: 105 }
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
          dataSource={series1Data}
          xName="x"
          yName="y"
          type="Area"
        />
        <RangenavigatorSeriesDirective
          dataSource={series2Data}
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

## Series Configuration Properties

### Common Series Properties

All series types support these properties:

- **dataSource**: Array of data objects
- **xName**: Field name for x-axis values in the data
- **yName**: Field name for y-axis values in the data
- **type**: Series rendering type ('Line' | 'Area' | 'StepLine')
- **fill**: Fill color for the series
- **width**: Line width (for Line and StepLine)
- **opacity**: Series opacity (0 to 1)

### Series Configuration Example

```tsx
<RangenavigatorSeriesDirective
  dataSource={data}
  xName="x"
  yName="y"
  type="Area"
  fill="#4472C4"
  opacity={0.6}
/>
```

## Complete Example with All Series Types

```tsx
import { 
  RangeNavigatorComponent, 
  LineSeries, 
  AreaSeries, 
  StepLineSeries, 
  DateTime, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective 
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';
import { useState } from 'react';

function App() {
  const [seriesType, setSeriesType] = useState('Area');

  const data = [
    { date: new Date(2023, 0, 1), value: 100 },
    { date: new Date(2023, 1, 1), value: 110 },
    { date: new Date(2023, 2, 1), value: 105 },
    { date: new Date(2023, 3, 1), value: 115 },
    { date: new Date(2023, 4, 1), value: 120 },
    { date: new Date(2023, 5, 1), value: 125 }
  ];

  return (
    <div>
      <div>
        <button onClick={() => setSeriesType('Line')}>Line</button>
        <button onClick={() => setSeriesType('Area')}>Area</button>
        <button onClick={() => setSeriesType('StepLine')}>StepLine</button>
      </div>
      
      <RangeNavigatorComponent
        id="rangeNavigator"
        valueType="DateTime"
        labelFormat="MMM"
      >
        <Inject services={[LineSeries, AreaSeries, StepLineSeries, DateTime]} />
        <RangenavigatorSeriesCollectionDirective>
          <RangenavigatorSeriesDirective
            dataSource={data}
            xName="date"
            yName="value"
            type={seriesType}
          />
        </RangenavigatorSeriesCollectionDirective>
      </RangeNavigatorComponent>
    </div>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
ReactDOM.render(<App />, document.getElementById("charts"));
```

## Series Type Selection Guide

| Series Type | Visual Style | Best For | Module |
|------------|--------------|----------|--------|
| Line | Connected line | Simple trends, stock prices | LineSeries |
| Area | Filled area | Emphasizing magnitude, volume | AreaSeries |
| StepLine | Staircase pattern | Discrete changes, price tiers | StepLineSeries |

## Key Points

1. **Module Injection**: Always inject the required series module (LineSeries, AreaSeries, or StepLineSeries)
2. **Default Type**: Line is the default if no type is specified
3. **DateTime Support**: All series types work with DateTime axes
4. **Multiple Series**: You can combine different series types in one Range Navigator
5. **Performance**: Line series is typically fastest; Area series adds fill rendering overhead

## API Links

Full Range Navigator API: https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default

Series-related complex API references:
- [`series`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#series) (RangeNavigatorSeriesModel[]), `RangenavigatorSeriesDirective` properties: [`dataSource`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#dataSource), [`xName`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#xName), [`yName`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#yName), [`type`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#series), [`fill`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#series), [`opacity`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#series), [`width`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#series)
- Series modules: [`LineSeries`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#lineSeriesModule), [`AreaSeries`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#areaSeriesModule), [`StepLineSeries`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#stepLineSeriesModule)

