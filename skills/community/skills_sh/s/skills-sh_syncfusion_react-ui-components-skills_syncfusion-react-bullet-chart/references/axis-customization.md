# Axis Customization in React Bullet Chart

## Table of Contents
- [Overview](#overview)
- [Tick Lines Customization](#tick-lines-customization)
  - [Major Tick Lines](#major-tick-lines)
  - [Minor Tick Lines](#minor-tick-lines)
  - [Using Range Colors](#using-range-colors)
- [Tick Placement](#tick-placement)
- [Label Formatting](#label-formatting)
  - [Standard Formats](#standard-formats)
  - [Format Table](#format-table)
- [Group Separator](#group-separator)
- [Custom Label Format](#custom-label-format)
- [Label Placement](#label-placement)
- [Opposed Position](#opposed-position)
- [Category Labels](#category-labels)
- [Category Label Customization](#category-label-customization)
- [Complete Examples](#complete-examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

The Bullet Chart axis provides various customization options including tick marks, labels, formatting, and positioning. These customizations help tailor the chart to match your specific design and data requirements.

## Tick Lines Customization

Tick lines are the small marks on the axis that indicate scale divisions. The Bullet Chart supports both major and minor tick lines.

### Major Tick Lines

Major tick lines appear at the main axis intervals. Customize them using the `majorTickLines` property.

**Available Properties:**
- **width**: Tick line thickness
- **height**: Tick line length
- **color**: Tick line color
- **useRangeColor**: Use colors from ranges

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
            minimum={0}
            maximum={300}
            interval={50}
            majorTickLines={{
                width: 2,              // Line thickness
                height: 15,            // Line length
                color: "#424242"       // Dark gray
            }}
        />
    );
}
```

### Minor Tick Lines

Minor tick lines appear between major tick marks. Customize them using the `minorTickLines` property.

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    minimum={0}
    maximum={300}
    interval={50}
    minorTicksPerInterval={4}    // Number of minor ticks between major ticks
    minorTickLines={{
        width: 1,                  // Thinner than major
        height: 8,                 // Shorter than major
        color: "#757575"           // Lighter gray
    }}
/>
```

### Using Range Colors

Set `useRangeColor` to `true` to make tick lines inherit colors from the corresponding range.

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
            minimum={0}
            maximum={300}
            interval={50}
            majorTickLines={{
                width: 2,
                height: 15,
                useRangeColor: true    // Ticks match range colors
            }}
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

## Tick Placement

The `tickPosition` property controls whether ticks appear inside or outside the ranges.

### Outside Placement (Default)

```tsx
<BulletChartComponent
    tickPosition="Outside"      // Ticks outside the chart
    minimum={0}
    maximum={300}
/>
```

### Inside Placement

```tsx
<BulletChartComponent
    tickPosition="Inside"       // Ticks inside the chart
    minimum={0}
    maximum={300}
/>
```

## Label Formatting

Use the `labelFormat` property to format axis labels with various number formats.

### Standard Formats

```tsx
// Number format with 1 decimal place
<BulletChartComponent
    labelFormat="n1"           // 1000.0
    minimum={0}
    maximum={3000}
/>

// Percentage format with 1 decimal place
<BulletChartComponent
    labelFormat="p1"           // 1.0%
    minimum={0}
    maximum={1}
/>

// Currency format with 2 decimal places
<BulletChartComponent
    labelFormat="c2"           // $1000.00
    minimum={0}
    maximum={5000}
/>
```

### Format Table

| Label Value | Format | Result | Description |
|-------------|--------|--------|-------------|
| 1000 | n1 | 1000.0 | Number rounded to 1 decimal place |
| 1000 | n2 | 1000.00 | Number rounded to 2 decimal places |
| 1000 | n3 | 1000.000 | Number rounded to 3 decimal places |
| 0.01 | p1 | 1.0% | Converted to percentage with 1 decimal |
| 0.01 | p2 | 1.00% | Converted to percentage with 2 decimals |
| 0.01 | p3 | 1.000% | Converted to percentage with 3 decimals |
| 1000 | c1 | $1000.0 | Currency with 1 decimal place |
| 1000 | c2 | $1000.00 | Currency with 2 decimal places |

### Complete Format Example

```tsx
import { BulletChartComponent } from "@syncfusion/ej2-react-charts";

function App() {
    const data = [
        { value: 1270, target: 1250 }
    ];

    return (
        <BulletChartComponent
            id="bulletChart"
            dataSource={data}
            valueField="value"
            targetField="target"
            title="Revenue"
            labelFormat="c2"           // Currency format: $1000.00
            minimum={0}
            maximum={2000}
            interval={500}
        />
    );
}
```

## Group Separator

Enable `enableGroupSeparator` to add thousand separators to axis labels.

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    enableGroupSeparator={true}    // 1,000 instead of 1000
    minimum={0}
    maximum={100000}
    interval={20000}
/>
```

**Example Output:**
- Without separator: `20000`, `40000`, `60000`
- With separator: `20,000`, `40,000`, `60,000`

## Custom Label Format

Use the `${value}` placeholder to create custom label formats.

### Basic Custom Format

```tsx
// Append 'K' for thousands
<BulletChartComponent
    labelFormat="${value}K"    // 100K, 200K, 300K
    minimum={0}
    maximum={300}
/>
```

### Currency with Custom Suffix

```tsx
// Custom currency format
<BulletChartComponent
    labelFormat="$${value}K"   // $100K, $200K, $300K
    minimum={0}
    maximum={300}
/>
```

### Complete Custom Format Example

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
            title="Sales (in thousands)"
            labelFormat="${value}K"    // 50K, 100K, 150K, etc.
            minimum={0}
            maximum={300}
            interval={50}
        />
    );
}
```

## Label Placement

The `labelPosition` property controls whether labels appear inside or outside the ranges.

### Outside Placement (Default)

```tsx
<BulletChartComponent
    labelPosition="Outside"    // Labels outside ranges
    minimum={0}
    maximum={300}
/>
```

### Inside Placement

```tsx
<BulletChartComponent
    labelPosition="Inside"     // Labels inside ranges
    minimum={0}
    maximum={300}
/>
```

## Opposed Position

Set `opposedPosition` to `true` to place the axis on the opposite side.

### Standard Position

```tsx
<BulletChartComponent
    opposedPosition={false}    // Default position
    minimum={0}
    maximum={300}
/>
```

### Opposed Position

```tsx
<BulletChartComponent
    opposedPosition={true}     // Opposite side
    minimum={0}
    maximum={300}
/>
```

**Use Cases:**
- Mirrored chart layouts
- Comparing two related metrics side-by-side
- Alternative dashboard designs

## Category Labels

Use the `categoryField` property to display X-axis labels from your data.

### Basic Category Labels

```tsx
import { BulletChartComponent } from "@syncfusion/ej2-react-charts";

function App() {
    const data = [
        { value: 270, target: 250, category: "Product A" },
        { value: 180, target: 200, category: "Product B" },
        { value: 220, target: 210, category: "Product C" }
    ];

    return (
        <BulletChartComponent
            id="bulletChart"
            dataSource={data}
            valueField="value"
            targetField="target"
            categoryField="category"    // Display category from data
            minimum={0}
            maximum={300}
        />
    );
}
```

The chart will display "Product A", "Product B", "Product C" as category labels.

## Category Label Customization

Customize category and axis labels using `categoryLabelStyle` and `labelStyle`.

### Category Label Style

```tsx
<BulletChartComponent
    categoryField="category"
    categoryLabelStyle={{
        color: "#2C3E50",
        size: "14px",
        fontFamily: "Arial, sans-serif",
        fontWeight: "600"
    }}
    minimum={0}
    maximum={300}
/>
```

### Axis Label Style

```tsx
<BulletChartComponent
    labelStyle={{
        color: "#757575",
        size: "12px",
        fontFamily: "Arial, sans-serif",
        fontWeight: "normal"
    }}
    minimum={0}
    maximum={300}
/>
```

### Using Range Colors for Labels

```tsx
<BulletChartComponent
    categoryLabelStyle={{
        useRangeColor: true,      // Category labels match range colors
        size: "14px",
        fontWeight: "600"
    }}
    labelStyle={{
        useRangeColor: true,      // Axis labels match range colors
        size: "12px"
    }}
/>
```

### Complete Label Customization Example

```tsx
import { 
    BulletChartComponent,
    BulletRangeCollectionDirective,
    BulletRangeDirective
} from "@syncfusion/ej2-react-charts";

function App() {
    const data = [
        { value: 270, target: 250, category: "Q1 Revenue" }
    ];

    return (
        <BulletChartComponent
            id="bulletChart"
            dataSource={data}
            valueField="value"
            targetField="target"
            categoryField="category"
            
            // Category label styling
            categoryLabelStyle={{
                color: "#2C3E50",
                size: "14px",
                fontFamily: "Segoe UI, Arial, sans-serif",
                fontWeight: "600"
            }}
            
            // Axis label styling
            labelStyle={{
                color: "#757575",
                size: "11px",
                fontFamily: "Segoe UI, Arial, sans-serif",
                fontWeight: "normal"
            }}
            
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

## Complete Examples

### Fully Customized Axis

```tsx
import { 
    BulletChartComponent,
    BulletRangeCollectionDirective,
    BulletRangeDirective
} from "@syncfusion/ej2-react-charts";

function App() {
    const data = [
        { value: 27000, target: 25000 }
    ];

    return (
        <BulletChartComponent
            id="bulletChart"
            dataSource={data}
            valueField="value"
            targetField="target"
            title="Annual Revenue"
            
            // Axis configuration
            minimum={0}
            maximum={40000}
            interval={10000}
            labelFormat="${value}"
            enableGroupSeparator={true}
            
            // Tick customization
            majorTickLines={{
                width: 2,
                height: 12,
                color: "#424242"
            }}
            minorTicksPerInterval={4}
            minorTickLines={{
                width: 1,
                height: 6,
                color: "#757575"
            }}
            tickPosition="Outside"
            
            // Label customization
            labelPosition="Outside"
            labelStyle={{
                color: "#424242",
                size: "11px",
                fontFamily: "Arial, sans-serif"
            }}
            
            width="90%"
            height="120px"
        >
            <BulletRangeCollectionDirective>
                <BulletRangeDirective end={15000} color="#E74C3C" opacity={0.3} />
                <BulletRangeDirective end={30000} color="#F39C12" opacity={0.3} />
                <BulletRangeDirective end={40000} color="#27AE60" opacity={0.3} />
            </BulletRangeCollectionDirective>
        </BulletChartComponent>
    );
}
```

## Best Practices

### Tick Lines
- **Major ticks**: 1.5-2px width, 10-15px height
- **Minor ticks**: 1px width, 6-8px height (50-60% of major tick height)
- Use **useRangeColor** for visually integrated designs
- Place ticks **outside** for clarity, **inside** for compact layouts

### Label Formatting
- Choose format based on data type: **n** for numbers, **p** for percentages, **c** for currency
- Use **custom formats** with ${value} for branded metrics
- Enable **group separators** for large numbers (>10,000)
- Keep decimal places minimal (0-2) for readability

### Label Styling
- Use **readable font sizes**: 10-12px for axis labels
- Keep **sufficient contrast** with background
- Use **consistent fonts** across all charts
- **Category labels** should be slightly larger/bolder than axis labels

### Positioning
- **Default** (outside, non-opposed) works for most cases
- Use **opposed position** for comparative layouts only
- **Inside** placement saves space but may reduce readability

## Troubleshooting

**Issue: Tick lines not visible**
- Increase tick width (2-3px minimum)
- Increase tick height (10-15px for major)
- Ensure tick color contrasts with background
- Check that tick properties are correctly nested

**Issue: Labels overlapping**
- Increase interval value
- Reduce label font size
- Use shorter label format (n0 instead of n2)
- Increase chart width
- Enable group separator for better spacing

**Issue: Label format not applying**
- Verify format string is correct (n1, p2, c1, etc.)
- Check for typos in labelFormat property
- Ensure format matches data type (don't use p1 for large numbers)
- Use ${value} for custom formats

**Issue: Custom format not showing**
- Ensure ${value} placeholder is used
- Check for proper escaping in template strings
- Verify labelFormat is a string, not an object
- Test with simple format first: "${value}"

**Issue: Group separator not working**
- Verify enableGroupSeparator is set to true (boolean, not string)
- Check that numbers are large enough to have separators (>999)
- Ensure labelFormat doesn't override separator

**Issue: Category labels not displaying**
- Verify categoryField property matches data property name exactly
- Check that data objects contain the category property
- Ensure chart has sufficient height for labels
- Verify categoryLabelStyle isn't hiding labels (check opacity, color)

**Issue: useRangeColor not working**
- Ensure ranges are defined with BulletRangeCollectionDirective
- Verify useRangeColor is true (boolean)
- Check that ranges have valid color values
- Tick/label positions must overlap with ranges to inherit colors
