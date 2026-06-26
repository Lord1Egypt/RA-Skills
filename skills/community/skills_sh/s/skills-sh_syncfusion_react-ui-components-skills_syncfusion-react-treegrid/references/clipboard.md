---
name: clipboard
description: 'Clipboard in React TreeGrid - copy operations, copy cells, copy rows with hierarchy, paste functionality and clipboard events.'
---

# Clipboard

## Table of Contents
- [Copy Operations](#copy-operations)
- [Copy with Hierarchy](#copy-with-hierarchy)
- [Key APIs](#key-apis)
- [Common Patterns](#common-patterns)

## Copy Operations

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  const data = [
    { TaskID: 1, TaskName: 'Planning', Priority: 'High', Children: [] }
  ];

  return (
    <TreeGridComponent
      dataSource={data}
      childMapping="Children"
      selectionSettings={{ type: 'Cell', mode: 'Multiple' }}
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
        <ColumnDirective field="Priority" headerText="Priority" width={100} />
      </ColumnsDirective>
      <Inject services={[]} />
    </TreeGridComponent>
  );
}

// Copy with Ctrl+C, Paste with Ctrl+V
```


## Copy with Hierarchy

Copy with hierarchical structure preserved:

```tsx
import { DropDownListComponent } from "@syncfusion/ej2-react-dropdowns";
import { ColumnDirective, ColumnsDirective } from '@syncfusion/ej2-react-treegrid';
import { TreeGridComponent } from '@syncfusion/ej2-react-treegrid';
import * as React from 'react';
import { sampleData } from './datasource';
function App() {
    let treegrid;
    const data = ['Parent', 'Child', 'Both', 'None'];
    const settings = { type: 'Multiple', mode: 'Row' };
    const onChange = (sel) => {
        const mode = sel.value.toString();
        if (treegrid) {
            treegrid.copyHierarchyMode = mode;
        }
    };
    return (<div>
    <DropDownListComponent popupHeight="250px" dataSource={data} value="Parent" change={onChange} width="150px"/>
        <TreeGridComponent dataSource={sampleData} treeColumnIndex={1} childMapping='subtasks' height='225' allowFiltering={true} selectionSettings={settings} ref={g => treegrid = g}>
        <ColumnsDirective>
            <ColumnDirective field='taskID' headerText='Task ID' width='75' textAlign='Right'/>
            <ColumnDirective field='taskName' headerText='Task Name' width='180'/>
            <ColumnDirective field='startDate' headerText='Start Date' width='90' format='yMd' textAlign='Right' type='date'/>
            <ColumnDirective field='duration' headerText='Duration' width='80' textAlign='Right'/>
        </ColumnsDirective>
    </TreeGridComponent>
    </div>);
}
;
export default App;
```

## Key APIs

| Property/Method | Type | Description |
|---|---|---|
| `copy` | method | Copy to clipboard |

## Common Patterns

1. **Bulk Copy**: Copy multiple rows to paste into Excel
2. **Copy with Format**: Preserve hierarchy indentation
3. **CSV Export**: Format and copy as CSV

