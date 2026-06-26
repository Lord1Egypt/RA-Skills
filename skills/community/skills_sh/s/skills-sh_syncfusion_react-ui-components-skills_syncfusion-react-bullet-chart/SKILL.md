---
name: syncfusion-react-bullet-chart
description: Implements the Syncfusion React Bullet Chart component for KPI and performance indicator visualization. Use this when users need feature measure displays, comparative measures, target comparisons, or metric visualizations. Covers data binding, value bars, target bars, ranges, titles, tooltips, data labels, axis customization, orientation, and accessibility.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion React Bullet Charts

A skill for implementing and customizing Syncfusion's React Bullet Chart component. Bullet charts are compact data visualization components designed to compare a primary measure (actual value) against a target measure within qualitative ranges.

## When to Use This Skill

Use this skill when users need to:
- Display performance metrics or KPIs with target comparisons
- Create compact data visualizations showing actual vs. target values
- Visualize progress against goals with qualitative ranges (poor/good/excellent)
- Build dashboards with space-efficient performance indicators
- Show feature measures (actual bars) compared to comparative measures (target bars)
- Implement horizontal or vertical bullet charts
- Display multiple metrics in a compact layout
- Create accessible, keyboard-navigable chart visualizations

## Component Overview

The Bullet Chart consists of:
- **Value Bar (Feature Measure)**: The primary data/actual value being measured
- **Comparative Bar (Target Marker)**: The target or comparison value
- **Qualitative Ranges**: Background bands indicating performance levels (e.g., poor, satisfactory, good)
- **Quantitative Scale**: The axis showing numerical measurements
- **Title/Subtitle**: Descriptive text for the chart

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

### API Reference
📄 **Read:** [references/api.md](references/api.md)
- Summarizes `BulletChartComponent` props, methods, events and directives used across examples

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)

### Value Bar Configuration
📄 **Read:** [references/value-bar.md](references/value-bar.md)
- Value bar (Feature Measure) overview and purpose
- Mapping valueField from data source
- Types of actual bar shapes (Rect, Dot)
- Changing bar type with type property
- Border customization using valueBorder (color, width)
- Fill color customization using valueFill
- Height customization using valueHeight
- Binding colors dynamically from dataSource
- Complete examples for each customization option

### Comparative Bar Configuration
📄 **Read:** [references/comparative-bar.md](references/comparative-bar.md)
- Comparative bar (Target Measure) overview
- Mapping targetField from data source
- Types of target bar shapes (Circle, Cross, Rect)
- Changing target type with targetTypes property
- Customizing target appearance with targetColor
- Adjusting target width with targetWidth property
- Binding target colors from dataSource
- Complete examples for each target type

### Ranges Configuration
📄 **Read:** [references/ranges.md](references/ranges.md)
- Ranges representing qualitative bands (Good, Bad, Satisfactory)
- Using BulletRangeCollectionDirective and BulletRangeDirective
- Setting range boundaries with end property
- Understanding minimum value as range starting point
- Configuring multiple ranges for different quality levels
- Color customization with color property
- Opacity adjustment with opacity property
- Complete examples with multiple colored ranges

### Titles and Subtitles
📄 **Read:** [references/titles.md](references/titles.md)
- Adding chart title with title property
- Adding subtitle for additional information
- Title positioning with titlePosition property (Left, Right, Top, Bottom)
- Default position (Top) behavior
- Title style customization with titleStyle (color, opacity, font properties)
- Subtitle style customization with subtitleStyle (color, opacity, font properties)
- Complete examples for each position
- Font customization examples (size, family, weight, style)

### Tooltips
📄 **Read:** [references/tooltips.md](references/tooltips.md)
- Default tooltip behavior (hidden by default)
- Enabling tooltips with tooltip.enable property
- Injecting BulletTooltip module into services
- Displaying actual and target values on hover
- Creating custom templates with template property
- Using ${target} and ${value} placeholders in templates
- Tooltip appearance customization (fill, border, textStyle)
- Font customization for tooltip text
- Complete examples for default and custom tooltips

### Data Labels
📄 **Read:** [references/data-labels.md](references/data-labels.md)
- Data labels for identifying actual bar values
- Enabling data labels with dataLabel.enable property
- Label display behavior and positioning
- Style customization with labelStyle property
- Font properties (size, family, weight, style)
- Color and opacity adjustments
- Complete examples with styled data labels

### Axis Customization
📄 **Read:** [references/axis-customization.md](references/axis-customization.md)
- MajorTickLines customization (width, height, color, useRangeColor)
- MinorTickLines customization (width, height, color, useRangeColor)
- Tick placement with tickPosition (Inside, Outside)
- Label formatting with labelFormat (globalize formats: n1, n2, p1, c1, etc.)
- Format table showing common number, percentage, and currency formats
- Group separator for thousands with enableGroupSeparator
- Custom label format with ${value} placeholder
- Label placement with labelPosition (Inside, Outside)
- Opposed position with opposedPosition property
- Category labels with categoryField for X-axis
- Category label styling with categoryLabelStyle and labelStyle
- useRangeColor for labels matching range colors
- Complete examples for each axis feature

### Chart Dimensions
📄 **Read:** [references/dimensions.md](references/dimensions.md)
- Container size configuration with inline styles and CSS
- Setting chart dimensions with width and height properties
- Pixel sizing for fixed dimensions
- Percentage sizing for responsive behavior relative to container
- Default size behavior (126px height, window width)
- Complete examples for container and direct sizing

### Customization Options
📄 **Read:** [references/customization.md](references/customization.md)
- Orientation with orientation property (Horizontal, Vertical)
- Default Horizontal orientation
- Right-to-left (RTL) support with enableRtl property
- Animation configuration with animation property (duration, delay)
- Linear animation for actual and target bars
- Theme support with theme property
- Available Syncfusion themes
- Complete examples for each customization

### Accessibility
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- Accessibility compliance (ADA, Section 508, WCAG 2.2)
- Accessibility features table with compatibility status
- WAI-ARIA attributes and patterns (img role, button role, aria-label, aria-pressed)
- Keyboard interaction support (Tab, Shift+Tab, Ctrl+P)
- Screen reader support
- Right-to-left (RTL) support for internationalization
- Color contrast compliance
- Mobile device support
- Testing with accessibility-checker and axe-core tools
- Sample accessibility demo reference

## Quick Start Example

```tsx
import { BulletChartComponent, BulletRangeCollectionDirective, BulletRangeDirective, BulletTooltip, Inject } from '@syncfusion/ej2-react-charts';

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
```

## Common Patterns

### Performance Dashboard with Multiple Metrics
Display multiple bullet charts vertically to show various KPIs:
```tsx
const metrics = [
  { value: 270, target: 250, category: 'Revenue' },
  { value: 85, target: 100, category: 'Profit' },
  { value: 180, target: 150, category: 'Sales' }
];

// Map each metric to a separate BulletChartComponent with categoryField
```

### Dynamic Color from Data
Bind colors directly from your data source:
```tsx
const data = [
  { value: 270, target: 250, valueColor: '#5B5FC7', targetColor: '#646464' }
];

<BulletChartComponent
  dataSource={data}
  valueFill="valueColor"
  targetColor="targetColor"
/>
```

### Custom Tooltip Template
Show formatted values with custom HTML:
```tsx
<BulletChartComponent
  tooltip={{
    enable: true,
    template: '<div><b>Actual:</b> ${value}<br/><b>Target:</b> ${target}</div>'
  }}
/>
```

### Responsive Layout
Use percentage-based sizing for responsive dashboards:
```tsx
<BulletChartComponent
  width="100%"
  height="80px"
/>
```

## Key Props

| Property | Type | Purpose |
|----------|------|---------|
| `dataSource` | Array | Data collection for the chart |
| `valueField` | string | Field name for actual/feature measure |
| `targetField` | string | Field name for target/comparative measure |
| `minimum` | number | Minimum value of quantitative scale |
| `maximum` | number | Maximum value of quantitative scale |
| `interval` | number | Interval between axis labels |
| `title` | string | Chart title text |
| `subtitle` | string | Chart subtitle text |
| `type` | string | Value bar shape: 'Rect' or 'Dot' |
| `targetTypes` | string[] | Target bar shapes: 'Circle', 'Cross', 'Rect' |
| `orientation` | string | Chart orientation: 'Horizontal' or 'Vertical' |
| `width` | string | Chart width (pixels or percentage) |
| `height` | string | Chart height (pixels or percentage) |
| `enableRtl` | boolean | Enable right-to-left rendering |
| `theme` | string | Apply Syncfusion theme |
| `tooltip` | object | Tooltip configuration with enable, template, fill, border, textStyle |
| `dataLabel` | object | Data label configuration with enable, labelStyle |

## Common Use Cases

### KPI Dashboard
Use bullet charts to display multiple performance indicators:
- Set different targets for each metric
- Use red/yellow/green ranges for performance levels
- Add category labels for metric names
- Enable tooltips for detailed information

### Sales Performance Tracker
Compare actual sales against targets:
- Map revenue data to valueField
- Set quarterly/monthly targets in targetField
- Configure ranges for underperforming/meeting/exceeding targets
- Use data labels to show exact values

### Progress Indicators
Show progress toward goals with visual context:
- Use percentage-based ranges (0-50%, 50-75%, 75-100%)
- Customize colors to match brand guidelines
- Add animations for engaging transitions
- Position titles on the left for compact layout

### Comparative Analysis
Compare multiple items side-by-side:
- Use vertical orientation for space efficiency
- Set consistent scale across all charts
- Apply category labels for clear identification
- Customize target types (Circle, Cross) for distinction

### Mobile Dashboards
Create responsive, touch-friendly visualizations:
- Use percentage-based dimensions
- Increase touch target sizes for bars
- Enable mobile-optimized tooltips
- Test with accessibility tools for screen readers

## Edge Cases and Troubleshooting

**Data not displaying:**
- Verify valueField and targetField match data source property names
- Check that dataSource is an array with valid objects
- Ensure minimum/maximum encompass your data range

**Ranges not visible:**
- Import BulletRangeCollectionDirective and BulletRangeDirective from @syncfusion/ej2-react-charts
- Set end values in ascending order
- Verify end values are within minimum/maximum bounds

**Tooltips not working:**
- Inject BulletTooltip module: `<Inject services={[BulletTooltip]} />`
- Set tooltip.enable to true
- Check that tooltip object is properly configured

**Title/subtitle overlapping:**
- Adjust titlePosition to Left, Right, Top, or Bottom
- Increase chart dimensions (width/height)
- Customize titleStyle and subtitleStyle font sizes

**Axis labels cut off:**
- Increase chart width or height
- Adjust label format to shorter notation (e.g., 'n1' instead of full numbers)
- Use enableGroupSeparator for better readability

## Implementation Checklist

- [ ] Install @syncfusion/ej2-react-charts package
- [ ] Import BulletChartComponent and directives
- [ ] Prepare data with value and target fields
- [ ] Configure dataSource, valueField, targetField
- [ ] Set minimum, maximum, and interval for scale
- [ ] Add ranges using BulletRangeCollectionDirective
- [ ] Configure title and subtitle if needed
- [ ] Enable and customize tooltip (inject BulletTooltip)
- [ ] Test with different data ranges
- [ ] Verify accessibility with keyboard navigation
- [ ] Test responsive behavior with different screen sizes
