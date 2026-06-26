# Interactivity and Events

## Table of contents

- [Tooltip Configuration](#tooltip-configuration)
  - [Basic Tooltip Setup](#basic-tooltip-setup)
  - [Tooltip Properties](#tooltip-properties)
  - [Customized Tooltip](#customized-tooltip)
  - [Default Tooltip Content](#default-tooltip-content)
  - [Template-Based Tooltips](#template-based-tooltips)
- [Event Handling](#event-handling)
  - [Available Events](#available-events)
  - [Basic Event Handler](#basic-event-handler)
  - [Link Click Event](#link-click-event)
  - [Load Event](#load-event)
- [User Interactions - Highlighting](#user-interactions---highlighting)
  - [Hover Highlighting](#hover-highlighting)
- [Best Practices](#best-practices)

## Tooltip Configuration

Tooltips display detailed information when users hover over nodes or links.

### Basic Tooltip Setup

```tsx
<SankeyComponent
  width="90%"
  height="420px"
  title="Chart with Tooltips"
  tooltip={{ enable: true }}
>
  {/* nodes and links */}
  <Inject services={[SankeyTooltip]} />
</SankeyComponent>
```

### Tooltip Properties

| Property | Type | Purpose |
|----------|------|---------|
| `enable` | boolean | Enable/disable tooltip display |
| `fill` | string | Tooltip background color |
| `textStyle` | object | Font styling (size, family, color) |
| `border` | object | Border configuration |
| `opacity` | number | Background opacity (0-1) |

### Customized Tooltip

```tsx
<SankeyComponent
  title="Custom Tooltips"
  tooltip={{
    enable: true,
    fill: '#2E3440',           // Dark background
    textStyle: {
      color: '#ECEFF4',        // Light text
      size: 12,
      fontFamily: 'Arial'
    }
  }}
>
  {/* nodes and links */}
  <Inject services={[SankeyTooltip]} />
</SankeyComponent>
```

### Default Tooltip Content

By default, tooltips show:
- **For Nodes:** Node ID and label
- **For Links:** Source, Target, and Flow Value

```
Node: Solar
Label: Solar Energy

Source: Solar → Target: Generation
Value: 450 units
```

### Template-Based Tooltips

Customize tooltip content using templates (advanced):

```tsx
import React from 'react';

function CustomTooltipSankey() {

  return (
    <SankeyComponent
      title="Templated Tooltips"
      tooltip={{
        enable: true,
        nodeTemplate: '${name}: ${value}KX',
        linkTemplate: '${start.name}: ${start.out} KW → ${target.name}: ${target.in} KW'
      }}
    >
      {/* nodes and links */}
      <Inject services={[SankeyTooltip]} />
    </SankeyComponent>
  );
}

export default CustomTooltipSankey;
```
**Note**: Tooltip contents can be formatted using `nodeFormat` and `linkFormat` for nodes and links respectively.

## Event Handling

### Available Events

| Event | Trigger | Use Case |
|-------|---------|----------|
| `nodeClick` | Node is clicked | Track selections, drill-down |
| `linkClick` | Link is clicked | Analyze flow, filter data |
| `load` | Chart fully loaded | Initialize, fetch data |
| `loaded` | Chart rendering complete | Post-render operations |
| `tooltipRender` | Tooltip about to show | Custom tooltip content |

### Basic Event Handler

```tsx
import React, { useState } from 'react';

function SankeyWithClickEvents() {
  const [selectedNode, setSelectedNode] = useState(null);

  const onNodeClick = (args) => {
    console.log('Node clicked:', args.data);
    setSelectedNode(args.data.id);
  };

  return (
    <div>
      {selectedNode && (
        <p>Selected Node: {selectedNode}</p>
      )}

      <SankeyComponent
        width="90%"
        height="420px"
        title="Interactive Nodes"
        nodeClick={onNodeClick}
      >
        {/* nodes and links */}
      </SankeyComponent>
    </div>
  );
}

export default SankeyWithClickEvents;
```

### Link Click Event

```tsx
function SankeyWithLinkEvents() {
  const onLinkClick = (args) => {
    const { source, target, value } = args.data;
    console.log(`Flow: ${source} → ${target} = ${value}`);
    
    // Perform analytics or filtering
    analyzeFlow(source, target, value);
  };

  return (
    <SankeyComponent
      title="Track Link Flows"
      linkClick={onLinkClick}
    >
      {/* nodes and links */}
    </SankeyComponent>
  );
}
```

### Load Event

```tsx
function SankeyWithLoadEvent() {
  const onChartLoad = (args) => {
    console.log('Chart loaded, initializing features...');
    // Initialize tooltips, legends, etc.
  };

  const onChartLoaded = (args) => {
    console.log('Chart rendering complete');
    // Update UI, store reference
  };

  return (
    <SankeyComponent
      title="With Load Events"
      load={onChartLoad}
      loaded={onChartLoaded}
    >
      {/* nodes and links */}
    </SankeyComponent>
  );
}
```

## User Interactions - Highlighting

### Hover Highlighting

Highlighting for Sankey nodes and links is enabled by default. The highlight opacity for both nodes and links can be customized using the `highlightOpacity` and `inactiveOpacity` properties.

```tsx
import React, { useState } from 'react';

function SankeyWithHoverHighlight() {

  return (
    <SankeyComponent
      title="Hover to Highlight"
    >
      <SankeyNodesCollectionDirective>
        <SankeyNodeDirective
          id="A"
          label={{ text: 'Node A' }}
        />
        {/* More nodes */}
      </SankeyNodesCollectionDirective>
      <Inject services={[SankeyTooltip]} />
    </SankeyComponent>
  );
}

export default SankeyWithHoverHighlight;
```

## Best Practices

1. **Provide visual feedback** - Highlight selected items
2. **Keep tooltips concise** - Show relevant info without clutter
3. **Use consistent events** - Standard click patterns across app
4. **Handle edge cases** - Empty selections, multiple clicks
5. **Performance** - Avoid heavy operations in event handlers
6. **Mobile considerations** - Touch events instead of hover
7. **Accessibility** - Keyboard alternatives to mouse events
