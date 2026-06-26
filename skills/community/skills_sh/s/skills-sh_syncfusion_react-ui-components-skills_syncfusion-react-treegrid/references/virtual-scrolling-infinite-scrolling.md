---
name: virtual-scrolling-infinite-scrolling
description: 'Virtual Scrolling and Infinite Scrolling in React TreeGrid - virtual scroll for 1000+ rows, infinite scroll with caching, performance optimization.'
---

# Virtual Scrolling and Infinite Scrolling

## Table of Contents
- [Virtual Scrolling](#virtual-scrolling)
- [Infinite Scrolling](#infinite-scrolling)
- [Performance Tips](#performance-tips)
- [Common Patterns](#common-patterns)

## Virtual Scrolling

Render only visible rows and columns for performance with large datasets.

### Virtual Scrolling - Row Virtualization

Render only visible rows to handle large vertical scrolling datasets:

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, VirtualScroll } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  // Generate 10,000 rows of data
  const data = Array.from({ length: 10000 }, (_, i) => ({
    TaskID: i + 1,
    TaskName: `Task ${i + 1}`,
    Duration: Math.floor(Math.random() * 10) + 1,
    Children: []
  }));

  return (
    <TreeGridComponent
      dataSource={data}
      childMapping="Children"
      height={400}
      enableVirtualization={true}
      rowHeight={30}
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

**Use when:**
- Large datasets with thousands of rows
- Consistent row heights
- Vertical scrolling is the primary interaction

### Virtual Scrolling - Column Virtualization

Render only visible columns to handle grids with many columns:

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, VirtualScroll } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  // Generate data with many columns
  const data = Array.from({ length: 5000 }, (_, i) => {
    const row = {
      TaskID: i + 1,
      TaskName: `Task ${i + 1}`,
      Children: []
    };
    // Add 50 additional columns
    for (let j = 0; j < 50; j++) {
      row[`Column${j}`] = `Value ${i}-${j}`;
    }
    return row;
  });

  return (
    <TreeGridComponent
      dataSource={data}
      childMapping="Children"
      height={400}
      width="100%"
      enableVirtualization={true}
      virtualScrollSettings={{ mode: 'Both' }}
      rowHeight={30}
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={200} />
        {Array.from({ length: 50 }, (_, i) => (
          <ColumnDirective key={i} field={`Column${i}`} headerText={`Col ${i}`} width={100} />
        ))}
      </ColumnsDirective>
      <Inject services={[VirtualScroll]} />
    </TreeGridComponent>
  );
}
```

**Use when:**
- Many columns (50+) to display
- Horizontal scrolling is frequent
- Need to optimize memory for wide grids

## Infinite Scrolling

Load data on-demand as user scrolls.

### Infinite Scrolling - Normal Mode

Load data without caching previously loaded blocks:

```tsx
import React, { useState } from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, InfiniteScroll } from '@syncfusion/ej2-react-treegrid';
import { DataManager, UrlAdaptor } from '@syncfusion/ej2-data';

export default function App() {
  const dataManager = new DataManager({
    url: 'url',
    adaptor: new UrlAdaptor()
  });

  return (
    <TreeGridComponent
      dataSource={dataManager}
      childMapping="Children"
      height={400}
      enableInfiniteScrolling={true}
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
      </ColumnsDirective>
      <Inject services={[InfiniteScroll]} />
    </TreeGridComponent>
  );
}
```

**Use when:**
- Memory is limited
- Re-fetching data is acceptable
- Large datasets where caching all blocks would use too much memory

### Infinite Scrolling - Cache Mode

Load data with caching for faster re-access to previously loaded blocks:

```tsx
import React, { useState } from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, InfiniteScroll } from '@syncfusion/ej2-react-treegrid';
import { DataManager, UrlAdaptor } from '@syncfusion/ej2-data';

export default function App() {
  const dataManager = new DataManager({
    url: 'url',
    adaptor: new UrlAdaptor()
  });

  return (
    <TreeGridComponent
      dataSource={dataManager}
      childMapping="Children"
      height={400}
      enableInfiniteScrolling={true}
      infiniteScrollSettings={{ 
        enableCache: true,
      }}
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
      </ColumnsDirective>
      <Inject services={[InfiniteScroll]} />
    </TreeGridComponent>
  );
}
```

**Use when:**
- Users scroll back and forth frequently
- Memory is available
- Want faster performance when revisiting previously scrolled sections

## Performance Tips

1. **Set Accurate Row Height**: `rowHeight` must match actual row height
2. **Use DataManager**: Pair virtual scroll with DataManager for remote data
3. **Disable Features**: Turn off features not needed (aggregates, grouping) to improve performance
4. **Batch Size**: Configure appropriate data batch size for infinite scroll

## Key APIs

| Property | Type | Description |
|---|---|---|
| `enableVirtualization` | boolean | Enable virtual scrolling |
| `rowHeight` | number | Height of each row |
| `enableInfiniteScrolling` | boolean | Enable infinite scrolling |
| `infiniteScrollSettings` | object | Configure infinite scroll |
| `mode` | string | 'Continuous' or 'OnDemand' |
| `enableCache` | boolean | Cache loaded pages |

## Common Patterns

1. **Large Dataset Display**: Use virtual scroll for 10,000+ rows
2. **Server-side Paging**: Use infinite scroll for API-driven data
3. **Memory Optimization**: Virtual scroll reduces DOM elements

