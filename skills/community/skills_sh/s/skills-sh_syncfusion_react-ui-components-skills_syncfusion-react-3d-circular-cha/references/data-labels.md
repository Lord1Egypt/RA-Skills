# Data Labels

This guide covers adding and customizing data labels in 3D Circular Charts, including positioning, templates, connector lines, text formatting, and dynamic customization.

## Table of Contents
- [Overview](#overview)
- [Enabling Data Labels](#enabling-data-labels)
- [Positioning](#positioning)
- [Data Label Templates](#data-label-templates)
- [Connector Lines](#connector-lines)
- [Text Mapping](#text-mapping)
- [Format Options](#format-options)
- [Dynamic Customization](#dynamic-customization)
- [Percentage Display](#percentage-display)

## Overview

Data labels display values, percentages, or custom text directly on chart slices, making it easier for users to read exact values without hovering. The 3D Circular Chart automatically arranges labels to prevent overlapping.

## Enabling Data Labels

### Module Injection

First, inject the `CircularChartDataLabel3D` module:

```tsx
import {
  CircularChart3DComponent,
  CircularChart3DSeriesCollectionDirective,
  CircularChart3DSeriesDirective,
  PieSeries3D,
  CircularChartDataLabel3D,  // Import module
  Inject
} from '@syncfusion/ej2-react-charts';
```

### Basic Data Label Setup

Enable data labels by setting `visible: true` in the `dataLabel` property:

```tsx
function DataLabelExample() {
  const data = [
    { category: 'Chrome', usage: 65 },
    { category: 'Firefox', usage: 15 },
    { category: 'Safari', usage: 12 },
    { category: 'Edge', usage: 8 }
  ];

  return (
    <CircularChart3DComponent
      id="chart"
      title="Browser Usage"
    >
      <Inject services={[PieSeries3D, CircularChartDataLabel3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="category"
          yName="usage"
          dataLabel={{ visible: true }}  // Enable data labels
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

**Result**: Labels displaying category names appear on each slice with smart positioning to avoid overlap.

### Smart Label Arrangement

The component automatically:
- Prevents label overlapping
- Adjusts label positions for readability
- Uses connector lines when labels are outside
- Optimizes placement based on slice size

## Positioning

Data labels can be positioned either **inside** or **outside** the chart slices.

### Inside Position

Labels appear within the chart slices (default for larger slices):

```tsx
<CircularChart3DSeriesDirective
  dataSource={data}
  xName="category"
  yName="value"
  dataLabel={{
    visible: true,
    position: 'Inside'
  }}
/>
```

**Best for**: Large slices with enough space for text.

### Outside Position

Labels appear outside the chart with connector lines:

```tsx
<CircularChart3DSeriesDirective
  dataSource={data}
  xName="category"
  yName="value"
  dataLabel={{
    visible: true,
    position: 'Outside'
  }}
/>
```

**Best for**: Small slices or when you want to avoid cluttering the chart.

### Position Comparison

```tsx
function PositionComparison() {
  const data = [
    { item: 'A', value: 40 },
    { item: 'B', value: 30 },
    { item: 'C', value: 20 },
    { item: 'D', value: 10 }
  ];

  return (
    <div style={{ display: 'flex', gap: '20px' }}>
      <CircularChart3DComponent title="Inside Labels">
        <Inject services={[PieSeries3D, CircularChartDataLabel3D]} />
        <CircularChart3DSeriesCollectionDirective>
          <CircularChart3DSeriesDirective
            dataSource={data}
            xName="item"
            yName="value"
            dataLabel={{ visible: true, position: 'Inside' }}
          />
        </CircularChart3DSeriesCollectionDirective>
      </CircularChart3DComponent>

      <CircularChart3DComponent title="Outside Labels">
        <Inject services={[PieSeries3D, CircularChartDataLabel3D]} />
        <CircularChart3DSeriesCollectionDirective>
          <CircularChart3DSeriesDirective
            dataSource={data}
            xName="item"
            yName="value"
            dataLabel={{ visible: true, position: 'Outside' }}
          />
        </CircularChart3DSeriesCollectionDirective>
      </CircularChart3DComponent>
    </div>
  );
}
```

## Data Label Templates

Templates allow you to create custom label layouts with HTML and dynamic placeholders.

### Template Placeholders

- `${point.x}`: Category/label value
- `${point.y}`: Data value
- `${point.percentage}`: Percentage (if calculated)
- `${series.name}`: Series name

### Basic Template

```tsx
function TemplateExample() {
  const data = [
    { product: 'Laptops', sales: 35 },
    { product: 'Phones', sales: 28 },
    { product: 'Tablets', sales: 20 },
    { product: 'Accessories', sales: 17 }
  ];

  const labelTemplate = '<div style="background: #fff; padding: 5px; border-radius: 3px;">' +
                        '<b>${point.x}</b><br/>' +
                        'Sales: ${point.y}' +
                        '</div>';

  return (
    <CircularChart3DComponent title="Product Sales">
      <Inject services={[PieSeries3D, CircularChartDataLabel3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="product"
          yName="sales"
          dataLabel={{
            visible: true,
            position: 'Outside',
            template: labelTemplate
          }}
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

### Styled Template with Icons

```tsx
const richTemplate = '<div style="' +
                    'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);' +
                    'color: white;' +
                    'padding: 8px 12px;' +
                    'border-radius: 5px;' +
                    'box-shadow: 0 2px 4px rgba(0,0,0,0.2);' +
                    'font-family: Arial;' +
                    '">' +
                    '<div style="font-size: 12px; opacity: 0.9;">${point.x}</div>' +
                    '<div style="font-size: 16px; font-weight: bold;">${point.y}</div>' +
                    '</div>';

<CircularChart3DSeriesDirective
  dataSource={data}
  xName="category"
  yName="value"
  dataLabel={{
    visible: true,
    position: 'Outside',
    template: richTemplate
  }}
/>
```

### React Function Template

For more complex templates, use a function:

```tsx
function FunctionTemplateExample() {
  const data = [
    { region: 'North', revenue: 45000 },
    { region: 'South', revenue: 38000 },
    { region: 'East', revenue: 52000 },
    { region: 'West', revenue: 41000 }
  ];

  const template = (props) => {
    const color = props.point.y > 45000 ? '#4CAF50' : '#2196F3';
    return (
      <div style={{ 
        background: color, 
        color: 'white', 
        padding: '6px 10px',
        borderRadius: '4px',
        fontSize: '11px'
      }}>
        <div style={{ fontWeight: 'bold' }}>{props.point.x}</div>
        <div>${(props.point.y / 1000).toFixed(0)}K</div>
      </div>
    );
  };

  return (
    <CircularChart3DComponent title="Regional Revenue">
      <Inject services={[PieSeries3D, CircularChartDataLabel3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="region"
          yName="revenue"
          dataLabel={{
            visible: true,
            position: 'Outside',
            template: template
          }}
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

## Connector Lines

Connector lines connect labels to their slices when positioned outside. Customize them using `connectorStyle`.

### Basic Connector Customization

```tsx
<CircularChart3DSeriesDirective
  dataSource={data}
  xName="category"
  yName="value"
  dataLabel={{
    visible: true,
    position: 'Outside',
    connectorStyle: {
      color: '#333333',
      width: 2,
      length: '30px',
      dashArray: '5,3'  // Dashed line
    }
  }}
/>
```

### Connector Properties

- **`color`**: Line color (hex, rgb, or color name)
- **`width`**: Line thickness in pixels
- **`length`**: Distance from chart to label
- **`dashArray`**: Dash pattern (e.g., '5,3' for dashes)

### Styled Connectors Example

```tsx
function StyledConnectors() {
  const data = [
    { category: 'Product A', sales: 45 },
    { category: 'Product B', sales: 30 },
    { category: 'Product C', sales: 25 }
  ];

  return (
    <CircularChart3DComponent title="Sales Distribution">
      <Inject services={[PieSeries3D, CircularChartDataLabel3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="category"
          yName="sales"
          dataLabel={{
            visible: true,
            position: 'Outside',
            connectorStyle: {
              color: '#2196F3',
              width: 2,
              length: '50px'  // Longer connector for spacing
            },
            font: { size: '12px', fontWeight: 'bold', color: '#333' }
          }}
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

## Text Mapping

Map custom text from your data source to display as labels instead of default values.

### Using Name Property

```tsx
function TextMappingExample() {
  const data = [
    { id: 1, name: 'Premium Users', count: 150, displayText: '150 Premium' },
    { id: 2, name: 'Standard Users', count: 300, displayText: '300 Standard' },
    { id: 3, name: 'Free Users', count: 550, displayText: '550 Free' }
  ];

  return (
    <CircularChart3DComponent title="User Distribution">
      <Inject services={[PieSeries3D, CircularChartDataLabel3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="name"      // Show name in label
          yName="count"
          dataLabel={{
            visible: true,
            name: 'displayText'  // Use custom text from data
          }}
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

## Format Options

Format numeric labels using standard format strings.

### Common Format Patterns

| Format | Input | Output | Description |
|--------|-------|--------|-------------|
| `n1` | 1000 | 1000.0 | 1 decimal place |
| `n2` | 1000 | 1000.00 | 2 decimal places |
| `p1` | 0.01 | 1.0% | Percentage with 1 decimal |
| `p2` | 0.01 | 1.00% | Percentage with 2 decimals |
| `c1` | 1000 | $1000.0 | Currency with 1 decimal |
| `c2` | 1000 | $1000.00 | Currency with 2 decimals |

### Using Format Property

```tsx
function FormattedLabels() {
  const data = [
    { department: 'Engineering', budget: 125000 },
    { department: 'Marketing', budget: 85000 },
    { department: 'Sales', budget: 110000 },
    { department: 'Operations', budget: 75000 }
  ];

  return (
    <CircularChart3DComponent title="Department Budgets">
      <Inject services={[PieSeries3D, CircularChartDataLabel3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="department"
          yName="budget"
          dataLabel={{
            visible: true,
            position: 'Outside',
            format: 'c0'  // Currency with no decimals: $125,000
          }}
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

### Percentage Format

```tsx
const fractionalData = [
  { category: 'A', value: 0.35 },  // 35%
  { category: 'B', value: 0.28 },  // 28%
  { category: 'C', value: 0.37 }   // 37%
];

<CircularChart3DSeriesDirective
  dataSource={fractionalData}
  xName="category"
  yName="value"
  dataLabel={{
    visible: true,
    format: 'p0'  // Shows as 35%, 28%, 37%
  }}
/>
```

## Dynamic Customization

Use the `textRender` event to customize label text dynamically before rendering.

### Basic textRender Usage

```tsx
function DynamicLabels() {
  const data = [
    { item: 'Item A', value: 45 },
    { item: 'Item B', value: 30 },
    { item: 'Item C', value: 25 }
  ];

  const handleTextRender = (args) => {
    // Modify label text
    args.text = `${args.point.x}: ${args.point.y} units`;
  };

  return (
    <CircularChart3DComponent
      title="Inventory"
      textRender={handleTextRender}
    >
      <Inject services={[PieSeries3D, CircularChartDataLabel3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="item"
          yName="value"
          dataLabel={{ visible: true }}
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

### Conditional Styling

```tsx
function ConditionalLabels() {
  const data = [
    { product: 'Product A', sales: 85 },
    { product: 'Product B', sales: 45 },  // Low
    { product: 'Product C', sales: 92 },
    { product: 'Product D', sales: 38 }   // Low
  ];

  const handleTextRender = (args) => {
    if (args.point.y < 50) {
      args.color = '#F44336';  // Red for low sales
      args.text = `⚠️ ${args.text}`;  // Add warning icon
    } else if (args.point.y > 90) {
      args.color = '#4CAF50';  // Green for high sales
      args.text = `✓ ${args.text}`;  // Add checkmark
    }
  };

  return (
    <CircularChart3DComponent
      title="Sales Performance"
      textRender={handleTextRender}
    >
      <Inject services={[PieSeries3D, CircularChartDataLabel3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="product"
          yName="sales"
          dataLabel={{ visible: true, position: 'Outside' }}
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

## Percentage Display

Display percentages calculated from the total of all values.

### Using textRender for Percentages

```tsx
function PercentageLabels() {
  const data = [
    { category: 'A', value: 35 },
    { category: 'B', value: 28 },
    { category: 'C', value: 20 },
    { category: 'D', value: 17 }
  ];

  const handleTextRender = (args) => {
    const total = data.reduce((sum, item) => sum + item.value, 0);
    const percentage = ((args.point.y / total) * 100).toFixed(1);
    args.text = `${args.point.x}\n${percentage}%`;
  };

  return (
    <CircularChart3DComponent
      title="Market Share"
      textRender={handleTextRender}
    >
      <Inject services={[PieSeries3D, CircularChartDataLabel3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="category"
          yName="value"
          dataLabel={{
            visible: true,
            position: 'Outside',
            font: { size: '11px', fontWeight: '600' }
          }}
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

### Using Template for Percentages

```tsx
function PercentageTemplate() {
  const data = [
    { type: 'Type A', count: 40 },
    { type: 'Type B', count: 30 },
    { type: 'Type C', count: 30 }
  ];

  const total = data.reduce((sum, item) => sum + item.count, 0);

  const percentTemplate = (props) => {
    const percent = ((props.point.y / total) * 100).toFixed(1);
    return (
      <div style={{ textAlign: 'center', fontSize: '11px' }}>
        <div style={{ fontWeight: 'bold' }}>{props.point.x}</div>
        <div style={{ color: '#666' }}>{percent}%</div>
        <div style={{ fontSize: '10px', color: '#999' }}>({props.point.y})</div>
      </div>
    );
  };

  return (
    <CircularChart3DComponent title="Distribution">
      <Inject services={[PieSeries3D, CircularChartDataLabel3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="type"
          yName="count"
          dataLabel={{
            visible: true,
            position: 'Outside',
            template: percentTemplate
          }}
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

## Summary

You've learned how to:
- ✅ Enable data labels with CircularChartDataLabel3D module
- ✅ Position labels inside or outside chart slices
- ✅ Create custom templates with HTML and placeholders
- ✅ Customize connector lines (color, width, length, dash)
- ✅ Map custom text from data source
- ✅ Format numbers with n, p, c patterns
- ✅ Dynamically customize labels with textRender event
- ✅ Display calculated percentages

**Best Practices:**
- Use Outside position for small slices
- Keep templates simple for better performance
- Use format strings for standard numeric displays
- Apply textRender for complex calculations
- Style connector lines to match your theme