# Legend

## Table of Contents
- [Overview](#overview)
- [Enabling Legend](#enabling-legend)
- [Legend Position](#legend-position)
- [Legend Shapes](#legend-shapes)
- [Legend Paging](#legend-paging)
- [Legend Text Wrap](#legend-text-wrap)
- [Legend Templates](#legend-templates)
- [Legend Layout](#legend-layout)
- [Legend Item Customization](#legend-item-customization)
- [Legend Click Event](#legend-click-event)
- [Toggling Series Visibility](#toggling-series-visibility)

## Overview

The legend provides a visual guide to identify different data points or categories in the chart, typically displaying colored symbols with corresponding labels.

## Enabling Legend

Enable the legend by injecting the `AccumulationLegend` module and setting `visible: true`:

```tsx
import { 
  AccumulationChartComponent,
  AccumulationSeriesCollectionDirective,
  AccumulationSeriesDirective,
  Inject,
  PieSeries,
  AccumulationLegend
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
      legendSettings={{ visible: true }}  // Enable legend
    >
      <Inject services={[PieSeries, AccumulationLegend]} />
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

## Legend Position

Position the legend using the `position` property:

```tsx
legendSettings={{
  visible: true,
  position: 'Bottom'  // 'Top', 'Bottom', 'Left', 'Right', 'Auto'
}}
```

**Position options:**
- `'Top'`: Above the chart
- `'Bottom'`: Below the chart (default)
- `'Left'`: Left side of chart
- `'Right'`: Right side of chart
- `'Auto'`: Automatically determined based on available space

**Alignment within position:**

```tsx
legendSettings={{
  visible: true,
  position: 'Bottom',
  alignment: 'Center'  // 'Near', 'Center', 'Far'
}}
```

**Complete example:**

```tsx
function PositionedLegend() {
  const data = [
    { x: 'Product A', y: 45 },
    { x: 'Product B', y: 30 },
    { x: 'Product C', y: 25 }
  ];

  return (
    <AccumulationChartComponent 
      id='positioned-legend'
      legendSettings={{
        visible: true,
        position: 'Right',
        alignment: 'Center',
        height: '100',
        width: '150'
      }}
    >
      <Inject services={[PieSeries, AccumulationLegend]} />
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

## Legend Shapes

Customize legend item shapes using the `legendShape` property:

```tsx
legendSettings={{
  visible: true,
  legendShape: 'Circle'  // Shape for all items
}}
```

**Shape options:**
- `'Circle'`
- `'Rectangle'`
- `'Triangle'`
- `'Diamond'`
- `'Pentagon'`
- `'Cross'`
- `'HorizontalLine'`
- `'VerticalLine'`

**Per-point shape customization:**

```tsx
function CustomShapes() {
  const data = [
    { x: 'Chrome', y: 61.3, legendShape: 'Circle' },
    { x: 'Safari', y: 24.6, legendShape: 'Rectangle' },
    { x: 'Firefox', y: 14.1, legendShape: 'Triangle' }
  ];

  return (
    <AccumulationChartComponent 
      id='custom-shapes'
      legendSettings={{ visible: true }}
    >
      <Inject services={[PieSeries, AccumulationLegend]} />
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

## Legend Paging

Enable paging when the legend has many items:

```tsx
legendSettings={{
  visible: true,
  enablePages: true,  // Enable paging
  padding: 8
}}
```

**How paging works:**
- When legend items exceed available space, paging controls appear
- Users can navigate through pages using arrow buttons
- Page size automatically calculated based on legend dimensions

**Example with many items:**

```tsx
function PagedLegend() {
  const data = Array.from({ length: 20 }, (_, i) => ({
    x: `Category ${i + 1}`,
    y: Math.floor(Math.random() * 50) + 10
  }));

  return (
    <AccumulationChartComponent 
      id='paged-legend'
      legendSettings={{
        visible: true,
        position: 'Bottom',
        enablePages: true,
        height: '50',  // Limit height to trigger paging
        padding: 5
      }}
    >
      <Inject services={[PieSeries, AccumulationLegend]} />
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

## Legend Text Wrap

Wrap long legend text using `textWrap`:

```tsx
legendSettings={{
  visible: true,
  textWrap: 'Wrap',  // 'Normal', 'Wrap', or 'AnyWhere'
  maximumLabelWidth: 100  // Max width before wrapping
}}
```

**textWrap modes:**
- `'Normal'`: No wrapping, text truncated with ellipsis
- `'Wrap'`: Wrap at word boundaries
- `'AnyWhere'`: Wrap anywhere if needed

**Example:**

```tsx
function WrappedLegendText() {
  const data = [
    { 
      x: 'Google Chrome Browser with Extensions', 
      y: 61.3 
    },
    { 
      x: 'Apple Safari with Intelligent Tracking', 
      y: 24.6 
    },
    { 
      x: 'Mozilla Firefox Quantum', 
      y: 14.1 
    }
  ];

  return (
    <AccumulationChartComponent 
      id='wrapped-legend'
      legendSettings={{
        visible: true,
        position: 'Right',
        textWrap: 'Wrap',
        maximumLabelWidth: 120,
        width: '150'
      }}
    >
      <Inject services={[PieSeries, AccumulationLegend]} />
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

## Legend Templates

Create custom legend item layouts using HTML templates:

```tsx
function TemplateLegend() {
  const data = [
    { x: 'Chrome', y: 61.3, fill: '#4285F4' },
    { x: 'Safari', y: 24.6, fill: '#0088FF' },
    { x: 'Firefox', y: 14.1, fill: '#FF6600' }
  ];

  const legendTemplate = (args: any) => {
    return (
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        padding: '5px',
        backgroundColor: '#f5f5f5',
        borderRadius: '4px'
      }}>
        <div style={{
          width: '20px',
          height: '20px',
          backgroundColor: args.fill,
          borderRadius: '50%'
        }} />
        <div>
          <div style={{ fontWeight: 'bold', fontSize: '12px' }}>
            {args.x}
          </div>
          <div style={{ fontSize: '10px', color: '#666' }}>
            {args.y}%
          </div>
        </div>
      </div>
    );
  };

  return (
    <AccumulationChartComponent 
      id='template-legend'
      legendSettings={{
        visible: true,
        position: 'Right',
        template: legendTemplate
      }}
    >
      <Inject services={[PieSeries, AccumulationLegend]} />
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

## Legend Layout

Control legend layout using `width`, `height`, and `padding`:

```tsx
legendSettings={{
  visible: true,
  position: 'Right',
  width: '200',     // Fixed width
  height: '150',    // Fixed height
  padding: 10,      // Padding around legend
  border: {
    width: 1,
    color: '#cccccc'
  }
}}
```

**Layout properties:**
- `width`: Fixed width (string with units or number)
- `height`: Fixed height
- `padding`: Space inside legend border
- `border`: Border styling
- `background`: Background color

**Example with styled layout:**

```tsx
function StyledLegendLayout() {
  const data = [
    { x: 'Product A', y: 45 },
    { x: 'Product B', y: 30 },
    { x: 'Product C', y: 25 }
  ];

  return (
    <AccumulationChartComponent 
      id='styled-legend'
      legendSettings={{
        visible: true,
        position: 'Bottom',
        width: '100%',
        height: '60',
        padding: 15,
        background: '#f9f9f9',
        border: {
          width: 2,
          color: '#0078d4'
        },
        textStyle: {
          fontFamily: 'Segoe UI',
          size: '12px',
          fontWeight: '600'
        }
      }}
    >
      <Inject services={[PieSeries, AccumulationLegend]} />
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

## Legend Item Customization

Customize individual legend items using `legendRender` event:

```tsx
import { IAccLegendRenderEventArgs } from '@syncfusion/ej2-react-charts';

function CustomizedLegendItems() {
  const data = [
    { x: 'Chrome', y: 61.3 },
    { x: 'Safari', y: 24.6 },
    { x: 'Firefox', y: 14.1 }
  ];

  const onLegendRender = (args: IAccLegendRenderEventArgs): void => {
    // Customize legend text
    args.text = args.text + ' (' + args.shape + ')';
    
    // Change shape for specific item
    if (args.text.includes('Chrome')) {
      args.shape = 'Circle';
      args.fill = '#4285F4';
    }
  };

  return (
    <AccumulationChartComponent 
      id='customized-items'
      legendRender={onLegendRender}
      legendSettings={{ visible: true }}
    >
      <Inject services={[PieSeries, AccumulationLegend]} />
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

## Legend Click Event

Handle legend item clicks using `legendClick` event:

```tsx
import { IAccLegendClickEventArgs } from '@syncfusion/ej2-react-charts';

function LegendClickHandler() {
  const data = [
    { x: 'Chrome', y: 61.3 },
    { x: 'Safari', y: 24.6 },
    { x: 'Firefox', y: 14.1 }
  ];

  const onLegendClick = (args: IAccLegendClickEventArgs): void => {
    console.log('Legend clicked:', args.legendText);
    console.log('Series index:', args.seriesIndex);
    console.log('Point index:', args.pointIndex);
    
    // Cancel default toggle behavior if needed
    // args.cancel = true;
  };

  return (
    <AccumulationChartComponent 
      id='legend-click'
      legendClick={onLegendClick}
      legendSettings={{
        visible: true,
        toggleVisibility: true  // Enable click to toggle
      }}
    >
      <Inject services={[PieSeries, AccumulationLegend]} />
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

## Toggling Series Visibility

Enable click-to-toggle functionality to show/hide data points:

```tsx
legendSettings={{
  visible: true,
  toggleVisibility: true  // Click legend to hide/show points
}}
```

**How it works:**
- Click legend item to hide corresponding data point
- Click again to show it
- Visual feedback: grayed out legend item when hidden
- Useful for focusing on specific data

**Complete example with toggle:**

```tsx
function ToggleableLegend() {
  const data = [
    { x: 'Chrome', y: 61.3 },
    { x: 'Safari', y: 24.6 },
    { x: 'Firefox', y: 14.1 },
    { x: 'Edge', y: 5.0 },
    { x: 'Others', y: 8.0 }
  ];

  return (
    <AccumulationChartComponent 
      id='toggle-legend'
      title='Browser Market Share (Click legend to toggle)'
      legendSettings={{
        visible: true,
        toggleVisibility: true,
        position: 'Bottom',
        alignment: 'Center'
      }}
    >
      <Inject services={[PieSeries, AccumulationLegend]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          radius='90%'
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Common Issues and Solutions

**Issue: Legend not showing**
- Solution: Ensure `AccumulationLegend` module is injected
- Solution: Verify `visible: true` in legendSettings
- Solution: Check if data has valid x values for legend labels

**Issue: Legend text truncated**
- Solution: Increase `maximumLabelWidth` property
- Solution: Use `textWrap: 'Wrap'` for multi-line labels
- Solution: Increase legend width if positioned on sides

**Issue: Legend overlapping chart**
- Solution: Adjust chart `margin` to provide space
- Solution: Use `position: 'Bottom'` or 'Top' for horizontal layout
- Solution: Set explicit `width` or `height` for legend

**Issue: Too many legend items**
- Solution: Enable paging with `enablePages: true`
- Solution: Consider grouping small values
- Solution: Use legend template with scrolling container

**Issue: Legend click not working**
- Solution: Verify `toggleVisibility: true` is set
- Solution: Ensure `legendClick` event handler is properly attached
- Solution: Check that event is not cancelled (args.cancel = false)
