---
name: syncfusion-react-circular-gauge
description: Implement Syncfusion React Circular Gauge for displaying KPIs, sensor data, speedometers, and real-time monitoring dashboards. Use this skill when users need to visualize quantitative measurements on a circular scale. Covers axes, pointers, ranges, customization, animations, print/export, accessibility, and internationalization.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion React Circular Gauge

## When to Use This Skill

Use the Circular Gauge component when you need to:
- **Display measurements** on a circular scale (speedometers, temperature gauges, fuel indicators)
- **Monitor KPIs and metrics** in dashboards (business metrics, sensor readings)
- **Visualize progress or percentages** in a circular format
- **Show real-time data** with animated pointer updates
- **Create responsive data visualizations** with multiple pointers and ranges
- **Print or export gauge visualizations** for reports

The Circular Gauge is ideal for applications requiring visual representation of values on a circular scale with customizable appearance, animations, and interactivity.

---


## Component Overview

**Syncfusion React Circular Gauge** (`@syncfusion/ej2-react-circulargauge`) is a data visualization component that displays values on a circular scale. It consists of:

- **Axes** - The circular scale tracks with customizable angles, direction, and styling
- **Pointers** - Value indicators in three types: Needle (default), RangeBar, or Marker
- **Ranges** - Colored segments representing value ranges (e.g., 0-25%, 25-50%)
- **Annotations** - Text or image overlays for labels and callouts
- **Legend** - Optional legend displaying range meanings
- **Export** - Print, PDF, PNG, or SVG export capabilities

---

## Documentation and Navigation Guide

Choose the reference based on what you need to implement:

### Getting Started & Setup
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Install `@syncfusion/ej2-react-circulargauge` package
- Setup in Vite or Create React App
- Basic component initialization
- Minimal working example
- CSS imports and themes
- **When to read:** First time setup or new project integration

### Gauge Structure: Axes, Pointers & Ranges
📄 **Read:** [references/axes-pointers-ranges.md](references/axes-pointers-ranges.md)
- Configure axes (angles, direction, styling)
- Add and customize pointers (Needle, RangeBar, Marker types)
- Define ranges with colors and labels
- Multiple axes and pointers
- **When to read:** Building the core gauge structure and data visualization

### Visual Appearance & Dimensions
📄 **Read:** [references/appearance-dimensions.md](references/appearance-dimensions.md)
- Add titles and customize styling
- Position gauge (centerX, centerY)
- Set dimensions (width, height, margin)
- Apply backgrounds, borders, color schemes
- Responsive design
- **When to read:** Customizing gauge look, sizing, and layout

### Annotations & Legend
📄 **Read:** [references/annotations-legend.md](references/annotations-legend.md)
- Add text annotations
- Add image annotations
- Position annotations
- Display and customize legend
- Handle legend interactions
- **When to read:** Adding labels, callouts, or explanatory elements

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Animation effects and timing
- User interaction (events, tooltips)
- Print and export to PDF/PNG/SVG
- Real-time data binding
- Multiple gauge instances
- **When to read:** Adding interactions, animations, or export functionality

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Component props, events, methods, and child directive reference
- Quick lookup for commonly used props, methods and event args
- **When to read:** When you need exact API names, types or method signatures

### Accessibility & Internationalization
📄 **Read:** [references/accessibility-i18n.md](references/accessibility-i18n.md)
- WCAG 2.1 compliance and ARIA support
- Screen reader compatibility
- Keyboard navigation
- RTL language support
- Localization and culture settings
- **When to read:** Making gauges accessible or supporting multiple languages

### Common Patterns & Use Cases
📄 **Read:** [references/common-patterns.md](references/common-patterns.md)
- Speedometer pattern
- Progress/percentage gauge pattern
- Temperature/sensor monitoring
- Multi-pointer dashboards
- Real-time updates with animations
- Performance tips and troubleshooting
- **When to read:** Looking for common implementations or solving issues

---

## Quick Start Example

Here's a minimal working example to get started:

```tsx
import React from 'react';
import { CircularGaugeComponent, AxesDirective, AxisDirective, 
         PointersDirective, PointerDirective, RangesDirective, RangeDirective } 
  from '@syncfusion/ej2-react-circulargauge';

export function App() {
  return (
    <div style={{ height: '500px' }}>
      <CircularGaugeComponent 
        title="Speedometer"
        centerX="50%"
        centerY="50%"
      >
        <AxesDirective>
          <AxisDirective 
            startAngle={270} 
            endAngle={90}
            minimum={0}
            maximum={100}
          >
            <RangesDirective>
              <RangeDirective start={0} end={30} color='#1E7145' />
              <RangeDirective start={30} end={60} color='#F7D900' />
              <RangeDirective start={60} end={100} color='#C1192B' />
            </RangesDirective>
            
            <PointersDirective>
              <PointerDirective 
                value={65} 
                type='Needle'
                radius='70%'
              />
            </PointersDirective>
          </AxisDirective>
        </AxesDirective>
      </CircularGaugeComponent>
    </div>
  );
}
```

Install the package first:
```bash
npm install @syncfusion/ej2-react-circulargauge --save
```

---

## Common Patterns

### Pattern 1: Simple Progress Indicator
```tsx
<CircularGaugeComponent>
  <AxesDirective>
    <AxisDirective minimum={0} maximum={100}>
      <RangesDirective>
        <RangeDirective start={0} end={50} color='#E8E8E8' />
        <RangeDirective start={50} end={100} color='#4CAF50' />
      </RangesDirective>
      <PointersDirective>
        <PointerDirective value={75} type='RangeBar' />
      </PointersDirective>
    </AxisDirective>
  </AxesDirective>
</CircularGaugeComponent>
```

### Pattern 2: Multi-Pointer Dashboard
Use multiple pointers on the same axis to compare values:
```tsx
<PointersDirective>
  <PointerDirective value={45} type='Needle' />
  <PointerDirective value={60} type='Marker' />
</PointersDirective>
```

### Pattern 3: Real-Time Updates
```tsx
const [value, setValue] = useState(50);

// Update pointer value on interval
useEffect(() => {
  const timer = setInterval(() => {
    setValue(prev => (prev + Math.random() * 10) % 100);
  }, 1000);
  return () => clearInterval(timer);
}, []);

// Bind value to pointer
<PointerDirective value={value} />
```

---

## Key Configuration Props

| Prop | Type | Purpose |
|------|------|---------|
| `title` | string | Gauge title displayed at top |
| `centerX` / `centerY` | string | Position (% or px) |
| `startAngle` / `endAngle` | number | Axis sweep degrees (0-360) |
| `minimum` / `maximum` | number | Axis scale range |
| `value` (pointer) | number | Current pointer value |
| `type` (pointer) | 'Needle' \| 'RangeBar' \| 'Marker' | Pointer visualization type |
| `radius` (pointer) | string | Pointer length (% or px) |
| `color` | string | Element color (hex, rgb, name) |
| `direction` | 'ClockWise' \| 'AntiClockWise' | Axis direction |
| `animationDuration` | number | Animation time in milliseconds |

---

For the complete API listing (all component props, events, methods and child directives) see: [references/api-reference.md](references/api-reference.md)

## Common Use Cases

1. **Speedometer/Speed Monitor** - Display vehicle speed with colored ranges
2. **Temperature Gauge** - Monitor temperature with hot/cold indicators
3. **Performance KPI** - Show system metrics or business KPIs
4. **Fuel/Battery Level** - Visualize resource consumption
5. **Network Traffic** - Display bandwidth usage in real-time
6. **Sports/Gaming Scores** - Show player stats or game progress
7. **Industrial Monitoring** - Sensor data visualization
8. **Percentage/Progress** - Alternative circular progress visualization

---

## Next Steps

1. **Start with Getting Started** to set up your first gauge
2. **Build structure** using Axes, Pointers & Ranges reference
3. **Customize appearance** with styling reference
4. **Add interactions** with Advanced Features reference
5. **Test accessibility** using Accessibility reference
6. **Reference common patterns** for implementation ideas

For more details or advanced scenarios, consult the specific reference files linked above.
