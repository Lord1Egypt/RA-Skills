# TreeMap Layouts

## Table of Contents

- [Layout Types](#layout-types)
- [Squarified Layout](#squarified-layout)
  - [Basic Squarified Example](#basic-squarified-example)
  - [Market Dominance Visualization](#market-dominance-visualization)
- [Horizontal Layout](#horizontal-layout)
  - [Horizontal Layout Example](#horizontal-layout-example)
  - [Budget Distribution Example](#budget-distribution-example)
- [Vertical Layout](#vertical-layout)
  - [Vertical Layout Example](#vertical-layout-example)
  - [Storage Usage Visualization](#storage-usage-visualization)
- [Slice and Dice Layout](#slice-and-dice-layout)
  - [SliceAndDice Example](#sliceanddice-example)
- [Choosing the Right Layout](#choosing-the-right-layout)
  - [Use Squarified When](#use-squarified-when)
  - [Use Horizontal When](#use-horizontal-when)
  - [Use Vertical When](#use-vertical-when)
  - [Use SliceAndDice When](#use-sliceanddice-when)
- [Dynamic Layout Selection](#dynamic-layout-selection)
  - [Responsive Layout Based on Container](#responsive-layout-based-on-container)
  - [Layout Based on Data Size](#layout-based-on-data-size)
  - [Layout Comparison View](#layout-comparison-view)
- [Layout Performance Tips](#layout-performance-tips)
- [Common Issues](#common-issues)
- [Next Steps](#next-steps)

## Layout Types

TreeMap supports four layout algorithms that determine how rectangles are arranged. Each layout has different characteristics affecting aspect ratio, readability, and visual appeal.

| Layout | Aspect Ratio | Best For | Algorithm |
|--------|-------------|----------|-----------|
| **Squarified** | Balanced | General purpose, balanced aspect ratios | Optimizes for square-like rectangles |
| **Horizontal** | Wide/narrow | Comparing similar-sized items | Left-to-right ordering |
| **Vertical** | Tall/narrow | Category hierarchies | Top-to-bottom ordering |
| **SliceAndDice** | Variable | Exploring hierarchies | Alternating rows/columns |

## Squarified Layout

Squarified (default) layout creates rectangles with balanced aspect ratios, approximately square-shaped.

### Basic Squarified Example

```jsx
import { TreeMapComponent } from '@syncfusion/ej2-react-treemap';

const data = [
  { Fruit: 'Apple', Count: 5000 },
  { Fruit: 'Mango', Count: 3000 },
  { Fruit: 'Orange', Count: 2300 },
  { Fruit: 'Banana', Count: 500 },
  { Fruit: 'Grape', Count: 4300 }
];

<TreeMapComponent
  height="350px"
  dataSource={data}
  weightValuePath="Count"
  layoutType="Squarified"  // Default layout
  leafItemSettings={{ labelPath: 'Fruit' }}
/>
```

**Characteristics:**
- Aspect ratios close to 1:1 (square-like)
- Most visually balanced
- Best for general-purpose visualization
- Improved readability for varied data sizes

### Market Dominance Visualization

```jsx
const marketData = [
  { Company: 'Samsung', MarketShare: 25 },
  { Company: 'Apple', MarketShare: 20 },
  { Company: 'Xiaomi', MarketShare: 15 },
  { Company: 'Oppo', MarketShare: 12 },
  { Company: 'Vivo', MarketShare: 10 },
  { Company: 'Others', MarketShare: 18 }
];

<TreeMapComponent
  dataSource={marketData}
  weightValuePath="MarketShare"
  layoutType="Squarified"
  leafItemSettings={{
    labelPath: 'Company',
    labelFormat: '${Company}\n${MarketShare}%'
  }}
/>
```

## Horizontal Layout

Horizontal layout arranges items in rows, creating wide rectangles, left-to-right ordering.

### Horizontal Layout Example

```jsx
const regionData = [
  { Region: 'Asia', Sales: 45000 },
  { Region: 'Europe', Sales: 38000 },
  { Region: 'Americas', Sales: 52000 },
  { Region: 'Africa', Sales: 15000 },
  { Region: 'Oceania', Sales: 8000 }
];

<TreeMapComponent
  dataSource={regionData}
  weightValuePath="Sales"
  layoutType="SliceAndDiceHorizontal"
  leafItemSettings={{
    labelPath: 'Region',
    labelFormat: '${Region}\n${Sales}'
  }}
/>
```

**Characteristics:**
- Creates horizontal row-like layout
- Good for top-to-bottom reading
- Items ordered left-to-right
- Better for items with wide aspect ratios

### Budget Distribution Example

```jsx
const budgetData = [
  { Department: 'Engineering', Budget: 500000 },
  { Department: 'Marketing', Budget: 250000 },
  { Department: 'Sales', Budget: 300000 },
  { Department: 'Operations', Budget: 150000 },
  { Department: 'HR', Budget: 100000 }
];

<TreeMapComponent
  dataSource={budgetData}
  weightValuePath="Budget"
  layoutType="SliceAndDiceHorizontal"
  leafItemSettings={{
    labelPath: 'Department'
  }}
  palette={['#3498DB', '#E74C3C', '#2ECC71', '#F39C12', '#9B59B6']}
/>
```

## Vertical Layout

Vertical layout arranges items in columns, creating tall rectangles, top-to-bottom ordering.

### Vertical Layout Example

```jsx
const categoryData = [
  { Category: 'Electronics', Sales: 45000 },
  { Category: 'Clothing', Sales: 35000 },
  { Category: 'Books', Sales: 28000 },
  { Category: 'Furniture', Sales: 52000 },
  { Category: 'Sports', Sales: 18000 }
];

<TreeMapComponent
  dataSource={categoryData}
  weightValuePath="Sales"
  layoutType="SliceAndDiceVertical"
  leafItemSettings={{
    labelPath: 'Category'
  }}
/>
```

**Characteristics:**
- Creates vertical column-like layout
- Items ordered top-to-bottom, left-to-right
- Better for narrower containers
- Emphasizes vertical reading flow

### Storage Usage Visualization

```jsx
const storageData = [
  { Folder: 'Documents', Size: 25000 },
  { Folder: 'Photos', Size: 350000 },
  { Folder: 'Videos', Size: 1500000 },
  { Folder: 'Music', Size: 250000 },
  { Folder: 'Downloads', Size: 500000 }
];

<TreeMapComponent
  height="500px"
  dataSource={storageData}
  weightValuePath="Size"
  layoutType="SliceAndDiceVertical"
  leafItemSettings={{
    labelPath: 'Folder',
    labelFormat: '${Folder}\n${Size} MB'
  }}
/>
```

## Slice and Dice Layout

Slice and Dice layout alternates between horizontal and vertical divisions, useful for hierarchical data.

### SliceAndDice Example

```jsx
import { LevelsDirective, LevelDirective } from '@syncfusion/ej2-react-treemap';

const hierarchicalData = [
  { Company: 'TechCorp', Division: 'Software', Department: 'Frontend', Headcount: 45 },
  { Company: 'TechCorp', Division: 'Software', Department: 'Backend', Headcount: 60 },
  { Company: 'TechCorp', Division: 'Hardware', Department: 'R&D', Headcount: 35 },
  { Company: 'TechCorp', Division: 'Hardware', Department: 'Manufacturing', Headcount: 80 }
];

<TreeMapComponent
  dataSource={hierarchicalData}
  weightValuePath="Headcount"
  layoutType="SliceAndDiceAuto"
  leafItemSettings={{ labelPath: 'Department' }}
>
  <LevelsDirective>
    <LevelDirective groupPath="Division" />
  </LevelsDirective>
</TreeMapComponent>
```

**Characteristics:**
- Alternates horizontal and vertical divisions
- Good for hierarchies with many levels
- Creates clear visual separation
- Useful for file system or org chart visualization

## Choosing the Right Layout

### Use Squarified When:
- **Visual balance is priority:** Want aesthetically pleasing visualization
- **Mixed-size data:** Items vary significantly in size
- **General exploration:** Users exploring data without specific reading pattern
- **Example:** Market share, product comparison

```jsx
<TreeMapComponent
  layoutType="Squarified"  // Default, good choice
/>
```

### Use Horizontal When:
- **Reading left-to-right:** Users accustomed to horizontal scanning
- **Many items:** Large number of categories to display
- **Label space:** Need horizontal space for item labels
- **Example:** Budget distribution, regional comparison

```jsx
<TreeMapComponent
  layoutType="SliceAndDiceHorizontal"  // Best for label readability
/>
```

### Use Vertical When:
- **Tall containers:** Container height > width
- **Hierarchical exploration:** Parent-child relationships matter
- **Column-based reading:** Users naturally read top-to-bottom
- **Example:** Folder structure, category hierarchy

```jsx
<TreeMapComponent
  layoutType="SliceAndDiceVertical"  // Fits tall viewports
/>
```

### Use SliceAndDice When:
- **Deep hierarchies:** Multiple levels of grouping
- **Clear separation needed:** Distinguish parent groups visually
- **Alternating logic:** Want alternating row/column arrangement
- **Example:** Organization chart, file system

```jsx
<TreeMapComponent
  layoutType="SliceAndDiceAuto"  // For hierarchical data
>
  <LevelsDirective>
    {/* Multiple level groups */}
  </LevelsDirective>
</TreeMapComponent>
```

## Dynamic Layout Selection

### Responsive Layout Based on Container

```jsx
export function ResponsiveTreeMap() {
  const containerRef = React.useRef(null);
  const [layout, setLayout] = React.useState('Squarified');

  React.useEffect(() => {
    function handleResize() {
      const width = containerRef.current?.offsetWidth || 0;
      const height = containerRef.current?.offsetHeight || 0;
      
      // Wide container → Horizontal
      if (width > height * 1.5) {
        setLayout('Horizontal');
      }
      // Tall container → Vertical
      else if (height > width * 1.5) {
        setLayout('Vertical');
      }
      // Balanced → Squarified
      else {
        setLayout('Squarified');
      }
    }

    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <div ref={containerRef} style={{ width: '100%', height: '100vh' }}>
      <TreeMapComponent
        dataSource={data}
        layoutType={layout}
        height="100%"
      />
    </div>
  );
}
```

### Layout Based on Data Size

```jsx
export function AdaptiveTreeMap({ data }) {
  // Choose layout based on number of items
  const getLayout = () => {
    if (data.length > 100) return 'SliceAndDice';  // Many items
    if (data.length > 30) return 'Horizontal';      // Many items
    return 'Squarified';                            // Few items
  };

  return (
    <TreeMapComponent
      dataSource={data}
      layoutType={getLayout()}
    />
  );
}
```

### Layout Comparison View

```jsx
export function CompareLayouts({ data }) {
  const layouts = ['Squarified', 'Horizontal', 'Vertical', 'SliceAndDice'];

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
      {layouts.map(layout => (
        <div key={layout}>
          <h3>{layout}</h3>
          <TreeMapComponent
            dataSource={data}
            layoutType={layout}
            height="300px"
          />
        </div>
      ))}
    </div>
  );
}
```

## Layout Performance Tips

1. **Squarified:** Best default, good performance for any data
2. **Horizontal/Vertical:** Linear calculation, slightly faster than squarified
3. **SliceAndDice:** Best for hierarchies, consider for deep nesting
4. **Large datasets:** All layouts perform similarly; optimize data instead

## Common Issues

**Issue:** Labels overlapping in horizontal layout
- **Solution:** Increase container width or use label templates to format

**Issue:** Rectangles too narrow/wide in vertical layout
- **Solution:** Consider container proportions or switch to Squarified

**Issue:** Layout doesn't match expectations
- **Solution:** Verify `layoutType` prop spelling (case-sensitive)

## Next Steps

- **Drill-Down:** See [drilldown.md](drilldown.md) for hierarchical navigation
- **Color Mapping:** See [color-mapping.md](color-mapping.md) to add visual distinction
- **Labels:** See [leaf-items-and-labels.md](leaf-items-and-labels.md) for label positioning
