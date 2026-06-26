# Value Bar in React Bullet Chart

The value bar (also called actual bar or feature bar) displays the primary data or current value being measured in the Bullet Chart. This guide covers how to configure and customize the value bar appearance.

## Table of contents

- [Overview](#overview)
- [Displaying the Value Bar](#displaying-the-value-bar)
- [Types of Actual Bar](#types-of-actual-bar)
- [Actual Bar Customization](#actual-bar-customization)
- [Dynamic Color from Data Source](#dynamic-color-from-data-source)
- [Complete Customization Example](#complete-customization-example)
- [Common Patterns](#common-patterns)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

The value bar represents the **Feature Measure** - the actual or current value of the data being measured. It should be encoded as a bar to make it easily distinguishable from the target marker.

## Displaying the Value Bar

To display the actual bar, map the `valueField` property to the appropriate field from your data source.

### Basic Example

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
            valueField="value"     // Maps to the 'value' property
            targetField="target"
            minimum={0}
            maximum={300}
            interval={50}
        />
    );
}
```

The chart will display a horizontal bar representing the value `270`.

## Types of Actual Bar

The shape of the actual bar can be customized using the `type` property. The Bullet Chart supports two shapes:

### Available Types

- **`Rect`** (Default): Rectangular bar shape
- **`Dot`**: Circular dot shape

### Rect Type (Default)

The default rectangular shape provides a clear visual representation:

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    type="Rect"           // Rectangular bar (default)
    minimum={0}
    maximum={300}
/>
```

### Dot Type

Display the actual value as a circular dot:

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    type="Dot"            // Circular dot shape
    minimum={0}
    maximum={300}
/>
```

**When to use Dot:**
- When you want a more compact visualization
- To emphasize the exact point value
- For minimalist dashboard designs

## Actual Bar Customization

### Border Customization

Use the `valueBorder` property to customize the border appearance of the actual bar.

#### Border Color and Width

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    valueBorder={{
        color: "#424242",      // Border color
        width: 2               // Border width in pixels
    }}
    minimum={0}
    maximum={300}
/>
```

#### Complete Border Example

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
            title="Sales Performance"
            valueBorder={{
                color: "#000000",
                width: 3
            }}
            minimum={0}
            maximum={300}
            interval={50}
        />
    );
}
```

### Fill Color Customization

Customize the fill color and height of the actual bar using `valueFill` and `valueHeight` properties.

#### Static Fill Color

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    valueFill="#5B5FC7"        // Purple fill color
    minimum={0}
    maximum={300}
/>
```

#### Height Customization

Control the thickness of the value bar:

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    valueHeight={15}           // Bar height in pixels
    minimum={0}
    maximum={300}
/>
```

#### Combined Fill and Height

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
            title="Revenue Target"
            valueFill="#4CAF50"      // Green color
            valueHeight={20}         // Thicker bar
            minimum={0}
            maximum={300}
            interval={50}
        />
    );
}
```

## Dynamic Color from Data Source

You can bind the fill color directly from your data source, allowing different values to have different colors.

### Data Structure with Color

```tsx
const data = [
    { 
        value: 270, 
        target: 250,
        color: "#5B5FC7"       // Color stored in data
    }
];

<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    valueFill="color"          // Binds to the 'color' property
    minimum={0}
    maximum={300}
/>
```

### Multiple Items with Different Colors

```tsx
import { BulletChartComponent } from "@syncfusion/ej2-react-charts";

function App() {
    const metrics = [
        { 
            value: 270, 
            target: 250, 
            color: "#4CAF50",     // Green (exceeding target)
            name: "Product A" 
        },
        { 
            value: 180, 
            target: 250, 
            color: "#F44336",     // Red (below target)
            name: "Product B" 
        },
        { 
            value: 245, 
            target: 250, 
            color: "#FFC107",     // Yellow (near target)
            name: "Product C" 
        }
    ];

    return (
        <div>
            {metrics.map((metric, index) => (
                <div key={index} style={{ marginBottom: '20px' }}>
                    <BulletChartComponent
                        id={`chart-${index}`}
                        dataSource={[metric]}
                        valueField="value"
                        targetField="target"
                        valueFill="color"
                        title={metric.name}
                        minimum={0}
                        maximum={300}
                        height="80px"
                    />
                </div>
            ))}
        </div>
    );
}
```

## Complete Customization Example

Combining all customization options:

```tsx
import { 
    BulletChartComponent,
    BulletRangeCollectionDirective,
    BulletRangeDirective
} from "@syncfusion/ej2-react-charts";

function App() {
    const data = [
        { 
            value: 270, 
            target: 250,
            barColor: "#5B5FC7"
        }
    ];

    return (
        <BulletChartComponent
            id="bulletChart"
            dataSource={data}
            valueField="value"
            targetField="target"
            title="Quarterly Revenue"
            subtitle="Q1 2024"
            
            // Value bar customization
            type="Rect"                    // Bar shape
            valueFill="barColor"           // Color from data
            valueHeight={18}               // Bar thickness
            valueBorder={{                 // Border styling
                color: "#424242",
                width: 2
            }}
            
            minimum={0}
            maximum={300}
            interval={50}
            width="80%"
            height="100px"
        >
            <BulletRangeCollectionDirective>
                <BulletRangeDirective end={150} color="#E74C3C" />
                <BulletRangeDirective end={250} color="#F39C12" />
                <BulletRangeDirective end={300} color="#27AE60" />
            </BulletRangeCollectionDirective>
        </BulletChartComponent>
    );
}

export default App;
```

## Common Patterns

### Conditional Color Based on Performance

```tsx
function App() {
    const data = [
        { value: 270, target: 250 }
    ];

    // Determine color based on whether target is met
    const barColor = data[0].value >= data[0].target ? "#4CAF50" : "#F44336";

    return (
        <BulletChartComponent
            dataSource={data}
            valueField="value"
            targetField="target"
            valueFill={barColor}
            minimum={0}
            maximum={300}
        />
    );
}
```

### Thin Bar for Compact Dashboards

```tsx
<BulletChartComponent
    dataSource={data}
    valueField="value"
    targetField="target"
    valueHeight={8}              // Thin bar
    height="60px"                // Compact height
    width="100%"
/>
```

### Emphasized Bar with Border

```tsx
<BulletChartComponent
    dataSource={data}
    valueField="value"
    targetField="target"
    valueFill="#2196F3"
    valueHeight={20}
    valueBorder={{
        color: "#1976D2",
        width: 3
    }}
/>
```

### Dot Style for Precision Display

```tsx
<BulletChartComponent
    dataSource={data}
    valueField="value"
    targetField="target"
    type="Dot"                   // Use dot instead of bar
    valueFill="#9C27B0"
    minimum={0}
    maximum={300}
/>
```

## Best Practices

### Choosing Bar Type
- **Use Rect** for general purpose visualizations and when showing ranges
- **Use Dot** for precise point values and minimalist designs

### Color Selection
- Use **green** (#4CAF50) for values exceeding targets
- Use **yellow/orange** (#FFC107) for values near targets
- Use **red** (#F44336) for values below targets
- Ensure sufficient contrast with background and ranges

### Bar Height
- **8-12px**: Compact dashboards with multiple charts
- **15-20px**: Standard single chart displays
- **20-25px**: Emphasis on primary metrics

### Border Usage
- Add borders when multiple bars might overlap visually
- Use darker borders for improved definition
- Keep border width 1-3px for optimal appearance

## Troubleshooting

**Issue: Value bar not visible**
- Verify `valueField` matches a property in your data
- Check that the value is within `minimum` and `maximum` range
- Ensure `valueFill` color contrasts with the background

**Issue: Bar appears too small/large**
- Adjust `valueHeight` property for appropriate thickness
- Check chart `height` property for sufficient space
- Verify `minimum` and `maximum` provide appropriate scale

**Issue: Color not applying**
- When binding from data, ensure property name matches exactly
- Check that color values are valid CSS colors (hex, rgb, color names)
- Verify the data property exists in your data objects

**Issue: Border not showing**
- Increase `valueBorder.width` to at least 2 for visibility
- Ensure border color contrasts with bar fill color
- Check that `valueBorder` object has both `color` and `width` properties

**Issue: Dot type not visible**
- Increase chart dimensions to accommodate the dot
- Adjust `valueFill` to a more visible color
- Verify the value is within the scale range

## API Reference

Relevant properties and events for working with the value bar (see full reference: [references/api.md](references/api.md))

- `valueField: string` — Field name in `dataSource` used for the actual/feature value shown by the value bar.
- `valueFill: string | string[]` — Color value or data-field name to use as the fill for the value bar.
- `valueHeight: number` — Height (thickness) of the value bar in pixels.
- `valueBorder: { color?: string; width?: number }` — Border settings for the value bar.
- `type: 'Rect' | 'Dot'` — Shape of the value bar.
- `createSvg(): void` — Method to (re)create the chart SVG; can be called via component ref.
- `destroy(): void` — Method to clean up the component and listeners.
- `tooltipRender(args)` — Event fired before tooltip content is shown; useful to customize tooltip text for the value bar.
- `bulletChartMouseClick(args)` — Event fired on mouse click; `args.data` contains the data point with the `valueField`.

