# Sorting and Ordering

## Table of Contents

1. [Overview](#overview)
2. [Global Sorting](#global-sorting)
3. [Level-Wise Sorting](#level-wise-sorting)
4. [Custom Sorting Algorithms](#custom-sorting-algorithms)
5. [DataManager Query Sorting](#datamanager-query-sorting)
6. [Sorting Events](#sorting-events)
7. [Performance Considerations](#performance-considerations)
8. [Troubleshooting](#troubleshooting)

## Overview

TreeView supports multiple sorting approaches:

| Method | Scope | Complexity | Performance |
|--------|-------|-----------|-------------|
| Global | Entire tree | Low | Fast |
| Level-wise | Per level | Medium | Good |
| Custom | Custom logic | High | Depends on algorithm |
| DataManager | Server-side | Medium | Best for remote data |

## Global Sorting

Sort entire tree ascending or descending:

### sortOrder Property

```tsx
import * as React from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  const data = [
    { id: 3, name: 'Zebra' },
    { id: 1, name: 'Apple' },
    { id: 2, name: 'Mango' }
  ];

  return (
    <div>
      {/* Ascending */}
      <TreeViewComponent
        fields={{ dataSource: data, id: 'id', text: 'name' }}
        sortOrder="Ascending"
      />

      {/* Descending */}
      <TreeViewComponent
        fields={{ dataSource: data, id: 'id', text: 'name' }}
        sortOrder="Descending"
      />

      {/* No sorting (default) */}
      <TreeViewComponent
        fields={{ dataSource: data, id: 'id', text: 'name' }}
        sortOrder="None"
      />
    </div>
  );
}

export default App;
```

### Programmatic Sorting

```tsx
// Pre-sort data before binding
const sortedData = [...data].sort((a, b) => 
  a.name.localeCompare(b.name)
);

<TreeViewComponent
  fields={{ dataSource: sortedData, id: 'id', text: 'name' }}
/>
```

## Level-Wise Sorting

Sort each level independently:

### Different Sort Per Level

```tsx
function sortByLevel(data, sortFunctions) {
  return data.map(node => {
    const levelFunc = sortFunctions[0]; // Root level
    if (levelFunc) {
      // Don't mutate original
    }
    if (node.child) {
      node.child = sortByLevel(node.child, sortFunctions.slice(1));
    }
    return node;
  }).sort(sortFunctions[0]);
}

// Define sort for each level
const levelSort = [
  (a, b) => a.name.localeCompare(b.name),      // Level 0: alphabetical
  (a, b) => b.priority - a.priority,            // Level 1: by priority DESC
  (a, b) => new Date(a.date) - new Date(b.date) // Level 2: by date
];

const sorted = sortByLevel(data, levelSort);
```

### Practical Level-Wise Example

```tsx
function App() {
  const organizationData = [
    {
      id: 1,
      name: 'CEO',
      level: 0,
      priority: 1,
      child: [
        { id: 2, name: 'Manager A', level: 1, priority: 3 },
        { id: 3, name: 'Manager B', level: 1, priority: 2 },
        { id: 4, name: 'Manager C', level: 1, priority: 1 }
      ]
    },
    {
      id: 5,
      name: 'VP',
      level: 0,
      priority: 2,
      child: [
        { id: 6, name: 'Director A', level: 1, priority: 2 },
        { id: 7, name: 'Director B', level: 1, priority: 1 }
      ]
    }
  ];

  // Sort: Level 0 by priority, Level 1 by name
  function sortByLevelAndProperty(data) {
    const sortFunction = (nodes, level) => {
      return nodes.sort((a, b) => {
        if (level === 0) {
          return a.priority - b.priority; // Level 0: priority
        } else {
          return a.name.localeCompare(b.name); // Level 1+: name
        }
      }).map(node => ({
        ...node,
        child: node.child ? sortFunction(node.child, level + 1) : node.child
      }));
    };

    return sortFunction(data, 0);
  }

  const sorted = sortByLevelAndProperty(organizationData);

  return (
    <TreeViewComponent
      fields={{
        dataSource: sorted,
        id: 'id',
        text: 'name',
        child: 'child'
      }}
    />
  );
}

export default App;
```

## Custom Sorting Algorithms

### Sort by Multiple Properties

```tsx
function multiPropertySort(data, properties) {
  // properties = [{ field: 'priority', order: 'asc' }, { field: 'name', order: 'asc' }]
  
  const sorted = (nodes) => nodes.sort((a, b) => {
    for (const prop of properties) {
      const aVal = a[prop.field];
      const bVal = b[prop.field];

      let comparison = 0;
      if (typeof aVal === 'string') {
        comparison = aVal.localeCompare(bVal);
      } else {
        comparison = aVal - bVal;
      }

      if (comparison !== 0) {
        return prop.order === 'asc' ? comparison : -comparison;
      }
    }
    return 0;
  }).map(node => ({
    ...node,
    child: node.child ? sorted(node.child) : node.child
  }));

  return sorted(data);
}

// Usage
const result = multiPropertySort(data, [
  { field: 'priority', order: 'asc' },
  { field: 'name', order: 'asc' }
]);
```

### Sort by Computed Value

```tsx
function sortByComputedValue(data, computeFunc) {
  const withComputed = data.map(node => ({
    ...node,
    _sortValue: computeFunc(node),
    child: node.child ? sortByComputedValue(node.child, computeFunc) : node.child
  }));

  return withComputed.sort((a, b) => a._sortValue - b._sortValue);
}

// Example: Sort by number of children
const sorted = sortByComputedValue(data, (node) => node.child ? node.child.length : 0);
```

### Natural Sort (Alphanumeric)

```tsx
function naturalSort(a, b) {
  const aStr = a.name;
  const bStr = b.name;

  return aStr.localeCompare(bStr, undefined, {
    numeric: true,
    sensitivity: 'base'
  });
}

// Usage
const sorted = data.sort(naturalSort);
```

### Case-Insensitive Sort

```tsx
const caseSensitiveData = data.sort((a, b) => 
  a.name.toLowerCase().localeCompare(b.name.toLowerCase())
);
```

## DataManager Query Sorting

Sort using DataManager Query:

### Basic Query Sort

```tsx
import { DataManager, Query } from '@syncfusion/ej2-data';

const data = new DataManager([
  { id: 3, name: 'Zebra' },
  { id: 1, name: 'Apple' },
  { id: 2, name: 'Mango' }
]);

// Ascending
const query = new Query().sortBy('name');
const result = data.executeLocal(query);

// Descending
const queryDesc = new Query().sortBy('name', undefined, true); // true = descending
const resultDesc = data.executeLocal(queryDesc);
```

### Multiple Sort Fields

```tsx
const query = new Query()
  .sortBy('category')
  .sortBy('name');

const result = data.executeLocal(query);
```

### Remote Data Sorting

```tsx
import { DataManager, WebApiAdaptor, Query } from '@syncfusion/ej2-data';

const data = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor()
});

const query = new Query()
  .sortBy('priority', undefined, true); // Sort by priority DESC

const result = data.executeQuery(query);
```

## Sorting Events

### Sort Before Rendering

```tsx
function App() {
  const [data, setData] = React.useState(originalData);

  const handleNodeExpanded = (args) => {
    // Sort children when parent expands
    if (args.nodeData.child) {
      args.nodeData.child.sort((a, b) => 
        a.name.localeCompare(b.name)
      );
    }
  };

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', text: 'name', child: 'child' }}
      onNodeExpanding={handleNodeExpanded}
    />
  );
}
```

### Dynamic Re-sort

```tsx
const treeRef = React.useRef(null);

function resortTree(sortField, order) {
  if (treeRef.current) {
    const data = treeRef.current.fields.dataSource;
    const sorted = sortTree(data, sortField, order);
    // Update TreeView data
    setData(sorted);
  }
}

return (
  <div>
    <select onChange={(e) => resortTree(e.target.value, 'asc')}>
      <option value="name">Sort by Name</option>
      <option value="priority">Sort by Priority</option>
    </select>

    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: data, id: 'id', text: 'name' }}
    />
  </div>
);
```

## Performance Considerations

### Memoize Sorted Data

```tsx
const sortedData = React.useMemo(() => {
  return [...data].sort((a, b) => a.name.localeCompare(b.name));
}, [data]);

<TreeViewComponent
  fields={{ dataSource: sortedData, id: 'id', text: 'name' }}
/>
```

### Sort Large Datasets Efficiently

```tsx
// ✅ Sort before binding to TreeView
const sorted = [...largeData].sort(compareFn); // O(n log n)

<TreeViewComponent
  fields={{ dataSource: sorted, id: 'id', text: 'name' }}
/>

// ❌ Avoid: Sorting inside TreeView events (called many times)
onNodeExpanding={(args) => {
  args.nodeData.child.sort(...); // Bad - sorting every expand
}}
```

### Use Stable Sort

```tsx
// JavaScript sort is stable (since ES2019)
// Same order preserved for equal elements
const data = [
  { id: 1, name: 'Apple', priority: 1 },
  { id: 2, name: 'Apricot', priority: 1 }
];

const sorted = data.sort((a, b) => a.priority - b.priority);
// 'Apple' stays before 'Apricot' (stable sort)
```

## Troubleshooting

### sortOrder Not Working

```tsx
// ✅ Correct property name
<TreeViewComponent
  sortOrder="Ascending"  // ✅ sortOrder
/>

// ❌ Wrong
<TreeViewComponent
  sort="Ascending"  // ❌ Should be sortOrder
/>
```

### Custom Sort Not Applied

```tsx
// ❌ Wrong - Modifying original array
const newData = data.sort(...);

// ✅ Correct - Create new array
const newData = [...data].sort(...);

// Update TreeView
setData(newData);
```

### Child Nodes Not Sorted

```tsx
// ✅ Correct - Sort recursively
function sortRecursive(nodes) {
  return nodes
    .sort((a, b) => a.name.localeCompare(b.name))
    .map(node => ({
      ...node,
      child: node.child ? sortRecursive(node.child) : node.child
    }));
}

const sorted = sortRecursive(data);
```

---

**Key Takeaways:**
- ✅ Use `sortOrder` property for global sorting
- ✅ Implement custom functions for level-wise sorting
- ✅ Use DataManager Query for remote data
- ✅ Sort before binding for better performance
- ✅ Memoize sorted results to prevent re-sorts
- ✅ Apply sorting recursively for nested data

