````markdown
# API Reference

## Table of Contents
- [AccumulationChartComponent Properties](#accumulationchartcomponent-properties)
- [AccumulationChartComponent Methods](#accumulationchartcomponent-methods)
- [AccumulationChartComponent Events](#accumulationchartcomponent-events)
- [AccumulationSeriesDirective Properties](#accumulationserisdirective-properties)
- [Common Model Interfaces](#common-model-interfaces)
- [Module Services](#module-services)

---

## AccumulationChartComponent Properties

Complete reference for `AccumulationChartComponent` properties based on the official Syncfusion EJ2 React Accumulation Charts API.

### Core Configuration

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `id` | string | Required | Unique identifier for the accumulation chart instance |
| `width` | string | null | Chart width (e.g., '100%', '800px') |
| `height` | string | null | Chart height (e.g., '400px', '100%') |
| `title` | string | null | Main title displayed at the top |
| `subTitle` | string | null | Subtitle displayed below main title |
| `theme` | AccumulationTheme | 'Material' | Visual theme (Material, Fabric, Bootstrap, Tailwind, Fluent, etc.) |
| `background` | string | null | Background color (hex, rgba, or named color) |
| `backgroundImage` | string | null | Background image URL |
| `locale` | string | '' | Localization/culture setting (e.g., 'en-US', 'fr-FR') |

### Data and Series

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `dataSource` | Object[] \| DataManager | '' | Global data source for all series |
| `series` | AccumulationSeriesModel[] | [] | Collection of accumulation series to display |

### Styling

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `titleStyle` | TitleStyleSettingsModel | - | Title font, size, weight, and color styling |
| `subTitleStyle` | TitleStyleSettingsModel | - | Subtitle font, size, weight, and color styling |
| `border` | BorderModel | - | Chart border configuration (width, color) |
| `margin` | MarginModel | - | Outer margins (left, right, top, bottom) |
| `center` | PieCenterModel | {x: '50%', y: '50%'} | Center position of pie/doughnut chart |

### Color Configuration

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `palettes` | string[] | [] | Color palette for series slices |

### Interaction Features

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `selectionMode` | AccumulationSelectionMode | 'None' | Selection behavior ('None', 'Point') |
| `selectionPattern` | SelectionPattern | 'None' | Visual pattern for selected items (Chessboard, Dots, DiagonalForward, etc.) |
| `highlightMode` | AccumulationHighlightMode | 'None' | Highlighting behavior ('None', 'Point') |
| `highlightPattern` | SelectionPattern | 'None' | Visual pattern for highlighted items |
| `highlightColor` | string | '' | Color for highlighted elements |
| `isMultiSelect` | boolean | false | Enable multi-point selection |
| `selectedDataIndexes` | IndexesModel[] | [] | Pre-selected point indexes on load |
| `enableBorderOnMouseMove` | boolean | true | Show border when mouse moves over slice |

### Smart Labels

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `enableSmartLabels` | boolean | true | Intelligently arrange labels to prevent overlapping |

### Legend

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `legendSettings` | LegendSettingsModel | - | Legend position, styling, and behavior |

### Tooltip

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `tooltip` | TooltipSettingsModel | - | Tooltip configuration |

### Annotations

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `annotations` | AccumulationAnnotationSettingsModel[] | [] | Text, image, and shape annotations |

### Center Label

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `centerLabel` | CenterLabelModel | - | Label configuration for center of doughnut chart |

### Accessibility

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `accessibility` | AccessibilityModel | - | Accessibility options for screen readers |
| `tabIndex` | number | 1 | Tab order for keyboard navigation |
| `focusBorderColor` | string | null | Focus indicator border color |
| `focusBorderWidth` | number | 1.5 | Focus indicator border width (pixels) |
| `focusBorderMargin` | number | 0 | Focus indicator margin (pixels) |

### Display Options

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `enableAnimation` | boolean | true | Enable/disable series animations |
| `enableRtl` | boolean | false | Right-to-left rendering |
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

### No Data Template

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `noDataTemplate` | string \| Function | null | Template to display when chart has no data |

### Module References (Read-Only)

These properties reference injected modules and are set automatically when services are injected.

| Property | Type | Description |
|----------|------|-------------|
| `accumulationDataLabelModule` | AccumulationDataLabel | Module for data labels |
| `accumulationHighlightModule` | AccumulationHighlight | Module for highlighting |
| `accumulationLegendModule` | AccumulationLegend | Module for legend |
| `accumulationSelectionModule` | AccumulationSelection | Module for selection |
| `accumulationTooltipModule` | AccumulationTooltip | Module for tooltip |
| `annotationModule` | AccumulationAnnotation | Module for annotations |
| `exportModule` | Export | Module for export |

---

## AccumulationChartComponent Methods

Methods available on the `AccumulationChartComponent` instance via refs.

### Chart Manipulation

```jsx
const chartRef = useRef(null);

// Access methods via chartRef.current
```

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `calculateBounds` | - | void | Calculate and update chart bounds |

### Display Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `showTooltip` | Not available | - | Use tooltip settings instead |
| `hideTooltip` | Not available | - | Use tooltip settings instead |

### Export and Print

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `export` | type: ExportType, fileName: string | void | Export chart (PNG, JPEG, PDF, SVG) |
| `print` | id?: string[] \| string \| Element | void | Print chart or specific elements |

### Annotations

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `setAnnotationValue` | annotationIndex: number, content: string | void | Update annotation content dynamically |

### Utility Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `getModuleName` | - | string | Get component name ('accumulationchart') |
| `destroy` | - | void | Destroy chart instance and free resources |

---

## AccumulationChartComponent Events

Event handlers for accumulation chart interactions and lifecycle.

### Lifecycle Events

| Event | Type | Description |
|-------|------|-------------|
| `load` | EmitType<IAccLoadedEventArgs> | Before chart loads (customization opportunity) |
| `loaded` | EmitType<IAccLoadedEventArgs> | After chart fully loaded |
| `beforeResize` | EmitType<IAccBeforeResizeEventArgs> | Before chart resize |
| `resized` | EmitType<IAccResizeEventArgs> | After chart resized |

### Rendering Events

| Event | Type | Description |
|-------|------|-------------|
| `seriesRender` | EmitType<IAccSeriesRenderEventArgs> | Before series rendered (customize series properties) |
| `pointRender` | EmitType<IAccPointRenderEventArgs> | Before each point rendered (customize individual slices) |
| `legendRender` | EmitType<ILegendRenderEventArgs> | Before legend rendered |
| `textRender` | EmitType<IAccTextRenderEventArgs> | Before data label rendered |
| `tooltipRender` | EmitType<ITooltipRenderEventArgs> | Before tooltip rendered |
| `annotationRender` | EmitType<IAnnotationRenderEventArgs> | Before annotation rendered |

### Animation Events

| Event | Type | Description |
|-------|------|-------------|
| `animationComplete` | EmitType<IAccAnimationCompleteEventArgs> | After series animation completed |

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
| `pointClick` | EmitType<IPointEventArgs> | On data point (slice) click |
| `pointMove` | EmitType<IPointEventArgs> | On data point (slice) hover |

### Legend Events

| Event | Type | Description |
|-------|------|-------------|
| `legendClick` | EmitType<IAccLegendClickEventArgs> | On legend item click |

### Selection Events

| Event | Type | Description |
|-------|------|-------------|
| `selectionComplete` | EmitType<IAccSelectionCompleteEventArgs> | After selection completed |

### Export/Print Events

| Event | Type | Description |
|-------|------|-------------|
| `beforeExport` | EmitType<IExportEventArgs> | Before export starts (customize filename, cancel export) |
| `afterExport` | EmitType<IAfterExportEventArgs> | After export completed |
| `beforePrint` | EmitType<IPrintEventArgs> | Before printing starts |

---

## AccumulationSeriesDirective Properties

Properties for configuring individual accumulation series (Pie, Doughnut, Funnel, Pyramid).

### Core Series Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `dataSource` | Object[] \| DataManager | - | Data array for this series |
| `xName` | string | - | Property name for category/label values |
| `yName` | string | - | Property name for numeric values |
| `type` | AccumulationSeriesType | 'Pie' | Series type ('Pie', 'Funnel', 'Pyramid') |
| `name` | string | - | Series name (appears in legend) |
| `opacity` | number | 1 | Series opacity (0-1) |

### Query for Remote Data

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `query` | Query | - | Query object for DataManager to filter/sort data |

### Pie and Doughnut Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `radius` | string | '80%' | Outer radius of pie/doughnut (percentage or pixels) |
| `innerRadius` | string | '0%' | Inner radius for doughnut hole (0% = pie, >0% = doughnut) |
| `startAngle` | number | 0 | Starting angle in degrees (0-360) |
| `endAngle` | number | 360 | Ending angle in degrees (0-360) |

### Funnel and Pyramid Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `width` | string | '80%' | Funnel/pyramid width relative to chart |
| `height` | string | '80%' | Funnel/pyramid height relative to chart |
| `neckWidth` | string | '20%' | Neck width for funnel chart |
| `neckHeight` | string | '20%' | Neck height for funnel chart |
| `gapRatio` | number | 0 | Gap between segments (0-1) |
| `pyramidMode` | PyramidMode | 'Linear' | Pyramid rendering mode ('Linear', 'Surface') |
| `funnelMode` | FunnelMode | 'Standard' | Funnel rendering mode ('Standard', 'Trapezoidal') |

### Explode Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `explode` | boolean | false | Enable click-to-explode or initial explode |
| `explodeAll` | boolean | false | Explode all slices initially |
| `explodeIndex` | number | - | Index of slice to explode by default |
| `explodeOffset` | string | '30%' | Distance to separate exploded slice |

### Styling

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `pointColorMapping` | string | - | Property name for per-point colors |
| `border` | BorderModel | - | Series border configuration (width, color) |
| `borderRadius` | number | 0 | Corner radius for rounded slices (0-50 pixels) |
| `applyPattern` | boolean | false | Apply pattern fills for printing/accessibility |

### Data Labels

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `dataLabel` | AccumulationDataLabelSettingsModel | - | Data label configuration |

### Grouping

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `groupTo` | string | - | Value threshold or point count for grouping |
| `groupMode` | GroupModes | 'Value' | Grouping mode ('Value', 'Point') |

### Empty Points

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `emptyPointSettings` | EmptyPointSettingsModel | - | How to handle missing data points |

### Animation

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `animation` | AnimationModel | - | Animation settings (enable, duration, delay) |

### Legend Mapping

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `legendShape` | LegendShape | - | Shape for legend items ('Circle', 'Rectangle', 'Triangle', etc.) |
| `legendImageUrl` | string | - | Image URL for legend items |

### Tooltips

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `tooltipMappingName` | string | - | Property name for custom tooltip text |

### Visibility

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `visible` | boolean | true | Show or hide the series |

---

## Common Model Interfaces

Key model interfaces used in accumulation chart configuration.

### LegendSettingsModel

```typescript
interface LegendSettingsModel {
  visible?: boolean;
  position?: 'Top' | 'Bottom' | 'Left' | 'Right' | 'Auto';
  alignment?: 'Near' | 'Center' | 'Far';
  toggleVisibility?: boolean;
  background?: string;
  border?: BorderModel;
  padding?: number;
  margin?: MarginModel;
  height?: string;
  width?: string;
  textStyle?: FontModel;
  shapeHeight?: number;
  shapeWidth?: number;
  shapePadding?: number;
  enablePages?: boolean;
  textWrap?: 'Normal' | 'Wrap' | 'AnyWhere';
  maximumLabelWidth?: number;
  title?: string;
  titleStyle?: FontModel;
  template?: string | Function;
}
```

### TooltipSettingsModel

```typescript
interface TooltipSettingsModel {
  enable?: boolean;
  enableMarker?: boolean;
  format?: string;
  template?: string | Function;
  fill?: string;
  border?: BorderModel;
  opacity?: number;
  header?: string;
  textStyle?: FontModel;
  location?: { x: number; y: number };
  enableAnimation?: boolean;
  duration?: number;
  fadeOutDuration?: number;
}
```

### AccumulationDataLabelSettingsModel

```typescript
interface AccumulationDataLabelSettingsModel {
  visible?: boolean;
  position?: 'Inside' | 'Outside';
  name?: string; // Property name for label text
  format?: string;
  font?: FontModel;
  fill?: string;
  border?: BorderModel;
  angle?: number;
  enableRotation?: boolean;
  maxWidth?: number;
  textWrap?: 'Normal' | 'Wrap' | 'AnyWhere';
  connectorStyle?: ConnectorModel;
  template?: string | Function;
}
```

### ConnectorModel

```typescript
interface ConnectorModel {
  type?: 'Line' | 'Curve';
  length?: string;
  width?: number;
  color?: string;
  dashArray?: string;
}
```

### BorderModel

```typescript
interface BorderModel {
  width?: number;
  color?: string;
  dashArray?: string;
}
```

### MarginModel

```typescript
interface MarginModel {
  left?: number;
  right?: number;
  top?: number;
  bottom?: number;
}
```

### PieCenterModel

```typescript
interface PieCenterModel {
  x?: string;
  y?: string;
}
```

### CenterLabelModel

```typescript
interface CenterLabelModel {
  text?: string;
  textStyle?: FontModel;
  hoverTextFormat?: string;
}
```

### AccumulationAnnotationSettingsModel

```typescript
interface AccumulationAnnotationSettingsModel {
  content?: string | Function;
  x?: string | number;
  y?: string | number;
  coordinateUnits?: 'Pixel' | 'Point';
  region?: 'Chart' | 'Series';
  description?: string;
}
```

### EmptyPointSettingsModel

```typescript
interface EmptyPointSettingsModel {
  mode?: 'Zero' | 'Drop' | 'Average' | 'Gap';
  fill?: string;
  border?: BorderModel;
}
```

### FontModel

```typescript
interface FontModel {
  size?: string;
  fontFamily?: string;
  fontWeight?: string;
  fontStyle?: string;
  color?: string;
  textAlignment?: 'Near' | 'Center' | 'Far';
  textOverflow?: 'None' | 'Trim' | 'Wrap';
}
```

### IndexesModel

```typescript
interface IndexesModel {
  series: number;
  point: number;
}
```

### AnimationModel

```typescript
interface AnimationModel {
  enable?: boolean;
  duration?: number;
  delay?: number;
}
```

### AccessibilityModel

```typescript
interface AccessibilityModel {
  accessibilityDescription?: string;
  accessibilityRole?: string;
}
```

---

## Module Services

Services that must be injected via `<Inject services={[...]} />` to enable features.

### Accumulation Chart Types

```jsx
import {
  PieSeries,
  FunnelSeries,
  PyramidSeries
} from '@syncfusion/ej2-react-charts';
```

**Note:** `PieSeries` is used for both Pie and Doughnut charts (doughnut is created by setting `innerRadius` > 0%).

### Features

```jsx
import {
  AccumulationLegend,
  AccumulationTooltip,
  AccumulationDataLabel,
  AccumulationSelection,
  AccumulationHighlight,
  AccumulationAnnotation,
  Export
} from '@syncfusion/ej2-react-charts';
```

### Module Descriptions

| Module | Purpose | When to Inject |
|--------|---------|----------------|
| `PieSeries` | Enable Pie and Doughnut charts | Always (for pie/doughnut) |
| `FunnelSeries` | Enable Funnel charts | When using type='Funnel' |
| `PyramidSeries` | Enable Pyramid charts | When using type='Pyramid' |
| `AccumulationLegend` | Display legend | When legendSettings.visible = true |
| `AccumulationTooltip` | Display tooltips | When tooltip.enable = true |
| `AccumulationDataLabel` | Display data labels | When dataLabel.visible = true |
| `AccumulationSelection` | Enable point selection | When selectionMode = 'Point' |
| `AccumulationHighlight` | Enable point highlighting | When highlightMode = 'Point' |
| `AccumulationAnnotation` | Add custom annotations | When using annotations |
| `Export` | Export and print functionality | When using export/print methods |

---

## Usage Example with API References

### Basic Pie Chart with All Features

```jsx
import React, { useRef, useState } from 'react';
import {
  AccumulationChartComponent,
  AccumulationSeriesCollectionDirective,
  AccumulationSeriesDirective,
  AccumulationAnnotationsDirective,
  AccumulationAnnotationDirective,
  Inject,
  PieSeries,
  AccumulationLegend,
  AccumulationTooltip,
  AccumulationDataLabel,
  AccumulationSelection,
  AccumulationHighlight,
  AccumulationAnnotation,
  Export
} from '@syncfusion/ej2-react-charts';

export default function APIExampleAccumulationChart() {
  const chartRef = useRef(null);
  const [selectedPoint, setSelectedPoint] = useState(null);

  const data = [
    { browser: 'Chrome', share: 61.3, fill: '#4285F4' },
    { browser: 'Safari', share: 24.6, fill: '#0088FF' },
    { browser: 'Firefox', share: 14.1, fill: '#FF6600' },
    { browser: 'Edge', share: 5.0, fill: '#0078D4' },
    { browser: 'Others', share: 5.0, fill: '#999999' }
  ];

  const handleExport = (type) => {
    chartRef.current?.export(type, `browser-chart-${Date.now()}`);
  };

  const handlePrint = () => {
    chartRef.current?.print();
  };

  const onPointClick = (args) => {
    setSelectedPoint(`${args.point.x}: ${args.point.y}%`);
  };

  const onLoad = (args) => {
    console.log('Accumulation Chart loaded');
  };

  const onPointRender = (args) => {
    // Customize points dynamically
    if (args.point.y > 50) {
      args.border = { width: 3, color: '#28a745' };
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <div style={{ marginBottom: '15px' }}>
        <button onClick={() => handleExport('PNG')}>Export PNG</button>
        <button onClick={() => handleExport('PDF')}>Export PDF</button>
        <button onClick={handlePrint}>Print</button>
        {selectedPoint && (
          <span style={{ marginLeft: '15px', fontWeight: 'bold' }}>
            Selected: {selectedPoint}
          </span>
        )}
      </div>

      <AccumulationChartComponent
        ref={chartRef}
        id='api-accumulation-chart'
        width='100%'
        height='450px'
        title='Browser Market Share 2024'
        subTitle='Desktop and Mobile Combined'
        theme='Material'
        background='#ffffff'
        enableSmartLabels={true}
        enableAnimation={true}
        enableBorderOnMouseMove={true}
        selectionMode='Point'
        highlightMode='Point'
        highlightColor='#ff4081'
        selectionPattern='DiagonalForward'
        isMultiSelect={false}
        selectedDataIndexes={[{ series: 0, point: 0 }]}
        center={{ x: '50%', y: '50%' }}
        enableExport={true}
        useGroupingSeparator={true}
        margin={{ left: 20, right: 20, top: 50, bottom: 20 }}
        border={{ width: 0 }}
        titleStyle={{
          fontFamily: 'Segoe UI',
          size: '20px',
          fontWeight: '600',
          color: '#333'
        }}
        subTitleStyle={{
          fontFamily: 'Segoe UI',
          size: '14px',
          color: '#666'
        }}
        legendSettings={{
          visible: true,
          position: 'Right',
          alignment: 'Center',
          toggleVisibility: true,
          background: '#f9f9f9',
          border: { width: 1, color: '#e0e0e0' },
          padding: 10,
          textStyle: {
            size: '12px',
            fontFamily: 'Segoe UI'
          }
        }}
        tooltip={{
          enable: true,
          format: '${point.x}: <b>${point.y}%</b>',
          header: 'Market Share',
          border: { width: 1, color: '#0078d4' }
        }}
        load={onLoad}
        pointClick={onPointClick}
        pointRender={onPointRender}
        loaded={(args) => {
          console.log('Chart rendering completed');
        }}
        beforeExport={(args) => {
          console.log('Exporting as', args.type);
        }}
        afterExport={(args) => {
          console.log('Export completed');
        }}
      >
        <Inject services={[
          PieSeries,
          AccumulationLegend,
          AccumulationTooltip,
          AccumulationDataLabel,
          AccumulationSelection,
          AccumulationHighlight,
          AccumulationAnnotation,
          Export
        ]} />
        
        <AccumulationSeriesCollectionDirective>
          <AccumulationSeriesDirective
            dataSource={data}
            xName='browser'
            yName='share'
            type='Pie'
            radius='90%'
            innerRadius='0%'
            startAngle={0}
            endAngle={360}
            explode={false}
            explodeOffset='10%'
            explodeIndex={0}
            pointColorMapping='fill'
            border={{ width: 2, color: '#ffffff' }}
            borderRadius={4}
            opacity={0.95}
            dataLabel={{
              visible: true,
              position: 'Outside',
              name: 'browser',
              format: '{point.x}: {point.y}%',
              font: {
                size: '11px',
                fontFamily: 'Segoe UI',
                fontWeight: '500'
              },
              connectorStyle: {
                type: 'Curve',
                length: '40px',
                width: 2,
                color: '#0078d4'
              }
            }}
            animation={{
              enable: true,
              duration: 1000,
              delay: 0
            }}
          />
        </AccumulationSeriesCollectionDirective>

        <AccumulationAnnotationsDirective>
          <AccumulationAnnotationDirective
            content='<div style="font-size:14px;font-weight:bold;color:#666;">100M Users</div>'
            region='Series'
            x='50%'
            y='50%'
          />
        </AccumulationAnnotationsDirective>
      </AccumulationChartComponent>
    </div>
  );
}
```

### Doughnut Chart Example

```jsx
function DoughnutChartExample() {
  const data = [
    { category: 'Mobile', value: 55 },
    { category: 'Desktop', value: 30 },
    { category: 'Tablet', value: 15 }
  ];

  return (
    <AccumulationChartComponent
      id='doughnut-chart'
      title='Device Distribution'
      legendSettings={{ visible: true, position: 'Bottom' }}
      tooltip={{ enable: true }}
      enableSmartLabels={true}
    >
      <Inject services={[
        PieSeries,
        AccumulationLegend,
        AccumulationTooltip,
        AccumulationDataLabel
      ]} />
      
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='category'
          yName='value'
          type='Pie'
          radius='90%'
          innerRadius='50%'  // Doughnut hole
          dataLabel={{
            visible: true,
            position: 'Inside',
            font: { color: 'white', fontWeight: 'bold' }
          }}
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

### Funnel Chart Example

```jsx
import { FunnelSeries } from '@syncfusion/ej2-react-charts';

function FunnelChartExample() {
  const salesData = [
    { stage: 'Website Visits', count: 10000 },
    { stage: 'Sign Ups', count: 5000 },
    { stage: 'Active Users', count: 3000 },
    { stage: 'Premium Users', count: 1500 },
    { stage: 'Retained', count: 1200 }
  ];

  return (
    <AccumulationChartComponent
      id='funnel-chart'
      title='Sales Conversion Funnel'
      legendSettings={{ visible: false }}
      tooltip={{ enable: true }}
    >
      <Inject services={[
        FunnelSeries,
        AccumulationTooltip,
        AccumulationDataLabel
      ]} />
      
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={salesData}
          xName='stage'
          yName='count'
          type='Funnel'
          width='60%'
          height='80%'
          neckWidth='25%'
          neckHeight='5%'
          gapRatio={0.08}
          dataLabel={{
            visible: true,
            position: 'Outside',
            connectorStyle: { length: '30px' }
          }}
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

### Pyramid Chart Example

```jsx
import { PyramidSeries } from '@syncfusion/ej2-react-charts';

function PyramidChartExample() {
  const data = [
    { level: 'Executive', count: 10 },
    { level: 'Management', count: 50 },
    { level: 'Supervisors', count: 200 },
    { level: 'Employees', count: 1000 }
  ];

  return (
    <AccumulationChartComponent
      id='pyramid-chart'
      title='Organizational Hierarchy'
      legendSettings={{ visible: true }}
      tooltip={{ enable: true }}
    >
      <Inject services={[
        PyramidSeries,
        AccumulationLegend,
        AccumulationTooltip,
        AccumulationDataLabel
      ]} />
      
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='level'
          yName='count'
          type='Pyramid'
          width='70%'
          height='85%'
          pyramidMode='Linear'
          gapRatio={0.05}
          dataLabel={{
            visible: true,
            position: 'Inside',
            font: { color: 'white', size: '12px' }
          }}
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

---

## Event Arguments Interfaces

### IAccLoadedEventArgs

```typescript
interface IAccLoadedEventArgs {
  cancel: boolean;
  name: string;
  accumulation: AccumulationChart;
}
```

### IAccPointRenderEventArgs

```typescript
interface IAccPointRenderEventArgs {
  cancel: boolean;
  name: string;
  series: AccumulationSeries;
  point: AccumulationPoints;
  fill: string;
  border: BorderModel;
  data: Object;
}
```

### IAccSeriesRenderEventArgs

```typescript
interface IAccSeriesRenderEventArgs {
  cancel: boolean;
  name: string;
  series: AccumulationSeries;
  data: Object;
}
```

### IAccTextRenderEventArgs

```typescript
interface IAccTextRenderEventArgs {
  cancel: boolean;
  name: string;
  series: AccumulationSeries;
  point: AccumulationPoints;
  text: string | string[];
  border: BorderModel;
  color: string;
  template: string | Function;
  font: FontModel;
}
```

### IPointEventArgs

```typescript
interface IPointEventArgs {
  cancel: boolean;
  name: string;
  series: AccumulationSeries;
  point: AccumulationPoints;
  seriesIndex: number;
  pointIndex: number;
  x: number;
  y: number;
}
```

### IAccLegendClickEventArgs

```typescript
interface IAccLegendClickEventArgs {
  cancel: boolean;
  name: string;
  legendText: string;
  legendShape: LegendShape;
  series: AccumulationSeries;
  point: AccumulationPoints;
  seriesIndex: number;
  pointIndex: number;
}
```

---

## Official API Documentation

For the most up-to-date and complete API reference, visit:
- **AccumulationChartComponent API:** https://ej2.syncfusion.com/react/documentation/api/accumulation-chart/
- **AccumulationSeriesModel API:** https://ej2.syncfusion.com/react/documentation/api/accumulation-chart/accumulationseriesmodel
- **Complete Index:** https://ej2.syncfusion.com/react/documentation/api/accumulation-chart/index-default

---

## Quick Reference Checklist

When using Syncfusion React Accumulation Charts, ensure you:

✅ Import required modules (AccumulationChartComponent, AccumulationSeriesDirective, etc.)  
✅ Inject necessary services (PieSeries, AccumulationLegend, AccumulationTooltip, etc.)  
✅ Set unique `id` on AccumulationChartComponent  
✅ Map data with `dataSource`, `xName`, and `yName`  
✅ Specify series `type` ('Pie', 'Funnel', or 'Pyramid')  
✅ Configure `radius` and `innerRadius` for pie/doughnut  
✅ Enable features via settings (tooltip, legend, dataLabel, etc.)  
✅ Add event handlers for interactions (pointClick, pointRender, etc.)  
✅ Use `enableSmartLabels={true}` for charts with many slices  
✅ Inject `Export` module if using export/print functionality  

---

## Selection Patterns Reference

Available patterns for `selectionPattern` and `highlightPattern`:

- `None` - No pattern
- `Chessboard` - Chessboard pattern
- `Dots` - Dot pattern
- `DiagonalForward` - Forward diagonal lines
- `DiagonalBackward` - Backward diagonal lines
- `Crosshatch` - Crosshatch pattern
- `Pacman` - Pacman pattern
- `Grid` - Grid pattern
- `Turquoise` - Turquoise pattern
- `Star` - Star pattern
- `Triangle` - Triangle pattern
- `Circle` - Circle pattern
- `Tile` - Tile pattern
- `HorizontalDash` - Horizontal dashes
- `VerticalDash` - Vertical dashes
- `Rectangle` - Rectangle pattern
- `Box` - Box pattern
- `VerticalStripe` - Vertical stripes
- `HorizontalStripe` - Horizontal stripes
- `Bubble` - Bubble pattern

---

## Themes Reference

Available themes for `theme` property:

- `Material` - Google Material Design
- `Material3` - Material Design 3
- `MaterialDark` - Material Dark
- `Material3Dark` - Material 3 Dark
- `Fabric` - Microsoft Fabric
- `FabricDark` - Microsoft Fabric Dark
- `Bootstrap` - Bootstrap 3
- `BootstrapDark` - Bootstrap 3 Dark
- `Bootstrap4` - Bootstrap 4
- `Bootstrap5` - Bootstrap 5
- `Bootstrap5Dark` - Bootstrap 5 Dark
- `Tailwind` - Tailwind CSS
- `TailwindDark` - Tailwind CSS Dark
- `Tailwind3` - Tailwind CSS 3
- `Tailwind3Dark` - Tailwind CSS 3 Dark
- `Fluent` - Microsoft Fluent
- `FluentDark` - Microsoft Fluent Dark
- `Fluent2` - Microsoft Fluent 2
- `Fluent2Dark` - Microsoft Fluent 2 Dark
- `Fluent2HighContrast` - Fluent 2 High Contrast
- `HighContrast` - High Contrast
- `HighContrastLight` - High Contrast Light

---

## Export Types Reference

Available export types for `export()` method:

- `'PNG'` - Portable Network Graphics (recommended for web)
- `'JPEG'` - JPEG format (smaller file size)
- `'SVG'` - Scalable Vector Graphics (perfect quality at any size)
- `'PDF'` - Portable Document Format (for reports and printing)

---

## Common Gotchas and Tips

### 1. Doughnut vs Pie
```jsx
// Pie chart
<AccumulationSeriesDirective innerRadius='0%' />

// Doughnut chart
<AccumulationSeriesDirective innerRadius='40%' />
```

### 2. Data Label Position
```jsx
// Inside labels (good for large slices)
dataLabel={{ visible: true, position: 'Inside' }}

// Outside labels (better for many small slices)
dataLabel={{ visible: true, position: 'Outside' }}
```

### 3. Smart Labels
```jsx
// Always enable for charts with 8+ slices
<AccumulationChartComponent enableSmartLabels={true}>
```

### 4. Grouping Small Values
```jsx
// Group values below 5
<AccumulationSeriesDirective
  groupTo='5'
  groupMode='Value'
/>

// Group to show only top 4 items
<AccumulationSeriesDirective
  groupTo='4'
  groupMode='Point'
/>
```

### 5. Export Requires Module
```jsx
// Don't forget to inject Export module
<Inject services={[PieSeries, Export]} />
```

### 6. TypeScript Typing
```jsx
import { AccumulationChartComponent } from '@syncfusion/ej2-react-charts';

const chartRef = useRef<AccumulationChartComponent>(null);
```

---

This comprehensive API reference should cover all your Accumulation Chart needs! 🎉

````