# Data Labels in React Bullet Chart

Data labels identify the value of the actual bar in the Bullet Chart component, providing at-a-glance value information without requiring user interaction.

## Table of contents

- [Overview](#overview)
- [Enabling Data Labels](#enabling-data-labels)
- [Complete Basic Example](#complete-basic-example)
- [Data Label Customization](#data-label-customization)
- [Complete Customization](#complete-customization)
- [Common Patterns](#common-patterns)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

Data labels display the actual bar's value directly on the chart, making it easy to read exact values without hovering or interacting with the chart. They are particularly useful for static reports, printed materials, or when precise values are critical.

## Enabling Data Labels

Data labels are disabled by default. Enable them by setting the `enable` property to `true` in the `dataLabel` configuration.

### Basic Data Label

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
            title="Revenue"
            minimum={0}
            maximum={300}
            dataLabel={{ enable: true }}
        />
    );
}
```

The value `270` will be displayed as a label on or near the actual bar.

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
            dataLabel={{ enable: true }}
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

## Data Label Customization

Use the `labelStyle` property within `dataLabel` to customize the appearance of data labels.

### Available Style Properties

- **color**: Text color
- **opacity**: Transparency (0-1)
- **size**: Font size
- **fontFamily**: Font typeface
- **fontWeight**: Font weight (normal, bold, etc.)
- **fontStyle**: Font style (normal, italic, oblique)

### Color and Size

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    dataLabel={{
        enable: true,
        labelStyle: {
            color: "#FFFFFF",      // White text
            size: "14px"           // Font size
        }
    }}
    minimum={0}
    maximum={300}
/>
```

### Font Weight and Style

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    dataLabel={{
        enable: true,
        labelStyle: {
            color: "#333333",
            size: "13px",
            fontWeight: "bold",     // Bold text
            fontStyle: "normal"     // Normal style
        }
    }}
    minimum={0}
    maximum={300}
/>
```

### Complete Customization

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
            title="Quarterly Revenue"
            minimum={0}
            maximum={300}
            interval={50}
            dataLabel={{
                enable: true,
                labelStyle: {
                    color: "#2C3E50",                    // Dark blue-gray
                    opacity: 1,                          // Fully opaque
                    size: "14px",                        // Medium size
                    fontFamily: "Arial, sans-serif",     // Arial font
                    fontWeight: "600",                   // Semi-bold
                    fontStyle: "normal"                  // Normal style
                }
            }}
        />
    );
}
```

## Complete Styled Example

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
            title="Sales Target Achievement"
            subtitle="Q1 2024"
            
            // Chart styling
            valueFill="#5B5FC7"
            valueHeight={18}
            targetColor="#424242"
            targetWidth={5}
            
            // Data label configuration
            dataLabel={{
                enable: true,
                labelStyle: {
                    color: "#FFFFFF",                // White text
                    size: "13px",
                    fontFamily: "Segoe UI, Arial, sans-serif",
                    fontWeight: "bold",
                    opacity: 1
                }
            }}
            
            minimum={0}
            maximum={300}
            interval={50}
            width="90%"
            height="120px"
        >
            <BulletRangeCollectionDirective>
                <BulletRangeDirective end={150} color="#E74C3C" opacity={0.3} />
                <BulletRangeDirective end={250} color="#F39C12" opacity={0.3} />
                <BulletRangeDirective end={300} color="#27AE60" opacity={0.3} />
            </BulletRangeCollectionDirective>
        </BulletChartComponent>
    );
}

export default App;
```

## Common Patterns

### High Contrast Labels

For dark value bars, use light text:
```tsx
dataLabel={{
    enable: true,
    labelStyle: {
        color: "#FFFFFF",          // White text
        fontWeight: "bold",
        size: "14px"
    }
}}
```

For light value bars, use dark text:
```tsx
dataLabel={{
    enable: true,
    labelStyle: {
        color: "#333333",          // Dark text
        fontWeight: "600",
        size: "14px"
    }
}}
```

### Subtle Labels

For minimalist designs:
```tsx
dataLabel={{
    enable: true,
    labelStyle: {
        color: "#757575",          // Medium gray
        size: "12px",
        fontWeight: "normal",
        opacity: 0.8
    }
}}
```

### Emphasized Labels

For important metrics:
```tsx
dataLabel={{
    enable: true,
    labelStyle: {
        color: "#2C3E50",
        size: "16px",
        fontWeight: "800",         // Extra bold
        fontFamily: "Arial Black, sans-serif"
    }
}}
```

## Font Weight Options

```tsx
// Numeric values
fontWeight: "300"     // Light
fontWeight: "400"     // Normal
fontWeight: "500"     // Medium
fontWeight: "600"     // Semi-bold
fontWeight: "700"     // Bold
fontWeight: "800"     // Extra bold

// Named values
fontWeight: "normal"  // 400
fontWeight: "bold"    // 700
```

## Font Style Options

```tsx
fontStyle: "normal"   // Default
fontStyle: "italic"   // Slanted text
fontStyle: "oblique"  // Slanted text (similar to italic)
```

## Best Practices

### When to Use Data Labels
- **Enable** for static displays, reports, and presentations
- **Enable** when exact values are critical
- **Disable** for interactive dashboards with tooltips
- **Disable** when space is limited or labels overlap

### Text Visibility
- Use **high contrast** between label and value bar
- **White text** on dark bars (#FFFFFF)
- **Dark text** on light bars (#333333, #2C3E50)
- Ensure **4.5:1 minimum contrast ratio** for accessibility

### Font Size
- **11-12px**: Compact charts, multiple metrics
- **13-14px**: Standard single metric (recommended)
- **15-16px**: Emphasized primary KPIs
- **17px+**: Dashboard headers, hero metrics

### Font Weight
- **400-500**: Subtle, minimalist designs
- **600**: Recommended for general use (readable, not overwhelming)
- **700-800**: Emphasized metrics, bold statements

### Typography
- Use **sans-serif fonts** for better readability at small sizes
- Stick to **system fonts** (Arial, Segoe UI, Helvetica) for consistency
- Avoid **decorative fonts** that reduce legibility

## Troubleshooting

**Issue: Data labels not showing**
- Verify `dataLabel.enable` is set to `true`
- Check that `dataLabel` object is properly configured
- Ensure chart has sufficient height for labels to display
- Verify value is within minimum and maximum range

**Issue: Labels are cut off**
- Increase chart height and width
- Reduce label font size
- Adjust chart margins if available
- Use shorter number formats

**Issue: Labels hard to read**
- Increase contrast between label color and value bar color
- Use white text on dark bars, dark text on light bars
- Increase font size if too small
- Add font-weight: bold for better visibility

**Issue: Label color not applying**
- Ensure color value is valid CSS color (hex, rgb, color name)
- Check property is `color` not `fill` in labelStyle
- Verify labelStyle object is nested correctly in dataLabel
- Use quotes for color values: `color: "#FFFFFF"`

**Issue: Font styling not working**
- Verify property names are exact: `fontWeight`, `fontFamily`, `fontStyle`
- Use quotes for all string values
- Check font family is available in the system
- Include fallback fonts: `fontFamily: "Arial, sans-serif"`

**Issue: Labels overlap with chart elements**
- Reduce font size
- Adjust value bar height to accommodate labels
- Consider using tooltips instead of persistent labels
- Increase chart dimensions

**Issue: Opacity not visible**
- Ensure opacity value is between 0 and 1
- Check that opacity is reducing visibility (1 = opaque, 0 = transparent)
- Verify sufficient contrast even with reduced opacity
- Test with solid opacity: 1 first
