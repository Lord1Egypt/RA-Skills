# Multiple Panes Layout

Multiple panes allow you to divide the chart area into rows and columns, enabling different series to display in separate chart regions while sharing axes or having independent axes.

## Table of contents

- [Basic Multiple Rows](multiple-panes.md#basic-multiple-rows)
- [Row Configuration](multiple-panes.md#row-configuration)
  - [Equal Height Rows](multiple-panes.md#equal-height-rows)
  - [Custom Height Distribution](multiple-panes.md#custom-height-distribution)
  - [Row Borders](multiple-panes.md#row-borders)
- [Assigning Series to Rows](multiple-panes.md#assigning-series-to-rows)
- [Shared Axes Across Rows](multiple-panes.md#shared-axes-across-rows)
- [Spanning Multiple Rows](multiple-panes.md#spanning-multiple-rows)
- [Complete Multiple Panes Example](multiple-panes.md#complete-multiple-panes-example)
- [Use Cases](multiple-panes.md#use-cases)
- [Best Practices](multiple-panes.md#best-practices)
- [Common Issues](multiple-panes.md#common-issues)

## Basic Multiple Rows

```tsx
import { Chart3DComponent, Chart3DSeriesCollectionDirective, Chart3DSeriesDirective, Inject, ColumnSeries3D, Category3D } from '@syncfusion/ej2-react-charts';

function MultipleRowsChart() {
  const salesData = [
    { month: 'Jan', sales: 35, profit: 12 },
    { month: 'Feb', sales: 42, profit: 15 },
    { month: 'Mar', sales: 38, profit: 11 },
    { month: 'Apr', sales: 48, profit: 18 }
  ];

  return (
    <Chart3DComponent
      id='chart'
      primaryXAxis={{
        valueType: 'Category'
      }}
      rows={[
        { height: '50%' },  // Top row
        { height: '50%' }   // Bottom row
      ]}
      axes={[
        {
          name: 'yAxis1',
          rowIndex: 0,
          title: 'Sales',
          opposedPosition: true
        },
        {
          name: 'yAxis2',
          rowIndex: 1,
          title: 'Profit'
        }
      ]}
    >
      <Inject services={[ColumnSeries3D, Category3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={salesData}
          xName='month'
          yName='sales'
          type='Column'
          name='Sales'
          yAxisName='yAxis1'
        />
        <Chart3DSeriesDirective
          dataSource={salesData}
          xName='month'
          yName='profit'
          type='Column'
          name='Profit'
          yAxisName='yAxis2'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

## Row Configuration

### Equal Height Rows

```tsx
<Chart3DComponent
  rows={[
    { height: '33%' },
    { height: '33%' },
    { height: '34%' }
  ]}
>
  {/* Three rows with equal height */}
</Chart3DComponent>
```

### Custom Height Distribution

```tsx
<Chart3DComponent
  rows={[
    { height: '60%' },  // Main chart takes 60%
    { height: '40%' }   // Secondary chart takes 40%
  ]}
>
  {/* Two rows with different heights */}
</Chart3DComponent>
```

## Assigning Series to Rows

Use `yAxisName` and axis `rowIndex` to control placement:

```tsx
function ThreeRowChart() {
  const data = [
    { x: 'A', revenue: 120, cost: 80, profit: 40 },
    { x: 'B', revenue: 150, cost: 95, profit: 55 },
    { x: 'C', revenue: 135, cost: 88, profit: 47 }
  ];

  return (
    <Chart3DComponent
      id='three-row'
      primaryXAxis={{ valueType: 'Category' }}
      rows={[
        { height: '40%' },
        { height: '30%' },
        { height: '30%' }
      ]}
      axes={[
        {
          name: 'yAxis1',
          rowIndex: 0,
          title: 'Revenue',
          minimum: 0,
          maximum: 200
        },
        {
          name: 'yAxis2',
          rowIndex: 1,
          title: 'Cost',
          minimum: 0,
          maximum: 150,
          opposedPosition: true
        },
        {
          name: 'yAxis3',
          rowIndex: 2,
          title: 'Profit',
          minimum: 0,
          maximum: 80
        }
      ]}
    >
      <Inject services={[ColumnSeries3D, Category3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='x'
          yName='revenue'
          type='Column'
          name='Revenue'
          yAxisName='yAxis1'
        />
        <Chart3DSeriesDirective
          dataSource={data}
          xName='x'
          yName='cost'
          type='Column'
          name='Cost'
          yAxisName='yAxis2'
        />
        <Chart3DSeriesDirective
          dataSource={data}
          xName='x'
          yName='profit'
          type='Column'
          name='Profit'
          yAxisName='yAxis3'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

## Shared Axes Across Rows

Multiple series can share the same row:

```tsx
function SharedRowChart() {
  const data = [
    { month: 'Jan', actual: 35, target: 40 },
    { month: 'Feb', actual: 42, target: 40 },
    { month: 'Mar', actual: 38, target: 40 }
  ];

  return (
    <Chart3DComponent
      id='shared-row'
      primaryXAxis={{ valueType: 'Category' }}
      rows={[{ height: '100%' }]}
      axes={[
        {
          name: 'yAxis1',
          rowIndex: 0,
          title: 'Sales',
          opposedPosition: true
        }
      ]}
    >
      <Inject services={[ColumnSeries3D, Category3D, Legend3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='month'
          yName='actual'
          type='Column'
          name='Actual'
          yAxisName='yAxis1'
        />
        <Chart3DSeriesDirective
          dataSource={data}
          xName='month'
          yName='target'
          type='Column'
          name='Target'
          yAxisName='yAxis1'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

## Spanning Multiple Rows

An axis can span multiple rows:

```tsx
<Chart3DComponent
  rows={[
    { height: '50%' },
    { height: '50%' }
  ]}
  axes={[
    {
      name: 'yAxis1',
      rowIndex: 0,
      span: 2,  // Spans both rows
      title: 'Shared Axis'
    }
  ]}
>
  {/* Series in different rows but sharing same axis */}
</Chart3DComponent>
```

## Complete Multiple Panes Example

```tsx
import { Chart3DComponent, Chart3DSeriesCollectionDirective, Chart3DSeriesDirective, Inject, ColumnSeries3D, Category3D, Export3D, Legend3D } from '@syncfusion/ej2-react-charts';
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import React, { useRef } from 'react';

function MultiplePane() {
  const financialData = [
    { quarter: 'Q1', revenue: 120, expenses: 80, netIncome: 40 },
    { quarter: 'Q2', revenue: 150, expenses: 95, netIncome: 55 },
    { quarter: 'Q3', revenue: 135, expenses: 88, netIncome: 47 },
    { quarter: 'Q4', revenue: 165, expenses: 102, netIncome: 63 }
  ];

  return (
    <Chart3DComponent
      id='multi-pane-financial'
      title='Quarterly Financial Performance'
      primaryXAxis={{
        valueType: 'Category',
        title: 'Quarter'
      }}
      rows={[
        {
          height: '40%',
          border: { width: 1, color: '#E0E0E0' }
        },
        {
          height: '30%',
          border: { width: 1, color: '#E0E0E0' }
        },
        {
          height: '30%',
          border: { width: 1, color: '#E0E0E0' }
        }
      ]}
      axes={[
        {
          name: 'revenueAxis',
          rowIndex: 0,
          title: 'Revenue ($K)',
          minimum: 0,
          maximum: 200,
          interval: 50,
          labelFormat: '${value}K',
          majorGridLines: { width: 1, color: '#E0E0E0' }
        },
        {
          name: 'expenseAxis',
          rowIndex: 1,
          title: 'Expenses ($K)',
          minimum: 0,
          maximum: 150,
          interval: 50,
          labelFormat: '${value}K',
          majorGridLines: { width: 1, color: '#E0E0E0' },
          opposedPosition: true
        },
        {
          name: 'incomeAxis',
          rowIndex: 2,
          title: 'Net Income ($K)',
          minimum: 0,
          maximum: 80,
          interval: 20,
          labelFormat: '${value}K',
          majorGridLines: { width: 1, color: '#E0E0E0' }
        }
      ]}
      rotation={7}
      tilt={10}
    >
      <Inject services={[ColumnSeries3D, Category3D, Legend3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={financialData}
          xName='quarter'
          yName='revenue'
          type='Column'
          name='Revenue'
          yAxisName='revenueAxis'
        />
        <Chart3DSeriesDirective
          dataSource={financialData}
          xName='quarter'
          yName='expenses'
          type='Column'
          name='Expenses'
          yAxisName='expenseAxis'
        />
        <Chart3DSeriesDirective
          dataSource={financialData}
          xName='quarter'
          yName='netIncome'
          type='Column'
          name='Net Income'
          yAxisName='incomeAxis'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}

export default MultiplePane;
ReactDOM.render(<MultiplePane />, document.getElementById('charts'));
```

## Use Cases

**Financial dashboards:**
- Revenue, expenses, and profit in separate panes
- Each with appropriate scale

**Multi-metric monitoring:**
- Temperature, humidity, pressure
- Different units, separate ranges

**Comparison charts:**
- Actual vs budget in top pane
- Variance in bottom pane

**Time series analysis:**
- Main data series on top
- Moving average or trend below

## Best Practices

**Height distribution:**
- Primary data gets larger pane (50-60%)
- Secondary/supporting data gets smaller pane (30-40%)
- Equal heights only if metrics are equally important

**Axis configuration:**
- Match axis `rowIndex` with row position (0-indexed)
- Set appropriate `minimum`, `maximum` for each axis
- Use consistent `labelFormat` for similar metrics

**Visual consistency:**
- Use row borders sparingly (may clutter)
- Maintain consistent color scheme across panes
- Align gridlines if possible

**Performance:**
- Limit to 2-4 rows for readability
- Too many panes reduce individual chart size
- Consider separate charts if >4 metrics

## Common Issues

**Series not appearing in correct row:**
- Verify axis `rowIndex` matches row position
- Check series `yAxisName` matches axis `name`
- Ensure `rows` array has correct number of entries

**Rows overlapping:**
- Total height percentages should sum to 100%
- Use exact percentages: '33.33%' instead of '33%' for three equal rows

**Axes not aligned:**
- Set matching `rowIndex` for axes that should be in same row
- Use `span` property for axes spanning multiple rows

**Uneven spacing:**
- Specify explicit height percentages
- Check for border widths affecting layout

---

See also: [api-reference.md](api-reference.md) | [usage-example.md](usage-example.md)
