# Category Axis Configuration

A category axis displays string labels for discrete data points. It's the most common axis type for 3D charts showing data across named categories.

## Table of contents

- [Basic Category Axis](category-axis.md#basic-category-axis)
  - [Key requirement](category-axis.md#key-requirement-must-inject-category3d-service-for-category-axis-to-work)
- [Axis Title Configuration](category-axis.md#axis-title-configuration)
- [Label Customization](category-axis.md#label-customization)
  - [Label Styling](category-axis.md#label-styling)
  - [Label Rotation](category-axis.md#label-rotation)
  - [Label Trimming](category-axis.md#label-trimming)
- [Grid Lines](category-axis.md#grid-lines)
- [Axis Line Customization](category-axis.md#axis-line-customization)
- [Label Placement](category-axis.md#label-placement)
- [Multiple Category Levels](category-axis.md#multiple-category-levels)
- [Tick Customization](category-axis.md#tick-customization)
- [Axis Visibility](category-axis.md#axis-visibility)
- [Complete Category Axis Example](category-axis.md#complete-category-axis-example)
- [Common Issues](category-axis.md#common-issues)

## Basic Category Axis

```tsx
import { Chart3DComponent, Chart3DSeriesCollectionDirective, Chart3DSeriesDirective, Inject, ColumnSeries3D, Category3D } from '@syncfusion/ej2-react-charts';

function CategoryAxisChart() {
  const data = [
    { product: 'Laptop', sales: 45 },
    { product: 'Mobile', sales: 60 },
    { product: 'Tablet', sales: 35 },
    { product: 'Desktop', sales: 28 },
    { product: 'Accessory', sales: 52 }
  ];

  return (
    <Chart3DComponent
      id='chart'
      primaryXAxis={{
        valueType: 'Category',
        title: 'Products'
      }}
      primaryYAxis={{
        title: 'Sales (Units)'
      }}
    >
      <Inject services={[ColumnSeries3D, Category3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='product'
          yName='sales'
          type='Column'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

**Key requirement:** Must inject `Category3D` service for category axis to work.

## Axis Title Configuration

```tsx
<Chart3DComponent
  id='chart'
  primaryXAxis={{
    valueType: 'Category',
    title: 'Product Categories',
    titleStyle: {
      fontFamily: 'Segoe UI',
      size: '14px',
      fontWeight: '600',
      color: '#333'
    }
  }}
>
  {/* Series */}
</Chart3DComponent>
```

## Label Customization

### Label Styling

```tsx
<Chart3DComponent
  id='chart'
  primaryXAxis={{
    valueType: 'Category',
    labelStyle: {
      size: '12px',
      fontFamily: 'Arial',
      fontWeight: '500',
      color: '#555'
    }
  }}
>
  {/* Series */}
</Chart3DComponent>
```

### Label Rotation

For long category names:

```tsx
<Chart3DComponent
  id='chart'
  primaryXAxis={{
    valueType: 'Category',
    labelRotation: -45,  // Rotate 45 degrees counterclockwise
    labelStyle: { size: '11px' }
  }}
>
  {/* Series */}
</Chart3DComponent>
```

**Common rotation angles:**
- `-45`: Good for moderately long labels
- `-90`: Vertical labels, saves horizontal space
- `0`: Default horizontal (best for short labels)

### Label Trimming

Handle long labels automatically:

```tsx
<Chart3DComponent
  id='chart'
  primaryXAxis={{
    valueType: 'Category',
    labelIntersectAction: 'Trim',  // Options: 'None', 'Trim', 'Wrap', 'MultipleRows', 'Rotate45', 'Rotate90'
    maximumLabelWidth: 100
  }}
>
  {/* Series */}
</Chart3DComponent>
```

**Label intersect actions:**
- `None`: No action, labels may overlap
- `Trim`: Truncate with ellipsis (...)
- `Wrap`: Wrap to multiple lines
- `MultipleRows`: Arrange in staggered rows
- `Rotate45`: Rotate 45 degrees
- `Rotate90`: Rotate 90 degrees

## Grid Lines

```tsx
<Chart3DComponent
  id='chart'
  primaryXAxis={{
    valueType: 'Category',
    majorGridLines: {
      width: 1,
      color: '#E0E0E0'
    },
    minorGridLines: {
      width: 0  // Hide minor grid lines
    }
  }}
>
  {/* Series */}
</Chart3DComponent>
```

## Label Placement

```tsx
<Chart3DComponent
  id='chart'
  primaryXAxis={{
    valueType: 'Category',
    labelPlacement: 'BetweenTicks',  // Options: 'BetweenTicks', 'OnTicks'
    edgeLabelPlacement: 'Shift'  // Options: 'None', 'Shift', 'Hide'
  }}
>
  {/* Series */}
</Chart3DComponent>
```

**Label placement:**
- `BetweenTicks`: Labels centered between tick marks (default for Category)
- `OnTicks`: Labels aligned with tick marks

**Edge label placement:**
- `None`: Default behavior
- `Shift`: Move edge labels inside chart area
- `Hide`: Hide labels at edges

## Tick Customization

```tsx
<Chart3DComponent
  id='chart'
  primaryXAxis={{
    valueType: 'Category',
    majorTickLines: {
      width: 1,
      height: 8,
      color: '#333'
    },
    minorTickLines: {
      width: 0  // Hide minor ticks
    }
  }}
>
  {/* Series */}
</Chart3DComponent>
```

## Complete Category Axis Example

```tsx
function AdvancedCategoryAxis() {
  const salesData = [
    { department: 'Marketing', revenue: 120000 },
    { department: 'Sales', revenue: 180000 },
    { department: 'Engineering', revenue: 95000 },
    { department: 'Support', revenue: 78000 },
    { department: 'Operations', revenue: 110000 }
  ];

  return (
    <Chart3DComponent
      id='advanced-category'
      title='Department Revenue'
      primaryXAxis={{
        valueType: 'Category',
        title: 'Departments',
        titleStyle: {
          fontFamily: 'Segoe UI',
          size: '14px',
          fontWeight: '600'
        },
        labelStyle: {
          size: '12px',
          fontWeight: '500'
        },
        labelRotation: -45,
        labelIntersectAction: 'Trim',
        maximumLabelWidth: 80,
        majorGridLines: {
          width: 1,
          color: '#E0E0E0'
        },
        majorTickLines: {
          width: 1,
          height: 6
        }
      }}
      primaryYAxis={{
        title: 'Revenue ($)',
        labelFormat: '${value}K'
      }}
      rotation={7}
      tilt={10}
    >
      <Inject services={[ColumnSeries3D, Category3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={salesData}
          xName='department'
          yName='revenue'
          type='Column'
          name='Revenue'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

## Common Issues

**Labels overlapping:**
- Use `labelRotation: -45` or `-90`
- Set `labelIntersectAction: 'Rotate45'` or `'Trim'`
- Reduce `labelStyle.size`

**Categories not showing:**
- Ensure `valueType: 'Category'` is set
- Verify `Category3D` is injected
- Check `xName` matches data property exactly

**Wrong order:**
- Categories display in data order, not alphabetically
- Pre-sort data array if specific order needed
---

See also: [api-reference.md](api-reference.md) | [usage-example.md](usage-example.md)