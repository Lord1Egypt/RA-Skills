# Caching & Offline Mode in React DataManager

## Table of Contents
- [enableCache Property](#enablecache-property)
- [How Cache Works](#how-cache-works)
- [Cache Clearing](#cache-clearing)
- [Programmatic Cache Clearing](#manual-cache-clearing-with-clearcache)
- [Offline Mode Implementation](#offline-mode-implementation)
- [Local Storage Persistence](#local-storage-persistence)
- [Sync After Reconnection](#sync-after-reconnection)
- [Performance Best Practices](#performance-best-practices)

---

## enableCache Property

Enable caching to prevent redundant HTTP requests for previously visited pages:

```tsx
import React, { useEffect, useState } from 'react';
import { DataManager, WebApiAdaptor, Query } from '@syncfusion/ej2-data';

export default function CachingExample() {
  const [page1Data, setPage1Data] = useState([]);
  const [page2Data, setPage2Data] = useState([]);

  useEffect(() => {
    const dataManager = new DataManager({
      url: 'url',
      adaptor: new WebApiAdaptor(),
      enableCache: true  // Enable caching
    });

    // First request - hits server
    dataManager.executeQuery(new Query().take(10).skip(0))
      .then((e) => {
        console.log('Page 1 loaded from server');
        setPage1Data(e.result);
      });

    // Later request - same page retrieved from cache
    dataManager.executeQuery(new Query().take(10).skip(0))
      .then((e) => {
        console.log('Page 1 loaded from cache (no server call)');
        setPage1Data(e.result);
      });

    // Different page - hits server
    dataManager.executeQuery(new Query().take(10).skip(10))
      .then((e) => {
        console.log('Page 2 loaded from server');
        setPage2Data(e.result);
      });
  }, []);

  return <div>Check network tab to see cached requests</div>;
}
```

**Benefits:**
- Reduces server load
- Faster UI response
- Lower bandwidth usage
- Better offline support
- Seamless pagination

**Performance impact:**
- First load: No improvement (still hits server)
- Subsequent same-page loads: ~95% faster (from cache)
- Memory usage: Increases slightly (stores pages in RAM)

---

## How Cache Works

DataManager automatically generates a unique cache ID and stores page data:

```tsx
// Without caching
const dm1 = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor(),
  enableCache: false  // Each request hits server
});

// Query page 1
dm1.executeQuery(new Query().take(10).skip(0))  // Server request
   .then((e) => setData(e.result));

// Query page 1 again
dm1.executeQuery(new Query().take(10).skip(0))  // Another server request (same data!)

// With caching
const dm2 = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor(),
  enableCache: true   // Pages cached in memory
});

// Query page 1
dm2.executeQuery(new Query().take(10).skip(0))  // Server request, then cached
   .then((e) => setData(e.result));

// Query page 1 again
dm2.executeQuery(new Query().take(10).skip(0))  // Retrieved from cache (no server call!)
   .then((e) => setData(e.result));

// Query page 2
dm2.executeQuery(new Query().take(10).skip(10)) // Server request (new page)
   .then((e) => setData(e.result));

// Query page 1 once more
dm2.executeQuery(new Query().take(10).skip(0))  // From cache again
   .then((e) => setData(e.result));
```

---

## Cache Clearing

Cache is automatically cleared when data operations occur:

```tsx
const dataManager = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor(),
  enableCache: true
});

// Load page 1 (cached)
dataManager.executeQuery(new Query().take(10)).then((e) => {
  console.log('Page 1 cached');
});

// Cache is cleared when:
await dataManager.insert(newOrder, 'Orders');      // Insert clears cache
await dataManager.update('OrderID', order, 'Orders');         // Update clears cache
await dataManager.remove('OrderID', id, 'Orders'); // Delete clears cache

// After any CRUD operation
dataManager.executeQuery(new Query().take(10)).then((e) => {
  console.log('Page 1 reloaded from server (cache was cleared)');
});
```

**Cache cleared on:**
- ✓ insert() - add new records
- ✓ update() - modify records
- ✓ remove() - delete records
- ✓ saveChanges() - batch operations
- ✓ where() - filtering changes
- ✓ sortBy() - sorting changes
- ✓ group() - grouping changes

**Cache persists:**
- ✗ Pagination (take/skip)
- ✗ Field selection (select)
- ✗ Expand (same query structure)

---

## Manual Cache Clearing with clearCache()

Clear all cached data manually using the `clearCache()` method:

```tsx
const dataManager = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor(),
  enableCache: true
});

// Load data (cached automatically)
dataManager.executeQuery(new Query().take(10)).then(() => {
  console.log('Data cached');
});

// Option 1: Clear all cached data
dataManager.clearCache();
console.log('All cache cleared');

// Next query will hit server
dataManager.executeQuery(new Query().take(10)).then(() => {
  console.log('Fresh data from server');
});
```

**Method signature:** `dm.clearCache()`

**Purpose:** Clears all cached data from offline mode or browser memory storage

**When to use:**
- After modifying offline data
- During user logout/session end
- Resetting application state
- Manually invalidating entire cache
- After critical data updates

**Real-world example:**

```tsx
export default function OrderManagement() {
  const dataManager = new DataManager({
    url: 'url',
    adaptor: new WebApiAdaptor(),
    enableCache: true
  });

  const handleLogout = () => {
    // Clear all cached user data before logout
    dataManager.clearCache();
    console.log('Cache cleared for security');
    // Redirect to login
    window.location.href = '/login';
  };

  const handleCriticalUpdate = async () => {
    try {
      // Make critical change to data
      await dataManager.update('Orders', criticalData);
      
      // Forces all users to refresh data
      dataManager.clearCache();
      console.log('Cache cleared - all data refreshed');
      
      // Notify UI to reload
      window.location.reload();
    } catch (error) {
      console.error('Update failed:', error);
    }
  };

  return (
    <div>
      <button onClick={handleLogout}>Logout</button>
      <button onClick={handleCriticalUpdate}>Apply Critical Update</button>
    </div>
  );
}
```

**Comparison with automatic clearing:**

```tsx
// AUTOMATIC: CRUD operations clear cache
await dataManager.insert(newOrder, 'Orders');  // Cache cleared automatically
await dataManager.update('OrderID', updated, 'Orders');   // Cache cleared automatically
await dataManager.remove('OrderID', id, 'Orders');        // Cache cleared automatically

// MANUAL: Explicit clearCache() call
dataManager.clearCache();  // Clears all cache regardless of CRUD ops
```

---

## Offline Mode Implementation

Enable offline support for working without internet connection:

```tsx
import React, { useEffect, useState } from 'react';
import { DataManager, WebApiAdaptor, Query } from '@syncfusion/ej2-data';

export default function OfflineModeExample() {
  const [orders, setOrders] = useState([]);
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const dataManager = new DataManager({
      url: 'url',
      adaptor: new WebApiAdaptor(),
      offline: true,          // Enable offline support
      enableCache: true       // Cache data locally
    });

    // Listen for online/offline events
    window.addEventListener('online', () => {
      console.log('Back online - syncing data...');
      setIsOnline(true);
      // Trigger sync of pending changes
      dataManager.saveChanges(changes).then(() => {
        console.log('Data synced');
      });
    });

    window.addEventListener('offline', () => {
      console.log('Going offline - using cached data');
      setIsOnline(false);
    });

    // Load initial data
    dataManager.executeQuery(new Query().take(50))
      .then((e) => {
        setOrders(e.result);
        console.log('Data cached locally for offline use');
      });

    return () => {
      window.removeEventListener('online', () => {});
      window.removeEventListener('offline', () => {});
    };
  }, []);

  return (
    <div>
      <p>Status: {isOnline ? '🟢 Online' : '🔴 Offline'}</p>
      <p>Orders: {orders.length}</p>
      <p>Note: Changes made while offline will sync when reconnected</p>
    </div>
  );
}
```

**Offline mode workflow:**
1. User loads data while online
2. Data cached in browser (localStorage)
3. User goes offline, makes changes
4. Changes queued locally
5. User returns online
6. Changes automatically synced to server

---

## Local Storage Persistence

Store cached data in browser's localStorage for persistent offline access:

> 🔒 **Security Warning:** `localStorage` and `sessionStorage` store data **unencrypted** in the browser. **Never store sensitive data** (passwords, tokens, PII, payment info, user secrets, authentication credentials) in persisted TreeGrid state. State persistence is safe for **UI state only** (expand/collapse state, page number, sort order, column visibility, filter selections). For sensitive configuration or user data, use secure server-side session storage instead.

```tsx
const dataManager = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor(),
  offline: true           // Uses localStorage by default
});

// Data automatically saved to localStorage
dataManager.executeQuery(new Query().take(100)).then((e) => {
  // Data also stored in:
  // localStorage.key = "DataManager_Orders_0" containing e.result
});

// Even after browser closes/reopens, data is available
// (as long as localStorage isn't cleared)

window.addEventListener('beforeunload', () => {
  // localStorage automatically updated before page unload
  console.log('Data persisted to localStorage');
});
```

**localStorage details:**
- **Capacity:** 5-10 MB per domain (varies by browser)
- **Persistence:** Survives browser close/restart
- **Security:** Same-origin policy (same domain only)
- **Clearing:** User can clear via browser settings

**Check what's stored:**
```tsx
// View all DataManager cache in browser DevTools
Object.keys(localStorage).forEach(key => {
  if (key.startsWith('DataManager')) {
    console.log(key, localStorage.getItem(key));
  }
});

// Clear cache manually
localStorage.removeItem('DataManager_Orders_0');
localStorage.clear(); // Clear all
```

---

## Sync After Reconnection

Handle synchronization of offline changes when reconnecting:

```tsx
import React, { useEffect, useState } from 'react';
import { DataManager, WebApiAdaptor, Query } from '@syncfusion/ej2-data';

export default function OfflineSyncExample() {
  const [pendingChanges, setPendingChanges] = useState({
    added: [],
    changed: [],
    deleted: []
  });

  useEffect(() => {
    const dataManager = new DataManager({
      url: 'url',
      adaptor: new WebApiAdaptor(),
      offline: true,
      keyColumn: 'OrderID'
    });

    let offlineChanges = {
      added: [],
      changed: [],
      deleted: []
    };

    // Track changes while offline
    const queueChange = (type, data) => {
      offlineChanges[type].push(data);
      setPendingChanges(offlineChanges);
    };

    // Simulate offline edit
    const editOrder = (order) => {
      if (navigator.onLine) {
        // Online - sync immediately
        dataManager.update('Orders', order);
      } else {
        // Offline - queue for later
        queueChange('changed', order);
      }
    };

    // Listen for reconnection
    window.addEventListener('online', async () => {
      if (offlineChanges.added.length > 0 || 
          offlineChanges.changed.length > 0 ||
          offlineChanges.deleted.length > 0) {
        
        console.log('Syncing offline changes...');
        
        try {
          const result = await dataManager.saveChanges(offlineChanges);
          console.log('Sync complete:', result);
          
          // Clear queued changes after successful sync
          offlineChanges = { added: [], changed: [], deleted: [] };
          setPendingChanges(offlineChanges);
        } catch (error) {
          console.error('Sync failed:', error);
          // Keep pending changes for retry
        }
      }
    });

    return () => {
      window.removeEventListener('online', () => {});
    };
  }, []);

  return (
    <div>
      <p>Pending changes: {pendingChanges.added.length + 
                           pendingChanges.changed.length + 
                           pendingChanges.deleted.length}</p>
    </div>
  );
}
```

**Sync patterns:**
1. **Immediate sync:** Push changes on reconnect
2. **Conflict resolution:** Handle data conflicts
3. **Partial sync:** Retry failed items
4. **Timeout handling:** Mark old offline data as stale

---

## Performance Best Practices

### 1. Use Pagination with Caching

```tsx
const dataManager = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor(),
  enableCache: true,
  pageSize: 20  // Smaller pages = more efficient cache
});

// Load pages as needed
const loadPage = (pageNumber) => {
  const pageSize = 20;
  dataManager.executeQuery(
    new Query()
      .take(pageSize)
      .skip((pageNumber - 1) * pageSize)
  ).then((e) => {
    // Each page cached separately
    console.log(`Page ${pageNumber} loaded`);
  });
};
```

### 2. Monitor Cache Size

```tsx
// Large datasets + caching = high memory usage
// Solution: Limit cache or use virtual scrolling

const dataManager = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor(),
  enableCache: true,
  // Don't cache if expecting 10,000+ records
  pageSize: 50  // Smaller pages, load on demand
});
```

### 3. Clear Cache Explicitly

```tsx
// Force refresh
const refreshData = async () => {
  // Trigger a dummy CRUD to clear cache
  await dataManager.insert(emptyRecord, 'Orders');
  
  // Then reload
  dataManager.executeQuery(new Query().take(10))
    .then((e) => setData(e.result));
};
```

### 4. Combine Cache + Offline Mode

```tsx
const dataManager = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor(),
  enableCache: true,     // Cache for performance
  offline: true,         // Also persist for offline
  crossDomain: true
});

// Result: Fast loading + Offline support + Automatic sync
```

---

## Limitations & Gotchas

| Feature | Limitation |
|---------|-----------|
| **Cache size** | Limited to available browser RAM (varies by browser) |
| **Large datasets** | Cache needs separate memory - consider pagination |
| **Real-time data** | Cache may be stale - no live updates |
| **Multi-tab sync** | Cache not shared between browser tabs |
| **Mobile** | Limited storage on mobile devices |
| **Security** | Cached data visible via DevTools (don't cache secrets) |

---

## Complete Example: Cache + Offline + Sync

```tsx
import React, { useEffect, useState } from 'react';
import { DataManager, WebApiAdaptor, Query } from '@syncfusion/ej2-data';

export default function CompleteOfflineExample() {
  const [orders, setOrders] = useState([]);
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [pendingCount, setPendingCount] = useState(0);

  useEffect(() => {
    const dataManager = new DataManager({
      url: 'url',
      adaptor: new WebApiAdaptor(),
      enableCache: true,      // Performance optimization
      offline: true,          // Offline support
      keyColumn: 'OrderID'
    });

    let changes = { added: [], changed: [], deleted: [] };

    // Online/offline listeners
    window.addEventListener('online', () => {
      setIsOnline(true);
      // Sync any pending changes
      if (changes.added.length > 0 || changes.changed.length > 0 || changes.deleted.length > 0) {
        dataManager.saveChanges(changes).then(() => {
          changes = { added: [], changed: [], deleted: [] };
          setPendingCount(0);
        });
      }
    });

    window.addEventListener('offline', () => {
      setIsOnline(false);
    });

    // Load data
    dataManager.executeQuery(new Query().take(50))
      .then((e) => setOrders(e.result));
  }, []);

  return (
    <div>
      <header>
        <p>Status: {isOnline ? '🟢 Online' : '🔴 Offline'}</p>
        {pendingCount > 0 && <p>Pending changes: {pendingCount}</p>}
      </header>
      <table>
        <thead><tr><th>Order</th><th>Customer</th></tr></thead>
        <tbody>
          {orders.map((order) => (
            <tr key={order.OrderID}>
              <td>{order.OrderID}</td>
              <td>{order.CustomerID}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```
