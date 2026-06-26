# Map Providers in React Maps

## Table of Contents
- [Overview](#overview)
- [When to Use Map Providers](#when-to-use-map-providers)
- [Bing Maps](#bing-maps)
- [OpenStreetMap](#openstreetmap)
- [Azure Maps](#azure-maps)
- [Hybrid Approach](#hybrid-approach)
- [Common Patterns](#common-patterns)
- [Troubleshooting](#troubleshooting)

## Overview

Map providers offer real-world tile-based map layers (satellite, aerial, street views) as alternatives or complements to GeoJSON shapes.

**Supported Providers:**
- **Bing Maps**: Microsoft's mapping service (requires API key)
- **OpenStreetMap (OSM)**: Free, open-source maps (no API key needed)
- **Azure Maps**: Microsoft Azure's mapping service (requires API key)

## When to Use Map Providers

### Use GeoJSON When:
- Displaying statistical/regional data (choropleth maps)
- Custom boundary visualization
- Offline capability required
- Full control over styling needed
- Data binding to specific regions

### Use Map Providers When:
- Need real-world street-level detail
- Satellite/aerial imagery required
- Familiar map interface expected (like Google Maps)
- Real-time navigation context needed
- Displaying POIs and street names

### Use Hybrid (Both) When:
- Overlaying custom data on real-world maps
- Combining statistical regions with street context
- Need both geographical shapes and street details

## Bing Maps

### Setup

```tsx
import {
  MapsComponent,
  LayersDirective,
  LayerDirective
} from '@syncfusion/ej2-react-maps';

function BingMap() {
  return (
    <MapsComponent>
      <LayersDirective>
        <LayerDirective
          urlTemplate="https://dev.virtualearth.net/REST/V1/Imagery/Metadata/RoadOnDemand?output=json&uriScheme=https&key=YOUR_BING_MAPS_KEY"
          key="YOUR_BING_MAPS_KEY"
        />
      </LayersDirective>
    </MapsComponent>
  );
}
```

### Bing Maps URL Template Retrieval

React Maps can auto-fetch the correct URL template for Bing Maps using getBingUrlTemplate().
This removes the need to manually build metadata URLs.

```tsx
const template = await mapsRef.current.getBingUrlTemplate(
  "https://dev.virtualearth.net/REST/V1/Imagery/Metadata/Aerial?output=json&key=YOUR_KEY")
```

### Get Bing Maps API Key

1. Visit [Bing Maps Dev Center](https://www.bingmapsportal.com/)
2. Sign in with Microsoft account
3. Create a new key under "My account" → "My keys"
4. Copy the key and use in your application

### Bing Maps Tile Types

```tsx
// Road map
urlTemplate="https://dev.virtualearth.net/REST/V1/Imagery/Metadata/RoadOnDemand?output=json&uriScheme=https&key=YOUR_KEY"

// Aerial view
urlTemplate="https://dev.virtualearth.net/REST/V1/Imagery/Metadata/Aerial?output=json&uriScheme=https&key=YOUR_KEY"

// Aerial with labels
urlTemplate="https://dev.virtualearth.net/REST/V1/Imagery/Metadata/AerialWithLabels?output=json&uriScheme=https&key=YOUR_KEY"
```

### Example with Markers

```tsx
function BingMapWithMarkers() {
  const locations = [
    { latitude: 40.7128, longitude: -74.0060, name: 'New York' },
    { latitude: 34.0522, longitude: -118.2437, name: 'Los Angeles' }
  ];

  return (
    <MapsComponent
      zoomSettings={{
        enable: true,
        zoomFactor: 4
      }}
      centerPosition={{
        latitude: 37.0902,
        longitude: -95.7129
      }}
    >
      <Inject services={[Marker, Zoom]} />
      <LayersDirective>
        <LayerDirective
          urlTemplate="https://dev.virtualearth.net/REST/V1/Imagery/Metadata/RoadOnDemand?output=json&uriScheme=https&key=YOUR_KEY"
          key="YOUR_KEY"
        >
          <MarkersDirective>
            <MarkerDirective
              visible={true}
              dataSource={locations}
              shape='Circle'
              fill='#FF0000'
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

## OpenStreetMap

### Setup (No API Key Required)

```tsx
function OSMMap() {
  return (
    <MapsComponent>
      <LayersDirective>
        <LayerDirective
          urlTemplate="Add your URL link"
        />
      </LayersDirective>
    </MapsComponent>
  );
}
```

### OSM Tile Servers

```tsx
// Standard OpenStreetMap
urlTemplate="Add your URL link"

// OpenStreetMap Humanitarian
urlTemplate="Add your URL link"

// OpenTopoMap (topographical)
urlTemplate="Add your URL link"
```

### Basic OSM Example

```tsx
function OpenStreetMapExample() {
  return (
    <MapsComponent
      zoomSettings={{
        enable: true,
        zoomFactor: 5
      }}
      centerPosition={{
        latitude: 51.5074,
        longitude: -0.1278
      }}
    >
      <Inject services={[Zoom]} />
      <LayersDirective>
        <LayerDirective
          urlTemplate="Add your URL link"
        />
      </LayersDirective>
    </MapsComponent>
  );
}
```

### OSM with Custom Markers

```tsx
function OSMStoreLocator() {
  const stores = [
    { latitude: 51.5074, longitude: -0.1278, name: 'London Store' },
    { latitude: 48.8566, longitude: 2.3522, name: 'Paris Store' }
  ];

  return (
    <MapsComponent
      titleSettings={{ text: 'Store Locations' }}
      zoomSettings={{ enable: true, zoomFactor: 4 }}
      centerPosition={{ latitude: 50, longitude: 1 }}
    >
      <Inject services={[Marker, Zoom, MapsTooltip]} />
      <LayersDirective>
        <LayerDirective
          urlTemplate="Add your URL link"
        >
          <MarkersDirective>
            <MarkerDirective
              visible={true}
              dataSource={stores}
              shape='Image'
              imageUrl='./store-icon.png'
              height={30}
              width={30}
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

## Azure Maps

### Setup

```tsx
function AzureMap() {
  return (
    <MapsComponent>
      <LayersDirective>
        <LayerDirective
          urlTemplate="https://atlas.microsoft.com/map/tile?subscription-key=YOUR_AZURE_KEY&api-version=2.0&tilesetId=microsoft.base.road&zoom=level&x=tileX&y=tileY"
          key="YOUR_AZURE_KEY"
        />
      </LayersDirective>
    </MapsComponent>
  );
}
```

### Get Azure Maps Key

1. Create Azure account at [portal.azure.com](https://portal.azure.com)
2. Create Azure Maps resource
3. Navigate to "Authentication" → "Primary Key"
4. Copy the key

### Azure Maps Tile Sets

```tsx
// Road map
tilesetId=microsoft.base.road

// Satellite
tilesetId=microsoft.imagery

// Hybrid (satellite with labels)
tilesetId=microsoft.base.hybrid

// Dark mode
tilesetId=microsoft.base.darkgrey
```

## Hybrid Approach

Combine GeoJSON shapes with map provider tiles:

### GeoJSON Overlay on OpenStreetMap

```tsx
function HybridMap() {
  const stateData = [
    { name: 'California', population: 39538223 },
    { name: 'Texas', population: 29145505 }
  ];

  return (
    <MapsComponent
      zoomSettings={{ enable: true, zoomFactor: 5 }}
      centerPosition={{ latitude: 37, longitude: -96 }}
    >
      <Inject services={[Zoom, Legend]} />
      <LayersDirective>
        {/* Base layer: OpenStreetMap */}
        <LayerDirective
          urlTemplate="Add your URL link"
        />
        
        {/* Overlay: State boundaries with data */}
        <LayerDirective
          type="SubLayer"
          shapeData={usa_states}
          dataSource={stateData}
          shapeDataPath='name'
          shapePropertyPath='name'
          shapeSettings={{
            fill: 'transparent',
            colorValuePath: 'population',
            colorMapping: [
              { from: 0, to: 10000000, color: 'rgba(255,165,0,0.4)' },
              { from: 10000000, to: 50000000, color: 'rgba(255,69,0,0.4)' }
            ],
            border: {
              color: '#FF6347',
              width: 2
            }
          }}
        />
      </LayersDirective>
    </MapsComponent>
  );
}
```

### Bing Maps with Custom Shapes

```tsx
function BingHybridMap() {
  return (
    <MapsComponent zoomSettings={{ enable: true }}>
      <Inject services={[Zoom]} />
      <LayersDirective>
        {/* Base: Bing Maps */}
        <LayerDirective
          urlTemplate="https://dev.virtualearth.net/REST/V1/Imagery/Metadata/Aerial?output=json&uriScheme=https&key=YOUR_KEY"
          key="YOUR_KEY"
        />
        
        {/* Overlay: Custom region */}
        <LayerDirective
          type="SubLayer"
          shapeData={custom_region}
          shapeSettings={{
            fill: 'rgba(255,0,0,0.3)',
            border: { color: '#FF0000', width: 3 }
          }}
        />
      </LayersDirective>
    </MapsComponent>
  );
}
```

## Common Patterns

### Pattern 1: Store Locator on Real Map

```tsx
function StoreLocatorMap() {
  const stores = [
    { lat: 37.7749, lng: -122.4194, name: 'SF Store', address: '123 Market St' },
    { lat: 34.0522, lng: -118.2437, name: 'LA Store', address: '456 Sunset Blvd' }
  ];

  return (
    <MapsComponent
      titleSettings={{ text: 'Find Our Stores' }}
      zoomSettings={{ enable: true, zoomFactor: 7 }}
      centerPosition={{ latitude: 36, longitude: -120 }}
    >
      <Inject services={[Marker, Zoom, MapsTooltip]} />
      <LayersDirective>
        <LayerDirective
          urlTemplate="Add your URL link"
        >
          <MarkersDirective>
            <MarkerDirective
              visible={true}
              dataSource={stores}
              shape='Balloon'
              fill='#FF6347'
              height={30}
              width={30}
              tooltipSettings={{
                visible: true,
                format: '${name}<br/>${address}'
              }}
            />
          </MarkersDirective>
        </LayerDirective>
      </LayersDirective>
    </MapsComponent>
  );
}
```

### Pattern 2: Delivery Tracking

```tsx
function DeliveryTrackingMap() {
  const [vehiclePosition, setVehiclePosition] = React.useState([
    { latitude: 40.7128, longitude: -74.0060, vehicle: 'Truck 1' }
  ]);

  return (
    <MapsComponent
      zoomSettings={{ enable: true, zoomFactor: 12 }}
      centerPosition={{ latitude: 40.7128, longitude: -74.0060 }}
    >
      <Inject services={[Marker, Zoom]} />
      <LayersDirective>
        <LayerDirective
          urlTemplate="Add your URL link"
        >
          <MarkersDirective>
            <MarkerDirective
              visible={true}
              dataSource={vehiclePosition}
              shape='Image'
              imageUrl='./truck-icon.png'
              height={40}
              width={40}
            />
          </MarkersDirective>
        </LayerDirective>
      </LayersDirective>
    </MapsComponent>
  );
}
```

### Pattern 3: Event Venue Map

```tsx
function EventVenueMap() {
  const venue = { latitude: 51.5074, longitude: -0.1278 };

  return (
    <MapsComponent
      zoomSettings={{ enable: true, zoomFactor: 15 }}
      centerPosition={{ latitude: 51.5074, longitude: -0.1278 }}
    >
      <Inject services={[Marker, Zoom]} />
      <LayersDirective>
        <LayerDirective
          urlTemplate="Add your URL link"
        >
          <MarkersDirective>
            <MarkerDirective
              visible={true}
              dataSource={[venue]}
              shape='Star'
              fill='#FFD700'
              height={40}
              width={40}
            />
          </MarkersDirective>
        </LayerDirective>
      </LayersDirective>
    </MapsComponent>
  );
}
```

## Troubleshooting

### Issue: Tiles not loading

**Causes & Solutions:**

1. **Invalid URL template**
```tsx
// ✅ Correct OSM template
urlTemplate="your URL links .png"

```

2. **Missing or invalid API key (Bing/Azure)**
```tsx
// ✅ Correct - valid key
<LayerDirective key="YOUR_VALID_KEY" urlTemplate="..." />

// ❌ Wrong - placeholder key
<LayerDirective key="YOUR_KEY" urlTemplate="..." />
```

3. **CORS issues**
- Check browser console for CORS errors
- Some tile servers may block requests from certain domains
- Use approved tile servers or configure CORS on your server

### Issue: Map appears blank

**Solutions:**
- Set appropriate `zoomFactor` and `centerPosition`
- Check network tab for failed tile requests
- Verify API key permissions and quotas

```tsx
<MapsComponent
  zoomSettings={{ enable: true, zoomFactor: 4 }}
  centerPosition={{ latitude: 40, longitude: -100 }}
>
```

### Issue: Low zoom shows no detail

**Cause:** Tile servers have minimum zoom levels

**Solution:** Increase `zoomFactor` for street-level detail
```tsx
zoomSettings={{
  enable: true,
  zoomFactor: 12,  // Higher zoom for more detail
  minZoom: 5,
  maxZoom: 19
}}
```

### Issue: Hybrid overlay not visible

**Cause:** SubLayer fill not transparent

**Solution:**
```tsx
// ✅ Correct - transparent fill shows base map
<LayerDirective
  type="SubLayer"
  shapeSettings={{
    fill: 'transparent',  // or rgba(255,0,0,0.3)
    border: { color: '#FF0000', width: 2 }
  }}
/>
```

## Cost Considerations

- **OpenStreetMap**: Free (respect usage policies)
- **Bing Maps**: Free tier available, paid for high volume
- **Azure Maps**: Pay-as-you-go pricing

Always check current pricing and quotas for commercial applications.
