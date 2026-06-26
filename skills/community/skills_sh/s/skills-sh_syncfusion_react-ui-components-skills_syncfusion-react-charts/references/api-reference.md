````markdown
# API Reference

## Table of Contents
- [ChartComponent Properties](#chartcomponent-properties)
- [ChartComponent Methods](#chartcomponent-methods)
- [ChartComponent Events](#chartcomponent-events)
- [SeriesDirective Properties](#seriesdirective-properties)
- [Common Model Interfaces](#common-model-interfaces)
- [Module Services](#module-services)

---

## ChartComponent Properties

Complete reference for `ChartComponent` properties based on the official Syncfusion EJ2 React Charts API.

### Core Configuration

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `id` | string | Required | Unique identifier for the chart instance |
| `width` | string | null | Chart width (e.g., '100%', '800px') |
| `height` | string | null | Chart height (e.g., '400px', '100%') |
| `title` | string | '' | Main title displayed at the top |
| `subTitle` | string | '' | Subtitle displayed below main title |
| `theme` | ChartTheme | 'Material' | Visual theme (Material, Fabric, Bootstrap, etc.) |
| `background` | string | null | Background color (hex, rgba, or named color) |
| `backgroundImage` | string | null | Background image URL |
| `locale` | string | '' | Localization/culture setting |

### Axes Configuration

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `primaryXAxis` | AxisModel | - | Primary horizontal axis configuration |
| `primaryYAxis` | AxisModel | - | Primary vertical axis configuration |
| `axes` | AxisModel[] | [] | Secondary axes collection |
| `rows` | RowModel[] | [] | Horizontal panes for splitting chart |
| `columns` | ColumnModel[] | [] | Vertical panes for splitting chart |

### Data and Series

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `dataSource` | Object/DataManager | '' | Global data source for all series |
| `series` | SeriesModel[] | [] | Collection of series to display |
| `palettes` | string[] | [] | Color palette for series |
| `rangeColorSettings` | RangeColorSettingModel[] | [] | Color rules based on value ranges |

### Styling

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `titleStyle` | TitleSettingsModel | - | Title font and color styling |
| `subTitleStyle` | TitleSettingsModel | - | Subtitle font and color styling |
| `border` | BorderModel | - | Chart border configuration |
| `chartArea` | ChartAreaModel | - | Chart area border and background |
| `margin` | MarginModel | - | Outer margins (left, right, top, bottom) |

### Interaction Features

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `selectionMode` | SelectionMode | 'None' | Selection behavior (Point, Series, Cluster, DragXY, DragX, DragY, Lasso, None) |
| `selectionPattern` | SelectionPattern | 'None' | Visual pattern for selected items |
| `highlightMode` | HighlightMode | 'None' | Highlighting behavior (None, Point, Series, Cluster) |
| `highlightPattern` | SelectionPattern | 'None' | Visual pattern for highlighted items |
| `highlightColor` | string | '' | Color for highlighted elements |
| `isMultiSelect` | boolean | false | Enable multi-point/series selection |
| `allowMultiSelection` | boolean | false | Enable multi-drag selection (requires DragX/Y mode) |
| `selectedDataIndexes` | IndexesModel[] | [] | Pre-selected point indexes on load |

### Zoom Configuration

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `zoomSettings` | ZoomSettingsModel | - | Zoom and pan configuration |
| `enableAutoIntervalOnBothAxis` | boolean | false | Auto-calculate intervals when zoomed |

### Legend

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `legendSettings` | LegendSettingsModel | - | Legend position, styling, and behavior |

### Tooltip and Crosshair

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `tooltip` | TooltipSettingsModel | - | Tooltip configuration |
| `crosshair` | CrosshairSettingsModel | - | Crosshair line configuration |

### Annotations

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `annotations` | ChartAnnotationSettingsModel[] | [] | Text, image, and shape annotations |

### Technical Indicators

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `indicators` | TechnicalIndicatorModel[] | [] | Technical indicators (MA, RSI, MACD, etc.) |

### Accessibility

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `accessibility` | AccessibilityModel | - | Accessibility options for screen readers |
| `description` | string | null | Chart description for screen readers |
| `tabIndex` | number | 1 | Tab order for keyboard navigation |
| `focusBorderColor` | string | null | Focus indicator border color |
| `focusBorderWidth` | number | 1.5 | Focus indicator border width |
| `focusBorderMargin` | number | 0 | Focus indicator margin |

### Display Options

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `enableAnimation` | boolean | true | Enable/disable series animations |
| `enableCanvas` | boolean | false | Use canvas rendering instead of SVG |
| `enableRtl` | boolean | false | Right-to-left rendering |
| `enableSideBySidePlacement` | boolean | true | Column series side-by-side placement |
| `isTransposed` | boolean | false | Transpose X and Y axes |
| `useGroupingSeparator` | boolean | false | Use thousand separators in numbers |
| `enableHtmlSanitizer` | boolean | false | Sanitize HTML in templates |

### Export and Print

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `allowExport` | boolean | false | Enable export feature (Blazor only) |
| `enableExport` | boolean | true | Enable chart export functionality |

### State Management

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `enablePersistence` | boolean | false | Persist chart state across page reloads |

### Stack Labels

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `stackLabels` | StackLabelSettingsModel | - | Stack label configuration for stacked series |

### No Data Template

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `noDataTemplate` | string/Function | null | Template to display when chart has no data |

---

## ChartComponent Methods

Methods available on the `ChartComponent` instance via refs.

### Chart Manipulation

```jsx
const chartRef = useRef(null);

// Access methods via chartRef.current
```

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `addSeries` | seriesCollection: SeriesModel[] | void | Add new series to the chart |
| `removeSeries` | index: number | void | Remove series by index |
| `addAxes` | axisCollection: AxisModel[] | void | Add secondary axes |
| `clearSeries` | - | void | Remove all series from chart |
| `refreshLiveData` | - | void | Refresh chart for live data updates |

### Display Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `showTooltip` | x: number/string/Date, y: number, isPoint?: boolean | void | Display tooltip at coordinates |
| `hideTooltip` | - | void | Hide active tooltip |
| `showCrosshair` | x: number, y: number | void | Display crosshair at coordinates |
| `hideCrosshair` | - | void | Hide active crosshair |

### Export and Print

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `export` | type: ExportType, fileName: string | void | Export chart (PNG, JPEG, PDF, SVG) |
| `print` | id?: string[]/string/Element | void | Print chart or specific elements |

### Annotations

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `setAnnotationValue` | annotationIndex: number, content: string | void | Update annotation content dynamically |

### Utility Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `getModuleName` | - | string | Get component name |
| `getLocalizedLabel` | key: string | string | Get localized label by key |
| `destroy` | - | void | Destroy chart instance |

---

## ChartComponent Events

Event handlers for chart interactions and lifecycle.

### Lifecycle Events

| Event | Type | Description |
|-------|------|-------------|
| `load` | EmitType<ILoadedEventArgs> | Before chart loads (customization opportunity) |
| `loaded` | EmitType<ILoadedEventArgs> | After chart fully loaded |
| `beforeResize` | EmitType<IBeforeResizeEventArgs> | Before chart resize |
| `resized` | EmitType<IResizeEventArgs> | After chart resized |

### Rendering Events

| Event | Type | Description |
|-------|------|-------------|
| `seriesRender` | EmitType<ISeriesRenderEventArgs> | Before series rendered |
| `pointRender` | EmitType<IPointRenderEventArgs> | Before each point rendered |
| `axisLabelRender` | EmitType<IAxisLabelRenderEventArgs> | Before axis label rendered |
| `axisMultiLabelRender` | EmitType<IAxisMultiLabelRenderEventArgs> | Before multi-label rendered |
| `axisRangeCalculated` | EmitType<IAxisRangeCalculatedEventArgs> | After axis range calculated |
| `annotationRender` | EmitType<IAnnotationRenderEventArgs> | Before annotation rendered |
| `legendRender` | EmitType<ILegendRenderEventArgs> | Before legend rendered |
| `textRender` | EmitType<ITextRenderEventArgs> | Before data label rendered |
| `tooltipRender` | EmitType<ITooltipRenderEventArgs> | Before tooltip rendered |
| `sharedTooltipRender` | EmitType<ISharedTooltipRenderEventArgs> | Before shared tooltip rendered |

### Animation Events

| Event | Type | Description |
|-------|------|-------------|
| `animationComplete` | EmitType<IAnimationCompleteEventArgs> | After series animation completed |

### Mouse Events

| Event | Type | Description |
|-------|------|-------------|
| `chartMouseClick` | EmitType<IMouseEventArgs> | On chart click |
| `chartDoubleClick` | EmitType<IMouseEventArgs> | On chart double-click |
| `chartMouseMove` | EmitType<IMouseEventArgs> | On mouse move over chart |
| `chartMouseDown` | EmitType<IMouseEventArgs> | On mouse down |
| `chartMouseUp` | EmitType<IMouseEventArgs> | On mouse up |
| `chartMouseLeave` | EmitType<IMouseEventArgs> | On mouse leave chart |

### Point Events

| Event | Type | Description |
|-------|------|-------------|
| `pointClick` | EmitType<IPointEventArgs> | On data point click |
| `pointDoubleClick` | EmitType<IPointEventArgs> | On data point double-click |
| `pointMove` | EmitType<IPointEventArgs> | On data point hover |

### Axis Events

| Event | Type | Description |
|-------|------|-------------|
| `axisLabelClick` | EmitType<IAxisLabelClickEventArgs> | On axis label click |
| `multiLevelLabelClick` | EmitType<IMultiLevelLabelClickEventArgs> | On multi-level label click |

### Legend Events

| Event | Type | Description |
|-------|------|-------------|
| `legendClick` | EmitType<ILegendClickEventArgs> | On legend item click |

### Selection Events

| Event | Type | Description |
|-------|------|-------------|
| `selectionComplete` | EmitType<ISelectionCompleteEventArgs> | After selection completed |

### Zoom Events

| Event | Type | Description |
|-------|------|-------------|
| `onZooming` | EmitType<IZoomingEventArgs> | On zoom started |
| `zoomComplete` | EmitType<IZoomCompleteEventArgs> | After zoom completed |

### Scroll Events

| Event | Type | Description |
|-------|------|-------------|
| `scrollStart` | EmitType<IScrollEventArgs> | On scroll start |
| `scrollChanged` | EmitType<IScrollEventArgs> | On scroll position change |
| `scrollEnd` | EmitType<IScrollEventArgs> | On scroll end |

### Drag Events (Data Editing)

| Event | Type | Description |
|-------|------|-------------|
| `dragStart` | EmitType<IDataEditingEventArgs> | On point drag start |
| `drag` | EmitType<IDataEditingEventArgs> | While point being dragged |
| `dragEnd` | EmitType<IDataEditingEventArgs> | On point drag end |
| `dragComplete` | EmitType<IDragCompleteEventArgs> | After drag selection completed |

### Export/Print Events

| Event | Type | Description |
|-------|------|-------------|
| `beforeExport` | EmitType<IExportEventArgs> | Before export starts |
| `afterExport` | EmitType<IAfterExportEventArgs> | After export completed |
| `beforePrint` | EmitType<IPrintEventArgs> | Before printing starts |

---

## SeriesDirective Properties

Properties for configuring individual chart series.

### Core Series Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `dataSource` | Object[] | - | Data array for this series |
| `xName` | string | - | Property name for X-axis values |
| `yName` | string | - | Property name for Y-axis values |
| `type` | ChartSeriesType | - | Series type (Line, Column, Bar, Area, etc.) |
| `name` | string | - | Series name (appears in legend) |
| `fill` | string | - | Series fill color |
| `opacity` | number | 1 | Series opacity (0-1) |
| `width` | number | 2 | Line width (for line series) |

### Axis Assignment

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `xAxisName` | string | - | Bind to specific X-axis by name |
| `yAxisName` | string | - | Bind to specific Y-axis by name |

### Financial Data Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `high` | string | - | Property name for high value (financial) |
| `low` | string | - | Property name for low value (financial) |
| `open` | string | - | Property name for open value (financial) |
| `close` | string | - | Property name for close value (financial) |

### Bubble/Range Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `size` | string | - | Property name for bubble size |

### Styling

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `border` | BorderModel | - | Series border configuration |
| `cornerRadius` | number | 0 | Corner radius for columns (0-50) |
| `columnSpacing` | number | 0 | Spacing between columns (0-1) |
| `dashArray` | string | - | Dash pattern for lines (e.g., '5,3') |

### Markers

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `marker` | MarkerSettingsModel | - | Data point marker configuration |

### Data Labels

Data labels are configured **inside the `marker` property** using `marker.dataLabel`. Inject the `DataLabel` service to enable this feature.

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `marker.dataLabel` | DataLabelSettingsModel | - | Data label configuration nested within the marker object |

### Trendlines

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `trendlines` | TrendlineModel[] | [] | Trendline overlays (MA, Linear, etc.) |

### Empty Points

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `emptyPointSettings` | EmptyPointSettingsModel | - | How to handle missing data points |

### Color Mapping

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `pointColorMapping` | string | - | Property name for per-point colors |

### Remote Data

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `dataSource` | Object[] \| DataManager | - | Local array or `DataManager` instance for remote data binding |
| `query` | Query | - | `Query` object to filter, sort, or paginate the DataManager data source |

---

## SeriesDirective Methods

Methods available directly on a series instance (accessed via `chartRef.current.series[index]`).

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `addPoint` | dataPoint: Object, duration?: number | void | Append a single data point to the series with optional animation duration (ms) |
| `removePoint` | index: number, duration?: number | void | Remove the data point at the specified index with optional animation duration (ms) |
| `setData` | data: Object[], duration?: number | void | Replace the entire series data source with optional animation duration (ms) |

### addPoint Example

```jsx
// Append a new point with 300ms animation
chartRef.current.series[0].addPoint({ month: 'Jun', value: 45 }, 300);
```

### removePoint Example

```jsx
// Remove the first point (index 0) with 300ms animation
chartRef.current.series[0].removePoint(0, 300);
```

### setData Example

```jsx
const newData = [{ month: 'Apr', value: 50 }, { month: 'May', value: 60 }];
// Replace all data with 500ms animation
chartRef.current.series[0].setData(newData, 500);
```

---

## Common Model Interfaces

Key model interfaces used in chart configuration.

### AxisModel

```typescript
interface AxisModel {
  valueType?: 'Category' | 'Numeric' | 'DateTime' | 'Logarithmic';
  title?: string;
  titleStyle?: FontModel;
  labelFormat?: string;
  labelRotation?: number;
  minimum?: number;
  maximum?: number;
  interval?: number;
  intervalType?: 'Auto' | 'Years' | 'Months' | 'Days' | 'Hours' | 'Minutes' | 'Seconds';
  majorGridLines?: { width?: number; color?: string; dashArray?: string };
  minorGridLines?: { width?: number; color?: string };
  majorTickLines?: { width?: number; size?: number; color?: string };
  minorTickLines?: { visible?: boolean; width?: number; size?: number };
  opposedPosition?: boolean;
  crossesAt?: number;
  labelIntersectAction?: 'None' | 'Hide' | 'Rotate45' | 'Rotate90' | 'Wrap' | 'MultipleRows';
  edgelabelPlacement?: 'None' | 'Hide' | 'Shift';
}
```

### ZoomSettingsModel

```typescript
interface ZoomSettingsModel {
  enableSelectionZoom?: boolean;
  enablePinchZooming?: boolean;
  enableMouseWheelZooming?: boolean;
  enableDeferredZoom?: boolean;
  mode?: 'X' | 'Y' | 'XY';
  toolbarItems?: ('ZoomIn' | 'ZoomOut' | 'Reset' | 'Pan')[];
}
```

### TooltipSettingsModel

```typescript
interface TooltipSettingsModel {
  enable?: boolean;
  shared?: boolean;
  enableMarker?: boolean;
  format?: string;
  template?: string | Function;
  fill?: string;
  border?: BorderModel;
  opacity?: number;
}
```

### LegendSettingsModel

```typescript
interface LegendSettingsModel {
  visible?: boolean;
  position?: 'Top' | 'Bottom' | 'Left' | 'Right' | 'Custom';
  alignment?: 'Near' | 'Center' | 'Far';
  toggleVisibility?: boolean;
  background?: string;
  border?: BorderModel;
  padding?: number;
  margin?: MarginModel;
}
```

### MarkerSettingsModel

```typescript
interface MarkerSettingsModel {
  visible?: boolean;
  shape?: 'Circle' | 'Square' | 'Diamond' | 'Triangle' | 'Pentagon' | 'Cross' | 'Plus';
  width?: number;
  height?: number;
  fill?: string;
  border?: BorderModel;
}
```

### CrosshairSettingsModel

```typescript
interface CrosshairSettingsModel {
  enable?: boolean;
  lineType?: 'Vertical' | 'Horizontal' | 'Both';
  line?: { width?: number; color?: string; dashArray?: string };
  lineStyle?: { width?: number; color?: string; dashArray?: string };
}
```

---

## Module Services

Services that must be injected via `<Inject services={[...]} />` to enable features.

### Chart Series Types

```jsx
import {
  LineSeries,
  ColumnSeries,
  BarSeries,
  AreaSeries,
  ScatterSeries,
  BubbleSeries,
  StepLineSeries,
  StepAreaSeries,
  SplineSeries,
  SplineAreaSeries,
  PolarSeries,
  RadarSeries,
  CandleSeries,
  HiloSeries,
  HiloOpenCloseSeries,
  RangeColumnSeries,
  RangeAreaSeries,
  RangeStepAreaSeries,
  SplineRangeAreaSeries,
  StackingColumnSeries,
  StackingBarSeries,
  StackingAreaSeries,
  StackingLineSeries,
  StackingStepAreaSeries,
  WaterfallSeries,
  BoxAndWhiskerSeries,
  HistogramSeries,
  ParetoSeries,
  MultiColoredLineSeries,
  MultiColoredAreaSeries
} from '@syncfusion/ej2-react-charts';
```

### Axis Types

```jsx
import {
  Category,
  DateTime,
  DateTimeCategory,
  Logarithmic
} from '@syncfusion/ej2-react-charts';
```

### Features

```jsx
import {
  Legend,
  Tooltip,
  Crosshair,
  Selection,
  Highlight,
  Zoom,
  DataLabel,
  Export,
  ChartAnnotation,
  ErrorBar,
  Trendlines,
  StripLine,
  MultiLevelLabel,
  ScrollBar,
  DataEditing
} from '@syncfusion/ej2-react-charts';
```

### Technical Indicators

```jsx
import {
  EmaIndicator,
  SmaIndicator,
  TmaIndicator,
  MacdIndicator,
  AtrIndicator,
  RsiIndicator,
  MomentumIndicator,
  StochasticIndicator,
  BollingerBands,
  AccumulationDistributionIndicator
} from '@syncfusion/ej2-react-charts';
```

---

## Usage Example with API References

```jsx
import React, { useRef } from 'react';
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
  Zoom,
  Selection,
  DataLabel
} from '@syncfusion/ej2-react-charts';

export default function APIExampleChart() {
  const chartRef = useRef(null);

  const data = [
    { month: 'Jan', sales: 35, profit: 8 },
    { month: 'Feb', sales: 28, profit: 6 },
    { month: 'Mar', sales: 34, profit: 7 }
  ];

  const handleExport = () => {
    chartRef.current?.export('PNG', 'my-chart');
  };

  return (
    <>
      <button onClick={handleExport}>Export Chart</button>
      <ChartComponent
        ref={chartRef}
        id='api-chart'
        width='100%'
        height='400px'
        title='Sales Performance'
        primaryXAxis={{
          valueType: 'Category',
          labelFormat: '{value}',
          majorGridLines: { width: 0 }
        }}
        primaryYAxis={{
          labelFormat: '${value}K',
          minimum: 0,
          maximum: 50,
          interval: 10
        }}
        tooltip={{
          enable: true,
          shared: true,
          format: '${series.name}: ${point.y}'
        }}
        legendSettings={{
          visible: true,
          position: 'Top'
        }}
        zoomSettings={{
          enableSelectionZoom: true,
          enableMouseWheelZooming: true,
          mode: 'XY'
        }}
        selectionMode='Point'
        highlightMode='Series'
        enableAnimation={true}
        palettes={['#3B82F6', '#10B981']}
        pointRender={(args) => {
          if (args.point.y > 30) {
            args.fill = '#4CAF50';
          }
        }}
        loaded={(args) => {
          console.log('Chart loaded successfully');
        }}
      >
        <Inject services={[
          LineSeries,
          ColumnSeries,
          Category,
          Legend,
          Tooltip,
          Zoom,
          Selection,
          DataLabel
        ]} />
        
        <SeriesCollectionDirective>
          <SeriesDirective
            dataSource={data}
            xName='month'
            yName='sales'
            name='Sales'
            type='Column'
            fill='#3B82F6'
            opacity={0.85}
            cornerRadius={{ topLeft: 4, topRight: 4 }}
            marker={{
              dataLabel: {
                visible: true,
                position: 'Top'
              }
            }}
          />
          <SeriesDirective
            dataSource={data}
            xName='month'
            yName='profit'
            name='Profit'
            type='Line'
            width={2}
            marker={{
              visible: true,
              shape: 'Circle',
              width: 8,
              height: 8,
              dataLabel: { visible: false }
            }}
          />
        </SeriesCollectionDirective>
      </ChartComponent>
    </>
  );
}
```

---

## Official API Documentation

For the most up-to-date and complete API reference, visit:
- **ChartComponent API:** https://ej2.syncfusion.com/react/documentation/api/chart/
- **SeriesModel API:** https://ej2.syncfusion.com/react/documentation/api/chart/seriesmodel
- **AxisModel API:** https://ej2.syncfusion.com/react/documentation/api/chart/axismodel

---

## Quick Reference Checklist

When using Syncfusion React Charts, ensure you:

✅ Import required modules (ChartComponent, SeriesDirective, etc.)  
✅ Inject necessary services (LineSeries, Category, Legend, etc.)  
✅ Set unique `id` on ChartComponent  
✅ Configure `primaryXAxis` and `primaryYAxis`  
✅ Map data with `dataSource`, `xName`, and `yName`  
✅ Specify series `type`  
✅ Add event handlers for interactions  
✅ Enable features via settings (tooltip, zoom, legend, etc.)  

````