# Tooltip

This guide covers enabling and customizing tooltips in 3D Circular Charts, including headers, format strings, templates, fixed positioning, styling, and dynamic customization.

## Table of contents

- [Overview](tooltip.md#overview)
- [Enabling Tooltips](tooltip.md#enabling-tooltips)
  - [Module Injection](tooltip.md#module-injection)
  - [Basic Tooltip Setup](tooltip.md#basic-tooltip-setup)
- [Header](tooltip.md#header)
  - [Setting Tooltip Header](tooltip.md#setting-tooltip-header)
  - [Dynamic Header Example](tooltip.md#dynamic-header-example)
- [Format](tooltip.md#format)
  - [Format Placeholders](tooltip.md#format-placeholders)
  - [Basic Format Example](tooltip.md#basic-format-example)
  - [Advanced Format Patterns](tooltip.md#advanced-format-patterns)
- [Tooltip Template](tooltip.md#tooltip-template)
  - [Basic Template](tooltip.md#basic-template)
  - [Rich Styled Template](tooltip.md#rich-styled-template)
  - [React Function Template](tooltip.md#react-function-template)
- [Fixed Tooltip](tooltip.md#fixed-tooltip)
- [Customization](tooltip.md#customization)
  - [Basic Styling](tooltip.md#basic-styling)
  - [Complete Styling Example](tooltip.md#complete-styling-example)
- [Customization of Individual Tooltip](tooltip.md#customization-of-individual-tooltip)
  - [Basic tooltipRender](tooltip.md#basic-tooltiprender)
  - [Conditional Styling](tooltip.md#conditional-styling)
  - [Adding Calculated Values](tooltip.md#adding-calculated-values)
- [Summary](tooltip.md#summary)

## Overview

Tooltips display detailed information about data points when users hover over chart slices. They provide an interactive way to explore data without cluttering the chart with labels.

## Enabling Tooltips

### Module Injection

First, inject the `CircularChartTooltip3D` module:

```tsx
import {
  CircularChart3DComponent,
  CircularChart3DSeriesCollectionDirective,
  CircularChart3DSeriesDirective,
  PieSeries3D,
  CircularChartTooltip3D,  // Import tooltip module
  Inject
} from '@syncfusion/ej2-react-charts';
```

### Basic Tooltip Setup

Enable tooltips by setting `enable: true` in the `tooltip` property:

```tsx
function TooltipExample() {
  const data = [
    { browser: 'Chrome', usage: 65 },
    { browser: 'Firefox', usage: 15 },
    { browser: 'Safari', usage: 12 },
    { browser: 'Edge', usage: 8 }
  ];

  return (
    <CircularChart3DComponent
      id="chart"
      title="Browser Market Share"
      tooltip={{ enable: true }}  // Enable tooltips
    >
      <Inject services={[PieSeries3D, CircularChartTooltip3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="browser"
          yName="usage"
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

**Result**: When hovering over any slice, a tooltip displays the browser name and usage value.

### Default Tooltip Behavior

By default, tooltips show:
- Category name (x-axis value)
- Data value (y-axis value)
- Auto-positioning near the cursor
- Fade-in/fade-out animations

## Header

Add a custom header to provide context for tooltip information.

### Setting Tooltip Header

```tsx
<CircularChart3DComponent
  title="Sales Data"
  tooltip={{
    enable: true,
    header: 'Product Information'  // Custom header
  }}
>
  {/* Chart content */}
</CircularChart3DComponent>
```

### Dynamic Header Example

```tsx
function HeaderExample() {
  const data = [
    { product: 'Laptops', sales: 35000, region: 'North' },
    { product: 'Phones', sales: 28000, region: 'South' },
    { product: 'Tablets', sales: 20000, region: 'East' },
    { product: 'Accessories', sales: 17000, region: 'West' }
  ];

  return (
    <CircularChart3DComponent
      title="Product Sales by Region"
      tooltip={{
        enable: true,
        header: 'Sales Details'
      }}
    >
      <Inject services={[PieSeries3D, CircularChartTooltip3D]} />
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

**Tip**: Headers help users understand what the tooltip data represents, especially in complex charts.

## Format

Customize tooltip content using format strings with placeholders.

### Format Placeholders

- **`${point.x}`**: Category/label value
- **`${point.y}`**: Data value
- **`${series.name}`**: Series name

### Basic Format Example

```tsx
<CircularChart3DComponent
  tooltip={{
    enable: true,
    format: '${point.x}: ${point.y} units'
  }}
>
  {/* Chart content */}
</CircularChart3DComponent>
```

### Advanced Format Patterns

```tsx
function FormattedTooltips() {
  const data = [
    { department: 'Engineering', budget: 125000 },
    { department: 'Marketing', budget: 85000 },
    { department: 'Sales', budget: 110000 },
    { department: 'Operations', budget: 75000 }
  ];

  return (
    <CircularChart3DComponent
      title="Department Budgets"
      tooltip={{
        enable: true,
        header: 'Budget Allocation',
        format: '<b>${point.x}</b><br/>Budget: $${point.y}<br/>Department Total'
      }}
    >
      <Inject services={[PieSeries3D, CircularChartTooltip3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="department"
          yName="budget"
          name="2024 Budget"
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

### Percentage Display

```tsx
function PercentageTooltip() {
  const data = [
    { category: 'A', value: 0.35 },  // 35%
    { category: 'B', value: 0.28 },  // 28%
    { category: 'C', value: 0.20 },  // 20%
    { category: 'D', value: 0.17 }   // 17%
  ];

  return (
    <CircularChart3DComponent
      title="Market Share"
      tooltip={{
        enable: true,
        format: '${point.x}: ${point.y}%'  // Display as percentage
      }}
    >
      <Inject services={[PieSeries3D, CircularChartTooltip3D]} />
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

## Tooltip Template

Create custom HTML templates for rich, styled tooltip content.

### Basic Template

```tsx
function TemplateTooltip() {
  const data = [
    { product: 'Product A', sales: 45, growth: '+12%' },
    { product: 'Product B', sales: 30, growth: '+8%' },
    { product: 'Product C', sales: 25, growth: '-3%' }
  ];

  const tooltipTemplate = '<div style="background: #f5f5f5; padding: 10px; border-radius: 5px;">' +
                         '<div style="font-weight: bold; color: #333;">${x}</div>' +
                         '<div>Sales: ${y}</div>' +
                         '</div>';

  return (
    <CircularChart3DComponent
      title="Product Performance"
      tooltip={{
        enable: true,
        template: tooltipTemplate
      }}
    >
      <Inject services={[PieSeries3D, CircularChartTooltip3D]} />
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

### Rich Styled Template

```tsx
function RichTooltip() {
  const data = [
    { region: 'North America', revenue: 450000, customers: 1200 },
    { region: 'Europe', revenue: 380000, customers: 950 },
    { region: 'Asia Pacific', revenue: 520000, customers: 1500 }
  ];

  const richTemplate = '<div style="' +
                      'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);' +
                      'color: white;' +
                      'padding: 12px 16px;' +
                      'border-radius: 8px;' +
                      'box-shadow: 0 4px 6px rgba(0,0,0,0.3);' +
                      'min-width: 180px;' +
                      '">' +
                      '<div style="font-size: 14px; font-weight: bold; margin-bottom: 8px;">${x}</div>' +
                      '<div style="font-size: 12px; opacity: 0.9;">Revenue: $${y}</div>' +
                      '</div>';

  return (
    <CircularChart3DComponent
      title="Regional Revenue"
      tooltip={{
        enable: true,
        template: richTemplate
      }}
    >
      <Inject services={[PieSeries3D, CircularChartTooltip3D]} />
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

## Fixed Tooltip

Pin the tooltip to a specific location instead of following the mouse.

### Setting Fixed Location

```tsx
function FixedTooltip() {
  const data = [
    { category: 'A', value: 35 },
    { category: 'B', value: 28 },
    { category: 'C', value: 22 },
    { category: 'D', value: 15 }
  ];

  return (
    <CircularChart3DComponent
      title="Fixed Position Tooltip"
      tooltip={{
        enable: true,
        location: { x: 200, y: 150 }  // Fixed at x: 200, y: 150
      }}
    >
      <Inject services={[PieSeries3D, CircularChartTooltip3D]} />
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

**Use cases**:
- Dashboard displays where tooltip shouldn't move
- Presentation mode with fixed information panel
- Touch interfaces where hover position is ambiguous

## Customization

Style the tooltip appearance with colors, borders, and fonts.

### Basic Styling

```tsx
<CircularChart3DComponent
  tooltip={{
    enable: true,
    fill: '#1e293b',        // Background color
    border: {
      color: '#3b82f6',     // Border color
      width: 2              // Border width
    },
    textStyle: {
      color: '#ffffff',     // Text color
      size: '12px',         // Font size
      fontFamily: 'Arial'   // Font family
    }
  }}
>
  {/* Chart content */}
</CircularChart3DComponent>
```

### Complete Styling Example

```tsx
function StyledTooltip() {
  const data = [
    { product: 'Product A', sales: 45000 },
    { product: 'Product B', sales: 32000 },
    { product: 'Product C', sales: 28000 }
  ];

  return (
    <CircularChart3DComponent
      title="Styled Tooltips"
      tooltip={{
        enable: true,
        header: 'Sales Information',
        format: '${point.x}<br/>Revenue: $${point.y}',
        fill: '#263238',
        opacity: 0.95,
        border: {
          color: '#00bcd4',
          width: 3
        },
        textStyle: {
          color: '#ffffff',
          size: '13px',
          fontFamily: 'Segoe UI',
          fontWeight: '500'
        }
      }}
    >
      <Inject services={[PieSeries3D, CircularChartTooltip3D]} />
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

### Highlight Color

Change the color of the data point when hovering:

```tsx
<CircularChart3DComponent
  tooltip={{
    enable: true,
    highlightColor: '#ff6b6b'  // Red highlight on hover
  }}
>
  {/* Chart content */}
</CircularChart3DComponent>
```

## Customization of Individual Tooltip

Use the `tooltipRender` event to customize tooltips dynamically for specific points.

### Basic tooltipRender

```tsx
function IndividualTooltip() {
  const data = [
    { item: 'Item A', value: 45 },
    { item: 'Item B', value: 30 },
    { item: 'Item C', value: 25 }
  ];

  const handleTooltipRender = (args) => {
    // Customize tooltip text
    args.text = `${args.point.x}: ${args.point.y} units sold`;
  };

  return (
    <CircularChart3DComponent
      title="Inventory"
      tooltip={{ enable: true }}
      tooltipRender={handleTooltipRender}
    >
      <Inject services={[PieSeries3D, CircularChartTooltip3D]} />
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

### Conditional Styling

Apply different styles based on data values:

```tsx
function ConditionalTooltip() {
  const data = [
    { product: 'Product A', sales: 95 },
    { product: 'Product B', sales: 45 },  // Low
    { product: 'Product C', sales: 88 },
    { product: 'Product D', sales: 32 }   // Low
  ];

  const handleTooltipRender = (args) => {
    const value = args.point.y;
    
    if (value < 50) {
      // Warning style for low values
      args.fill = '#f44336';
      args.border = { color: '#c62828', width: 2 };
      args.text = `⚠️ ${args.point.x}<br/>Low Sales: ${value}`;
    } else if (value > 90) {
      // Success style for high values
      args.fill = '#4caf50';
      args.border = { color: '#2e7d32', width: 2 };
      args.text = `✓ ${args.point.x}<br/>Excellent: ${value}`;
    } else {
      // Default style
      args.fill = '#2196f3';
      args.text = `${args.point.x}<br/>Sales: ${value}`;
    }
  };

  return (
    <CircularChart3DComponent
      title="Sales Performance"
      tooltip={{ enable: true }}
      tooltipRender={handleTooltipRender}
    >
      <Inject services={[PieSeries3D, CircularChartTooltip3D]} />
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

### Adding Calculated Values

```tsx
function CalculatedTooltip() {
  const data = [
    { region: 'North', revenue: 450000, expenses: 320000 },
    { region: 'South', revenue: 380000, expenses: 275000 },
    { region: 'East', revenue: 520000, expenses: 390000 }
  ];

  const handleTooltipRender = (args) => {
    const point = args.point;
    const dataItem = data.find(d => d.region === point.x);
    const profit = dataItem.revenue - dataItem.expenses;
    const margin = ((profit / dataItem.revenue) * 100).toFixed(1);
    
    args.text = `<b>${point.x}</b><br/>` +
                `Revenue: $${point.y.toLocaleString()}<br/>` +
                `Expenses: $${dataItem.expenses.toLocaleString()}<br/>` +
                `Profit: $${profit.toLocaleString()}<br/>` +
                `Margin: ${margin}%`;
  };

  return (
    <CircularChart3DComponent
      title="Regional Performance"
      tooltip={{ enable: true }}
      tooltipRender={handleTooltipRender}
    >
      <Inject services={[PieSeries3D, CircularChartTooltip3D]} />
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

## Summary

You've learned how to:
- ✅ Enable tooltips with CircularChartTooltip3D module
- ✅ Add custom headers for context
- ✅ Format tooltip content with placeholders
- ✅ Create HTML templates for rich displays
- ✅ Use React function templates for complex logic
- ✅ Pin tooltips to fixed locations
- ✅ Style tooltips (colors, borders, fonts)
- ✅ Highlight data points on hover
- ✅ Dynamically customize tooltips with tooltipRender
- ✅ Apply conditional styling based on values

**Best Practices:**
- Use format strings for simple customizations
- Use templates for rich, styled content
- Keep tooltip content concise and readable
- Apply conditional styling to highlight important data
- Test on mobile/touch devices (tooltips may behave differently)
- Consider accessibility (keyboard navigation, screen readers)