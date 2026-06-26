# User Interactions in React Maps

## Table of Contents
- [Overview](#overview)
- [Zooming](#zooming)
- [Panning](#panning)
- [Tooltips](#tooltips)
- [Selection](#selection)
- [Highlighting](#highlighting)
- [Events](#events)
- [Common Patterns](#common-patterns)
- [Troubleshooting](#troubleshooting)

## Overview

User interactions make maps explorable and informative through zooming, panning, tooltips, selection, and highlighting.

## Zooming

### Enable Zooming

```tsx
import {
  MapsComponent,
  LayersDirective,
  LayerDirective,
  Inject,
  Zoom
} from '@syncfusion/ej2-react-maps';

function ZoomableMap() {
  return (
    <MapsComponent
      zoomSettings={{
        enable: true,
        zoomFactor: 1,           // Initial zoom level
        maxZoom: 20,             // Maximum zoom
        minZoom: 1               // Minimum zoom
      }}
    >
      <Inject services={[Zoom]} />
      <LayersDirective>
        <LayerDirective shapeData={world_map} />
      </LayersDirective>
    </MapsComponent>
  );
}
```

### Zoom Methods

```tsx
zoomSettings={{
  enable: true,
  enableZoomingToolBar: true,   // Show zoom toolbar
  enableMouseWheelZoom: true,   // Mouse wheel zoom
  enableDoubleClickZoom: true,  // Double-click to zoom
  enablePinchZoom: true,        // Touch pinch zoom
  zoomFactor: 2,                // Initial zoom level
  shouldZoomInitially: true     // Apply zoomFactor on load
}}
```

### Zoom Toolbar

Adds +/- buttons and reset:

```tsx
<MapsComponent
  zoomSettings={{
    enable: true,
    toolbarSettings: {
      buttonSettings: {
        toolbarItems: ['Zoom', 'ZoomIn', 'ZoomOut', 'Pan', 'Reset'],
        color: '#FFFFFF',
        highlightColor: '#FF6347',
        selectionColor: '#4CAF50',
        horizontalAlignment: 'Near',  // Near, Center, Far
        verticalAlignment: 'Near'      // Near, Center, Far
      }
    }
  }}
>
  <Inject services={[Zoom]} />
</MapsComponent>
```

### Zoom to Specific Region

```tsx
function ZoomToRegion() {
  const mapsRef = React.useRef(null);

  const zoomToUSA = () => {
    if (mapsRef.current) {
      mapsRef.current.zoomToCoordinates(
        25, // min latitude
        50, // max latitude
        -125, // min longitude
        -65   // max longitude
      );
    }
  };

  return (
    <>
      <button onClick={zoomToUSA}>Zoom to USA</button>
      <MapsComponent
        ref={mapsRef}
        zoomSettings={{ enable: true }}
      >
        <Inject services={[Zoom]} />
        <LayersDirective>
          <LayerDirective shapeData={world_map} />
        </LayersDirective>
      </MapsComponent>
    </>
  );
}
```

### Shape Border Merging on Zoom

Borders automatically simplify at lower zoom levels and refine when zooming deeper.

```tsx
shapeSettings={{
    border: { width: 0.5, color: "#888" }
}}
```


## Panning

### Enable Panning

```tsx
<MapsComponent
  zoomSettings={{
    enable: true,
    enablePanning: true  // Allow dragging
  }}
>
  <Inject services={[Zoom]} />
</MapsComponent>
```

### Pan to Coordinates

```tsx
function PanToLocation() {
  const mapsRef = React.useRef(null);

  const panToLondon = () => {
    if (mapsRef.current) {
      mapsRef.current.panToCoordinate(51.5074, -0.1278);
    }
  };

  return (
    <>
      <button onClick={panToLondon}>Pan to London</button>
      <MapsComponent
        ref={mapsRef}
        zoomSettings={{
          enable: true,
          enablePanning: true,
          zoomFactor: 5
        }}
      >
        <Inject services={[Zoom]} />
        <LayersDirective>
          <LayerDirective shapeData={world_map} />
        </LayersDirective>
      </MapsComponent>
    </>
  );
}
```

## Tooltips

### Basic Tooltips

```tsx
import {
  MapsComponent,
  LayersDirective,
  LayerDirective,
  Inject,
  MapsTooltip
} from '@syncfusion/ej2-react-maps';

function TooltipMap() {
  return (
    <MapsComponent>
      <Inject services={[MapsTooltip]} />
      <LayersDirective>
        <LayerDirective
          shapeData={world_map}
          tooltipSettings={{
            visible: true,
            valuePath: 'name'  // Field from GeoJSON properties
          }}
        />
      </LayersDirective>
    </MapsComponent>
  );
}
```

### Custom Tooltip Format

```tsx
<LayerDirective
  shapeData={world_map}
  dataSource={countryData}
  shapeDataPath='name'
  shapePropertyPath='name'
  tooltipSettings={{
    visible: true,
    format: '${name}<br/>Population: ${population}<br/>Capital: ${capital}'
  }}
/>
```

### Tooltip Styling

```tsx
tooltipSettings={{
  visible: true,
  valuePath: 'name',
  fill: '#333333',
  textStyle: {
    color: '#FFFFFF',
    fontFamily: 'Arial',
    size: '14px',
    fontWeight: 'Bold'
  },
  border: {
    color: '#FF6347',
    width: 2
  }
}}
```

### Marker Tooltips

```tsx
<MarkersDirective>
  <MarkerDirective
    visible={true}
    dataSource={cityData}
    tooltipSettings={{
      visible: true,
      valuePath: 'city',
      format: '${city}<br/>Population: ${population}'
    }}
  />
</MarkersDirective>
```

### Bubble Tooltips

```tsx
<BubblesDirective>
  <BubbleDirective
    visible={true}
    dataSource={data}
    valuePath='gdp'
    tooltipSettings={{
      visible: true,
      format: '${country}<br/>GDP: $${gdp}B'
    }}
  />
</BubblesDirective>
```

### Advanced Tooltip Templates

Tooltips support fully customizable HTML/React templates for multi-line or styled content.

```tsx
tooltipSettings={{
   visible: true,
   template: (props) => (
      <div>
         <strong>{props.name}</strong><br/>
         Value: {props.value}
      </div>
   )
}}
```

## Selection

### Enable Selection

```tsx
import {
  MapsComponent,
  LayersDirective,
  LayerDirective,
  Inject,
  Selection
} from '@syncfusion/ej2-react-maps';

function SelectableMap() {
  return (
    <MapsComponent
      selectionSettings={{
        enable: true,
        fill: '#FF6347',
        opacity: 0.8,
        enableMultiSelect: false  // Allow single selection only
      }}
    >
      <Inject services={[Selection]} />
      <LayersDirective>
        <LayerDirective shapeData={world_map} />
      </LayersDirective>
    </MapsComponent>
  );
}
```

### Multi-Selection

```tsx
<MapsComponent
  selectionSettings={{
    enable: true,
    fill: '#4CAF50',
    enableMultiSelect: true,  // Allow multiple selections
    border: {
      color: '#2E7D32',
      width: 2
    }
  }}
>
  <Inject services={[Selection]} />
</MapsComponent>
```

### Get Selected Shapes

```tsx
function SelectionHandlerMap() {
  const handleShapeSelected = (event) => {
    console.log('Selected shape:', event.data);
    console.log('Shape properties:', event.shapeData);
  };

  return (
    <MapsComponent
      shapeSelected={handleShapeSelected}
      selectionSettings={{
        enable: true,
        fill: '#FFD700'
      }}
    >
      <Inject services={[Selection]} />
      <LayersDirective>
        <LayerDirective shapeData={world_map} />
      </LayersDirective>
    </MapsComponent>
  );
}
```

## Highlighting

### Enable Highlighting

```tsx
import {
  MapsComponent,
  LayersDirective,
  LayerDirective,
  Inject,
  Highlight
} from '@syncfusion/ej2-react-maps';

function HighlightMap() {
  return (
    <MapsComponent
      highlightSettings={{
        enable: true,
        fill: '#FF6347',
        opacity: 0.6,
        border: {
          color: '#8B0000',
          width: 2
        }
      }}
    >
      <Inject services={[Highlight]} />
      <LayersDirective>
        <LayerDirective shapeData={world_map} />
      </LayersDirective>
    </MapsComponent>
  );
}
```

### Highlight with Tooltips

```tsx
<MapsComponent
  highlightSettings={{
    enable: true,
    fill: '#FFD700',
    opacity: 0.7
  }}
>
  <Inject services={[Highlight, MapsTooltip]} />
  <LayersDirective>
    <LayerDirective
      shapeData={world_map}
      tooltipSettings={{
        visible: true,
        valuePath: 'name'
      }}
    />
  </LayersDirective>
</MapsComponent>
```

## Events

### Click Event

```tsx
function ClickEventMap() {
  const handleClick = (event) => {
    console.log('Clicked coordinates:', event.latitude, event.longitude);
    console.log('Clicked shape:', event.target);
  };

  return (
    <MapsComponent click={handleClick}>
      <LayersDirective>
        <LayerDirective shapeData={world_map} />
      </LayersDirective>
    </MapsComponent>
  );
}
```

### Shape Selected Event

```tsx
const handleShapeSelected = (event) => {
  alert(`Selected: ${event.shapeData.name}`);
};

<MapsComponent
  shapeSelected={handleShapeSelected}
  selectionSettings={{ enable: true }}
>
  <Inject services={[Selection]} />
</MapsComponent>
```

### Zoom Complete Event

```tsx
const handleZoomComplete = (event) => {
  console.log('Current zoom factor:', event.zoomFactor);
};

<MapsComponent
  zoomComplete={handleZoomComplete}
  zoomSettings={{ enable: true }}
>
  <Inject services={[Zoom]} />
</MapsComponent>
```

### Marker Click Event

```tsx
const handleMarkerClick = (event) => {
  alert(`Marker clicked: ${event.data.name}`);
};

<MapsComponent markerClick={handleMarkerClick}>
  <Inject services={[Marker]} />
</MapsComponent>
```

## Common Patterns

### Pattern 1: Explorer Map

Full interactivity:

```tsx
function ExplorerMap() {
  return (
    <MapsComponent
      zoomSettings={{
        enable: true,
        enablePanning: true,
        enableMouseWheelZoom: true,
        enableDoubleClickZoom: true,
        toolbarSettings: {
          buttonSettings: {
            toolbarItems: ['Zoom', 'ZoomIn', 'ZoomOut', 'Pan', 'Reset']
          }
        }
      }}
      highlightSettings={{
        enable: true,
        fill: '#FFD700',
        opacity: 0.6
      }}
    >
      <Inject services={[Zoom, Highlight, MapsTooltip]} />
      <LayersDirective>
        <LayerDirective
          shapeData={world_map}
          tooltipSettings={{
            visible: true,
            valuePath: 'name'
          }}
        />
      </LayersDirective>
    </MapsComponent>
  );
}
```

### Pattern 2: Interactive Dashboard

```tsx
function InteractiveDashboard() {
  const [selectedCountry, setSelectedCountry] = React.useState(null);

  const handleSelection = (event) => {
    setSelectedCountry(event.shapeData);
  };

  return (
    <div>
      <div style={{ padding: '10px', background: '#f0f0f0' }}>
        {selectedCountry ? (
          <div>
            <h3>{selectedCountry.name}</h3>
            <p>Population: {selectedCountry.population}</p>
          </div>
        ) : (
          <p>Click a country to see details</p>
        )}
      </div>
      
      <MapsComponent
        shapeSelected={handleSelection}
        selectionSettings={{
          enable: true,
          fill: '#4CAF50'
        }}
      >
        <Inject services={[Selection, MapsTooltip]} />
        <LayersDirective>
          <LayerDirective
            shapeData={world_map}
            dataSource={countryData}
            shapeDataPath='name'
            shapePropertyPath='name'
            tooltipSettings={{
              visible: true,
              format: '${name}'
            }}
          />
        </LayersDirective>
      </MapsComponent>
    </div>
  );
}
```

### Pattern 3: Drill-Down Map

```tsx
function DrillDownMap() {
  const [zoomLevel, setZoomLevel] = React.useState('world');

  const handleCountryClick = (event) => {
    if (event.shapeData.name === 'United States') {
      setZoomLevel('usa');
      // Load USA state data
    }
  };

  return (
    <MapsComponent click={handleCountryClick}>
      <Inject services={[Zoom]} />
      <LayersDirective>
        <LayerDirective
          shapeData={zoomLevel === 'world' ? world_map : usa_map}
        />
      </LayersDirective>
    </MapsComponent>
  );
}
```

## Troubleshooting

### Issue: Zoom not working

**Solutions:**
1. Inject `Zoom` service
2. Set `enable: true`
3. Ensure `zoomFactor` is set

```tsx
// ✅ Correct
<MapsComponent zoomSettings={{ enable: true }}>
  <Inject services={[Zoom]} />
</MapsComponent>
```

### Issue: Tooltips not appearing

**Solutions:**
1. Inject `MapsTooltip` service
2. Set `visible: true`
3. Verify `valuePath` or `format` is correct

```tsx
// ✅ Correct
<MapsComponent>
  <Inject services={[MapsTooltip]} />
  <LayerDirective
    tooltipSettings={{
      visible: true,
      valuePath: 'name'
    }}
  />
</MapsComponent>
```

### Issue: Selection not working

**Solutions:**
1. Inject `Selection` service
2. Enable in selectionSettings
3. Check if shapes are selectable (not markers by default)

```tsx
// ✅ Correct
<MapsComponent selectionSettings={{ enable: true }}>
  <Inject services={[Selection]} />
</MapsComponent>
```

### Issue: Pan not working after zoom

**Cause:** `enablePanning` not set

**Solution:**
```tsx
zoomSettings={{
  enable: true,
  enablePanning: true  // Must be explicitly enabled
}}
```
