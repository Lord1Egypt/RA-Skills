# Appearance & Dimensions

Reference the API quick guide: [api-reference.md](api-reference.md) for prop names such as `centerX`, `centerY`, `width`, `height`, and `background`.

## Table of Contents
- [Gauge Title](#gauge-title)
  - [Adding a Title](#adding-a-title)
  - [Title Customization](#title-customization)
  - [Title Positioning](#title-positioning)
- [Gauge Position](#gauge-position)
  - [Center Position](#center-position)
    - [Percentage (Recommended)](#percentage-recommended)
    - [In Pixels](#in-pixels)
  - [Common Positioning Examples](#common-positioning-examples)
- [Gauge Dimensions](#gauge-dimensions)
  - [Width and Height](#width-and-height)
  - [Responsive Sizing](#responsive-sizing)
  - [Margins](#margins)
- [Gauge Background and Borders](#gauge-background-and-borders)
  - [Background Color](#background-color)
  - [Border Styling](#border-styling)
  - [Shadow Effects](#shadow-effects)
- [Colors and Styling](#colors-and-styling)
  - [Color Scheme Example](#color-scheme-example)
  - [Dark Mode](#dark-mode)
  - [Gradient and Advanced Styling](#gradient-and-advanced-styling)
- [Responsive Design](#responsive-design)
  - [Mobile-First Approach](#mobile-first-approach)
  - [CSS Media Queries](#css-media-queries)
  - [Flexbox Layout](#flexbox-layout)
- [Container Setup](#container-setup)
  - [Basic Container](#basic-container)
  - [Container with Padding and Borders](#container-with-padding-and-borders)
  - [Grid Layout with Multiple Gauges](#grid-layout-with-multiple-gauges)
  - [Card-Style Container](#card-style-container)
- [Tips and Best Practices](#tips-and-best-practices)

---

## Gauge Title

### Adding a Title

Display a title at the top of the gauge:

```tsx
<CircularGaugeComponent
  title="Speed (km/h)"
>
  {/* gauge content */}
</CircularGaugeComponent>
```

### Title Customization

Customize title appearance with `titleStyle`:

```tsx
<CircularGaugeComponent
  title="Dashboard KPI"
  titleStyle={{
    size: '24px',
    color: '#1976d2',
    fontFamily: 'Arial, sans-serif',
    fontWeight: 'bold',
    alignment: 'Center',  // Center, Far, Near
    opacity: 1
  }}
>
  {/* gauge content */}
</CircularGaugeComponent>
```

### Title Positioning

The title always appears at the top-center by default. To create custom layouts, use CSS:

```tsx
<div style={{ position: 'relative' }}>
  <h2 style={{ textAlign: 'center', marginBottom: '10px' }}>
    Custom Title Position
  </h2>
  <CircularGaugeComponent>
    {/* No title prop, using CSS above */}
  </CircularGaugeComponent>
</div>
```

---

## Gauge Position

### Center Position

The gauge is positioned within its container using `centerX` and `centerY`. These values can be in percentage or pixels:

#### Percentage (Recommended)

Position relative to the container:

```tsx
<CircularGaugeComponent
  centerX="50%"   // Horizontal center (default)
  centerY="50%"   // Vertical center (default)
>
  {/* gauge content */}
</CircularGaugeComponent>
```

**Percentage positioning is responsive** and works well with various container sizes.

#### In Pixels

Absolute pixel positioning:

```tsx
<CircularGaugeComponent
  centerX="200px"   // 200 pixels from left
  centerY="150px"   // 150 pixels from top
>
  {/* gauge content */}
</CircularGaugeComponent>
```

### Common Positioning Examples

```tsx
// Top-left corner
<CircularGaugeComponent centerX="25%" centerY="25%" />

// Top-center
<CircularGaugeComponent centerX="50%" centerY="25%" />

// Top-right corner
<CircularGaugeComponent centerX="75%" centerY="25%" />

// Left side
<CircularGaugeComponent centerX="20%" centerY="50%" />

// Center (default)
<CircularGaugeComponent centerX="50%" centerY="50%" />

// Right side
<CircularGaugeComponent centerX="80%" centerY="50%" />

// Bottom-left corner
<CircularGaugeComponent centerX="25%" centerY="75%" />

// Bottom-center
<CircularGaugeComponent centerX="50%" centerY="75%" />

// Bottom-right corner
<CircularGaugeComponent centerX="75%" centerY="75%" />
```

---

## Gauge Dimensions

### Width and Height

Set explicit dimensions or use CSS:

```tsx
// Option 1: Wrap in div with size
<div style={{ width: '600px', height: '600px' }}>
  <CircularGaugeComponent>
    {/* gauge content */}
  </CircularGaugeComponent>
</div>

// Option 2: Use component props
<CircularGaugeComponent
  width="600"
  height="600"
>
  {/* gauge content */}
</CircularGaugeComponent>
```

**Note:** Circular gauges work best when width and height are equal to maintain a perfect circle.

### Responsive Sizing

For responsive designs, use viewport units or percentages:

```tsx
<div style={{
  width: '100%',
  maxWidth: '600px',
  height: 'auto',
  aspectRatio: '1'  // Maintain square aspect
}}>
  <CircularGaugeComponent>
    {/* gauge content */}
  </CircularGaugeComponent>
</div>
```

### Margins

Add margin to the gauge using container CSS:

```tsx
<div style={{
  width: '100%',
  height: '500px',
  margin: '20px auto',  // Auto horizontal centers
  padding: '20px'
}}>
  <CircularGaugeComponent>
    {/* gauge content */}
  </CircularGaugeComponent>
</div>
```

---

## Gauge Background and Borders

### Background Color

Set the gauge background:

```tsx
<CircularGaugeComponent
  background='#ffffff'  // White background
>
  {/* gauge content */}
</CircularGaugeComponent>

// Transparent
<CircularGaugeComponent
  background='transparent'
>
  {/* gauge content */}
</CircularGaugeComponent>

// Semi-transparent
<CircularGaugeComponent
  background='rgba(255, 255, 255, 0.95)'
>
  {/* gauge content */}
</CircularGaugeComponent>
```

### Border Styling

Add border to the gauge container:

```tsx
<div style={{
  width: '500px',
  height: '500px',
  border: '2px solid #1976d2',
  borderRadius: '8px',
  overflow: 'hidden'
}}>
  <CircularGaugeComponent>
    {/* gauge content */}
  </CircularGaugeComponent>
</div>
```

### Shadow Effects

Add shadow for depth:

```tsx
<div style={{
  width: '500px',
  height: '500px',
  boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
  borderRadius: '8px'
}}>
  <CircularGaugeComponent>
    {/* gauge content */}
  </CircularGaugeComponent>
</div>
```

---

## Colors and Styling

### Color Scheme Example

Create a cohesive color scheme:

```tsx
<CircularGaugeComponent
  background='#f5f5f5'
  title='Performance Gauge'
  titleStyle={{ color: '#1976d2' }}
>
  <AxesDirective>
    <AxisDirective
      lineStyle={{ width: 2, color: '#1976d2' }}
      majorTicks={{ color: '#1976d2' }}
      minorTicks={{ color: '#90caf9' }}
      labelStyle={{ color: '#424242' }}
    >
      <RangesDirective>
        <RangeDirective start={0} end={33} color='#4caf50' startWidth={10} endWidth={10} />
        <RangeDirective start={33} end={66} color='#fbc02d' startWidth={10} endWidth={10} />
        <RangeDirective start={66} end={100} color='#f44336' startWidth={10} endWidth={10} />
      </RangesDirective>
      <PointersDirective>
        <PointerDirective value={60} type='Needle' color='#1976d2' />
      </PointersDirective>
    </AxisDirective>
  </AxesDirective>
</CircularGaugeComponent>
```

### Dark Mode

Create a dark-themed gauge:

```tsx
<div style={{ backgroundColor: '#212121', padding: '20px', borderRadius: '8px' }}>
  <CircularGaugeComponent
    background='#1e1e1e'
    title='Dark Mode Gauge'
    titleStyle={{ color: '#ffffff' }}
  >
    <AxesDirective>
      <AxisDirective
        lineStyle={{ color: '#4a4a4a' }}
        labelStyle={{ color: '#e0e0e0' }}
      >
        <RangesDirective>
          <RangeDirective start={0} end={100} color='#404040' startWidth={10} endWidth={10} />
        </RangesDirective>
        <PointersDirective>
          <PointerDirective value={60} type='Needle' color='#81c784' />
        </PointersDirective>
      </AxisDirective>
    </AxesDirective>
  </CircularGaugeComponent>
</div>
```

### Gradient and Advanced Styling

Use CSS for gradient backgrounds:

```tsx
<div style={{
  width: '500px',
  height: '500px',
  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  padding: '20px',
  borderRadius: '8px'
}}>
  <CircularGaugeComponent
    background='rgba(255, 255, 255, 0.95)'
  >
    {/* gauge content */}
  </CircularGaugeComponent>
</div>
```

---

## Responsive Design

### Mobile-First Approach

```tsx
import React, { useState, useEffect } from 'react';
import { CircularGaugeComponent} from '@syncfusion/ej2-react-circulargauge';

export function ResponsiveGauge() {
  const [size, setSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight
  });

  useEffect(() => {
    const handleResize = () => {
      setSize({
        width: window.innerWidth,
        height: window.innerHeight
      });
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const gaugeSize = Math.min(size.width, size.height) * 0.8;

  return (
    <div style={{
      width: '100%',
      height: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center'
    }}>
      <div style={{
        width: `${gaugeSize}px`,
        height: `${gaugeSize}px`
      }}>
        <CircularGaugeComponent>
          {/* gauge content */}
        </CircularGaugeComponent>
      </div>
    </div>
  );
}
```

### CSS Media Queries

```tsx
<div className="gauge-container">
  <CircularGaugeComponent>
    {/* gauge content */}
  </CircularGaugeComponent>
</div>
```

```css
.gauge-container {
  width: 100%;
  height: 100%;
  min-height: 500px;
}

/* Tablet */
@media (max-width: 768px) {
  .gauge-container {
    min-height: 400px;
  }
}

/* Mobile */
@media (max-width: 480px) {
  .gauge-container {
    min-height: 300px;
  }
}
```

### Flexbox Layout

```tsx
<div style={{
  display: 'flex',
  flexWrap: 'wrap',
  gap: '20px',
  padding: '20px'
}}>
  <div style={{ flex: 1, minWidth: '300px', height: '400px' }}>
    <CircularGaugeComponent>
      {/* Gauge 1 */}
    </CircularGaugeComponent>
  </div>
  <div style={{ flex: 1, minWidth: '300px', height: '400px' }}>
    <CircularGaugeComponent>
      {/* Gauge 2 */}
    </CircularGaugeComponent>
  </div>
</div>
```

---

## Container Setup

### Basic Container

```tsx
<div style={{ height: '500px' }}>
  <CircularGaugeComponent>
    {/* gauge content */}
  </CircularGaugeComponent>
</div>
```

### Container with Padding and Borders

```tsx
<div style={{
  height: '600px',
  padding: '20px',
  border: '1px solid #e0e0e0',
  borderRadius: '4px',
  backgroundColor: '#fafafa'
}}>
  <CircularGaugeComponent
    centerX="50%"
    centerY="50%"
  >
    {/* gauge content */}
  </CircularGaugeComponent>
</div>
```

### Grid Layout with Multiple Gauges

```tsx
<div style={{
  display: 'grid',
  gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
  gap: '20px',
  padding: '20px'
}}>
  <div style={{ height: '400px' }}>
    <CircularGaugeComponent>
      {/* Gauge 1 */}
    </CircularGaugeComponent>
  </div>
  <div style={{ height: '400px' }}>
    <CircularGaugeComponent>
      {/* Gauge 2 */}
    </CircularGaugeComponent>
  </div>
  <div style={{ height: '400px' }}>
    <CircularGaugeComponent>
      {/* Gauge 3 */}
    </CircularGaugeComponent>
  </div>
</div>
```

### Card-Style Container

```tsx
<div style={{
  width: '100%',
  maxWidth: '500px',
  margin: '20px auto',
  boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
  borderRadius: '8px',
  overflow: 'hidden'
}}>
  <div style={{
    backgroundColor: '#1976d2',
    color: '#fff',
    padding: '16px',
    fontSize: '18px',
    fontWeight: 'bold'
  }}>
    Performance Metrics
  </div>
  <div style={{ height: '500px' }}>
    <CircularGaugeComponent
      centerX="50%"
      centerY="50%"
    >
      {/* gauge content */}
    </CircularGaugeComponent>
  </div>
</div>
```

---

## Tips and Best Practices

- **Always set container height:** Gauges require explicit height to render properly
- **Use percentage positioning:** `centerX` and `centerY` with percentages adapt better to container changes
- **Match width and height:** For perfect circular gauges, use equal width and height
- **Responsive containers:** Use flexbox or CSS Grid for multi-gauge layouts
- **Theme consistency:** Choose one theme and stick with it across your application
- **Color contrast:** Ensure labels and pointers have sufficient contrast with background
