# Data Adaptors in React Grid

## Table of Contents
- [Overview](#overview)
- [URL Adaptor](#url-adaptor)
- [ODataV4 Adaptor](#odatav4-adaptor)
- [WebAPI Adaptor](#webapi-adaptor)
- [GraphQL Adaptor](#graphql-adaptor)
- [Custom Adaptor](#custom-adaptor)
- [RemoteSave Adaptor](#remotesave-adaptor)
- [Adaptor Comparison](#adaptor-comparison)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

## Overview

Data adaptors provide an interface between the Grid component and various backend services. They handle data fetching, filtering, sorting, grouping, and CRUD operations on the server side.

Adaptors are configured through the `DataManager` component using the `adaptor` property.

## URL Adaptor

Simplest adaptor for REST APIs with standard HTTP GET/POST requests.

### Setup

```tsx
import { DataManager, UrlAdaptor } from '@syncfusion/ej2-data';
import { GridComponent } from '@syncfusion/ej2-react-grids';

const data = new DataManager({
  url: 'url,
  adaptor: new UrlAdaptor()
});

<GridComponent dataSource={data}>
  {/* columns */}
</GridComponent>
```

### Server Response Format

```json
{
  "d": [
    { "OrderID": 10248, "CustomerID": "VINET", "Freight": 32.38 },
    { "OrderID": 10249, "CustomerID": "TOMSP", "Freight": 11.61 }
  ],
  "__count": 830
}
```

Or with array response:
```json
[
  { "OrderID": 10248, "CustomerID": "VINET", "Freight": 32.38 },
  { "OrderID": 10249, "CustomerID": "TOMSP", "Freight": 11.61 }
]
```

### Example Implementation

```tsx
import { DataManager, UrlAdaptor } from '@syncfusion/ej2-data';
import { GridComponent, ColumnsDirective, ColumnDirective, Inject, Page, Sort, Filter } from '@syncfusion/ej2-react-grids';

function App() {
  const data = new DataManager({
    url: 'url',
    adaptor: new UrlAdaptor()
  });

  return (
    <GridComponent dataSource={data} allowPaging={true} allowSorting={true} allowFiltering={true}>
      <ColumnsDirective>
        <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
        <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
        <ColumnDirective field='Freight' headerText='Freight' width='100' format='C2' />
      </ColumnsDirective>
      <Inject services={[Page, Sort, Filter]} />
    </GridComponent>
  );
}

export default App;
```

---

## ODataV4 Adaptor

Specialized for OData v4 protocol. Provides advanced filtering, sorting, and server-side operations.

### Setup

```tsx
import { DataManager, ODataV4Adaptor } from '@syncfusion/ej2-data';

const data = new DataManager({
  url: 'url',
  adaptor: new ODataV4Adaptor()
});

<GridComponent dataSource={data}>
  {/* columns */}
</GridComponent>
```

### Benefits

- **Advanced Filtering**: Complex filter expressions
- **Selective Loading**: Only required columns via $select
- **Server-Side Aggregates**: Count, sum, average on server
- **Relationship Navigation**: Access related entities via $expand

### Query Parameters

```
$select     - Select specific columns
$filter     - Complex filter expressions  
$orderby    - Sort by one or more fields
$skip       - Skip N records (pagination)
$top        - Return N records
$count      - Include total count
$expand     - Include related data
```

### Example Queries

```
// Basic with paging
/Orders?$skip=0&$top=12&$count=true

// With filtering
/Orders?$filter=Freight gt 50 and ShipCity eq 'London'

// With sorting
/Orders?$orderby=OrderDate desc,CustomerID asc

// Selective columns
/Orders?$select=OrderID,CustomerID,Freight

// With relationships
/Orders?$expand=Customer,Employee

// Complex filter
/Orders?$filter=contains(tolower(CustomerID),'a') and Freight lt 100
```

### Complex OData Filters

```tsx
import { Predicate } from '@syncfusion/ej2-data';

const predicate = new Predicate('Freight', 'greaterThan', 50);
predicate = predicate.and('ShipCity', 'equal', 'London');
predicate = predicate.or('CustomerID', 'startsWith', 'A');

const gridInstance = gridRef.current;
gridInstance.query = new Query().where(predicate);
gridInstance.refresh();
```

### Example with Expand

```tsx
const data = new DataManager({
  url: 'url',
  adaptor: new ODataV4Adaptor()
});

<GridComponent dataSource={data}>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
    <ColumnDirective field='Customer.CompanyName' headerText='Company' width='150' />
    <ColumnDirective field='Employee.FirstName' headerText='Employee' width='120' />
    <ColumnDirective field='Freight' headerText='Freight' width='100' format='C2' />
  </ColumnsDirective>
  <Inject services={[Page, Sort, Filter]} />
</GridComponent>
```

---

## WebAPI Adaptor

For ASP.NET Web API services using RESTful conventions.

### Setup

```tsx
import { DataManager, WebApiAdaptor } from '@syncfusion/ej2-data';

const data = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor(),
  crossDomain: true
});

<GridComponent dataSource={data}>
  {/* columns */}
</GridComponent>
```

### ASP.NET Web API Controller

```csharp
[ApiController]
[Route("api/[controller]")]
public class OrdersController : ControllerBase
{
    [HttpGet]
    public IActionResult GetOrders([FromQuery] DataManagerRequest dm)
    {
        var orders = GetAllOrders(); // Your data source
        
        if (dm.Search != null && dm.Search.Count > 0)
        {
            orders = orders.Where(o => o.CustomerID.Contains(dm.Search[0].Key)).ToList();
        }

        if (dm.Sorted != null && dm.Sorted.Count > 0)
        {
            foreach (var sort in dm.Sorted)
            {
                if (sort.Direction == "Ascending")
                    orders = orders.OrderBy(x => x.GetType().GetProperty(sort.Name)?.GetValue(x)).ToList();
                else
                    orders = orders.OrderByDescending(x => x.GetType().GetProperty(sort.Name)?.GetValue(x)).ToList();
            }
        }

        var count = orders.Count();
        
        if (dm.Skip > 0)
            orders = orders.Skip(dm.Skip).ToList();
        
        if (dm.Take > 0)
            orders = orders.Take(dm.Take).ToList();

        return Ok(new { result = orders, count = count });
    }

    [HttpPost]
    public IActionResult Create([FromBody] Order value)
    {
        // Insert logic
        return Ok(value);
    }

    [HttpPut("{id}")]
    public IActionResult Update(int id, [FromBody] Order value)
    {
        // Update logic
        return Ok(value);
    }

    [HttpDelete("{id}")]
    public IActionResult Delete(int id)
    {
        // Delete logic
        return Ok(id);
    }
}
```

### React Grid With CRUD

```tsx
import { DataManager, WebApiAdaptor } from '@syncfusion/ej2-data';
import { GridComponent, Inject, Edit, Toolbar } from '@syncfusion/ej2-react-grids';

const data = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor(),
  insertUrl: 'url',
  updateUrl: 'url',
  removeUrl: 'url',
  batchUrl: 'url/batch'
});

<GridComponent
  dataSource={data}
  editSettings={{ allowEditing: true, allowAdding: true, allowDeleting: true, mode: 'Dialog' }}
  toolbar={['Add', 'Edit', 'Delete', 'Update', 'Cancel']}
>
  {/* columns */}
  <Inject services={[Edit, Toolbar]} />
</GridComponent>
```

---

## GraphQL Adaptor

For GraphQL endpoints returning complex nested queries.

### Setup

```tsx
import { DataManager, GraphQLAdaptor } from '@syncfusion/ej2-data';

const data = new DataManager({
  url: 'url',
  adaptor: new GraphQLAdaptor(),
  query: `query {
    orders(skip: 0, take: 12) {
      items {
        orderId
        customerId
        freight
      }
      totalCount
    }
  }`
});

<GridComponent dataSource={data}>
  {/* columns */}
</GridComponent>
```

### GraphQL Query with Variables

```tsx
const data = new DataManager({
  url: 'url',
  adaptor: new GraphQLAdaptor(),
  query: `query getOrders($skip: Int!, $take: Int!, $filter: String) {
    orders(skip: $skip, take: $take, filter: $filter) {
      items {
        orderId
        customerId
        orderDate
        freight
      }
      totalCount
    }
  }`
});
```

### GraphQL API Example (Node.js)

```javascript
const express = require('express');
const { graphql, buildSchema } = require('graphql');

const schema = buildSchema(`
  type Query {
    orders(skip: Int, take: Int, filter: String): OrderResult
  }
  
  type Order {
    orderId: Int
    customerId: String
    orderDate: String
    freight: Float
  }
  
  type OrderResult {
    items: [Order]
    totalCount: Int
  }
`);

const root = {
  orders: ({ skip = 0, take = 12, filter }) => {
    let orders = getAllOrders(); // Your data
    
    if (filter) {
      orders = orders.filter(o => o.customerId.includes(filter));
    }
    
    return {
      items: orders.slice(skip, skip + take),
      totalCount: orders.length
    };
  }
};

app.post('/graphql', express.json(), async (req, res) => {
  const result = await graphql(schema, req.body.query, root);
  res.json(result);
});
```

---

## Custom Adaptor

For non-standard backend implementations.

### Creating a Custom Adaptor

```tsx
import { DataManager, Adaptor, Query } from '@syncfusion/ej2-data';

class CustomAdaptor extends Adaptor {
  processQuery(dm, query, hierarchyIndex) {
    // Custom query processing
    const req = this.baseUrl;
    const filter = query.params.filter || '';
    const sort = query.params.sort || '';
    const page = query.params.pageIndex || 1;
    const pageSize = query.params.pageSize || 12;

    return {
      type: 'GET',
      url: `${req}?filter=${filter}&sort=${sort}&page=${page}&pageSize=${pageSize}`
    };
  }

  processResponse(data, dm, query, xhr, request, key) {
    // Process response to expected format
    if (data.result) {
      return { result: data.result, count: data.totalCount };
    }
    return data;
  }

  insert(dm, value, tableName, key) {
    // Custom insert logic
    return {
      type: 'POST',
      url: dm.insertUrl || dm.baseUrl,
      data: JSON.stringify(value),
      contentType: 'application/json'
    };
  }

  update(dm, keyField, value, tableName, key) {
    // Custom update logic
    return {
      type: 'PUT',
      url: `${dm.updateUrl || dm.baseUrl}/${value[keyField]}`,
      data: JSON.stringify(value),
      contentType: 'application/json'
    };
  }

  remove(dm, keyField, value, tableName, key) {
    // Custom delete logic
    return {
      type: 'DELETE',
      url: `${dm.removeUrl || dm.baseUrl}/${value[keyField]}`
    };
  }
}

// Usage
const data = new DataManager({
  url: 'url,
  adaptor: new CustomAdaptor()
});
```

### Custom Adaptor with Special Headers

```tsx
class AuthenticatedAdaptor extends Adaptor {
  processRequest(dm, request, state) {
    request.headers = {
      ...request.headers,
      'Authorization': `send_token`,
      'X-Custom-Header': 'CustomValue'
    };
    return request;
  }

  processResponse(data, dm, query, xhr, request, key) {
    if (xhr.status === 401) {
      // Handle unauthorized
      redirectToLogin();
    }
    return data;
  }
}
```

---

## RemoteSave Adaptor

Specialized for batch CRUD operations (multiple insert/update/delete in single request).

### Setup

```tsx
import { DataManager, RemoteSaveAdaptor } from '@syncfusion/ej2-data';
import { GridComponent, Inject, Edit, Toolbar } from '@syncfusion/ej2-react-grids';

const data = new DataManager({
  url: 'url',
  adaptor: new RemoteSaveAdaptor(),
  batchUrl: 'url/batch'
});

<GridComponent
  dataSource={data}
  editSettings={{ allowEditing: true, allowAdding: true, allowDeleting: true, mode: 'Batch' }}
  toolbar={['Add', 'Edit', 'Delete', 'Update', 'Cancel']}
>
  {/* columns */}
  <Inject services={[Edit, Toolbar]} />
</GridComponent>
```

### Batch Request Format

```json
{
  "changed": [
    { "OrderID": 10248, "CustomerID": "VINET_UPDATED" }
  ],
  "added": [
    { "CustomerID": "NEWCUST", "Freight": 25.5 }
  ],
  "deleted": [
    { "OrderID": 10249 }
  ]
}
```

### ASP.NET Backend

```csharp
[HttpPost("batch")]
public IActionResult UpdateBatch([FromBody] BatchRequest request)
{
    if (request.Changed != null)
        foreach (var order in request.Changed)
            UpdateOrder(order);
    
    if (request.Added != null)
        foreach (var order in request.Added)
            InsertOrder(order);
    
    if (request.Deleted != null)
        foreach (var order in request.Deleted)
            DeleteOrder(order.OrderID);

    return Ok();
}

public class BatchRequest
{
    public List<Order> Changed { get; set; }
    public List<Order> Added { get; set; }
    public List<Order> Deleted { get; set; }
}
```

---

## Adaptor Comparison

| Feature | URL | OData | WebAPI | GraphQL | Custom |
|---------|-----|-------|--------|---------|--------|
| **Easy Setup** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⚠️ Complex |
| **Filtering** | ⭐⭐⭐ | ⭐⭐⭐ | Good | Complex | Custom |
| **Sorting** | ⭐⭐⭐ | ⭐⭐⭐ | Good | Custom | Custom |
| **Pagination** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | Custom | Custom |
| **Aggregates** | ⭐⭐⭐ | ⭐⭐⭐ | ⚠️ | Custom | Custom |
| **Relationships** | ❌ | ⭐⭐⭐ | Basic | ⭐⭐⭐ | Custom |
| **CRUD** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | Custom | Custom |
| **Performance** | Good | Good | Good | Variable | Variable |

---

## Error Handling

### Global Error Handler

```tsx
const data = new DataManager({
  url: 'url,
  adaptor: new UrlAdaptor()
});

<GridComponent
  dataSource={data}
  actionFailure={(error) => handleError(error)}
>
  {/* columns */}
</GridComponent>

const handleError = (error) => {
  console.error('Grid Error:', error);
  
  if (error.error?.status === 401) {
    // Handle unauthorized
    redirectToLogin();
  } else if (error.error?.status === 500) {
    // Handle server error
    showErrorNotification('Server error occurred');
  } else {
    showErrorNotification('An error occurred');
  }
};
```

### Request/Response Interceptor

```tsx
class InterceptorAdaptor extends Adaptor {
  beforeSend(request) {
    console.log('Request:', request);
    // Add auth headers, etc.
    return request;
  }

  processResponse(data, dm, query, xhr, request, key) {
    console.log('Response:', data);
    
    if (data.error) {
      throw new Error(data.error.message);
    }
    
    return data;
  }
}
```

### Retry Logic for Failed Requests

```tsx
const createDataManagerWithRetry = (url) => {
  const data = new DataManager({
    url: url,
    adaptor: new UrlAdaptor()
  });

  let retryCount = 0;
  const maxRetries = 3;

  data.onActionFailure = (error) => {
    if (retryCount < maxRetries) {
      retryCount++;
      console.log(`Retry attempt ${retryCount}...`);
      setTimeout(() => data.executeQuery(), 1000 * retryCount);
    } else {
      console.error('Max retries exceeded');
    }
  };

  return data;
};
```

---

## Best Practices

1. **Choose the right adaptor** for your backend type
2. **Implement server-side filtering** for large datasets
3. **Use pagination** to limit data transfer
4. **Handle errors gracefully** with user-friendly messages
5. **Add loading indicators** during data fetching
6. **Optimize queries** - only fetch needed columns
7. **Implement authentication** for secure APIs
8. **Cache data** when appropriate
9. **Test error scenarios** thoroughly
10. **Monitor performance** with network inspector
