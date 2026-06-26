# Data Binding

Learn how to bind data to the Query Builder using local JavaScript arrays or remote RESTful JSON services through DataManager.

## Table of Contents
- [Overview](#overview)
- [Local Data Binding](#local-data-binding)
- [Remote Data Binding](#remote-data-binding)
- [DataManager Integration](#datamanager-integration)
- [Binding Rules with Data](#binding-rules-with-data)
- [Dynamic Data Updates](#dynamic-data-updates)

## Overview

The Query Builder uses the `dataSource` property to bind data. Two binding methods are available:

1. **Local Data** - JavaScript object arrays
2. **Remote Data** - RESTful services via DataManager

The `dataSource` supports:
- Plain JavaScript object arrays
- DataManager instances with various adaptors
- Dynamic updates and refreshes

## Local Data Binding

### Basic Local Data

Assign a JavaScript object array directly to the `dataSource` property:

```tsx
import { ColumnsModel, QueryBuilderComponent } from '@syncfusion/ej2-react-querybuilder';
import React from 'react';

const employeeData = [
  { EmployeeID: 1001, FirstName: 'Nancy', Title: 'Sales Manager', Country: 'USA' },
  { EmployeeID: 1002, FirstName: 'Michael', Title: 'Sales Representative', Country: 'UK' },
  { EmployeeID: 1003, FirstName: 'Robert', Title: 'Sales Manager', Country: 'USA' },
  { EmployeeID: 1004, FirstName: 'Andrew', Title: 'Software Developer', Country: 'Canada' }
];

function App() {
  const columns: ColumnsModel[] = [
    { field: 'EmployeeID', label: 'Employee ID', type: 'number' },
    { field: 'FirstName', label: 'First Name', type: 'string' },
    { field: 'Title', label: 'Title', type: 'string' },
    { field: 'Country', label: 'Country', type: 'string' }
  ];

  return (
    <QueryBuilderComponent 
      width="100%" 
      dataSource={employeeData}
      columns={columns}
    />
  );
}

export default App;
```

> **Note:** By default, DataManager uses JsonAdaptor for local data binding, so you don't need to explicitly specify it.

### Local Data with Initial Rules

Combine local data with predefined filter rules:

```tsx
import { RuleModel } from '@syncfusion/ej2-react-querybuilder';

function App() {
  const columns: ColumnsModel[] = [
    { field: 'EmployeeID', label: 'Employee ID', type: 'number' },
    { field: 'FirstName', label: 'First Name', type: 'string' },
    { field: 'Title', label: 'Title', type: 'string' },
    { field: 'Country', label: 'Country', type: 'string' }
  ];

  const initialRules: RuleModel = {
    condition: 'and',
    rules: [
      {
        field: 'Country',
        label: 'Country',
        operator: 'equal',
        type: 'string',
        value: 'USA'
      },
      {
        field: 'Title',
        label: 'Title',
        operator: 'contains',
        type: 'string',
        value: 'Manager'
      }
    ]
  };

  return (
    <QueryBuilderComponent
      width="100%"
      dataSource={employeeData}
      columns={columns}
      rule={initialRules}
    />
  );
}
```

## Remote Data Binding

### Binding Remote Data with DataManager

Assign service data as a DataManager instance to the `dataSource` property with the service endpoint URL:

```tsx
import { DataManager, ODataV4Adaptor } from '@syncfusion/ej2-data';
import { ColumnsModel, QueryBuilderComponent } from '@syncfusion/ej2-react-querybuilder';
import React from 'react';

function App() {
  const data = new DataManager({
    url: 'url',
    adaptor: new ODataV4Adaptor()
  });

  const columns: ColumnsModel[] = [
    { field: 'EmployeeID', label: 'Employee ID', type: 'number' },
    { field: 'FirstName', label: 'First Name', type: 'string' },
    { field: 'Title', label: 'Title', type: 'string' },
    { field: 'HireDate', label: 'Hire Date', type: 'date', format: 'dd/MM/yyyy' },
    { field: 'Country', label: 'Country', type: 'string' },
    { field: 'City', label: 'City', type: 'string' }
  ];

  return (
    <QueryBuilderComponent
      width="100%"
      dataSource={data}
      columns={columns}
    />
  );
}

export default App;
```

### Using JsonAdaptor for Remote JSON

If your API returns standard JSON without OData protocol:

```tsx
import { DataManager, JsonAdaptor } from '@syncfusion/ej2-data';

const data = new DataManager({
  url: 'url',
  adaptor: new JsonAdaptor()
});

<QueryBuilderComponent dataSource={data} columns={columns} />
```

### REST Adaptor for Custom APIs

For APIs that follow REST conventions:

```tsx
import { DataManager } from '@syncfusion/ej2-data';

const data = new DataManager({
  url: 'url',
  adaptor: new JsonAdaptor(),
  crossDomain: true
});
```

## DataManager Integration

### Available Adaptors

| Adaptor | Use Case |
|---------|----------|
| `ODataV4Adaptor` | OData v4 services |
| `ODataAdaptor` | OData v3 services |
| `JsonAdaptor` | Standard JSON APIs |
| `UrlAdaptor` | REST-style endpoints |
| `GraphQLAdaptor` | GraphQL endpoints |

### Creating DataManager with Options

```tsx
import { DataManager } from '@syncfusion/ej2-data';

const data = new DataManager({
  url: 'url',
  adaptor: new ODataV4Adaptor(),
  pageSize: 50,
  offline: false,
  timeStamp: false,
  crossDomain: true
});
```

**Key Options:**
- `url` - API endpoint
- `adaptor` - Protocol adaptor
- `pageSize` - Records per request
- `offline` - Cache data locally
- `crossDomain` - Enable CORS requests

## Binding Rules with Data

### Initializing with Rules

Load initial filter rules with data:

```tsx
const initialRules: RuleModel = {
  condition: 'and',
  rules: [
    {
      field: 'EmployeeID',
      label: 'Employee ID',
      operator: 'equal',
      type: 'number',
      value: 1001
    },
    {
      field: 'Title',
      label: 'Title',
      operator: 'equal',
      type: 'string',
      value: 'Sales Manager'
    }
  ]
};

<QueryBuilderComponent
  dataSource={employeeData}
  columns={columns}
  rule={initialRules}
/>
```

### Filtering Data with Rules

Use `getPredicate()` to convert rules into a predicate for DataManager filtering:

```tsx
let qryBldrObj: QueryBuilderComponent;

function applyFilter(): void {
  const predicate = qryBldrObj.getPredicate(qryBldrObj.rule);
  const filteredData = data.executeQuery(new Query().where(predicate));
  // Use filteredData for display
}

<QueryBuilderComponent
  ref={(scope) => { qryBldrObj = scope as QueryBuilderComponent; }}
/>
```

## Dynamic Data Updates

### Updating DataSource

Change the data source dynamically at runtime:

```tsx
let qryBldrObj: QueryBuilderComponent;
const dataManager = new DataManager(employeeData);

function updateData(): void {
  const newData = [
    { EmployeeID: 2001, FirstName: 'John', Title: 'Manager', Country: 'USA' },
    { EmployeeID: 2002, FirstName: 'Jane', Title: 'Developer', Country: 'UK' }
  ];
  dataManager.dataSource.json = newData;
  qryBldrObj.dataSource = dataManager;
}

<QueryBuilderComponent
  dataSource={dataManager}
  ref={(scope) => { qryBldrObj = scope as QueryBuilderComponent; }}
/>
```

### Handling Data Changes

Use the `dataBound` event when remote data loads:

```tsx
function onDataBound(args: any): void {
  console.log('Data has been bound to the Query Builder');
  // Update UI or trigger other logic
}

<QueryBuilderComponent
  dataSource={remoteData}
  dataBound={onDataBound}
/>
```

## Complete Example: Local and Remote Data

```tsx
import { DataManager, ODataV4Adaptor } from '@syncfusion/ej2-data';
import { ColumnsModel, QueryBuilderComponent, RuleModel } from '@syncfusion/ej2-react-querybuilder';
import React, { useState } from 'react';

function App() {
  const [dataSource, setDataSource] = useState(employeeData);

  const columns: ColumnsModel[] = [
    { field: 'EmployeeID', label: 'Employee ID', type: 'number' },
    { field: 'FirstName', label: 'First Name', type: 'string' },
    { field: 'Title', label: 'Title', type: 'string' },
    { field: 'Country', label: 'Country', type: 'string' }
  ];

  const initialRules: RuleModel = {
    condition: 'and',
    rules: [{
      field: 'Country',
      label: 'Country',
      operator: 'equal',
      type: 'string',
      value: 'USA'
    }]
  };

  function switchToRemote(): void {
    const remoteData = new DataManager({
      url: 'url',
      adaptor: new ODataV4Adaptor()
    });
    setDataSource(remoteData);
  }

  function switchToLocal(): void {
    setDataSource(employeeData);
  }

  return (
    <div>
      <button onClick={switchToLocal}>Use Local Data</button>
      <button onClick={switchToRemote}>Use Remote Data</button>
      <QueryBuilderComponent
        width="100%"
        dataSource={dataSource}
        columns={columns}
        rule={initialRules}
      />
    </div>
  );
}

export default App;
```

This example demonstrates:
- Switching between local and remote data sources
- Using DataManager with ODataV4Adaptor
- Preserving filter rules during data source changes
