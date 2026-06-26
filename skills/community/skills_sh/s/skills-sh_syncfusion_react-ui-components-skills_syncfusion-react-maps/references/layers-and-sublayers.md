# Layers and Sublayers in React Maps

## Table of Contents
- [Overview](#overview)
- [Understanding Layer Architecture](#understanding-layer-architecture)
- [Main Layer vs Sublayer](#main-layer-vs-sublayer)
- [Creating Multiple Layers](#creating-multiple-layers)
- [Layer Types](#layer-types)
- [Layer Configuration](#layer-configuration)
- [Stacking and Ordering](#stacking-and-ordering)
- [Drill‑Down Navigation](#drilldown-navigation)
- [Use Cases](#use-cases)
- [Common Patterns](#common-patterns)
- [Troubleshooting](#troubleshooting)

## Overview

Layers are the fundamental building blocks of Maps. The component renders content through multiple layers, allowing complex visualizations by stacking shapes, highlighting regions, or combining different data sources.

## Understanding Layer Architecture

```
Maps Component
├── Main Layer (Base)
│   └── World map or country GeoJSON
├── Sublayer 1 (Overlay)
│   └── Highlighted state/region
├── Sublayer 2 (Overlay)
│   └── Another region or data
└── Sublayer N...
```

**Key Concepts:**
- **Main Layer**: The base map, typically a larger geographical area
- **Sublayers**: Overlays that render on top of the main layer
- **Stacking**: Layers render in the order defined
- **Independence**: Each layer has its own settings, data, and styling

## Main Layer vs Sublayer

### Main Layer

The first layer in `LayersDirective` is the main layer:

```tsx
<LayersDirective>
  <LayerDirective 
    shapeData={world_map}
    // This is the MAIN layer (default type)
  />
</LayersDirective>
```

**Characteristics:**
- Serves as the base map
- Fills the entire map container
- Usually covers the broadest geographical area
- No `type` property needed (defaults to "Layer")

### Sublayer

Additional layers with `type="SubLayer"`:

```tsx
<LayersDirective>
  <LayerDirective shapeData={world_map} />
  
  <LayerDirective 
    shapeData={texas}
    type="SubLayer"  // This makes it an overlay
  />
</LayersDirective>
```

**Characteristics:**
- Renders on top of main layer
- Can highlight specific regions
- Transparent areas show base layer underneath
- Requires `type="SubLayer"` property

## Creating Multiple Layers

### Basic Multi-Layer Example

```tsx
import { usa_map } from './usa-map';
import { california } from './california';
import { texas } from './texas';

function App() {
  return (
    <MapsComponent>
      <LayersDirective>
        {/* Main layer: Full USA map */}
        <LayerDirective
          shapeData={usa_map}
          shapeSettings={{
            fill: '#E5E5E5',
            border: { width: 0.5, color: 'black' }
          }}
        />
        
        {/* Sublayer 1: Highlight Texas */}
        <LayerDirective
          shapeData={texas}
          type="SubLayer"
          shapeSettings={{
            fill: 'rgba(141, 206, 255, 0.6)',
            border: { width: 1, color: '#1a9cff' }
          }}
        />
        
        {/* Sublayer 2: Highlight California */}
        <LayerDirective
          shapeData={california}
          type="SubLayer"
          shapeSettings={{
            fill: 'rgba(255, 165, 0, 0.6)',
            border: { width: 1, color: '#ff8c00' }
          }}
        />
      </LayersDirective>
    </MapsComponent>
  );
}
```

**Result**: USA map with Texas and California highlighted in different colors.

### Multi-Layer with Different Data

```tsx
function RegionalSalesMap() {
  const countryData = [
    { name: 'United States', sales: 5000000 },
    { name: 'Canada', sales: 2000000 }
  ];

  const stateData = [
    { name: 'California', sales: 1500000 },
    { name: 'Texas', sales: 1200000 }
  ];

  return (
    <MapsComponent>
      <LayersDirective>
        {/* Main layer: North America */}
        <LayerDirective
          shapeData={northAmerica}
          dataSource={countryData}
          shapeDataPath='name'
          shapePropertyPath='name'
          shapeSettings={{
            colorValuePath: 'sales',
            colorMapping: [
              { from: 0, to: 3000000, color: '#C3E6CB' },
              { from: 3000000, to: 6000000, color: '#2F7C4F' }
            ]
          }}
        />
        
        {/* Sublayer: US States detail */}
        <LayerDirective
          shapeData={usStates}
          type="SubLayer"
          dataSource={stateData}
          shapeDataPath='name'
          shapePropertyPath='name'
          shapeSettings={{
            colorValuePath: 'sales',
            colorMapping: [
              { from: 0, to: 1000000, color: '#FFE5B4' },
              { from: 1000000, to: 2000000, color: '#FF8C00' }
            ]
          }}
        />
      </LayersDirective>
    </MapsComponent>
  );
}
```

## Layer Types

### Type: "Layer" (Default - Main Layer)

```tsx
<LayerDirective
  shapeData={world_map}
  // type="Layer" is implicit
/>
```

**When to use:**
- First layer in your map
- Base geographical area
- Primary data visualization

### Type: "SubLayer" (Overlay)

```tsx
<LayerDirective
  shapeData={region}
  type="SubLayer"
/>
```

**When to use:**
- Highlighting specific regions
- Overlaying additional data
- Creating visual emphasis
- Showing nested geographical relationships

## Layer Configuration

### Individual Layer Settings

Each layer can have unique configurations:

```tsx
<LayersDirective>
  <LayerDirective
    shapeData={world_map}
    shapeSettings={{
      fill: '#f0f0f0',
      border: { width: 1, color: '#333' }
    }}
    dataLabelSettings={{
      visible: true,
      labelPath: 'name'
    }}
  />
  
  <LayerDirective
    shapeData={highlighted_countries}
    type="SubLayer"
    shapeSettings={{
      fill: '#ff6b6b',
      border: { width: 2, color: '#c92a2a' }
    }}
    // No data labels on this layer
  />
</LayersDirective>
```

### Layer-Specific Features

Each layer can have:
- **Markers**: Different marker sets per layer
- **Bubbles**: Unique bubble configurations
- **Data Labels**: Independent label settings
- **Tooltips**: Layer-specific tooltip content
- **Color Mapping**: Different data visualization per layer

```tsx
<LayersDirective>
  {/* Base layer with country data */}
  <LayerDirective
    shapeData={world_map}
    dataSource={countryData}
    markerSettings={[
      {
        visible: true,
        dataSource: capitalCities,
        shape: 'Circle'
      }
    ]}
  />
  
  {/* Overlay with regional markers */}
  <LayerDirective
    shapeData={europeRegion}
    type="SubLayer"
    markerSettings={[
      {
        visible: true,
        dataSource: touristAttractions,
        shape: 'Star'
      }
    ]}
  />
</LayersDirective>
```

### Per‑Layer Zoom Constraints

You can restrict zooming for individual layers using minimum and maximum zoom levels.
Useful for lockstep navigation or multi-layered visualizations.

```tsx
<LayerDirective
    shapeData={usa_map}
    layerSettings={{ minZoom: 2, maxZoom: 10 }}
/>
```

### Conditional Layer Visibility

Layers can appear or hide dynamically based on current zoom, supporting multi-resolution transitions.

```tsx
<LayerDirective visible={currentZoom > 4} />
```

## Stacking and Ordering

Layers render in the order they're defined:

```tsx
<LayersDirective>
  <LayerDirective shapeData={layer1} />  {/* Bottom */}
  <LayerDirective shapeData={layer2} type="SubLayer" />  {/* Middle */}
  <LayerDirective shapeData={layer3} type="SubLayer" />  {/* Top */}
</LayersDirective>
```

**Visual Result:**
```
Layer 3 (top)
Layer 2 (middle)
Layer 1 (bottom)
```

## Drill‑Down Navigation

Drill-down enables transitioning from larger geographical regions to more detailed shapes, such as switching from a world map to a country-level map when a shape is clicked.

```tsx
const [showDetail, setShowDetail] = React.useState(false);

<MapsComponent>
  <LayersDirective>
    <LayerDirective shapeData={world_map} />
    
    {showDetail && (
      <LayerDirective
        shapeData={country_detail}
        type="SubLayer"
        shapeSettings={{
          fill: 'rgba(76, 175, 80, 0.6)'
        }}
      />
    )}
  </LayersDirective>
</MapsComponent>
```

### Controlling Visual Hierarchy with Opacity

Use opacity to create depth:

```tsx
<LayersDirective>
  {/* Base: Solid */}
  <LayerDirective
    shapeData={world_map}
    shapeSettings={{
      fill: '#E5E5E5',
      opacity: 1
    }}
  />
  
  {/* Middle: Semi-transparent */}
  <LayerDirective
    shapeData={continents}
    type="SubLayer"
    shapeSettings={{
      fill: '#4CAF50',
      opacity: 0.5
    }}
  />
  
  {/* Top: More transparent */}
  <LayerDirective
    shapeData={countries}
    type="SubLayer"
    shapeSettings={{
      fill: '#2196F3',
      opacity: 0.3
    }}
  />
</LayersDirective>
```

## Use Cases

### Use Case 1: Country with Highlighted States

**Scenario**: Show USA map with specific states highlighted

```tsx
function USAStateHighlight() {
  const highlightedStates = [
    { name: 'California' },
    { name: 'Texas' },
    { name: 'New York' }
  ];

  return (
    <MapsComponent>
      <LayersDirective>
        <LayerDirective
          shapeData={usa_map}
          shapeSettings={{
            fill: '#D3D3D3',
            border: { width: 0.5, color: 'black' }
          }}
        />
        
        <LayerDirective
          shapeData={highlighted_states_geojson}
          type="SubLayer"
          dataSource={highlightedStates}
          shapeSettings={{
            fill: '#FFD700',
            border: { width: 1.5, color: '#FF8C00' }
          }}
        />
      </LayersDirective>
    </MapsComponent>
  );
}
```

### Use Case 2: Election Results Map

**Scenario**: Display election results with winning states colored

```tsx
function ElectionMap() {
  const electionResults = [
    { state: 'California', winner: 'Democrat', votes: 11110000 },
    { state: 'Texas', winner: 'Republican', votes: 8750000 },
    { state: 'Florida', winner: 'Republican', votes: 9700000 }
  ];

  return (
    <MapsComponent>
      <Inject services={[Legend]} />
      <LayersDirective>
        <LayerDirective
          shapeData={usa_map}
          dataSource={electionResults}
          shapeDataPath='state'
          shapePropertyPath='name'
          shapeSettings={{
            colorValuePath: 'winner',
            colorMapping: [
              { value: 'Democrat', color: '#0015BC' },
              { value: 'Republican', color: '#DE0100' }
            ]
          }}
        />
      </LayersDirective>
    </MapsComponent>
  );
}
```

### Use Case 3: Sales Territory Overlay

**Scenario**: Show sales territories over geographical map

```tsx
function SalesTerritoryMap() {
  return (
    <MapsComponent>
      <LayersDirective>
        {/* Base: Country borders */}
        <LayerDirective
          shapeData={country_map}
          shapeSettings={{
            fill: '#f5f5f5',
            border: { width: 1, color: '#666' }
          }}
        />
        
        {/* Overlay: North Territory */}
        <LayerDirective
          shapeData={north_territory}
          type="SubLayer"
          shapeSettings={{
            fill: 'rgba(255, 99, 71, 0.4)',
            border: { width: 2, color: '#FF6347' }
          }}
        />
        
        {/* Overlay: South Territory */}
        <LayerDirective
          shapeData={south_territory}
          type="SubLayer"
          shapeSettings={{
            fill: 'rgba(135, 206, 235, 0.4)',
            border: { width: 2, color: '#4682B4' }
          }}
        />
      </LayersDirective>
    </MapsComponent>
  );
}
```

## Common Patterns

### Pattern 1: Drill-Down Effect

Show progressively more detail:

```tsx
const [showDetail, setShowDetail] = React.useState(false);

<MapsComponent>
  <LayersDirective>
    <LayerDirective shapeData={world_map} />
    
    {showDetail && (
      <LayerDirective
        shapeData={country_detail}
        type="SubLayer"
        shapeSettings={{
          fill: 'rgba(76, 175, 80, 0.6)'
        }}
      />
    )}
  </LayersDirective>
</MapsComponent>
```

### Pattern 2: Conditional Layer Visibility

Toggle layers based on user selection:

```tsx
const [visibleLayers, setVisibleLayers] = React.useState({
  population: true,
  gdp: false,
  climate: false
});

<MapsComponent>
  <LayersDirective>
    <LayerDirective shapeData={world_map} />
    
    {visibleLayers.population && (
      <LayerDirective shapeData={populationData} type="SubLayer" />
    )}
    
    {visibleLayers.gdp && (
      <LayerDirective shapeData={gdpData} type="SubLayer" />
    )}
  </LayersDirective>
</MapsComponent>
```

### Pattern 3: Multiple Data Overlays

Combine different datasets:

```tsx
<LayersDirective>
  {/* Base geographical data */}
  <LayerDirective shapeData={base_map} />
  
  {/* Population density */}
  <LayerDirective shapeData={population_layer} type="SubLayer" />
  
  {/* Major cities */}
  <LayerDirective 
    shapeData={cities_layer} 
    type="SubLayer"
    markerSettings={[{ visible: true, dataSource: cityData }]}
  />
  
  {/* Transportation routes */}
  <LayerDirective 
    shapeData={routes_layer} 
    type="SubLayer"
    navigationLineSettings={[{ visible: true, dataSource: routeData }]}
  />
</LayersDirective>
```

## Troubleshooting

### Issue: Sublayer not visible

**Cause**: Missing `type="SubLayer"` or sublayer is fully transparent

**Solution**:
```tsx
// ✅ Correct
<LayerDirective 
  shapeData={overlay}
  type="SubLayer"
  shapeSettings={{ fill: 'rgba(255, 0, 0, 0.5)' }}  // Visible opacity
/>

// ❌ Wrong
<LayerDirective 
  shapeData={overlay}
  // Missing type="SubLayer"
/>
```

### Issue: Layers rendering in wrong order

**Cause**: Layer order in JSX

**Solution**: Reorder layers - first layer is bottom, last is top
```tsx
<LayersDirective>
  <LayerDirective shapeData={base} />      {/* Bottom */}
  <LayerDirective shapeData={middle} type="SubLayer" />
  <LayerDirective shapeData={top} type="SubLayer" />  {/* Top */}
</LayersDirective>
```

### Issue: Sublayer covers entire map instead of specific region

**Cause**: Sublayer GeoJSON covers entire map area

**Solution**: Ensure sublayer GeoJSON only contains the specific region shapes you want to highlight.

### Issue: Performance degradation with many layers

**Cause**: Too many layers or complex GeoJSON data

**Solution**:
- Simplify GeoJSON geometry
- Reduce number of layers
- Use conditional rendering to show/hide layers
- Consider combining similar layers
