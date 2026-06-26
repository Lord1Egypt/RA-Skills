# Getting Started with 3D Charts

This guide covers installation, setup, and creating your first Syncfusion React 3D Chart.


## Table of contents

- [Installation](getting-started.md#installation)
- [Required Imports](getting-started.md#required-imports)
- [CSS Imports](getting-started.md#css-imports)
- [Basic 3D Column Chart](getting-started.md#basic-3d-column-chart)
- [Essential Props](getting-started.md#essential-props)
- [Module Injection](getting-started.md#module-injection)
- [Data Binding](getting-started.md#data-binding)
  - [Array of Objects (Recommended)](getting-started.md#array-of-objects-recommended)
  - [Multiple Series](getting-started.md#multiple-series)
- [Adding Title and Subtitle](getting-started.md#adding-title-and-subtitle)
- [Troubleshooting](getting-started.md#troubleshooting)

## Installation

Install the required package:

```bash
npm install @syncfusion/ej2-react-charts --save
```

## Required Imports

Import the necessary modules in your component:

```tsx
import { Chart3DComponent, Chart3DSeriesCollectionDirective, Chart3DSeriesDirective, Inject, ColumnSeries3D, Category3D, Legend3D, DataLabel3D, Tooltip3D } from '@syncfusion/ej2-react-charts';
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
<Chart3DComponent theme='Material3Dark'>
  {/* Sankey content */}
</Chart3DComponent>
```


## Basic 3D Column Chart

Create a simple 3D column chart with category axis:

```tsx
import React from 'react';
import { Chart3DComponent, Chart3DSeriesCollectionDirective, Chart3DSeriesDirective, Inject, ColumnSeries3D, Category3D } from '@syncfusion/ej2-react-charts';

function App() {
  const data = [
    { month: 'Jan', sales: 35 },
    { month: 'Feb', sales: 28 },
    { month: 'Mar', sales: 34 },
    { month: 'Apr', sales: 32 },
    { month: 'May', sales: 40 }
  ];

  return (
    <Chart3DComponent
      id='chart'
      primaryXAxis={{ valueType: 'Category' }}
      primaryYAxis={{ title: 'Sales' }}
    >
      <Inject services={[ColumnSeries3D, Category3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='month'
          yName='sales'
          type='Column'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}

export default App;
```

## Essential Props

**Chart3DComponent:**
- `id`: Unique identifier (required)
- `primaryXAxis`: X-axis configuration
- `primaryYAxis`: Y-axis configuration
- `enableRotation`: Enable 3D rotation (default: true)
- `rotation`: Rotation angle (0-360, default: 7)
- `tilt`: Tilt angle (0-90, default: 10)
- `depth`: Chart depth (20-100, default: 100)

**Chart3DSeriesDirective:**
- `dataSource`: Array of data objects
- `xName`: Property name for x-axis values
- `yName`: Property name for y-axis values
- `type`: Chart type ('Column', 'Bar', 'StackingColumn', etc.)

## Module Injection

The `Inject` component registers modules needed by the chart. Common modules:

- `ColumnSeries3D`: Column chart type
- `BarSeries3D`: Bar chart type
- `StackingColumnSeries3D`: Stacked column type
- `StackingBarSeries3D`: Stacked bar type
- `Category3D`: Category axis
- `DateTime3D`: DateTime axis
- `Logarithmic3D`: Logarithmic axis
- `Legend3D`: Legend support
- `DataLabel3D`: Data label support
- `Tooltip3D`: Tooltip support
- `Highlight3D`: Highlight on hover
- `Selection3D`: Data point selection
- `Export3D`: Export functionality

**Always inject the series type and axis type you're using.**

## Data Binding

### Array of Objects (Recommended)

```tsx
const data = [
  { category: 'Product A', value: 30 },
  { category: 'Product B', value: 40 },
  { category: 'Product C', value: 25 }
];

<Chart3DSeriesDirective
  dataSource={data}
  xName='category'
  yName='value'
  type='Column'
/>
```

### Multiple Series

```tsx
const salesData = [
  { month: 'Jan', product1: 35, product2: 28 },
  { month: 'Feb', product1: 28, product2: 34 },
  { month: 'Mar', product1: 34, product2: 40 }
];

<Chart3DSeriesCollectionDirective>
  <Chart3DSeriesDirective
    dataSource={salesData}
    xName='month'
    yName='product1'
    type='Column'
    name='Product 1'
  />
  <Chart3DSeriesDirective
    dataSource={salesData}
    xName='month'
    yName='product2'
    type='Column'
    name='Product 2'
  />
</Chart3DSeriesCollectionDirective>
```

## Adding Title and Subtitle

```tsx
<Chart3DComponent
  id='chart'
  title='Monthly Sales Report'
  titleStyle={{ fontFamily: 'Segoe UI', fontWeight: '600', size: '16px' }}
  subTitle='2024 Data'
  subTitleStyle={{ fontFamily: 'Segoe UI', size: '12px' }}
  primaryXAxis={{ valueType: 'Category' }}
>
  {/* Series */}
</Chart3DComponent>
```

## Troubleshooting

**Chart not rendering:**
- Verify CSS imports are present
- Check that `Inject` includes the chart type (e.g., `ColumnSeries3D`)
- Ensure `primaryXAxis.valueType` matches your data (Category, Numeric, DateTime)
- Verify container has height/width (set explicit dimensions if needed)

**Data not displaying:**
- Check `xName` and `yName` match property names in dataSource exactly (case-sensitive)
- Ensure dataSource is an array of objects, not null/undefined
- Verify numeric values are numbers, not strings

**TypeScript errors:**
- Import types: `import { Chart3DLoadedEventArgs } from '@syncfusion/ej2-react-charts';`
- Type your data array: `const data: { month: string; sales: number }[] = [...]`

**3D view not visible:**
- Set `enableRotation={true}` explicitly
- Adjust `rotation` (0-360) and `tilt` (0-90) values
- Increase `depth` for more pronounced 3D effect

---

See also: [api-reference.md](api-reference.md) | [usage-example.md](usage-example.md)
