# Chart Types Reference

## Table of Contents
- [Overview](#overview)
- [Cartesian Charts](#cartesian-charts)
- [Polar and Radar Charts](#polar-and-radar-charts)
- [Financial Charts](#financial-charts)
- [Specialty Charts](#specialty-charts)
- [Choosing the Right Chart Type](#choosing-the-right-chart-type)
- [Type-Specific Configurations](#type-specific-configurations)

---

## Overview

Syncfusion React Charts supports 20+ chart types, each optimized for different data visualization scenarios. Chart type is specified via the `type` prop on `SeriesDirective`.

**Common Import Pattern:**
```jsx
import { ChartComponent, SeriesDirective, LineSeries, ColumnSeries, AreaSeries, BarSeries, ScatterSeries, BubbleSeries, ... } from '@syncfusion/ej2-react-charts';
```

Each chart type must be:
1. Imported from the package
2. Injected via `<Inject services={[...]}>`
3. Specified as `type='TypeName'` on the series

---

## Cartesian Charts

Cartesian charts use X and Y axes for data positioning. Most common in business analytics.

### Line Chart
**When to use:** Trends, time-series data, continuous values

```jsx
import { LineSeries } from '@syncfusion/ej2-react-charts';

<SeriesDirective
  dataSource={data}
  xName='date'
  yName='value'
  type='Line'
/>
```

**Properties:**
- `width`: Line thickness (default 2)
- `dashArray`: Dash pattern (e.g., '5,3' for dashed)
- `marker`: Point marker config
- `fill`: Line color

### Column Chart
**When to use:** Comparing categories, discrete values

```jsx
<SeriesDirective
  dataSource={data}
  xName='category'
  yName='value'
  type='Column'
/>
```

**Properties:**
- `cornerRadius`: Round corners (0-50)
- `columnSpacing`: Gap between columns (0-1, default 0)
- `border`: Border styling
- `fill`: Column color

### Bar Chart
**When to use:** Comparing categories horizontally (better for long labels)

```jsx
<ChartComponent
  primaryXAxis={{ valueType: 'Category' }}
  primaryYAxis={{ valueType: 'Double' }}
>
  <SeriesDirective type='Bar' ... />
</ChartComponent>
```

**Key difference from Column:** Axes are reversed (categories on Y-axis)

### Area Chart
**When to use:** Cumulative trends, magnitude emphasis

```jsx
<SeriesDirective
  dataSource={data}
  xName='month'
  yName='value'
  type='Area'
/>
```

**Properties:**
- `opacity`: Fill transparency (0-1)
- `drawType`: Smooth or straight segments

### Scatter Chart
**When to use:** Correlations, distribution patterns

```jsx
<SeriesDirective
  dataSource={data}
  xName='x'
  yName='y'
  type='Scatter'
/>
```

**Requires `Numeric` axes:**
```jsx
primaryXAxis={{ valueType: 'Double' }}
primaryYAxis={{ valueType: 'Double' }}
```

### Bubble Chart
**When to use:** Trivariate data (3 dimensions)

```jsx
import { BubbleSeries } from '@syncfusion/ej2-react-charts';

<SeriesDirective
  dataSource={data}
  xName='x'
  yName='y'
  size='size'
  type='Bubble'
/>
```

Data must include `size` property for bubble radius.

### Step Line Chart
**When to use:** Stepped values, discrete state changes

```jsx
<SeriesDirective type='StepLine' ... />
```

---

## Polar and Radar Charts

Non-Cartesian charts for directional data and multi-dimensional comparisons.

### Polar Chart
**When to use:** Directional or angular data

```jsx
import { PolarSeries } from '@syncfusion/ej2-react-charts';

<ChartComponent chartArea={{ border: { width: 0 } }}>
  <SeriesDirective type='Polar' drawType='Column' ... />
</ChartComponent>
```

Available draw types: Line, Column, Area, Spline, RangeColumn

### Radar Chart
**When to use:** Skill or characteristic comparison across multiple axes

```jsx
import { RadarSeries } from '@syncfusion/ej2-react-charts';

<SeriesDirective type='Radar' drawType='Line' ... />
```

Similar to Polar but drawn with straight lines connecting points.

---

## Financial Charts

Specialized charts for stock market and financial data analysis.

### Candlestick Chart
**When to use:** OHLC data (Open, High, Low, Close)

```jsx
import { CandleSeries } from '@syncfusion/ej2-react-charts';

<SeriesDirective
  dataSource={data}
  xName='date'
  low='low'
  high='high'
  open='open'
  close='close'
  type='Candle'
/>
```

Data properties: `low`, `high`, `open`, `close`

### HLOC Chart
**When to use:** High-Low-Open-Close visualization

```jsx
<SeriesDirective type='HighLowOpenClose' ... />
```

Similar data structure to Candlestick but different visual representation.

### HiLo Chart (High-Low)
**When to use:** Simple high-low range visualization

```jsx
<SeriesDirective type='HiLo' ... />
```

---

## Specialty Charts

### Box and Whisker Plot
**When to use:** Statistical distribution, quartiles

```jsx
import { BoxAndWhiskerSeries } from '@syncfusion/ej2-react-charts';

<SeriesDirective type='BoxAndWhisker' ... />
```

### Waterfall Chart
**When to use:** Cumulative effect visualization

```jsx
import { WaterfallSeries } from '@syncfusion/ej2-react-charts';

<SeriesDirective type='Waterfall' ... />
```

### Histogram
**When to use:** Frequency distribution

```jsx
import { HistogramSeries } from '@syncfusion/ej2-react-charts';

<SeriesDirective type='Histogram' ... />
```

### Error Bar Chart
**When to use:** Displaying uncertainty ranges

```jsx
<SeriesDirective
  type='Column'
  errorBar={{ visible: true, type: 'StandardDeviation' }}
  ...
/>
```

### Pareto Chart
**When to use:** 80/20 analysis, Pareto principle visualization

```jsx
import { ParetoSeries } from '@syncfusion/ej2-react-charts';

<SeriesDirective type='Pareto' ... />
```

---

## Choosing the Right Chart Type

### Decision Matrix

| Need | Chart Type | Why |
|------|-----------|-----|
| Show trend over time | Line, Area | Continuous representation |
| Compare categories | Column, Bar | Clear discrete comparison |
| Show part-to-whole | Pie, Doughnut | Proportional visualization |
| Correlations | Scatter, Bubble | XY positioning reveals patterns |
| Directional data | Polar, Radar | Angular representation |
| Stock prices | Candlestick, HLOC | Shows open, high, low, close |
| Statistical analysis | Box-Whisker, Histogram | Distribution visualization |
| Cumulative change | Waterfall, Area | Shows running totals |
| Multi-axis comparison | Radar | Compare across many dimensions |

### Real-World Examples

**Sales Dashboard:**
- Revenue trend: Line or Area
- Sales by region: Column or Bar
- Top performers: Pie or Doughnut

**Financial Dashboard:**
- Stock prices: Candlestick
- Portfolio allocation: Pie
- Moving average: Line overlaid on candlestick

**Analytics Dashboard:**
- Page views over time: Line
- Traffic by source: Column or Bar
- User demographics: Radar or multi-axis

---

## Type-Specific Configurations

### Stacked Charts

Stack multiple series on top of each other:

```jsx
// Column series stacking
<SeriesDirective
  dataSource={q1Data}
  type='StackingColumn'
/>
<SeriesDirective
  dataSource={q2Data}
  type='StackingColumn'
/>
```

Available: StackingColumn, StackingBar, StackingArea, StackingLine

### 100% Stacked Charts

Show proportions as percentages:

```jsx
<SeriesDirective type='StackingColumn100' />
```

Available: StackingColumn100, StackingBar100, StackingArea100

### Range Charts

Show min-max ranges:

```jsx
<SeriesDirective
  dataSource={data}
  xName='x'
  high='high'
  low='low'
  type='RangeColumn'
/>
```

Data must include `high` and `low` properties.

Available: RangeColumn, RangeArea, RangeStepArea

### Spline Charts

Smooth curves instead of straight lines:

```jsx
<SeriesDirective type='Spline' /> // Line with smooth curves
<SeriesDirective type='SplineArea' /> // Area with smooth curves
<SeriesDirective type='SplineRangeArea' /> // Range area with smooth curves
```

---

## Performance Considerations

- **Many data points (1000+)?** Use Line chart over Scatter
- **Real-time updates?** Consider virtual scrolling with zooming
- **Large series count (10+)?** Use Column chart over Pie
- **Mobile viewing?** Prefer Column/Bar over dense Scatter

---

## Common Configuration Across All Types

```jsx
<SeriesDirective
  type='Column'
  fill='#3B82F6'
  border={{ width: 1, color: '#1E40AF' }}
  opacity={0.85}
  marker={{
    visible: true,
    shape: 'Circle',
    width: 8,
    height: 8
  }}
/>
```
