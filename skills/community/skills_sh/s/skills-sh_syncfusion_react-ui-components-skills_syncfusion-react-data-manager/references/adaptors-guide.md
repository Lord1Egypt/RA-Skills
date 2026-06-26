# Adaptors Guide for React DataManager

## Table of Contents
- [Adaptor Overview](#adaptor-overview)
- [Decision Tree: Which Adaptor to Use](#decision-tree-which-adaptor-to-use)
- [Adaptor Comparison](#adaptor-comparison)
- [JsonAdaptor](#jsonadaptor)
- [ODataAdaptor](#odataadaptor)
- [ODataV4Adaptor](#odatav4adaptor)
- [UrlAdaptor](#urladaptor)
- [WebApiAdaptor](#webapiadaptor)
- [RemoteSaveAdaptor](#remotesaveadaptor)
- [WebMethodAdaptor](#webmethodadaptor)
- [GraphQLAdaptor](#graphqladaptor)
- [CustomDataAdaptor](#customdataadaptor)
- [CustomAdaptor](#customadaptor)
- [CORS & crossDomain Configuration](#cors--crossdomain-configuration)

---

## Adaptor Overview

An **adaptor** is an interface that enables DataManager to communicate with different types of data sources. Each adaptor handles:
- Request formatting
- Response parsing
- Paging/filtering/sorting communication
- Error handling
- Platform-specific conventions

Choose the adaptor that matches your backend service.

---

## Decision Tree: Which Adaptor to Use

```
Is your data source?

├─ JavaScript array (in-memory)
│  └─ Use: JsonAdaptor

├─ REST API
│  ├─ Need full control over request/response?
│  │  └─ FIRST CHOICE: CustomDataAdaptor ⭐ (MOST FLEXIBLE)
│  │      └─ Use ANY fetching tool (fetch, axios, Socket.IO, etc.)
│  │      └─ Return standard: { result, count }
│  │
│  ├─ ASP.NET Web API?
│  │  └─ Use: WebApiAdaptor
│  ├─ Generic REST (GET/POST standard)?
│  │  └─ Use: UrlAdaptor
│  ├─ Need client + server queries?
│  │  └─ Use: RemoteSaveAdaptor
│  └─ Still need more control after choosing above?
│     └─ SECONDARY CHOICE: CustomAdaptor (Extend built-in)

├─ OData Service?
│  ├─ OData v3?
│  │  └─ Use: ODataAdaptor
│  ├─ OData v4?
│  │  └─ Use: ODataV4Adaptor

├─ GraphQL Endpoint?
│  └─ Use: GraphQLAdaptor

├─ Legacy ASMX Web Service?
│  └─ Use: WebMethodAdaptor

└─ None of above?
   └─ Use CustomDataAdaptor (covers 95% custom scenarios)
```

---

## Adaptor Comparison

| Feature | Json | OData v3 | OData v4 | Url | WebApi | RemoteSave | WebMethod | GraphQL | CustomData | Custom |
|---------|------|----------|----------|-----|--------|-----------|-----------|---------|------------|--------|
| **Local data** | ✓ | - | - | - | - | - | - | - | - | - |
| **Remote API** | - | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Query support** | ✓ Client | ✓ Server | ✓ Server | ✓ Server | ✓ Server | ✓ Both* | Limited | ✓ Server | ✓ Custom | ✓ Custom |
| **CRUD** | ✓ Local | ✓ Server | ✓ Server | ✓ Server | ✓ Server | ✓ Server | ✓ Server | ✓ Server | ✓ Server | ✓ Server |
| **Batch CRUD** | - | Limited | ✓ | Limited | ✓ | ✓ | - | - | ✓ | ✓ |
| **Paging** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Limited | ✓ | ✓ | ✓ |
| **Sorting** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Limited | ✓ | ✓ | ✓ |

*RemoteSaveAdaptor: Client-side queries (filter/sort/page) + Server-side CRUD

---

## JsonAdaptor

**Use case:** Local JavaScript arrays, no server needed

```tsx
import React, { useEffect, useState } from 'react';
import { DataManager, JsonAdaptor, Query } from '@syncfusion/ej2-data';

export default function JsonAdaptorExample() {
  const [results, setResults] = useState([]);

  useEffect(() => {
    // Local data
    const dataArray = [
      { OrderID: 10248, CustomerID: 'VINET', Freight: 32.38 },
      { OrderID: 10249, CustomerID: 'TOMSP', Freight: 11.61 },
      { OrderID: 10250, CustomerID: 'HANAR', Freight: 65.83 },
    ];

    // No URL needed - data is in memory
    const dataManager = new DataManager(dataArray);

    // Client-side query execution
    dataManager.executeLocal(
      new Query()
        .where('Freight', 'greaterthan', 30)
        .sortBy('CustomerID')
        .take(10)
    ).then((e) => {
      setResults(e.result);
    });
  }, []);

  return <pre>{JSON.stringify(results, null, 2)}</pre>;
}
```

**When to use:**
- Small datasets (< 10,000 records)
- All data available in browser
- Quick prototyping
- Offline-first applications

---

## ODataAdaptor

**Use case:** OData v3 services (older ASP.NET services, SharePoint)

```tsx
import { DataManager, ODataAdaptor, Query } from '@syncfusion/ej2-data';

const dataManager = new DataManager({
  url: 'url',
  adaptor: new ODataAdaptor(),
  crossDomain: true
});

dataManager.executeQuery(
  new Query()
    .from('Orders')
    .where('Freight', 'lessthan', 100)
    .take(10)
).then((e) => {
  console.log(e.result); // OData v3 response
});
```

**Response format:**
```json
{
  "d": {
    "results": [
      { "OrderID": 10248, "CustomerID": "VINET", "Freight": 32.38 }
    ],
    "__count": "100"
  }
}
```

---

## ODataV4Adaptor

**Use case:** OData v4 services (newer Microsoft services, modern backends)

```tsx
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';

const dataManager = new DataManager({
  url: 'url',
  adaptor: new ODataV4Adaptor(),
  crossDomain: true
});

// Query syntax same, but response format is OData v4
dataManager.executeQuery(
  new Query()
    .from('Orders')
    .where('Freight', 'greaterthan', 50)
    .select(['OrderID', 'CustomerID', 'Freight'])
    .take(20)
).then((e) => {
  console.log(e.result);
});

// Expand related data
const expandQuery = new Query()
  .from('Orders')
  .expand('Customer')
  .take(10);
```

**Response format:**
```json
{
  "value": [
    { "OrderID": 10248, "CustomerID": "VINET", "Freight": 32.38 }
  ],
  "@odata.count": 100
}
```

**Key differences from v3:**
- `value` array instead of `d.results`
- `@odata.count` instead of `__count`
- Better support for `expand()`
- Richer query syntax

---

## UrlAdaptor

**Use case:** Generic REST APIs without standard conventions. **Important:** UrlAdaptor sends **only POST requests** with query parameters in the request body - never GET.

```tsx
import { DataManager, UrlAdaptor, Query } from '@syncfusion/ej2-data';

const dataManager = new DataManager({
  url: 'url',
  adaptor: new UrlAdaptor(),
  crossDomain: true
});

dataManager.executeQuery(
  new Query()
    .where('status', 'equal', 'shipped')
    .take(10)
    .skip(0)
).then((e) => {
  console.log(e.result);
});
```

**Expected server response:**
```json
{
  "result": [
    { "id": 1, "name": "Order 1" },
    { "id": 2, "name": "Order 2" }
  ],
  "count": 100
}
```

**Query parameters sent (POST only):**
```
POST url
Body: { skip: 0, take: 10, where: [...{field: Status, operator: equal, value: 'active'}], $sorted: [{field: Name, direction: Ascending"}] }
```

---

## WebApiAdaptor

**Use case:** ASP.NET Web API projects (standard REST conventions)

```tsx
import { DataManager, WebApiAdaptor, Query } from '@syncfusion/ej2-data';

const dataManager = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor(),
  crossDomain: true
});

// CRUD operations specify keyField as parameter
dataManager.update('Orders', recordData, { key: 10248 });

// Works with ASP.NET OData conventions
dataManager.executeQuery(
  new Query()
    .where('Freight', 'greaterthan', 50)
    .take(10)
).then((e) => {
  console.log(e.result);
});

// CRUD operations send proper HTTP methods
await dataManager.insert(newOrder, 'Orders'); // POST
await dataManager.update('OrderID', updatedOrder, 'Orders'); // PUT
await dataManager.remove('OrderID', 10248, 'Orders'); // DELETE
```

**Expected server response:**
```json
{
  "Items": [
    { "id": 1, "name": "Order 1" },
    { "id": 2, "name": "Order 2" }
  ],
  "Count": 100
}
```

**HTTP methods:**
- GET: Queries
- POST: Insert
- PUT: Update
- DELETE: Delete

---

## RemoteSaveAdaptor

**Use case:** Hybrid approach - client-side filtering/sorting but server-side CRUD

```tsx
import { DataManager, RemoteSaveAdaptor, Query } from '@syncfusion/ej2-data';

const dataManager = new DataManager({
  url: 'url',
  adaptor: new RemoteSaveAdaptor(),
  crossDomain: true,
  insertUrl: 'url/insert', // Executed Automaticaly
  updateUrl: 'url/update', // Executed Automaticaly
  removeUrl: 'url/delete', // Executed Automaticaly
});

// Executed LOCALLY (filtering, sorting happens in browser)
dataManager.executeLocal(
  new Query()
    .where('Freight', 'greaterthan', 50)
    .sortByDesc('OrderDate')
    .take(10)
).then((e) => {
  console.log(e.result);
});

// CRUD sent to SERVER (specify keyField as parameter)
await dataManager.insert(newOrder, 'Orders'); // Server handles insert
await dataManager.update('OrderID', order, 'Orders'); // Server handles update

// Initial data fetch
const query = new Query().take(1000); // Load all/most data
```

**When to use:**
- Need client-side filtering for performance
- Server handles updates only
- Cache all data locally
- Avoid repeated server requests

---

## WebMethodAdaptor

**Use case:** Legacy ASP.NET ASMX Web Services

```tsx
import { DataManager, WebMethodAdaptor, Query } from '@syncfusion/ej2-data';

const dataManager = new DataManager({
  url: 'url',
  adaptor: new WebMethodAdaptor(),
  crossDomain: true
});

dataManager.executeQuery(
  new Query()
    .where('Status', 'equal', 'Pending')
    .take(20)
).then((e) => {
  console.log(e.result);
});
```

**Note:** Limited support for advanced queries. Use for legacy systems only.

---

## GraphQLAdaptor

**Use case:** GraphQL endpoints

```tsx
import { DataManager, GraphQLAdaptor, Query } from '@syncfusion/ej2-data';

const dataManager = new DataManager({
  url: 'url',
  adaptor: new GraphQLAdaptor(),
  crossDomain: true
});

// Convert Query to GraphQL format
dataManager.executeQuery(
  new Query()
    .select(['id', 'name', 'email'])
    .where('status', 'equal', 'active')
    .take(10)
).then((e) => {
  console.log(e.result);
});
```

**GraphQL query generated:**
```graphql
query {
  orders(
    where: { status: "active" }
    first: 10
  ) {
    id
    name
    email
  }
}
```

---

## CustomDataAdaptor

**Use case:** Custom request/response formats with full control over data transformation

```tsx
import { DataManager, CustomDataAdaptor, Query } from '@syncfusion/ej2-data';

class MyCustomAdaptor extends CustomDataAdaptor {
  getData(args, query) {
    if (args.action === 'read') {
      // Custom fetch pattern
      const params = {
        pageNum: Math.ceil(args.skip / args.take) + 1,
        pageSize: args.take,
        search: query?.params?.search || ''
      };

      return fetch('url/data', {
        method: 'POST'
      })
        .then(response => response.json())
        .then(data => new Promise((resolve) => {
          // Transform backend format to DataManager format
          resolve({
            result: data.items,
            count: data.total
          });
        }));
    }
  }
}

const dataManager = new DataManager({
  adaptor: new MyCustomAdaptor()
});

dataManager.executeQuery(new Query().take(10)).then((e) => {
  console.log('Custom data:', e.result);
});
```

**When to use CustomDataAdaptor:**
- API returns non-standard format
- Need complete control over request/response
- Complex data transformation required
- Backend uses proprietary JSON structure

---

## CustomAdaptor

**Use case:** Proprietary or complex APIs requiring custom logic

```tsx
import { DataManager, Adaptor } from '@syncfusion/ej2-data';

class CustomAdaptorExample extends Adaptor {
  constructor() {
    super();
    this.baseUrl = 'url';
  }

  // Handle query processing
  processQuery = (dataManager: DataManager, query: Query, hierarchyPreference: any) => {
    // Custom logic: transform Query to API format
    const params = {
      filter: query.queries.filter(q => q.fn === 'where'),
      sort: query.queries.filter(q => q.fn === 'sortBy'),
      page: query.pageIndex,
      pageSize: query.pageSize
    };

    return {
      type: 'GET',
      url: `${this.baseUrl}/orders`,
      data: params
    };
  };

  // Override beforeSend to add headers
  beforeSend(dm: DataManager, request: XMLHttpRequest | Request, settings?: any): void {
    super.beforeSend(dm, request, settings);
    
    if (request instanceof XMLHttpRequest) {
      request.setRequestHeader('Authorization', `send_token`);
      request.setRequestHeader('X-API-Key', 'apikey');
    }
  }

  // Override processResponse to transform data
  processResponse(response: any, dm?: DataManager, query?: Query, xhr?: XMLHttpRequest, request?: Request, params?: any): any {
    const result = super.processResponse(response, dm, query, xhr, request, params);
    
    // Transform result
    if (result && result.result) {
      result.result = result.result.map((item: any) => ({
        ...item,
        processed: true
      }));
    }
    
    return result;
  }

  // Handle insert
  insert = (dataManager: DataManager, data, tableName) => {
    return {
      type: 'POST',
      url: `${this.baseUrl}/${tableName}`,
      data: JSON.stringify(data),
      contentType: 'application/json'
    };
  };

  // Handle update
  update = (dataManager: DataManager, keyField, value, tableName) => {
    return {
      type: 'PATCH',
      url: `${this.baseUrl}/${tableName}/${value[keyField]}`,
      data: JSON.stringify(value),
      contentType: 'application/json'
    };
  };

  // Handle delete
  remove = (dataManager: DataManager, keyField, value, tableName) => {
    return {
      type: 'DELETE',
      url: `${this.baseUrl}/${tableName}/${value}`
    };
  };
}

// Use in DataManager
const dataManager = new DataManager({
  adaptor: new CustomAdaptorExample(),
  crossDomain: true
});
```

**When to create CustomAdaptor:**
- APIs with non-standard conventions
- Complex request/response mapping
- Authentication requirements
- Special error handling

---

## CORS & crossDomain Configuration

Most remote adaptors need CORS handling:

```tsx
const dataManager = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor(),
  crossDomain: true  // Enable CORS requests
});
```

**CORS errors occur when:**
- Frontend and backend on different domains
- Backend doesn't allow cross-origin requests

**Solutions:**
1. **Enable on backend:** Add CORS headers
2. **Set crossDomain: true** in DataManager
3. **Use JSONP:** For older browsers (limited support)
4. **Proxy through same domain:** API gateway

---

## Platform-Specific Configuration

### ASP.NET Web API
```tsx
new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor()
  // Pass keyField in CRUD operations: 
  // dm.update('OrderID', data, 'Orders')
})
```

### Node.js Express
```tsx
new DataManager({
  url: 'url',
  adaptor: new UrlAdaptor(),
  crossDomain: true
})
```

### OData Service (any platform)
```tsx
new DataManager({
  url: 'url',
  adaptor: new ODataV4Adaptor(),
  crossDomain: true
})
```

### GraphQL (Apollo, Hasura, etc.)
```tsx
new DataManager({
  url: 'url',
  adaptor: new GraphQLAdaptor(),
  crossDomain: true
})
```
