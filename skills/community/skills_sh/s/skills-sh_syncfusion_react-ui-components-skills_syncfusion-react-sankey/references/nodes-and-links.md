# Nodes and Links Configuration

## Table of contents

- [Node Structure](#node-structure)
  - [Node Properties](#node-properties)
  - [Essential Properties](#essential-properties)
  - [Basic Node Example](#basic-node-example)
  - [Node Label Configuration](#node-label-configuration)
- [Link Structure](#link-structure)
  - [Link Properties](#link-properties)
  - [Essential Properties](#essential-properties-1)
  - [Basic Link Example](#basic-link-example)
- [Data Binding Patterns](#data-binding-patterns)
  - [Pattern 1: Static Nodes and Links](#pattern-1-static-nodes-and-links)
  - [Pattern 2: Dynamic Nodes and Links from State](#pattern-2-dynamic-nodes-and-links-from-state)
  - [Pattern 3: Data from API](#pattern-3-data-from-api)
- [Node Positioning](#node-positioning)
  - [Offset for Alignment](#offset-for-alignment)
  - [Practical Example: Multi-Level Flow](#practical-example-multi-level-flow)
- [Link Styling](#link-styling)
  - [Link Style Properties](#link-style-properties)
  - [Color Type Options](#color-type-options)
  - [Link Styling Example](#link-styling-example)
- [Performance Optimization](#performance-optimization)
  - [Large Dataset Handling](#large-dataset-handling)
  - [Tips for Better Performance](#tips-for-better-performance)

## Node Structure

Nodes represent categories or stages in your flow diagram. Each node is a destination/source point for links.

### Node Properties

```tsx
<SankeyNodeDirective
  id="nodeIdentifier"                // Unique identifier (required)
  label={{ text: 'Display Label' }} // Label configuration
  offset={0}                         // Position offset
  color="blue"                       // Node fill color (optional)
/>
```

### Essential Properties

| Property | Type | Purpose |
|----------|------|---------|
| `id` | string | Unique identifier for referencing in links |
| `label` | object | Label configuration with text and styling |
| `offset` | number | Vertical positioning offset in pixels |
| `color` | string | Node fill color (hex or named color) |

### Basic Node Example

```tsx
<SankeyNodesCollectionDirective>
  <SankeyNodeDirective 
    id="Source1" 
    label={{ text: 'Data Source' }}
  />
  <SankeyNodeDirective 
    id="Processing" 
    label={{ text: 'Process Layer' }}
  />
  <SankeyNodeDirective 
    id="Output" 
    label={{ text: 'Output' }}
  />
</SankeyNodesCollectionDirective>
```

### Node Label Configuration

Customize node labels with detailed properties:

```tsx
<SankeyNodeDirective
  id="Node1"
  label={{
    text: 'Custom Label',
    fill: '#FFF',              // Label text color
    textOpacity: 1,
    fontSize: 12,
    fontFamily: 'Arial'
  }}
/>
```

## Link Structure

Links represent the flow between nodes with specific values representing the magnitude of flow.

### Link Properties

```tsx
<SankeyLinkDirective
  sourceId="source"      // Source node ID (required)
  targetId="target"      // Target node ID (required)
  value={100}            // Flow magnitude (required)
/>
```

### Essential Properties

| Property | Type | Purpose |
|----------|------|---------|
| `sourceId` | string | ID of the originating node |
| `targetId` | string | ID of the destination node |
| `value` | number | Flow quantity or weight |

### Basic Link Example

```tsx
<SankeyLinksCollectionDirective>
  <SankeyLinkDirective sourceId="A" targetId="B" value={100} />
  <SankeyLinkDirective sourceId="A" targetId="C" value={50} />
  <SankeyLinkDirective sourceId="B" targetId="D" value={80} />
</SankeyLinksCollectionDirective>
```

## Data Binding Patterns

### Pattern 1: Static Nodes and Links

Define all nodes and links declaratively:

```tsx
<SankeyComponent title="Energy Flow">
  <SankeyNodesCollectionDirective>
    <SankeyNodeDirective id="Solar" label={{ text: 'Solar' }} />
    <SankeyNodeDirective id="Wind" label={{ text: 'Wind' }} />
    <SankeyNodeDirective id="Grid" label={{ text: 'Grid' }} />
  </SankeyNodesCollectionDirective>
  <SankeyLinksCollectionDirective>
    <SankeyLinkDirective sourceId="Solar" targetId="Grid" value={450} />
    <SankeyLinkDirective sourceId="Wind" targetId="Grid" value={200} />
  </SankeyLinksCollectionDirective>
  <Inject services={[SankeyTooltip, SankeyLegend]} />
</SankeyComponent>
```

### Pattern 2: Dynamic Nodes and Links from State

Use React state to manage node and link data:

```tsx
import * as ReactDOM from "react-dom";
import React, { useState } from 'react';
import {
  SankeyComponent, Inject, SankeyTooltip, SankeyLegend,
  SankeyNodeDirective, SankeyNodesCollectionDirective,
  SankeyLinkDirective, SankeyLinksCollectionDirective
} from '@syncfusion/ej2-react-charts';

function DynamicSankey() {
  const [nodes] = useState([
    { id: 'A', label: { text: 'Source A' } },
    { id: 'B', label: { text: 'Source B' } },
    { id: 'Output', label: { text: 'Output' } }
  ]);

  const [links] = useState([
    { sourceId: 'A', targetId: 'Output', value: 100 },
    { sourceId: 'B', targetId: 'Output', value: 75 }
  ]);

  return (
    <SankeyComponent width="90%" height="420px" title="Dynamic Data">
      <SankeyNodesCollectionDirective>
        {nodes.map((node) => (
          <SankeyNodeDirective
            key={node.id}
            id={node.id}
            label={node.label}
          />
        ))}
      </SankeyNodesCollectionDirective>
      <SankeyLinksCollectionDirective>
        {links.map((link, index) => (
          <SankeyLinkDirective
            key={index}
            sourceId={link.sourceId}
            targetId={link.targetId}
            value={link.value}
          />
        ))}
      </SankeyLinksCollectionDirective>
      <Inject services={[SankeyTooltip, SankeyLegend]} />
    </SankeyComponent>
  );
}

export default DynamicSankey;
ReactDOM.render(<DynamicSankey />, document.getElementById("charts"));
```

### Pattern 3: Data from API

Fetch and update flow data from a remote source:

```tsx
import * as ReactDOM from "react-dom";
import React, { useState, useEffect } from 'react';
import {
  SankeyComponent, Inject, SankeyTooltip, SankeyLegend,
  SankeyNodeDirective, SankeyNodesCollectionDirective,
  SankeyLinkDirective, SankeyLinksCollectionDirective
} from '@syncfusion/ej2-react-charts';

function APIBasedSankey() {
  const [nodes, setNodes] = useState([]);
  const [links, setLinks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/sankey-data')
      .then(res => res.json())
      .then(data => {
        setNodes(data.nodes);
        setLinks(data.links);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to load data:', err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <SankeyComponent width="90%" height="420px" title="Live Data">
      <SankeyNodesCollectionDirective>
        {nodes.map((node) => (
          <SankeyNodeDirective
            key={node.id}
            id={node.id}
            label={node.label}
          />
        ))}
      </SankeyNodesCollectionDirective>
      <SankeyLinksCollectionDirective>
        {links.map((link, index) => (
          <SankeyLinkDirective
            key={index}
            sourceId={link.sourceId}
            targetId={link.targetId}
            value={link.value}
          />
        ))}
      </SankeyLinksCollectionDirective>
      <Inject services={[SankeyTooltip, SankeyLegend]} />
    </SankeyComponent>
  );
}

export default APIBasedSankey;
ReactDOM.render(<APIBasedSankey />, document.getElementById("charts"));
```

## Node Positioning

Control node vertical alignment using the `offset` property:

### Offset for Alignment

```tsx
<SankeyNodesCollectionDirective>
  <SankeyNodeDirective 
    id="Top" 
    label={{ text: 'Top' }}
    offset={-100}  // Negative value: pull upward
  />
  <SankeyNodeDirective 
    id="Middle" 
    label={{ text: 'Middle' }}
    offset={0}     // No offset: center
  />
  <SankeyNodeDirective 
    id="Bottom" 
    label={{ text: 'Bottom' }}
    offset={100}   // Positive value: push downward
  />
</SankeyNodesCollectionDirective>
```

### Practical Example: Multi-Level Flow

Position nodes for a three-layer flow:

```tsx
<SankeyComponent width="90%" height="600px">
  <SankeyNodesCollectionDirective>
    {/* Input Layer */}
    <SankeyNodeDirective id="Input1" offset={-80} />
    <SankeyNodeDirective id="Input2" offset={-40} />
    
    {/* Processing Layer */}
    <SankeyNodeDirective id="Process" offset={0} />
    
    {/* Output Layer */}
    <SankeyNodeDirective id="Output1" offset={-40} />
    <SankeyNodeDirective id="Output2" offset={40} />
  </SankeyNodesCollectionDirective>
  <SankeyLinksCollectionDirective>
    {/* Links between layers */}
  </SankeyLinksCollectionDirective>
  <Inject services={[SankeyTooltip, SankeyLegend]} />
</SankeyComponent>
```

## Link Styling

### Link Style Properties

Control link appearance globally or per-link:

```tsx
<SankeyComponent
  linkStyle={{
    opacity: 0.6,           // Link transparency (0-1)
    curvature: 0.55,        // Link curve intensity (0-1)
    colorType: 'Source'     // 'Source' or other color strategy
  }}
>
  {/* nodes and links */}
</SankeyComponent>
```

### Color Type Options

| Option | Behavior |
|--------|----------|
| `'Source'` | Links inherit color from source node |
| `'Target'` | Links inherit color from target node |
| Custom hex | Static color for all links |

### Link Styling Example

```tsx
<SankeyComponent
  title="Styled Links"
  linkStyle={{
    opacity: 0.5,
    curvature: 0.7,
    colorType: 'Source'
  }}
>
  <SankeyNodesCollectionDirective>
    <SankeyNodeDirective id="A" color="#FF6B6B" />
    <SankeyNodeDirective id="B" color="#4ECDC4" />
    <SankeyNodeDirective id="C" />
  </SankeyNodesCollectionDirective>
  <SankeyLinksCollectionDirective>
    <SankeyLinkDirective sourceId="A" targetId="C" value={100} />
    <SankeyLinkDirective sourceId="B" targetId="C" value={75} />
  </SankeyLinksCollectionDirective>
  <Inject services={[SankeyTooltip, SankeyLegend]} />
</SankeyComponent>
```

## Performance Optimization

### Large Dataset Handling

When dealing with hundreds of nodes or links:

1. **Lazy Load Data** - Load nodes/links in batches
2. **Virtual Scrolling** - For cases with many items
3. **Simplify Rendering** - Disable unnecessary features

```tsx
function LargeDatasetSankey() {
  const [displayNodes, setDisplayNodes] = useState([]);
  const [displayLinks, setDisplayLinks] = useState([]);

  useEffect(() => {
    // Load first 100 nodes
    const allNodes = generateAllNodes(1000);
    setDisplayNodes(allNodes.slice(0, 100));
    
    const allLinks = generateAllLinks(1000);
    setDisplayLinks(allLinks.slice(0, 200));
  }, []);

  return (
    <SankeyComponent
      width="90%"
      height="600px"
    >
      <SankeyNodesCollectionDirective>
        {displayNodes.map(node => (
          <SankeyNodeDirective key={node.id} {...node} />
        ))}
      </SankeyNodesCollectionDirective>
      <SankeyLinksCollectionDirective>
        {displayLinks.map((link, i) => (
          <SankeyLinkDirective key={i} {...link} />
        ))}
      </SankeyLinksCollectionDirective>
    </SankeyComponent>
  );
}
```

### Tips for Better Performance

- Use React keys properly for list rendering
- Avoid inline object creation in render methods
- Consider memoization for expensive calculations
- Limit link count per node to maintain responsiveness
