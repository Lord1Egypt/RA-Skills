# Data Visualization Elements in React Maps

## Table of Contents
- [Overview](#overview)
- [Bubbles](#bubbles)
- [Data Labels](#data-labels)
- [Smart Label Modes](#smart-label-modes)
- [Label Templates](#label-templates)
- [Combining Bubbles and Labels](#combining-bubbles-and-labels)
- [Visual Hierarchy Best Practices](#visual-hierarchy-best-practices)
- [Heatmap Layer](#heatmap-layer)
- [Common Use Cases](#common-use-cases)
- [Troubleshooting](#troubleshooting)

## Overview

Data visualization elements help display quantitative information directly on maps. Two primary elements:

- **Bubbles**: Size-based visualization showing data magnitude
- **Data Labels**: Text labels displaying information on shapes

## Bubbles

Bubbles visualize data magnitude using proportional circles. Larger values = larger bubbles.

### Enabling Bubbles

```tsx
import {
  MapsComponent,
  LayersDirective,
  LayerDirective,
  BubblesDirective,
  BubbleDirective,
  Inject,
  Bubble
} from '@syncfusion/ej2-react-maps';

function BubbleMap() {
  const populationData = [
    { name: 'India', population: 1380000000, latitude: 20.5937, longitude: 78.9629 },
    { name: 'China', population: 1439000000, latitude: 35.8617, longitude: 104.1954 },
    { name: 'USA', population: 331000000, latitude: 37.0902, longitude: -95.7129 }
  ];

  return (
    <MapsComponent>
      <Inject services={[Bubble]} />
      <LayersDirective>
        <LayerDirective shapeData={world_map}>
          <BubblesDirective>
            <BubbleDirective
              visible={true}
              dataSource={populationData}
              valuePath='population'
              minRadius={10}
              maxRadius={40}
              fill='#FF6347'
              opacity={0.6}
            />
          </BubblesDirective>
        </LayerDirective>
      </LayersDirective>
    </MapsComponent>
  );
}
```

### Bubble Configuration

```tsx
<BubbleDirective
  visible={true}
  dataSource={data}
  valuePath='population'        // Field determining bubble size
  minRadius={5}                 // Minimum bubble size (px)
  maxRadius={50}                // Maximum bubble size (px)
  fill='#4CAF50'                // Bubble color
  opacity={0.7}                 // Transparency (0-1)
  border={{
    color: '#2E7D32',
    width: 1
  }}
  animationDuration={1000}      // Animation duration (ms)
  animationDelay={0}            // Delay before animation
/>
```

### Bubble Color Mapping

Apply different colors based on value ranges:

```tsx
<BubbleDirective
  visible={true}
  dataSource={cityData}
  valuePath='population'
  minRadius={10}
  maxRadius={40}
  colorValuePath='population'
  colorMapping={[
    { from: 0, to: 1000000, color: '#C3E6CB' },
    { from: 1000000, to: 5000000, color: '#6AB187' },
    { from: 5000000, to: 50000000, color: '#2F7C4F' }
  ]}
/>
```

### Multiple Bubble Sets

Display different datasets:

```tsx
<LayerDirective shapeData={world_map}>
  <BubblesDirective>
    {/* Population bubbles */}
    <BubbleDirective
      visible={true}
      dataSource={populationData}
      valuePath='population'
      fill='#2196F3'
      minRadius={10}
      maxRadius={40}
    />
    
    {/* GDP bubbles */}
    <BubbleDirective
      visible={true}
      dataSource={gdpData}
      valuePath='gdp'
      fill='#FF9800'
      minRadius={8}
      maxRadius={35}
    />
  </BubblesDirective>
</LayerDirective>
```

### Bubble Tooltips

```tsx
<MapsComponent>
  <Inject services={[Bubble, MapsTooltip]} />
  <LayersDirective>
    <LayerDirective shapeData={world_map}>
      <BubblesDirective>
        <BubbleDirective
          visible={true}
          dataSource={data}
          valuePath='population'
          tooltipSettings={{
            visible: true,
            valuePath: 'name',
            format: '${name}<br/>Population: ${population}'
          }}
          minRadius={10}
          maxRadius={40}
        />
      </BubblesDirective>
    </LayerDirective>
  </LayersDirective>
</MapsComponent>
```

## Data Labels

Display text information directly on map shapes.

### Basic Data Labels

```tsx
import {
  MapsComponent,
  LayersDirective,
  LayerDirective,
  Inject,
  DataLabel
} from '@syncfusion/ej2-react-maps';

function DataLabelMap() {
  return (
    <MapsComponent>
      <Inject services={[DataLabel]} />
      <LayersDirective>
        <LayerDirective
          shapeData={world_map}
          dataLabelSettings={{
            visible: true,
            labelPath: 'name',          // Field from GeoJSON properties
            smartLabelMode: 'Trim'
          }}
        />
      </LayersDirective>
    </MapsComponent>
  );
}
```

### Data Label Configuration

```tsx
dataLabelSettings={{
  visible: true,
  labelPath: 'name',               // Data field to display
  smartLabelMode: 'Trim',          // Trim, Hide, or None
  intersectionAction: 'Hide',      // Hide overlapping labels
  textStyle: {
    size: '12px',
    color: '#000000',
    fontFamily: 'Arial',
    fontWeight: 'Normal',
    fontStyle: 'Normal',
    opacity: 1
  },
  border: {
    color: '#FFFFFF',
    width: 1
  }
}}
```

### Data Labels with Custom Data

```tsx
function CustomDataLabelMap() {
  const countryData = [
    { name: 'United States', code: 'USA', population: '331M' },
    { name: 'China', code: 'CHN', population: '1.4B' },
    { name: 'India', code: 'IND', population: '1.4B' }
  ];

  return (
    <MapsComponent>
      <Inject services={[DataLabel]} />
      <LayersDirective>
        <LayerDirective
          shapeData={world_map}
          dataSource={countryData}
          shapeDataPath='name'
          shapePropertyPath='name'
          dataLabelSettings={{
            visible: true,
            labelPath: 'code',        // Display country codes
            smartLabelMode: 'Trim',
            textStyle: {
              size: '14px',
              fontWeight: 'Bold',
              color: '#FFFFFF'
            }
          }}
        />
      </LayersDirective>
    </MapsComponent>
  );
}
```

## Smart Label Modes

Control how labels behave when space is limited.

### Trim Mode

Truncates text with ellipsis when it doesn't fit:

```tsx
dataLabelSettings={{
  visible: true,
  labelPath: 'name',
  smartLabelMode: 'Trim'
}}
```

**Result**: "United States of America" → "United States..."

### Hide Mode

Hides labels that don't fit:

```tsx
dataLabelSettings={{
  visible: true,
  labelPath: 'name',
  smartLabelMode: 'Hide'
}}
```

**Result**: Small shapes may have no label visible.

### None Mode

Shows full text regardless of space:

```tsx
dataLabelSettings={{
  visible: true,
  labelPath: 'name',
  smartLabelMode: 'None'
}}
```

**Result**: Text may overlap or extend beyond shape.

### Intersection Action

Control overlapping labels:

```tsx
dataLabelSettings={{
  visible: true,
  labelPath: 'name',
  smartLabelMode: 'Trim',
  intersectionAction: 'Hide'  // Options: Hide, Trim, None
}}
```

## Label Templates

Create custom label designs:

```tsx
function TemplateLabelMap() {
  const labelTemplate = (props) => {
    return (
      <div style={{
        backgroundColor: 'rgba(0, 0, 0, 0.7)',
        color: 'white',
        padding: '4px 8px',
        borderRadius: '4px',
        fontSize: '11px',
        fontWeight: 'bold',
        border: '1px solid white'
      }}>
        {props.name}
        <div style={{ fontSize: '9px', opacity: 0.8 }}>
          Pop: {props.population}
        </div>
      </div>
    );
  };

  return (
    <MapsComponent>
      <Inject services={[DataLabel]} />
      <LayersDirective>
        <LayerDirective
          shapeData={world_map}
          dataSource={countryData}
          shapeDataPath='name'
          shapePropertyPath='name'
          dataLabelSettings={{
            visible: true,
            template: labelTemplate
          }}
        />
      </LayersDirective>
    </MapsComponent>
  );
}
```

### Conditional Label Styling

```tsx
const conditionalLabelTemplate = (props) => {
  const isHighPopulation = props.population > 100000000;
  
  return (
    <div style={{
      backgroundColor: isHighPopulation ? '#FF6347' : '#4CAF50',
      color: 'white',
      padding: '3px 6px',
      borderRadius: '3px',
      fontSize: isHighPopulation ? '12px' : '10px',
      fontWeight: isHighPopulation ? 'bold' : 'normal'
    }}>
      {props.name}
    </div>
  );
};
```

## Combining Bubbles and Labels

Display both bubbles and labels for rich visualization:

```tsx
function CombinedVisualization() {
  const cityData = [
    { 
      name: 'Tokyo', 
      latitude: 35.6762, 
      longitude: 139.6503, 
      population: 37400000 
    },
    { 
      name: 'Delhi', 
      latitude: 28.7041, 
      longitude: 77.1025, 
      population: 30290000 
    },
    { 
      name: 'Shanghai', 
      latitude: 31.2304, 
      longitude: 121.4737, 
      population: 27058000 
    }
  ];

  return (
    <MapsComponent>
      <Inject services={[Bubble, DataLabel, MapsTooltip]} />
      <LayersDirective>
        <LayerDirective
          shapeData={world_map}
          dataLabelSettings={{
            visible: true,
            labelPath: 'name',
            smartLabelMode: 'Trim',
            textStyle: {
              size: '10px',
              color: '#333333'
            }
          }}
        >
          <BubblesDirective>
            <BubbleDirective
              visible={true}
              dataSource={cityData}
              valuePath='population'
              minRadius={15}
              maxRadius={50}
              fill='#FF6347'
              opacity={0.5}
              tooltipSettings={{
                visible: true,
                valuePath: 'name',
                format: '${name}<br/>Population: ${population}'
              }}
            />
          </BubblesDirective>
        </LayerDirective>
      </LayersDirective>
    </MapsComponent>
  );
}
```

## Visual Hierarchy Best Practices

### 1. Use Appropriate Sizes

```tsx
// Small labels for dense areas
dataLabelSettings={{
  textStyle: { size: '8px' }
}}

// Large labels for emphasis
dataLabelSettings={{
  textStyle: { size: '14px', fontWeight: 'Bold' }
}}
```

### 2. Color Contrast

```tsx
// Light labels on dark shapes
dataLabelSettings={{
  textStyle: {
    color: '#FFFFFF'
  }
}}

// Dark labels on light shapes
dataLabelSettings={{
  textStyle: {
    color: '#000000'
  }
}}

// Add border for better visibility
dataLabelSettings={{
  textStyle: {
    color: '#FFFFFF'
  },
  border: {
    color: '#000000',
    width: 1
  }
}}
```

### 3. Bubble Opacity

```tsx
// Semi-transparent for overlapping bubbles
<BubbleDirective
  opacity={0.6}  // Allows seeing shapes behind
  fill='#2196F3'
/>

// Solid for emphasis
<BubbleDirective
  opacity={1}
  fill='#FF6347'
/>
```

### 4. Layering Order

```tsx
// Bubbles first (background), then labels (foreground)
<LayerDirective shapeData={world_map}>
  <BubblesDirective>
    <BubbleDirective visible={true} dataSource={data} />
  </BubblesDirective>
  
  {/* Labels render on top of bubbles */}
</LayerDirective>
```

## Heatmap Layer

Heatmaps visualize density/intensity directly on the map using color gradients.
React Maps supports heat map configurations via colorMapping.

```tsx
<LayerDirective
   shapeData={world_map}
   dataSource={heatData}
   shapeSettings={{
      colorValuePath: "intensity",
      colorMapping: [
        { from: 0, to: 10, color: "#ffeeee" },
        { from: 10, to: 50, color: "#ff0000" }
      ]
   }}
/>
```

## Common Use Cases

### Population Density Map

```tsx
function PopulationDensityMap() {
  const densityData = [
    { country: 'Monaco', density: 26337, latitude: 43.7384, longitude: 7.4246 },
    { country: 'Singapore', density: 8358, latitude: 1.3521, longitude: 103.8198 },
    { country: 'Bangladesh', density: 1265, latitude: 23.6850, longitude: 90.3563 }
  ];

  return (
    <MapsComponent
      titleSettings={{ text: 'Population Density by Country' }}
    >
      <Inject services={[Bubble, DataLabel, MapsTooltip, Legend]} />
      <LayersDirective>
        <LayerDirective
          shapeData={world_map}
          dataLabelSettings={{
            visible: true,
            labelPath: 'name',
            smartLabelMode: 'Trim',
            textStyle: { size: '10px' }
          }}
        >
          <BubblesDirective>
            <BubbleDirective
              visible={true}
              dataSource={densityData}
              valuePath='density'
              minRadius={10}
              maxRadius={50}
              colorValuePath='density'
              colorMapping={[
                { from: 0, to: 100, color: '#C3E6CB', label: 'Low' },
                { from: 100, to: 1000, color: '#6AB187', label: 'Medium' },
                { from: 1000, to: 30000, color: '#2F7C4F', label: 'High' }
              ]}
              tooltipSettings={{
                visible: true,
                format: '${country}<br/>Density: ${density} per km²'
              }}
            />
          </BubblesDirective>
        </LayerDirective>
      </LayersDirective>
    </MapsComponent>
  );
}
```

### Sales Performance Map

```tsx
function SalesMap() {
  const salesData = [
    { region: 'North', sales: 5000000, code: 'NR' },
    { region: 'South', sales: 3500000, code: 'SR' },
    { region: 'East', sales: 4200000, code: 'ER' },
    { region: 'West', sales: 4800000, code: 'WR' }
  ];

  const labelTemplate = (props) => {
    return (
      <div style={{ textAlign: 'center' }}>
        <div style={{
          fontSize: '16px',
          fontWeight: 'bold',
          color: '#2196F3'
        }}>
          {props.code}
        </div>
        <div style={{
          fontSize: '11px',
          color: '#666'
        }}>
          ${(props.sales / 1000000).toFixed(1)}M
        </div>
      </div>
    );
  };

  return (
    <MapsComponent>
      <Inject services={[DataLabel]} />
      <LayersDirective>
        <LayerDirective
          shapeData={regionMap}
          dataSource={salesData}
          shapeDataPath='region'
          shapePropertyPath='name'
          shapeSettings={{
            colorValuePath: 'sales',
            colorMapping={[
              { from: 0, to: 4000000, color: '#FFE5B4' },
              { from: 4000000, to: 6000000, color: '#FF8C00' }
            ]}
          }}
          dataLabelSettings={{
            visible: true,
            template: labelTemplate
          }}
        />
      </LayersDirective>
    </MapsComponent>
  );
}
```

## Troubleshooting

### Issue: Bubbles not appearing

**Solutions:**
1. Inject `Bubble` service
2. Set `visible={true}`
3. Ensure data has latitude/longitude fields
4. Check `valuePath` matches data field

```tsx
// ✅ Correct
<MapsComponent>
  <Inject services={[Bubble]} />
  <BubbleDirective visible={true} valuePath='population' dataSource={data} />
</MapsComponent>
```

### Issue: Data labels not showing

**Solutions:**
1. Inject `DataLabel` service
2. Set `visible={true}`
3. Verify `labelPath` matches GeoJSON property or data field

```tsx
// ✅ Correct
<MapsComponent>
  <Inject services={[DataLabel]} />
  <LayerDirective
    dataLabelSettings={{ visible: true, labelPath: 'name' }}
  />
</MapsComponent>
```

### Issue: Labels overlapping or cut off

**Solutions:**
- Use `smartLabelMode: 'Trim'` or `'Hide'`
- Reduce font size
- Set `intersectionAction: 'Hide'`
- Increase map size

### Issue: Bubble sizes not varying

**Cause:** minRadius and maxRadius too close

**Solution:**
```tsx
// ✅ Good range
<BubbleDirective minRadius={10} maxRadius={50} />

// ❌ Too close
<BubbleDirective minRadius={20} maxRadius={22} />
```

