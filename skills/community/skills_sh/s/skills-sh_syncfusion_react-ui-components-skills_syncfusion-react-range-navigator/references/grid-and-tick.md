# Grid Lines and Tick Lines

Grid lines and tick lines provide visual reference points on the Range Navigator axis. Grid lines help users identify axis divisions, while tick lines mark the axis labels. Both can be customized extensively.

## Table of contents
- [Grid Line Customization](#grid-line-customization)
  - [Grid Line Properties](#grid-line-properties)
  - [Basic Grid Line Customization](#basic-grid-line-customization)
  - [Grid Line Styles](#grid-line-styles)
    - [Solid Grid Lines](#solid-grid-lines)
    - [Dashed Grid Lines](#dashed-grid-lines)
    - [Dotted Grid Lines](#dotted-grid-lines)
    - [Long Dash Grid Lines](#long-dash-grid-lines)
    - [Thick Grid Lines](#thick-grid-lines)
    - [No Grid Lines](#no-grid-lines)
- [Tick Line Customization](#tick-line-customization)
  - [Tick Line Properties](#tick-line-properties)
- [Combining Grid and Tick Lines](#combining-grid-and-tick-lines)
- [Complete Example with Both Customizations](#complete-example-with-both-customizations)
- [Numeric Axis Grid and Tick Lines](#numeric-axis-grid-and-tick-lines)
- [Themed Grid and Tick Lines](#themed-grid-and-tick-lines)
- [Interactive Example with Style Switching](#interactive-example-with-style-switching)
- [Configuration Summary](#configuration-summary)
- [API Links](#api-links)
- [Best Practices](#best-practices)

## Grid Line Customization

Gridlines are horizontal or vertical lines that indicate axis divisions, helping users interpret data values more accurately.

### Grid Line Properties

Configure gridlines using the `majorGridLines` property:

- **width**: Line thickness in pixels
- **color**: Line color
- **dashArray**: Dash pattern (e.g., '5,3' for dashed line)

### Basic Grid Line Customization

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
  const data = [
    { date: new Date(2023, 0, 1), value: 100 },
    { date: new Date(2023, 1, 1), value: 110 },
    { date: new Date(2023, 2, 1), value: 105 },
    { date: new Date(2023, 3, 1), value: 115 },
    { date: new Date(2023, 4, 1), value: 120 },
    { date: new Date(2023, 5, 1), value: 125 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="DateTime"
      labelFormat="MMM"
      majorGridLines={{
        width: 1,
        color: '#E0E0E0',
        dashArray: '0'
      }}
    >
      <Inject services={[AreaSeries, DateTime]} />
      <RangenavigatorSeriesCollectionDirective>
        <RangenavigatorSeriesDirective
          dataSource={data}
          xName="date"
          yName="value"
          type="Area"
        />
      </RangenavigatorSeriesCollectionDirective>
    </RangeNavigatorComponent>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

### Grid Line Styles

#### Solid Grid Lines

```tsx
majorGridLines={{
  width: 1,
  color: '#CCCCCC',
  dashArray: '0'
}}
```

#### Dashed Grid Lines

```tsx
majorGridLines={{
  width: 1,
  color: '#CCCCCC',
  dashArray: '5,5'  // 5px dash, 5px gap
}}
```

#### Dotted Grid Lines

```tsx
majorGridLines={{
  width: 1,
  color: '#CCCCCC',
  dashArray: '2,2'  // 2px dash, 2px gap
}}
```

#### Long Dash Grid Lines

```tsx
majorGridLines={{
  width: 1,
  color: '#CCCCCC',
  dashArray: '10,5'  // 10px dash, 5px gap
}}
```

#### Thick Grid Lines

```tsx
majorGridLines={{
  width: 2,
  color: '#999999',
  dashArray: '0'
}}
```

#### No Grid Lines

```tsx
majorGridLines={{
  width: 0
}}
```

### DashArray Pattern Examples

The `dashArray` property accepts a string of numbers representing dash and gap lengths:

```tsx
// Pattern format: 'dash,gap,dash,gap,...'

'5,5'      // Simple dashed: 5px dash, 5px gap
'10,5'     // Long dash: 10px dash, 5px gap
'2,2'      // Dotted: 2px dash, 2px gap
'5,5,1,5'  // Dash-dot: 5px dash, 5px gap, 1px dot, 5px gap
'10,5,5,5' // Dash-dash: 10px dash, 5px gap, 5px dash, 5px gap
'0'        // Solid line (no dashes)
```

### Complete Grid Line Example

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
      intervalType="Months"
      majorGridLines={{
        width: 1.5,
        color: '#BDBDBD',
        dashArray: '5,3'
      }}
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

## Tick Line Customization

Ticklines are small lines drawn on the axis representing axis labels. By default, tick lines are drawn outside the axis.

### Tick Line Properties

Configure tick lines using the `majorTickLines` property:

- **width**: Line thickness in pixels
- **color**: Line color
- **dashArray**: Dash pattern

### Basic Tick Line Customization

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
  const data = [
    { date: new Date(2023, 0, 1), value: 100 },
    { date: new Date(2023, 1, 1), value: 110 },
    { date: new Date(2023, 2, 1), value: 105 },
    { date: new Date(2023, 3, 1), value: 115 },
    { date: new Date(2023, 4, 1), value: 120 },
    { date: new Date(2023, 5, 1), value: 125 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="DateTime"
      labelFormat="MMM"
      majorTickLines={{
        width: 2,
        color: '#2196F3',
        dashArray: '0'
      }}
    >
      <Inject services={[AreaSeries, DateTime]} />
      <RangenavigatorSeriesCollectionDirective>
        <RangenavigatorSeriesDirective
          dataSource={data}
          xName="date"
          yName="value"
          type="Area"
        />
      </RangenavigatorSeriesCollectionDirective>
    </RangeNavigatorComponent>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

### Tick Line Styles

#### Standard Tick Lines

```tsx
majorTickLines={{
  width: 1,
  color: '#666666',
  dashArray: '0'
}}
```

#### Bold Tick Lines

```tsx
majorTickLines={{
  width: 3,
  color: '#333333',
  dashArray: '0'
}}
```

#### Colored Tick Lines

```tsx
majorTickLines={{
  width: 2,
  color: '#2196F3',
  dashArray: '0'
}}
```

#### Dashed Tick Lines

```tsx
majorTickLines={{
  width: 1,
  color: '#666666',
  dashArray: '3,3'
}}
```

#### No Tick Lines

```tsx
majorTickLines={{
  width: 0
}}
```

## Combining Grid and Tick Lines

Coordinate grid and tick line styles for a cohesive appearance:

### Subtle Grid with Prominent Ticks

```tsx
<RangeNavigatorComponent
  majorGridLines={{
    width: 1,
    color: '#E0E0E0',
    dashArray: '2,2'
  }}
  majorTickLines={{
    width: 2,
    color: '#333333',
    dashArray: '0'
  }}
>
  {/* Series configuration */}
</RangeNavigatorComponent>
```

### Prominent Grid with Subtle Ticks

```tsx
<RangeNavigatorComponent
  majorGridLines={{
    width: 2,
    color: '#BDBDBD',
    dashArray: '0'
  }}
  majorTickLines={{
    width: 1,
    color: '#E0E0E0',
    dashArray: '0'
  }}
>
  {/* Series configuration */}
</RangeNavigatorComponent>
```

### Matching Styles

```tsx
<RangeNavigatorComponent
  majorGridLines={{
    width: 1,
    color: '#2196F3',
    dashArray: '5,5'
  }}
  majorTickLines={{
    width: 1,
    color: '#2196F3',
    dashArray: '5,5'
  }}
>
  {/* Series configuration */}
</RangeNavigatorComponent>
```

### Minimal Style (No Lines)

```tsx
<RangeNavigatorComponent
  majorGridLines={{ width: 0 }}
  majorTickLines={{ width: 0 }}
>
  {/* Series configuration */}
</RangeNavigatorComponent>
```

## Complete Example with Both Customizations

```tsx
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
import * as React from 'react';

function App() {
  const data = [
    { date: new Date(2023, 0, 1), value: 100 },
    { date: new Date(2023, 1, 1), value: 110 },
    { date: new Date(2023, 2, 1), value: 105 },
    { date: new Date(2023, 3, 1), value: 115 },
    { date: new Date(2023, 4, 1), value: 120 },
    { date: new Date(2023, 5, 1), value: 125 },
    { date: new Date(2023, 6, 1), value: 130 },
    { date: new Date(2023, 7, 1), value: 128 },
    { date: new Date(2023, 8, 1), value: 135 },
    { date: new Date(2023, 9, 1), value: 140 },
    { date: new Date(2023, 10, 1), value: 138 },
    { date: new Date(2023, 11, 1), value: 145 }
  ];

  return (
    <div className="App">
      <h2>Range Navigator with Custom Grid and Tick Lines</h2>
      <RangeNavigatorComponent
        id="rangeNavigator"
        valueType="DateTime"
        labelFormat="MMM"
        value={[new Date(2023, 2, 1), new Date(2023, 9, 1)]}
        tooltip={{ enable: true }}
        
        // Grid line customization
        majorGridLines={{
          width: 1.5,
          color: '#BDBDBD',
          dashArray: '5,3'
        }}
        
        // Tick line customization
        majorTickLines={{
          width: 2,
          color: '#2196F3',
          dashArray: '0'
        }}
      >
        <Inject services={[AreaSeries, DateTime, RangeTooltip ]} />
        <RangenavigatorSeriesCollectionDirective>
          <RangenavigatorSeriesDirective
            dataSource={data}
            xName="date"
            yName="value"
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

## Numeric Axis Grid and Tick Lines

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
    { x: 50, y: 55 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="Double"
      interval={10}
      majorGridLines={{
        width: 1,
        color: '#E0E0E0',
        dashArray: '0'
      }}
      majorTickLines={{
        width: 2,
        color: '#666666',
        dashArray: '0'
      }}
    >
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
};

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## Themed Grid and Tick Lines

Match grid and tick lines to your application theme:

### Material Theme Style

```tsx
majorGridLines={{
  width: 1,
  color: '#E0E0E0',
  dashArray: '0'
}}
majorTickLines={{
  width: 1,
  color: '#757575',
  dashArray: '0'
}}
```

### Dark Theme Style

```tsx
majorGridLines={{
  width: 1,
  color: '#424242',
  dashArray: '0'
}}
majorTickLines={{
  width: 2,
  color: '#BDBDBD',
  dashArray: '0'
}}
```

### Fluent Theme Style

```tsx
majorGridLines={{
  width: 1,
  color: '#EDEBE9',
  dashArray: '0'
}}
majorTickLines={{
  width: 1,
  color: '#605E5C',
  dashArray: '0'
}}
```

## Interactive Example with Style Switching

```tsx
import { useState } from 'react';
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
  const [gridStyle, setGridStyle] = useState('default');

  const data = [
    { date: new Date(2023, 0, 1), value: 100 },
    { date: new Date(2023, 1, 1), value: 110 },
    { date: new Date(2023, 2, 1), value: 105 },
    { date: new Date(2023, 3, 1), value: 115 }
  ];

  const gridStyles = {
    default: {
      grid: { width: 1, color: '#E0E0E0', dashArray: '0' },
      tick: { width: 1, color: '#666666', dashArray: '0' }
    },
    dashed: {
      grid: { width: 1, color: '#BDBDBD', dashArray: '5,5' },
      tick: { width: 2, color: '#2196F3', dashArray: '0' }
    },
    minimal: {
      grid: { width: 0 },
      tick: { width: 0 }
    },
    bold: {
      grid: { width: 2, color: '#999999', dashArray: '0' },
      tick: { width: 3, color: '#333333', dashArray: '0' }
    }
  };

  return (
    <div>
      <div>
        <button onClick={() => setGridStyle('default')}>Default</button>
        <button onClick={() => setGridStyle('dashed')}>Dashed</button>
        <button onClick={() => setGridStyle('minimal')}>Minimal</button>
        <button onClick={() => setGridStyle('bold')}>Bold</button>
      </div>

      <RangeNavigatorComponent
        id="rangeNavigator"
        valueType="DateTime"
        labelFormat="MMM"
        majorGridLines={gridStyles[gridStyle].grid}
        majorTickLines={gridStyles[gridStyle].tick}
      >
        <Inject services={[AreaSeries, DateTime]} />
        <RangenavigatorSeriesCollectionDirective>
          <RangenavigatorSeriesDirective
            dataSource={data}
            xName="date"
            yName="value"
            type="Area"
          />
        </RangenavigatorSeriesCollectionDirective>
      </RangeNavigatorComponent>
    </div>
  );
};

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## Configuration Summary

### Major Grid Lines Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| width | Number | 1 | Line thickness in pixels |
| color | String | '#E0E0E0' | Line color |
| dashArray | String | '0' | Dash pattern (e.g., '5,3') |

### Major Tick Lines Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| width | Number | 1 | Line thickness in pixels |
| color | String | '#666666' | Line color |
| dashArray | String | '0' | Dash pattern (e.g., '5,3') |

## API Links

Full Range Navigator API: https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default

Grid/tick complex API references:
- [`majorGridLines`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#majorGridLines) (width, color, dashArray)
- [`majorTickLines`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#majorTickLines) (width, color, dashArray)
- [`tickPosition`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#tickPosition) and axis positioning props


## Best Practices

1. **Subtle Grid Lines**: Use light colors (#E0E0E0, #F5F5F5) for grid lines to avoid visual clutter
2. **Contrast**: Ensure sufficient contrast between grid/tick lines and background
3. **Consistency**: Match grid and tick line styles for cohesive appearance
4. **Accessibility**: Don't rely solely on grid lines for data interpretation
5. **Performance**: Avoid extremely thin lines (< 0.5px) on low-DPI screens
6. **Theme Matching**: Coordinate colors with your application theme
7. **Minimal When Possible**: Hide grid/tick lines if not needed for cleaner appearance

## Common Use Cases

### Financial Charts
- Subtle dashed grid lines for reference
- Bold tick lines for precise time markers

### Analytics Dashboards
- Solid light grid lines
- Standard tick lines

### Minimalist Design
- No grid lines
- Subtle or no tick lines

### High Contrast
- Bold grid lines
- Prominent tick lines in accent colors
