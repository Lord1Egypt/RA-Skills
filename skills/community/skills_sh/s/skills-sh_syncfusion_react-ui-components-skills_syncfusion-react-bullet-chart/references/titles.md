# Titles and Subtitles in React Bullet Chart

## Table of Contents
- [Overview](#overview)
- [Adding a Title](#adding-a-title)
- [Adding a Subtitle](#adding-a-subtitle)
- [Title Positioning](#title-positioning)
  - [Top Position (Default)](#top-position-default)
  - [Bottom Position](#bottom-position)
  - [Left Position](#left-position)
  - [Right Position](#right-position)
- [Title Customization](#title-customization)
- [Subtitle Customization](#subtitle-customization)
- [Complete Examples](#complete-examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

Titles and subtitles provide context and information about the data plotted in the Bullet Chart. The title displays primary information, while the subtitle shows additional descriptive text.

## Adding a Title

Use the `title` property to display information about the chart's data.

### Basic Title

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
            minimum={0}
            maximum={300}
        />
    );
}
```

The title "Revenue Performance" will appear on the chart.

## Adding a Subtitle

Use the `subtitle` property to show additional information about the data.

### Basic Subtitle

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    title="Revenue Performance"
    subtitle="Q1 2024 - In Thousands"
    minimum={0}
    maximum={300}
/>
```

### Complete Title and Subtitle Example

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
            subtitle="January - March 2024"
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
```

## Title Positioning

The `titlePosition` property controls where the title and subtitle appear relative to the chart. Available positions: **Top**, **Bottom**, **Left**, **Right**.

### Top Position (Default)

By default, title and subtitle appear at the top of the chart.

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    title="Revenue"
    subtitle="Q1 2024"
    titlePosition="Top"      // Default position
    minimum={0}
    maximum={300}
/>
```

**When to use Top:**
- Standard dashboard layouts
- Traditional chart presentations
- When chart is the primary focus below the title

### Bottom Position

Display title and subtitle at the bottom of the chart.

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    title="Revenue"
    subtitle="Q1 2024"
    titlePosition="Bottom"
    minimum={0}
    maximum={300}
/>
```

**When to use Bottom:**
- Chart-first presentations where data is more important
- When grouping multiple charts with bottom labels
- Footer-style annotations

### Left Position

Display title and subtitle on the left side of the chart.

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    title="Revenue"
    subtitle="Q1 2024"
    titlePosition="Left"
    minimum={0}
    maximum={300}
/>
```

**When to use Left:**
- Vertical stacking of multiple bullet charts
- KPI dashboards with left-aligned labels
- Space-efficient layouts

**Complete Left Position Example:**
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
            subtitle="In thousands"
            titlePosition="Left"
            minimum={0}
            maximum={300}
            interval={50}
            width="600px"
            height="100px"
        />
    );
}
```

### Right Position

Display title and subtitle on the right side of the chart.

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    title="Revenue"
    subtitle="Q1 2024"
    titlePosition="Right"
    minimum={0}
    maximum={300}
/>
```

**When to use Right:**
- RTL (right-to-left) layouts
- Alternative dashboard designs
- When charts are aligned to the left edge

**Complete Right Position Example:**
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
            subtitle="Q1 2024"
            titlePosition="Right"
            minimum={0}
            maximum={300}
            interval={50}
            width="600px"
            height="100px"
        />
    );
}
```

## Title Customization

Use the `titleStyle` property to customize the title's appearance.

### Available Style Properties

- **color**: Text color
- **opacity**: Transparency (0-1)
- **size**: Font size
- **fontFamily**: Font typeface
- **fontWeight**: Font weight (normal, bold, etc.)
- **fontStyle**: Font style (normal, italic, oblique)

### Basic Title Styling

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    title="Revenue Performance"
    titleStyle={{
        color: "#424242",
        size: "18px",
        fontWeight: "bold"
    }}
    minimum={0}
    maximum={300}
/>
```

### Complete Title Style Example

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
            titleStyle={{
                color: "#2C3E50",
                opacity: 1,
                size: "20px",
                fontFamily: "Arial, sans-serif",
                fontWeight: "bold",
                fontStyle: "normal"
            }}
            minimum={0}
            maximum={300}
            interval={50}
        />
    );
}
```

### Font Weight Options

```tsx
// Light weight
titleStyle={{ fontWeight: "300" }}

// Normal weight (default)
titleStyle={{ fontWeight: "normal" }}

// Bold weight
titleStyle={{ fontWeight: "bold" }}

// Extra bold
titleStyle={{ fontWeight: "800" }}
```

### Font Style Options

```tsx
// Normal (default)
titleStyle={{ fontStyle: "normal" }}

// Italic
titleStyle={{ fontStyle: "italic" }}

// Oblique
titleStyle={{ fontStyle: "oblique" }}
```

## Subtitle Customization

Use the `subtitleStyle` property to customize the subtitle's appearance.

### Basic Subtitle Styling

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    title="Revenue"
    subtitle="Q1 2024"
    subtitleStyle={{
        color: "#757575",
        size: "14px",
        fontStyle: "italic"
    }}
    minimum={0}
    maximum={300}
/>
```

### Complete Subtitle Style Example

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
            subtitle="January - March 2024"
            subtitleStyle={{
                color: "#616161",
                opacity: 0.9,
                size: "12px",
                fontFamily: "Arial, sans-serif",
                fontWeight: "normal",
                fontStyle: "italic"
            }}
            minimum={0}
            maximum={300}
            interval={50}
        />
    );
}
```

## Complete Examples

### Professional Dashboard Style

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
            
            // Title configuration
            title="Quarterly Revenue"
            titlePosition="Top"
            titleStyle={{
                color: "#2C3E50",
                size: "18px",
                fontFamily: "Segoe UI, Arial, sans-serif",
                fontWeight: "600"
            }}
            
            // Subtitle configuration
            subtitle="Q1 2024 - In Thousands USD"
            subtitleStyle={{
                color: "#7F8C8D",
                size: "12px",
                fontFamily: "Segoe UI, Arial, sans-serif",
                fontWeight: "normal",
                fontStyle: "italic"
            }}
            
            minimum={0}
            maximum={300}
            interval={50}
            width="90%"
            height="120px"
        >
            <BulletRangeCollectionDirective>
                <BulletRangeDirective end={150} color="#E74C3C" opacity={0.4} />
                <BulletRangeDirective end={250} color="#F39C12" opacity={0.4} />
                <BulletRangeDirective end={300} color="#27AE60" opacity={0.4} />
            </BulletRangeCollectionDirective>
        </BulletChartComponent>
    );
}
```

### Left-Aligned KPI Dashboard

```tsx
import { BulletChartComponent } from "@syncfusion/ej2-react-charts";

function App() {
    const metrics = [
        { value: 270, target: 250, name: "Revenue", unit: "K USD" },
        { value: 85, target: 100, name: "Profit", unit: "K USD" },
        { value: 180, target: 150, name: "Sales", unit: "Units" }
    ];

    return (
        <div style={{ padding: '20px' }}>
            {metrics.map((metric, index) => (
                <div key={index} style={{ marginBottom: '15px' }}>
                    <BulletChartComponent
                        id={`chart-${index}`}
                        dataSource={[metric]}
                        valueField="value"
                        targetField="target"
                        title={metric.name}
                        subtitle={metric.unit}
                        titlePosition="Left"
                        titleStyle={{
                            color: "#34495E",
                            size: "16px",
                            fontWeight: "600"
                        }}
                        subtitleStyle={{
                            color: "#95A5A6",
                            size: "11px"
                        }}
                        minimum={0}
                        maximum={300}
                        width="100%"
                        height="80px"
                    />
                </div>
            ))}
        </div>
    );
}
```

### Minimalist Design

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    title="Performance"
    titlePosition="Top"
    titleStyle={{
        color: "#333333",
        size: "14px",
        fontWeight: "500",
        fontFamily: "Helvetica, sans-serif"
    }}
    minimum={0}
    maximum={300}
    width="100%"
    height="60px"
/>
```

## Best Practices

### Title Text
- Keep titles concise (2-5 words)
- Use descriptive, meaningful text
- Avoid abbreviations unless widely known
- Use title case or sentence case consistently

### Subtitle Text
- Provide context: time period, units, qualifiers
- Keep under 10 words
- Use for supplementary information only

### Position Selection
- **Top**: Most readable, traditional choice
- **Left**: Best for vertical lists of charts
- **Bottom**: Use sparingly, less conventional
- **Right**: Primarily for RTL layouts

### Font Styling
- **Title**: Larger (16-20px), bold or semi-bold
- **Subtitle**: Smaller (11-14px), normal or light weight
- **Contrast**: Ensure sufficient color contrast with background
- **Consistency**: Use same fonts across dashboard

### Color Coordination
- Title: Use dark, high-contrast colors (#2C3E50, #333333)
- Subtitle: Use medium gray tones (#757575, #95A5A6)
- Maintain 4.5:1 contrast ratio for accessibility

## Troubleshooting

**Issue: Title not displaying**
- Verify `title` property has a non-empty string value
- Check that chart has sufficient height for title
- Ensure title color contrasts with background

**Issue: Title cut off or overlapping**
- Increase chart width or height
- Reduce title font size
- Use shorter title text
- Adjust `titlePosition` for better fit

**Issue: Subtitle not visible**
- Verify `subtitle` property is set
- Check subtitle color isn't same as background
- Increase chart dimensions if truncated
- Ensure subtitle font size is readable

**Issue: Title positioning not working**
- Verify `titlePosition` value is one of: "Top", "Bottom", "Left", "Right"
- Check for typos (case-sensitive)
- Ensure chart has sufficient dimensions for chosen position

**Issue: Custom fonts not applying**
- Verify font family is installed or available
- Use fallback fonts: `fontFamily: "CustomFont, Arial, sans-serif"`
- Check for typos in font family name

**Issue: Title/subtitle style not changing**
- Ensure style properties are in correct object: `titleStyle={{}}` or `subtitleStyle={{}}`
- Check property names match exactly (case-sensitive)
- Verify color values are valid CSS colors
- Use quotes for size values: `size: "16px"` not `size: 16px`
