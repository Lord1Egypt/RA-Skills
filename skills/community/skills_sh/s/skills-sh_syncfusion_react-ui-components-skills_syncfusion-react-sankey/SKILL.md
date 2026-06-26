---
name: syncfusion-react-sankey
description: Implement Syncfusion React Sankey Chart to visualize energy flows, process dependencies, and hierarchical relationships between nodes. Use this skill when creating Sankey diagrams, flow visualizations, or node-link networks. Covers installation, nodes and links configuration, labeling, legends, tooltips, events, appearance customization, RTL support, accessibility, and export features.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion React Sankey Chart

## When to Use This Skill

Use this skill when you need to:
- Display energy flows or process dependencies
- Visualize hierarchical relationships and data movement between categories
- Create interactive node-link diagrams with custom styling
- Build responsive flow visualizations with legends and tooltips
- Enable user interactions like clicks and hover effects
- Export or print flow diagrams
- Support accessibility features and RTL layouts

## Component Overview

The Syncfusion React Sankey Chart component visualizes flow data through interconnected nodes and links, perfect for displaying energy consumption, data flows, process hierarchies, and organizational relationships. It provides rich customization options for appearance, interactivity, and accessibility.

**Key Features:**
- **Node & Link Configuration** - Define data sources and destinations with custom styling
- **Labels & Positioning** - Control text display, node positioning, and title/subtitle
- **Legend Support** - Display legend with customizable positioning and styling
- **Interactivity** - Tooltips, click events, and user interactions
- **Appearance Customization** - Colors, opacity, link curvature, and theming
- **RTL Support** - Right-to-left layout for international applications
- **Accessibility** - WCAG compliance and screen reader support
- **Export Capabilities** - Export diagrams and print functionality

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Dependencies and module injection
- Basic Sankey component creation
- Development environment setup
- Running your first example

### Nodes and Links Configuration
📄 **Read:** [references/nodes-and-links.md](references/nodes-and-links.md)
- Node structure and properties
- Link structure and data flow
- Data binding and source/target relationships
- Node positioning with offset property
- Link styling and customization
- Performance optimization for large datasets

### Labels and Positioning
📄 **Read:** [references/labels-and-positioning.md](references/labels-and-positioning.md)
- Label visibility and configuration
- Node label positioning and alignment
- Title and subtitle settings
- Text formatting and styling options
- Handling label overflow scenarios

### Legend and Display Options
📄 **Read:** [references/legend-and-display.md](references/legend-and-display.md)
- Legend configuration and visibility
- Legend positioning (Top, Bottom, Left, Right)
- Display options and item padding
- Visual styling and theming
- Color customization

### Interactivity and Events
📄 **Read:** [references/interactivity.md](references/interactivity.md)
- Tooltip configuration and display
- Event handling (nodeClick, linkClick, load events)
- User interaction patterns
- Enabling/disabling interactive features
- Event callbacks and data access

### Appearance and Styling
📄 **Read:** [references/appearance-and-styling.md](references/appearance-and-styling.md)
- Link styling (opacity, curvature, colorType)
- Node appearance customization
- Color schemes and theming
- CSS integration and custom styling
- Responsive design considerations

### Accessibility and Orientation
📄 **Read:** [references/accessibility-and-orientation.md](references/accessibility-and-orientation.md)
- RTL (Right-to-Left) layout support
- WCAG accessibility compliance
- Keyboard navigation support
- Screen reader compatibility
- Device responsiveness

### Export and Print Features
📄 **Read:** [references/export-and-print.md](references/export-and-print.md)
- Export functionality and image formats
- Print capabilities
- Exporting diagram data
- Configuration options
- Common export scenarios

### API Reference
📄 **Read:** [references/sankey-props.md](references/sankey-props.md) • [references/sankey-events.md](references/sankey-events.md) • [references/sankey-methods.md](references/sankey-methods.md) • [references/sankey-examples.md](references/sankey-examples.md)
- Machine-parsable API listings for component props, events, and methods
- Verified defaults, types, and short descriptions mapped from Syncfusion React Sankey API
- Implementation examples illustrating common patterns and method usage

## Quick Start Example

```tsx
import React from 'react';
import {
  SankeyComponent, Inject, SankeyTooltip, SankeyLegend, SankeyExport,
  SankeyNodeDirective,
  SankeyNodesCollectionDirective,
  SankeyLinkDirective,
  SankeyLinksCollectionDirective
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";

function BasicSankey() {
  return (
    <div className="control-pane">
      <div className="control-section">
        <SankeyComponent
          width="90%"
          height="420px"
          title="Energy Flow"
          tooltip={{ enable: true }}
          legendSettings={{ visible: true, position: 'Bottom' }}
        >
          <SankeyNodesCollectionDirective>
            <SankeyNodeDirective id="Solar" label={{ text: 'Solar' }} />
            <SankeyNodeDirective id="Generation" label={{ text: 'Generation' }} />
            <SankeyNodeDirective id="Consumption" label={{ text: 'Consumption' }} />
          </SankeyNodesCollectionDirective>
          <SankeyLinksCollectionDirective>
            <SankeyLinkDirective sourceId="Solar" targetId="Generation" value={450} />
            <SankeyLinkDirective sourceId="Generation" targetId="Consumption" value={400} />
          </SankeyLinksCollectionDirective>
          <Inject services={[SankeyTooltip, SankeyLegend, SankeyExport]} />
        </SankeyComponent>
      </div>
    </div>
  );
}

export default BasicSankey;
ReactDOM.render(<BasicSankey />, document.getElementById("charts"));
```

## Common Patterns

### Pattern 1: Multi-Level Flow Visualization
Create hierarchical flows with multiple source and destination nodes for complex data relationships.

```tsx
<SankeyComponent title="Process Flow">
  <SankeyNodesCollectionDirective>
    <SankeyNodeDirective id="Input" />
    <SankeyNodeDirective id="Processing" />
    <SankeyNodeDirective id="Output" />
  </SankeyNodesCollectionDirective>
  <SankeyLinksCollectionDirective>
    <SankeyLinkDirective sourceId="Input" targetId="Processing" value={100} />
    <SankeyLinkDirective sourceId="Processing" targetId="Output" value={80} />
  </SankeyLinksCollectionDirective>
  <Inject services={[SankeyTooltip, SankeyLegend]} />
</SankeyComponent>
```

### Pattern 2: Styled Links with Color Types
Customize link appearance using colorType to inherit colors from source or apply custom styling.

```tsx
<SankeyComponent
  linkStyle={{ 
    opacity: 0.6, 
    curvature: 0.55, 
    colorType: 'Source'
  }}
>
  {/* nodes and links */}
  <Inject services={[SankeyTooltip, SankeyLegend]} />
</SankeyComponent>
```

### Pattern 3: Responsive with Device Detection
Adapt component dimensions and display based on device type for better UX.

```tsx
import { Browser } from '@syncfusion/ej2-base';

<SankeyComponent
  height={Browser.isDevice ? '600px' : '450px'}
  labelSettings={{ visible: !Browser.isDevice }}
>
  {/* nodes and links */}
  <Inject services={[SankeyTooltip, SankeyLegend]} />
</SankeyComponent>
```

## Key Props Reference

| Prop | Type | Purpose |
|------|------|---------|
| `width` | string | Chart width (e.g., '90%', '800px') |
| `height` | string | Chart height (e.g., '420px') |
| `title` | string | Main chart title |
| `subTitle` | string | Chart subtitle |
| `tooltip` | object | Tooltip configuration |
| `legendSettings` | object | Legend visibility and positioning |
| `labelSettings` | object | Node label configuration |
| `linkStyle` | object | Link styling (opacity, curvature, colorType) |

## Common Use Cases

1. **Energy Consumption Flow** - Track energy from sources through generation, distribution, to consumption sectors
2. **Process Dependencies** - Visualize workflow stages and data movement through processes
3. **Organizational Hierarchy** - Display reporting structures and resource allocation
4. **Supply Chain Flow** - Show product movement from suppliers through manufacturing to distribution
5. **Data Pipeline** - Visualize data transformation and routing through system components

---
