# Navigation Lines in React Maps

## Overview

Navigation lines visualize connections between geographical locations - perfect for showing routes, migration patterns, trade flows, or any directional relationships between points.

**Key Features:**
- Connect two or more locations with lines
- Curved lines and custom angles
- Arrow indicators for direction
- Line styling (color, width, dash patterns)
- Animation effects

## Basic Navigation Lines

```tsx
import {
  MapsComponent,
  LayersDirective,
  LayerDirective,
  NavigationLinesDirective,
  NavigationLineDirective,
  Inject,
  NavigationLine
} from '@syncfusion/ej2-react-maps';

function RouteMap() {
  const flightRoutes = [
    {
      latitude: [40.7128, 51.5074],      // NYC to London
      longitude: [-74.0060, -0.1278],
      angle: -0.5
    },
    {
      latitude: [35.6762, 1.3521],        // Tokyo to Singapore
      longitude: [139.6503, 103.8198],
      angle: 0.5
    }
  ];

  return (
    <MapsComponent>
      <Inject services={[NavigationLine]} />
      <LayersDirective>
        <LayerDirective shapeData={world_map}>
          <NavigationLinesDirective>
            <NavigationLineDirective
              visible={true}
              dataSource={flightRoutes}
              width={2}
              color='#FF6347'
              angle={0}
            />
          </NavigationLinesDirective>
        </LayerDirective>
      </LayersDirective>
    </MapsComponent>
  );
}
```

## Data Structure

```typescript
interface NavigationLineData {
  latitude: [number, number];   // [start, end]
  longitude: [number, number];  // [start, end]
  angle?: number;               // Curve angle (-1 to 1)
  [key: string]: any;           // Custom fields
}

const routes: NavigationLineData[] = [
  {
    latitude: [37.7749, 40.7128],  // San Francisco to New York
    longitude: [-122.4194, -74.0060],
    angle: -0.3,
    routeName: 'West to East',
    distance: 2565
  }
];
```

## Line Styling

### Basic Styling

```tsx
<NavigationLineDirective
  visible={true}
  dataSource={routes}
  width={3}                    // Line thickness
  color='#2196F3'              // Line color
  angle={-0.4}                 // Curve (-1 to 1)
  dashArray='5,3'              // Dash pattern
/>
```

### Arrow Indicators

```tsx
<NavigationLineDirective
  visible={true}
  dataSource={routes}
  width={2}
  color='#4CAF50'
  arrowSettings={{
    showArrow: true,
    position: 'End',           // Start, End, or Both
    size: 10,
    color: '#4CAF50'
  }}
/>
```

### Line with Labels

```tsx
<NavigationLineDirective
  visible={true}
  dataSource={routes}
  width={2}
  color='#FF9800'
  labelSettings={{
    visible: true,
    labelPath: 'routeName',
    textStyle: {
      size: '12px',
      color: '#333',
      fontWeight: 'Bold'
    }
  }}
/>
```

## Curved Lines

Control line curvature with the angle property:

```tsx
// Straight line
<NavigationLineDirective angle={0} />

// Curved upward
<NavigationLineDirective angle={-0.5} />

// Curved downward
<NavigationLineDirective angle={0.5} />

// Strong curve
<NavigationLineDirective angle={-0.8} />
```

**Angle values:**
- `0`: Straight line
- Negative (`-0.1` to `-1`): Curve upward
- Positive (`0.1` to `1`): Curve downward

## Animation Effects

```tsx
<NavigationLineDirective
  visible={true}
  dataSource={routes}
  width={2}
  color='#FF6347'
  animationDuration={2000}     // 2 seconds
  animationDelay={0}           // Start immediately
/>
```

## Multiple Navigation Line Sets

Display different route types:

```tsx
<LayerDirective shapeData={world_map}>
  <NavigationLinesDirective>
    {/* Direct flights - Red */}
    <NavigationLineDirective
      visible={true}
      dataSource={directFlights}
      width={3}
      color='#FF0000'
      arrowSettings={{ showArrow: true, position: 'End' }}
    />
    
    {/* Connecting flights - Blue */}
    <NavigationLineDirective
      visible={true}
      dataSource={connectingFlights}
      width={2}
      color='#0000FF'
      dashArray='5,3'
      arrowSettings={{ showArrow: true, position: 'End' }}
    />
    
    {/* Cargo routes - Green */}
    <NavigationLineDirective
      visible={true}
      dataSource={cargoRoutes}
      width={2}
      color='#00FF00'
      angle={0.3}
    />
  </NavigationLinesDirective>
</LayerDirective>
```

## Common Use Cases

### Flight Route Map

```tsx
function FlightRouteMap() {
  const routes = [
    {
      latitude: [40.7128, 51.5074],
      longitude: [-74.0060, -0.1278],
      flight: 'NYC → London',
      duration: '7h 30m'
    },
    {
      latitude: [35.6762, 1.3521],
      longitude: [139.6503, 103.8198],
      flight: 'Tokyo → Singapore',
      duration: '6h 45m'
    }
  ];

  return (
    <MapsComponent>
      <Inject services={[NavigationLine, MapsTooltip]} />
      <LayersDirective>
        <LayerDirective shapeData={world_map}>
          <NavigationLinesDirective>
            <NavigationLineDirective
              visible={true}
              dataSource={routes}
              width={2}
              color='#FF6347'
              angle={-0.3}
              arrowSettings={{
                showArrow: true,
                position: 'End',
                size: 8
              }}
              tooltipSettings={{
                visible: true,
                format: '${flight}<br/>Duration: ${duration}'
              }}
            />
          </NavigationLinesDirective>
        </LayerDirective>
      </LayersDirective>
    </MapsComponent>
  );
}
```

### Migration Pattern Map

```tsx
function MigrationMap() {
  const migrationData = [
    {
      latitude: [52.5200, 40.7128],  // Berlin to NYC
      longitude: [13.4050, -74.0060],
      from: 'Germany',
      to: 'USA',
      count: 15000,
      angle: -0.4
    },
    {
      latitude: [19.4326, 51.5074],  // Mexico City to London
      longitude: [-99.1332, -0.1278],
      from: 'Mexico',
      to: 'UK',
      count: 8000,
      angle: -0.3
    }
  ];

  return (
    <MapsComponent titleSettings={{ text: 'Migration Flows 2023' }}>
      <Inject services={[NavigationLine, MapsTooltip]} />
      <LayersDirective>
        <LayerDirective shapeData={world_map}>
          <NavigationLinesDirective>
            <NavigationLineDirective
              visible={true}
              dataSource={migrationData}
              width={3}
              color='#4CAF50'
              arrowSettings={{
                showArrow: true,
                position: 'End',
                size: 10,
                color: '#2E7D32'
              }}
              tooltipSettings={{
                visible: true,
                format: '${from} → ${to}<br/>Migrants: ${count}'
              }}
            />
          </NavigationLinesDirective>
        </LayerDirective>
      </LayersDirective>
    </MapsComponent>
  );
}
```

### Shipping Routes

```tsx
function ShippingMap() {
  const shippingRoutes = [
    {
      latitude: [31.2304, 51.5074],
      longitude: [121.4737, -0.1278],
      route: 'Shanghai → London',
      cargo: 'Electronics',
      angle: -0.2
    }
  ];

  return (
    <MapsComponent>
      <Inject services={[NavigationLine]} />
      <LayersDirective>
        <LayerDirective shapeData={world_map}>
          <NavigationLinesDirective>
            <NavigationLineDirective
              visible={true}
              dataSource={shippingRoutes}
              width={4}
              color='#2196F3'
              dashArray='10,5'
              angle={-0.2}
              arrowSettings={{
                showArrow: true,
                position: 'End',
                size: 12
              }}
            />
          </NavigationLinesDirective>
        </LayerDirective>
      </LayersDirective>
    </MapsComponent>
  );
}
```

## Combining with Markers

Show start/end points with markers:

```tsx
function RouteWithMarkersMap() {
  const routes = [
    { latitude: [40.7128, 51.5074], longitude: [-74.0060, -0.1278] }
  ];

  const cities = [
    { latitude: 40.7128, longitude: -74.0060, city: 'New York' },
    { latitude: 51.5074, longitude: -0.1278, city: 'London' }
  ];

  return (
    <MapsComponent>
      <Inject services={[NavigationLine, Marker]} />
      <LayersDirective>
        <LayerDirective shapeData={world_map}>
          <NavigationLinesDirective>
            <NavigationLineDirective
              visible={true}
              dataSource={routes}
              width={2}
              color='#FF6347'
              arrowSettings={{ showArrow: true, position: 'End' }}
            />
          </NavigationLinesDirective>
          
          <MarkersDirective>
            <MarkerDirective
              visible={true}
              dataSource={cities}
              shape='Circle'
              fill='#FF6347'
              height={15}
              width={15}
              tooltipSettings={{
                visible: true,
                valuePath: 'city'
              }}
            />
          </MarkersDirective>
        </LayerDirective>
      </LayersDirective>
    </MapsComponent>
  );
}
```

## Troubleshooting

### Issue: Navigation lines not appearing

**Solutions:**
1. Inject `NavigationLine` service
2. Set `visible={true}`
3. Verify latitude/longitude arrays have two values each

```tsx
// ✅ Correct
<MapsComponent>
  <Inject services={[NavigationLine]} />
  <NavigationLineDirective
    visible={true}
    dataSource={[
      { latitude: [40, 51], longitude: [-74, -0] }  // Valid
    ]}
  />
</MapsComponent>
```

### Issue: Lines not curved

**Cause:** angle property not set or set to 0

**Solution:**
```tsx
// Add curvature
<NavigationLineDirective angle={-0.4} />
```

### Issue: Arrows not showing

**Cause:** arrowSettings not configured

**Solution:**
```tsx
<NavigationLineDirective
  arrowSettings={{
    showArrow: true,
    position: 'End'
  }}
/>
```
