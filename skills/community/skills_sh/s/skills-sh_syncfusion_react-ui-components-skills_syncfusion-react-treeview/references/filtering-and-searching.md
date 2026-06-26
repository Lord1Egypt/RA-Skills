# Filtering and Searching

## Table of Contents

1. [Overview](#overview)
2. [Text-Based Filtering](#text-based-filtering)
3. [Parent Chain Inclusion](#parent-chain-inclusion)
4. [DataManager Filtering with Predicates](#datamanager-filtering-with-predicates)
5. [Dynamic Filtering](#dynamic-filtering)
6. [Advanced Filter Patterns](#advanced-filter-patterns)
7. [Combining Filters](#combining-filters)
8. [Performance Optimization](#performance-optimization)
9. [Troubleshooting](#troubleshooting)

## Overview

TreeView filtering allows you to:
- Search nodes by text
- Filter by custom conditions
- Include parent nodes in results
- Dynamically update filters
- Preserve tree hierarchy in filtered view

## Text-Based Filtering

### Simple Text Search

```tsx
import * as React from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  const [searchText, setSearchText] = React.useState('');
  const [filteredData, setFilteredData] = React.useState([]);
  const [originalData] = React.useState([
    { id: 1, name: 'Angular', expanded: true },
    { id: 2, name: 'React' },
    { id: 3, name: 'Vue' },
    { id: 4, name: 'Angular Forms', expanded: true },
    { id: 5, name: 'Angular Router' }
  ]);

  const handleSearch = (text) => {
    setSearchText(text);
    
    if (!text) {
      setFilteredData(originalData);
      return;
    }

    // Simple filtering - shows only matching nodes
    const filtered = originalData.filter(node =>
      node.name.toLowerCase().includes(text.toLowerCase())
    );

    setFilteredData(filtered);
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Search..."
        value={searchText}
        onChange={(e) => handleSearch(e.target.value)}
      />

      <TreeViewComponent
        fields={{
          dataSource: filteredData,
          id: 'id',
          text: 'name',
          expanded: 'expanded'
        }}
      />
    </div>
  );
}

export default App;
```

### Search with Highlighting

```tsx
const nodeTemplate = (data) => {
  const regex = new RegExp(searchText, 'gi');
  const highlighted = data.name.replace(
    regex,
    (match) => `<mark>${match}</mark>`
  );

  return <div dangerouslySetInnerHTML={{ __html: highlighted }} />;
};
```

## Parent Chain Inclusion

**Key Concept:** When filtering, include parent nodes so filtered nodes appear in context.

### Example: Show Parents of Matching Nodes

```tsx
function filterWithParents(data, searchText) {
  // Recursively collect matching nodes
  const matchingIds = new Set();

  function findMatches(nodes) {
    nodes.forEach(node => {
      if (node.name.toLowerCase().includes(searchText.toLowerCase())) {
        matchingIds.add(node.id);
      }
      if (node.child) {
        findMatches(node.child);
      }
    });
  }

  // Mark all ancestors of matching nodes
  const parentIds = new Set();

  function markAncestors(nodes, parentId = null) {
    nodes.forEach(node => {
      if (matchingIds.has(node.id)) {
        if (parentId) parentIds.add(parentId);
        // Mark all ancestors
        let current = parentId;
        while (current) {
          parentIds.add(current);
          // Find parent of current (needs parent mapping)
          current = null;
        }
      }
      if (node.child) {
        markAncestors(node.child, node.id);
      }
    });
  }

  // Filter result includes matches and their parents
  function filterResult(nodes) {
    return nodes.filter(node => {
      const include = matchingIds.has(node.id) || parentIds.has(node.id);
      if (include && node.child) {
        node.child = filterResult(node.child);
      }
      return include;
    });
  }

  findMatches(data);
  markAncestors(data);
  return filterResult(data);
}

// Usage
const filtered = filterWithParents(originalData, 'Angular');
```

## DataManager Filtering with Predicates

### Using Predicate for Complex Filters

```tsx
import { DataManager, Predicate, Query } from '@syncfusion/ej2-data';

function App() {
  const data = [
    { id: 1, name: 'Angular', category: 'Framework', popularity: 9 },
    { id: 2, name: 'React', category: 'Library', popularity: 10 },
    { id: 3, name: 'Vue', category: 'Framework', popularity: 8 },
    { id: 4, name: 'Svelte', category: 'Framework', popularity: 7 }
  ];

  // Filter: category === 'Framework' AND popularity >= 8
  const predicate = new Predicate('category', 'equal', 'Framework')
    .and('popularity', 'greaterThanOrEqual', 8);

  const query = new Query().where(predicate);
  const manager = new DataManager(data);
  const result = manager.executeLocal(query);

  console.log(result); // Returns matching nodes
}
```

### Predicate Operators

```tsx
// Equality
new Predicate('status', 'equal', 'active')
new Predicate('status', 'notequal', 'inactive')

// Comparison
new Predicate('priority', 'greaterThan', 5)
new Predicate('priority', 'greaterThanOrEqual', 5)
new Predicate('priority', 'lessThan', 10)
new Predicate('priority', 'lessThanOrEqual', 10)

// Text matching
new Predicate('name', 'contains', 'Angular')
new Predicate('name', 'startsWith', 'An')
new Predicate('name', 'endsWith', 'ar')

// Case-insensitive
new Predicate('name', 'contains', 'angular', false, true) // ignoreCase=true

// Multiple conditions
new Predicate('status', 'equal', 'active')
  .and('priority', 'greaterThan', 5)
  .or('category', 'equal', 'important')
```

## Dynamic Filtering

### Filter on Input Change

```tsx
import * as React from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';
import { DataManager, Predicate, Query } from '@syncfusion/ej2-data';

function App() {
  const [search, setSearch] = React.useState('');
  const [filtered, setFiltered] = React.useState([]);
  const originalData = [ /* your data */ ];

  const handleSearch = (text) => {
    setSearch(text);

    if (!text) {
      setFiltered(originalData);
      return;
    }

    // Create predicate for case-insensitive search
    const predicate = new Predicate('name', 'contains', text, false, true);
    const query = new Query().where(predicate);
    
    const manager = new DataManager(originalData);
    const result = manager.executeLocal(query);
    
    setFiltered(result);
  };

  return (
    <>
      <input
        placeholder="Search nodes..."
        value={search}
        onChange={(e) => handleSearch(e.target.value)}
      />

      <TreeViewComponent
        fields={{
          dataSource: filtered,
          id: 'id',
          text: 'name'
        }}
      />
    </>
  );
}
```

### Multi-Field Search

```tsx
const handleSearch = (text) => {
  if (!text) {
    setFiltered(originalData);
    return;
  }

  // Search in multiple fields
  const predicate1 = new Predicate('name', 'contains', text, false, true);
  const predicate2 = new Predicate('category', 'contains', text, false, true);
  const predicate3 = new Predicate('description', 'contains', text, false, true);

  const combined = predicate1.or(predicate2).or(predicate3);
  const query = new Query().where(combined);
  
  const result = new DataManager(originalData).executeLocal(query);
  setFiltered(result);
};
```

## Advanced Filter Patterns

### Filter by Custom Property

```tsx
// Filter nodes where isActive === true
const filtered = originalData.filter(node => node.isActive === true);

// Filter nodes by type
const filtered = originalData.filter(node => node.type === 'folder');

// Filter with compound conditions
const filtered = originalData.filter(node => 
  node.isActive && node.priority > 5 && node.category === 'important'
);
```

### Range Filter

```tsx
function filterByRange(data, min, max, property = 'priority') {
  return data.filter(node => {
    const value = node[property];
    return value >= min && value <= max;
  });
}

// Usage
const results = filterByRange(data, 5, 10, 'priority');
```

### Date Filter

```tsx
function filterByDateRange(data, startDate, endDate) {
  return data.filter(node => {
    const nodeDate = new Date(node.createdDate);
    return nodeDate >= startDate && nodeDate <= endDate;
  });
}

// Usage
const start = new Date('2024-01-01');
const end = new Date('2024-12-31');
const results = filterByDateRange(data, start, end);
```

## Combining Filters

### AND Condition

```tsx
// All conditions must be true
const filtered = data.filter(node =>
  node.status === 'active' &&
  node.priority >= 5 &&
  node.name.includes('Angular')
);
```

### OR Condition

```tsx
// At least one condition must be true
const filtered = data.filter(node =>
  node.category === 'Framework' ||
  node.category === 'Library' ||
  node.category === 'Tool'
);
```

### Complex Conditions

```tsx
// (status === 'active' AND priority >= 5) OR (featured === true)
const filtered = data.filter(node =>
  (node.status === 'active' && node.priority >= 5) ||
  node.featured === true
);

// Using Predicates
const cond1 = new Predicate('status', 'equal', 'active')
  .and('priority', 'greaterThanOrEqual', 5);
const cond2 = new Predicate('featured', 'equal', true);

const combined = cond1.or(cond2);
const query = new Query().where(combined);
```

## Performance Optimization

### Memoize Filter Results

```tsx
import React, { useMemo } from 'react';

function App() {
  const [search, setSearch] = React.useState('');
  const [originalData] = React.useState(/* large dataset */);

  // Memoize filtered result - only recalculate when search changes
  const filtered = useMemo(() => {
    if (!search) return originalData;
    
    return originalData.filter(node =>
      node.name.toLowerCase().includes(search.toLowerCase())
    );
  }, [search, originalData]);

  return (
    <div>
      <input
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
      <TreeViewComponent
        fields={{ dataSource: filtered, id: 'id', text: 'name' }}
      />
    </div>
  );
}
```

### Debounce Search Input

```tsx
import React, { useState, useEffect } from 'react';

function useDebounce(value, delay) {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(handler);
  }, [value, delay]);

  return debounced;
}

function App() {
  const [search, setSearch] = useState('');
  const debouncedSearch = useDebounce(search, 300); // Wait 300ms

  const filtered = useMemo(() => {
    // Filter only when debounced value changes
    if (!debouncedSearch) return originalData;
    return originalData.filter(node =>
      node.name.toLowerCase().includes(debouncedSearch.toLowerCase())
    );
  }, [debouncedSearch]);

  return (
    <input
      value={search}
      onChange={(e) => setSearch(e.target.value)}
      placeholder="Search..."
    />
  );
}
```

### Lazy Filtering with Load-on-Demand

```tsx
// Only filter visible nodes (not entire tree)
function App() {
  const [expandedNodes, setExpandedNodes] = React.useState([]);

  const handleNodeExpanding = (args) => {
    // Filter happens on expand - only for visible branches
    setExpandedNodes([...expandedNodes, args.nodeData.id]);
  };

  return (
    <TreeViewComponent
      onNodeExpanding={handleNodeExpanding}
      loadOnDemand={true}
    />
  );
}
```

## Troubleshooting

### Filter Not Working

```tsx
// ❌ Wrong - Case-sensitive search
const filtered = data.filter(node => node.name === searchText);

// ✅ Correct - Case-insensitive
const filtered = data.filter(node => 
  node.name.toLowerCase().includes(searchText.toLowerCase())
);
```

### Parent Not Showing in Filtered Results

```tsx
// ❌ Wrong - Filters only matching nodes
const filtered = data.filter(node => node.name.includes('Angular'));

// ✅ Correct - Includes parent nodes
function filterWithParents(data, searchText) {
  const matches = new Set();
  
  // Find all matches
  function findMatches(nodes) {
    nodes.forEach(node => {
      if (node.name.includes(searchText)) matches.add(node.id);
      if (node.child) findMatches(node.child);
    });
  }

  // Include matches and their parents
  function filterResult(nodes) {
    return nodes.filter(node => {
      if (matches.has(node.id)) return true;
      if (node.child) {
        node.child = filterResult(node.child);
        return node.child.length > 0;
      }
      return false;
    });
  }

  findMatches(data);
  return filterResult(data);
}
```

### Predicate Returns Empty

```tsx
// ❌ Wrong - Property name doesn't exist
const predicate = new Predicate('label', 'contains', 'text'); // Data has 'name' not 'label'

// ✅ Correct
const predicate = new Predicate('name', 'contains', 'text');
```

---

**Key Takeaways:**
- ✅ Use `.toLowerCase()` for case-insensitive search
- ✅ Include parent nodes in filtered results
- ✅ Use DataManager Predicates for complex filters
- ✅ Memoize filter results for performance
- ✅ Debounce search input for large datasets
- ✅ Test filter logic with edge cases

