# Pie and Donut Charts

This guide covers creating and customizing pie and donut chart variations using the 3D Circular Chart component, including radius customization, varied slice sizes, color mapping, and point-level customization.

## Table of Contents
- [Pie Chart Basics](#pie-chart-basics)
- [Radius Customization](#radius-customization)
- [Various Radius Pie Chart](#various-radius-pie-chart)
- [Donut Chart](#donut-chart)
- [Text and Fill Color Mapping](#text-and-fill-color-mapping)
- [Point Customization](#point-customization)

## Pie Chart Basics

A pie chart displays data as proportional slices of a circle, making it perfect for showing percentages and parts of a whole.

### Module Injection

To render a pie series, you must inject the `PieSeries3D` module:

```tsx
import {
  CircularChart3DComponent,
  CircularChart3DSeriesCollectionDirective,
  CircularChart3DSeriesDirective,
  PieSeries3D,
  Inject
} from '@syncfusion/ej2-react-charts';

<CircularChart3DComponent>
  <Inject services={[PieSeries3D]} />
  {/* Chart series */}
</CircularChart3DComponent>
```

### Basic Pie Chart

```tsx
import * as ReactDOM from 'react-dom';
import {
  CircularChart3DComponent,
  CircularChart3DSeriesCollectionDirective,
  CircularChart3DSeriesDirective,
  PieSeries3D,
  Inject,
  CircularChartLegend3D,
} from '@syncfusion/ej2-react-charts';
import * as React from 'react';

function App() {
  const data = [
    { category: 'Electronics', sales: 45, color: '#2196F3' },
    { category: 'Clothing', sales: 28, color: '#4CAF50' },
    { category: 'Home & Garden', sales: 18, color: '#FF9800' },
    { category: 'Sports', sales: 9, color: '#9C27B0' },
  ];

  return (
    <CircularChart3DComponent id="pie-chart" title="Browser Market Share">
      <Inject services={[PieSeries3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="category"
          yName="sales"
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}

export default App;
const root = ReactDOM.createRoot(document.getElementById('charts'));
root.render(<App />);
```

**Result**: A 3D pie chart with four slices representing browser usage percentages.

## Radius Customization

By default, the pie chart radius is **80%** of the chart's size (minimum of width and height). You can customize this using the `radius` property.

### Default Radius (80%)

```tsx
<CircularChart3DSeriesDirective
  dataSource={data}
  xName="category"
  yName="value"
  // radius="80%" is the default
/>
```

### Custom Radius

```tsx
<CircularChart3DSeriesDirective
  dataSource={data}
  xName="category"
  yName="value"
  radius="60%"  // Smaller pie
/>
```

### Common Radius Values

- **`50%`**: Small, compact pie
- **`70%`**: Medium size (good for charts with legends)
- **`80%`**: Default size
- **`90%`**: Large pie filling most of the chart area
- **`100%`**: Maximum size (touches chart edges)

### Example: Side-by-Side Size Comparison

```tsx
function RadiusComparison() {
  const data = [
    { item: 'A', value: 30 },
    { item: 'B', value: 40 },
    { item: 'C', value: 30 }
  ];

  return (
    <div style={{ display: 'flex', gap: '20px' }}>
      <CircularChart3DComponent
        title="Small (50%)"
        width="300px"
        height="300px"
      >
        <Inject services={[PieSeries3D]} />
        <CircularChart3DSeriesCollectionDirective>
          <CircularChart3DSeriesDirective
            dataSource={data}
            xName="item"
            yName="value"
            radius="50%"
          />
        </CircularChart3DSeriesCollectionDirective>
      </CircularChart3DComponent>

      <CircularChart3DComponent
        title="Large (90%)"
        width="300px"
        height="300px"
      >
        <Inject services={[PieSeries3D]} />
        <CircularChart3DSeriesCollectionDirective>
          <CircularChart3DSeriesDirective
            dataSource={data}
            xName="item"
            yName="value"
            radius="90%"
          />
        </CircularChart3DSeriesCollectionDirective>
      </CircularChart3DComponent>
    </div>
  );
}
```

## Various Radius Pie Chart

You can create a unique "exploded" or "varied" pie chart where each slice has a different radius, creating a dynamic visual effect.

### How It Works

Add a `radius` property to each data object, and the chart will use those individual radius values:

```tsx
function VariousRadiusPie() {
  const data = [
    { category: 'Product A', sales: 35, radius: '100' },  // Largest slice
    { category: 'Product B', sales: 25, radius: '80' },
    { category: 'Product C', sales: 20, radius: '70' },
    { category: 'Product D', sales: 20, radius: '60' }    // Smallest slice
  ];

  return (
    <CircularChart3DComponent
      id="various-radius-chart"
      title="Product Sales with Emphasis"
    >
      <Inject services={[PieSeries3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="category"
          yName="sales"
          radius="radius"  // Uses radius from data
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

### Use Cases

**Emphasis**: Make important slices larger to draw attention
```tsx
{ category: 'Top Performer', value: 40, radius: '100' }  // Emphasized
{ category: 'Others', value: 60, radius: '70' }          // De-emphasized
```

**Progressive Display**: Create a cascading or layered effect
```tsx
const data = [
  { month: 'Jan', value: 25, radius: '100' },
  { month: 'Feb', value: 25, radius: '90' },
  { month: 'Mar', value: 25, radius: '80' },
  { month: 'Apr', value: 25, radius: '70' }
];
```

## Donut Chart

A donut chart is a pie chart with a hollow center, created by setting an `innerRadius`. This creates a ring shape that's often more visually appealing and can contain center text.

### Creating a Donut Chart

Set the `innerRadius` property to any value greater than `0%`:

```tsx
function DonutChartExample() {
  const data = [
    { category: 'Marketing', budget: 40 },
    { category: 'Development', budget: 35 },
    { category: 'Operations', budget: 25 }
  ];

  return (
    <CircularChart3DComponent
      id="donut-chart"
      title="Budget Allocation"
    >
      <Inject services={[PieSeries3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="category"
          yName="budget"
          innerRadius="40%"  // Creates donut
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

### InnerRadius Values

The `innerRadius` property accepts values from `0%` to `100%` of the pie radius:

- **`0%`**: Standard pie chart (no hole)
- **`30%`**: Thin ring, large center
- **`40-50%`**: Balanced donut (most common)
- **`60-70%`**: Thick ring, small hole
- **`80%+`**: Very thick ring (unusual but possible)

### Common Donut Configurations

**Classic Donut** (balanced ring):
```tsx
<CircularChart3DSeriesDirective
  radius="80%"
  innerRadius="40%"  // Half of radius
/>
```

**Thin Ring** (emphasis on center):
```tsx
<CircularChart3DSeriesDirective
  radius="80%"
  innerRadius="60%"  // Large hole
/>
```

**Thick Donut** (emphasis on data):
```tsx
<CircularChart3DSeriesDirective
  radius="90%"
  innerRadius="30%"  // Small hole
/>
```

### Pie vs. Donut Comparison

```tsx
function PieVsDonut() {
  const data = [
    { type: 'A', value: 35 },
    { type: 'B', value: 30 },
    { type: 'C', value: 35 }
  ];

  return (
    <div style={{ display: 'flex', gap: '20px' }}>
      {/* Pie Chart */}
      <CircularChart3DComponent title="Pie Chart">
        <Inject services={[PieSeries3D]} />
        <CircularChart3DSeriesCollectionDirective>
          <CircularChart3DSeriesDirective
            dataSource={data}
            xName="type"
            yName="value"
            // No innerRadius = Pie
          />
        </CircularChart3DSeriesCollectionDirective>
      </CircularChart3DComponent>

      {/* Donut Chart */}
      <CircularChart3DComponent title="Donut Chart">
        <Inject services={[PieSeries3D]} />
        <CircularChart3DSeriesCollectionDirective>
          <CircularChart3DSeriesDirective
            dataSource={data}
            xName="type"
            yName="value"
            innerRadius="40%"  // Donut
          />
        </CircularChart3DSeriesCollectionDirective>
      </CircularChart3DComponent>
    </div>
  );
}
```

## Text and Fill Color Mapping

You can map custom text labels and colors directly from your data source using `pointColorMapping`.

### Color Mapping

Instead of using automatic colors, specify colors in your data:

```tsx
function ColorMappedChart() {
  const data = [
    { status: 'Success', count: 85, color: '#4CAF50' },   // Green
    { status: 'Warning', count: 10, color: '#FFC107' },   // Yellow
    { status: 'Error', count: 5, color: '#F44336' }       // Red
  ];

  return (
    <CircularChart3DComponent title="System Status">
      <Inject services={[PieSeries3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="status"
          yName="count"
          pointColorMapping="color"  // Map colors from data
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

### Custom Text with Name Property

You can provide custom display text separate from the data value:

```tsx
const data = [
  { id: 'prod_1', name: 'Premium Plan', revenue: 50000, color: '#673AB7' },
  { id: 'prod_2', name: 'Basic Plan', revenue: 30000, color: '#2196F3' },
  { id: 'prod_3', name: 'Free Plan', revenue: 20000, color: '#9E9E9E' }
];

<CircularChart3DSeriesDirective
  dataSource={data}
  xName="name"              // Display name instead of id
  yName="revenue"
  pointColorMapping="color"
/>
```

### Complete Example with Both Mappings

```tsx
function FullyMappedChart() {
  const salesData = [
    {
      region: 'North America',
      displayName: 'NA Region',
      sales: 45,
      color: '#1E88E5',
      text: '45% - NA'
    },
    {
      region: 'Europe',
      displayName: 'EU Region',
      sales: 30,
      color: '#43A047',
      text: '30% - EU'
    },
    {
      region: 'Asia Pacific',
      displayName: 'APAC Region',
      sales: 25,
      color: '#E53935',
      text: '25% - APAC'
    }
  ];

  return (
    <CircularChart3DComponent title="Global Sales Distribution">
      <Inject services={[PieSeries3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={salesData}
          xName="displayName"         // Custom labels
          yName="sales"
          pointColorMapping="color"   // Custom colors
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

## Point Customization

Use the `pointRender` event to customize individual points dynamically based on conditions or data values.

### Understanding pointRender

The `pointRender` event fires for each data point before rendering, allowing you to modify:
- Fill color
- Border properties
- Visibility
- Any other point-specific styling

### Basic Point Customization

```tsx
function CustomizedPoints() {
  const data = [
    { product: 'Product A', sales: 45 },
    { product: 'Product B', sales: 30 },
    { product: 'Product C', sales: 25 }
  ];

  const handlePointRender = (args) => {
    // Customize based on point index
    const colors = ['#FF6384', '#36A2EB', '#FFCE56'];
    args.fill = colors[args.point.index];
  };

  return (
    <CircularChart3DComponent
      title="Sales by Product"
      pointRender={handlePointRender}
    >
      <Inject services={[PieSeries3D]} />
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

### Conditional Styling

Highlight specific points based on data values:

```tsx
function ConditionalStyling() {
  const data = [
    { category: 'Q1', revenue: 25000 },
    { category: 'Q2', revenue: 35000 },  // Best quarter
    { category: 'Q3', revenue: 28000 },
    { category: 'Q4', revenue: 30000 }
  ];

  const handlePointRender = (args) => {
    // Highlight best performer in gold
    if (args.point.y > 33000) {
      args.fill = '#FFD700';  // Gold
      args.border = { color: '#FFA500', width: 3 };
    }
    // Mark low performers in gray
    else if (args.point.y < 27000) {
      args.fill = '#BDBDBD';  // Gray
    }
  };

  return (
    <CircularChart3DComponent
      title="Quarterly Revenue"
      pointRender={handlePointRender}
    >
      <Inject services={[PieSeries3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="category"
          yName="revenue"
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

### Advanced: Pattern-Based Styling

```tsx
function PatternStyling() {
  const data = [
    { dept: 'Engineering', budget: 40 },
    { dept: 'Marketing', budget: 30 },
    { dept: 'Sales', budget: 20 },
    { dept: 'Support', budget: 10 }
  ];

  const handlePointRender = (args) => {
    const pointName = args.point.x.toLowerCase();
    
    // Apply department-specific colors
    if (pointName.includes('engineering')) {
      args.fill = '#2196F3';  // Blue for tech
    } else if (pointName.includes('marketing')) {
      args.fill = '#FF9800';  // Orange for marketing
    } else if (pointName.includes('sales')) {
      args.fill = '#4CAF50';  // Green for sales
    } else {
      args.fill = '#9C27B0';  // Purple for others
    }

    // Add border to all points
    args.border = { color: '#ffffff', width: 2 };
  };

  return (
    <CircularChart3DComponent
      title="Department Budget"
      pointRender={handlePointRender}
    >
      <Inject services={[PieSeries3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="dept"
          yName="budget"
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

## Summary

You've learned how to:
- ✅ Create basic pie charts with PieSeries3D injection
- ✅ Customize chart radius (default 80%, adjustable)
- ✅ Create various radius pie charts for emphasis
- ✅ Build donut charts using innerRadius property
- ✅ Map custom colors from data with pointColorMapping
- ✅ Use custom text labels from data
- ✅ Dynamically customize points with pointRender event

**Next Steps**: Add data labels, legends, or tooltips to enhance your pie and donut charts.
