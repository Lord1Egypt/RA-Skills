# Interactive Features: Legend, Tooltip, and Crosshair

Stock Chart provides three key interactive features for enhanced user experience: Legend for series information, Tooltip for point details on hover, and Crosshair for precise value reading.

## Table of Contents
> Reference API: [references/api.md](./api.md)

- [Legend](#legend)
  - [Enabling Legend](#enabling-legend)
  - [Position and Alignment](#position-and-alignment)
  - [Customization](#legend-customization)
  - [Legend Title](#legend-title)
  - [Legend Template](#legend-template)
- [Tooltip](#tooltip)
  - [Enabling Tooltip](#enabling-tooltip)
  - [Format Customization](#tooltip-format-customization)
  - [Position Control](#tooltip-position)
  - [Appearance Styling](#tooltip-appearance)
- [Crosshair](#crosshair)
  - [Enabling Crosshair](#enabling-crosshair)
  - [Axis Tooltips](#crosshair-axis-tooltips)
  - [Customization](#crosshair-customization)
  - [Trackball](#trackball-shared-tooltip)

## Legend

Legend provides information about the series rendered in the Stock Chart. It's especially useful when displaying multiple series or comparing different stocks.

### Enabling Legend

Enable legend by setting `visible` to `true` in `legendSettings`:

```typescript
import { 
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  Inject,
  DateTime,
  CandleSeries,
  StockLegend
} from '@syncfusion/ej2-react-charts';

function LegendChart() {
  const stockData = [
    // Stock data...
  ];

  return (
    <StockChartComponent
      id='stockchart'
      primaryXAxis={{ valueType: 'DateTime' }}
      legendSettings={{ visible: true }}
    >
      <Inject services={[DateTime, CandleSeries, StockLegend]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={stockData}
          type='Candle'
          xName='x'
          high='high'
          low='low'
          open='open'
          close='close'
          name='AAPL'
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}
```

**Important:** Inject `StockLegend` module to use legend features.

### Position and Alignment

Legend can be positioned at `Left`, `Right`, `Top`, `Bottom`, or `Custom` locations.

**Bottom position (default):**
```typescript
<StockChartComponent
  legendSettings={{ 
    visible: true,
    position: 'Bottom'  // Default position
  }}
>
  {/* ... */}
</StockChartComponent>
```

**Top position:**
```typescript
<StockChartComponent
  legendSettings={{ 
    visible: true,
    position: 'Top'
  }}
>
  {/* ... */}
</StockChartComponent>
```

**Custom position with x, y coordinates:**
```typescript
<StockChartComponent
  legendSettings={{ 
    visible: true,
    position: 'Custom',
    location: { x: 100, y: 50 }
  }}
>
  {/* ... */}
</StockChartComponent>
```

**Legend alignment:**

Align legend as `Center`, `Far`, or `Near`:

```typescript
<StockChartComponent
  legendSettings={{ 
    visible: true,
    position: 'Bottom',
    alignment: 'Center'  // 'Center', 'Far', or 'Near'
  }}
>
  {/* ... */}
</StockChartComponent>
```

### Legend Customization

**Legend icon shape:**

Change the legend icon using `legendShape` in series:

```typescript
<StockChartSeriesDirective
  dataSource={stockData}
  type='Candle'
  legendShape='Circle'  // Circle, Rectangle, Triangle, Diamond, etc.
  name='Stock Price'
/>
```

**Legend size:**

Control legend dimensions with `width` and `height`:

```typescript
<StockChartComponent
  legendSettings={{ 
    visible: true,
    width: '300px',   // Legend width
    height: '100px'   // Legend height
  }}
>
  {/* ... */}
</StockChartComponent>
```

**Legend item size:**

Customize icon size with `shapeHeight` and `shapeWidth`:

```typescript
<StockChartComponent
  legendSettings={{ 
    visible: true,
    shapeHeight: 15,   // Icon height
    shapeWidth: 15     // Icon width
  }}
>
  {/* ... */}
</StockChartComponent>
```

**Collapsing legend items:**

Skip legend for a specific series by providing an empty series name:

```typescript
<StockChartSeriesDirective
  dataSource={stockData}
  type='Line'
  name=''  // Empty name - series won't appear in legend
/>
```

### Legend Title

Add a title to the legend:

```typescript
<StockChartComponent
  legendSettings={{ 
    visible: true,
    title: 'Stock Symbols',
    titleStyle: {
      fontFamily: 'Arial',
      fontSize: '14px',
      fontWeight: 'bold',
      color: '#333333',
      textAlignment: 'Center'
    },
    titlePosition: 'Top',  // 'Top', 'Left', 'Right'
    maximumTitleWidth: 200
  }}
>
  {/* ... */}
</StockChartComponent>
```

### Legend Template

Customize legend items with HTML templates:

```typescript
import { 
    StockChartComponent,
    StockChartSeriesCollectionDirective,
    StockChartSeriesDirective,
    Inject,
    DateTime,
    CandleSeries,
    StockLegend
  } from '@syncfusion/ej2-react-charts';
function LegendTemplateChart() {
  const stockData = [ /* data */ ];

  const legendTemplate = (args) => {
    return (
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <div style={{
              width: '16px',
              height: '16px',
              backgroundColor: args.fill,
              borderRadius: '50%'
            }}></div>
      
            <span style={{ fontWeight: 'bold' }}>{args.text}</span>
      
            <span style={{ color: '#666' }}>
              ({args.series?.dataSource?.length ?? 0} points)
            </span>
          </div>
    );
  };

  return (
    <StockChartComponent
      legendSettings={{ 
        visible: true,
        template: legendTemplate
      }}
    >
      <Inject services={[DateTime, CandleSeries, StockLegend]} />
      {/* ... series ... */}
    </StockChartComponent>
  );
}
export default LegendTemplateChart;
```

### Complete Legend Example

```typescript
import { 
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  Inject,
  DateTime,
  CandleSeries,
  LineSeries,
  StockLegend
} from '@syncfusion/ej2-react-charts';

function CompleteLegendChart() {
  const applData = [ /* AAPL stock data */ ];
  const googData = [ /* GOOG stock data */ ];

  return (
    <StockChartComponent
      id='stockchart'
      title='Stock Comparison'
      primaryXAxis={{ valueType: 'DateTime' }}
      legendSettings={{
        visible: true,
        position: 'Bottom',
        alignment: 'Center',
        shapeHeight: 12,
        shapeWidth: 12,
        title: 'Stocks',
        titleStyle: {
          fontSize: '12px',
          fontWeight: 'bold'
        }
      }}
    >
      <Inject services={[DateTime, CandleSeries, LineSeries, StockLegend]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={applData}
          type='Line'
          xName='x'
          yName='close'
          name='AAPL'
          legendShape='Circle'
          fill='#0080ff'
        />
        <StockChartSeriesDirective
          dataSource={googData}
          type='Line'
          xName='x'
          yName='close'
          name='GOOG'
          legendShape='Diamond'
          fill='#ff0080'
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}
```

## Tooltip

Tooltips display point details when users hover over the chart.

### Enabling Tooltip

Enable tooltip by setting `enable` to `true`:

```typescript
import { 
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  Inject,
  DateTime,
  CandleSeries,
  Tooltip
} from '@syncfusion/ej2-react-charts';

function TooltipChart() {
  const stockData = [ /* data */ ];

  return (
    <StockChartComponent
      id='stockchart'
      primaryXAxis={{ valueType: 'DateTime' }}
      tooltip={{ enable: true }}
    >
      <Inject services={[DateTime, CandleSeries, Tooltip]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={stockData}
          type='Candle'
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}
```

**Important:** Inject `Tooltip` module to use tooltip features.

### Tooltip Format Customization

Customize tooltip content with format strings:

```typescript
<StockChartComponent
  tooltip={{ 
    enable: true,
    format: '${series.name} ${point.x}: Open: ${point.open}, Close: ${point.close}'
  }}
>
  {/* ... */}
</StockChartComponent>
```

**Available format tokens:**
- `${series.name}` - Series name
- `${point.x}` - X-axis value (date)
- `${point.y}` - Y-axis value
- `${point.open}` - Open price
- `${point.high}` - High price
- `${point.low}` - Low price
- `${point.close}` - Close price
- `${point.volume}` - Volume

**Examples:**

Simple format:
```typescript
tooltip={{ 
  enable: true,
  format: 'Price: ${point.close}'
}}
```

Detailed format:
```typescript
tooltip={{ 
  enable: true,
  format: '${point.x}<br/>O: ${point.open}<br/>H: ${point.high}<br/>L: ${point.low}<br/>C: ${point.close}'
}}
```

### Tooltip Position

Control tooltip position relative to the mouse:

```typescript
<StockChartComponent
  tooltip={{ 
    enable: true,
    position: 'Nearest'  // Tooltip follows mouse closely
  }}
>
  {/* ... */}
</StockChartComponent>
```

**Position options:**
- `'Auto'` - Positioned automatically (default)
- `'Nearest'` - Stays near the mouse cursor

### Tooltip Appearance

Customize tooltip background, border, and text style:

```typescript
<StockChartComponent
  tooltip={{ 
    enable: true,
    fill: '#333333',  // Background color
    border: {
      width: 2,
      color: '#0080ff'
    },
    textStyle: {
      fontFamily: 'Arial',
      fontSize: '14px',
      fontWeight: 'normal',
      color: '#ffffff'
    }
  }}
>
  {/* ... */}
</StockChartComponent>
```

### Complete Tooltip Example

```typescript
import { 
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  Inject,
  DateTime,
  CandleSeries,
  Tooltip,
  RangeTooltip
} from '@syncfusion/ej2-react-charts';

function StyledTooltipChart() {
  const stockData = [ /* data */ ];

  return (
    <StockChartComponent
      id='stockchart'
      title='Stock Price with Custom Tooltip'
      primaryXAxis={{ valueType: 'DateTime' }}
      tooltip={{
        enable: true,
        shared: false,
        format: '<b>${point.x}</b><br/>Open: <b>${point.open}</b><br/>High: <b>${point.high}</b><br/>Low: <b>${point.low}</b><br/>Close: <b>${point.close}</b>',
        fill: 'rgba(0, 0, 0, 0.8)',
        border: { width: 1, color: '#0080ff' },
        textStyle: {
          fontSize: '12px',
          color: '#ffffff'
        },
        position: 'Nearest'
      }}
    >
      <Inject services={[DateTime, CandleSeries, Tooltip, RangeTooltip]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={stockData}
          type='Candle'
          xName='x'
          high='high'
          low='low'
          open='open'
          close='close'
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}
```

## Crosshair

Crosshair displays vertical and horizontal lines to help users read exact values at the mouse position.

### Enabling Crosshair

Enable crosshair lines:

```typescript
import { 
  StockChartComponent,
  Inject,
  DateTime,
  CandleSeries,
  Crosshair
} from '@syncfusion/ej2-react-charts';

function CrosshairChart() {
  const stockData = [ /* data */ ];

  return (
    <StockChartComponent
      id='stockchart'
      primaryXAxis={{ valueType: 'DateTime' }}
      crosshair={{ enable: true }}
    >
      <Inject services={[DateTime, CandleSeries, Crosshair]} />
      {/* ... series ... */}
    </StockChartComponent>
  );
}
```

**Important:** Inject `Crosshair` module to use crosshair features.

**Line type options:**
```typescript
crosshair={{ 
  enable: true,
  lineType: 'Both'  // 'Vertical', 'Horizontal', or 'Both'
}}
```

### Crosshair Axis Tooltips

Enable axis value tooltips on the crosshair:

```typescript
<StockChartComponent
  primaryXAxis={{ 
    valueType: 'DateTime',
    crosshairTooltip: { enable: true }
  }}
  primaryYAxis={{
    crosshairTooltip: { enable: true }
  }}
  crosshair={{ enable: true }}
>
  {/* ... */}
</StockChartComponent>
```

### Crosshair Customization

Customize crosshair line and tooltip appearance:

```typescript
<StockChartComponent
  primaryXAxis={{ 
    valueType: 'DateTime',
    crosshairTooltip: { 
      enable: true,
      fill: '#0080ff',
      textStyle: {
        color: '#ffffff',
        fontSize: '12px'
      }
    }
  }}
  primaryYAxis={{
    crosshairTooltip: { 
      enable: true,
      fill: '#ff8000',
      textStyle: {
        color: '#ffffff',
        fontSize: '12px'
      }
    }
  }}
  crosshair={{ 
    enable: true,
    line: {
      width: 2,
      color: '#0080ff',
      dashArray: '5,5'  // Dashed line
    } , lineType: 'Both'
  }}
>
  {/* ... */}
</StockChartComponent>
```

**Snap to data:**

Make crosshair snap to nearest data point:

```typescript
<StockChartComponent
  crosshair={{ 
    enable: true,
    snapToData: true  // Snaps to nearest point
  }}
>
  {/* ... */}
</StockChartComponent>
```

### Complete Crosshair Example

```typescript
import { 
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  Inject,
  DateTime,
  CandleSeries,
  Crosshair,
  RangeTooltip
} from '@syncfusion/ej2-react-charts';

function StyledCrosshairChart() {
  const stockData = [ /* data */ ];

  return (
    <StockChartComponent
      id='stockchart'
      title='Stock Price with Crosshair'
      primaryXAxis={{ 
        valueType: 'DateTime',
        crosshairTooltip: { 
          enable: true,
          fill: 'rgba(0, 128, 255, 0.9)',
          textStyle: { color: '#ffffff' }
        }
      }}
      primaryYAxis={{
        crosshairTooltip: { 
          enable: true,
          fill: 'rgba(255, 128, 0, 0.9)',
          textStyle: { color: '#ffffff' }
        }
      }}
      crosshair={{ 
        enable: true,
        lineType: 'Both',
        line: {
          width: 1,
          color: '#0080ff',
          dashArray: '5,5'
        },
        snapToData: true
      }}
    >
      <Inject services={[DateTime, CandleSeries, Crosshair, RangeTooltip]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={stockData}
          type='Candle'
          xName='x'
          high='high'
          low='low'
          open='open'
          close='close'
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}
```

### Trackball (Shared Tooltip)

Trackball shows a shared tooltip across all series at the crosshair position, perfect for multi-series charts:

```typescript
import { 
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  Inject,
  DateTime,
  LineSeries,
  Crosshair,
  Tooltip
} from '@syncfusion/ej2-react-charts';

function TrackballChart() {
  const applData = [ /* AAPL data */ ];
  const googData = [ /* GOOG data */ ];

  return (
    <StockChartComponent
      id='stockchart'
      title='Stock Comparison with Trackball'
      primaryXAxis={{ valueType: 'DateTime' }}
      crosshair={{ enable: true }}
      tooltip={{ 
        enable: true,
        shared: true  // Enables trackball
      }}
    >
      <Inject services={[DateTime, LineSeries, Crosshair, Tooltip]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={applData}
          type='Line'
          xName='x'
          yName='close'
          name='AAPL'
        />
        <StockChartSeriesDirective
          dataSource={googData}
          type='Line'
          xName='x'
          yName='close'
          name='GOOG'
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}
export default TrackballChart;
```

**Key for trackball:**
- `crosshair={{ enable: true }}` - Enables crosshair lines
- `tooltip={{ enable: true, shared: true }}` - Enables shared tooltip (trackball)

## Combining All Interactive Features

Complete example with legend, tooltip, and crosshair:

```typescript
import { 
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  Inject,
  DateTime,
  CandleSeries,
  LineSeries,
  StockLegend,
  Tooltip,
  RangeTooltip,
  Crosshair
} from '@syncfusion/ej2-react-charts';

function FullyInteractiveChart() {
  const stockData = [ /* data */ ];

  return (
    <StockChartComponent
      id='stockchart'
      title='Fully Interactive Stock Chart'
      primaryXAxis={{ 
        valueType: 'DateTime',
        crosshairTooltip: { enable: true }
      }}
      primaryYAxis={{
        crosshairTooltip: { enable: true }
      }}
      legendSettings={{
        visible: true,
        position: 'Bottom'
      }}
      tooltip={{
        enable: true,
        shared: true,
        format: '<b>${point.x}</b><br/>Open: ${point.open}<br/>Close: ${point.close}'
      }}
      crosshair={{
        enable: true,
        lineType: 'Both'
      }}
    >
      <Inject services={[
        DateTime, 
        CandleSeries, 
        LineSeries,
        StockLegend, 
        Tooltip, 
        RangeTooltip,
        Crosshair
      ]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={stockData}
          type='Candle'
          xName='x'
          high='high'
          low='low'
          open='open'
          close='close'
          name='Stock Price'
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}

export default FullyInteractiveChart;
```

## Best Practices

**Legend:**
- Use legend for multiple series comparison
- Keep legend items concise with short names
- Position legend to avoid overlapping chart data
- Use legend template for rich, branded content

**Tooltip:**
- Enable tooltips for all stock charts (essential for detail viewing)
- Format tooltips to show relevant OHLC data
- Use shared tooltips for multi-series charts
- Keep tooltip styling consistent with application theme

**Crosshair:**
- Enable crosshair for precise value reading
- Use axis tooltips to show exact axis values
- Enable snapToData for cleaner point selection
- Combine with trackball for multi-series analysis

**Performance:**
- All three features are lightweight and can be used together
- No performance impact for typical datasets (<10,000 points)
- Consider disabling features on mobile for touch optimization

---

## Mouse and Chart Events

The Stock Chart provides comprehensive mouse and interaction events for tracking user interactions and building custom behaviors.

### Point Interaction Events

#### pointClick
Fired when a data point is clicked.

```typescript
import { StockChartComponent } from '@syncfusion/ej2-react-charts';

function PointClickExample() {
  const handlePointClick = (args) => {
    console.log('Clicked point at:', args.x);
    console.log('Point value:', args.y);
    console.log('Series index:', args.seriesIndex);
    console.log('Point index:', args.pointIndex);
  };

  return (
    <StockChartComponent
      id='stockchart'
      primaryXAxis={{ valueType: 'DateTime' }}
      pointClick={handlePointClick}
    >
      {/* Series configuration */}
    </StockChartComponent>
  );
}
```

**Event Args:**
- `pointIndex: number` — Index of clicked point
- `seriesIndex: number` — Index of clicked series
- `x: Date | number` — X-axis value
- `y: number` — Y-axis value

#### pointMove
Fired when mouse moves over a data point.

```typescript
const handlePointMove = (args) => {
  console.log('Moving over point:', args.x);
  // Update UI based on current point
};

<StockChartComponent pointMove={handlePointMove} />
```

### Mouse Events

Stock Chart provides fine-grained mouse event tracking.

#### stockChartMouseClick
Triggers when clicking on the chart area.

```typescript
const handleMouseClick = (args) => {
  console.log('Chart clicked at coordinates:', args.x, args.y);
};

<StockChartComponent stockChartMouseClick={handleMouseClick} />
```

#### stockChartMouseDown
Triggers on mouse down event.

```typescript
const handleMouseDown = (args) => {
  console.log('Mouse down');
  // Start drag operation or selection
};

<StockChartComponent stockChartMouseDown={handleMouseDown} />
```

#### stockChartMouseUp
Triggers on mouse up event.

```typescript
const handleMouseUp = (args) => {
  console.log('Mouse up');
  // End drag operation or selection
};

<StockChartComponent stockChartMouseUp={handleMouseUp} />
```

#### stockChartMouseMove
Triggers when hovering over the stock chart.

```typescript
const handleMouseMove = (args) => {
  console.log('Mouse position:', args.x, args.y);
  // Update crosshair or overlay based on position
};

<StockChartComponent stockChartMouseMove={handleMouseMove} />
```

#### stockChartMouseLeave
Triggers when cursor leaves the chart area.

```typescript
const handleMouseLeave = (args) => {
  console.log('Mouse left chart');
  // Hide tooltips or reset UI state
};

<StockChartComponent stockChartMouseLeave={handleMouseLeave} />
```

### Combined Mouse Event Example

```typescript
import React, { useState } from 'react';
import { StockChartComponent, StockChartSeriesCollectionDirective,
         StockChartSeriesDirective, Inject, DateTime, CandleSeries,
         Tooltip, RangeTooltip, Crosshair } from '@syncfusion/ej2-react-charts';

function InteractiveChartWithMouseEvents() {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [isHovering, setIsHovering] = useState(false);

  const handleMouseMove = (args) => {
    setMousePosition({ x: args.x, y: args.y });
    setIsHovering(true);
  };

  const handleMouseLeave = () => {
    setIsHovering(false);
  };

  const handlePointClick = (args) => {
    alert(`Clicked: ${args.x}, Value: ${args.y}`);
  };

  return (
    <div>
      <p>Status: {isHovering ? 'Over Chart' : 'Outside Chart'}</p>
      <p>Position: X={mousePosition.x}, Y={mousePosition.y}</p>
      
      <StockChartComponent
        id='stockchart'
        primaryXAxis={{ valueType: 'DateTime' }}
        tooltip={{ enable: true }}
        crosshair={{ enable: true }}
        stockChartMouseMove={handleMouseMove}
        stockChartMouseLeave={handleMouseLeave}
        pointClick={handlePointClick}
      >
        <Inject services={[DateTime, CandleSeries, Tooltip, RangeTooltip, Crosshair]} />
        <StockChartSeriesCollectionDirective>
          <StockChartSeriesDirective
            dataSource={stockData}
            type='Candle'
            xName='x'
            high='high'
            low='low'
            open='open'
            close='close'
          />
        </StockChartSeriesCollectionDirective>
      </StockChartComponent>
    </div>
  );
}

export default InteractiveChartWithMouseEvents;
```

### Legend Events

#### legendClick
Fired when a legend item is clicked (e.g., to toggle series visibility).

```typescript
const handleLegendClick = (args) => {
  console.log('Legend item clicked:', args.legendText);
};

<StockChartComponent legendClick={handleLegendClick} />
```

#### legendRender
Fired when legend items are rendered (for customization).

```typescript
const handleLegendRender = (args) => {
  // Customize legend appearance
  if (args.legendText.includes('AAPL')) {
    args.fill = '#ff0000'; // Red for Apple
  }
};

<StockChartComponent legendRender={handleLegendRender} />
```

### Range Selection Events

#### rangeChange
Emitted when the selected date range changes via period selector or range selector.

```typescript
const handleRangeChange = (args) => {
  console.log('Range changed');
  console.log('Start:', args.start);
  console.log('End:', args.end);
  // Refresh data or update analysis
};

<StockChartComponent rangeChange={handleRangeChange} />
```

### Tooltip Event

#### tooltipRender
Modify tooltip content before display.

```typescript
const handleTooltipRender = (args) => {
  // Customize tooltip text
  args.text = `<b>Price: ${args.text}</b>`;
};

<StockChartComponent tooltipRender={handleTooltipRender} />
```

### Crosshair Event

#### crosshairLabelRender
Triggers before the crosshair tooltip is rendered.

```typescript
const handleCrosshairLabelRender = (args) => {
  // Add custom formatting to crosshair label
  args.text = '$' + parseFloat(args.text).toFixed(2);
};

<StockChartComponent crosshairLabelRender={handleCrosshairLabelRender} />
```

### Best Practices for Events

1. **Event Performance:**
   - Minimize heavy computations in event handlers
   - Use debouncing for high-frequency events like `stockChartMouseMove`
   - Avoid DOM manipulation in real-time events

2. **Event Handling:**
   - Use `stockChartMouseMove` for continuous tracking
   - Use `pointClick` for discrete selections
   - Use `rangeChange` for data filtering/refresh

3. **User Experience:**
   - Provide visual feedback for mouse interactions
   - Use events to update related UI elements
   - Combine multiple events for complex interactions

4. **Common Patterns:**
   - Point selection: Use `pointClick` + `selectedDataIndexes`
   - Range filtering: Use `rangeChange` + `dataSource` update
   - Hover effects: Use `pointMove` + `stockChartMouseLeave`
   - Export on demand: Trigger `export()` method on button click