# Labels and Positioning

## Table of contents

- [Label Configuration](#label-configuration)
  - [Label Settings Properties](#label-settings-properties)
  - [Global vs. Per-Node Labels](#global-vs-per-node-labels)
- [Node Labels](#node-labels)
  - [Basic Node Label](#basic-node-label)
  - [Styled Node Label](#styled-node-label)
  - [Label Visibility Control](#label-visibility-control)
- [Title and Subtitle](#title-and-subtitle)
  - [Basic Title and Subtitle](#basic-title-and-subtitle)
  - [Styled Title Example](#styled-title-example)
  - [Dynamic Titles](#dynamic-titles)
- [Label Formatting](#label-formatting)
  - [Number Formatting in Labels](#number-formatting-in-labels)
  - [Conditional Label Formatting](#conditional-label-formatting)
- [Handling Label Overflow](#handling-label-overflow)
  - [Strategy 1: Abbreviate Labels](#strategy-1-abbreviate-labels)
  - [Strategy 2: Increase Chart Height](#strategy-2-increase-chart-height)
  - [Strategy 3: Conditional Label Visibility](#strategy-3-conditional-label-visibility)
  - [Strategy 4: Use Tooltips Instead](#strategy-4-use-tooltips-instead)
  - [Complete Overflow Handling Example](#complete-overflow-handling-example)
- [Best Practices](#best-practices)

## Label Configuration

Labels provide text context for nodes and the overall diagram. Control visibility and positioning through `labelSettings`.

### Label Settings Properties

```tsx
<SankeyComponent
  labelSettings={{
    visible: true,          // Label text transparency
    fontSize: 12,              // Font size in pixels
    fontFamily: 'Arial',       // Font family
    fontWeight: 'normal'       // Font weight
  }}
>
  {/* nodes and links */}
</SankeyComponent>
```

### Global vs. Per-Node Labels

**Global Configuration:**
```tsx
<SankeyComponent
  labelSettings={{
    visible: true,
    fontSize: 14,
    fontFamily: 'Segoe UI'
  }}
>
  {/* All nodes use these settings */}
</SankeyComponent>
```

**Per-Node Customization:**
```tsx
<SankeyNodeDirective
  id="Node1"
  label={{
    text: 'Custom Label',
    fill: '#333',           // Text color
    fontSize: 14,
    textOpacity: 0.9
  }}
/>
```

## Node Labels

Each node can display text that identifies it in the diagram.

### Basic Node Label

```tsx
<SankeyNodeDirective
  id="Energy"
  label={{ text: 'Energy Input' }}
/>
```

### Styled Node Label

```tsx
<SankeyNodesCollectionDirective>
  <SankeyNodeDirective
    id="Source"
    label={{
      text: 'Data Source',
      fill: '#FFFFFF',        // Text color
      textOpacity: 1,
      fontSize: 13,
      fontFamily: 'Courier New',
      fontWeight: 'bold'
    }}
  />
  <SankeyNodeDirective
    id="Destination"
    label={{
      text: 'Output',
      fill: '#333333',
      fontSize: 12
    }}
  />
</SankeyNodesCollectionDirective>
```

### Label Visibility Control

Hide labels for specific nodes or based on conditions:

```tsx
import React, { useState } from 'react';
import {
  SankeyComponent, Inject, SankeyTooltip, SankeyLegend, SankeyExport,
  SankeyNodeDirective,
  SankeyNodesCollectionDirective,
  SankeyLinkDirective,
  SankeyLinksCollectionDirective
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";

function SankeyWithTogglableLabels() {
  const [showLabels, setShowLabels] = useState(true);

  return (
    <div>
      <button onClick={() => setShowLabels(!showLabels)}>
        Toggle Labels
      </button>
      
      <SankeyComponent
        width="90%"
        height="420px"
        title="Selective Labels"
        labelSettings={{ visible: showLabels }}
      >
        <SankeyNodesCollectionDirective>
          <SankeyNodeDirective id="A" label={{ text: 'Node A' }} />
          <SankeyNodeDirective id="B" label={{ text: 'Node B' }} />
          <SankeyNodeDirective id="C" label={{ text: 'Node C' }} />
        </SankeyNodesCollectionDirective>
        <SankeyLinksCollectionDirective>
          <SankeyLinkDirective sourceId="A" targetId="B" value={100} />
          <SankeyLinkDirective sourceId="B" targetId="C" value={80} />
        </SankeyLinksCollectionDirective>
        <Inject services={[SankeyTooltip, SankeyLegend]} />
      </SankeyComponent>
    </div>
  );
}

export default SankeyWithTogglableLabels;
ReactDOM.render(<SankeyWithTogglableLabels />, document.getElementById("charts"));
```

## Title and Subtitle

Provide context with chart title and subtitle displayed above the diagram.

### Basic Title and Subtitle

```tsx
<SankeyComponent
  width="90%"
  height="420px"
  title="Energy Flow 2024"
  subTitle="California Consumption by Sector"
>
  {/* nodes and links */}
</SankeyComponent>
```

### Styled Title Example

```tsx
<SankeyComponent
  width="90%"
  height="500px"
  title="Supply Chain Flow"
  subTitle="Product movement from suppliers to customers"
  titleStyle={{
    fontFamily: 'Arial',
    size: '18px',
    color: '#2E3440'
  }}
>
  {/* nodes and links */}
</SankeyComponent>
```

### Dynamic Titles

Update titles based on data or user selection:

```tsx
import React, { useState } from 'react';

function DynamicTitleSankey() {
  const [selectedYear, setSelectedYear] = useState(2024);

  const getTitle = (year) => {
    return `Energy Consumption ${year}`;
  };

  const getSubtitle = (year) => {
    return `Annual flow analysis for year ${year}`;
  };

  return (
    <div>
      <select onChange={(e) => setSelectedYear(parseInt(e.target.value))}>
        <option value={2022}>2022</option>
        <option value={2023}>2023</option>
        <option value={2024}>2024</option>
      </select>

      <SankeyComponent
        width="90%"
        height="420px"
        title={getTitle(selectedYear)}
        subTitle={getSubtitle(selectedYear)}
        key={selectedYear}
      >
        {/* nodes and links vary by year */}
      </SankeyComponent>
    </div>
  );
}

export default DynamicTitleSankey;
```

## Label Formatting

Format labels to enhance readability and information density.

### Number Formatting in Labels

```tsx
function formatFlow(value) {
  if (value >= 1000000) {
    return (value / 1000000).toFixed(1) + 'M';
  } else if (value >= 1000) {
    return (value / 1000).toFixed(1) + 'K';
  }
  return value.toString();
}

// Use in labels
<SankeyNodeDirective
  id="Input"
  label={{
    text: `Input: ${formatFlow(150000)}`
  }}
/>
```

### Conditional Label Formatting

Show different information based on node type:

```tsx
function getLabelText(nodeId, nodeType) {
  switch(nodeType) {
    case 'source':
      return `Source: ${nodeId}`;
    case 'processing':
      return `Process: ${nodeId}`;
    case 'destination':
      return `Output: ${nodeId}`;
    default:
      return nodeId;
  }
}

<SankeyNodeDirective
  id="A"
  label={{ text: getLabelText('A', 'source') }}
/>
```

## Handling Label Overflow

Labels can overflow when text is long or space is limited. Implement strategies to manage this.

### Strategy 1: Abbreviate Labels

Shorten long node names:

```tsx
function abbreviate(text, maxLength = 15) {
  if (text.length > maxLength) {
    return text.substring(0, maxLength - 3) + '...';
  }
  return text;
}

<SankeyNodeDirective
  id="LongNodeName"
  label={{ text: abbreviate('Very Long Process Name Here') }}
/>
```

### Strategy 2: Increase Chart Height

Give more vertical space to accommodate labels:

```tsx
import { Browser } from '@syncfusion/ej2-base';

<SankeyComponent
  width="90%"
  height={Browser.isDevice ? '700px' : '500px'}
  title="Sankey with More Space"
>
  {/* nodes and links */}
</SankeyComponent>
```

### Strategy 3: Conditional Label Visibility

Hide labels on small devices:

```tsx
import { Browser } from '@syncfusion/ej2-base';

<SankeyComponent
  width="90%"
  height={Browser.isDevice ? '600px' : '450px'}
  labelSettings={{
    visible: !Browser.isDevice  // Only show on desktop
  }}
>
  {/* nodes and links */}
</SankeyComponent>
```

### Strategy 4: Use Tooltips Instead

Move detailed information to tooltips:

```tsx
<SankeyComponent
  title="Energy Flow"
  labelSettings={{
    visible: true,
    fontSize: 10  // Smaller labels
  }}
  tooltip={{ enable: true }}
>
  <SankeyNodesCollectionDirective>
    <SankeyNodeDirective
      id="Node1"
      label={{ text: 'N1' }}  // Abbreviated
    />
    {/* Tooltip will show full name on hover */}
  </SankeyNodesCollectionDirective>
  <Inject services={[SankeyTooltip]} />
</SankeyComponent>
```

### Complete Overflow Handling Example

```tsx
import React, { useState } from 'react';
import { Browser } from '@syncfusion/ej2-base';
import {
  SankeyComponent, Inject, SankeyTooltip, SankeyLegend, SankeyExport,
  SankeyNodeDirective,
  SankeyNodesCollectionDirective,
  SankeyLinkDirective,
  SankeyLinksCollectionDirective
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";

function SmartLabelSankey() {
  const [labelMode, setLabelMode] = useState('auto');

  const nodes = [
    { id: 'Source1', fullName: 'Primary Data Source' },
    { id: 'Source2', fullName: 'Secondary Data Source' },
    { id: 'Process', fullName: 'Data Processing Pipeline' },
    { id: 'Output', fullName: 'Final Output' }
  ];

  const getDisplayLabel = (node) => {
    if (labelMode === 'full') return node.fullName;
    if (labelMode === 'abbreviated') {
      return node.fullName.substring(0, 10) + '...';
    }
    return node.id;
  };

  return (
    <div>
      <div>
        <label>Label Mode: </label>
        <select onChange={(e) => setLabelMode(e.target.value)}>
          <option value="auto">Auto</option>
          <option value="abbreviated">Abbreviated</option>
          <option value="full">Full</option>
        </select>
      </div>

      <SankeyComponent
        width="90%"
        height={Browser.isDevice ? '700px' : '500px'}
        labelSettings={{
          visible: labelMode !== 'hidden',
          fontSize: labelMode === 'full' ? 10 : 12
        }}
      >
        <SankeyNodesCollectionDirective>
          {nodes.map(node => (
            <SankeyNodeDirective
              key={node.id}
              id={node.id}
              label={{ text: getDisplayLabel(node) }}
            />
          ))}
        </SankeyNodesCollectionDirective>
        <SankeyLinksCollectionDirective>
          <SankeyLinkDirective sourceId="Source1" targetId="Process" value={100} />
          <SankeyLinkDirective sourceId="Source2" targetId="Process" value={75} />
          <SankeyLinkDirective sourceId="Process" targetId="Output" value={150} />
        </SankeyLinksCollectionDirective>
        <Inject services={[SankeyTooltip, SankeyLegend]} />
      </SankeyComponent>
    </div>
  );
}

export default SmartLabelSankey;
ReactDOM.render(<SmartLabelSankey />, document.getElementById("charts"));
```

## Best Practices

1. **Keep labels concise** - Aim for 1-3 words per label
2. **Use consistent formatting** - Apply styles uniformly
3. **Leverage tooltips** - Show full details on hover
4. **Test on mobile** - Ensure labels work on small screens
5. **Contrast matters** - Use readable label colors against backgrounds
6. **Group related labels** - Similar node types should have similar styling
