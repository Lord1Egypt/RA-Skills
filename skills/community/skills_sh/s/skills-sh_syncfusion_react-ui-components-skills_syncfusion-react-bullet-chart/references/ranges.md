# Ranges in React Bullet Chart

Ranges represent qualitative bands in the Bullet Chart, such as **Good**, **Bad**, and **Satisfactory**. They provide visual context by dividing the chart scale into performance levels.

## Table of contents

- [Overview](#overview)
- [Basic Range Configuration](#basic-range-configuration)
- [Range Properties](#range-properties)
- [Color Customization](#color-customization)
- [Opacity Customization](#opacity-customization)
- [Common Range Patterns](#common-range-patterns)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

Ranges are background bands that help interpret the value bar's performance level. Common uses include:
- **Performance levels**: Poor, Average, Good, Excellent
- **Status indicators**: Critical, Warning, Normal
- **Quality bands**: Below Target, Near Target, Above Target

## Basic Range Configuration

### Import Range Directives

First, import the necessary range components:

```tsx
import { 
    BulletChartComponent,
    BulletRangeCollectionDirective,
    BulletRangeDirective
} from "@syncfusion/ej2-react-charts";
```

### Define Ranges

Use `BulletRangeCollectionDirective` as a container and `BulletRangeDirective` for each individual range:

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    minimum={0}
    maximum={300}
>
    <BulletRangeCollectionDirective>
        <BulletRangeDirective end={150} color="red" />
        <BulletRangeDirective end={250} color="yellow" />
        <BulletRangeDirective end={300} color="green" />
    </BulletRangeCollectionDirective>
</BulletChartComponent>
```

## Range Properties

### end Property

The `end` property specifies the ending point of a qualitative range. Each range starts where the previous one ends (or from the `minimum` value for the first range).

**Example:**
```tsx
<BulletRangeCollectionDirective>
    <BulletRangeDirective end={100} />  {/* Range: 0-100 (from minimum) */}
    <BulletRangeDirective end={200} />  {/* Range: 100-200 */}
    <BulletRangeDirective end={300} />  {/* Range: 200-300 */}
</BulletRangeCollectionDirective>
```

**Key Points:**
- First range starts at the `minimum` value
- Each subsequent range starts at the previous range's `end` value
- Last range should typically end at or near the `maximum` value

### Understanding Range Boundaries

```tsx
<BulletChartComponent
    minimum={0}      // Starting point for first range
    maximum={300}
>
    <BulletRangeCollectionDirective>
        <BulletRangeDirective end={150} color="red" />     {/* 0-150 */}
        <BulletRangeDirective end={250} color="yellow" />  {/* 150-250 */}
        <BulletRangeDirective end={300} color="green" />   {/* 250-300 */}
    </BulletRangeCollectionDirective>
</BulletChartComponent>
```

## Complete Basic Example

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
        <BulletChartComponent
            id="bulletChart"
            dataSource={data}
            valueField="value"
            targetField="target"
            title="Sales Performance"
            minimum={0}
            maximum={300}
            interval={50}
        >
            <BulletRangeCollectionDirective>
                <BulletRangeDirective end={150} color="red" />
                <BulletRangeDirective end={250} color="yellow" />
                <BulletRangeDirective end={300} color="green" />
            </BulletRangeCollectionDirective>
        </BulletChartComponent>
    );
}

export default App;
```

## Color Customization

### Using CSS Color Names

```tsx
<BulletRangeCollectionDirective>
    <BulletRangeDirective end={100} color="red" />
    <BulletRangeDirective end={200} color="orange" />
    <BulletRangeDirective end={300} color="green" />
</BulletRangeCollectionDirective>
```

### Using Hex Color Codes

```tsx
<BulletRangeCollectionDirective>
    <BulletRangeDirective end={150} color="#E74C3C" />
    <BulletRangeDirective end={250} color="#F39C12" />
    <BulletRangeDirective end={300} color="#27AE60" />
</BulletRangeCollectionDirective>
```

### Using RGB Values

```tsx
<BulletRangeCollectionDirective>
    <BulletRangeDirective end={100} color="rgb(231, 76, 60)" />
    <BulletRangeDirective end={200} color="rgb(243, 156, 18)" />
    <BulletRangeDirective end={300} color="rgb(39, 174, 96)" />
</BulletRangeCollectionDirective>
```

## Opacity Customization

Control the transparency of ranges using the `opacity` property. Values range from 0 (transparent) to 1 (opaque).

### Basic Opacity

```tsx
<BulletRangeCollectionDirective>
    <BulletRangeDirective end={150} color="red" opacity={0.5} />
    <BulletRangeDirective end={250} color="yellow" opacity={0.5} />
    <BulletRangeDirective end={300} color="green" opacity={0.5} />
</BulletRangeCollectionDirective>
```

### Complete Opacity Example

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
        <BulletChartComponent
            id="bulletChart"
            dataSource={data}
            valueField="value"
            targetField="target"
            title="Performance Metrics"
            minimum={0}
            maximum={300}
            interval={50}
        >
            <BulletRangeCollectionDirective>
                <BulletRangeDirective 
                    end={150} 
                    color="#E74C3C" 
                    opacity={0.3}     // Light red
                />
                <BulletRangeDirective 
                    end={250} 
                    color="#F39C12" 
                    opacity={0.5}     // Medium yellow
                />
                <BulletRangeDirective 
                    end={300} 
                    color="#27AE60" 
                    opacity={0.7}     // Prominent green
                />
            </BulletRangeCollectionDirective>
        </BulletChartComponent>
    );
}
```

## Common Range Patterns

### Three-Level Performance (Poor/Average/Good)

```tsx
<BulletRangeCollectionDirective>
    <BulletRangeDirective end={100} color="#F44336" opacity={0.4} />  {/* Poor */}
    <BulletRangeDirective end={200} color="#FFC107" opacity={0.4} />  {/* Average */}
    <BulletRangeDirective end={300} color="#4CAF50" opacity={0.4} />  {/* Good */}
</BulletRangeCollectionDirective>
```

### Four-Level Quality Scale

```tsx
<BulletRangeCollectionDirective>
    <BulletRangeDirective end={75} color="#D32F2F" />    {/* Critical */}
    <BulletRangeDirective end={150} color="#F57C00" />   {/* Warning */}
    <BulletRangeDirective end={225} color="#FBC02D" />   {/* Acceptable */}
    <BulletRangeDirective end={300} color="#388E3C" />   {/* Excellent */}
</BulletRangeCollectionDirective>
```

### Five-Level Detail Scale

```tsx
<BulletRangeCollectionDirective>
    <BulletRangeDirective end={60} color="#B71C1C" />    {/* Very Poor */}
    <BulletRangeDirective end={120} color="#E65100" />   {/* Poor */}
    <BulletRangeDirective end={180} color="#F9A825" />   {/* Average */}
    <BulletRangeDirective end={240} color="#689F38" />   {/* Good */}
    <BulletRangeDirective end={300} color="#2E7D32" />   {/* Excellent */}
</BulletRangeCollectionDirective>
```

### Percentage-Based Ranges

```tsx
<BulletChartComponent
    minimum={0}
    maximum={100}
    interval={20}
>
    <BulletRangeCollectionDirective>
        <BulletRangeDirective end={50} color="red" />      {/* 0-50% */}
        <BulletRangeDirective end={75} color="yellow" />   {/* 50-75% */}
        <BulletRangeDirective end={100} color="green" />   {/* 75-100% */}
    </BulletRangeCollectionDirective>
</BulletChartComponent>
```

### Subtle Monochrome Ranges

```tsx
<BulletRangeCollectionDirective>
    <BulletRangeDirective end={100} color="#BDBDBD" opacity={0.3} />  {/* Light gray */}
    <BulletRangeDirective end={200} color="#757575" opacity={0.3} />  {/* Medium gray */}
    <BulletRangeDirective end={300} color="#424242" opacity={0.3} />  {/* Dark gray */}
</BulletRangeCollectionDirective>
```

## Best Practices

### Number of Ranges
- **3 ranges**: Simple good/average/poor distinction (most common)
- **4-5 ranges**: More granular performance levels
- **2 ranges**: Binary pass/fail scenarios
- Avoid more than 5 ranges (becomes visually cluttered)

### Color Selection
- **Traditional traffic light**: Red (poor), Yellow (average), Green (good)
- **Professional palette**: Use muted colors with lower opacity
- **Brand colors**: Adapt ranges to match brand guidelines
- **Accessibility**: Ensure sufficient contrast between ranges
- **Color blindness**: Consider patterns or labels for accessibility

### Opacity Guidelines
- **0.2-0.4**: Very subtle background, minimal distraction
- **0.4-0.6**: Standard range visibility (recommended)
- **0.6-0.8**: Emphasized ranges
- **0.8-1.0**: Prominent ranges (use sparingly)

### Range Boundaries
- Set boundaries at logical intervals (50, 100, 150 instead of 47, 93, 187)
- Ensure last range ends at or near maximum value
- Align boundaries with business thresholds or goals

## Complete Styled Example

```tsx
import { 
    BulletChartComponent,
    BulletRangeCollectionDirective,
    BulletRangeDirective,
    BulletTooltip,
    Inject
} from "@syncfusion/ej2-react-charts";

function App() {
    const data = [
        { value: 270, target: 250 }
    ];

    return (
        <div style={{ padding: '20px' }}>
            <BulletChartComponent
                id="bulletChart"
                dataSource={data}
                valueField="value"
                targetField="target"
                title="Quarterly Revenue"
                subtitle="In thousands USD"
                minimum={0}
                maximum={300}
                interval={50}
                valueFill="#5B5FC7"
                valueHeight={18}
                targetColor="#424242"
                targetWidth={5}
                tooltip={{ enable: true }}
                width="90%"
                height="120px"
            >
                <BulletRangeCollectionDirective>
                    <BulletRangeDirective 
                        end={150} 
                        color="#EF5350" 
                        opacity={0.5} 
                    />
                    <BulletRangeDirective 
                        end={250} 
                        color="#FFCA28" 
                        opacity={0.5} 
                    />
                    <BulletRangeDirective 
                        end={300} 
                        color="#66BB6A" 
                        opacity={0.5} 
                    />
                </BulletRangeCollectionDirective>
                <Inject services={[BulletTooltip]} />
            </BulletChartComponent>
        </div>
    );
}

export default App;
```

## Troubleshooting

**Issue: Ranges not visible**
- Verify you've imported `BulletRangeCollectionDirective` and `BulletRangeDirective`
- Check that ranges are wrapped in `<BulletRangeCollectionDirective>`
- Ensure `end` values are within `minimum` and `maximum` bounds
- Try increasing opacity if colors are too subtle

**Issue: Ranges overlap incorrectly**
- Ensure `end` values are in ascending order
- Check that first range starts from `minimum` value
- Verify no gaps between range boundaries

**Issue: Colors not showing**
- Verify color values are valid CSS colors
- Check opacity isn't set to 0
- Ensure colors contrast with chart background

**Issue: Last range doesn't reach maximum**
- Set the last range's `end` value equal to `maximum`
- Verify `maximum` property is correctly set

**Issue: Too many/few ranges displaying**
- Count `BulletRangeDirective` components
- Check for duplicate or missing directives
- Verify each directive has an `end` property
