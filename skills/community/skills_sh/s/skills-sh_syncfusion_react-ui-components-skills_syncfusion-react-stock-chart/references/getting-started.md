# Getting Started with Stock Charts

This guide covers the initial setup and basic implementation of the Syncfusion React Stock Chart component.

> See the concise API summary in [API Reference](./api.md) for full prop and event details.

## Table of Contents

- [Installation and Dependencies](#installation-and-dependencies)
  - [Required Package](#required-package)
  - [Dependencies Tree](#dependencies-tree)
- [Project Setup](#project-setup)
  - [Using Vite Recommended](#using-vite-recommended)
  - [Using Create React App Alternative](#using-create-react-app-alternative)
- [Basic Stock Chart Implementation](#basic-stock-chart-implementation)
  - [Minimal Example](#minimal-example)
- [Module Injection](#module-injection)
  - [Inject Modules](#inject-modules)
  - [Essential Modules for Stock Charts](#essential-modules-for-stock-charts)
  - [Stock Chart Series Modules](#stock-chart-series-modules)
  - [Range Navigator Modules](#range-navigator-modules)
  - [Axis Modules](#axis-modules)
  - [User Interaction Modules](#user-interaction-modules)
  - [Legend Module](#legend-module)
  - [Technical Indicator Modules](#technical-indicator-modules)
  - [Analysis Modules](#analysis-modules)
  - [Period Selector Module](#period-selector-module)
  - [Export Module](#export-module)
  - [Example Full Stock Chart Module Injection](#example-full-stock-chart-module-injection)
- [Interfaces](#interfaces)
  - [Stock Chart Configuration Interfaces](#stock-chart-configuration-interfaces)
  - [Stock Chart Axis Interfaces](#stock-chart-axis-interfaces)
  - [Stock Chart Series Interfaces](#stock-chart-series-interfaces)
  - [Tooltip and Crosshair Interfaces](#tooltip-and-crosshair-interfaces)
  - [Legend Interface](#legend-interface)
  - [Technical Indicator Interfaces](#technical-indicator-interfaces)
  - [Trendline Interfaces](#trendline-interfaces)
  - [Period Selector Interfaces](#period-selector-interfaces)
  - [Stock Event Setting Interfaces](#stock-event-setting-interfaces)
  - [Annotation Interfaces](#annotation-interfaces)
  - [Range Navigator Configuration Interfaces](#range-navigator-configuration-interfaces)
  - [Range Navigator Style Interfaces](#range-navigator-style-interfaces)
  - [Shared Chart Layout Interfaces](#shared-chart-layout-interfaces)
  - [Stock Chart Lifecycle Event Interfaces](#stock-chart-lifecycle-event-interfaces)
  - [Stock Chart Series and Point Event Interfaces](#stock-chart-series-and-point-event-interfaces)
  - [Stock Chart Axis Event Interfaces](#stock-chart-axis-event-interfaces)
  - [Stock Chart Tooltip Event Interfaces](#stock-chart-tooltip-event-interfaces)
  - [Stock Chart Legend Event Interfaces](#stock-chart-legend-event-interfaces)
  - [Stock Chart Interaction Event Interfaces](#stock-chart-interaction-event-interfaces)
  - [Stock Chart Range Selector Event Interfaces](#stock-chart-range-selector-event-interfaces)
  - [Stock Event Interfaces](#stock-event-interfaces)
  - [Export and Print Event Interfaces](#export-and-print-event-interfaces)
  - [Range Navigator Event Interfaces](#range-navigator-event-interfaces)
  - [Example Importing Interfaces](#example-importing-interfaces)
- [Understanding Stock Data Structure](#understanding-stock-data-structure)
  - [Data Format](#data-format)
- [Creating Your First Stock Chart with Data](#creating-your-first-stock-chart-with-data)
  - [Complete Working Example](#complete-working-example)
  - [Key Configuration Points](#key-configuration-points)
- [Adding Chart Title](#adding-chart-title)
- [Adding Crosshair for Precise Reading](#adding-crosshair-for-precise-reading)
- [Adding Trackball for Multi-Series](#adding-trackball-for-multi-series)
- [Complete Starter Template](#complete-starter-template)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)

## Installation and Dependencies

### Required Package

Install the Stock Chart package from npm:

```bash
npm install @syncfusion/ej2-react-charts --save
```

You may also need to import the required CSS for your chosen Syncfusion theme when using the component in a real application.

### Dependencies Tree

The `@syncfusion/ej2-react-charts` package includes these dependencies:

- `@syncfusion/ej2-base` - Base library
- `@syncfusion/ej2-data` - Data management
- `@syncfusion/ej2-charts` - Core charting library
- `@syncfusion/ej2-react-base` - React base
- `@syncfusion/ej2-pdf-export` - PDF export
- `@syncfusion/ej2-file-utils` - File utilities
- `@syncfusion/ej2-compression` - Compression
- `@syncfusion/ej2-svg-base` - SVG rendering
- `@syncfusion/ej2-navigations` - Navigation components
- `@syncfusion/ej2-calendars` - Calendar components
- `@syncfusion/ej2-popups` - Popup components
- `@syncfusion/ej2-lists` - List components
- `@syncfusion/ej2-inputs` - Input components
- `@syncfusion/ej2-buttons` - Button components
- `@syncfusion/ej2-splitbuttons` - Split button components

All dependencies are automatically installed with the main package.

## Project Setup

### Using Vite Recommended

Vite provides faster development and smaller bundle sizes. Create a new React project:

```bash
npm create vite@latest my-stock-app
cd my-stock-app
npm install
npm install @syncfusion/ej2-react-charts --save
npm run dev
```

For TypeScript:

```bash
npm create vite@latest my-stock-app -- --template react-ts
cd my-stock-app
npm install
npm install @syncfusion/ej2-react-charts --save
npm run dev
```

For JavaScript:

```bash
npm create vite@latest my-stock-app -- --template react
cd my-stock-app
npm install
npm install @syncfusion/ej2-react-charts --save
npm run dev
```

### Using Create React App Alternative

```bash
npx create-react-app my-stock-app
cd my-stock-app
npm install @syncfusion/ej2-react-charts --save
npm start
```

## Basic Stock Chart Implementation

### Minimal Example

Add the Stock Chart component to your `src/App.tsx` or `src/App.jsx` file:

```typescript
import { StockChartComponent } from '@syncfusion/ej2-react-charts';
import * as React from 'react';
import * as ReactDOM from 'react-dom/client';

function App() {
  return <StockChartComponent />;
}

export default App;

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);
root.render(<App />);
```

This creates an empty stock chart container. Add data and inject the required modules to render a functional stock chart.

## Module Injection

React Stock Chart features are modular and require module injection to enable them. This reduces bundle size by loading only the required stock chart series, range navigator series, axis types, indicators, and interactive features.

Because Stock Chart includes range selection behavior, the injected modules can include both Stock Chart modules and Range Navigator-related modules.

### Inject Modules

```tsx
import * as React from 'react';
import {
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  Inject,
  LineSeries,
  SplineSeries,
  AreaSeries,
  StepLineSeries,
  RangeAreaSeries,
  HiloSeries,
  HiloOpenCloseSeries,
  CandleSeries,
  ColumnSeries,
  DateTime,
  DateTimeCategory,
  Category,
  Logarithmic,
  Tooltip,
  RangeTooltip,
  Crosshair,
  Zoom,
  StockLegend,
  SmaIndicator,
  EmaIndicator,
  TmaIndicator,
  AtrIndicator,
  AccumulationDistributionIndicator,
  BollingerBands,
  MacdIndicator,
  MomentumIndicator,
  RsiIndicator,
  StochasticIndicator,
  Trendlines,
  PeriodSelector,
  Export
} from '@syncfusion/ej2-react-charts';

function App() {
  const primaryXAxis: Object = {
    valueType: 'DateTime'
  };

  const data: Object[] = [
    { date: new Date('2024-01-01'), open: 120, high: 125, low: 118, close: 123, volume: 1000 },
    { date: new Date('2024-01-02'), open: 123, high: 128, low: 121, close: 126, volume: 1200 },
    { date: new Date('2024-01-03'), open: 126, high: 130, low: 124, close: 129, volume: 1400 }
  ];

  return (
    <StockChartComponent primaryXAxis={primaryXAxis}>
      <Inject
        services={[
          LineSeries,
          SplineSeries,
          AreaSeries,
          StepLineSeries,
          RangeAreaSeries,
          HiloSeries,
          HiloOpenCloseSeries,
          CandleSeries,
          ColumnSeries,
          DateTime,
          DateTimeCategory,
          Category,
          Logarithmic,
          Tooltip,
          RangeTooltip,
          Crosshair,
          Zoom,
          StockLegend,
          SmaIndicator,
          EmaIndicator,
          TmaIndicator,
          AtrIndicator,
          AccumulationDistributionIndicator,
          BollingerBands,
          MacdIndicator,
          MomentumIndicator,
          RsiIndicator,
          StochasticIndicator,
          Trendlines,
          PeriodSelector,
          Export
        ]}
      />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={data}
          type="Candle"
          xName="date"
          high="high"
          low="low"
          open="open"
          close="close"
          volume="volume"
          name="Stock"
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}

export default App;
```

### Essential Modules for Stock Charts

Common modules to inject:

- `CandleSeries` - Candle/candlestick charts
- `LineSeries` - Line charts
- `SplineSeries` - Spline/smooth line charts
- `HiloSeries` - High-Low range bars
- `HiloOpenCloseSeries` - OHLC bars
- `DateTime` - DateTime axis, essential for stock data
- `Tooltip` - Hover tooltips
- `RangeTooltip` - Range selector tooltips
- `Crosshair` - Crosshair lines
- `DataLabel` - Data labels on points
- `StockLegend` - Legend support for Stock Chart
- `PeriodSelector` - Period selector support for range filtering
- `Export` - Export and print support

### Stock Chart Series Modules

| Module | Purpose | Import package |
|--------|---------|----------------|
| `LineSeries` | Enable line series in Stock Chart | `@syncfusion/ej2-react-charts` |
| `SplineSeries` | Enable spline series in Stock Chart | `@syncfusion/ej2-react-charts` |
| `AreaSeries` | Enable area series in Stock Chart | `@syncfusion/ej2-react-charts` |
| `HiloSeries` | Enable high-low financial series in Stock Chart | `@syncfusion/ej2-react-charts` |
| `HiloOpenCloseSeries` | Enable high-low-open-close financial series in Stock Chart | `@syncfusion/ej2-react-charts` |
| `CandleSeries` | Enable candle and hollow candle financial series in Stock Chart | `@syncfusion/ej2-react-charts` |
| `ColumnSeries` | Enable column rendering for volume or chart-based stock visualization | `@syncfusion/ej2-react-charts` |

### Range Navigator Modules

| Module | Purpose | Import package |
|--------|---------|----------------|
| `LineSeries` | Enable line series rendering in the range navigator | `@syncfusion/ej2-react-charts` |
| `AreaSeries` | Enable area series rendering in the range navigator | `@syncfusion/ej2-react-charts` |
| `RangeAreaSeries` | Enable range area series rendering in the Stock Chart range selector | `@syncfusion/ej2-react-charts` |
| `StepLineSeries` | Enable step line series rendering in the range navigator | `@syncfusion/ej2-react-charts` |
| `RangeTooltip` | Enable tooltip support in the range navigator | `@syncfusion/ej2-react-charts` |
| `PeriodSelector` | Enable period selector support for range filtering | `@syncfusion/ej2-react-charts` |

### Axis Modules

| Module | Purpose | Import package |
|--------|---------|----------------|
| `DateTime` | Enable date-time axis support for stock data | `@syncfusion/ej2-react-charts` |
| `DateTimeCategory` | Enable date-time category axis support | `@syncfusion/ej2-react-charts` |
| `Category` | Enable category axis support | `@syncfusion/ej2-react-charts` |
| `Logarithmic` | Enable logarithmic axis support | `@syncfusion/ej2-react-charts` |

### User Interaction Modules

| Module | Purpose | Import package |
|--------|---------|----------------|
| `Tooltip` | Enable tooltip and trackball support in Stock Chart | `@syncfusion/ej2-react-charts` |
| `RangeTooltip` | Enable tooltip support in the range navigator | `@syncfusion/ej2-react-charts` |
| `Crosshair` | Enable crosshair interaction in Stock Chart | `@syncfusion/ej2-react-charts` |
| `Zoom` | Enable zooming and panning support in Stock Chart | `@syncfusion/ej2-react-charts` |

### Legend Module

| Module | Purpose | Import package |
|--------|---------|----------------|
| `StockLegend` | Enable legend support in Stock Chart | `@syncfusion/ej2-react-charts` |

### Technical Indicator Modules

| Module | Purpose | Import package |
|--------|---------|----------------|
| `SmaIndicator` | Enable Simple Moving Average indicator | `@syncfusion/ej2-react-charts` |
| `EmaIndicator` | Enable Exponential Moving Average indicator | `@syncfusion/ej2-react-charts` |
| `TmaIndicator` | Enable Triangular Moving Average indicator | `@syncfusion/ej2-react-charts` |
| `AtrIndicator` | Enable Average True Range indicator | `@syncfusion/ej2-react-charts` |
| `AccumulationDistributionIndicator` | Enable Accumulation Distribution indicator | `@syncfusion/ej2-react-charts` |
| `BollingerBands` | Enable Bollinger Bands indicator | `@syncfusion/ej2-react-charts` |
| `MacdIndicator` | Enable MACD indicator | `@syncfusion/ej2-react-charts` |
| `MomentumIndicator` | Enable Momentum indicator | `@syncfusion/ej2-react-charts` |
| `RsiIndicator` | Enable Relative Strength Index indicator | `@syncfusion/ej2-react-charts` |
| `StochasticIndicator` | Enable Stochastic indicator | `@syncfusion/ej2-react-charts` |

### Analysis Modules

| Module | Purpose | Import package |
|--------|---------|----------------|
| `Trendlines` | Enable trendline support in Stock Chart | `@syncfusion/ej2-react-charts` |

### Period Selector Module

| Module | Purpose | Import package |
|--------|---------|----------------|
| `PeriodSelector` | Enable period selector support for Stock Chart range filtering | `@syncfusion/ej2-react-charts` |

### Export Module

| Module | Purpose | Import package |
|--------|---------|----------------|
| `Export` | Enable Stock Chart export and print support | `@syncfusion/ej2-react-charts` |

### Example Full Stock Chart Module Injection

```tsx
import * as React from 'react';
import {
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  Inject,
  LineSeries,
  SplineSeries,
  AreaSeries,
  StepLineSeries,
  RangeAreaSeries,
  HiloSeries,
  HiloOpenCloseSeries,
  CandleSeries,
  ColumnSeries,
  DateTime,
  DateTimeCategory,
  Category,
  Logarithmic,
  Tooltip,
  RangeTooltip,
  Crosshair,
  Zoom,
  StockLegend,
  SmaIndicator,
  EmaIndicator,
  TmaIndicator,
  AtrIndicator,
  AccumulationDistributionIndicator,
  BollingerBands,
  MacdIndicator,
  MomentumIndicator,
  RsiIndicator,
  StochasticIndicator,
  Trendlines,
  PeriodSelector,
  Export
} from '@syncfusion/ej2-react-charts';

function App() {
  const data: Object[] = [
    { date: new Date('2024-01-01'), open: 120, high: 125, low: 118, close: 123, volume: 1000 },
    { date: new Date('2024-01-02'), open: 123, high: 128, low: 121, close: 126, volume: 1200 },
    { date: new Date('2024-01-03'), open: 126, high: 130, low: 124, close: 129, volume: 1400 }
  ];

  return (
    <StockChartComponent>
      <Inject
        services={[
          LineSeries,
          SplineSeries,
          AreaSeries,
          StepLineSeries,
          RangeAreaSeries,
          HiloSeries,
          HiloOpenCloseSeries,
          CandleSeries,
          ColumnSeries,
          DateTime,
          DateTimeCategory,
          Category,
          Logarithmic,
          Tooltip,
          RangeTooltip,
          Crosshair,
          Zoom,
          StockLegend,
          SmaIndicator,
          EmaIndicator,
          TmaIndicator,
          AtrIndicator,
          AccumulationDistributionIndicator,
          BollingerBands,
          MacdIndicator,
          MomentumIndicator,
          RsiIndicator,
          StochasticIndicator,
          Trendlines,
          PeriodSelector,
          Export
        ]}
      />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={data}
          type="Candle"
          xName="date"
          high="high"
          low="low"
          open="open"
          close="close"
          volume="volume"
          name="Stock"
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}

export default App;
```

## Interfaces

React Stock Chart provides TypeScript interfaces to strongly type stock chart configuration, range navigator configuration, axis settings, series settings, indicators, trendlines, stock events, annotations, tooltips, legends, and event arguments.

### Stock Chart Configuration Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `StockChartModel` | Defines the complete configuration model for the Stock Chart component | `@syncfusion/ej2-react-charts` |
| `StockChartAreaModel` | Defines stock chart area customization options such as background and border | `@syncfusion/ej2-react-charts` |
| `StockChartBorderModel` | Defines stock chart border color and width settings | `@syncfusion/ej2-react-charts` |
| `StockChartFontModel` | Defines font style, size, color, weight, and family settings used in Stock Chart | `@syncfusion/ej2-react-charts` |
| `StockMarginModel` | Defines margin settings for the Stock Chart | `@syncfusion/ej2-react-charts` |

### Stock Chart Axis Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `StockChartAxisModel` | Defines configuration for primary and secondary Stock Chart axes | `@syncfusion/ej2-react-charts` |
| `StockChartRowModel` | Defines row configuration for multi-row Stock Chart layout | `@syncfusion/ej2-react-charts` |
| `StockChartColumnModel` | Defines column configuration for multi-column Stock Chart layout | `@syncfusion/ej2-react-charts` |
| `MajorGridLinesModel` | Defines major grid line settings for chart axes | `@syncfusion/ej2-react-charts` |
| `MinorGridLinesModel` | Defines minor grid line settings for chart axes | `@syncfusion/ej2-react-charts` |
| `MajorTickLinesModel` | Defines major tick line settings for chart axes | `@syncfusion/ej2-react-charts` |
| `MinorTickLinesModel` | Defines minor tick line settings for chart axes | `@syncfusion/ej2-react-charts` |
| `AxisLineModel` | Defines axis line style settings | `@syncfusion/ej2-react-charts` |
| `CrosshairTooltipModel` | Defines crosshair tooltip settings for Stock Chart axes | `@syncfusion/ej2-react-charts` |
| `StripLineSettingsModel` | Defines strip line settings for Stock Chart axes | `@syncfusion/ej2-react-charts` |

### Stock Chart Series Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `StockChartSeriesModel` | Defines Stock Chart series configuration | `@syncfusion/ej2-react-charts` |
| `StockChartEmptyPointSettingsModel` | Defines empty point behavior and appearance for Stock Chart series | `@syncfusion/ej2-react-charts` |
| `StockChartConnectorModel` | Defines connector line settings used by labels and related Stock Chart elements | `@syncfusion/ej2-react-charts` |
| `StockChartIndexesModel` | Defines series and point index information used for selection or highlighting | `@syncfusion/ej2-react-charts` |
| `AnimationModel` | Defines animation duration, delay, and enable settings for chart rendering | `@syncfusion/ej2-react-charts` |
| `BorderModel` | Defines border color, width, and dash array settings used by series and chart elements | `@syncfusion/ej2-react-charts` |
| `MarkerSettingsModel` | Defines marker settings for chart series points | `@syncfusion/ej2-react-charts` |
| `DataLabelSettingsModel` | Defines data label settings for chart points | `@syncfusion/ej2-react-charts` |
| `EmptyPointSettingsModel` | Defines empty point behavior and appearance for chart series | `@syncfusion/ej2-react-charts` |

### Tooltip and Crosshair Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `TooltipSettingsModel` | Defines Stock Chart tooltip settings | `@syncfusion/ej2-react-charts` |
| `TooltipLocationModel` | Defines tooltip location settings | `@syncfusion/ej2-react-charts` |
| `CrosshairSettingsModel` | Defines crosshair settings for Stock Chart interaction | `@syncfusion/ej2-react-charts` |
| `CrosshairTooltipModel` | Defines tooltip settings displayed with the crosshair | `@syncfusion/ej2-react-charts` |

### Legend Interface

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `StockChartLegendSettingsModel` | Defines Stock Chart legend settings | `@syncfusion/ej2-react-charts` |
| `LegendSettingsModel` | Defines shared chart legend settings | `@syncfusion/ej2-react-charts` |

### Technical Indicator Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `StockChartIndicatorModel` | Defines Stock Chart technical indicator settings such as SMA, EMA, RSI, MACD, Bollinger Bands, Momentum, ATR, TMA, Stochastic, and Accumulation Distribution indicators | `@syncfusion/ej2-react-charts` |
| `TechnicalIndicatorModel` | Defines shared technical indicator settings | `@syncfusion/ej2-react-charts` |

### Trendline Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `StockChartTrendlineModel` | Defines trendline settings for Stock Chart series | `@syncfusion/ej2-react-charts` |
| `TrendlineModel` | Defines shared trendline settings for chart series | `@syncfusion/ej2-react-charts` |
| `TrendlineMarkerModel` | Defines marker settings for trendline points | `@syncfusion/ej2-react-charts` |

### Period Selector Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `StockChartPeriodModel` | Defines period selector button configuration for Stock Chart | `@syncfusion/ej2-react-charts` |
| `PeriodSelectorSettingsModel` | Defines period selector configuration used for range filtering | `@syncfusion/ej2-react-charts` |
| `PeriodModel` | Defines individual period button settings | `@syncfusion/ej2-react-charts` |

### Stock Event Setting Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `StockEventsSettingsModel` | Defines stock event marker settings such as date, text, description, type, background, border, and series indexes | `@syncfusion/ej2-react-charts` |
| `StockChartStockEventsModel` | Defines Stock Chart stock event collection settings | `@syncfusion/ej2-react-charts` |

### Annotation Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `StockChartAnnotationSettingsModel` | Defines annotation settings for Stock Chart | `@syncfusion/ej2-react-charts` |
| `ChartAnnotationSettingsModel` | Defines shared annotation settings for chart | `@syncfusion/ej2-react-charts` |

### Range Navigator Configuration Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `RangeNavigatorModel` | Defines the complete configuration model for the Range Navigator component | `@syncfusion/ej2-react-charts` |
| `RangeNavigatorSeriesModel` | Defines Range Navigator series configuration | `@syncfusion/ej2-react-charts` |
| `RangeNavigatorMajorGridLinesModel` | Defines major grid line settings for Range Navigator | `@syncfusion/ej2-react-charts` |
| `RangeNavigatorMajorTickLinesModel` | Defines major tick line settings for Range Navigator | `@syncfusion/ej2-react-charts` |
| `RangeNavigatorLabelStyleModel` | Defines label style settings for Range Navigator axis labels | `@syncfusion/ej2-react-charts` |
| `RangeNavigatorMarginModel` | Defines margin settings for Range Navigator | `@syncfusion/ej2-react-charts` |

### Range Navigator Style Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `RangeNavigatorStyleSettingsModel` | Defines selected region, unselected region, thumb, grid, and background style settings | `@syncfusion/ej2-react-charts` |
| `RangeNavigatorThumbSettingsModel` | Defines thumb border, fill, size, and type settings | `@syncfusion/ej2-react-charts` |
| `RangeNavigatorBorderModel` | Defines border settings for Range Navigator elements | `@syncfusion/ej2-react-charts` |
| `RangeNavigatorFontModel` | Defines font settings for Range Navigator labels and text | `@syncfusion/ej2-react-charts` |

### Shared Chart Layout Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `ChartAreaModel` | Defines chart area customization options such as background and border | `@syncfusion/ej2-react-charts` |
| `MarginModel` | Defines margin settings for chart components | `@syncfusion/ej2-react-charts` |
| `FontModel` | Defines font style, size, color, weight, and family settings | `@syncfusion/ej2-react-charts` |
| `BorderModel` | Defines border color, width, and dash array settings | `@syncfusion/ej2-react-charts` |

### Stock Chart Lifecycle Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `IStockChartEventArgs` | Defines common Stock Chart event arguments for load, loaded, and Stock Chart lifecycle events | `@syncfusion/ej2-react-charts` |
| `ILoadEventArgs` | Defines event arguments for chart load event | `@syncfusion/ej2-react-charts` |
| `ILoadedEventArgs` | Defines event arguments after chart rendering is completed | `@syncfusion/ej2-react-charts` |
| `IResizeEventArgs` | Defines event arguments for chart resize events | `@syncfusion/ej2-react-charts` |

### Stock Chart Series and Point Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `IPointEventArgs` | Defines event arguments for point mouse and interaction events | `@syncfusion/ej2-react-charts` |
| `IPointRenderEventArgs` | Defines event arguments used while rendering each chart point | `@syncfusion/ej2-react-charts` |
| `ISeriesRenderEventArgs` | Defines event arguments used while rendering each Stock Chart series | `@syncfusion/ej2-react-charts` |
| `ITextRenderEventArgs` | Defines event arguments used while rendering chart text such as labels | `@syncfusion/ej2-react-charts` |

### Stock Chart Axis Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `IAxisLabelRenderEventArgs` | Defines event arguments used while rendering axis labels | `@syncfusion/ej2-react-charts` |
| `IAxisRangeCalculatedEventArgs` | Defines event arguments after axis range calculation | `@syncfusion/ej2-react-charts` |

### Stock Chart Tooltip Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `ITooltipRenderEventArgs` | Defines event arguments used while rendering Stock Chart tooltip | `@syncfusion/ej2-react-charts` |
| `ISharedTooltipRenderEventArgs` | Defines event arguments used while rendering shared tooltip content | `@syncfusion/ej2-react-charts` |
| `ITooltipRenderCompleteEventArgs` | Defines event arguments after tooltip rendering is completed | `@syncfusion/ej2-react-charts` |

### Stock Chart Legend Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `IStockLegendRenderEventArgs` | Defines event arguments used while rendering Stock Chart legend items | `@syncfusion/ej2-react-charts` |
| `IStockLegendClickEventArgs` | Defines event arguments for Stock Chart legend click events | `@syncfusion/ej2-react-charts` |
| `ILegendRenderEventArgs` | Defines shared chart legend render event arguments | `@syncfusion/ej2-react-charts` |
| `ILegendClickEventArgs` | Defines shared chart legend click event arguments | `@syncfusion/ej2-react-charts` |

### Stock Chart Interaction Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `IMouseEventArgs` | Defines event arguments for Stock Chart mouse events | `@syncfusion/ej2-react-charts` |
| `IZoomingEventArgs` | Defines event arguments while zooming is performed | `@syncfusion/ej2-react-charts` |
| `IZoomCompleteEventArgs` | Defines event arguments after zooming is completed | `@syncfusion/ej2-react-charts` |
| `ISelectionCompleteEventArgs` | Defines event arguments after point or series selection is completed | `@syncfusion/ej2-react-charts` |

### Stock Chart Range Selector Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `IRangeChangeEventArgs` | Defines event arguments when the Stock Chart range is changed | `@syncfusion/ej2-react-charts` |
| `IRangeSelectorRenderEventArgs` | Defines event arguments before the range selector is rendered | `@syncfusion/ej2-react-charts` |

### Stock Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `IStockEventRenderArgs` | Defines event arguments used while rendering stock event markers | `@syncfusion/ej2-react-charts` |

### Export and Print Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `IPrintEventArgs` | Defines event arguments for Stock Chart print events | `@syncfusion/ej2-react-charts` |
| `IExportEventArgs` | Defines event arguments for Stock Chart export events | `@syncfusion/ej2-react-charts` |

### Range Navigator Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `IRangeLoadedEventArgs` | Defines event arguments for Range Navigator load and loaded events | `@syncfusion/ej2-react-charts` |
| `IRangeBeforeResizeEventArgs` | Defines event arguments before Range Navigator resize | `@syncfusion/ej2-react-charts` |
| `IResizeRangeNavigatorEventArgs` | Defines event arguments after Range Navigator resize | `@syncfusion/ej2-react-charts` |
| `IChangedEventArgs` | Defines event arguments after the selected Range Navigator range changes | `@syncfusion/ej2-react-charts` |
| `ILabelRenderEventsArgs` | Defines event arguments before Range Navigator labels are rendered | `@syncfusion/ej2-react-charts` |
| `IRangeSelectorRenderEventArgs` | Defines event arguments before the Range Navigator selector is rendered | `@syncfusion/ej2-react-charts` |
| `IRangeTooltipRenderEventArgs` | Defines event arguments before Range Navigator tooltip rendering | `@syncfusion/ej2-react-charts` |

### Example Importing Interfaces

```tsx
import {
  StockChartModel,
  StockChartAxisModel,
  StockChartSeriesModel,
  StockChartIndicatorModel,
  StockChartTrendlineModel,
  StockChartPeriodModel,
  StockEventsSettingsModel,
  StockChartAnnotationSettingsModel,
  TooltipSettingsModel,
  CrosshairSettingsModel,
  StockChartLegendSettingsModel,
  RangeNavigatorModel,
  RangeNavigatorSeriesModel,
  IStockChartEventArgs,
  IStockLegendClickEventArgs,
  IStockLegendRenderEventArgs,
  IStockEventRenderArgs,
  IRangeChangeEventArgs,
  IRangeSelectorRenderEventArgs,
  ITooltipRenderEventArgs,
  IAxisLabelRenderEventArgs,
  ISeriesRenderEventArgs,
  IPointEventArgs,
  IMouseEventArgs,
  IExportEventArgs,
  IPrintEventArgs
} from '@syncfusion/ej2-react-charts';

const primaryXAxis: StockChartAxisModel = {
  valueType: 'DateTime'
};

const tooltip: TooltipSettingsModel = {
  enable: true
};

const crosshair: CrosshairSettingsModel = {
  enable: true
};

const series: StockChartSeriesModel = {
  dataSource: [
    { date: new Date('2024-01-01'), open: 120, high: 125, low: 118, close: 123, volume: 1000 },
    { date: new Date('2024-01-02'), open: 123, high: 128, low: 121, close: 126, volume: 1200 },
    { date: new Date('2024-01-03'), open: 126, high: 130, low: 124, close: 129, volume: 1400 }
  ],
  xName: 'date',
  type: 'Candle',
  high: 'high',
  low: 'low',
  open: 'open',
  close: 'close',
  volume: 'volume',
  name: 'Stock'
};

const indicator: StockChartIndicatorModel = {
  type: 'Sma',
  field: 'Close',
  seriesName: 'Stock'
};

const trendline: StockChartTrendlineModel = {
  type: 'Linear'
};

const period: StockChartPeriodModel = {
  intervalType: 'Months',
  interval: 1,
  text: '1M'
};

const stockEvent: StockEventsSettingsModel = {
  date: new Date('2024-01-02'),
  text: 'E',
  description: 'Stock event',
  type: 'Flag'
};

const annotation: StockChartAnnotationSettingsModel = {
  content: '<div>Annotation</div>',
  coordinateUnits: 'Point',
  x: new Date('2024-01-02'),
  y: 126
};

const legendSettings: StockChartLegendSettingsModel = {
  visible: true,
  position: 'Top'
};

const stockChartOptions: StockChartModel = {
  primaryXAxis,
  tooltip,
  crosshair,
  series: [series],
  indicators: [indicator],
  trendlines: [trendline],
  periods: [period],
  stockEvents: [stockEvent],
  annotations: [annotation],
  legendSettings
};

const rangeNavigatorSeries: RangeNavigatorSeriesModel = {
  dataSource: [
    { x: new Date('2024-01-01'), y: 123 },
    { x: new Date('2024-01-02'), y: 126 },
    { x: new Date('2024-01-03'), y: 129 }
  ],
  xName: 'x',
  yName: 'y',
  type: 'Line'
};

const rangeNavigatorOptions: RangeNavigatorModel = {
  valueType: 'DateTime',
  series: [rangeNavigatorSeries],
  tooltip: {
    enable: true
  }
};

const load = (args: IStockChartEventArgs): void => {
  // Stock Chart loading.
};

const legendClick = (args: IStockLegendClickEventArgs): void => {
  // Stock Chart legend clicked.
};

const legendRender = (args: IStockLegendRenderEventArgs): void => {
  // Stock Chart legend rendering.
};

const stockEventRender = (args: IStockEventRenderArgs): void => {
  // Stock event marker rendering.
};

const rangeChange = (args: IRangeChangeEventArgs): void => {
  // Stock Chart selected range changed.
};

const selectorRender = (args: IRangeSelectorRenderEventArgs): void => {
  // Range selector rendering.
};

const tooltipRender = (args: ITooltipRenderEventArgs): void => {
  // Tooltip rendering.
};

const axisLabelRender = (args: IAxisLabelRenderEventArgs): void => {
  // Axis label rendering.
};

const seriesRender = (args: ISeriesRenderEventArgs): void => {
  // Series rendering.
};

const pointClick = (args: IPointEventArgs): void => {
  // Point clicked.
};

const stockChartMouseMove = (args: IMouseEventArgs): void => {
  // Stock Chart mouse move.
};

const beforeExport = (args: IExportEventArgs): void => {
  // Before Stock Chart export.
};

const beforePrint = (args: IPrintEventArgs): void => {
  // Before Stock Chart print.
};
```

## Understanding Stock Data Structure

Stock Chart expects data in a specific format with datetime and OHLC (Open, High, Low, Close) values.

### Data Format

```typescript
const stockData = [
  {
    x: new Date('2012-04-02T00:00:00.000Z'),
    open: 320.705719,
    high: 324.074066,
    low: 317.737732,
    close: 323.783783,
    volume: 45638000
  },
  {
    x: new Date('2012-04-03T00:00:00.000Z'),
    open: 323.028015,
    high: 324.299286,
    low: 319.639648,
    close: 321.631622,
    volume: 40857000
  }
];
```

**Required fields for different series types:**

- **Candle/HiloOpenClose:** `x`, `open`, `high`, `low`, `close`
- **Hilo:** `x`, `high`, `low`
- **Line/Spline:** `x`, `close` or any y-value field
- **Volume:** `volume` field for optional volume visualization

## Creating Your First Stock Chart with Data

### Complete Working Example

```typescript
import {
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  Inject,
  DateTime,
  Tooltip,
  RangeTooltip,
  Crosshair,
  CandleSeries
} from '@syncfusion/ej2-react-charts';
import * as React from 'react';

function App() {
  const data = [
    {
      x: new Date('2012-04-02'),
      open: 320.705719,
      high: 324.074066,
      low: 317.737732,
      close: 323.783783,
      volume: 45638000
    },
    {
      x: new Date('2012-04-03'),
      open: 323.028015,
      high: 324.299286,
      low: 319.639648,
      close: 321.631622,
      volume: 40857000
    },
    {
      x: new Date('2012-04-04'),
      open: 319.544556,
      high: 319.819824,
      low: 315.865875,
      close: 317.892883,
      volume: 32519000
    },
    {
      x: new Date('2012-04-05'),
      open: 316.436432,
      high: 318.533539,
      low: 314.599609,
      close: 316.476471,
      volume: 46327000
    }
  ];

  return (
    <StockChartComponent
      id="stockchart"
      primaryXAxis={{
        valueType: 'DateTime'
      }}
    >
      <Inject services={[DateTime, Tooltip, RangeTooltip, Crosshair, CandleSeries]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={data}
          type="Candle"
          xName="x"
          high="high"
          low="low"
          open="open"
          close="close"
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}

export default App;
```

### Key Configuration Points

1. **Primary X-axis with DateTime:** Always set `valueType: 'DateTime'` for stock data.
2. **Series dataSource:** Bind your data array to the Stock Chart series.
3. **Series type:** Choose from `Candle`, `Line`, `Spline`, `Hilo`, and `HiloOpenClose`.
4. **Field mapping:** Map data fields to chart properties such as `xName`, `high`, `low`, `open`, and `close`.

## Adding Chart Title

Provide context with a descriptive title:

```typescript
<StockChartComponent
  id="stockchart"
  title="AAPL Stock Price"
  primaryXAxis={{ valueType: 'DateTime' }}
>
  {/* series configuration */}
</StockChartComponent>
```

## Adding Crosshair for Precise Reading

Crosshair adds vertical and horizontal lines to help users read exact values:

```typescript
<StockChartComponent
  id="stockchart"
  title="Stock Price with Crosshair"
  primaryXAxis={{ valueType: 'DateTime' }}
  crosshair={{
    enable: true,
    lineType: 'Both'
  }}
>
  <Inject services={[DateTime, Tooltip, RangeTooltip, Crosshair, CandleSeries]} />
  {/* series */}
</StockChartComponent>
```

## Adding Trackball for Multi-Series

Trackball shows a shared tooltip across all series at the mouse position:

```typescript
<StockChartComponent
  id="stockchart"
  primaryXAxis={{ valueType: 'DateTime' }}
  crosshair={{ enable: true }}
  tooltip={{ enable: true, shared: true }}
>
  <Inject services={[DateTime, Tooltip, RangeTooltip, Crosshair, CandleSeries]} />
  {/* series */}
</StockChartComponent>
```

## Complete Starter Template

Here's a complete, production-ready starter template:

```typescript
import {
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  Inject,
  DateTime,
  Tooltip,
  RangeTooltip,
  Crosshair,
  LineSeries,
  SplineSeries,
  CandleSeries,
  HiloOpenCloseSeries,
  HiloSeries,
  RangeAreaSeries,
  Trendlines
} from '@syncfusion/ej2-react-charts';
import * as React from 'react';

function StockChartApp() {
  const stockData = [
    { x: new Date('2012-04-02'), open: 85.97, high: 90.58, low: 85.97, close: 90.58, volume: 660187068 },
    { x: new Date('2012-04-09'), open: 89.02, high: 92.50, low: 88.50, close: 92.90, volume: 490033264 },
    { x: new Date('2012-04-16'), open: 92.52, high: 93.00, low: 88.50, close: 92.52, volume: 450167016 }
  ];

  return (
    <div style={{ padding: '20px' }}>
      <StockChartComponent
        id="stockchart"
        title="Stock Price Analysis"
        primaryXAxis={{ valueType: 'DateTime' }}
        crosshair={{ enable: true }}
        tooltip={{ enable: true }}
        height="450px"
      >
        <Inject services={[
          DateTime,
          Tooltip,
          RangeTooltip,
          Crosshair,
          LineSeries,
          SplineSeries,
          CandleSeries,
          HiloOpenCloseSeries,
          HiloSeries,
          RangeAreaSeries,
          Trendlines
        ]} />
        <StockChartSeriesCollectionDirective>
          <StockChartSeriesDirective
            dataSource={stockData}
            type="Candle"
            xName="x"
            high="high"
            low="low"
            open="open"
            close="close"
            volume="volume"
          />
        </StockChartSeriesCollectionDirective>
      </StockChartComponent>
    </div>
  );
}

export default StockChartApp;
```

## Troubleshooting

**Chart not displaying:**

- Ensure the `DateTime` module is injected.
- Verify `primaryXAxis.valueType` is set to `'DateTime'`.
- Check the data format. The x field should contain valid `Date` objects.
- Confirm the series type module is injected, such as `CandleSeries` for candle charts.

**Data not showing:**

- Verify field mappings such as `xName`, `high`, `low`, `open`, and `close`.
- Check that the data array is not empty.
- Ensure date values are valid `Date` objects.

**Console errors about modules:**

- Add the missing module to the `Inject` services array.
- Import the module from `@syncfusion/ej2-react-charts`.

## Next Steps

After getting your basic stock chart running:

1. **Explore different series types** - Try Line, Spline, Hilo, HiloOpenClose, and Candle.
2. **Add period selector** - Add quick navigation buttons for date ranges such as 1D, 5D, and 1M.
3. **Configure range selector** - Add thumb-based range selection.
4. **Add technical indicators** - Add SMA, EMA, RSI, MACD, and Bollinger Bands.
5. **Customize appearance** - Configure colors, themes, and gradients.
6. **Add stock events** - Mark significant events on the chart.
7. **Enable export/print** - Allow users to save or print charts.
