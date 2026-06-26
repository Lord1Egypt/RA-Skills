# Field Mapping & Custom Data Structures

## Table of Contents
- [FieldsModel Overview](#fieldsmodel-overview)
- [Core Fields](#core-fields)
- [Node State Fields](#node-state-fields)
- [Display Enhancement Fields](#display-enhancement-fields)
- [Remote Data Fields](#remote-data-fields)
- [Complete Field Mapping Examples](#complete-field-mapping-examples)

## FieldsModel Overview

The `fields` property is a `FieldsModel` object that maps your data structure to the Dropdown Tree component. It tells the component which properties to use for different purposes.

### Basic FieldsModel Structure

```tsx
const fields = {
  // Core mapping
  dataSource: data,           // Data array or DataManager
  value: 'id',                // Unique identifier field
  text: 'name',               // Display text field
  
  // Hierarchy
  child: 'children',          // Child items field (hierarchical)
  // OR
  parentValue: 'parentId',    // Parent reference field (self-referential)
  
  // Optional enhancements
  expanded: 'isExpanded',     // Initial expand state
  hasChildren: 'hasChild',    // Indicates if node has children
  selectable: 'canSelect',    // Whether node can be selected
  selected: 'isSelected',     // Pre-selected nodes
  iconCss: 'icon',            // CSS class for icon
  imageUrl: 'image',          // Image URL for node
  htmlAttributes: 'attrs'     // HTML attributes object
};

<DropDownTreeComponent fields={fields} />
```

## Core Fields

### dataSource

Specifies the data array or DataManager instance to populate the tree.

```tsx
// Local array
const fields = {
  dataSource: [
    { id: 1, name: 'Item 1' },
    { id: 2, name: 'Item 2' }
  ],
  value: 'id',
  text: 'name'
};

// Remote DataManager
import { DataManager, ODataV4Adaptor } from '@syncfusion/ej2-data';

const fields = {
  dataSource: new DataManager({
    url: 'url',
    adaptor: new ODataV4Adaptor
  }),
  value: 'id',
  text: 'name'
};
```

### value

Field name containing the unique identifier for each node. Used for selection tracking and event data.

```tsx
const data = [
  { itemId: 1, name: 'Item 1' },
  { itemId: 2, name: 'Item 2' }
];

const fields = {
  dataSource: data,
  value: 'itemId',  // Custom identifier field
  text: 'name'
};
```

**Important:** The `value` field must be unique across all nodes.

### text

Field name containing the display text for each node in the dropdown tree.

```tsx
const data = [
  { id: 1, label: 'Electronics' },
  { id: 2, label: 'Computers' }
];

const fields = {
  dataSource: data,
  value: 'id',
  text: 'label'  // Custom text field
};
```

## Hierarchy Fields

### child (Hierarchical Data)

Field name containing child items array for nested hierarchies. Use this for data where children are nested within parents.

```tsx
const hierarchicalData = [
  {
    id: 1,
    name: 'Fruits',
    children: [
      { id: 2, name: 'Apple', children: [] },
      { id: 3, name: 'Orange', children: [] }
    ]
  },
  {
    id: 4,
    name: 'Vegetables',
    children: [
      { id: 5, name: 'Carrot', children: [] }
    ]
  }
];

const fields = {
  dataSource: hierarchicalData,
  value: 'id',
  text: 'name',
  child: 'children'  // Nested children array
};
```

### parentValue (Self-Referential Data)

Field name containing the parent's identifier. Use this for flat arrays where each child references its parent.

```tsx
const selfReferentialData = [
  { id: 1, name: 'Fruits', parentId: null },
  { id: 2, name: 'Apple', parentId: 1 },
  { id: 3, name: 'Orange', parentId: 1 },
  { id: 4, name: 'Vegetables', parentId: null },
  { id: 5, name: 'Carrot', parentId: 4 }
];

const fields = {
  dataSource: selfReferentialData,
  value: 'id',
  text: 'name',
  parentValue: 'parentId'  // Parent reference field
};
```

**Root nodes** have `parentValue` as `null` or undefined.

### hasChildren

Field name indicating whether a node has children. Useful for lazy loading or UI optimization.

```tsx
const data = [
  { id: 1, name: 'Fruits', hasChild: true },
  { id: 2, name: 'Apple', hasChild: false },
  { id: 3, name: 'Vegetables', hasChild: true }
];

const fields = {
  dataSource: data,
  value: 'id',
  text: 'name',
  parentValue: 'parentId',
  hasChildren: 'hasChild'  // Boolean field
};
```

**Benefits:**
- Shows expand arrow even without fetched children
- Required for lazy loading to work properly
- Prevents unnecessary loading attempts on leaf nodes

## Node State Fields

### expanded

Field name controlling which nodes are initially expanded in the tree.

```tsx
const data = [
  { id: 1, name: 'Fruits', expanded: true, children: [...] },
  { id: 2, name: 'Vegetables', expanded: false, children: [...] }
];

const fields = {
  dataSource: data,
  value: 'id',
  text: 'name',
  child: 'children',
  expanded: 'expanded'  // Boolean field
};
```

**Result:** "Fruits" branch opens automatically, "Vegetables" stays closed.

### selected

Field name pre-selecting nodes when the component initializes.

```tsx
const data = [
  { id: 1, name: 'Fruits', selected: true },
  { id: 2, name: 'Apple', selected: false },
  { id: 3, name: 'Orange', selected: true }
];

const fields = {
  dataSource: data,
  value: 'id',
  text: 'name',
  selected: 'selected'  // Boolean field
};
```

**Note:** Works with single selection (no checkboxes).

### selectable

Field name controlling whether a node can be selected. Set to `false` to disable selection for specific nodes.

```tsx
const data = [
  { id: 1, name: 'Category', canSelect: false }, // Can't select category
  { id: 2, name: 'Item 1', canSelect: true },
  { id: 3, name: 'Item 2', canSelect: true }
];

const fields = {
  dataSource: data,
  value: 'id',
  text: 'name',
  selectable: 'canSelect'
};
```

**Use Cases:**
- Disable selection for category headers
- Prevent selection of disabled items
- Create read-only tree branches

## Display Enhancement Fields

### iconCss

Field name containing CSS class names for icons displayed before node text.

```tsx
const data = [
  { id: 1, name: 'Documents', icon: 'e-icons e-folder' },
  { id: 2, name: 'Resume.pdf', icon: 'e-icons e-pdf' },
  { id: 3, name: 'Report.docx', icon: 'e-icons e-docx' }
];

const fields = {
  dataSource: data,
  value: 'id',
  text: 'name',
  iconCss: 'icon'
};
```

**Using Syncfusion Icons:**
```tsx
const data = [
  { id: 1, name: 'Add', icon: 'e-icons e-add' },
  { id: 2, name: 'Edit', icon: 'e-icons e-edit' },
  { id: 3, name: 'Delete', icon: 'e-icons e-delete' }
];
```

**Using Font Awesome:**
```tsx
const data = [
  { id: 1, name: 'Documents', icon: 'fa fa-folder' },
  { id: 2, name: 'File', icon: 'fa fa-file' }
];
```

### imageUrl

Field name containing image URLs displayed before or instead of text.

```tsx
const data = [
  { id: 1, name: 'User 1', image: '/images/user1.jpg' },
  { id: 2, name: 'User 2', image: '/images/user2.jpg' },
  { id: 3, name: 'User 3', image: '/images/user3.jpg' }
];

const fields = {
  dataSource: data,
  value: 'id',
  text: 'name',
  imageUrl: 'image'
};
```

**CSS to style images:**
```css
.e-ddtree .e-list-item img {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  margin-right: 8px;
}
```

### htmlAttributes

Field name containing HTML attributes object for custom attributes on tree items.

```tsx
const data = [
  { 
    id: 1, 
    name: 'Item 1',
    attrs: { title: 'Tooltip text', 'data-category': 'important' }
  },
  { 
    id: 2, 
    name: 'Item 2',
    attrs: { title: 'Another item', 'data-category': 'normal' }
  }
];

const fields = {
  dataSource: data,
  value: 'id',
  text: 'name',
  htmlAttributes: 'attrs'
};
```

**Result:** Items render with custom HTML attributes:
```html
<li title="Tooltip text" data-category="important">Item 1</li>
```

## Remote Data Fields

### query

Query configuration for remote data fetching. Used with DataManager.

```tsx
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';

const data = new DataManager({
  url: 'url',
  adaptor: new ODataV4Adaptor,
  crossDomain: true
});

const query = new Query().from('Employees').select('EmployeeID,FirstName,Title').take(10);

const fields = {
  dataSource: data,
  query: query,  // Query for remote data
  value: 'EmployeeID',
  text: 'FirstName'
};
```

### tableName

Table or resource name for server-side queries.

```tsx
const fields = {
  dataSource: new DataManager({
    url: 'url',
    adaptor: new UrlAdaptor
  }),
  tableName: 'Employees',  // Server resource name
  value: 'EmployeeID',
  text: 'FirstName'
};
```

## Nested Field Mapping for Hierarchical Data

For hierarchical data with children, specify field mapping for child level as well.

```tsx
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';

const remoteData = new DataManager({
  url: 'url',
  adaptor: new ODataV4Adaptor,
  crossDomain: true
});

const query = new Query().from('Employees').select('EmployeeID,FirstName').take(5);
const query1 = new Query().from('Orders').select('OrderID,EmployeeID,ShipName').take(5);

const fields = {
  // Parent level
  dataSource: remoteData,
  query: query,
  value: 'EmployeeID',
  text: 'FirstName',
  hasChildren: 'EmployeeID',
  
  // Child level
  child: {
    dataSource: remoteData,
    query: query1,
    value: 'OrderID',
    parentValue: 'EmployeeID',
    text: 'ShipName'
  }
};
```

## Complete Field Mapping Examples

### Example 1: Simple Hierarchical Data

```tsx
const data = [
  {
    id: 1,
    name: 'Electronics',
    children: [
      { id: 2, name: 'Laptops', children: [] },
      { id: 3, name: 'Phones', children: [] }
    ]
  }
];

const fields = {
  dataSource: data,
  value: 'id',
  text: 'name',
  child: 'children'
};
```

### Example 2: Self-Referential with All Fields

```tsx
const data = [
  { id: 1, name: 'Fruits', parentId: null, expanded: true, hasChild: true, canSelect: true },
  { id: 2, name: 'Apple', parentId: 1, expanded: false, hasChild: false, canSelect: true }
];

const fields = {
  dataSource: data,
  value: 'id',
  text: 'name',
  parentValue: 'parentId',
  expanded: 'expanded',
  hasChildren: 'hasChild',
  selectable: 'canSelect'
};
```

### Example 3: With Display Enhancements (Icons & Images)

```tsx
const data = [
  {
    id: 1,
    name: 'John Doe',
    image: '/images/john.jpg',
    parentId: null,
    hasChild: true
  },
  {
    id: 2,
    name: 'New Task',
    icon: 'e-icons e-task',
    parentId: 1,
    hasChild: false
  }
];

const fields = {
  dataSource: data,
  value: 'id',
  text: 'name',
  parentValue: 'parentId',
  hasChildren: 'hasChild',
  imageUrl: 'image',
  iconCss: 'icon'
};
```

### Example 4: Remote Data with Query

```tsx
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';

const remoteData = new DataManager({
  url: 'url',
  adaptor: new ODataV4Adaptor
});

const fields = {
  dataSource: remoteData,
  query: new Query().from('Categories').select('CategoryID,CategoryName'),
  value: 'CategoryID',
  text: 'CategoryName',
  hasChildren: 'CategoryID'
};
```

## Field Mapping Best Practices

1. **Always specify `value` field**: Must be unique across all nodes
2. **Use meaningful field names**: Match your data structure
3. **Specify `hasChildren` for lazy loading**: Required for load-on-demand
4. **Use `child` for small datasets**: Nested structure
5. **Use `parentValue` for large datasets**: Flat structure, better performance
6. **Test field mappings with sample data**: Verify all properties are accessible
7. **Consider readonly branches**: Use `selectable: false` for categories

## Troubleshooting

**Issue:** Tree shows no items
- **Solution:** Verify `dataSource`, `value`, and `text` fields are correctly mapped

**Issue:** Child items not appearing
- **Solution:** Ensure `child` or `parentValue` field is correctly specified and data structure matches

**Issue:** Icons not displaying
- **Solution:** Verify CSS classes exist, check `iconCss` field mapping

**Issue:** Lazy loading not working
- **Solution:** Ensure `hasChildren` field is present and set to `true` for parent nodes

**Issue:** Pre-selected items not showing as selected
- **Solution:** Verify `selected` field is present and set correctly
