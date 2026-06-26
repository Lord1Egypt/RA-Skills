---
name: syncfusion-react-linear-gauge
description: Implement Syncfusion React Linear Gauge for displaying measurements on a linear scale. Use this skill when users need temperature sensors, KPI indicators, progress gauges, or real-time monitoring dashboards. Covers axes configuration, pointer types, ranges, annotations, customization, animations, print/export, accessibility, and internationalization.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion React Linear Gauge

## When to Use This Skill

Use the Linear Gauge component when you need to:
- **Display measurements** on a linear/horizontal scale (temperature gauges, thermometers, fuel indicators)
- **Monitor real-time data** with animated pointer updates (sensor readings, system metrics)
- **Show progress or percentages** in a linear format
- **Create dashboards** with multiple gauges displaying KPIs
- **Visualize ranges** with different colors (e.g., safe, warning, critical zones)
- **Build responsive data visualizations** with customizable appearance and interactivity
- **Print or export gauge visualizations** for reports and documentation

The Linear Gauge is ideal for applications requiring visual representation of values on a horizontal/linear scale with customizable axes, pointers, ranges, and interactive features.

---

## Component Overview

**Syncfusion React Linear Gauge** (`@syncfusion/ej2-react-lineargauge`) is a data visualization component that displays values on a linear scale. It consists of:

- **Axes** - The linear scale with customizable range, ticks, labels, and styling
- **Pointers** - Value indicators in two types: Bar (default) or Marker (shapes)
- **Ranges** - Colored segments representing value ranges (e.g., cold, warm, hot)
- **Annotations** - Text or image overlays for labels and callouts
- **Ticks & Labels** - Scale markers with customizable formatting
- **Export** - Print, PDF, PNG, or SVG export capabilities

---

## Documentation and Navigation Guide

Choose the reference based on what you need to implement:

### Getting Started & Setup
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Install `@syncfusion/ej2-react-lineargauge` package
- Setup in Vite or Create React App
- Basic component initialization
- Minimal working example
- CSS imports and themes
- **When to read:** First time setup or new project integration

### Gauge Structure: Axes, Ticks & Labels
📄 **Read:** [references/axis-ticks-labels.md](references/axis-ticks-labels.md)
- Configure axes (minimum, maximum range)
- Customize axis line (height, width, color)
- Configure major and minor ticks
- Format and customize labels
- Set label units and formatting
- Multiple axes configuration
- **When to read:** Building the core gauge structure and scale

### Pointer Types & Configuration
📄 **Read:** [references/pointers.md](references/pointers.md)
- Bar pointer type (default, fill styles)
- Marker pointer types (Circle, Rectangle, Triangle, Diamond, Image, Text)
- Setting and updating pointer values
- Customize pointer appearance (width, color, radius)
- Multiple pointers on same axis
- Drag-drop interactions
- Performance optimization
- **When to read:** Adding value indicators and interactive features

### Ranges & Annotations
📄 **Read:** [references/ranges-annotations.md](references/ranges-annotations.md)
- Creating ranges with start/end values
- Range styling (colors, gradient effects)
- Range labels and positions
- Text annotations for callouts and labels
- Image annotations
- Positioning and alignment
- **When to read:** Highlighting value zones or adding descriptive elements

### Visual Appearance & Customization
📄 **Read:** [references/appearance-customization.md](references/appearance-customization.md)
- Add titles
- Set gauge dimensions (width, height, margin)
- Customize background and borders
- Apply themes and color schemes
- Responsive design patterns
- CSS class customization
- RTL language support
- **When to read:** Styling and customizing gauge appearance

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Animation effects and timing
- Event handling (valueChange, print, export)
- Tooltips and hover effects
- Print and export to PDF/PNG/SVG
- Real-time data binding and updates
- Combining multiple features
- Performance tips and optimization
- **When to read:** Adding interactions, animations, or export functionality


## Quick Start Example

Here's a minimal working example to get started:

```tsx
import React from 'react';
import { LinearGaugeComponent, AxesDirective, AxisDirective, 
         PointersDirective, PointerDirective, RangesDirective, RangeDirective } 
  from '@syncfusion/ej2-react-lineargauge';
import '@syncfusion/ej2-lineargauge/styles/material.css';

export function App() {
  return (
    <div style={{ height: '400px', width: '100%' }}>
      <LinearGaugeComponent 
        title="Temperature Monitor"
        orientation="Horizontal"
      >
        <AxesDirective>
          <AxisDirective 
            minimum={0}
            maximum={100}
            labelStyle={{ format: '{value}°C' }}
          >
            <RangesDirective>
              <RangeDirective start={0} end={30} color='#1E90FF' />
              <RangeDirective start={30} end={70} color='#FFA500' />
              <RangeDirective start={70} end={100} color='#FF4500' />
            </RangesDirective>
            
            <PointersDirective>
              <PointerDirective value={55} />
            </PointersDirective>
          </AxisDirective>
        </AxesDirective>
      </LinearGaugeComponent>
    </div>
  );
}
```

Install the package first:
```bash
npm install @syncfusion/ej2-react-lineargauge --save
```

---

## Common Patterns

### Pattern 1: Simple Temperature Gauge
```tsx
<LinearGaugeComponent title="Temperature">
  <AxesDirective>
    <AxisDirective minimum={-40} maximum={50} labelStyle={{ format: '{value}°C' }}>
      <RangesDirective>
        <RangeDirective start={-40} end={0} color='#4CAF50' />
        <RangeDirective start={0} end={25} color='#8BC34A' />
        <RangeDirective start={25} end={50} color='#FF5722' />
      </RangesDirective>
      <PointersDirective>
        <PointerDirective value={20} />
      </PointersDirective>
    </AxisDirective>
  </AxesDirective>
</LinearGaugeComponent>
```

### Pattern 2: Progress/Percentage Indicator
```tsx
<PointersDirective>
  <PointerDirective 
    value={75} 
    type='Marker'
    markerType='Rectangle'
    width={20}
    color='#007AFF'
  />
</PointersDirective>
```

### Pattern 3: Real-Time Updates
```tsx
const [value, setValue] = useState(50);

useEffect(() => {
  const timer = setInterval(() => {
    setValue(prev => (prev + (Math.random() - 0.5) * 10) % 100);
  }, 1000);
  return () => clearInterval(timer);
}, []);

<PointerDirective value={value} />
```

---

## LinearGaugeComponent API Reference

### **Verified Props (Based on Official Syncfusion Documentation)**

| Prop | Type | Purpose | Example |
|------|------|---------|---------|
| `title` | string | Gauge title text | `title="Temperature"` |
| `orientation` | "Horizontal" \| "Vertical" | Layout orientation (default: Vertical) | `orientation="Horizontal"` |
| `width` | string | Gauge width | `width="100%"` or `width="400px"` |
| `height` | string | Gauge height | `height="300px"` |

---

## AxisDirective API Reference

### **Verified Props for AxisDirective**

| Prop | Type | Purpose | Example |
|------|------|---------|---------|
| `minimum` | number | Start value of the axis range | `minimum={0}` |
| `maximum` | number | End value of the axis range | `maximum={200}` |
| `labelStyle` | object | Label customization (use `format` property) | `labelStyle={{ format: '{value}°C' }}` |

### **labelStyle Format Options**
- `{ format: '{value}' }` - Shows value as-is
- `{ format: '{value}°C' }` - Adds °C suffix
- `{ format: '${value}K' }` - Adds $ prefix and K suffix
- `{ format: '{value}%' }` - Adds % suffix

**⚠️ NOT SUPPORTED:**
- ❌ `majorTicksInterval` - Not a valid property
- ❌ `minorTicksInterval` - Not a valid property
- ❌ `axisLineStyle` - Not a valid property (use axis-level styling instead)

---

## PointerDirective API Reference

### **Verified Props for PointerDirective**

| Prop | Type | Purpose | Example |
|------|------|---------|---------|
| `value` | number | The value to display | `value={140}` |
| `color` | string | Pointer color (hex or named) | `color='green'` or `color='#1976D2'` |
| `type` | "Bar" \| "Marker" | Pointer shape type (default: Bar) | `type="Marker"` |
| `markerType` | "Circle" \| "Rectangle" \| "Triangle" \| "Diamond" \| "Image" \| "Text" | Shape for marker pointers | `markerType="Rectangle"` |
| `width` | number | Pointer width in pixels | `width={8}` |

### **Pointer Type Examples**

**Bar Pointer (Default)**
```tsx
<PointerDirective value={140} color='blue' width={8} />
```

**Marker Pointer**
```tsx
<PointerDirective 
  value={75} 
  type='Marker'
  markerType='Rectangle'
  width={15}
  color='#1976D2'
/>
```

---

## RangeDirective API Reference

### **Verified Props for RangeDirective**

| Prop | Type | Purpose | Example |
|------|------|---------|---------|
| `start` | number | Start value of the range | `start={0}` |
| `end` | number | End value of the range | `end={80}` |
| `color` | string | Range background color | `color='#4CAF50'` |
| `startWidth` | number | Width of start edge | `startWidth={15}` |
| `endWidth` | number | Width of end edge | `endWidth={15}` |

### **Example with Width**
```tsx
<RangeDirective start={0} end={80} color='#4CAF50' startWidth={15} endWidth={15} />
```

---

## Working Code Examples

### **Example 1: Temperature Gauge (Verified)**
```tsx
import React from 'react';
import { LinearGaugeComponent, AxesDirective, AxisDirective, 
         PointersDirective, PointerDirective, RangesDirective, RangeDirective } 
  from '@syncfusion/ej2-react-lineargauge';

export function App() {
  return (
    <LinearGaugeComponent>
      <AxesDirective>
        <AxisDirective minimum={0} maximum={200} labelStyle={{ format: '{value}°C' }}>
          <PointersDirective>
            <PointerDirective value={140} color='green'></PointerDirective>
          </PointersDirective>
          <RangesDirective>
            <RangeDirective start={0} end={80} startWidth={15} endWidth={15}></RangeDirective>
            <RangeDirective start={80} end={120} startWidth={15} endWidth={15}></RangeDirective>
            <RangeDirective start={120} end={140} startWidth={15} endWidth={15}></RangeDirective>
            <RangeDirective start={140} end={200} startWidth={15} endWidth={15}></RangeDirective>
          </RangesDirective>
        </AxisDirective>
      </AxesDirective>
    </LinearGaugeComponent>
  );
}
```

### **Example 2: Progress Indicator (Verified)**
```tsx
<LinearGaugeComponent title="Project Status">
  <AxesDirective>
    <AxisDirective minimum={0} maximum={100} labelStyle={{ format: '{value}%' }}>
      <RangesDirective>
        <RangeDirective start={0} end={30} color='#EF5350' startWidth={15} endWidth={15}></RangeDirective>
        <RangeDirective start={30} end={70} color='#FFCA28' startWidth={15} endWidth={15}></RangeDirective>
        <RangeDirective start={70} end={100} color='#66BB6A' startWidth={15} endWidth={15}></RangeDirective>
      </RangesDirective>
      <PointersDirective>
        <PointerDirective value={75} color='#1976D2' width={8}></PointerDirective>
      </PointersDirective>
    </AxisDirective>
  </AxesDirective>
</LinearGaugeComponent>
```

### **Example 3: Multi-Pointer Gauge (Verified)**
```tsx
<LinearGaugeComponent>
  <AxesDirective>
    <AxisDirective minimum={0} maximum={1000} labelStyle={{ format: '${value}K' }}>
      <RangesDirective>
        <RangeDirective start={0} end={400} color='#E53935' startWidth={15} endWidth={15}></RangeDirective>
        <RangeDirective start={400} end={700} color='#FB8C00' startWidth={15} endWidth={15}></RangeDirective>
        <RangeDirective start={700} end={1000} color='#43A047' startWidth={15} endWidth={15}></RangeDirective>
      </RangesDirective>
      <PointersDirective>
        <PointerDirective value={650} color='#1976D2' width={6}></PointerDirective>
        <PointerDirective value={850} type='Marker' markerType='Circle' width={10} color='#FF6F00'></PointerDirective>
      </PointersDirective>
    </AxisDirective>
  </AxesDirective>
</LinearGaugeComponent>
```

---

### LinearGaugeComponent Methods & Events

Use the following methods/events when you need interactivity like animation lifecycle, tooltips, drag, export, and print:

**Methods**
- `destroy()`
- `export(type, fileName, orientation?, allowDownload?)`
- `print(id?)`
- `setAnnotationValue(annotationIndex, content, axisValue?)`
- `setPointerValue(axisIndex, pointerIndex, value)`

**Events**
- `load`, `loaded`, `resized`
- `valueChange` (pointer value changes)
- `dragStart`, `dragMove`, `dragEnd`
- `beforePrint`
- `tooltipRender`
- `animationComplete`
- `annotationRender`, `axisLabelRender`
- `gaugeMouseDown`, `gaugeMouseMove`, `gaugeMouseUp`, `gaugeMouseLeave`

---

## Common Use Cases

1. **Temperature Monitoring** - Real-time temperature with hot/cold indicators
2. **Sensor Data Visualization** - Display sensor readings (pressure, humidity, etc.)
3. **Performance Metrics** - Show system performance, CPU usage, memory
4. **Progress Indicators** - Visualize task completion or download progress
5. **Fuel/Battery Level** - Monitor resource consumption
6. **Speed/RPM Gauges** - Display rotation speeds or velocities
7. **Network Traffic** - Show bandwidth usage in real-time
8. **Quality/Score Indicators** - Display ratings or quality metrics

---

## Next Steps

1. **Start with Getting Started** to install and setup your first gauge
2. **Build structure** using Axes, Ticks & Labels reference
3. **Add pointers** using Pointer Types & Configuration reference
4. **Highlight zones** with Ranges & Annotations reference
5. **Customize appearance** with Visual Appearance reference
6. **Add interactions** with Advanced Features reference
7. **Test accessibility** using Accessibility reference

For more details or advanced scenarios, consult the specific reference files linked above.
