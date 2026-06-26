---
name: syncfusion-react-treemaps
description: Comprehensive guide for implementing Syncfusion React TreeMap component. Use this skill when users need help creating hierarchical data visualizations, configuring drill-down interactions, applying color mapping, working with multiple hierarchy levels, customizing leaf items, or troubleshooting TreeMap data binding and display issues. Covers installation, data binding patterns, layouts, legends, tooltips, selection, accessibility, and advanced customization for interactive hierarchical data exploration.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion React TreeMap

A comprehensive guide for implementing and customizing the Syncfusion React TreeMap component for hierarchical data visualization. The TreeMap displays nested rectangles where area represents data values, supporting multiple hierarchy levels, interactive drill-down, and rich customization.

## When to Use This Skill

Use this skill when you need to:
- Install and set up the TreeMap component
- Bind hierarchical or flat data to TreeMap
- Visualize tree-structured data with multiple levels
- Implement drill-down interactions for data exploration
- Apply color mapping strategies (range, equal, desaturation)
- Configure layouts (square, horizontal, vertical, auto)
- Add legends, tooltips, and data labels
- Implement selection and highlight features
- Customize leaf items and label positioning
- Handle accessibility requirements
- Export or print TreeMap visualizations
- Internationalize or apply RTL support

## Component Overview

The **TreeMap** component is a powerful hierarchical data visualization tool that:
- Renders nested rectangles using SVG for scalability
- Supports any number of hierarchy levels
- Provides four layout algorithms for optimal space utilization
- Enables drill-down for exploring nested data
- Offers three color mapping types for data-driven styling
- Includes interactive features: selection, highlight, tooltips
- Supports data labels, legends, and custom templates
- Provides accessibility and internationalization support

### When to Choose TreeMap

**Choose TreeMap when:**
- Visualizing hierarchical data (organizational charts, file systems, category hierarchies)
- Comparing multiple values across categories using area encoding
- Exploring nested categories through drill-down interaction
- Displaying tree-structured data with many items at multiple levels
- Need space-efficient visualization that uses area encoding

**Don't use TreeMap for:**
- Simple flat data with few items (use Bar/Column charts)
- Time-series data (use Line/Area charts)
- Relationships between entities (use Diagram/Graph)
- Single hierarchy with few nodes (consider alternative layouts)

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installing @syncfusion/ej2-react-treemap
- Package dependencies and setup
- Module injection for features
- Creating your first TreeMap
- Rendering basic hierarchical data

### Data Binding & Hierarchies
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Flat vs hierarchical data structures
- Configuring weightValuePath for sizing
- Binding multilevel hierarchies with levels
- Remote data source integration
- Data transformation patterns

### Color Mapping Strategies
📄 **Read:** [references/color-mapping.md](references/color-mapping.md)
- Range-based color mapping (gradient by values)
- Equal value color mapping (categorical colors)
- Desaturation mapping (opacity-based variation)
- Dynamic color assignment
- Choosing color mapping strategies

### Layouts and Layout Selection
📄 **Read:** [references/layouts.md](references/layouts.md)
- Square layout (balanced aspect ratio)
- Horizontal layout (left-to-right ordering)
- Vertical layout (top-to-bottom ordering)
- Auto layout (default optimal layout)
- When to use each layout type

### Drill-Down and Navigation
📄 **Read:** [references/drilldown.md](references/drilldown.md)
- Enabling drill-down with enableDrillDown
- Configuring levels for multi-level exploration
- Drill-down events and callbacks
- Breadcrumb navigation patterns
- Back navigation handling

### Leaf Items, Labels & Templates
📄 **Read:** [references/leaf-items-and-labels.md](references/leaf-items-and-labels.md)
- Leaf item configuration and styling
- Label positioning (TopLeft, Center, BottomRight, etc.)
- Data label formatting and templates
- Border and fill customization
- Label overflow handling

### Legends, Tooltips & Selection
📄 **Read:** [references/legends-tooltips-selection.md](references/legends-tooltips-selection.md)
- Creating and configuring legends
- Tooltip templates and styling
- Selection and highlight modes
- Interactive features and events
- Responding to user interactions

### Customization, Accessibility & Export
📄 **Read:** [references/customization-accessibility.md](references/customization-accessibility.md)
- WCAG compliance and keyboard navigation
- RTL (right-to-left) support
- Internationalization and localization
- Theming and CSS customization
- Print and export functionality

## Quick Start Example

```jsx
import * as React from 'react';
import { TreeMapComponent } from '@syncfusion/ej2-react-treemap';

export function TreeMapDemo() {
  const data = [
    { Title: 'USA', State: 'California', Sales: 2830 },
    { Title: 'USA', State: 'Texas', Sales: 2020 },
    { Title: 'USA', State: 'Florida', Sales: 1880 },
    { Title: 'Germany', State: 'Berlin', Sales: 1880 },
    { Title: 'Germany', State: 'Munich', Sales: 1550 },
  ];

  return (
    <TreeMapComponent
      height="350px"
      dataSource={data}
      weightValuePath="Sales"
      leafItemSettings={{
        labelPath: 'State',
        colorMapping: [
          { from: 1500, to: 2000, color: '#FF6B6B' },
          { from: 2000, to: 2500, color: '#4ECDC4' },
          { from: 2500, to: 3000, color: '#45B7D1' }
        ]
      }}
    />
  );
}
```

## Common Patterns

### Pattern 1: Hierarchical Data with Drill-Down

```jsx
<TreeMapComponent
  enableDrillDown={true}
  dataSource={data}
  weightValuePath="Sales"
>
  <LevelsDirective>
    <LevelDirective groupPath="Country" />
    <LevelDirective groupPath="State" />
    <LevelDirective groupPath="City" />
  </LevelsDirective>
</TreeMapComponent>
```

**When to use:** Exploring multilevel hierarchies with progressive disclosure through drill-down interaction.

### Pattern 2: Color-Coded Categories

```jsx
<TreeMapComponent
  equalColorValuePath="Category"
  leafItemSettings={{
    colorMapping: [
      { value: 'Electronics', color: '#3498db' },
      { value: 'Furniture', color: '#e74c3c' },
      { value: 'Clothing', color: '#2ecc71' }
    ]
  }}
/>
```

**When to use:** Categorizing items with distinct colors for quick visual identification.

### Pattern 3: Value-Range Color Gradient

```jsx
<TreeMapComponent
  rangeColorValuePath="Sales"
  leafItemSettings={{
    colorMapping: [
      { from: 0, to: 10000, color: '#90EE90' },
      { from: 10000, to: 50000, color: '#FFD700' },
      { from: 50000, to: 100000, color: '#FF6347' }
    ]
  }}
/>
```

**When to use:** Showing magnitude differences through color intensity for performance metrics, sales, or other continuous values.

## Key Props and Configuration

| Prop | Purpose | Common Values |
|------|---------|---------------|
| `dataSource` | Hierarchical or flat data array | Array of objects |
| `weightValuePath` | Property path for item sizing | e.g., 'Sales', 'Count' |
| `equalColorValuePath` | Property for categorical coloring | e.g., 'Category', 'Type' |
| `rangeColorValuePath` | Property for range-based coloring | e.g., 'Sales', 'Value' |
| `enableDrillDown` | Enable click-to-drill interaction | true/false |
| `layoutType` | Spatial layout algorithm | 'Squarified', 'Horizontal', 'Vertical', 'SliceAndDice' |
| `height` | Component height | e.g., '350px', '100%' |
| `palette` | Array of colors for items | ['#color1', '#color2', ...] |

## Common Use Cases


## API Reference

This section summarizes the most commonly used `TreeMap` props, methods, and events. For the complete API with typed models, see the official docs: https://ej2.syncfusion.com/react/documentation/api/treemap/index-default

### Important Properties (selected)
- `dataSource` (Array|DataManager) — The data source for TreeMap. Can be flat or hierarchical. Default: `null`
- `weightValuePath` (string) — Path to numeric value used for sizing each item. Default: `null`
- `colorValuePath` (string) — Field used for continuous color mapping (range palettes).
- `equalColorValuePath` (string[]) — Field(s) for categorical/equal color mapping.
- `rangeColorValuePath` (string[]) — Field(s) used for range-based color mapping.
- `leafItemSettings` (object) — Configuration for leaf items (e.g., `labelPath`, `colorMapping`, `border`, `gap`).
- `levels` (LevelSettingsModel[]) — Array of level configuration objects to define grouping and appearance per hierarchy level.
- `layoutType` (string) — Layout algorithm: `Squarified` (default), `SliceAndDiceHorizontal`, `SliceAndDiceVertical`, `SliceAndDiceAuto`, etc.
- `enableDrillDown` (boolean) — Enable drill-down interaction. Default: `false`
- `drillDownView` (boolean) — Use drill-down view layout. Default: `false`
- `enableBreadcrumb` (boolean) — Show breadcrumb when drilling. Default: `false`
- `breadcrumbConnector` (string) — Separator shown between breadcrumb items.
- `initialDrillDown` (object) — Configure initial drill-down level/state.
- `enableHtmlSanitizer` (boolean) — Sanitize HTML in templates/tooltips. Default: `true`
- `enablePersistence` (boolean) — Persist component state between reloads. Default: `false`
- `enableRtl` (boolean) — Enable right-to-left rendering. Default: `false`
- `palette` (string[]) — Array of palette colors used for fills.
- `highlightSettings` (object) — Highlight configuration and styling.
- `selectionSettings` (object) — Selection configuration (mode, enable, etc.).
- `legendSettings` (object) — Legend configuration (position, title, shape, etc.).
- `titleSettings` (object) — Title and subtitle configuration.
- `tooltipSettings` (object) — Tooltip templates and behavior.
- `format` (string) — Formatting string for labels or values.
- `useGroupingSeparator` (boolean) — Apply grouping separator for numeric values. Default: `true`
- `description` (string) — Accessibility description for the TreeMap.
- `margin` (object) — Margin settings for the component (`{ top, right, bottom, left }`).
- `height` / `width` (string|number) — Size of the component (e.g., `350px` or `100%`).
- `theme` (string) — Theme name (e.g., `Material`, `Bootstrap`).

### Common Methods
- `destroy()` — Clean up the TreeMap instance and remove listeners.
- `export(type, fileName, orientation, allowDownload)` — Export the TreeMap as `PNG|JPEG|SVG|PDF`. Returns a Promise for PDF export flows.
- `print(id)` — Print TreeMap content by element id, DOM element, or array of ids.
- `doubleClickOnTreeMap(e)` — Programmatically trigger double-click behavior.
- `selectItem(levelOrder, isSelected)` — Select or deselect an item by level order array.

### Common Events
- `load` / `loaded` — Lifecycle events fired before/after component load.
- `itemRendering` — Fired while items are rendered; use to customize item appearance.
- `click` / `itemClick` — Fired on item click.
- `doubleClick` — Fired on item double click.
- `drillStart` / `drillEnd` — Fired when drill-down starts/ends.
- `itemHighlight` / `itemSelected` — Events for highlight/selection lifecycle.
- `legendRendering` / `legendItemRendering` — Events during legend rendering.
- `tooltipRendering` — Fired when tooltip content is prepared.
- `resize` — Fired on component resize.
- `beforePrint` / `print` — Hooks around printing/export.

### Quick Import Example

```jsx
import { TreeMapComponent, LevelsDirective, LevelDirective, Inject, TreeMapTooltip } from '@syncfusion/ej2-react-treemap';

<TreeMapComponent dataSource={data} weightValuePath="value" enableDrillDown={true}>
  <LevelsDirective>
    <LevelDirective groupPath="category" />
  </LevelsDirective>
  <Inject services={[TreeMapTooltip]} />
</TreeMapComponent>
```

1. **Organization Hierarchies:** Visualize employee counts across departments, regions, and divisions
2. **File System Browser:** Display disk usage by folders and subfolders with drill-down
3. **Sales Performance:** Compare regional sales, product categories, and territories
4. **Website Analytics:** Explore traffic sources, pages, and user segments hierarchically
5. **Portfolio Allocation:** Visualize asset distribution across categories and subcategories
6. **Market Share:** Display competitive landscape with company hierarchies
7. **Budget Analysis:** Allocate and visualize budget across departments and line items

## Next Steps

1. **Start with Getting Started guide** to install and render your first TreeMap
2. **Choose a data binding pattern** based on your data structure
3. **Select color mapping strategy** (range, equal, or desaturation)
4. **Configure layout** and drill-down if exploring hierarchies
5. **Customize leaf items, labels, and tooltips** for your use case
6. **Add interactivity** with selection and events
7. **Ensure accessibility** and internationalization requirements

---

**Ready to implement TreeMap?** Start with [references/getting-started.md](references/getting-started.md) or choose a specific feature guide from the navigation options above.
