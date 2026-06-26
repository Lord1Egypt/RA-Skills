````markdown
# Complete Stock Chart API Reference Guide

Comprehensive master reference for all Syncfusion React Stock Chart APIs, including all properties, methods, events, directives, and related components with official documentation links.

**Official API Documentation:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default

## Table of contents

- [Main Component](#main-component)
  - [StockChartComponent](#stockchartcomponent)
- [Props by Category](#props-by-category)
  - [Data & Series Props](#data--series-props)
    - [dataSource](#datasource)
    - [series](#series)
  - [Axis Props](#axis-props)
    - [primaryXAxis](#primaryxaxis)
    - [primaryYAxis](#primaryyaxis)
    - [axes](#axes)
  - [Navigation & Selection Props](#navigation--selection-props)
    - [periods](#periods)
    - [enablePeriodSelector](#enableperiodselector)
    - [enableSelector](#enableselector)
    - [enableCustomRange](#enablecustomrange)
    - [selectedDataIndexes](#selecteddataindexes)
    - [selectionMode](#selectionmode)
    - [isMultiSelect](#ismultiselect)
  - [Technical Analysis Props](#technical-analysis-props)
    - [indicators](#indicators)
    - [stockEvents](#stockevents)
  - [Interaction Props](#interaction-props)
    - [tooltip](#tooltip)
    - [crosshair](#crosshair)
    - [legendSettings](#legendsettings)
  - [Appearance Props](#appearance-props)
    - [title](#title)
    - [titleStyle](#titlestyle)
    - [theme](#theme)
    - [background](#background)
    - [border](#border)
    - [chartArea](#chartarea)
    - [margin](#margin)
  - [Sizing Props](#sizing-props)
    - [width](#width)
    - [height](#height)
  - [Export & Persistence Props](#export--persistence-props)
    - [exportType](#exporttype)
    - [enablePersistence](#enablepersistence)
  - [Accessibility & Localization Props](#accessibility--localization-props)
    - [enableRtl](#enablertl)
  - [Advanced Props](#advanced-props)
    - [rows](#rows)
    - [zoomSettings](#zoomsettings)
    - [annotations](#annotations)
    - [noDataTemplate](#nodatatemplate)
    - [locale](#locale)
    - [isTransposed](#istransposed)
    - [seriesType](#seriestype)
    - [indicatorType](#indicatortype)
    - [trendlineType](#trendlinetype)
    - [stockLegendModule](#stocklegendmodule)
- [Methods](#methods)
  - [export()](#export)
  - [print()](#print)
  - [destroy()](#destroy)
  - [getModuleName()](#getmodulename)
  - [rangeChanged()](#rangechanged)
  - [renderPeriodSelector()](#renderperiodselector)
- [Events](#events)
  - [Lifecycle Events](#lifecycle-events)
    - [load](#load)
    - [loaded](#loaded)
  - [Data & Rendering Events](#data--rendering-events)
    - [axisLabelRender](#axislabelrender)
    - [crosshairLabelRender](#crosshairlabelrender)
    - [seriesRender](#seriesrender)
    - [beforeExport](#beforeexport)
  - [User Interaction Events](#user-interaction-events)
    - [pointClick](#pointclick)
    - [pointMove](#pointmove)
  - [Mouse & Chart Events](#mouse--chart-events)
    - [stockChartMouseClick](#stockchartmouseclick)
    - [stockChartMouseDown](#stockchartmousedown)
    - [stockChartMouseLeave](#stockchartmouseleave)
    - [stockChartMouseMove](#stockchartmousemove)
    - [stockChartMouseUp](#stockchartmouseup)
  - [Legend Events](#legend-events)
    - [legendClick](#legendclick)
    - [legendRender](#legendrender)
  - [Tooltip & Crosshair Events](#tooltip--crosshair-events)
    - [tooltipRender](#tooltiprender)
  - [Range & Selector Events](#range--selector-events)
    - [rangeChange](#rangechange)
    - [selectorRender](#selectorrender)
  - [Technical Analysis Events](#technical-analysis-events)
    - [stockEventRender](#stockeventrender)
    - [onZooming](#onzooming)
- [Directives](#directives)
  - [StockChartSeriesCollectionDirective / StockChartSeriesDirective](#stockchartseriescollectiondirective--stockchartseriesdirective)
  - [StockChartIndicatorsDirective / StockChartIndicatorDirective](#stockchartindicatorsdirective--stockchartindicatordirective)
  - [Stock Events (Prop-based, Not a Directive)](#stock-events-prop-based-not-a-directive)
  - [StockChartTrendlinesDirective / StockChartTrendlineDirective](#stockcharttrendlinesdirective--stockcharttrendlinedirective)
  - [StockChartAxesDirective / StockChartAxisDirective](#stockchartaxesdirective--stockchartaxisdirective)
  - [StockChartRowsDirective / StockChartRowDirective](#stockchartrowsdirective--stockchartrowdirective)
- [Models & Interfaces](#models--interfaces)
  - [StockSeriesModel](#stockseriesmodel)
  - [StockChartAxisModel](#stockchartaxismodel)
  - [StockChartIndicatorModel](#stockchartindicatormodel)
  - [StockEventModel](#stockeventmodel)
- [Modules to Inject](#modules-to-inject)
  - [Essential Modules](#essential-modules)
  - [Axis Module](#axis-module)
  - [Series Type Modules](#series-type-modules)
  - [Interaction Modules](#interaction-modules)
  - [Technical Indicator Modules](#technical-indicator-modules)
  - [Export & Print Modules](#export--print-modules)
  - [Complete Module Injection](#complete-module-injection)
- [Common Patterns](#common-patterns)
  - [1. Basic Stock Chart with Candle Series](#1-basic-stock-chart-with-candle-series)
  - [2. Stock Chart with Multiple Series and Comparison](#2-stock-chart-with-multiple-series-and-comparison)
  - [3. Stock Chart with Technical Indicators](#3-stock-chart-with-technical-indicators)
  - [4. Stock Chart with Events, Export, and Print](#4-stock-chart-with-events-export-and-print)
- [API Quick Links](#api-quick-links)
- [Last Updated](#last-updated)


## Main Component

### StockChartComponent

**Package:** `@syncfusion/ej2-react-charts`  
**Class:** `StockChartComponent`  
**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel

Main component that renders the Stock Chart UI and manages all functionality.

**Basic Import:**
```typescript
import { StockChartComponent } from '@syncfusion/ej2-react-charts';
```

**Usage:**
```typescript
<StockChartComponent
  id='stockchart'
  title='Stock Analysis'
  primaryXAxis={{ valueType: 'DateTime' }}
>
  <Inject services={[DateTime, CandleSeries, Tooltip]} />
  {/* Series, indicators, events, etc. */}
</StockChartComponent>
```

---

## Props by Category

### Data & Series Props

#### dataSource
- **Type:** `Object[] | DataManager | IDataOptions`
- **Default:** `[]`
- **Description:** Source data for the chart. Array of objects with x, open, high, low, close, volume fields.
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#datasource

```typescript
dataSource={[
  { x: new Date('2012-04-02'), open: 320.71, high: 324.07, low: 317.74, close: 323.78, volume: 45638000 },
  { x: new Date('2012-04-03'), open: 323.03, high: 324.30, low: 319.64, close: 321.63, volume: 40857000 }
]}
```

#### series
- **Type:** `StockSeriesModel[]`
- **Description:** Array of series definitions using `StockChartSeriesCollectionDirective`
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#series

```typescript
<StockChartSeriesCollectionDirective>
  <StockChartSeriesDirective type='Candle' dataSource={data} />
</StockChartSeriesCollectionDirective>
```

### Axis Props

#### primaryXAxis
- **Type:** `StockChartAxisModel`
- **Description:** Primary X-axis configuration (typically DateTime for stock charts)
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartAxis-model

```typescript
primaryXAxis={{
  valueType: 'DateTime',
  title: 'Trading Date',
  labelFormat: 'MMM dd, yyyy'
}}
```

**Key sub-properties:**
- `valueType: 'DateTime' | 'Numeric' | 'Logarithmic' | 'Category'` — Axis type
- `title: string` — Axis title
- `labelFormat: string` — Date/number format (e.g., 'MMM dd, yyyy')
- `interval: number` — Interval between labels
- `intervalType: 'Auto' | 'Years' | 'Months' | 'Days' | 'Hours' | 'Minutes'` — Interval type
- `majorGridLines: { width, color, dashArray }` — Grid line styling
- `titleStyle: { fontFamily, fontSize, fontWeight, color }` — Title styling
- `crosshairTooltip: { enable: boolean }` — Enable/disable crosshair tooltip
- API Reference: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartAxis-model

#### primaryYAxis
- **Type:** `StockChartAxisModel`
- **Description:** Primary Y-axis configuration (usually for price values)
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartAxis-model

```typescript
primaryYAxis={{
  labelFormat: '${value}',
  title: 'Price (USD)',
  minimum: 300,
  maximum: 400,
  interval: 20
}}
```

**Key sub-properties:**
- `labelFormat: string` — Value format (e.g., '${value}', '{value}%')
- `minimum: number` — Minimum axis value
- `maximum: number` — Maximum axis value
- `interval: number` — Interval between ticks
- `rangePadding: 'None' | 'Normal' | 'Additional' | 'Round' | 'Auto'` — Axis padding
- API Reference: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartAxis-model

#### axes
- **Type:** `StockChartAxisModel[]`
- **Description:** Array of additional axes for multi-axis scenarios
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#axes

```typescript
<StockChartAxesDirective>
  <StockChartAxisDirective name='volumeAxis' opposedPosition={true} />
</StockChartAxesDirective>
```

### Navigation & Selection Props

#### periods
- **Type:** `PeriodsModel[]`
- **Description:** Array of period selector button configurations
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#periods

```typescript
import { type PeriodsModel } from '@syncfusion/ej2-react-charts';
periods={[
  { intervalType: 'Days', interval: 1, text: '1D' },
  { intervalType: 'Months', interval: 1, text: '1M' },
  { text: 'All' }
]}
```

**Period properties:**
- `interval: number` — Count value
- `intervalType: string` — 'Years' | 'Months' | 'Weeks' | 'Days' | 'Hours' | 'Minutes'
- `text: string` — Button label

#### enablePeriodSelector
- **Type:** `boolean`
- **Default:** `true`
- **Description:** Show/hide period selector buttons
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#enableperiodselector

```typescript
enablePeriodSelector={true}
```

#### enableSelector
- **Type:** `boolean`
- **Default:** `true`
- **Description:** Show/hide range selector (thumbs)
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#enableselector

```typescript
enableSelector={true}
```

#### enableCustomRange
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Enable custom date range selection
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#enablecustomrange

```typescript
enableCustomRange={true}
```

#### selectedDataIndexes
- **Type:** `StockChartIndexesModel[][]`
- **Description:** Programmatically select specific data points
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#selecteddataindexes

```typescript
selectedDataIndexes={[[0], [5], [10]]}
```

#### selectionMode
- **Type:** `'None' | 'Point' | 'Series'`
- **Default:** `'None'`
- **Description:** Enable data point selection mode
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#selectionmode

```typescript
selectionMode='Point'
```

#### isMultiSelect
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Allow multiple data points to be selected simultaneously
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#ismultiselect

```typescript
isMultiSelect={true}
```

### Technical Analysis Props

#### indicators
- **Type:** `StockChartIndicatorModel[]`
- **Description:** Array of technical indicators (SMA, EMA, RSI, MACD, etc.)
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartIndicatorModel

```typescript
<StockChartIndicatorsDirective>
  <StockChartIndicatorDirective type='Sma' period={20} field='Close' />
  <StockChartIndicatorDirective type='Ema' period={50} field='Close' />
</StockChartIndicatorsDirective>
```

**Indicator properties:**
- `type: string` — Indicator type (Sma, Ema, Rsi, Macd, BollingerBands, Tma, Momentum, Stochastic, Atr, AccumulationDistribution)
- `field: string` — Data field to apply indicator (typically 'Close')
- `seriesName: string` — Series name to apply indicator to
- `period: number` — Calculation period
- `fill: string` — Indicator line color
- API Reference: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartIndicatorModel

#### stockEvents
- **Type:** `StockEventModel[]`
- **Description:** Array of stock event markers (earnings, dividends, splits, etc.) passed directly as a prop
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockEventModel

```typescript
<StockChartComponent
  stockEvents={[
    {
      date: new Date('2012-02-01'),
      text: 'Q1',
      description: 'Q1 Earnings',
      type: 'Flag',
      background: '#6c757d',
      border: { color: '#6c757d' },
      seriesIndexes: [0]
    },
    {
      date: new Date('2012-03-15'),
      text: 'Earnings',
      description: 'Earnings announcement',
      type: 'Circle',
      background: '#f48a21',
      textStyle: { color: 'white' },
      seriesIndexes: [0]
    }
  ]}
>
  {/* Series and other config */}
</StockChartComponent>
```

**Stock Event properties:**
- `date: Date` — Event date (required)
- `text: string` — Event label (required)
- `description: string` — Tooltip description
- `type: string` — Marker type (Flag, Circle, Square, Triangle, InvertedTriangle, ArrowUp, ArrowDown, Pin, Text)
- `background: string` — Marker color
- `border: { color: string, width?: number }` — Border styling
- `textStyle: { color: string }` — Text color styling
- `seriesIndexes: number[]` — Optional: limit event to specific series indices
- `showOnSeries: boolean` — Optional: show marker on series or above chart
- API Reference: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockEventModel

### Interaction Props

#### tooltip
- **Type:** `StockTooltipSettingsModel`
- **Description:** Tooltip configuration for data points
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartTooltipSettingsModel

```typescript
tooltip={{
  enable: true,
  shared: true,
  format: '<b>${point.x}</b><br/>O: ${point.open} C: ${point.close}'
}}
```

**Tooltip properties:**
- `enable: boolean` — Enable/disable tooltips
- `shared: boolean` — Show shared tooltip across series (trackball)
- `format: string` — Format string with ${} tokens
- `position: 'Auto' | 'Nearest'` — Tooltip position
- `fill: string` — Background color
- `border: { width, color }` — Border styling
- `textStyle: { fontFamily, fontSize, color }` — Text styling
- API Reference: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartTooltipSettingsModel

**Format tokens:**
- `${series.name}` — Series name
- `${point.x}` — X-value (date)
- `${point.y}` — Y-value
- `${point.open}` — Open price
- `${point.high}` — High price
- `${point.low}` — Low price
- `${point.close}` — Close price
- `${point.volume}` — Volume

#### crosshair
- **Type:** `CrosshairSettingsModel`
- **Description:** Crosshair lines and trackball configuration
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/chart/crosshairSettings

```typescript
crosshair={{
  enable: true,
  lineType: 'Both',
  snapToData: true
}}
```

**Crosshair properties:**
- `enable: boolean` — Enable/disable crosshair
- `lineType: 'Vertical' | 'Horizontal' | 'Both'` — Crosshair line type
- `snapToData: boolean` — Snap to nearest data point
- `line: { width, color, dashArray }` — Line styling
- API Reference: https://ej2.syncfusion.com/react/documentation/api/chart/crosshairSettings

#### legendSettings
- **Type:** `StockChartLegendSettingsModel`
- **Description:** Legend display and styling
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartLegendSettingsModel

```typescript
legendSettings={{
  visible: true,
  position: 'Bottom',
  alignment: 'Center',
  shapeHeight: 12,
  shapeWidth: 12
}}
```

**Legend properties:**
- `visible: boolean` — Show/hide legend
- `position: 'Bottom' | 'Top' | 'Left' | 'Right' | 'Custom'` — Legend position
- `alignment: 'Near' | 'Center' | 'Far'` — Legend alignment
- `shapeHeight: number` — Icon height
- `shapeWidth: number` — Icon width
- `width: string` — Legend width
- `height: string` — Legend height
- `title: string` — Legend title
- `titlePosition: 'Top' | 'Left' | 'Right'` — Title position
- API Reference: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartLegendSettingsModel

### Appearance Props

#### title
- **Type:** `string`
- **Description:** Chart title
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#title

```typescript
title='AAPL Stock Price Analysis'
```

#### titleStyle
- **Type:** `StockChartFontModel`
- **Description:** Title font and styling
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartFontModel

```typescript
titleStyle={{
  fontFamily: 'Arial',
  fontSize: '18px',
  fontWeight: 'bold',
  color: '#333333'
}}
```

#### theme
- **Type:** `'Material' | 'MaterialDark' | 'Fabric' | 'FabricDark' | 'Bootstrap' | 'Bootstrap4' | 'BootstrapDark' | 'HighContrast' | 'HighContrastLight' | 'Tailwind' | 'TailwindDark'`
- **Default:** `'Material'`
- **Description:** Chart theme
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#theme

```typescript
theme='Material'
```

#### background
- **Type:** `string`
- **Description:** Chart background color
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#background

```typescript
background='#f9f9f9'
```

#### border
- **Type:** `StockChartBorderModel`
- **Description:** Chart border configuration
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartBorderModel

```typescript
border={{
  width: 2,
  color: '#cccccc'
}}
```

#### chartArea
- **Type:** `StockChartAreaModel`
- **Description:** Chart plotting area styling
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartAreaModel

```typescript
chartArea={{
  background: '#ffffff',
  border: { width: 1, color: '#e0e0e0' }
}}
```

#### margin
- **Type:** `StockMarginModel`
- **Description:** Chart margins
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockMarginModel

```typescript
margin={{
  left: 40,
  right: 40,
  top: 40,
  bottom: 40
}}
```

### Sizing Props

#### width
- **Type:** `string | number`
- **Default:** Window width
- **Description:** Chart width (e.g., '100%', '800px')
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#width

```typescript
width='100%'
width='1200px'
```

#### height
- **Type:** `string | number`
- **Default:** `450px`
- **Description:** Chart height
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#height

```typescript
height='500px'
height='80%'
```

### Export & Persistence Props

#### exportType
- **Type:** `('PNG' | 'JPEG' | 'SVG' | 'PDF')[]`
- **Default:** `['PNG', 'JPEG', 'SVG', 'PDF']`
- **Description:** Available export formats
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#exporttype

```typescript
exportType={['PNG', 'PDF']}  // Only PNG and PDF
exportType={[]}  // Disable export
```

#### enablePersistence
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Persist chart state (zoom, range, etc.) between page reloads
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#enablepersistence

```typescript
enablePersistence={true}
```

### Accessibility & Localization Props

#### enableRtl
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Enable right-to-left rendering for RTL languages
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#enablertl

```typescript
enableRtl={true}
```

### Advanced Props

#### rows
- **Type:** `StockChartRowModel[]`
- **Description:** Define multiple rows for multi-pane layouts
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartRowModel

```typescript
<StockChartRowsDirective>
  <StockChartRowDirective height='60%' />
  <StockChartRowDirective height='40%' />
</StockChartRowsDirective>
```

#### zoomSettings
- **Type:** `ZoomSettingsModel`
- **Description:** Zoom and pan configuration
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/zoomSettingsModel

```typescript
zoomSettings={{
  enableMouseWheelZooming: true,
  enableSelectionZooming: true,
  enableDeferredZooming: true
}}
```

#### annotations
- **Type:** `StockChartAnnotationSettingsModel[]`
- **Description:** Chart annotations and drawings
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartAnnotationSettingsModel

```typescript
<StockChartAnnotationsDirective>
  <StockChartAnnotationSettive x='2012-02-02' y={95} content='Event' />
</StockChartAnnotationsDirective>
```

#### noDataTemplate
- **Type:** `string | Function`
- **Description:** Template/content shown when no data is available
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#nodatatemplate

```typescript
noDataTemplate='No data available'
noDataTemplate={() => <div>Loading data...</div>}
```

#### locale
- **Type:** `string`
- **Default:** `'en-US'`
- **Description:** Overrides global culture and localization value for this component
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#locale

```typescript
locale='fr-FR'  // Use French locale
locale='de-DE'  // Use German locale
locale='ja-JP'  // Use Japanese locale
```

#### isTransposed
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Specifies whether the stockChart should render in transposed manner
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#istransposed

```typescript
isTransposed={true}
```

#### seriesType
- **Type:** `ChartSeriesType[]`
- **Description:** Types of series available in financial chart
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#seriestype

Supported series types:
- `Candle` — Candlestick series (default for stock charts)
- `Line` — Line series
- `Spline` — Spline/smooth curve series
- `Hilo` — High-Low range series
- `HiloOpenClose` — OHLC bars series
- `RangeArea` — Range area series

#### indicatorType
- **Type:** `TechnicalIndicators[]`
- **Description:** Types of technical indicators available
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#indicatortype

Supported indicator types:
- `Sma` — Simple Moving Average
- `Ema` — Exponential Moving Average
- `Rsi` — Relative Strength Index
- `Macd` — MACD (Moving Average Convergence Divergence)
- `BollingerBands` — Bollinger Bands
- `Tma` — Triangular Moving Average
- `Momentum` — Momentum indicator
- `Stochastic` — Stochastic indicator
- `Atr` — Average True Range
- `AccumulationDistribution` — Accumulation Distribution

#### trendlineType
- **Type:** `TrendlineTypes[]`
- **Description:** Types of trendlines supported for series analysis
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#trendlinetype

Supported trendline types:
- `Linear` — Linear trend line
- `Exponential` — Exponential trend line
- `Logarithmic` — Logarithmic trend line
- `Polynomial` — Polynomial trend line
- `Power` — Power trend line
- `MovingAverage` — Moving average trend line

#### stockLegendModule
- **Type:** `any`
- **Description:** Internal stock legend module reference (used internally)
- **Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#stocklegendmodule

---

## Methods

All methods are called on the component reference.

### export()

Export chart to file (PNG, JPEG, SVG, or PDF).

**Signature:**
```typescript
export(type: 'PNG' | 'JPEG' | 'SVG' | 'PDF', fileName: string, orientation?: 'Portrait' | 'Landscape'): void
```

**Parameters:**
- `type` — Export format
- `fileName` — Output file name (without extension)
- `orientation` — PDF orientation (optional)

**Example:**
```typescript
import { useRef } from 'react';

const chartRef = useRef(null);

const exportToPNG = () => {
  chartRef.current?.export('PNG', 'StockChart');
};

<button onClick={exportToPNG}>Export as PNG</button>
<StockChartComponent ref={chartRef} {...props} />
```

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#export

### print()

Print the chart using browser print dialog.

**Signature:**
```typescript
print(): void
```

**Example:**
```typescript
const chartRef = useRef(null);

const printChart = () => {
  chartRef.current?.print();
};

<button onClick={printChart}>Print</button>
<StockChartComponent ref={chartRef} {...props} />
```

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#print

### destroy()

Clean up the chart instance and free resources.

**Signature:**
```typescript
destroy(): void
```

**Example:**
```typescript
useEffect(() => {
  return () => {
    chartRef.current?.destroy();
  };
}, []);
```

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#destroy

### getModuleName()

Get the module name of the Stock Chart.

**Signature:**
```typescript
getModuleName(): string
```

**Returns:** `'StockChart'`

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#getmodulename

### rangeChanged()

Programmatically change the visible date range.

**Signature:**
```typescript
rangeChanged(start: Date | number, end: Date | number): void
```

**Parameters:**
- `start` — Start date or timestamp
- `end` — End date or timestamp

**Example:**
```typescript
const chartRef = useRef(null);

const goToLastMonth = () => {
  const end = new Date();
  const start = new Date();
  start.setMonth(start.getMonth() - 1);
  
  chartRef.current?.rangeChanged(start, end);
};
```

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#rangechanged

### renderPeriodSelector()

Programmatically render or re-render the period selector UI.

**Signature:**
```typescript
renderPeriodSelector(): void
```

**Example:**
```typescript
const chartRef = useRef(null);

const refreshSelector = () => {
  chartRef.current?.renderPeriodSelector();
};
```

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#renderperiodselector

---

## Events

Events are triggered during chart lifecycle and user interactions.

### Lifecycle Events

#### load
Fired before the chart component is loaded.

**Signature:**
```typescript
onLoad?: (args: IStockChartEventArgs) => void
```

**Example:**
```typescript
<StockChartComponent
  onLoad={(args) => {
    console.log('Chart loading:', args);
  }}
/>
```

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#load

#### loaded
Fired after the chart component is fully loaded.

**Signature:**
```typescript
onLoaded?: (args: IStockChartEventArgs) => void
```

**Example:**
```typescript
<StockChartComponent
  onLoaded={(args) => {
    console.log('Chart loaded:', args);
  }}
/>
```

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#loaded

### Data & Rendering Events

#### axisLabelRender
Customize axis labels before rendering.

**Signature:**
```typescript
onAxisLabelRender?: (args: IAxisLabelRenderEventArgs) => void
```

**Parameters:**
- `args.text` — Label text
- `args.value` — Label value
- `args.axis` — Axis information

**Example:**
```typescript
<StockChartComponent
  onAxisLabelRender={(args) => {
    if (args.axis.name === 'primaryYAxis') {
      args.text = '$' + args.text;
    }
  }}
/>
```

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#axislabelrender

#### crosshairLabelRender
Triggers before the crosshair tooltip for the series is rendered.

**Signature:**
```typescript
onCrosshairLabelRender?: (args: ICrosshairLabelRenderEventArgs) => void
```

**Example:**
```typescript
<StockChartComponent
  onCrosshairLabelRender={(args) => {
    args.text = 'Price: ' + args.text;
  }}
/>
```

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#crosshairlabelrender

#### seriesRender
Fired when a series is rendered.

**Signature:**
```typescript
onSeriesRender?: (args: ISeriesRenderEventArgs) => void
```

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#seriesrender

#### beforeExport
Fired before export operation begins.

**Signature:**
```typescript
onBeforeExport?: (args: IExportEventArgs) => void
```

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#beforeexport

### User Interaction Events

#### pointClick
Fired when a data point is clicked.

**Signature:**
```typescript
onPointClick?: (args: IPointEventArgs) => void
```

**Parameters:**
- `args.pointIndex` — Index of clicked point
- `args.seriesIndex` — Index of clicked series
- `args.x` — X-value
- `args.y` — Y-value

**Example:**
```typescript
<StockChartComponent
  onPointClick={(args) => {
    console.log(`Clicked point at ${args.x}: ${args.y}`);
  }}
/>
```

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#pointclick

#### pointMove
Fired when mouse moves over a data point.

**Signature:**
```typescript
onPointMove?: (args: IPointEventArgs) => void
```

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#pointmove

### Mouse & Chart Events

#### stockChartMouseClick
Triggers when clicking on the stock chart.

**Signature:**
```typescript
onStockChartMouseClick?: (args: IMouseEventArgs) => void
```

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#stockchartmouseclick

#### stockChartMouseDown
Triggers on mouse down event.

**Signature:**
```typescript
onStockChartMouseDown?: (args: IMouseEventArgs) => void
```

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#stockchartmousedown

#### stockChartMouseLeave
Triggers when cursor leaves the chart.

**Signature:**
```typescript
onStockChartMouseLeave?: (args: IMouseEventArgs) => void
```

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#stockchartmouseleave

#### stockChartMouseMove
Triggers when hovering over the stock chart.

**Signature:**
```typescript
onStockChartMouseMove?: (args: IMouseEventArgs) => void
```

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#stockchartmousemove

#### stockChartMouseUp
Triggers on mouse up event.

**Signature:**
```typescript
onStockChartMouseUp?: (args: IMouseEventArgs) => void
```

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#stockchartmouseup

### Legend Events

#### legendClick
Fired when a legend item is clicked.

**Signature:**
```typescript
onLegendClick?: (args: ILegendClickEventArgs) => void
```

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#legendclick

#### legendRender
Fired when legend items are rendered.

**Signature:**
```typescript
onLegendRender?: (args: ILegendRenderEventArgs) => void
```

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#legendrender

### Tooltip & Crosshair Events

#### tooltipRender
Modify tooltip content before display.

**Signature:**
```typescript
onTooltipRender?: (args: ITooltipRenderEventArgs) => void
```

**Parameters:**
- `args.text` — Tooltip text
- `args.pointIndex` — Point index
- `args.seriesIndex` — Series index
- `args.textStyle` — Text styling

**Example:**
```typescript
<StockChartComponent
  onTooltipRender={(args) => {
    args.text = `Custom: ${args.text}`;
  }}
/>
```

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#tooltiprender

### Range & Selector Events

#### rangeChange
Emitted when the selected date range changes.

**Signature:**
```typescript
onRangeChange?: (args: IRangeChangeEventArgs) => void
```

**Parameters:**
- `args.start` — Range start date
- `args.end` — Range end date

**Example:**
```typescript
<StockChartComponent
  onRangeChange={(args) => {
    console.log(`Range changed: ${args.start} to ${args.end}`);
  }}
/>
```

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#rangechange

#### selectorRender
Triggered when range selector renders.

**Signature:**
```typescript
onSelectorRender?: (args: IRangeSelectorRenderEventArgs) => void
```

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#selectorrender

### Technical Analysis Events

#### stockEventRender
Customize stock event marker rendering.

**Signature:**
```typescript
onStockEventRender?: (args: IStockEventRenderArgs) => void
```

**Parameters:**
- `args.text` — Event text
- `args.description` — Event description
- `args.type` — Event marker type
- `args.background` — Event color

**Example:**
```typescript
<StockChartComponent
  onStockEventRender={(args) => {
    if (args.type === 'Flag') {
      args.background = '#ff0000';
    }
  }}
/>
```

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#stockeventrender

#### onZooming
Fired during zoom interactions.

**Signature:**
```typescript
onZooming?: (args: IZoomingEventArgs) => void
```

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#onzooming

---

## Directives

Directives are used in JSX markup to define nested structures for series and indicators.

### StockChartSeriesCollectionDirective / StockChartSeriesDirective

Define chart series using directives.

**Usage:**
```typescript
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
    name='Stock Price'
  />
</StockChartSeriesCollectionDirective>
```

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockSeries-model

### StockChartIndicatorsDirective / StockChartIndicatorDirective

Define technical indicators using directives.

**Usage:**
```typescript
<StockChartIndicatorsDirective>
  <StockChartIndicatorDirective
    type='Sma'
    field='Close'
    seriesName='Stock'
    period={20}
    fill='#0000ff'
  />
</StockChartIndicatorsDirective>
```

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartIndicatorModel

### Stock Events (Prop-based, Not a Directive)

Stock events are defined as a **prop array** on `StockChartComponent`, not using directives.

**Usage:**
```typescript
<StockChartComponent
  stockEvents={[
    {
      date: new Date('2012-02-01'),
      text: 'Q1',
      description: 'Q1 Earnings',
      type: 'Flag',
      background: '#6c757d',
      seriesIndexes: [0]
    }
  ]}
>
  {/* Chart content */}
</StockChartComponent>
```

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockEventModel

### StockChartTrendlinesDirective / StockChartTrendlineDirective

Define trend lines for series.

**Usage:**
```typescript
<StockChartSeriesDirective>
  <StockChartTrendlinesDirective>
    <StockChartTrendlineDirective
      type='Linear'
      fill='#ff0000'
      width={2}
    />
  </StockChartTrendlinesDirective>
</StockChartSeriesDirective>
```

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartTrendlineModel

### StockChartAxesDirective / StockChartAxisDirective

Define additional Y-axes for multi-axis charts.

**Usage:**
```typescript
<StockChartAxesDirective>
  <StockChartAxisDirective
    name='volumeAxis'
    opposedPosition={true}
    title='Volume'
  />
</StockChartAxesDirective>
```

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartAxis-model

### StockChartRowsDirective / StockChartRowDirective

Define multi-row/pane layouts.

**Usage:**
```typescript
<StockChartRowsDirective>
  <StockChartRowDirective height='60%' />
  <StockChartRowDirective height='40%' />
</StockChartRowsDirective>
```

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartRowModel

---

## Models & Interfaces

### StockSeriesModel

Defines a single stock chart series.

**Key Properties:**
- `dataSource: Object[]` — Series data
- `type: 'Candle' | 'Line' | 'Spline' | 'Hilo' | 'HiloOpenClose'` — Series type
- `xName: string` — X field name
- `open: string` — Open price field
- `high: string` — High price field
- `low: string` — Low price field
- `close: string` — Close price field
- `volume: string` — Volume field
- `name: string` — Series name for legend
- `fill: string` — Series color
- `opacity: number` — Series opacity (0-1)
- `width: number` — Line width
- `bearFillColor: string` — Bearish candle color
- `bullFillColor: string` — Bullish candle color
- `enableSolidCandle: boolean` — Use solid candles instead of hollow

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockSeries-model

### StockChartAxisModel

Defines a chart axis (X or Y).

**Key Properties:**
- `valueType: 'DateTime' | 'Numeric' | 'Logarithmic' | 'Category'` — Axis type
- `title: string` — Axis title
- `labelFormat: string` — Label format
- `interval: number` — Interval between labels
- `intervalType: string` — Interval type (for DateTime)
- `minimum: number` — Minimum value
- `maximum: number` — Maximum value
- `rangePadding: string` — Padding mode
- `majorGridLines: {}` — Grid line styling
- `minorGridLines: {}` — Minor grid line styling
- `lineStyle: {}` — Axis line styling

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartAxis-model

### StockChartIndicatorModel

Defines a technical indicator.

**Key Properties:**
- `type: string` — Indicator type
- `field: string` — Data field
- `seriesName: string` — Target series
- `period: number` — Calculation period
- `fill: string` — Indicator color
- Additional type-specific properties (e.g., `standardDeviation` for Bollinger Bands)

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartIndicatorModel

### StockEventModel

Defines a stock event marker.

**Key Properties:**
- `date: Date` — Event date
- `text: string` — Event label
- `description: string` — Event description
- `type: string` — Marker type
- `background: string` — Marker color
- `border: {}` — Border styling
- `seriesIndexes: number[]` — Limit to specific series

**Official API:** https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockEventModel

---

## Modules to Inject

### Essential Modules

All Stock Chart features must be explicitly injected:

```typescript
import { Inject } from '@syncfusion/ej2-react-charts';

<StockChartComponent>
  <Inject services={[/* modules */]} />
</StockChartComponent>
```

### Axis Module

**DateTime** (required for stock charts)
```typescript
import { DateTime } from '@syncfusion/ej2-react-charts';

<Inject services={[DateTime]} />
```

### Series Type Modules

```typescript
import {
  LineSeries,
  SplineSeries,
  CandleSeries,
  HiloSeries,
  HiloOpenCloseSeries,
  RangeAreaSeries,
  Trendlines
} from '@syncfusion/ej2-react-charts';

<Inject services={[LineSeries, SplineSeries, CandleSeries, HiloSeries, HiloOpenCloseSeries, RangeAreaSeries, Trendlines]} />
```

### Interaction Modules

```typescript
import {
  Tooltip,
  RangeTooltip,
  Crosshair,
  StockLegend,
  DataLabel
} from '@syncfusion/ej2-react-charts';

<Inject services={[Tooltip, RangeTooltip, Crosshair, StockLegend, DataLabel]} />
```

### Technical Indicator Modules

```typescript
import {
  SmaIndicator,
  EmaIndicator,
  RsiIndicator,
  MacdIndicator,
  BollingerBands,
  TmaIndicator,
  MomentumIndicator,
  StochasticIndicator,
  AtrIndicator,
  AccumulationDistributionIndicator
} from '@syncfusion/ej2-react-charts';

<Inject services={[
  SmaIndicator,
  EmaIndicator,
  RsiIndicator,
  MacdIndicator,
  BollingerBands,
  TmaIndicator,
  MomentumIndicator,
  StochasticIndicator,
  AtrIndicator,
  AccumulationDistributionIndicator
]} />
```

### Export & Print Modules

- No modules are required for stock chart printing.

```typescript
import { Export } from '@syncfusion/ej2-react-charts';

<Inject services={[Export]} />
```

### Complete Module Injection

For a fully-featured Stock Chart:

```typescript
import {
  // Main component
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  StockChartIndicatorsDirective,
  StockChartIndicatorDirective,
  StockEventsDirective,
  StockEventDirective,
  StockChartTrendlinesDirective,
  StockChartTrendlineDirective,
  Inject,
  // Axes
  DateTime,
  // Series
  LineSeries,
  SplineSeries,
  CandleSeries,
  HiloSeries,
  HiloOpenCloseSeries,
  RangeAreaSeries,
  Trendlines,
  // Interaction
  Tooltip,
  RangeTooltip,
  Crosshair,
  StockLegend,
  DataLabel,
  // Indicators
  SmaIndicator,
  EmaIndicator,
  RsiIndicator,
  MacdIndicator,
  BollingerBands,
  TmaIndicator,
  MomentumIndicator,
  StochasticIndicator,
  AtrIndicator,
  AccumulationDistributionIndicator,
  // Export
  Export
} from '@syncfusion/ej2-react-charts';

<Inject services={[
  DateTime,
  LineSeries,
  SplineSeries,
  CandleSeries,
  HiloSeries,
  HiloOpenCloseSeries,
  RangeAreaSeries,
  Trendlines,
  Tooltip,
  RangeTooltip,
  Crosshair,
  StockLegend,
  DataLabel,
  SmaIndicator,
  EmaIndicator,
  RsiIndicator,
  MacdIndicator,
  BollingerBands,
  TmaIndicator,
  MomentumIndicator,
  StochasticIndicator,
  AtrIndicator,
  AccumulationDistributionIndicator,
  Export
]} />
```

---

## Common Patterns

### 1. Basic Stock Chart with Candle Series

```typescript
import { StockChartComponent, StockChartSeriesCollectionDirective, StockChartSeriesDirective, Inject, DateTime, CandleSeries, Tooltip, RangeTooltip, Crosshair } from '@syncfusion/ej2-react-charts';

function BasicStockChart() {
  const data = [
    { x: new Date('2012-04-02'), open: 85.97, high: 90.58, low: 85.97, close: 90.58 },
    { x: new Date('2012-04-03'), open: 89.02, high: 92.50, low: 88.50, close: 92.90 }
  ];

  return (
    <StockChartComponent
      id='stockchart'
      title='Stock Price'
      primaryXAxis={{ valueType: 'DateTime' }}
      tooltip={{ enable: true }}
      crosshair={{ enable: true }}
    >
      <Inject services={[DateTime, CandleSeries, Tooltip, RangeTooltip, Crosshair]} />
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

### 2. Stock Chart with Multiple Series and Comparison

```typescript
<StockChartComponent>
  <Inject services={[DateTime, LineSeries, Tooltip, RangeTooltip, Crosshair, StockLegend]} />
  <StockChartSeriesCollectionDirective>
    <StockChartSeriesDirective
      dataSource={applData}
      type='Line'
      name='AAPL'
      xName='x'
      yName='close'
      fill='#0080ff'
    />
    <StockChartSeriesDirective
      dataSource={googData}
      type='Line'
      name='GOOG'
      xName='x'
      yName='close'
      fill='#ff8000'
    />
  </StockChartSeriesCollectionDirective>
</StockChartComponent>
```

### 3. Stock Chart with Technical Indicators

```typescript
<StockChartComponent>
  <Inject services={[DateTime, CandleSeries, SmaIndicator, EmaIndicator, Tooltip]} />
  <StockChartSeriesCollectionDirective>
    <StockChartSeriesDirective dataSource={data} type='Candle' />
  </StockChartSeriesCollectionDirective>
  <StockChartIndicatorsDirective>
    <StockChartIndicatorDirective type='Sma' period={20} field='Close' fill='#0000ff' />
    <StockChartIndicatorDirective type='Ema' period={50} field='Close' fill='#ff0000' />
  </StockChartIndicatorsDirective>
</StockChartComponent>
```

### 4. Stock Chart with Events, Export, and Print

```tsx
import { useRef } from 'react';
import {type StockEventsSettingsModel }from '@syncfusion/ej2-react-charts';
function AdvancedStockChart() { 
  const chartRef = useRef(null);
  const events: StockEventsSettingsModel[] = [
    { date: new Date('2012-02-01'), text: 'Earnings', type: 'Flag', background: '#6c757d' }
  ];

  return (
    <>
      <button onClick={() => chartRef.current?.export('PNG', 'StockChart')}>
        Export PNG
      </button>
      <button onClick={() => chartRef.current?.print()}>Print</button>

      <StockChartComponent
        ref={chartRef}
        stockEvents={events}
        exportType={['PNG', 'JPEG', 'SVG', 'PDF']}
      >
        <Inject services={[DateTime, CandleSeries, Export, Tooltip]} />
      </StockChartComponent>
    </>
  );
}
```

---

## API Quick Links

**Master API Documentation:**
- Stock Chart Component: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
- Stock Chart Models: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel

**Detailed API References:**
- Stock Chart Main Model: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel
- Stock Series Model: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockSeries-model
- Stock Chart Axis Model: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartAxis-model
- Stock Chart Indicator Model: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartIndicatorModel
- Stock Event Model: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockEventModel
- Stock Chart Legend Settings: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartLegendSettingsModel
- Stock Chart Tooltip Settings: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartTooltipSettingsModel

**Feature Documentation:**
- Getting Started: https://ej2.syncfusion.com/react/documentation/stock-chart/getting-started
- Stock Chart Features: https://ej2.syncfusion.com/react/documentation/stock-chart/
- Export & Print: https://ej2.syncfusion.com/react/documentation/stock-chart/
- Technical Indicators: https://ej2.syncfusion.com/react/documentation/stock-chart/
- Stock Events: https://ej2.syncfusion.com/react/documentation/stock-chart/

---

**Last Updated:** March 27, 2026  
**API Version:** Stock Chart v24.1+  
**React Version:** 16.8+
````