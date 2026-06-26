# Tooltips in React Bullet Chart

Tooltips display important summary information about the actual and target bar values when the mouse hovers over a bar in the Bullet Chart.

## Table of contents

- [Overview](#overview)
- [Enabling Tooltips](#enabling-tooltips)
- [Default Tooltip](#default-tooltip)
- [Custom Tooltip Template](#custom-tooltip-template)
- [Tooltip Appearance Customization](#tooltip-appearance-customization)
- [Complete Styled Example](#complete-styled-example)
- [Common Patterns](#common-patterns)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

Tooltips provide on-demand information without cluttering the chart. They appear when users hover over the value bar or target marker, showing detailed information about the values.

## Enabling Tooltips

Tooltips are not visible by default. To enable them, you must:
1. Set `enable` to `true` in the `tooltip` configuration
2. Inject the `BulletTooltip` module

### Basic Tooltip Setup

```tsx
import { 
    BulletChartComponent,
    BulletTooltip,
    Inject
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
            title="Revenue"
            minimum={0}
            maximum={300}
            tooltip={{ enable: true }}
        >
            <Inject services={[BulletTooltip]} />
        </BulletChartComponent>
    );
}
```

**Important:** Both the `tooltip={{ enable: true }}` property AND the `<Inject services={[BulletTooltip]} />` component are required.

## Default Tooltip

The default tooltip displays the actual value and target value in a simple format.

### Complete Default Example

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
        <BulletChartComponent
            id="bulletChart"
            dataSource={data}
            valueField="value"
            targetField="target"
            title="Sales Performance"
            minimum={0}
            maximum={300}
            interval={50}
            tooltip={{ enable: true }}
        >
            <BulletRangeCollectionDirective>
                <BulletRangeDirective end={150} color="red" />
                <BulletRangeDirective end={250} color="yellow" />
                <BulletRangeDirective end={300} color="green" />
            </BulletRangeCollectionDirective>
            <Inject services={[BulletTooltip]} />
        </BulletChartComponent>
    );
}

export default App;
```

When you hover over the chart, you'll see a tooltip showing both the value and target.

## Custom Tooltip Template

Use the `template` property to display custom HTML content in the tooltip. You can use placeholders `${value}` and `${target}` to access data from the data source.

### Basic Template

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    tooltip={{
        enable: true,
        template: '<div><b>Actual:</b> ${value}<br/><b>Target:</b> ${target}</div>'
    }}
    minimum={0}
    maximum={300}
>
    <Inject services={[BulletTooltip]} />
</BulletChartComponent>
```

### Styled Template

```tsx
const tooltipTemplate = `
    <div style="padding: 10px; background: #f5f5f5; border: 2px solid #333;">
        <div style="font-weight: bold; color: #2196F3;">Actual: \${value}</div>
        <div style="font-weight: bold; color: #FF9800;">Target: \${target}</div>
    </div>
`;

<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    tooltip={{
        enable: true,
        template: tooltipTemplate
    }}
    minimum={0}
    maximum={300}
>
    <Inject services={[BulletTooltip]} />
</BulletChartComponent>
```

### Template with Units

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    tooltip={{
        enable: true,
        template: '<div><b>Revenue:</b> $${value}K<br/><b>Goal:</b> $${target}K</div>'
    }}
    minimum={0}
    maximum={300}
>
    <Inject services={[BulletTooltip]} />
</BulletChartComponent>
```

## Tooltip Appearance Customization

Customize the tooltip's visual appearance using `fill`, `border`, and `textStyle` properties.

### Background Color (fill)

```tsx
<BulletChartComponent
    tooltip={{
        enable: true,
        fill: "#333333"          // Dark background
    }}
>
    <Inject services={[BulletTooltip]} />
</BulletChartComponent>
```

### Border Customization

```tsx
<BulletChartComponent
    tooltip={{
        enable: true,
        border: {
            color: "#2196F3",      // Border color
            width: 2               // Border width in pixels
        }
    }}
>
    <Inject services={[BulletTooltip]} />
</BulletChartComponent>
```

### Text Style Customization

```tsx
<BulletChartComponent
    tooltip={{
        enable: true,
        textStyle: {
            color: "#FFFFFF",                    // Text color
            size: "14px",                        // Font size
            fontFamily: "Arial, sans-serif",     // Font family
            fontWeight: "bold",                  // Font weight
            fontStyle: "normal"                  // Font style
        }
    }}
>
    <Inject services={[BulletTooltip]} />
</BulletChartComponent>
```

### Complete Appearance Customization

```tsx
import { 
    BulletChartComponent,
    BulletTooltip,
    Inject
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
            tooltip={{
                enable: true,
                fill: "#424242",              // Background color
                border: {
                    color: "#FFC107",         // Border color
                    width: 2                  // Border width
                },
                textStyle: {
                    color: "#FFFFFF",          // White text
                    size: "13px",
                    fontFamily: "Segoe UI, Arial, sans-serif",
                    fontWeight: "500"
                }
            }}
        >
            <Inject services={[BulletTooltip]} />
        </BulletChartComponent>
    );
}
```

## Complete Styled Example

Combining template and appearance customization:

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

    const tooltipTemplate = `
        <div style="padding: 8px;">
            <div style="margin-bottom: 4px;">
                <span style="font-weight: 600;">Actual:</span> 
                <span style="color: #4CAF50;">\${value}K</span>
            </div>
            <div>
                <span style="font-weight: 600;">Target:</span> 
                <span style="color: #FF9800;">\${target}K</span>
            </div>
        </div>
    `;

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
            valueFill="#5B5FC7"
            valueHeight={18}
            tooltip={{
                enable: true,
                template: tooltipTemplate,
                fill: "#FFFFFF",
                border: {
                    color: "#DDDDDD",
                    width: 1
                },
                textStyle: {
                    color: "#333333",
                    size: "12px",
                    fontFamily: "Arial, sans-serif"
                }
            }}
            width="90%"
            height="120px"
        >
            <BulletRangeCollectionDirective>
                <BulletRangeDirective end={150} color="#E74C3C" opacity={0.3} />
                <BulletRangeDirective end={250} color="#F39C12" opacity={0.3} />
                <BulletRangeDirective end={300} color="#27AE60" opacity={0.3} />
            </BulletRangeCollectionDirective>
            <Inject services={[BulletTooltip]} />
        </BulletChartComponent>
    );
}

export default App;
```

## Common Patterns

### Percentage Display

```tsx
<BulletChartComponent
    tooltip={{
        enable: true,
        template: '<div>Completion: ${value}%<br/>Goal: ${target}%</div>'
    }}
>
    <Inject services={[BulletTooltip]} />
</BulletChartComponent>
```

### Currency Format

```tsx
<BulletChartComponent
    tooltip={{
        enable: true,
        template: '<div><b>Revenue:</b> $${value},000<br/><b>Target:</b> $${target},000</div>'
    }}
>
    <Inject services={[BulletTooltip]} />
</BulletChartComponent>
```

### Performance Indicator

```tsx
const getPerformanceTemplate = () => {
    return `
        <div style="padding: 10px;">
            <div><b>Actual:</b> \${value}</div>
            <div><b>Target:</b> \${target}</div>
            <div style="margin-top: 5px; color: ${data[0].value >= data[0].target ? '#4CAF50' : '#F44336'};">
                <b>Status:</b> ${data[0].value >= data[0].target ? 'Target Met ✓' : 'Below Target ✗'}
            </div>
        </div>
    `;
};
```

## Best Practices

### When to Use Tooltips
- Always enable tooltips for interactive dashboards
- Use when exact values are important
- Provide context that doesn't fit in the main view

### Template Design
- Keep templates concise (2-4 lines of info)
- Use bold for labels, regular weight for values
- Include units (K, M, %, $) for clarity
- Maintain consistent formatting across charts

### Styling
- Ensure sufficient contrast between text and background
- Use readable font sizes (12-14px)
- Keep borders subtle (1-2px width)
- Match tooltip style with overall dashboard theme

### Accessibility
- Don't rely solely on tooltips for critical information
- Provide alternative ways to view data (data labels, legends)
- Ensure tooltip text is readable with sufficient contrast

## Troubleshooting

**Issue: Tooltip not appearing**
- Verify `tooltip.enable` is set to `true`
- Check that `BulletTooltip` module is imported and injected
- Ensure `<Inject services={[BulletTooltip]} />` is inside the component
- Try hovering directly over the value bar or target marker

**Issue: Template not rendering**
- Check template string syntax (use backticks for multi-line)
- Verify placeholder syntax: `${value}` and `${target}`
- Escape special characters if needed
- Test with a simple template first

**Issue: Tooltip styling not applying**
- Ensure properties are nested correctly in tooltip object
- Check that color values are valid CSS colors
- Verify font size includes units: "14px" not 14
- Use correct property names (case-sensitive)

**Issue: Tooltip text hard to read**
- Increase contrast between text color and fill color
- Adjust text color: light text on dark background, dark text on light background
- Increase font size if too small
- Add padding in custom templates

**Issue: Tooltip appearing but shows wrong values**
- Verify `valueField` and `targetField` match data properties
- Check data source for correct values
- Ensure placeholders in template match: `${value}` and `${target}`
