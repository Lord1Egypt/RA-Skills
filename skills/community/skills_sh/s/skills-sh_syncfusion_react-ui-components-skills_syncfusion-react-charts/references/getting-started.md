# Getting Started with Syncfusion React Charts

This guide covers the complete setup process for integrating the Syncfusion React Charts component into your React application, from installation through creating your first chart.

## Table of Contents

- [Installation and Package Setup](#installation-and-package-setup)
  - [Install Required Packages](#install-required-packages)
  - [Import Required Modules](#import-required-modules)
- [Creating Your First Chart](#creating-your-first-chart)
  - [Minimal Chart Example](#minimal-chart-example)
  - [Chart with Title and Axes Labels](#chart-with-title-and-axes-labels)
- [Basic Chart Configuration](#basic-chart-configuration)
  - [Chart Sizing](#chart-sizing)
  - [Adding Legend](#adding-legend)
  - [Adding Tooltip](#adding-tooltip)
- [Module Injection](#module-injection)
  - [Inject Services](#inject-services)
  - [Series Modules](#series-modules)
  - [Axis Modules](#axis-modules)
  - [User Interaction Modules](#user-interaction-modules)
  - [Label and Annotation Modules](#label-and-annotation-modules)
  - [Legend Module](#legend-module)
  - [Technical Indicator Modules](#technical-indicator-modules)
  - [Analysis Modules](#analysis-modules)
  - [Export Module](#export-module)
  - [Example Full Chart Injection](#example-full-chart-injection)
- [Interfaces](#interfaces)
  - [Chart Configuration Interfaces](#chart-configuration-interfaces)
  - [Axis Interfaces](#axis-interfaces)
  - [Series Interfaces](#series-interfaces)
  - [Tooltip and Crosshair Interfaces](#tooltip-and-crosshair-interfaces)
  - [Legend Interface](#legend-interface)
  - [Zoom and Selection Interfaces](#zoom-and-selection-interfaces)
  - [Annotation Interface](#annotation-interface)
  - [Analysis Interfaces](#analysis-interfaces)
  - [Technical Indicator Interface](#technical-indicator-interface)
  - [Lifecycle Event Interfaces](#lifecycle-event-interfaces)
  - [Series and Point Event Interfaces](#series-and-point-event-interfaces)
  - [Axis Event Interfaces](#axis-event-interfaces)
  - [Tooltip Event Interfaces](#tooltip-event-interfaces)
  - [Legend Event Interfaces](#legend-event-interfaces)
  - [Interaction Event Interfaces](#interaction-event-interfaces)
  - [Annotation Event Interface](#annotation-event-interface)
  - [Export and Print Event Interfaces](#export-and-print-event-interfaces)
  - [Animation Event Interface](#animation-event-interface)
  - [Example Importing Interfaces](#example-importing-interfaces)
- [Common Setup Issues](#common-setup-issues)
  - [Issue Chart Not Rendering](#issue-chart-not-rendering)
  - [Issue Data Not Displaying](#issue-data-not-displaying)
  - [Issue Labels Not Showing on Axes](#issue-labels-not-showing-on-axes)
- [Full Example Sales Chart with Multiple Features](#full-example-sales-chart-with-multiple-features)
- [Additional Configuration Options](#additional-configuration-options)
  - [Theme Selection](#theme-selection)
  - [Background and Borders](#background-and-borders)
  - [Animation Control](#animation-control)
  - [No Data Template](#no-data-template)
- [Quick Reference](#quick-reference)

## Installation and Package Setup

### Install Required Packages

```bash
npm install @syncfusion/ej2-react-charts @syncfusion/ej2-base
```

### Import Required Modules

```jsx
import {
  ChartComponent,
  SeriesCollectionDirective,
  SeriesDirective,
  Inject,
  LineSeries,
  Category,
  Legend,
  Tooltip
} from '@syncfusion/ej2-react-charts';
```

The `Inject` component is required to register the chart modules that your chart uses, such as `LineSeries`, `Category`, `Legend`, and `Tooltip`. Without injecting the required modules, those features will not work.

**Available themes:**

- `Material` - Material Design
- `Bootstrap` - Bootstrap theme
- `Bootstrap4` - Bootstrap 4 theme
- `Tailwind` - Tailwind CSS theme

Choose the theme that matches your application's design system. Use only one theme import at a time.

## Creating Your First Chart

### Minimal Chart Example

```jsx
import React from 'react';
import {
  ChartComponent,
  SeriesCollectionDirective,
  SeriesDirective,
  Inject,
  LineSeries,
  Category
} from '@syncfusion/ej2-react-charts';

export default function MyChart() {
  const chartData = [
    { month: 'Jan', sales: 35 },
    { month: 'Feb', sales: 28 },
    { month: 'Mar', sales: 34 },
    { month: 'Apr', sales: 32 },
    { month: 'May', sales: 40 }
  ];

  return (
    <ChartComponent>
      <Inject services={[LineSeries, Category]} />
      <SeriesCollectionDirective>
        <SeriesDirective
          dataSource={chartData}
          xName="month"
          yName="sales"
          type="Line"
        />
      </SeriesCollectionDirective>
    </ChartComponent>
  );
}
```

**What this does:**

- `ChartComponent`: Main chart container
- `SeriesCollectionDirective`: Container for all chart series
- `SeriesDirective`: Single data series with X/Y mapping
- `Inject`: Registers `LineSeries` and `Category` axis modules

### Chart with Title and Axes Labels

```jsx
<ChartComponent
  id="sales-chart"
  primaryXAxis={{ valueType: 'Category', labelFormat: '{value}' }}
  primaryYAxis={{ labelFormat: '${value}K' }}
  title="Monthly Sales"
  subTitle="Q1 2024 Performance"
>
  <Inject services={[LineSeries, Category]} />
  <SeriesCollectionDirective>
    <SeriesDirective
      dataSource={chartData}
      xName="month"
      yName="sales"
      type="Line"
      name="Sales"
    />
  </SeriesCollectionDirective>
</ChartComponent>
```

**Key additions:**

- `id`: Unique identifier for the chart, especially when rendering multiple charts
- `primaryXAxis`: Configures category values with label formatting
- `primaryYAxis`: Formats Y-axis labels, such as currency with a `$` symbol
- `title`: Main chart heading displayed at the top
- `subTitle`: Additional context displayed below the title
- `name`: Series name for legend display

## Basic Chart Configuration

### Chart Sizing

Set explicit dimensions to control layout:

```jsx
<ChartComponent width="800px" height="400px">
  {/* chart content */}
</ChartComponent>
```

**Responsive sizing** is recommended for modern apps:

```jsx
<ChartComponent width="100%" height="400px">
  {/* chart content */}
</ChartComponent>
```

This makes the chart responsive to the container width while maintaining a fixed height.

### Adding Legend

```jsx
<ChartComponent legendSettings={{ visible: true, position: 'Right' }}>
  <Inject services={[LineSeries, Category, Legend]} />
  {/* series */}
</ChartComponent>
```

**Legend positions:** `Top`, `Bottom`, `Left`, `Right`, `Custom`

### Adding Tooltip

```jsx
<ChartComponent tooltip={{ enable: true, shared: true }}>
  <Inject services={[LineSeries, Category, Tooltip]} />
  {/* series */}
</ChartComponent>
```

**Tooltip props:**

- `enable`: Shows tooltips on hover
- `shared`: Displays all series values at once for multi-series charts
- `template`: Defines a custom HTML template for tooltip content

## Module Injection

React Chart features are modular and require injection to enable them. This reduces bundle size by loading only the required chart series, axis types, indicators, and interactive features.

### Inject Services

```tsx
import {
  ChartComponent,
  SeriesCollectionDirective,
  SeriesDirective,
  Inject,
  LineSeries,
  ColumnSeries,
  Category,
  Legend,
  Tooltip,
  DataLabel
} from '@syncfusion/ej2-react-charts';

<ChartComponent primaryXAxis={{ valueType: 'Category' }}>
  <SeriesCollectionDirective>
    <SeriesDirective
      dataSource={data}
      xName="x"
      yName="y"
      type="Line"
      name="Sales"
    />
  </SeriesCollectionDirective>

  <Inject services={[LineSeries, ColumnSeries, Category, Legend, Tooltip, DataLabel]} />
</ChartComponent>
```

### Series Modules

| Module | Purpose | Import package |
|--------|---------|----------------|
| `LineSeries` | Enable line chart series | `@syncfusion/ej2-react-charts` |
| `ColumnSeries` | Enable column chart series | `@syncfusion/ej2-react-charts` |
| `BarSeries` | Enable bar chart series | `@syncfusion/ej2-react-charts` |
| `AreaSeries` | Enable area chart series | `@syncfusion/ej2-react-charts` |
| `SplineSeries` | Enable spline chart series | `@syncfusion/ej2-react-charts` |
| `SplineAreaSeries` | Enable spline area chart series | `@syncfusion/ej2-react-charts` |
| `StepLineSeries` | Enable step line chart series | `@syncfusion/ej2-react-charts` |
| `StepAreaSeries` | Enable step area chart series | `@syncfusion/ej2-react-charts` |
| `ScatterSeries` | Enable scatter chart series | `@syncfusion/ej2-react-charts` |
| `BubbleSeries` | Enable bubble chart series | `@syncfusion/ej2-react-charts` |
| `RangeColumnSeries` | Enable range column chart series | `@syncfusion/ej2-react-charts` |
| `RangeAreaSeries` | Enable range area chart series | `@syncfusion/ej2-react-charts` |
| `SplineRangeAreaSeries` | Enable spline range area chart series | `@syncfusion/ej2-react-charts` |
| `HiloSeries` | Enable high-low chart series | `@syncfusion/ej2-react-charts` |
| `HiloOpenCloseSeries` | Enable high-low-open-close chart series | `@syncfusion/ej2-react-charts` |
| `CandleSeries` | Enable candle chart series | `@syncfusion/ej2-react-charts` |
| `WaterfallSeries` | Enable waterfall chart series | `@syncfusion/ej2-react-charts` |
| `HistogramSeries` | Enable histogram chart series | `@syncfusion/ej2-react-charts` |
| `BoxAndWhiskerSeries` | Enable box and whisker chart series | `@syncfusion/ej2-react-charts` |
| `ParetoSeries` | Enable Pareto chart series | `@syncfusion/ej2-react-charts` |
| `PolarSeries` | Enable polar chart series | `@syncfusion/ej2-react-charts` |
| `RadarSeries` | Enable radar chart series | `@syncfusion/ej2-react-charts` |
| `StackingLineSeries` | Enable stacked line and 100% stacked line chart series | `@syncfusion/ej2-react-charts` |
| `StackingColumnSeries` | Enable stacked column and 100% stacked column chart series | `@syncfusion/ej2-react-charts` |
| `StackingBarSeries` | Enable stacked bar and 100% stacked bar chart series | `@syncfusion/ej2-react-charts` |
| `StackingAreaSeries` | Enable stacked area and 100% stacked area chart series | `@syncfusion/ej2-react-charts` |
| `StackingStepAreaSeries` | Enable stacked step area and 100% stacked step area chart series | `@syncfusion/ej2-react-charts` |
| `MultiColoredLineSeries` | Enable multi-colored line chart series | `@syncfusion/ej2-react-charts` |
| `MultiColoredAreaSeries` | Enable multi-colored area chart series | `@syncfusion/ej2-react-charts` |

### Axis Modules

| Module | Purpose | Import package |
|--------|---------|----------------|
| `Category` | Enable category axis | `@syncfusion/ej2-react-charts` |
| `DateTime` | Enable date-time axis | `@syncfusion/ej2-react-charts` |
| `DateTimeCategory` | Enable date-time category axis | `@syncfusion/ej2-react-charts` |
| `Logarithmic` | Enable logarithmic axis | `@syncfusion/ej2-react-charts` |
| `MultiLevelLabel` | Enable multi-level axis labels | `@syncfusion/ej2-react-charts` |
| `StripLine` | Enable strip line support in chart axes | `@syncfusion/ej2-react-charts` |
| `ScrollBar` | Enable scrollbar support for chart axes | `@syncfusion/ej2-react-charts` |

### User Interaction Modules

| Module | Purpose | Import package |
|--------|---------|----------------|
| `Tooltip` | Enable tooltip and trackball support | `@syncfusion/ej2-react-charts` |
| `Crosshair` | Enable crosshair interaction | `@syncfusion/ej2-react-charts` |
| `Zoom` | Enable zooming and panning | `@syncfusion/ej2-react-charts` |
| `Selection` | Enable point or series selection | `@syncfusion/ej2-react-charts` |
| `Highlight` | Enable point or series highlighting | `@syncfusion/ej2-react-charts` |
| `DataEditing` | Enable interactive data editing by dragging chart points | `@syncfusion/ej2-react-charts` |

### Label and Annotation Modules

| Module | Purpose | Import package |
|--------|---------|----------------|
| `DataLabel` | Enable data labels for chart points | `@syncfusion/ej2-react-charts` |
| `LastValueLabel` | Enable last value labels for chart series | `@syncfusion/ej2-react-charts` |
| `ChartAnnotation` | Enable annotations in chart | `@syncfusion/ej2-react-charts` |

### Legend Module

| Module | Purpose | Import package |
|--------|---------|----------------|
| `Legend` | Enable chart legend | `@syncfusion/ej2-react-charts` |

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
| `Trendlines` | Enable trendline support | `@syncfusion/ej2-react-charts` |
| `ErrorBar` | Enable error bar support | `@syncfusion/ej2-react-charts` |

### Export Module

| Module | Purpose | Import package |
|--------|---------|----------------|
| `Export` | Enable chart export support | `@syncfusion/ej2-react-charts` |

### Example Full Chart Injection

```tsx
import {
  ChartComponent,
  SeriesCollectionDirective,
  SeriesDirective,
  Inject,
  LineSeries,
  ColumnSeries,
  BarSeries,
  AreaSeries,
  SplineSeries,
  SplineAreaSeries,
  StepLineSeries,
  StepAreaSeries,
  ScatterSeries,
  BubbleSeries,
  RangeColumnSeries,
  RangeAreaSeries,
  SplineRangeAreaSeries,
  HiloSeries,
  HiloOpenCloseSeries,
  CandleSeries,
  WaterfallSeries,
  HistogramSeries,
  BoxAndWhiskerSeries,
  ParetoSeries,
  PolarSeries,
  RadarSeries,
  StackingLineSeries,
  StackingColumnSeries,
  StackingBarSeries,
  StackingAreaSeries,
  StackingStepAreaSeries,
  MultiColoredLineSeries,
  MultiColoredAreaSeries,
  Category,
  DateTime,
  DateTimeCategory,
  Logarithmic,
  MultiLevelLabel,
  StripLine,
  ScrollBar,
  Tooltip,
  Crosshair,
  Zoom,
  Selection,
  Highlight,
  DataEditing,
  DataLabel,
  LastValueLabel,
  ChartAnnotation,
  Legend,
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
  ErrorBar,
  Export
} from '@syncfusion/ej2-react-charts';

<ChartComponent>
  <SeriesCollectionDirective>
    <SeriesDirective
      dataSource={data}
      xName="x"
      yName="y"
      type="Line"
      lastValueLabel={{
        enable: true
      }}
    />
  </SeriesCollectionDirective>

  <Inject
    services={[
      LineSeries,
      ColumnSeries,
      BarSeries,
      AreaSeries,
      SplineSeries,
      SplineAreaSeries,
      StepLineSeries,
      StepAreaSeries,
      ScatterSeries,
      BubbleSeries,
      RangeColumnSeries,
      RangeAreaSeries,
      SplineRangeAreaSeries,
      HiloSeries,
      HiloOpenCloseSeries,
      CandleSeries,
      WaterfallSeries,
      HistogramSeries,
      BoxAndWhiskerSeries,
      ParetoSeries,
      PolarSeries,
      RadarSeries,
      StackingLineSeries,
      StackingColumnSeries,
      StackingBarSeries,
      StackingAreaSeries,
      StackingStepAreaSeries,
      MultiColoredLineSeries,
      MultiColoredAreaSeries,
      Category,
      DateTime,
      DateTimeCategory,
      Logarithmic,
      MultiLevelLabel,
      StripLine,
      ScrollBar,
      Tooltip,
      Crosshair,
      Zoom,
      Selection,
      Highlight,
      DataEditing,
      DataLabel,
      LastValueLabel,
      ChartAnnotation,
      Legend,
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
      ErrorBar,
      Export
    ]}
  />
</ChartComponent>
```

## Interfaces

React Chart provides TypeScript interfaces to strongly type chart configuration, axis settings, series settings, labels, annotations, technical indicators, and event arguments.

### Chart Configuration Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `ChartModel` | Defines the complete configuration model for the Chart component | `@syncfusion/ej2-react-charts` |
| `ChartAreaModel` | Defines chart area customization options such as background and border | `@syncfusion/ej2-react-charts` |
| `MarginModel` | Defines margin settings for the chart | `@syncfusion/ej2-react-charts` |
| `BorderModel` | Defines border color, width, and dash array settings | `@syncfusion/ej2-react-charts` |
| `FontModel` | Defines font style, size, color, weight, and family settings | `@syncfusion/ej2-react-charts` |
| `AnimationModel` | Defines animation duration, delay, and enable settings | `@syncfusion/ej2-react-charts` |
| `ChartAccessibilityModel` | Defines accessibility settings for the chart | `@syncfusion/ej2-react-charts` |

### Axis Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `AxisModel` | Defines configuration for primary and secondary chart axes | `@syncfusion/ej2-react-charts` |
| `RowModel` | Defines row configuration for multi-row chart layout | `@syncfusion/ej2-react-charts` |
| `ColumnModel` | Defines column configuration for multi-column chart layout | `@syncfusion/ej2-react-charts` |
| `MajorGridLinesModel` | Defines major grid line settings for chart axes | `@syncfusion/ej2-react-charts` |
| `MinorGridLinesModel` | Defines minor grid line settings for chart axes | `@syncfusion/ej2-react-charts` |
| `MajorTickLinesModel` | Defines major tick line settings for chart axes | `@syncfusion/ej2-react-charts` |
| `MinorTickLinesModel` | Defines minor tick line settings for chart axes | `@syncfusion/ej2-react-charts` |
| `LineStyleModel` | Defines axis line style settings | `@syncfusion/ej2-react-charts` |
| `LabelBorderModel` | Defines border settings for axis labels | `@syncfusion/ej2-react-charts` |
| `StripLineSettingsModel` | Defines strip line settings for chart axes | `@syncfusion/ej2-react-charts` |
| `MultiLevelLabelsModel` | Defines multi-level axis label settings | `@syncfusion/ej2-react-charts` |
| `MultiLevelCategoriesModel` | Defines category range settings inside multi-level labels | `@syncfusion/ej2-react-charts` |

### Series Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `SeriesModel` | Defines chart series configuration | `@syncfusion/ej2-react-charts` |
| `MarkerSettingsModel` | Defines marker settings for chart series points | `@syncfusion/ej2-react-charts` |
| `DataLabelSettingsModel` | Defines data label settings for chart points | `@syncfusion/ej2-react-charts` |
| `LastValueLabelSettingsModel` | Defines last value label settings for chart series | `@syncfusion/ej2-react-charts` |
| `EmptyPointSettingsModel` | Defines empty point behavior and appearance for chart series | `@syncfusion/ej2-react-charts` |
| `CornerRadiusModel` | Defines corner radius settings for column-like series | `@syncfusion/ej2-react-charts` |
| `ConnectorModel` | Defines connector line settings for labels | `@syncfusion/ej2-react-charts` |
| `ParetoOptionsModel` | Defines Pareto chart-specific options | `@syncfusion/ej2-react-charts` |
| `DragSettingsModel` | Defines data editing drag settings for chart series | `@syncfusion/ej2-react-charts` |

### Tooltip and Crosshair Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `TooltipSettingsModel` | Defines chart tooltip settings | `@syncfusion/ej2-react-charts` |
| `TooltipLocationModel` | Defines tooltip location settings | `@syncfusion/ej2-react-charts` |
| `CrosshairSettingsModel` | Defines crosshair settings for chart interaction | `@syncfusion/ej2-react-charts` |
| `CrosshairTooltipModel` | Defines tooltip settings displayed with the crosshair | `@syncfusion/ej2-react-charts` |

### Legend Interface

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `LegendSettingsModel` | Defines chart legend settings | `@syncfusion/ej2-react-charts` |

### Zoom and Selection Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `ZoomSettingsModel` | Defines zooming and panning behavior for chart | `@syncfusion/ej2-react-charts` |
| `IndexesModel` | Defines series and point index information for selection and highlighting | `@syncfusion/ej2-react-charts` |

### Annotation Interface

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `ChartAnnotationSettingsModel` | Defines annotation settings for chart | `@syncfusion/ej2-react-charts` |

### Analysis Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `TrendlineModel` | Defines trendline settings for chart series | `@syncfusion/ej2-react-charts` |
| `TrendlineMarkerModel` | Defines marker settings for trendline points | `@syncfusion/ej2-react-charts` |
| `ErrorBarSettingsModel` | Defines error bar settings for chart series | `@syncfusion/ej2-react-charts` |

### Technical Indicator Interface

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `TechnicalIndicatorModel` | Defines technical indicator settings such as SMA, EMA, RSI, MACD, Bollinger Bands, Momentum, ATR, TMA, Stochastic, and Accumulation Distribution indicators | `@syncfusion/ej2-react-charts` |

### Lifecycle Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `ILoadEventArgs` | Defines event arguments for the chart load event | `@syncfusion/ej2-react-charts` |
| `ILoadedEventArgs` | Defines event arguments after chart rendering is completed | `@syncfusion/ej2-react-charts` |
| `IChartEventArgs` | Defines common chart event arguments | `@syncfusion/ej2-react-charts` |
| `IResizeEventArgs` | Defines event arguments for chart resize events | `@syncfusion/ej2-react-charts` |

### Series and Point Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `IPointRenderEventArgs` | Defines event arguments used while rendering each chart point | `@syncfusion/ej2-react-charts` |
| `ISeriesRenderEventArgs` | Defines event arguments used while rendering each chart series | `@syncfusion/ej2-react-charts` |
| `IPointEventArgs` | Defines event arguments for chart point mouse and interaction events | `@syncfusion/ej2-react-charts` |
| `ITextRenderEventArgs` | Defines event arguments used while rendering chart text such as data labels | `@syncfusion/ej2-react-charts` |

### Axis Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `IAxisLabelRenderEventArgs` | Defines event arguments used while rendering axis labels | `@syncfusion/ej2-react-charts` |
| `IAxisMultiLabelRenderEventArgs` | Defines event arguments used while rendering multi-level axis labels | `@syncfusion/ej2-react-charts` |
| `IAxisRangeCalculatedEventArgs` | Defines event arguments after axis range calculation | `@syncfusion/ej2-react-charts` |

### Tooltip Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `ITooltipRenderEventArgs` | Defines event arguments used while rendering chart tooltip | `@syncfusion/ej2-react-charts` |
| `ISharedTooltipRenderEventArgs` | Defines event arguments used while rendering shared tooltip content | `@syncfusion/ej2-react-charts` |
| `ITooltipRenderCompleteEventArgs` | Defines event arguments after tooltip rendering is completed | `@syncfusion/ej2-react-charts` |

### Legend Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `ILegendRenderEventArgs` | Defines event arguments used while rendering chart legend items | `@syncfusion/ej2-react-charts` |
| `ILegendClickEventArgs` | Defines event arguments for legend click events | `@syncfusion/ej2-react-charts` |

### Interaction Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `IMouseEventArgs` | Defines event arguments for chart mouse events | `@syncfusion/ej2-react-charts` |
| `ISelectionCompleteEventArgs` | Defines event arguments after point or series selection is completed | `@syncfusion/ej2-react-charts` |
| `IZoomCompleteEventArgs` | Defines event arguments after zooming is completed | `@syncfusion/ej2-react-charts` |
| `IScrollEventArgs` | Defines event arguments for chart scroll events | `@syncfusion/ej2-react-charts` |
| `IScrollChangedEventArgs` | Defines event arguments after chart scroll position changes | `@syncfusion/ej2-react-charts` |
| `IDragCompleteEventArgs` | Defines event arguments after chart point dragging is completed | `@syncfusion/ej2-react-charts` |

### Annotation Event Interface

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `IAnnotationRenderEventArgs` | Defines event arguments used while rendering chart annotations | `@syncfusion/ej2-react-charts` |

### Export and Print Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `IPrintEventArgs` | Defines event arguments for chart print events | `@syncfusion/ej2-react-charts` |
| `IExportEventArgs` | Defines event arguments for chart export events | `@syncfusion/ej2-react-charts` |

### Animation Event Interface

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `IAnimationCompleteEventArgs` | Defines event arguments after chart animation is completed | `@syncfusion/ej2-react-charts` |

### Example Importing Interfaces

```tsx
import {
  ChartModel,
  AxisModel,
  SeriesModel,
  TooltipSettingsModel,
  ILoadedEventArgs,
  IPointRenderEventArgs
} from '@syncfusion/ej2-react-charts';

const primaryXAxis: AxisModel = {
  valueType: 'Category'
};

const tooltip: TooltipSettingsModel = {
  enable: true
};

const series: SeriesModel = {
  dataSource: [
    { x: 'Jan', y: 35 },
    { x: 'Feb', y: 28 },
    { x: 'Mar', y: 34 }
  ],
  xName: 'x',
  yName: 'y',
  type: 'Line'
};

const chartOptions: ChartModel = {
  primaryXAxis,
  tooltip,
  series: [series]
};

const loaded = (args: ILoadedEventArgs): void => {
  // Chart rendering completed.
};

const pointRender = (args: IPointRenderEventArgs): void => {
  // Customize each point before rendering.
};
```

## Common Setup Issues

### Issue Chart Not Rendering

**Cause:** Missing CSS imports or undeclared modules.

**Solution:**

1. Verify CSS files are imported at the top of your component file or app entry file.
2. Check that all modules used in the chart are included in `<Inject services={[...]}>`.
3. Ensure each module is imported from `@syncfusion/ej2-react-charts`.

### Issue Data Not Displaying

**Cause:** Incorrect property mapping through `xName` or `yName`.

**Solution:**

1. Verify `xName` and `yName` match your data object property names exactly. These values are case-sensitive.
2. Confirm `dataSource` contains objects with these properties.
3. Check that `type` matches the series module imported and injected.

### Issue Labels Not Showing on Axes

**Cause:** Category axis not injected or `valueType` not set correctly.

**Solution:**

1. Ensure the `Category` module is injected for string-based axes.
2. For numeric data, use the default numeric axis behavior or configure the axis appropriately.
3. Verify data contains the mapped properties.

## Full Example Sales Chart with Multiple Features

```jsx
import React from 'react';
import {
  ChartComponent,
  SeriesCollectionDirective,
  SeriesDirective,
  Inject,
  LineSeries,
  Category,
  Legend,
  Tooltip,
  DataLabel
} from '@syncfusion/ej2-react-charts';

export default function SalesChart() {
  const data = [
    { month: 'Jan', revenue: 35, profit: 8 },
    { month: 'Feb', revenue: 28, profit: 6 },
    { month: 'Mar', revenue: 34, profit: 7 },
    { month: 'Apr', revenue: 32, profit: 7 },
    { month: 'May', revenue: 40, profit: 9 }
  ];

  return (
    <ChartComponent
      id="sales-chart"
      primaryXAxis={{
        valueType: 'Category',
        majorGridLines: { width: 0 }
      }}
      primaryYAxis={{
        labelFormat: '${value}K',
        edgeLabelPlacement: 'Shift'
      }}
      title="2024 Sales Performance"
      width="100%"
      height="420px"
      tooltip={{ enable: true, shared: true }}
      legendSettings={{ visible: true, position: 'Top' }}
    >
      <Inject services={[LineSeries, Category, Legend, Tooltip, DataLabel]} />
      <SeriesCollectionDirective>
        <SeriesDirective
          dataSource={data}
          xName="month"
          yName="revenue"
          name="Revenue"
          width={2}
          type="Line"
          marker={{
            visible: true,
            width: 7,
            height: 7,
            dataLabel: { visible: true, position: 'Top' }
          }}
        />
        <SeriesDirective
          dataSource={data}
          xName="month"
          yName="profit"
          name="Profit"
          width={2}
          type="Line"
          marker={{
            visible: true,
            width: 7,
            height: 7
          }}
        />
      </SeriesCollectionDirective>
    </ChartComponent>
  );
}
```

This example demonstrates:

- Multiple series for comparison
- Custom axis label formatting
- Legend and tooltip configuration
- Responsive width and fixed height
- Professional styling with proper spacing

## Additional Configuration Options

### Theme Selection

Choose from built-in themes to match your application design:

```jsx
<ChartComponent theme="Bootstrap5">
  {/* chart content */}
</ChartComponent>
```

**Available themes:**

- `Material`, `MaterialDark`
- `Fabric`, `FabricDark`
- `Bootstrap`, `BootstrapDark`, `Bootstrap4`, `Bootstrap5`, `Bootstrap5Dark`
- `Tailwind`, `TailwindDark`
- `Fluent`, `FluentDark`, `Fluent2`, `Fluent2Dark`, `Fluent2HighContrast`
- `Material3`, `Material3Dark`
- `HighContrast`, `HighContrastLight`

### Background and Borders

```jsx
<ChartComponent
  background="#f5f5f5"
  backgroundImage="/pattern.png"
  border={{
    color: '#e0e0e0',
    width: 2
  }}
  chartArea={{
    border: { color: '#cccccc', width: 1 },
    backgroundColor: '#ffffff'
  }}
>
  {/* chart content */}
</ChartComponent>
```

### Animation Control

```jsx
<ChartComponent enableAnimation={true}>
  {/* chart content */}
</ChartComponent>
```

### No Data Template

Display custom content when the chart has no data:

```jsx
<ChartComponent noDataTemplate='<div style="padding: 20px;">No data available to display</div>'>
  {/* chart content */}
</ChartComponent>
```

## Quick Reference

For complete API documentation and all available properties, see:

- **API Reference:** https://ej2.syncfusion.com/react/documentation/api/chart/overview
- **Official Documentation:** https://ej2.syncfusion.com/react/documentation/api/chart/
