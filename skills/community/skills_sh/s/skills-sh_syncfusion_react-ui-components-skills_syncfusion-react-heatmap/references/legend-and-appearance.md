# Legend, Appearance & Styling

## Table of Contents

- [Legend Basics](#legend-basics)
  - [Enable Legend](#enable-legend)
  - [Legend Properties](#legend-properties)
- [Legend Placement](#legend-placement)
  - [Right Position (Default)](#right-position-default)
  - [Bottom Position](#bottom-position)
  - [Top Position](#top-position)
  - [Left Position](#left-position)
  - [Responsive Legend Positioning](#responsive-legend-positioning)
- [Legend Customization](#legend-customization)
  - [Title and Labels](#title-and-labels)
  - [Legend Type: List](#legend-type-list)
  - [Custom Legend Size](#custom-legend-size)
  - [Remove Legend](#remove-legend)
- [Color Palettes](#color-palettes)
  - [Default Palettes](#default-palettes)
  - [Custom Gradient Palette](#custom-gradient-palette)
  - [Fixed Color Mapping (Non-Continuous)](#fixed-color-mapping-non-continuous)
  - [Colorblind-Friendly Palettes](#colorblind-friendly-palettes)
- [Dimensions & Sizing](#dimensions--sizing)
  - [Fixed Dimensions with Scrolling](#fixed-dimensions-with-scrolling)
- [Rendering Modes](#rendering-modes)
  - [Automatic Mode Selection](#automatic-mode-selection)
  - [Force SVG Mode](#force-svg-mode)
  - [Force Canvas Mode](#force-canvas-mode)
- [CSS Styling](#css-styling)
  - [Global Theme CSS](#global-theme-css)
  - [Custom CSS Styling](#custom-css-styling)
  - [Cell-Level Styling](#cell-level-styling)
- [Theme Integration](#theme-integration)
  - [Light Theme](#light-theme)
  - [Dark Theme](#dark-theme)
- [Complete Styling Example](#complete-styling-example)

## Legend Basics

### Enable Legend

```jsx
import { HeatMapComponent, Inject, Legend, Tooltip } from '@syncfusion/ej2-react-heatmap';

<HeatMapComponent id='heatmap' dataSource={data}>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

The legend displays a color scale showing the mapping between values and colors.

### Legend Properties

```jsx
<HeatMapComponent
  id='heatmap'
  dataSource={data}
  legendSettings={{
    position: 'Right',          // Position: 'Right', 'Bottom', 'Top', 'Left'
    visible: true,              // Show/hide legend
    width: '150px',             // Legend width
    height: 'auto',             // Legend height
    title: { text: 'Value Range' },
  }}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

## Legend Placement

### Right Position (Default)

```jsx
<HeatMapComponent
  id='heatmap'
  dataSource={data}
  legendSettings={{
    position: 'Right',
    width: '150px',
    alignment: 'Center'
  }}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

**Use when:** You have extra horizontal space and a tall heatmap.

### Bottom Position

```jsx
<HeatMapComponent
  id='heatmap'
  dataSource={data}
  legendSettings={{
    position: 'Bottom',
    height: '80px',
    alignment: 'Center'
  }}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

**Use when:** You have extra vertical space or limited height.

### Top Position

```jsx
<HeatMapComponent
  id='heatmap'
  dataSource={data}
  legendSettings={{
    position: 'Top',
    alignment: 'Far'  // 'Near', 'Center', 'Far'
  }}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

**Use when:** Legend should appear above the heatmap data.

### Left Position

```jsx
<HeatMapComponent
  id='heatmap'
  dataSource={data}
  legendSettings={{
    position: 'Left',
    alignment: 'Center'
  }}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

### Responsive Legend Positioning

```jsx
import { useState, useEffect } from 'react';

export function ResponsiveHeatmap() {
  const [legendPosition, setLegendPosition] = useState('Right');

  useEffect(() => {
    function handleResize() {
      const width = window.innerWidth;
      // Legend at bottom on mobile, right on desktop
      setLegendPosition(width < 768 ? 'Bottom' : 'Right');
    }

    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <HeatMapComponent
      id='heatmap'
      dataSource={data}
      legendSettings={{
        position: legendPosition
      }}
    >
      <Inject services={[Legend, Tooltip]} />
    </HeatMapComponent>
  );
}
```

## Legend Customization

### Title and Labels

```jsx
<HeatMapComponent
    id='heatmap'
    dataSource={data}
    legendRender={(args) => {
        args.text = args.text + ' units';
    }
    }
    legendSettings={{
        position: 'Right',
        title: {
            text: 'Temperature (°C)',
            textStyle: {
                size: '14px',
                fontWeight: 'bold',
                color: '#333'
            }
        },
        labelFormat: '{value}°',     // Format legend labels
    }}
>
    <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

### Legend Type: List

```jsx
<HeatMapComponent
  id='heatmap'
  dataSource={data}
  legendSettings={{
    mode: 'Categories'
  }}
  palette={[
    { value: 0, color: '#3498db' },     // Blue: Low
    { value: 50, color: '#f39c12' },    // Orange: Medium
    { value: 100, color: '#e74c3c' }    // Red: High
  ]}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

### Custom Legend Size

```jsx
<HeatMapComponent
  id='heatmap'
  dataSource={data}
  legendSettings={{
    position: 'Right',
    width: '200px',
    height: '300px',
  }}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

### Remove Legend

```jsx
<HeatMapComponent
  id='heatmap'
  dataSource={data}
  legendSettings={{
    visible: false  // Hide legend completely
  }}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

## Color Palettes

### Default Palettes

```jsx
// Blue-Green (good for data analysis)
palette={[
  { value: 0, color: '#3498db' },
  { value: 100, color: '#2ecc71' }
]}

// Red-Yellow-Green (traffic light style)
palette={[
  { value: 0, color: '#e74c3c' },
  { value: 50, color: '#f39c12' },
  { value: 100, color: '#2ecc71' }
]}

// Purple-White (heatmap style)
palette={[
  { value: 0, color: '#f7f7f7' },
  { value: 100, color: '#7b3ff2' }
]}
```

### Custom Gradient Palette

```jsx
<HeatMapComponent
    id='heatmap'
    dataSource={data}
    paletteSettings={{
        palette: [{ value: 0, color: '#1a1a2e' },      // Very dark blue
        { value: 25, color: '#16213e' },     // Dark blue
        { value: 50, color: '#0f3460' },     // Medium blue
        { value: 75, color: '#ee2e24' },     // Red-orange
        { value: 100, color: '#ffff00' }]
    }}
>
    <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

### Fixed Color Mapping (Non-Continuous)

```jsx
const data = [
  { row: 'App A', column: 'Mon', value: 1, status: 'healthy' },
  { row: 'App A', column: 'Tue', value: 2, status: 'warning' },
  { row: 'App B', column: 'Mon', value: 3, status: 'critical' }
];

<HeatMapComponent
    id='heatmap'
    dataSource={data}
    dataSourceSettings={{ valueMapping: 'value' }}
    paletteSettings={{
        palette: [{ value: 1, color: '#2ecc71' },   // Green: healthy
        { value: 2, color: '#f39c12' },   // Orange: warning
        { value: 3, color: '#e74c3c' }]
    }}

    cellRender={(args) => {
        const statusMap = {
            'healthy': '✓',
            'warning': '⚠',
            'critical': '✕'
        };
        const status = data.find(d =>
            d.row === args.row && d.column === args.column
        )?.status;
        args.displayText = statusMap[status] || '';
    }}
>
    <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

### Colorblind-Friendly Palettes

```jsx
// Deuteranopia-friendly (red-green colorblind)
const colorblindPalette = [
  { value: 0, color: '#e8e8e8' },   // Light gray
  { value: 50, color: '#b3b3b3' },  // Medium gray
  { value: 100, color: '#212121' }  // Dark gray
];

// Better: Viridis-style (works for most color blindness)
const viridis = [
  { value: 0, color: '#440154' },
  { value: 50, color: '#31688e' },
  { value: 100, color: '#35b779' }
];
```

## Dimensions & Sizing

### Fixed Dimensions with Scrolling

```jsx
<div style={{
  width: '800px',
  height: '600px',
  overflow: 'auto',
  border: '1px solid #ddd'
}}>
  <HeatMapComponent
    id='heatmap'
    dataSource={largeData}
    width='100%'
    height='100%'
  >
    <Inject services={[Legend, Tooltip]} />
  </HeatMapComponent>
</div>
```

## Rendering Modes

### Automatic Mode Selection

```jsx
<HeatMapComponent
  id='heatmap'
  dataSource={data}
  renderingMode='Auto'  // Switches to Canvas if >1000 cells
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

The component automatically chooses:
- **SVG** for small datasets (<1000 cells) - Better for styling
- **Canvas** for large datasets (>1000 cells) - Better performance

### Force SVG Mode

```jsx
<HeatMapComponent
  id='heatmap'
  dataSource={data}
  renderingMode='SVG'  // Always use SVG
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

**Use when:** You need detailed styling and have small data.

### Force Canvas Mode

```jsx
<HeatMapComponent
  id='heatmap'
  dataSource={largeData}
  renderingMode='Canvas'  // Always use Canvas
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

**Use when:** Performance is critical with large data.

## CSS Styling

### Global Theme CSS

```jsx
// Material theme (Material Design colors)
import '@syncfusion/ej2-base/styles/material.css';

// Bootstrap 5 theme
import '@syncfusion/ej2-base/styles/bootstrap5.css';

// Fluent theme (Microsoft Fluent Design)
import '@syncfusion/ej2-base/styles/fabric.css';

// Tailwind theme
import '@syncfusion/ej2-base/styles/tailwind.css';
```

### Custom CSS Styling

```jsx
import '@syncfusion/ej2-base/styles/material.css';
import './CustomHeatmap.css';

export function App() {
  return (
    <div className='custom-heatmap-container'>
      <HeatMapComponent id='heatmap' dataSource={data}>
        <Inject services={[Legend, Tooltip]} />
      </HeatMapComponent>
    </div>
  );
}
```

**CustomHeatmap.css:**
```css
.custom-heatmap-container .e-heatmap {
  border: 2px solid #333;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.custom-heatmap-container .e-heatmap-labels {
  font-family: 'Arial', sans-serif;
  font-weight: bold;
}

.custom-heatmap-container .e-heatmap-cell {
  border-radius: 2px;
}
```

### Cell-Level Styling

```jsx
<HeatMapComponent
  id='heatmap'
  dataSource={data}
  cellRender={(args) => {
    // Highlight cells above threshold
    if (args.value > 80) {
      args.cellElement.style.borderWidth = '2px';
      args.cellElement.style.borderColor = '#000';
    }
    
    // Add patterns or icons
    if (args.value < 20) {
      args.displayText = '❄️';  // Freezing
    } else if (args.value > 80) {
      args.displayText = '🔥';  // Hot
    }
  }}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

## Theme Integration

### Light Theme

```jsx
import '@syncfusion/ej2-base/styles/material.css';

export function App() {
  return (
      <HeatMapComponent
          id='heatmap'
          dataSource={data}
          // Light colors work well
          paletteSettings={{
              palette: [{ value: 0, color: '#e8f4f8' },
              { value: 100, color: '#0066cc' }]
          }}
      >
          <Inject services={[Legend, Tooltip]} />
      </HeatMapComponent>
  );
}
```

### Dark Theme

```jsx
import '@syncfusion/ej2-base/styles/material-dark.css';

export function App() {
  return (
<HeatMapComponent
    id='heatmap'
    dataSource={data}
    // Bright colors for dark backgrounds
    paletteSettings={{
        palette: [{ value: 0, color: '#1a1a2e' },
        { value: 100, color: '#00ff88' }]
    }}

>
    <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
  );
}
```

## Complete Styling Example

```jsx
import { HeatMapComponent, Inject, Legend, Tooltip } from '@syncfusion/ej2-react-heatmap';
import '@syncfusion/ej2-base/styles/bootstrap5.css';
import './HeatmapStyles.css';

export function StyledHeatmap() {
  const data = [
    { row: 'Product A', column: 'Q1', value: 150 },
    { row: 'Product A', column: 'Q2', value: 200 },
    { row: 'Product B', column: 'Q1', value: 100 },
    { row: 'Product B', column: 'Q2', value: 180 }
  ];

  return (
    <div className='heatmap-wrapper'>
      <div className='heatmap-header'>
        <h2>Quarterly Performance</h2>
        <p className='subtitle'>Sales data across products</p>
      </div>

      <HeatMapComponent
          id='heatmap'
          dataSource={data}
          dataSourceSettings={{ xDataMapping: 'column', yDataMapping: 'row', valueMapping: 'value' }}
          xAxis={{
              valueType: 'Category'
          }}
          yAxis={{
              valueType: 'Category'
          }}
          paletteSettings={{
              palette: [{ value: 0, color: '#e3f2fd' },
              { value: 50, color: '#42a5f5' },
              { value: 100, color: '#1565c0' }]
          }}
          legendSettings={{
              position: 'Right',
              title: { text: 'Sales Volume' }
          }}
      >
          <Inject services={[Legend, Tooltip]} />
      </HeatMapComponent>
    </div>
  );
}
```

**HeatmapStyles.css:**
```css
.heatmap-wrapper {
  padding: 20px;
  background: #f5f5f5;
  border-radius: 8px;
}

.heatmap-header {
  margin-bottom: 20px;
}

.heatmap-header h2 {
  color: #333;
  margin: 0 0 5px 0;
}

.subtitle {
  color: #666;
  font-size: 14px;
  margin: 0;
}
```
