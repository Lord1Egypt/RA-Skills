# Axes, Pointers & Ranges

See the API quick reference: [api-reference.md](api-reference.md) for exact prop and child directive names (e.g., `PointersDirective`, `RangeDirective`, `setPointerValue`).

## Table of Contents
- [Axis Customization](#axis-customization)
  - [Line Style](#line-style)
  - [Axis Background](#axis-background)
  - [Complete Axis Styling Example](#complete-axis-styling-example)
- [Axis Angles and Direction](#axis-angles-and-direction)
  - [Start and End Angles](#start-and-end-angles)
  - [Axis Direction](#axis-direction)
  - [Common Angle Combinations](#common-angle-combinations)
- [Axis Scale and Labels](#axis-scale-and-labels)
  - [Minimum and Maximum Values](#minimum-and-maximum-values)
  - [Major and Minor Ticks](#major-and-minor-ticks)
  - [Labels](#labels)
- [Pointer Types](#pointer-types)
  - [Needle Pointer (Default)](#needle-pointer-default)
  - [RangeBar Pointer](#rangebar-pointer)
  - [Marker Pointer](#marker-pointer)
- [Needle Pointer](#needle-pointer)
  - [Basic Needle Configuration](#basic-needle-configuration)
  - [Needle with Cap and Tail](#needle-with-cap-and-tail)
  - [Styled Speedometer Needle](#styled-speedometer-needle)
- [RangeBar Pointer](#rangebar-pointer-1)
  - [Basic RangeBar](#basic-rangebar)
  - [RangeBar with Rounded Corners](#rangebar-with-rounded-corners)
  - [Multiple RangeBars (Progress Layers)](#multiple-rangebars-progress-layers)
- [Marker Pointer](#marker-pointer-1)
  - [Basic Marker](#basic-marker)
  - [Different Marker Shapes](#different-marker-shapes)
  - [Custom Marker with Image](#custom-marker-with-image)
  - [Styled Marker](#styled-marker)
- [Ranges](#ranges)
  - [Basic Range](#basic-range)
  - [Multiple Ranges](#multiple-ranges)
  - [Range Customization](#range-customization)
  - [Temperature Gauge with Ranges](#temperature-gauge-with-ranges)
- [Multiple Axes and Pointers](#multiple-axes-and-pointers)
  - [Dual-Axis Gauge](#dual-axis-gauge)
  - [Multiple Pointers on Same Axis](#multiple-pointers-on-same-axis)
  - [Multi-Pointer Dashboard](#multi-pointer-dashboard)
- [Common Patterns](#common-patterns)
- [Troubleshooting](#troubleshooting)

---

## Axis Customization

### Line Style

Customize the axis line (the circular track) with width and color:

```tsx
<AxisDirective
  lineStyle={{
    width: 2,
    color: '#e0e0e0'
  }}
/>
```

### Axis Background

Add a background color or pattern to the axis area:

```tsx
<AxisDirective
  background='rgba(200, 220, 240, 0.3)'
/>
```

### Complete Axis Styling Example

```tsx
<AxisDirective
  lineStyle={{
    width: 3,
    color: '#1976d2'
  }}
  background='rgba(25, 118, 210, 0.1)'
  majorTicks={{
    interval: 10,
    width: 2,
    color: '#1976d2',
    offset: 5
  }}
  minorTicks={{
    interval: 2,
    width: 1,
    color: '#90caf9',
    offset: 5
  }}
  labelStyle={{
    color: '#1976d2',
    offset: 15,
    format: '{value}%'
  }}
/>
```

---

## Axis Angles and Direction

### Start and End Angles

By default, the gauge sweeps from 200° to 160° (semi-circular). Customize with `startAngle` and `endAngle`:

```tsx
// Semicircular (bottom half)
<AxisDirective
  startAngle={180}
  endAngle={0}
  
/>

// Full circle
<AxisDirective
  startAngle={0}
  endAngle={360}
/>

// Quarter circle (top-right)
<AxisDirective
  startAngle={270}
  endAngle={0}
/>

// Speedometer style (bottom-left to top-right)
<AxisDirective
  startAngle={270}
  endAngle={90}
/>
```

**Angle reference:**
- 0° = Right (3 o'clock)
- 90° = Bottom (6 o'clock)
- 180° = Left (9 o'clock)
- 270° = Top (12 o'clock)

### Axis Direction

Control whether the axis sweeps clockwise or counter-clockwise:

```tsx
// Clockwise (default, values increase going right)
<AxisDirective direction='ClockWise' />

// Counter-clockwise (values increase going left)
<AxisDirective direction='AntiClockWise' />
```

### Common Angle Combinations

```tsx
// Semicircular gauge (bottom to top)
<AxisDirective startAngle={270} endAngle={90} />

// Speedometer (quarter circle)
<AxisDirective startAngle={270} endAngle={0} direction='ClockWise' />

// Temperature gauge (bottom half)
<AxisDirective startAngle={180} endAngle={0} />

// Linear-like gauge (full circle, might show 180° only)
<AxisDirective startAngle={0} endAngle={180} />
```

---

## Axis Scale and Labels

### Minimum and Maximum Values

Define the scale range:

```tsx
<AxisDirective
  minimum={0}
  maximum={100}
/>

// For percentage gauge
<AxisDirective
  minimum={0}
  maximum={100}
/>

// For temperature (-50 to 50 Celsius)
<AxisDirective
  minimum={-50}
  maximum={50}
/>

// For speed (0 to 300 km/h)
<AxisDirective
  minimum={0}
  maximum={300}
/>
```

### Major and Minor Ticks

Control tick marks on the axis:

```tsx
<AxisDirective
  majorTicks={{
    interval: 20,        // Every 20 units
    width: 2,           // Thickness
    color: '#616161',   // Color
    offset: 5           // Distance from axis
  }}
  minorTicks={{
    interval: 4,        // Every 4 units (5 minor between each major)
    width: 1,
    color: '#9e9e9e',
    offset: 5
  }}
/>
```

### Labels

Format and position the numeric labels:

```tsx
<AxisDirective
  labelStyle={{
    position: 'Outside' // 'Inside', 'Outside','Cross'
    color: '#424242',
    size: '14px',
    offset: 15,      // Distance from axis line
    format: '{value}°C'  // Custom format
  }}
/>
```

---

## Pointer Types

The gauge supports three pointer types for displaying values:

### Needle Pointer (Default)

Classic needle/hand indicator, ideal for speedometers:

```tsx
<PointerDirective
  type='Needle'
  value={75}
/>
```

**Needle-specific properties:**
- `radius` - Length of the needle (50%, 80%, etc.)
- `pointerWidth` - Width of the needle line
- `needleTail` - Configuration object for tail:
  - `length` - Tail length (20%, 30%, etc.)
  - `color` - Tail color
- `cap` - Configuration object for center cap:
  - `radius` - Cap radius
  - `color` - Cap color
  - `border` - Border configuration

### RangeBar Pointer

Filled bar from center to value, ideal for progress indicators:

```tsx
<PointerDirective value={60} type="RangeBar" radius="80%" pointerWidth={10} color="#4caf50" roundedCorners={true} />
```

**RangeBar-specific properties:**
- `radius` - Length from center (50%, 80%, etc.)
- `pointerWidth` - Bar thickness
- `color` - Bar fill color
- `roundedCorners` - Round the bar ends (boolean)

### Marker Pointer

Symbol at the value position, ideal for multi-pointer displays:

```tsx

<PointerDirective value={45} type="Marker" markerShape="Circle" markerWidth={20} markerHeight={20} offset={10} color="#f44336" />
```

**Marker-specific properties:**
- `markerShape` - Shape type
- `markerWidth` - Marker size (20, 30, etc.)
- `markerHeight` - Marker height
- `imageUrl` - URL for Image marker type
- `radius` - Distance from center where marker is positioned (50%, 80%, etc.)

---

## Needle Pointer

### Basic Needle Configuration

```tsx
<PointerDirective
  value={85}
  type='Needle'
  radius='80%'
  pointerWidth={5}
  color='#424242'
/>
```

### Needle with Cap and Tail

```tsx
<PointerDirective
  value={85}
  type='Needle'
  radius='80%'
  pointerWidth={6}
  color='#1976d2'
  cap={{
    radius: 10,
    color: '#1976d2',
    border: {
      width: 3,
      color: '#ffffff'
    }
  }}
  needleTail={{
    length: '25%',
    width: 4,
    color: '#1976d2'
  }}
/>
```

### Styled Speedometer Needle

```tsx
<PointerDirective
  value={60}
  type='Needle'
  radius='75%'
  pointerWidth={4}
  color='#f57c00'
  animation={{
    duration: 500,
    enable: true
  }}
  cap={{
    radius: 12,
    color: '#f57c00',
    border: {
      width: 2,
      color: '#ffd54f'
    }
  }}
  needleTail={{
    length: '20%',
    width: 3,
    color: '#f57c00'
  }}
/>
```

---

## RangeBar Pointer

### Basic RangeBar

```tsx
<PointerDirective
  value={65}
  type='RangeBar'
  radius='80%'
  pointerWidth={12}
  color='#4caf50'
/>
```

### RangeBar with Rounded Corners

```tsx
<PointerDirective
  value={70}
  type='RangeBar'
  radius='75%'
  pointerWidth={15}
  color='#2196f3'
  roundedCorners={true}
/>
```

### Multiple RangeBars (Progress Layers)

```tsx
<PointersDirective>
  {/* Background bar */}
  <PointerDirective
    value={100}
    type='RangeBar'
    radius='60%'
    pointerWidth={20}
    color='#e0e0e0'
  />
  {/* Actual progress */}
  <PointerDirective
    value={75}
    type='RangeBar'
    radius='60%'
    pointerWidth={20}
    color='#4caf50'
  />
</PointersDirective>
```

---

## Marker Pointer

### Basic Marker

```tsx
<PointerDirective
  value={50}
  type='Marker'
  markerShape='Circle'
/>
```

### Different Marker Shapes

```tsx
<PointersDirective>
  <PointerDirective value={20} type='Marker' markerShape='Circle' />
  <PointerDirective value={40} type='Marker' markerShape='Rectangle' />
  <PointerDirective value={60} type='Marker' markerShape='Triangle' />
  <PointerDirective value={80} type='Marker' markerShape='Diamond' />
</PointersDirective>
```

### Custom Marker with Image

```tsx
<PointerDirective
  value={75}
  type='Marker'
  markerShape='Image'
  imageUrl='./assets/arrow.png'
  markerWidth={30}
  markerHeight={40}
/>
```

### Styled Marker

```tsx
<PointerDirective
  value={50}
  type='Marker'
  markerShape='Circle'
  markerWidth={20}
  markerHeight={20}
  color='#ff6f00'
  radius='85%'
/>
```

---

## Ranges

Ranges define colored segments on the axis background to indicate value zones:

### Basic Range

```tsx
<RangeDirective
  start={0}
  end={30}
  color='#4caf50'
/>
```

### Multiple Ranges

```tsx
import * as React from 'react';
import { createRoot } from 'react-dom/client';
import {
  CircularGaugeComponent,
  AxesDirective,
  AxisDirective,
  RangesDirective,
  RangeDirective,
} from '@syncfusion/ej2-react-circulargauge';
export function App() {
  return (
    <CircularGaugeComponent>
      <AxesDirective>
        <AxisDirective>
          <RangesDirective>
            <RangeDirective
              start={0}
              end={33}
              color="#4caf50"
              startWidth={10}
              endWidth={10}
            />
            <RangeDirective
              start={33}
              end={66}
              color="#fbc02d"
              startWidth={10}
              endWidth={10}
            />
            <RangeDirective
              start={66}
              end={100}
              color="#f44336"
              startWidth={10}
              endWidth={10}
            />
          </RangesDirective>
        </AxisDirective>
      </AxesDirective>
    </CircularGaugeComponent>
  );
}
const root = createRoot(document.getElementById('container'));
root.render(<App />);

```

### Range Customization

```tsx
<RangeDirective
  start={40}
  end={80}
  color='#2196f3'
  startWidth={5}      // Width at start point
  endWidth={10}       // Width at end point (tapered)
  opacity={0.8}       // Transparency (0-1)
  roundedCorners={true}
/>
```

### Temperature Gauge with Ranges

```tsx
<RangesDirective>
  {/* Cold (blue) */}
  <RangeDirective start={-50} end={0} color='#2196f3' startWidth={12} endWidth={12} />
  {/* Moderate (green) */}
  <RangeDirective start={0} end={30} color='#4caf50' startWidth={12} endWidth={12} />
  {/* Warm (orange) */}
  <RangeDirective start={30} end={40} color='#ff9800' startWidth={12} endWidth={12} />
  {/* Hot (red) */}
  <RangeDirective start={40} end={50} color='#f44336' startWidth={12} endWidth={12} />
</RangesDirective>
```

---

## Multiple Axes and Pointers

### Dual-Axis Gauge

Display two independent scales:

```tsx
import React from 'react';
import { createRoot } from 'react-dom/client';
import {
  CircularGaugeComponent,
  AxesDirective,
  AxisDirective,
  PointersDirective,
  PointerDirective,
} from '@syncfusion/ej2-react-circulargauge';

export function RealtimeDashboard() {
  return (
    <div style={{ height: '500px', width: '100%' }}>
      <CircularGaugeComponent>
        <AxesDirective>
          {/* First axis (Celsius) */}
          <AxisDirective
            minimum={0}
            maximum={50}
            lineStyle={{ color: '#2196f3' }}
            labelStyle={{ format: '{value}°C' }}
          >
            <PointersDirective>
              <PointerDirective value={25} color="#2196f3" />
            </PointersDirective>
          </AxisDirective>

          {/* Second axis (Fahrenheit) */}
          <AxisDirective
            minimum={32}
            maximum={122}
            lineStyle={{ color: '#f44336' }}
            labelStyle={{ format: '{value}°F' }}
          >
            <PointersDirective>
              <PointerDirective value={77} color="#f44336" />
            </PointersDirective>
          </AxisDirective>
        </AxesDirective>
      </CircularGaugeComponent>
    </div>
  );
}

// Mounting
const root = createRoot(document.getElementById('container'));
root.render(<RealtimeDashboard />);

```

### Multiple Pointers on Same Axis

Compare different values:

```tsx
import React from 'react';
import { createRoot } from 'react-dom/client';
import {
  CircularGaugeComponent,
  AxesDirective,
  AxisDirective,
  PointersDirective,
  PointerDirective
} from '@syncfusion/ej2-react-circulargauge';

export function RealtimeDashboard() {
  return (
    <div style={{ height: '500px', width: '100%' }}>
      <CircularGaugeComponent>
        <AxesDirective>
          <AxisDirective>
            <PointersDirective>
              <PointerDirective value={30} type="Needle" color="#1976d2" />
              <PointerDirective
                value={50}
                type="Marker"
                markerShape="Circle"
                color="#f44336"
              />
              <PointerDirective value={70} type="RangeBar" color="#4caf50" />
            </PointersDirective>
          </AxisDirective>
        </AxesDirective>
      </CircularGaugeComponent>
    </div>
  );
}

// Mounting
const root = createRoot(document.getElementById('container'));
root.render(<RealtimeDashboard />);

```

### Multi-Pointer Dashboard

Combine multiple axes for complex monitoring:

```tsx
import React from 'react';
import { createRoot } from 'react-dom/client';
import {
  CircularGaugeComponent,
  AxesDirective,
  AxisDirective,
  PointersDirective,
  PointerDirective,
  RangesDirective,
  RangeDirective,
} from '@syncfusion/ej2-react-circulargauge';

export function RealtimeDashboard() {
  return (
    <div style={{ height: '500px', width: '100%' }}>
      <CircularGaugeComponent>
        <AxesDirective>
          <AxisDirective minimum={0} maximum={100}>
            <PointersDirective>
              <PointerDirective value={60} type="Needle" color="#1976d2" />
              <PointerDirective value={75} type="Marker" color="#f44336" />
            </PointersDirective>
          </AxisDirective>

          <AxisDirective minimum={0} maximum={200}>
            <PointersDirective>
              <PointerDirective value={120} type="RangeBar" color="#4caf50" />
            </PointersDirective>
          </AxisDirective>
        </AxesDirective>
      </CircularGaugeComponent>
    </div>
  );
}

// Mounting
const root = createRoot(document.getElementById('container'));
root.render(<RealtimeDashboard />);

```

---

## Common Patterns

### Speedometer
```tsx
import React from 'react';
import { createRoot } from 'react-dom/client';
import {
  CircularGaugeComponent,
  AxesDirective,
  AxisDirective,
  PointersDirective,
  PointerDirective,
  RangesDirective,
  RangeDirective
} from '@syncfusion/ej2-react-circulargauge';

export function RealtimeDashboard() {
  return (
    <div style={{ height: '500px', width: '100%' }}>
      <CircularGaugeComponent>
        <AxesDirective>
          <AxisDirective
            startAngle={270}
            endAngle={90}
            minimum={0}
            maximum={240}
          >
            <RangesDirective>
              <RangeDirective start={0} end={80} color="#4caf50" startWidth={10} endWidth={10} />
              <RangeDirective start={80} end={160} color="#fbc02d" startWidth={10} endWidth={10} />
              <RangeDirective start={160} end={240} color="#f44336" startWidth={10} endWidth={10} />
            </RangesDirective>

            <PointersDirective>
              <PointerDirective value={120} radius="80%" />
            </PointersDirective>
          </AxisDirective>
        </AxesDirective>
      </CircularGaugeComponent>
    </div>
  );
}

// Mounting
const root = createRoot(document.getElementById('container'));
root.render(<RealtimeDashboard />);
```

### Progress/Percentage
```tsx
import React from 'react';
import { createRoot } from 'react-dom/client';
import {
  CircularGaugeComponent,
  AxesDirective,
  AxisDirective,
  PointersDirective,
  PointerDirective,
  RangesDirective,
  RangeDirective,
} from '@syncfusion/ej2-react-circulargauge';

export function RealtimeDashboard() {
  return (
    <div style={{ height: '500px', width: '100%' }}>
      <CircularGaugeComponent>
        <AxesDirective>
          <AxisDirective
            startAngle={270}
            endAngle={90}
            minimum={0}
            maximum={100}
          >
            <RangesDirective>
              <RangeDirective
                start={0}
                end={100}
                color="#e0e0e0"
                startWidth={15}
                endWidth={15}
              />
            </RangesDirective>
            <PointersDirective>
              <PointerDirective value={65} type="RangeBar" color="#4caf50" />
            </PointersDirective>
          </AxisDirective>
        </AxesDirective>
      </CircularGaugeComponent>
    </div>
  );
}

// Mounting
const root = createRoot(document.getElementById('container'));
root.render(<RealtimeDashboard />);

```

---

## Troubleshooting

**Pointer not visible:** Check that pointer value is within axis minimum/maximum range.

**Range colors not showing:** Ensure range start/end values are within axis scale.

**Multiple pointers overlapping:** Use different pointer types or adjust `radius` values.
