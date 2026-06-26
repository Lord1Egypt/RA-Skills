# Accessibility

## Table of Contents
- [Overview](#overview)
- [WCAG Compliance](#wcag-compliance)
- [Keyboard Navigation](#keyboard-navigation)
- [ARIA Attributes](#aria-attributes)
- [Screen Reader Support](#screen-reader-support)
- [High Contrast Mode](#high-contrast-mode)
- [Focus Management](#focus-management)
- [Accessible Color Palettes](#accessible-color-palettes)

## Overview

Accessibility features ensure that accumulation charts are usable by people with disabilities, including those who rely on screen readers, keyboard navigation, or high contrast modes.

## WCAG Compliance

Syncfusion Accumulation Charts follow WCAG 2.1 guidelines for accessible data visualizations:

```tsx
import { 
  AccumulationChartComponent,
  AccumulationSeriesCollectionDirective,
  AccumulationSeriesDirective,
  Inject,
  PieSeries,
  AccumulationDataLabel
} from '@syncfusion/ej2-react-charts';

function AccessibleChart() {
  const data = [
    { x: 'Chrome', y: 61.3 },
    { x: 'Safari', y: 24.6 },
    { x: 'Firefox', y: 14.1 }
  ];

  return (
    <AccumulationChartComponent 
      id='accessible-chart'
      title='Browser Market Share'
      tabIndex={0}  // Make chart focusable
    >
      <Inject services={[PieSeries, AccumulationDataLabel]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          dataLabel={{ visible: true }}  // Visible labels for all users
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

**WCAG compliance features:**
- Keyboard navigation support (Level A)
- Screen reader compatibility (Level A)
- Color contrast ratios meet AA standards
- Text alternatives for visual content (Level A)
- Focus indicators (Level AA)

## Keyboard Navigation

Enable full keyboard control for chart interaction:

```tsx
function KeyboardNavigation() {
  const data = [
    { x: 'Q1', y: 35 },
    { x: 'Q2', y: 28 },
    { x: 'Q3', y: 42 },
    { x: 'Q4', y: 31 }
  ];

  return (
    <AccumulationChartComponent 
      id='keyboard-nav'
      title='Quarterly Sales (Use arrow keys to navigate)'
      tabIndex={0}
      selectionMode='Point'  // Enable point selection
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

**Keyboard shortcuts:**
- **Tab**: Focus on chart
- **Arrow Keys** (←→↑↓): Navigate between data points
- **Enter/Space**: Select focused point
- **Escape**: Clear selection
- **Home**: Focus first point
- **End**: Focus last point

**Keyboard event handling:**

```tsx
function KeyboardEvents() {
  const data = [
    { x: 'Chrome', y: 61.3 },
    { x: 'Safari', y: 24.6 },
    { x: 'Firefox', y: 14.1 }
  ];

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ' ') {
      console.log('Point selected via keyboard');
    }
  };

  return (
    <AccumulationChartComponent 
      id='keyboard-events'
      tabIndex={0}
      onKeyDown={handleKeyDown}
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

## ARIA Attributes

ARIA (Accessible Rich Internet Applications) attributes provide context for assistive technologies:

```tsx
function ARIAAttributes() {
  const data = [
    { x: 'Chrome', y: 61.3 },
    { x: 'Safari', y: 24.6 },
    { x: 'Firefox', y: 14.1 }
  ];

  return (
    <div>
      <AccumulationChartComponent 
        id='aria-chart'
        title='Browser Market Share'
        tabIndex={0}
        role='img'
        aria-label='Pie chart showing browser market share. Chrome leads with 61.3%, followed by Safari at 24.6% and Firefox at 14.1%'
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
      
      {/* Text alternative for complete accessibility */}
      <div className="sr-only">
        <h3>Browser Market Share Data</h3>
        <ul>
          {data.map((item, index) => (
            <li key={index}>
              {item.x}: {item.y}%
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
```

**Key ARIA attributes:**
- `role='img'`: Identifies chart as image
- `aria-label`: Provides chart description
- `aria-describedby`: Links to detailed description
- `aria-live`: Announces dynamic updates
- `tabIndex={0}`: Makes element keyboard-focusable

**Dynamic ARIA labels:**

```tsx
function DynamicARIA() {
  const [selectedPoint, setSelectedPoint] = React.useState<string>('');
  
  const data = [
    { x: 'Product A', y: 45 },
    { x: 'Product B', y: 30 },
    { x: 'Product C', y: 25 }
  ];

  const total = data.reduce((sum, item) => sum + item.y, 0);

  const onPointClick = (args: any) => {
    setSelectedPoint(`${args.point.x}: ${args.point.y} units (${((args.point.y/total)*100).toFixed(1)}%)`);
  };

  return (
    <div>
      <AccumulationChartComponent 
        id='dynamic-aria'
        tabIndex={0}
        pointClick={onPointClick}
        aria-label={`Sales distribution chart. ${selectedPoint || 'Click a slice for details'}`}
        aria-live='polite'
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
      
      <div 
        id='chart-description' 
        aria-live='polite'
        style={{ position: 'absolute', left: '-9999px' }}
      >
        {selectedPoint}
      </div>
    </div>
  );
}
```

## Screen Reader Support

Optimize charts for screen reader users:

```tsx
function ScreenReaderOptimized() {
  const data = [
    { x: 'Completed', y: 65, status: 'success' },
    { x: 'In Progress', y: 25, status: 'warning' },
    { x: 'Failed', y: 10, status: 'error' }
  ];

  const total = data.reduce((sum, item) => sum + item.y, 0);

  const generateDescription = () => {
    const descriptions = data.map(item => 
      `${item.x}: ${item.y} tasks, which is ${((item.y/total)*100).toFixed(1)}% of total`
    );
    return `Task status chart. Total ${total} tasks. ${descriptions.join('. ')}.`;
  };

  return (
    <div>
      <h2 id='chart-title'>Task Status Distribution</h2>
      
      <AccumulationChartComponent 
        id='screen-reader-chart'
        tabIndex={0}
        role='img'
        aria-labelledby='chart-title'
        aria-describedby='chart-detailed-description'
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

      <div 
        id='chart-detailed-description' 
        className='sr-only'
      >
        {generateDescription()}
      </div>

      {/* Fallback data table */}
      <table className='sr-only'>
        <caption>Task Status Data</caption>
        <thead>
          <tr>
            <th>Status</th>
            <th>Count</th>
            <th>Percentage</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              <td>{item.x}</td>
              <td>{item.y}</td>
              <td>{((item.y/total)*100).toFixed(1)}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

**Screen reader best practices:**
- Provide meaningful chart titles
- Include detailed text descriptions
- Offer data table alternative
- Use semantic HTML structure
- Announce dynamic updates with aria-live

## High Contrast Mode

Support high contrast mode for users with visual impairments:

```tsx
function HighContrastMode() {
  const data = [
    { x: 'Category A', y: 35 },
    { x: 'Category B', y: 28 },
    { x: 'Category C', y: 22 },
    { x: 'Category D', y: 15 }
  ];

  // High contrast color palette
  const highContrastPalette = [
    '#000000',  // Black
    '#FFFFFF',  // White
    '#FFFF00',  // Yellow
    '#00FF00'   // Green
  ];

  return (
    <AccumulationChartComponent 
      id='high-contrast'
      palettes={highContrastPalette}
    >
      <Inject services={[PieSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          border={{
            width: 3,
            color: '#000000'  // Strong borders for definition
          }}
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

**High contrast features:**
- Strong color contrasts (minimum 4.5:1 ratio)
- Bold borders between slices
- Clear focus indicators
- Pattern fills as alternative to color

## Focus Management

Implement clear focus indicators and management:

```tsx
function FocusManagement() {
  const chartRef = React.useRef<AccumulationChartComponent>(null);
  const data = [
    { x: 'Item A', y: 45 },
    { x: 'Item B', y: 30 },
    { x: 'Item C', y: 25 }
  ];

  const focusChart = () => {
    chartRef.current?.element?.focus();
  };

  return (
    <div>
      <button onClick={focusChart}>
        Focus Chart
      </button>

      <AccumulationChartComponent 
        id='focus-management'
        ref={chartRef}
        tabIndex={0}
        selectionMode='Point'
        style={{
          outline: '2px solid transparent',
          outlineOffset: '2px'
        }}
        // CSS will handle focus styling
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

      <style>{`
        #focus-management:focus {
          outline: 3px solid #0078d4;
          outline-offset: 2px;
        }
      `}</style>
    </div>
  );
}
```

## Accessible Color Palettes

Use color-blind friendly palettes:

```tsx
function ColorBlindFriendly() {
  const data = [
    { x: 'Category A', y: 35 },
    { x: 'Category B', y: 28 },
    { x: 'Category C', y: 22 },
    { x: 'Category D', y: 15 }
  ];

  // Color-blind safe palette (deuteranopia-friendly)
  const accessiblePalette = [
    '#0173B2',  // Blue
    '#DE8F05',  // Orange
    '#029E73',  // Green
    '#CC78BC'   // Purple
  ];

  return (
    <AccumulationChartComponent 
      id='colorblind-friendly'
      title='Accessible Color Palette'
      palettes={accessiblePalette}
    >
      <Inject services={[PieSeries, AccumulationDataLabel]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          dataLabel={{ visible: true }}  // Labels help identify categories
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

**Accessible palette guidelines:**
- Avoid red-green combinations
- Use high luminance contrast
- Include patterns or textures
- Test with color blindness simulators
- Provide labels as primary identification

## Common Issues and Solutions

**Issue: Chart not keyboard accessible**
- Solution: Add `tabIndex={0}` to make chart focusable
- Solution: Enable `selectionMode='Point'` for navigation
- Solution: Verify chart is not inside non-focusable container

**Issue: Screen reader not announcing chart**
- Solution: Add `role='img'` and `aria-label` attributes
- Solution: Provide detailed text description with `aria-describedby`
- Solution: Include hidden data table alternative

**Issue: Focus indicator not visible**
- Solution: Add CSS outline styles for :focus state
- Solution: Ensure outline contrasts with background
- Solution: Test with keyboard-only navigation

**Issue: Colors hard to distinguish**
- Solution: Use accessible color palettes
- Solution: Add border to slices for definition
- Solution: Enable data labels for all slices
- Solution: Consider pattern fills

**Issue: Dynamic updates not announced**
- Solution: Use `aria-live='polite'` or 'assertive'
- Solution: Update aria-label when data changes
- Solution: Provide status messages for updates
