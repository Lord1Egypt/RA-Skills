# Data Binding

## Table of Contents

- [Local Data Binding](#local-data-binding)
- [Hierarchical Data](#hierarchical-data)
- [Self-Referential Data](#self-referential-data)
- [Remote Data Binding](#remote-data-binding)
- [DataManager Adaptors](#datamanager-adaptors)
- [Load on Demand](#load-on-demand)
- [Prevent Node Selection](#prevent-node-selection)

## Local Data Binding

Dropdown Tree supports local JavaScript arrays as data source. The component requires three essential field mappings to render hierarchical data: **value** (unique identifier), **text** (display text), and **parentValue** or **child** (hierarchy relationship).

### Field Mapping

```jsx
const data = [
  { id: 1, name: 'Parent', children: [...] },
  { id: 2, name: 'Child', parentId: 1 },
];

<DropDownTreeComponent
  fields={{
    dataSource: data,
    value: 'id',        // Unique identifier
    text: 'name',       // Display text
    parentValue: 'parentId',  // For self-referential
    child: 'children'   // For hierarchical (nested)
  }}
/>
```

**Default mappings** (if not specified):
- value: 'id'
- text: 'text'
- parentValue: null

## Hierarchical Data

Hierarchical data contains nested arrays of objects representing parent-child relationships through nesting.

### Example - Product Categories

```jsx
const hierarchicalData = [
  {
    code: 'Electronics',
    name: 'Electronics',
    expanded: true,
    children: [
      {
        code: 'Laptops',
        name: 'Laptops',
        children: [
          { code: 'HP', name: 'HP Laptop' },
          { code: 'Dell', name: 'Dell Laptop' },
        ],
      },
      {
        code: 'Phones',
        name: 'Mobile Phones',
        children: [
          { code: 'iPhone', name: 'Apple iPhone' },
          { code: 'Samsung', name: 'Samsung Galaxy' },
        ],
      },
    ],
  },
  {
    code: 'Furniture',
    name: 'Furniture',
    children: [
      { code: 'Chairs', name: 'Chairs' },
      { code: 'Tables', name: 'Tables' },
    ],
  },
];

function App() {
  return (
    <DropDownTreeComponent
      fields={{
        dataSource: hierarchicalData,
        value: 'code',
        text: 'name',
        child: 'children',
      }}
      placeholder="Select a category"
    />
  );
}
```

**Key points:**
- Nesting depth is unlimited
- `expanded` property controls initial expansion state
- Map the nested array field to `child` property

## Self-Referential Data

Self-referential data uses parent-child references within a flat array structure.

### Example - Organizational Structure

```jsx
const selfReferentialData = [
  { id: 1, pid: null, name: 'CEO', hasChild: true },
  { id: 2, pid: 1, name: 'Manager', hasChild: true },
  { id: 3, pid: 1, name: 'Developer', hasChild: false },
  { id: 4, pid: 2, name: 'Team Lead', hasChild: false },
  { id: 5, pid: 2, name: 'Engineer', hasChild: false },
];

function App() {
  return (
    <DropDownTreeComponent
      fields={{
        dataSource: selfReferentialData,
        value: 'id',
        text: 'name',
        parentValue: 'pid',
        hasChildren: 'hasChild', // Optional: indicates if item has children
      }}
      placeholder="Select employee"
    />
  );
}
```

**Key points:**
- Root items have `pid: null` or undefined
- Each item references parent by `pid`
- `hasChildren` helps optimize rendering (optional)
- Flat structure easier to manage than nested

### Field Properties

| Property | Type | Purpose |
|----------|------|---------|
| `value` | String | Unique identifier |
| `text` | String | Display text in dropdown |
| `parentValue` | String | Parent reference (self-referential) |
| `child` | String | Children array (hierarchical) |
| `hasChildren` | String | Boolean flag for parent nodes |
| `selectable` | String | Boolean - disable selection for specific nodes |
| `expanded` | String | Boolean - initial expand state |

## Remote Data Binding

Bind Dropdown Tree to remote data services using DataManager for dynamic, large-scale datasets.

### Basic Remote Binding

```jsx
import { DataManager, ODataV4Adaptor } from '@syncfusion/ej2-data';

const dataManager = new DataManager({
  url: 'url',
  adaptor: new ODataV4Adaptor(),
});

function App() {
  return (
    <DropDownTreeComponent
      fields={{
        dataSource: dataManager,
        value: 'EmployeeID',
        text: 'FirstName',
        hasChildren: 'EmployeeID', // Or check for children
      }}
      placeholder="Select employee"
    />
  );
}
```

### Nested Remote - Two Level Binding

```jsx
const dataManager = new DataManager({
  url: 'url',
  adaptor: new ODataV4Adaptor(),
  crossDomain: true,
});

function App() {
  return (
    <DropDownTreeComponent
      fields={{
        dataSource: dataManager,
        value: 'EmployeeID',
        text: 'FirstName',
        child: {
          dataSource: new DataManager({
            url: 'url',
            adaptor: new ODataV4Adaptor(),
            crossDomain: true,
          }),
          value: 'OrderID',
          parentValue: 'EmployeeID',
          text: 'ShipName',
        },
      }}
      placeholder="Select employee then order"
    />
  );
}
```

## DataManager Adaptors

Choose the appropriate adaptor based on your data service:

### ODataAdaptor (Default)

For OData endpoints:

```jsx
import { DataManager, ODataAdaptor } from '@syncfusion/ej2-data';

const dataManager = new DataManager({
  url: 'url',
  adaptor: new ODataAdaptor(),
});
```

### ODataV4Adaptor

For OData V4 endpoints (modern OData):

```jsx
import { DataManager, ODataV4Adaptor } from '@syncfusion/ej2-data';

const dataManager = new DataManager({
  url: 'url',
  adaptor: new ODataV4Adaptor(),
});
```

### WebApiAdaptor

For RESTful Web APIs:

```jsx
import { DataManager, WebApiAdaptor } from '@syncfusion/ej2-data';

const dataManager = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor(),
});
```

### UrlAdaptor

For standard HTTP endpoints:

```jsx
import { DataManager, UrlAdaptor } from '@syncfusion/ej2-data';

const dataManager = new DataManager({
  url: 'url',
  adaptor: new UrlAdaptor(),
});
```

## Load on Demand

Optimize performance with large datasets by loading child items only when parent is expanded (lazy loading).

### Enable Load on Demand

```jsx
<DropDownTreeComponent
  fields={{
    dataSource: data,
    value: 'id',
    text: 'name',
    parentValue: 'parentId',
    hasChildren: 'hasChild', // Required for lazy loading
  }}
  treeSettings={{
    loadOnDemand: true, // Enable lazy loading
  }}
  placeholder="Select item (lazy loaded)"
/>
```

### With Remote Data

```jsx
const dataManager = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor(),
});

<DropDownTreeComponent
  fields={{
    dataSource: dataManager,
    value: 'id',
    text: 'name',
    hasChildren: 'hasChild',
    child: {
      dataSource: new DataManager({
        url: 'url',
        adaptor: new WebApiAdaptor(),
      }),
      value: 'id',
      parentValue: 'categoryId',
      text: 'name',
    },
  }}
  treeSettings={{
    loadOnDemand: true,
  }}
/>
```

**Benefits:**
- Reduces initial load time
- Minimizes bandwidth usage
- Improves user experience with large trees
- Scales to massive datasets

## Prevent Node Selection

Disable selection for specific tree nodes using the `selectable` field mapping.

### Example - Parent Nodes Non-Selectable

```jsx
const data = [
  { id: 1, name: 'Parent 1', parentId: null, selectable: false },
  { id: 2, name: 'Child 1.1', parentId: 1, selectable: true },
  { id: 3, name: 'Child 1.2', parentId: 1, selectable: true },
  { id: 4, name: 'Parent 2', parentId: null, selectable: false },
];

<DropDownTreeComponent
  fields={{
    dataSource: data,
    value: 'id',
    text: 'name',
    parentValue: 'parentId',
    selectable: 'selectable', // Only select items with selectable: true
  }}
  placeholder="Select child items only"
/>
```

**Use cases:**
- Prevent category selection, only allow leaf nodes
- Gray out disabled options
- Force users to select specific item types
- Enforce business rules in hierarchical structures

### Dynamic Selection Control

```jsx
const data = [
  { id: 1, name: 'Category', parentId: null, isLeaf: false },
  { id: 2, name: 'Product A', parentId: 1, isLeaf: true },
  { id: 3, name: 'Product B', parentId: 1, isLeaf: true },
];

// Map selectable based on isLeaf flag
fields={{
  selectable: 'isLeaf', // Only leaf nodes are selectable
}}
```

**Performance tip:** Mark parent nodes with `selectable: false` when you only want leaf node selection.
