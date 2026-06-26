# Legend and Display Options

## Table of Contents
- [Legend Configuration](#legend-configuration)
  - [Basic Legend Setup](#basic-legend-setup)
  - [Legend Properties](#legend-properties)
- [Legend Positioning](#legend-positioning)
  - [Bottom Position (Default)](#bottom-position-default)
  - [Top Position](#top-position)
  - [Right Position](#right-position)
  - [Left Position](#left-position)
- [Display Options and Styling](#display-options-and-styling)
  - [Show/Hide Legend Conditionally](#showhide-legend-conditionally)
  - [Legend with Border and Background](#legend-with-border-and-background)
  - [Styled Legend Text](#styled-legend-text)
- [Theming and Color Customization](#theming-and-color-customization)
  - [Node Color Assignment](#node-color-assignment)
  - [Color Schemes for Categories](#color-schemes-for-categories)
  - [Link Color Inheritance](#link-color-inheritance)
- [Responsive Display](#responsive-display)
  - [Mobile-Responsive Legend](#mobile-responsive-legend)
  - [Adaptive Display Configuration](#adaptive-display-configuration)
- [Display Modes](#display-modes)
  - [Compact Display](#compact-display)
  - [Full Information Display](#full-information-display)
  - [Interactive Display](#interactive-display)
- [Best Practices](#best-practices)

## Legend Configuration

The legend displays visual indicators for nodes in your Sankey diagram, helping users understand the flow representation.

### Basic Legend Setup

```tsx
<SankeyComponent
  width="90%"
  height="420px"
  title="Chart with Legend"
  legendSettings={{
    visible: true,        // Show legend
    position: 'Bottom'    // Legend position
  }}
>
  {/* nodes and links */}
  <Inject services={[SankeyLegend]} />
</SankeyComponent>
```

### Legend Properties

| Property | Type | Options |
|----------|------|---------|
| `visible` | boolean | `true` \| `false` |
| `position` | string | `'Top'` \| `'Bottom'` \| `'Left'` \| `'Right'` |
| `itemPadding` | number | Spacing between legend items (pixels) |
| `border` | object | Border configuration |
| `background` | string | Legend background color |
| `textStyle` | object | Text styling options |

## Legend Positioning

Position the legend based on your diagram layout and content flow.

### Bottom Position (Default)

```tsx
<SankeyComponent
  title="Energy Flow"
  legendSettings={{
    visible: true,
    position: 'Bottom',
    itemPadding: 8
  }}
>
  {/* nodes and links */}
</SankeyComponent>
```

**Best For:** Horizontal space availability, wide diagrams

### Top Position

```tsx
<SankeyComponent
  title="Process Flow"
  legendSettings={{
    visible: true,
    position: 'Top',
    itemPadding: 8
  }}
>
  {/* nodes and links */}
</SankeyComponent>
```

**Best For:** Mobile layouts, content below chart

### Right Position

```tsx
<SankeyComponent
  width="70%"
  height="500px"
  title="Vertical Flow"
  legendSettings={{
    visible: true,
    position: 'Right',
    itemPadding: 10
  }}
>
  {/* nodes and links */}
</SankeyComponent>
```

**Best For:** Tall diagrams with horizontal space

### Left Position

```tsx
<SankeyComponent
  width="70%"
  height="500px"
  title="RTL Support"
  legendSettings={{
    visible: true,
    position: 'Left',
    itemPadding: 10
  }}
>
  {/* nodes and links */}
</SankeyComponent>
```

**Best For:** Right-to-left layouts, RTL support

## Display Options and Styling

### Show/Hide Legend Conditionally

```tsx
import React, { useState } from 'react';

function SankeyWithLegendToggle() {
  const [showLegend, setShowLegend] = useState(true);

  return (
    <div>
      <button onClick={() => setShowLegend(!showLegend)}>
        {showLegend ? 'Hide' : 'Show'} Legend
      </button>

      <SankeyComponent
        width="90%"
        height="420px"
        title="Toggleable Legend"
        legendSettings={{
          visible: showLegend,
          position: 'Bottom'
        }}
      >
        {/* nodes and links */}
      </SankeyComponent>
    </div>
  );
}

export default SankeyWithLegendToggle;
```

### Legend with Border and Background

```tsx
<SankeyComponent
  legendSettings={{
    visible: true,
    position: 'Bottom',
    itemPadding: 8,
    border: {
      color: '#CCCCCC',
      width: 1
    },
    background: '#F5F5F5'
  }}
>
  {/* nodes and links */}
</SankeyComponent>
```

### Styled Legend Text

```tsx
<SankeyComponent
  legendSettings={{
    visible: true,
    position: 'Bottom',
    textStyle: {
      fontFamily: 'Arial',
      size: 12,
      bold: true,
      color: '#333333'
    }
  }}
>
  {/* nodes and links */}
</SankeyComponent>
```

## Theming and Color Customization

### Node Color Assignment

Assign colors to nodes for visual distinction:

```tsx
<SankeyNodesCollectionDirective>
  <SankeyNodeDirective 
    id="Solar"
    color="#FFD700"        // Gold
    label={{ text: 'Solar' }}
  />
  <SankeyNodeDirective 
    id="Wind"
    color="#87CEEB"        // Sky blue
    label={{ text: 'Wind' }}
  />
  <SankeyNodeDirective 
    id="Natural Gas"
    color="#FF6347"        // Tomato
    label={{ text: 'Natural Gas' }}
  />
  <SankeyNodeDirective 
    id="Grid"
    color="#32CD32"        // Lime green
    label={{ text: 'Grid' }}
  />
</SankeyNodesCollectionDirective>
```

### Color Schemes for Categories

Use consistent color schemes for different data categories:

```tsx
const energySources = {
  renewable: ['#FFD700', '#87CEEB', '#32CD32'],    // Gold, Sky blue, Lime
  fossil: ['#FF6347', '#8B4513', '#696969'],       // Red, Brown, Gray
  output: ['#FF69B4', '#00CED1', '#9370DB']        // Pink, Turquoise, Purple
};

<SankeyNodesCollectionDirective>
  <SankeyNodeDirective id="Solar" color={energySources.renewable[0]} />
  <SankeyNodeDirective id="Wind" color={energySources.renewable[1]} />
  <SankeyNodeDirective id="Coal" color={energySources.fossil[0]} />
  <SankeyNodeDirective id="Grid" color={energySources.output[0]} />
</SankeyNodesCollectionDirective>
```

### Link Color Inheritance

Configure how links inherit colors:

```tsx
<SankeyComponent
  linkStyle={{
    colorType: 'Source',      // Links use source node color
    opacity: 0.6,
    curvature: 0.55
  }}
>
  {/* nodes and links */}
</SankeyComponent>
```

## Responsive Display

Adapt legend and display options for different screen sizes.

### Mobile-Responsive Legend

```tsx
import { Browser } from '@syncfusion/ej2-base';

<SankeyComponent
  width="100%"
  height={Browser.isDevice ? '500px' : '420px'}
  legendSettings={{
    visible: true,
    position: Browser.isDevice ? 'Bottom' : 'Right',
    itemPadding: Browser.isDevice ? 4 : 8
  }}
>
  {/* nodes and links */}
</SankeyComponent>
```

### Adaptive Display Configuration

```tsx
import React from 'react';
import { Browser } from '@syncfusion/ej2-base';

function ResponsiveSankey() {
  const getDisplayConfig = () => {
    if (Browser.isDevice) {
      return {
        width: '100%',
        height: '600px',
        legendPosition: 'Bottom',
        legendVisible: true,
        labelVisible: false,
        tooltipEnabled: true
      };
    } else {
      return {
        width: '90%',
        height: '500px',
        legendPosition: 'Right',
        legendVisible: true,
        labelVisible: true,
        tooltipEnabled: true
      };
    }
  };

  const config = getDisplayConfig();

  return (
    <SankeyComponent
      width={config.width}
      height={config.height}
      labelSettings={{ visible: config.labelVisible }}
      legendSettings={{
        visible: config.legendVisible,
        position: config.legendPosition
      }}
      tooltip={{ enable: config.tooltipEnabled }}
    >
      {/* nodes and links */}
      <Inject services={[SankeyTooltip, SankeyLegend]} />
    </SankeyComponent>
  );
}

export default ResponsiveSankey;
```

## Display Modes

### Compact Display

Minimize visual elements for space constraints:

```tsx
<SankeyComponent
  width="100%"
  height="400px"
  title="Compact View"
  labelSettings={{
    visible: false        // Hide labels to save space
  }}
  legendSettings={{
    visible: false       // Hide legend
  }}
  tooltip={{ enable: false }}
>
  {/* nodes and links */}
</SankeyComponent>
```

### Full Information Display

Show all details for presentation or analysis:

```tsx
<SankeyComponent
  width="100%"
  height="600px"
  title="Detailed Energy Flow 2024"
  subTitle="Complete analysis by source and consumption sector"
  labelSettings={{
    visible: true,
    fontSize: 13
  }}
  legendSettings={{
    visible: true,
    position: 'Bottom',
    itemPadding: 10,
    border: { color: '#CCCCCC', width: 1 },
    background: '#F9F9F9'
  }}
  tooltip={{ enable: true }}
>
  {/* nodes and links */}
  <Inject services={[SankeyTooltip, SankeyLegend]} />
</SankeyComponent>
```

### Interactive Display

Allow users to control display options:

```tsx
import React, { useState } from 'react';
import * as ReactDOM from 'react-dom';
import {
  SankeyComponent,
  Inject,
  SankeyTooltip,
  SankeyLegend,
  SankeyExport,
  SankeyNodeDirective,
  SankeyNodesCollectionDirective,
  SankeyLinkDirective,
  SankeyLinksCollectionDirective,
} from '@syncfusion/ej2-react-charts';

function InteractiveSankey() {
  const [displayOptions, setDisplayOptions] = useState({
    showLegend: true,
    showLabels: true,
    showTooltips: true,
    legendPosition: 'Bottom',
  });

  const handleToggle = (option) => {
    setDisplayOptions((prev) => ({
      ...prev,
      [option]: !prev[option],
    }));
  };

  const handlePositionChange = (position) => {
    setDisplayOptions((prev) => ({
      ...prev,
      legendPosition: position,
    }));
  };

  return (
    <div>
      <div style={{ marginBottom: '20px' }}>
        <label>
          <input
            type="checkbox"
            checked={displayOptions.showLegend}
            onChange={() => handleToggle('showLegend')}
          />
          Show Legend
        </label>

        <label style={{ marginLeft: '15px' }}>
          <input
            type="checkbox"
            checked={displayOptions.showLabels}
            onChange={() => handleToggle('showLabels')}
          />
          Show Labels
        </label>

        <label style={{ marginLeft: '15px' }}>
          Legend Position:
          <select
            value={displayOptions.legendPosition}
            onChange={(e) => handlePositionChange(e.target.value)}
          >
            <option value="Top">Top</option>
            <option value="Bottom">Bottom</option>
            <option value="Left">Left</option>
            <option value="Right">Right</option>
          </select>
        </label>
      </div>

      <SankeyComponent
        width="90%"
        height="420px"
        title="Interactive Display"
        labelSettings={{ visible: displayOptions.showLabels }}
        legendSettings={{
          visible: displayOptions.showLegend,
          position: displayOptions.legendPosition,
        }}
      >
        <SankeyNodesCollectionDirective>
          <SankeyNodeDirective id="Solar" label={{ text: 'Solar' }} />
          <SankeyNodeDirective id="Generation" label={{ text: 'Generation' }} />
          <SankeyNodeDirective
            id="Consumption"
            label={{ text: 'Consumption' }}
          />
        </SankeyNodesCollectionDirective>
        <SankeyLinksCollectionDirective>
          <SankeyLinkDirective
            sourceId="Solar"
            targetId="Generation"
            value={450}
          />
          <SankeyLinkDirective
            sourceId="Generation"
            targetId="Consumption"
            value={400}
          />
        </SankeyLinksCollectionDirective>
        <Inject services={[SankeyTooltip, SankeyLegend]} />
      </SankeyComponent>
    </div>
  );
}

export default InteractiveSankey;
ReactDOM.render(<InteractiveSankey />, document.getElementById('charts'));
```

## Best Practices

1. **Choose appropriate position** - Consider available space and content flow
2. **Limit legend items** - Too many items reduce readability
3. **Consistent colors** - Use color schemes across related data
4. **Responsive positioning** - Adapt legend position for mobile
5. **Test visibility** - Ensure legend is readable on all devices
6. **Match theme** - Align legend styling with overall application theme
7. **Use meaningful labels** - Legend items should be self-explanatory
