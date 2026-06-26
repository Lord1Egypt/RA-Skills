# Dimensions and Sizing

## Table of contents
- [Overview](dimensions-and-sizing.md#overview)
- [Container-Based Sizing](dimensions-and-sizing.md#container-based-sizing)
  - [Using Inline Styles](dimensions-and-sizing.md#using-inline-styles)
  - [Using CSS Classes](dimensions-and-sizing.md#using-css-classes)
  - [Responsive Container Sizing](dimensions-and-sizing.md#responsive-container-sizing)
- [Pixel-Based Sizing](dimensions-and-sizing.md#pixel-based-sizing)
  - [Basic Pixel Sizing](dimensions-and-sizing.md#basic-pixel-sizing)
  - [Standard Size Presets](dimensions-and-sizing.md#standard-size-presets)
  - [Dynamic Pixel Sizing](dimensions-and-sizing.md#dynamic-pixel-sizing)
- [Percentage-Based Sizing](dimensions-and-sizing.md#percentage-based-sizing)
  - [Basic Percentage Sizing](dimensions-and-sizing.md#basic-percentage-sizing)
  - [Partial Percentage Sizing](dimensions-and-sizing.md#partial-percentage-sizing)
  - [Responsive Grid Layout](dimensions-and-sizing.md#responsive-grid-layout)
- [Choosing the Right Approach](dimensions-and-sizing.md#choosing-the-right-approach)
  - [Use Container-Based Sizing When](dimensions-and-sizing.md#use-container-based-sizing-when)
  - [Use Pixel-Based Sizing When](dimensions-and-sizing.md#use-pixel-based-sizing-when)
  - [Use Percentage-Based Sizing When](dimensions-and-sizing.md#use-percentage-based-sizing-when)
- [Complete Examples](dimensions-and-sizing.md#complete-examples)
  - [Full-Screen Chart](dimensions-and-sizing.md#full-screen-chart)
  - [Dashboard Card Layout](dimensions-and-sizing.md#dashboard-card-layout)
  - [Responsive Multi-Chart View](dimensions-and-sizing.md#responsive-multi-chart-view)
  - [Window Resize Handler](dimensions-and-sizing.md#window-resize-handler)
- [Best Practices](dimensions-and-sizing.md#best-practices)
  - [Aspect Ratio](dimensions-and-sizing.md#aspect-ratio)
  - [Minimum Dimensions](dimensions-and-sizing.md#minimum-dimensions)
  - [Maximum Dimensions](dimensions-and-sizing.md#maximum-dimensions)
  - [Mobile Considerations](dimensions-and-sizing.md#mobile-considerations)
  - [Print-Friendly Sizing](dimensions-and-sizing.md#print-friendly-sizing)

## Overview

You can render the Smith Chart with dimensions that correspond to its container size or specify exact dimensions using the `width` and `height` properties. Smith Charts support three primary sizing approaches: container-based, pixel-based, and percentage-based sizing.

## Container-Based Sizing

Render the Smith Chart to match its container's size by specifying the container's dimensions using inline styles or CSS. The chart will automatically adapt to the container's width and height.

### Using Inline Styles

Define the container size directly in the JSX using the `style` attribute:

```tsx
import * as React from "react";
import { SmithchartComponent, SeriesCollectionDirective, SeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const data = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <div style={{ width: '650px', height: '350px' }}>
      <SmithchartComponent id="smithchart">
        <SmithChartSeriesCollectionDirective>
          <SmithChartSeriesDirective points={data} />
        </SeriesCollectionDirective>
      </SmithchartComponent>
    </div>
  );
}

export default App;
```

### Using CSS Classes

Define container dimensions in CSS for better separation of concerns:

**App.css:**
```css
.smith-chart-container {
  width: 650px;
  height: 350px;
}
```

**App.tsx:**
```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective } from '@syncfusion/ej2-react-charts';
import './App.css';

function App() {
  const data = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <div className="smith-chart-container">
      <SmithchartComponent id="smithchart">
        <SmithchartSeriesCollectionDirective>
          <SmithchartSeriesDirective points={data} />
        </SmithchartSeriesCollectionDirective>
      </SmithchartComponent>
    </div>
  );
}

export default App;
```

### Responsive Container Sizing

Create responsive containers that adapt to viewport size:

**App.css:**
```css
.responsive-container {
  width: 100%;
  max-width: 800px;
  height: 400px;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .responsive-container {
    height: 300px;
  }
}
```

**App.tsx:**
```tsx
import * as React from "react";
import { SmithchartComponent, SeriesCollectionDirective, SeriesDirective } from '@syncfusion/ej2-react-charts';
import './App.css';

function App() {
  const data = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <div className="responsive-container">
      <SmithchartComponent id="smithchart">
        <SmithchartSeriesCollectionDirective>
          <SmithchartSeriesDirective points={data} />
        </SmithchartSeriesCollectionDirective>
      </SmithchartComponent>
    </div>
  );
}

export default App;
```

## Pixel-Based Sizing

Directly set the chart dimensions in pixels using the `width` and `height` properties. This provides precise control over chart size.

### Basic Pixel Sizing

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const data = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <SmithchartComponent
      id="smithchart"
      width="700px"
      height="400px"
    >
      <SmithchartSeriesCollectionDirective>
        <SmithchartSeriesDirective points={data} />
      </SmithchartSeriesCollectionDirective>
    </SmithchartComponent>
  );
}

export default App;
```

### Standard Size Presets

Common chart sizes for different use cases:

**Small (Dashboard tile):**
```tsx
<SmithchartComponent
  id="smithchart"
  width="400px"
  height="300px"
>
  {/* series configuration */}
</SmithchartComponent>
```

**Medium (Standard view):**
```tsx
<SmithchartComponent
  id="smithchart"
  width="700px"
  height="500px"
>
  {/* series configuration */}
</SmithchartComponent>
```

**Large (Detailed analysis):**
```tsx
<SmithchartComponent
  id="smithchart"
  width="1000px"
  height="700px"
>
  {/* series configuration */}
</SmithchartComponent>
```

### Dynamic Pixel Sizing

Adjust chart size based on state or props:

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const [chartSize, setChartSize] = React.useState({ width: '600px', height: '400px' });

  const data = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  const sizes = {
    small: { width: '400px', height: '300px' },
    medium: { width: '600px', height: '400px' },
    large: { width: '800px', height: '600px' }
  };

  return (
    <div>
      <div>
        <button onClick={() => setChartSize(sizes.small)}>Small</button>
        <button onClick={() => setChartSize(sizes.medium)}>Medium</button>
        <button onClick={() => setChartSize(sizes.large)}>Large</button>
      </div>

      <SmithchartComponent
        id="smithchart"
        width={chartSize.width}
        height={chartSize.height}
      >
        <SmithchartSeriesCollectionDirective>
          <SmithchartSeriesDirective points={data} />
        </SmithchartSeriesCollectionDirective>
      </SmithchartComponent>
    </div>
  );
}

export default App;
```

## Percentage-Based Sizing

Specify dimensions as percentages to create responsive charts that scale relative to their container.

### Basic Percentage Sizing

```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const data = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <div style={{ width: '800px', height: '600px' }}>
      <SmithchartComponent
        id="smithchart"
        width="100%"
        height="100%"
      >
        <SmithchartSeriesCollectionDirective>
          <SmithchartSeriesDirective points={data} />
        </SmithchartSeriesCollectionDirective>
      </SmithchartComponent>
    </div>
  );
}

export default App;
```

In this example:
- Chart width: 100% of 800px = 800px
- Chart height: 100% of 600px = 600px

### Partial Percentage Sizing

Use percentages less than 100% to size the chart relative to its container:

```tsx
<div style={{ width: '1000px', height: '700px', border: '1px solid #ccc' }}>
  <SmithchartComponent
    id="smithchart"
    width="80%"   {/* 80% of 1000px = 800px */}
    height="75%"  {/* 75% of 700px = 525px */}
  >
    <SmithchartSeriesCollectionDirective>
      <SmithchartSeriesDirective points={data} />
    </SmithchartSeriesCollectionDirective>
  </SmithchartComponent>
</div>
```

### Responsive Grid Layout

Use percentage sizing with CSS Grid or Flexbox:

**App.css:**
```css
.chart-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  padding: 20px;
}

.chart-cell {
  border: 1px solid #ddd;
  padding: 10px;
  height: 400px;
}
```

**App.tsx:**
```tsx
import * as React from "react";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective } from '@syncfusion/ej2-react-charts';
import './App.css';

function App() {
  const data1 = [{ resistance: 0, reactance: 0.05 }, { resistance: 1.0, reactance: 0.5 }];
  const data2 = [{ resistance: 0.2, reactance: 0.1 }, { resistance: 1.2, reactance: 0.6 }];

  return (
    <div className="chart-grid">
      <div className="chart-cell">
        <SmithchartComponent id="chart1" width="100%" height="100%">
          <SmithchartSeriesCollectionDirective>
            <SmithchartSeriesDirective name="Chart 1" points={data1} />
          </SmithchartSeriesCollectionDirective>
        </SmithchartComponent>
      </div>
      
      <div className="chart-cell">
        <SmithchartComponent id="chart2" width="100%" height="100%">
          <SmithchartSeriesCollectionDirective>
            <SmithchartSeriesDirective name="Chart 2" points={data2} />
          </SmithchartSeriesCollectionDirective>
        </SmithchartComponent>
      </div>
    </div>
  );
}

export default App;
```

## Choosing the Right Approach

### Use Container-Based Sizing When:

- Building responsive layouts
- Chart size should adapt to viewport changes
- Working with CSS frameworks (Bootstrap, Material-UI, Tailwind)
- Size determined by parent layout constraints
- Need media queries for different screen sizes

**Advantages:**
- CSS-driven responsiveness
- Easier to maintain with design systems
- Better separation of concerns
- Works well with CSS Grid and Flexbox

### Use Pixel-Based Sizing When:

- Need exact, predictable dimensions
- Creating fixed-size dashboard tiles
- Generating charts for specific print dimensions
- Requirements specify exact pixel measurements
- Chart appears in modals or fixed-size containers

**Advantages:**
- Precise control over dimensions
- Consistent rendering across different contexts
- Predictable layout behavior
- Easier to test and debug

### Use Percentage-Based Sizing When:

- Building fluid, scalable layouts
- Chart should fill variable-sized containers
- Creating multi-chart dashboards
- Supporting multiple screen resolutions
- Chart lives in resizable panels or split views

**Advantages:**
- Automatic scaling with container
- Maintains aspect ratio
- Works well with responsive containers
- Adapts to dynamic layout changes

## Complete Examples

### Full-Screen Chart

```tsx
import * as React from "react";
import { createRoot } from "react-dom/client";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const data = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <div style={{ width: '100vw', height: '100vh', padding: '20px', boxSizing: 'border-box' }}>
      <SmithchartComponent
        id="smithchart"
        width="100%"
        height="100%"
        title={{ text: 'Full-Screen Smith Chart' }}
      >
        <SmithchartSeriesCollectionDirective>
          <SmithchartSeriesDirective points={data} />
        </SmithchartSeriesCollectionDirective>
      </SmithchartComponent>
    </div>
  );
}

export default App;
```

### Dashboard Card Layout

```tsx
import * as React from "react";
import { createRoot } from "react-dom/client";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const data = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  const cardStyle = {
    width: '450px',
    height: '350px',
    border: '1px solid #ddd',
    borderRadius: '8px',
    padding: '15px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
  };

  return (
    <div style={cardStyle}>
      <SmithchartComponent
        id="smithchart"
        width="100%"
        height="100%"
        title={{ text: 'Impedance Analysis' }}
      >
        <SmithchartSeriesCollectionDirective>
          <SmithchartSeriesDirective points={data} />
        </SmithchartSeriesCollectionDirective>
      </SmithchartComponent>
    </div>
  );
}

export default App;
```

### Responsive Multi-Chart View

```tsx
import * as React from "react";
import { createRoot } from "react-dom/client";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SmithchartSeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const data1 = [{ resistance: 0, reactance: 0.05 }, { resistance: 1.0, reactance: 0.5 }];
  const data2 = [{ resistance: 0.2, reactance: 0.1 }, { resistance: 1.2, reactance: 0.6 }];
  const data3 = [{ resistance: 0.3, reactance: 0.15 }, { resistance: 1.3, reactance: 0.65 }];

  const containerStyle = {
    display: 'flex',
    flexWrap: 'wrap' as const,
    gap: '20px',
    padding: '20px'
  };

  const chartBoxStyle = {
    flex: '1 1 calc(50% - 10px)',
    minWidth: '400px',
    height: '350px',
    border: '1px solid #ddd',
    padding: '10px'
  };

  return (
    <div style={containerStyle}>
      <div style={chartBoxStyle}>
        <SmithchartComponent id="chart1" width="100%" height="100%" title={{ text: 'Chart 1' }}>
          <SmithchartSeriesCollectionDirective>
            <SmithchartSeriesDirective points={data1} />
          </SmithchartSeriesCollectionDirective>
        </SmithchartComponent>
      </div>

      <div style={chartBoxStyle}>
        <SmithchartComponent id="chart2" width="100%" height="100%" title={{ text: 'Chart 2' }}>
          <SmithchartSeriesCollectionDirective>
            <SmithchartSeriesDirective points={data2} />
          </SmithchartSeriesCollectionDirective>
        </SmithchartComponent>
      </div>

      <div style={chartBoxStyle}>
        <SmithchartComponent id="chart3" width="100%" height="100%" title={{ text: 'Chart 3' }}>
          <SmithchartSeriesCollectionDirective>
            <SmithchartSeriesDirective points={data3} />
          </SmithchartSeriesCollectionDirective>
        </SmithchartComponent>
      </div>
    </div>
  );
}

export default App;
```

### Window Resize Handler

Dynamic sizing based on window dimensions:

```tsx
import * as React from "react";
import { createRoot } from "react-dom/client";
import { SmithchartComponent, SmithchartSeriesCollectionDirective, SeriesDirective } from '@syncfusion/ej2-react-charts';

function App() {
  const [dimensions, setDimensions] = React.useState({
    width: window.innerWidth * 0.8,
    height: window.innerHeight * 0.6
  });

  React.useEffect(() => {
    const handleResize = () => {
      setDimensions({
        width: window.innerWidth * 0.8,
        height: window.innerHeight * 0.6
      });
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const data = [
    { resistance: 0, reactance: 0.05 },
    { resistance: 0.5, reactance: 0.3 },
    { resistance: 1.0, reactance: 0.5 }
  ];

  return (
    <div style={{ padding: '20px' }}>
      <SmithchartComponent
        id="smithchart"
        width={`${dimensions.width}px`}
        height={`${dimensions.height}px`}
        title={{ text: 'Resizable Smith Chart' }}
      >
        <SmithchartSeriesCollectionDirective>
          <SmithchartSeriesDirective points={data} />
        </SmithchartSeriesCollectionDirective>
      </SmithchartComponent>
    </div>
  );
}

export default App;
```

## Best Practices

### Aspect Ratio

Smith Charts work best with aspect ratios close to 4:3 or 16:9:

- **4:3 ratio**: 800×600, 640×480, 1024×768
- **16:9 ratio**: 800×450, 1280×720, 1600×900
- **Square**: 600×600, 800×800 (also acceptable)

### Minimum Dimensions

Maintain minimum dimensions for readability:

- **Minimum width**: 400px (smaller reduces readability)
- **Minimum height**: 300px (smaller compromises axis labels)
- **Recommended minimum**: 500×400px for optimal viewing

### Maximum Dimensions

Consider practical limits:

- **Maximum width**: 2000px (larger may reduce performance)
- **Maximum height**: 1500px (chart detail doesn't scale indefinitely)
- **Recommended maximum**: 1200×900px for most use cases

### Mobile Considerations

For mobile devices:

```css
.smith-chart-mobile {
  width: 100%;
  height: 300px;
  max-width: 500px;
}
```

### Print-Friendly Sizing

For print layouts, use pixel sizing:

```tsx
<SmithchartComponent
  id="print-chart"
  width="700px"   // Standard print width
  height="525px"  // 4:3 aspect ratio
>
  {/* series configuration */}
</SmithchartComponent>
```

This comprehensive guide covers all sizing approaches for Smith Charts, enabling you to create charts that work perfectly in any layout or device context.
