# Advanced Features in React DataManager

## Table of Contents
- [Load on Demand & Pagination](#load-on-demand--pagination)
- [Virtual Scrolling](#virtual-scrolling)
- [Lazy Loading with Expand](#lazy-loading-with-expand)
- [Deferred Operations](#deferred-operations)
- [Async/Await Patterns](#asyncawait-patterns)
- [State Persistence](#state-persistence)
- [Memory Management](#memory-management)
- [Error Handling Strategies](#error-handling-strategies)
- [Performance Optimization Tips](#performance-optimization-tips)
- [Common Pitfalls](#common-pitfalls)

---

## Load on Demand & Pagination

Implement pagination to load data incrementally instead of all at once:

```tsx
import React, { useEffect, useState } from 'react';
import { DataManager, WebApiAdaptor, Query } from '@syncfusion/ej2-data';

export default function PaginationExample() {
  const [orders, setOrders] = useState([]);
  const [pageSize] = useState(10);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalRecords, setTotalRecords] = useState(0);

  useEffect(() => {
    const dataManager = new DataManager({
      url: 'url',
      adaptor: new WebApiAdaptor()
    });

    // Calculate skip
    const skip = (currentPage - 1) * pageSize;

    // Load current page
    dataManager.executeQuery(
      new Query()
        .skip(skip)
        .take(pageSize)
    ).then((e) => {
      setOrders(e.result);
      setTotalRecords(e.count);
    });
  }, [currentPage, pageSize]);

  const totalPages = Math.ceil(totalRecords / pageSize);

  return (
    <div>
      <table>
        <tbody>
          {orders.map((order) => (
            <tr key={order.OrderID}>
              <td>{order.OrderID}</td>
              <td>{order.CustomerID}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <nav>
        <button 
          onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
          disabled={currentPage === 1}
        >
          Previous
        </button>
        <span>Page {currentPage} of {totalPages}</span>
        <button 
          onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
          disabled={currentPage === totalPages}
        >
          Next
        </button>
      </nav>
    </div>
  );
}
```

**Benefits:**
- Reduced initial load time
- Lower bandwidth usage
- Better for large datasets (100k+ records)
- Smoother user experience

---

## Virtual Scrolling

Render only visible rows for extremely large datasets:

```tsx
// Virtual scrolling with DataManager
import { DataManager, WebApiAdaptor, Query } from '@syncfusion/ej2-data';

export default function VirtualScrollingExample() {
  const [visibleRows, setVisibleRows] = useState([]);
  const pageSize = 10;
  
  const dataManager = new DataManager({
    url: 'url',
    adaptor: new WebApiAdaptor(),
    enableCache: true  // Cache for performance
  });

  const handleScroll = (e) => {
    const { scrollTop, clientHeight } = e.target;
    const scrollPercent = scrollTop / (e.target.scrollHeight - clientHeight);
    
    if (scrollPercent > 0.8) {
      // User scrolled 80% - load next page
      loadNextPage();
    }
  };

  const loadNextPage = async () => {
    const currentCount = visibleRows.length;
    const result = await dataManager.executeQuery(
      new Query()
        .skip(currentCount)
        .take(pageSize)
    );
    
    setVisibleRows([...visibleRows, ...result.result]);
  };

  return (
    <div onScroll={handleScroll} style={{ height: '600px', overflow: 'auto' }}>
      {visibleRows.map((row) => (
        <div key={row.OrderID}>{row.CustomerID}</div>
      ))}
    </div>
  );
}
```

**Use virtual scrolling when:**
- 10,000+ records to display
- Need smooth scrolling without lag
- Working on mobile devices
- Memory usage is critical

---

## Lazy Loading with Expand

Load related data only when needed:

```tsx
import { DataManager, Query, ODataV4Adaptor } from '@syncfusion/ej2-data';

const dataManager = new DataManager({
  url: 'url',
  adaptor: new ODataV4Adaptor()
});

// Basic query (no related data)
const basicQuery = new Query()
  .take(20);

dataManager.executeQuery(basicQuery).then((e) => {
  // { OrderID, CustomerID, ... } but no Customer details
  console.log('Basic:', e.result);
});

// With expand (includes related Customer)
const expandedQuery = new Query()
  .expand('Customer')  // Lazy load related data
  .take(20);

dataManager.executeQuery(expandedQuery).then((e) => {
  // { OrderID, CustomerID, ..., Customer: { CompanyName, ... } }
  console.log('With expand:', e.result[0].Customer);
});

// Multiple related entities
const multiExpandQuery = new Query()
  .expand('Customer')
  .expand('Employee')
  .take(20);

dataManager.executeQuery(multiExpandQuery).then((e) => {
  console.log('Multiple expand:', e.result[0]);
});
```

**Key points:**
- `expand()` only works with OData services that support navigation properties
- Lazy loading reduces initial payload size
- Related data comes nested in the result object
- Use multiple `expand()` calls for multiple relationships

---

## Deferred Operations

The `Deferred` object provides methods for managing asynchronous operations with proper error handling using `.resolve()`, `.reject()`, `.then()`, and `.catch()`:

```tsx
import { DataManager, Deferred, Query, WebApiAdaptor } from '@syncfusion/ej2-data';

// Create a deferred object for async operation management
const deferred = new Deferred();

// Simulate async work (e.g., fetching from API)
setTimeout(() => {
  const result = {
    result: [
      { id: 1, name: 'Order 1' },
      { id: 2, name: 'Order 2' }
    ],
    count: 2
  };
  deferred.resolve(result);  // Mark operation as successful
}, 1000);

// Handle the deferred operation result
deferred.promise
  .then((result) => {
    console.log('Operation succeeded:', result.result);
  })
  .catch((error) => {
    console.error('Operation failed:', error.message);
  });
```

### Deferred with Rejection (Error Handling)

```tsx
import { DataManager, Deferred } from '@syncfusion/ej2-data';

function fetchDataWithError(shouldFail = false) {
  const deferred = new Deferred();

  setTimeout(() => {
    if (shouldFail) {
      deferred.reject(new Error('API returned 500 Server Error'));
    } else {
      deferred.resolve({ result: [{ id: 1, value: 'Success' }] });
    }
  }, 1000);

  return deferred;
}

// Handling rejected deferred
fetchDataWithError(true)
  .promise
  .then((result) => {
    console.log('Success:', result.result);
  })
  .catch((error) => {
    console.error('Error caught:', error.message);  // "API returned 500 Server Error"
  });
```

### Deferred with Query Execution

```tsx
import { DataManager, Query, WebApiAdaptor } from '@syncfusion/ej2-data';

const dm = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor()
});

// executeQuery() returns a Deferred internally
const deferred = dm.executeQuery(
  new Query().where('Status', 'equal', 'Completed').take(10)
);

deferred
  .then((result) => {
    console.log('Query succeeded:', result.result);
    return result.result;
  })
  .catch((error) => {
    console.error('Query failed:', error);
  });
```

### Multiple Deferred Operations (Parallel Execution)

```tsx
import { Deferred } from '@syncfusion/ej2-data';

const deferred1 = new Deferred();
const deferred2 = new Deferred();
const deferred3 = new Deferred();

// Simulate multiple async operations
setTimeout(() => deferred1.resolve({ data: 'Result 1' }), 500);
setTimeout(() => deferred2.resolve({ data: 'Result 2' }), 700);
setTimeout(() => deferred3.resolve({ data: 'Result 3' }), 600);

// Wait for all deferred operations to complete
Promise.all([deferred1.promise, deferred2.promise, deferred3.promise])
  .then((results) => {
    console.log('All operations complete:', results);
  })
  .catch((error) => {
    console.error('One or more operations failed:', error);
  });
```

---

## Async/Await Patterns

Modern async/await syntax for cleaner Promise handling with proper imports:

```tsx
import { DataManager, WebApiAdaptor, Query } from '@syncfusion/ej2-data';

const dataManager = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor(),
  keyColumn: 'OrderID'
});

// AVOID: Without async/await (callback nesting/pyramid of doom)
dataManager.executeQuery(new Query().take(10)).then((e1) => {
  dataManager.executeQuery(new Query().skip(10).take(10)).then((e2) => {
    dataManager.executeQuery(new Query().skip(20).take(10)).then((e3) => {
      console.log('Nested results:', e1.result, e2.result, e3.result);
    }).catch((error) => console.error('Query 3 error:', error));
  }).catch((error) => console.error('Query 2 error:', error));
}).catch((error) => console.error('Query 1 error:', error));

// RECOMMENDED: With async/await (sequential execution)
const loadDataSequential = async () => {
  try {
    // Execute queries one after another
    const result1 = await dataManager.executeQuery(new Query().take(10));
    const result2 = await dataManager.executeQuery(new Query().skip(10).take(10));
    const result3 = await dataManager.executeQuery(new Query().skip(20).take(10));
    
    console.log('Sequential results:', result1.result, result2.result, result3.result);
  } catch (error) {
    if (error.status === 401) {
      console.error('Unauthorized - refresh token');
    } else if (error.status === 500) {
      console.error('Server error - retry later');
    } else {
      console.error('Query failed:', error.message);
    }
  }
};

await loadDataSequential();

// BEST: Parallel async operations with Promise.all()
const loadDataParallel = async () => {
  try {
    // Execute all queries simultaneously
    const [result1, result2, result3] = await Promise.all([
      dataManager.executeQuery(new Query().take(10)),
      dataManager.executeQuery(new Query().skip(10).take(10)),
      dataManager.executeQuery(new Query().skip(20).take(10))
    ]);
    
    console.log('Parallel results:', result1.result, result2.result, result3.result);
  } catch (error) {
    console.error('One or more queries failed:', error);
  }
};

await loadDataParallel();
```

---

## State Persistence

Syncfusion DataManager provides built-in state persistence using browser localStorage. Query states are automatically saved and restored across page reloads.

### Basic State Persistence

```tsx
import React, { useEffect, useState } from 'react';
import { DataManager, WebApiAdaptor, Query } from '@syncfusion/ej2-data';

export default function StatePersistenceExample() {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    const dataManager = new DataManager({
      url: 'url',
      adaptor: new WebApiAdaptor(),
      enablePersistence: true,      // Enable state persistence
      id: 'reactOrderManager'       // Unique ID for localStorage key
    });

    // Execute a query with sorting
    dataManager.executeQuery(
      new Query().sortBy('CustomerID', 'descending').take(10)
    ).then((result) => {
      setOrders(result.result);
      // Query state (sorting) automatically saved to localStorage
    }).catch((error) => {
      console.error('Error:', error);
    });
  }, []);

  return (
    <div>
      <h3>Orders (sorted by CustomerID desc)</h3>
      <ul>
        {orders.map((order) => (
          <li key={order.OrderID}>{order.CustomerID} - ${order.Freight}</li>
        ))}
      </ul>
      <p>Note: Sorting state persisted. Refresh page to see state restored.</p>
    </div>
  );
}
```

### Excluding Queries from Persistence

```tsx
import React, { useEffect, useState } from 'react';
import { DataManager, UrlAdaptor, Query } from '@syncfusion/ej2-data';

export default function SelectivePersistenceExample() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    const dataManager = new DataManager({
      url: 'url',
      adaptor: new UrlAdaptor(),
      enablePersistence: true,
      id: 'reactProductManager',
      ignoreOnPersist: ['onSortBy', 'onSearch']  // Don't persist sorting and search
    });

    // These will be persisted: filtering, grouping
    // These will NOT be persisted: sorting, search

    dataManager.executeQuery(
      new Query()
        .where('Status', 'equal', 'Active')
        .sortBy('Price', 'descending')  // Won't persist
    ).then((result) => {
      setProducts(result.result);
    }).catch((error) => {
      console.error('Error:', error);
    });
  }, []);

  return (
    <div>
      <h3>Products</h3>
      <ul>
        {products.map((product) => (
          <li key={product.ProductID}>{product.ProductName}</li>
        ))}
      </ul>
    </div>
  );
}
```

### Retrieve Persisted State

```tsx
import React from 'react';
import { DataManager } from '@syncfusion/ej2-data';

export default function GetPersistedDataExample() {
  const handleGetState = () => {
    // Retrieve the persisted query state from localStorage
    const persisted = DataManager.getPersistedData('reactOrderManager');
    console.log('Persisted state:', persisted);
    // Output: { onSortBy: [{field: 'CustomerID', direction: 'descending'}], ... }
  };

  return (
    <button onClick={handleGetState}>Show Persisted State</button>
  );
}
```

### Update Persisted State

```tsx
import React from 'react';
import { DataManager, Query } from '@syncfusion/ej2-data';

export default function SetPersistedDataExample() {
  const handleUpdateState = () => {
    // Create a new query to be persisted
    const newQuery = new Query()
      .where('Freight', 'greaterThan', 100)
      .sortBy('EmployeeID', 'descending');

    // Update the persisted state in localStorage
    DataManager.setPersistData(
      null,                         // event: null when not in event context
      'reactOrderManager',         // DataManager id
      newQuery                     // New query to persist
    );

    console.log('Persisted state updated');
  };

  return (
    <button onClick={handleUpdateState}>Update Persisted State</button>
  );
}
```

### Clear Persisted State

```tsx
import React from 'react';
import { DataManager } from '@syncfusion/ej2-data';

export default function ClearPersistenceExample() {
  const handleClear = () => {
    // Remove all persisted data for this DataManager
    DataManager.clearPersistence('reactOrderManager');
    console.log('Persisted state cleared - DataManager reset to initial state');
  };

  const handleLogout = () => {
    // Clear persistence for multiple DataManagers on logout
    DataManager.clearPersistence('reactOrderManager');
    DataManager.clearPersistence('reactProductManager');
    console.log('All persisted states cleared');
  };

  return (
    <div>
      <button onClick={handleClear}>Clear This DataManager</button>
      <button onClick={handleLogout}>Clear All (Logout)</button>
    </div>
  );
}
```

### Persistence Properties Reference

| Property | Type | Purpose |
|----------|------|---------|
| `enablePersistence` | boolean | Enable/disable state persistence |
| `id` | string | Unique identifier for localStorage key |
| `ignoreOnPersist` | string[] | Query types to exclude: `onSortBy`, `onSearch`, `onWhere`, `Grouping` |

---

## Memory Management

Prevent memory leaks and manage memory efficiently:

> 🔒 **Security Warning:** `localStorage` and `sessionStorage` store data **unencrypted** in the browser. **Never store sensitive data** (passwords, tokens, PII, payment info, user secrets, authentication credentials) in persisted TreeGrid state. State persistence is safe for **UI state only** (expand/collapse state, page number, sort order, column visibility, filter selections). For sensitive configuration or user data, use secure server-side session storage instead.

```tsx
import { DataManager, WebApiAdaptor, Query } from '@syncfusion/ej2-data';

const dataManager = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor(),
  enableCache: true
});

// ❌ WRONG: Creates memory leak
const loadAllPagesBad = () => {
  for (let i = 0; i < 1000; i++) {
    dataManager.executeQuery(
      new Query().take(10).skip(i * 10)
    ); // All promises kept in memory - results never freed
  }
};

// ✅ CORRECT: Load on demand
const loadPageOnDemand = (pageNumber: number) => {
  dataManager.executeQuery(
    new Query()
      .take(10)
      .skip((pageNumber - 1) * 10)
  ).then((e: any) => {
    // Process page, release previous results
    console.log('Page loaded:', e.result);
    // e.result is automatically garbage collected after use
  }).catch((error: any) => {
    console.error('Load failed:', error);
  });
};

// ✅ CORRECT: Clear cache periodically
setInterval(() => {
  // Clear old cache entries manually if needed
  localStorage.removeItem('DataManager_old_cache');
  // Or clear specific datetime-based caches
}, 3600000); // Every hour

// ✅ CORRECT: Limit concurrent requests
let activeRequests = 0;
const maxConcurrent = 5;

const loadWithLimit = async (pageNumber: number) => {
  if (activeRequests >= maxConcurrent) {
    // Queue or wait
    await new Promise(r => setTimeout(r, 100));
  }
  
  activeRequests++;
  try {
    const result = await dataManager.executeQuery(
      new Query().take(10).skip((pageNumber - 1) * 10)
    );
    return result.result;
  } finally {
    activeRequests--;
  }
};
```

**Memory management best practices:**
- Use `take()` and `skip()` for pagination, not load-all patterns
- Enable `enableCache: true` but understand cache size limits
- Clear localStorage cache periodically for offline-enabled DataManagers
- Limit concurrent requests to avoid browser resource exhaustion
- Release references to large result sets when no longer needed

---

## Error Handling Strategies

DataManager uses Promise-based error handling. Errors from `executeQuery()` and `executeLocal()` are caught using `.catch()` on the Promise or `try/catch` with `async/await`.

**Strategy 1: Promise .catch() Pattern**

```tsx
const dataManager = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor(),
  keyColumn: 'OrderID'
});

const query = new Query().take(10);

dataManager.executeQuery(query)
  .then((result) => {
    console.log('Data loaded successfully:', result);
  })
  .catch((error) => {
    // Error object properties: status, statusText, message
    if (error.status === 401) {
      console.error('Unauthorized: Please log in again');
    } else if (error.status === 500) {
      console.error('Server error: Please try again later');
    } else if (error.status === 0) {
      console.error('Network error: Check your connection');
    } else {
      console.error('Failed to load data:', error.message);
    }
  });
```

**Strategy 2: Try/Catch with Async/Await**

```tsx
const handleDataLoad = async () => {
  try {
    const query = new Query().take(10);
    const result = await dataManager.executeQuery(query);
    console.log('Data loaded successfully:', result);
  } catch (error) {
    if (error.status === 401) {
      // Handle authentication errors
      redirectToLogin();
    } else if (error.status === 403) {
      // Handle authorization errors
      showMessage('You do not have permission to access this data');
    } else if (error.status === 500) {
      // Handle server errors
      showMessage('Server error - please try again later');
    } else if (error.status === 0) {
      // Handle network errors
      showMessage('Network error - check your connection');
    } else {
      // Handle other errors
      showMessage('Failed to load data');
    }
  }
};
```

**Strategy 3: Retry with Exponential Backoff**

```tsx
const executeWithRetry = async (query: Query, maxRetries = 3): Promise<any> => {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await dataManager.executeQuery(query);
    } catch (error) {
      if (attempt === maxRetries) {
        throw error; // Throw on final attempt
      }
      
      // Exponential backoff: 1s, 2s, 4s
      const delayMs = Math.pow(2, attempt - 1) * 1000;
      await new Promise(resolve => setTimeout(resolve, delayMs));
    }
  }
};

// Usage
try {
  const result = await executeWithRetry(query);
} catch (error) {
  console.error('Failed after retries:', error);
}
```

**Strategy 4: Fallback Data with User Notification**

```tsx
const loadDataWithFallback = async (query: Query) => {
  try {
    return await dataManager.executeQuery(query);
  } catch (error) {
    console.warn('Failed to load from server, using fallback data:', error);
    
    // Show user notification
    showNotification({
      type: 'warning',
      message: 'Using offline data - some information may be outdated'
    });
    
    // Return cached or default data
    return getFallbackData();
  }
};
```

**Key Points on Error Handling:**

- Error objects contain: `status` (HTTP status code), `statusText`, `message`, `responseText`
- Common status codes: 401 (unauthorized), 403 (forbidden), 500 (server error), 0 (network error)
- Always catch errors from `executeQuery()` and `executeLocal()` using `.catch()` or `try/catch`
- Use error status codes to determine appropriate user-facing messages
- Apply retry logic for transient failures (network errors, temporary server issues)
- Implement fallback strategies for mission-critical data operations

---

## Performance Optimization Tips

| Tip | Impact | Implementation |
|-----|--------|-----------------|
| **Use pagination** | High | take()/skip() for large datasets |
| **Enable caching** | High | enableCache: true |
| **Select only needed fields** | Medium | select(['field1', 'field2']) |
| **Use appropriate adaptor** | High | Match your backend (OData, WebApi, etc.) |
| **Async/await instead of callbacks** | Low | Cleaner code, same performance |
| **Virtual scrolling** | High | For 10,000+ visible rows |
| **Expand over multiple queries** | Medium | Use expand() for related data |
| **Batch CRUD operations** | High | saveChanges() instead of multiple calls |

---

## Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| **No KeyField** | Can't update/delete | Set keyColumn property |
| **Large dataset without paging** | Browser freeze | Implement pagination |
| **Cache too aggressive** | Stale data | Understand cache clearing rules |
| **Missing error handling** | Silent failures | Add try/catch with async/await or .catch() on Promises |
| **Synchronous CRUD** | Blocking UI | Use async/await patterns |
| **No offline support** | Offline not working | Set offline: true |
| **All data on first load** | Slow initial load | Use pagination/lazy loading |
| **Unoptimized queries** | Slow performance | Use select(), where(), pagination |

---

## Complete Advanced Example

```tsx
import React, { useEffect, useState, useCallback } from 'react';
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';

export default function AdvancedDataManager() {
  const [orders, setOrders] = useState([]);
  const [page, setPage] = useState(1);
  const [filter, setFilter] = useState('');
  const [sort, setSortBy] = useState('OrderDate');
  const [loading, setLoading] = useState(false);

  const dataManager = new DataManager({
    url: 'url',
    adaptor: new ODataV4Adaptor(),
    enableCache: true,
    offline: true,
    keyColumn: 'OrderID'
  });

  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      const pageSize = 20;
      let query = new Query()
        .skip((page - 1) * pageSize)
        .take(pageSize)
        .expand('Customer')
        .sortBy(sort);

      if (filter) {
        query = query.where('ShipCity', 'equal', filter);
      }

      const result = await dataManager.executeQuery(query);
      setOrders(result.result);
    } catch (error) {
      console.error('Load failed:', error);
    } finally {
      setLoading(false);
    }
  }, [page, filter, sort]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  return (
    <div>
      <input 
        type="text" 
        placeholder="Filter by city..."
        value={filter}
        onChange={(e) => {
          setFilter(e.target.value);
          setPage(1); // Reset to page 1 on filter change
        }}
      />

      <select value={sort} onChange={(e) => setSortBy(e.target.value)}>
        <option value="OrderDate">Date</option>
        <option value="ShipCity">City</option>
        <option value="Freight">Freight</option>
      </select>

      {loading && <p>Loading...</p>}

      <table>
        <thead>
          <tr>
            <th>Order ID</th>
            <th>Customer</th>
            <th>City</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {orders.map((order) => (
            <tr key={order.OrderID}>
              <td>{order.OrderID}</td>
              <td>{order.Customer?.CompanyName}</td>
              <td>{order.ShipCity}</td>
              <td>{new Date(order.OrderDate).toLocaleDateString()}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <nav>
        <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1}>
          Previous
        </button>
        <span>Page {page}</span>
        <button onClick={() => setPage(p => p + 1)}>Next</button>
      </nav>
    </div>
  );
}
```
