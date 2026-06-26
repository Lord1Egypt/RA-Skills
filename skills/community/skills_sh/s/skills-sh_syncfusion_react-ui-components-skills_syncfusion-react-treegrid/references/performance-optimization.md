---
name: performance-optimization
description: 'Performance Optimization in React TreeGrid - virtual scrolling, bundle optimization, rendering optimization, and benchmarking.'
---

# Performance Optimization

## Table of Contents
- [Performance Rules](#performance-rules)
- [Virtual Scrolling](#virtual-scrolling)
- [Infinite Scrolling](#infinite-scrolling)
- [Bundle Size Optimization](#bundle-size-optimization)
- [Disable Unnecessary Features](#disable-unnecessary-features)
- [Query Optimization](#query-optimization)
- [Template Optimization](#template-optimization)
- [Event Handler Optimization](#event-handler-optimization)
- [Avoid Performance Pitfalls](#avoid-performance-pitfalls)
- [Performance Checklist](#performance-checklist)

Best practices for optimizing TreeGrid performance.

## Performance Rules

### Rule 1: Virtual Scrolling for 1000+ Rows
**Severity**: 🟠 IMPORTANT - Performance degrades significantly without virtualization for large datasets

**Requirement in React**:
```jsx
// ✅ REQUIRED for large datasets (1000+ rows)
import { TreeGridComponent, Inject, VirtualScroll } from '@syncfusion/ej2-react-treegrid';

<TreeGridComponent 
  dataSource={largeData}
  enableVirtualization={true}
  height='600px'
  pageSettings={{ pageSize: 100 }}>
  <Inject services={[VirtualScroll]} />
</TreeGridComponent>

// ✅ RECOMMENDED: Set rowHeight explicitly for better performance
<TreeGridComponent 
  dataSource={largeData}
  enableVirtualization={true}
  height='600px'
  rowHeight={36}
  pageSettings={{ pageSize: 100 }}>
  <Inject services={[VirtualScroll]} />
</TreeGridComponent>

// ❌ DON'T use without virtualization for large data (1000+ rows)
<TreeGridComponent 
  dataSource={largeData}>  {/* Renders ALL 10,000 rows = very slow */}
</TreeGridComponent>

// ❌ WRONG - No height set
<TreeGridComponent 
  dataSource={largeData}
  enableVirtualization={true}>  {/* Error: Virtual scroll requires height */}
</TreeGridComponent>
```

**Performance Impact**:
```jsx
// Without Virtual Scrolling:
1,000 rows: ~500ms render time
10,000 rows: ~5s render time
100,000 rows: Browser freeze or crash

// With Virtual Scrolling:
1,000 rows: ~50ms render time
10,000 rows: ~100ms render time
100,000 rows: ~200ms render time (handles well!)
```

---

### Rule 2: Use React.memo or useMemo for Large Grids
**Severity**: 🟠 IMPORTANT - Prevents unnecessary re-renders and improves performance

**Requirement in React**:
```jsx
// ✅ RECOMMENDED - Wrap component in React.memo
import { memo } from 'react';

const TreeGridMemo = memo(function TreeGridComponent({ data, settings }) {
  return (
    <TreeGridComponent 
      dataSource={data}
      {...settings}>
      <ColumnsDirective>
        <ColumnDirective field='TaskID'></ColumnDirective>
      </ColumnsDirective>
    </TreeGridComponent>
  );
});

// ✅ ALTERNATIVE - Use useMemo for data
import { useMemo } from 'react';

export default function GridPage({ rawData }) {
  const memoizedData = useMemo(() => {
    // Process data only when rawData changes
    return rawData.filter(item => item.active);
  }, [rawData]);
  
  return (
    <TreeGridComponent dataSource={memoizedData}>
      <ColumnsDirective>
        <ColumnDirective field='TaskID'></ColumnDirective>
      </ColumnsDirective>
    </TreeGridComponent>
  );
}

// ❌ SLOWER - No memoization, re-renders on parent update
export default function GridPage({ data }) {
  return (
    <TreeGridComponent dataSource={data}>
      {/* Every parent re-render causes TreeGrid re-render */}
    </TreeGridComponent>
  );
}

// ❌ WRONG - Creating new array on each render
export default function GridPage({ rawData }) {
  return (
    <TreeGridComponent dataSource={rawData.filter(x => x.active)}>
      {/* New array created on every render = performance issue */}
    </TreeGridComponent>
  );
}
```

**React Performance Patterns**:
```jsx
// Pattern 1: Memoize expensive computations
const data = useMemo(() => computeHeavyData(source), [source]);

// Pattern 2: Memoize entire component
export default memo(function Grid({ data }) {
  return <TreeGridComponent dataSource={data} />;
});

// Pattern 3: Memoize callbacks
const handleEdit = useCallback((args) => {
  // Handle edit
}, [dependencies]);

<TreeGridComponent onActionComplete={handleEdit} />
```

---

### Rule 3: Server-Side Operations for Large Datasets (10,000+ rows)
**Severity**: 🟠 IMPORTANT - Load only visible/necessary data to avoid memory issues

**Requirement in React**:
```jsx
// ✅ REQUIRED for 10,000+ rows - Server handles filtering/sorting/paging
import { DataManager, UrlAdaptor } from '@syncfusion/ej2-data';

export default function GridWithServerOps() {
  const dataManager = new DataManager({
    url: 'url',
    adaptor: new UrlAdaptor(),
    offline: false  // Use server-side operations
  });
  
  return (
    <TreeGridComponent 
      dataSource={dataManager}
      allowPaging={true}
      allowSorting={true}
      allowFiltering={true}
      pageSettings={{ pageSize: 50 }}>
      <Inject services={[Page, Sort, Filter]} />
    </TreeGridComponent>
  );
}

// ❌ WRONG - Loading all 100,000 rows to memory
export default function GridWrong() {
  const [allData, setAllData] = useState([]);
  
  useEffect(() => {
    // Fetch ALL rows at once (bad!)
    fetch('/api/all-tasks')
      .then(r => r.json())
      .then(allRows => setAllData(allRows));
  }, []);
  
  return (
    <TreeGridComponent dataSource={allData}>
      {/* Very slow - all data in memory */}
    </TreeGridComponent>
  );
}
```

**Server Implementation Requirements**:
```jsx
// Server endpoint must handle these query parameters:
- $skip: Pagination offset (for Page module)
- $top: Page size (for Page module)
- $orderby: Sorting field and direction
- $filter: Filter conditions

Example REQUEST:
GET /api/tasks?$skip=0&$top=50&$orderby=Priority desc&$filter=Status eq 'Active'

Example RESPONSE:
{
  "value": [
    { "TaskID": 1, "TaskName": "Task 1", ... },
    { "TaskID": 2, "TaskName": "Task 2", ... }
  ],
  "__count": 5000  // Total records (for pagination)
}
```

---

## Virtual Scrolling

Render only visible rows:

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, VirtualScroll } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  // Generate 100,000 rows
  const largeData = Array.from({ length: 100000 }, (_, i) => ({
    TaskID: i + 1,
    TaskName: `Task ${i + 1}`,
    Duration: Math.floor(Math.random() * 10) + 1,
    Children: []
  }));

  return (
    <TreeGridComponent
      dataSource={largeData}
      childMapping="Children"
      height={600}
      enableVirtualization={true}
      rowHeight={30}  // Exact row height for calculation
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={200} />
        <ColumnDirective field="Duration" headerText="Duration" width={100} />
      </ColumnsDirective>
      <Inject services={[VirtualScroll]} />
    </TreeGridComponent>
  );
}
```

### Critical Requirements

⚠️ **Virtual scrolling requires:**
1. `enableVirtualization={true}`
2. `height` must be set (e.g., `'600px'`, not `'auto'`)
3. Inject `VirtualScroll` module
4. Do NOT use `allowPaging` (conflicts with virtual scroll)

### Virtual Scrolling with Row Height

For better performance, specify consistent row height:

```tsx
<TreeGridComponent
  enableVirtualization={true}
  height="600px"
  rowHeight={48} // Consistent row height improves performance
>
```

## Infinite Scrolling

Load data in batches:

```tsx
<TreeGridComponent
  dataSource={dataManager}
  childMapping="Children"
  height={600}
  enableInfiniteScrolling={true}
  infiniteScrollSettings={{
    enableCache: true,      // Cache loaded pages
    maxBlocks: 5,           // Keep 5 blocks in cache
    pageSize: 50            // Rows per block
  }}
>
  {/* columns */}
</TreeGridComponent>
```

## Bundle Size Optimization

Only import needed modules:

```tsx
// ✅ Good - Import only needed modules
import { 
  TreeGridComponent, 
  ColumnsDirective, 
  ColumnDirective, 
  Inject, 
  Page,
  Sort,
  Filter
} from '@syncfusion/ej2-react-treegrid';

// USE ONLY THE MODULES YOU NEED
<Inject services={[Page, Sort, Filter]} />

// ❌ Avoid - Don't import everything
import * from '@syncfusion/ej2-react-treegrid'
```

## Disable Unnecessary Features

Only enable features you use:

```tsx
// ✅ Minimal configuration
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  editSettings={{ mode: 'Cell' }}  // Only cell editing
  // Don't add features you don't use:
  // allowPaging, allowSorting, allowFiltering, etc.
>

// ❌ Over-featured configuration
<TreeGridComponent
  dataSource={data}
  allowPaging
  pageSettings={{ pageSize: 10 }}
  allowSorting
  sortSettings={{...}}
  allowFiltering
  filterSettings={{...}}
  allowSearching
  allowReordering
  allowResizing
  // ... many more features
>
```




## Query Optimization

Fetch only needed data:

```tsx
// ✅ Optimized - Select specific columns
import { Query } from '@syncfusion/ej2-data';

const query = new Query()
  .select(['TaskID', 'TaskName', 'Duration'])  // Only needed columns
  .take(50);  // Limit rows

dataManager.executeQuery(query);

// ❌ Not optimized - Get all columns
dataManager.url = '/api/tasks';  // Gets all columns
```

## Template Optimization

Efficient rendering templates:

```tsx
// ✅ Efficient - Simple template
const simpleTemplate = (props) => props.TaskName;

// ✅ Efficient - Memoized complex template
const complexTemplate = React.memo((props) => (
  <div>
    <span className="badge">{props.Priority}</span>
    <span>{props.TaskName}</span>
  </div>
));

// ❌ Inefficient - Heavy computation in template
const badTemplate = (props) => {
  // Don't do heavy operations in templates!
  const result = expensiveCalculation(props);
  return <div>{result}</div>;
};
```

## Event Handler Optimization

Use event delegation:

```tsx
// ✅ Efficient - Single handler for all rows
<TreeGridComponent
  rowDataBound={(args) => {
    // Handle all rows here
    if (args.data.Priority === 'High') {
      args.row.classList.add('high-priority');
    }
  }}
>

// ❌ Inefficient - Multiple event listeners
data.forEach((row) => {
  const element = document.querySelector(`[data-id="${row.id}"]`);
  element.addEventListener('click', handleClick);
});
```


## Avoid Performance Pitfalls

### ❌ Never Make API Calls in Render Events

```tsx
// ❌ WRONG - API call in rowDataBound (fires on every render!)
const handleRowDataBound = (args) => {
  fetch(`/api/status/${args.data.id}`) // DON'T DO THIS!
    .then(response => response.json())
    .then(status => {
      args.row.classList.add(status.className);
    });
};

// ✅ CORRECT - Pre-fetch data, then merge
useEffect(() => {
  Promise.all([
    fetchTreeData(),
    fetchStatuses()
  ]).then(([treeData, statuses]) => {
    const enrichedData = treeData.map(item => ({
      ...item,
      status: statuses[item.id]
    }));
    setTreeData(enrichedData);
  });
}, []);

const handleRowDataBound = (args) => {
  // Use pre-fetched data for styling
  if (args.data.status === 'active') {
    args.row.classList.add('active-row');
  }
};
```

### ❌ Don't Combine Paging with Virtual Scrolling

```tsx
// ❌ WRONG - Conflicting features
<TreeGridComponent
  allowPaging={true}
  enableVirtualization={true} // Conflicts with paging!
>
  <Inject services={[Page, VirtualScroll]} />
</TreeGridComponent>

// ✅ CORRECT - Choose one
// Option 1: Paging for < 1,000 rows
<TreeGridComponent allowPaging={true}>
  <Inject services={[Page]} />
</TreeGridComponent>

// Option 2: Virtual scroll for 1,000+ rows
<TreeGridComponent 
  enableVirtualization={true} 
  height="600px"
>
  <Inject services={[VirtualScroll]} />
</TreeGridComponent>
```

### ❌ Avoid Heavy Column Templates

```tsx
// ❌ WRONG - Heavy computation in template
const HeavyTemplate = (props) => {
  const complexCalculation = performExpensiveOperation(props); // Runs on every render!
  return <div>{complexCalculation}</div>;
};

// ✅ CORRECT - Pre-calculate data
const treeData = useMemo(() => {
  return rawData.map(item => ({
    ...item,
    calculatedValue: performExpensiveOperation(item) // Calculate once
  }));
}, [rawData]);

const LightTemplate = (props) => {
  return <div>{props.calculatedValue}</div>; // Just display
};
```

## Performance Checklist

- ✅ Use virtual scrolling for 1,000+ rows
- ✅ Set consistent `rowHeight` for virtual scroll
- ✅ Memoize data transformations with `useMemo`
- ✅ Memoize event handlers with `useCallback`
- ✅ Memoize templates with `React.memo`
- ✅ Debounce search/filter operations
- ✅ Pre-fetch and merge data (don't call APIs in render events)
- ✅ Cleanup on unmount (`destroy()`)
- ✅ Use server-side operations for 100K+ rows
- ✅ Only inject modules you actually use
- ❌ Never call APIs in `rowDataBound` or `queryCellInfo`
- ❌ Don't combine `allowPaging` with virtual scrolling
- ❌ Avoid heavy computations in column templates