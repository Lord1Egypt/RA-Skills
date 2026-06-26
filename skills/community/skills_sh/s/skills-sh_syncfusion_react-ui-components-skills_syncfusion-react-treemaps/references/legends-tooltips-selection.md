# Legends, Tooltips & Selection

## Table of Contents

- [Legend Configuration](#legend-configuration)
  - [Basic Legend Setup](#basic-legend-setup)
  - [Legend Positions](#legend-positions)
  - [Legend Customization](#legend-customization)
- [Tooltip Customization](#tooltip-customization)
  - [Basic Tooltip Setup](#basic-tooltip-setup)
  - [Tooltip Formats](#tooltip-formats)
  - [Tooltip Styling](#tooltip-styling)
  - [Template-Based Tooltips](#template-based-tooltips)
- [Selection and Highlight](#selection-and-highlight)
  - [Enable Selection](#enable-selection)
  - [Selection Modes](#selection-modes)
  - [Selection Types](#selection-types)
  - [Highlight (Hover) Effect](#highlight-hover-effect)
- [Interactive Features](#interactive-features)
  - [Combined Selection and Highlight](#combined-selection-and-highlight)
  - [Synchronized Legend and Selection](#synchronized-legend-and-selection)
- [Event Handling](#event-handling)
  - [Item Selected Event](#item-selected-event)
  - [Item Highlighted Event](#item-highlighted-event)
  - [Item Click Event](#item-click-event)
- [Advanced Interactions](#advanced-interactions)
  - [Pattern 1: Click to Focus on Category](#pattern-1-click-to-focus-on-category)
  - [Pattern 2: Show Details on Selection](#pattern-2-show-details-on-selection)
  - [Pattern 3: Conditional Highlighting by Criteria](#pattern-3-conditional-highlighting-by-criteria)
  - [Pattern 4: Cross-Filter with Legend](#pattern-4-cross-filter-with-legend)
- [Best Practices](#best-practices)
- [Common Issues](#common-issues)
- [Next Steps](#next-steps)

## Legend Configuration

Legends display item categories or ranges to help users interpret the TreeMap.

### Basic Legend Setup

```jsx
import { TreeMapComponent, Inject } from '@syncfusion/ej2-react-treemap';
import { TreeMapLegend } from '@syncfusion/ej2-react-treemap';

const data = [
  { Car: 'Mustang', Brand: 'Ford', Count: 232 },
  { Car: 'Swift', Brand: 'Maruti', Count: 143 },
  { Car: 'A3 Cabriolet', Brand: 'Audi', Count: 123 }
];

<TreeMapComponent
  dataSource={data}
  equalColorValuePath="Brand"
  leafItemSettings={{
    colorMapping: [
      { value: 'Ford', color: '#3498DB' },
      { value: 'Maruti', color: '#E74C3C' },
      { value: 'Audi', color: '#2ECC71' }
    ]
  }}
  legendSettings={{
    visible: true,
    position: 'Bottom'
  }}
>
  <Inject services={[TreeMapLegend]} />
</TreeMapComponent>
```

### Legend Positions

```jsx
// Top position
legendSettings={{ visible: true, position: 'Top' }}

// Bottom position (default for most charts)
legendSettings={{ visible: true, position: 'Bottom' }}

// Left position
legendSettings={{ visible: true, position: 'Left' }}

// Right position
legendSettings={{ visible: true, position: 'Right' }}
```

### Legend Customization

```jsx
<TreeMapComponent
  legendSettings={{
    visible: true,
    position: 'Right',
    height: '200px',
    width: '200px',
    labelDisplayMode: 'Trim',  // Truncate long labels
    title: {text: 'Brands'}
  }}
/>
```

## Tooltip Customization

Tooltips display detailed information when hovering over items.

### Basic Tooltip Setup

```jsx
import { TreeMapTooltip } from '@syncfusion/ej2-react-treemap';

<TreeMapComponent
  dataSource={data}
  tooltipSettings={{
    visible: true,
    format: '${Item}: ${Value} units'
  }}
>
  <Inject services={[TreeMapTooltip]} />
</TreeMapComponent>
```

### Tooltip Formats

```jsx
// Simple format
tooltipSettings={{
  visible: true,
  format: '${Item}'
}}

// Multi-line format
tooltipSettings={{
  visible: true,
  format: '${Item}\nValue: ${Value}\nCategory: ${Category}'
}}

// With labels
tooltipSettings={{
  visible: true,
  format: 'Item: ${Item}<br>Sales: ${Sales}<br>Region: ${Region}'
}}
```

### Tooltip Styling

```jsx
tooltipSettings={{
  visible: true,
  format: '${Item}: ${Value}',
  textStyle: {
    fontFamily: 'Arial',
    fontSize: '12px',
    color: '#FFFFFF'
  },
  borderStyle: {
    color: '#333',
    width: 1
  },
  backgroundColor: '#000000'
}}
```

### Template-Based Tooltips

```jsx
export function TemplateTooltip() {
  const tooltipTemplate = (props) => {
    return (
      <div style={{
        padding: '10px',
        backgroundColor: '#f0f0f0',
        borderRadius: '4px'
      }}>
        <div style={{ fontWeight: 'bold' }}>
          {props.Item}
        </div>
        <div>
          Sales: ${props.Value}
        </div>
        <div style={{ fontSize: '12px', color: '#666' }}>
          {props.Category}
        </div>
      </div>
    );
  };

  return (
    <TreeMapComponent
      dataSource={data}
      tooltipSettings={{
        visible: true,
        template: tooltipTemplate
      }}
    >
      <Inject services={[TreeMapTooltip]} />
    </TreeMapComponent>
  );
}
```

## Selection and Highlight

Allow users to select and highlight TreeMap items.

### Enable Selection

```jsx
import { TreeMapSelection } from '@syncfusion/ej2-react-treemap';

<TreeMapComponent
  dataSource={data}
  selectionSettings={{
    mode: 'Item',         // Select individual items
    fill: '#FF6B6B',      // Selection fill color
    border: {
      color: '#333',
      width: 2
    }
  }}
>
  <Inject services={[TreeMapSelection]} />
</TreeMapComponent>
```

### Selection Modes

| Mode | Behavior |
|------|----------|
| `Item` | Click item to select |
| `Parent` | Click parent to select all children |
| `Group` | Click to select related group |

### Selection Types

```jsx
// Single selection
selectionSettings={{ type: 'Single' }}

// Multiple selection
selectionSettings={{ type: 'Multiple' }}
```

### Highlight (Hover) Effect

```jsx
import { TreeMapHighlight } from '@syncfusion/ej2-react-treemap';

<TreeMapComponent
  dataSource={data}
  highlightSettings={{
    enable: true,
    fill: '#FFD700',      // Highlight color
    border: {
      color: '#333',
      width: 2
    },
    opacity: '0.8'
  }}
>
  <Inject services={[TreeMapHighlight]} />
</TreeMapComponent>
```

## Interactive Features

### Combined Selection and Highlight

```jsx
export function InteractiveTreeMap() {
  return (
    <TreeMapComponent
      dataSource={data}
      selectionSettings={{
        mode: 'Item',
        fill: '#4ECDC4'
      }}
      highlightSettings={{
        enable: true,
        fill: '#FFD700',
        opacity: '0.7'
      }}
      legendSettings={{
        visible: true,
        position: 'Right'
      }}
      tooltipSettings={{
        visible: true,
        format: '${Item}: ${Value}'
      }}
    >
      <Inject services={[
        TreeMapSelection,
        TreeMapHighlight,
        TreeMapLegend,
        TreeMapTooltip
      ]} />
    </TreeMapComponent>
  );
}
```

### Synchronized Legend and Selection

```jsx
export function SynchronizedSelection() {
  const [selectedBrand, setSelectedBrand] = React.useState(null);

  const handleItemSelected = (args) => {
    const brand = args.item?.Brand;
    setSelectedBrand(brand);
  };

  return (
    <TreeMapComponent
      dataSource={data}
      equalColorValuePath="Brand"
      onItemSelected={handleItemSelected}
      selectionSettings={{
        mode: 'Item',
        type: 'Multiple',
        fill: '#FF6B6B'
      }}
      legendSettings={{
        visible: true
      }}
    >
      <Inject services={[TreeMapSelection, TreeMapLegend]} />
    </TreeMapComponent>
  );
}
```

## Event Handling

### Item Selected Event

```jsx
export function HandleItemSelection() {
  const handleItemSelected = (args) => {
    console.log('Selected item:', args.item);
    console.log('Index:', args.itemIndex);
    // Update external state or trigger action
  };

  return (
    <TreeMapComponent
      dataSource={data}
      onItemSelected={handleItemSelected}
      selectionSettings={{
        enable: true
      }}
    >
      <Inject services={[TreeMapSelection]} />
    </TreeMapComponent>
  );
}
```

### Item Highlighted Event

```jsx
export function HandleItemHighlight() {
  const handleItemHighlight = (args) => {
    console.log('Highlighted item:', args.item?.label);
    // Could use to show details panel
  };

  return (
    <TreeMapComponent
      dataSource={data}
      onItemHighlight={handleItemHighlight}
      highlightSettings={{
        enable: true,
        fill: '#FFD700'
      }}
    >
      <Inject services={[TreeMapHighlight]} />
    </TreeMapComponent>
  );
}
```

### Item Click Event

```jsx
export function HandleItemClick() {
  const [clickedItem, setClickedItem] = React.useState(null);

  const handleItemClick = (args) => {
    setClickedItem({
      label: args.item?.label,
      value: args.item?.value,
      timestamp: new Date()
    });
  };

  return (
    <div>
      <TreeMapComponent
        dataSource={data}
        onItemClick={handleItemClick}
      />
      {clickedItem && (
        <div>
          Last clicked: {clickedItem.label} ({clickedItem.value})
        </div>
      )}
    </div>
  );
}
```

## Advanced Interactions

### Pattern 1: Click to Focus on Category

```jsx
export function FocusOnCategory() {
  const [focusCategory, setFocusCategory] = React.useState(null);
  const treeMapRef = React.useRef(null);

  const handleItemClick = (args) => {
    const category = args.item?.Brand;
    setFocusCategory(category);
    
    // Highlight only items from selected category
    const filtered = data.filter(item => item.Brand === category);
  };

  return (
    <TreeMapComponent
      ref={treeMapRef}
      dataSource={data}
      onItemClick={handleItemClick}
      selectionSettings={{
       enable: true
      }}
    >
      <Inject services={[TreeMapSelection]} />
    </TreeMapComponent>
  );
}
```

### Pattern 2: Show Details on Selection

```jsx
export function ShowDetailsPanel() {
  const [selectedItem, setSelectedItem] = React.useState(null);

  const handleItemSelected = (args) => {
    setSelectedItem({
      name: args.item?.label,
      value: args.item?.value,
      category: args.item?.Brand,
      details: args.item__
    });
  };

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '20px' }}>
      <TreeMapComponent
        dataSource={data}
        onItemSelected={handleItemSelected}
        selectionSettings={{ enable: true }}
      >
        <Inject services={[TreeMapSelection]} />
      </TreeMapComponent>
      
      {selectedItem && (
        <div style={{
          padding: '20px',
          border: '1px solid #ccc',
          borderRadius: '4px'
        }}>
          <h3>{selectedItem.name}</h3>
          <p>Value: {selectedItem.value}</p>
          <p>Category: {selectedItem.category}</p>
        </div>
      )}
    </div>
  );
}
```

### Pattern 3: Conditional Highlighting by Criteria

```jsx
export function ConditionalHighlight() {
  const handleItemHighlight = (args) => {
    const value = args.item?.value;
    
    // Change highlight color based on value
    if (value > 5000) {
      args.highlightSettings.fill = '#27AE60';  // Green for high
    } else if (value > 2000) {
      args.highlightSettings.fill = '#F39C12';  // Orange for medium
    } else {
      args.highlightSettings.fill = '#E74C3C';  // Red for low
    }
  };

  return (
    <TreeMapComponent
      dataSource={data}
      onItemHighlight={handleItemHighlight}
      highlightSettings={{ enable: true }}
    >
      <Inject services={[TreeMapHighlight]} />
    </TreeMapComponent>
  );
}
```

### Pattern 4: Cross-Filter with Legend

```jsx
export function CrossFilterWithLegend() {
  const filteredData = selectedBrands.size === 0 
    ? data 
    : data.filter(item => selectedBrands.has(item.Brand));

  return (
    <TreeMapComponent
      dataSource={filteredData}
      legendSettings={{
        visible: true,
        mode: 'Interactive'  // Click legend to filter
      }}
    >
      <Inject services={[TreeMapLegend]} />
    </TreeMapComponent>
  );
}
```

## Best Practices

1. **Legends:** Always include legends when using color mapping
2. **Tooltips:** Provide detailed information on hover
3. **Selection:** Clear visual feedback when items selected
4. **Highlight:** Subtle highlight effect to guide users
5. **Mobile:** Ensure interactions work on touch devices
6. **Accessibility:** Provide keyboard navigation alternatives

## Common Issues

**Issue:** Legend not showing
- **Solution:** Ensure TreeMapLegend service injected and legendSettings.visible = true

**Issue:** Tooltip not appearing
- **Solution:** Check TreeMapTooltip service injected, verify format property

**Issue:** Selection not working
- **Solution:** Inject TreeMapSelection service, verify selectionSettings configured

## Next Steps

- **Drill-Down:** See [drilldown.md](drilldown.md) for hierarchical navigation
- **Color Mapping:** See [color-mapping.md](color-mapping.md) for visual strategies
- **Customization:** See [customization-accessibility.md](customization-accessibility.md) for advanced styling
