# Legend in React Maps

## Table of Contents
- [Overview](#overview)
- [Enabling Legend](#enabling-legend)
- [Legend Positioning](#legend-positioning)
- [Legend Modes](#legend-modes)
- [Customizing Appearance](#customizing-appearance)
- [Legend with Color Mapping](#legend-with-color-mapping)
- [Interactive Legends](#interactive-legends)
- [Common Patterns](#common-patterns)
- [Troubleshooting](#troubleshooting)

## Overview

Legends provide a visual key to interpret map data. They explain what colors, shapes, or symbols represent, making maps easier to understand.

**Key Features:**
- Multiple positioning options (Top, Bottom, Left, Right)
- Alignment control (Near, Center, Far)
- Interactive mode for toggling visibility
- Custom styling and templates
- Automatic generation from color mapping

## Enabling Legend

### Basic Legend Setup

```tsx
import {
  MapsComponent,
  LayersDirective,
  LayerDirective,
  Inject,
  Legend
} from '@syncfusion/ej2-react-maps';

function MapWithLegend() {
  const countryData = [
    { name: 'United States', membership: 'Permanent' },
    { name: 'Russia', membership: 'Permanent' },
    { name: 'Brazil', membership: 'Non-Permanent' }
  ];

  return (
    <MapsComponent
      legendSettings={{
        visible: true
      }}
    >
      <Inject services={[Legend]} />
      <LayersDirective>
        <LayerDirective
          shapeData={world_map}
          dataSource={countryData}
          shapeDataPath='name'
          shapePropertyPath='name'
          shapeSettings={{
            colorValuePath: 'membership',
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
```

**Required:**
1. Import and inject `Legend` service
2. Set `legendSettings.visible` to `true`
3. Configure color mapping in layer settings

## Legend Positioning

### Dock Positioning

Position legend at edges of the map:

```tsx
legendSettings={{
  visible: true,
  position: 'Bottom'  // Options: Top, Bottom, Left, Right
}}
```

**Available Positions:**
- `'Top'`: Above the map
- `'Bottom'`: Below the map
- `'Left'`: Left side of map
- `'Right'`: Right side of map

### Alignment

Fine-tune position within the dock:

```tsx
legendSettings={{
  visible: true,
  position: 'Bottom',
  alignment: 'Center'  // Options: Near, Center, Far
}}
```

**Alignment Options:**
- `'Near'`: Start of the position (left for Top/Bottom, top for Left/Right)
- `'Center'`: Middle of the position
- `'Far'`: End of the position (right for Top/Bottom, bottom for Left/Right)

**12 Positioning Combinations:**

```tsx
// Top positions
{ position: 'Top', alignment: 'Near' }    // Top-left
{ position: 'Top', alignment: 'Center' }  // Top-center
{ position: 'Top', alignment: 'Far' }     // Top-right

// Bottom positions
{ position: 'Bottom', alignment: 'Near' }    // Bottom-left
{ position: 'Bottom', alignment: 'Center' }  // Bottom-center (default)
{ position: 'Bottom', alignment: 'Far' }     // Bottom-right

// Left positions
{ position: 'Left', alignment: 'Near' }    // Left-top
{ position: 'Left', alignment: 'Center' }  // Left-center
{ position: 'Left', alignment: 'Far' }     // Left-bottom

// Right positions
{ position: 'Right', alignment: 'Near' }    // Right-top
{ position: 'Right', alignment: 'Center' }  // Right-center
{ position: 'Right', alignment: 'Far' }     // Right-bottom
```

### Absolute Positioning

Place legend at specific coordinates:

```tsx
legendSettings={{
  visible: true,
  position: 'Float',
  location: { x: 10, y: 10 }  // X, Y coordinates in pixels
}}
```

**Use cases for absolute positioning:**
- Custom layouts
- Overlaying legend on map
- Precise placement requirements

## Legend Modes

### Default Mode

Standard legend display:

```tsx
legendSettings={{
  visible: true,
  mode: 'Default'  // Static legend
}}
```

### Interactive Mode

Allow users to toggle layer visibility by clicking legend items:

```tsx
legendSettings={{
  visible: true,
  mode: 'Interactive',
  toggleVisibility: true  // Enable click to hide/show
}}
```

**Interactive behavior:**
- Click legend item to toggle shape visibility
- Useful for comparing different data categories
- Visual feedback on active/inactive items

## Customizing Appearance

### Legend Size and Shape

```tsx
legendSettings={{
  visible: true,
  height: '60px',
  width: '300px',
  shape: 'Circle',  // Options: Circle, Rectangle, Triangle, Diamond, 
                    // Cross, Star, Pentagon, InvertedTriangle
  shapeHeight: 20,
  shapeWidth: 20,
  shapePadding: 10
}}
```

### Text Styling

```tsx
legendSettings={{
  visible: true,
  textStyle: {
    size: '14px',
    color: '#000000',
    fontFamily: 'Arial',
    fontWeight: 'Normal',
    fontStyle: 'Normal',
    opacity: 1
  }
}}
```

### Legend Border and Background

```tsx
legendSettings={{
  visible: true,
  background: '#FFFFFF',
  border: {
    color: '#CCCCCC',
    width: 2
  },
  opacity: 0.95
}}
```

### Orientation

```tsx
legendSettings={{
  visible: true,
  orientation: 'Horizontal'  // Options: Horizontal, Vertical
}}
```

### Title

Add a title to the legend:

```tsx
legendSettings={{
  visible: true,
  title: {
    text: 'Country Membership Status',
    description: 'UN Security Council',
    textStyle: {
      size: '16px',
      fontWeight: 'Bold',
      color: '#333333'
    }
  }
}}
```

## Legend with Color Mapping

### Equal Color Mapping

Discrete categories:

```tsx
function CategoryLegend() {
  return (
    <MapsComponent
      legendSettings={{
        visible: true,
        position: 'Bottom',
        shape: 'Circle',
        shapeHeight: 15,
        shapeWidth: 15
      }}
    >
      <Inject services={[Legend]} />
      <LayersDirective>
        <LayerDirective
          shapeData={world_map}
          dataSource={membershipData}
          shapeDataPath='country'
          shapePropertyPath='name'
          shapeSettings={{
            colorValuePath: 'membership',
            colorMapping: [
              { value: 'Permanent', color: '#D84444', label: 'Permanent Member' },
              { value: 'Non-Permanent', color: '#316DB5', label: 'Non-Permanent Member' },
              { value: 'Observer', color: '#FFD700', label: 'Observer Status' }
            ]
          }}
        />
      </LayersDirective>
    </MapsComponent>
  );
}
```

### Range Color Mapping

Numeric ranges with legend labels:

```tsx
function RangeLegend() {
  return (
    <MapsComponent
      legendSettings={{
        visible: true,
        position: 'Right',
        alignment: 'Center',
        orientation: 'Vertical',
        title: {
          text: 'Population (millions)'
        }
      }}
    >
      <Inject services={[Legend]} />
      <LayersDirective>
        <LayerDirective
          shapeData={world_map}
          dataSource={populationData}
          shapeDataPath='country'
          shapePropertyPath='name'
          shapeSettings={{
            colorValuePath: 'population',
            colorMapping: [
              { from: 0, to: 10000000, color: '#C3E6CB', label: '< 10M' },
              { from: 10000000, to: 100000000, color: '#6AB187', label: '10M - 100M' },
              { from: 100000000, to: 500000000, color: '#4A9068', label: '100M - 500M' },
              { from: 500000000, to: 2000000000, color: '#2F7C4F', label: '> 500M' }
            ]
          }}
        />
      </LayersDirective>
    </MapsComponent>
  );
}
```

### Custom Labels

Override automatic legend labels:

```tsx
shapeSettings={{
  colorValuePath: 'gdp',
  colorMapping: [
    { from: 0, to: 1000, color: '#FFE5B4', label: 'Low Income' },
    { from: 1000, to: 5000, color: '#FFB347', label: 'Lower Middle Income' },
    { from: 5000, to: 20000, color: '#FF8C00', label: 'Upper Middle Income' },
    { from: 20000, to: 100000, color: '#FF6347', label: 'High Income' }
  ]
}}
```

## Interactive Legends

### Toggle Visibility Example

```tsx
function InteractiveLegendMap() {
  return (
    <MapsComponent
      legendSettings={{
        visible: true,
        mode: 'Interactive',
        toggleVisibility: true,
        position: 'Bottom',
        alignment: 'Center',
        textStyle: {
          size: '13px'
        }
      }}
    >
      <Inject services={[Legend]} />
      <LayersDirective>
        <LayerDirective
          shapeData={world_map}
          dataSource={continentData}
          shapeDataPath='continent'
          shapePropertyPath='continent'
          shapeSettings={{
            colorValuePath: 'continent',
            colorMapping: [
              { value: 'Asia', color: '#FF6B6B' },
              { value: 'Africa', color: '#4ECDC4' },
              { value: 'Europe', color: '#45B7D1' },
              { value: 'North America', color: '#FFA07A' },
              { value: 'South America', color: '#98D8C8' },
              { value: 'Australia', color: '#F7DC6F' }
            ]
          }}
        />
      </LayersDirective>
    </MapsComponent>
  );
}
```

**User interaction:**
- Click "Asia" in legend → Hides Asian countries
- Click again → Shows Asian countries
- Helps focus on specific data categories

## Common Patterns

### Pattern 1: Horizontal Legend at Bottom

Most common placement for choropleth maps:

```tsx
legendSettings={{
  visible: true,
  position: 'Bottom',
  alignment: 'Center',
  orientation: 'Horizontal',
  shape: 'Rectangle',
  shapeHeight: 12,
  shapeWidth: 30,
  shapePadding: 8,
  textStyle: {
    size: '12px'
  },
  border: {
    color: '#E0E0E0',
    width: 1
  }
}}
```

### Pattern 2: Vertical Legend on Right

Good for narrow maps or many categories:

```tsx
legendSettings={{
  visible: true,
  position: 'Right',
  alignment: 'Center',
  orientation: 'Vertical',
  shape: 'Circle',
  shapeHeight: 15,
  shapeWidth: 15,
  height: '300px',
  width: '150px'
}}
```

### Pattern 3: Compact Legend with Title

```tsx
legendSettings={{
  visible: true,
  position: 'Top',
  alignment: 'Far',
  orientation: 'Horizontal',
  title: {
    text: 'Legend',
    textStyle: {
      size: '14px',
      fontWeight: 'Bold'
    }
  },
  shapeHeight: 10,
  shapeWidth: 10,
  shapePadding: 5,
  textStyle: {
    size: '11px'
  }
}}
```

### Pattern 4: Floating Legend with Custom Position

```tsx
legendSettings={{
  visible: true,
  position: 'Float',
  location: { x: 20, y: 20 },
  background: 'rgba(255, 255, 255, 0.9)',
  border: {
    color: '#333333',
    width: 1
  },
  shape: 'Circle',
  shapeHeight: 12,
  shapeWidth: 12
}}
```

## Troubleshooting

### Issue: Legend not appearing

**Causes & Solutions:**

1. **Forgot to inject Legend service**
```tsx
// ✅ Correct
<MapsComponent>
  <Inject services={[Legend]} />
</MapsComponent>

// ❌ Wrong
<MapsComponent>
  {/* Missing injection */}
</MapsComponent>
```

2. **visible not set to true**
```tsx
// ✅ Correct
legendSettings={{ visible: true }}

// ❌ Wrong
legendSettings={{}}  // visible defaults to false
```

3. **No color mapping configured**
```tsx
// ✅ Correct - legend needs color mapping to display
shapeSettings={{
  colorMapping: [
    { value: 'Category1', color: '#FF0000' }
  ]
}}

// ❌ Wrong - no color mapping
shapeSettings={{}}
```

### Issue: Legend items not matching colors

**Cause:** colorValuePath doesn't match data field

**Solution:**
```tsx
// Ensure colorValuePath matches your data field
shapeSettings={{
  colorValuePath: 'status',  // Must match data field name exactly
  colorMapping: [
    { value: 'Active', color: '#00FF00' }
  ]
}}
```

### Issue: Legend text cut off

**Solutions:**
- Increase legend width: `width: '400px'`
- Reduce text size: `textStyle: { size: '10px' }`
- Use shorter labels in colorMapping

### Issue: Interactive legend not working

**Cause:** Missing mode or toggleVisibility

**Solution:**
```tsx
// ✅ Correct
legendSettings={{
  visible: true,
  mode: 'Interactive',
  toggleVisibility: true
}}

// ❌ Wrong
legendSettings={{
  visible: true
  // Missing mode and toggleVisibility
}}
```

### Issue: Legend overlapping map content

**Solutions:**
1. Adjust alignment and position
2. Use Float mode with custom location
3. Increase map container padding
4. Make legend background semi-transparent

```tsx
legendSettings={{
  visible: true,
  position: 'Float',
  location: { x: 10, y: 10 },
  background: 'rgba(255, 255, 255, 0.9)'  // Semi-transparent
}}
```

## Complete Example

```tsx
function CompleteLegendMap() {
  const economicData = [
    { country: 'United States', gdp: 21427, classification: 'Developed' },
    { country: 'China', gdp: 14343, classification: 'Developing' },
    { country: 'Japan', gdp: 5082, classification: 'Developed' },
    { country: 'Germany', gdp: 3846, classification: 'Developed' },
    { country: 'India', gdp: 2875, classification: 'Developing' }
  ];

  return (
    <MapsComponent
      titleSettings={{
        text: 'World GDP by Country Classification',
        textStyle: { size: '18px', fontWeight: 'Bold' }
      }}
      legendSettings={{
        visible: true,
        mode: 'Interactive',
        toggleVisibility: true,
        position: 'Bottom',
        alignment: 'Center',
        orientation: 'Horizontal',
        shape: 'Rectangle',
        shapeHeight: 15,
        shapeWidth: 40,
        shapePadding: 10,
        title: {
          text: 'Country Classification',
          textStyle: {
            size: '14px',
            fontWeight: 'Bold',
            color: '#333'
          }
        },
        textStyle: {
          size: '13px',
          color: '#666'
        },
        border: {
          color: '#E0E0E0',
          width: 1
        },
        background: '#FAFAFA'
      }}
    >
      <Inject services={[Legend]} />
      <LayersDirective>
        <LayerDirective
          shapeData={world_map}
          dataSource={economicData}
          shapeDataPath='country'
          shapePropertyPath='name'
          shapeSettings={{
            fill: '#E5E5E5',
            colorValuePath: 'classification',
            colorMapping: [
              { 
                value: 'Developed', 
                color: '#4CAF50', 
                label: 'Developed Countries' 
              },
              { 
                value: 'Developing', 
                color: '#FF9800', 
                label: 'Developing Countries' 
              }
            ],
            border: {
              width: 0.5,
              color: '#CCCCCC'
            }
          }}
        />
      </LayersDirective>
    </MapsComponent>
  );
}
```
