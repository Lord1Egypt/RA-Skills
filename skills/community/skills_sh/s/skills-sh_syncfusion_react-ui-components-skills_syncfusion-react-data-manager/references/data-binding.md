# Data Binding in React DataManager

Connect your React components to data sources using DataManager. It supports both local JavaScript arrays and remote REST/OData services.

## Local Data Binding

Bind DataManager directly to a JavaScript array for client-side operations:

### Using the json Property

```tsx
import React, { useEffect, useState } from 'react';
import { DataManager, Query } from '@syncfusion/ej2-data';

export default function LocalDataBinding() {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    // Local data array
    const dataArray = [
      { OrderID: 10248, CustomerID: 'VINET', Freight: 32.38, OrderDate: new Date(1996, 6, 4) },
      { OrderID: 10249, CustomerID: 'TOMSP', Freight: 11.61, OrderDate: new Date(1996, 6, 5) },
      { OrderID: 10250, CustomerID: 'HANAR', Freight: 65.83, OrderDate: new Date(1996, 6, 8) },
      { OrderID: 10251, CustomerID: 'VICTE', Freight: 41.34, OrderDate: new Date(1996, 6, 9) },
    ];

    // Initialize DataManager with local data
    const dataManager = new DataManager(dataArray);

    // Execute local query
    dataManager.executeLocal(new Query().take(10)).then((e) => {
      setOrders(e.result);
    });
  }, []);

  return (
    <table>
      <thead>
        <tr>
          <th>Order ID</th>
          <th>Customer</th>
          <th>Freight</th>
        </tr>
      </thead>
      <tbody>
        {orders.map((order) => (
          <tr key={order.OrderID}>
            <td>{order.OrderID}</td>
            <td>{order.CustomerID}</td>
            <td>${order.Freight.toFixed(2)}</td>
          </tr>
        ))}
      </tbody>
    </table>;
  );
}
```

### Passing Data During Constructor

```tsx
const local_data = [
  { ID: 1, Name: 'Alice', Status: 'Active' },
  { ID: 2, Name: 'Bob', Status: 'Inactive' },
];

const dataManager = new DataManager(local_data);
```

**When to use local binding:**
- Small datasets (< 1000 records)
- No server-side filtering needed
- Offline scenarios
- Quick prototyping

## Remote Data Binding

Connect to remote REST APIs, OData services, or any HTTP endpoint:

### Using the url Property with WebApiAdaptor

```tsx
import React, { useEffect, useState } from 'react';
import { DataManager, Query, WebApiAdaptor } from '@syncfusion/ej2-data';

export default function RemoteDataBinding() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Create DataManager with remote endpoint
    const dataManager = new DataManager({
      url: 'url',
      adaptor: new WebApiAdaptor(),
      crossDomain: true
    });

    // Execute remote query
    dataManager.executeQuery(new Query().take(10)).then((e) => {
      setOrders(e.result);
      setLoading(false);
    }).catch((error) => {
      console.error('Error fetching data:', error);
      setLoading(false);
    });
  }, []);

  if (loading) return <p>Loading...</p>;

  return (
    <table>
      <thead>
        <tr>
          <th>Order ID</th>
          <th>Customer</th>
          <th>Freight</th>
        </tr>
      </thead>
      <tbody>
        {orders.map((order) => (
          <tr key={order.OrderID}>
            <td>{order.OrderID}</td>
            <td>{order.CustomerID}</td>
            <td>${order.Freight}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

**When to use remote binding:**
- Large datasets (server-side paging)
- Real-time data from API
- Shared data across users
- Server-side filtering/sorting needed

## executeLocal() vs executeQuery()

| Method | Use Case | Data Source | Execution |
|--------|----------|------------|-----------|
| **executeLocal()** | Client-side operations | Local arrays (json property) | In-memory, instant |
| **executeQuery()** | Server operations | Remote endpoints (url property) | HTTP request, async |

### executeLocal() Example

```tsx
// Use for local arrays - synchronous operations on client side
const dataManager = new DataManager([
  { id: 1, name: 'Product A', price: 100 },
  { id: 2, name: 'Product B', price: 200 },
]);

dataManager.executeLocal(
  new Query()
    .where('price', 'greaterthan', 150)
    .sortBy('name')
).then((e) => {
  console.log(e.result); // Returns [{id: 2, name: 'Product B', price: 200}]
});
```

### executeQuery() Example

```tsx
// Use for remote data - asynchronous HTTP request
const dataManager = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor()
});

dataManager.executeQuery(
  new Query().take(10).skip(0)
).then((e) => {
  console.log(e.result); // Returns server response
}).catch((error) => {
  console.error('API Error:', error);
});
```

## Switching Between Data Sources

Change data source dynamically without recreating components:

```tsx
import React, { useState } from 'react';
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';

export default function SwitchingDataSources() {
  const [dataSource, setDataSource] = useState('local');
  const [data, setData] = useState([]);

  const loadLocalData = () => {
    const localArray = [
      { id: 1, name: 'Item 1' },
      { id: 2, name: 'Item 2' },
    ];
    const dm = new DataManager(localArray);
    dm.executeLocal(new Query().take(10)).then((e) => setData(e.result));
  };

  const loadRemoteData = () => {
    const dm = new DataManager({
      url: 'url',
      adaptor: new ODataV4Adaptor(),
      crossDomain: true
    });
    dm.executeQuery(new Query().take(10)).then((e) => setData(e.result));
  };

  const handleSwitch = (source) => {
    setDataSource(source);
    if (source === 'local') loadLocalData();
    if (source === 'remote') loadRemoteData();
  };

  return (
    <div>
      <button onClick={() => handleSwitch('local')}>Load Local Data</button>
      <button onClick={() => handleSwitch('remote')}>Load Remote Data</button>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
```

## Response Format & Expectations

DataManager expects different response formats based on adaptor type:

### JSON Response Format (JsonAdaptor / UrlAdaptor)

```json
{
  "result": [
    { "id": 1, "name": "Item 1" },
    { "id": 2, "name": "Item 2" }
  ],
  "count": 100
}
```

### OData Response Format

```json
{
  "d": {
    "results": [
      { "ID": 1, "Name": "Item 1" },
      { "ID": 2, "Name": "Item 2" }
    ],
    "__count": "100"
  }
}
```

### OData v4 Response Format

```json
{
  "value": [
    { "id": 1, "name": "Item 1" },
    { "id": 2, "name": "Item 2" }
  ],
  "@odata.count": 100
}
```

## Error Handling During Binding

Handle errors gracefully during data binding using Promise `.catch()` or `try/catch`:

```tsx
const dataManager = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor()
});

// Approach 1: Using Promise .catch()
dataManager.executeQuery(new Query().take(10))
  .then((result) => {
    console.log('Success:', result.result);
  })
  .catch((error) => {
    console.error('Fetch failed:', error);
    if (error.status === 401) {
      console.log('Unauthorized - redirect to login');
    } else if (error.status === 500) {
      console.log('Server error - try again later');
    } else if (error.status === 0) {
      console.log('Network error - check connection');
    }
  });

// Approach 2: Using async/await with try/catch
async function loadData() {
  try {
    const result = await dataManager.executeQuery(new Query().take(10));
    console.log('Success:', result.result);
  } catch (error) {
    console.error('Fetch failed:', error);
    if (error.status === 401) {
      // Redirect to login
    } else if (error.status === 500) {
      // Show server error message
    }
  }
}
```

## Performance Considerations

- **enableCache**: Set to `true` for remote data to avoid re-fetching same pages
- **take()**: Use pagination instead of loading all records at once
- **select()**: Request only required fields from server
- **Offline mode**: Cache data locally for faster access and offline support

```tsx
const dataManager = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor(),
  enableCache: true, // Cache pages
  offline: true, // Enable offline support
  crossDomain: true
});
```
