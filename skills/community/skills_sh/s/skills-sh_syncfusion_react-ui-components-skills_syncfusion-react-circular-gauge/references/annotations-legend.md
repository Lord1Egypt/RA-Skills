# Annotations & Legend

See the API quick reference: [api-reference.md](api-reference.md) for annotation and legend model properties (e.g., `AnnotationDirective`, `legendSettings`).

## Table of Contents
- [Text Annotations](#text-annotations)
  - [Basic Text Annotation](#basic-text-annotation)
  - [Text Styling](#text-styling)
  - [Multiple Text Annotations](#multiple-text-annotations)
  - [HTML Content in Annotations](#html-content-in-annotations)
  - [Annotation with Positioning Units](#annotation-with-positioning-units)
  - [Center Annotation](#center-annotation)
  - [Dynamic Annotation Positioning](#dynamic-annotation-positioning)
- [Image Annotations](#image-annotations)
  - [Basic Image Annotation](#basic-image-annotation)
  - [Image with Custom Size](#image-with-custom-size)
  - [Image with Text Overlay](#image-with-text-overlay)
  - [Multiple Image Annotations](#multiple-image-annotations)
- [Annotation Positioning](#annotation-positioning)
  - [Angle-Based Positioning](#angle-based-positioning)
  - [Radius-Based Positioning](#radius-based-positioning)
- [Legend Display](#legend-display)
  - [Basic Legend](#basic-legend)
  - [Legend Positions](#legend-positions)
  - [Legend Styling](#legend-styling)
  - [Legend with Title](#legend-with-title)
- [Legend Customization](#legend-customization)
  - [Range Labels in Legend](#range-labels-in-legend)
  - [Legend Shape and Icon](#legend-shape-and-icon)
  - [Legend Text Formatting](#legend-text-formatting)
- [Legend Interactions](#legend-interactions)
  - [Toggle Legend Visibility](#toggle-legend-visibility)
  - [Legend Item Click Event](#legend-item-click-event)
  - [Custom Legend Item Render](#custom-legend-item-render)
  - [Dynamic Legend Updates](#dynamic-legend-updates)
- [Complete Example: Dashboard with Annotations and Legend](#complete-example-dashboard-with-annotations-and-legend)
- [Tips and Best Practices](#tips-and-best-practices)

## Text Annotations

### Basic Text Annotation

Add text labels to the gauge:

```tsx
import {
  CircularGaugeComponent,
  AxesDirective,
  AxisDirective,
  AnnotationsDirective,
  AnnotationDirective,
} from '@syncfusion/ej2-react-circulargauge';

export function App() {
  return (
    <CircularGaugeComponent >
      <AxesDirective>
        <AxisDirective>
          {/* pointer and range content */}

          <AnnotationsDirective>
            <AnnotationDirective content="90 mph" angle={0} radius="100%" />
          </AnnotationsDirective>
        </AxisDirective>
      </AxesDirective>
    </CircularGaugeComponent>
  );
}
const root = createRoot(document.getElementById('container'));
root.render(<App />);

```

### Text Styling

Customize annotation appearance:

```tsx
<AnnotationDirective
  content="Speed: 120 km/h"
  angle={0}
  radius="100%"
  textStyle={{
    color: '#1976d2',
    size: '18px',
    fontFamily: 'Arial',
    fontWeight: 'bold'
  }}
/>
```

### Multiple Text Annotations

Add multiple labels:

```tsx
<AnnotationsDirective>
  <AnnotationDirective
    content="Min: 0"
    angle={270}
    radius="90%"
    textStyle={{ size: '14px' }}
  />
  <AnnotationDirective
    content="Max: 120"
    angle={90}
    radius="90%"
    textStyle={{ size: '14px' }}
  />
  <AnnotationDirective
    content="Current Speed"
    angle={0}
    radius="120%"
    textStyle={{ size: '16px', fontWeight: 'bold' }}
  />
</AnnotationsDirective>
```

### HTML Content in Annotations

Use HTML for rich formatting:

```tsx
<AnnotationDirective
  content="<div style='background: #1976d2; color: white; padding: 8px; border-radius: 4px;'>75°C</div>"
  angle={180}
  radius="0%"
/>
```

### Annotation with Positioning Units

```tsx
// Percentage of gauge radius
<AnnotationDirective
  content="50%"
  radius="50%"
  angle={90}
/>

// Pixels
<AnnotationDirective
  content="100px"
  radius="100px"
  angle={45}
/>
```

---

## Image Annotations

### Basic Image Annotation

Add an image to the gauge:

```tsx
<AnnotationsDirective>
  <AnnotationDirective
    imageUrl="./assets/speedometer-icon.png"
    angle={0}
    radius="100%"
    description="Speed Icon"
  />
</AnnotationsDirective>
```

### Image with Custom Size

```tsx
<AnnotationDirective
  imageUrl="./assets/temperature-icon.svg"
  angle={90}
  radius="80%"
  imageWidth={40}
  imageHeight={40}
/>
```

### Image with Text Overlay

Combine image and text:

```tsx
<AnnotationsDirective>
  <AnnotationDirective
    imageUrl="./assets/status-ok.png"
    angle={180}
    radius="110%"
    imageWidth={32}
    imageHeight={32}
  />
  <AnnotationDirective
    content="OK"
    angle={180}
    radius="130%"
    textStyle={{ size: '16px', fontWeight: 'bold' }}
  />
</AnnotationsDirective>
```

### Multiple Image Annotations

```tsx
<AnnotationsDirective>
  <AnnotationDirective
    imageUrl="./assets/arrow-up.svg"
    angle={0}
    radius="50%"
    imageWidth={20}
    imageHeight={20}
  />
  <AnnotationDirective
    imageUrl="./assets/arrow-down.svg"
    angle={180}
    radius="50%"
    imageWidth={20}
    imageHeight={20}
  />
</AnnotationsDirective>
```

---

## Annotation Positioning

### Angle-Based Positioning

Position annotations around the circle using angles:

```tsx
// 0° = right (3 o'clock)
// 90° = bottom (6 o'clock)
// 180° = left (9 o'clock)
// 270° = top (12 o'clock)

<AnnotationsDirective>
  <AnnotationDirective content="Right" angle={0} radius="100%" />
  <AnnotationDirective content="Bottom" angle={90} radius="100%" />
  <AnnotationDirective content="Left" angle={180} radius="100%" />
  <AnnotationDirective content="Top" angle={270} radius="100%" />
  <AnnotationDirective content="Diagonal" angle={45} radius="100%" />
</AnnotationsDirective>
```

### Radius-Based Positioning

Position closer to or farther from center:

```tsx
<AnnotationsDirective>
  {/* Close to center */}
  <AnnotationDirective content="Inner" radius="20%" angle={0} />
  
  {/* Middle */}
  <AnnotationDirective content="Middle" radius="60%" angle={90} />
  
  {/* Outer (beyond gauge) */}
  <AnnotationDirective content="Outer" radius="120%" angle={180} />
</AnnotationsDirective>
```

### Center Annotation

Add text in the center of the gauge:

```tsx
<AnnotationDirective
  content="75%"
  radius="0%"
  angle={0}
  textStyle={{
    size: '24px',
    fontWeight: 'bold',
    color: '#1976d2'
  }}
/>
```

### Dynamic Annotation Positioning

Position annotation based on pointer value:

```tsx
import React, { useState } from 'react';

export function DynamicAnnotation() {
  const [value, setValue] = useState(50);
  
  // Calculate angle based on pointer value
  // Assuming 0-100 scale across 180° (semicircle)
  const angle = 270 + (value * 1.8); // 270° to 90°

  return (
    <CircularGaugeComponent>
      <AxesDirective>
        <AxisDirective minimum={0} maximum={100}>
          <AnnotationsDirective>
            <AnnotationDirective
              content={`${value}%`}
              angle={angle}
              radius="100%"
              textStyle={{ size: '16px' }}
            />
          </AnnotationsDirective>
        </AxisDirective>
      </AxesDirective>
    </CircularGaugeComponent>
  );
}
```

---

## Legend Display

### Basic Legend

Display a legend showing range meanings:

```tsx
import { CircularGaugeComponent, AxesDirective, AxisDirective, 
         RangesDirective, RangeDirective, Inject, Legend } 
  from '@syncfusion/ej2-react-circulargauge';

<CircularGaugeComponent
  legendSettings={{
    visible: true,
    position: 'Auto'  // Auto, Top, Bottom, Left, Right, Custom
  }}
>
  <Inject services={[ Legend ]}/>
  <AxesDirective>
    <AxisDirective minimum={0} maximum={100}>
      <RangesDirective>
        <RangeDirective 
          start={0} 
          end={30} 
          color='#4caf50'
          legendText='Low'
          radius='108%'
        />
        <RangeDirective 
          start={30} 
          end={60} 
          color='#fbc02d'
          legendText='Medium'
          radius='108%'
        />
        <RangeDirective 
          start={60} 
          end={100} 
          color='#f44336'
          legendText='High'
          radius='108%'
        />
      </RangesDirective>
    </AxisDirective>
  </AxesDirective>
</CircularGaugeComponent>
```

### Legend Positions

```tsx
// Auto (default)
legendSettings={{ visible: true, position: 'Auto' }}

// Top
legendSettings={{ visible: true, position: 'Top' }}

// Bottom
legendSettings={{ visible: true, position: 'Bottom' }}

// Left
legendSettings={{ visible: true, position: 'Left' }}

// Right
legendSettings={{ visible: true, position: 'Right' }}

// Custom - position using location
legendSettings={{ 
  visible: true, 
  position: 'Custom',
  location: { x: 100, y: 150 }
}}
```

### Legend Styling

Customize legend appearance:

```tsx
<CircularGaugeComponent
  legendSettings={{
    visible: true,
    position: 'Bottom',  // Top, Bottom, Left, Right, Custom, Auto
    alignment: 'Center',  // Center, Far, Near
    height: '50px',
    width: '100%',
    background: '#f5f5f5',
    opacity: 1,
    padding: 8,
    border: {
      color: '#e0e0e0',
      width: 1
    },
    textStyle: {
      color: '#424242',
      size: '14px',
      fontFamily: 'Segoe UI',
      fontStyle: 'Normal',
      fontWeight: 'Normal'
    },
    toggleVisibility: true,
    shape: 'Circle',  // Circle, Rectangle, Diamond, Triangle, InvertedTriangle, Image
    shapeWidth: 10,
    shapeHeight: 10,
    shapePadding: 5,
    shapeBorder: {
      color: '#e0e0e0',
      width: 1
    },
    margin: {
      top: 10,
      bottom: 10,
      left: 10,
      right: 10
    }
  }}
>
  {/* gauge content */}
</CircularGaugeComponent>
```


## Legend Customization

### Range Labels in Legend

Control what appears in the legend using `legendText` property:

```tsx
<RangesDirective>
  <RangeDirective 
    start={0} 
    end={30} 
    color='#4caf50'
    legendText='Safe (0-30%)'
    radius='108%'
  />
  <RangeDirective 
    start={30} 
    end={60} 
    color='#fbc02d'
    legendText='Caution (30-60%)'
    radius='108%'
  />
  <RangeDirective 
    start={60} 
    end={100} 
    color='#f44336'
    legendText='Danger (60-100%)'
    radius='108%'
  />
</RangesDirective>
```

### Legend Shape and Icon

```tsx
<CircularGaugeComponent
  legendSettings={{
    visible: true,
    shape: 'Circle',  // Circle, Rectangle, Triangle, InvertedTriangle, Diamond, Image
    shapeWidth: 30,
    shapeHeight: 30,
    shapePadding: 5,
    shapeBorder: {
      color: '#e0e0e0',
      width: 1
    }
  }}
>
  {/* gauge content */}
</CircularGaugeComponent>
```

### Legend Text Formatting

```tsx
<CircularGaugeComponent
  legendSettings={{
    visible: true,
    toggleVisibility: true,
    textStyle: {
      color: '#424242',
      size: '14px',
      fontFamily: 'Segoe UI',
      fontStyle: 'Normal',
      fontWeight: 'Normal',
      opacity: 0.8
    }
  }}
>
  {/* gauge content */}
</CircularGaugeComponent>
```

---

## Legend Interactions

### Toggle Legend Visibility

Allow users to toggle visibility of ranges:

```tsx
<CircularGaugeComponent
  legendSettings={{
    visible: true,
    toggleVisibility: true  // Click legend item to toggle range
  }}
>
  {/* gauge content */}
</CircularGaugeComponent>
```

### Legend Item Click Event

Handle legend item clicks:

```tsx
import React, { useState } from 'react';

export function InteractiveLegend() {
  const [ranges, setRanges] = useState([
    { start: 0, end: 30, visible: true },
    { start: 30, end: 60, visible: true },
    { start: 60, end: 100, visible: true }
  ]);

  const handleLegendItemClick = (e: any) => {
    console.log('Legend item clicked:', e.data);
    // Handle toggle logic
  };

  return (
    <CircularGaugeComponent
      legendSettings={{
        visible: true,
        toggleVisibility: true
      }}
      legendRender={handleLegendItemClick}
    >
      {/* gauge content */}
    </CircularGaugeComponent>
  );
}
```

### Custom Legend Item Render

Use the `legendRendering` event to customize legend items before rendering:

```tsx
<CircularGaugeComponent
  legendRendering={(args: any) => {
    // Customize legend item before render
    if (args.text.includes('High')) {
      args.shape = 'Diamond';
    }
    // You can also customize: fill, text, shape, name, cancel
  }}
  legendSettings={{ visible: true }}
>
  {/* gauge content */}
</CircularGaugeComponent>
```

### Dynamic Legend Updates

Update legend when ranges change:

```tsx
import React, { useEffect, useRef } from 'react';

export function DynamicLegend() {
  const gaugeRef = useRef<CircularGaugeComponent>(null);

  useEffect(() => {
    // Update ranges dynamically
    const updatedRanges = [
      { start: 0, end: 25, color: '#4caf50', label: 'Optimal' },
      { start: 25, end: 50, color: '#fbc02d', label: 'Normal' },
      { start: 50, end: 100, color: '#f44336', label: 'Alert' }
    ];
    
    // Refresh gauge with new ranges
    if (gaugeRef.current) {
      gaugeRef.current.refresh();
    }
  }, []);

  return (
    <CircularGaugeComponent
      ref={gaugeRef}
      legendSettings={{ visible: true }}
    >
      {/* gauge content */}
    </CircularGaugeComponent>
  );
}
```

---

## Complete Example: Dashboard with Annotations and Legend

```tsx
import React from 'react';
import { CircularGaugeComponent, AxesDirective, AxisDirective,
         PointersDirective, PointerDirective, RangesDirective, RangeDirective,
         AnnotationsDirective, AnnotationDirective, Inject, Legend } 
  from '@syncfusion/ej2-react-circulargauge';

export function CompleteDashboard() {
  return (
    <CircularGaugeComponent
      legendSettings={{
        visible: true,
        position: 'Bottom',
        alignment: 'Center',
        shape: 'Circle',
        shapeWidth: 30,
        shapeHeight: 30,
        padding: 15,
        border: {
          color: 'green',
          width: 3
        }
      }}
    >
      <Inject services={[ Legend ]}/>
      <AxesDirective>
        <AxisDirective minimum={0} maximum={100}>
          <RangesDirective>
            <RangeDirective 
              start={0} 
              end={30} 
              color='#4caf50'
              legendText='Good'
              radius='108%'
              startWidth={10}
              endWidth={10}
            />
            <RangeDirective 
              start={30} 
              end={60} 
              color='#fbc02d'
              legendText='Normal'
              radius='108%'
              startWidth={10}
              endWidth={10}
            />
            <RangeDirective 
              start={60} 
              end={100} 
              color='#f44336'
              legendText='Poor'
              radius='108%'
              startWidth={10}
              endWidth={10}
            />
          </RangesDirective>

          <PointersDirective>
            <PointerDirective value={75} type='Needle' />
          </PointersDirective>

          <AnnotationsDirective>
            <AnnotationDirective
              content="75%"
              radius="0%"
              angle={0}
              textStyle={{ size: '20px', fontWeight: 'bold' }}
            />
            <AnnotationDirective
              content="Current Status"
              radius="120%"
              angle={90}
              textStyle={{ size: '14px' }}
            />
          </AnnotationsDirective>
        </AxisDirective>
      </AxesDirective>
    </CircularGaugeComponent>
  );
}
```

---

## Tips and Best Practices

- **Use meaningful labels:** Legend labels should clearly describe what ranges represent
- **Position annotations carefully:** Avoid overlapping with pointers or other elements
- **Limit annotations:** Too many annotations clutter the gauge
- **Color consistency:** Use legend colors that match range colors exactly
- **Test positioning:** Verify annotations display correctly at different gauge sizes
- **HTML content:** Keep HTML annotations simple and lightweight
