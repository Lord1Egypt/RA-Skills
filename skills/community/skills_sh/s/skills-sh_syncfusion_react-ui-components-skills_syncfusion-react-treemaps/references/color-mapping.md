# Color Mapping Strategies

## Table of Contents

- [Range Color Mapping](#range-color-mapping)
  - [Basic Range Mapping](#basic-range-mapping)
  - [Sales Performance Gradient](#sales-performance-gradient)
  - [HeatMap Intensity](#heatmap-intensity)
- [Equal Value Color Mapping](#equal-value-color-mapping)
  - [Category Colors](#category-colors)
  - [Status Colors](#status-colors)
  - [Department Colors](#department-colors)
- [Desaturation Color Mapping](#desaturation-color-mapping)
  - [Opacity-Based Intensity](#opacity-based-intensity)
  - [Risk-Level Visualization](#risk-level-visualization)
- [Choosing Color Mapping Strategy](#choosing-color-mapping-strategy)
  - [Use Range Color Mapping When](#use-range-color-mapping-when)
  - [Use Equal Color Mapping When](#use-equal-color-mapping-when)
  - [Use Desaturation When](#use-desaturation-when)
- [Common Patterns](#common-patterns)
  - [Pattern 1: Traffic Light Status](#pattern-1-traffic-light-status)
  - [Pattern 2: Multi-Metric with Ranges](#pattern-2-multi-metric-with-ranges)
  - [Pattern 3: Performance vs Target](#pattern-3-performance-vs-target)
- [Tips for Effective Color Mapping](#tips-for-effective-color-mapping)
- [Next Steps](#next-steps)

## Range Color Mapping

Range color mapping assigns colors based on value intervals. Items within a range get the specified color, creating a gradient effect.

### Basic Range Mapping

```jsx
import { TreeMapComponent } from '@syncfusion/ej2-react-treemap';
import * as React from "react";

const data = [
  { Fruit: 'Apple', Sales: 5000 },
  { Fruit: 'Mango', Sales: 3000 },
  { Fruit: 'Orange', Sales: 2300 },
  { Fruit: 'Banana', Sales: 500 },
  { Fruit: 'Grape', Sales: 4300 },
  { Fruit: 'Papaya', Sales: 1200 },
  { Fruit: 'Melon', Sales: 4500 }
];

<TreeMapComponent
  dataSource={data}
  weightValuePath="Sales"
  rangeColorValuePath="Sales"  // Color based on Sales values
  leafItemSettings={{
    labelPath: 'Fruit',
    colorMapping: [
      { from: 500, to: 1500, color: '#FF6B6B' },      // Red
      { from: 1500, to: 3000, color: '#FFD93D' },    // Yellow
      { from: 3000, to: 5000, color: '#6BCB77' }     // Green
    ]
  }}
/>
```

**Result:** 
- Banana (500) → Red
- Orange (2300), Papaya (1200) → Yellow
- Mango (3000), Grape (4300), Apple (5000), Melon (4500) → Green

### Sales Performance Gradient

```jsx
const salesData = [
  { Region: 'North', Revenue: 45000 },
  { Region: 'South', Revenue: 28000 },
  { Region: 'East', Revenue: 52000 },
  { Region: 'West', Revenue: 38000 },
  { Region: 'Central', Revenue: 18000 }
];

<TreeMapComponent
  dataSource={salesData}
  weightValuePath="Revenue"
  rangeColorValuePath="Revenue"
  leafItemSettings={{
    labelPath: 'Region',
    colorMapping: [
      { from: 0, to: 20000, color: '#E74C3C' },      // Poor (Red)
      { from: 20000, to: 40000, color: '#F39C12' }, // Fair (Orange)
      { from: 40000, to: 60000, color: '#27AE60' }  // Good (Green)
    ]
  }}
/>
```

**Use case:** Performance tiers where color represents achievement level.

### HeatMap Intensity

```jsx
const tempData = [
  { Region: 'Desert', Temperature: 55 },
  { Region: 'Tropical', Temperature: 32 },
  { Region: 'Arctic', Temperature: -40 },
  { Region: 'Temperate', Temperature: 15 }
];

<TreeMapComponent
  dataSource={tempData}
  rangeColorValuePath="Temperature"
  leafItemSettings={{
    labelPath: 'Region',
    colorMapping: [
      { from: -50, to: 0, color: '#3498DB' },    // Blue (Cold)
      { from: 0, to: 20, color: '#2ECC71' },     // Green (Cool)
      { from: 20, to: 35, color: '#F39C12' },    // Orange (Warm)
      { from: 35, to: 60, color: '#E74C3C' }     // Red (Hot)
    ]
  }}
/>
```

## Equal Value Color Mapping

Equal color mapping assigns colors based on exact categorical values, not ranges. Perfect for categorical data.

### Category Colors

```jsx
const carData = [
  { Car: 'Mustang', Brand: 'Ford', Count: 232 },
  { Car: 'EcoSport', Brand: 'Ford', Count: 121 },
  { Car: 'Swift', Brand: 'Maruti', Count: 143 },
  { Car: 'Baleno', Brand: 'Maruti', Count: 454 },
  { Car: 'A3 Cabriolet', Brand: 'Audi', Count: 123 },
  { Car: 'RS7 Sportback', Brand: 'Audi', Count: 523 }
];

<TreeMapComponent
  dataSource={carData}
  weightValuePath="Count"
  equalColorValuePath="Brand"  // Color by Brand value
  leafItemSettings={{
    labelPath: 'Car',
    colorMapping: [
      { value: 'Ford', color: '#3498DB' },    // Blue for Ford
      { value: 'Maruti', color: '#E74C3C' },  // Red for Maruti
      { value: 'Audi', color: '#2ECC71' }     // Green for Audi
    ]
  }}
/>
```

**Result:** All Ford cars → Blue, all Maruti cars → Red, all Audi cars → Green.

### Status Colors

```jsx
const projectData = [
  { Project: 'Alpha', Team: 'Backend', Status: 'On Track', Tasks: 15 },
  { Project: 'Beta', Team: 'Frontend', Status: 'At Risk', Tasks: 12 },
  { Project: 'Gamma', Team: 'DevOps', Status: 'Blocked', Tasks: 8 },
  { Project: 'Delta', Team: 'QA', Status: 'On Track', Tasks: 20 }
];

<TreeMapComponent
  dataSource={projectData}
  weightValuePath="Tasks"
  equalColorValuePath="Status"
  leafItemSettings={{
    labelPath: 'Project',
    colorMapping: [
      { value: 'On Track', color: '#27AE60' },  // Green
      { value: 'At Risk', color: '#F39C12' },   // Orange
      { value: 'Blocked', color: '#E74C3C' }    // Red
    ]
  }}
/>
```

### Department Colors

```jsx
const employeeData = [
  { Name: 'John', Department: 'Engineering', Count: 1 },
  { Name: 'Sarah', Department: 'Sales', Count: 1 },
  { Name: 'Mike', Department: 'HR', Count: 1 },
  { Name: 'Lisa', Department: 'Engineering', Count: 1 }
];

<TreeMapComponent
  dataSource={employeeData}
  equalColorValuePath="Department"
  leafItemSettings={{
    colorMapping: [
      { value: 'Engineering', color: '#9B59B6' },
      { value: 'Sales', color: '#3498DB' },
      { value: 'HR', color: '#E67E22' }
    ]
  }}
/>
```

## Desaturation Color Mapping

Desaturation mapping applies opacity variation to a base color, creating lighter/darker shades based on values.

### Opacity-Based Intensity

```jsx
const data = [
  { Product: 'Laptop', Sales: 2500 },
  { Product: 'Phone', Sales: 3200 },
  { Product: 'Tablet', Sales: 1800 },
  { Product: 'Watch', Sales: 900 }
];

<TreeMapComponent
  dataSource={data}
  weightValuePath="Sales"
  rangeColorValuePath="Sales"
  leafItemSettings={{
    labelPath: 'Product',
    colorMapping: [
      {
        from: 900,
        to: 3200,
        color: '#3498DB',
        minOpacity: 0.2,  // Light blue for low values
        maxOpacity: 1.0   // Full blue for high values
      }
    ]
  }}
/>
```

**Result:** 
- Watch (900) → Very light blue (0.2 opacity)
- Phone (3200) → Full blue (1.0 opacity)
- Others → Intermediate opacity based on sales

### Risk-Level Visualization

```jsx
const riskData = [
  { Project: 'A', Status: 'Risk', Level: 85 },
  { Project: 'B', Status: 'Risk', Level: 45 },
  { Project: 'C', Status: 'Risk', Level: 25 }
];

<TreeMapComponent
  dataSource={riskData}
  rangeColorValuePath="Level"
  leafItemSettings={{
    labelPath: 'Project',
    colorMapping: [
      {
        from: 20,
        to: 90,
        color: '#E74C3C',
        minOpacity: 0.3,  // Light red = low risk
        maxOpacity: 1.0   // Deep red = high risk
      }
    ]
  }}
/>
```

## Choosing Color Mapping Strategy

### Use Range Color Mapping When:
- **Visualizing continuous values:** Revenue, temperature, performance scores
- **Showing gradients:** Low → Medium → High representation
- **Comparing magnitude:** Larger values show different color intensity
- **Example:** Heatmap-style visualization of quarterly sales

### Use Equal Color Mapping When:
- **Categorizing items:** Brand, department, region, status
- **Discrete categories:** No gradient needed, each category has fixed color
- **Quick visual identification:** Users need instant category recognition
- **Example:** Different departments with distinct colors

### Use Desaturation When:
- **Subtle intensity variations:** Want same hue, different saturation
- **Professional appearance:** Avoid too many distinct colors
- **Print-friendly:** Desaturation works better in grayscale printing
- **Example:** Risk levels (light red = low risk, dark red = high risk)

## Common Patterns

### Pattern 1: Traffic Light Status

```jsx
const taskData = [
  { Task: 'Feature A', Progress: 85 },
  { Task: 'Feature B', Progress: 45 },
  { Task: 'Feature C', Progress: 25 }
];

<TreeMapComponent
  dataSource={taskData}
  weightValuePath="Progress"
  rangeColorValuePath="Progress"
  leafItemSettings={{
    labelPath: 'Task',
    colorMapping: [
      { from: 0, to: 33, color: '#E74C3C' },    // Red (Danger)
      { from: 33, to: 67, color: '#F39C12' },   // Yellow (Warning)
      { from: 67, to: 100, color: '#27AE60' }   // Green (Success)
    ]
  }}
/>
```

### Pattern 2: Multi-Metric with Ranges

```jsx
const salesByRegion = [
  { Region: 'North', Q1: 30000, Q2: 35000, Q3: 40000, Avg: 35000 },
  { Region: 'South', Q1: 20000, Q2: 22000, Q3: 21000, Avg: 21000 },
  { Region: 'East', Q1: 45000, Q2: 48000, Q3: 52000, Avg: 48333 }
];

<TreeMapComponent
  dataSource={salesByRegion}
  weightValuePath="Avg"
  rangeColorValuePath="Avg"
  leafItemSettings={{
    labelFormat: '${Region}\n${Avg}',
    colorMapping: [
      { from: 0, to: 25000, color: '#BDC3C7' },
      { from: 25000, to: 40000, color: '#3498DB' },
      { from: 40000, to: 60000, color: '#27AE60' }
    ]
  }}
/>
```

### Pattern 3: Performance vs Target

```jsx
const performanceData = [
  { Team: 'Team A', Target: 100000, Actual: 95000, Percentage: 95 },
  { Team: 'Team B', Target: 80000, Actual: 92000, Percentage: 115 },
  { Team: 'Team C', Target: 120000, Actual: 85000, Percentage: 71 }
];

<TreeMapComponent
  dataSource={performanceData}
  rangeColorValuePath="Percentage"
  leafItemSettings={{
    labelPath: 'Team',
    colorMapping: [
      { from: 0, to: 80, color: '#E74C3C' },      // Below target
      { from: 80, to: 100, color: '#F39C12' },    // Near target
      { from: 100, to: 150, color: '#27AE60' }    // Above target
    ]
  }}
/>
```

## Tips for Effective Color Mapping

1. **Use color consistently:** Same value should have same color across visualizations
2. **Limit colors:** Use 3-5 ranges for range mapping, avoid too many categories
3. **Contrast:** Ensure colors have enough contrast for visibility
4. **Accessibility:** Avoid red-green only combinations, support colorblind users
5. **Legend:** Always provide legend when using color mapping
6. **Documentation:** Explain color meaning to users (poor/fair/good, etc.)

## Next Steps

- **Leaf Items:** See [leaf-items-and-labels.md](leaf-items-and-labels.md) to customize label appearance
- **Legends:** See [legends-tooltips-selection.md](legends-tooltips-selection.md) to add legends
- **Drill-Down:** See [drilldown.md](drilldown.md) for hierarchical exploration
