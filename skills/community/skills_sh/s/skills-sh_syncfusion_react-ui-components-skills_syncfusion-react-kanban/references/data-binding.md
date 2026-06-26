# Data Binding: Connecting to Data Sources

## Table of Contents
- [Overview](#overview)
- [Static Array Binding](#static-array-binding)
- [DataManager with Remote APIs](#datamanager-with-remote-apis)
- [OData Services](#odata-services)
- [REST APIs](#rest-apis)
- [Real-Time Updates](#real-time-updates)
- [Troubleshooting](#troubleshooting)

## Overview

Kanban supports two data binding approaches:

1. **Local/Static**: JavaScript array of objects
2. **Remote**: DataManager with OData, REST, or custom adaptors

Choose based on your data source and update frequency.

## Static Array Binding

### Simple Array Binding

```ts
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

**Best for:**
- Static data that doesn't change
- Initial prototypes
- Small datasets

### Dynamic Updates with useState

```tsx
import * as React from 'react';
import { useState } from 'react';
import { KanbanComponent } from '@syncfusion/ej2-react-kanban';

// Data shape: { Id, Status, Summary }
const [data, setData] = useState(initialData);

const handleAddCard = (): void => {
  const newCard: { [key: string]: Object } = {
    Id: Math.max(...data.map(d => d.Id)) + 1,
    Status: 'Open',
    Summary: 'New Task'
  };
  setData([...data, newCard]);
};

<KanbanComponent dataSource={data}>
  {/* ... */}
</KanbanComponent>
```

**Best for:**
- Local form submissions
- Client-side only changes
- Small datasets

## DataManager with Remote APIs

### Basic DataManager Setup

```ts
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { DataManager, ODataAdaptor } from '@syncfusion/ej2-data';
import { KanbanComponent, ColumnsDirective, ColumnDirective, DialogEventArgs } from "@syncfusion/ej2-react-kanban";

function App() {
  let data = new DataManager({
    url: 'https://services.syncfusion.com/react/production/api/Kanban',
    adaptor: new ODataAdaptor
  });
  
  function DialogOpen(args: DialogEventArgs): void {
    args.cancel = true;
  }
  
  return (
    <KanbanComponent 
      id="kanban" 
      keyField="Status" 
      dataSource={data} 
      cardSettings={{ contentField: "Summary", headerField: "Id" }} 
      allowDragAndDrop={false} 
      dialogOpen={DialogOpen}
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

**Key properties:**
- `url`: API endpoint
- `adaptor`: Protocol handler (ODataAdaptor, UrlAdaptor, JsonAdaptor)
- Automatically handles fetch, CRUD, and sync

## OData Services

OData is a standardized protocol for data access. Use `ODataAdaptor`:

```tsx
import { DataManager, ODataAdaptor } from '@syncfusion/ej2-data';
import { KanbanComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-kanban';
import { DialogEventArgs } from '@syncfusion/ej2-react-kanban';

const data: DataManager = new DataManager({
  url: 'https://services.syncfusion.com/react/production/api/Kanban',
  adaptor: new ODataAdaptor(),
  crossDomain: true  // Required for cross-origin requests
});

const handleDialogOpen = (args: DialogEventArgs): void => {
  args.cancel = true;
};

<KanbanComponent 
  id="kanban" 
  keyField="Status" 
  dataSource={data} 
  cardSettings={{ contentField: "Summary", headerField: "Id" }} 
  allowDragAndDrop={false} 
  dialogOpen={handleDialogOpen}
>
  <ColumnsDirective>
    <ColumnDirective headerText="To Do" keyField="Open" />
    <ColumnDirective headerText="In Progress" keyField="InProgress" />
    <ColumnDirective headerText="Testing" keyField="Testing" />
    <ColumnDirective headerText="Done" keyField="Close" />
  </ColumnsDirective>
</KanbanComponent>
```

**OData query examples built-in:**
- Filter: `?$filter=Status eq 'Open'`
- Sorting: `?$orderby=Priority descend`
- Paging: `?$skip=0&$top=50`
- Selection: `?$select=Id,Summary,Status`

DataManager automatically appends these based on component actions.

## REST APIs

For custom REST endpoints, use `UrlAdaptor`:

```tsx
import { DataManager, UrlAdaptor } from '@syncfusion/ej2-data';
import { KanbanComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-kanban';

const data: DataManager = new DataManager({
  url: 'Home/DataSource',
  updateUrl: 'Home/Update',
  insertUrl: 'Home/Insert',
  removeUrl: 'Home/Delete',
  adaptor: new UrlAdaptor(),
  crossDomain: true
});

<KanbanComponent 
  id="kanban" 
  keyField="Status" 
  dataSource={data} 
  cardSettings={{ contentField: "Summary", headerField: "Id" }}
>
  <ColumnsDirective>
    <ColumnDirective headerText="To Do" keyField="Open" />
    <ColumnDirective headerText="In Progress" keyField="InProgress" />
    <ColumnDirective headerText="Testing" keyField="Testing" />
    <ColumnDirective headerText="Done" keyField="Close" />
  </ColumnsDirective>
</KanbanComponent>
```

### Expected API Endpoints

**GET** `/tasks`
```json
[
  { "Id": 1, "Status": "Open", "Summary": "Task A" },
  { "Id": 2, "Status": "InProgress", "Summary": "Task B" }
]
```

**POST** `/tasks/add`
```json
Request: { "Id": 3, "Status": "Open", "Summary": "New Task" }
Response: { "Id": 3, "Status": "Open", "Summary": "New Task" }
```

**PUT** `/tasks/update`
```json
Request: { "Id": 1, "Status": "InProgress", "Summary": "Task A" }
Response: { "Id": 1, "Status": "InProgress", "Summary": "Task A" }
```

**DELETE** `/tasks/delete?id=1`
```json
Response: { "success": true }
```

## Real-Time Updates

### Refresh Data After External Changes

```tsx
import { useRef } from 'react';
import { KanbanComponent } from '@syncfusion/ej2-react-kanban';
import { DataManager } from '@syncfusion/ej2-data';

const kanbanRef = useRef<KanbanComponent>(null);

const handleRefresh = (): void => {
  if (kanbanRef.current?.dataSource instanceof DataManager) {
    const dataManager = kanbanRef.current.dataSource as DataManager;
    dataManager.executeQuery();
  }
};
```

<KanbanComponent ref={kanbanRef} dataSource={dataManager}>
  {/* ... */}
</KanbanComponent>

<button onClick={handleRefresh}>Refresh Board</button>
```

### WebSocket-Based Updates

For real-time collaboration:

```tsx
import { useEffect, useRef, useState } from 'react';
import { KanbanComponent } from '@syncfusion/ej2-react-kanban';

// WebSocket update shape: { action: 'cardUpdated'|'cardAdded'|'cardDeleted', card?, cardId? }
export default function RealtimeKanban(): JSX.Element {
  const [data, setData] = useState([]);
  const kanbanRef = useRef<KanbanComponent>(null);

  useEffect(() => {
    // Initial data fetch
    fetch('/api/tasks').then(r => r.json()).then(setData);

    // WebSocket for real-time updates
    const ws = new WebSocket('wss://api.example.com/kanban-live');
    
    ws.onmessage = (event: MessageEvent): void => {
      const update: WebSocketUpdate = JSON.parse(event.data);
      
      if (update.action === 'cardUpdated' && update.card) {
        setData(data.map(card => 
          card.Id === update.card!.Id ? update.card! : card
        ));
      } else if (update.action === 'cardAdded' && update.card) {
        setData([...data, update.card]);
      } else if (update.action === 'cardDeleted' && update.cardId) {
        setData(data.filter(card => card.Id !== update.cardId));
      }
    };

    return () => ws.close();
  }, []);

  return (
    <KanbanComponent dataSource={data} ref={kanbanRef}>
      {/* ... */}
    </KanbanComponent>
  );
}
```

### Poll Server for Changes

```tsx
import { useEffect } from 'react';

// Data shape: { Id, Status, Summary }
useEffect(() => {
  const interval = setInterval((): void => {
    fetch('/api/tasks')
      .then(r => r.json())
      .then((tasks) => setData(tasks))
      .catch(err => console.error('Failed to fetch tasks:', err));
  }, 5000);  // Refresh every 5 seconds

  return () => clearInterval(interval);
}, []);
```

## Troubleshooting

### No data showing
- Verify API endpoint returns valid JSON array
- Check network tab for API errors
- Confirm `keyField` matches field in API response

### CORS errors
- Add `crossDomain: true` to DataManager
- Ensure server allows cross-origin requests
- Check API has `Access-Control-Allow-Origin` headers

### Drag-drop not saving
- Verify `insertUrl`, `updateUrl`, `removeUrl` are configured
- Check API returns updated record with same Id
- Monitor network tab for CRUD request failures

### Data not refreshing
- Use `dataManager.executeQuery()` to manual refresh
- Set polling interval if server doesn't support real-time
- Check DataManager `requestType` for DELETE/UPDATE operations

### Performance issues with large datasets
- Implement server-side pagination with `pageSize`
- Use virtual scrolling (covered in customization-and-styling.md)
- Filter data on server before sending to client
