# Pointer Types & Configuration in React Linear Gauge

See API Reference: [API Reference](api-reference.md)

## Table of Contents

- [Bar Pointer Type](#bar-pointer-type)
  - [Basic Bar Pointer](#basic-bar-pointer)
  - [Customized Bar Pointer](#customized-bar-pointer)
  - [Bar Gradient Fill](#bar-gradient-fill)
- [Marker Pointer Type](#marker-pointer-type)
  - [Basic Marker Pointer](#basic-marker-pointer)
  - [Available Marker Shapes](#available-marker-shapes)
  - [Customized Marker Pointer](#customized-marker-pointer)
  - [Image Marker](#image-marker)
  - [Text Marker](#text-marker)
- [Setting Pointer Values](#setting-pointer-values)
  - [Static Value](#static-value)
  - [Dynamic Value with State](#dynamic-value-with-state)
  - [Real-Time Updates](#real-time-updates)
- [Pointer Customization](#pointer-customization)
  - [Styling Properties](#styling-properties)
  - [Animation](#animation)
- [Multiple Pointers](#multiple-pointers)
- [Drag and Drop](#drag-and-drop)
  - [Handling Drag Events](#handling-drag-events)
- [Performance Tips](#performance-tips)
  - [1. Use Bar Pointers for Simple Cases](#1-use-bar-pointers-for-simple-cases)
  - [2. Limit Animation Duration](#2-limit-animation-duration)
  - [3. Use useCallback for Event Handlers](#3-use-usecallback-for-event-handlers)
  - [4. Debounce Frequent Updates](#4-debounce-frequent-updates)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)

## Bar Pointer Type

Bar pointers fill the gauge from the minimum to the pointer value. This is the default pointer type.

### Basic Bar Pointer

```tsx
import React from 'react';
import { LinearGaugeComponent, AxesDirective, AxisDirective, 
         PointersDirective, PointerDirective } 
  from '@syncfusion/ej2-react-lineargauge';

export function App() {
  return (
    <LinearGaugeComponent>
      <AxesDirective>
        <AxisDirective minimum={0} maximum={100}>
          <PointersDirective>
            <PointerDirective 
              value={65}
              type="Bar"
            />
          </PointersDirective>
        </AxisDirective>
      </AxesDirective>
    </LinearGaugeComponent>
  );
}

export default App;
```

**Result:** A bar that fills from 0 to 65 on the scale.

### Customized Bar Pointer

```tsx
<PointerDirective 
  value={65}
  type="Bar"
  width={15}              // Thickness of the bar
  color="#FF6B6B"         // Bar color
  offset={5}              // Distance from axis line
  roundedCornerRadius={0}
/>
```

**Bar Properties:**
- `type` - Must be "Bar"
- `value` - Current value (0-100 by default)
- `width` - Bar thickness in pixels (default: 7)
- `color` - Bar color (hex, rgb, or name)
- `offset` - Distance from axis line
- `roundedCornerRadius` - Rounded corner radius

### Bar Gradient Fill

```tsx
<PointerDirective 
  value={75}
  type="Bar"
  color="url(#barGradient)"
  width={20}
/>
```

## Marker Pointer Type

Marker pointers use a shape instead of a bar. They're useful for precise value indication.

### Basic Marker Pointer

```tsx
<PointerDirective 
  value={80}
  type="Marker"
  markerType="Circle"
/>
```

**Result:** A circular marker at value 80.

### Available Marker Shapes

The `markerType` property supports these shapes:

```tsx
// Circle marker
<PointerDirective value={50} type="Marker" markerType="Circle" />

// Rectangle marker
<PointerDirective value={50} type="Marker" markerType="Rectangle" />

// Triangle marker
<PointerDirective value={50} type="Marker" markerType="Triangle" />

// Inverted Triangle marker (default)
<PointerDirective value={50} type="Marker" markerType="InvertedTriangle" />

// Diamond marker
<PointerDirective value={50} type="Marker" markerType="Diamond" />
```

### Customized Marker Pointer

```tsx
<PointerDirective 
  value={60}
  type="Marker"
  markerType="Rectangle"
  width={20}              // Marker width
  color="#00BCD4"         // Marker color
  border={{
    width: 2,
    color: "#1976D2"      // Border color
  }}
  offset={0}              // Distance from axis line
/>
```

### Image Marker

Use a custom image as a marker:

```tsx
<PointerDirective 
  value={50}
  type="Marker"
  markerType="Image"
  imageUrl="/path/to/marker.png"
  width={30}
  height={30}
/>
```

**Note:** `imageUrl` must be a valid image path (PNG, JPG, SVG).

### Text Marker

Display text as a marker:

```tsx
<PointerDirective 
  value={75}
  type="Marker"
  markerType="Text"
  text="75%"
/>
```

## Setting Pointer Values

### Static Value

```tsx
<PointerDirective value={50} />
```

### Dynamic Value with State

```tsx
import React, { useState } from 'react';

export function App() {
  const [value, setValue] = useState(50);

  return (
    <div>
      <button onClick={() => setValue(value + 10)}>Increase</button>
      <button onClick={() => setValue(value - 10)}>Decrease</button>
      
      <LinearGaugeComponent>
        <AxesDirective>
          <AxisDirective minimum={0} maximum={100}>
            <PointersDirective>
              <PointerDirective value={value} />
            </PointersDirective>
          </AxisDirective>
        </AxesDirective>
      </LinearGaugeComponent>
    </div>
  );
}
```

### Real-Time Updates

```tsx
import React, { useState, useEffect } from 'react';

export function App() {
  const [value, setValue] = useState(50);

  useEffect(() => {
    // Update every second with random variation
    const interval = setInterval(() => {
      setValue(prev => {
        const newValue = prev + (Math.random() - 0.5) * 20;
        return Math.max(0, Math.min(100, newValue)); // Clamp between 0-100
      });
    }, 1000);
    
    return () => clearInterval(interval);
  }, []);

  return (
    <LinearGaugeComponent>
      {/* Configuration with value={value} */}
    </LinearGaugeComponent>
  );
}
```

## Pointer Customization

### Styling Properties

```tsx
<PointerDirective 
  value={70}
  type="Bar"
  width={15}
  color="#FF6B6B"
  opacity={0.8}          // Transparency (0-1)
  offset={3}             // Distance from axis
  border={{
    width: 2,
    color: "#C1192B"
  }}
  roundedCornerRadius={2}       // For bar pointers only
/>
```

### Animation

```tsx
<PointerDirective 
  value={75}
  animationDuration={1000}  // 1 second animation
/>
```

## Multiple Pointers

Add multiple pointers to compare or track multiple values:

```tsx
import React from 'react';
import { LinearGaugeComponent, AxesDirective, AxisDirective, 
         PointersDirective, PointerDirective } 
  from '@syncfusion/ej2-react-lineargauge';

export function App() {
  return (
    <LinearGaugeComponent title="Multi-Pointer Gauge">
      <AxesDirective>
        <AxisDirective minimum={0} maximum={100}>
          <PointersDirective>
            {/* Actual value */}
            <PointerDirective 
              value={65}
              type="Bar"
              color="#1976D2"
              width={12}
            />
            
            {/* Target value */}
            <PointerDirective 
              value={80}
              type="Marker"
              markerType="Circle"
              color="#FF6B6B"
              width={20}
            />
            
            {/* Previous value */}
            <PointerDirective 
              value={55}
              type="Marker"
              markerType="Diamond"
              color="#FFA500"
              width={15}
            />
          </PointersDirective>
        </AxisDirective>
      </AxesDirective>
    </LinearGaugeComponent>
  );
}

export default App;
```

**Use Cases:**
- **Actual vs Target:** Compare current value against goal
- **Current vs Previous:** Track changes over time
- **Multiple Sensors:** Display readings from different sources

## Drag and Drop

Enable users to drag pointers to update values interactively:

```tsx
<PointerDirective 
  value={50}
  type="Bar"
  enableDrag={true}
/>
```

### Handling Drag Events

```tsx
import React, { useState } from 'react';

export function App() {
  const [value, setValue] = useState(50);

  const onPointerValueChange = (e) => {
    // e.value contains the new pointer value
    console.log('Pointer moved to:', e.value);
    setValue(e.value);
  };

  return (
    <LinearGaugeComponent
      valueChange={onPointerValueChange}
    >
      <AxesDirective>
        <AxisDirective minimum={0} maximum={100}>
          <PointersDirective>
            <PointerDirective 
              value={value}
              type="Bar"
              enableDrag={true}
            />
          </PointersDirective>
        </AxisDirective>
      </AxesDirective>
    </LinearGaugeComponent>
  );
}
```

## Performance Tips

### 1. Use Bar Pointers for Simple Cases

Bar pointers render faster than marker pointers with animations.

```tsx
// Fast
<PointerDirective value={50} type="Bar" />

// Slower with many animations
<PointerDirective value={50} type="Marker" markerType="Circle" 
  animationDuration={2000} />
```

### 2. Limit Animation Duration

Keep animations under 1-2 seconds for responsive feel:

```tsx
// Good
<PointerDirective value={50} animationDuration={800} />

// Slow
<PointerDirective value={50} animationDuration={5000} />
```

### 3. Use useCallback for Event Handlers

Prevent unnecessary re-renders:

```tsx
import React, { useCallback } from 'react';

export function App() {
  const handlePointerChange = useCallback((e) => {
    // Update pointer value
  }, []);

  return (
    <LinearGaugeComponent valueChange={handlePointerChange}>
      {/* */}
    </LinearGaugeComponent>
  );
}
```

### 4. Debounce Frequent Updates

For real-time data, debounce updates to avoid excessive re-renders:

```tsx
import React, { useState, useEffect } from 'react';

export function App() {
  const [value, setValue] = useState(50);
  const [displayValue, setDisplayValue] = useState(50);

  useEffect(() => {
    // Update display every 500ms instead of on every change
    const timer = setTimeout(() => {
      setDisplayValue(value);
    }, 500);
    return () => clearTimeout(timer);
  }, [value]);

  return (
    <LinearGaugeComponent>
      <AxesDirective>
        <AxisDirective minimum={0} maximum={100}>
          <PointersDirective>
            <PointerDirective value={displayValue} />
          </PointersDirective>
        </AxisDirective>
      </AxesDirective>
    </LinearGaugeComponent>
  );
}
```

## Troubleshooting

**Q: Pointer value not updating**
- Ensure `value` prop is bound to state: `value={stateValue}`
- Check that axis `minimum` and `maximum` encompass the pointer value

**Q: Animation not playing**
- Verify `animationDuration` > 0
- Check that component is not already at the final value

**Q: Marker not visible**
- Ensure `markerType` is valid (Circle, Rectangle, Triangle, etc.)
- Check `width` is not 0
- Verify `color` contrasts with background

## Next Steps

- Read **Ranges & Annotations** to add value zone highlights
- Read **Advanced Features** for event handling and animations
- Read **Customization** for styling options
