# Middleware & Customization in React DataManager

## Table of Contents
- [Pre-Request Middleware](#pre-request-middleware)
- [Post-Request Middleware](#post-request-middleware)
- [Custom Headers](#custom-headers)
- [Additional Parameters](#additional-parameters)
- [Response Transformation](#response-transformation)
- [Error Handler](#error-handler)
- [Middleware Execution Order](#middleware-execution-order)

---

## Pre-Request Middleware

Intercept and modify requests before they're sent to the server using `applyPreRequestMiddlewares()`:

> 🔒 **Security Warning:** `localStorage` and `sessionStorage` store data **unencrypted** in the browser. **Never store sensitive data** (passwords, tokens, PII, payment info, user secrets, authentication credentials) in persisted TreeGrid state. State persistence is safe for **UI state only** (expand/collapse state, page number, sort order, column visibility, filter selections). For sensitive configuration or user data, use secure server-side session storage instead.

```tsx
import React, { useEffect, useState } from 'react';
import { DataManager, WebApiAdaptor, Query } from '@syncfusion/ej2-data';

export default function PreRequestMiddleware() {
  useEffect(() => {
    const dataManager = new DataManager({
      url: 'url',
      adaptor: new WebApiAdaptor()
    });

    // Apply pre-request middleware to add auth token
    dataManager.applyPreRequestMiddlewares([
      async (context) => {
        // Fetch token from auth service
        const token = localStorage.getItem('authToken');
        
        if (token) {
          // Add to request headers
          context.request.headers = context.request.headers || {};
          context.request.headers['Authorization'] = `send_token`;
        }
        
        // Can also modify query parameters or body
        console.log('Request prepared:', context.request);
      }
    ]);

    dataManager.executeQuery(new Query().take(10))
      .then((e) => console.log(e.result));
  }, []);

  return <div>Check console for middleware execution</div>;
}
```

**Common use cases:**
- **Authentication:** Add JWT tokens or API keys
- **Request tracking:** Add correlation IDs
- **Header normalization:** Set Content-Type, Accept headers
- **Request logging:** Track API calls
- **Request validation:** Verify before sending

```tsx
// Multiple middleware functions
dataManager.applyPreRequestMiddlewares([
  async (context) => {
    // First: Add auth token
    context.request.headers['Authorization'] = `send_token`;
  },
  async (context) => {
    // Second: Add correlation ID
    context.request.headers['X-Correlation-ID'] = generateId();
  },
  async (context) => {
    // Third: Log request
    console.log('Outgoing request:', context.request);
  }
]);
```

---

## Post-Request Middleware

Process responses before they're bound to components using `applyPostRequestMiddlewares()`:

```tsx
import React, { useEffect, useState } from 'react';
import { DataManager, WebApiAdaptor, Query } from '@syncfusion/ej2-data';

export default function PostRequestMiddleware() {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    const dataManager = new DataManager({
      url: 'url',
      adaptor: new WebApiAdaptor()
    });

    // Apply post-request middleware to transform response
    dataManager.applyPostRequestMiddlewares([
      async (context) => {
        // Transform response data format
        if (context.response && context.response.result) {
          context.response.result = context.response.result.map(item => ({
            id: item.OrderID,
            customer: item.CustomerID,
            amount: parseFloat(item.Freight),
            date: new Date(item.OrderDate).toLocaleDateString()
          }));
        }
        
        console.log('Response transformed:', context.response);
      }
    ]);

    dataManager.executeQuery(new Query().take(10))
      .then((e) => {
        setOrders(e.result); // Already transformed
      });
  }, []);

  return (
    <ul>
      {orders.map((order) => (
        <li key={order.id}>{order.customer} - ${order.amount}</li>
      ))}
    </ul>
  );
}
```

**Common use cases:**
- **Data transformation:** Convert server field names to UI format
- **Data formatting:** Parse dates, format numbers
- **Data filtering:** Remove sensitive fields
- **Data aggregation:** Combine related fields
- **Response validation:** Verify expected structure
- **Error mapping:** Transform error responses

```tsx
// Filter sensitive data from response
dataManager.applyPostRequestMiddlewares([
  async (context) => {
    context.response.result = context.response.result.map(item => {
      const { password, ssn, ...safe } = item;
      return safe; // Exclude sensitive fields
    });
  }
]);

// Format currency and dates
dataManager.applyPostRequestMiddlewares([
  async (context) => {
    context.response.result = context.response.result.map(item => ({
      ...item,
      Freight: `$${item.Freight.toFixed(2)}`,
      OrderDate: new Date(item.OrderDate).toLocaleDateString('en-US')
    }));
  }
]);
```

---

## Custom Headers

Add custom headers to all requests:

```tsx
const dataManager = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor()
});

dataManager.applyPreRequestMiddlewares([
  async (context) => {
    context.request.headers = {
      ...context.request.headers,
      'Authorization': `send_token`,
      'X-API-Version': '2.0',
      'X-Client-ID': 'mobile-app',
      'X-Request-ID': generateUUID(),
      'User-Agent': 'CustomApp/1.0'
    };
  }
]);
```

**Common custom headers:**
- `Authorization`: Authentication token
- `X-API-Key`: API key (less secure than Bearer)
- `X-API-Version`: API version (for versioning)
- `X-Client-ID`: Identify client app
- `X-Request-ID`: Correlation ID for logging
- `X-Tenant-ID`: Multi-tenant applications

```tsx
// Conditional header based on user role
dataManager.applyPreRequestMiddlewares([
  async (context) => {
    const userRole = getCurrentUserRole();
    
    if (userRole === 'admin') {
      context.request.headers['X-Admin-Access'] = 'true';
    }
    
    if (isOfflineMode()) {
      context.request.headers['X-Offline-Mode'] = 'sync';
    }
  }
]);
```

---

## Additional Parameters

Send extra data with every request:

```tsx
const dataManager = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor()
});

// Method 1: Pre-request middleware
dataManager.applyPreRequestMiddlewares([
  async (context) => {
    // Add query parameters
    const params = new URLSearchParams();
    params.append('userId', '12345');
    params.append('language', 'en-US');
    params.append('timezone', 'UTC');
    
    context.request.url = context.request.url + '?' + params.toString();
  }
]);

// Method 2: With Query class (server-side filtering)
const query = new Query()
  .addParams('userId', '12345')
  .addParams('language', 'en-US')
  .take(10);

dataManager.executeQuery(query);
```

**Sending additional parameters for:**
- **User context:** User ID, timezone, language
- **Tracking:** Session ID, request ID, source
- **Filtering:** Tenant ID, organization, etc.
- **API versioning:** Version number

```tsx
// Multi-tenant example
dataManager.applyPreRequestMiddlewares([
  async (context) => {
    const tenantId = getCurrentTenantId();
    
    // Add to URL
    context.request.url = context.request.url + `?tenantId=${tenantId}`;
    
    // Or add to headers
    context.request.headers['X-Tenant-ID'] = tenantId;
  }
]);
```

---

## Response Transformation

Convert server response format to application format:

```tsx
// Problem: Server returns old format, app expects new format
// Server response:
// { order_id: 123, customer_name: "John", total_amount: 99.99 }

// Expected format:
// { OrderID: 123, CustomerName: "John", TotalAmount: 99.99 }

dataManager.applyPostRequestMiddlewares([
  async (context) => {
    context.response.result = context.response.result.map(item => ({
      OrderID: item.order_id,
      CustomerName: item.customer_name,
      TotalAmount: item.total_amount,
      FormattedAmount: `$${item.total_amount.toFixed(2)}`
    }));
  }
]);
```

**Advanced transformation:**
```tsx
// Convert nested response structure
dataManager.applyPostRequestMiddlewares([
  async (context) => {
    // Flatten nested data
    context.response.result = context.response.result.map(item => ({
      ...item,
      CustomerCity: item.customer?.address?.city,
      CustomerCountry: item.customer?.address?.country
    }));
  }
]);

// Aggregate related items
dataManager.applyPostRequestMiddlewares([
  async (context) => {
    const grouped = {};
    
    for (const item of context.response.result) {
      const key = item.orderId;
      if (!grouped[key]) {
        grouped[key] = { ...item, items: [] };
      }
      grouped[key].items.push(item.lineItem);
    }
    
    context.response.result = Object.values(grouped);
  }
]);
```

---

## Error Handling with Middleware

Handle errors from middleware-wrapped requests using Promise `.catch()` or `try/catch`:

```tsx
const dataManager = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor()
});

// Apply pre-request middleware
dataManager.applyPreRequestMiddlewares = async (args: any) => {
  const headers = args.headers || {};
  headers['Authorization'] = `send_token`;
  args.headers = headers;
  return args;
};

// Handle errors by catching on executeQuery/executeLocal Promises
dataManager.executeQuery(new Query())
  .then((result) => {
    console.log('Success:', result.result);
  })
  .catch((error) => {
    console.error('Middleware or fetch error:', error);
    
    // Handle specific error types
    if (error.status === 401) {
      // Unauthorized - token may be expired
      refreshToken();
      redirectToLogin();
    } else if (error.status === 403) {
      // Forbidden - permission denied
      showNotification('You do not have permission to access this data');
    } else if (error.status === 500) {
      // Server error
      console.error('Server error - please try again later');
    } else if (error.status === 0) {
      // Network error
      console.error('Network error - check your connection');
    }
  });
```

---

## Middleware Execution Order

Middleware functions execute in defined order:

```
1. Pre-Request Middleware (in order defined)
   ↓
2. HTTP Request sent
   ↓
3. Response received
   ↓
4. Post-Request Middleware (in order defined)
   ↓
5. Data bound to component
```

**Example showing order:**
```tsx
dataManager.applyPreRequestMiddlewares([
  async (context) => {
    console.log('1. First pre-request middleware');
  },
  async (context) => {
    console.log('2. Second pre-request middleware');
  }
]);

dataManager.applyPostRequestMiddlewares([
  async (context) => {
    console.log('4. First post-request middleware');
  },
  async (context) => {
    console.log('5. Second post-request middleware');
  }
]);

dataManager.executeQuery(new Query().take(10))
  .then((e) => {
    console.log('6. Results bound:', e.result);
  });

// Console output order:
// 1. First pre-request middleware
// 2. Second pre-request middleware
// (Request sent...)
// 4. First post-request middleware
// 5. Second post-request middleware
// 6. Results bound
```

---

## Complete Example: Authentication + Transformation + Error Handling

> 🔒 **Security Warning:** `localStorage` and `sessionStorage` store data **unencrypted** in the browser. **Never store sensitive data** (passwords, tokens, PII, payment info, user secrets, authentication credentials) in persisted TreeGrid state. State persistence is safe for **UI state only** (expand/collapse state, page number, sort order, column visibility, filter selections). For sensitive configuration or user data, use secure server-side session storage instead.

```tsx
import React, { useEffect, useState } from 'react';
import { DataManager, WebApiAdaptor, Query } from '@syncfusion/ej2-data';

export default function CompleteMiddlewareExample() {
  const [orders, setOrders] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const dataManager = new DataManager({
      url: 'url',
      adaptor: new WebApiAdaptor()
    });

    // Pre-request: Add authentication
    dataManager.applyPreRequestMiddlewares([
      async (context) => {
        const token = localStorage.getItem('authToken');
        context.request.headers = {
          ...context.request.headers,
          'Authorization': `send_token`,
          'X-REQUEST-ID': Math.random().toString(36).substr(2, 9)
        };
      }
    ]);

    // Post-request: Transform response
    dataManager.applyPostRequestMiddlewares([
      async (context) => {
        if (context.response?.result) {
          context.response.result = context.response.result.map(item => ({
            id: item.OrderID,
            customer: item.CustomerID,
            freight: `$${parseFloat(item.Freight).toFixed(2)}`,
            date: new Date(item.OrderDate).toLocaleDateString()
          }));
        }
      }
    ]);

    // Execute query with error handling
    dataManager.executeQuery(new Query().take(10))
      .then((e) => {
        setOrders(e.result);
        setError(null);
      })
      .catch((err) => {
        console.error('Failed to load orders:', err);
        
        // Handle specific errors
        if (err.status === 401) {
          setError('Authentication failed - please log in again');
          redirectToLogin();
        } else if (err.status === 403) {
          setError('You do not have permission to access this data');
        } else if (err.status === 0) {
          setError('Network error - check your connection');
        } else {
          setError('Failed to load data - please try again');
        }
      });
  }, []);

  if (error) {
    return <div style={{color: 'red'}}>{error}</div>;
  }

  return (
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Customer</th>
          <th>Freight</th>
          <th>Date</th>
        </tr>
      </thead>
      <tbody>
        {orders.map((order) => (
          <tr key={order.id}>
            <td>{order.id}</td>
            <td>{order.customer}</td>
            <td>{order.freight}</td>
            <td>{order.date}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```
