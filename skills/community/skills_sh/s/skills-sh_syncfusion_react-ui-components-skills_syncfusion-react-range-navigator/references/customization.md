# Customization

The Range Navigator provides extensive customization options for its appearance and behavior, including navigator regions, thumbs, borders, update modes, snapping, and animation.

## Table of Contents
- [Navigator Appearance](#navigator-appearance)
- [Thumb Customization](#thumb-customization)
- [Border Customization](#border-customization)
- [Deferred Update](#deferred-update)
- [Allow Snapping](#allow-snapping)
- [Animation Duration](#animation-duration)

## Navigator Appearance

Customize the Range Selector appearance using the `navigatorStyleSettings` property. You can configure colors for selected and unselected regions.

### Selected and Unselected Regions

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
    { x: new Date(2023, 0, 1), y: 100 },
    { x: new Date(2023, 1, 1), y: 110 },
    { x: new Date(2023, 2, 1), y: 105 },
    { x: new Date(2023, 3, 1), y: 115 },
    { x: new Date(2023, 4, 1), y: 120 },
    { x: new Date(2023, 5, 1), y: 125 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="DateTime"
      navigatorStyleSettings={{
        selectedRegionColor: 'rgba(33, 150, 243, 0.3)',
        unselectedRegionColor: 'rgba(128, 128, 128, 0.1)'
      }}
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

### Navigator Style Settings Properties

- **selectedRegionColor**: Color for the selected range (default: varies by theme)
- **unselectedRegionColor**: Color for the unselected regions (default: transparent)

### Common Color Patterns

```tsx
// Transparent unselected region (default)
navigatorStyleSettings={{
  selectedRegionColor: 'rgba(33, 150, 243, 0.3)',
  unselectedRegionColor: 'transparent'
}}

// Subtle gray for unselected
navigatorStyleSettings={{
  selectedRegionColor: 'rgba(0, 123, 255, 0.4)',
  unselectedRegionColor: 'rgba(200, 200, 200, 0.1)'
}}

// High contrast
navigatorStyleSettings={{
  selectedRegionColor: 'rgba(76, 175, 80, 0.5)',
  unselectedRegionColor: 'rgba(0, 0, 0, 0.05)'
}}
```

## Thumb Customization

Thumbs are the draggable handles on the Range Selector. Customize their appearance including shape, size, color, and border.

### Thumb Properties

- **type**: Shape of the thumb ('Circle' | 'Rectangle')
- **width**: Width of the thumb in pixels
- **height**: Height of the thumb in pixels
- **fill**: Fill color of the thumb
- **border**: Border configuration (width, color)

### Circle Thumb

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
    { x: new Date(2023, 0, 1), y: 100 },
    { x: new Date(2023, 1, 1), y: 110 },
    { x: new Date(2023, 2, 1), y: 105 },
    { x: new Date(2023, 3, 1), y: 115 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="DateTime"
      navigatorStyleSettings={{
        thumb: {
          type: 'Circle',
          width: 20,
          height: 20,
          fill: '#2196F3',
          border: { width: 2, color: '#ffffff' }
        }
      }}
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

### Rectangle Thumb

```tsx
<RangeNavigatorComponent
  id="rangeNavigator"
  valueType="DateTime"
  navigatorStyleSettings={{
    thumb: {
      type: 'Rectangle',
      width: 15,
      height: 40,
      fill: '#4CAF50',
      border: { width: 1, color: '#2E7D32' }
    }
  }}
>
  {/* Series configuration */}
</RangeNavigatorComponent>
```

### Complete Thumb Customization Example

```tsx
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
      navigatorStyleSettings={{
        selectedRegionColor: 'rgba(33, 150, 243, 0.3)',
        unselectedRegionColor: 'transparent',
        thumb: {
          type: 'Circle',
          width: 24,
          height: 24,
          fill: '#2196F3',
          border: { 
            width: 3, 
            color: '#ffffff' 
          }
        }
      }}
    >
      <Inject services={[AreaSeries, DateTime]} />
      <RangenavigatorSeriesCollectionDirective>
        <RangenavigatorSeriesDirective
          dataSource={stockData}
          xName="date"
          yName="price"
          type="Area"
        />
      </RangenavigatorSeriesCollectionDirective>
    </RangeNavigatorComponent>
  );
}
```

## Border Customization

Customize the border around the entire Range Navigator using the `navigatorBorder` property.

### Border Properties

- **width**: Border width in pixels
- **color**: Border color

### Basic Border Customization

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
    { x: new Date(2023, 0, 1), y: 100 },
    { x: new Date(2023, 1, 1), y: 110 },
    { x: new Date(2023, 2, 1), y: 105 },
    { x: new Date(2023, 3, 1), y: 115 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="DateTime"
      navigatorBorder={{ 
        width: 2, 
        color: '#2196F3' 
      }}
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

### Border Styles

```tsx
// Thin border
navigatorBorder={{ width: 1, color: '#CCCCCC' }}

// Medium border (default-like)
navigatorBorder={{ width: 2, color: '#2196F3' }}

// Thick border
navigatorBorder={{ width: 4, color: '#1976D2' }}

// No border
navigatorBorder={{ width: 0, color: 'transparent' }}
```

### Complete Border and Appearance Example

```tsx
function App() {
  const data = [
    { x: new Date(2023, 0, 1), y: 100 },
    { x: new Date(2023, 1, 1), y: 110 },
    { x: new Date(2023, 2, 1), y: 105 },
    { x: new Date(2023, 3, 1), y: 115 },
    { x: new Date(2023, 4, 1), y: 120 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="DateTime"
      navigatorBorder={{ 
        width: 3, 
        color: '#2196F3' 
      }}
      navigatorStyleSettings={{
        selectedRegionColor: 'rgba(33, 150, 243, 0.3)',
        unselectedRegionColor: 'transparent',
        thumb: {
          type: 'Rectangle',
          width: 15,
          height: 45,
          fill: '#2196F3',
          border: { width: 2, color: '#ffffff' }
        }
      }}
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
```

## Deferred Update

The `enableDeferredUpdate` property controls when the `changed` event fires during thumb dragging.

### Behavior

- **false** (default): `changed` event fires continuously while dragging
- **true**: `changed` event fires only after dragging completes

### Enable Deferred Update

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
    { x: new Date(2023, 0, 1), y: 100 },
    { x: new Date(2023, 1, 1), y: 110 },
    { x: new Date(2023, 2, 1), y: 105 },
    { x: new Date(2023, 3, 1), y: 115 }
  ];

  const handleChange = (args) => {
    console.log('Range changed:', args.start, args.end);
    // This fires only after dragging completes when enableDeferredUpdate is true
  };

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="DateTime"
      enableDeferredUpdate={true}
      changed={handleChange}
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

### When to Use Deferred Update

**Use `enableDeferredUpdate={true}` when:**
- Performing expensive operations on range change (API calls, heavy calculations)
- Updating large data grids or charts
- Network requests based on selected range
- Performance optimization is needed

**Use `enableDeferredUpdate={false}` (default) when:**
- Real-time updates are needed
- Simple UI updates
- Immediate feedback is important
- Operations are lightweight

### Deferred Update with Data Grid Example

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
  const [selectedRange, setSelectedRange] = useState({
    start: new Date(2023, 0, 1),
    end: new Date(2023, 5, 1)
  });

  const data = [
    { date: new Date(2023, 0, 1), value: 100 },
    { date: new Date(2023, 1, 1), value: 110 },
    { date: new Date(2023, 2, 1), value: 105 },
    { date: new Date(2023, 3, 1), value: 115 },
    { date: new Date(2023, 4, 1), value: 120 },
    { date: new Date(2023, 5, 1), value: 125 }
  ];

  const handleRangeChange = (args) => {
    setSelectedRange({
      start: args.start,
      end: args.end
    });
    // Fetch filtered data from API
    // fetchData(args.start, args.end);
  };

  return (
    <div>
      <RangeNavigatorComponent
        id="rangeNavigator"
        valueType="DateTime"
        enableDeferredUpdate={true}
        changed={handleRangeChange}
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

      <div>
        <p>Selected Range:</p>
        <p>Start: {selectedRange.start.toDateString()}</p>
        <p>End: {selectedRange.end.toDateString()}</p>
      </div>
    </div>
  );
}
```

## Allow Snapping

The `allowSnapping` property toggles whether the slider snaps exactly to the nearest interval.

### Behavior

- **false** (default): Slider can be placed anywhere
- **true**: Slider snaps to nearest interval tick

### Enable Snapping

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
    { x: new Date(2023, 0, 1), y: 100 },
    { x: new Date(2023, 1, 1), y: 110 },
    { x: new Date(2023, 2, 1), y: 105 },
    { x: new Date(2023, 3, 1), y: 115 },
    { x: new Date(2023, 4, 1), y: 120 },
    { x: new Date(2023, 5, 1), y: 125 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="DateTime"
      intervalType="Months"
      allowSnapping={true}
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

### When to Use Snapping

**Use `allowSnapping={true}` when:**
- Data points are at specific intervals (months, quarters, years)
- Precise alignment with data points is required
- Filtering by exact time periods
- Categorical or discrete data

**Use `allowSnapping={false}` (default) when:**
- Continuous data ranges
- Flexibility in range selection is needed
- Sub-interval precision is important

### Snapping with Numeric Intervals

```tsx
<RangeNavigatorComponent
  valueType="Double"
  minimum={0}
  maximum={100}
  interval={10}
  allowSnapping={true}
>
  {/* Slider snaps to 0, 10, 20, 30, ... 100 */}
</RangeNavigatorComponent>
```

## Animation Duration

Control the speed of Range Navigator animations using the `animationDuration` property.

### Animation Duration Property

- **Default:** 500 milliseconds
- **Range:** 0 to any positive number
- **Unit:** Milliseconds
- **0:** Disables animation

### Custom Animation Duration

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
    { x: new Date(2023, 0, 1), y: 100 },
    { x: new Date(2023, 1, 1), y: 110 },
    { x: new Date(2023, 2, 1), y: 105 },
    { x: new Date(2023, 3, 1), y: 115 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="DateTime"
      animationDuration={1000}
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

### Animation Duration Examples

```tsx
// No animation
animationDuration={0}

// Fast animation
animationDuration={200}

// Default animation
animationDuration={500}

// Slow animation
animationDuration={1000}

// Very slow animation
animationDuration={2000}
```

### When to Adjust Animation Duration

**Use faster animations (200-300ms) when:**
- Frequent user interactions expected
- Real-time data updates
- Performance is critical

**Use default (500ms) when:**
- Standard user experience desired
- Balanced performance and visual appeal

**Use slower animations (800-1200ms) when:**
- Emphasis on visual transitions
- Tutorial or demonstration mode
- Smooth, elegant transitions desired

**Disable animations (0ms) when:**
- Maximum performance needed
- Accessibility requirements (reduced motion)
- Testing or automation

## Complete Customization Example

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
  const stockData = [
    { date: new Date(2023, 0, 1), price: 100 },
    { date: new Date(2023, 1, 1), price: 110 },
    { date: new Date(2023, 2, 1), price: 105 },
    { date: new Date(2023, 3, 1), price: 115 },
    { date: new Date(2023, 4, 1), price: 120 },
    { date: new Date(2023, 5, 1), price: 125 },
    { date: new Date(2023, 6, 1), price: 130 },
    { date: new Date(2023, 7, 1), price: 128 },
    { date: new Date(2023, 8, 1), price: 135 },
    { date: new Date(2023, 9, 1), price: 140 },
    { date: new Date(2023, 10, 1), price: 138 },
    { date: new Date(2023, 11, 1), price: 145 }
  ];

  const handleRangeChange = (args) => {
    console.log('Selected Range:', args.start, 'to', args.end);
  };

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="DateTime"
      labelFormat="MMM"
      value={[new Date(2023, 2, 1), new Date(2023, 9, 1)]}
      
      // Appearance
      navigatorStyleSettings={{
        selectedRegionColor: 'rgba(33, 150, 243, 0.3)',
        unselectedRegionColor: 'transparent',
        thumb: {
          type: 'Circle',
          width: 24,
          height: 24,
          fill: '#2196F3',
          border: { width: 3, color: '#ffffff' }
        }
      }}
      navigatorBorder={{ width: 2, color: '#2196F3' }}
      
      // Behavior
      enableDeferredUpdate={true}
      allowSnapping={true}
      animationDuration={800}
      
      // Event
      changed={handleRangeChange}
    >
      <Inject services={[AreaSeries, DateTime]} />
      <RangenavigatorSeriesCollectionDirective>
        <RangenavigatorSeriesDirective
          dataSource={stockData}
          xName="date"
          yName="price"
          type="Area"
        />
      </RangenavigatorSeriesCollectionDirective>
    </RangeNavigatorComponent>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## Customization Summary

| Feature | Property | Default | Options |
|---------|----------|---------|---------|
| Selected region color | navigatorStyleSettings.selectedRegionColor | Theme-based | Any color/rgba |
| Unselected region color | navigatorStyleSettings.unselectedRegionColor | transparent | Any color/rgba |
| Thumb shape | navigatorStyleSettings.thumb.type | Circle | Circle, Rectangle |
| Thumb size | navigatorStyleSettings.thumb.width/height | 15/15 | Any number |
| Border | navigatorBorder.width/color | 1/theme | Any number/color |
| Deferred update | enableDeferredUpdate | false | true, false |
| Snapping | allowSnapping | false | true, false |
| Animation speed | animationDuration | 500 | 0-any number (ms) |

## API Links

Full Range Navigator API: https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default

Customization-specific complex API references:
- [`navigatorStyleSettings`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#navigatorStyleSettings) (selectedRegionColor, unselectedRegionColor, thumb: { type, width, height, fill, border })
- [`navigatorBorder`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#navigatorBorder) (width, color)
- [`enableDeferredUpdate`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#enableDeferredUpdate), [`allowSnapping`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#allowSnapping), [`animationDuration`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#animationDuration), [`allowIntervalData`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#allowIntervalData)

