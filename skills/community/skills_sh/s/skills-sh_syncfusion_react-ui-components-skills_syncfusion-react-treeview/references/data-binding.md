# Data Binding and Sources

## Table of Contents

1. [Overview](#overview)
2. [Hierarchical Data Binding](#hierarchical-data-binding)
3. [Self-Referential Data Binding](#self-referential-data-binding)
4. [DataManager Integration](#datamanager-integration)
5. [Remote Data with OData](#remote-data-with-odata)
6. [Remote Data with Web API](#remote-data-with-web-api)
7. [Load-on-Demand Binding](#load-on-demand-binding)
8. [Data Binding Events](#data-binding-events)
9. [Field Mapping Reference](#field-mapping-reference)
10. [Troubleshooting](#troubleshooting)

## Overview

TreeView supports 5 primary data binding approaches:

| Method | Use Case | Performance | Complexity |
|--------|----------|-------------|-----------|
| Hierarchical | Nested arrays in memory | Good | Simple |
| Self-Referential | Flat arrays with parentID | Good | Simple |
| OData | Standardized remote API | Better | Medium |
| Web API | Custom backend API | Better | Medium |
| Load-on-Demand | Large datasets, lazy load | Best | Complex |

Choose based on data structure and size:
- **<1000 nodes:** Hierarchical or Self-Referential
- **1000-10000 nodes:** Web API with load-on-demand
- **10000+ nodes:** Load-on-demand with caching

## Hierarchical Data Binding

Data organized as nested arrays with `child` property:

### Basic Hierarchical Example

```tsx
import * as React from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  const hierarchicalData = [
    {
      id: 1,
      name: 'Syncfusion',
      expanded: true,
      child: [
        { id: 2, name: 'React Components' },
        { id: 3, name: 'Angular Components' },
        { id: 4, name: 'Vue Components' }
      ]
    },
    {
      id: 5,
      name: 'Essential Studio',
      expanded: false,
      child: [
        { id: 6, name: 'Web' },
        { id: 7, name: 'Desktop' }
      ]
    }
  ];

  return (
    <TreeViewComponent
      fields={{
        dataSource: hierarchicalData,
        id: 'id',
        text: 'name',
        child: 'child',
        expanded: 'expanded'
      }}
    />
  );
}

export default App;
```

### Multi-Level Nesting

```tsx
const deepData = [
  {
    id: 1,
    name: 'Level 0',
    child: [
      {
        id: 2,
        name: 'Level 1.1',
        child: [
          { id: 3, name: 'Level 2.1' },
          { id: 4, name: 'Level 2.2' }
        ]
      },
      {
        id: 5,
        name: 'Level 1.2',
        child: [
          { id: 6, name: 'Level 2.3' }
        ]
      }
    ]
  }
];

<TreeViewComponent
  fields={{
    dataSource: deepData,
    id: 'id',
    text: 'name',
    child: 'child'
  }}
/>
```

### Fields Configuration

```tsx
const fields = {
  dataSource: data,           // Array of data
  id: 'id',                   // Unique identifier property
  text: 'name',               // Display text property
  child: 'child',             // Children array property
  expanded: 'expanded',       // Initial expand state (optional)
  selected: 'selected',       // Initial selection (optional)
  iconCss: 'icon',            // Icon CSS class (optional)
  imageUrl: 'image',          // Image URL (optional)
  tooltip: 'tooltip',         // Tooltip text (optional)
  htmlAttributes: 'attr'      // HTML attributes (optional)
};
```

## Self-Referential Data Binding

Flat array with parent-child relationship via IDs:

### Basic Self-Referential Example

```tsx
import * as React from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  const selfRefData = [
    { id: 1, pid: null, name: 'Syncfusion', hasChild: true },
    { id: 2, pid: 1, name: 'React Components' },
    { id: 3, pid: 1, name: 'Angular Components' },
    { id: 4, pid: 1, name: 'Vue Components' },
    { id: 5, pid: null, name: 'Essential Studio', hasChild: true },
    { id: 6, pid: 5, name: 'Web' },
    { id: 7, pid: 5, name: 'Desktop' }
  ];

  return (
    <TreeViewComponent
      fields={{
        dataSource: selfRefData,
        id: 'id',
        parentID: 'pid',        // Parent reference
        text: 'name',
        hasChildren: 'hasChild' // Leaf detection
      }}
    />
  );
}

export default App;
```

### Self-Referential Fields

```tsx
const fields = {
  dataSource: data,
  id: 'id',              // Unique ID
  parentID: 'pid',       // Parent ID (null = root node)
  text: 'name',          // Display text
  hasChildren: 'hasChild' // Boolean: has children?
};
```

### When to Use Self-Referential

- ✅ Data from database query (flat result set)
- ✅ Load-on-demand (children loaded separately)
- ✅ Dynamically adding/removing nodes
- ✅ Large datasets (better DB query support)
- ❌ Not recommended for pre-loaded hierarchical data

## DataManager Integration

DataManager handles remote data and querying:

### Basic DataManager Example

```tsx
import * as React from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';
import { DataManager, Query, ODataV4Adaptor } from '@syncfusion/ej2-data';

function App() {
  const data = new DataManager({
    url: 'url',
    adaptor: new ODataV4Adaptor()
  });

  const query = new Query()
    .select(['OrderID', 'CustomerName', 'Freight'])
    .take(50);

  return (
    <TreeViewComponent
      fields={{
        dataSource: data,
        id: 'OrderID',
        text: 'CustomerName',
        query: query
      }}
    />
  );
}

export default App;
```

## Remote Data with OData

Standard OData v4 service integration:

### OData Setup

```tsx
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';
import { DataManager, Query, ODataV4Adaptor } from '@syncfusion/ej2-data';

function App() {
  const data = new DataManager({
    url: 'url',
    adaptor: new ODataV4Adaptor()
  });

  const query = new Query()
    .select(['ID', 'FirstName', 'LastName'])
    .filter('FirstName', 'equal', 'John')
    .take(100);

  return (
    <TreeViewComponent
      fields={{
        dataSource: data,
        id: 'ID',
        text: 'FirstName',
        query: query
      }}
    />
  );
}

export default App;
```

## Remote Data with Web API

Custom Web API integration:

### Web API Setup

```tsx
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';
import { DataManager, Query, WebApiAdaptor } from '@syncfusion/ej2-data';

function App() {
  const data = new DataManager({
    url: 'url',
    adaptor: new WebApiAdaptor()
  });

  const query = new Query()
    .select(['id', 'text', 'parentID'])
    .addParams('pageSize', 50);

  return (
    <TreeViewComponent
      fields={{
        dataSource: data,
        id: 'id',
        parentID: 'parentID',
        text: 'text',
        query: query,
        hasChildren: 'hasChildren'
      }}
      loadOnDemand={true}
    />
  );
}

export default App;
```

### Server Response Format

Expected JSON response:

```json
{
  "result": [
    { "id": 1, "text": "Parent 1", "parentID": null, "hasChildren": true },
    { "id": 2, "text": "Child 1.1", "parentID": 1, "hasChildren": false },
    { "id": 3, "text": "Child 1.2", "parentID": 1, "hasChildren": true }
  ],
  "count": 3
}
```

## Load-on-Demand Binding

Lazy load children when parent expands:

### Basic Load-on-Demand

```tsx
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';
import { DataManager, Query, WebApiAdaptor } from '@syncfusion/ej2-data';

function App() {
  const data = new DataManager({
    url: 'url',
    adaptor: new WebApiAdaptor()
  });

  const query = new Query()
    .select(['id', 'text', 'parentID', 'hasChildren'])
    .where('parentID', 'equal', null); // Load only root nodes initially

  const handleNodeExpanding = (args) => {
    // When node expands, query for its children
    if (args.nodeData.hasChildren) {
      const childQuery = new Query()
        .select(['id', 'text', 'parentID', 'hasChildren'])
        .where('parentID', 'equal', args.nodeData.id);
      
      // Fetch children and add to tree
      data.executeQuery(childQuery).then((result) => {
        args.nodeData.child = result.result;
      });
    }
  };

  return (
    <TreeViewComponent
      fields={{
        dataSource: data,
        id: 'id',
        parentID: 'parentID',
        text: 'text',
        query: query,
        hasChildren: 'hasChildren'
      }}
      loadOnDemand={true}
      onNodeExpanding={handleNodeExpanding}
    />
  );
}

export default App;
```

### Load-on-Demand with Caching

```tsx
function App() {
  const [cache, setCache] = React.useState({});
  const data = new DataManager({
    url: 'url',
    adaptor: new WebApiAdaptor()
  });

  const handleNodeExpanding = async (args) => {
    const nodeId = args.nodeData.id;

    // Check cache first
    if (cache[nodeId]) {
      args.nodeData.child = cache[nodeId];
      return;
    }

    // Fetch from server
    if (args.nodeData.hasChildren) {
      const query = new Query()
        .where('parentID', 'equal', nodeId);
      
      const result = await data.executeQuery(query);
      
      // Cache the result
      setCache({
        ...cache,
        [nodeId]: result.result
      });

      args.nodeData.child = result.result;
    }
  };

  return (
    <TreeViewComponent
      // ... props
      onNodeExpanding={handleNodeExpanding}
      loadOnDemand={true}
    />
  );
}
```

## Data Binding Events

### created Event

Fires when TreeView initializes:

```tsx
<TreeViewComponent
  onCreated={() => {
    console.log('TreeView created');
  }}
/>
```

### dataBound Event

Fires after data binding completes:

```tsx
<TreeViewComponent
  onDataBound={() => {
    console.log('Data binding complete');
    // Expand all nodes
    treeObj.expandAll();
  }}
/>
```

### Using Events for Data Operations

```tsx
function App() {
  const treeRef = React.useRef(null);

  const handleDataBound = () => {
    console.log('Tree rendered with data');
    
    // Perform operations after data loads
    if (treeRef.current) {
      treeRef.current.expandAll();
    }
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource, id: 'id', text: 'name' }}
      onDataBound={handleDataBound}
    />
  );
}
```

## Field Mapping Reference

### Complete Fields Object

```tsx
const fields = {
  // Data source
  dataSource: array | DataManager,      // Data array or DataManager instance
  query: Query,                         // Query for DataManager
  
  // Identification
  id: 'id',                             // Unique identifier property
  text: 'name',                         // Display text property
  
  // Hierarchy
  child: 'child',                       // Children array (hierarchical)
  parentID: 'pid',                      // Parent ID reference (self-referential)
  hasChildren: 'hasChild',              // Boolean: has children?
  
  // State
  expanded: 'expanded',                 // Initial expand state
  selected: 'selected',                 // Initial selection
  isChecked: 'isChecked',              // Initial checked state
  
  // Appearance
  iconCss: 'icon',                      // Icon CSS class
  imageUrl: 'image',                    // Image URL
  tooltip: 'tooltip',                   // Tooltip text
  htmlAttributes: 'attr'                // HTML attributes object
};
```

### Field Property Mapping Examples

```tsx
// Employee data structure
const employees = [
  {
    empId: 101,
    empName: 'John Doe',
    reportsTo: null,
    designation: 'Manager',
    department: 'IT',
    profileImage: 'john.jpg',
    isManager: true
  }
];

// Field mapping
const fields = {
  dataSource: employees,
  id: 'empId',                    // Maps to empId
  parentID: 'reportsTo',          // Maps to reportsTo
  text: 'empName',                // Maps to empName
  hasChildren: 'isManager',       // Maps to isManager
  imageUrl: 'profileImage',       // Maps to profileImage
  tooltip: 'designation'          // Maps to designation
};
```

## Troubleshooting

### Data Not Displaying

```tsx
// ❌ Wrong - Field names don't match data properties
const data = [{ id: 1, name: 'Item', children: [] }];
<TreeViewComponent
  fields={{
    dataSource: data,
    id: 'id',
    text: 'name',
    child: 'child'  // Wrong - data has 'children' not 'child'
  }}
/>

// ✅ Correct
<TreeViewComponent
  fields={{
    dataSource: data,
    id: 'id',
    text: 'name',
    child: 'children'  // Correct property name
  }}
/>
```

### Load-on-Demand Not Triggering

```tsx
// ✅ Required for load-on-demand
<TreeViewComponent
  loadOnDemand={true}  // Enable lazy loading
  onNodeExpanding={handleExpand}
/>

// ✅ In self-referential data, set hasChildren on parent nodes
const data = [
  { id: 1, pid: null, name: 'Parent', hasChild: true },  // hasChild=true
  { id: 2, pid: 1, name: 'Child' }
];
```

### DataManager Query Not Working

```tsx
// ✅ Correct Query syntax
const query = new Query()
  .select(['id', 'text'])           // Select specific properties
  .where('status', 'equal', 'active') // Filter
  .take(50);                        // Limit results

// ❌ Wrong - property not selected
const query = new Query()
  .where('status', 'equal', 'active')
  // Missing .select() - might not return needed properties
```

---

**Key Takeaways:**
- ✅ Use hierarchical for pre-loaded data
- ✅ Use self-referential for database queries
- ✅ Use DataManager for remote data
- ✅ Use load-on-demand for 10000+ nodes
- ✅ Map fields correctly to data properties
- ✅ Set hasChildren on parent nodes for load-on-demand

