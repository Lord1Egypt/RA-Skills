# Data Labels, Legend, and Tooltip

## Table of contents
- [Data Labels](data-labels-legend-tooltip.md#data-labels)
  - [Basic Data Labels](data-labels-legend-tooltip.md#basic-data-labels)
  - [Data Label Position](data-labels-legend-tooltip.md#data-label-position)
  - [Data Label Styling](data-labels-legend-tooltip.md#data-label-styling)
  - [Custom Data Label Format](data-labels-legend-tooltip.md#custom-data-label-format)
  - [Data Label with Percentage](data-labels-legend-tooltip.md#data-label-with-percentage)
- [Legend Configuration](data-labels-legend-tooltip.md#legend-configuration)
  - [Basic Legend](data-labels-legend-tooltip.md#basic-legend)
  - [Legend Position](data-labels-legend-tooltip.md#legend-position)
  - [Legend Alignment](data-labels-legend-tooltip.md#legend-alignment)
  - [Legend Styling](data-labels-legend-tooltip.md#legend-styling)
  - [Hide Specific Series icon from Legend](data-labels-legend-tooltip.md#hide-specific-series-icon-from-legend)
- [Tooltip Customization](data-labels-legend-tooltip.md#tooltip-customization)
  - [Basic Tooltip](data-labels-legend-tooltip.md#basic-tooltip)
  - [Tooltip Format](data-labels-legend-tooltip.md#tooltip-format)
  - [Tooltip Styling](data-labels-legend-tooltip.md#tooltip-styling)
  - [Custom Tooltip Template](data-labels-legend-tooltip.md#custom-tooltip-template)
  - [Shared Tooltip (Multiple Series)](data-labels-legend-tooltip.md#shared-tooltip-multiple-series)
- [Combining All Three](data-labels-legend-tooltip.md#combining-all-three)
- [Best Practices](data-labels-legend-tooltip.md#best-practices)
- [Common Issues](data-labels-legend-tooltip.md#common-issues)

Visual enhancements that improve chart readability and user interaction.

## Data Labels

### Basic Data Labels

```tsx
import { Chart3DComponent, Chart3DSeriesCollectionDirective, Chart3DSeriesDirective, Inject, ColumnSeries3D, Category3D, DataLabel3D } from '@syncfusion/ej2-react-charts';

function DataLabelsChart() {
  const data = [
    { month: 'Jan', sales: 35 },
    { month: 'Feb', sales: 42 },
    { month: 'Mar', sales: 38 },
    { month: 'Apr', sales: 48 }
  ];

  return (
    <Chart3DComponent
      id='chart'
      primaryXAxis={{ valueType: 'Category' }}
    >
      <Inject services={[ColumnSeries3D, Category3D, DataLabel3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='month'
          yName='sales'
          type='Column'
          dataLabel={{ visible: true }}
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

**Key requirement:** Must inject `DataLabel3D` service for data labels to work.

### Data Label Position

```tsx
<Chart3DSeriesDirective
  dataSource={data}
  xName='month'
  yName='sales'
  type='Column'
  dataLabel={{ visible: true, position: 'Top' }}
/>
```

**Positions:**
- `Top`: Above the data point
- `Middle`: Center of the column/bar
- `Bottom`: Below/at base
- `Outer`: Outside the chart area
- `Auto`: Automatically determined

### Data Label Styling

```tsx
<Chart3DSeriesDirective
  dataSource={data}
  xName="month"
  yName="sales"
  type="Column"
  dataLabel={{
    visible: true,
    position: 'Top',
    font: {
      fontFamily: 'Segoe UI',
      size: '12px',
      fontWeight: '600',
      color: '#333',
    },
    fill: '#FFF', // Background color
    border: {
      width: 1,
      color: '#DDD',
    },
    margin: {
      left: 5,
      right: 5,
      top: 5,
      bottom: 5,
    },
  }}
/>
```

### Custom Data Label Format

```tsx
<Chart3DSeriesDirective
  dataSource={data}
  xName="month"
  yName="sales"
  type="Column"
  dataLabel={{
    visible: true,
    position: 'Top',
    template: '<div style="background: #333; color: #FFF; padding: 5px; border-radius: 3px;">${point.y}K</div>'
  }}
/>
```

### Data Label with Percentage

For stacked charts showing percentage:

```tsx
<Chart3DSeriesDirective
  dataSource={data}
  xName="month"
  yName="sales"
  type="Column"
  dataLabel={{
    visible: true,
    position: 'Top',
    format: '{value}%',
    font: { color: 'red', fontWeight: 'bold' }
  }}
/>
```

## Legend Configuration

### Basic Legend

```tsx
import { Chart3DComponent, Chart3DSeriesCollectionDirective, Chart3DSeriesDirective, Inject, ColumnSeries3D, Category3D, Legend3D } from '@syncfusion/ej2-react-charts';

function LegendChart() {
  const data = [
    { month: 'Jan', actual: 35, target: 40 },
    { month: 'Feb', actual: 42, target: 40 },
    { month: 'Mar', actual: 38, target: 40 }
  ];

  return (
    <Chart3DComponent
      id='chart'
      primaryXAxis={{ valueType: 'Category' }}
      legendSettings={{
        visible: true  // Enable legend (default)
      }}
    >
      <Inject services={[ColumnSeries3D, Category3D, Legend3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='month'
          yName='actual'
          type='Column'
          name='Actual'
        />
        <Chart3DSeriesDirective
          dataSource={data}
          xName='month'
          yName='target'
          type='Column'
          name='Target'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

**Key requirement:** Must inject `Legend3D` service for legend to work.

### Legend Position

```tsx
<Chart3DComponent
  primaryXAxis={{ valueType: 'Category' }}
  legendSettings={{
    visible: true,
    position: 'Bottom'  // Options: 'Top', 'Bottom', 'Left', 'Right', 'Custom'
  }}
>
  {/* Series */}
</Chart3DComponent>
```

### Legend Alignment

```tsx
<Chart3DComponent
  primaryXAxis={{ valueType: 'Category' }}
  legendSettings={{
    visible: true,
    position: 'Bottom',
    alignment: 'Center'  // Options: 'Near', 'Center', 'Far'
  }}
>
  {/* Series */}
</Chart3DComponent>
```

### Legend Styling

```tsx
<Chart3DComponent
  primaryXAxis={{ valueType: 'Category' }}
  legendSettings={{
    visible: true,
    position: 'Right',
    background: '#F9F9F9',
    border: {
      width: 1,
      color: '#DDD'
    },
    textStyle: {
      fontFamily: 'Segoe UI',
      size: '12px',
      fontWeight: '500',
      color: '#333'
    },
    padding: 10,
    shapePadding: 8,
    shapeHeight: 12,
    shapeWidth: 12
  }}
>
  {/* Series */}
</Chart3DComponent>
```

### Hide Specific Series icon from Legend

```tsx
<Chart3DSeriesDirective
  dataSource={data}
  xName='x'
  yName='y'
  type='Column'
  name='Hidden Series'
  legendShape= 'None'  // Hide this icon of series from legend
/>
```

## Tooltip Customization

### Basic Tooltip

```tsx
import { Chart3DComponent, Chart3DSeriesCollectionDirective, Chart3DSeriesDirective, Inject, ColumnSeries3D, Category3D, Tooltip3D } from '@syncfusion/ej2-react-charts';

function TooltipChart() {
  const data = [
    { month: 'Jan', sales: 35 },
    { month: 'Feb', sales: 42 },
    { month: 'Mar', sales: 38 }
  ];

  return (
    <Chart3DComponent
      id='chart'
      primaryXAxis={{ valueType: 'Category' }}
      tooltip={{
        enable: true  // Enable tooltip
      }}
    >
      <Inject services={[ColumnSeries3D, Category3D, Tooltip3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='month'
          yName='sales'
          type='Column'
          name='Sales'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

**Key requirement:** Must inject `Tooltip3D` service for tooltips to work.

### Tooltip Format

```tsx
<Chart3DComponent
  tooltip={{
    enable: true,
    format: '${series.name}: ${point.y}K'
  }}
>
  {/* Series */}
</Chart3DComponent>
```

**Available tokens:**
- `${point.x}`: X-axis value
- `${point.y}`: Y-axis value
- `${series.name}`: Series name
- `${point.tooltip}`: Custom tooltip text from data

### Tooltip Styling

```tsx
<Chart3DComponent
  tooltip={{
    enable: true,
    fill: '#333',
    textStyle: {
      color: '#FFF',
      fontFamily: 'Segoe UI',
      size: '12px'
    },
    border: {
      width: 2,
      color: '#FFF'
    },
    opacity: 0.9
  }}
>
  {/* Series */}
</Chart3DComponent>
```

### Custom Tooltip Template

```tsx
<Chart3DComponent
  tooltip={{
    enable: true,
    template: '<div style="background: #333; color: #FFF; padding: 10px; border-radius: 5px;"><b>${x}</b><br/>Sales: <b>${y}K</b><br/>Growth: <b>+12%</b></div>'
  }}
>
  {/* Series */}
</Chart3DComponent>
```

### Shared Tooltip (Multiple Series)

```tsx
<Chart3DComponent
  tooltip={{
    enable: true,
    shared: true,  // Show all series values in one tooltip
    format: '<b>${point.x}</b><br/>${series.name}: ${point.y}'
  }}
>
  {/* Multiple series */}
</Chart3DComponent>
```

## Combining All Three

```tsx
import {
  Chart3DComponent,
  Chart3DSeriesCollectionDirective,
  Chart3DSeriesDirective,
  Inject,
  Category3D,
  ColumnSeries3D,
  DataLabel3D,
  Legend3D,
  Tooltip3D,
} from '@syncfusion/ej2-react-charts';
import * as React from 'react';
import { createRoot } from 'react-dom/client';

function App() {
  const salesData = [
    { quarter: 'Q1', actual: 45, target: 50, region: 'North' },
    { quarter: 'Q2', actual: 55, target: 50, region: 'North' },
    { quarter: 'Q3', actual: 48, target: 50, region: 'North' },
    { quarter: 'Q4', actual: 62, target: 50, region: 'North' },
  ];

  return (
    <Chart3DComponent
      id="comprehensive-chart"
      title="Quarterly Sales Performance"
      primaryXAxis={{
        valueType: 'Category',
        title: 'Quarter',
      }}
      primaryYAxis={{
        title: 'Sales ($K)',
        minimum: 0,
        maximum: 70,
        interval: 10,
      }}
      legendSettings={{
        visible: true,
        position: 'Bottom',
        alignment: 'Center',
        textStyle: {
          fontFamily: 'Segoe UI',
          size: '12px',
        },
        shapeHeight: 12,
        shapeWidth: 12,
      }}
      tooltip={{
        enable: true,
        shared: true,
        format: '<b>${point.x}</b><br/>${series.name}: <b>${point.y}K</b>',
        fill: '#333',
        textStyle: {
          color: '#FFF',
          size: '12px',
        },
        border: { width: 2, color: '#FFF' },
      }}
      rotation={7}
      tilt={10}
    >
      <Inject
        services={[
          ColumnSeries3D,
          Category3D,
          Legend3D,
          DataLabel3D,
          Tooltip3D,
        ]}
      />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={salesData}
          xName="quarter"
          yName="actual"
          type="Column"
          name="Actual Sales"
          dataLabel={{
            visible: true,
            position: 'Top',
            format: '{value}K',
            font: {
              fontWeight: '600',
              size: '11px',
              color: '#2C5F2D',
            },
          }}
        />
        <Chart3DSeriesDirective
          dataSource={salesData}
          xName="quarter"
          yName="target"
          type="Column"
          name="Target"
          dataLabel={{
            visible: true,
            position: 'Top',
            format: '{value}K',
            font: {
              fontWeight: '600',
              size: '11px',
              color: '#8B4513',
            },
          }}
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
export default App;
createRoot(document.getElementById('charts')).render(<App />);
```

## Best Practices

**Data labels:**
- Use for small datasets (<10 points) to avoid clutter
- Position at 'Top' for column charts, 'Outer' for bars
- Use contrasting colors for readability
- Consider hiding when chart has many series

**Legend:**
- Place 'Bottom' or 'Right' for most use cases
- Use 'Top' sparingly (interferes with title)
- Keep series names concise (<20 characters)
- Hide legend if only one series

**Tooltips:**
- Always enable for interactive charts
- Use shared tooltip for multi-series comparison
- Include units in format (K, %, etc.)
- Keep template HTML simple for performance

**Combining:**
- Data labels + tooltip: Use labels for key points, tooltip for details
- Legend + tooltip: Essential for multi-series charts
- All three: Only when all serve distinct purposes

## Common Issues

**Data labels overlapping:**
- Reduce number of data points
- Use `position: 'Outer'` or 'Auto'
- Adjust `font.size` to smaller value
- Consider hiding labels, using tooltip instead

**Legend not showing:**
- Ensure `Legend3D` service is injected
- Check `legendSettings.visible` is true
- Verify series have `name` property
- Check legend position doesn't place it outside viewport

**Tooltip not appearing:**
- Inject `Tooltip3D` service
- Set `tooltip.enable: true`
- Ensure hovering over data points (not empty space)
- Check tooltip not blocked by CSS z-index issues

**Custom templates not rendering:**
- Use proper HTML syntax in template string
- Escape special characters if needed
- Test with simple template first, then add complexity

---

See also: [api-reference.md](api-reference.md) | [usage-example.md](usage-example.md)
