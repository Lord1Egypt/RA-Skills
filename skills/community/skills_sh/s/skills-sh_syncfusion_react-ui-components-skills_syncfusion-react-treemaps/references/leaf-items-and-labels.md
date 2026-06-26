# Leaf Items, Labels & Templates

## Table of Contents

- [Leaf Item Configuration](#leaf-item-configuration)
  - [Basic Configuration](#basic-configuration)
  - [Core Leaf Item Properties](#core-leaf-item-properties)
- [Label Positioning](#label-positioning)
  - [Available Positions](#available-positions)
  - [Position Examples](#position-examples)
  - [Choosing Label Position](#choosing-label-position)
- [Data Labels and Formatting](#data-labels-and-formatting)
  - [Simple Label Format](#simple-label-format)
  - [Multi-Line Labels](#multi-line-labels)
  - [Calculated Properties in Label](#calculated-properties-in-label)
  - [Currency and Number Formatting](#currency-and-number-formatting)
- [Label Templates](#label-templates)
  - [Template-Based Label](#template-based-label)
  - [Rich Content Template](#rich-content-template)
- [Text Wrapping & Overflow](#text-wrapping--overflow)
  - [Word Wrapping](#word-wrapping)
  - [Wrapping Options](#wrapping-options)
  - [Handling Small Rectangles](#handling-small-rectangles)
- [Border and Fill Customization](#border-and-fill-customization)
  - [Individual Item Styling](#individual-item-styling)
  - [Border Configuration](#border-configuration)
  - [Gradient Borders for Hierarchy Levels](#gradient-borders-for-hierarchy-levels)
- [Advanced Customization](#advanced-customization)
  - [Pattern 1: Size-Responsive Font](#pattern-1-size-responsive-font)
  - [Pattern 2: Highlight Important Items](#pattern-2-highlight-important-items)
  - [Pattern 3: Icon-Based Labels](#pattern-3-icon-based-labels)
  - [Pattern 4: Percentage Display](#pattern-4-percentage-display)
- [Best Practices](#best-practices)
- [Common Issues](#common-issues)
- [Next Steps](#next-steps)

## Leaf Item Configuration

Leaf items are the innermost/lowest-level items in the TreeMap hierarchy. Configure them with `leafItemSettings`.

### Basic Configuration

```jsx
import { TreeMapComponent } from '@syncfusion/ej2-react-treemap';

const data = [
  { Fruit: 'Apple', Count: 5000 },
  { Fruit: 'Mango', Count: 3000 },
  { Fruit: 'Orange', Count: 2300 }
];

<TreeMapComponent
  dataSource={data}
  weightValuePath="Count"
  leafItemSettings={{
    labelPath: 'Fruit',        // Display property
    fill: '#FF6B6B',           // Background color
    border: {
      color: '#333',
      width: 2
    }
  }}
/>
```

### Core Leaf Item Properties

| Property | Type | Purpose |
|----------|------|---------|
| `labelPath` | string | Data property to display as label |
| `fill` | string | Background color of item |
| `labelFormat` | string | Format template for label |
| `border` | object | Border configuration |
| `labelPosition` | string | Label placement position |
| `labelFontStyle` | object | Font styling for labels |

## Label Positioning

Control where labels appear within rectangles.

### Available Positions

```jsx
const positions = [
  'TopLeft',      // Top-left corner
  'TopCenter',    // Top center
  'TopRight',     // Top-right corner
  'CenterLeft',   // Middle left
  'Center',       // Center (default)
  'CenterRight',  // Middle right
  'BottomLeft',   // Bottom-left corner
  'BottomCenter', // Bottom center
  'BottomRight'   // Bottom-right corner
];
```

### Position Examples

```jsx
const data = [
  { Item: 'A', Value: 100 },
  { Item: 'B', Value: 200 }
];

// Top-left positioning
<TreeMapComponent
  dataSource={data}
  leafItemSettings={{
    labelPath: 'Item',
    labelPosition: 'TopLeft'
  }}
/>

// Center positioning (default)
<TreeMapComponent
  dataSource={data}
  leafItemSettings={{
    labelPath: 'Item',
    labelPosition: 'Center'
  }}
/>

// Bottom-right positioning
<TreeMapComponent
  dataSource={data}
  leafItemSettings={{
    labelPath: 'Item',
    labelPosition: 'BottomRight'
  }}
/>
```

### Choosing Label Position

- **Center:** Best for balanced rectangles
- **TopLeft/TopRight:** Good for wide rectangles
- **BottomLeft/BottomRight:** For hierarchical visualization
- **CenterLeft/CenterRight:** For tall rectangles

## Data Labels and Formatting

Format labels to display multiple data properties:

### Simple Label Format

```jsx
const salesData = [
  { Region: 'North', Sales: 45000 },
  { Region: 'South', Sales: 28000 }
];

<TreeMapComponent
  dataSource={salesData}
  weightValuePath="Sales"
  leafItemSettings={{
    labelFormat: '${Region}'  // Only region name
  }}
/>
```

### Multi-Line Labels

```jsx
const productData = [
  { Product: 'Laptop', Sales: 2500, Profit: 800 },
  { Product: 'Phone', Sales: 3200, Profit: 1200 }
];

<TreeMapComponent
  dataSource={productData}
  leafItemSettings={{
    labelFormat: '${Product}\n${Sales}',  // Product on line 1, Sales on line 2
    labelFontStyle: {
      size: '14px',
      fontFamily: 'Arial'
    }
  }}
/>
```

### Calculated Properties in Label

```jsx
<TreeMapComponent
  dataSource={data}
  leafItemSettings={{
    labelFormat: '${Item}: ${Value} units'
  }}
/>
```

### Currency and Number Formatting

```jsx
const data = [
  { Category: 'Electronics', Revenue: 125000.50 },
  { Category: 'Clothing', Revenue: 87500.25 }
];

<TreeMapComponent
  dataSource={data}
  leafItemSettings={{
    labelFormat: '${Category}\n$${Revenue}'  // Dollar sign prefix
  }}
/>
```

## Label Templates

Use custom templates for complex label rendering:

### Template-Based Label

```jsx
export function TemplateBasedLabels() {
  const labelTemplate = (props) => {
    return (
      <div style={{
        padding: '5px',
        textAlign: 'center',
        fontSize: '12px'
      }}>
        <div style={{ fontWeight: 'bold' }}>
          {props.label}
        </div>
        <div style={{ fontSize: '10px', color: '#666' }}>
          {props.value}
        </div>
      </div>
    );
  };

  return (
    <TreeMapComponent
      dataSource={data}
      leafItemSettings={{
        labelTemplate: labelTemplate
      }}
    />
  );
}
```

### Rich Content Template

```jsx
export function RichLabelTemplate() {
  const data = [
    { Item: 'Product A', Sales: 2500, Growth: '+12%' },
    { Item: 'Product B', Sales: 3200, Growth: '+8%' }
  ];

  const labelTemplate = (props) => {
    const isGrowing = props.Growth?.includes('+');
    return (
      <div style={{
        width: '100%',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        color: 'white'
      }}>
        <div style={{ fontSize: '14px', fontWeight: 'bold' }}>
          {props.Item}
        </div>
        <div style={{ fontSize: '12px' }}>
          ${props.Sales}
        </div>
        <div style={{
          fontSize: '11px',
          color: isGrowing ? '#90EE90' : '#FFB6C6'
        }}>
          {props.Growth}
        </div>
      </div>
    );
  };

  return (
    <TreeMapComponent
      dataSource={data}
      leafItemSettings={{
        labelTemplate: labelTemplate
      }}
    />
  );
}
```

## Text Wrapping & Overflow

Control how labels handle overflow in small rectangles:

### Word Wrapping

```jsx
<TreeMapComponent
  dataSource={data}
  leafItemSettings={{
    labelPath: 'Item',
    interSectAction: 'WrapByWord'  // Wrap text to next line
  }}
/>
```

### Wrapping Options

| Option | Behavior |
|--------|----------|
| `None` | No wrapping, may overflow |
| `WrapByWord` | Wrap to next line at word boundaries |
| `Wrap` | Wrap at any character |
| `Trim` | Truncate with ellipsis (...) |

### Handling Small Rectangles

```jsx
<TreeMapComponent
  dataSource={data}
  leafItemSettings={{
    labelFormat: '${Item}: ${Value}',
    interSectAction: 'WrapByWord',  // Wrap if too long
    labelFontStyle: {
      size: '12px'
    }
  }}
/>
```

## Border and Fill Customization

Customize appearance of leaf items:

### Individual Item Styling

```jsx
const data = [
  { Item: 'A', Value: 100, Color: '#FF6B6B', BorderColor: '#333' },
  { Item: 'B', Value: 200, Color: '#4ECDC4', BorderColor: '#333' }
];

<TreeMapComponent
  dataSource={data}
  leafItemSettings={{
    labelPath: 'Item',
    fill: '#default_color',
    border: {
      color: '#border_default',
      width: 1
    }
  }}
/>
```

### Border Configuration

```jsx
<TreeMapComponent
  dataSource={data}
  leafItemSettings={{
    labelPath: 'Item',
    border: {
      color: '#333',      // Border color
      width: 2,           // Border width in pixels
    }
  }}
/>
```

### Gradient Borders for Hierarchy Levels

```jsx
import { LevelsDirective, LevelDirective } from '@syncfusion/ej2-react-treemap';

<TreeMapComponent
  dataSource={hierarchicalData}
>
  <LevelsDirective>
    <LevelDirective 
      groupPath="Category"
      border={{ color: '#999', width: 1 }}
    />
    <LevelDirective 
      groupPath="Type"
      border={{ color: '#CCC', width: 0.5 }}
    />
  </LevelsDirective>
</TreeMapComponent>
```

## Advanced Customization

### Pattern 1: Size-Responsive Font

Adjust font size based on rectangle size:

```jsx
export function ResponsiveFontSize() {
  const labelTemplate = (props) => {
    // Larger rectangles get larger fonts
    const fontSize = props.value > 3000 ? '16px' : '12px';
    
    return (
      <div style={{ fontSize }}>
        {props.label}
      </div>
    );
  };

  return (
    <TreeMapComponent
      dataSource={data}
      leafItemSettings={{
        labelTemplate: labelTemplate
      }}
    />
  );
}
```

### Pattern 2: Highlight Important Items

```jsx
export function HighlightImportantItems() {
  const labelTemplate = (props) => {
    const isImportant = props.value > 5000;
    
    return (
      <div style={{
        fontWeight: isImportant ? 'bold' : 'normal',
        fontSize: isImportant ? '14px' : '12px',
        color: isImportant ? '#FFF' : '#333'
      }}>
        {props.label}
      </div>
    );
  };

  return (
    <TreeMapComponent
      dataSource={data}
      leafItemSettings={{
        labelTemplate: labelTemplate
      }}
    />
  );
}
```

### Pattern 3: Icon-Based Labels

```jsx
export function IconLabels() {
  const categoryIcons = {
    'Electronics': '📱',
    'Clothing': '👕',
    'Books': '📖',
    'Furniture': '🪑'
  };

  const labelTemplate = (props) => {
    const icon = categoryIcons[props.Category] || '📦';
    
    return (
      <div style={{ textAlign: 'center' }}>
        <div style={{ fontSize: '20px' }}>{icon}</div>
        <div style={{ fontSize: '11px' }}>
          {props.Category}
        </div>
      </div>
    );
  };

  return (
    <TreeMapComponent
      dataSource={data}
      leafItemSettings={{
        labelTemplate: labelTemplate
      }}
    />
  );
}
```

### Pattern 4: Percentage Display

```jsx
export function PercentageLabels() {
  const totalValue = data.reduce((sum, item) => sum + item.value, 0);

  const labelTemplate = (props) => {
    const percentage = ((props.value / totalValue) * 100).toFixed(1);
    
    return (
      <div style={{ textAlign: 'center' }}>
        <div style={{ fontSize: '14px', fontWeight: 'bold' }}>
          {percentage}%
        </div>
        <div style={{ fontSize: '10px' }}>
          {props.label}
        </div>
      </div>
    );
  };

  return (
    <TreeMapComponent
      dataSource={data}
      leafItemSettings={{
        labelTemplate: labelTemplate
      }}
    />
  );
}
```

## Best Practices

1. **Label Position:** Center for balanced items, corners for wide/tall items
2. **Font Size:** 12-14px for best readability
3. **Multi-Line:** Use newlines (\n) for complex labels
4. **Overflow:** Use WrapByWord for longer text
5. **Hierarchy:** Different borders for different levels
6. **Accessibility:** Ensure contrast between text and background

## Common Issues

**Issue:** Labels not visible
- **Solution:** Check labelPath property matches data, verify font color vs background

**Issue:** Text overlaps in small rectangles
- **Solution:** Use `interSectAction: 'WrapByWord'` or reduce font size

**Issue:** Template not rendering
- **Solution:** Ensure labelTemplate function returns valid React element

## Next Steps

- **Color Mapping:** See [color-mapping.md](color-mapping.md) to color items by value
- **Legends:** See [legends-tooltips-selection.md](legends-tooltips-selection.md) for legend integration
- **Drill-Down:** See [drilldown.md](drilldown.md) for hierarchical navigation
