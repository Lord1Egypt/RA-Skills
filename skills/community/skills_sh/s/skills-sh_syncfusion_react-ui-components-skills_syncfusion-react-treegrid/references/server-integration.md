---
name: server-integration
description: 'Server Integration in React TreeGrid - CRUD operations, remote data binding, server-side filtering/sorting/paging, and API integration patterns.'
---

# Server Integration

## Table of Contents
- [Basic Server Data Binding](#basic-server-data-binding)
- [Server-side CRUD Operations](#server-side-crud-operations)
- [Server-side Filtering](#server-side-filtering)
- [Server-side Sorting](#server-side-sorting)
- [Server-side Paging](#server-side-paging)
- [Custom Request/Response Handling](#custom-requestresponse-handling)
- [Error Handling](#error-handling)
- [Batch Operations](#batch-operations)

Complete guide for integrating TreeGrid with server APIs.

## Basic Server Data Binding

Connect to remote API:

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, Page } from '@syncfusion/ej2-react-treegrid';
import { DataManager, UrlAdaptor } from '@syncfusion/ej2-data';

export default function App() {
  const dataManager = new DataManager({
    url: 'url',
    adaptor: new UrlAdaptor(),
    offline: false
  });

  return (
    <TreeGridComponent
      dataSource={dataManager}
      idMapping="TaskID"
      parentIdMapping="parentID"
      treeColumnIndex={1}
      allowPaging={true}
      pageSettings={{ pageSize: 10 }}
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
      </ColumnsDirective>
      <Inject services={[Page]} />
    </TreeGridComponent>
  );
}
```

## Server-side CRUD Operations

Handle Create, Read, Update, Delete on server:

```tsx
const treeGridRef = React.useRef();

<TreeGridComponent
  ref={treeGridRef}
  dataSource={dataManager}
  idMapping="TaskID"
  parentIdMapping="parentID"
  editSettings={{
    allowEditing: true,
    allowAdding: true,
    allowDeleting: true,
    mode: 'Cell'
  }}
  actionComplete={(args) => {
    if (args.requestType === 'save') {
      // Server auto-handles the update via DataManager
      console.log('Data saved to server');
    }
    if (args.requestType === 'add') {
      console.log('New record added:', args.data);
    }
    if (args.requestType === 'delete') {
      console.log('Record deleted');
    }
  }}
>
  {/* columns */}
</TreeGridComponent>
```

## Server-side Filtering

Apply filters on server:

```tsx
<TreeGridComponent
  dataSource={dataManager}
  idMapping="TaskID"
  parentIdMapping="parentID"
  allowFiltering={true}
  filterSettings={{ type: 'FilterBar' }}
  actionComplete={(args) => {
    if (args.requestType === 'filtering') {
      // Server receives the filter condition
      console.log('Filtered on server:', args.filterSettings);
    }
  }}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} allowFiltering={true} />
    <ColumnDirective field="Priority" headerText="Priority" width={100} allowFiltering={true} />
  </ColumnsDirective>
  <Inject services={[Filter]} />
</TreeGridComponent>
```

## Server-side Sorting

Apply sorting on server:

```tsx
<TreeGridComponent
  dataSource={dataManager}
  idMapping="TaskID"
  parentIdMapping="parentID"
  allowSorting={true}
  sortChange={(args) => {
    console.log('Sorting on server:', args.columns);
  }}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} allowSorting={true} />
  </ColumnsDirective>
  <Inject services={[Sort]} />
</TreeGridComponent>
```

## Server-side Paging

Implement server paging for large datasets:

```tsx
<TreeGridComponent
  dataSource={dataManager}
  idMapping="TaskID"
  parentIdMapping="parentID"
  allowPaging={true}
  pageSettings={{ pageSize: 50, pageCount: 5 }}
  actionComplete={(args) => {
    if (args.requestType === 'paging') {
      console.log('Page changed on server - Current page:', args.data[0].currentPage);
    }
  }}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
  <Inject services={[Page]} />
</TreeGridComponent>
```

## Custom Server Request/Response

Handle complex server interaction:

```tsx
import { DataManager, UrlAdaptor } from '@syncfusion/ej2-data';

const customAdapter = new UrlAdaptor();

// Override default processing
customAdapter.beforeSend = (request) => {
  // Add custom headers
  request.headers = request.headers || {};
  request.headers['Authorization'] = `send_token`;
  request.headers['API-Key'] = 'your-api-key';
};

const dataManager = new DataManager({
  url: 'url',
  adaptor: customAdapter,
  offline: false
});

<TreeGridComponent
  dataSource={dataManager}
  idMapping="TaskID"
  parentIdMapping="parentID"
>
  {/* columns */}
</TreeGridComponent>
```

## Error Handling

Handle server errors gracefully:

```tsx
<TreeGridComponent
  dataSource={dataManager}
  idMapping="TaskID"
  parentIdMapping="parentID"
  actionFailure={(args) => {
    console.error('Server error:', args.error);
    
    if (args.error.status === 401) {
      // Unauthorized - redirect to login
      window.location.href = '/login';
    } else if (args.error.status === 403) {
      // Forbidden - show permission error
      alert('You do not have permission to perform this action');
    } else if (args.error.status >= 500) {
      // Server error
      alert('Server error. Please try again later.');
    }
  }}
>
  {/* columns */}
</TreeGridComponent>
```

## Batch Operations

Save multiple changes in one request:

```tsx
<TreeGridComponent
  dataSource={dataManager}
  idMapping="TaskID"
  parentIdMapping="parentID"
  editSettings={{
    mode: 'Batch',
    allowEditing: true,
    allowAdding: true,
    allowDeleting: true
  }}
  actionComplete={(args) => {
    if (args.requestType === 'save') {
      console.log('Batch save completed');
      console.log('Added:', args.data.added);
      console.log('Modified:', args.data.modified);
      console.log('Deleted:', args.data.deleted);
    }
  }}
>
  {/* columns */}
</TreeGridComponent>
```

## Refresh Data from Server

Reload data after changes:

```tsx
const refreshData = () => {
  treeGridRef.current.refresh();  // Reload all data
};

const refreshTreeData = () => {
  // Refresh specific node
  const parentId = 1;
  const query = new Query().where('parentID', 'equal', parentId);
  treeGridRef.current.dataSource.executeQuery(query);
};
```

## API Endpoint Examples

Expected server request/response format:

### GET - Fetch Data
```
Request: GET /api/treegrid?$skip=0&$take=10&$inlinecount=allpages

Response:
{
  "result": [
    { "TaskID": 1, "TaskName": "Planning", "parentID": null },
    { "TaskID": 2, "TaskName": "Plan timeline", "parentID": 1 }
  ],
  "count": 100
}
```

### POST - Add Record
```
Request: POST /api/treegrid
Body: { "TaskName": "New Task", "parentID": 1 }

Response:
{ "TaskID": 100, "TaskName": "New Task", "parentID": 1 }
```

### PUT - Update Record
```
Request: PUT /api/treegrid/1
Body: { "TaskID": 1, "TaskName": "Updated Task" }

Response:
{ "TaskID": 1, "TaskName": "Updated Task" }
```

### DELETE - Delete Record
```
Request: DELETE /api/treegrid/1

Response:
{ "success": true }
```

## Key APIs

| Method | Type | Description |
|---|---|---|
| `new DataManager({ url, adaptor })` | Class | Create data connection |
| `new UrlAdaptor()` | Class | Default HTTP adapter |
| `actionComplete` | Event | After server operation |
| `actionFailure` | Event | On server error |
| `beforeSend` | Method | Intercept requests |
| `refresh()` | Method | Reload data |

## Common Patterns

1. **Authentication**: Add JWT token to requests
2. **Error Recovery**: Retry failed requests
3. **Pagination**: Server-side paging for large datasets
4. **Change Tracking**: Save changes incrementally
5. **Optimization**: Load only visible rows (virtual scroll)

