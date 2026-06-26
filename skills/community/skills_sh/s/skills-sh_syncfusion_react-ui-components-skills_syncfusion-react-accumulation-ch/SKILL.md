---
name: syncfusion-react-accumulation-chart
description: Implement Syncfusion React Accumulation Charts including Pie, Doughnut, Funnel, and Pyramid chart types. Use this skill when users need circular data visualization, percentage-based charts, or proportional data displays. Covers data labels, legends, tooltips, grouping, smart labels, drill-down charts, explode effects, theming, accessibility, export/print capabilities, and dynamic data updates.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion React Accumulation Charts

A comprehensive skill for implementing Syncfusion's React Accumulation Chart components (`AccumulationChartComponent`), which provide circular and hierarchical data visualizations including Pie, Doughnut, Funnel, and Pyramid charts with rich interactive features, export capabilities, and full accessibility support.

## When to Use This Skill

Use this skill when you need to:
- Create pie or doughnut charts for proportional data display
- Implement funnel or pyramid charts for hierarchical/process visualization
- Display percentage-based or categorical data in circular layouts
- Add interactive features like tooltips, legends, and data labels
- Implement smart label positioning to avoid overlaps
- Create drill-down or multi-level accumulation charts
- Apply explode effects to highlight specific data points
- Group small data values for better visualization
- Customize chart appearance with themes, colors, and patterns
- Handle empty or missing data points elegantly
- Implement accessible data visualizations with WCAG compliance

## Component Overview

The Syncfusion React Accumulation Chart component provides four primary chart types:

- **Pie Chart:** Circular chart divided into slices representing data proportions
- **Doughnut Chart:** Pie chart with a hollow center (configurable inner radius)
- **Funnel Chart:** Inverted triangle showing progressive reduction (sales funnels, conversion rates)
- **Pyramid Chart:** Triangle showing hierarchical data (population pyramids, organizational structures)

**Key Features:**
- Smart labels that avoid overlapping
- Grouping based on value or point count
- Interactive tooltips and legends
- Explode effects for emphasis
- Semi-pie charts with custom angles
- Multi-level drill-down capability
- Border radius for modern appearance
- Pattern fills and custom colors

## Documentation and Navigation Guide

### Getting Started

📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installing @syncfusion/ej2-react-charts package
- Setting up React project (Vite or Create React App)
- Importing AccumulationChartComponent
- Registering CSS themes
- Creating your first pie chart with data binding
- Understanding AccumulationSeriesCollectionDirective pattern
- Basic series configuration (xName, yName, dataSource)

### Pie and Doughnut Charts

📄 **Read:** [references/pie-doughnut-charts.md](references/pie-doughnut-charts.md)
- Creating basic pie charts with PieSeries injection
- Customizing radius (default 80%, custom values)
- Positioning pie center (centerX, centerY properties)
- Creating doughnut charts with innerRadius
- Various radius pie charts (different slice sizes)
- Semi-pie charts using startAngle and endAngle
- Color and text mapping from data source
- Border radius for modern rounded slices
- Hiding/showing borders on mouse hover
- Applying pattern fills (stripes, dots, grids)
- Multi-level drill-down with pointClick event
- Point customization with pointRender event

### Funnel and Pyramid Charts

📄 **Read:** [references/funnel-pyramid-charts.md](references/funnel-pyramid-charts.md)
- Creating funnel charts with FunnelSeries injection
- Funnel size customization (width and height)
- Neck size configuration (neckWidth, neckHeight)
- Gap between segments (gapRatio 0 to 1)
- Funnel rendering modes (Standard vs Trapezoidal)
- Creating pyramid charts with PyramidSeries injection
- Pyramid rendering modes (Linear vs Surface)
- Pyramid size customization
- Explode effects (explode, explodeOffset, explodeIndex)
- Smart data label positioning for funnels/pyramids

### Data Labels

📄 **Read:** [references/data-labels.md](references/data-labels.md)
- Enabling data labels (visible property, AccumulationDataLabel injection)
- Positioning labels (Inside vs Outside)
- Rotating data labels (angle and enableRotation)
- Smart labels to prevent overlapping (enableSmartLabels)
- Formatting label text (n, p, c number formats)
- Custom data label templates with HTML
- Connector line customization (type, color, width, length, dashArray)
- Text mapping from data source (name property)
- Customizing labels with textRender event
- Text wrapping (textWrap, maxWidth)
- Displaying percentages in labels (textRender vs template approaches)

### Legend Configuration

📄 **Read:** [references/legend.md](references/legend.md)
- Enabling legend (AccumulationLegend injection)
- Position and alignment (left, right, top, bottom, center, far, near)
- Reversing legend item order
- Legend shape customization (Circle, Rectangle, Triangle, etc.)
- Legend and legend item size configuration
- Automatic pagination for many items
- Text wrapping for long labels (textWrap, maximumLabelWidth)
- Animation on legend click toggle
- Legend title configuration and styling
- Arrow page navigation (enablePages false)
- Legend item padding adjustment
- Layout options (horizontal, vertical, auto with maximumColumns)
- Custom legend templates with HTML
- Fixed width legend items

### Tooltip Customization

📄 **Read:** [references/tooltip.md](references/tooltip.md)
- Enabling tooltips (AccumulationTooltip injection)
- Custom tooltip headers
- Format strings (${point.x}, ${point.y}, ${series.name})
- Tooltip mapping from data source (tooltipMappingName)
- Custom tooltip templates with HTML/React components
- Fixed tooltip positioning (location property)
- Tooltip styling and appearance

### Data Grouping

📄 **Read:** [references/grouping.md](references/grouping.md)
- Grouping by value threshold (groupTo property)
- Grouping by point count
- Group mode configuration (Value vs Point)
- Custom group names and labels
- Group appearance customization
- When to use grouping for better visualization

### Annotations

📄 **Read:** [references/annotations.md](references/annotations.md)
- Adding annotations with AccumulationAnnotation injection
- Annotation content and HTML templates
- Positioning annotations (x, y coordinates)
- Coordinate units (Pixel vs Point)
- Multiple annotations per chart
- Dynamic annotation updates

### Customization and Styling

📄 **Read:** [references/customization.md](references/customization.md)
- Point-level customization with pointRender event
- Custom color schemes and palettes
- Setting colors per data point (fill property)
- Border customization (width, color)
- Pattern fills for slices (applyPattern)
- Point-specific styling based on data values
- Conditional styling patterns

### Accessibility Features

📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WCAG 2.1 compliance features
- Keyboard navigation support (Tab, Arrow keys)
- ARIA attributes configuration
- Screen reader support and announcements
- High contrast mode compatibility
- Advanced accessibility configuration
- Focus indicators and visible focus

### Empty Points Handling

📄 **Read:** [references/empty-points.md](references/empty-points.md)
- Handling null, undefined, or NaN data
- Empty point modes (Zero, Drop, Average, Gap)
- Customizing empty point appearance
- Fill and border configuration for empty points
- When to use each empty point mode

### Appearance and Theming

📄 **Read:** [references/appearance-theming.md](references/appearance-theming.md)
- Built-in themes (Material, Bootstrap, Fluent, Tailwind, Fabric)
- Importing and applying themes
- Gradient fills for slices
- Title and subtitle configuration
- Dynamic data updates and animation
- Chart dimensions and responsive sizing

### Export and Print

📄 **Read:** [references/export-print.md](references/export-print.md)
- Enabling export functionality with Export module
- Export to image formats (PNG, JPEG)
- Export to PDF and SVG
- Export customization with beforeExport event
- Print chart functionality
- Exporting multiple charts
- After export event handling
- File naming conventions and best practices

### API Reference

📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Complete AccumulationChartComponent properties reference
- AccumulationSeriesDirective properties
- All methods (export, print, setAnnotationValue, calculateBounds)
- All events (lifecycle, rendering, mouse, selection, export)
- Common model interfaces (LegendSettings, TooltipSettings, DataLabel)
- Module services and injection requirements
- Event argument interfaces
- Selection patterns reference
- Themes reference
- Complete usage examples with TypeScript

## Quick Start Example

Here's a minimal example to create a basic pie chart:

```tsx
import { 
  AccumulationChartComponent, 
  AccumulationSeriesCollectionDirective, 
  AccumulationSeriesDirective,
  Inject,
  AccumulationLegend,
  AccumulationDataLabel,
  AccumulationTooltip,
  PieSeries
} from '@syncfusion/ej2-react-charts';

function App() {
  const data = [
    { x: 'Chrome', y: 61.3, text: 'Chrome: 61.3%' },
    { x: 'Safari', y: 24.6, text: 'Safari: 24.6%' },
    { x: 'Edge', y: 5.0, text: 'Edge: 5.0%' },
    { x: 'Firefox', y: 4.8, text: 'Firefox: 4.8%' },
    { x: 'Others', y: 4.3, text: 'Others: 4.3%' }
  ];

  return (
    <AccumulationChartComponent 
      id='pie-chart'
      title='Browser Market Share'
      legendSettings={{ visible: true }}
      tooltip={{ enable: true }}
      enableSmartLabels={true}
    >
      <Inject services={[
        AccumulationLegend, 
        AccumulationDataLabel, 
        AccumulationTooltip, 
        PieSeries
      ]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          radius='90%'
          dataLabel={{
            visible: true,
            position: 'Outside',
            name: 'text'
          }}
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Common Patterns

### Pattern 1: Doughnut Chart with Legend

```tsx
<AccumulationChartComponent 
  id='doughnut-chart'
  legendSettings={{ visible: true, position: 'Right' }}
>
  <Inject services={[AccumulationLegend, PieSeries]} />
  <AccumulationSeriesCollectionDirective>
    <AccumulationSeriesDirective
      dataSource={data}
      xName='category'
      yName='value'
      innerRadius='40%'  // Creates doughnut hole
      radius='100%'
    />
  </AccumulationSeriesCollectionDirective>
</AccumulationChartComponent>
```

### Pattern 2: Funnel Chart with Data Labels

```tsx
<AccumulationChartComponent id='funnel-chart'>
  <Inject services={[FunnelSeries, AccumulationDataLabel]} />
  <AccumulationSeriesCollectionDirective>
    <AccumulationSeriesDirective
      dataSource={salesData}
      xName='stage'
      yName='count'
      type='Funnel'
      neckWidth='25%'
      neckHeight='5%'
      gapRatio={0.08}
      dataLabel={{ visible: true, position: 'Outside' }}
    />
  </AccumulationSeriesCollectionDirective>
</AccumulationChartComponent>
```

### Pattern 3: Semi-Pie Chart (Gauge Style)

```tsx
<AccumulationSeriesDirective
  dataSource={data}
  xName='x'
  yName='y'
  startAngle={270}  // Start from bottom
  endAngle={90}     // End at bottom (semi-circle)
  radius='100%'
  innerRadius='40%'
  dataLabel={{ visible: true, position: 'Inside' }}
/>
```

### Pattern 4: Exploded Pie Chart

```tsx
<AccumulationSeriesDirective
  dataSource={data}
  xName='product'
  yName='sales'
  explode={true}           // Enable click-to-explode
  explodeOffset='10%'      // Distance when exploded
  explodeIndex={2}         // Explode third slice by default
  explodeAll={false}       // Don't explode all at once
/>
```

## API Reference

### AccumulationChartComponent Properties

#### Core Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `dataSource` | Object[] \| DataManager | '' | Data source for the chart |
| `series` | AccumulationSeriesModel[] | - | Collection of series configurations |
| `title` | string | null | Main title of the chart |
| `subTitle` | string | null | Subtitle displayed below the main title |
| `width` | string | null | Width of the chart ('100px', '100%') |
| `height` | string | null | Height of the chart ('100px', '100%') |
| `theme` | AccumulationTheme | 'Material' | Visual theme (Material, Bootstrap5, Fluent, Tailwind, etc.) |
| `background` | string | null | Background color (hex or rgba) |
| `backgroundImage` | string | null | Background image URL |

#### Feature Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `enableSmartLabels` | boolean | true | Prevent label overlapping with smart positioning |
| `enableAnimation` | boolean | true | Enable animations for chart rendering |
| `enableBorderOnMouseMove` | boolean | true | Show border on mouse hover |
| `enableExport` | boolean | true | Enable export functionality (JPEG, PNG, SVG, PDF) |
| `useGroupingSeparator` | boolean | false | Use thousand separators in numbers |
| `enablePersistence` | boolean | false | Persist component state across page reloads |
| `enableRtl` | boolean | false | Enable right-to-left rendering |
| `enableHtmlSanitizer` | boolean | false | Sanitize untrusted HTML values |

#### Interactive Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `selectionMode` | AccumulationSelectionMode | 'None' | Point selection mode ('None', 'Point') |
| `selectionPattern` | SelectionPattern | 'None' | Pattern for selected points (Chessboard, Dots, etc.) |
| `highlightMode` | AccumulationHighlightMode | 'None' | Point highlighting mode ('None', 'Point') |
| `highlightPattern` | SelectionPattern | 'None' | Pattern for highlighted points |
| `highlightColor` | string | '' | Color for highlighted points |
| `isMultiSelect` | boolean | false | Allow multiple point selection |
| `selectedDataIndexes` | IndexesModel[] | [] | Initially selected point indexes |

#### Layout Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `center` | PieCenterModel | {x: '50%', y: '50%'} | Center position of pie chart |
| `margin` | MarginModel | - | Chart margins (left, right, top, bottom) |
| `border` | BorderModel | - | Chart border (color, width) |
| `legendSettings` | LegendSettingsModel | - | Legend configuration |
| `tooltip` | TooltipSettingsModel | - | Tooltip configuration |
| `annotations` | AccumulationAnnotationSettingsModel[] | - | Chart annotations |
| `centerLabel` | CenterLabelModel | - | Label at chart center |

#### Accessibility Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `accessibility` | AccessibilityModel | - | Accessibility configuration for screen readers |
| `focusBorderColor` | string | null | Custom focus border color |
| `focusBorderWidth` | number | 1.5 | Focus border width in pixels |
| `focusBorderMargin` | number | 0 | Focus border margin in pixels |
| `locale` | string | 'en-US' | Localization culture string |

### AccumulationSeriesDirective Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `type` | string | 'Pie' | Chart type ('Pie', 'Funnel', 'Pyramid') |
| `dataSource` | Object[] | - | Data array for the series |
| `xName` | string | - | Property name for category/label values |
| `yName` | string | - | Property name for numeric values |
| `radius` | string | '80%' | Outer radius of pie/doughnut |
| `innerRadius` | string | '0%' | Inner radius (doughnut hole) |
| `startAngle` | number | 0 | Starting angle (0-360 degrees) |
| `endAngle` | number | 360 | Ending angle (0-360 degrees) |
| `explode` | boolean | false | Enable click-to-explode functionality |
| `explodeAll` | boolean | false | Explode all slices initially |
| `explodeIndex` | number | - | Index of slice to explode by default |
| `explodeOffset` | string | '30%' | Distance when slice is exploded |
| `neckWidth` | string | '20%' | Funnel neck width |
| `neckHeight` | string | '20%' | Funnel neck height |
| `gapRatio` | number | 0 | Gap between funnel/pyramid segments (0-1) |
| `width` | string | '80%' | Funnel/pyramid width |
| `height` | string | '80%' | Funnel/pyramid height |
| `groupTo` | string | - | Value/count threshold for grouping |
| `groupMode` | string | 'Value' | Grouping mode ('Value', 'Point') |
| `pointColorMapping` | string | - | Property name for point colors |
| `borderRadius` | number | 0 | Corner radius for rounded slices |
| `applyPattern` | boolean | false | Apply pattern fills to slices |

### Methods

| Method | Parameters | Description |
|--------|------------|-------------|
| `export()` | type: ExportType, fileName: string | Export chart (JPEG, PNG, SVG, PDF) |
| `print()` | id?: string[] \| string \| Element | Print chart |
| `calculateBounds()` | - | Calculate chart bounds |
| `setAnnotationValue()` | annotationIndex: number, content: string | Update annotation dynamically |

### Events

| Event | Args Type | Description |
|-------|-----------|-------------|
| `load` | IAccLoadedEventArgs | Before chart loads |
| `loaded` | IAccLoadedEventArgs | After chart loads |
| `seriesRender` | IAccSeriesRenderEventArgs | Before series renders |
| `pointRender` | IAccPointRenderEventArgs | Before each point renders |
| `textRender` | IAccTextRenderEventArgs | Before data labels render |
| `legendRender` | ILegendRenderEventArgs | Before legend renders |
| `legendClick` | IAccLegendClickEventArgs | When legend item is clicked |
| `annotationRender` | IAnnotationRenderEventArgs | Before annotation renders |
| `tooltipRender` | ITooltipRenderEventArgs | Before tooltip renders |
| `pointClick` | IPointEventArgs | When point is clicked |
| `pointMove` | IPointEventArgs | When mouse moves over point |
| `chartMouseClick` | IMouseEventArgs | When chart is clicked |
| `chartMouseDown` | IMouseEventArgs | On mouse down event |
| `chartMouseUp` | IMouseEventArgs | On mouse up event |
| `chartMouseMove` | IMouseEventArgs | When mouse moves over chart |
| `chartMouseLeave` | IMouseEventArgs | When mouse leaves chart |
| `chartDoubleClick` | IMouseEventArgs | When chart is double-clicked |
| `animationComplete` | IAccAnimationCompleteEventArgs | After animation completes |
| `selectionComplete` | IAccSelectionCompleteEventArgs | After selection completes |
| `resized` | IAccResizeEventArgs | After window resize |
| `beforeResize` | IAccBeforeResizeEventArgs | Before window resize |
| `beforePrint` | IPrintEventArgs | Before print starts |
| `beforeExport` | IExportEventArgs | Before export starts |
| `afterExport` | IAfterExportEventArgs | After export completes |

## Key Props Summary

| Property | Purpose | Example Values |
|----------|---------|----------------|
| `type` | Chart type | `'Pie'`, `'Funnel'`, `'Pyramid'` |
| `radius` | Outer size | `'90%'`, `'100%'` |
| `innerRadius` | Doughnut hole | `'0%'` (pie), `'40%'` (doughnut) |
| `startAngle` / `endAngle` | Slice range | `0` to `360` |
| `explode` | Enable explode | `true`, `false` |
| `neckWidth` / `neckHeight` | Funnel neck | `'25%'`, `'5%'` |
| `gapRatio` | Segment spacing | `0` to `1` |
| `enableSmartLabels` | Smart positioning | `true`, `false` |

## Common Use Cases

1. **Market Share Analysis:** Pie/doughnut charts showing competitive distribution
2. **Sales Funnels:** Funnel charts for conversion tracking at each stage
3. **Budget Allocation:** Pie charts showing spending categories
4. **Survey Results:** Doughnut charts with percentage breakdowns
5. **Population Demographics:** Pyramid charts for age distribution
6. **Process Efficiency:** Funnel charts showing drop-off rates
7. **Portfolio Distribution:** Pie charts for asset allocation
8. **Website Traffic Sources:** Doughnut charts with referral data
9. **Project Time Allocation:** Pie charts for resource distribution
10. **Customer Segmentation:** Multiple pie charts for cohort analysis

## Tips and Best Practices

- **Use smart labels** when dealing with many small slices to prevent overlap
- **Group small values** (< 5%) into "Others" category for clarity
- **Prefer doughnut over pie** when displaying a key metric in the center
- **Use funnel mode** 'Trapezoidal' for clearer stage comparison
- **Enable tooltips** for detailed information without cluttering labels
- **Choose appropriate colors** that provide sufficient contrast
- **Consider accessibility** by providing text alternatives and keyboard navigation
- **Use explode effects** sparingly to highlight important data points
- **Set enableSmartLabels** to true for charts with 8+ data points
- **Apply themes consistently** with other charts in your application

## Related Components

When building comprehensive dashboards, combine Accumulation Charts with:
- Line/Area Charts for trend analysis
- Bar/Column Charts for comparisons
- Gantt Charts for project timelines
- TreeMap for hierarchical proportional data
