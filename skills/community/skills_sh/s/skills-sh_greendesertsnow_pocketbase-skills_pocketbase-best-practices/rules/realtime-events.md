---
title: Handle Realtime Events Properly
impact: MEDIUM
impactDescription: Consistent UI state, proper optimistic updates
tags: realtime, events, state-management, ui
---

## Handle Realtime Events Properly

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
