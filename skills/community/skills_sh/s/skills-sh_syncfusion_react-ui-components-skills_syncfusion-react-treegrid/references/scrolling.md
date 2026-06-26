---
name: scrolling
description: 'Scrolling in React TreeGrid - virtual scrolling, infinite scroll, height and width management, and scroll positioning.'
---

# Scrolling

## Table of Contents
- [Scrolling & Paging Rules](#scrolling--paging-rules)
- [Virtual Scrolling](#virtual-scrolling)
- [Infinite Scrolling](#infinite-scrolling)
- [Height and Width](#height-and-width)
- [Scroll Position](#scroll-position)
- [Horizontal Scrolling](#horizontal-scrolling)
- [Key APIs](#key-apis)
- [Common Patterns](#common-patterns)

## Scrolling & Paging Rules

### Rule 1: Virtual Scrolling, Infinite Scrolling, and Paging are MUTUALLY EXCLUSIVE
**Severity**: 🔴 CRITICAL - Cannot use together; will cause conflicts

**Allowed Combinations in React**:
```jsx
// ✅ OPTION 1: enableVirtualization ONLY
<TreeGridComponent 
  dataSource={data}
  enableVirtualization={true}
  allowPaging={false}
  height='600px'>
  <Inject services={[VirtualScroll]} />
</TreeGridComponent>

// ✅ OPTION 2: allowPaging ONLY
<TreeGridComponent 
  dataSource={data}
  allowPaging={true}
  pageSettings={{ pageSize: 20 }}
  enableVirtualization={false}>
  <Inject services={[Page]} />
</TreeGridComponent>

// ✅ OPTION 3: enableInfiniteScrolling ONLY
<TreeGridComponent 
  dataSource={data}
  enableInfiniteScrolling={true}
  allowPaging={false}
  enableVirtualization={false}>
</TreeGridComponent>

// ✅ OPTION 4: No scrolling (small datasets)
<TreeGridComponent 
  dataSource={data}
  allowPaging={false}
  enableVirtualization={false}>
</TreeGridComponent>

// ❌ CONFLICT - Do NOT combine these
<TreeGridComponent 
  enableVirtualization={true}
  allowPaging={true}>  {/* ERROR: Conflicting settings */}
</TreeGridComponent>

// ❌ CONFLICT - Do NOT combine
<TreeGridComponent 
  enableInfiniteScrolling={true}
  allowPaging={true}>  {/* ERROR: Conflicting settings */}
</TreeGridComponent>
```

**When to Use Each**:
| Mode | Use Case | Dataset Size | Performance |
|------|----------|--------------|-------------|
| **Virtual Scrolling** | All rows visible in viewport, smooth scrolling | 1,000 - 100,000+ rows | Excellent |
| **Pagination** | Server-side data fetch per page | Any size | Good |
| **Infinite Scroll** | Progressive loading as user scrolls | 10,000+ rows | Good |
| **None** | Complete data in memory | < 1,000 rows | Fast |

---

### Rule 2: Virtual Scrolling Requires Fixed Height
**Severity**: 🔴 CRITICAL - Virtual scrolling won't work with auto height or percentage height

**Requirement in React**:
```jsx
// ✅ REQUIRED - Must set explicit pixel height
<TreeGridComponent 
  dataSource={data}
  enableVirtualization={true}
  height='600px'>  {/* MANDATORY: Fixed pixel height */}
  <Inject services={[VirtualScroll]} />
</TreeGridComponent>

// ✅ ALTERNATIVE - Use container div with fixed height
<div style={{ height: '600px', width: '100%' }}>
  <TreeGridComponent 
    dataSource={data}
    enableVirtualization={true}>
    <Inject services={[VirtualScroll]} />
  </TreeGridComponent>
</div>

// ❌ WRONG - Auto height breaks virtual scrolling
<TreeGridComponent 
  dataSource={data}
  enableVirtualization={true}
  height='auto'>  {/* ERROR: Will not virtualize properly */}
</TreeGridComponent>

// ❌ WRONG - Percentage height doesn't work
<TreeGridComponent 
  dataSource={data}
  enableVirtualization={true}
  height='100%'>  {/* ERROR: Will not virtualize */}
</TreeGridComponent>

// ❌ WRONG - No height breaks virtual scrolling
<TreeGridComponent 
  dataSource={data}
  enableVirtualization={true}>  {/* ERROR: Will not virtualize */}
</TreeGridComponent>
```

**Height Requirements**:
```jsx
// Virtual scrolling height settings (pixel values only)
height='400px'      // ✅ Small grids
height='600px'      // ✅ Medium grids
height='800px'      // ✅ Large datasets
height='calc(100vh - 100px)'  // ✅ Responsive (with pixel calculation)

// Also set pageSize/rowHeight appropriately
pageSettings={{ pageSize: 100 }}  // Match visible row count
rowHeight={36}                      // Helps virtual scroll calculate viewport
```

---

### Rule 3: Pagination Requires Page Module
**Severity**: 🔴 CRITICAL - Paging won't work without module injection

**Requirement in React**:
```jsx
// ✅ REQUIRED - Page module injection
import { TreeGridComponent, Inject, Page } from '@syncfusion/ej2-react-treegrid';

export default function PaginatedGrid() {
  return (
    <TreeGridComponent 
      dataSource={data}
      allowPaging={true}
      pageSettings={{ pageSize: 20 }}>
      <Inject services={[Page]} />  {/* MANDATORY */}
    </TreeGridComponent>
  );
}

// ✅ Also required: pageSettings configuration
const pageSettings = {
  pageSize: 20,           // Rows per page
  pageCount: 5,           // Navigation buttons to show
  currentPage: 1          // Start page
};

<TreeGridComponent 
  dataSource={data}
  allowPaging={true}
  pageSettings={pageSettings}>
  <Inject services={[Page]} />
</TreeGridComponent>

// ❌ WRONG - Missing Page module injection
<TreeGridComponent 
  dataSource={data}
  allowPaging={true}
  pageSettings={{ pageSize: 20 }}>
  {/* Paging won't work without <Inject services={[Page]} /> */}
</TreeGridComponent>

// ❌ WRONG - Not using Inject
export default function Grid() {
  // Missing: <Inject services={[Page]} />
  return (
    <TreeGridComponent 
      dataSource={data}
      allowPaging={true}>
    </TreeGridComponent>
  );
}
```

---

## Virtual Scrolling

Load large datasets efficiently with virtual scrolling:

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, VirtualScroll } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  const largeData = [];
  for (let i = 1; i <= 10000; i++) {
    largeData.push({
      TaskID: i,
      TaskName: `Task ${i}`,
      StartDate: new Date(2018, 2, 3),
      Duration: Math.floor(Math.random() * 10) + 1,
      Children: []
    });
  }

  return (
    <TreeGridComponent
      dataSource={largeData}
      childMapping="Children"
      height={400}
      enableVirtualization={true}
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
        <ColumnDirective field="StartDate" headerText="Start Date" type="date" format="yMd" width={120} />
        <ColumnDirective field="Duration" headerText="Duration" width={100} />
      </ColumnsDirective>
      <Inject services={[VirtualScroll]} />
    </TreeGridComponent>
  );
}
```

### Virtual Scrolling Benefits
- Supports 100,000+ rows efficiently
- Only renders visible rows in viewport
- Smooth scrolling experience with minimal lag
- Reduces memory footprint significantly
- Improves application performance

### Enable Virtual Scrolling
Key property: `enableVirtualization={true}` - Enables virtual scrolling for all rows

## Infinite Scrolling

Automatically load more data on scroll:

```tsx
import React, { useState } from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-treegrid';

export default function App() {
 
  return (
    <TreeGridComponent
      dataSource={data}
      childMapping="Children"
      height={400}
      enableInfiniteScrolling={true}
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
      </ColumnsDirective>
    </TreeGridComponent>
  );
}
```

### Infinite Scroll Configuration
- Load data in chunks as user scrolls
- Implement server-side pagination
- Track scroll position and trigger load
- Combine with virtual scrolling for optimal performance

## Height and Width

### Fixed Height
Enable vertical scrolling with fixed container height:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  height={500}  // Fixed height in pixels
>
  <ColumnsDirective>
    <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
</TreeGridComponent>
```

### Percentage Height
```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  height="100%"  // Percentage height
>
  <ColumnsDirective>
    <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
  </ColumnsDirective>
</TreeGridComponent>
```

### Auto Height
Grid grows with content (no vertical scroll):

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  height="auto"  // Grows with content
>
  <ColumnsDirective>
    <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
  </ColumnsDirective>
</TreeGridComponent>
```

## Scroll Position

### Get Scroll Position
```tsx
const treeGridRef = React.useRef();

const getScrollPosition = () => {
  const content = treeGridRef.current?.getContent();
  if (content) {
    console.log('Scroll Top:', content.scrollTop);
    console.log('Scroll Left:', content.scrollLeft);
  }
};

// In JSX:
<button onClick={getScrollPosition}>Get Scroll Position</button>
<TreeGridComponent ref={treeGridRef} dataSource={data} childMapping="Children" height={400}>
  {/* columns */}
</TreeGridComponent>
```

### Set Scroll Position
```tsx
const setScrollPosition = () => {
  const content = treeGridRef.current?.getContent();
  if (content) {
    content.scrollTop = 500;
    content.scrollLeft = 100;
  }
};
```

## Horizontal Scrolling

### Enable Horizontal Scroll
```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  height={400}
  width="100%"
>
  <ColumnsDirective>
    <ColumnDirective field="TaskID" headerText="Task ID" width={100} />
    <ColumnDirective field="TaskName" headerText="Task Name" width={200} />
    <ColumnDirective field="StartDate" headerText="Start Date" width={120} />
    <ColumnDirective field="EndDate" headerText="End Date" width={120} />
    <ColumnDirective field="Priority" headerText="Priority" width={100} />
    <ColumnDirective field="Status" headerText="Status" width={100} />
    <ColumnDirective field="Duration" headerText="Duration" width={100} />
  </ColumnsDirective>
</TreeGridComponent>
```

### Frozen Columns with Horizontal Scroll
Keep specific columns frozen while others scroll:

```tsx
// First column stays frozen, others scroll horizontally
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  height={400}
  frozenColumns={1}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskID" headerText="Task ID" width={100} /> {/* Frozen */}
    <ColumnDirective field="TaskName" headerText="Task Name" width={200} />
    <ColumnDirective field="StartDate" headerText="Start Date" width={120} />
  </ColumnsDirective>
</TreeGridComponent>
```

---

## Key APIs

| Property/Method | Type | Description |
|---|---|---|
| `height` | number/string | Container height (pixels, percentage, or 'auto') |
| `width` | number/string | Container width |
| `enableVirtualization` | boolean | Enable virtual scrolling for large datasets |
| `frozenRows` | number | Number of rows to freeze from top |
| `frozenColumns` | number | Number of columns to freeze from left |
| `getContent` | method | Get scrollable content container |
| `scrollTop` | property | Get/set vertical scroll position |
| `scrollLeft` | property | Get/set horizontal scroll position |
| `recordDoubleClick` | event | Fires on row double-click |

## Common Patterns

1. **Fixed Height with Virtual Scroll**: Combine fixed height with virtual scrolling for large datasets (1000+ rows)
2. **Responsive Height**: Calculate height based on available viewport space
3. **Scroll to Top**: Reset scroll position on data refresh or filter change
4. **Sticky Headers**: Use frozen rows to keep headers visible while scrolling
5. **Horizontal Scroll Prevention**: Set explicit column widths to trigger horizontal scroll
6. **Performance**: Use virtual scrolling instead of paging for better UX with large datasets

## Common Issues

### Virtual Scroll Not Working
- Ensure `enableVirtualization={true}` is set
- Grid must have fixed height (not 'auto')
- Works best with 1000+ rows
- Check that `childMapping` is configured for hierarchical data

### Horizontal Scroll Not Appearing
- Total column width must exceed container width
- Set explicit widths on columns (avoid default auto)
- Enable horizontal scroll by setting width="100%"

### Performance Issues with Large Data
- Use virtual scrolling instead of paging
- Implement server-side data loading
- Reduce number of rendered columns
- Apply column filtering to limit initial data
- Avoid complex cell templates

