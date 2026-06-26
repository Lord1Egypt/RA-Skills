````markdown
# Syncfusion React Maps API Reference

## Table of Contents
- [MapsComponent](#mapscomponent)
  - [Properties](#properties)
  - [Methods](#methods)
  - [Events](#events)
- [Layer Settings](#layer-settings)
- [Marker Settings](#marker-settings)
- [Bubble Settings](#bubble-settings)
- [Data Label Settings](#data-label-settings)
- [Legend Settings](#legend-settings)
- [Zoom Settings](#zoom-settings)
- [Tooltip Settings](#tooltip-settings)
- [Quick Reference Examples](#quick-reference-examples)

## MapsComponent

The main React component for rendering interactive maps with geographical data visualization.

```tsx
<MapsComponent
  // Essential properties
  id="maps"
  width="100%"
  height="500px"
  
  // Configuration
  titleSettings={{ text: 'World Map' }}
  legendSettings={{ visible: true }}
  zoomSettings={{ enable: true }}
>
  <Inject services={[Legend, Zoom, MapsTooltip]} />
  <LayersDirective>
    <LayerDirective shapeData={geoJsonData} />
  </LayersDirective>
</MapsComponent>
```

---

## Properties

### allowImageExport
- **Type**: `boolean`
- **Default**: `false`
- **Description**: Enables or disables the export to image functionality (PNG, JPEG, SVG)
- **Requires**: `ImageExport` service injection

```tsx
import { ImageExport } from '@syncfusion/ej2-react-maps';

<MapsComponent allowImageExport={true}>
  <Inject services={[ImageExport]} />
</MapsComponent>
```

### allowPdfExport
- **Type**: `boolean`
- **Default**: `false`
- **Description**: Enables or disables the export to PDF functionality
- **Requires**: `PdfExport` service injection

```tsx
import { PdfExport } from '@syncfusion/ej2-react-maps';

<MapsComponent allowPdfExport={true}>
  <Inject services={[PdfExport]} />
</MapsComponent>
```

### allowPrint
- **Type**: `boolean`
- **Default**: `false`
- **Description**: Enables or disables the print functionality
- **Requires**: `Print` service injection

```tsx
import { Print } from '@syncfusion/ej2-react-maps';

<MapsComponent allowPrint={true}>
  <Inject services={[Print]} />
</MapsComponent>
```

### annotations
- **Type**: `AnnotationModel[]`
- **Description**: Gets or sets the options for customizing annotations in the maps
- **Requires**: `Annotations` service injection

```tsx
<MapsComponent
  annotations={[
    {
      content: '<div>Custom Annotation</div>',
      x: '50%',
      y: '50%',
      horizontalAlignment: 'Center',
      verticalAlignment: 'Center'
    }
  ]}
>
  <Inject services={[Annotations]} />
</MapsComponent>
```

### background
- **Type**: `string`
- **Default**: `null`
- **Description**: Gets or sets the background color of the maps container

```tsx
<MapsComponent background="#F5F5F5">
```

### baseLayerIndex
- **Type**: `number`
- **Default**: `0`
- **Description**: Gets or sets the index of the layer that will be the base layer

```tsx
<MapsComponent baseLayerIndex={0}>
  <LayersDirective>
    <LayerDirective shapeData={worldMap} />
    <LayerDirective type="SubLayer" shapeData={countryMap} />
  </LayersDirective>
</MapsComponent>
```

### border
- **Type**: `BorderModel`
- **Description**: Gets or sets the options for customizing the border of the maps

```tsx
<MapsComponent
  border={{
    color: '#000000',
    width: 2
  }}
>
```

### centerPosition
- **Type**: `CenterPositionModel`
- **Description**: Gets or sets the center position of the maps

```tsx
<MapsComponent
  centerPosition={{
    latitude: 23.5937,
    longitude: 78.9629
  }}
>
```

### description
- **Type**: `string`
- **Default**: `null`
- **Description**: Gets or sets the description for assistive technology (accessibility)

```tsx
<MapsComponent
  description="Interactive world map showing country populations"
>
```

### enablePersistence
- **Type**: `boolean`
- **Default**: `false`
- **Description**: Enable or disable persisting component's state between page reloads (localStorage)

```tsx
<MapsComponent id="maps" enablePersistence={true}>
```

### enableRtl
- **Type**: `boolean`
- **Default**: `false`
- **Description**: Enable or disable rendering component in right to left direction

```tsx
<MapsComponent enableRtl={true}>
```

### format
- **Type**: `string`
- **Default**: `null`
- **Description**: Gets or sets the format to apply internationalization for text

```tsx
<MapsComponent format="n2">
```

### height
- **Type**: `string`
- **Default**: `null`
- **Description**: Gets or sets the height in which the maps is to be rendered

```tsx
<MapsComponent height="600px">
<MapsComponent height="100%">
```

### isShapeSelected
- **Type**: `boolean`
- **Description**: Specifies whether the shape is selected in the maps or not (read-only)

### layers
- **Type**: `LayerSettingsModel[]`
- **Description**: Gets or sets the options to customize the layers of the maps

```tsx
<MapsComponent>
  <LayersDirective>
    <LayerDirective
      shapeData={worldMap}
      shapeSettings={{ fill: '#E5E5E5' }}
    />
  </LayersDirective>
</MapsComponent>
```

### legendSettings
- **Type**: `LegendSettingsModel`
- **Description**: Gets or sets the options to customize the legend
- **Requires**: `Legend` service injection

```tsx
<MapsComponent
  legendSettings={{
    visible: true,
    position: 'Bottom',
    alignment: 'Center'
  }}
>
  <Inject services={[Legend]} />
</MapsComponent>
```

### locale
- **Type**: `string`
- **Default**: `''`
- **Description**: Overrides the global culture and localization value for this component

```tsx
import { L10n } from '@syncfusion/ej2-base';

L10n.load({
  'de': {
    'maps': {
      'ZoomIn': 'Hineinzoomen',
      'ZoomOut': 'Rauszoomen'
    }
  }
});

<MapsComponent locale="de">
```

### mapsArea
- **Type**: `MapsAreaSettingsModel`
- **Description**: Gets or sets the options to customize the area around the map

```tsx
<MapsComponent
  mapsArea={{
    background: '#FFFFFF',
    border: { color: '#000000', width: 1 }
  }}
>
```

### margin
- **Type**: `MarginModel`
- **Description**: Gets or sets the options to customize the margin of the maps

```tsx
<MapsComponent
  margin={{
    left: 10,
    right: 10,
    top: 10,
    bottom: 10
  }}
>
```

### projectionType
- **Type**: `ProjectionType`
- **Default**: `'Mercator'`
- **Description**: Gets or sets the projection type for rendering the map
- **Options**: `'Mercator'`, `'Equirectangular'`, `'Miller'`, `'Eckert3'`, `'Eckert5'`, `'Eckert6'`, `'Winkel3'`, `'AitOff'`

```tsx
<MapsComponent projectionType="Mercator">
<MapsComponent projectionType="Miller">
<MapsComponent projectionType="Equirectangular">
```

### tabIndex
- **Type**: `number`
- **Default**: `0`
- **Description**: Gets or sets the tab index value for the maps (accessibility)

```tsx
<MapsComponent tabIndex={1}>
```

### theme
- **Type**: `MapsTheme`
- **Default**: `'Material'`
- **Description**: Gets or sets the theme styles supported for maps
- **Options**: `'Material'`, `'Fabric'`, `'Bootstrap'`, `'Bootstrap4'`, `'Bootstrap5'`, `'Tailwind'`, `'Fluent'`, `'Material3'`, etc.

```tsx
<MapsComponent theme="Bootstrap5">
<MapsComponent theme="Material3">
<MapsComponent theme="Tailwind">
```

### titleSettings
- **Type**: `TitleSettingsModel`
- **Description**: Gets or sets the options to customize the title of the maps

```tsx
<MapsComponent
  titleSettings={{
    text: 'World Population Map',
    textStyle: {
      size: '18px',
      fontWeight: 'Bold',
      color: '#000000',
      fontFamily: 'Arial'
    },
    alignment: 'Center',
    subtitleSettings: {
      text: 'Data as of 2024',
      textStyle: { size: '12px' }
    }
  }}
>
```

### tooltipDisplayMode
- **Type**: `TooltipGesture`
- **Default**: `'MouseMove'`
- **Description**: Gets or sets the mode in which the tooltip is displayed
- **Options**: `'MouseMove'`, `'Click'`, `'DoubleClick'`

```tsx
<MapsComponent tooltipDisplayMode="Click">
<MapsComponent tooltipDisplayMode="MouseMove">
```

### useGroupingSeparator
- **Type**: `boolean`
- **Default**: `false`
- **Description**: Enables or disables the visibility state of the separator for grouping (thousands separator)

```tsx
<MapsComponent useGroupingSeparator={true}>
// 1000000 displays as 1,000,000
```

### width
- **Type**: `string`
- **Default**: `null`
- **Description**: Gets or sets the width in which the maps is to be rendered

```tsx
<MapsComponent width="800px">
<MapsComponent width="100%">
```

### zoomSettings
- **Type**: `ZoomSettingsModel`
- **Description**: Gets or sets the options to customize the zooming operations
- **Requires**: `Zoom` service injection

```tsx
<MapsComponent
  zoomSettings={{
    enable: true,
    enablePanning: true,
    zoomFactor: 1,
    maxZoom: 10,
    minZoom: 1,
    toolbars: ['Zoom', 'ZoomIn', 'ZoomOut', 'Pan', 'Reset']
  }}
>
  <Inject services={[Zoom]} />
</MapsComponent>
```

---

## Methods

Access methods using a ref to the MapsComponent:

```tsx
const mapsRef = React.useRef(null);

<MapsComponent ref={mapsRef}>
```

### addLayer
Adds layers dynamically to the maps.

```tsx
const addNewLayer = () => {
  mapsRef.current.addLayer({
    shapeData: newGeoJson,
    type: 'SubLayer',
    shapeSettings: { fill: '#FF0000' }
  });
};
```

**Parameters:**
- `layer` (Object): Specifies the layer to be added

**Returns:** `void`

### addMarker
Adds markers dynamically to the maps.

```tsx
const addMarkers = () => {
  mapsRef.current.addMarker(0, [
    {
      visible: true,
      dataSource: [
        { latitude: 40.7128, longitude: -74.0060, name: 'New York' }
      ]
    }
  ]);
};
```

**Parameters:**
- `layerIndex` (optional, number): Specifies the index of the layer
- `markerCollection` (optional, MarkerSettingsModel[]): Specifies the marker settings

**Returns:** `void`

### destroy
Destroys the maps component and removes all events.

```tsx
const destroyMap = () => {
  mapsRef.current.destroy();
};
```

**Returns:** `void`

### export
Exports the maps to specified format.

```tsx
const exportMap = () => {
  // Export as PNG
  mapsRef.current.export('PNG', 'world-map');
  
  // Export as PDF (Portrait)
  mapsRef.current.export('PDF', 'world-map', 0);
  
  // Export as PDF (Landscape)
  mapsRef.current.export('PDF', 'world-map', 1);
  
  // Get base64 string instead of download
  mapsRef.current.export('PNG', 'world-map', null, false).then((data) => {
    console.log(data);
  });
};
```

**Parameters:**
- `type` (ExportType): `'PNG'`, `'JPEG'`, `'SVG'`, `'PDF'`
- `fileName` (string): Name of the exported file
- `orientation` (optional, PdfPageOrientation): `0` for Portrait, `1` for Landscape
- `allowDownload` (optional, boolean): `true` to download, `false` to get base64 string

**Returns:** `Promise<string>`

### getBingUrlTemplate
Gets the Bing maps URL template.

```tsx
const setupBingMaps = async () => {
  const url = await mapsRef.current.getBingUrlTemplate(
    'Add your URL link'
  );
  console.log('Bing URL:', url);
};
```

**Parameters:**
- `url` (string): Bing maps URL with API key

**Returns:** `Promise<string>`

### getGeoLocation
Gets geographical coordinates for pixel location (shape maps).

```tsx
const getLocation = () => {
  const geoPosition = mapsRef.current.getGeoLocation(0, 250, 150);
  console.log('Latitude:', geoPosition.latitude);
  console.log('Longitude:', geoPosition.longitude);
};
```

**Parameters:**
- `layerIndex` (number): Index of the layer
- `x` (number): X position in pixels
- `y` (number): Y position in pixels

**Returns:** `GeoPosition { latitude: number, longitude: number }`

### getTileGeoLocation
Gets geographical coordinates for pixel location (online map providers).

```tsx
const getTileLocation = () => {
  const geoPosition = mapsRef.current.getTileGeoLocation(250, 150);
  console.log('Latitude:', geoPosition.latitude);
  console.log('Longitude:', geoPosition.longitude);
};
```

**Parameters:**
- `x` (number): X position in pixels
- `y` (number): Y position in pixels

**Returns:** `GeoPosition { latitude: number, longitude: number }`

### panByDirection
Performs panning in the specified direction.

```tsx
const panMap = (direction) => {
  mapsRef.current.panByDirection(direction);
};

// Usage
<button onClick={() => panMap('Left')}>Pan Left</button>
<button onClick={() => panMap('Right')}>Pan Right</button>
<button onClick={() => panMap('Top')}>Pan Up</button>
<button onClick={() => panMap('Bottom')}>Pan Down</button>
```

**Parameters:**
- `direction` (PanDirection): `'Left'`, `'Right'`, `'Top'`, `'Bottom'`
- `mouseLocation` (optional, PointerEvent | TouchEvent): Mouse/touch event

**Returns:** `void`

### pointToLatLong
Converts pixel point to latitude and longitude.

```tsx
const convertPoint = () => {
  const latLong = mapsRef.current.pointToLatLong(300, 200);
  console.log('Lat:', latLong.latitude, 'Long:', latLong.longitude);
};
```

**Parameters:**
- `pageX` (number): X position in pixels
- `pageY` (number): Y position in pixels

**Returns:** `Object { latitude: number, longitude: number }`

### print
Prints the maps.

```tsx
const printMap = () => {
  // Print current map
  mapsRef.current.print();
  
  // Print specific element
  mapsRef.current.print('maps-container');
  
  // Print multiple elements
  mapsRef.current.print(['map1', 'map2']);
};
```

**Parameters:**
- `id` (optional, string | string[] | Element): Element(s) to print

**Returns:** `void`

### removeLayer
Removes a layer from the maps.

```tsx
const removeSecondLayer = () => {
  mapsRef.current.removeLayer(1);
};
```

**Parameters:**
- `index` (number): Index of the layer to remove

**Returns:** `void`

### shapeSelection
Selects or deselects a shape in the maps.

```tsx
const selectShape = () => {
  // Select shape
  mapsRef.current.shapeSelection(0, 'name', 'United States', true);
  
  // Deselect shape
  mapsRef.current.shapeSelection(0, 'name', 'United States', false);
};
```

**Parameters:**
- `layerIndex` (number): Index of the layer
- `propertyName` (string | string[]): Property name from data source
- `name` (string): Name of the shape to select
- `enable` (optional, boolean): `true` to select, `false` to deselect

**Returns:** `void`

### zoomByPosition
Zooms the map to specified center position.

```tsx
const zoomToLocation = () => {
  mapsRef.current.zoomByPosition(
    { latitude: 40.7128, longitude: -74.0060 },
    2  // Zoom factor
  );
};
```

**Parameters:**
- `centerPosition` (Object): `{ latitude: number, longitude: number }`
- `zoomFactor` (number): Zoom factor to apply

**Returns:** `void`

### zoomToCoordinates
Zooms to the specified coordinate bounds.

```tsx
const zoomToBounds = () => {
  mapsRef.current.zoomToCoordinates(
    25.0,   // minLatitude
    -125.0, // minLongitude
    49.0,   // maxLatitude
    -66.0   // maxLongitude
  );
};
```

**Parameters:**
- `minLatitude` (number): Minimum latitude
- `minLongitude` (number): Minimum longitude
- `maxLatitude` (number): Maximum latitude
- `maxLongitude` (number): Maximum longitude

**Returns:** `void`

---

## Events

All events are passed as props to the MapsComponent:

```tsx
<MapsComponent
  load={(args) => console.log('Loading')}
  loaded={(args) => console.log('Loaded')}
  click={(args) => console.log('Clicked')}
>
```

### animationComplete
- **Type**: `EmitType<IAnimationCompleteEventArgs>`
- **Description**: Triggers after the animation is completed

```tsx
<MapsComponent
  animationComplete={(args) => {
    console.log('Animation completed');
  }}
>
```

### annotationRendering
- **Type**: `EmitType<IAnnotationRenderingEventArgs>`
- **Description**: Triggers before rendering an annotation

```tsx
<MapsComponent
  annotationRendering={(args) => {
    // Customize annotation before rendering
    args.content = '<div>Modified Annotation</div>';
  }}
>
```

### beforePrint
- **Type**: `EmitType<IPrintEventArgs>`
- **Description**: Triggers before the print gets started

```tsx
<MapsComponent
  beforePrint={(args) => {
    console.log('Starting print');
  }}
>
```

### bubbleClick
- **Type**: `EmitType<IBubbleClickEventArgs>`
- **Description**: Triggers when clicking on a bubble element

```tsx
<MapsComponent
  bubbleClick={(args) => {
    console.log('Bubble clicked:', args.data);
  }}
>
```

### bubbleMouseMove
- **Type**: `EmitType<IBubbleMoveEventArgs>`
- **Description**: Triggers when hovering over a bubble element

```tsx
<MapsComponent
  bubbleMouseMove={(args) => {
    console.log('Hovering bubble:', args.data);
  }}
>
```

### bubbleRendering
- **Type**: `EmitType<IBubbleRenderingEventArgs>`
- **Description**: Triggers before the bubble element gets rendered

```tsx
<MapsComponent
  bubbleRendering={(args) => {
    // Customize bubble before rendering
    if (args.data.population > 1000000) {
      args.fill = '#FF0000';
    }
  }}
>
```

### click
- **Type**: `EmitType<IMouseEventArgs>`
- **Description**: Triggers when clicking on an element in maps

```tsx
<MapsComponent
  click={(args) => {
    console.log('Clicked at:', args.x, args.y);
  }}
>
```

### dataLabelRendering
- **Type**: `EmitType<ILabelRenderingEventArgs>`
- **Description**: Triggers before the data-label gets rendered

```tsx
<MapsComponent
  dataLabelRendering={(args) => {
    // Customize label before rendering
    args.text = args.text.toUpperCase();
  }}
>
```

### doubleClick
- **Type**: `EmitType<IMouseEventArgs>`
- **Description**: Triggers when double clicking on an element

```tsx
<MapsComponent
  doubleClick={(args) => {
    console.log('Double clicked at:', args.x, args.y);
  }}
>
```

### itemHighlight
- **Type**: `EmitType<ISelectionEventArgs>`
- **Description**: Triggers before shape, bubble, or marker gets highlighted

```tsx
<MapsComponent
  itemHighlight={(args) => {
    console.log('Highlighting:', args.shapeData);
  }}
>
```

### itemSelection
- **Type**: `EmitType<ISelectionEventArgs>`
- **Description**: Triggers before shape, bubble, or marker gets selected

```tsx
<MapsComponent
  itemSelection={(args) => {
    console.log('Selected:', args.shapeData);
    // Prevent selection
    args.cancel = true;
  }}
>
```

### layerRendering
- **Type**: `EmitType<ILayerRenderingEventArgs>`
- **Description**: Triggers before the maps layer gets rendered

```tsx
<MapsComponent
  layerRendering={(args) => {
    console.log('Rendering layer:', args.index);
  }}
>
```

### legendRendering
- **Type**: `EmitType<ILegendRenderingEventArgs>`
- **Description**: Triggers before the legend gets rendered

```tsx
<MapsComponent
  legendRendering={(args) => {
    // Customize legend items
    args.fill = '#FF0000';
  }}
>
```

### load
- **Type**: `EmitType<ILoadEventArgs>`
- **Description**: Triggers before the maps gets rendered

```tsx
<MapsComponent
  load={(args) => {
    console.log('Maps loading');
  }}
>
```

### loaded
- **Type**: `EmitType<ILoadedEventArgs>`
- **Description**: Triggers after the maps gets rendered

```tsx
<MapsComponent
  loaded={(args) => {
    console.log('Maps loaded successfully');
  }}
>
```

### markerClick
- **Type**: `EmitType<IMarkerClickEventArgs>`
- **Description**: Triggers when clicking on a marker element

```tsx
<MapsComponent
  markerClick={(args) => {
    console.log('Marker clicked:', args.data);
    alert(`Clicked: ${args.data.name}`);
  }}
>
```

### markerClusterClick
- **Type**: `EmitType<IMarkerClusterClickEventArgs>`
- **Description**: Triggers when clicking on a marker cluster

```tsx
<MapsComponent
  markerClusterClick={(args) => {
    console.log('Cluster clicked, count:', args.data.length);
  }}
>
```

### markerClusterMouseMove
- **Type**: `EmitType<IMarkerClusterMoveEventArgs>`
- **Description**: Triggers when hovering over a marker cluster

```tsx
<MapsComponent
  markerClusterMouseMove={(args) => {
    console.log('Hovering cluster');
  }}
>
```

### markerClusterRendering
- **Type**: `EmitType<IMarkerClusterRenderingEventArgs>`
- **Description**: Triggers before the marker cluster gets rendered

```tsx
<MapsComponent
  markerClusterRendering={(args) => {
    // Customize cluster appearance
    args.fill = '#FF0000';
  }}
>
```

### markerDragEnd
- **Type**: `EmitType<IMarkerDragEventArgs>`
- **Description**: Triggers when marker stops dragging

```tsx
<MapsComponent
  markerDragEnd={(args) => {
    console.log('Marker dropped at:', args.latitude, args.longitude);
  }}
>
```

### markerDragStart
- **Type**: `EmitType<IMarkerDragEventArgs>`
- **Description**: Triggers when marker starts dragging

```tsx
<MapsComponent
  markerDragStart={(args) => {
    console.log('Started dragging marker:', args.data);
  }}
>
```

### markerMouseMove
- **Type**: `EmitType<IMarkerMoveEventArgs>`
- **Description**: Triggers when moving mouse over marker element

```tsx
<MapsComponent
  markerMouseMove={(args) => {
    console.log('Hovering marker:', args.data);
  }}
>
```

### markerRendering
- **Type**: `EmitType<IMarkerRenderingEventArgs>`
- **Description**: Triggers before the marker gets rendered

```tsx
<MapsComponent
  markerRendering={(args) => {
    // Customize marker before rendering
    if (args.data.type === 'capital') {
      args.fill = '#FFD700';
      args.height = 30;
      args.width = 30;
    }
  }}
>
```

### mouseMove
- **Type**: `EmitType<IMouseMoveEventArgs>`
- **Description**: Triggers when mouse pointer moves over the map

```tsx
<MapsComponent
  mouseMove={(args) => {
    console.log('Mouse at:', args.x, args.y);
  }}
>
```

### onclick
- **Type**: `EmitType<IMouseEventArgs>`
- **Description**: Triggers when clicking on an element (alias for click)

### pan
- **Type**: `EmitType<IMapPanEventArgs>`
- **Description**: Triggers before performing the panning operation

```tsx
<MapsComponent
  pan={(args) => {
    console.log('Panning to:', args.latitude, args.longitude);
    // Prevent panning
    args.cancel = true;
  }}
>
```

### panComplete
- **Type**: `EmitType<IMapPanEventArgs>`
- **Description**: Triggers after performing the panning action

```tsx
<MapsComponent
  panComplete={(args) => {
    console.log('Pan completed');
  }}
>
```

### resize
- **Type**: `EmitType<IResizeEventArgs>`
- **Description**: Triggers when the maps is resized

```tsx
<MapsComponent
  resize={(args) => {
    console.log('Resized to:', args.currentSize);
  }}
>
```

### rightClick
- **Type**: `EmitType<IMouseEventArgs>`
- **Description**: Triggers when performing right click operation

```tsx
<MapsComponent
  rightClick={(args) => {
    console.log('Right clicked at:', args.x, args.y);
    // Show custom context menu
  }}
>
```

### shapeHighlight
- **Type**: `EmitType<IShapeSelectedEventArgs>`
- **Description**: Triggers before the shape gets highlighted

```tsx
<MapsComponent
  shapeHighlight={(args) => {
    console.log('Highlighting shape:', args.data);
  }}
>
```

### shapeRendering
- **Type**: `EmitType<IShapeRenderingEventArgs>`
- **Description**: Triggers before the shape gets rendered

```tsx
<MapsComponent
  shapeRendering={(args) => {
    // Customize shape before rendering
    if (args.data.population > 100000000) {
      args.fill = '#FF0000';
    }
  }}
>
```

### shapeSelected
- **Type**: `EmitType<IShapeSelectedEventArgs>`
- **Description**: Triggers when a shape is selected

```tsx
<MapsComponent
  shapeSelected={(args) => {
    console.log('Shape selected:', args.data);
    alert(`Selected: ${args.data.name}`);
  }}
>
```

### tooltipRender
- **Type**: `EmitType<ITooltipRenderEventArgs>`
- **Description**: Triggers before the tooltip gets rendered

```tsx
<MapsComponent
  tooltipRender={(args) => {
    // Customize tooltip content
    args.content = `<div style="padding: 10px;">
      <b>${args.data.name}</b><br/>
      Population: ${args.data.population}
    </div>`;
  }}
>
```

### tooltipRenderComplete
- **Type**: `EmitType<ITooltipRenderCompleteEventArgs>`
- **Description**: Triggers after the tooltip gets rendered

```tsx
<MapsComponent
  tooltipRenderComplete={(args) => {
    console.log('Tooltip rendered');
  }}
>
```

### zoom
- **Type**: `EmitType<IMapZoomEventArgs>`
- **Description**: Triggers before zoom operations (zoom in/out)

```tsx
<MapsComponent
  zoom={(args) => {
    console.log('Zooming to factor:', args.currentZoomFactor);
    // Prevent zoom
    args.cancel = true;
  }}
>
```

### zoomComplete
- **Type**: `EmitType<IMapPanEventArgs>`
- **Description**: Triggers after the zooming operation is completed

```tsx
<MapsComponent
  zoomComplete={(args) => {
    console.log('Zoom completed');
  }}
>
```

---

## Layer Settings

Configuration for individual map layers:

```tsx
<LayerDirective
  // Data
  shapeData={geoJsonData}
  dataSource={customData}
  shapeDataPath="Country"
  shapePropertyPath="name"
  
  // Type
  type="Layer"  // or "SubLayer"
  
  // Visual Settings
  shapeSettings={{
    fill: '#E5E5E5',
    colorValuePath: 'Population',
    colorMapping: [...]
  }}
  
  // Features
  markerSettings={[...]}
  bubbleSettings={[...]}
  dataLabelSettings={{...}}
  tooltipSettings={{...}}
  navigationLineSettings={[...]}
/>
```

---

## Marker Settings

```tsx
<MarkerDirective
  visible={true}
  dataSource={[
    { latitude: 40.7128, longitude: -74.0060, name: 'NYC' }
  ]}
  
  // Shape
  shape="Circle"  // Circle, Diamond, Star, Triangle, etc.
  height={20}
  width={20}
  
  // Appearance
  fill="#FF0000"
  opacity={0.8}
  border={{ color: '#000000', width: 1 }}
  
  // Template
  template={(props) => <div>{props.name}</div>}
  
  // Clustering
  clusterSettings={{
    allowClustering: true,
    shape: 'Circle',
    width: 30,
    height: 30,
    fill: '#4CAF50'
  }}
  
  // Tooltip
  tooltipSettings={{
    visible: true,
    valuePath: 'name',
    format: '${name}'
  }}
/>
```

---

## Bubble Settings

```tsx
<BubbleDirective
  visible={true}
  dataSource={data}
  
  // Size
  valuePath="population"
  minRadius={10}
  maxRadius={50}
  
  // Appearance
  fill="#FF6347"
  opacity={0.6}
  border={{ color: '#FF0000', width: 1 }}
  
  // Color Mapping
  colorValuePath="population"
  colorMapping={[
    { from: 0, to: 100000, color: '#C3E6CB' },
    { from: 100000, to: 1000000, color: '#6AB187' }
  ]}
  
  // Animation
  animationDuration={1000}
  animationDelay={0}
  
  // Tooltip
  tooltipSettings={{
    visible: true,
    valuePath: 'name'
  }}
/>
```

---

## Data Label Settings

```tsx
dataLabelSettings={{
  visible: true,
  labelPath: 'name',
  
  // Smart Label
  smartLabelMode: 'Trim',  // Trim, Hide, None
  intersectionAction: 'Hide',
  
  // Style
  textStyle: {
    size: '12px',
    color: '#000000',
    fontFamily: 'Arial',
    fontWeight: 'Normal',
    fontStyle: 'Normal',
    opacity: 1
  },
  
  // Border
  border: {
    color: '#FFFFFF',
    width: 1
  },
  
  // Template
  template: (props) => <div>{props.name}</div>
}}
```

---

## Legend Settings

```tsx
legendSettings={{
  visible: true,
  
  // Position
  position: 'Bottom',  // Top, Bottom, Left, Right
  alignment: 'Center',  // Near, Center, Far
  
  // Mode
  mode: 'Default',  // Default, Interactive
  
  // Appearance
  height: '50px',
  width: '200px',
  background: '#FFFFFF',
  border: { color: '#000000', width: 1 },
  
  // Text Style
  textStyle: {
    size: '12px',
    color: '#000000',
    fontFamily: 'Arial'
  },
  
  // Shape
  shape: 'Circle',  // Circle, Rectangle, Triangle, etc.
  shapeHeight: 15,
  shapeWidth: 15,
  shapePadding: 5,
  
  // Template
  legendTemplate: (props) => <div>{props.text}</div>
}}
```

---

## Zoom Settings

```tsx
zoomSettings={{
  enable: true,
  enablePanning: true,
  enableSelectionZooming: false,
  
  // Zoom Factor
  zoomFactor: 1,
  maxZoom: 10,
  minZoom: 1,
  
  // Zoom On Area
  zoomOnClick: false,
  
  // Mouse Wheel
  mouseWheelZoom: true,
  doubleClickZoom: false,
  pinchZooming: true,
  
  // Toolbar
  toolbars: ['Zoom', 'ZoomIn', 'ZoomOut', 'Pan', 'Reset'],
  
  // Toolbar Orientation
  horizontalAlignment: 'Near',  // Near, Center, Far
  verticalAlignment: 'Near',  // Near, Center, Far
  
  // Toolbar Style
  toolbarSettings: {
    backgroundColor: '#FFFFFF',
    borderColor: '#000000',
    borderWidth: 1,
    buttonSettings: {
      fill: '#FFFFFF',
      color: '#000000',
      padding: 10
    }
  }
}}
```

---

## Tooltip Settings

```tsx
tooltipSettings={{
  visible: true,
  
  // Content
  valuePath: 'name',
  format: '${name}: ${population}',
  
  // Template
  template: (props) => (
    <div>
      <b>{props.name}</b><br/>
      Population: {props.population}
    </div>
  ),
  
  // Style
  fill: '#FFFFFF',
  textStyle: {
    size: '12px',
    color: '#000000',
    fontFamily: 'Arial'
  },
  border: {
    color: '#000000',
    width: 1
  }
}}
```

---

## Quick Reference Examples

### Complete Feature-Rich Map

```tsx
import * as React from 'react';
import {
  MapsComponent,
  LayersDirective,
  LayerDirective,
  MarkersDirective,
  MarkerDirective,
  BubblesDirective,
  BubbleDirective,
  Inject,
  Legend,
  MapsTooltip,
  Zoom,
  DataLabel,
  Marker,
  Bubble,
  Selection,
  Highlight,
  Print,
  ImageExport,
  PdfExport
} from '@syncfusion/ej2-react-maps';
import { world_map } from './world-map';

function ComprehensiveMap() {
  const mapsRef = React.useRef(null);
  
  const countryData = [
    { name: 'United States', population: 331000000, gdp: 21427700 },
    { name: 'China', population: 1439000000, gdp: 14342900 },
    { name: 'India', population: 1380000000, gdp: 2875142 }
  ];
  
  const cityMarkers = [
    { latitude: 40.7128, longitude: -74.0060, city: 'New York' },
    { latitude: 51.5074, longitude: -0.1278, city: 'London' },
    { latitude: 35.6762, longitude: 139.6503, city: 'Tokyo' }
  ];
  
  const exportToPNG = () => {
    mapsRef.current.export('PNG', 'world-map');
  };
  
  const exportToPDF = () => {
    mapsRef.current.export('PDF', 'world-map', 0);
  };
  
  const printMap = () => {
    mapsRef.current.print();
  };
  
  return (
    <div>
      <div style={{ marginBottom: '10px' }}>
        <button onClick={exportToPNG}>Export PNG</button>
        <button onClick={exportToPDF}>Export PDF</button>
        <button onClick={printMap}>Print</button>
      </div>
      
      <MapsComponent
        ref={mapsRef}
        id="maps"
        height="600px"
        
        // Export & Print
        allowImageExport={true}
        allowPdfExport={true}
        allowPrint={true}
        
        // Title
        titleSettings={{
          text: 'World Population & GDP Map',
          textStyle: { size: '18px', fontWeight: 'Bold' }
        }}
        
        // Zoom
        zoomSettings={{
          enable: true,
          enablePanning: true,
          toolbars: ['Zoom', 'ZoomIn', 'ZoomOut', 'Pan', 'Reset']
        }}
        
        // Legend
        legendSettings={{
          visible: true,
          position: 'Bottom',
          alignment: 'Center'
        }}
        
        // Events
        load={(args) => console.log('Loading')}
        loaded={(args) => console.log('Loaded')}
        shapeSelected={(args) => console.log('Selected:', args.data)}
        markerClick={(args) => alert(`Clicked: ${args.data.city}`)}
      >
        <Inject services={[
          Legend,
          MapsTooltip,
          Zoom,
          DataLabel,
          Marker,
          Bubble,
          Selection,
          Highlight,
          Print,
          ImageExport,
          PdfExport
        ]} />
        
        <LayersDirective>
          <LayerDirective
            shapeData={world_map}
            dataSource={countryData}
            shapeDataPath='name'
            shapePropertyPath='name'
            
            // Shape Settings
            shapeSettings={{
              fill: '#E5E5E5',
              colorValuePath: 'population',
              colorMapping: [
                { from: 0, to: 100000000, color: '#C3E6CB', label: '< 100M' },
                { from: 100000000, to: 500000000, color: '#6AB187', label: '100M-500M' },
                { from: 500000000, to: 2000000000, color: '#2F7C4F', label: '> 500M' }
              ]
            }}
            
            // Tooltip
            tooltipSettings={{
              visible: true,
              valuePath: 'name',
              format: '${name}<br/>Population: ${population}<br/>GDP: $${gdp}M'
            }}
            
            // Data Labels
            dataLabelSettings={{
              visible: true,
              labelPath: 'name',
              smartLabelMode: 'Trim',
              textStyle: { size: '10px' }
            }}
            
            // Selection & Highlight
            selectionSettings={{
              enable: true,
              fill: '#FF6347',
              opacity: 0.8
            }}
            highlightSettings={{
              enable: true,
              fill: '#FFA500',
              opacity: 0.5
            }}
          >
            {/* Markers */}
            <MarkersDirective>
              <MarkerDirective
                visible={true}
                dataSource={cityMarkers}
                shape='Star'
                height={20}
                width={20}
                fill='#FFD700'
                tooltipSettings={{
                  visible: true,
                  valuePath: 'city'
                }}
              />
            </MarkersDirective>
            
            {/* Bubbles */}
            <BubblesDirective>
              <BubbleDirective
                visible={true}
                dataSource={countryData}
                valuePath='gdp'
                minRadius={10}
                maxRadius={40}
                fill='#2196F3'
                opacity={0.5}
                tooltipSettings={{
                  visible: true,
                  format: '${name}<br/>GDP: $${gdp}M'
                }}
              />
            </BubblesDirective>
          </LayerDirective>
        </LayersDirective>
      </MapsComponent>
    </div>
  );
}

export default ComprehensiveMap;
```

---

## Related Documentation

- [Getting Started](./getting-started.md)
- [Markers](./markers.md)
- [Data Visualization](./data-visualization.md)
- [User Interactions](./user-interactions.md)
- [Legend](./legend.md)
- [Color Mapping](./color-mapping.md)
- [Advanced Features](./advanced-features.md)

---

## External Resources

- [Official Syncfusion Maps API Documentation](https://ej2.syncfusion.com/react/documentation/api/maps/index-default)
- [Syncfusion Maps Component Page](https://www.syncfusion.com/react-components/react-maps)
- [Live Demos](https://ej2.syncfusion.com/react/demos/#/material/maps/default)

````