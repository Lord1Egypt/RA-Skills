---
name: syncfusion-react-data-manager
description: Implements Syncfusion DataManager for local/remote binding, CRUD, querying, caching, and middleware. Supports JsonAdaptor, ODataAdaptor, ODataV4Adaptor, UrlAdaptor, WebApiAdaptor, WebMethodAdaptor, RemoteSaveAdaptor, GraphQLAdaptor, CustomDataAdaptor, and CustomAdaptor. Covers Query class, filtering, sorting, paging, grouping, persistence, offline mode, caching, and error handling.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "DataManager"
---

# Syncfusion React DataManager

The DataManager is a gateway component for managing local and remote data operations in React applications. It acts as an abstraction layer that enables seamless data binding, querying, CRUD operations, caching, and middleware customization without writing complex server communication code.

Use this skill whenever a user needs to:
- Bind local or remote data sources to UI components
- Query data (filter, sort, page, group, search)
- Perform CRUD operations (insert, update, delete, batch edits)
- Work with different data sources (JSON, OData, REST APIs, GraphQL, etc.)
- Cache data for performance
- Implement offline mode
- Add custom headers or authentication
- Transform request/response data
- Handle complex data scenarios in React applications

## ⚠️ Security & Trust Boundary

- This skill generates code only, the agent does not execute data operations or fetch remote endpoints — all DataManager interactions occur solely within the user's application at runtime.
- Generated code must treat all third-party API responses as untrusted input, never bind to unvalidated or user-provided URLs, and ensure authentication is enforced on all remote endpoints.

## When to Use DataManager

**DataManager** is best for:
- **Flexible data management** → Works with any data source (local, REST, OData, GraphQL)
- **Complex queries** → Filtering, sorting, paging, grouping, searching
- **CRUD operations** → With batch support and transaction patterns
- **Middleware customization** → Pre/post request hooks
- **Offline support** → Cache and sync when connection restored
- **Adaptor switching** → Change data sources without code changes

**Direct component binding** (Grid, Scheduler, etc.) is better when:
- You only need basic data binding without complex querying
- Performance is critical for very large datasets
- You don't need middleware customization

## Key Concepts

### Data Binding
Connect DataManager to data sources using the **json** property (local arrays) or **url** property (remote APIs). Query methods: **executeLocal()** for local data, **executeQuery()** for remote data.

### Query Class
Build structured queries using the Query class: **from()**, **where()**, **select()**, **sortBy()**, **take()**, **expand()**, **group()** chained together for powerful data operations.

### Adaptors
**Adaptors** are interfaces that enable DataManager to communicate with different data sources:
- **JsonAdaptor** → Local JavaScript arrays
- **ODataAdaptor** → OData v3 services
- **ODataV4Adaptor** → OData v4 services
- **UrlAdaptor** → Generic REST endpoints
- **WebApiAdaptor** → ASP.NET Web API
- **RemoteSaveAdaptor** → Hybrid client-side queries + server-side CRUD
- **WebMethodAdaptor** → Legacy ASP.NET ASMX services
- **GraphQLAdaptor** → GraphQL endpoints
- **CustomAdaptor** → Custom implementation for proprietary services

### CRUD Operations
- **insert()** → Add records to data source
- **update()** → Modify existing records (keyField as first parameter)
- **remove()** → Delete records (keyField as first parameter)
- **saveChanges()** → Batch multiple operations into single request

### Middleware & Customization
- **applyPreRequestMiddlewares()** → Modify request before sending (auth tokens, headers)
- **applyPostRequestMiddlewares()** → Transform response before binding (formatting, filtering)
- Custom adaptors for proprietary APIs
- Error handlers for request failures

### Caching & Performance
- **enableCache** → Prevent re-requesting previously loaded pages
- **Offline mode** → Store data locally, sync when connection restored
- **Load on demand** → Lazy load data as user scrolls (virtual scrolling)
- **Deferred operations** → Promise-based async/await patterns

## Documentation & Navigation Guide

Choose the reference file based on your current task:

### Getting Started Setup
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation steps (npm)
- Project setup & imports
- Basic DataManager initialization
- First query execution
- Environment setup
- Common errors & fixes

### Data Binding Strategies
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Local data binding with json property
- Remote data binding with url property
- executeLocal() for client-side queries
- executeQuery() for server requests
- Switching between data sources
- Response format handling
- When to use each approach

### Query Operations & Filtering
📄 **Read:** [references/querying-and-filtering.md](references/querying-and-filtering.md)
- Query class fundamentals
- Filtering with where() and Predicate
- Sorting (ascending/descending)
- Pagination with take() and skip()
- Field projection with select()
- Related data loading with expand()
- Grouping data by field(s)
- Complex multi-condition queries
- Chaining query operations

### CRUD Operations & Batch Edits
📄 **Read:** [references/crud-operations.md](references/crud-operations.md)
- insert() → Add new records
- update() → Modify existing records
- remove() → Delete records
- keyField in CRUD method parameters
- saveChanges() for batch operations
- Batch insert/update/remove
- Transaction patterns
- Data validation before operations
- Response handling

### Choosing & Using Adaptors
📄 **Read:** [references/adaptors-guide.md](references/adaptors-guide.md)
- Which adaptor to use (decision tree)
- JsonAdaptor for local arrays
- OData adaptors (v3 & v4)
- REST API adaptors (Url, WebApi)
- RemoteSaveAdaptor hybrid approach
- Legacy ASMX (WebMethodAdaptor)
- GraphQL endpoint integration
- Custom adaptor implementation
- CORS & crossDomain configuration
- Platform-specific response handling

### Middleware & Request Customization
📄 **Read:** [references/middleware-customization.md](references/middleware-customization.md)
- Pre-request middleware for auth tokens
- Custom header injection
- Request transformation
- Post-request middleware for response mapping
- Error handler functions
- Data validation & filtering in middleware
- Custom adaptor implementation
- Middleware execution order & timing

### Caching & Offline Mode
📄 **Read:** [references/caching-offline-mode.md](references/caching-offline-mode.md)
- enableCache property for performance
- When cache clears (sort, filter, CRUD)
- Offline mode implementation
- Local storage persistence
- Sync strategies after reconnection
- Cache size & memory management
- Best practices & performance patterns

### Advanced Features & Patterns
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Load on demand & pagination patterns
- Virtual scrolling setup
- Lazy loading data
- Deferred operations (Promise API)
- Async/await with DataManager
- State persistence across sessions
- Memory management
- Error handling strategies
- Performance optimization tips
- Common pitfalls & solutions

## Quick Start Example

```tsx
import React, { useEffect, useState } from 'react';
import { DataManager, WebApiAdaptor, Query } from '@syncfusion/ej2-data';

export default function DataManagerDemo() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    // Create DataManager with remote data source
    const dataManager = new DataManager({
      url: 'url',
      adaptor: new WebApiAdaptor(),
      crossDomain: true
    });

    // Execute query with filtering, sorting, paging
    dataManager.executeQuery(
      new Query()
        .where('Freight', 'greaterthan', 500) // Filter
        .sortBy('OrderDate') // Sort
        .take(10) // Pagination
    ).then((e) => {
      setItems(e.result); // Bind results
    });
  }, []);

  return (
    <div>
      <h2>Orders</h2>
      <ul>
        {items.map((item) => (
          <li key={item.OrderID}>{item.CustomerID} - ${item.Freight}</li>
        ))}
      </ul>
    </div>
  );
}
```

## Common Use Cases

**Case 1: Display local data with filtering**
→ Use JsonAdaptor + Query + where() for client-side filtering

**Case 2: Fetch server data with authentication**
→ Use WebApiAdaptor + applyPreRequestMiddlewares() for token injection

**Case 3: Work offline, sync later**
→ Use enableCache + offline mode + saveChanges() for batch sync

**Case 4: Complex nested data relationships**
→ Use ODataV4Adaptor or RemoteSaveAdaptor + expand() for related data

**Case 5: GraphQL backend**
→ Use GraphQLAdaptor with custom query builder

**Case 6: Legacy ASP.NET ASMX service**
→ Use WebMethodAdaptor with appropriate response mapping

## Key Props & Options

| Property | Type | Purpose |
|----------|------|---------|
| **json** | Array | Local JavaScript array of objects |
| **url** | string | Remote server endpoint URL |
| **adaptor** | Adaptor | JsonAdaptor, ODataAdaptor, WebApiAdaptor, etc. |
| **enableCache** | boolean | Cache pages to prevent redundant requests |
| **offline** | boolean | Enable offline mode with local storage |
| **crossDomain** | boolean | CORS requests to different domain |

## Comparison: DataManager vs Direct Binding

| Feature | DataManager | Direct Binding |
|---------|------------|----------------|
| Flexible adaptors | ✓ Easy switching | ✗ Fixed to one source |
| Complex queries | ✓ Query class with chaining | ✗ Limited filtering |
| CRUD operations | ✓ Full support + batch | ✗ Basic operations |
| Middleware | ✓ Pre/post hooks | ✗ None |
| Caching | ✓ Built-in | ✗ Manual implementation |
| Offline mode | ✓ Built-in | ✗ Manual implementation |
| Performance (small datasets) | ≈ Same | ✓ Slightly faster |
| Performance (large datasets) | ✓ Lazy loading support | ✗ All at once |

**Use DataManager** when building data-driven applications with flexibility, caching, and middleware needs.

**Use direct binding** for simple, one-off displays without complex queries or offline support.
