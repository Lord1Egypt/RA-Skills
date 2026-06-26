# Ranges & Annotations in React Linear Gauge

## Table of Contents

- [Creating Ranges](#creating-ranges)
  - [Basic Range Example](#basic-range-example)
  - [Range Properties](#range-properties)
- [Range Styling](#range-styling)
  - [Solid Colors](#solid-colors)
  - [Semantic Colors (Traffic Light)](#semantic-colors-traffic-light)
  - [Gradient Colors](#gradient-colors)
  - [Tapered Ranges (Varying Width)](#tapered-ranges-varying-width)
  - [Temperature Gauge Styling](#temperature-gauge-styling)
- [Range Labels](#range-labels)
- [Text Annotations](#text-annotations)
  - [Basic Text Annotation](#basic-text-annotation)
  - [Position Annotations](#position-annotations)
  - [HTML Content in Annotations](#html-content-in-annotations)
- [Image Annotations](#image-annotations)
- [Annotation Positioning](#annotation-positioning)
  - [Positioning System](#positioning-system)
  - [Common Positions](#common-positions)
- [Common Patterns](#common-patterns)
  - [Pattern 1: Temperature Gauge with Zones and Labels](#pattern-1-temperature-gauge-with-zones-and-labels)
  - [Pattern 2: Dashboard Gauge with Status Indicator](#pattern-2-dashboard-gauge-with-status-indicator)
  - [Pattern 3: Multiple Annotations](#pattern-3-multiple-annotations)
  - [Pattern 4: Ranges for CPU Usage](#pattern-4-ranges-for-cpu-usage)
- [Interactive Annotations with State](#interactive-annotations-with-state)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)

## Creating Ranges

Ranges are colored segments on the gauge that represent different value zones. They help visualize which range a value falls into.

### Basic Range Example

```tsx
import React from 'react';
import { LinearGaugeComponent, AxesDirective, AxisDirective,
         RangesDirective, RangeDirective, PointersDirective, PointerDirective } 
  from '@syncfusion/ej2-react-lineargauge';

export function App() {
  return (
    <LinearGaugeComponent>
      <AxesDirective>
        <AxisDirective minimum={0} maximum={100}>
          <RangesDirective>
            <RangeDirective start={0} end={33} color='#1E90FF' />
            <RangeDirective start={33} end={66} color='#FFA500' />
            <RangeDirective start={66} end={100} color='#FF6B6B' />
          </RangesDirective>
          
          <PointersDirective>
            <PointerDirective value={45} />
          </PointersDirective>
        </AxisDirective>
      </AxesDirective>
    </LinearGaugeComponent>
  );
}

export default App;
```

**Result:** Three colored zones - blue (low), orange (medium), red (high).

### Range Properties

```tsx
<RangeDirective 
  start={30}           // Start value of the range
  end={70}             // End value of the range
  color="#FF6B6B"      // Range color
  startWidth={15}      // Width at start (optional)
  endWidth={15}        // Width at end (optional)
/>
```

**Key Props:**
- `start` - Range start value (required)
- `end` - Range end value (required)
- `color` - Range color (hex, rgb, or name)
- `startWidth` - Width at start of range (pixels)
- `endWidth` - Width at end of range (pixels)

## Range Styling

### Solid Colors

```tsx
<RangeDirective start={0} end={30} color='#1E90FF' />      // Blue
<RangeDirective start={30} end={70} color='#FFA500' />     // Orange
<RangeDirective start={70} end={100} color='#FF6B6B' />    // Red
```

### Semantic Colors (Traffic Light)

```tsx
<RangesDirective>
  <RangeDirective start={0} end={33} color='#4CAF50' />    {/* Green - Good */}
  <RangeDirective start={33} end={66} color='#FFC107' />   {/* Yellow - Warning */}
  <RangeDirective start={66} end={100} color='#F44336' />  {/* Red - Critical */}
</RangesDirective>
```

### Gradient Colors

Use CSS gradients for smooth color transitions:

```tsx
<RangeDirective 
  start={0} 
  end={50}
  color="url(#rangeGradient)"
/>
```

### Tapered Ranges (Varying Width)

```tsx
<RangeDirective 
  start={20}
  end={80}
  startWidth={25}      // Thicker at start
  endWidth={5}         // Thinner at end (tapered effect)
  color='#FF6B6B'
/>
```

### Temperature Gauge Styling

```tsx
<RangesDirective>
  {/* Freezing */}
  <RangeDirective start={-50} end={0} color='#0066CC' startWidth={15} endWidth={15} />
  
  {/* Cold */}
  <RangeDirective start={0} end={10} color='#1E90FF' startWidth={15} endWidth={15} />
  
  {/* Cool */}
  <RangeDirective start={10} end={20} color='#00CED1' startWidth={15} endWidth={15} />
  
  {/* Comfortable */}
  <RangeDirective start={20} end={28} color='#228B22' startWidth={15} endWidth={15} />
  
  {/* Warm */}
  <RangeDirective start={28} end={35} color='#FFA500' startWidth={15} endWidth={15} />
  
  {/* Hot */}
  <RangeDirective start={35} end={50} color='#FF4500' startWidth={15} endWidth={15} />
</RangesDirective>
```

## Range Labels

Syncfusion Linear Gauge ranges are primarily styled using start/end and color (and optional border/gradient). If you need text labels for ranges, use AnnotationDirective to place text at a specific axis position.

```tsx
<AnnotationsDirective>
  {/* Label placed near the middle of the range (axisValue) */}
  <AnnotationDirective
    content="<div style='color:#1E90FF; font-weight:bold;'>Low</div>"
    axisIndex={0}
    axisValue={16.5}
    zIndex="1"
  />
</AnnotationsDirective>
```

## Text Annotations

Annotations are text elements placed at specific positions. They're useful for labels and callouts.

### Basic Text Annotation

```tsx
import React from 'react';
import { LinearGaugeComponent, AxesDirective, AxisDirective,
         AnnotationsDirective, AnnotationDirective } 
  from '@syncfusion/ej2-react-lineargauge';

export function App() {
  return (
    <LinearGaugeComponent>
      <AxesDirective>
        <AxisDirective minimum={0} maximum={100}>
        </AxisDirective>
      </AxesDirective>
      
      <AnnotationsDirective>
        <AnnotationDirective 
          content="<div>Current: 65%</div>"
          x={50}
          y={100}
        />
      </AnnotationsDirective>
    </LinearGaugeComponent>
  );
}

export default App;
```

### Position Annotations

```tsx
<AnnotationDirective 
  content="<div style='color: #1976D2; font-weight: bold;'>Temperature: 25°C</div>"
  x={45}          // X position (% or px)
  y={50}          // Y position (% or px)
  zIndex={'1'}      // Stacking order
/>
```

### HTML Content in Annotations

```tsx
<AnnotationDirective 
  content={`
    <div style='
      padding: 8px 12px;
      background: white;
      border: 1px solid #ccc;
      border-radius: 4px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    '>
      <strong>Value: 65%</strong><br/>
      <small>Target: 75%</small>
    </div>
  `}
  x={50}
  y={80}
/>
```

## Image Annotations

Use images for visual markers or icons:

```tsx
<AnnotationDirective 
  content="<img src='/images/thermometer.svg' width='30' height='30' />"
  x={50}
  y={20}
/>
```

## Annotation Positioning

### Positioning System

- `x` - Horizontal position (0-100% or pixels)
- `y` - Vertical position (0-100% or pixels)
- `zIndex` - Stacking order (higher = on top)

### Common Positions

```tsx
{/* Top center */}
<AnnotationDirective content="..." x={50} y={10} />

{/* Center */}
<AnnotationDirective content="..." x={50} y={50} />

{/* Bottom center */}
<AnnotationDirective content="..." x={50} y={90} />

{/* Left side */}
<AnnotationDirective content="..." x={10} y={50} />

{/* Right side */}
<AnnotationDirective content="..." x={90} y={50} />
```

## Common Patterns

### Pattern 1: Temperature Gauge with Zones and Labels

```tsx
import React, { useState } from 'react';
import { LinearGaugeComponent, AxesDirective, AxisDirective,
         RangesDirective, RangeDirective, PointersDirective, PointerDirective,
         AnnotationsDirective, AnnotationDirective } 
  from '@syncfusion/ej2-react-lineargauge';

export function App() {
  const [temp, setTemp] = useState(22);

  return (
    <LinearGaugeComponent title="Room Temperature">
      <AxesDirective>
        <AxisDirective 
          minimum={0}
          maximum={40}
          labelStyle={{ format: '{value}°C' }}
        >
          <RangesDirective>
            <RangeDirective start={0} end={15} color='#4CAF50' />
            <RangeDirective start={15} end={25} color='#8BC34A' />
            <RangeDirective start={25} end={40} color='#FF5722' />
          </RangesDirective>
          
          <PointersDirective>
            <PointerDirective value={temp} type="Bar" />
          </PointersDirective>
        </AxisDirective>
      </AxesDirective>
      
      <AnnotationsDirective>
        <AnnotationDirective 
          content={`<div style='font-size: 16px; font-weight: bold;'>${temp}°C</div>`}
          x={50}
          y={75}
        />
      </AnnotationsDirective>
    </LinearGaugeComponent>
  );
}

export default App;
```

### Pattern 2: Dashboard Gauge with Status Indicator

```tsx
<LinearGaugeComponent title="System Performance">
  <AxesDirective>
    <AxisDirective minimum={0} maximum={100} labelStyle={{ format: '{value}%' }}>
      <RangesDirective>
        <RangeDirective start={0} end={30} color='#FF6B6B' />
        <RangeDirective start={30} end={70} color='#FFA500' />
        <RangeDirective start={70} end={100} color='#4CAF50' />
      </RangesDirective>
      
      <PointersDirective>
        <PointerDirective value={85} type="Bar" />
      </PointersDirective>
    </AxisDirective>
  </AxesDirective>
  
  <AnnotationsDirective>
    <AnnotationDirective 
      content="<div style='color: #4CAF50; font-weight: bold;'>✓ OPTIMAL</div>"
      x={50}
      y={80}
    />
  </AnnotationsDirective>
</LinearGaugeComponent>
```

### Pattern 3: Multiple Annotations

```tsx
<AnnotationsDirective>
  {/* Current value label */}
  <AnnotationDirective 
    content="<div style='font-size: 18px; font-weight: bold;'>65%</div>"
    x={50}
    y={40}
  />
  
  {/* Zone indicator */}
  <AnnotationDirective 
    content="<div style='font-size: 12px; color: #666;'>NORMAL ZONE</div>"
    x={50}
    y={60}
  />
  
  {/* Timestamp */}
  <AnnotationDirective 
    content="<div style='font-size: 10px; color: #999;'>Updated: 14:32:15</div>"
    x={50}
    y={90}
  />
</AnnotationsDirective>
```

### Pattern 4: Ranges for CPU Usage

```tsx
<RangesDirective>
  {/* Normal */}
  <RangeDirective start={0} end={50} color='#4CAF50' startWidth={20} endWidth={20} />
  
  {/* Warning */}
  <RangeDirective start={50} end={80} color='#FFC107' startWidth={20} endWidth={20} />
  
  {/* Critical */}
  <RangeDirective start={80} end={100} color='#FF5722' startWidth={20} endWidth={20} />
</RangesDirective>
```

## Interactive Annotations with State

Update annotations based on pointer value:

```tsx
import React, { useState } from 'react';
import { LinearGaugeComponent, AxesDirective, AxisDirective,
         PointersDirective, PointerDirective, AnnotationsDirective, AnnotationDirective } 
  from '@syncfusion/ej2-react-lineargauge';

export function App() {
  const [value, setValue] = useState(50);
  
  const getStatus = (val) => {
    if (val < 33) return { status: 'LOW', color: '#4CAF50' };
    if (val < 66) return { status: 'MEDIUM', color: '#FFA500' };
    return { status: 'HIGH', color: '#FF6B6B' };
  };

  const status = getStatus(value);

  return (
    <LinearGaugeComponent valueChange={(e) => setValue(e.value)}>
      <AxesDirective>
        <AxisDirective minimum={0} maximum={100}>
          <PointersDirective>
            <PointerDirective value={value} enableDrag={true} />
          </PointersDirective>
        </AxisDirective>
      </AxesDirective>
      
      <AnnotationsDirective>
        <AnnotationDirective 
          content={`<div style='color: ${status.color}; font-weight: bold;'>${status.status}</div>`}
          x={50}
          y={75}
        />
      </AnnotationsDirective>
    </LinearGaugeComponent>
  );
}
```

## API Reference

### Key Properties (selected)
- `allowImageExport` (boolean) — enable image export
- `allowPdfExport` (boolean)
- `allowPrint` (boolean)
- `animationDuration` (number)
- `annotations` (AnnotationModel[])
- `axes` (AxisModel[])
- `background` (string)
- `border` (BorderModel)
- `container` (ContainerModel)
- `description` (string)
- `edgeLabelPlacement` (string)
- `enablePersistence` (boolean)
- `enableRtl` (boolean)
- `format` (string)
- `height` (string)
- `margin` (MarginModel)
- `orientation` (string)
- `rangePalettes` (string[][])
- `theme` (string)
- `title` (string)
- `tooltip` (TooltipSettingsModel)
- `useGroupingSeparator` (boolean)
- `width` (string)

### Methods
- `destroy(): void`
- `export(type, fileName, orientation, allowDownload): Promise`
- `print(id?: string | string[] | Element): void`
- `setAnnotationValue(annotationIndex, content, axisValue): void`
- `setPointerValue(axisIndex, pointerIndex, value): void`

### Events
- `animationComplete` — fired after animation completes
- `annotationRender` — fired before an annotation is rendered
- `axisLabelRender` — fired while rendering axis labels
- `beforePrint` — fired before print
- `dragEnd`, `dragMove`, `dragStart` — pointer drag lifecycle
- `gaugeMouseDown`, `gaugeMouseLeave`, `gaugeMouseMove`, `gaugeMouseUp` — mouse interactions
- `load`, `loaded` — component load lifecycle
- `resized` — when gauge is resized
- `tooltipRender` — before tooltip is shown
- `valueChange` — when pointer value changes

### Example (short)
```tsx
<LinearGaugeComponent
  allowImageExport
  allowPdfExport
  allowPrint
  animationDuration={1500}
  axes={[{ minimum:0, maximum:100 }]}
  annotations={[{ axisIndex:0, axisValue:50, content:'<div>50</div>' }]}
  annotationRender={handleAnnotationRender}
  axisLabelRender={handleAxisLabelRender}
/>
```

Note: Use `PointersDirective`, `RangesDirective`, and `AnnotationsDirective` child directives to configure pointers, ranges and annotations respectively. For full API details see Syncfusion docs: https://ej2.syncfusion.com/react/documentation/api/linear-gauge/index-default

## Troubleshooting

**Q: Ranges not appearing**
- Verify `start` and `end` are within axis `minimum` and `maximum`
- Check `color` is valid (hex, rgb, or CSS color name)

**Q: Annotation text overlapping**
- Adjust `x` and `y` positions
- Use `zIndex` to reorder overlapping annotations

**Q: Annotations shifting on resize**
- Use percentage-based positioning (0-100) instead of pixels
- Test responsive behavior

## Next Steps

- Read **Customization** for styling options
- Read **Advanced Features** for event handling and animations
- Read **Accessibility** for accessible range/annotation design
