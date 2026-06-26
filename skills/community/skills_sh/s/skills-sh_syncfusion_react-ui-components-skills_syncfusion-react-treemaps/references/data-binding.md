# Data Binding and Hierarchical Data

## Table of Contents

- [Understanding Weight Value Path](#understanding-weight-value-path)
- [Flat Data Binding](#flat-data-binding)
  - [Simple Category Comparison](#simple-category-comparison)
  - [Market Share Visualization](#market-share-visualization)
- [Hierarchical Data with Levels](#hierarchical-data-with-levels)
  - [Two-Level Hierarchy](#two-level-hierarchy)
  - [Data Structure Notes](#data-structure-notes)
- [Multi-Level Hierarchies](#multi-level-hierarchies)
  - [Three-Level Organization Hierarchy](#three-level-organization-hierarchy)
  - [Folder Structure Example](#folder-structure-example)
- [Remote Data Sources](#remote-data-sources)
  - [Using Async/Await](#using-asyncawait)
  - [Data Transformation Before Binding](#data-transformation-before-binding)
- [Data Transformation Patterns](#data-transformation-patterns)
  - [Pattern 1: Aggregating Related Records](#pattern-1-aggregating-related-records)
  - [Pattern 2: Filtering Data](#pattern-2-filtering-data)
  - [Pattern 3: Adding Calculated Properties](#pattern-3-adding-calculated-properties)
- [Common Issues](#common-issues)
- [Next Steps](#next-steps)

## Understanding Weight Value Path

The `weightValuePath` property determines the **size** of each rectangle based on a numeric value from your data.

```jsx
const data = [
  { Item: 'Laptop', Sales: 2500 },    // 2500 → rectangle area
  { Item: 'Phone', Sales: 3200 },     // 3200 → larger rectangle
  { Item: 'Tablet', Sales: 1800 }     // 1800 → smaller rectangle
];

<TreeMapComponent
  dataSource={data}
  weightValuePath="Sales"  // Use Sales values for sizing
  leafItemSettings={{ labelPath: 'Item' }}
/>
```

**Key points:**
- Must be a numeric property
- Proportional sizing: larger values → larger rectangles
- Negative values treated as zero
- Missing/undefined values default to 0

## Flat Data Binding

Flat data has all items at the same level with no grouping:

### Simple Category Comparison

```jsx
const salesData = [
  { Region: 'North America', Revenue: 45000 },
  { Region: 'Europe', Revenue: 38000 },
  { Region: 'Asia Pacific', Revenue: 52000 },
  { Region: 'Latin America', Revenue: 28000 },
  { Region: 'Middle East', Revenue: 15000 }
];

<TreeMapComponent
  height="350px"
  dataSource={salesData}
  weightValuePath="Revenue"
  leafItemSettings={{
    labelPath: 'Region'
  }}
/>
```

**Result:** Compares regional revenue with rectangle sizes proportional to revenue values.

### Market Share Visualization

```jsx
const marketData = [
  { Company: 'Apple', MarketCap: 2800 },
  { Company: 'Microsoft', MarketCap: 2500 },
  { Company: 'Google', MarketCap: 1800 },
  { Company: 'Amazon', MarketCap: 1600 },
  { Company: 'Tesla', MarketCap: 1000 }
];

<TreeMapComponent
  dataSource={marketData}
  weightValuePath="MarketCap"
  leafItemSettings={{ labelPath: 'Company' }}
  palette={['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']}
/>
```

**Use case:** Compare market positions at a glance.

## Hierarchical Data with Levels

Hierarchical data groups items into parent-child relationships. Use `<LevelsDirective>` to define hierarchy:

### Two-Level Hierarchy

```jsx
import { LevelsDirective, LevelDirective } from '@syncfusion/ej2-react-treemap';

const data = [
  { Country: 'USA', State: 'California', Sales: 2830 },
  { Country: 'USA', State: 'Texas', Sales: 2020 },
  { Country: 'USA', State: 'Florida', Sales: 1880 },
  { Country: 'Canada', State: 'Ontario', Sales: 1200 },
  { Country: 'Canada', State: 'British Columbia', Sales: 1100 }
];

<TreeMapComponent
  dataSource={data}
  weightValuePath="Sales"
  leafItemSettings={{ labelPath: 'State' }}
>
  <LevelsDirective>
    <LevelDirective groupPath="Country" />
  </LevelsDirective>
</TreeMapComponent>
```

**Result:** 
- Top-level groups by Country
- Within each country, shows individual states
- Rectangle sizes represent Sales values

### Data Structure Notes

- Each record in data must have all hierarchy properties
- `groupPath` order determines hierarchy levels
- Leaf items (innermost level) use `leafItemSettings.labelPath`

## Multi-Level Hierarchies

Support any depth of hierarchy for complex data structures:

### Three-Level Organization Hierarchy

```jsx
const orgData = [
  { Division: 'Engineering', Department: 'Backend', Team: 'API Services', HeadCount: 12 },
  { Division: 'Engineering', Department: 'Backend', Team: 'Database', HeadCount: 8 },
  { Division: 'Engineering', Department: 'Frontend', Team: 'Web', HeadCount: 10 },
  { Division: 'Engineering', Department: 'Frontend', Team: 'Mobile', HeadCount: 9 },
  { Division: 'Sales', Department: 'Enterprise', Team: 'Team A', HeadCount: 15 },
  { Division: 'Sales', Department: 'Enterprise', Team: 'Team B', HeadCount: 12 },
  { Division: 'Sales', Department: 'SMB', Team: 'Team C', HeadCount: 8 }
];

<TreeMapComponent
  dataSource={orgData}
  weightValuePath="HeadCount"
  leafItemSettings={{
    labelPath: 'Team',
    labelFormat: '${Team}\n${HeadCount}hr'
  }}
>
  <LevelsDirective>
    <LevelDirective groupPath="Division" />
    <LevelDirective groupPath="Department" />
  </LevelsDirective>
</TreeMapComponent>
```

**Structure:**
- Level 1: Division (Engineering, Sales)
- Level 2: Department (Backend, Frontend, Enterprise, SMB)
- Leaf level: Team (individual teams)

### Folder Structure Example

```jsx
const fileSystem = [
  { Drive: 'C:', Folder: 'Documents', Subfolder: 'Work', Size: 2500 },
  { Drive: 'C:', Folder: 'Documents', Subfolder: 'Personal', Size: 1800 },
  { Drive: 'C:', Folder: 'Downloads', Subfolder: 'Apps', Size: 5000 },
  { Drive: 'D:', Folder: 'Media', Subfolder: 'Videos', Size: 15000 }
];

<TreeMapComponent
  dataSource={fileSystem}
  weightValuePath="Size"
  leafItemSettings={{ labelPath: 'Subfolder' }}
>
  <LevelsDirective>
    <LevelDirective groupPath="Drive" />
    <LevelDirective groupPath="Folder" />
  </LevelsDirective>
</TreeMapComponent>
```

## Remote Data Sources

Fetch data from APIs and bind to TreeMap:

### Using Async/Await

```jsx
export function RemoteTreeMap() {
  const [data, setData] = React.useState([]);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    async function fetchData() {
      try {
        const response = await fetch('https://api.example.com/sales');
        const result = await response.json();
        setData(result);
      } catch (error) {
        console.error('Failed to load data:', error);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <TreeMapComponent
      height="350px"
      dataSource={data}
      weightValuePath="Sales"
      leafItemSettings={{ labelPath: 'Region' }}
    />
  );
}
```

### Data Transformation Before Binding

```jsx
export function TransformedTreeMap() {
  const [data, setData] = React.useState([]);

  React.useEffect(() => {
    async function loadAndTransform() {
      const response = await fetch('https://api.example.com/products');
      const rawData = await response.json();
      
      // Transform flat API response to hierarchical format
      const transformed = rawData.map(item => ({
        Category: item.category,
        Type: item.subcategory,
        Product: item.name,
        Sales: item.sales_amount
      }));
      
      setData(transformed);
    }
    loadAndTransform();
  }, []);

  return (
    <TreeMapComponent
      dataSource={data}
      weightValuePath="Sales"
      leafItemSettings={{ labelPath: 'Product' }}
    >
      <LevelsDirective>
        <LevelDirective groupPath="Category" />
        <LevelDirective groupPath="Type" />
      </LevelsDirective>
    </TreeMapComponent>
  );
}
```

## Data Transformation Patterns

### Pattern 1: Aggregating Related Records

Combine multiple records with same category into single weight:

```jsx
const rawData = [
  { Region: 'USA', Quarter: 'Q1', Sales: 10000 },
  { Region: 'USA', Quarter: 'Q2', Sales: 12000 },
  { Region: 'USA', Quarter: 'Q3', Sales: 11500 },
  { Region: 'Canada', Quarter: 'Q1', Sales: 5000 }
];

// Transform to total sales per region
const aggregated = rawData.reduce((acc, item) => {
  const existing = acc.find(r => r.Region === item.Region);
  if (existing) {
    existing.TotalSales += item.Sales;
  } else {
    acc.push({ Region: item.Region, TotalSales: item.Sales });
  }
  return acc;
}, []);

// Use aggregated data
<TreeMapComponent
  dataSource={aggregated}
  weightValuePath="TotalSales"
/>
```

### Pattern 2: Filtering Data

Show only items above a threshold:

```jsx
const allData = [
  { Product: 'Laptop', Sales: 2500 },
  { Product: 'Mouse', Sales: 150 },
  { Product: 'Keyboard', Sales: 300 },
  { Product: 'Monitor', Sales: 1200 }
];

// Show only items with sales > 300
const filtered = allData.filter(item => item.Sales > 300);

<TreeMapComponent
  dataSource={filtered}
  weightValuePath="Sales"
/>
```

### Pattern 3: Adding Calculated Properties

Compute derived values for coloring or sizing:

```jsx
const data = [
  { Product: 'A', Sold: 1000, Target: 1200 },
  { Product: 'B', Sold: 800, Target: 1000 },
  { Product: 'C', Sold: 950, Target: 900 }
];

// Add performance metrics
const enhanced = data.map(item => ({
  ...item,
  Achievement: (item.Sold / item.Target) * 100,
  Variance: item.Sold - item.Target
}));

<TreeMapComponent
  dataSource={enhanced}
  weightValuePath="Sold"
  rangeColorValuePath="Achievement"
/>
```

## Common Issues

**Issue:** Rectangle sizes don't match weightValuePath values
- **Cause:** Non-numeric values in weight property
- **Solution:** Convert to numbers: `item.sales = Number(item.sales)`

**Issue:** Hierarchy not showing correctly
- **Cause:** Missing groupPath properties in data
- **Solution:** Ensure all data records have every groupPath and leaf property

**Issue:** Performance slow with large datasets
- **Cause:** Too many items or levels
- **Solution:** Aggregate data, filter to top N items, or use virtual scrolling patterns

## Next Steps

- **Color Mapping:** See [color-mapping.md](color-mapping.md) to color items by value
- **Drill-Down:** See [drilldown.md](drilldown.md) to navigate hierarchies interactively
- **Customization:** See [leaf-items-and-labels.md](leaf-items-and-labels.md) to customize appearance
