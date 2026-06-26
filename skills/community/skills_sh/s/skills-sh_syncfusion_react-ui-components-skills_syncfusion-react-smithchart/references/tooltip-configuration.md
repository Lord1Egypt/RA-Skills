# Tooltip Configuration

## Overview

Tooltips display detailed information about data points when users hover over them with the mouse. They provide an alternative to data labels when you cannot display information permanently due to space constraints or visual clutter. By default, tooltips are disabled in Smith Charts.

## Table of Contents

- [Overview](#overview)
- [Enabling Tooltips](#enabling-tooltips)
- [Per-Series Tooltip Configuration](#per-series-tooltip-configuration)
- [Tooltip Display Information](#tooltip-display-information)
- [When to Use Tooltips](#when-to-use-tooltips)
  - [Use Tooltips When:](#use-tooltips-when)
  - [Avoid Tooltips When:](#avoid-tooltips-when)
- [Complete Examples](#complete-examples)
  - [Basic Tooltip Implementation](#basic-tooltip-implementation)
  - [Multiple Series with Tooltips](#multiple-series-with-tooltips)
  - [Combining Tooltips with Markers](#combining-tooltips-with-markers)
  - [Selective Tooltip Usage](#selective-tooltip-usage)
- [Best Practices](#best-practices)
  - [When to Enable Tooltips](#when-to-enable-tooltips)
  - [Tooltip vs Data Labels](#tooltip-vs-data-labels)
  - [Module Injection](#module-injection)
  - [Performance Considerations](#performance-considerations)
  - [Accessibility Considerations](#accessibility-considerations)
- [Common Patterns](#common-patterns)
  - [Dynamic Tooltip Control](#dynamic-tooltip-control)
  - [Conditional Tooltips Based on Data](#conditional-tooltips-based-on-data)
  - [Tooltips with All Features](#tooltips-with-all-features)
- [Troubleshooting](#troubleshooting)
  - [Tooltips Not Appearing](#tooltips-not-appearing)
  - [Tooltip Performance](#tooltip-performance)

## Enabling Tooltips

To enable tooltips, you must:

1. Inject the `TooltipRender` module into the component
2. Set the `visible` property to `true` in the `tooltip` object of each series

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective, Inject, TooltipRender } from '@syncfusion/ej2-react-charts';

function App() {
  const transmissionData = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.3, reactance: 0.2 },
    { resistance: 0.7, reactance: 0.4 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <SmithchartComponent id="smithchart">
      <Inject services={[TooltipRender]} />
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective
          name="Transmission Line"
          points={transmissionData}
          tooltip={{ visible: true }}
        />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

## Per-Series Tooltip Configuration

You can enable or disable tooltips independently for each series, allowing fine-grained control over which data displays hover information.

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective, Inject, TooltipRender } from '@syncfusion/ej2-react-charts';

function App() {
  const measuredData = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  const simulatedData = [
    { resistance: 0.1, reactance: 0.1 },
    { resistance: 0.6, reactance: 0.35 },
    { resistance: 1.1, reactance: 0.55 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      title={{ text: 'Measured vs Simulated Data' }}
    >
      <Inject services={[TooltipRender]} />
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective
          name="Measured Data"
          points={measuredData}
          fill="#3498db"
          tooltip={{ visible: true }}  // Tooltips enabled
        />
        <SmithchartSeriesDirective
          name="Simulated Data"
          points={simulatedData}
          fill="#95a5a6"
          tooltip={{ visible: false }}  // Tooltips disabled
        />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

## Tooltip Display Information

When enabled, tooltips automatically display:
- **Series name** - The name of the series the point belongs to
- **Resistance value** - The resistance coordinate of the data point
- **Reactance value** - The reactance coordinate of the data point

The tooltip appears on mouse hover and disappears when the mouse moves away from the data point.

## When to Use Tooltips

### Use Tooltips When:

1. **Space is limited** - Chart has many data points and permanent labels would clutter the visualization
2. **Interactive exploration** - Users need to explore data interactively rather than view all values at once
3. **Optional information** - Exact values are helpful but not critical for primary interpretation
4. **Multiple series** - Displaying all data labels would create visual confusion
5. **Web applications** - Mouse interaction is available and expected
6. **Dashboard views** - Space is premium and interaction is acceptable

### Avoid Tooltips When:

1. **Static reports** - Printed documents or PDFs don't support hover interaction
2. **Mobile-first** - Touch devices don't have hover states (though tap-to-show can work)
3. **Critical values** - Exact numbers must be immediately visible without interaction
4. **Accessibility priority** - Users rely on screen readers (use data labels or text alternatives)
5. **Presentations** - No mouse interaction during slideshow

## Complete Examples

### Basic Tooltip Implementation

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective, Inject, TooltipRender } from '@syncfusion/ej2-react-charts';

function App() {
  const impedanceData = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.1, reactance: 0.1 },
    { resistance: 0.3, reactance: 0.2 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 0.8, reactance: 0.4 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      title={{ text: 'Impedance Matching Analysis' }}
    >
      <Inject services={[TooltipRender]} />
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective
          name="Input Impedance"
          points={impedanceData}
          fill="#e74c3c"
          width={2}
          marker={{ visible: true }}
          tooltip={{ visible: true }}
        />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

### Multiple Series with Tooltips

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective, Inject, TooltipRender, SmithchartLegend } from '@syncfusion/ej2-react-charts';

function App() {
  const line50 = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.3, reactance: 0.2 },
    { resistance: 0.8, reactance: 0.4 }
  ];

  const line75 = [
    { resistance: 0.1, reactance: 0.1 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.1, reactance: 0.55 }
  ];

  const line100 = [
    { resistance: 0.2, reactance: 0.15 },
    { resistance: 0.6, reactance: 0.35 },
    { resistance: 1.2, reactance: 0.6 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      title={{ text: 'Transmission Line Comparison' }}
      legendSettings={{ visible: true, position: 'Bottom' }}
    >
      <Inject services={[TooltipRender, SmithchartLegend]} />
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective
          name="50Ω Line"
          points={line50}
          fill="#3498db"
          tooltip={{ visible: true }}
        />
        <SmithchartSeriesDirective
          name="75Ω Line"
          points={line75}
          fill="#e74c3c"
          tooltip={{ visible: true }}
        />
        <SmithchartSeriesDirective
          name="100Ω Line"
          points={line100}
          fill="#2ecc71"
          tooltip={{ visible: true }}
        />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

### Combining Tooltips with Markers

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective, Inject, TooltipRender } from '@syncfusion/ej2-react-charts';

function App() {
  const rfData = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.2, reactance: 0.15 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 0.8, reactance: 0.4 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      title={{ text: 'RF Circuit S-Parameters' }}
    >
      <Inject services={[TooltipRender]} />
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective
          name="S11 Parameters"
          points={rfData}
          fill="#9b59b6"
          width={2}
          marker={{
            visible: true,
            width: 10,
            height: 10,
            shape: 'Diamond',
            fill: '#9b59b6',
            border: { width: 2, color: '#8e44ad' }
          }}
          tooltip={{ visible: true }}
        />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

### Selective Tooltip Usage

Enable tooltips only for series that need them:

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective, Inject, TooltipRender, SmithchartLegend } from '@syncfusion/ej2-react-charts';

function App() {
  const primaryData = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  const referenceData = [
    { resistance: 0, reactance: 0 },
    { resistance: 1.0, reactance: 0 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      title={{ text: 'Impedance Data with Reference' }}
      legendSettings={{ visible: true }}
    >
      <Inject services={[TooltipRender, SmithchartLegend]} />
      <SmithchartSeriesCollectionDirective>
        {/* Primary data: Tooltips enabled */}
        <SmithchartSeriesDirective
          name="Measured Impedance"
          points={primaryData}
          fill="#3498db"
          width={2}
          marker={{ visible: true }}
          tooltip={{ visible: true }}
        />
        
        {/* Reference line: No tooltips needed */}
        <SmithchartSeriesDirective
          name="Reference Line"
          points={referenceData}
          fill="#95a5a6"
          width={1}
          opacity={0.5}
          tooltip={{ visible: false }}
        />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

## Best Practices

### When to Enable Tooltips

1. **Data exploration interfaces** - Users actively investigate data
2. **Dense visualizations** - Many overlapping data points
3. **Secondary information** - Values are helpful but not primary focus
4. **Interactive dashboards** - Mouse interaction is standard
5. **Comparison tasks** - Users compare values across series

### Tooltip vs Data Labels

| Scenario | Use Tooltips | Use Data Labels |
|----------|--------------|-----------------|
| Few data points (<5) | Optional | Recommended |
| Many data points (>10) | Recommended | Avoid |
| Static reports/PDFs | No | Yes |
| Interactive web apps | Yes | Optional |
| Mobile apps | Conditional | Recommended |
| Critical exact values | No | Yes |
| Space-constrained charts | Yes | No |

### Module Injection

Always remember to inject the `TooltipRender` module:

```tsx
<Inject services={[TooltipRender]} />
```

Without this injection, tooltips will not work even if `visible: true` is set.

### Performance Considerations

- Tooltips have minimal performance impact
- They render on-demand (only on hover)
- No additional rendering overhead when not displayed
- Safe to enable for all series if interaction is desired

### Accessibility Considerations

**Important:** Tooltips rely on mouse hover, which creates accessibility challenges:

- Screen readers cannot access hover-only content
- Keyboard navigation doesn't trigger hover states
- Touch devices may require tap-and-hold or special gestures

**Solutions:**
1. Provide data labels as alternative for critical information
2. Include data table or text summary for screen reader users
3. Use ARIA labels on markers for accessibility
4. Consider click-to-show tooltips for keyboard/touch users

## Common Patterns

### Dynamic Tooltip Control

Allow users to toggle tooltips on/off:

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective, Inject, TooltipRender } from '@syncfusion/ej2-react-charts';

function App() {
  const [showTooltips, setShowTooltips] = React.useState(true);

  const data = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <div>
      <label>
        <input
          type="checkbox"
          checked={showTooltips}
          onChange={(e) => setShowTooltips(e.target.checked)}
        />
        Show Tooltips
      </label>

      <SmithchartComponent id="smithchart">
        <Inject services={[TooltipRender]} />
        <SmithchartSeriesCollectionDirective>
          <SmithchartSeriesDirective
            name="Data Series"
            points={data}
            tooltip={{ visible: showTooltips }}
          />
        </SmithchartSeriesCollectionDirective>
      </SmithchartComponent>
    </div>
  );
}
```

### Conditional Tooltips Based on Data

Enable tooltips only for specific data series:

```tsx
function App() {
  const seriesConfigs = [
    { name: "Primary", data: data1, showTooltip: true },
    { name: "Secondary", data: data2, showTooltip: true },
    { name: "Reference", data: data3, showTooltip: false }
  ];

  return (
    <SmithchartComponent id="smithchart">
      <Inject services={[TooltipRender]} />
      <SmithchartSeriesCollectionDirective>
        {seriesConfigs.map((config, index) => (
          <SmithchartSeriesDirective
            key={index}
            name={config.name}
            points={config.data}
            tooltip={{ visible: config.showTooltip }}
          />
        ))}
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}
```

### Tooltips with All Features

Complete example with markers, legend, and tooltips:

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective, Inject, TooltipRender, SmithchartLegend } from '@syncfusion/ej2-react-charts';

function App() {
  const impedanceData = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.2, reactance: 0.15 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 0.8, reactance: 0.4 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      title={{ text: 'Complete Interactive Smith Chart' }}
      legendSettings={{
        visible: true,
        position: 'Bottom',
        toggleVisibility: true
      }}
    >
      <Inject services={[TooltipRender, SmithchartLegend]} />
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective
          name="Impedance Measurements"
          points={impedanceData}
          fill="#3498db"
          width={2}
          marker={{
            visible: true,
            width: 10,
            height: 10,
            shape: 'Circle',
            fill: '#3498db',
            border: { width: 2, color: '#2980b9' }
          }}
          tooltip={{ visible: true }}
        />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

## Troubleshooting

### Tooltips Not Appearing

**Check these common issues:**

1. **Module not injected:**
   ```tsx
   <Inject services={[TooltipRender]} />  // Required!
   ```

2. **Tooltip not enabled:**
   ```tsx
   tooltip={{ visible: true }}  // Must be true
   ```

3. **Mouse events disabled** - Check if CSS or other code prevents mouse events

4. **Markers too small** - Increase marker size for easier hover targeting

5. **Browser compatibility** - Test in different browsers

### Tooltip Performance

If experiencing performance issues:

- Reduce the number of data points (consider data sampling)
- Limit the number of series with tooltips enabled
- Check for JavaScript errors in console
- Ensure React component isn't re-rendering excessively

This comprehensive guide covers all aspects of tooltip configuration in Smith Charts, enabling you to create interactive, user-friendly visualizations for transmission line and impedance analysis.
