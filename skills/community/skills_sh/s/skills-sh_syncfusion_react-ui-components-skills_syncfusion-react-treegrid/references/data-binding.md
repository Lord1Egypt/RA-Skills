---
name: data-binding
description: 'Data Binding in React TreeGrid - local and remote data binding, childMapping, parentID mapping, self-referential relationships, and dynamic data loading.'
---

# Data Binding

## Table of Contents
- [Data Binding Approaches](#data-binding-approaches)
- [Hierarchical Data with childMapping](#hierarchical-data-with-childmapping)
- [Flat Data with parentID](#flat-data-with-parentid)
- [Remote Data Binding](#remote-data-binding)
- [ExpandStateMapping](#expandstatemapping)
- [Dynamic Data Loading](#dynamic-data-loading)
- [Complex Data Binding](#complex-data-binding)
- [Key APIs](#key-apis)
- [Common Patterns](#common-patterns)

## Data Binding Approaches

TreeGrid supports multiple data binding approaches for hierarchical data:

```tsx
// Node represents relationship type
Local Array → childMapping (nested Children property)
Flat Array → parentID (foreign key mapping)
Remote Service → DataManager with UrlAdaptor
```

### Basic Setup

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, Page } from '@syncfusion/ej2-react-treegrid';

interface ITreeData {
  TaskID: number;
  TaskName: string;
  Duration?: number;
  Children?: ITreeData[];
}

export default function App() {
  const data: ITreeData[] = [
    {
      TaskID: 1,
      TaskName: 'Planning',
      Duration: 5,
      Children: [
        { TaskID: 2, TaskName: 'Plan timeline', Duration: 5 },
        { TaskID: 3, TaskName: 'Plan budget', Duration: 5 }
      ]
    }
  ];

  return (
    <TreeGridComponent
      dataSource={data}
      childMapping="Children"
      treeColumnIndex={1}
      height="auto"
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
      </ColumnsDirective>
    </TreeGridComponent>
  );
}
```

## Hierarchical Data with childMapping

Bind data where child records are nested in a `Children` property:

```tsx
const hierarchicalData = [
  {
    TaskID: 1,
    TaskName: 'Planning',
    StartDate: new Date(2018, 2, 3),
    Children: [
      {
        TaskID: 2,
        TaskName: 'Plan timeline',
        StartDate: new Date(2018, 2, 3),
        Children: [
          { TaskID: 21, TaskName: 'Identify project scope' }
        ]
      },
      { TaskID: 3, TaskName: 'Plan budget' }
    ]
  },
  { TaskID: 4, TaskName: 'Design' }
];

<TreeGridComponent
  dataSource={hierarchicalData}
  childMapping="Children"
  treeColumnIndex={1}
>
  {/* columns */}
</TreeGridComponent>
```

**Key Binding Properties**:
- `dataSource`: Your hierarchical data array
- `childMapping="Children"`: Property name containing child records
- `treeColumnIndex={1}`: Column index to show tree (expand/collapse arrows)

## Flat Data with parentID

Bind flat arrays by mapping a foreign key (parentID) to identify parent-child relationships:

```tsx

const flatData = [
  { TaskID: 1, TaskName: 'Planning', ParentID: null },
  { TaskID: 2, TaskName: 'Plan timeline', ParentID: 1 },
  { TaskID: 3, TaskName: 'Plan budget', ParentID: 1 },
  { TaskID: 4, TaskName: 'Design', ParentID: null },
  { TaskID: 5, TaskName: 'UI Design', ParentID: 4 }
];

<TreeGridComponent
  dataSource={flatData}
  idMapping="TaskID"
  parentIdMapping="ParentID"
  treeColumnIndex={1}
>
  {/* columns */}
</TreeGridComponent>
```

**Key Binding Properties**:
- `idMapping="TaskID"`: Unique identifier for each record
- `parentIdMapping="ParentID"`: Foreign key pointing to parent ID (null for root records)

## Remote Data Binding

Bind TreeGrid to server-side data using DataManager:

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-treegrid';
import { DataManager, UrlAdaptor } from '@syncfusion/ej2-data';

export default function App() {
  const dataManager = new DataManager({
    url: 'url',
    adaptor: new UrlAdaptor(),
    offline: false  // Set true to cache response locally
  });

  return (
    <TreeGridComponent
      dataSource={dataManager}
      idMapping="TaskID"
      parentIdMapping="parentID"
      treeColumnIndex={1}
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
      </ColumnsDirective>
    </TreeGridComponent>
  );
}
```

## ExpandStateMapping

Control which records start expanded or collapsed via data property:

```tsx
const data = [
  {
    TaskID: 1,
    TaskName: 'Planning',
    expandState: true,  // This parent starts expanded
    Children: [
      {
        TaskID: 2,
        TaskName: 'Plan timeline',
        expandState: false,  // This parent starts collapsed
        Children: [
          { TaskID: 21, TaskName: 'Identify scope' }
        ]
      }
    ]
  }
];

<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  expandStateMapping="expandState"  // Maps to expandState property
>
  {/* columns */}
</TreeGridComponent>
```

## Dynamic Data Loading

Update data source programmatically:

```tsx
const treeGridRef = React.useRef();

const updateData = (newData) => {
  treeGridRef.current.dataSource = newData;
  treeGridRef.current.refresh();
};

const addRow = (parentData, newChildRecord) => {
  if (!parentData.Children) {
    parentData.Children = [];
  }
  parentData.Children.push(newChildRecord);
  treeGridRef.current.refresh();
};

<TreeGridComponent ref={treeGridRef} dataSource={data} childMapping="Children">
  {/* columns */}
</TreeGridComponent>
```

---

## Complex Data Binding

For nested objects and complex property mapping:

```tsx
const data = [
  {
    TaskID: 1,
    info: {
      TaskName: 'Planning',
      Category: 'Development'
    },
    metadata: {
      StartDate: new Date(2018, 2, 3)
    },
    Children: [
      {
        TaskID: 2,
        info: { TaskName: 'Plan timeline' },
        metadata: { StartDate: new Date(2018, 2, 3) }
      }
    ]
  }
];

<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  treeColumnIndex={1}
>
  <ColumnsDirective>
    <ColumnDirective field="info.TaskName" headerText="Task Name" width={160} />
    <ColumnDirective field="metadata.StartDate" headerText="Start Date" type="date" width={120} />
  </ColumnsDirective>
</TreeGridComponent>
```

**Note**: Use dot notation for nested properties (e.g., `info.TaskName`)


## Key APIs

| Property/Method | Type | Description |
|---|---|---|
| `dataSource` | array \| DataManager | Data array or remote source |
| `childMapping` | string | Property containing child records |
| `idMapping` | string | Unique identifier (for parentID binding) |
| `parentIdMapping` | string | Foreign key to parent ID |
| `treeColumnIndex` | number | Column showing tree structure |
| `expandByDefault` | string | Property controlling expand/collapse state |
| `refresh` | method | Refresh grid with updated data |
| `expanding` | event | Fired before parent expands |
| `expanded` | event | Fired after parent expands |
| `collapsing` | event | Fired before parent collapses |

## Common Patterns

1. **Nested Hierarchy**: Use childMapping for naturally nested data structures
2. **Flat Normalization**: Use parentID mapping for flattened hierarchical data
3. **Dynamic Updates**: Refresh data after add/edit/delete operations
4. **Initial State**: Use expandByDefault to show expanded hierarchy on load
```tsx
const data = [
  {
    TaskID: 1,
    info: {
      TaskName: 'Planning',
      Category: 'Development'
    },
  }
];

<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  expandStateMapping="expandState"
  treeColumnIndex={1}
/>
```

**Use Case**: Restore saved expand state or pre-expand specific hierarchy levels on load.
