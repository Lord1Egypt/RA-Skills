# StockChart API Reference

This document is a concise, machine-friendly summary of the public API for `StockChartComponent` from `@syncfusion/ej2-react-charts`. It is intended to be used by the skill documentation and examples and is based on the official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default

## Quick links
- Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
- Package: `@syncfusion/ej2-react-charts`

## Key props (name : type — brief)

**Data & Series:**
- `dataSource: Object | DataManager | []` — Source data for series (objects with `x, open, high, low, close, volume`). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#datasource
- `series: StockSeriesModel[]` — Series definitions (type: `Candle`, `Line`, `Spline`, `Hilo`, `HiloOpenClose`, etc.). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#series
- `seriesType: ChartSeriesType[]` — Types of series available in financial chart. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#seriestype

**Axes:**
- `primaryXAxis: StockChartAxisModel` — Primary X axis (typically `valueType: 'DateTime'`). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#primaryxaxis
- `primaryYAxis: StockChartAxisModel` — Primary Y axis. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#primaryyaxis
- `axes: StockChartAxisModel[]` — Additional axes definitions for multi-series scaling. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#axes

**Layout & Appearance:**
- `width: string | number` — Chart width. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#width
- `height: string | number` — Chart height. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#height
- `title: string` — Chart title. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#title
- `titleStyle: StockChartFontModel` — Styling for chart title. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#titlestyle
- `background: string` — Chart background color. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#background
- `border: StockChartBorderModel` — Chart border configuration. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#border
- `chartArea: StockChartAreaModel` — Chart area styling. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#chartarea
- `margin: StockMarginModel` — Chart margin configuration. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#margin
- `theme: ChartTheme` — Theme (material, bootstrap, fabric, tailwind, etc.). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#theme

**Navigation & Selectors:**
- `periods: PeriodsModel[]` — Period selector button configuration (objects with `intervalType`, `interval`, `text`). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#periods
- `enablePeriodSelector: boolean` — Show the period selector control. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#enableperiodselector
- `enableSelector: boolean` — Show the range selector (thumbs). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#enableselector
- `enableCustomRange: boolean` — Enable custom range selection. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#enablecustomrange

**Analysis & Events:**
- `indicators: StockChartIndicatorModel[]` — List of technical indicators (SMA, EMA, RSI, MACD, BollingerBands, ...). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#indicators
- `indicatorType: TechnicalIndicators[]` — Types of indicators available. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#indicatortype
- `stockEvents: StockEventModel[]` — Stock event markers (date, text, description, type, background). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#stockevents
- `annotations: StockChartAnnotationSettingsModel[]` — Annotations rendered on chart. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#annotations

**Interaction & UI:**
- `tooltip: StockTooltipSettingsModel` — Tooltip configuration. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#tooltip
- `crosshair: CrosshairSettingsModel` — Crosshair enable and styling options. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#crosshair
- `legendSettings: StockChartLegendSettingsModel` — Legend visibility and styling. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#legendsettings
- `zoomSettings: ZoomSettingsModel` — Zoom and pan settings. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#zoomsettings

**Selection & State:**
- `selectedDataIndexes: StockChartIndexesModel[][]` — Programmatically set selected data point indexes. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#selecteddataindexes
- `selectionMode: SelectionMode` — Selection mode (None, Point, Series, Cluster, DragXY, DragX, DragY). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#selectionmode
- `isMultiSelect: boolean` — Allow multiple selection of data points. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#ismultiselect
- `isSelect: boolean` — Indicates selection state. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#isselect

**Layout & Multi-Row:**
- `rows: StockChartRowModel[]` — Row definitions for multi-row layouts. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#rows

**Localization & Persistence:**
- `enablePersistence: boolean` — Persist chart state between page reloads. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#enablepersistence
- `enableRtl: boolean` — Enable right-to-left rendering. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#enablertl
- `locale: string` — Overrides global culture and localization value for this component. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#locale

**Export & Templates:**
- `exportType: ExportType[]` — Export formats (PNG, JPEG, SVG, PDF). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#exporttype
- `noDataTemplate: string | Function` — Template/text shown when no data available. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#nodatatemplate

**Trend Lines:**
- `trendlineType: TrendlineTypes[]` — Types of trendlines supported (Linear, Exponential, Logarithmic, Polynomial, Power, MovingAverage). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#trendlinetype

**Internal Module Reference:**
- `stockLegendModule: any` — Internal stock legend module reference. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#stocklegendmodule
- `isTransposed: boolean` — Render chart in transposed manner. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#istransposed
 - `enablePersistence: boolean` — Persist chart state between page loads.
 - `enableRtl: boolean` — Enable right-to-left rendering.
 - `enableCustomRange: boolean` — Enable custom range selection.
 - `enablePeriodSelector: boolean` — Show the period selector control.
 - `enableSelector: boolean` — Show the range selector (thumbs).
 - `exportType: ExportType[]` — Allowed export formats (e.g., ['PNG','JPEG','SVG','PDF']).
 - `height: string | number` — Chart height.
 - `indicatorType: TechnicalIndicators[]` — Shorthand list of indicator types available.
 - `indicators: StockChartIndicatorModel[]` — List of technical indicators (SMA, EMA, RSI, MACD, BollingerBands, ...).
 - `isMultiSelect: boolean` — Allow multiple selection of data points.
 - `isSelect: boolean` — Indicates selection state.
 - `legendSettings: StockChartLegendSettingsModel` — Legend visibility and styling.
 - `margin: StockMarginModel` — Chart margin configuration.
 - `noDataTemplate: string | Function` — Template or text shown when no data is available.
 - `periods: PeriodsModel[]` — Period selector button configuration (objects with `intervalType`, `interval`, `text`).
 - `primaryXAxis: StockChartAxisModel` — Primary X axis (typically `valueType: 'DateTime'`).
 - `primaryYAxis: StockChartAxisModel` — Primary Y axis.
 - `rows: StockChartRowModel[]` — Row definitions for multi-row layouts.
 - `selectedDataIndexes: StockChartIndexesModel[][]` — Programmatically set selected points indexes.
 - `selectionMode: SelectionMode` — Selection interaction mode (e.g., None, Point, Series).
 - `series: StockSeriesModel[]` — Series definitions (type: `Candle`, `Line`, `Spline`, `Hilo`, `HiloOpenClose`, etc.).
 - `stockEvents: StockEventModel[]` — Stock event markers (date, text, description, type, background).
 - `stockLegendModule: any` — Internal stock legend module reference.
 - `theme: ChartTheme` — Theme (material, bootstrap, fabric, tailwind, etc.).
 - `title: string` — Chart title.
 - `titleStyle: StockChartFontModel` — Styling for chart title.
 - `tooltip: StockTooltipSettingsModel` — Tooltip configuration.
 - `trendlineType: TrendlineTypes[]` — Types of trendlines supported.
 - `width: string | number` — Chart width.
 - `zoomSettings: ZoomSettingsModel` — Zoom and pan settings.
  - `enablePersistence: boolean` — Persist chart state between page loads. — Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
  - `enableRtl: boolean` — Enable right-to-left rendering. — Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
  - `enableCustomRange: boolean` — Enable custom range selection. — Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
  - `enablePeriodSelector: boolean` — Show the period selector control. — Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
  - `enableSelector: boolean` — Show the range selector (thumbs). — Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
  - `exportType: ExportType[]` — Allowed export formats (e.g., ['PNG','JPEG','SVG','PDF']). — Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
  - `height: string | number` — Chart height. — Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
  - `indicatorType: TechnicalIndicators[]` — Shorthand list of indicator types available. — Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
  - `indicators: StockChartIndicatorModel[]` — List of technical indicators (SMA, EMA, RSI, MACD, BollingerBands, ...). — Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
  - `isMultiSelect: boolean` — Allow multiple selection of data points. — Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
  - `isSelect: boolean` — Indicates selection state. — Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
  - `legendSettings: StockChartLegendSettingsModel` — Legend visibility and styling. — Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
  - `margin: StockMarginModel` — Chart margin configuration. — Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
  - `noDataTemplate: string | Function` — Template or text shown when no data is available. — Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
  - `periods: PeriodsModel[]` — Period selector button configuration (objects with `intervalType`, `interval`, `text`). — Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
  - `primaryXAxis: StockChartAxisModel` — Primary X axis (typically `valueType: 'DateTime'`). — Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
  - `primaryYAxis: StockChartAxisModel` — Primary Y axis. — Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
  - `rows: StockChartRowModel[]` — Row definitions for multi-row layouts. — Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
  - `selectedDataIndexes: StockChartIndexesModel[][]` — Programmatically set selected points indexes. — Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
  - `selectionMode: SelectionMode` — Selection interaction mode (e.g., None, Point, Series). — Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
  - `series: StockSeriesModel[]` — Series definitions (type: `Candle`, `Line`, `Spline`, `Hilo`, `HiloOpenClose`, etc.). — Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
  - `stockEvents: StockEventModel[]` — Stock event markers (date, text, description, type, background). — Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
  - `stockLegendModule: any` — Internal stock legend module reference. — Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
  - `theme: ChartTheme` — Theme (material, bootstrap, fabric, tailwind, etc.). — Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
  - `title: string` — Chart title. — Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
  - `titleStyle: StockChartFontModel` — Styling for chart title. — Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
  - `tooltip: StockTooltipSettingsModel` — Tooltip configuration. — Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
  - `trendlineType: TrendlineTypes[]` — Types of trendlines supported. — Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
  - `width: string | number` — Chart width. — Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
  - `zoomSettings: ZoomSettingsModel` — Zoom and pan settings. — Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default

## Methods (name — signature)

- `destroy(): void` — Destroy the chart instance and free resources. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#destroy
- `getModuleName(): string` — Return component module name. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#getmodulename
- `rangeChanged(start: number | Date, end: number | Date): void` — Programmatically change visible range. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#rangechanged
- `renderPeriodSelector(): void` — Render (or re-render) the period selector UI. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#renderperiodselector
- `export(type: string, fileName: string): void` — Export chart to PNG, JPEG, SVG, or PDF format. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#export
- `print(): void` — Print the chart to printer or PDF. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#print

## Events (name — payload type / purpose)

**Lifecycle & Rendering Events:**
- `load` — Component lifecycle before range navigator rendering (IStockChartEventArgs). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#load
- `loaded` — Component lifecycle after range navigator rendering (IStockChartEventArgs). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#loaded

**Axis & Label Events:**
- `axisLabelRender` — Customize each axis label before rendering (IAxisLabelRenderEventArgs). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#axislabelrender
- `crosshairLabelRender` — Triggers before the crosshair tooltip for the series is rendered (ICrosshairLabelRenderEventArgs). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#crosshairlabelrender

**Data & Export Events:**
- `beforeExport` — Fired before export operation (IExportEventArgs). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#beforeexport
- `seriesRender` — Fired when a series is rendered (ISeriesRenderEventArgs). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#seriesrender

**Legend Events:**
- `legendClick` — Triggers after click on legend (IStockLegendClickEventArgs). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#legendclick
- `legendRender` — Triggers before the legend is rendered (IStockLegendRenderEventArgs). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#legendrender

**Point & Mouse Events:**
- `pointClick` — Triggers on point click (IPointEventArgs). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#pointclick
- `pointMove` — Triggers on point move (IPointEventArgs). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#pointmove
- `stockChartMouseClick` — Triggers on clicking the stock chart (IMouseEventArgs). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#stockchartmouseclick
- `stockChartMouseDown` — Triggers on mouse down (IMouseEventArgs). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#stockchartmousedown
- `stockChartMouseLeave` — Triggers when cursor leaves the chart (IMouseEventArgs). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#stockchartmouseleave
- `stockChartMouseMove` — Triggers on hovering the stock chart (IMouseEventArgs). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#stockchartmousemove
- `stockChartMouseUp` — Triggers on mouse up (IMouseEventArgs). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#stockchartmouseup

**Range & Selector Events:**
- `rangeChange` — Triggers if the range is changed (IRangeChangeEventArgs). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#rangechange
- `selectorRender` — Triggers before render the selector (IRangeSelectorRenderEventArgs). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#selectorrender

**Technical Analysis & Tooltip Events:**
- `stockEventRender` — When a stock event marker is rendered/customized (IStockEventRenderArgs). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#stockeventrender
- `tooltipRender` — Modify tooltip content before it shows (ITooltipRenderEventArgs). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#tooltiprender

**Zoom Events:**
- `onZooming` — Fired during zoom interactions (IZoomingEventArgs). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#onzooming

## Child directives / nested models (common)
- `StockChartSeriesCollectionDirective` → `StockChartSeriesDirective` (props: `type`, `dataSource`, `xName`, `open`, `high`, `low`, `close`, `volume`, `name`)
- `StockChartTrendlinesDirective` → `StockChartTrendlineDirective` (props: `type`, `period`, `polynomialOrder`, `enableTooltip`, `fill`, `width`)
- `StockEventsDirective` → `StockEventDirective` (props: `date`, `text`, `description`, `type`, `background`)

## Minimal usage example (React)

```tsx
import React from 'react';
import {
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  Inject,
  DateTime,
  CandleSeries,
  Tooltip,
  Crosshair,
  RangeTooltip
} from '@syncfusion/ej2-react-charts';

const data = [
  { x: new Date(2023,0,1), open: 120, high: 135, low: 115, close: 130, volume: 10000 },
  { x: new Date(2023,0,2), open: 130, high: 140, low: 125, close: 138, volume: 12000 }
];

export default function Example() {
  return (
    <StockChartComponent id="stockchart" dataSource={data} primaryXAxis={{ valueType: 'DateTime' }} tooltip={{ enable: true }} crosshair={{ enable: true }}>
      <Inject services={[DateTime, CandleSeries, Tooltip, Crosshair, RangeTooltip]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective type="Candle" xName="x" open="open" high="high" low="low" close="close" volume="volume" />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}
```

## Export/Print Modules
The Stock Chart supports export and print functionality through these modules:

- `Export` — Enables export to PNG, JPEG, SVG, PDF formats. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
- `Print` — Enables print functionality via Print module. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default

## Technical Indicator Modules
Advanced technical analysis with 10+ indicator types:

- `SmaIndicator` — Simple Moving Average (SMA) indicator. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
- `EmaIndicator` — Exponential Moving Average (EMA) indicator. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
- `RsiIndicator` — Relative Strength Index (RSI) momentum oscillator. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
- `MacdIndicator` — MACD (Moving Average Convergence Divergence) indicator. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
- `BollingerBands` — Bollinger Bands volatility indicator. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
- `TmaIndicator` — Triangular Moving Average (TMA) indicator. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
- `MomentumIndicator` — Momentum indicator for rate of change. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
- `StochasticIndicator` — Stochastic momentum oscillator. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
- `AtrIndicator` — Average True Range (ATR) volatility indicator. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
- `AccumulationDistributionIndicator` — Accumulation Distribution money flow indicator. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default

## Series Type Modules
Different visualization series for stock data:

- `LineSeries` — Line chart series for price trends. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockSeries-model
- `SplineSeries` — Smooth spline/curve series. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockSeries-model
- `CandleSeries` — Candlestick series (OHLC). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockSeries-model
- `HiloSeries` — High-Low range bar series. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockSeries-model
- `HiloOpenCloseSeries` — OHLC bar series. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockSeries-model
- `RangeAreaSeries` — Range area series for range visualization. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockSeries-model
- `Trendlines` — Trend line support for series analysis. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockSeries-model

## Legend and UI Modules
Interactive UI components:

- `StockLegend` — Legend display for series information. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#legendsettings

## Interactive Feature Modules
User interaction and tooltips:

- `Tooltip` — Hover tooltips for data points. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#tooltip
- `RangeTooltip` — Tooltips for range selector. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default
- `Crosshair` — Crosshair and trackball feature. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartModel#crosshair
- `DataLabel` — Data labels on chart points. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockSeries-model

## Axis Module
Date/time axis support:

- `DateTime` — DateTime axis for handling date-based stock data. **REQUIRED for all stock charts**. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartAxis-model

## Stock Events
- `StockEventsDirective` → `StockEventDirective` — Markup directives for defining stock event markers. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default

## Stock Chart Indicators
- `StockChartIndicatorsDirective` → `StockChartIndicatorDirective` — Markup directives for technical indicators. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default

## Stock Chart Trend Lines
- `StockChartTrendlinesDirective` → `StockChartTrendlineDirective` — Markup directives for trend lines (Linear, Exponential, Logarithmic, Polynomial, Power, MovingAverage). Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default

## Stock Chart Axes (Multiple Axes)
- `StockChartAxesDirective` → `StockChartAxisDirective` — Markup directives for defining multiple Y-axes for multi-series scaling. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockChartAxis-model

## Stock Chart Rows (Multi-Row Layout)
- `StockChartRowsDirective` → `StockChartRowDirective` — Markup directives for row-based multi-chart layouts. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default

## Additional Essential Directives
- `StockChartSeriesCollectionDirective` → `StockChartSeriesDirective` — Main series collection and individual series definition. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/stockSeries-model
- `StockChartAnnotationSettingsModel[]` — Annotations/drawings on chart. Official API: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default

## Complete Module Injection Pattern

For comprehensive stock chart with all features:

```typescript
import { 
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  StockChartIndicatorsDirective,
  StockChartIndicatorDirective,
  StockChartTrendlinesDirective,
  StockChartTrendlineDirective,
  StockEventsDirective,
  StockEventDirective,
  Inject,
  DateTime,
  Tooltip,
  RangeTooltip,
  Crosshair,
  StockLegend,
  Export,
  // Series types
  LineSeries,
  SplineSeries,
  CandleSeries,
  HiloOpenCloseSeries,
  HiloSeries,
  RangeAreaSeries,
  Trendlines,
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
  AccumulationDistributionIndicator
} from '@syncfusion/ej2-react-charts';
```

Then inject services:
```typescript
<Inject services={[
  DateTime,
  Tooltip,
  RangeTooltip,
  Crosshair,
  StockLegend,
  Export,
  LineSeries,
  SplineSeries,
  CandleSeries,
  HiloOpenCloseSeries,
  HiloSeries,
  RangeAreaSeries,
  Trendlines,
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

## Notes for skill updates
- Use the prop lists above to reconcile `SKILL.md` and `references/*` files.
- Prefer to reference the official API link for exhaustive details and types.
- All modules must be injected explicitly for the features to work
- DateTime module is **REQUIRED** for Stock Chart functionality
- See official Syncfusion Stock Chart API reference: https://ej2.syncfusion.com/react/documentation/api/stock-chart/index-default


