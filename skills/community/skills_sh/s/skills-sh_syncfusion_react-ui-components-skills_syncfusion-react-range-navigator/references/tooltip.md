# Tooltip

Tooltips display the selected start and end values when users interact with the range sliders. The Range Navigator provides extensive customization options for tooltip appearance and behavior.

## Table of Contents
- [Enabling Tooltip](#enabling-tooltip)
- [Tooltip Customization](#tooltip-customization)
- [Label Format](#label-format)
- [Display Modes](#display-modes)

## Enabling Tooltip

### Module Injection Required

To use tooltips, inject the `RangeTooltip` module:

```tsx
import { RangeTooltip } from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';
<Inject services={[RangeTooltip, AreaSeries, DateTime]} />
```

### Basic Tooltip Implementation

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
    { date: new Date(2023, 3, 1), value: 115 }
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

## Tooltip Customization

Customize tooltip appearance using these properties:

- **enable**: Show or hide tooltip
- **fill**: Background color of tooltip
- **opacity**: Transparency level (0 to 1)
- **textStyle**: Font customization (size, color, family, style, weight)
- **displayMode**: When to show tooltip ('OnDemand' or 'Always')

### Complete Tooltip Customization

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
    { date: new Date(2023, 4, 1), value: 120 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="DateTime"
      labelFormat="MMM"
      tooltip={{
        enable: true,
        fill: '#2196F3',
        opacity: 0.9,
        textStyle: {
          size: '14px',
          color: '#ffffff',
          fontFamily: 'Segoe UI',
          fontWeight: '600'
        },
        displayMode: 'Always'
      }}
    >
      <Inject services={[AreaSeries, DateTime, RangeTooltip  ]} />
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

### Tooltip Fill Color Examples

```tsx
// Material Design Blue
tooltip={{ enable: true, fill: '#2196F3', opacity: 0.9 }}

// Success Green
tooltip={{ enable: true, fill: '#4CAF50', opacity: 0.85 }}

// Dark Theme
tooltip={{ enable: true, fill: '#212121', opacity: 0.95 }}

// Gradient (requires CSS)
tooltip={{ enable: true, fill: '#FF6B6B', opacity: 0.9 }}
```

### Text Style Customization

```tsx
tooltip={{
  enable: true,
  textStyle: {
    size: '16px',           // Font size
    color: '#ffffff',       // Text color
    fontFamily: 'Arial',    // Font family
    fontStyle: 'normal',    // normal | italic | oblique
    fontWeight: 'bold'      // normal | bold | 100-900
  }
}}
```

## Label Format

The `labelFormat` property formats the date values displayed in tooltips.

### DateTime Format Examples

```tsx
// Month name
tooltip={{ enable: true, labelFormat: 'MMM' }}
// Result: Jan, Feb, Mar

// Month/Day/Year
tooltip={{ enable: true, labelFormat: 'yMd' }}
// Result: 04/10/2000

// Full day name
tooltip={{ enable: true, labelFormat: 'EEEE' }}
// Result: Monday, Tuesday

// Month and year
tooltip={{ enable: true, labelFormat: 'MMM yyyy' }}
// Result: Jan 2023, Feb 2023

// Time display
tooltip={{ enable: true, labelFormat: 'hm' }}
// Result: 12:00 AM, 1:30 PM

// Full date and time
tooltip={{ enable: true, labelFormat: 'yMd hms' }}
// Result: 04/10/2000 12:00:00 AM
```

### DateTime Format Reference Table

| Label Value | Format | Result | Description |
|------------|--------|--------|-------------|
| new Date(2000, 3, 10) | EEEE | Monday | Day name in full |
| new Date(2000, 3, 10) | yMd | 04/10/2000 | Month/date/year format |
| new Date(2000, 3, 10) | MMM | Apr | Month abbreviation |
| new Date(2000, 3, 10) | hm | 12:00 AM | Time in hours:minutes |
| new Date(2000, 3, 10) | hms | 12:00:00 AM | Time with seconds |

### Complete Label Format Example

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
      tooltip={{
        enable: true,
        labelFormat: 'MMM dd, yyyy',
        fill: '#2196F3',
        opacity: 0.9,
        textStyle: {
          size: '14px',
          color: '#ffffff',
          fontWeight: '600'
        }
      }}
    >
      <Inject services={[AreaSeries, DateTime, RangeTooltip ]} />
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

## Display Modes

The `displayMode` property controls when tooltips appear.

### OnDemand Mode (Default)

Tooltips appear only when user hovers over or drags the thumb:

```tsx
tooltip={{
  enable: true,
  displayMode: 'OnDemand'
}}
```

**Use OnDemand when:**
- Clean UI is preferred
- Tooltips might obstruct view
- Users are experienced
- Screen space is limited

### Always Mode

Tooltips are always visible on both thumbs:

```tsx
tooltip={{
  enable: true,
  displayMode: 'Always'
}}
```

**Use Always when:**
- Range values are critical
- Users need constant feedback
- Data precision is important
- Training or demo scenarios

### Display Mode Comparison

```tsx
import { useState } from 'react';
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
  const [displayMode, setDisplayMode] = useState('OnDemand');

  const data = [
    { date: new Date(2023, 0, 1), value: 100 },
    { date: new Date(2023, 1, 1), value: 110 },
    { date: new Date(2023, 2, 1), value: 105 },
    { date: new Date(2023, 3, 1), value: 115 }
  ];

  return (
    <div>
      <div>
        <button onClick={() => setDisplayMode('OnDemand')}>OnDemand</button>
        <button onClick={() => setDisplayMode('Always')}>Always</button>
      </div>

      <RangeNavigatorComponent
        id="rangeNavigator"
        valueType="DateTime"
        tooltip={{
          enable: true,
          displayMode: displayMode
        }}
      >
        <Inject services={[AreaSeries, DateTime, RangeTooltip  ]} />
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

## Numeric Value Tooltip

For numeric data, tooltips display the selected numeric range:

```tsx
import { 
  RangeNavigatorComponent, 
  AreaSeries, 
  RangeTooltip, 
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
    { x: 40, y: 35 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="Double"
      tooltip={{
        enable: true,
        fill: '#4CAF50',
        textStyle: {
          size: '14px',
          color: '#ffffff'
        }
      }}
    >
      <Inject services={[AreaSeries, RangeTooltip]} />
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

## Tooltip with Period Selector

```tsx
import { 
  RangeNavigatorComponent, 
  AreaSeries, 
  DateTime, 
  RangeTooltip, 
  PeriodSelector, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective 
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const data = [
    { date: new Date(2020, 0, 1), value: 100 },
    { date: new Date(2020, 3, 1), value: 110 },
    { date: new Date(2020, 6, 1), value: 105 },
    { date: new Date(2020, 9, 1), value: 115 },
    { date: new Date(2021, 0, 1), value: 120 },
    { date: new Date(2021, 3, 1), value: 130 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="DateTime"
      labelFormat="MMM yyyy"
      tooltip={{
        enable: true,
        displayMode: 'Always',
        labelFormat: 'MMM dd, yyyy',
        fill: '#2196F3',
        opacity: 0.9
      }}
      periodSelectorSettings={{
        periods: [
          { intervalType: 'Months', interval: 3, text: '3M' },
          { intervalType: 'Months', interval: 6, text: '6M' },
          { intervalType: 'Years', interval: 1, text: '1Y' }
        ]
      }}
    >
      <Inject services={[AreaSeries, DateTime, RangeTooltip, PeriodSelector]} />
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

## Complete Tooltip Example

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

  return (
    <div className="App">
      <h2>Stock Price Navigator with Tooltip</h2>
      <RangeNavigatorComponent
        id="rangeNavigator"
        valueType="DateTime"
        labelFormat="MMM"
        value={[new Date(2023, 2, 1), new Date(2023, 9, 1)]}
        tooltip={{
          enable: true,
          displayMode: 'Always',
          labelFormat: 'MMM dd, yyyy',
          fill: '#2196F3',
          opacity: 0.95,
          textStyle: {
            size: '14px',
            color: '#ffffff',
            fontFamily: 'Segoe UI',
            fontWeight: '600'
          }
        }}
      >
        <Inject services={[AreaSeries, DateTime, RangeTooltip ]} />
        <RangenavigatorSeriesCollectionDirective>
          <RangenavigatorSeriesDirective
            dataSource={stockData}
            xName="date"
            yName="price"
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

## Tooltip Configuration Summary

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| enable | Boolean | false | Enable or disable tooltip |
| fill | String | Theme-based | Background color |
| opacity | Number | 0.95 | Transparency (0-1) |
| displayMode | String | 'OnDemand' | 'OnDemand' or 'Always' |
| labelFormat | String | Auto | Date/time format string |
| textStyle.size | String | '12px' | Font size |
| textStyle.color | String | '#ffffff' | Text color |
| textStyle.fontFamily | String | 'Segoe UI' | Font family |
| textStyle.fontWeight | String | 'normal' | Font weight |
| textStyle.fontStyle | String | 'normal' | Font style |

## Key Points

1. **Module Injection**: Always inject `RangeTooltip` module to use tooltips
2. **Enable Required**: Set `tooltip.enable` to `true`
3. **Format Flexibility**: Use `labelFormat` for custom date/time display
4. **Display Modes**: Choose between 'OnDemand' (hover) and 'Always' (persistent)
5. **Full Customization**: Customize colors, fonts, opacity, and text styling
6. **Works with All Features**: Compatible with period selector, lightweight mode, and all value types

## API Links

Full Range Navigator API: https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default

Tooltip-specific complex API references:
- [`tooltip`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#tooltip) (): `enable`, `fill`, `opacity`, `textStyle`, `displayMode`, `labelFormat`
- Module: [`RangeTooltip`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#rangeTooltipModule) and ``
- Event: [`tooltipRender`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#tooltipRender)

