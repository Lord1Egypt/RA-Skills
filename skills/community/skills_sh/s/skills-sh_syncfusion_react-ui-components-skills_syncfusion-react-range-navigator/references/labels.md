# Labels

The Range Navigator provides extensive label customization options including multilevel labels, grouping, smart label overlap handling, positioning, and style customization.

## Table of Contents
- [Multilevel Labels](#multilevel-labels)
- [Grouping](#grouping)
- [Smart Labels](#smart-labels)
- [Label Positioning](#label-positioning)
- [Label Style Customization](#label-style-customization)

## Multilevel Labels

Multilevel labels display hierarchical date information (e.g., months grouped under years). This feature is restricted to DateTime axis only.

### Enabling Multilevel Labels

Set the `enableGrouping` property to `true`:

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
    { date: new Date(2020, 0, 1), value: 100 },
    { date: new Date(2020, 1, 1), value: 110 },
    { date: new Date(2020, 2, 1), value: 105 },
    { date: new Date(2020, 3, 1), value: 115 },
    { date: new Date(2020, 4, 1), value: 120 },
    { date: new Date(2020, 5, 1), value: 125 },
    { date: new Date(2020, 6, 1), value: 130 },
    { date: new Date(2020, 7, 1), value: 128 },
    { date: new Date(2020, 8, 1), value: 135 },
    { date: new Date(2020, 9, 1), value: 140 },
    { date: new Date(2020, 10, 1), value: 138 },
    { date: new Date(2020, 11, 1), value: 145 },
    { date: new Date(2021, 0, 1), value: 150 },
    { date: new Date(2021, 1, 1), value: 155 },
    { date: new Date(2021, 2, 1), value: 160 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="DateTime"
      enableGrouping={true}
      labelFormat="MMM"
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

### How Multilevel Labels Work

When `enableGrouping` is enabled:
- **First Level**: Individual time units (days, months, hours)
- **Second Level**: Grouped time units (months, years, days)

**Example:**
- First level shows: Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec
- Second level shows: 2020, 2021

## Grouping

The `groupBy` property controls how multilevel labels are grouped.

### Available Grouping Interval Types

- **Auto**: Automatically determined based on data range
- **Years**: Group by years
- **Quarter**: Group by quarters (Q1, Q2, Q3, Q4)
- **Months**: Group by months
- **Weeks**: Group by weeks
- **Days**: Group by days
- **Hours**: Group by hours
- **Minutes**: Group by minutes
- **Seconds**: Group by seconds

### Grouping by Years

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
    { date: new Date(2018, 0, 1), value: 100 },
    { date: new Date(2018, 6, 1), value: 110 },
    { date: new Date(2019, 0, 1), value: 120 },
    { date: new Date(2019, 6, 1), value: 130 },
    { date: new Date(2020, 0, 1), value: 140 },
    { date: new Date(2020, 6, 1), value: 150 },
    { date: new Date(2021, 0, 1), value: 160 },
    { date: new Date(2021, 6, 1), value: 170 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="DateTime"
      enableGrouping={true}
      groupBy="Years"
      labelFormat="MMM"
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

### Grouping by Months

```tsx
<RangeNavigatorComponent
  valueType="DateTime"
  enableGrouping={true}
  groupBy="Months"
  intervalType="Days"
  labelFormat="dd"
>
  {/* First level: Days (1, 2, 3, 4...) */}
  {/* Second level: Months (Jan, Feb, Mar...) */}
</RangeNavigatorComponent>
```

### Grouping by Quarter

```tsx
<RangeNavigatorComponent
  valueType="DateTime"
  enableGrouping={true}
  groupBy="Quarter"
  intervalType="Months"
  labelFormat="MMM"
>
  {/* First level: Months (Jan, Feb, Mar...) */}
  {/* Second level: Quarters (Q1, Q2, Q3, Q4) */}
</RangeNavigatorComponent>
```

### Auto Grouping

```tsx
<RangeNavigatorComponent
  valueType="DateTime"
  enableGrouping={true}
  groupBy="Auto"
>
  {/* Automatically determines best grouping based on data */}
</RangeNavigatorComponent>
```

## Smart Labels

The `labelIntersectAction` property prevents label overlap by hiding overlapping labels.

### Available Actions

- **None** (default): No action, labels may overlap
- **Hide**: Hide overlapping labels

### Basic Smart Labels

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
    { date: new Date(2023, 0, 5), value: 105 },
    { date: new Date(2023, 0, 10), value: 110 },
    { date: new Date(2023, 0, 15), value: 108 },
    { date: new Date(2023, 0, 20), value: 115 },
    { date: new Date(2023, 0, 25), value: 120 },
    { date: new Date(2023, 0, 30), value: 125 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="DateTime"
      labelIntersectAction="Hide"
      labelFormat="dd MMM"
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

### When to Use Smart Labels

**Use `labelIntersectAction="Hide"` when:**
- Many data points in narrow space
- Long label text
- Small screen sizes
- Zoomed in views
- Preventing visual clutter

**Use `labelIntersectAction="None"` (default) when:**
- Sufficient space between labels
- Short label text
- All labels must be visible
- Custom label management

## Label Positioning

Control whether labels appear inside or outside the Range Navigator using the `labelPosition` property.

### Available Positions

- **Outside** (default): Labels appear below the Range Navigator
- **Inside**: Labels appear inside the Range Navigator

### Labels Outside (Default)

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
    { date: new Date(2023, 3, 1), value: 115 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="DateTime"
      labelPosition="Outside"
      labelFormat="MMM"
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

### Labels Inside

```tsx
<RangeNavigatorComponent
  id="rangeNavigator"
  valueType="DateTime"
  labelPosition="Inside"
  labelFormat="MMM"
>
  {/* Labels appear inside the navigator area */}
</RangeNavigatorComponent>
```

### Position Selection Guide

**Use `labelPosition="Outside"` when:**
- More space available vertically
- Clean separator between navigator and labels
- Traditional chart appearance preferred

**Use `labelPosition="Inside"` when:**
- Compact vertical layout needed
- Minimizing component height
- Integrated appearance preferred
- Labels should be closer to data

## Label Style Customization

Customize label appearance using the `labelStyle` property. You can configure font size, color, family, weight, and style.

### Label Style Properties

- **size**: Font size (e.g., '12px', '14px')
- **color**: Text color
- **fontFamily**: Font family name
- **fontWeight**: Font weight (normal, bold, 100-900)
- **fontStyle**: Font style (normal, italic, oblique)

### Basic Label Style

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
    { date: new Date(2023, 3, 1), value: 115 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="DateTime"
      labelFormat="MMM"
      labelStyle={{
        size: '14px',
        color: '#2196F3',
        fontFamily: 'Arial',
        fontWeight: 'bold'
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

### Label Style Variations

```tsx
// Large bold labels
labelStyle={{
  size: '16px',
  color: '#333333',
  fontWeight: 'bold'
}}

// Italic subtle labels
labelStyle={{
  size: '12px',
  color: '#666666',
  fontStyle: 'italic',
  fontWeight: 'normal'
}}

// Custom font family
labelStyle={{
  size: '14px',
  color: '#2196F3',
  fontFamily: 'Roboto',
  fontWeight: '600'
}}
```

## Complete Labels Example

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
    { date: new Date(2020, 0, 1), value: 100 },
    { date: new Date(2020, 1, 1), value: 110 },
    { date: new Date(2020, 2, 1), value: 105 },
    { date: new Date(2020, 3, 1), value: 115 },
    { date: new Date(2020, 4, 1), value: 120 },
    { date: new Date(2020, 5, 1), value: 125 },
    { date: new Date(2020, 6, 1), value: 130 },
    { date: new Date(2020, 7, 1), value: 128 },
    { date: new Date(2020, 8, 1), value: 135 },
    { date: new Date(2020, 9, 1), value: 140 },
    { date: new Date(2020, 10, 1), value: 138 },
    { date: new Date(2020, 11, 1), value: 145 },
    { date: new Date(2021, 0, 1), value: 150 },
    { date: new Date(2021, 1, 1), value: 155 },
    { date: new Date(2021, 2, 1), value: 160 },
    { date: new Date(2021, 3, 1), value: 165 }
  ];

  return (
    <div className="App">
      <h2>Range Navigator with Custom Labels</h2>
      <RangeNavigatorComponent
        id="rangeNavigator"
        valueType="DateTime"
        enableGrouping={true}
        groupBy="Years"
        labelFormat="MMM"
        labelPosition="Outside"
        labelIntersectAction="Hide"
        labelStyle={{
          size: '13px',
          color: '#1976D2',
          fontFamily: 'Segoe UI',
          fontWeight: '600'
        }}
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
    </div>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## Grouping Interval Types

The `groupBy` property specifies the interval type for the second level of multilevel labels.

### Years Grouping

```tsx
<RangeNavigatorComponent
  valueType="DateTime"
  enableGrouping={true}
  groupBy="Years"
  intervalType="Months"
  labelFormat="MMM"
>
  {/* First level: Jan, Feb, Mar... */}
  {/* Second level: 2020, 2021, 2022 */}
</RangeNavigatorComponent>
```

### Quarter Grouping

```tsx
<RangeNavigatorComponent
  valueType="DateTime"
  enableGrouping={true}
  groupBy="Quarter"
  intervalType="Months"
  labelFormat="MMM"
>
  {/* First level: Jan, Feb, Mar... */}
  {/* Second level: Q1, Q2, Q3, Q4 */}
</RangeNavigatorComponent>
```

### Months Grouping

```tsx
<RangeNavigatorComponent
  valueType="DateTime"
  enableGrouping={true}
  groupBy="Months"
  intervalType="Days"
  labelFormat="dd"
>
  {/* First level: 1, 2, 3, 4... (days) */}
  {/* Second level: Jan, Feb, Mar... (months) */}
</RangeNavigatorComponent>
```

### Weeks Grouping

```tsx
<RangeNavigatorComponent
  valueType="DateTime"
  enableGrouping={true}
  groupBy="Weeks"
  intervalType="Days"
  labelFormat="dd"
>
  {/* First level: Days */}
  {/* Second level: Week numbers */}
</RangeNavigatorComponent>
```

### Days Grouping

```tsx
<RangeNavigatorComponent
  valueType="DateTime"
  enableGrouping={true}
  groupBy="Days"
  intervalType="Hours"
  labelFormat="hh a"
>
  {/* First level: Hours (12 AM, 1 AM, 2 AM...) */}
  {/* Second level: Days (Mon 1, Tue 2...) */}
</RangeNavigatorComponent>
```

### Hours Grouping

```tsx
<RangeNavigatorComponent
  valueType="DateTime"
  enableGrouping={true}
  groupBy="Hours"
  intervalType="Minutes"
  labelFormat="mm"
>
  {/* First level: Minutes (00, 15, 30, 45) */}
  {/* Second level: Hours (12 AM, 1 AM...) */}
</RangeNavigatorComponent>
```

### Auto Grouping (Recommended)

```tsx
<RangeNavigatorComponent
  valueType="DateTime"
  enableGrouping={true}
  groupBy="Auto"
>
  {/* Automatically determines best grouping based on data range */}
</RangeNavigatorComponent>
```

## Complete Multilevel Labels Example

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
  const yearlyData = [
    { date: new Date(2018, 0, 1), value: 100 },
    { date: new Date(2018, 3, 1), value: 110 },
    { date: new Date(2018, 6, 1), value: 105 },
    { date: new Date(2018, 9, 1), value: 115 },
    { date: new Date(2019, 0, 1), value: 120 },
    { date: new Date(2019, 3, 1), value: 130 },
    { date: new Date(2019, 6, 1), value: 125 },
    { date: new Date(2019, 9, 1), value: 135 },
    { date: new Date(2020, 0, 1), value: 140 },
    { date: new Date(2020, 3, 1), value: 145 },
    { date: new Date(2020, 6, 1), value: 150 },
    { date: new Date(2020, 9, 1), value: 155 },
    { date: new Date(2021, 0, 1), value: 160 },
    { date: new Date(2021, 3, 1), value: 165 },
    { date: new Date(2021, 6, 1), value: 170 },
    { date: new Date(2021, 9, 1), value: 175 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="DateTime"
      enableGrouping={true}
      groupBy="Years"
      intervalType="Months"
      interval={3}
      labelFormat="MMM"
      labelIntersectAction="Hide"
      labelStyle={{
        size: '13px',
        color: '#1976D2',
        fontFamily: 'Segoe UI',
        fontWeight: '600'
      }}
    >
      <Inject services={[AreaSeries, DateTime]} />
      <RangenavigatorSeriesCollectionDirective>
        <RangenavigatorSeriesDirective
          dataSource={yearlyData}
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

## Labels Configuration Summary

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| enableGrouping | Boolean | false | Enable multilevel labels (DateTime only) |
| groupBy | String | 'Auto' | Grouping interval type |
| labelPosition | String | 'Outside' | Label position ('Outside' or 'Inside') |
| labelIntersectAction | String | 'None' | Overlap handling ('None' or 'Hide') |
| labelFormat | String | Auto | Format string for labels |
| labelStyle | Object | Theme-based | Font and color settings |

### Label Style Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| size | String | '12px' | Font size |
| color | String | Theme-based | Text color |
| fontFamily | String | 'Segoe UI' | Font family |
| fontWeight | String | 'normal' | Font weight |
| fontStyle | String | 'normal' | Font style |

## Best Practices

1. **Enable Grouping**: Use multilevel labels for long time ranges to provide context
2. **Smart Labels**: Enable `labelIntersectAction="Hide"` for crowded labels
3. **Consistent Style**: Match label style with your application theme
4. **Appropriate Grouping**: Choose groupBy based on data range (Years for multi-year, Months for single year)
5. **Position Wisely**: Use Outside for clarity, Inside for compact layouts
6. **Readable Fonts**: Ensure sufficient contrast and size for accessibility
7. **Test Overlap**: Verify label visibility at different screen sizes

## API Links

Full Range Navigator API: https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default

Labeling-related complex API references:
- [`enableGrouping`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#enableGrouping), [`groupBy`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#groupBy), [`labelFormat`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#labelFormat), [`labelIntersectAction`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#labelIntersectAction), [`labelPosition`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#labelPosition), [`labelStyle`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#labelStyle), [`secondaryLabelAlignment`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#secondaryLabelAlignment)
- See API page for [`RangeIntervalType`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/rangeintervaltype) and supported interval enums

