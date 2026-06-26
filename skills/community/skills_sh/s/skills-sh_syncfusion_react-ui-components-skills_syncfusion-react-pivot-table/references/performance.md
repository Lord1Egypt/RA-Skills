# Performance Optimization

## ⚠️ SECURITY NOTICE

**Server-side data sources MUST use authenticated, configuration-based endpoints.** Never hardcode server URLs.

✅ **Required Security Controls:**
- Environment-based configuration (`.env` files)
- Authentication and authorization
- HTTPS/SSL for all remote connections
- Input validation and sanitization

## Table of Contents
- [Virtual Scrolling](#virtual-scrolling)
- [Paging Configuration](#paging-configuration)
- [Data Compression](#data-compression)
- [Memory Optimization](#memory-optimization)
- [Rendering Optimization](#rendering-optimization)
- [Network Optimization](#network-optimization)
- [Performance Best Practices](#performance-best-practices)
- [Performance Monitoring](#performance-monitoring)
- [Troubleshooting](#troubleshooting)

## Virtual Scrolling

### Enabling Virtual Scrolling

Virtual scrolling efficiently handles large datasets by rendering only visible rows and columns:

```typescript
import { VirtualScroll, Inject } from '@syncfusion/ej2-react-pivotview';

<PivotViewComponent
  enableVirtualization={true}
  dataSourceSettings={dataSourceSettings}
  height={500}  // Required for virtual scrolling
>
  <Inject services={[VirtualScroll]} />
</PivotViewComponent>
```

### Virtual Scrolling with Settings

Customize virtual scrolling behavior using `virtualScrollSettings`:

```typescript
import { VirtualScroll, Inject } from '@syncfusion/ej2-react-pivotview';

const virtualScrollSettings = {
  allowSinglePage: false     // Render multiple pages
};

<PivotViewComponent
  enableVirtualization={true}
  virtualScrollSettings={virtualScrollSettings}
  dataSourceSettings={dataSourceSettings}
  height={500}
>
  <Inject services={[VirtualScroll]} />
</PivotViewComponent>
```

### Benefits

- Handles 100K+ rows efficiently
- Reduces initial load time
- Improves memory usage
- Smooth scrolling experience

### Virtual Scrolling Example

```typescript
function VirtualPivot() {
  const largeDataset = generateLargeDataset(100000); // 100K records

  return (
    <PivotViewComponent
      id="virtual-pivot"
      dataSourceSettings={{
        dataSource: largeDataset as IDataSet[],
        rows: [{ name: 'Country' }, { name: 'Region' }],
        columns: [{ name: 'Year' }, { name: 'Quarter' }],
        values: [{ name: 'Sales' }]
      }}
      enableVirtualization={true}
      height={500}
    >
      <Inject services={[VirtualScroll]} />
    </PivotViewComponent>
  );
}
```

## Paging Configuration

### Enable Paging

```typescript
<PivotViewComponent
  enablePaging={true}
  pageSettings={{
    rowPageSize: 10,
    columnPageSize: 5
  }}
  dataSourceSettings={dataSourceSettings}
/>
```

### Page Size Options

```typescript
const pageSettings = {
  rowPageSize: 10,      // Records per row page
  columnPageSize: 5,    // Columns per column page
  currentRowPage: 1,    // Initial row page
  currentColumnPage: 1  // Initial column page
};

<PivotViewComponent pageSettings={pageSettings} />
```

### Paging Example

```typescript
function PagingPivot() {
  const [rowPage, setRowPage] = React.useState(1);
  const [colPage, setColPage] = React.useState(1);

  return (
    <>
      <div style={{ marginBottom: '10px' }}>
        <label>
          Row Page Size:
          <select defaultValue="10">
            <option value="5">5</option>
            <option value="10">10</option>
            <option value="20">20</option>
          </select>
        </label>
      </div>
      <PivotViewComponent
        enablePaging={true}
        pageSettings={{
          rowPageSize: 10,
          columnPageSize: 5
        }}
        dataSourceSettings={dataSourceSettings}
      />
    </>
  );
}
```

## Data Compression

Data compression optimizes performance when working with large volumes of raw relational data by compressing the input data based on uniqueness before aggregation. This significantly reduces processing time and memory usage during initial rendering and report operations.

### How Data Compression Works

When enabled, the pivot table:
1. Compresses raw input data based on data uniqueness
2. Uses compressed data for aggregation calculations
3. Reduces looping complexity during operations
4. Maintains exact calculation accuracy

**Example Impact:** 1 million raw records → 1,000 unique records = 3x faster rendering

### Enabling Data Compression

```typescript
import { PivotViewComponent, VirtualScroll, Inject } from '@syncfusion/ej2-react-pivotview';

<PivotViewComponent
  allowDataCompression={true}  // Enable compression
  dataSourceSettings={dataSourceSettings}
  enableVirtualization={true}   // Often combined with virtual scrolling
>
  <Inject services={[VirtualScroll]} />
</PivotViewComponent>
```

### Data Compression with Large Dataset

```typescript
function CompressedPivot() {
  const largeDataset = generateLargeDataset(1000000); // 1 million records

  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: largeDataset as IDataSet[],
    rows: [{ name: 'ProductID' }],
    columns: [{ name: 'Year' }],
    values: [
      { name: 'Price', caption: 'Unit Price', format: 'C0' },
      { name: 'Sold', caption: 'Unit Sold' }
    ]
  };

  return (
    <PivotViewComponent
      id="compressed-pivot"
      dataSourceSettings={dataSourceSettings}
      allowDataCompression={true}  // Enable compression for large data
      enableVirtualization={true}   // Virtual scrolling for rendering
      height={500}
    >
      <Inject services={[VirtualScroll]} />
    </PivotViewComponent>
  );
}
```

### Important Limitations

When data compression is enabled, the following aggregation types are **not fully supported**:

| Aggregation Type | Behavior |
|------------------|----------|
| Average | Converted to Sum |
| PopulationStDev | Converted to Sum |
| SampleStDev | Converted to Sum |
| PopulationVar | Converted to Sum |
| SampleVar | Converted to Sum |
| DistinctCount | Functions as Count |

**Note on Calculated Fields:** Existing fields in calculated fields revert to their default aggregation type for calculation, even if explicitly changed.

### When to Use Data Compression

✅ **Use when:**
- Working with relational data sources (SQL, REST APIs returning raw data)
- Dataset size > 100K records
- Many duplicate values across rows
- Initial load time is critical

❌ **Avoid when:**
- Using statistical aggregations (StDev, Variance)
- Data source is already aggregated
- Real-time changes with streaming data
- Calculated fields require non-Sum aggregations

## Rendering Optimization

### 1. Defer Updates with Batch Operations

Use `deferUpdate` mode for multiple field changes:

```typescript
function BatchFieldChanges() {
  let pivotObj: PivotViewComponent;

  const applyChanges = (): void => {
    if (pivotObj) {
      // All changes render once with Apply button
      pivotObj.dataSourceSettings!.columns = [{ name: 'Year' }];
      pivotObj.dataSourceSettings!.rows = [{ name: 'Country' }];
      pivotObj.dataSourceSettings!.values = [{ name: 'Sales' }];
    }
  };

  return (
    <>
      <button onClick={applyChanges}>Apply Changes</button>
      <PivotViewComponent
        ref={(d: PivotViewComponent) => pivotObj = d}
        dataSourceSettings={dataSourceSettings}
        allowDeferLayoutUpdate={true}  // Single render after changes
      />
    </>
  );
}
```

### 2. Conditional Cell Templates

Avoid expensive operations in templates:

```typescript
// ❌ Bad: Expensive calculations in template
function getCellTemplate(props: any) {
  const value = complexCalculation(props.cellInfo.value);  // Runs on every render
  return <span>{value}</span>;
}

// ✅ Good: Pre-calculate or memoize
const cellTemplate = React.memo((props: any) => (
  <span>{props.cellInfo.value}</span>
));
```

## Network Optimization

### 1. Server-Side Aggregation

> **⚠️ SECURITY:** Use environment variables for server URLs. See security notice at top of document.

Use server-side aggregation for relational data:

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  url: process.env.REACT_APP_PIVOT_SERVICE_URL,  // Environment-based URL
  mode: 'Server'  // Server-side aggregation
  rows: [{ name: 'Country' }],
  columns: [{ name: 'Year' }],
  values: [{ name: 'Sales' }]
};

<PivotViewComponent dataSourceSettings={dataSourceSettings} />
```

## Troubleshooting

### Slow Initial Load

**Problem:** First render takes several seconds

**Solutions:**
1. Enable virtual scrolling: `enableVirtualization={true}`
2. Use data compression: `allowDataCompression={true}`
3. Reduce initial data size with filters before binding
4. Use paging: `enablePaging={true}`

### High Memory Usage

**Problem:** Browser memory keeps increasing

**Solutions:**
1. Clear unused data regularly
2. Use pagination instead of loading all data
3. Reduce number of value fields
4. Limit field list items with `maxNodeLimitInMemberEditor`
5. Implement data caching with TTL

### Lag During Drill-Down/Filtering

**Problem:** Drill operations are slow

**Solutions:**
1. Use `deferUpdate` for multiple changes
2. Limit hierarchy depth (3-4 levels recommended)
3. Pre-aggregate data server-side
4. Use paging in drill-through results

### Jary Scrolling

**Problem:** Virtual scrolling is jerky/stuttering

**Solutions:**
1. Reduce number of columns
2. Simplify cell templates
3. Set appropriate `height` property
4. Use simpler data types
5. Limit conditional formatting

### Memory Leak on Unmount

**Problem:** Memory is not freed when pivot table is destroyed

**Solutions:**
1. Properly clean up event listeners
2. Clear data sources before unmounting
3. Use React.useEffect cleanup functions
4. Unbind all custom events

```typescript
React.useEffect(() => {
  return () => {
    // Cleanup
    if (pivotRef.current) {
      pivotRef.current.element = null;
    }
  };
}, []);
```

## Performance Checklist

✅ **For 10K-100K rows:**
- [ ] Enable virtual scrolling
- [ ] Use paging for columns
- [ ] Optimize field count (~20 or fewer)
- [ ] Use 2-3 level hierarchies
- [ ] Apply format settings

✅ **For 100K-1M+ rows:**
- [ ] Enable data compression
- [ ] Enable virtual scrolling
- [ ] Use paging for both axes
- [ ] Server-side aggregation if possible
- [ ] Minimize number of aggregations
- [ ] Use lazy loading for data
- [ ] Implement result caching

✅ **For Real-Time Dashboards:**
- [ ] Use deferred updates
- [ ] Implement refresh rate limiting
- [ ] Cache previous results
- [ ] Only update changed items
- [ ] Consider WebSocket instead of polling

## Related Features

- **Defer Update**: Batch field operations for single render
- **Virtual Scrolling**: Efficient rendering of large datasets
- **Paging**: Navigate large tables page by page
- **Data Compression**: Compress relational data for faster processing
- **Export**: Export optimized for specific formats
- **Filtering**: Reduce dataset before display

