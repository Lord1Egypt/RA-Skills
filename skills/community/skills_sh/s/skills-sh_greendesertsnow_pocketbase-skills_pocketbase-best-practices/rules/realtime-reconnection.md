---
title: Handle Realtime Connection Issues
impact: MEDIUM
impactDescription: Reliable realtime even with network interruptions
tags: realtime, reconnection, resilience, offline
---

## Handle Realtime Connection Issues

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
