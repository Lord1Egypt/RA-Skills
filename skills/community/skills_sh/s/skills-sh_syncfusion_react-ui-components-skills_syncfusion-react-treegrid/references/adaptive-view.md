---
name: adaptive-view
description: 'Adaptive View in React TreeGrid - enable adaptive UI, responsive columns, horizontal row layout, mobile optimization.'
---

# Adaptive View

## Table of Contents
- [Enable Adaptive UI](#enable-adaptive-ui)

## Enable Adaptive UI

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, Edit, Toolbar, Filter } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  const data = [
    { TaskID: 1, TaskName: 'Planning', Priority: 'High', Children: [] }
  ];

  return (
    <TreeGridComponent
      dataSource={data}
      childMapping="Children"
      enableAdaptiveUI={true}
      editSettings={{ 
        mode: 'Dialog', 
        allowEditing: true, 
        allowAdding: true,
        allowDeleting: true,
      }}
      toolbar={['Add', 'Edit', 'Delete']}
      allowFiltering={true}
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
        <ColumnDirective field="Priority" headerText="Priority" width={100} />
      </ColumnsDirective>
      <Inject services={[Edit, Toolbar, Filter]} />
    </TreeGridComponent>
  );
}
```

## Key APIs

| Property | Type | Description |
|---|---|---|
| `enableAdaptiveUI` | boolean | Enable adaptive UI for small screens |

## Common Patterns

1. **Mobile-First**: Design for mobile, enhance for desktop
2. **Touch Events**: Handle touch interactions
3. **Responsive Dialogs**: Full-screen edit forms on mobile
4. **Flexible Layout**: Adjust layout per screen size

