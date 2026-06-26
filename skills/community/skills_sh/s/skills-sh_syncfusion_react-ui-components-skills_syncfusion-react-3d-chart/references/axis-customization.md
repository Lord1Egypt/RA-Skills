# Advanced Axis Customization

## Table of contents
- [Axis Crossing](axis-customization.md#axis-crossing)
- [Multiple Axes](axis-customization.md#multiple-axes)
- [Axis Line Break](axis-customization.md#axis-line-break)
- [Custom Label Content](axis-customization.md#custom-label-content)
  - [Format Based on Value](axis-customization.md#format-based-on-value)
- [Axis Visibility Control](axis-customization.md#axis-visibility-control)
  - [Hide Axis Completely](axis-customization.md#hide-axis-completely)
  - [Hide Axis Line Only](axis-customization.md#hide-axis-line-only)
  - [Hide Grid Lines](axis-customization.md#hide-grid-lines)
- [Inversed Axis](axis-customization.md#inversed-axis)
- [Edge Label Placement](axis-customization.md#edge-label-placement)
- [Complete Advanced Example](axis-customization.md#complete-advanced-example)
- [Common Issues](axis-customization.md#common-issues)

This guide covers advanced axis customization features for precise control over axis behavior and appearance.

## Axis Crossing

Control where axes intersect each other:

```tsx
function AxisCrossing() {
  const data = [
    { x: 'A', y: -10 },
    { x: 'B', y: 15 },
    { x: 'C', y: -5 },
    { x: 'D', y: 20 },
    { x: 'E', y: 8 }
  ];

  return (
    <Chart3DComponent
      id='chart'
      primaryXAxis={{
        valueType: 'Category',
        crossesAt: 0  // X-axis crosses Y-axis at 0
      }}
      primaryYAxis={{
        crossesAt: 'B',  // Y-axis crosses X-axis at category 'B'
        minimum: -15,
        maximum: 25,
        interval: 5
      }}
    >
      <Inject services={[ColumnSeries3D, Category3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          type='Column'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

**Use cases:**
- Show positive and negative values with axis at zero
- Center axis for better data visualization
- Create custom chart layouts

## Multiple Axes

Add multiple Y-axes for different value scales:

```tsx
function MultipleAxesChart() {
  const data = [
    { month: 'Jan', temperature: 5, rainfall: 78, humidity: 65 },
    { month: 'Feb', temperature: 8, rainfall: 65, humidity: 68 },
    { month: 'Mar', temperature: 12, rainfall: 55, humidity: 62 },
    { month: 'Apr', temperature: 18, rainfall: 45, humidity: 58 },
    { month: 'May', temperature: 23, rainfall: 38, humidity: 55 },
    { month: 'Jun', temperature: 28, rainfall: 25, humidity: 52 }
  ];

  return (
    <Chart3DComponent
      id='multiple-axes'
      title='Weather Data with Multiple Axes'
      primaryXAxis={{
        valueType: 'Category',
        title: 'Month'
      }}
      primaryYAxis={{
        name: 'yAxis1',
        title: 'Temperature (°C)',
        minimum: 0,
        maximum: 35,
        interval: 5,
        labelFormat: '{value}°C',
        lineStyle: { width: 2, color: '#E94649' }
      }}
      axes={[
        {
          name: 'yAxis2',
          opposedPosition: true,
          title: 'Rainfall (mm)',
          minimum: 0,
          maximum: 100,
          interval: 20,
          labelFormat: '{value}mm',
          lineStyle: { width: 2, color: '#4472C4' }
        },
        {
          name: 'yAxis3',
          opposedPosition: true,
          title: 'Humidity (%)',
          minimum: 0,
          maximum: 100,
          interval: 20,
          labelFormat: '{value}%',
          lineStyle: { width: 2, color: '#70AD47' },
          rowIndex: 0,
          span: 1
        }
      ]}
    >
      <Inject services={[ColumnSeries3D, Category3D, Legend3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='month'
          yName='temperature'
          type='Column'
          name='Temperature'
          yAxisName='yAxis1'
        />
        <Chart3DSeriesDirective
          dataSource={data}
          xName='month'
          yName='rainfall'
          type='Column'
          name='Rainfall'
          yAxisName='yAxis2'
        />
        <Chart3DSeriesDirective
          dataSource={data}
          xName='month'
          yName='humidity'
          type='Column'
          name='Humidity'
          yAxisName='yAxis3'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

**Key points:**
- Name each axis with unique `name` property
- Reference axis in series using `yAxisName`
- Use `opposedPosition: true` to place on right side
- Match axis `lineStyle.color` with series color for clarity

## Axis Line Break

Not directly supported in 3D charts, but can simulate with range adjustment:

```tsx
function SimulatedAxisBreak() {
  const data = [
    { x: 'A', y: 10 },
    { x: 'B', y: 15 },
    { x: 'C', y: 100 },  // Outlier
    { x: 'D', y: 12 },
    { x: 'E', y: 18 }
  ];

  return (
    <Chart3DComponent
      id='chart'
      primaryXAxis={{ valueType: 'Category' }}
      primaryYAxis={{
        minimum: 0,
        maximum: 25,  // Limit range to exclude outlier
        interval: 5
      }}
    >
      <Inject services={[ColumnSeries3D, Category3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          type='Column'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

**Alternative:** Filter outliers or use logarithmic scale for wide ranges.

## Custom Label Content

Customize axis labels dynamically:

```tsx
function CustomLabels() {
  const data = [
    { value: 1, sales: 45 },
    { value: 2, sales: 55 },
    { value: 3, sales: 38 },
    { value: 4, sales: 65 }
  ];

  const axisLabelRender = (args: any) => {
    const labels = ['Q1', 'Q2', 'Q3', 'Q4'];
  };

  return (
    <Chart3DComponent
      id='custom-labels'
      primaryXAxis={{
        valueType: 'Double',
        minimum: 0.5,
        maximum: 4.5,
        interval: 1
      }}
      axisLabelRender={axisLabelRender}
    >
      <Inject services={[ColumnSeries3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='value'
          yName='sales'
          type='Column'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

### Format Based on Value

```tsx
const axisLabelRender = (args: any) => {
  if (args.axis.name === 'primaryYAxis') {
    if (args.value >= 1000000) {
      args.text = (args.value / 1000000).toFixed(1) + 'M';
    } else if (args.value >= 1000) {
      args.text = (args.value / 1000).toFixed(1) + 'K';
    }
  }
};
```

## Axis Visibility Control

### Hide Axis Completely

```tsx
<Chart3DComponent
  primaryYAxis={{
    visible: false  // Hide entire Y-axis including labels
  }}
>
  {/* Series */}
</Chart3DComponent>
```

### Hide Axis Line Only

```tsx
<Chart3DComponent
  primaryYAxis={{
    lineStyle: { width: 0 },  // Hide axis line
    majorTickLines: { width: 0 },  // Hide tick marks
    // Labels still visible
  }}
>
  {/* Series */}
</Chart3DComponent>
```

### Hide Grid Lines

```tsx
<Chart3DComponent
  primaryYAxis={{
    majorGridLines: { width: 0 },
    minorGridLines: { width: 0 }
  }}
>
  {/* Series */}
</Chart3DComponent>
```

## Inversed Axis

Reverse axis direction:

```tsx
function InversedAxisChart() {
  const rankingData = [
    { team: 'Team A', rank: 1 },
    { team: 'Team B', rank: 2 },
    { team: 'Team C', rank: 3 },
    { team: 'Team D', rank: 4 },
    { team: 'Team E', rank: 5 }
  ];

  return (
    <Chart3DComponent
      id='inversed-chart'
      title='Team Rankings (Lower is Better)'
      primaryXAxis={{
        valueType: 'Category'
      }}
      primaryYAxis={{
        isInversed: true,  // Reverse Y-axis
        title: 'Rank',
        minimum: 0,
        maximum: 6,
        interval: 1
      }}
    >
      <Inject services={[ColumnSeries3D, Category3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={rankingData}
          xName='team'
          yName='rank'
          type='Column'
          name='Rank'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

**Use cases:**
- Rankings (where 1 is best, higher at top)
- Depth charts (deeper values at bottom)
- Temperature scales (certain contexts)

## Edge Label Placement

Handle labels at chart edges:

```tsx
<Chart3DComponent
  primaryXAxis={{
    valueType: 'Category',
    edgeLabelPlacement: 'Shift'  // Options: 'None', 'Shift', 'Hide'
  }}
>
  {/* Series */}
</Chart3DComponent>
```

**Options:**
- `None`: Default, may overlap edges
- `Shift`: Move inside chart area
- `Hide`: Hide edge labels entirely

## Complete Advanced Example

```tsx
function AdvancedAxisCustomization() {
  const data = [
    { month: 'Jan', actual: 45, target: 50 },
    { month: 'Feb', actual: 55, target: 50 },
    { month: 'Mar', actual: 38, target: 50 },
    { month: 'Apr', actual: 65, target: 50 },
    { month: 'May', actual: 72, target: 50 },
    { month: 'Jun', actual: 68, target: 50 }
  ];

  return (
    <Chart3DComponent
      id='advanced-axis'
      title='Sales Performance vs Target'
      primaryXAxis={{
        valueType: 'Category',
        title: 'Month',
        majorGridLines: { width: 1, color: '#E0E0E0' },
        edgeLabelPlacement: 'Shift'
      }}
      primaryYAxis={{
        title: 'Sales',
        minimum: 0,
        maximum: 100,
        interval: 20,
        labelFormat: '{value}K'
      }}
      rotation={7}
      tilt={10}
    >
      <Inject services={[ColumnSeries3D, Category3D, Legend3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='month'
          yName='actual'
          type='Column'
          name='Actual Sales'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

## Common Issues

**Multiple axes not showing:**
- Ensure each axis has unique `name` property
- Verify series `yAxisName` matches axis `name`
- Check `opposedPosition` for positioning

**Strip lines not visible:**
- Verify `start` value is within axis range
- Check `opacity` is > 0
- Ensure `color` is valid

**Custom labels not applying:**
- Use `axisLabelRender` event correctly
- Modify `args.text`, not `args.value`
- Check axis name in event if targeting specific axis

---

See also: [api-reference.md](api-reference.md) | [usage-example.md](usage-example.md)
