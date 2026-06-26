# Legend

This guide covers adding and customizing legends in 3D Circular Charts, including positioning, alignment, pagination, styling, and advanced legend features.

## Table of Contents
- [Overview](#overview)
- [Enabling Legend](#enabling-legend)
- [Position and Alignment](#position-and-alignment)
- [Legend Reverse](#legend-reverse)
- [Legend Shape](#legend-shape)
- [Legend Size](#legend-size)
- [Legend Item Size](#legend-item-size)
- [Legend Paging](#legend-paging)
- [Text Wrap](#text-wrap)
- [Legend Title](#legend-title)
- [Arrow Page Navigation](#arrow-page-navigation)
- [Item Padding](#item-padding)

## Overview

Legends provide information about data points in the chart, making it easy to understand what each color/slice represents. They're especially useful when chart slices are small or numerous.

## Enabling Legend

### Module Injection

First, inject the `CircularChartLegend3D` module:

```tsx
import {
  CircularChart3DComponent,
  CircularChart3DSeriesCollectionDirective,
  CircularChart3DSeriesDirective,
  PieSeries3D,
  CircularChartLegend3D,  // Import legend module
  Inject
} from '@syncfusion/ej2-react-charts';
```

### Basic Legend Setup

Enable the legend by setting `visible: true` in `legendSettings`:

```tsx
function LegendExample() {
  const data = [
    { product: 'Laptops', sales: 35 },
    { product: 'Phones', sales: 28 },
    { product: 'Tablets', sales: 20 },
    { product: 'Accessories', sales: 17 }
  ];

  return (
    <CircularChart3DComponent
      id="chart"
      title="Product Sales"
      legendSettings={{ visible: true }}  // Enable legend
    >
      <Inject services={[PieSeries3D, CircularChartLegend3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="product"
          yName="sales"
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

**Result**: A legend appears on the right side showing all product categories with their colors.

## Position and Alignment

Control where the legend appears and how it's aligned within that position.

### Position Options

The legend can be positioned at four locations:
- **`Right`** (default)
- **`Left`**
- **`Top`**
- **`Bottom`**

### Alignment Options

Within each position, legends can be aligned:
- **`Center`** (default)
- **`Near`** (start of the position)
- **`Far`** (end of the position)

### Position Examples

```tsx
// Right side (default)
<CircularChart3DComponent
  legendSettings={{
    visible: true,
    position: 'Right'
  }}
>
  {/* Chart content */}
</CircularChart3DComponent>

// Bottom center
<CircularChart3DComponent
  legendSettings={{
    visible: true,
    position: 'Bottom',
    alignment: 'Center'
  }}
>
  {/* Chart content */}
</CircularChart3DComponent>

// Top left corner
<CircularChart3DComponent
  legendSettings={{
    visible: true,
    position: 'Top',
    alignment: 'Near'
  }}
>
  {/* Chart content */}
</CircularChart3DComponent>
```

### Complete Position Demo

```tsx
function PositionDemo() {
  const data = [
    { category: 'A', value: 35 },
    { category: 'B', value: 28 },
    { category: 'C', value: 22 },
    { category: 'D', value: 15 }
  ];

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
      <CircularChart3DComponent
        title="Legend: Right"
        legendSettings={{ visible: true, position: 'Right' }}
      >
        <Inject services={[PieSeries3D, CircularChartLegend3D]} />
        <CircularChart3DSeriesCollectionDirective>
          <CircularChart3DSeriesDirective
            dataSource={data}
            xName="category"
            yName="value"
          />
        </CircularChart3DSeriesCollectionDirective>
      </CircularChart3DComponent>

      <CircularChart3DComponent
        title="Legend: Bottom"
        legendSettings={{ visible: true, position: 'Bottom' }}
      >
        <Inject services={[PieSeries3D, CircularChartLegend3D]} />
        <CircularChart3DSeriesCollectionDirective>
          <CircularChart3DSeriesDirective
            dataSource={data}
            xName="category"
            yName="value"
          />
        </CircularChart3DSeriesCollectionDirective>
      </CircularChart3DComponent>
    </div>
  );
}
```

## Legend Reverse

Reverse the order of legend items using the `reverse` property.

### Default Order (First to Last)

By default, the first data point appears first in the legend.

### Reversed Order (Last to First)

```tsx
function ReversedLegend() {
  const data = [
    { rank: '1st Place', score: 95 },
    { rank: '2nd Place', score: 87 },
    { rank: '3rd Place', score: 76 },
    { rank: '4th Place', score: 65 }
  ];

  return (
    <CircularChart3DComponent
      title="Competition Results"
      legendSettings={{
        visible: true,
        reverse: true  // Reverse legend order
      }}
    >
      <Inject services={[PieSeries3D, CircularChartLegend3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="rank"
          yName="score"
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

**Use case**: Show most important items last, or reverse chronological order.

## Legend Shape

Customize the shape of legend markers using `legendShape` in the series.

### Available Shapes

- **`Circle`**
- **`Rectangle`**
- **`Triangle`**
- **`Diamond`**
- **`Cross`**
- **`HorizontalLine`**
- **`VerticalLine`**
- **`Pentagon`**
- **`InvertedTriangle`**
- **`SeriesType`** (default - matches series type)

### Custom Shape Example

```tsx
function CustomShapes() {
  const data = [
    { status: 'Active', count: 45 },
    { status: 'Pending', count: 28 },
    { status: 'Completed', count: 27 }
  ];

  return (
    <CircularChart3DComponent
      title="Project Status"
      legendSettings={{ visible: true }}
    >
      <Inject services={[PieSeries3D, CircularChartLegend3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="status"
          yName="count"
          legendShape="Diamond"  // Diamond markers
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

## Legend Size

Control the overall dimensions of the legend container.

### Setting Width and Height

```tsx
<CircularChart3DComponent
  title="Sales Data"
  legendSettings={{
    visible: true,
    width: '200px',   // Legend container width
    height: '150px'   // Legend container height
  }}
>
  {/* Chart content */}
</CircularChart3DComponent>
```

### Responsive Legend

```tsx
function ResponsiveLegend() {
  const data = [
    { region: 'North America', revenue: 45 },
    { region: 'Europe', revenue: 30 },
    { region: 'Asia Pacific', revenue: 25 }
  ];

  return (
    <CircularChart3DComponent
      title="Regional Revenue"
      width="100%"
      legendSettings={{
        visible: true,
        width: '25%',    // Percentage-based width
        position: 'Right'
      }}
    >
      <Inject services={[PieSeries3D, CircularChartLegend3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="region"
          yName="revenue"
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

## Legend Item Size

Customize the size of individual legend markers (shapes).

### Shape Height and Width

```tsx
<CircularChart3DComponent
  title="Product Categories"
  legendSettings={{
    visible: true,
    shapeHeight: 15,  // Marker height in pixels
    shapeWidth: 15    // Marker width in pixels
  }}
>
  {/* Chart content */}
</CircularChart3DComponent>
```

### Custom Item Sizing

```tsx
function CustomItemSize() {
  const data = [
    { category: 'Premium', value: 35 },
    { category: 'Standard', value: 45 },
    { category: 'Basic', value: 20 }
  ];

  return (
    <CircularChart3DComponent
      title="Subscription Tiers"
      legendSettings={{
        visible: true,
        position: 'Bottom',
        shapeHeight: 20,  // Larger markers
        shapeWidth: 20
      }}
    >
      <Inject services={[PieSeries3D, CircularChartLegend3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="category"
          yName="value"
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

**Tip**: Larger markers (15-25px) are better for accessibility and touch interfaces.

## Legend Paging

When legend items exceed available space, pagination is automatically enabled with navigation buttons.

### Automatic Paging

Paging activates automatically when there are many legend items:

```tsx
function ManyLegendItems() {
  // Generate many data points
  const data = Array.from({ length: 20 }, (_, i) => ({
    item: `Item ${i + 1}`,
    value: Math.floor(Math.random() * 50) + 10
  }));

  return (
    <CircularChart3DComponent
      title="Many Categories"
      height="600px"
      legendSettings={{
        visible: true,
        position: 'Right',
        width: '150px',
        height: '400px'
      }}
    >
      <Inject services={[PieSeries3D, CircularChartLegend3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="item"
          yName="value"
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

**Features**:
- Previous/Next buttons appear automatically
- Page number indicator shows current page
- Users can navigate through legend items
- Click-through still works on all items

## Text Wrap

Control how legend text wraps when it exceeds the available width.

### Text Wrap Property

```tsx
<CircularChart3DComponent
  legendSettings={{
    visible: true,
    textWrap: 'Wrap'  // Options: 'Normal', 'Wrap', 'Trim'
  }}
>
  {/* Chart content */}
</CircularChart3DComponent>
```

### Maximum Label Width

```tsx
function TextWrapExample() {
  const data = [
    { product: 'Very Long Product Name That Exceeds Width', sales: 35 },
    { product: 'Another Extremely Long Category Name', sales: 28 },
    { product: 'Short', sales: 20 },
    { product: 'Medium Length Product', sales: 17 }
  ];

  return (
    <CircularChart3DComponent
      title="Product Sales"
      legendSettings={{
        visible: true,
        textWrap: 'Wrap',
        maximumLabelWidth: 100,  // Wrap after 100px
        width: '200px'
      }}
    >
      <Inject services={[PieSeries3D, CircularChartLegend3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="product"
          yName="sales"
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

### Text Wrap Options

- **`Normal`**: No wrapping, text may overflow
- **`Wrap`**: Wrap text to next line
- **`Trim`**: Truncate with ellipsis (...)

## Legend Title

Add a title to the legend for additional context.

### Basic Title

```tsx
<CircularChart3DComponent
  legendSettings={{
    visible: true,
    title:  'Product Categories'
  }}
>
  {/* Chart content */}
</CircularChart3DComponent>
```

### Styled Title

```tsx
function StyledLegendTitle() {
  const data = [
    { quarter: 'Q1 2024', revenue: 45000 },
    { quarter: 'Q2 2024', revenue: 52000 },
    { quarter: 'Q3 2024', revenue: 48000 },
    { quarter: 'Q4 2024', revenue: 55000 }
  ];

  return (
    <CircularChart3DComponent
      title="Quarterly Performance"
      legendSettings={{
        visible: true,
        position: 'Bottom',
        title: 'Fiscal Quarters',
        textStyle: {
          size: '14px',
          fontWeight: 'Bold',
          color: '#2196F3',
          fontFamily: 'Arial',
          textAlignment: 'Center',
        },
      }}
    >
      <Inject services={[PieSeries3D, CircularChartLegend3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="quarter"
          yName="revenue"
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

### Title Style Properties

- **`size`**: Font size (e.g., '12px', '14px')
- **`fontWeight`**: 'Normal', 'Bold', '600'
- **`color`**: Text color
- **`fontFamily`**: Font name
- **`textAlignment`**: 'Near', 'Center', 'Far'
- **`textOverflow`**: 'None', 'Trim', 'Wrap'

## Arrow Page Navigation

Disable page numbers and use arrow buttons only for cleaner pagination.

### Enable Arrow Navigation

```tsx
function ArrowNavigation() {
  // Many items to trigger pagination
  const data = Array.from({ length: 15 }, (_, i) => ({
    category: `Category ${String.fromCharCode(65 + i)}`,
    value: Math.floor(Math.random() * 30) + 10
  }));

  return (
    <CircularChart3DComponent
      title="Many Categories"
      height="500px"
      legendSettings={{
        visible: true,
        position: 'Right',
        width: '150px',
        height: '300px',
        enablePages: false  // Hide page numbers, show only arrows
      }}
    >
      <Inject services={[PieSeries3D, CircularChartLegend3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="category"
          yName="value"
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

**Comparison**:
- **`enablePages: true`** (default): Shows "Page 1 of 3" with arrows
- **`enablePages: false`**: Shows only left/right arrow buttons

## Item Padding

Adjust spacing between legend items for better readability.

### Setting Item Padding

```tsx
<CircularChart3DComponent
  legendSettings={{
    visible: true,
    itemPadding: 15  // Padding in pixels between items
  }}
>
  {/* Chart content */}
</CircularChart3DComponent>
```

### Padding Example

```tsx
function PaddingComparison() {
  const data = [
    { type: 'Type A', value: 30 },
    { type: 'Type B', value: 25 },
    { type: 'Type C', value: 25 },
    { type: 'Type D', value: 20 }
  ];

  return (
    <div style={{ display: 'flex', gap: '20px' }}>
      <CircularChart3DComponent
        title="Default Padding"
        legendSettings={{
          visible: true,
          position: 'Bottom'
          // itemPadding: 8 (default)
        }}
      >
        <Inject services={[PieSeries3D, CircularChartLegend3D]} />
        <CircularChart3DSeriesCollectionDirective>
          <CircularChart3DSeriesDirective
            dataSource={data}
            xName="type"
            yName="value"
          />
        </CircularChart3DSeriesCollectionDirective>
      </CircularChart3DComponent>

      <CircularChart3DComponent
        title="Large Padding"
        legendSettings={{
          visible: true,
          position: 'Bottom',
          itemPadding: 20  // More spacing
        }}
      >
        <Inject services={[PieSeries3D, CircularChartLegend3D]} />
        <CircularChart3DSeriesCollectionDirective>
          <CircularChart3DSeriesDirective
            dataSource={data}
            xName="type"
            yName="value"
          />
        </CircularChart3DSeriesCollectionDirective>
      </CircularChart3DComponent>
    </div>
  );
}
```

**Guidelines**:
- Default: 8px (compact)
- Medium: 12-15px (balanced)
- Large: 20px+ (spacious, touch-friendly)

## Complete Configuration Example

```tsx
function FullyConfiguredLegend() {
  const data = [
    { category: 'Electronics', sales: 45, color: '#2196F3' },
    { category: 'Clothing', sales: 28, color: '#4CAF50' },
    { category: 'Home & Garden', sales: 18, color: '#FF9800' },
    { category: 'Sports', sales: 9, color: '#9C27B0' }
  ];

  return (
    <CircularChart3DComponent
      title="Sales by Department"
      width="800px"
      height="500px"
      legendSettings={{
        visible: true,
        position: 'Bottom',
        alignment: 'Center',
        width: '100%',
        height: '100px',
        shapeHeight: 18,
        shapeWidth: 18,
        itemPadding: 15,
        textWrap: 'Wrap',
        maximumLabelWidth: 150,
        title: 'Departments',
        textStyle: {
          size: '13px',
          fontWeight: 'Bold',
          color: '#333'
        }
      }}
    >
      <Inject services={[PieSeries3D, CircularChartLegend3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="category"
          yName="sales"
          pointColorMapping="color"
          legendShape="Circle"
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

## Summary

You've learned how to:
- ✅ Enable legends with CircularChartLegend3D module
- ✅ Position legends (Left, Right, Top, Bottom)
- ✅ Align legends (Near, Center, Far)
- ✅ Reverse legend order
- ✅ Customize legend shapes (Circle, Diamond, Triangle, etc.)
- ✅ Set legend size (width and height)
- ✅ Customize marker size (shapeHeight, shapeWidth)
- ✅ Enable automatic pagination for many items
- ✅ Wrap and truncate long text labels
- ✅ Add and style legend titles
- ✅ Use arrow-only navigation
- ✅ Adjust item spacing with padding

**Best Practices:**
- Use Bottom position for many horizontal items
- Use Right position for vertical layouts
- Enable text wrap for long category names
- Increase padding for touch interfaces
- Add titles for complex multi-series charts