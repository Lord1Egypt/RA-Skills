# Color Mapping in React Maps

## Table of Contents
- [Overview](#overview)
- [Equal Color Mapping](#equal-color-mapping)
- [Range Color Mapping](#range-color-mapping)
- [Desaturation Color Mapping](#desaturation-color-mapping)
- [Color Value Path](#color-value-path)
- [Custom Color Schemes](#custom-color-schemes)
- [Visual Strategies](#visual-strategies)
- [Common Use Cases](#common-use-cases)
- [Troubleshooting](#troubleshooting)

## Overview

Color mapping applies colors to map shapes based on data values, creating choropleth maps for visual data analysis.

**Three Types:**
1. **Equal**: Discrete categories (e.g., countries by continent)
2. **Range**: Numeric ranges (e.g., population brackets)
3. **Desaturation**: Gradient based on values (e.g., temperature scale)

## Equal Color Mapping

Assign specific colors to distinct categorical values.

### Basic Example

```tsx
function CategoricalMap() {
  const membershipData = [
    { name: 'United States', membership: 'Permanent' },
    { name: 'France', membership: 'Permanent' },
    { name: 'Brazil', membership: 'Non-Permanent' },
    { name: 'Germany', membership: 'Observer' }
  ];

  return (
    <MapsComponent>
      <LayersDirective>
        <LayerDirective
          shapeData={world_map}
          dataSource={membershipData}
          shapeDataPath='name'
          shapePropertyPath='name'
          shapeSettings={{
            colorValuePath: 'membership',
            colorMapping: [
              { value: 'Permanent', color: '#D84444' },
              { value: 'Non-Permanent', color: '#316DB5' },
              { value: 'Observer', color: '#FFD700' }
            ]
          }}
        />
      </LayersDirective>
    </MapsComponent>
  );
}
```

### With Legend Labels

```tsx
colorMapping: [
  { value: 'Permanent', color: '#D84444', label: 'Permanent Member' },
  { value: 'Non-Permanent', color: '#316DB5', label: 'Non-Permanent Member' },
  { value: 'Observer', color: '#FFD700', label: 'Observer Status' }
]
```

### Multiple Categories Example

```tsx
const continentData = [
  { country: 'United States', continent: 'North America' },
  { country: 'Brazil', continent: 'South America' },
  { country: 'China', continent: 'Asia' },
  { country: 'France', continent: 'Europe' },
  { country: 'Nigeria', continent: 'Africa' },
  { country: 'Australia', continent: 'Australia' }
];

<LayerDirective
  shapeData={world_map}
  dataSource={continentData}
  shapeDataPath='country'
  shapePropertyPath='name'
  shapeSettings={{
    colorValuePath: 'continent',
    colorMapping: [
      { value: 'Asia', color: '#FF6B6B' },
      { value: 'Africa', color: '#4ECDC4' },
      { value: 'Europe', color: '#45B7D1' },
      { value: 'North America', color: '#FFA07A' },
      { value: 'South America', color: '#98D8C8' },
      { value: 'Australia', color: '#F7DC6F' },
      { value: 'Antarctica', color: '#E8E8E8' }
    ]
  }}
/>
```

## Range Color Mapping

Apply colors based on numeric value ranges.

### Basic Range Example

```tsx
function PopulationMap() {
  const populationData = [
    { country: 'China', population: 1439323776 },
    { country: 'India', population: 1380004385 },
    { country: 'United States', population: 331002651 },
    { country: 'Indonesia', population: 273523615 },
    { country: 'Iceland', population: 341243 }
  ];

  return (
    <MapsComponent>
      <Inject services={[Legend]} />
      <LayersDirective>
        <LayerDirective
          shapeData={world_map}
          dataSource={populationData}
          shapeDataPath='country'
          shapePropertyPath='name'
          shapeSettings={{
            fill: '#E5E5E5',  // Default color for unmatched shapes
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

### GDP Classification

```tsx
colorMapping: [
  { from: 0, to: 1000, color: '#FFE5B4', label: 'Low Income' },
  { from: 1000, to: 4000, color: '#FFB347', label: 'Lower Middle' },
  { from: 4000, to: 12000, color: '#FF8C00', label: 'Upper Middle' },
  { from: 12000, to: 100000, color: '#FF6347', label: 'High Income' }
]
```

### Temperature Range

```tsx
colorMapping: [
  { from: -50, to: 0, color: '#0000FF', label: 'Freezing' },
  { from: 0, to: 10, color: '#4169E1', label: 'Cold' },
  { from: 10, to: 20, color: '#87CEEB', label: 'Cool' },
  { from: 20, to: 30, color: '#FFD700', label: 'Warm' },
  { from: 30, to: 40, color: '#FF8C00', label: 'Hot' },
  { from: 40, to: 60, color: '#FF0000', label: 'Very Hot' }
]
```

## Desaturation Color Mapping

Create gradient effect using single color with varying intensity.

### Basic Desaturation

```tsx
function DensityMap() {
  const densityData = [
    { country: 'Monaco', density: 26337 },
    { country: 'Singapore', density: 8358 },
    { country: 'Bangladesh', density: 1265 },
    { country: 'United States', density: 36 },
    { country: 'Mongolia', density: 2 }
  ];

  return (
    <MapsComponent>
      <LayersDirective>
        <LayerDirective
          shapeData={world_map}
          dataSource={densityData}
          shapeDataPath='country'
          shapePropertyPath='name'
          shapeSettings={{
            fill: '#E5E5E5',
            colorValuePath: 'density',
            colorMapping: [
              { 
                from: 0, 
                to: 30000, 
                color: '#2E7D32',  // Base color
                minOpacity: 0.2,   // Lowest density
                maxOpacity: 1      // Highest density
              }
            ]
          }}
        />
      </LayersDirective>
    </MapsComponent>
  );
}
```

**How it works:**
- Single color with varying opacity/saturation
- Lower values = lighter shade
- Higher values = darker shade
- Smooth gradient effect

### Multiple Desaturation Ranges

```tsx
colorMapping: [
  { from: 0, to: 100, color: '#4CAF50', minOpacity: 0.2, maxOpacity: 0.6 },
  { from: 100, to: 1000, color: '#FF9800', minOpacity: 0.4, maxOpacity: 0.8 },
  { from: 1000, to: 30000, color: '#F44336', minOpacity: 0.6, maxOpacity: 1 }
]
```

## Color Value Path

Specifies which data field determines the color.

### Single Field

```tsx
shapeSettings={{
  colorValuePath: 'population',  // Uses population field
  colorMapping: [...]
}}
```

### Nested Field

```tsx
const data = [
  { 
    country: 'USA', 
    statistics: { 
      economy: { gdp: 21427 } 
    } 
  }
];

shapeSettings={{
  colorValuePath: 'statistics.economy.gdp',  // Nested path
  colorMapping: [...]
}}
```

### Computed Values

Use data transformation before binding:

```tsx
const processedData = countryData.map(item => ({
  ...item,
  gdpPerCapita: item.gdp / item.population
}));

<LayerDirective
  dataSource={processedData}
  shapeSettings={{
    colorValuePath: 'gdpPerCapita',
    colorMapping: [...]
  }}
/>
```

## Custom Color Schemes

### Diverging Color Scheme

For data with meaningful midpoint (e.g., election results):

```tsx
colorMapping: [
  { from: 0, to: 30, color: '#0015BC', label: 'Strong Blue' },
  { from: 30, to: 45, color: '#7DA2D9', label: 'Lean Blue' },
  { from: 45, to: 55, color: '#E8E8E8', label: 'Swing' },
  { from: 55, to: 70, color: '#F4A7A5', label: 'Lean Red' },
  { from: 70, to: 100, color: '#DE0100', label: 'Strong Red' }
]
```

### Sequential Color Scheme

Progressive intensity (e.g., unemployment rate):

```tsx
colorMapping: [
  { from: 0, to: 3, color: '#FFFFCC', label: 'Very Low' },
  { from: 3, to: 5, color: '#C7E9B4', label: 'Low' },
  { from: 5, to: 7, color: '#7FCDBB', label: 'Moderate' },
  { from: 7, to: 10, color: '#41B6C4', label: 'High' },
  { from: 10, to: 15, color: '#2C7FB8', label: 'Very High' },
  { from: 15, to: 30, color: '#253494', label: 'Extreme' }
]
```

### Qualitative Color Scheme

Distinct colors for unordered categories:

```tsx
colorMapping: [
  { value: 'Agriculture', color: '#8DD3C7' },
  { value: 'Manufacturing', color: '#FFFFB3' },
  { value: 'Services', color: '#BEBADA' },
  { value: 'Technology', color: '#FB8072' },
  { value: 'Finance', color: '#80B1D3' },
  { value: 'Healthcare', color: '#FDB462' }
]
```

## Visual Strategies

### Strategy 1: High Contrast for Key Differences

```tsx
// Election results - clear distinction
colorMapping: [
  { value: 'Candidate A', color: '#0015BC', label: 'Candidate A' },
  { value: 'Candidate B', color: '#DE0100', label: 'Candidate B' },
  { value: 'No Data', color: '#E8E8E8', label: 'No Data' }
]
```

### Strategy 2: Gradient for Continuous Data

```tsx
// Temperature - smooth transition
colorMapping: [
  { from: -10, to: 0, color: '#08519C' },
  { from: 0, to: 10, color: '#3182BD' },
  { from: 10, to: 20, color: '#6BAED6' },
  { from: 20, to: 30, color: '#9ECAE1' },
  { from: 30, to: 40, color: '#C6DBEF' }
]
```

### Strategy 3: Color-Blind Friendly

```tsx
// Accessible color palette
colorMapping: [
  { value: 'Category 1', color: '#0173B2' },  // Blue
  { value: 'Category 2', color: '#DE8F05' },  // Orange
  { value: 'Category 3', color: '#029E73' },  // Green
  { value: 'Category 4', color: '#CC78BC' }   // Purple
]
```

### Strategy 4: Default Color for Missing Data

```tsx
shapeSettings={{
  fill: '#F0F0F0',  // Light gray for countries without data
  colorValuePath: 'value',
  colorMapping: [
    { from: 0, to: 100, color: '#4CAF50' }
  ],
  border: {
    color: '#CCCCCC',
    width: 0.5
  }
}}
```

## Common Use Cases

### Choropleth Map: Population Density

```tsx
function PopulationDensityMap() {
  const densityData = [
    { country: 'Monaco', density: 26337, tier: 'very-high' },
    { country: 'Singapore', density: 8358, tier: 'very-high' },
    { country: 'Bangladesh', density: 1265, tier: 'high' },
    { country: 'India', density: 464, tier: 'medium' },
    { country: 'China', density: 153, tier: 'medium' },
    { country: 'United States', density: 36, tier: 'low' },
    { country: 'Canada', density: 4, tier: 'very-low' }
  ];

  return (
    <MapsComponent
      titleSettings={{ text: 'Population Density (per km²)' }}
      legendSettings={{ visible: true }}
    >
      <Inject services={[Legend]} />
      <LayersDirective>
        <LayerDirective
          shapeData={world_map}
          dataSource={densityData}
          shapeDataPath='country'
          shapePropertyPath='name'
          shapeSettings={{
            fill: '#E8E8E8',
            colorValuePath: 'density',
            colorMapping: [
              { from: 0, to: 50, color: '#FFF5E6', label: '0-50' },
              { from: 50, to: 200, color: '#FFD699', label: '50-200' },
              { from: 200, to: 500, color: '#FFB84D', label: '200-500' },
              { from: 500, to: 2000, color: '#FF9900', label: '500-2000' },
              { from: 2000, to: 30000, color: '#CC7A00', label: '2000+' }
            ]
          }}
        />
      </LayersDirective>
    </MapsComponent>
  );
}
```

### Election Results Map

```tsx
function ElectionMap() {
  const results = [
    { state: 'California', winner: 'Democrat', margin: 29.2 },
    { state: 'Texas', winner: 'Republican', margin: 5.6 },
    { state: 'Florida', winner: 'Republican', margin: 3.4 },
    { state: 'Pennsylvania', winner: 'Democrat', margin: 1.2 }
  ];

  return (
    <MapsComponent legendSettings={{ visible: true, mode: 'Interactive' }}>
      <Inject services={[Legend]} />
      <LayersDirective>
        <LayerDirective
          shapeData={usa_map}
          dataSource={results}
          shapeDataPath='state'
          shapePropertyPath='name'
          shapeSettings={{
            colorValuePath: 'winner',
            colorMapping: [
              { value: 'Democrat', color: '#0015BC', label: 'Democrat' },
              { value: 'Republican', color: '#DE0100', label: 'Republican' }
            ],
            border: { color: 'white', width: 2 }
          }}
        />
      </LayersDirective>
    </MapsComponent>
  );
}
```

### COVID-19 Cases Map

```tsx
function CovidMap() {
  const covidData = [
    { country: 'United States', cases: 95000000, severity: 'critical' },
    { country: 'India', cases: 44000000, severity: 'high' },
    { country: 'Brazil', cases: 37000000, severity: 'high' },
    { country: 'France', cases: 38000000, severity: 'moderate' }
  ];

  return (
    <MapsComponent
      titleSettings={{ text: 'COVID-19 Total Cases by Country' }}
      legendSettings={{ visible: true, position: 'Right' }}
    >
      <Inject services={[Legend]} />
      <LayersDirective>
        <LayerDirective
          shapeData={world_map}
          dataSource={covidData}
          shapeDataPath='country'
          shapePropertyPath='name'
          shapeSettings={{
            fill: '#F0F0F0',
            colorValuePath: 'cases',
            colorMapping: [
              { from: 0, to: 1000000, color: '#FFF9C4', label: '< 1M' },
              { from: 1000000, to: 10000000, color: '#FFF176', label: '1M - 10M' },
              { from: 10000000, to: 50000000, color: '#FFB300', label: '10M - 50M' },
              { from: 50000000, to: 100000000, color: '#F57C00', label: '50M - 100M' }
            ]
          }}
        />
      </LayersDirective>
    </MapsComponent>
  );
}
```

## Troubleshooting

### Issue: Colors not applying

**Causes & Solutions:**

1. **colorValuePath doesn't match data field**
```tsx
// ✅ Correct - field names match
const data = [{ country: 'USA', status: 'Active' }];
shapeSettings={{ colorValuePath: 'status' }}

// ❌ Wrong - field name mismatch
const data = [{ country: 'USA', status: 'Active' }];
shapeSettings={{ colorValuePath: 'state' }}  // Wrong field
```

2. **shapeDataPath/shapePropertyPath mismatch**
```tsx
// ✅ Correct - paths connect data to GeoJSON
shapeDataPath='country'        // Field in your data
shapePropertyPath='name'       // Field in GeoJSON properties

// ❌ Wrong - paths don't match
shapeDataPath='name'           // Doesn't exist in data
shapePropertyPath='country'    // Doesn't exist in GeoJSON
```

3. **Values don't match color mapping**
```tsx
// ✅ Correct - values match
data: [{ country: 'USA', type: 'Developed' }]
colorMapping: [{ value: 'Developed', color: '#00FF00' }]

// ❌ Wrong - value mismatch (case-sensitive)
data: [{ country: 'USA', type: 'developed' }]
colorMapping: [{ value: 'Developed', color: '#00FF00' }]
```

### Issue: Some shapes not colored

**Cause:** Data missing for those shapes or out of range

**Solution:**
```tsx
// Set default color for unmatched shapes
shapeSettings={{
  fill: '#E5E5E5',  // Default gray
  colorValuePath: 'value',
  colorMapping: [...]
}}
```

### Issue: Range colors not working correctly

**Cause:** Overlapping or missing ranges

**Solution:**
```tsx
// ✅ Correct - continuous non-overlapping ranges
colorMapping: [
  { from: 0, to: 100, color: '#C3E6CB' },
  { from: 100, to: 500, color: '#6AB187' },    // Start where previous ends
  { from: 500, to: 1000, color: '#2F7C4F' }
]

// ❌ Wrong - gaps in ranges
colorMapping: [
  { from: 0, to: 100, color: '#C3E6CB' },
  { from: 200, to: 500, color: '#6AB187' },   // Gap: 100-200 missing
  { from: 600, to: 1000, color: '#2F7C4F' }   // Gap: 500-600 missing
]
```

### Issue: Desaturation not visible

**Cause:** minOpacity and maxOpacity too similar

**Solution:**
```tsx
// ✅ Good opacity range
{ from: 0, to: 100, color: '#2E7D32', minOpacity: 0.2, maxOpacity: 1 }

// ❌ Poor contrast
{ from: 0, to: 100, color: '#2E7D32', minOpacity: 0.8, maxOpacity: 0.9 }
```
