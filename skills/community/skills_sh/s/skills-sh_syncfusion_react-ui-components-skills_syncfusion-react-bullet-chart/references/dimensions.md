# Bullet Chart Dimensions in React Bullet Chart

This guide covers how to control the size and dimensions of the Bullet Chart component using container sizing, direct sizing, and responsive techniques.

## Table of contents

- [Overview](#overview)
- [Container Size Configuration](#container-size-configuration)
- [Direct Component Sizing](#direct-component-sizing)
- [Pixel Sizing](#pixel-sizing)
- [Percentage Sizing](#percentage-sizing)
- [Default Size Behavior](#default-size-behavior)
- [Common Sizing Patterns](#common-sizing-patterns)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

The Bullet Chart's size can be controlled in two ways:
1. **Container-based**: Chart inherits size from its parent container
2. **Direct sizing**: Use `width` and `height` properties on the component

## Container Size Configuration

The Bullet Chart can be sized by its parent container element using inline styles or CSS.

### Inline Styles

```tsx
import { BulletChartComponent } from "@syncfusion/ej2-react-charts";

function App() {
    const data = [
        { value: 270, target: 250 }
    ];

    return (
        <div style={{ width: '650px', height: '350px' }}>
            <BulletChartComponent
                id="bulletChart"
                dataSource={data}
                valueField="value"
                targetField="target"
                minimum={0}
                maximum={300}
            />
        </div>
    );
}
```

The chart will fill the entire 650px × 350px container.

### CSS Styling

```tsx
// In your CSS file
.chart-container {
    width: 650px;
    height: 350px;
}

// In your component
function App() {
    return (
        <div className="chart-container">
            <BulletChartComponent
                id="bulletChart"
                dataSource={data}
                valueField="value"
                targetField="target"
                minimum={0}
                maximum={300}
            />
        </div>
    );
}
```

## Direct Component Sizing

Use the `width` and `height` properties directly on the BulletChartComponent.

### Basic Width and Height

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    width="650px"
    height="350px"
    minimum={0}
    maximum={300}
/>
```

## Pixel Sizing

Set explicit pixel dimensions for fixed-size charts.

### Fixed Pixel Values

```tsx
import { BulletChartComponent } from "@syncfusion/ej2-react-charts";

function App() {
    const data = [
        { value: 270, target: 250 }
    ];

    return (
        <BulletChartComponent
            id="bulletChart"
            dataSource={data}
            valueField="value"
            targetField="target"
            title="Revenue Performance"
            width="600px"              // Fixed 600 pixels wide
            height="100px"             // Fixed 100 pixels tall
            minimum={0}
            maximum={300}
            interval={50}
        />
    );
}
```

### When to Use Pixel Sizing

- **Fixed layouts**: When chart position and size are predetermined
- **Print layouts**: For consistent sizing in reports
- **Specific designs**: When exact dimensions are required
- **Non-responsive**: Desktop-only applications

## Percentage Sizing

Use percentage values for responsive layouts that adapt to container size.

### Percentage Width and Height

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    width="100%"               // Full container width
    height="50%"               // Half container height
    minimum={0}
    maximum={300}
/>
```

### Responsive Example

```tsx
import { BulletChartComponent } from "@syncfusion/ej2-react-charts";

function App() {
    const data = [
        { value: 270, target: 250 }
    ];

    return (
        <div style={{ width: '100%', height: '400px' }}>
            <BulletChartComponent
                id="bulletChart"
                dataSource={data}
                valueField="value"
                targetField="target"
                title="Performance Metric"
                width="100%"           // Responsive width
                height="100px"         // Fixed height for consistency
                minimum={0}
                maximum={300}
                interval={50}
            />
        </div>
    );
}
```

The chart width will adjust based on the container or viewport size.

### When to Use Percentage Sizing

- **Responsive layouts**: Adapting to different screen sizes
- **Dashboards**: Flexible grid layouts
- **Mobile apps**: Supporting various device widths
- **Dynamic containers**: Parent elements with changing sizes

## Default Size Behavior

If no size is specified, the Bullet Chart uses default dimensions:

- **Height**: 126px
- **Width**: Full width of the parent container (or window if no container)

### Default Size Example

```tsx
// No width or height specified
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    minimum={0}
    maximum={300}
/>
// Chart will be 126px tall and fill available width
```

## Common Sizing Patterns

### Compact Dashboard Card

```tsx
<BulletChartComponent
    width="100%"
    height="80px"              // Compact height
    minimum={0}
    maximum={300}
/>
```

### Standard Single Metric

```tsx
<BulletChartComponent
    width="600px"
    height="120px"             // Standard height
    minimum={0}
    maximum={300}
/>
```

### Full-Width Responsive

```tsx
<BulletChartComponent
    width="100%"
    height="100px"
    minimum={0}
    maximum={300}
/>
```

### Multiple Metrics Stack

```tsx
function App() {
    const metrics = [
        { value: 270, target: 250, name: "Revenue" },
        { value: 180, target: 200, name: "Profit" },
        { value: 220, target: 210, name: "Sales" }
    ];

    return (
        <div style={{ width: '100%' }}>
            {metrics.map((metric, index) => (
                <div key={index} style={{ marginBottom: '15px' }}>
                    <BulletChartComponent
                        id={`chart-${index}`}
                        dataSource={[metric]}
                        valueField="value"
                        targetField="target"
                        title={metric.name}
                        width="100%"           // Responsive
                        height="80px"          // Consistent height
                        minimum={0}
                        maximum={300}
                    />
                </div>
            ))}
        </div>
    );
}
```

### Large Dashboard Display

```tsx
<BulletChartComponent
    width="900px"
    height="150px"             // Larger for visibility
    minimum={0}
    maximum={300}
/>
```

## Complete Responsive Example

```tsx
import { 
    BulletChartComponent,
    BulletRangeCollectionDirective,
    BulletRangeDirective
} from "@syncfusion/ej2-react-charts";

function App() {
    const data = [
        { value: 270, target: 250 }
    ];

    return (
        <div style={{ 
            width: '100%', 
            maxWidth: '800px', 
            margin: '0 auto',
            padding: '20px' 
        }}>
            <BulletChartComponent
                id="bulletChart"
                dataSource={data}
                valueField="value"
                targetField="target"
                title="Quarterly Revenue"
                subtitle="Q1 2024"
                
                // Responsive dimensions
                width="100%"               // Adapts to container
                height="120px"             // Fixed for consistency
                
                minimum={0}
                maximum={300}
                interval={50}
                valueFill="#5B5FC7"
                valueHeight={18}
                targetColor="#424242"
            >
                <BulletRangeCollectionDirective>
                    <BulletRangeDirective end={150} color="#E74C3C" opacity={0.3} />
                    <BulletRangeDirective end={250} color="#F39C12" opacity={0.3} />
                    <BulletRangeDirective end={300} color="#27AE60" opacity={0.3} />
                </BulletRangeCollectionDirective>
            </BulletChartComponent>
        </div>
    );
}
```

## Best Practices

### Height Guidelines
- **60-80px**: Compact dashboard cards, multiple metrics
- **100-120px**: Standard single metric display (recommended)
- **140-160px**: Large displays, emphasis metrics
- **Never below 50px**: Chart elements become illegible

### Width Guidelines
- **Minimum 300px**: Ensure axis labels don't overlap
- **400-600px**: Comfortable single metric width
- **100% responsive**: Best for most dashboard layouts
- **Consider mobile**: Test at 320px width minimum

### Responsive Strategy
- Use **percentage width** (100%) for flexible layouts
- Use **pixel height** for consistent vertical rhythm
- Set **max-width** on containers to prevent excessive stretching
- Test across **multiple screen sizes**

### Container vs Direct Sizing
- **Container sizing**: Better for complex layouts with multiple elements
- **Direct sizing**: Simpler, more explicit control
- **Combination**: Container width (%), direct height (px) works well

## Troubleshooting

**Issue: Chart too small**
- Check container has explicit dimensions if using container sizing
- Increase width and height values
- Verify parent elements don't have height: 0 or width: 0
- Use browser inspector to check computed dimensions

**Issue: Chart too large**
- Reduce width and height values
- Add max-width constraint on container
- Check for unintended 100% width on large containers
- Verify no CSS overrides

**Issue: Chart not responsive**
- Use percentage for width instead of pixels
- Ensure parent container is responsive
- Check for fixed-width ancestors
- Test window resize behavior

**Issue: Labels cut off**
- Increase chart height
- Reduce label font size
- Adjust title position
- Increase chart width if horizontal labels overlap

**Issue: Chart overflowing container**
- Verify width/height don't exceed container
- Check for box-sizing issues (add box-sizing: border-box)
- Look for padding/margin on chart or container
- Use width: 100% instead of fixed pixels

**Issue: Height not applying**
- Ensure height value includes units ("100px" not "100")
- Check parent container has explicit height if using percentages
- Verify no CSS overrides with !important
- Use browser inspector to check computed height

**Issue: Inconsistent sizing across browsers**
- Always include units (px, %, em)
- Set explicit box-sizing: border-box
- Avoid relying on default dimensions
- Test in multiple browsers during development
