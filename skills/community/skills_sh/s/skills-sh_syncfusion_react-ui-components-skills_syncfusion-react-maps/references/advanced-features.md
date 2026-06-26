# Advanced Features in React Maps

## Table of Contents
- [Overview](#overview)
- [Internationalization](#internationalization)
- [Localization](#localization)
- [Accessibility](#accessibility)
- [State Persistence](#state-persistence)
- [Print and Export](#print-and-export)
- [Event Handling](#event-handling)
- [Methods and API](#methods-and-api)
- [Performance Optimization](#performance-optimization)

## Overview

Advanced features for enterprise-grade Maps applications: i18n, accessibility, state management, export, and performance.

## Internationalization

### RTL Support

```tsx
<MapsComponent enableRtl={true}>
  <LayersDirective>
    <LayerDirective shapeData={world_map} />
  </LayersDirective>
</MapsComponent>
```

## Localization

### Load Culture

```tsx
import { L10n, setCulture } from '@syncfusion/ej2-base';

// Set culture
setCulture('de');

// Load German locale
L10n.load({
  'de': {
    'maps': {
      'ZoomIn': 'Hineinzoomen',
      'ZoomOut': 'Rauszoomen',
      'Reset': 'Zurücksetzen',
      'Pan': 'Schwenken',
      'Zoom': 'Zoomen'
    }
  }
});

function LocalizedMap() {
  return (
    <MapsComponent locale='de'>
      <Inject services={[Zoom]} />
      <LayersDirective>
        <LayerDirective shapeData={world_map} />
      </LayersDirective>
    </MapsComponent>
  );
}
```

### Multiple Languages

```tsx
L10n.load({
  'fr': {
    'maps': {
      'ZoomIn': 'Agrandir',
      'ZoomOut': 'Dézoomer',
      'Reset': 'Réinitialiser'
    }
  },
  'es': {
    'maps': {
      'ZoomIn': 'Acercar',
      'ZoomOut': 'Alejar',
      'Reset': 'Restablecer'
    }
  }
});
```

## Accessibility

### WCAG Compliance

```tsx
<MapsComponent
  titleSettings={{
    text: 'World Map',
    description: 'Interactive world map showing country data'
  }}
>
  <LayersDirective>
    <LayerDirective
      shapeData={world_map}
      tooltipSettings={{
        visible: true,
        format: '${name}: ${value}'  // Screen reader friendly
      }}
    />
  </LayersDirective>
</MapsComponent>
```

**Features:**
- Keyboard navigation (arrow keys, +/- for zoom)
- Screen reader support
- High contrast mode
- Focus indicators

### Keyboard Shortcuts

- **Arrow keys**: Pan map
- **+ / =**: Zoom in
- **- / _**: Zoom out
- **R**: Reset zoom
- **Tab**: Navigate focusable elements

## State Persistence

### Enable Persistence

```tsx
<MapsComponent
  id='maps'
  enablePersistence={true}  // Saves zoom, pan state to localStorage
>
```

### Custom State Management

```tsx
function StatefulMap() {
  const [mapState, setMapState] = React.useState({
    zoomFactor: 1,
    centerPosition: { latitude: 0, longitude: 0 }
  });

  const handleZoomChange = (args) => {
    setMapState({
      zoomFactor: args.currentZoomFactor,
      centerPosition: args.centerPosition
    });
  };

  return (
    <MapsComponent
      zoomSettings={{
        enable: true,
        zoomFactor: mapState.zoomFactor
      }}
      centerPosition={mapState.centerPosition}
      zoom={handleZoomChange}
    >
      <Inject services={[Zoom]} />
      <LayersDirective>
        <LayerDirective shapeData={world_map} />
      </LayersDirective>
    </MapsComponent>
  );
}
```

## Print and Export

### Print Map

```tsx
import { MapsComponent, Print, ImageExport, PdfExport } from '@syncfusion/ej2-react-maps';

function PrintableMap() {
  const mapsRef = React.useRef(null);

  const printMap = () => {
    mapsRef.current.print();
  };

  return (
    <>
      <button onClick={printMap}>Print Map</button>
      <MapsComponent ref={mapsRef} allowPrint={true}>
        <Inject services={[Print]} />
        <LayersDirective>
          <LayerDirective shapeData={world_map} />
        </LayersDirective>
      </MapsComponent>
    </>
  );
}
```

### Export as Image

```tsx
function ExportableMap() {
  const mapsRef = React.useRef(null);

  const exportToPNG = () => {
    mapsRef.current.export('PNG', 'world-map');
  };

  const exportToJPEG = () => {
    mapsRef.current.export('JPEG', 'world-map');
  };

  const exportToSVG = () => {
    mapsRef.current.export('SVG', 'world-map');
  };

  return (
    <>
      <button onClick={exportToPNG}>Export PNG</button>
      <button onClick={exportToJPEG}>Export JPEG</button>
      <button onClick={exportToSVG}>Export SVG</button>
      
      <MapsComponent ref={mapsRef} allowImageExport={true}>
        <Inject services={[ImageExport]} />
        <LayersDirective>
          <LayerDirective shapeData={world_map} />
        </LayersDirective>
      </MapsComponent>
    </>
  );
}
```

### Export as PDF

```tsx
function PDFExportMap() {
  const mapsRef = React.useRef(null);

  const exportToPDF = () => {
    mapsRef.current.export('PDF', 'world-map', 0);  // 0 = Portrait, 1 = Landscape
  };

  return (
    <>
      <button onClick={exportToPDF}>Export PDF</button>
      
      <MapsComponent ref={mapsRef} allowPdfExport={true}>
        <Inject services={[PdfExport]} />
        <LayersDirective>
          <LayerDirective shapeData={world_map} />
        </LayersDirective>
      </MapsComponent>
    </>
  );
}
```

### Export Options (PDF Orientation & More)

Maps can export to PNG, JPEG, SVG, or PDF with optional orientation.

```tsx
mapsRef.current.export("PDF", "world-map", "Landscape");
```

## Event Handling

### Load Event

```tsx
<MapsComponent
  load={(args) => {
    console.log('Map is loading');
  }}
  loaded={(args) => {
    console.log('Map loaded successfully');
  }}
>
```

### Click Events

```tsx
<MapsComponent
  click={(args) => {
    console.log('Map clicked at:', args.x, args.y);
  }}
  shapeSelected={(args) => {
    console.log('Shape selected:', args.data);
  }}
>
```

### Zoom Events

```tsx
<MapsComponent
  zoom={(args) => {
    console.log('Zoom factor:', args.currentZoomFactor);
  }}
  pan={(args) => {
    console.log('Pan to:', args.latitude, args.longitude);
  }}
>
```

### Animation Events

```tsx
<MapsComponent
  animationComplete={(args) => {
    console.log('Animation completed');
  }}
>
```

## Methods and API

Access component methods using a ref to the MapsComponent. For complete API documentation, [API Documentation](https://ej2.syncfusion.com/react/documentation/api/maps/overview).

### Refresh Map

```tsx
function RefreshableMap() {
  const mapsRef = React.useRef(null);

  const refreshMap = () => {
    mapsRef.current.refresh();
  };

  return (
    <>
      <button onClick={refreshMap}>Refresh</button>
      <MapsComponent ref={mapsRef}>
        <LayersDirective>
          <LayerDirective shapeData={world_map} />
        </LayersDirective>
      </MapsComponent>
    </>
  );
}
```

### Zoom Methods

```tsx
function ZoomControlMap() {
  const mapsRef = React.useRef(null);

  const zoomByPosition = () => {
    // Zoom to specific location
    mapsRef.current.zoomByPosition(
      { latitude: 40.7128, longitude: -74.0060 },
      2  // Zoom factor
    );
  };

  const zoomToCoordinates = () => {
    // Zoom to bounds
    mapsRef.current.zoomToCoordinates(
      25.0,   // minLatitude
      -125.0, // minLongitude
      49.0,   // maxLatitude
      -66.0   // maxLongitude
    );
  };

  return (
    <>
      <button onClick={zoomByPosition}>Zoom to NYC</button>
      <button onClick={zoomToCoordinates}>Zoom to USA</button>
      
      <MapsComponent ref={mapsRef}>
        <Inject services={[Zoom]} />
        <LayersDirective>
          <LayerDirective shapeData={world_map} />
        </LayersDirective>
      </MapsComponent>
    </>
  );
}
```

### Pan To Location

```tsx
function PanControlMap() {
  const mapsRef = React.useRef(null);

  const panByDirection = (direction) => {
    // Pan in specific direction
    mapsRef.current.panByDirection(direction);
  };

  return (
    <>
      <button onClick={() => panByDirection('Left')}>Pan Left</button>
      <button onClick={() => panByDirection('Right')}>Pan Right</button>
      <button onClick={() => panByDirection('Top')}>Pan Up</button>
      <button onClick={() => panByDirection('Bottom')}>Pan Down</button>
      
      <MapsComponent ref={mapsRef}>
        <Inject services={[Zoom]} />
        <LayersDirective>
          <LayerDirective shapeData={world_map} />
        </LayersDirective>
      </MapsComponent>
    </>
  );
}
```

### Dynamic Layer Management

```tsx
function DynamicLayerMap() {
  const mapsRef = React.useRef(null);

  const addLayer = () => {
    // Add a new sublayer dynamically
    mapsRef.current.addLayer({
      shapeData: stateMap,
      type: 'SubLayer',
      shapeSettings: {
        fill: '#FF6347',
        opacity: 0.6
      }
    });
  };

  const removeLayer = (index) => {
    // Remove layer by index
    mapsRef.current.removeLayer(index);
  };

  return (
    <>
      <button onClick={addLayer}>Add Layer</button>
      <button onClick={() => removeLayer(1)}>Remove Second Layer</button>
      
      <MapsComponent ref={mapsRef}>
        <LayersDirective>
          <LayerDirective shapeData={world_map} />
        </LayersDirective>
      </MapsComponent>
    </>
  );
}
```

### Dynamic Marker Management

```tsx
function DynamicMarkerMap() {
  const mapsRef = React.useRef(null);

  const addMarkers = () => {
    // Add markers to layer 0
    mapsRef.current.addMarker(0, [
      {
        visible: true,
        dataSource: [
          { latitude: 40.7128, longitude: -74.0060, name: 'New York' },
          { latitude: 51.5074, longitude: -0.1278, name: 'London' }
        ],
        height: 20,
        width: 20,
        shape: 'Circle',
        fill: '#FF0000'
      }
    ]);
  };

  return (
    <>
      <button onClick={addMarkers}>Add Markers</button>
      
      <MapsComponent ref={mapsRef}>
        <Inject services={[Marker]} />
        <LayersDirective>
          <LayerDirective shapeData={world_map} />
        </LayersDirective>
      </MapsComponent>
    </>
  );
}
```

### Shape Selection

```tsx
function SelectableMap() {
  const mapsRef = React.useRef(null);

  const selectShape = (shapeName, select = true) => {
    // Select or deselect a shape
    mapsRef.current.shapeSelection(
      0,              // Layer index
      'name',         // Property name
      shapeName,      // Shape name
      select          // true to select, false to deselect
    );
  };

  return (
    <>
      <button onClick={() => selectShape('United States', true)}>
        Select USA
      </button>
      <button onClick={() => selectShape('United States', false)}>
        Deselect USA
      </button>
      
      <MapsComponent ref={mapsRef}>
        <Inject services={[Selection]} />
        <LayersDirective>
          <LayerDirective
            shapeData={world_map}
            selectionSettings={{
              enable: true,
              fill: '#FF6347'
            }}
          />
        </LayersDirective>
      </MapsComponent>
    </>
  );
}
```

### Programmatic Shape Selection

Shapes can be selected directly via API, without user interaction.

```tsx
mapsRef.current.shapeSelection(0, "name", "United States", true);
```

### Coordinate Conversion

```tsx
function CoordinateConversionMap() {
  const mapsRef = React.useRef(null);

  const getLocationFromPixel = (pageX, pageY) => {
    // Convert pixel coordinates to lat/long
    const latLong = mapsRef.current.pointToLatLong(pageX, pageY);
    console.log('Latitude:', latLong.latitude);
    console.log('Longitude:', latLong.longitude);
    return latLong;
  };

  const getPixelFromLocation = (layerIndex, lat, long) => {
    // Convert lat/long to pixel coordinates (for shape maps)
    const geoPosition = mapsRef.current.getGeoLocation(layerIndex, lat, long);
    return geoPosition;
  };

  const handleMapClick = (args) => {
    const location = getLocationFromPixel(args.x, args.y);
    alert(`Clicked at: ${location.latitude.toFixed(2)}, ${location.longitude.toFixed(2)}`);
  };

  return (
    <MapsComponent ref={mapsRef} click={handleMapClick}>
      <LayersDirective>
        <LayerDirective shapeData={world_map} />
      </LayersDirective>
    </MapsComponent>
  );
}
```

#### Tile Geo‑location Conversion

Converts pixel positions from tile-based map providers (OSM/Bing/Azure) into latitude/longitude.
Useful for drawing overlays or capturing pointer coordinates.

```tsx
const loc = mapsRef.current.getTileGeoLocation(pageX, pageY);
```

#### Projection Coordinate Conversion

Convert latitude/longitude to pixel points

```tsx
const pt = mapsRef.current.latLongToPoint(40.7128, -74.006)
```

### Bing Maps Integration

```tsx
function BingMapsSetup() {
  const mapsRef = React.useRef(null);

  React.useEffect(() => {
    const setupBingMaps = async () => {
      const bingUrl = await mapsRef.current.getBingUrlTemplate(
        'Add your URL link'
      );
      console.log('Bing Maps URL Template:', bingUrl);
    };

    setupBingMaps();
  }, []);

  return (
    <MapsComponent ref={mapsRef}>
      <LayersDirective>
        <LayerDirective
          urlTemplate="Add your URL link"
        />
      </LayersDirective>
    </MapsComponent>
  );
}
```

**Available Methods:**
- `addLayer(layer)` - Add layer dynamically
- `addMarker(layerIndex, markerCollection)` - Add markers dynamically
- `destroy()` - Destroy the component
- `export(type, fileName, orientation, allowDownload)` - Export map
- `getBingUrlTemplate(url)` - Get Bing Maps URL
- `getGeoLocation(layerIndex, x, y)` - Convert pixels to coordinates (shape maps)
- `getTileGeoLocation(x, y)` - Convert pixels to coordinates (tile maps)
- `panByDirection(direction, mouseLocation)` - Pan in direction
- `pointToLatLong(pageX, pageY)` - Convert pixel to lat/long
- `print(id)` - Print map
- `removeLayer(index)` - Remove layer
- `shapeSelection(layerIndex, propertyName, name, enable)` - Select shape
- `zoomByPosition(centerPosition, zoomFactor)` - Zoom to position
- `zoomToCoordinates(minLat, minLong, maxLat, maxLong)` - Zoom to bounds

For detailed method signatures and parameters, refer to [API Documentation](https://ej2.syncfusion.com/react/documentation/api/maps/overview).

## Performance Optimization

### Lazy Loading

```tsx
const world_map = React.lazy(() => import('./data/world-map.json'));

function OptimizedMap() {
  return (
    <React.Suspense fallback={<div>Loading map...</div>}>
      <MapsComponent>
        <LayersDirective>
          <LayerDirective shapeData={world_map} />
        </LayersDirective>
      </MapsComponent>
    </React.Suspense>
  );
}
```

### Simplify GeoJSON

**Before optimization:**
```json
// Large GeoJSON with detailed coordinates
{
  "type": "Feature",
  "geometry": {
    "type": "Polygon",
    "coordinates": [/* 10000+ coordinate pairs */]
  }
}
```

**After simplification (use mapshaper or turf.js):**
```json
// Reduced GeoJSON
{
  "type": "Feature",
  "geometry": {
    "type": "Polygon",
    "coordinates": [/* 500 coordinate pairs */]
  }
}
```

### Conditional Rendering

```tsx
function ConditionalMap() {
  const [showMarkers, setShowMarkers] = React.useState(false);

  return (
    <>
      <input
        type="checkbox"
        checked={showMarkers}
        onChange={(e) => setShowMarkers(e.target.checked)}
      />
      
      <MapsComponent>
        <Inject services={showMarkers ? [Marker] : []} />
        <LayersDirective>
          <LayerDirective
            shapeData={world_map}
            markerSettings={showMarkers ? [{
              visible: true,
              dataSource: markerData
            }] : []}
          />
        </LayersDirective>
      </MapsComponent>
    </>
  );
}
```

### Memoization

```tsx
const MemoizedMap = React.memo(function Map({ shapeData, dataSource }) {
  return (
    <MapsComponent>
      <LayersDirective>
        <LayerDirective
          shapeData={shapeData}
          dataSource={dataSource}
        />
      </LayersDirective>
    </MapsComponent>
  );
});
```

## Troubleshooting

### Issue: Slow rendering with large GeoJSON

**Solutions:**
1. Simplify GeoJSON geometries
2. Reduce coordinate precision
3. Use layer visibility to hide unnecessary layers

### Issue: Export not working

**Solution:** Inject required service
```tsx
<MapsComponent allowPdfExport={true}>
  <Inject services={[PdfExport]} />
</MapsComponent>
```

### Issue: State persistence not saving

**Solution:** Provide unique `id` attribute
```tsx
<MapsComponent id='unique-map-id' enablePersistence={true}>
```
