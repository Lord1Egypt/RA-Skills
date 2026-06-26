---
title: Implement Realtime Subscriptions Correctly
impact: MEDIUM
impactDescription: Live updates without polling, reduced server load
tags: realtime, subscriptions, sse, websocket
---

## Implement Realtime Subscriptions Correctly

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
