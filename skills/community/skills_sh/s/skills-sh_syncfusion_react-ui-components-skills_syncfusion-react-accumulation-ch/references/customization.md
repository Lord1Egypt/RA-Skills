# Customization

## Table of Contents
- [Overview](#overview)
- [Point Colors](#point-colors)
- [Border Customization](#border-customization)
- [Pattern Fills](#pattern-fills)
- [Conditional Styling with pointRender](#conditional-styling-with-pointrender)
- [Series Customization](#series-customization)
- [Exploding Slices](#exploding-slices)
- [Chart Background and Margins](#chart-background-and-margins)
- [Font and Text Styling](#font-and-text-styling)

## Overview

Customization options allow you to control colors, borders, patterns, and visual styles to match your application's design system or highlight specific data points.

## Point Colors

Customize individual point colors using color mapping or inline styles:

**Method 1: Color Mapping from Data**

```tsx
import { 
  AccumulationChartComponent,
  AccumulationSeriesCollectionDirective,
  AccumulationSeriesDirective,
  Inject,
  PieSeries
} from '@syncfusion/ej2-react-charts';

function ColorMapping() {
  const data = [
    { x: 'Chrome', y: 61.3, fill: '#4285F4' },
    { x: 'Safari', y: 24.6, fill: '#0088FF' },
    { x: 'Firefox', y: 14.1, fill: '#FF6600' }
  ];

  return (
    <AccumulationChartComponent id='color-mapped'>
      <Inject services={[PieSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          pointColorMapping='fill'  // Map 'fill' field to colors
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

**Method 2: Palette Colors**

```tsx
function PaletteColors() {
  const data = [
    { x: 'Product A', y: 35 },
    { x: 'Product B', y: 28 },
    { x: 'Product C', y: 22 },
    { x: 'Product D', y: 15 }
  ];

  const customPalette = ['#667eea', '#764ba2', '#f093fb', '#4facfe'];

  return (
    <AccumulationChartComponent 
      id='palette-colors'
      palettes={customPalette}  // Custom color palette
    >
      <Inject services={[PieSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Border Customization

Customize slice borders using the `border` property:

```tsx
function BorderCustomization() {
  const data = [
    { x: 'Jan', y: 35 },
    { x: 'Feb', y: 28 },
    { x: 'Mar', y: 34 }
  ];

  return (
    <AccumulationChartComponent id='border-custom'>
      <Inject services={[PieSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          border={{
            width: 3,
            color: '#ffffff'  // White borders between slices
          }}
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

**Border properties:**
- `width`: Border thickness (pixels)
- `color`: Border color (hex, rgb, name)

**Example with varied borders:**

```tsx
function VariedBorders() {
  const data = [
    { x: 'Success', y: 45, fill: '#28a745', borderColor: '#1e7e34', borderWidth: 2 },
    { x: 'Warning', y: 30, fill: '#ffc107', borderColor: '#e0a800', borderWidth: 2 },
    { x: 'Error', y: 25, fill: '#dc3545', borderColor: '#bd2130', borderWidth: 2 }
  ];

  const onPointRender = (args: any) => {
    args.border.width = args.data.borderWidth;
    args.border.color = args.data.borderColor;
  };

  return (
    <AccumulationChartComponent 
      id='varied-borders'
      pointRender={onPointRender}
    >
      <Inject services={[PieSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          pointColorMapping='fill'
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Pattern Fills

Apply pattern fills to slices for printing or accessibility:

```tsx
function PatternFills() {
  const data = [
    { x: 'Category A', y: 35 },
    { x: 'Category B', y: 28 },
    { x: 'Category C', y: 22 }
  ];

  const onPointRender = (args: any) => {
    const patterns = [
      'url(#pattern1)',  // Dots
      'url(#pattern2)',  // Stripes
      'url(#pattern3)'   // Grid
    ];
    args.fill = patterns[args.point.index];
  };

  return (
    <div>
      <svg width="0" height="0">
        <defs>
          <pattern id="pattern1" patternUnits="userSpaceOnUse" width="8" height="8">
            <circle cx="4" cy="4" r="2" fill="#667eea" />
          </pattern>
          <pattern id="pattern2" patternUnits="userSpaceOnUse" width="8" height="8">
            <path d="M 0,0 l 8,8" stroke="#764ba2" strokeWidth="2" />
          </pattern>
          <pattern id="pattern3" patternUnits="userSpaceOnUse" width="10" height="10">
            <rect width="10" height="10" fill="none" stroke="#f093fb" strokeWidth="1" />
          </pattern>
        </defs>
      </svg>

      <AccumulationChartComponent 
        id='pattern-fills'
        pointRender={onPointRender}
      >
        <Inject services={[PieSeries]} />
        <AccumulationSeriesCollectionDirective>
          <AccumulationSeriesDirective
            dataSource={data}
            xName='x'
            yName='y'
          />
        </AccumulationSeriesCollectionDirective>
      </AccumulationChartComponent>
    </div>
  );
}
```

## Conditional Styling with pointRender

Apply dynamic styling based on data values:

```tsx
import { IAccPointRenderEventArgs } from '@syncfusion/ej2-react-charts';

function ConditionalStyling() {
  const data = [
    { x: 'Q1', y: 7, target: 10 },
    { x: 'Q2', y: 15, target: 12 },
    { x: 'Q3', y: 21, target: 20 },
    { x: 'Q4', y: 18, target: 22 }
  ];

  const onPointRender = (args: IAccPointRenderEventArgs): void => {
    const point = args.data as any;
    
    // Color based on target achievement
    if (point.y >= point.target) {
      args.fill = '#28a745';  // Green for success
      args.border = { width: 2, color: '#1e7e34' };
    } else {
      args.fill = '#dc3545';  // Red for below target
      args.border = { width: 2, color: '#bd2130' };
    }
  };

  return (
    <AccumulationChartComponent 
      id='conditional-styling'
      title='Quarterly Performance vs Target'
      pointRender={onPointRender}
    >
      <Inject services={[PieSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

**Advanced conditional styling:**

```tsx
function AdvancedConditionalStyling() {
  const data = [
    { x: 'Product A', y: 45, category: 'premium' },
    { x: 'Product B', y: 30, category: 'standard' },
    { x: 'Product C', y: 25, category: 'budget' }
  ];

  const onPointRender = (args: IAccPointRenderEventArgs): void => {
    const point = args.data as any;
    
    const categoryStyles: any = {
      premium: { 
        fill: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        borderWidth: 3,
        borderColor: '#764ba2'
      },
      standard: { 
        fill: '#4facfe',
        borderWidth: 2,
        borderColor: '#00c6ff'
      },
      budget: { 
        fill: '#43e97b',
        borderWidth: 1,
        borderColor: '#38f9d7'
      }
    };

    const style = categoryStyles[point.category];
    if (style) {
      args.fill = style.fill;
      args.border = { 
        width: style.borderWidth, 
        color: style.borderColor 
      };
    }
  };

  return (
    <AccumulationChartComponent 
      id='advanced-conditional'
      pointRender={onPointRender}
    >
      <Inject services={[PieSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Series Customization

Customize series-level properties:

```tsx
function SeriesCustomization() {
  const data = [
    { x: 'Chrome', y: 61.3 },
    { x: 'Safari', y: 24.6 },
    { x: 'Firefox', y: 14.1 }
  ];

  return (
    <AccumulationChartComponent id='series-custom'>
      <Inject services={[PieSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          radius='90%'               // Slice radius
          innerRadius='40%'          // Doughnut inner radius
          startAngle={0}             // Starting angle
          endAngle={360}             // Ending angle
          opacity={0.9}              // Transparency
          animation={{ enable: true, duration: 1000 }}
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Exploding Slices

Emphasize specific slices by separating them from the chart:

```tsx
function ExplodingSlices() {
  const data = [
    { x: 'Chrome', y: 61.3, explode: true },  // Explode this slice
    { x: 'Safari', y: 24.6, explode: false },
    { x: 'Firefox', y: 14.1, explode: false }
  ];

  return (
    <AccumulationChartComponent id='exploding-slices'>
      <Inject services={[PieSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          explode={true}            // Enable explode feature
          explodeOffset='10%'       // Distance to separate
          explodeIndex={0}          // Index of slice to explode
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

**Explode all slices:**

```tsx
function ExplodeAll() {
  const data = [
    { x: 'A', y: 25 },
    { x: 'B', y: 25 },
    { x: 'C', y: 25 },
    { x: 'D', y: 25 }
  ];

  return (
    <AccumulationChartComponent id='explode-all'>
      <Inject services={[PieSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          explode={true}
          explodeAll={true}         // Explode all slices
          explodeOffset='5%'
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Chart Background and Margins

Customize chart container appearance:

```tsx
function BackgroundAndMargins() {
  const data = [
    { x: 'Product A', y: 45 },
    { x: 'Product B', y: 30 },
    { x: 'Product C', y: 25 }
  ];

  return (
    <AccumulationChartComponent 
      id='background-custom'
      background='#f5f5f5'           // Chart background
      margin={{ left: 20, right: 20, top: 20, bottom: 20 }}
      border={{ width: 2, color: '#e0e0e0' }}
    >
      <Inject services={[PieSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Font and Text Styling

Customize text elements throughout the chart:

```tsx
function FontStyling() {
  const data = [
    { x: 'Chrome', y: 61.3 },
    { x: 'Safari', y: 24.6 },
    { x: 'Firefox', y: 14.1 }
  ];

  return (
    <AccumulationChartComponent 
      id='font-styling'
      title='Browser Market Share'
      titleStyle={{
        fontFamily: 'Segoe UI',
        size: '18px',
        fontWeight: '600',
        color: '#333'
      }}
    >
      <Inject services={[PieSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

**Complete customization example:**

```tsx
function FullyCustomizedChart() {
  const data = [
    { x: 'Chrome', y: 61.3, fill: '#4285F4' },
    { x: 'Safari', y: 24.6, fill: '#0088FF' },
    { x: 'Firefox', y: 14.1, fill: '#FF6600' }
  ];

  const onPointRender = (args: IAccPointRenderEventArgs): void => {
    // Add subtle shadow effect
    args.border = { width: 2, color: '#ffffff' };
  };

  return (
    <AccumulationChartComponent 
      id='fully-customized'
      title='Browser Statistics 2024'
      titleStyle={{
        fontFamily: 'Segoe UI',
        size: '20px',
        fontWeight: 'bold',
        color: '#333'
      }}
      background='linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)'
      margin={{ left: 30, right: 30, top: 40, bottom: 30 }}
      pointRender={onPointRender}
    >
      <Inject services={[PieSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          pointColorMapping='fill'
          radius='85%'
          opacity={0.95}
          animation={{ enable: true, duration: 1200 }}
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Selection and Highlighting

Enable point selection and highlighting for interactive charts:

**Selection Mode:**

```tsx
import { 
  AccumulationChartComponent,
  AccumulationSeriesCollectionDirective,
  AccumulationSeriesDirective,
  Inject,
  PieSeries,
  AccumulationSelection
} from '@syncfusion/ej2-react-charts';

function SelectionExample() {
  const data = [
    { x: 'Chrome', y: 61.3 },
    { x: 'Safari', y: 24.6 },
    { x: 'Firefox', y: 14.1 },
    { x: 'Edge', y: 5.0 }
  ];

  const onSelectionComplete = (args: any) => {
    console.log('Selected point:', args);
  };

  return (
    <AccumulationChartComponent 
      id='selection-chart'
      selectionMode='Point'  // Enable point selection
      isMultiSelect={false}  // Single selection only
      selectedDataIndexes={[{ series: 0, point: 0 }]}  // Pre-select first point
      selectionPattern='DiagonalForward'  // Pattern for selected points
      selectionComplete={onSelectionComplete}
    >
      <Inject services={[PieSeries, AccumulationSelection]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

**Highlight Mode:**

```tsx
import { AccumulationHighlight } from '@syncfusion/ej2-react-charts';

function HighlightExample() {
  const data = [
    { x: 'Product A', y: 45 },
    { x: 'Product B', y: 30 },
    { x: 'Product C', y: 25 }
  ];

  return (
    <AccumulationChartComponent 
      id='highlight-chart'
      highlightMode='Point'  // Enable point highlighting on hover
      highlightColor='#ff4081'  // Custom highlight color
      highlightPattern='Dots'  // Pattern for highlighted points
    >
      <Inject services={[PieSeries, AccumulationHighlight]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

**Multi-Select:**

```tsx
function MultiSelectExample() {
  const [selectedPoints, setSelectedPoints] = React.useState<any[]>([]);
  
  const data = [
    { x: 'Q1', y: 35 },
    { x: 'Q2', y: 28 },
    { x: 'Q3', y: 42 },
    { x: 'Q4', y: 31 }
  ];

  const onPointClick = (args: any) => {
    const pointInfo = `${args.point.x}: ${args.point.y}`;
    setSelectedPoints(prev => 
      prev.includes(pointInfo) 
        ? prev.filter(p => p !== pointInfo)
        : [...prev, pointInfo]
    );
  };

  return (
    <div>
      <div style={{ marginBottom: '10px' }}>
        <strong>Selected Points:</strong> {
          selectedPoints.length > 0 
            ? selectedPoints.join(', ') 
            : 'None'
        }
      </div>

      <AccumulationChartComponent 
        id='multi-select'
        selectionMode='Point'
        isMultiSelect={true}  // Enable multiple selection
        pointClick={onPointClick}
      >
        <Inject services={[PieSeries, AccumulationSelection]} />
        <AccumulationSeriesCollectionDirective>
          <AccumulationSeriesDirective
            dataSource={data}
            xName='x'
            yName='y'
          />
        </AccumulationSeriesCollectionDirective>
      </AccumulationChartComponent>
    </div>
  );
}
```

### SelectionComplete Event

Capture selection changes using the `selectionComplete` event:

```tsx
import { IAccSelectionCompleteEventArgs } from '@syncfusion/ej2-react-charts';

function SelectionCompleteExample() {
  const [selectedItems, setSelectedItems] = React.useState<string[]>([]);

  const onSelectionComplete = (args: IAccSelectionCompleteEventArgs): void => {
    const selected = args.selectedDataValues.map(item => 
      `${item.x}: ${item.y}`
    );
    setSelectedItems(selected);
  };

  return (
    <div>
      <AccumulationChartComponent 
        id='selection-complete'
        selectionMode='Point'
        isMultiSelect={true}
        selectionComplete={onSelectionComplete}
      >
        <Inject services={[PieSeries, AccumulationSelection]} />
        <AccumulationSeriesCollectionDirective>
          {/* your series */}
        </AccumulationSeriesCollectionDirective>
      </AccumulationChartComponent>

      {selectedItems.length > 0 && (
        <div style={{ marginTop: '15px' }}>
          <strong>Selected:</strong> {selectedItems.join(', ')}
        </div>
      )}
    </div>
  );
}
```

**When to use**: Track user selections for filtering, drill-down, or analytics.

## Common Issues and Solutions

**Issue: Custom colors not applying**
- Solution: Ensure `pointColorMapping` property points to correct field
- Solution: Verify data has fill/color field with valid color values
- Solution: Check that palette array has enough colors for all points

**Issue: Border not visible**
- Solution: Increase `border.width` value
- Solution: Use contrasting color for border
- Solution: Check if slice colors are too similar to border

**Issue: Exploded slice not separating**
- Solution: Verify `explode: true` is set on series
- Solution: Increase `explodeOffset` value ('10%', '15%')
- Solution: Check `explodeIndex` matches intended slice

**Issue: pointRender changes not applying**
- Solution: Ensure event handler is properly attached
- Solution: Verify args properties are being modified correctly
- Solution: Check that changes don't conflict with other settings

**Issue: Gradient fills not working**
- Solution: Use SVG patterns or pointRender for complex fills
- Solution: Verify gradient syntax is correct
- Solution: Consider using solid colors for better browser compatibility
