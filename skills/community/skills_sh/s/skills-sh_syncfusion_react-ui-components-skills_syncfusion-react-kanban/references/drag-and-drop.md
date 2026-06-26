# Drag-and-Drop: Moving Cards and Managing Flow

## Table of Contents
- [Overview](#overview)
- [Internal Drag-and-Drop](#internal-drag-and-drop)
- [External Drag-and-Drop](#external-drag-and-drop)
- [Column-Level Control](#column-level-control)
- [Handling Drag Events](#handling-drag-events)
- [Transition Columns](#transition-columns)
- [Common Patterns](#common-patterns)

## Overview

Kanban's drag-and-drop allows users to move cards between columns, within columns, across swimlanes, or even to external sources. By default, drag-and-drop is **enabled**. Control it with:

- **Global**: `allowDragAndDrop` property on `KanbanComponent`
- **Per-column**: `allowDrag` and `allowDrop` on each `ColumnDirective`
- **Transition logic**: `transitionColumns` to restrict card flow

## Internal Drag-and-Drop

### Column-to-Column Movement
Cards can be dragged from one column to another:

```tsx
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { extend } from '@syncfusion/ej2-base';
import { KanbanComponent, ColumnsDirective, ColumnDirective } from "@syncfusion/ej2-react-kanban";
import { kanbanData } from './datasource';

function App() {
  let data = extend([], kanbanData, null, true);
  
  return (
    <KanbanComponent 
      id="kanban" 
      keyField="Status" 
      dataSource={data} 
      cardSettings={{ contentField: "Summary", headerField: "Id" }} 
      allowDragAndDrop={true}
    >
      <ColumnsDirective>
        <ColumnDirective headerText="To Do" keyField="Open" />
        <ColumnDirective headerText="In Progress" keyField="InProgress" />
        <ColumnDirective headerText="Testing" keyField="Testing" />
        <ColumnDirective headerText="Done" keyField="Close" />
      </ColumnsDirective>
    </KanbanComponent>
  );
}

export default App;

ReactDOM.render(<App />, document.getElementById('kanban'));
```

**Effect:** User drags "Task A" from "To Do" to "In Progress", card's Status field updates to "InProgress".

### Disable Drag-and-Drop
You can disable drag-and-drop functionality globally:

```tsx
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { extend } from '@syncfusion/ej2-base';
import { KanbanComponent, ColumnsDirective, ColumnDirective } from "@syncfusion/ej2-react-kanban";
import { kanbanData } from './datasource';

function App() {
  let data = extend([], kanbanData, null, true);
  
  return (
    <KanbanComponent 
      id="kanban" 
      keyField="Status" 
      dataSource={data} 
      cardSettings={{ contentField: "Summary", headerField: "Id" }} 
      allowDragAndDrop={false}
    >
      <ColumnsDirective>
        <ColumnDirective headerText="To Do" keyField="Open" />
        <ColumnDirective headerText="In Progress" keyField="InProgress" />
        <ColumnDirective headerText="Testing" keyField="Testing" />
        <ColumnDirective headerText="Done" keyField="Close" />
      </ColumnsDirective>
    </KanbanComponent>
  );
}

export default App;

ReactDOM.render(<App />, document.getElementById('kanban'));
```

**Effect:** Users cannot drag cards at all when `allowDragAndDrop={false}`.

### Swimlane Drag and Drop
By default, Swimlane allows drag and drop across the columns within the swimlane row. You cannot drag cards across the swimlane rows by default.

```tsx
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { extend } from '@syncfusion/ej2-base';
import { KanbanComponent, ColumnsDirective, ColumnDirective } from "@syncfusion/ej2-react-kanban";
import { kanbanData } from './datasource';

function App() {
  let data = extend([], kanbanData, null, true);
  
  return (
    <KanbanComponent 
      id="kanban" 
      keyField="Status" 
      dataSource={data} 
      cardSettings={{ contentField: "Summary", headerField: "Id" }} 
      swimlaneSettings={{ keyField: "Assignee" }}
    >
      <ColumnsDirective>
        <ColumnDirective headerText="To Do" keyField="Open" />
        <ColumnDirective headerText="In Progress" keyField="InProgress" />
        <ColumnDirective headerText="Testing" keyField="Testing" />
        <ColumnDirective headerText="Done" keyField="Close" />
      </ColumnsDirective>
    </KanbanComponent>
  );
}

export default App;

ReactDOM.render(<App />, document.getElementById('kanban'));
```

**Effect:** Cards stay within their assigned swimlane row when moved between columns.

## External Drag-and-Drop

### Kanban-to-Kanban
Drag cards between two Kanban boards:

```tsx
import { useState } from 'react';
import { KanbanComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-kanban';

// Data shape: { Id, Status, Summary }
export default function MultiKanban(): JSX.Element {
  const [backlogData, setBacklogData] = useState(initialBacklog);
  const [activeData, setActiveData] = useState(initialActive);

  return (
    <div style={{ display: 'flex', gap: '20px' }}>
      <div style={{ flex: 1 }}>
        <h3>Backlog</h3>
        <KanbanComponent dataSource={backlogData}>
          {/* Columns */}
        </KanbanComponent>
      </div>
      <div style={{ flex: 1 }}>
        <h3>Active Sprint</h3>
        <KanbanComponent dataSource={activeData}>
          {/* Columns */}
        </KanbanComponent>
      </div>
    </div>
  );
}
```

Cards can be dragged from Backlog to Active Sprint, moving the item's data source.

### Kanban to External List
Drag cards to external HTML elements:

```tsx
import * as React from 'react';
import { useRef, useState } from 'react';
import { KanbanComponent } from '@syncfusion/ej2-react-kanban';
import { DragEventArgs } from '@syncfusion/ej2-react-kanban';

// Data shape: { Id, Summary, Status }
export default function KanbanToExternal() {
  const kanbanRef = useRef<KanbanComponent>(null);
  const [deletedCards, setDeletedCards] = useState([]);

  const handleDragStop = (args: DragEventArgs): void => {
    // Check if dropped outside Kanban
    if (!args.element.closest('.e-kanban')) {
      setDeletedCards([...deletedCards, args.data]);
      kanbanRef.current?.deleteCard(args.data);
    }
  };

  return (
    <div>
      <KanbanComponent ref={kanbanRef} dragStop={handleDragStop}>
        {/* Columns */}
      </KanbanComponent>
      <div style={{ marginTop: '20px', padding: '10px', border: '1px dashed red' }}>
        <h3>Dropped Items ({deletedCards.length})</h3>
        {deletedCards.map(card => <div key={card.Id}>{card.Summary}</div>)}
      </div>
    </div>
  );
}
```

## Column-Level Control

Control drag-drop per column with `allowDrag` and `allowDrop`:

### Read-Only Done Column
```tsx
<ColumnDirective 
  keyField="Done" 
  headerText="Done"
  allowDrag={false}  // Cannot drag FROM this column
  allowDrop={true}   // CAN drop INTO this column
/>
```

Cards can move into Done, but once there, they're locked and cannot be moved out.

### Drop-Only Recycle Bin
```tsx
<ColumnDirective 
  keyField="Deleted" 
  headerText="Archived"
  allowDrag={true}   // CAN drag FROM this column to restore
  allowDrop={true}   // CAN drop INTO this column
  allowToggle={false} // Always visible
/>
```

### No Drag-Drop Column
```tsx
<ColumnDirective 
  keyField="OnHold" 
  headerText="On Hold"
  allowDrag={false}
  allowDrop={false}
/>
```

Cards stuck in this column until status manually updated or moved via method.

## Handling Drag Events

Respond to drag operations with event handlers:

```tsx
import { KanbanComponent, DragEventArgs, CardClickEventArgs } from '@syncfusion/ej2-react-kanban';

const handleDragStart = (args: DragEventArgs): void => {
  console.log('Dragging card:', args.data.Id);
  console.log('From column:', args.data.Status);
  // Can prevent drag: args.cancel = true;
};

const handleDragStop = (args: DragEventArgs): void => {
  console.log('Card dropped');
  console.log('New status:', args.data.Status);
};

const handleCardDoubleClick = (args: CardClickEventArgs): void => {
  console.log('Editing card:', args.data.Id);
};

<KanbanComponent
  dragStart={handleDragStart}
  dragStop={handleDragStop}
  cardDoubleClick={handleCardDoubleClick}
>
  {/* Columns */}
</KanbanComponent>
```

### Prevent Drag Based on Card Properties
```tsx
import { DragEventArgs } from '@syncfusion/ej2-react-kanban';

const handleDragStart = (args: DragEventArgs): void => {
  // Prevent dragging completed items
  if (args.data.Status === 'Done') {
    args.cancel = true;
  }
};
```

### Prevent Drop Into Specific Column
```tsx
import { DragEventArgs } from '@syncfusion/ej2-react-kanban';

const handleDragStop = (args: DragEventArgs): void => {
  // Only urgent tasks can go to InProgress
  if (args.data.Status === 'InProgress' && args.data.Priority !== 'Urgent') {
    args.cancel = true;
    alert('Only Urgent tasks can move to In Progress');
  }
};
```

## Transition Columns

Restrict which columns accept cards from other columns:

```tsx
<ColumnDirective 
  keyField="Open" 
  headerText="To Do"
  transitionColumns={['InProgress']}  // Can only transition to InProgress
/>
<ColumnDirective 
  keyField="InProgress" 
  headerText="In Progress"
  transitionColumns={['Testing', 'Done']}  // Can go to Testing or Done
/>
<ColumnDirective 
  keyField="Testing" 
  headerText="Testing"
  transitionColumns={['Done', 'Open']}  // Can go to Done or back to Open
/>
```

**Effect:**
- "To Do" cards can drag to "In Progress" only
- "In Progress" cards can drag to "Testing" or "Done"
- "Testing" cards can drag to "Done" or back to "To Do" if issues found

### Multi-Level Workflow
```tsx
<ColumnDirective 
  keyField="Analysis"
  transitionColumns={['Design']}
/>
<ColumnDirective 
  keyField="Design"
  transitionColumns={['Development']}
/>
<ColumnDirective 
  keyField="Development"
  transitionColumns={['Testing']}
/>
<ColumnDirective 
  keyField="Testing"
  transitionColumns={['Deployed']}
/>
```

Enforces strict left-to-right workflow with no skipping or backtracking.

## Common Patterns

### Approval Flow
```tsx
// Items must go: Open → Review → Approved → Deployed
<ColumnDirective keyField="Open" transitionColumns={['Review']} />
<ColumnDirective keyField="Review" transitionColumns={['Approved']} />
<ColumnDirective keyField="Approved" transitionColumns={['Deployed']} />
<ColumnDirective keyField="Deployed" allowDrag={false} />
```

### Optional Steps
```tsx
// Items can skip QA if directly deployed
<ColumnDirective keyField="Dev" transitionColumns={['QA', 'Prod']} />
<ColumnDirective keyField="QA" transitionColumns={['Prod']} />
<ColumnDirective keyField="Prod" allowDrag={false} />
```

### Blocking High-Risk Moves
```tsx
import { DragEventArgs } from '@syncfusion/ej2-react-kanban';

const handleDragStop = (args: DragEventArgs): void => {
  // Prevent moving to Live without approval
  if (args.data?.Status === 'Live' && !args.data?.ApprovedBy) {
    args.cancel = true;
    alert('This item requires approval before going live');
  }
};
```

### Audit Trail
```tsx
import { DragEventArgs } from '@syncfusion/ej2-react-kanban';

// Card shape: { Id, Status }
// AuditRecord shape: { cardId, fromStatus, toStatus, timestamp, movedBy }
const handleDragStop = (args: DragEventArgs): void => {
  const moveRecord = {
    cardId: args.data?.Id || '',
    fromStatus: args.previousStatus,
    toStatus: args.data?.Status || '',
    timestamp: new Date(),
    movedBy: getCurrentUser()
  };
  
  // Log to audit table or API
  fetch('/api/audit-trail', {
    method: 'POST',
    body: JSON.stringify(moveRecord)
  });
};
```
