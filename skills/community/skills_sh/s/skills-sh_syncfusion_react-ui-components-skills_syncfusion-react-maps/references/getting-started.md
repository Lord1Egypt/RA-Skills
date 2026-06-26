# Getting Started with Syncfusion React Maps

The Syncfusion React Maps component visualizes geographical data using SVG rendering. This guide covers installation, setup, GeoJSON usage, data binding, module injection, and a complete first map implementation.

## Table of Contents

- [Overview](#overview)
- [Dependencies](#dependencies)
- [Installation](#installation)
  - [Using npm](#using-npm)
  - [Using Vite Recommended](#using-vite-recommended)
  - [Using Create React App](#using-create-react-app)
- [Basic Setup](#basic-setup)
  - [Project Structure](#project-structure)
  - [Importing Components](#importing-components)
- [Understanding GeoJSON Data](#understanding-geojson-data)
  - [Getting GeoJSON Data](#getting-geojson-data)
- [Creating Your First Map](#creating-your-first-map)
  - [Minimal Example](#minimal-example)
- [Data Binding](#data-binding)
  - [Data Source Structure](#data-source-structure)
  - [Remote Data Binding DataManager](#remote-data-binding-datamanager)
  - [Binding Data to Shapes](#binding-data-to-shapes)
  - [Example with Color Mapping](#example-with-color-mapping)
- [Module Injection](#module-injection)
  - [Inject Modules](#inject-modules)
  - [Layer Modules](#layer-modules)
  - [Marker and Bubble Modules](#marker-and-bubble-modules)
  - [Navigation Line Module](#navigation-line-module)
  - [User Interaction Modules](#user-interaction-modules)
  - [Annotation Module](#annotation-module)
  - [Print and Export Modules](#print-and-export-modules)
  - [Example Full Maps Module Injection](#example-full-maps-module-injection)
- [Interfaces](#interfaces)
  - [Maps Configuration Interfaces](#maps-configuration-interfaces)
  - [Layer Interfaces](#layer-interfaces)
  - [Data Label Interfaces](#data-label-interfaces)
  - [Marker Interfaces](#marker-interfaces)
  - [Bubble Interfaces](#bubble-interfaces)
  - [Navigation Line Interfaces](#navigation-line-interfaces)
  - [Tooltip Interfaces](#tooltip-interfaces)
  - [Legend Interfaces](#legend-interfaces)
  - [Selection and Highlight Interfaces](#selection-and-highlight-interfaces)
  - [Zoom Interfaces](#zoom-interfaces)
  - [Annotation Interfaces](#annotation-interfaces)
  - [Tile Map and Ajax Interfaces](#tile-map-and-ajax-interfaces)
  - [Maps Lifecycle Event Interfaces](#maps-lifecycle-event-interfaces)
  - [Maps Shape Event Interfaces](#maps-shape-event-interfaces)
  - [Maps Marker Event Interfaces](#maps-marker-event-interfaces)
  - [Maps Bubble Event Interfaces](#maps-bubble-event-interfaces)
  - [Maps Navigation Line Event Interfaces](#maps-navigation-line-event-interfaces)
  - [Maps Tooltip and Legend Event Interfaces](#maps-tooltip-and-legend-event-interfaces)
  - [Maps Annotation Event Interfaces](#maps-annotation-event-interfaces)
  - [Maps Zoom and Pan Event Interfaces](#maps-zoom-and-pan-event-interfaces)
  - [Maps Mouse Event Interfaces](#maps-mouse-event-interfaces)
  - [Print and Export Event Interfaces](#print-and-export-event-interfaces)
  - [Example Importing Interfaces](#example-importing-interfaces)
- [CSS Theme Import](#css-theme-import)
  - [Available Themes](#available-themes)
- [Map Projections](#map-projections)
- [Complete Working Example](#complete-working-example)
  - [Appjsx](#appjsx)
  - [Running the Application](#running-the-application)
- [Common Setup Issues](#common-setup-issues)
  - [Issue Map Not Displaying](#issue-map-not-displaying)
  - [Issue Inject Is Not Defined](#issue-inject-is-not-defined)
  - [Issue Data Not Binding to Shapes](#issue-data-not-binding-to-shapes)
  - [Issue Module Features Not Working](#issue-module-features-not-working)
  - [Issue Shapes Render but No Colors](#issue-shapes-render-but-no-colors)

## Overview

The Syncfusion React Maps component visualizes geographical data using SVG rendering. Use it to render GeoJSON shapes, bind business data to map regions, display labels, add tooltips, show legends, add markers and bubbles, and enable interactions such as zooming, selection, and highlighting.

## Dependencies

The Maps component requires these packages:

```json
{
  "@syncfusion/ej2-react-maps": "^latest",
  "@syncfusion/ej2-maps": "^latest",
  "@syncfusion/ej2-base": "^latest",
  "@syncfusion/ej2-svg-base": "^latest",
  "@syncfusion/ej2-data": "^latest",
  "@syncfusion/ej2-pdf-export": "^latest",
  "@syncfusion/ej2-react-base": "^latest"
}
```

All dependencies are installed automatically with the main package.

## Installation

### Using npm

```bash
npm install @syncfusion/ej2-react-maps --save
```

### Using Vite Recommended

Create a new React project with Vite:

```bash
npm create vite@latest my-maps-app -- --template react
cd my-maps-app
npm install
npm install @syncfusion/ej2-react-maps --save
```

### Using Create React App

```bash
npx create-react-app my-maps-app
cd my-maps-app
npm install @syncfusion/ej2-react-maps --save
```

## Basic Setup

### Project Structure

```text
src/
├── App.jsx
├── world-map.ts
└── data.ts
```

### Importing Components

```tsx
import {
  MapsComponent,
  LayersDirective,
  LayerDirective
} from '@syncfusion/ej2-react-maps';
```

## Understanding GeoJSON Data

Maps render shapes from GeoJSON format. A GeoJSON object contains geographical features and coordinate information.

```typescript
const worldMap = {
  type: 'FeatureCollection',
  crs: {
    type: 'name',
    properties: { name: 'urn:ogc:def:crs:OGC:1.3:CRS84' }
  },
  features: [
    {
      type: 'Feature',
      properties: {
        name: 'United States',
        iso_3166_2: 'US'
      },
      geometry: {
        type: 'Polygon',
        coordinates: [[[-125.0, 50.0], [-66.0, 50.0], [-66.0, 25.0], [-125.0, 25.0]]]
      }
    }
  ]
};
```

**Key Components:**

- `features`: Array of geographical features.
- `properties`: Metadata such as country name and codes.
- `geometry`: Coordinate data for shapes.
- `coordinates`: Longitude and latitude pairs.

### Getting GeoJSON Data

Option 1: Download GeoJSON data and include it in your project.

Option 2: Use custom GeoJSON from your own source and save it as a `.ts` or `.json` file.

Example `world-map.ts`:

```typescript
export let world_map = {
  type: 'FeatureCollection',
  features: []
};
```

## Creating Your First Map

### Minimal Example

```tsx
import * as React from 'react';
import {
  MapsComponent,
  LayersDirective,
  LayerDirective
} from '@syncfusion/ej2-react-maps';
import { world_map } from './world-map';

function App() {
  return (
    <MapsComponent id="maps">
      <LayersDirective>
        <LayerDirective shapeData={world_map} />
      </LayersDirective>
    </MapsComponent>
  );
}

export default App;
```

**What Happens:**

1. `MapsComponent` acts as the main map container.
2. `LayersDirective` wraps one or more map layers.
3. `LayerDirective` renders an individual map layer.
4. `shapeData` receives the GeoJSON data to render.

## Data Binding

Bind custom data to map shapes for color mapping, tooltips, and labels.

### Data Source Structure

```typescript
export let countryData = [
  { Country: 'United States', Population: 331002651, Code: 'US' },
  { Country: 'China', Population: 1439323776, Code: 'CN' },
  { Country: 'India', Population: 1380004385, Code: 'IN' },
  { Country: 'Russia', Population: 145934462, Code: 'RU' }
];
```

### Remote Data Binding DataManager

React Maps can bind directly to remote data sources using Syncfusion DataManager. It supports adapters such as `OData`, `ODataV4`, `WebAPI`, and custom adapters for server-driven mapping scenarios.

```tsx
import { DataManager, ODataAdaptor } from '@syncfusion/ej2-data';

const remote = new DataManager({
  url: 'https://services.odata.org/V4/Northwind/Northwind.svc/Customers',
  adaptor: new ODataAdaptor()
});

<LayerDirective
  shapeData={world_map}
  dataSource={remote}
  shapeDataPath="Country"
  shapePropertyPath="name"
/>
```

### Binding Data to Shapes

```tsx
import { countryData } from './data';

<LayerDirective
  shapeData={world_map}
  dataSource={countryData}
  shapeDataPath="Country"
  shapePropertyPath="name"
/>
```

**How It Works:**

- `dataSource`: Your custom data array.
- `shapeDataPath`: Field in your data that identifies shapes.
- `shapePropertyPath`: Matching field in GeoJSON `properties`.
- When values match, data binds to that shape.

### Example with Color Mapping

```tsx
import { world_map } from './world-map';
import { countryData } from './data';

function App() {
  return (
    <MapsComponent>
      <LayersDirective>
        <LayerDirective
          shapeData={world_map}
          dataSource={countryData}
          shapeDataPath="Country"
          shapePropertyPath="name"
          shapeSettings={{
            colorValuePath: 'Population',
            colorMapping: [
              { from: 0, to: 100000000, color: '#C3E6CB' },
              { from: 100000000, to: 500000000, color: '#6AB187' },
              { from: 500000000, to: 1500000000, color: '#2F7C4F' }
            ]
          }}
        />
      </LayersDirective>
    </MapsComponent>
  );
}
```

## Module Injection

React Maps features are modular and require module injection to enable them. This reduces bundle size by loading only the required map layers, markers, bubbles, data labels, navigation lines, legends, annotations, tooltip, selection, highlight, zooming, print, and export features.

### Inject Modules

```tsx
import * as React from 'react';
import {
  MapsComponent,
  LayersDirective,
  LayerDirective,
  Inject,
  Legend,
  DataLabel,
  MapsTooltip,
  Marker,
  Bubble,
  NavigationLine,
  Zoom,
  Selection,
  Highlight,
  MapsAnnotation,
  Print,
  PdfExport,
  ImageExport
} from '@syncfusion/ej2-react-maps';

function App() {
  const shapeData: Object = {};

  const titleSettings: Object = {
    text: 'World Map'
  };

  const legendSettings: Object = {
    visible: true
  };

  const zoomSettings: Object = {
    enable: true
  };

  const shapeSettings: Object = {
    fill: '#E5E5E5'
  };

  const dataLabelSettings: Object = {
    visible: true,
    labelPath: 'name'
  };

  const tooltipSettings: Object = {
    visible: true,
    valuePath: 'name'
  };

  const markerSettings: Object[] = [
    {
      visible: true,
      dataSource: [
        { latitude: 13.0827, longitude: 80.2707, name: 'Chennai' }
      ],
      latitudeValuePath: 'latitude',
      longitudeValuePath: 'longitude',
      tooltipSettings: {
        visible: true,
        valuePath: 'name'
      }
    }
  ];

  return (
    <MapsComponent
      id="maps-container"
      titleSettings={titleSettings}
      legendSettings={legendSettings}
      zoomSettings={zoomSettings}
    >
      <Inject
        services={[
          Legend,
          DataLabel,
          MapsTooltip,
          Marker,
          Bubble,
          NavigationLine,
          Zoom,
          Selection,
          Highlight,
          MapsAnnotation,
          Print,
          PdfExport,
          ImageExport
        ]}
      />
      <LayersDirective>
        <LayerDirective
          shapeData={shapeData}
          shapeSettings={shapeSettings}
          dataLabelSettings={dataLabelSettings}
          tooltipSettings={tooltipSettings}
          markerSettings={markerSettings}
        />
      </LayersDirective>
    </MapsComponent>
  );
}

export default App;
```

### Layer Modules

| Module | Purpose | Import package |
|--------|---------|----------------|
| `DataLabel` | Enable data labels for map shapes | `@syncfusion/ej2-react-maps` |
| `MapsTooltip` | Enable tooltip support for shapes, markers, and bubbles | `@syncfusion/ej2-react-maps` |
| `Legend` | Enable legend support for map layers, markers, and bubbles | `@syncfusion/ej2-react-maps` |

### Marker and Bubble Modules

| Module | Purpose | Import package |
|--------|---------|----------------|
| `Marker` | Enable markers for specific geographic locations | `@syncfusion/ej2-react-maps` |
| `Bubble` | Enable bubbles to represent data values on map shapes | `@syncfusion/ej2-react-maps` |

### Navigation Line Module

| Module | Purpose | Import package |
|--------|---------|----------------|
| `NavigationLine` | Enable navigation lines to display paths between geographic locations | `@syncfusion/ej2-react-maps` |

### User Interaction Modules

| Module | Purpose | Import package |
|--------|---------|----------------|
| `Zoom` | Enable zooming and panning in Maps | `@syncfusion/ej2-react-maps` |
| `Selection` | Enable map shape selection | `@syncfusion/ej2-react-maps` |
| `Highlight` | Enable map shape highlighting | `@syncfusion/ej2-react-maps` |
| `MapsTooltip` | Enable tooltip interaction for map elements | `@syncfusion/ej2-react-maps` |

### Annotation Module

| Module | Purpose | Import package |
|--------|---------|----------------|
| `MapsAnnotation` | Enable annotations in Maps | `@syncfusion/ej2-react-maps` |

### Print and Export Modules

| Module | Purpose | Import package |
|--------|---------|----------------|
| `Print` | Enable Maps print support | `@syncfusion/ej2-react-maps` |
| `PdfExport` | Enable Maps PDF export support | `@syncfusion/ej2-react-maps` |
| `ImageExport` | Enable Maps image export support such as PNG, JPEG, and SVG | `@syncfusion/ej2-react-maps` |

### Example Full Maps Module Injection

```tsx
import * as React from 'react';
import {
  MapsComponent,
  LayersDirective,
  LayerDirective,
  Inject,
  Legend,
  DataLabel,
  MapsTooltip,
  Marker,
  Bubble,
  NavigationLine,
  Zoom,
  Selection,
  Highlight,
  MapsAnnotation,
  Print,
  PdfExport,
  ImageExport
} from '@syncfusion/ej2-react-maps';

function App() {
  const shapeData: Object = {};

  const titleSettings: Object = {
    text: 'Sales by Region'
  };

  const legendSettings: Object = {
    visible: true
  };

  const zoomSettings: Object = {
    enable: true,
    toolbarSettings: {
      visible: true
    }
  };

  const annotations: Object[] = [
    {
      content: '<div>Map Annotation</div>',
      x: '50%',
      y: '10%'
    }
  ];

  const shapeSettings: Object = {
    fill: '#E5E5E5',
    colorValuePath: 'value'
  };

  const dataLabelSettings: Object = {
    visible: true,
    labelPath: 'name'
  };

  const tooltipSettings: Object = {
    visible: true,
    valuePath: 'name'
  };

  const markerSettings: Object[] = [
    {
      visible: true,
      dataSource: [
        { latitude: 13.0827, longitude: 80.2707, name: 'Chennai' }
      ],
      latitudeValuePath: 'latitude',
      longitudeValuePath: 'longitude',
      tooltipSettings: {
        visible: true,
        valuePath: 'name'
      }
    }
  ];

  const bubbleSettings: Object[] = [
    {
      visible: true,
      valuePath: 'value',
      colorValuePath: 'value',
      minRadius: 10,
      maxRadius: 20
    }
  ];

  const navigationLineSettings: Object[] = [
    {
      visible: true,
      latitude: [13.0827, 28.6139],
      longitude: [80.2707, 77.2090],
      color: '#000000',
      width: 2
    }
  ];

  const selectionSettings: Object = {
    enable: true
  };

  const highlightSettings: Object = {
    enable: true
  };

  return (
    <MapsComponent
      id="maps-container"
      titleSettings={titleSettings}
      legendSettings={legendSettings}
      zoomSettings={zoomSettings}
      annotations={annotations}
    >
      <Inject
        services={[
          Legend,
          DataLabel,
          MapsTooltip,
          Marker,
          Bubble,
          NavigationLine,
          Zoom,
          Selection,
          Highlight,
          MapsAnnotation,
          Print,
          PdfExport,
          ImageExport
        ]}
      />
      <LayersDirective>
        <LayerDirective
          shapeData={shapeData}
          shapeSettings={shapeSettings}
          dataLabelSettings={dataLabelSettings}
          tooltipSettings={tooltipSettings}
          markerSettings={markerSettings}
          bubbleSettings={bubbleSettings}
          navigationLineSettings={navigationLineSettings}
          selectionSettings={selectionSettings}
          highlightSettings={highlightSettings}
        />
      </LayersDirective>
    </MapsComponent>
  );
}

export default App;
```

## Interfaces

React Maps provides TypeScript interfaces to strongly type map configuration, layers, shape settings, markers, bubbles, navigation lines, data labels, legends, annotations, zooming, selection, highlight, tooltips, margins, borders, titles, and event arguments.

### Maps Configuration Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `MapsModel` | Defines the complete configuration model for the Maps component | `@syncfusion/ej2-react-maps` |
| `MapsAreaSettingsModel` | Defines customization options for the area around the map | `@syncfusion/ej2-react-maps` |
| `BorderModel` | Defines border color and width settings | `@syncfusion/ej2-react-maps` |
| `MarginModel` | Defines margin settings for the Maps component | `@syncfusion/ej2-react-maps` |
| `CenterPositionModel` | Defines the center latitude and longitude position of the map | `@syncfusion/ej2-react-maps` |
| `TitleSettingsModel` | Defines map title settings | `@syncfusion/ej2-react-maps` |
| `SubTitleSettingsModel` | Defines map subtitle settings | `@syncfusion/ej2-react-maps` |
| `FontModel` | Defines font style, size, color, weight, opacity, and family settings | `@syncfusion/ej2-react-maps` |

### Layer Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `LayerSettingsModel` | Defines map layer configuration such as shape data, data source, markers, bubbles, data labels, navigation lines, selection, highlight, and tooltip settings | `@syncfusion/ej2-react-maps` |
| `ShapeSettingsModel` | Defines shape appearance settings such as fill, border, color mapping, and value path | `@syncfusion/ej2-react-maps` |
| `ColorMappingSettingsModel` | Defines color mapping settings for map shapes | `@syncfusion/ej2-react-maps` |
| `ToggleLegendSettingsModel` | Defines toggle behavior for map legend selection | `@syncfusion/ej2-react-maps` |
| `InitialShapeSelectionSettingsModel` | Defines initially selected map shapes | `@syncfusion/ej2-react-maps` |
| `PolygonSettingsModel` | Defines polygon shape settings for map layers | `@syncfusion/ej2-react-maps` |

### Data Label Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `DataLabelSettingsModel` | Defines data label settings for map shapes | `@syncfusion/ej2-react-maps` |
| `SmartLabelMode` | Defines smart label behavior for map labels | `@syncfusion/ej2-react-maps` |
| `IntersectAction` | Defines label intersection behavior | `@syncfusion/ej2-react-maps` |

### Marker Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `MarkerSettingsModel` | Defines marker settings such as data source, latitude, longitude, shape, template, and tooltip | `@syncfusion/ej2-react-maps` |
| `MarkerClusterSettingsModel` | Defines marker cluster settings | `@syncfusion/ej2-react-maps` |
| `MarkerClusterData` | Defines marker cluster data information | `@syncfusion/ej2-react-maps` |

### Bubble Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `BubbleSettingsModel` | Defines bubble settings such as value path, color value path, min radius, max radius, opacity, and tooltip | `@syncfusion/ej2-react-maps` |
| `BubbleData` | Defines bubble data information | `@syncfusion/ej2-react-maps` |

### Navigation Line Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `NavigationLineSettingsModel` | Defines navigation line settings such as latitude, longitude, color, width, angle, and dash array | `@syncfusion/ej2-react-maps` |
| `ArrowModel` | Defines arrow settings for navigation lines | `@syncfusion/ej2-react-maps` |

### Tooltip Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `TooltipSettingsModel` | Defines tooltip settings for shapes, markers, and bubbles | `@syncfusion/ej2-react-maps` |
| `TooltipBorderModel` | Defines tooltip border settings | `@syncfusion/ej2-react-maps` |

### Legend Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `LegendSettingsModel` | Defines legend settings for map layers, markers, and bubbles | `@syncfusion/ej2-react-maps` |
| `LegendTitleSettingsModel` | Defines legend title settings | `@syncfusion/ej2-react-maps` |
| `LegendLocationModel` | Defines legend location settings | `@syncfusion/ej2-react-maps` |

### Selection and Highlight Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `SelectionSettingsModel` | Defines selection settings for map shapes | `@syncfusion/ej2-react-maps` |
| `HighlightSettingsModel` | Defines highlight settings for map shapes | `@syncfusion/ej2-react-maps` |

### Zoom Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `ZoomSettingsModel` | Defines zooming and panning behavior for Maps | `@syncfusion/ej2-react-maps` |
| `ToolbarSettingsModel` | Defines zoom toolbar settings | `@syncfusion/ej2-react-maps` |
| `ZoomToolbarButtonSettingsModel` | Defines zoom toolbar button customization settings | `@syncfusion/ej2-react-maps` |
| `ZoomToolbarTooltipSettingsModel` | Defines zoom toolbar tooltip settings | `@syncfusion/ej2-react-maps` |

### Annotation Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `AnnotationModel` | Defines annotation settings for Maps | `@syncfusion/ej2-react-maps` |
| `MapsAnnotationModel` | Defines map annotation configuration | `@syncfusion/ej2-react-maps` |

### Tile Map and Ajax Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `MapAjaxModel` | Defines Ajax settings for loading map data | `@syncfusion/ej2-react-maps` |
| `OSM` | Defines OpenStreetMap tile provider support | `@syncfusion/ej2-react-maps` |
| `BingMap` | Defines Bing Maps tile provider support | `@syncfusion/ej2-react-maps` |

### Maps Lifecycle Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `ILoadEventArgs` | Defines event arguments before Maps loading | `@syncfusion/ej2-react-maps` |
| `ILoadedEventArgs` | Defines event arguments after Maps rendering is completed | `@syncfusion/ej2-react-maps` |
| `IResizeEventArgs` | Defines event arguments after Maps resize | `@syncfusion/ej2-react-maps` |
| `IAnimationCompleteEventArgs` | Defines event arguments after map animation is completed | `@syncfusion/ej2-react-maps` |

### Maps Shape Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `IShapeRenderingEventArgs` | Defines event arguments used while rendering map shapes | `@syncfusion/ej2-react-maps` |
| `IShapeSelectedEventArgs` | Defines event arguments when a map shape is selected | `@syncfusion/ej2-react-maps` |
| `IShapeHighlightEventArgs` | Defines event arguments when a map shape is highlighted | `@syncfusion/ej2-react-maps` |
| `IShapeSelectionCompleteEventArgs` | Defines event arguments after map shape selection is completed | `@syncfusion/ej2-react-maps` |

### Maps Marker Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `IMarkerRenderingEventArgs` | Defines event arguments used while rendering map markers | `@syncfusion/ej2-react-maps` |
| `IMarkerClickEventArgs` | Defines event arguments for marker click events | `@syncfusion/ej2-react-maps` |
| `IMarkerMoveEventArgs` | Defines event arguments for marker mouse move events | `@syncfusion/ej2-react-maps` |
| `IMarkerClusterRenderingEventArgs` | Defines event arguments used while rendering marker clusters | `@syncfusion/ej2-react-maps` |
| `IMarkerClusterClickEventArgs` | Defines event arguments for marker cluster click events | `@syncfusion/ej2-react-maps` |
| `IMarkerClusterMoveEventArgs` | Defines event arguments for marker cluster mouse move events | `@syncfusion/ej2-react-maps` |

### Maps Bubble Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `IBubbleRenderingEventArgs` | Defines event arguments used while rendering map bubbles | `@syncfusion/ej2-react-maps` |
| `IBubbleClickEventArgs` | Defines event arguments for bubble click events | `@syncfusion/ej2-react-maps` |
| `IBubbleMoveEventArgs` | Defines event arguments for bubble mouse move events | `@syncfusion/ej2-react-maps` |

### Maps Navigation Line Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `INavigationLineRenderingEventArgs` | Defines event arguments used while rendering navigation lines | `@syncfusion/ej2-react-maps` |

### Maps Tooltip and Legend Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `ITooltipRenderEventArgs` | Defines event arguments used while rendering Maps tooltip | `@syncfusion/ej2-react-maps` |
| `ILegendRenderingEventArgs` | Defines event arguments used while rendering Maps legend | `@syncfusion/ej2-react-maps` |

### Maps Annotation Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `IAnnotationRenderingEventArgs` | Defines event arguments used while rendering Maps annotations | `@syncfusion/ej2-react-maps` |

### Maps Zoom and Pan Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `IZoomEventArgs` | Defines event arguments for map zoom events | `@syncfusion/ej2-react-maps` |
| `IMapPanEventArgs` | Defines event arguments for map pan events | `@syncfusion/ej2-react-maps` |

### Maps Mouse Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `IClickEventArgs` | Defines event arguments for Maps click events | `@syncfusion/ej2-react-maps` |
| `IMouseMoveEventArgs` | Defines event arguments for Maps mouse move events | `@syncfusion/ej2-react-maps` |
| `IDoubleClickEventArgs` | Defines event arguments for Maps double-click events | `@syncfusion/ej2-react-maps` |
| `IRightClickEventArgs` | Defines event arguments for Maps right-click events | `@syncfusion/ej2-react-maps` |

### Print and Export Event Interfaces

| Interface | Purpose | Import package |
|-----------|---------|----------------|
| `IPrintEventArgs` | Defines event arguments for Maps print events | `@syncfusion/ej2-react-maps` |
| `IExportEventArgs` | Defines event arguments for Maps export events | `@syncfusion/ej2-react-maps` |

### Example Importing Interfaces

```tsx
import {
  MapsModel,
  LayerSettingsModel,
  ShapeSettingsModel,
  DataLabelSettingsModel,
  MarkerSettingsModel,
  BubbleSettingsModel,
  NavigationLineSettingsModel,
  LegendSettingsModel,
  TooltipSettingsModel,
  ZoomSettingsModel,
  SelectionSettingsModel,
  HighlightSettingsModel,
  AnnotationModel,
  MapsAreaSettingsModel,
  BorderModel,
  MarginModel,
  TitleSettingsModel,
  FontModel,
  CenterPositionModel,
  ColorMappingSettingsModel,
  InitialShapeSelectionSettingsModel,
  MarkerClusterSettingsModel,
  ToggleLegendSettingsModel,
  PolygonSettingsModel,
  MapAjaxModel,
  ILoadEventArgs,
  ILoadedEventArgs,
  IResizeEventArgs,
  IAnimationCompleteEventArgs,
  IShapeRenderingEventArgs,
  IShapeSelectedEventArgs,
  IMarkerRenderingEventArgs,
  IMarkerClickEventArgs,
  IBubbleRenderingEventArgs,
  INavigationLineRenderingEventArgs,
  ITooltipRenderEventArgs,
  ILegendRenderingEventArgs,
  IAnnotationRenderingEventArgs,
  IZoomEventArgs,
  IMapPanEventArgs,
  IClickEventArgs,
  IMouseMoveEventArgs,
  IPrintEventArgs,
  IExportEventArgs
} from '@syncfusion/ej2-react-maps';

const border: BorderModel = {
  color: '#000000',
  width: 1
};

const margin: MarginModel = {
  left: 10,
  right: 10,
  top: 10,
  bottom: 10
};

const titleStyle: FontModel = {
  size: '16px',
  fontWeight: '600'
};

const titleSettings: TitleSettingsModel = {
  text: 'Sales by Region',
  textStyle: titleStyle
};

const centerPosition: CenterPositionModel = {
  latitude: 20.5937,
  longitude: 78.9629
};

const mapsArea: MapsAreaSettingsModel = {
  background: '#FFFFFF',
  border
};

const colorMapping: ColorMappingSettingsModel = {
  from: 0,
  to: 100,
  color: '#D6EAF8',
  label: 'Low'
};

const shapeSettings: ShapeSettingsModel = {
  fill: '#E5E5E5',
  colorValuePath: 'value',
  colorMapping: [colorMapping]
};

const dataLabelSettings: DataLabelSettingsModel = {
  visible: true,
  labelPath: 'name'
};

const tooltipSettings: TooltipSettingsModel = {
  visible: true,
  valuePath: 'name'
};

const markerSettings: MarkerSettingsModel[] = [
  {
    visible: true,
    dataSource: [
      { latitude: 13.0827, longitude: 80.2707, name: 'Chennai' }
    ],
    latitudeValuePath: 'latitude',
    longitudeValuePath: 'longitude',
    tooltipSettings
  }
];

const bubbleSettings: BubbleSettingsModel[] = [
  {
    visible: true,
    valuePath: 'value',
    colorValuePath: 'value',
    minRadius: 10,
    maxRadius: 20,
    tooltipSettings
  }
];

const navigationLineSettings: NavigationLineSettingsModel[] = [
  {
    visible: true,
    latitude: [13.0827, 28.6139],
    longitude: [80.2707, 77.2090],
    color: '#000000',
    width: 2
  }
];

const selectionSettings: SelectionSettingsModel = {
  enable: true
};

const highlightSettings: HighlightSettingsModel = {
  enable: true
};

const initialShapeSelection: InitialShapeSelectionSettingsModel = {
  shapePath: 'name',
  shapeValue: 'India'
};

const markerClusterSettings: MarkerClusterSettingsModel = {
  allowClustering: true
};

const toggleLegendSettings: ToggleLegendSettingsModel = {
  enable: true
};

const polygonSettings: PolygonSettingsModel = {
  visible: true
};

const layer: LayerSettingsModel = {
  shapeData: {},
  shapeSettings,
  dataLabelSettings,
  tooltipSettings,
  markerSettings,
  bubbleSettings,
  navigationLineSettings,
  selectionSettings,
  highlightSettings,
  initialShapeSelection: [initialShapeSelection],
  markerClusterSettings,
  toggleLegendSettings,
  polygonSettings
};

const legendSettings: LegendSettingsModel = {
  visible: true
};

const zoomSettings: ZoomSettingsModel = {
  enable: true,
  toolbarSettings: {
    visible: true
  }
};

const annotation: AnnotationModel = {
  content: '<div>Map Annotation</div>',
  x: '50%',
  y: '10%'
};

const ajaxSettings: MapAjaxModel = {
  url: 'map-data.json'
};

const mapsOptions: MapsModel = {
  titleSettings,
  margin,
  mapsArea,
  centerPosition,
  legendSettings,
  zoomSettings,
  annotations: [annotation],
  layers: [layer]
};

const load = (args: ILoadEventArgs): void => {
  // Maps loading.
};

const loaded = (args: ILoadedEventArgs): void => {
  // Maps loaded.
};

const resized = (args: IResizeEventArgs): void => {
  // Maps resized.
};

const animationComplete = (args: IAnimationCompleteEventArgs): void => {
  // Maps animation completed.
};

const shapeRendering = (args: IShapeRenderingEventArgs): void => {
  // Map shape rendering.
};

const shapeSelected = (args: IShapeSelectedEventArgs): void => {
  // Map shape selected.
};

const markerRendering = (args: IMarkerRenderingEventArgs): void => {
  // Marker rendering.
};

const markerClick = (args: IMarkerClickEventArgs): void => {
  // Marker clicked.
};

const bubbleRendering = (args: IBubbleRenderingEventArgs): void => {
  // Bubble rendering.
};

const navigationLineRendering = (args: INavigationLineRenderingEventArgs): void => {
  // Navigation line rendering.
};

const tooltipRender = (args: ITooltipRenderEventArgs): void => {
  // Tooltip rendering.
};

const legendRendering = (args: ILegendRenderingEventArgs): void => {
  // Legend rendering.
};

const annotationRendering = (args: IAnnotationRenderingEventArgs): void => {
  // Annotation rendering.
};

const zoom = (args: IZoomEventArgs): void => {
  // Map zooming.
};

const pan = (args: IMapPanEventArgs): void => {
  // Map panning.
};

const click = (args: IClickEventArgs): void => {
  // Maps clicked.
};

const mouseMove = (args: IMouseMoveEventArgs): void => {
  // Maps mouse move.
};

const beforePrint = (args: IPrintEventArgs): void => {
  // Before Maps print.
};

const beforeExport = (args: IExportEventArgs): void => {
  // Before Maps export.
};
```

## CSS Theme Import

Import CSS for the theme you want to use. Use only one theme at a time.

### Available Themes

The component supports multiple themes, including:

- `Material`, `MaterialDark`, `Material3`, `Material3Dark`
- `Fabric`, `FabricDark`
- `Bootstrap`, `BootstrapDark`, `Bootstrap4`, `Bootstrap5`, `Bootstrap5Dark`, `Bootstrap5.3`, `Bootstrap5.3Dark`
- `Tailwind`, `TailwindDark`
- `Fluent`, `FluentDark`, `Fluent2`, `Fluent2Dark`, `Fluent2HighContrast`
- `HighContrast`, `HighContrastLight`

Switch themes with the `theme` prop:

```tsx
<MapsComponent theme="Material3Dark">
  {/* Maps content */}
</MapsComponent>
```

Import the selected theme at the top of your component file or in `main.jsx` / `App.jsx`.

## Map Projections

React Maps supports multiple geographical projection systems such as `Mercator`, `Miller`, `Winkel3`, and `Eckert` series. Choosing the right projection helps control shape distortion and improves geographical accuracy at different zoom levels.

```tsx
<LayerDirective
  shapeData={world_map}
  projectionType="Mercator"
/>
```

## Complete Working Example

### Appjsx

```tsx
import * as React from 'react';
import {
  MapsComponent,
  LayersDirective,
  LayerDirective,
  Inject,
  Legend,
  MapsTooltip
} from '@syncfusion/ej2-react-maps';
import { world_map } from './world-map';

function App() {
  const populationData = [
    { Country: 'China', Population: 1439323776 },
    { Country: 'United States', Population: 331002651 },
    { Country: 'India', Population: 1380004385 },
    { Country: 'Indonesia', Population: 273523615 },
    { Country: 'Pakistan', Population: 220892340 }
  ];

  return (
    <div style={{ margin: '20px' }}>
      <h2>World Population Map</h2>
      <MapsComponent
        id="maps"
        titleSettings={{
          text: 'Population by Country',
          textStyle: { size: '16px', fontWeight: '500' }
        }}
        legendSettings={{
          visible: true,
          position: 'Bottom'
        }}
      >
        <Inject services={[Legend, MapsTooltip]} />
        <LayersDirective>
          <LayerDirective
            shapeData={world_map}
            dataSource={populationData}
            shapeDataPath="Country"
            shapePropertyPath="name"
            shapeSettings={{
              fill: '#E5E5E5',
              colorValuePath: 'Population',
              colorMapping: [
                { from: 0, to: 100000000, color: '#C3E6CB', label: '< 100M' },
                { from: 100000000, to: 500000000, color: '#6AB187', label: '100M - 500M' },
                { from: 500000000, to: 1500000000, color: '#2F7C4F', label: '> 500M' }
              ]
            }}
            tooltipSettings={{
              visible: true,
              valuePath: 'Country',
              format: '${Country}: ${Population}'
            }}
          />
        </LayersDirective>
      </MapsComponent>
    </div>
  );
}

export default App;
```

### Running the Application

```bash
npm run dev
```

For Create React App:

```bash
npm start
```

## Common Setup Issues

### Issue Map Not Displaying

**Causes:**

- GeoJSON data is not imported correctly.
- CSS is not imported.
- GeoJSON structure is invalid.

**Solution:**

```tsx
import { world_map } from './world-map';
```

Ensure that `world_map` is exported from the `world-map` file.

### Issue Inject Is Not Defined

**Cause:** Missing import for `Inject`.

**Solution:**

```tsx
import { MapsComponent, Inject, Legend } from '@syncfusion/ej2-react-maps';
```

### Issue Data Not Binding to Shapes

**Causes:**

- `shapeDataPath` does not match the data field.
- `shapePropertyPath` does not match the GeoJSON property.
- Field name case mismatch.

**Solution:**

```tsx
console.log(world_map.features[0].properties);

<LayerDirective
  shapePropertyPath="name"
  shapeDataPath="Country"
/>
```

### Issue Module Features Not Working

**Cause:** Required module was not injected.

**Solution:**

```tsx
<MapsComponent legendSettings={{ visible: true }}>
  <Inject services={[Legend]} />
</MapsComponent>
```

### Issue Shapes Render but No Colors

**Cause:** Color mapping is not configured or data is not bound.

**Solution:**

```tsx
<LayerDirective
  shapeData={world_map}
  dataSource={data}
  shapeDataPath="Country"
  shapePropertyPath="name"
  shapeSettings={{
    colorValuePath: 'Population',
    colorMapping: [
      { from: 0, to: 100000000, color: '#C3E6CB' }
    ]
  }}
/>
```
