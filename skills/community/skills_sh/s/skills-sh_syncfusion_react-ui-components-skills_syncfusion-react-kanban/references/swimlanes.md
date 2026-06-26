# Swimlanes: Grouping Cards by Category

## Table of Contents
- [What Are Swimlanes](#what-are-swimlanes)
- [Basic Swimlane Setup](#basic-swimlane-setup)
- [Custom Swimlane Headers](#custom-swimlane-headers)
- [Swimlane Templates](#swimlane-templates)
- [Use Cases](#use-cases)
- [Troubleshooting](#troubleshooting)

## What Are Swimlanes

Swimlanes are horizontal grouping rows that organize cards by a category field (e.g., by user, team, priority). They provide a second dimension of organization alongside vertical columns.

**Without swimlanes:**
```
┌─────────────────────────────────────┐
│ To Do  │ In Progress │ Done         │
├─────────────────────────────────────┤
│ Card 1 │ Card 3      │ Card 5       │
│ Card 2 │ Card 4      │              │
└─────────────────────────────────────┘
```

**With swimlanes (grouped by assignee):**
```
┌──────────────────────────────────────┐
│ Sarah                                │
├────────┬─────────────┬───────────────┤
│ Card 1 │ Card 3      │               │
├────────┼─────────────┼───────────────┤
│ John                                 │
├────────┼─────────────┼───────────────┤
│ Card 2 │ Card 4      │ Card 5        │
└────────┴─────────────┴───────────────┘
```

Each swimlane groups cards horizontally, making it easy to see per-user or per-category workload.

## Basic Swimlane Setup

Enable swimlanes with `swimlaneSettings`:

```tsx
import React, { useState } from 'react';
import { KanbanComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-kanban';

export default function KanbanWithSwimlanes(): JSX.Element {
  const [data] = useState<{ [key: string]: Object }[]>([
    { 
      Id: 'Task-1', 
      Status: 'Open', 
      Summary: 'Build API', 
      Assignee: 'Sarah'
    },
    { 
      Id: 'Task-2', 
      Status: 'Open', 
      Summary: 'Design UI', 
      Assignee: 'John'
    },
    { 
      Id: 'Task-3', 
      Status: 'InProgress', 
      Summary: 'Write tests', 
      Assignee: 'Sarah'
    },
    { 
      Id: 'Task-4', 
      Status: 'InProgress', 
      Summary: 'Code review', 
      Assignee: 'John'
    },
    { 
      Id: 'Task-5', 
      Status: 'Closed', 
      Summary: 'Deploy', 
      Assignee: 'Sarah'
    }
  ]);

  return (
    <KanbanComponent
      id="kanban"
      keyField="Status"
      dataSource={data}
      cardSettings={{
        headerField: 'Id',
        contentField: 'Summary'
      }}
      swimlaneSettings={{
        keyField: 'Assignee'  // Group cards by the Assignee field
      }}
    >
      <ColumnsDirective>
        <ColumnDirective keyField="Open" headerText="To Do" />
        <ColumnDirective keyField="InProgress" headerText="In Progress" />
        <ColumnDirective keyField="Closed" headerText="Done" />
      </ColumnsDirective>
    </KanbanComponent>
  );
}
```

**Result:**
- Swimlane row for "Sarah" with her tasks grouped by column
- Swimlane row for "John" with his tasks grouped by column
- Cards remain draggable within and between columns in their swimlane row

## Custom Swimlane Headers

By default, swimlane headers show the raw key value. Use `textField` to display a custom name:

```jsx
const data = [
  { 
    Id: 'Task-1', 
    Status: 'Open', 
    Summary: 'Build API',
    AssigneeId: 'emp-001',
    AssigneeName: 'Sarah Johnson'  // Custom display name
  },
  { 
    Id: 'Task-2', 
    Status: 'Open', 
    Summary: 'Design UI',
    AssigneeId: 'emp-002',
    AssigneeName: 'John Smith'
  }
];

<KanbanComponent
  swimlaneSettings={{
    keyField: 'AssigneeId',      // Group by AssigneeId
    textField: 'AssigneeName'    // Display AssigneeName in header
  }}
>
  {/* ... */}
</KanbanComponent>
```

**Result:**
- Swimlane headers show "Sarah Johnson" and "John Smith" instead of raw IDs
- Cards still grouped by AssigneeId value

## Swimlane Templates

Customize swimlane headers with HTML:

```jsx
export default function KanbanWithCustomSwimlane() {
  const swimlaneTemplate = (props) => {
    return (
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <img 
          src={`/avatars/${props.AssigneeId}.jpg`} 
          alt={props.AssigneeName}
          style={{ width: '40px', height: '40px', borderRadius: '50%' }}
        />
        <div>
          <div style={{ fontWeight: 'bold' }}>{props.AssigneeName}</div>
          <div style={{ fontSize: '12px', color: '#666' }}>
            Status: {props.Status}
          </div>
        </div>
      </div>
    );
  };

  return (
    <KanbanComponent
      swimlaneSettings={{
        keyField: 'Assignee',
        template: swimlaneTemplate
      }}
    >
      {/* ... */}
    </KanbanComponent>
  );
}
```

**Customization options in template:**
- Add avatar images
- Show user role or title
- Display swimlane-level statistics
- Add icons or badges
- Color-code by team

## Use Cases

### Group by Assignee (Team Workload View)
```jsx
swimlaneSettings={{ keyField: 'Assignee' }}
```
Each team member has their own swimlane row. Managers can quickly see per-person workload and balance.

### Group by Priority (Issue Severity View)
```jsx
swimlaneSettings={{ keyField: 'Priority' }}
```
Swimlanes for Critical, High, Medium, Low. Focus high-priority work visually.

**Data structure:**
```js
{ Id: '1', Status: 'Open', Summary: 'Bug fix', Priority: 'Critical' },
{ Id: '2', Status: 'Open', Summary: 'Feature', Priority: 'Medium' }
```

### Group by Project (Multi-Project Board)
```jsx
swimlaneSettings={{ keyField: 'ProjectId', textField: 'ProjectName' }}
```
See all projects side-by-side. Each project gets its own swimlane.

**Data structure:**
```js
{ 
  Id: '1', 
  Status: 'Open', 
  Summary: 'API design',
  ProjectId: 'proj-a',
  ProjectName: 'Backend Services'
}
```

### Group by Type (Mixed Workflow View)
```jsx
swimlaneSettings={{ keyField: 'Type' }}
```
Swimlanes for Story, Bug, Task, Documentation. Helps balance different work types.

## Troubleshooting

### Swimlanes not showing
- **Ensure data has the swim lane field**: Every card object must include the field specified in `keyField`
- **Check field mapping**: Example: if `keyField: 'Assignee'`, all cards need an `Assignee` property

### Wrong swimlane grouping
- Verify all values in the swimlane field are consistent (case-sensitive)
- Example: `'John'` and `'john'` create separate swimlanes
- Use uppercase or lowercase consistently in your data

### Custom text not showing
- Check that `textField` points to a different property than `keyField`
- Example: `keyField: 'UserId'`, `textField: 'UserName'` (not both pointing to same field)
- Verify the textField exists in all data records

### Performance with many swimlanes
- If you have 100+ swimlanes, consider filtering data or using a smaller subset
- Use swimlane collapse feature (set `isExpanded: false` on columns) to hide less-active swimlanes
- Consider pagination if swimlane count is very high
