# Getting Started with React Accumulation Charts

This guide covers the installation, setup, and basic implementation of Syncfusion React Accumulation Charts.

## Table of Contents

- [Installation](#installation)
- [Dependencies](#dependencies)
- [Project Setup](#project-setup)
  - [Using Vite Recommended](#using-vite-recommended)
  - [Using Create React App](#using-create-react-app)
- [Importing Components](#importing-components)
- [Basic AccumulationChartComponent Usage](#basic-accumulationchartcomponent-usage)
- [First Pie Chart with Data Binding](#first-pie-chart-with-data-binding)
- [AccumulationSeriesCollectionDirective Pattern](#accumulationseriescollectiondirective-pattern)
- [Data Structure Requirements](#data-structure-requirements)
- [Module Injection](#module-injection)
  - [Inject Modules](#inject-modules)
  - [Series Modules](#series-modules)
  - [Label and Legend Modules](#label-and-legend-modules)
  - [User Interaction Modules](#user-interaction-modules)
  - [Annotation Module](#annotation-module)
  - [Export Module](#export-module)
  - [Example Full Accumulation Chart Module Injection](#example-full-accumulation-chart-module-injection)
- [Interfaces](#interfaces)
  - [Accumulation Chart Configuration Interfaces](#accumulation-chart-configuration-interfaces)
  - [Accumulation Series Interfaces](#accumulation-series-interfaces)
  - [Pie and Doughnut Interfaces](#pie-and-doughnut-interfaces)
  - [Funnel and Pyramid Interfaces](#funnel-and-pyramid-interfaces)
  - [Legend Interface](#legend-interface)
  - [Tooltip Interface](#tooltip-interface)
  - [Annotation Interfaces](#annotation-interfaces)
  - [Selection and Highlight Interfaces](#selection-and-highlight-interfaces)
  - [Export and Print Interfaces](#export-and-print-interfaces)
  - [Accumulation Chart Lifecycle Event Interfaces](#accumulation-chart-lifecycle-event-interfaces)
  - [Accumulation Chart Series and Point Event Interfaces](#accumulation-chart-series-and-point-event-interfaces)
  - [Accumulation Chart Tooltip Event Interfaces](#accumulation-chart-tooltip-event-interfaces)
  - [Accumulation Chart Legend Event Interfaces](#accumulation-chart-legend-event-interfaces)
  - [Accumulation Chart Interaction Event Interfaces](#accumulation-chart-interaction-event-interfaces)
  - [Accumulation Chart Annotation Event Interfaces](#accumulation-chart-annotation-event-interfaces)
  - [Example Importing Interfaces](#example-importing-interfaces)
- [Complete Starter Template](#complete-starter-template)
- [TypeScript Support](#typescript-support)
- [Common Setup Issues](#common-setup-issues)
  - [Issue Chart Not Rendering](#issue-chart-not-rendering)
  - [Issue Module Not Found Error](#issue-module-not-found-error)
  - [Issue Types Not Found TypeScript](#issue-types-not-found-typescript)
- [Next Steps](#next-steps)

## Installation

Install the Syncfusion React Charts package via npm:

```bash
npm install @syncfusion/ej2-react-charts --save
```

This package includes all chart types, including accumulation charts such as Pie, Doughnut, Funnel, and Pyramid.

## Dependencies

The accumulation chart component depends on these Syncfusion packages, which are installed automatically:

```text
@syncfusion/ej2-react-charts
  ├── @syncfusion/ej2-data
  ├── @syncfusion/ej2-pdf-export
  ├── @syncfusion/ej2-file-utils
  ├── @syncfusion/ej2-compression
  ├── @syncfusion/ej2-react-popups
  ├── @syncfusion/ej2-react-buttons
  └── @syncfusion/ej2-react-base
```

## Project Setup

### Using Vite Recommended

Create a new React project with Vite:

```bash
npm create vite@latest my-chart-app -- --template react
cd my-chart-app
npm install
npm install @syncfusion/ej2-react-charts --save
```

### Using Create React App

```bash
npx create-react-app my-chart-app
cd my-chart-app
npm install @syncfusion/ej2-react-charts --save
```

## Importing Components

Import the required components and modules:

```tsx
import {
  AccumulationChartComponent,
  AccumulationSeriesCollectionDirective,
  AccumulationSeriesDirective,
  Inject,
  PieSeries
} from '@syncfusion/ej2-react-charts';
```

## Basic AccumulationChartComponent Usage

The `AccumulationChartComponent` is the root container for all accumulation charts:

```tsx
import React from 'react';
import { AccumulationChartComponent } from '@syncfusion/ej2-react-charts';

function App() {
  return (
    <AccumulationChartComponent id="chart">
      {/* Series configuration goes here */}
    </AccumulationChartComponent>
  );
}

export default App;
```

## First Pie Chart with Data Binding

Here is a complete example creating a basic pie chart:

```tsx
import React from 'react';
import {
  AccumulationChartComponent,
  AccumulationSeriesCollectionDirective,
  AccumulationSeriesDirective,
  Inject,
  PieSeries
} from '@syncfusion/ej2-react-charts';

function App() {
  const data = [
    { month: 'Jan', sales: 35 },
    { month: 'Feb', sales: 28 },
    { month: 'Mar', sales: 34 },
    { month: 'Apr', sales: 32 },
    { month: 'May', sales: 40 }
  ];

  return (
    <AccumulationChartComponent
      id="pie-chart"
      title="Monthly Sales Distribution"
    >
      <Inject services={[PieSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName="month"
          yName="sales"
          radius="90%"
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}

export default App;
```

## AccumulationSeriesCollectionDirective Pattern

The series configuration uses a directive pattern:

```tsx
<AccumulationSeriesCollectionDirective>
  <AccumulationSeriesDirective
    dataSource={yourData}
    xName="categoryField"
    yName="valueField"
    type="Pie"
  />
</AccumulationSeriesCollectionDirective>
```

**Key Points:**

- `dataSource`: Array of data objects.
- `xName`: Property name for category or label field.
- `yName`: Property name for numeric value field.
- Each series represents one accumulation chart.

## Data Structure Requirements

Your data should be an array of objects with at least two properties:

```tsx
const data = [
  { category: 'Product A', value: 45 },
  { category: 'Product B', value: 30 },
  { category: 'Product C', value: 25 }
];

<AccumulationSeriesDirective
  dataSource={data}
  xName="category"
  yName="value"
/>
```

## Module Injection

React Accumulation Chart features are modular and require module injection to enable them. This reduces bundle size by loading only the required accumulation chart series types, labels, legends, annotations, tooltip, selection, highlight, and export features.

Accumulation Chart supports Pie, Doughnut, Funnel, and Pyramid chart types. Doughnut chart is rendered by using `PieSeries` with the `innerRadius` property.

### Inject Modules

```tsx
import * as React from 'react';
import {
  AccumulationChartComponent,
  AccumulationSeriesCollectionDirective,
  AccumulationSeriesDirective,
  Inject,
  PieSeries,
  FunnelSeries,
  PyramidSeries,
  AccumulationLegend,
  AccumulationDataLabel,
  AccumulationTooltip,
  AccumulationSelection,
  AccumulationHighlight,
  AccumulationAnnotation,
  Export
} from '@syncfusion/ej2-react-charts';

function App() {
  const data: Object[] = [
    { x: 'Chrome', y: 61.3, text: 'Chrome: 61.3%' },
    { x: 'Safari', y: 24.6, text: 'Safari: 24.6%' },
    { x: 'Edge', y: 5.0, text: 'Edge: 5.0%' },
    { x: 'Firefox', y: 2.7, text: 'Firefox: 2.7%' }
  ];

  return (
    <AccumulationChartComponent
      id="accumulation-chart"
      title="Browser Market Share"
      legendSettings={{ visible: true }}
      tooltip={{ enable: true }}
    >
      <Inject
        services={[
          PieSeries,
          FunnelSeries,
          PyramidSeries,
          AccumulationLegend,
          AccumulationDataLabel,
          AccumulationTooltip,
          AccumulationSelection,
          AccumulationHighlight,
          AccumulationAnnotation,
          Export
        ]}
      />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName="x"
          yName="y"
          type="Pie"
          dataLabel={{
            visible: true,
            name: 'text',
            position: 'Outside'
          }}
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}

export default App;
```

### Series Modules

| Module | Purpose | Import package |
|--------|---------|----------------|
| `PieSeries` | Enable pie and doughnut accumulation chart series | `@syncfusion/ej2-react-charts` |
| `FunnelSeries` | Enable funnel accumulation chart series | `@syncfusion/ej2-react-charts` |
| `PyramidSeries` | Enable pyramid accumulation chart series | `@syncfusion/ej2-react-charts` |

### Label and Legend Modules

| Module | Purpose | Import package |
|--------|---------|----------------|
| `AccumulationDataLabel` | Enable data labels for accumulation chart points | `@syncfusion/ej2-react-charts` |
| `AccumulationLegend` | Enable legend support in accumulation chart | `@syncfusion/ej2-react-charts` |

### User Interaction Modules

| Module | Purpose | Import package |
|--------|---------|----------------|
| `AccumulationTooltip` | Enable tooltip support in accumulation chart | `@syncfusion/ej2-react-charts` |
| `AccumulationSelection` | Enable point selection in accumulation chart | `@syncfusion/ej2-react-charts` |
| `AccumulationHighlight` | Enable point highlighting in accumulation chart | `@syncfusion/ej2-react-charts` |

### Annotation Module

| Module | Purpose | Import package |
|--------|---------|----------------|
| `AccumulationAnnotation` | Enable annotations in accumulation chart | `@syncfusion/ej2-react-charts` |

### Export Module

| Module | Purpose | Import package |
|--------|---------|----------------|
| `Export` | Enable accumulation chart export and print support | `@syncfusion/ej2-react-charts` |

### Example Full Accumulation Chart Module Injection

```tsx
import * as React from 'react';
import {
  AccumulationChartComponent,
  AccumulationSeriesCollectionDirective,
  AccumulationSeriesDirective,
  Inject,
  PieSeries,
  FunnelSeries,
  PyramidSeries,
  AccumulationLegend,
  AccumulationDataLabel,
  AccumulationTooltip,
  AccumulationSelection,
  AccumulationHighlight,
  AccumulationAnnotation,
  Export
} from '@syncfusion/ej2-react-charts';

function App() {
  const data: Object[] = [
    { x: 'Food', y: 35, text: 'Food: 35%' },
    { x: 'Transport', y: 25, text: 'Transport: 25%' },
    { x: 'Rent', y: 20, text: 'Rent: 20%' },
    { x: 'Utilities', y: 12, text: 'Utilities: 12%' },
    { x: 'Others', y: 8, text: 'Others: 8%' }
  ];

  return (
    <AccumulationChartComponent
      id="accumulation-chart"
      title="Expense Breakdown"
      legendSettings={{ visible: true }}
      tooltip={{ enable: true }}
      enableSmartLabels={true}
      enableAnimation={true}
    >
      <Inject
        services={[
          PieSeries,
          FunnelSeries,
          PyramidSeries,
          AccumulationLegend,
          AccumulationDataLabel,
          AccumulationTooltip,
          AccumulationSelection,
          AccumulationHighlight,
          AccumulationAnnotation,
          Export
        ]}
      />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName="x"
          yName="y"
          type="Pie"
          innerRadius="40%"
          explode={true}
          explodeIndex={0}
          dataLabel={{
            visible: true,
            name: 'text',
            position: 'Outside'
          }}
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}

export default App;
```

## Interfaces

React Accumulation Chart provides TypeScript interfaces to strongly type accumulation chart configuration, series settings, data labels, annotations, legends, tooltips, center labels, borders, margins, accessibility settings, and event arguments.

### Accumulation Chart Configuration Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `AccumulationChartModel` | Defines the complete configuration model for the Accumulation Chart component | `@syncfusion/ej2-react-charts` |
| `ChartAreaModel` | Defines chart area customization options such as background and border | `@syncfusion/ej2-react-charts` |
| `BorderModel` | Defines border color, width, and dash array settings | `@syncfusion/ej2-react-charts` |
| `MarginModel` | Defines margin settings for the accumulation chart | `@syncfusion/ej2-react-charts` |
| `FontModel` | Defines font style, size, color, weight, opacity, and family settings | `@syncfusion/ej2-react-charts` |
| `TitleStyleSettingsModel` | Defines title text style settings | `@syncfusion/ej2-react-charts` |
| `TitleBorderModel` | Defines title border customization settings | `@syncfusion/ej2-react-charts` |
| `TitleSettingsModel` | Defines title configuration settings | `@syncfusion/ej2-react-charts` |
| `AccessibilityModel` | Defines accessibility settings for accumulation chart elements | `@syncfusion/ej2-react-charts` |

### Accumulation Series Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `AccumulationSeriesModel` | Defines accumulation chart series configuration | `@syncfusion/ej2-react-charts` |
| `AccumulationDataLabelSettingsModel` | Defines data label settings for accumulation chart points | `@syncfusion/ej2-react-charts` |
| `EmptyPointSettingsModel` | Defines empty point behavior and appearance for accumulation chart series | `@syncfusion/ej2-react-charts` |
| `ConnectorModel` | Defines connector line settings for accumulation chart data labels | `@syncfusion/ej2-react-charts` |
| `AnimationModel` | Defines animation duration, delay, and enable settings | `@syncfusion/ej2-react-charts` |
| `SeriesAccessibilityModel` | Defines accessibility settings for accumulation chart series | `@syncfusion/ej2-react-charts` |
| `IndexesModel` | Defines point index information used for selection or highlighting | `@syncfusion/ej2-react-charts` |

### Pie and Doughnut Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `PieCenterModel` | Defines center position settings for pie and doughnut charts | `@syncfusion/ej2-react-charts` |
| `CenterLabelModel` | Defines center label settings for doughnut chart | `@syncfusion/ej2-react-charts` |
| `LocationModel` | Defines x and y location settings | `@syncfusion/ej2-react-charts` |

### Funnel and Pyramid Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `AccumulationSeriesModel` | Defines funnel and pyramid series settings such as neck width, neck height, gap ratio, and mode | `@syncfusion/ej2-react-charts` |
| `BorderModel` | Defines border settings for funnel and pyramid segments | `@syncfusion/ej2-react-charts` |

### Legend Interface

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `LegendSettingsModel` | Defines legend settings for accumulation chart | `@syncfusion/ej2-react-charts` |

### Tooltip Interface

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `TooltipSettingsModel` | Defines tooltip settings for accumulation chart | `@syncfusion/ej2-react-charts` |
| `LocationModel` | Defines tooltip location settings | `@syncfusion/ej2-react-charts` |
| `BorderModel` | Defines tooltip border settings | `@syncfusion/ej2-react-charts` |
| `FontModel` | Defines tooltip text style settings | `@syncfusion/ej2-react-charts` |

### Annotation Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `AccumulationAnnotationSettingsModel` | Defines annotation settings for accumulation chart | `@syncfusion/ej2-react-charts` |
| `LocationModel` | Defines annotation location settings | `@syncfusion/ej2-react-charts` |

### Selection and Highlight Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `IndexesModel` | Defines selected or highlighted point index information | `@syncfusion/ej2-react-charts` |
| `BorderModel` | Defines border settings applied during selection or highlight customization | `@syncfusion/ej2-react-charts` |

### Export and Print Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `IExportEventArgs` | Defines event arguments for accumulation chart export events | `@syncfusion/ej2-react-charts` |
| `IAfterExportEventArgs` | Defines event arguments after export is completed | `@syncfusion/ej2-react-charts` |
| `IPrintEventArgs` | Defines event arguments for accumulation chart print events | `@syncfusion/ej2-react-charts` |
| `IPDFArgs` | Defines PDF export event arguments | `@syncfusion/ej2-react-charts` |

### Accumulation Chart Lifecycle Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `IAccLoadedEventArgs` | Defines event arguments for accumulation chart load and loaded events | `@syncfusion/ej2-react-charts` |
| `IAccBeforeResizeEventArgs` | Defines event arguments before accumulation chart resize | `@syncfusion/ej2-react-charts` |
| `IAccResizeEventArgs` | Defines event arguments after accumulation chart resize | `@syncfusion/ej2-react-charts` |
| `IAccAnimationCompleteEventArgs` | Defines event arguments after accumulation chart animation is completed | `@syncfusion/ej2-react-charts` |

### Accumulation Chart Series and Point Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `IAccSeriesRenderEventArgs` | Defines event arguments used while rendering accumulation chart series | `@syncfusion/ej2-react-charts` |
| `IAccPointRenderEventArgs` | Defines event arguments used while rendering each accumulation chart point | `@syncfusion/ej2-react-charts` |
| `IPointEventArgs` | Defines event arguments for accumulation chart point click and point move events | `@syncfusion/ej2-react-charts` |
| `IAccTextRenderEventArgs` | Defines event arguments used while rendering accumulation chart data labels | `@syncfusion/ej2-react-charts` |

### Accumulation Chart Tooltip Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `IAccTooltipRenderEventArgs` | Defines event arguments used while rendering accumulation chart tooltip | `@syncfusion/ej2-react-charts` |

### Accumulation Chart Legend Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `IAccLegendRenderEventArgs` | Defines event arguments used while rendering accumulation chart legend items | `@syncfusion/ej2-react-charts` |
| `IAccLegendClickEventArgs` | Defines event arguments for accumulation chart legend click events | `@syncfusion/ej2-react-charts` |
| `ILegendRenderEventArgs` | Defines shared legend render event arguments | `@syncfusion/ej2-react-charts` |

### Accumulation Chart Interaction Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `IMouseEventArgs` | Defines event arguments for accumulation chart mouse events | `@syncfusion/ej2-react-charts` |
| `IAccSelectionCompleteEventArgs` | Defines event arguments after accumulation chart selection is completed | `@syncfusion/ej2-react-charts` |

### Accumulation Chart Annotation Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `IAnnotationRenderEventArgs` | Defines event arguments used while rendering accumulation chart annotations | `@syncfusion/ej2-react-charts` |

### Example Importing Interfaces

```tsx
import {
  AccumulationChartModel,
  AccumulationSeriesModel,
  AccumulationDataLabelSettingsModel,
  AccumulationAnnotationSettingsModel,
  PieCenterModel,
  CenterLabelModel,
  LegendSettingsModel,
  TooltipSettingsModel,
  BorderModel,
  FontModel,
  MarginModel,
  ChartAreaModel,
  AnimationModel,
  EmptyPointSettingsModel,
  ConnectorModel,
  IndexesModel,
  AccessibilityModel,
  IAccLoadedEventArgs,
  IAccBeforeResizeEventArgs,
  IAccResizeEventArgs,
  IAccAnimationCompleteEventArgs,
  IAccSeriesRenderEventArgs,
  IAccPointRenderEventArgs,
  IPointEventArgs,
  IAccTextRenderEventArgs,
  IAccTooltipRenderEventArgs,
  IAccLegendRenderEventArgs,
  IAccLegendClickEventArgs,
  IAccSelectionCompleteEventArgs,
  IAnnotationRenderEventArgs,
  IMouseEventArgs,
  IExportEventArgs,
  IAfterExportEventArgs,
  IPrintEventArgs
} from '@syncfusion/ej2-react-charts';

const border: BorderModel = {
  color: '#ffffff',
  width: 1
};

const titleStyle: FontModel = {
  size: '16px',
  fontWeight: '600'
};

const margin: MarginModel = {
  left: 10,
  right: 10,
  top: 10,
  bottom: 10
};

const chartArea: ChartAreaModel = {
  border: {
    width: 0
  }
};

const animation: AnimationModel = {
  enable: true,
  duration: 1000
};

const emptyPointSettings: EmptyPointSettingsModel = {
  mode: 'Drop'
};

const connector: ConnectorModel = {
  type: 'Curve',
  length: '20px'
};

const dataLabel: AccumulationDataLabelSettingsModel = {
  visible: true,
  name: 'text',
  position: 'Outside',
  connectorStyle: connector
};

const pieCenter: PieCenterModel = {
  x: '50%',
  y: '50%'
};

const centerLabel: CenterLabelModel = {
  text: 'Total'
};

const legendSettings: LegendSettingsModel = {
  visible: true,
  position: 'Bottom'
};

const tooltip: TooltipSettingsModel = {
  enable: true,
  format: '${point.x}: ${point.y}%'
};

const selectionIndex: IndexesModel = {
  point: 0,
  series: 0
};

const accessibility: AccessibilityModel = {
  accessibilityDescription: 'Browser market share accumulation chart',
  accessibilityRole: 'img'
};

const annotation: AccumulationAnnotationSettingsModel = {
  content: '<div>Annotation</div>',
  region: 'Chart',
  x: '50%',
  y: '50%'
};

const series: AccumulationSeriesModel = {
  dataSource: [
    { x: 'Chrome', y: 61.3, text: 'Chrome: 61.3%' },
    { x: 'Safari', y: 24.6, text: 'Safari: 24.6%' },
    { x: 'Edge', y: 5.0, text: 'Edge: 5.0%' },
    { x: 'Firefox', y: 2.7, text: 'Firefox: 2.7%' }
  ],
  xName: 'x',
  yName: 'y',
  type: 'Pie',
  innerRadius: '40%',
  explode: true,
  explodeIndex: 0,
  border,
  animation,
  emptyPointSettings,
  dataLabel
};

const accumulationChartOptions: AccumulationChartModel = {
  title: 'Browser Market Share',
  titleStyle,
  margin,
  chartArea,
  center: pieCenter,
  centerLabel,
  legendSettings,
  tooltip,
  annotations: [annotation],
  selectedDataIndexes: [selectionIndex],
  accessibility,
  series: [series]
};

const load = (args: IAccLoadedEventArgs): void => {
  // Accumulation Chart loading.
};

const loaded = (args: IAccLoadedEventArgs): void => {
  // Accumulation Chart loaded.
};

const beforeResize = (args: IAccBeforeResizeEventArgs): void => {
  // Before Accumulation Chart resize.
};

const resized = (args: IAccResizeEventArgs): void => {
  // Accumulation Chart resized.
};

const animationComplete = (args: IAccAnimationCompleteEventArgs): void => {
  // Accumulation Chart animation completed.
};

const seriesRender = (args: IAccSeriesRenderEventArgs): void => {
  // Accumulation Chart series rendering.
};

const pointRender = (args: IAccPointRenderEventArgs): void => {
  // Accumulation Chart point rendering.
};

const pointClick = (args: IPointEventArgs): void => {
  // Accumulation Chart point clicked.
};

const textRender = (args: IAccTextRenderEventArgs): void => {
  // Accumulation Chart data label rendering.
};

const tooltipRender = (args: IAccTooltipRenderEventArgs): void => {
  // Accumulation Chart tooltip rendering.
};

const legendRender = (args: IAccLegendRenderEventArgs): void => {
  // Accumulation Chart legend rendering.
};

const legendClick = (args: IAccLegendClickEventArgs): void => {
  // Accumulation Chart legend clicked.
};

const selectionComplete = (args: IAccSelectionCompleteEventArgs): void => {
  // Accumulation Chart selection completed.
};

const annotationRender = (args: IAnnotationRenderEventArgs): void => {
  // Accumulation Chart annotation rendering.
};

const chartMouseMove = (args: IMouseEventArgs): void => {
  // Accumulation Chart mouse move.
};

const beforeExport = (args: IExportEventArgs): void => {
  // Before Accumulation Chart export.
};

const afterExport = (args: IAfterExportEventArgs): void => {
  // After Accumulation Chart export.
};

const beforePrint = (args: IPrintEventArgs): void => {
  // Before Accumulation Chart print.
};
```

## Complete Starter Template

```tsx
import React from 'react';
import {
  AccumulationChartComponent,
  AccumulationSeriesCollectionDirective,
  AccumulationSeriesDirective,
  Inject,
  AccumulationLegend,
  AccumulationDataLabel,
  AccumulationTooltip,
  PieSeries
} from '@syncfusion/ej2-react-charts';

function App() {
  const data = [
    { x: 'Chrome', y: 61.3, text: 'Chrome: 61.3%' },
    { x: 'Safari', y: 24.6, text: 'Safari: 24.6%' },
    { x: 'Edge', y: 5.0, text: 'Edge: 5.0%' },
    { x: 'Firefox', y: 4.8, text: 'Firefox: 4.8%' },
    { x: 'Others', y: 4.3, text: 'Others: 4.3%' }
  ];

  return (
    <div style={{ padding: '20px' }}>
      <AccumulationChartComponent
        id="browser-chart"
        title="Browser Market Share 2024"
        legendSettings={{ visible: true }}
        tooltip={{ enable: true }}
      >
        <Inject services={[
          PieSeries,
          AccumulationLegend,
          AccumulationDataLabel,
          AccumulationTooltip
        ]} />
        <AccumulationSeriesCollectionDirective>
          <AccumulationSeriesDirective
            dataSource={data}
            xName="x"
            yName="y"
            radius="80%"
            dataLabel={{
              visible: true,
              name: 'text',
              position: 'Outside'
            }}
          />
        </AccumulationSeriesCollectionDirective>
      </AccumulationChartComponent>
    </div>
  );
}

export default App;
```

## TypeScript Support

For TypeScript projects, add type definitions through interfaces:

```tsx
import React from 'react';
import {
  AccumulationChartComponent,
  AccumulationSeriesCollectionDirective,
  AccumulationSeriesDirective,
  Inject,
  PieSeries
} from '@syncfusion/ej2-react-charts';

interface ChartData {
  category: string;
  value: number;
}

function App(): JSX.Element {
  const data: ChartData[] = [
    { category: 'A', value: 25 },
    { category: 'B', value: 35 },
    { category: 'C', value: 40 }
  ];

  return (
    <AccumulationChartComponent id="chart">
      <Inject services={[PieSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName="category"
          yName="value"
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}

export default App;
```

## Common Setup Issues

### Issue Chart Not Rendering

Ensure that you have:

1. Imported the required CSS theme.
2. Injected the required modules.
3. Provided valid data with `xName` and `yName` fields.
4. Set a container height if the parent has no height.

### Issue Module Not Found Error

Install the package:

```bash
npm install @syncfusion/ej2-react-charts
```

### Issue Types Not Found TypeScript

Types are included in the package. Ensure that import paths point to `@syncfusion/ej2-react-charts`.

## Next Steps

Now that you have a basic chart running, you can:

- Customize chart types such as Pie, Doughnut, Funnel, and Pyramid.
- Add data labels for better readability.
- Enable legends for categorical information.
- Add tooltips for interactive data exploration.
- Customize colors and styling.
- Handle user interactions with events.
