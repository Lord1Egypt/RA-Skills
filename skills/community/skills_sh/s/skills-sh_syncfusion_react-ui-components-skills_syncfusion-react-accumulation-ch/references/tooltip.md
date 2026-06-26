# Tooltip

## Table of Contents
- [Overview](#overview)
- [Enabling Tooltip](#enabling-tooltip)
- [Tooltip Format](#tooltip-format)
- [Tooltip Templates](#tooltip-templates)
- [Fixed Tooltip Position](#fixed-tooltip-position)
- [Tooltip Animation](#tooltip-animation)
- [Shared Tooltip](#shared-tooltip)
- [Tooltip Customization with tooltipRender](#tooltip-customization-with-tooltiprender)

## Overview

Tooltips display detailed information about data points when users hover over them, providing an interactive way to explore chart data without cluttering the visualization.

## Enabling Tooltip

Enable tooltips by injecting the `AccumulationTooltip` module and setting `enable: true`:

```tsx
import { 
  AccumulationChartComponent,
  AccumulationSeriesCollectionDirective,
  AccumulationSeriesDirective,
  Inject,
  PieSeries,
  AccumulationTooltip
} from '@syncfusion/ej2-react-charts';

function App() {
  const data = [
    { x: 'Chrome', y: 61.3 },
    { x: 'Safari', y: 24.6 },
    { x: 'Firefox', y: 14.1 }
  ];

  return (
    <AccumulationChartComponent 
      id='chart'
      tooltip={{ enable: true }}  // Enable tooltip
    >
      <Inject services={[PieSeries, AccumulationTooltip]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Tooltip Format

Format tooltip content using the `format` property with placeholders:

```tsx
tooltip={{
  enable: true,
  format: '${point.x}: <b>${point.y}%</b>'
}}
```

**Available placeholders:**
- `${point.x}`: Category/label value
- `${point.y}`: Numeric value
- `${point.percentage}`: Calculated percentage
- `${point.text}`: Custom text from data
- `${series.name}`: Series name

**Format examples:**

```tsx
// Percentage format
format: '${point.x}: ${point.percentage}%'

// Currency format
format: '${point.x}: $${point.y}'

// Multi-line format
format: '<b>${point.x}</b><br/>Value: ${point.y}<br/>Percentage: ${point.percentage}%'
```

**Complete example:**

```tsx
function FormattedTooltip() {
  const salesData = [
    { product: 'Laptop', revenue: 45000, units: 150 },
    { product: 'Phone', revenue: 38500, units: 220 },
    { product: 'Tablet', revenue: 25000, units: 180 }
  ];

  return (
    <AccumulationChartComponent 
      id='formatted-tooltip'
      title='Revenue Distribution'
      tooltip={{
        enable: true,
        format: '<b>${point.x}</b><br/>Revenue: $${point.y}<br/>Share: ${point.percentage}%'
      }}
    >
      <Inject services={[PieSeries, AccumulationTooltip]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={salesData}
          xName='product'
          yName='revenue'
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Tooltip Templates

Create custom tooltip layouts using HTML templates:

```tsx
function TemplatedTooltip() {
  const data = [
    { 
      x: 'Chrome', 
      y: 61.3, 
      users: '2.5B',
      fill: '#4285F4'
    },
    { 
      x: 'Safari', 
      y: 24.6, 
      users: '1.0B',
      fill: '#0088FF'
    },
    { 
      x: 'Firefox', 
      y: 14.1, 
      users: '0.6B',
      fill: '#FF6600'
    }
  ];

  const tooltipTemplate = (args: any) => {
    return (
      <div style={{
        backgroundColor: args.data.pointColor || '#fff',
        color: '#fff',
        padding: '10px 15px',
        borderRadius: '5px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.2)'
      }}>
        <div style={{ 
          fontSize: '14px', 
          fontWeight: 'bold',
          marginBottom: '5px'
        }}>
          {args.point.x}
        </div>
        <div style={{ fontSize: '12px' }}>
          Market Share: {args.point.y}%
        </div>
        <div style={{ fontSize: '12px' }}>
          Active Users: {args.point.users}
        </div>
      </div>
    );
  };

  return (
    <AccumulationChartComponent 
      id='template-tooltip'
      tooltip={{
        enable: true,
        template: tooltipTemplate
      }}
    >
      <Inject services={[PieSeries, AccumulationTooltip]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          pointColorMapping='fill'
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Fixed Tooltip Position

Set a fixed position for tooltips using `location` property:

```tsx
tooltip={{
  enable: true,
  location: { x: 100, y: 50 }  // Fixed x, y coordinates
}}
```

**When to use fixed positioning:**
- Prevent tooltip from covering important chart areas
- Keep tooltip visible in specific region
- Create custom tooltip placement strategies

**Example with fixed position:**

```tsx
function FixedPositionTooltip() {
  const data = [
    { x: 'Q1', y: 35 },
    { x: 'Q2', y: 28 },
    { x: 'Q3', y: 42 },
    { x: 'Q4', y: 31 }
  ];

  return (
    <AccumulationChartComponent 
      id='fixed-tooltip'
      tooltip={{
        enable: true,
        location: { x: 50, y: 20 },
        format: '${point.x}: ${point.y}',
        textStyle: {
          fontWeight: 'bold'
        }
      }}
    >
      <Inject services={[PieSeries, AccumulationTooltip]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Tooltip Animation

Control tooltip appearance animation:

```tsx
tooltip={{
  enable: true,
  enableAnimation: true,  // Enable animation (default: true)
  duration: 300,          // Animation duration in ms
  fadeOutDuration: 500    // Fade out duration
}}
```

**Animation properties:**
- `enableAnimation`: Enable/disable animations
- `duration`: Show animation duration (milliseconds)
- `fadeOutDuration`: Hide animation duration (milliseconds)

**Example:**

```tsx
function AnimatedTooltip() {
  const data = [
    { x: 'Chrome', y: 61.3 },
    { x: 'Safari', y: 24.6 },
    { x: 'Firefox', y: 14.1 }
  ];

  return (
    <AccumulationChartComponent 
      id='animated-tooltip'
      tooltip={{
        enable: true,
        enableAnimation: true,
        duration: 500,
        fadeOutDuration: 300,
        opacity: 0.9
      }}
    >
      <Inject services={[PieSeries, AccumulationTooltip]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Shared Tooltip

For accumulation charts, tooltips are point-specific. However, you can create shared-like behavior with custom templates:

```tsx
function SharedStyleTooltip() {
  const data = [
    { x: 'Product A', y: 45, target: 50 },
    { x: 'Product B', y: 30, target: 35 },
    { x: 'Product C', y: 25, target: 28 }
  ];

  const sharedTemplate = (args: any) => {
    const variance = args.point.y - args.point.target;
    const status = variance >= 0 ? 'Above' : 'Below';
    const color = variance >= 0 ? '#28a745' : '#dc3545';

    return (
      <div style={{
        backgroundColor: '#fff',
        padding: '12px',
        border: `2px solid ${color}`,
        borderRadius: '6px',
        minWidth: '150px'
      }}>
        <div style={{ fontWeight: 'bold', marginBottom: '8px' }}>
          {args.point.x}
        </div>
        <div style={{ marginBottom: '4px' }}>
          Actual: <b>{args.point.y}</b>
        </div>
        <div style={{ marginBottom: '4px' }}>
          Target: <b>{args.point.target}</b>
        </div>
        <div style={{ color: color, fontWeight: 'bold' }}>
          {status} Target by {Math.abs(variance)}
        </div>
      </div>
    );
  };

  return (
    <AccumulationChartComponent 
      id='shared-style-tooltip'
      tooltip={{
        enable: true,
        template: sharedTemplate
      }}
    >
      <Inject services={[PieSeries, AccumulationTooltip]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Tooltip Customization with tooltipRender

Customize tooltip content and styling dynamically using `tooltipRender` event:

```tsx
import { IAccTooltipRenderEventArgs } from '@syncfusion/ej2-react-charts';

function DynamicTooltip() {
  const data = [
    { x: 'Chrome', y: 61.3, trend: 'up' },
    { x: 'Safari', y: 24.6, trend: 'down' },
    { x: 'Firefox', y: 14.1, trend: 'stable' }
  ];

  const onTooltipRender = (args: IAccTooltipRenderEventArgs): void => {
    // Customize tooltip text
    const point = args.point as any;
    args.text = `${point.x}: ${point.y}% (${point.trend})`;
    
    // Customize tooltip header
    args.headerText = 'Browser Statistics';
    
    // Customize styling based on data
    if (point.trend === 'up') {
      args.textStyle = {
        color: '#28a745',
        fontWeight: 'bold'
      };
    } else if (point.trend === 'down') {
      args.textStyle = {
        color: '#dc3545',
        fontWeight: 'bold'
      };
    }
  };

  return (
    <AccumulationChartComponent 
      id='dynamic-tooltip'
      tooltipRender={onTooltipRender}
      tooltip={{ enable: true }}
    >
      <Inject services={[PieSeries, AccumulationTooltip]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

**tooltipRender event properties:**
- `args.text`: Modify tooltip content
- `args.headerText`: Set tooltip header
- `args.textStyle`: Customize text styling
- `args.data`: Access point data
- `args.cancel`: Cancel tooltip display

**Advanced example with conditional styling:**

```tsx
function ConditionalTooltip() {
  const data = [
    { x: 'Q1', y: 7, status: 'low' },
    { x: 'Q2', y: 15, status: 'medium' },
    { x: 'Q3', y: 21, status: 'high' },
    { x: 'Q4', y: 18, status: 'medium' }
  ];

  const onTooltipRender = (args: IAccTooltipRenderEventArgs): void => {
    const point = args.point as any;
    
    // Set background color based on status
    const colors: any = {
      low: '#ffc107',
      medium: '#17a2b8',
      high: '#28a745'
    };
    
    args.fill = colors[point.status] || '#6c757d';
    
    // Custom formatting
    args.text = [
      `<b>${point.x}</b>`,
      `Sales: ${point.y}M`,
      `Status: ${point.status.toUpperCase()}`
    ];
    
    args.textStyle = {
      color: '#fff',
      fontFamily: 'Segoe UI',
      size: '12px'
    };
  };

  return (
    <AccumulationChartComponent 
      id='conditional-tooltip'
      tooltipRender={onTooltipRender}
      tooltip={{
        enable: true,
        opacity: 0.95,
        border: { width: 2, color: '#fff' }
      }}
    >
      <Inject services={[PieSeries, AccumulationTooltip]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Common Issues and Solutions

**Issue: Tooltip not showing**
- Solution: Ensure `AccumulationTooltip` module is injected
- Solution: Verify `enable: true` in tooltip settings
- Solution: Check if data values are valid

**Issue: Tooltip text truncated**
- Solution: Use template instead of format for complex layouts
- Solution: Adjust tooltip border and padding
- Solution: Use `<br/>` tags in format string for multi-line

**Issue: Tooltip flickering**
- Solution: Reduce `duration` and `fadeOutDuration`
- Solution: Disable animation with `enableAnimation: false`
- Solution: Check for conflicting hover events

**Issue: Template not rendering**
- Solution: Ensure template function returns valid JSX
- Solution: Verify point data is accessible in template
- Solution: Check browser console for React errors

**Issue: Tooltip position incorrect**
- Solution: Avoid using fixed `location` unless necessary
- Solution: Check parent container positioning
- Solution: Ensure chart has proper dimensions
