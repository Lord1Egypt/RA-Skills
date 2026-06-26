# Markers in React Maps

## Table of Contents
- [Overview](#overview)
- [Adding Markers](#adding-markers)
- [Marker Data Source](#marker-data-source)
- [Marker Shapes](#marker-shapes)
- [Customizing Markers](#customizing-markers)
- [Marker Templates](#marker-templates)
- [Dynamic Markers](#dynamic-markers)
- [Marker Clustering](#marker-clustering)
- [Interactive Markers](#interactive-markers)
- [Multiple Marker Sets](#multiple-marker-sets)
- [Common Use Cases](#common-use-cases)
- [Troubleshooting](#troubleshooting)

## Overview

Markers are visual indicators that pinpoint specific locations on maps. They're perfect for highlighting points of interest, displaying store locations, showing event venues, or marking any geographical position.

**Key Features:**
- Multiple marker shapes (circle, diamond, star, triangle, etc.)
- Custom templates with HTML/React components
- Tooltips on hover
- Click events for interactivity
- Clustering for dense marker groups
- Animation effects

## Adding Markers

### Basic Marker Setup

```tsx
import { 
  MapsComponent, 
  LayersDirective, 
  LayerDirective,
  MarkersDirective,
  MarkerDirective,
  Inject,
  Marker
} from '@syncfusion/ej2-react-maps';

function App() {
  return (
    <MapsComponent>
      <Inject services={[Marker]} />
      <LayersDirective>
        <LayerDirective shapeData={world_map}>
          <MarkersDirective>
            <MarkerDirective
              visible={true}
              dataSource={[
                { latitude: 40.7128, longitude: -74.0060, city: 'New York' },
                { latitude: 51.5074, longitude: -0.1278, city: 'London' },
                { latitude: 35.6762, longitude: 139.6503, city: 'Tokyo' }
              ]}
              height={20}
              width={20}
            />
          </MarkersDirective>
        </LayerDirective>
      </LayersDirective>
    </MapsComponent>
  );
}
```

**Required:**
1. Import `Marker`, `MarkersDirective`, `MarkerDirective`
2. Inject `Marker` service
3. Wrap markers in `MarkersDirective`
4. Set `visible={true}`
5. Provide `dataSource` with latitude/longitude

### Marker Drag & Drop

React Maps supports marker dragging, making it ideal for editable locations or route design workflows.

```tsx
<MapsComponent
  markerDragStart={(args) => {
    console.log('Started dragging marker:', args.data);
  }}
>
```

## Marker Data Source

### Data Structure

Each marker object must have:
- `latitude`: Vertical position (Y-axis)
- `longitude`: Horizontal position (X-axis)
- Optional: Any custom fields for tooltips, labels, etc.

```typescript
interface MarkerData {
  latitude: number;
  longitude: number;
  name?: string;
  population?: number;
  [key: string]: any;  // Additional custom fields
}

const cities: MarkerData[] = [
  {
    latitude: 37.7749,
    longitude: -122.4194,
    name: 'San Francisco',
    population: 883305,
    country: 'USA'
  },
  {
    latitude: 48.8566,
    longitude: 2.3522,
    name: 'Paris',
    population: 2148000,
    country: 'France'
  }
];
```

### Using External Data

```tsx
import { cityData } from './data';

<MarkerDirective
  visible={true}
  dataSource={cityData}
  height={15}
  width={15}
/>
```

### Dynamic Data from API

```tsx
function MapWithMarkers() {
  const [markers, setMarkers] = React.useState([]);

  React.useEffect(() => {
    fetch('/api/locations')
      .then(res => res.json())
      .then(data => setMarkers(data));
  }, []);

  return (
    <MapsComponent>
      <Inject services={[Marker]} />
      <LayersDirective>
        <LayerDirective shapeData={world_map}>
          <MarkersDirective>
            <MarkerDirective
              visible={true}
              dataSource={markers}
              height={20}
              width={20}
            />
          </MarkersDirective>
        </LayerDirective>
      </LayersDirective>
    </MapsComponent>
  );
}
```

## Marker Shapes

### Built-in Shapes

```tsx
<MarkerDirective
  visible={true}
  dataSource={locationData}
  shape='Circle'     // Options: Circle, Diamond, Star, Triangle, 
                     // HorizontalLine, VerticalLine, Pentagon,
                     // InvertedTriangle, Rectangle, Balloon, Cross
  height={25}
  width={25}
  fill='#FF6347'
  border={{ color: '#8B0000', width: 2 }}
/>
```

### Shape Examples

```tsx
// Store locations - Circle
<MarkerDirective
  dataSource={stores}
  shape='Circle'
  fill='#4CAF50'
/>

// Important landmarks - Star
<MarkerDirective
  dataSource={landmarks}
  shape='Star'
  fill='#FFD700'
/>

// Events - Balloon
<MarkerDirective
  dataSource={events}
  shape='Balloon'
  fill='#FF69B4'
/>

// Warnings - Triangle
<MarkerDirective
  dataSource={warnings}
  shape='Triangle'
  fill='#FF4500'
/>
```

### Image Markers

Use custom images:

```tsx
<MarkerDirective
  visible={true}
  dataSource={locationData}
  shape='Image'
  imageUrl='./marker-icon.png'
  height={30}
  width={30}
/>
```

## Customizing Markers

### Size and Color

```tsx
<MarkerDirective
  visible={true}
  dataSource={markerData}
  height={30}
  width={30}
  fill='#2196F3'           // Marker fill color
  opacity={0.8}            // Transparency (0-1)
  border={{
    color: '#0D47A1',       // Border color
    width: 2                // Border thickness
  }}
/>
```

### Animation

Markers support smooth animated loading via duration and delay values.

```tsx
<MarkerDirective
  visible={true}
  dataSource={markers}
  animationDuration={1000}  // Animation duration in ms
  animationDelay={100}      // Delay before animation starts
  height={20}
  width={20}
/>
```

### Offset Position

Adjust marker position relative to coordinates:

```tsx
<MarkerDirective
  visible={true}
  dataSource={markers}
  offset={{
    x: -10,  // Move left/right
    y: -15   // Move up/down
  }}
  height={20}
  width={20}
/>
```

## Marker Templates

### Custom HTML Template

```tsx
function MapWithCustomMarkers() {
  const markerTemplate = (props) => {
    return (
      <div style={{
        background: '#FF6347',
        color: 'white',
        padding: '5px 10px',
        borderRadius: '15px',
        border: '2px solid white',
        fontSize: '12px',
        fontWeight: 'bold',
        whiteSpace: 'nowrap'
      }}>
        {props.name}
      </div>
    );
  };

  return (
    <MapsComponent>
      <Inject services={[Marker]} />
      <LayersDirective>
        <LayerDirective shapeData={world_map}>
          <MarkersDirective>
            <MarkerDirective
              visible={true}
              dataSource={[
                { latitude: 40.7128, longitude: -74.0060, name: 'NYC' },
                { latitude: 51.5074, longitude: -0.1278, name: 'London' }
              ]}
              template={markerTemplate}
            />
          </MarkersDirective>
        </LayerDirective>
      </LayersDirective>
    </MapsComponent>
  );
}
```

### Icon with Label Template

```tsx
const iconTemplate = (props) => {
  return (
    <div style={{ textAlign: 'center' }}>
      <div style={{
        backgroundColor: '#4CAF50',
        color: 'white',
        borderRadius: '50%',
        width: '30px',
        height: '30px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontWeight: 'bold',
        border: '3px solid white',
        boxShadow: '0 2px 6px rgba(0,0,0,0.3)'
      }}>
        {props.count}
      </div>
      <div style={{
        marginTop: '5px',
        fontSize: '11px',
        fontWeight: 'bold',
        textShadow: '0 0 3px white'
      }}>
        {props.city}
      </div>
    </div>
  );
};

<MarkerDirective
  visible={true}
  dataSource={cityData}
  template={iconTemplate}
/>
```

### Image + Text Template

```tsx
const imageTextTemplate = (props) => {
  return (
    <div style={{ textAlign: 'center' }}>
      <img 
        src={props.imageUrl} 
        alt={props.name}
        style={{ width: '40px', height: '40px', borderRadius: '50%' }}
      />
      <div style={{
        backgroundColor: 'rgba(0,0,0,0.7)',
        color: 'white',
        padding: '2px 6px',
        borderRadius: '3px',
        fontSize: '10px',
        marginTop: '3px'
      }}>
        {props.name}
      </div>
    </div>
  );
};
```

## Dynamic Markers

### Add/Remove Markers

```tsx
function DynamicMarkerMap() {
  const [markers, setMarkers] = React.useState([
    { latitude: 40.7128, longitude: -74.0060, name: 'New York' }
  ]);

  const addMarker = (lat, lng, name) => {
    setMarkers([...markers, { latitude: lat, longitude: lng, name }]);
  };

  const removeMarker = (index) => {
    setMarkers(markers.filter((_, i) => i !== index));
  };

  return (
    <>
      <button onClick={() => addMarker(51.5074, -0.1278, 'London')}>
        Add London
      </button>
      
      <MapsComponent>
        <Inject services={[Marker]} />
        <LayersDirective>
          <LayerDirective shapeData={world_map}>
            <MarkersDirective>
              <MarkerDirective
                visible={true}
                dataSource={markers}
                height={20}
                width={20}
              />
            </MarkersDirective>
          </LayerDirective>
        </LayersDirective>
      </MapsComponent>
    </>
  );
}
```

### Update Marker Properties

```tsx
const [markerColor, setMarkerColor] = React.useState('#FF0000');

<MarkerDirective
  visible={true}
  dataSource={markers}
  fill={markerColor}
  height={20}
  width={20}
/>

<button onClick={() => setMarkerColor('#00FF00')}>
  Change Color
</button>
```

## Marker Clustering

For dense marker groups, enable clustering:

```tsx
<MarkerDirective
  visible={true}
  dataSource={manyMarkers}  // Large dataset
  shape='Circle'
  height={15}
  width={15}
  clusterSettings={{
    allowClustering: true,
    shape: 'Circle',
    width: 30,
    height: 30,
    fill: '#4CAF50',
    opacity: 0.8,
    labelStyle: {
      color: 'white',
      size: '14px',
      fontWeight: 'bold'
    }
  }}
/>
```

**Clustering behavior:**
- Groups nearby markers into single cluster icon
- Shows count of markers in cluster
- Expands on zoom in
- Improves performance with large datasets

### Cluster Interaction Events

Clusters can emit events when clicked, allowing expansion or contextual actions.

```tsx
<MapsComponent
  markerClusterClick={(args) => {
    console.log('Cluster clicked, count:', args.data.length);
  }}
>
```

## Interactive Markers

### Marker Tooltips

```tsx
<MapsComponent>
  <Inject services={[Marker, MapsTooltip]} />
  <LayersDirective>
    <LayerDirective shapeData={world_map}>
      <MarkersDirective>
        <MarkerDirective
          visible={true}
          dataSource={cityData}
          tooltipSettings={{
            visible: true,
            valuePath: 'name',
            format: '${name}<br/>Population: ${population}'
          }}
          height={20}
          width={20}
        />
      </MarkersDirective>
    </LayerDirective>
  </LayersDirective>
</MapsComponent>
```

### Marker Click Events

```tsx
function InteractiveMarkerMap() {
  const handleMarkerClick = (event) => {
    console.log('Marker clicked:', event.data);
    alert(`You clicked: ${event.data.name}`);
  };

  return (
    <MapsComponent markerClick={handleMarkerClick}>
      <Inject services={[Marker]} />
      <LayersDirective>
        <LayerDirective shapeData={world_map}>
          <MarkersDirective>
            <MarkerDirective
              visible={true}
              dataSource={locationData}
              height={20}
              width={20}
            />
          </MarkersDirective>
        </LayerDirective>
      </LayersDirective>
    </MapsComponent>
  );
}
```

## Multiple Marker Sets

Display different marker types on same map:

```tsx
<LayerDirective shapeData={world_map}>
  <MarkersDirective>
    {/* Capitals - Stars */}
    <MarkerDirective
      visible={true}
      dataSource={capitals}
      shape='Star'
      fill='#FFD700'
      height={25}
      width={25}
    />
    
    {/* Major Cities - Circles */}
    <MarkerDirective
      visible={true}
      dataSource={majorCities}
      shape='Circle'
      fill='#4CAF50'
      height={15}
      width={15}
    />
    
    {/* Tourist Spots - Balloons */}
    <MarkerDirective
      visible={true}
      dataSource={touristSpots}
      shape='Balloon'
      fill='#FF69B4'
      height={20}
      width={20}
    />
  </MarkersDirective>
</LayerDirective>
```

## Common Use Cases

### Store Locator

```tsx
function StoreLocator() {
  const stores = [
    { latitude: 37.7749, longitude: -122.4194, name: 'SF Store', type: 'flagship' },
    { latitude: 34.0522, longitude: -118.2437, name: 'LA Store', type: 'regular' },
    { latitude: 40.7128, longitude: -74.0060, name: 'NY Store', type: 'flagship' }
  ];

  return (
    <MapsComponent>
      <Inject services={[Marker, MapsTooltip]} />
      <LayersDirective>
        <LayerDirective shapeData={usa_map}>
          <MarkersDirective>
            <MarkerDirective
              visible={true}
              dataSource={stores}
              shape='Circle'
              fill='#2196F3'
              height={20}
              width={20}
              tooltipSettings={{
                visible: true,
                valuePath: 'name'
              }}
            />
          </MarkersDirective>
        </LayerDirective>
      </LayersDirective>
    </MapsComponent>
  );
}
```

### Event Venue Map

```tsx
const eventTemplate = (props) => {
  return (
    <div style={{
      background: props.category === 'concert' ? '#FF6347' : '#4CAF50',
      color: 'white',
      padding: '8px 12px',
      borderRadius: '20px',
      fontSize: '12px',
      fontWeight: 'bold',
      boxShadow: '0 2px 8px rgba(0,0,0,0.3)'
    }}>
      🎵 {props.eventName}
    </div>
  );
};

<MarkerDirective
  visible={true}
  dataSource={events}
  template={eventTemplate}
/>
```

### Real-time Tracking

```tsx
function LiveTracking() {
  const [vehiclePosition, setVehiclePosition] = React.useState([
    { latitude: 37.7749, longitude: -122.4194, id: 'V1' }
  ]);

  React.useEffect(() => {
    const interval = setInterval(() => {
      // Simulate position updates
      fetchVehiclePositions().then(setVehiclePosition);
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <MapsComponent>
      <Inject services={[Marker]} />
      <LayersDirective>
        <LayerDirective shapeData={cityMap}>
          <MarkersDirective>
            <MarkerDirective
              visible={true}
              dataSource={vehiclePosition}
              shape='Image'
              imageUrl='./vehicle-icon.png'
              height={30}
              width={30}
            />
          </MarkersDirective>
        </LayerDirective>
      </LayersDirective>
    </MapsComponent>
  );
}
```

## Troubleshooting

### Issue: Markers not appearing

**Causes & Solutions:**

1. **Forgot to inject Marker service**
```tsx
// ✅ Correct
<MapsComponent>
  <Inject services={[Marker]} />
</MapsComponent>

// ❌ Wrong - missing injection
<MapsComponent>
```

2. **visible not set to true**
```tsx
// ✅ Correct
<MarkerDirective visible={true} dataSource={data} />

// ❌ Wrong
<MarkerDirective dataSource={data} />
```

3. **Invalid latitude/longitude values**
```tsx
// ✅ Correct: Valid coordinates
{ latitude: 40.7128, longitude: -74.0060 }

// ❌ Wrong: Values out of range
{ latitude: 200, longitude: -200 }  // Invalid
```

### Issue: Markers in wrong location

**Cause**: Latitude/longitude swapped

**Solution**: Remember - latitude is Y (vertical), longitude is X (horizontal)
```tsx
// ✅ Correct: latitude (Y), longitude (X)
{ latitude: 40.7128, longitude: -74.0060 }

// ❌ Wrong: Swapped
{ latitude: -74.0060, longitude: 40.7128 }
```

### Issue: Marker templates not rendering

**Cause**: Template function not returning JSX

**Solution**:
```tsx
// ✅ Correct
const template = (props) => {
  return <div>{props.name}</div>;
};

// ❌ Wrong
const template = (props) => {
  <div>{props.name}</div>;  // Missing return
};
```

### Issue: Too many markers causing performance issues

**Solutions:**
1. Enable clustering
2. Filter markers based on zoom level
3. Load markers on demand
4. Use simpler marker shapes (avoid complex templates)
