# Axis, Ticks & Labels in React Linear Gauge

See API Reference: [API Reference](api-reference.md)

## Table of Contents

- [Axis Range](#axis-range)
  - [Setting Minimum and Maximum](#setting-minimum-and-maximum)
- [Line Customization](#line-customization)
  - [Example: Custom Colored Line](#example-custom-colored-line)
- [Ticks Configuration](#ticks-configuration)
  - [Major Ticks](#major-ticks)
  - [Minor Ticks](#minor-ticks)
  - [Both Together](#both-together)
- [Label Customization](#label-customization)
  - [Basic Label Styling](#basic-label-styling)
  - [Common Label Formats](#common-label-formats)
  - [Label Position and Offset](#label-position-and-offset)
  - [Example: Temperature Labels](#example-temperature-labels)
- [Multiple Axes](#multiple-axes)
- [Axis Orientation](#axis-orientation)
  - [Vertical (Default)](#vertical-default)
  - [Horizontal](#horizontal)
  - [Dynamic Orientation](#dynamic-orientation)
- [Common Patterns](#common-patterns)
  - [Pattern 1: Temperature with Semantic Ranges](#pattern-1-temperature-with-semantic-ranges)
  - [Pattern 2: Percentage with Decimal Labels](#pattern-2-percentage-with-decimal-labels)
  - [Pattern 3: Compact Axis with Minimal Ticks](#pattern-3-compact-axis-with-minimal-ticks)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)

## Axis Range

The axis defines the scale range for the Linear Gauge using `minimum` and `maximum` properties. These values determine the start and end points displayed on the gauge.

### Setting Minimum and Maximum

```tsx
import React from 'react';
import { LinearGaugeComponent, AxesDirective, AxisDirective } 
  from '@syncfusion/ej2-react-lineargauge';

export function App() {
  return (
    <LinearGaugeComponent>
      <AxesDirective>
        <AxisDirective 
          minimum={20} 
          maximum={200}
        >
        </AxisDirective>
      </AxesDirective>
    </LinearGaugeComponent>
  );
}

export default App;
```

**Key Props:**
- `minimum` - Start value of the axis (default: 0)
- `maximum` - End value of the axis (default: 100)

**Use Cases:**
- Temperature gauge: `minimum={-50}` `maximum={50}`
- Percentage: `minimum={0}` `maximum={100}`
- Speed: `minimum={0}` `maximum={200}`

## Line Customization

The axis line is the baseline of the gauge. Customize its appearance using the `line` property object:

```tsx
<AxisDirective 
  minimum={0} 
  maximum={100}
  line={{
    height: 150,        // Length of the axis line in pixels
    width: 2,           // Thickness of the axis line
    color: '#4286f4',   // Line color (hex, rgb, or name)
    offset: 2           // Distance from the gauge container edge
  }}
>
</AxisDirective>
```

**Line Properties:**
- `height` - Length of the axis line (number in pixels)
- `width` - Thickness of the axis line (number in pixels, default: 1)
- `color` - Color of the line (default: '#000000')
- `offset` - Offset from the container edge (default: 0)

### Example: Custom Colored Line

```tsx
<AxisDirective 
  line={{
    height: 200,
    width: 3,
    color: '#FF6B6B',
    offset: 10
  }}
>
</AxisDirective>
```

## Ticks Configuration

Ticks are interval markers on the axis. There are two types:
- **Major ticks** - Larger marks at primary intervals
- **Minor ticks** - Smaller marks at secondary intervals

### Major Ticks

```tsx
<AxisDirective 
  minimum={0}
  maximum={100}
  majorTicks={{
    interval: 20,      // Spacing between major ticks
    height: 15,        // Length of each tick
    width: 2,          // Thickness of each tick
    color: '#000000'   // Color of ticks
  }}
>
</AxisDirective>
```

### Minor Ticks

Minor ticks appear between major ticks:

```tsx
<AxisDirective 
  minimum={0}
  maximum={100}
  minorTicks={{
    interval: 5,       // Spacing between minor ticks
    height: 8,         // Length of each tick
    width: 1,          // Thickness of each tick
    color: '#999999'   // Color of ticks
  }}
>
</AxisDirective>
```

### Both Together

```tsx
<AxisDirective 
  minimum={20}
  maximum={140}
  majorTicks={{ interval: 20, height: 15, color: '#333333' }}
  minorTicks={{ interval: 5, height: 8, color: '#CCCCCC' }}
>
</AxisDirective>
```

## Label Customization

Labels are the numeric values displayed along the axis. Customize their appearance and format:

### Basic Label Styling

```tsx
<AxisDirective 
  minimum={0}
  maximum={100}
  labelStyle={{
    format: '{value}%',           // Format with placeholder
    font: {
      size: '12px',               // Font size
      color: '#333333',          // Text color
      fontFamily: 'Arial'
    }
  }}
>
</AxisDirective>
```

### Common Label Formats

```tsx
// Percentage
labelStyle={{ format: '{value}%' }}

// Temperature with unit
labelStyle={{ format: '{value}°C' }}

// Decimal places
labelStyle={{ format: '{value:.2f}' }}

// Currency
labelStyle={{ format: '${value}' }}

// Custom text
labelStyle={{ format: 'Value: {value}' }}
```

### Label Position and Offset

```tsx
<AxisDirective 
  labelStyle={{
    position: 'Outside',   // 'Inside' or 'Outside'
    offset: 10,            // Distance from axis line
    format: '{value}°C'
  }}
>
</AxisDirective>
```

### Example: Temperature Labels

```tsx
<AxisDirective 
  minimum={-50}
  maximum={50}
  labelStyle={{
    format: '{value}°C',
    font: {
      size: '14px',
      color: '#FF5722',
      fontFamily: 'Georgia',
      fontStyle: 'italic'
    }
  }}
  majorTicks={{ interval: 10 }}
  minorTicks={{ interval: 5 }}
>
</AxisDirective>
```

## Multiple Axes

A single gauge can have multiple axes stacked vertically. This is useful for comparing related measurements:

```tsx
import React from 'react';
import { LinearGaugeComponent, AxesDirective, AxisDirective, 
         PointersDirective, PointerDirective, RangesDirective, RangeDirective } 
  from '@syncfusion/ej2-react-lineargauge';

export function App() {
  return (
    <LinearGaugeComponent 
      title="Multiple Axes Example"
      height="500px"
    >
      <AxesDirective>
        {/* First Axis - Temperature */}
        <AxisDirective 
          minimum={0}
          maximum={100}
          labelStyle={{ format: '{value}°C' }}
          line={{ height: 150, offset: 20 }}
        >
          <PointersDirective>
            <PointerDirective value={45} />
          </PointersDirective>
        </AxisDirective>

        {/* Second Axis - Humidity */}
        <AxisDirective 
          minimum={0}
          maximum={100}
          labelStyle={{ format: '{value}%' }}
          line={{ height: 150, offset: 100 }}
        >
          <PointersDirective>
            <PointerDirective value={65} />
          </PointersDirective>
        </AxisDirective>

        {/* Third Axis - Pressure */}
        <AxisDirective 
          minimum={950}
          maximum={1050}
          labelStyle={{ format: '{value}mb' }}
          line={{ height: 150, offset: 180 }}
        >
          <PointersDirective>
            <PointerDirective value={1013} />
          </PointersDirective>
        </AxisDirective>
      </AxesDirective>
    </LinearGaugeComponent>
  );
}

export default App;
```

**Key Points:**
- Use `line.offset` to position each axis vertically
- Each axis can have different ranges, labels, and pointers
- Ideal for comparing multiple metrics in one view

## Axis Orientation

The Linear Gauge can be rendered in two orientations:

### Vertical (Default)

```tsx
<LinearGaugeComponent orientation="Vertical">
  <AxesDirective>
    <AxisDirective minimum={0} maximum={100} />
  </AxesDirective>
</LinearGaugeComponent>
```

### Horizontal

```tsx
<LinearGaugeComponent orientation="Horizontal">
  <AxesDirective>
    <AxisDirective minimum={0} maximum={100} />
  </AxesDirective>
</LinearGaugeComponent>
```

### Dynamic Orientation

Choose based on container or user preference:

```tsx
const [orientation, setOrientation] = React.useState('Horizontal');

<LinearGaugeComponent orientation={orientation}>
  {/* axes */}
</LinearGaugeComponent>

<button onClick={() => setOrientation('Vertical')}>
  Switch to Vertical
</button>
```

## Common Patterns

### Pattern 1: Temperature with Semantic Ranges

```tsx
<AxisDirective 
  minimum={-40}
  maximum={50}
  labelStyle={{
    format: '{value}°C',
    font: { size: '12px' }
  }}
  majorTicks={{ interval: 10 }}
  minorTicks={{ interval: 2 }}
  line={{ height: 200, width: 2, color: '#1976D2' }}
>
</AxisDirective>
```

### Pattern 2: Percentage with Decimal Labels

```tsx
<AxisDirective 
  minimum={0}
  maximum={100}
  labelStyle={{ 
    format: '{value:.1f}%',
    font: { size: '11px' }
  }}
  majorTicks={{ interval: 25 }}
  minorTicks={{ interval: 5 }}
>
</AxisDirective>
```

### Pattern 3: Compact Axis with Minimal Ticks

```tsx
<AxisDirective 
  minimum={0}
  maximum={1000}
  labelStyle={{ format: '{value}ms' }}
  majorTicks={{ interval: 200 }}
  line={{ height: 100 }}
>
</AxisDirective>
```

## Troubleshooting

**Q: Labels are overlapping**
- Reduce font size: `size: '10px'`
- Use fewer major ticks: `interval: 25` instead of `10`
- Increase axis height: `line: { height: 250 }`

**Q: Ticks not showing**
- Verify `interval` is smaller than range (0-100 with interval 50 only shows 2 ticks)
- Ensure `height` > 0

**Q: Format not applying**
- Use `{value}` as placeholder in format string
- Test with simple format first: `'{value}'`

## Next Steps

- Read **Pointer Types** to add and customize pointers
- Read **Ranges & Annotations** to highlight value zones
- Read **Customization** for advanced styling options
