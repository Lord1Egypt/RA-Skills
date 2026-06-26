---
name: syncfusion-react-maps
description: Implement Syncfusion React Maps component for geographical data visualization. Use this when displaying interactive maps, location-based information, or regional data analysis. This skill covers map providers (Bing, OpenStreetMap), GeoJSON rendering, markers and bubbles, zooming/panning, data labels, legends, and choropleth visualizations in React applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion React Maps

A comprehensive skill for implementing the Syncfusion React Maps component to visualize geographical data with rich interactivity, multiple layers, markers, bubbles, legends, and map provider integration.

## When to Use This Skill

Use this skill when you need to:
- **Display geographical data** on interactive maps
- **Visualize location-based information** with markers, bubbles, or data labels
- **Create choropleth maps** with color-coded regions based on data values
- **Integrate map providers** like Bing Maps, OpenStreetMap, or Azure Maps
- **Render custom shapes** from GeoJSON data files
- **Build multi-layer maps** with overlays and sublayers
- **Add navigation lines** to show routes or connections between locations
- **Implement zooming and panning** for map exploration
- **Display statistical data** on geographical regions
- **Create interactive legends** for data interpretation
- **Support multiple projections** (Mercator, Miller, Eckert, etc.)
- **Handle user interactions** like tooltips, selection, and highlighting

## Component Overview

The Syncfusion React Maps component is a powerful data visualization tool that renders geographical data using Scalable Vector Graphics (SVG). It supports:

- **Any number of layers and sublayers** for complex visualizations
- **GeoJSON data binding** for custom shape rendering
- **Map providers** (Bing, OpenStreetMap, Azure) as base layers
- **6 types of projections** for different map representations
- **Visual elements**: Markers, Bubbles, Navigation Lines, Annotations, Data Labels, Legends
- **Interactive features**: Zooming, Panning, Tooltips, Selection, Highlighting
- **Accessibility**: WCAG 2.1 compliant with keyboard navigation
- **Globalization**: RTL support, internationalization, localization

## Key Capabilities

### Data Visualization Elements
- **Markers**: Pin locations with custom shapes, templates, and clustering
- **Bubbles**: Display data magnitude with size-based bubbles
- **Data Labels**: Show information directly on map shapes
- **Color Mapping**: Apply colors based on data values (equal, range, desaturation)
- **Navigation Lines**: Draw connections between locations with curves and arrows
- **Legends**: Provide visual keys for data interpretation

### Layer Architecture
- **Main Layer**: Base map from GeoJSON or map provider
- **Sublayers**: Overlay additional shapes on top of main layer
- **Multi-layer Support**: Stack multiple layers for rich visualizations

### Map Providers
- **Bing Maps**: Satellite, aerial, and road views
- **OpenStreetMap**: Free tile layer provider
- **Azure Maps**: Microsoft's map service
- **Hybrid Approach**: Combine GeoJSON shapes with provider tiles

### User Interactions
- **Zooming**: Mouse wheel, double-click, pinch, toolbar controls
- **Panning**: Drag to explore different regions
- **Tooltips**: Show data on hover
- **Selection**: Highlight shapes on click
- **Reset**: Return to initial view

## Documentation and Navigation Guide

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Complete MapsComponent properties reference
- All available methods with examples
- Comprehensive events documentation
- Layer, marker, bubble, and data label settings
- Legend, zoom, and tooltip configuration
- Quick reference code examples
- Type definitions and parameters

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package dependencies
- Basic Maps component implementation
- GeoJSON data structure and binding
- CSS theme imports
- Module injection pattern (feature-based)
- First world map example
- Data source binding with shapeDataPath and shapePropertyPath

### Layers and Structure
📄 **Read:** [references/layers-and-sublayers.md](references/layers-and-sublayers.md)
- Understanding layer architecture
- Main layer vs sublayer differences
- Creating multi-layer maps
- Layer types and stacking order
- Layer-specific settings and configuration
- When to use multiple layers

### Markers
📄 **Read:** [references/markers.md](references/markers.md)
- Adding markers to pinpoint locations
- Marker data source structure (latitude, longitude)
- Marker shapes and custom templates
- Marker clustering for dense data
- Dynamic marker updates
- Interactive markers with click events
- Marker tooltips and labels

### Data Visualization Elements
📄 **Read:** [references/data-visualization.md](references/data-visualization.md)
- Bubble visualization for data magnitude
- Configuring bubble size and colors
- Data label setup and formatting
- Smart label modes (trim, hide, none)
- Label templates for custom content
- Combining bubbles with data labels
- Best practices for visual hierarchy

### Legend
📄 **Read:** [references/legend.md](references/legend.md)
- Enabling and configuring legends
- Positioning strategies (absolute, dock)
- Legend alignment options (near, center, far)
- Interactive legends
- Legend modes (default, interactive)
- Customizing legend appearance
- Syncing legends with color mapping

### Color Mapping
📄 **Read:** [references/color-mapping.md](references/color-mapping.md)
- Color mapping types (equal, range, desaturation)
- Applying colors based on data values
- Setting up colorValuePath
- Creating choropleth maps
- Multiple color mapping rules
- Custom color schemes
- Visual data representation strategies

### Navigation Lines
📄 **Read:** [references/navigation-lines.md](references/navigation-lines.md)
- Creating lines between locations
- Line styling (width, color, dash array)
- Curved lines and angles
- Arrow indicators for direction
- Use cases (routes, connections, flows)
- Animation effects on lines

### Map Providers
📄 **Read:** [references/map-providers.md](references/map-providers.md)
- Overview of supported providers
- When to use GeoJSON vs map providers
- Bing Maps setup and API keys
- OpenStreetMap integration (free)
- Azure Maps configuration
- Tile layer types (satellite, aerial, road)
- Hybrid approaches (GeoJSON overlays on provider tiles)

### User Interactions
📄 **Read:** [references/user-interactions.md](references/user-interactions.md)
- Enabling and configuring zooming
- Zoom factor and toolbar controls
- Panning functionality
- Tooltip configuration and templates
- Selection and highlighting shapes
- Mouse wheel and double-click zoom
- Pinch zoom for touch devices
- Reset to initial view

### Annotations and Polygons
📄 **Read:** [references/annotations-polygon.md](references/annotations-polygon.md)
- Adding custom annotations to maps
- Polygon rendering for custom shapes
- Positioning and alignment
- Interactive annotations
- Use cases for overlays

### Customization
- Map projections (Mercator, Miller, Eckert, Winkel Tripel, Aitoff, Equirectangular)
- Title and subtitle configuration
- Border and background styling
- Margin and padding adjustments
- Custom CSS classes
- Theme integration
- Responsive design patterns

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Internationalization (i18n)
- Localization (l10n)
- Accessibility (WCAG compliance, keyboard navigation)
- State persistence across sessions
- Printing and export functionality
- Event handling patterns
- Accessing component methods via ref
- Performance optimization techniques
- Migration guide from EJ1 to EJ2

## Quick Start Example

```tsx
import * as React from 'react';
import { MapsComponent, LayersDirective, LayerDirective, Inject, Legend } from '@syncfusion/ej2-react-maps';
import { world_map } from './world-map'; // GeoJSON data

function MapExample() {
  const data = [
    { Country: 'United States', Population: 331000000, Membership: 'Permanent' },
    { Country: 'Russia', Population: 145900000, Membership: 'Permanent' },
    { Country: 'China', Population: 1439000000, Membership: 'Permanent' },
    { Country: 'India', Population: 1380000000, Membership: 'Non-Permanent' },
    { Country: 'Brazil', Population: 212500000, Membership: 'Non-Permanent' }
  ];

  return (
    <MapsComponent
      titleSettings={{ text: 'World Map with Country Membership' }}
      legendSettings={{ visible: true }}
    >
      <Inject services={[Legend]} />
      <LayersDirective>
        <LayerDirective
          shapeData={world_map}
          shapeDataPath='Country'
          shapePropertyPath='name'
          dataSource={data}
          shapeSettings={{
            colorValuePath: 'Membership',
            colorMapping: [
              { value: 'Permanent', color: '#D84444' },
              { value: 'Non-Permanent', color: '#316DB5' }
            ]
          }}
        />
      </LayersDirective>
    </MapsComponent>
  );
}

export default MapExample;
```

## Module Injection Guide

Maps features are modular. Inject only the modules you need:

```tsx
import { 
  MapsComponent, 
  Inject,
  Legend,        // For legends
  DataLabel,     // For data labels
  Marker,        // For markers
  Bubble,        // For bubbles
  MapsTooltip,   // For tooltips
  Zoom,          // For zooming and panning
  Highlight,     // For highlighting shapes
  Selection,     // For selecting shapes
  NavigationLine,// For navigation lines
  Annotations,   // For annotations
  Polygon        // For polygons
} from '@syncfusion/ej2-react-maps';

<MapsComponent>
  <Inject services={[Legend, Marker, MapsTooltip, Zoom]} />
  {/* Your layers */}
</MapsComponent>
```

**Only inject modules for features you're using** to minimize bundle size.

## Common Use Cases

### Choropleth Map (Color-Coded Regions)
**Goal**: Display statistical data with color-coded countries/regions

**Approach**:
1. Bind data source with `dataSource`, `shapeDataPath`, `shapePropertyPath`
2. Configure `shapeSettings.colorValuePath` to specify data field
3. Set up `colorMapping` with value-color pairs
4. Add `Legend` for interpretation

**Example**: Population density map, election results, COVID-19 statistics

---

### Location Markers Map
**Goal**: Show specific locations with custom markers

**Approach**:
1. Add `MarkersDirective` inside `LayerDirective`
2. Provide marker data with latitude/longitude
3. Customize marker shapes, sizes, and templates
4. Add tooltips for marker information

**Example**: Store locator, branch offices, tourist attractions

---

### Multi-Layer Overlay
**Goal**: Highlight specific regions on a base map

**Approach**:
1. First layer: Base map (e.g., entire country)
2. Additional layers with `type="SubLayer"`: Highlighted regions
3. Style sublayers distinctly (different colors, borders)
4. Control layer visibility and order

**Example**: State highlights on country map, sales regions

---

### Route Visualization
**Goal**: Show connections or routes between locations

**Approach**:
1. Add markers for start/end points
2. Use `NavigationLineDirective` to draw lines
3. Configure line curves, arrows, and styling
4. Optionally animate lines

**Example**: Flight routes, shipping lanes, migration patterns

---

### Map Provider Integration
**Goal**: Use real-world satellite/street map as base

**Approach**:
1. Configure layer with `urlTemplate` for provider
2. Set up API keys (Bing, Azure) if required
3. Overlay GeoJSON shapes as sublayers if needed
4. Add markers and labels on top

**Example**: Real estate map, delivery tracking, ride-sharing app

## Decision Trees

### Should I Use GeoJSON or Map Provider?

**Use GeoJSON when**:
- You need custom shapes or boundaries
- Data is region/country-based (choropleth maps)
- No real-world street-level detail needed
- Offline capability required
- Full control over styling and data binding

**Use Map Provider when**:
- Need real-world satellite/aerial imagery
- Street-level detail required
- Real-time map updates desired
- Users expect familiar map interface (like Google Maps)

**Use Both (Hybrid) when**:
- Need real-world base with custom shape overlays
- Combining statistical regions with street context

---

### Which Color Mapping Type?

**Equal Color Mapping**: 
- Use when data has discrete categories (e.g., Membership: Permanent/Non-Permanent)
- Each unique value gets a specific color

**Range Color Mapping**:
- Use when data is numeric and continuous (e.g., Population: 0-1M, 1M-10M, 10M+)
- Values within ranges get assigned colors

**Desaturation Color Mapping**:
- Use for gradient effects based on numeric values
- Single color with varying saturation levels

---

### How Many Layers Should I Use?

**Single Layer**:
- Simple visualizations with one data dimension
- Basic country/region maps
- When all data fits one layer

**Multiple Layers**:
- Highlighting specific regions on base map
- Combining different data sources
- Creating visual depth with overlays
- Showing borders, rivers, cities separately

## Key Props Reference

### MapsComponent
- `titleSettings`: Configure title and subtitle
- `legendSettings`: Legend visibility, position, alignment
- `zoomSettings`: Enable zooming, set initial zoom factor
- `layers`: Array of layer configurations

### LayerDirective
- `shapeData`: GeoJSON data for shapes
- `dataSource`: Data to bind to shapes
- `shapeDataPath`: Field in dataSource matching shapes
- `shapePropertyPath`: Field in GeoJSON matching dataSource
- `shapeSettings`: Fill, border, color mapping
- `type`: "Layer" (main) or "SubLayer" (overlay)
- `markerSettings`: Marker configurations
- `bubbleSettings`: Bubble visualizations
- `dataLabelSettings`: Label configurations
- `tooltipSettings`: Tooltip customization
- `navigationLineSettings`: Line visualizations

### Common Patterns
- **Module Injection**: Only inject needed services to reduce bundle size
- **Data Binding**: Use shapeDataPath + shapePropertyPath for automatic matching
- **Progressive Enhancement**: Start with basic map, add features incrementally
- **Responsive Design**: Maps auto-resize, but test on different viewports

## Troubleshooting Quick Checks

❌ **Map not displaying**: 
- Verify GeoJSON data is correctly imported
- Check console for errors
- Ensure CSS is imported

❌ **Colors not applied**:
- Confirm `shapeDataPath` matches data field name
- Verify `shapePropertyPath` matches GeoJSON property
- Check `colorValuePath` points to correct data field

❌ **Markers not showing**:
- Inject `Marker` service
- Set `visible={true}` in MarkerDirective
- Verify latitude/longitude values are valid

❌ **Zoom not working**:
- Inject `Zoom` service
- Set `zoomSettings.enable={true}`
- Check if `enablePanning` is needed

❌ **Legend not appearing**:
- Inject `Legend` service
- Set `legendSettings.visible={true}`
- Ensure color mapping is configured


## Next Steps

1. **Start Simple**: Begin with getting-started.md for basic map
2. **Add Data**: Follow data-visualization.md for markers/bubbles
3. **Style It**: Use color-mapping.md for choropleth effects
4. **Make Interactive**: Implement user-interactions.md for zoom/pan
5. **Enhance**: Add advanced features as needed

Choose the reference documentation that matches your current implementation phase and specific requirements.
