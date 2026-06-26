# Realtime

**Impact: MEDIUM**

SSE subscriptions, event handling, connection management, and authentication with realtime.

---

## 1. Authenticate Realtime Connections

**Impact: MEDIUM (Secure subscriptions respecting API rules)**

Realtime subscriptions respect collection API rules. Ensure the connection is authenticated before subscribing to protected data.

**Incorrect (subscribing without auth context):**

```javascript
// Subscribing before authentication
const pb = new PocketBase('http://127.0.0.1:8090');

// This will fail or return no data if collection requires auth
pb.collection('private_messages').subscribe('*', (e) => {
  // Won't receive events - not authenticated!
  console.log(e.record);
});

// Later user logs in, but subscription doesn't update
await pb.collection('users').authWithPassword(email, password);
// Existing subscription still unauthenticated!
```

**Correct (authenticated subscriptions):**

```javascript
// Subscribe after authentication
const pb = new PocketBase('http://127.0.0.1:8090');

async function initRealtime() {
  // First authenticate
  await pb.collection('users').authWithPassword(email, password);

  // Now subscribe - will use auth context
  pb.collection('private_messages').subscribe('*', (e) => {
    // Receives events for messages user can access
    console.log('New message:', e.record);
  });
}

// Re-subscribe after auth changes
function useAuthenticatedRealtime() {
  const [messages, setMessages] = useState([]);
  const unsubRef = useRef(null);

  // Watch auth changes
  useEffect(() => {
    const removeListener = pb.authStore.onChange((token, record) => {
      // Unsubscribe old connection
      if (unsubRef.current) {
        unsubRef.current();
        unsubRef.current = null;
      }

      // Re-subscribe with new auth context if logged in
      if (record) {
        setupSubscription();
      } else {
        setMessages([]);
      }
    }, true);

    return () => {
      removeListener();
      if (unsubRef.current) unsubRef.current();
    };
  }, []);

  async function setupSubscription() {
    unsubRef.current = await pb.collection('private_messages').subscribe('*', (e) => {
      handleMessage(e);
    });
  }
}

// Handle auth token refresh with realtime
pb.realtime.subscribe('PB_CONNECT', async (e) => {
  console.log('Realtime connected');

  // Verify auth is still valid
  if (pb.authStore.isValid) {
    try {
      await pb.collection('users').authRefresh();
    } catch {
      pb.authStore.clear();
      // Redirect to login
    }
  }
});
```

**API rules apply to subscriptions:**

```javascript
// Collection rule: listRule: 'owner = @request.auth.id'

// User A subscribed
await pb.collection('users').authWithPassword('a@test.com', 'password');
pb.collection('notes').subscribe('*', handler);
// Only receives events for notes where owner = User A

// Events from other users' notes are filtered out automatically
```

**Subscription authorization flow:**

1. SSE connection established (no auth check)
2. First subscription triggers authorization
3. Auth token from `pb.authStore` is used
4. Collection rules evaluated for each event
5. Only matching events sent to client

**Handling auth expiration:**

```javascript
// Setup disconnect handler
pb.realtime.onDisconnect = (subscriptions) => {
  console.log('Disconnected, had subscriptions:', subscriptions);

  // Check if auth expired
  if (!pb.authStore.isValid) {
    // Token expired - need to re-authenticate
    redirectToLogin();
    return;
  }

  // Connection issue - realtime will auto-reconnect
  // Re-subscribe after reconnection
  pb.realtime.subscribe('PB_CONNECT', () => {
    resubscribeAll(subscriptions);
  });
};

function resubscribeAll(subscriptions) {
  subscriptions.forEach(sub => {
    const [collection, topic] = sub.split('/');
    pb.collection(collection).subscribe(topic, handlers[sub]);
  });
}
```

Reference: [PocketBase Realtime Auth](https://pocketbase.io/docs/api-realtime/)

## 2. Handle Realtime Events Properly

**Impact: MEDIUM (Consistent UI state, proper optimistic updates)**

Realtime events should update local state correctly, handle edge cases, and maintain UI consistency.

**Incorrect (naive event handling):**

```javascript
// Blindly appending creates - may add duplicates
pb.collection('posts').subscribe('*', (e) => {
  if (e.action === 'create') {
    posts.push(e.record);  // Might already exist from optimistic update!
  }
});

// Not handling own actions
pb.collection('posts').subscribe('*', (e) => {
  // User creates post -> optimistic update
  // Realtime event arrives -> duplicate!
  setPosts(prev => [...prev, e.record]);
});

// Missing action types
pb.collection('posts').subscribe('*', (e) => {
  if (e.action === 'create') handleCreate(e);
  // Ignoring update and delete!
});
```

**Correct (robust event handling):**

```javascript
// Handle all action types with deduplication
function useRealtimePosts() {
  const [posts, setPosts] = useState([]);
  const pendingCreates = useRef(new Set());

  useEffect(() => {
    loadPosts();

    const unsub = pb.collection('posts').subscribe('*', (e) => {
      switch (e.action) {
        case 'create':
          // Skip if we created it (optimistic update already applied)
          if (pendingCreates.current.has(e.record.id)) {
            pendingCreates.current.delete(e.record.id);
            return;
          }
          setPosts(prev => {
            // Deduplicate - might already exist
            if (prev.some(p => p.id === e.record.id)) return prev;
            return [e.record, ...prev];
          });
          break;

        case 'update':
          setPosts(prev => prev.map(p =>
            p.id === e.record.id ? e.record : p
          ));
          break;

        case 'delete':
          setPosts(prev => prev.filter(p => p.id !== e.record.id));
          break;
      }
    });

    return unsub;
  }, []);

  async function createPost(data) {
    // Optimistic update
    const tempId = `temp_${Date.now()}`;
    const optimisticPost = { ...data, id: tempId };
    setPosts(prev => [optimisticPost, ...prev]);

    try {
      const created = await pb.collection('posts').create(data);
      // Mark as pending so realtime event is ignored
      pendingCreates.current.add(created.id);
      // Replace optimistic with real
      setPosts(prev => prev.map(p =>
        p.id === tempId ? created : p
      ));
      return created;
    } catch (error) {
      // Rollback optimistic update
      setPosts(prev => prev.filter(p => p.id !== tempId));
      throw error;
    }
  }

  return { posts, createPost };
}

// Batched updates for high-frequency changes
function useRealtimeWithBatching() {
  const [posts, setPosts] = useState([]);
  const pendingUpdates = useRef([]);
  const flushTimeout = useRef(null);

  useEffect(() => {
    const unsub = pb.collection('posts').subscribe('*', (e) => {
      pendingUpdates.current.push(e);

      // Batch updates every 100ms
      if (!flushTimeout.current) {
        flushTimeout.current = setTimeout(() => {
          flushUpdates();
          flushTimeout.current = null;
        }, 100);
      }
    });

    return () => {
      unsub();
      if (flushTimeout.current) clearTimeout(flushTimeout.current);
    };
  }, []);

  function flushUpdates() {
    const updates = pendingUpdates.current;
    pendingUpdates.current = [];

    setPosts(prev => {
      let next = [...prev];
      for (const e of updates) {
        if (e.action === 'create') {
          if (!next.some(p => p.id === e.record.id)) {
            next.unshift(e.record);
          }
        } else if (e.action === 'update') {
          next = next.map(p => p.id === e.record.id ? e.record : p);
        } else if (e.action === 'delete') {
          next = next.filter(p => p.id !== e.record.id);
        }
      }
      return next;
    });
  }
}
```

**Filtering events:**

```javascript
// Only handle events matching certain criteria
pb.collection('posts').subscribe('*', (e) => {
  // Only published posts
  if (e.record.status !== 'published') return;

  // Only posts by current user
  if (e.record.author !== pb.authStore.record?.id) return;

  handleEvent(e);
});

// Subscribe with expand to get related data
pb.collection('posts').subscribe('*', (e) => {
  // Note: expand data is included in realtime events
  // if the subscription options include expand
  console.log(e.record.expand?.author?.name);
}, { expand: 'author' });
```

Reference: [PocketBase Realtime Events](https://pocketbase.io/docs/api-realtime/)

## 3. Handle Realtime Connection Issues

**Impact: MEDIUM (Reliable realtime even with network interruptions)**

Realtime connections can disconnect due to network issues or server restarts. Implement proper reconnection handling and state synchronization.

**Incorrect (ignoring connection issues):**

```javascript
// No reconnection handling - stale data after disconnect
pb.collection('posts').subscribe('*', (e) => {
  updateUI(e.record);
});
// If connection drops, UI shows stale data indefinitely

// Assuming connection is always stable
function PostList() {
  useEffect(() => {
    pb.collection('posts').subscribe('*', handleChange);
  }, []);
  // No awareness of connection state
}
```

**Correct (robust connection handling):**

```javascript
// Monitor connection state
function useRealtimeConnection() {
  const [connected, setConnected] = useState(false);
  const [lastSync, setLastSync] = useState(null);

  useEffect(() => {
    // Track connection state
    const unsubConnect = pb.realtime.subscribe('PB_CONNECT', (e) => {
      console.log('Connected, client ID:', e.clientId);
      setConnected(true);

      // Re-sync data after reconnection
      if (lastSync) {
        syncMissedUpdates(lastSync);
      }
      setLastSync(new Date());
    });

    // Handle disconnection
    pb.realtime.onDisconnect = (activeSubscriptions) => {
      console.log('Disconnected');
      setConnected(false);
      showOfflineIndicator();
    };

    return () => {
      unsubConnect();
    };
  }, [lastSync]);

  return { connected };
}

// Sync missed updates after reconnection
async function syncMissedUpdates(since) {
  // Fetch records modified since last sync
  const updatedPosts = await pb.collection('posts').getList(1, 100, {
    filter: pb.filter('updated > {:since}', { since }),
    sort: '-updated'
  });

  // Merge with local state
  updateLocalState(updatedPosts.items);
}

// Full implementation with resilience
class RealtimeManager {
  constructor(pb) {
    this.pb = pb;
    this.subscriptions = new Map();
    this.lastSyncTimes = new Map();
    this.reconnectAttempts = 0;
    this.maxReconnectDelay = 30000;

    this.setupConnectionHandlers();
  }

  setupConnectionHandlers() {
    this.pb.realtime.subscribe('PB_CONNECT', () => {
      console.log('Realtime connected');
      this.reconnectAttempts = 0;
      this.onReconnect();
    });

    this.pb.realtime.onDisconnect = (subs) => {
      console.log('Realtime disconnected');
      this.scheduleReconnect();
    };
  }

  scheduleReconnect() {
    // Exponential backoff with jitter
    const delay = Math.min(
      1000 * Math.pow(2, this.reconnectAttempts) + Math.random() * 1000,
      this.maxReconnectDelay
    );

    this.reconnectAttempts++;

    setTimeout(() => {
      if (!this.pb.realtime.isConnected) {
        this.resubscribeAll();
      }
    }, delay);
  }

  async onReconnect() {
    // Sync data for each tracked collection
    for (const [collection, lastSync] of this.lastSyncTimes) {
      await this.syncCollection(collection, lastSync);
    }
  }

  async syncCollection(collection, since) {
    try {
      const updates = await this.pb.collection(collection).getList(1, 1000, {
        filter: this.pb.filter('updated > {:since}', { since }),
        sort: 'updated'
      });

      // Notify subscribers of missed updates
      const handler = this.subscriptions.get(collection);
      if (handler) {
        updates.items.forEach(record => {
          handler({ action: 'update', record });
        });
      }

      this.lastSyncTimes.set(collection, new Date());
    } catch (error) {
      console.error(`Failed to sync ${collection}:`, error);
    }
  }

  async subscribe(collection, handler) {
    this.subscriptions.set(collection, handler);
    this.lastSyncTimes.set(collection, new Date());

    return this.pb.collection(collection).subscribe('*', (e) => {
      this.lastSyncTimes.set(collection, new Date());
      handler(e);
    });
  }

  async resubscribeAll() {
    // Refresh auth token before resubscribing to ensure valid credentials
    if (this.pb.authStore.isValid) {
      try {
        await this.pb.collection('users').authRefresh();
      } catch {
        this.pb.authStore.clear();
      }
    }

    for (const [collection, handler] of this.subscriptions) {
      this.pb.collection(collection).subscribe('*', handler);
    }
  }
}

// Usage
const realtime = new RealtimeManager(pb);
await realtime.subscribe('posts', handlePostChange);
```

**Connection timeout handling:**

```javascript
// Server sends disconnect after 5 min of no messages
// SDK auto-reconnects, but you can handle it explicitly

let lastHeartbeat = Date.now();

pb.realtime.subscribe('PB_CONNECT', () => {
  lastHeartbeat = Date.now();
});

// Check for stale connection
setInterval(() => {
  if (Date.now() - lastHeartbeat > 6 * 60 * 1000) {
    console.log('Connection may be stale, refreshing...');
    pb.realtime.unsubscribe();
    resubscribeAll();
  }
}, 60000);
```

Reference: [PocketBase Realtime](https://pocketbase.io/docs/api-realtime/)

## 4. Implement Realtime Subscriptions Correctly

**Impact: MEDIUM (Live updates without polling, reduced server load)**

PocketBase uses Server-Sent Events (SSE) for realtime updates. Proper subscription management prevents memory leaks and ensures reliable event delivery.

**Incorrect (memory leaks and poor management):**

```javascript
// Missing unsubscribe - memory leak!
function PostList() {
  useEffect(() => {
    pb.collection('posts').subscribe('*', (e) => {
      updatePosts(e);
    });
    // No cleanup - subscription persists forever!
  }, []);
}

// Subscribing multiple times
function loadPosts() {
  // Called on every render - creates duplicate subscriptions!
  pb.collection('posts').subscribe('*', handleChange);
}

// Not handling reconnection
pb.collection('posts').subscribe('*', (e) => {
  // Assumes connection is always stable
  updateUI(e);
});
```

**Correct (proper subscription management):**

```javascript
// React example with cleanup
function PostList() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    // Initial load
    loadPosts();

    // Subscribe to changes
    const unsubscribe = pb.collection('posts').subscribe('*', (e) => {
      if (e.action === 'create') {
        setPosts(prev => [e.record, ...prev]);
      } else if (e.action === 'update') {
        setPosts(prev => prev.map(p =>
          p.id === e.record.id ? e.record : p
        ));
      } else if (e.action === 'delete') {
        setPosts(prev => prev.filter(p => p.id !== e.record.id));
      }
    });

    // Cleanup on unmount
    return () => {
      unsubscribe();
    };
  }, []);

  async function loadPosts() {
    const result = await pb.collection('posts').getList(1, 50);
    setPosts(result.items);
  }

  return <PostListUI posts={posts} />;
}

// Subscribe to specific record
async function watchPost(postId) {
  return pb.collection('posts').subscribe(postId, (e) => {
    console.log('Post changed:', e.action, e.record);
  });
}

// Subscribe to collection changes
async function watchAllPosts() {
  return pb.collection('posts').subscribe('*', (e) => {
    console.log(`Post ${e.action}:`, e.record.title);
  });
}

// Handle connection events
pb.realtime.subscribe('PB_CONNECT', (e) => {
  console.log('Realtime connected, client ID:', e.clientId);
  // Re-sync data after reconnection
  refreshData();
});

// Vanilla JS with proper cleanup
class PostManager {
  unsubscribes = [];

  async init() {
    this.unsubscribes.push(
      await pb.collection('posts').subscribe('*', this.handlePostChange)
    );
    this.unsubscribes.push(
      await pb.collection('comments').subscribe('*', this.handleCommentChange)
    );
  }

  destroy() {
    this.unsubscribes.forEach(unsub => unsub());
    this.unsubscribes = [];
  }

  handlePostChange = (e) => { /* ... */ };
  handleCommentChange = (e) => { /* ... */ };
}
```

**Subscription event structure:**

```javascript
pb.collection('posts').subscribe('*', (event) => {
  event.action;  // 'create' | 'update' | 'delete'
  event.record;  // The affected record
});

// Full event type
interface RealtimeEvent {
  action: 'create' | 'update' | 'delete';
  record: RecordModel;
}
```

**Unsubscribe patterns:**

```javascript
// Unsubscribe from specific callback
const unsub = await pb.collection('posts').subscribe('*', callback);
unsub();  // Remove this specific subscription

// Unsubscribe from all subscriptions on a topic
pb.collection('posts').unsubscribe('*');  // All collection subs
pb.collection('posts').unsubscribe('RECORD_ID');  // Specific record

// Unsubscribe from all collection subscriptions
pb.collection('posts').unsubscribe();

// Unsubscribe from everything
pb.realtime.unsubscribe();
```

**Performance considerations:**

```javascript
// Prefer specific record subscriptions over collection-wide when possible.
// subscribe('*') checks ListRule for every connected client on each change.
// subscribe(recordId) checks ViewRule -- fewer records to evaluate.

// For high-traffic collections, subscribe to specific records:
await pb.collection('orders').subscribe(orderId, handleOrderUpdate);
// Instead of: pb.collection('orders').subscribe('*', handleAllOrders);

// Use subscription options to reduce payload size (SDK v0.21+):
await pb.collection('posts').subscribe('*', handleChange, {
  fields: 'id,title,updated',  // Only receive specific fields
  expand: 'author',            // Include expanded relations
  filter: 'status = "published"'  // Only receive matching records
});
```

**Subscription scope guidelines:**

| Scenario | Recommended Scope |
|----------|-------------------|
| Watching a specific document | `subscribe(recordId)` |
| Chat room messages | `subscribe('*')` with filter for room |
| User notifications | `subscribe('*')` with filter for user |
| Admin dashboard | `subscribe('*')` (need to see all) |
| High-frequency data (IoT) | `subscribe(recordId)` per device |

Reference: [PocketBase Realtime](https://pocketbase.io/docs/api-realtime/)

