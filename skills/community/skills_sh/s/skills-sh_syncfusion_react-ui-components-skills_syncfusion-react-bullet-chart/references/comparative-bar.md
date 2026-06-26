# Comparative Bar in React Bullet Chart

The comparative bar (also called target bar or target marker) is a line marker that runs perpendicular to the orientation of the chart. It serves as a target or comparison point against the feature measure value.

## Table of contents

- [Overview](#overview)
- [Displaying the Target Bar](#displaying-the-target-bar)
- [Types of Target Bar](#types-of-target-bar)
- [Target Bar Customization](#target-bar-customization)
- [Dynamic Color from Data Source](#dynamic-color-from-data-source)
- [Complete Example with Value and Target Customization](#complete-example-with-value-and-target-customization)
- [Common Patterns](#common-patterns)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

The comparative bar represents the **Comparative Measure** - a target, goal, or benchmark value to compare against the actual value. It appears as a perpendicular marker on the chart.

## Displaying the Target Bar

To display the target bar, map the `targetField` property to the appropriate field from your data source.

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
            valueField="value"
            targetField="target"    // Maps to the 'target' property
            minimum={0}
            maximum={300}
            interval={50}
        />
    );
}
```

The chart will display a perpendicular marker at position `250`, representing the target value.

## Types of Target Bar

The shape of the target bar can be customized using the `targetTypes` property. The Bullet Chart supports three shapes:

### Available Types

- **`Rect`** (Default): Rectangular/bar marker
- **`Circle`**: Circular marker
- **`Cross`**: Cross/X-shaped marker

### Rect Type (Default)

The default rectangular marker provides a clear line:

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    targetTypes={["Rect"]}      // Rectangular marker (default)
    minimum={0}
    maximum={300}
/>
```

### Circle Type

Display the target as a circular marker:

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    targetTypes={["Circle"]}    // Circular marker
    minimum={0}
    maximum={300}
/>
```

**When to use Circle:**
- To create visual distinction from rectangular value bars
- For modern, rounded design aesthetics
- When emphasizing the target point precisely

### Cross Type

Display the target as a cross marker:

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    targetTypes={["Cross"]}     // Cross-shaped marker
    minimum={0}
    maximum={300}
/>
```

**When to use Cross:**
- To indicate critical target points
- For technical or engineering visualizations
- When comparing multiple targets with different markers

### Complete Type Example

```tsx
import { BulletChartComponent } from "@syncfusion/ej2-react-charts";

function App() {
    const data = [
        { value: 270, target: 250 }
    ];

    return (
        <div>
            <h3>Rect Target</h3>
            <BulletChartComponent
                id="chart1"
                dataSource={data}
                valueField="value"
                targetField="target"
                targetTypes={["Rect"]}
                title="Rectangular Target"
                minimum={0}
                maximum={300}
            />

            <h3>Circle Target</h3>
            <BulletChartComponent
                id="chart2"
                dataSource={data}
                valueField="value"
                targetField="target"
                targetTypes={["Circle"]}
                title="Circular Target"
                minimum={0}
                maximum={300}
            />

            <h3>Cross Target</h3>
            <BulletChartComponent
                id="chart3"
                dataSource={data}
                valueField="value"
                targetField="target"
                targetTypes={["Cross"]}
                title="Cross Target"
                minimum={0}
                maximum={300}
            />
        </div>
    );
}
```

## Target Bar Customization

### Target Color

Customize the fill color of the target bar using the `targetColor` property.

#### Static Target Color

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    targetColor="#646464"       // Dark gray target
    minimum={0}
    maximum={300}
/>
```

#### Complete Color Example

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
            title="Sales vs Target"
            targetColor="#E74C3C"      // Red target marker
            targetTypes={["Rect"]}
            minimum={0}
            maximum={300}
            interval={50}
        />
    );
}
```

### Target Width

Control the width (or thickness) of the target bar using the `targetWidth` property.

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    targetWidth={5}              // Width in pixels
    minimum={0}
    maximum={300}
/>
```

**Width Guidelines:**
- **3-5px**: Standard visibility
- **6-8px**: Emphasized targets
- **10+px**: Prominent critical targets

### Combined Customization

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
            title="Quarterly Performance"
            
            // Target customization
            targetTypes={["Circle"]}
            targetColor="#2196F3"       // Blue target
            targetWidth={8}             // Thicker marker
            
            minimum={0}
            maximum={300}
            interval={50}
            width="80%"
            height="100px"
        />
    );
}
```

## Dynamic Color from Data Source

Bind the target color directly from your data source for dynamic styling.

### Data Structure with Target Color

```tsx
const data = [
    { 
        value: 270, 
        target: 250,
        targetColor: "#646464"    // Target color in data
    }
];

<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    targetColor="targetColor"     // Binds to the 'targetColor' property
    minimum={0}
    maximum={300}
/>
```

### Multiple Charts with Different Target Colors

```tsx
import { BulletChartComponent } from "@syncfusion/ej2-react-charts";

function App() {
    const metrics = [
        { 
            value: 270, 
            target: 250, 
            targetColor: "#4CAF50",   // Green (target met)
            name: "Revenue" 
        },
        { 
            value: 180, 
            target: 250, 
            targetColor: "#F44336",   // Red (target missed)
            name: "Profit" 
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
                        targetColor="targetColor"
                        title={metric.name}
                        minimum={0}
                        maximum={300}
                    />
                </div>
            ))}
        </div>
    );
}
```

## Complete Example with Value and Target Customization

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
            valueColor: "#5B5FC7",
            targetColor: "#424242"
        }
    ];

    return (
        <BulletChartComponent
            id="bulletChart"
            dataSource={data}
            valueField="value"
            targetField="target"
            title="Q1 Performance"
            subtitle="Revenue in thousands"
            
            // Value bar customization
            valueFill="valueColor"
            valueHeight={18}
            
            // Target bar customization
            targetTypes={["Circle"]}
            targetColor="targetColor"
            targetWidth={7}
            
            minimum={0}
            maximum={300}
            interval={50}
            width="90%"
            height="120px"
        >
            <BulletRangeCollectionDirective>
                <BulletRangeDirective end={150} color="#FFE5E5" />
                <BulletRangeDirective end={250} color="#FFF4E5" />
                <BulletRangeDirective end={300} color="#E5F5E5" />
            </BulletRangeCollectionDirective>
        </BulletChartComponent>
    );
}

export default App;
```

## Common Patterns

### Conditional Target Styling

```tsx
function App() {
    const data = [
        { value: 270, target: 250 }
    ];

    // Style target based on whether it was met
    const targetColor = data[0].value >= data[0].target 
        ? "#4CAF50"   // Green if target met
        : "#F44336";  // Red if target missed

    return (
        <BulletChartComponent
            dataSource={data}
            valueField="value"
            targetField="target"
            targetColor={targetColor}
            targetWidth={6}
            minimum={0}
            maximum={300}
        />
    );
}
```

### Multiple Target Types for Comparison

```tsx
// Create multiple charts with different target markers for visual distinction
const goals = [
    { value: 270, target: 250, type: ["Rect"], label: "Primary Goal" },
    { value: 270, target: 280, type: ["Circle"], label: "Stretch Goal" },
    { value: 270, target: 220, type: ["Cross"], label: "Minimum Goal" }
];

<div>
    {goals.map((goal, index) => (
        <BulletChartComponent
            key={index}
            dataSource={[goal]}
            valueField="value"
            targetField="target"
            targetTypes={goal.type}
            title={goal.label}
            minimum={0}
            maximum={300}
        />
    ))}
</div>
```

### Emphasized Target Marker

```tsx
<BulletChartComponent
    dataSource={data}
    valueField="value"
    targetField="target"
    targetTypes={["Circle"]}
    targetColor="#FF5722"        // Bright orange
    targetWidth={10}             // Large marker
    minimum={0}
    maximum={300}
/>
```

## Best Practices

### Choosing Target Type
- **Rect**: Traditional, clear for horizontal/vertical comparisons
- **Circle**: Modern look, good for point values
- **Cross**: Technical feel, useful for critical thresholds

### Color Selection
- Use **contrasting colors** that stand out from value bar and ranges
- **Neutral colors** (gray, black) work well for standard targets
- **Red/orange** for critical or missed targets
- **Green** for achieved or exceeded targets

### Target Width
- **3-5px**: Standard charts, multiple metrics
- **6-8px**: Single prominent metric
- **10+px**: Dashboard headers, key performance indicators

### Visibility
- Ensure target marker is clearly visible against ranges
- Use sufficient width for small chart sizes
- Test visibility on different backgrounds and themes

## Troubleshooting

**Issue: Target bar not visible**
- Verify `targetField` matches a property in your data
- Check that target value is within `minimum` and `maximum` range
- Increase `targetWidth` for better visibility
- Ensure `targetColor` contrasts with background and ranges

**Issue: Target appears in wrong position**
- Verify target value in data is correct
- Check that `minimum` and `maximum` provide appropriate scale
- Ensure `targetField` property name matches data exactly

**Issue: Target type not changing**
- Ensure `targetTypes` is an array: `["Circle"]` not `"Circle"`
- Check import includes necessary chart modules
- Verify property name is `targetTypes` (plural) not `targetType`

**Issue: Color not applying**
- When binding from data, ensure property name matches exactly
- Check that color values are valid CSS colors
- Verify the data property exists in data objects

**Issue: Target too thick/thin**
- Adjust `targetWidth` property (recommended: 3-10px)
- For Circle/Cross types, width affects the marker size
- Test different widths based on chart dimensions
