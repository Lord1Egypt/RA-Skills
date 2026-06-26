---
name: syncfusion-react-stock-chart
description: Implements the Syncfusion React Stock Chart component for visualizing financial and market data. Use this when users need stock price visualization, OHLC charts, candlestick charts, or trading chart interfaces. Supports multiple series types, period selectors, range navigators, technical indicators (e.g., SMA, MACD, Bollinger Bands), and interactive analysis tools for financial data in React applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion React Stock Charts

The Stock Chart component is a specialized financial chart for visualizing stock price movements over time. It provides essential features for financial data analysis including candlestick/OHLC visualization, period selectors for quick date range navigation, range selectors for precise data filtering, technical indicators, and interactive tools like tooltips and crosshair.

## When to Use This Skill

Use this skill when you need to:

- **Visualize financial/stock data** - Display stock prices, trading volumes, market movements
- **Display OHLC data** - Show Open, High, Low, Close values with candlestick or Hilo charts
- **Implement period navigation** - Add quick time range buttons (1D, 5D, 1M, 6M, YTD, 1Y, ALL)
- **Enable range selection** - Allow users to select specific date ranges with thumb navigation
- **Add technical analysis** - Include technical indicators (SMA, EMA, RSI, MACD, etc.)
- **Show stock events** - Visualize earnings, dividends, splits, or other market events
- **Create financial dashboards** - Build comprehensive stock analysis interfaces
- **Display time-series data** - Any datetime-based financial or trading data

## Component Overview

**Package:** `@syncfusion/ej2-react-charts`  
**Component:** `StockChartComponent`  
**Key Features:**
- 6 series types (Line, Spline, Hilo, HiloOpenClose, Candle, Hollow Candle)
- Built-in period selector for quick date range navigation
- Range navigator with thumb controls for precise selection
- Technical indicators (20+ types) and `indicatorType` support
- Stock event annotations (`stockEvents`) and `stockEventRender`
- Interactive tooltip, crosshair (trackball), and legend
- Selection and interaction: `selectionMode`, `isMultiSelect`, `selectedDataIndexes`
- Zooming and panning (`zoomSettings`, `onZooming`)
- Export to image/PDF and print capabilities (`exportType`, `Export`, `Print`)
- Persistence and RTL support (`enablePersistence`, `enableRtl`)
- Responsive and accessible (WCAG, ARIA, keyboard navigation)

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

Read this first for initial setup:
- Installing @syncfusion/ej2-react-charts package
- Project setup with Vite or create-react-app
- Basic StockChartComponent implementation
- Module injection pattern (Inject services)
- Creating first chart with sample data
- Understanding data structure (x, open, high, low, close, volume)
- Adding chart title and basic configuration

### Axis Types and Configuration
📄 **Read:** [references/configuration.md](references/configuration.md)

For configuring and customizing axes:
- **DateTime Axis** - Date/time based x-axis (most common for stock charts)
- **DateTimeCategory Axis** - Business days only (excludes weekends/holidays)
- **Logarithmic Axis** - Logarithmic scale for wide value ranges
- **Numeric Axis** - Standard numeric axis for y-values
- Axis title, labels, and formatting
- Grid lines and tick customization
- Multiple Y-axes for different data scales
- Axis ranges and padding settings

### Series Types and Visualization
📄 **Read:** [references/series-types.md](references/series-types.md)

For choosing and configuring chart series:
- **Line series** - Continuous price lines
- **Spline series** - Smooth curves
- **Hilo series** - High-low range bars
- **HiloOpenClose series** - OHLC bars
- **Candle series** - Traditional candlesticks (default for stock charts)
- **Hollow Candle series** - Filled/hollow based on price movement
- Bear/Bull fill colors for candlesticks
- Series dropdown navigation and type switching
- Module injection for each series type
- When to use each type

### Period and Range Selectors
📄 **Read:** [references/selectors.md](references/selectors.md)

For implementing time range navigation:
- **Period Selector:** Quick navigation buttons (1D, 5D, 1M, etc.)
  - Periods array configuration (interval, text, intervalType)
  - IntervalType options (Years, Months, Weeks, Days, Hours, etc.)
  - Enabling/disabling period selector
- **Range Selector:** Precise range selection with thumbs
  - Thumb navigation and dragging
  - Label tapping for range selection
  - Date range button integration
  - Enabling/disabling range selector

### Interactive Features and Events
📄 **Read:** [references/interactive-features.md](references/interactive-features.md)

For adding user interaction and visual feedback:
- **Legend:** Display series information
  - Position and alignment options (Top, Bottom, Left, Right, Custom)
  - Customization (size, shape, colors, icons)
  - Legend title and template
  - Legend click/render events
- **Tooltip:** Show point data on hover
  - Format customization with tokens (${point.x}, ${point.open}, etc.)
  - Position control (Auto, Nearest)
  - Appearance styling (fill, border, textStyle)
  - Shared tooltips for multi-series
  - Header and custom formatting
- **Crosshair:** Vertical/horizontal lines for precise value reading
  - Crosshair tooltip for axis values on both axes
  - Line customization (width, color, dashArray)
  - Snap to data for cleaner interactions
  - Trackball mode for shared tooltip across series
  - Line type (Both, Vertical, Horizontal)
- **Mouse Events:** Comprehensive interaction tracking
  - pointClick, pointMove for data point interactions
  - stockChartMouseMove, stockChartMouseClick, etc.
  - stockChartMouseLeave for UI cleanup
  - Range change events for selector updates

### Technical Analysis Tools  
📄 **Read:** [references/technical-analysis.md](references/technical-analysis.md)

For financial analysis features:
- **Stock Events:** Annotate significant market events
  - Event types (Flag, Circle, Square, Triangle, etc.)
  - Event markers with customizable colors and shapes
  - Event descriptions and tooltips
  - Events for specific series targeting
  - stockEventRender event for custom styling
  - Event visibility control
- **Technical Indicators:** Add analysis overlays
  - 10+ indicator types:
    - Moving averages: SMA, EMA, TMA
    - Momentum: RSI, MACD, Stochastic, Momentum
    - Volume: Accumulation Distribution, ATR
    - Advanced: Bollinger Bands
  - Indicator configuration and styling
  - Multiple indicators on one chart
  - Field selection (Open, High, Low, Close)
  - Period and standard deviation customization
- **Trend Lines:** Draw trend analysis lines
  - 6 trendline types: Linear, Exponential, Logarithmic, Polynomial, Power, MovingAverage
  - Line configuration (start/end points, series binding)
  - Styling and customization (color, width, dashArray)
  - Multiple trend lines per series
  - Polynomial order customization
  - Moving average period configuration

### Tooltip, Crosshair, and Axis Configuration
📄 **Read:** [references/interactive-features.md](references/interactive-features.md) and [references/configuration.md](references/configuration.md)

For tooltip and crosshair setup:
- **Tooltip Configuration:** Point hover information
  - Enable/disable with `enable` property
  - Format strings for OHLC data display
  - Background color and border styling
  - Text style customization
  - Position modes (Auto, Nearest)
- **Crosshair Lines:** Precise value reading
  - Enable crosshair with `enable: true`
  - Line type: Both, Vertical, or Horizontal
  - Line customization (width, color, dashArray)
  - Snap to data point alignment
  - Crosshair line styling
- **Axis Tooltips:** Display axis values
  - Enable on primaryXAxis via `crosshairTooltip`
  - Enable on primaryYAxis via `crosshairTooltip`
  - Fill color and text style customization
  - Format axis value display

### Chart Configuration and Styling
📄 **Read:** [references/configuration.md](references/configuration.md)

For customizing chart appearance and behavior:
- **Axes Configuration:** Setup X and Y axes
  - Axis types: DateTime (default), DateTimeCategory, Logarithmic, Numeric
  - Label formatting and intervals
  - Multiple axes support with `axes` array
  - Axis ranges, padding, and grid lines
  - Major/minor tick and grid customization
- **Chart Dimensions:** Control size
  - Width and height properties (pixels or percentage)
  - Responsive sizing strategies
  - Container-based sizing
- **Appearance:** Theme and styling
  - Built-in themes (Material, Fabric, Bootstrap, HighContrast, etc.)
  - Background and border customization
  - Chart area styling
  - Margin and padding configuration
  - Title and title styling
- **Gradient Fills:** Advanced styling
  - Linear gradients (x1, y1, x2, y2 stops)
  - Radial gradients (cx, cy, r stops)
  - Gradient for series fill
  - SVG gradient definitions

### Export, Print, and Accessibility
📄 **Read:** [references/utilities.md](references/utilities.md)

For export functionality and accessibility:
- **Export:** Save charts as files
  - Export as PNG, JPEG, SVG
  - Export as PDF
  - Configuration options
- **Print:** Print chart directly
  - Print method and options
- **Accessibility:** WCAG compliance
  - Keyboard navigation
  - ARIA attributes
  - Screen reader support
  - Accessible color schemes

## Quick Start

### Basic Stock Chart

```typescript
import { StockChartComponent, StockChartSeriesCollectionDirective, 
         StockChartSeriesDirective, Inject, DateTime, Tooltip, 
         RangeTooltip, Crosshair, LineSeries, SplineSeries, 
         CandleSeries, HiloOpenCloseSeries, HiloSeries, 
         RangeAreaSeries, Trendlines } from '@syncfusion/ej2-react-charts';
import * as React from 'react';

function App() {
  const data = [
    { x: new Date('2012-04-02'), open: 85.97, high: 90.58, low: 85.97, close: 90.58, volume: 660187068 },
    { x: new Date('2012-04-09'), open: 89.02, high: 92.50, low: 88.50, close: 92.90, volume: 490033264 },
    { x: new Date('2012-04-16'), open: 92.52, high: 93.00, low: 88.50, close: 92.52, volume: 450167016 },
    // ... more data
  ];

  return (
    <StockChartComponent
      id='stockchart'
      title='AAPL Stock Price'
      primaryXAxis={{ valueType: 'DateTime' }}
    >
      <Inject services={[DateTime, Tooltip, RangeTooltip, Crosshair, LineSeries, 
                         SplineSeries, CandleSeries, HiloOpenCloseSeries, HiloSeries, 
                         RangeAreaSeries, Trendlines]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective 
          dataSource={data} 
          type='Candle'
          xName='x'
          high='high' 
          low='low' 
          open='open' 
          close='close'
          volume='volume'
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}

export default App;
```

### Stock Chart with Period Selector

```typescript
import { StockChartComponent, StockChartSeriesCollectionDirective, 
         StockChartSeriesDirective, Inject, DateTime, Tooltip, 
         RangeTooltip, Crosshair, CandleSeries } from '@syncfusion/ej2-react-charts';

function App() {
  const data = [ /* stock data */ ];
  
  const periods = [
    { intervalType: 'Days', interval: 1, text: '1D' },
    { intervalType: 'Days', interval: 5, text: '5D' },
    { intervalType: 'Months', interval: 1, text: '1M' },
    { intervalType: 'Months', interval: 3, text: '3M' },
    { intervalType: 'Months', interval: 6, text: '6M' },
    { intervalType: 'Years', interval: 1, text: '1Y' },
    { text: 'All' }
  ];

  return (
    <StockChartComponent
      id='stockchart'
      title='Stock Analysis'
      primaryXAxis={{ valueType: 'DateTime' }}
      periods={periods}
      enablePeriodSelector={true}
    >
      <Inject services={[DateTime, Tooltip, RangeTooltip, Crosshair, CandleSeries]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective 
          dataSource={data} 
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

## CSS Styling for Stock Chart

For the Stock Chart period selector UI to work properly, you need to include the required CSS stylesheets in your HTML file. Add the following `<link>` tags to the `<head>` section of your `index.html`:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    
    <!-- Syncfusion Tailwind CSS for Stock Chart styling -->
    <link href="https://cdn.syncfusion.com/ej2/33.1.44/tailwind3.css" rel="stylesheet" />
    
    <!-- Bootstrap CSS for additional styling support -->
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet" />
    
    <title>Stock Chart App</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

**Key CSS Stylesheets:**

1. **Syncfusion Tailwind CSS** (`tailwind3.css`) - Required for Stock Chart components
   - Version: 33.1.44 (update to match your Syncfusion version)
   - Provides styling for period selector buttons, range navigator, tooltips, and other UI elements
   - CDN URL: `https://cdn.syncfusion.com/ej2/33.1.44/tailwind3.css`

2. **Bootstrap CSS** - Optional but recommended for additional styling support
   - Version: 3.3.7
   - Provides base styling and layout utilities
   - CDN URL: `https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css`

**Important Notes:**
- Ensure the Syncfusion CSS version matches your `@syncfusion/ej2-react-charts` package version
- If you're using a different theme (Material, Bootstrap, Fabric, HighContrast), use the corresponding CSS file from Syncfusion CDN
- Place these stylesheets before other custom stylesheets to allow proper CSS cascade and overrides
- Without these stylesheets, the period selector buttons, tooltips, and other UI elements may not render correctly

**Alternative CSS URLs by Theme:**
- Material: `https://cdn.syncfusion.com/ej2/33.1.44/material.css`
- Bootstrap: `https://cdn.syncfusion.com/ej2/33.1.44/bootstrap.css`
- Fabric: `https://cdn.syncfusion.com/ej2/33.1.44/fabric.css`
- Tailwind: `https://cdn.syncfusion.com/ej2/33.1.44/tailwind3.css`
- HighContrast: `https://cdn.syncfusion.com/ej2/33.1.44/highcontrast.css`

## Axis Types Reference

Stock Chart supports multiple axis types for different data scenarios:

### DateTime Axis (Default)
Use for date-based stock data:
```typescript
primaryXAxis={{ 
  valueType: 'DateTime',
  majorGridLines: { width: 0 },
  majorTickLines: { color: 'transparent' }
}}
```
**Best for:** Stock price data with dates
**Inject:** `DateTime` module

### DateTimeCategory Axis
Displays only business days (excludes weekends/holidays):
```typescript
primaryXAxis={{ 
  valueType: 'DateTimeCategory',
  majorGridLines: { width: 0 }
}}
```
**Best for:** Business day-only trading data
**Inject:** `DateTimeCategory` module
**Note:** Requires `DateTimeCategory` module import and injection

### Logarithmic Axis
For Y-axis with logarithmic scale (useful for wide value ranges):
```typescript
primaryYAxis={{
  valueType: 'Logarithmic',
  labelFormat: '${value}'
}}
```
**Best for:** Data spanning multiple orders of magnitude
**Inject:** `Logarithmic` module
**Note:** Cannot contain zero or negative values

### Numeric Axis (Y-axis default)
Standard linear numeric scale:
```typescript
primaryYAxis={{
  valueType: 'Double',
  labelFormat: '${value}',
  minimum: 0,
  maximum: 500,
  interval: 50
}}
```
**Best for:** Price values and general Y-axis
**No module injection required** - This is the default

### Multi-Axis Configuration
Use multiple Y-axes for different scales:
```typescript
<StockChartComponent
  primaryXAxis={{ valueType: 'DateTime' }}
  primaryYAxis={{ title: 'Price', labelFormat: '${value}' }}
>
  {/* Additional axes using StockChartAxesDirective */}
  <StockChartAxesDirective>
    <StockChartAxisDirective
      name='volumeAxis'
      opposedPosition={true}
      title='Volume'
      labelFormat='{value}M'
    />
  </StockChartAxesDirective>
  
  {/* Series bind to respective axes */}
  <StockChartSeriesCollectionDirective>
    <StockChartSeriesDirective type='Candle' yAxisName='primaryYAxis' />
    <StockChartSeriesDirective type='Column' yAxisName='volumeAxis' />
  </StockChartSeriesCollectionDirective>
</StockChartComponent>
```

## Common Patterns

### Pattern 1: Financial Dashboard with Multiple Features

```typescript
import { StockChartComponent, StockChartSeriesCollectionDirective, 
         StockChartSeriesDirective, Inject, DateTime, Tooltip, 
         RangeTooltip, Crosshair, CandleSeries, StockLegend, 
         Export, Print } from '@syncfusion/ej2-react-charts';

function FinancialDashboard() {
  const handlePointClick = (args) => {
    console.log(`Point clicked: ${args.x}, Value: ${args.y}`);
  };

  const handleMouseMove = (args) => {
    console.log('Mouse moved over chart');
  };

  const handleRangeChange = (args) => {
    console.log(`Range changed: ${args.start} to ${args.end}`);
  };

  return (
    <StockChartComponent
      id='stockchart'
      title='Comprehensive Stock Analysis'
      primaryXAxis={{ valueType: 'DateTime' }}
      tooltip={{ enable: true, shared: true }}
      crosshair={{ enable: true }}
      legendSettings={{ visible: true }}
      enablePeriodSelector={true}
      enableSelector={true}
      pointClick={handlePointClick}
      stockChartMouseMove={handleMouseMove}
      rangeChange={handleRangeChange}
    >
      <Inject services={[DateTime, Tooltip, RangeTooltip, Crosshair, 
                         CandleSeries, StockLegend, Export, Print]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective 
          dataSource={stockData} 
          type='Candle'
          name='Apple Inc'
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}
```

### Pattern 2: Candlestick with Bear/Bull Colors and Animation

```typescript
function StyledCandleChart() {
  const stockData = [ /* stock data with open, high, low, close */ ];

  return (
    <StockChartComponent
      id='stockchart'
      primaryXAxis={{ valueType: 'DateTime' }}
      primaryYAxis={{ labelFormat: '${value}' }}
    >
      <Inject services={[DateTime, CandleSeries, Tooltip, RangeTooltip]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective 
          dataSource={stockData} 
          type='Candle'
          xName='x'
          open='open'
          high='high'
          low='low'
          close='close'
          bearFillColor='#ef5350'      // Red for downtrend
          bullFillColor='#26a69a'      // Green for uptrend
          animation={{ enable: true, duration: 500 }}
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}
```

### Pattern 3: Technical Analysis Chart

```typescript
function TechnicalAnalysisChart() {
  const indicators = [
    {
      type: 'Sma',
      field: 'Close',
      period: 14,
      fill: 'blue'
    },
    {
      type: 'BollingerBands',
      field: 'Close',
      period: 20,
      standardDeviation: 2,
      upperLine: { color: '#ff0000', width: 1 },
      lowerLine: { color: '#ff0000', width: 1 }
    }
  ];

  return (
    <StockChartComponent
      id='stockchart'
      primaryXAxis={{ valueType: 'DateTime' }}
      indicators={indicators}
    >
      <Inject services={[DateTime, CandleSeries, Tooltip, 
                         LineSeries, RangeTooltip, SmaIndicator, BollingerBands]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective 
          dataSource={stockData} 
          type='Candle'
        />
      </StockChartSeriesCollectionDirective>
      <StockChartIndicatorsDirective>
        {/* Indicators can also be added here via directives */}
      </StockChartIndicatorsDirective>
    </StockChartComponent>
  );
}
```

### Pattern 4: Crosshair with Axis Tooltips

```typescript
function CrosshairChart() {
  return (
    <StockChartComponent
      id='stockchart'
      primaryXAxis={{ 
        valueType: 'DateTime',
        majorGridLines: { width: 0 },
        majorTickLines: { color: 'transparent' },
        crosshairTooltip: { enable: true }  // X-axis tooltip
      }}
      primaryYAxis={{
        labelFormat: 'n0',
        majorTickLines: { width: 0 },
        crosshairTooltip: { enable: true }  // Y-axis tooltip
      }}
      crosshair={{ 
        enable: true,
        lineType: 'Both',
        line: { width: 1, color: '#0080ff' }
      }}
      tooltip={{ enable: true }}
    >
      <Inject services={[DateTime, CandleSeries, Crosshair, Tooltip, RangeTooltip]} />
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

### Pattern 5: Stock Events Visualization

```typescript
function StockEventsChart() {
  const stockEvents = [
    {
      date: new Date('2012-04-01'),
      text: 'Q1 Earnings',
      description: 'Quarterly earnings release',
      type: 'Flag',
      background: '#6c757d'
    },
    {
      date: new Date('2012-07-01'),
      text: 'Dividend',
      description: 'Dividend payout',
      type: 'Circle',
      background: '#28a745'
    }
  ];

  return (
    <StockChartComponent
      id='stockchart'
      primaryXAxis={{ valueType: 'DateTime' }}
      stockEvents={stockEvents}
    >
      <Inject services={[DateTime, SplineSeries, Tooltip]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective 
          dataSource={stockData} 
          type='Spline'
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}
```

### Pattern 6: Export and Print

```typescript
function ExportableChart() {
  const chartRef = useRef<StockChartComponent>(null);

  const handleExport = (type: string) => {
    if (chartRef.current) {
      chartRef.current.export(type, 'StockChart');
    }
  };

  const handlePrint = () => {
    if (chartRef.current) {
      chartRef.current.print();
    }
  };

  return (
    <div>
      <div>
        <button onClick={() => handleExport('PNG')}>Export PNG</button>
        <button onClick={() => handleExport('JPEG')}>Export JPEG</button>
        <button onClick={() => handleExport('SVG')}>Export SVG</button>
        <button onClick={() => handleExport('PDF')}>Export PDF</button>
        <button onClick={handlePrint}>Print Chart</button>
      </div>
      
      <StockChartComponent
        ref={chartRef}
        id='stockchart'
        primaryXAxis={{ valueType: 'DateTime' }}
        exportType={['PNG', 'JPEG', 'SVG', 'PDF']}
      >
        <Inject services={[DateTime, CandleSeries, Export]} />
        <StockChartSeriesCollectionDirective>
          <StockChartSeriesDirective 
            dataSource={stockData} 
            type='Candle'
          />
        </StockChartSeriesCollectionDirective>
      </StockChartComponent>
    </div>
  );
}
```

## Key Props

### StockChartComponent

| Prop | Type | Description |
|------|------|-------------|
| `primaryXAxis` | Object | X-axis configuration (typically DateTime) |
| `primaryYAxis` | Object | Y-axis configuration |
| `axes` | Array | Additional Y-axes for multi-axis scaling |
| `title` | string | Chart title |
| `titleStyle` | Object | Title font styling |
| `periods` | Array | Period selector buttons configuration |
| `enablePeriodSelector` | boolean | Show/hide period selector (default: true) |
| `enableSelector` | boolean | Show/hide range selector (default: true) |
| `enableCustomRange` | boolean | Enable custom date range selection |
| `tooltip` | Object | Tooltip configuration |
| `crosshair` | Object | Crosshair configuration |
| `legendSettings` | Object | Legend configuration |
| `stockEvents` | Array | Stock event markers |
| `indicators` | Array | Technical indicators |
| `height` | string | Chart height |
| `width` | string | Chart width |
| `margin` | Object | Chart margin configuration |
| `chartArea` | Object | Chart area styling |
| `background` | string | Chart background color |
| `border` | Object | Chart border configuration |
| `theme` | string | Chart theme |
| `zoomSettings` | Object | Zoom and pan configuration |
| `rows` | Array | Row definitions for multi-row layouts |
| `selectedDataIndexes` | Array | Programmatically select specific points |
| `selectionMode` | string | Selection mode (None, Point, Series, Cluster, DragXY, DragX, DragY) |
| `isMultiSelect` | boolean | Allow multiple data point selection |
| `exportType` | Array | Export formats (PNG, JPEG, SVG, PDF) |
| `enablePersistence` | boolean | Persist chart state between page reloads |
| `enableRtl` | boolean | Enable right-to-left rendering |
| `locale` | string | Override global culture/localization |
| `noDataTemplate` | string/Function | Template shown when no data available |
| `isTransposed` | boolean | Render chart in transposed manner |
| `seriesType` | Array | Available series types |
| `indicatorType` | Array | Available technical indicator types |
| `trendlineType` | Array | Available trendline types |
| `bearFillColor` | string | Fill color for downtrend (bear) candles |
| `bullFillColor` | string | Fill color for uptrend (bull) candles |
| `animation` | Object | Animation settings for series rendering |
| `pointClick` | Function | Event fired when a data point is clicked |
| `stockChartMouseMove` | Function | Event fired when mouse moves over chart |
| `stockChartMouseClick` | Function | Event fired when chart area is clicked |
| `stockChartMouseDown` | Function | Event fired on mouse down |
| `stockChartMouseUp` | Function | Event fired on mouse up |
| `stockChartMouseLeave` | Function | Event fired when cursor leaves chart |
| `tooltipRender` | Function | Event for customizing tooltip before display |
| `axisLabelRender` | Function | Event for customizing axis labels before rendering |
| `seriesRender` | Function | Event fired when series is rendered |
| `legendClick` | Function | Event fired when legend item is clicked |
| `legendRender` | Function | Event fired when legend items are rendered |
| `crosshairLabelRender` | Function | Event fired before crosshair tooltip is rendered |
| `selectorRender` | Function | Triggered when range selector renders |
| `onZooming` | Function | Event fired during zoom interactions |
| `load` | Function | Lifecycle event fired before chart is loaded |
| `loaded` | Function | Lifecycle event fired after chart is loaded |
| `beforeExport` | Function | Event fired before export operation |
| `stockEventRender` | Function | Customize stock event marker rendering |
| `rows` | Array | Row definitions for multi-row layouts |
| `isTransposed` | boolean | Render chart in transposed manner |
| `trendlines` | Array | Trend line configurations (StockChartTrendlinesDirective) |

### StockChartSeriesDirective

| Prop | Type | Description |
|------|------|-------------|
| `dataSource` | Array | Stock data array |
| `type` | string | Series type (Candle, Line, Spline, Hilo, HiloOpenClose) |
| `xName` | string | Data field for x-axis (date) |
| `high` | string | Data field for high values |
| `low` | string | Data field for low values |
| `open` | string | Data field for open values |
| `close` | string | Data field for close values |
| `volume` | string | Data field for volume values |
| `name` | string | Series name for legend |
| `yName` | string | Data field for y-axis values |
| `yAxisName` | string | Name of Y-axis to bind this series to (for multi-axis) |
| `bearFillColor` | string | Fill color for downtrend candles/bars |
| `bullFillColor` | string | Fill color for uptrend candles/bars |
| `fill` | string | Series color or gradient fill (e.g., 'url(#gradient1)') |
| `width` | number | Line width for series |
| `opacity` | number | Opacity of series (0-1) |
| `border` | Object | Border configuration for series (width, color, dashArray) |
| `marker` | Object | Data point marker configuration (visible, size, shape, fill, border) |
| `animation` | Object | Animation settings (enable, duration, delay) |
| `legendShape` | string | Legend icon shape (Circle, Rectangle, Triangle, Diamond, etc.) |
| `tooltip` | Object | Series-specific tooltip configuration |
| `trendlines` | Array | Trend lines for this series |
| `cornerRadius` | number | Corner radius for rectangular shapes |

## Common Use Cases

1. **Stock Trading Platform** - Display real-time or historical stock prices with candlestick charts
2. **Financial Analytics Dashboard** - Multi-chart layout with technical indicators and events
3. **Portfolio Tracker** - Visualize investment performance over time
4. **Market Research Tool** - Compare multiple stocks with different series types
5. **Trading Algorithm Backtesting** - Visualize strategy results with indicators and trend lines
6. **Economic Data Visualization** - Display time-series financial or economic data
7. **Cryptocurrency Charts** - Track crypto price movements with OHLC data

## Module Injection

Stock Chart requires explicit module injection for features:

```typescript
import { Inject, DateTime, DateTimeCategory, Logarithmic, 
         Tooltip, RangeTooltip, Crosshair, 
         LineSeries, SplineSeries, CandleSeries, HiloOpenCloseSeries, 
         HiloSeries, RangeAreaSeries, StockLegend, Trendlines, Export } from '@syncfusion/ej2-react-charts';
import { EmaIndicator, RsiIndicator, BollingerBands, TmaIndicator, 
         MomentumIndicator, SmaIndicator, AtrIndicator, 
         AccumulationDistributionIndicator, MacdIndicator, 
         StochasticIndicator } from '@syncfusion/ej2-react-charts';

<StockChartComponent>
  <Inject services={[DateTime, Tooltip, RangeTooltip, Crosshair, 
                     CandleSeries, StockLegend, Trendlines, Export,
                     EmaIndicator, SmaIndicator, BollingerBands]} />
</StockChartComponent>
```

**Common modules:**

**Axes:**
- **DateTime** - DateTime axis (required for stock charts)
- **DateTimeCategory** - DateTime category axis for business days only
- **Logarithmic** - Logarithmic scale axis

**UI Features:**
- **Tooltip** - Hover tooltips for data points
- **RangeTooltip** - Range selector tooltips
- **Crosshair** - Crosshair lines with axis tooltips
- **StockLegend** - Legend display for series

**Series Types:**
- **LineSeries, SplineSeries** - Line charts
- **CandleSeries** - Traditional candlestick chart
- **HiloOpenCloseSeries** - OHLC bars
- **HiloSeries** - High-Low bars
- **RangeAreaSeries** - Range area visualization

**Technical Analysis:**
- **Trendlines** - Trend line visualization (Linear, Exponential, Logarithmic, Polynomial, Power, Moving Average)
- **EmaIndicator, SmaIndicator, TmaIndicator** - Moving average indicators
- **RsiIndicator, BollingerBands, MacdIndicator** - Advanced indicators
- **StochasticIndicator, MomentumIndicator, AtrIndicator** - Momentum indicators
- **AccumulationDistributionIndicator** - Volume-based indicator

**Export:**
- **Export** - Export to PNG, JPEG, SVG, PDF

## Event Handling

Stock Chart provides comprehensive event support for tracking user interactions and building custom behaviors:

### Data Point Events

```typescript
// Point click event
const handlePointClick = (args) => {
  console.log('Point clicked:', args.pointIndex, args.seriesIndex);
  console.log('X:', args.x, 'Y:', args.y);
};

// Point move event (hover)
const handlePointMove = (args) => {
  console.log('Hovering over point:', args.x);
};

<StockChartComponent
  pointClick={handlePointClick}
  pointMove={handlePointMove}
>
  {/* ... */}
</StockChartComponent>
```

### Mouse Events

```typescript
// Various mouse tracking events
const handleMouseMove = (args) => {
  console.log('Mouse position:', args.x, args.y);
};

const handleMouseLeave = (args) => {
  console.log('Mouse left chart area');
};

const handleMouseClick = (args) => {
  console.log('Chart clicked');
};

<StockChartComponent
  stockChartMouseMove={handleMouseMove}
  stockChartMouseLeave={handleMouseLeave}
  stockChartMouseClick={handleMouseClick}
  stockChartMouseDown={(args) => console.log('Mouse down')}
  stockChartMouseUp={(args) => console.log('Mouse up')}
>
  {/* ... */}
</StockChartComponent>
```

### Range and Selector Events

```typescript
// Range change event (period selector or range selector)
const handleRangeChange = (args) => {
  console.log('Range changed:', args.start, 'to', args.end);
  // Refresh data or update analysis
};

<StockChartComponent
  rangeChange={handleRangeChange}
>
  {/* ... */}
</StockChartComponent>
```

### Legend Events

```typescript
// Legend click event
const handleLegendClick = (args) => {
  console.log('Legend item clicked:', args.legendText);
};

// Legend render event (for customization)
const handleLegendRender = (args) => {
  if (args.legendText === 'AAPL') {
    args.fill = '#ff0000'; // Customize legend color
  }
};

<StockChartComponent
  legendClick={handleLegendClick}
  legendRender={handleLegendRender}
>
  {/* ... */}
</StockChartComponent>
```

### Tooltip Events

```typescript
// Customize tooltip before rendering
const handleTooltipRender = (args) => {
  args.text = `<b>Stock Price: ${args.text}</b>`;
};

<StockChartComponent
  tooltip={{ enable: true }}
  tooltipRender={handleTooltipRender}
>
  {/* ... */}
</StockChartComponent>
```

### Stock Event Rendering

```typescript
// Customize stock event markers
const handleStockEventRender = (args) => {
  // Customize event styling, position, etc.
  if (args.text === 'Earnings') {
    args.background = '#ff0000'; // Custom color for earnings
  }
};

<StockChartComponent
  stockEvents={stockEvents}
  stockEventRender={handleStockEventRender}
>
  {/* ... */}
</StockChartComponent>
```

### Lifecycle Events

```typescript
// Load event (before rendering)
const handleLoad = (args) => {
  console.log('Chart loading');
};

// Loaded event (after rendering)
const handleLoaded = (args) => {
  console.log('Chart loaded');
};

<StockChartComponent
  load={handleLoad}
  loaded={handleLoaded}
>
  {/* ... */}
</StockChartComponent>
```

## API Reference

Below is a concise API reference derived from the official Syncfusion `StockChart` API. Include or expand these entries in `references/*` as needed.

**Complete API Documentation:**
- **Full Comprehensive API Reference:** [references/complete-api-reference.md](references/complete-api-reference.md) - Master reference with all props, methods, events, directives, and modules
- **Concise API Summary:** [references/api.md](references/api.md) - Quick reference for commonly used APIs
- **Official Syncfusion Docs:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default

### Selected Props (StockChartComponent)
All props with official API links: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel

**Data & Series:**
- `dataSource` (Array | DataManager) — Source data for series (objects with `x, open, high, low, close, volume`). API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#datasource
- `series` / `StockChartSeriesCollectionDirective` — Series definitions and types (Candle, Line, Spline, Hilo, HiloOpenClose). API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockSeries-model

**Axes:**
- `primaryXAxis` (Object) — X axis configuration (typically `valueType: 'DateTime'` | `'DateTimeCategory'` | `'Numeric'`). Supports `crosshairTooltip`, `majorGridLines`, `majorTickLines`. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartAxis-model
- `primaryYAxis` (Object) — Y axis configuration (typically `valueType: 'Double'` or `'Logarithmic'`). Supports `labelFormat`, `rangePadding`, `minorGridLines`, `crosshairTooltip`. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartAxis-model
- `axes` (Array) — Additional Y-axes for multi-series scaling (use `StockChartAxesDirective` with `StockChartAxisDirective`). API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#axes

**Navigation & Selectors:**
- `periods` (Array) — Period selector buttons (objects with `intervalType`, `interval`, `text`). API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#periods
- `enablePeriodSelector` (boolean) — Toggle period selector visibility (default: true). API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#enableperiodselector
- `enableSelector` (boolean) — Toggle range selector (thumbs) visibility (default: true). API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#enableselector
- `enableCustomRange` (boolean) — Enable custom range selection mode. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#enablecustomrange

**Analysis & Events:**
- `indicators` (Array) — Technical indicators configuration (SMA, EMA, RSI, MACD, Bollinger, etc.). API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartIndicatorModel
- `stockEvents` (Array) — Stock event markers (date, text, description, type, background). API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockEventModel

**Interaction & UI:**
- `tooltip` (Object) — Tooltip settings (`enable`, `format`, `shared`). API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartTooltipSettingsModel
- `crosshair` (Object) — Crosshair settings (`enable`, `lineType`). API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/crosshairSettingsModel
- `legendSettings` (Object) — Legend display and templates. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartLegendSettingsModel

**Selection & Appearance:**
- `selectedDataIndexes` (Array) — Programmatically set selected data points. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#selecteddataindexes
- `selectionMode` (string) — Selection mode (None, Point, Series). API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#selectionmode
- `isMultiSelect` (boolean) — Allow multiple data point selection. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#ismultiselect

**Theming & Layout:**
- `theme` (string) — Chart theme (Material, Bootstrap, Fabric, Tailwind, HighContrast, etc.). API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#theme
- `background` (string) — Chart background color. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#background
- `border` (Object) — Chart border configuration. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartBorderModel
- `chartArea` (Object) — Chart area styling. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartAreaModel
- `margin` (Object) — Chart margin configuration. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockMarginModel
- `title` (string) — Chart title. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#title
- `titleStyle` (Object) — Title font styling. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartFontModel
- `width`, `height` (string) — Dimensions. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#width

**Export & Persistence:**
- `exportType` (Array) — Export formats available in toolbar ['PNG', 'JPEG', 'SVG', 'PDF']. Set empty array `[]` to disable export. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#exporttype
- `enablePersistence` (boolean) — Persist chart state between page loads. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#enablepersistence

**Series & Analysis:**
- `series` / `StockChartSeriesCollectionDirective` — Series collection with StockChartSeriesDirective items. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockSeries-model
- `indicators` / `StockChartIndicatorsDirective` — Technical indicators collection with StockChartIndicatorDirective items. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartIndicatorModel
- `trendlines` / `StockChartTrendlinesDirective` — Trend lines collection with StockChartTrendlineDirective items. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartTrendlineModel

**Accessibility & RTL:**
- `enableRtl` (boolean) — Enable right-to-left rendering. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#enablertl

**Zoom & Pan:**
- `zoomSettings` (Object) — Zoom and pan configuration. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/zoomSettingsModel

### Methods
All methods with official API links: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#methods

- `export(type: string, fileName: string)` — Export chart as PNG, JPEG, SVG, or PDF. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#export
- `print()` — Print the chart to a printer or PDF. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#print
- `destroy()` — Clean up and remove the chart instance. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#destroy
- `getModuleName()` — Returns the component module name. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#getmodulename
- `renderPeriodSelector()` — Programmatically render the period selector. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#renderperiodselector
- `rangeChanged(start: Date | number, end: Date | number)` — Programmatically change the visible range. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#rangechanged

### Events
All events with official API links: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#events

**Lifecycle Events:**
- `load` — Fired before chart is loaded. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#load
- `loaded` — Fired after chart is loaded. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#loaded

**Data & Rendering Events:**
- `axisLabelRender` — Customize each axis label before rendering. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#axislabelrender
- `seriesRender` — Fired when a series is rendered. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#seriesrender
- `beforeExport` — Fired before export operation. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#beforeexport

**User Interaction Events:**
- `pointClick` — Fired when a data point is clicked. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#pointclick
- `pointMove` — Fired when mouse moves over a data point. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#pointmove
- `legendClick` — Fired when a legend item is clicked. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#legendclick
- `legendRender` — Fired when legend items are rendered. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#legendrender

**Tooltip & Crosshair Events:**
- `tooltipRender` — Modify tooltip content before display. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#tooltiprender

**Range & Selector Events:**
- `rangeChange` / `onRangeChange` — Emitted when the selected range changes. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#rangechange
- `selectorRender` — Triggered when range selector renders. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#selectorrender

**Technical Analysis Events:**
- `stockEventRender` — Customize stock event marker rendering. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#stockeventrender
- `onZooming` — Fired during zoom interactions. API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#onzooming

### Suggested reference files and sections
- `references/api.md` — Full API surface summary (props, methods, events) with links to official docs.
- `references/configuration.md` — Move/expand prop-specific docs (axes, theme, sizing).
- `references/interactive-features.md` — Add event hooks and examples for `tooltipRender`, `pointClick`, `axisLabelRender`.
- `references/technical-analysis.md` — Expand `indicators` and `stockEvents` API samples.

### Minimal API example (props + events)

```tsx
<StockChartComponent
  id="stockchart"
  dataSource={data}
  primaryXAxis={{ valueType: 'DateTime' }}
  enablePeriodSelector={true}
  indicators={[{ type: 'Sma', period: 14 }]}
  stockEvents={[{ date: new Date(2023,0,1), text: 'Earnings' }]}
  tooltip={{ enable: true }}
  crosshair={{ enable: true }}
  load={(args) => console.log('loading', args)}
  loaded={(args) => console.log('loaded', args)}
  axisLabelRender={(args) => {/* modify labels */}}
  pointClick={(args) => {/* handle point click */}}
>
  <Inject services={[DateTime, CandleSeries, Tooltip, Crosshair]} />
  <StockChartSeriesCollectionDirective>
    <StockChartSeriesDirective type="Candle" xName="x" open="open" high="high" low="low" close="close" />
  </StockChartSeriesCollectionDirective>
</StockChartComponent>
```
