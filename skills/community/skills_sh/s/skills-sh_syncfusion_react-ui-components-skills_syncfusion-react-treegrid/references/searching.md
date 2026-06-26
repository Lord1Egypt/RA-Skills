---
name: searching
description: 'Searching in React TreeGrid - global search across columns, search highlight, search configuration, and programmatic search.'
---

# Searching

## Table of Contents
- [Enable Searching](#enable-searching)
- [Search Bar](#search-bar)
- [Search Configuration](#search-configuration)
- [Search Highlight](#search-highlight)
- [Programmatic Search](#programmatic-search)
- [Search Events](#search-events)
- [Key APIs](#key-apis)
- [Common Patterns](#common-patterns)

## Enable Searching

Enable searching to allow users to search across all columns:

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, Search } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  const data = [
    { TaskID: 1, TaskName: 'Planning', Priority: 'High', Children: [] }
  ];

  return (
    <TreeGridComponent
      dataSource={data}
      childMapping="Children"
      searchSettings={{ ignoreCase: true }}
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
      </ColumnsDirective>
      <Inject services={[Filter]} />
    </TreeGridComponent>
  );
}
```

## Search Bar

Add search input to find data:

### Basic Search

```tsx
const treeGridRef = React.useRef();

const onSearchClick = (e) => {
  treeGridRef.current.search(e.target.value);
};

<div>
  <input 
    type="text" 
    placeholder="Search..." 
    onChange={onSearchClick}
    style={{ marginBottom: '10px', padding: '5px', width: '200px' }}
  />
  <TreeGridComponent ref={treeGridRef} dataSource={data} childMapping="Children">
    <ColumnsDirective>
      <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
    </ColumnsDirective>
  </TreeGridComponent>
</div>
```

## Search Configuration

Configure search behavior:

### Search Specific Columns

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  searchSettings={{
    fields: ['TaskName', 'Priority'],  // Search specific columns only
    ignoreCase: true,
    key: 'Planning'  // Initial search key
  }}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskName" allowSearching={true} width={160} />
    <ColumnDirective field="Priority" allowSearching={true} width={100} />
  </ColumnsDirective>
</TreeGridComponent>
```

### Search Case Sensitivity

Control case-sensitive search:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  searchSettings={{
    ignoreCase: true,   // Case-insensitive search (default: true)
    isAccentCharacter: false  // Ignore accent characters
  }}
>
  {/* columns */}
</TreeGridComponent>
```

## Search Highlight

Highlight search results in the grid:

### Enable Search Highlight

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  searchSettings={{ 
    ignoreCase: true,
    highlightSearchResults: true
  }}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} allowSearching={true} />
  </ColumnsDirective>
</TreeGridComponent>
```

## Programmatic Search

Search via code:

```tsx
const treeGridRef = React.useRef();

const searchByText = (searchText) => {
  treeGridRef.current.search(searchText);
};

const clearSearch = () => {
  treeGridRef.current.search('');
};

<TreeGridComponent ref={treeGridRef} dataSource={data} childMapping="Children">
  {/* columns */}
</TreeGridComponent>
```

## Search Events

### Action Complete Event

Detect when search action completes:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  actionComplete={(args) => {
    if (args.requestType === 'searching') {
      console.log('Search completed');
      console.log('Search key:', args.key);
    }
  }}
>
  {/* columns */}
</TreeGridComponent>
```

---

## Key APIs

| Property/Method | Type | Description |
|---|---|---|
| `searchSettings` | object | Configure search behavior |
| `ignoreCase` | boolean | Case-insensitive search |
| `fields` | array | Columns to search in |
| `highlightSearchResults` | boolean | Highlight matching text |
| `search` | method | Search programmatically |
| `key` | string | Initial search key/text |

## Common Patterns

1. **Real-time Search**: Search as user types in input field
2. **Multi-field Search**: Search across specific columns
3. **Search with Highlighting**: Highlight matching text in cells
4. **Debounced Search**: Throttle search for performance

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, Search } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  const data = [
    { TaskID: 1, TaskName: 'Planning', Priority: 'High', Children: [] }
  ];

  const onSearchClick = (e) => {
    const treeGridRef = React.useRef();
    if (treeGridRef.current) {
      treeGridRef.current.search(e.target.value);
    }
  };

  return (
    <div>
      <input 
        type="text" 
        placeholder="Search..." 
        onChange={onSearchClick}
        style={{ marginBottom: '10px', padding: '5px' }}
      />
      <TreeGridComponent
        dataSource={data}
        childMapping="Children"
        searchSettings={{ ignoreCase: true, isAccentCharacter: false }}
      >
        <ColumnsDirective>
          <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
          <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
          <ColumnDirective field="Priority" headerText="Priority" width={100} />
        </ColumnsDirective>
        <Inject services={[Filter]} />
      </TreeGridComponent>
    </div>
  );
}
```

## Search Highlight

Highlight search results:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  searchSettings={{ 
    ignoreCase: true,
    highlightSearchResults: true
  }}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} allowSearching={true} />
  </ColumnsDirective>
  <Inject services={[Filter]} />
</TreeGridComponent>
```

## Search Configuration

Configure search behavior:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  searchSettings={{
    fields: ['TaskName', 'Priority'],  // Search specific columns
    ignoreCase: true,
    key: 'Planning'  // Initial search key
  }}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} allowSearching={true} />
    <ColumnDirective field="Priority" headerText="Priority" width={100} allowSearching={true} />
  </ColumnsDirective>
</TreeGridComponent>
```

## Key APIs

| Property/Method | Type | Description |
|---|---|---|
| `searchSettings` | object | Configure search behavior |
| `ignoreCase` | boolean | Case-insensitive search |
| `fields` | array | Columns to search |
| `search` | method | Search programmatically |

## Common Patterns

1. **Real-time Search**: Search as user types in input field
2. **Multi-field Search**: Search across specific columns
3. **Search with Highlighting**: Highlight matching text in cells

