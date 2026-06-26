# Accessibility & Troubleshooting

## Table of Contents

- [Accessibility Features](#accessibility-features)
  - [Enable Accessibility](#enable-accessibility)
  - [Provide Semantic Context](#provide-semantic-context)
  - [Alternative Text Content](#alternative-text-content)
- [WCAG Compliance](#wcag-compliance)
  - [Color Contrast](#color-contrast)
  - [Color + Pattern Support](#color--pattern-support)
  - [Font Size and Readability](#font-size-and-readability)
- [Keyboard Navigation](#keyboard-navigation)
  - [Enable Keyboard Interaction](#enable-keyboard-interaction)
  - [Focus Indicators](#focus-indicators)
- [Screen Reader Support](#screen-reader-support)
  - [ARIA Labels](#aria-labels)
  - [Meaningful Tooltip Content](#meaningful-tooltip-content)
  - [Data Table as Fallback](#data-table-as-fallback)
- [Common Issues](#common-issues)
- [Troubleshooting Guide](#troubleshooting-guide)
  - [Issue 1: HeatMap Not Rendering](#issue-1-heatmap-not-rendering)
  - [Issue 2: Styles Not Applied](#issue-2-styles-not-applied)
  - [Issue 3: Axes Labels Overlapping](#issue-3-axes-labels-overlapping)
  - [Issue 4: Large Dataset Performance](#issue-4-large-dataset-performance)
  - [Issue 5: Tooltips Not Showing](#issue-5-tooltips-not-showing)
- [Migration from EJ1](#migration-from-ej1)
  - [EJ1 vs EJ2 Differences](#ej1-vs-ej2-differences)
  - [Basic Migration Example](#basic-migration-example)
  - [Data Format Migration](#data-format-migration)
  - [Event Name Changes](#event-name-changes)
  - [Complete Migration Template](#complete-migration-template)

## Accessibility Features

### Enable Accessibility

```jsx
import { HeatMapComponent, Inject, Legend, Tooltip } from '@syncfusion/ej2-react-heatmap';

export function AccessibleHeatmap() {
  return (
    <HeatMapComponent
      id='heatmap'
      dataSource={data}
      xAxis={{ 
        labels: ['Q1', 'Q2', 'Q3', 'Q4'],
        title: { text: 'Quarters' }  // Label for screen readers
      }}
      yAxis={{ 
        labels: ['North', 'South', 'East'],
        title: { text: 'Regions' }   // Label for screen readers
      }}
      title={{ text: 'Sales Data Heatmap' }}  // Main title for context
      showTooltip= {true} 
    >
      <Inject services={[Legend, Tooltip]} />
    </HeatMapComponent>
  );
}
```

### Provide Semantic Context

```jsx
<div>
  <h1>Sales Performance Analysis</h1>
  <p>
    This heatmap shows quarterly sales data across three regions.
    Darker colors indicate higher sales volumes.
  </p>
  
  <HeatMapComponent
    id='heatmap'
    dataSource={data}
    title={{ text: 'Quarterly Sales by Region' }}
    ariaLabel='Sales heatmap with quarterly data by region'
  >
    <Inject services={[Legend, Tooltip]} />
  </HeatMapComponent>
  
  <p>
    <strong>Color meaning:</strong> Blue indicates low sales, red indicates high sales.
  </p>
</div>
```

### Alternative Text Content

```jsx
export function AccessibleWithAlternative() {
  const data = [
    { row: 'North', column: 'Q1', value: 150 },
    { row: 'North', column: 'Q2', value: 200 },
    { row: 'South', column: 'Q1', value: 100 },
    { row: 'South', column: 'Q2', value: 180 }
  ];

  return (
    <div>
      {/* Visual heatmap */}
      <HeatMapComponent id='heatmap' dataSource={data}>
        <Inject services={[Legend, Tooltip]} />
      </HeatMapComponent>

      {/* Alternative text representation */}
      <div role='region' aria-label='Heatmap data table'>
        <h3>Data Table (Alternative Format)</h3>
        <table>
          <thead>
            <tr>
              <th>Region</th>
              <th>Q1</th>
              <th>Q2</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>North</td>
              <td>150</td>
              <td>200</td>
            </tr>
            <tr>
              <td>South</td>
              <td>100</td>
              <td>180</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
```

## WCAG Compliance

### Color Contrast

```jsx
import '@syncfusion/ej2-base/styles/material.css';

export function HighContrastHeatmap() {
  return (
    <HeatMapComponent
        id='heatmap'
        dataSource={data}
        // High contrast colors (WCAG AA compliant)
        paletteSettings={{
            palette: [{ value: 0, color: '#FFFFFF' },
            { value: 50, color: '#808080' },   // Gray
            { value: 100, color: '#000000' }
            ]
        }}
        legendSettings={{
            textStyle: {
                color: '#000000',                // High contrast text
                size: '14px'
            }
        }}
    >
        <Inject services={[Legend, Tooltip]} />
    </HeatMapComponent>
  );
}
```

### Color + Pattern Support

```jsx
export function PatternHeatmap() {
  const patterns = ['/', '\\', '|', '-', 'x'];

  return (
    <HeatMapComponent
      id='heatmap'
      dataSource={data}
      cellRender={(args) => {
        // Not just color - also add pattern
        const patternIndex = Math.floor(args.value / 20) % patterns.length;
        args.displayText = patterns[patternIndex];
        
        // Add visual indicator
        if (args.value > 80) {
          args.displayText += '●';  // Bullet for very high values
        }
      }}
    >
      <Inject services={[Legend, Tooltip]} />
    </HeatMapComponent>
  );
}
```

### Font Size and Readability

```jsx
<HeatMapComponent
        id='heatmap'
        dataSource={data}
        xAxis={{
            labels: ['Q1', 'Q2', 'Q3', 'Q4'],
            textStyle: {
                size: '14px',      // At least 14px
                fontWeight: 'bold' // Better readability
            }
        }}
        yAxis={{
            labels: ['North', 'South', 'East'],
            textStyle: {
                size: '14px',
                fontWeight: 'bold'
            }
        }}
    >
        <Inject services={[Legend, Tooltip]} />
    </HeatMapComponent>
```

## Keyboard Navigation

### Enable Keyboard Interaction

```jsx
export function KeyboardAccessibleHeatmap() {
  const [focusedCell, setFocusedCell] = useState(null);

  const handleKeyDown = (event) => {
    if (!focusedCell) return;

    const { row, col } = focusedCell;
    
    switch(event.key) {
      case 'ArrowUp':
        setFocusedCell({ row: Math.max(0, row - 1), col });
        event.preventDefault();
        break;
      case 'ArrowDown':
        setFocusedCell({ row: row + 1, col });
        event.preventDefault();
        break;
      case 'ArrowLeft':
        setFocusedCell({ row, col: Math.max(0, col - 1) });
        event.preventDefault();
        break;
      case 'ArrowRight':
        setFocusedCell({ row, col: col + 1 });
        event.preventDefault();
        break;
      case 'Enter':
      case ' ':
        // Activate cell
        handleCellActivation(row, col);
        event.preventDefault();
        break;
      default:
        break;
    }
  };

  const handleCellActivation = (row, col) => {
    console.log(`Cell activated: [${row}, ${col}]`);
  };

  return (
    <div
      role='grid'
      onKeyDown={handleKeyDown}
      tabIndex={0}
      style={{ outline: focusedCell ? '2px solid blue' : 'none' }}
    >
      <HeatMapComponent
        id='heatmap'
        dataSource={data}
        cellRender={(args) => {
          // Highlight focused cell
          if (focusedCell && focusedCell.row === args.row && focusedCell.col === args.column) {
            args.cellElement.style.outline = '3px solid blue';
          }
        }}
      >
        <Inject services={[Legend, Tooltip]} />
      </HeatMapComponent>
    </div>
  );
}
```

### Focus Indicators

```jsx
<HeatMapComponent
  id='heatmap'
  dataSource={data}
  cellRender={(args) => {
    // Add clear focus indicator
    const cellElement = args.cellElement;
    
    // Default state
    cellElement.style.outline = '1px solid transparent';
    
    // On focus (keyboard navigation)
    cellElement.onFocus = () => {
      cellElement.style.outline = '3px solid #0066cc';
      cellElement.style.outlineOffset = '2px';
    };
  }}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

## Screen Reader Support

### ARIA Labels

```jsx
<div role='main'>
  <h1 id='heatmap-title'>Quarterly Sales Heatmap</h1>
  
  <HeatMapComponent
    id='heatmap'
    dataSource={data}
    titleSettings={{text: 'Quarterly Sales by Region'}}
  >
    <Inject services={[Legend, Tooltip]} />
  </HeatMapComponent>

  <div aria-describedby='legend-description'>
    <h2>Legend</h2>
    <p id='legend-description'>
      Blue represents low sales (0-25%), green represents medium sales (25-75%),
      and red represents high sales (75-100%).
    </p>
  </div>
</div>
```

### Meaningful Tooltip Content

```jsx
<HeatMapComponent
  id='heatmap'
  dataSource={data}
  tooltipRender={(args) => {
    // Create descriptive tooltip for screen readers
    args.content = `
      Region: ${args.content.row}, 
      Quarter: ${args.content.column}, 
      Sales: $${args.content.value}000
    `;
        }}
    >
        <Inject services={[Legend, Tooltip]} />
    </HeatMapComponent>
```

### Data Table as Fallback

```jsx
export function AccessibleDataPresentation() {
  return (
    <div>
      <h1>Sales Data</h1>
      
      {/* Heatmap for sighted users */}
      <div role='img' aria-label='Sales data heatmap visualization'>
        <HeatMapComponent id='heatmap' dataSource={data}>
          <Inject services={[Legend, Tooltip]} />
        </HeatMapComponent>
      </div>

      {/* Data table for screen reader users */}
      <div role='region' aria-label='Data in table format'>
        <h2>Sales Data Table</h2>
        <table>
          <caption>Quarterly sales data by region</caption>
          <thead>
            <tr>
              <th>Region</th>
              <th>Q1 ($000)</th>
              <th>Q2 ($000)</th>
              <th>Q3 ($000)</th>
            </tr>
          </thead>
          <tbody>
            {data.map((item, idx) => (
              <tr key={idx}>
                <td>{item.row}</td>
                <td>{item.value}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
```

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Heatmap not displaying | Missing data or container | Provide dataSource and ensure container has dimensions |
| Styles not applying | CSS not imported | Add `import '@syncfusion/ej2-base/styles/material.css'` |
| Axes labels overlap | Too many labels in small space | Rotate labels with `labelRotation={45}` |
| Poor performance | Large dataset with SVG mode | Use `renderingMode='Canvas'` for >1000 cells |
| Tooltips not showing | Tooltip service not injected | Add `<Inject services={[Tooltip]} />` |

## Troubleshooting Guide

### Issue 1: HeatMap Not Rendering

**Symptoms:** Blank component, no error in console

**Diagnosis:**
```jsx
// Check if dataSource is provided
if (!dataSource || dataSource.length === 0) {
  console.error('No data provided');
}

// Check container dimensions
const container = document.getElementById('heatmap');
console.log('Container size:', {
  width: container.offsetWidth,
  height: container.offsetHeight
});
```

**Solution:**
```jsx
<div style={{ width: '800px', height: '600px' }}>
  <HeatMapComponent 
    id='heatmap' 
    dataSource={data}  // Must have data
    width='100%'
    height='100%'
  >
    <Inject services={[Legend, Tooltip]} />
  </HeatMapComponent>
</div>
```

### Issue 2: Styles Not Applied

**Symptoms:** Default gray colors, not using custom palette

**Diagnosis:**
```jsx
// Check if CSS is imported
try {
  const style = document.querySelector('link[href*="material.css"]');
  console.log('Theme CSS loaded:', !!style);
} catch(e) {
  console.error('CSS import error');
}
```

**Solution:**
```jsx
// In your entry file (main.jsx or index.js)
import '@syncfusion/ej2-base/styles/material.css';  // Must be at top

import { HeatMapComponent } from '@syncfusion/ej2-react-heatmap';
```

### Issue 3: Axes Labels Overlapping

**Symptoms:** Labels stacked or unreadable

**Solution:**
```jsx
<HeatMapComponent
  id='heatmap'
  dataSource={data}
  xAxis={{
    labels: longLabelList,
    labelRotation: 45,         // Rotate labels
    labelIntersectAction: 'Rotate45'  // Auto-rotate if needed
  }}
  yAxis={{
    labels: longLabelList,
    opposedPosition: false
  }}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

### Issue 4: Large Dataset Performance

**Symptoms:** Slow rendering, browser lag with >5000 cells

**Solution:**
```jsx
// Force Canvas rendering for large data
<HeatMapComponent
        id='heatmap'
        dataSource={largeData}
        renderingMode='Canvas'      // Not 'Auto'
        showTooltip={false}
    >
        <Inject services={[Legend]} />
    </HeatMapComponent>
```

### Issue 5: Tooltips Not Showing

**Symptoms:** Hover on cells, no tooltip appears

**Diagnosis:**
```jsx
// Check if Tooltip service is injected
const heatmap = document.querySelector('.e-heatmap');
console.log('Has tooltip service:', heatmap.ej2_instances?.[0]?.tooltipModule);
```

**Solution:**
```jsx
import { Tooltip } from '@syncfusion/ej2-react-heatmap';

<HeatMapComponent id='heatmap' dataSource={data}>
    <Inject services={[Legend, Tooltip]} />  // Add Tooltip
</HeatMapComponent>
```

## Migration from EJ1

### EJ1 vs EJ2 Differences

| Feature | EJ1 | EJ2 |
|---------|-----|-----|
| Package | @syncfusion/ej-react | @syncfusion/ej2-react-heatmap |
| Component | ejHeatMap | HeatMapComponent |
| Data binding | data property | dataSource property |
| Events | onCellClick | cellClick |
| Rendering | Auto | SVG/Canvas modes |

### Basic Migration Example

**EJ1 Code:**
```jsx
// Old EJ1 way
<EjHeatMap
  dataSource={data}
  onCellClick={handleClick}
/>
```

**EJ2 Code:**
```jsx
// New EJ2 way
import { HeatMapComponent, Inject, Legend, Tooltip } from '@syncfusion/ej2-react-heatmap';

<HeatMapComponent
    dataSource={data}
    cellClick={handleClick}
>
    <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

### Data Format Migration

**EJ1:**
```jsx
const data = [
  [10, 20, 30],
  [40, 50, 60]
];
```

**EJ2:** (Same format works)
```jsx
const data = [
  [10, 20, 30],
  [40, 50, 60]
];

// Or JSON format (EJ2 only)
const data = [
  { row: 'A', column: 'X', value: 10 },
  { row: 'A', column: 'Y', value: 20 }
];
```

### Event Name Changes

**EJ1 → EJ2:**
- `onCellClick` → `cellClick`
- `onCellMouseMove` → `cellMouseMove`
- `onCellMouseLeave` → `cellMouseLeave`
- `onCellSelection` → `cellSelected`

### Complete Migration Template

```jsx
// Old EJ1 component
/*
<EjHeatMap
  id='heatmap'
  dataSource={data}
  xAxis={{ labels: ['Q1', 'Q2'] }}
  yAxis={{ labels: ['North', 'South'] }}
  onCellClick={handleCellClick}
  onCellMouseMove={handleMouseMove}
/>
*/

// New EJ2 component
import { HeatMapComponent, Inject, Legend, Tooltip } from '@syncfusion/ej2-react-heatmap';
import '@syncfusion/ej2-base/styles/material.css';

<HeatMapComponent
  id='heatmap'
  dataSource={data}
  xAxis={{ labels: ['Q1', 'Q2'] }}
  yAxis={{ labels: ['North', 'South'] }}
  cellClick={handleCellClick}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```
