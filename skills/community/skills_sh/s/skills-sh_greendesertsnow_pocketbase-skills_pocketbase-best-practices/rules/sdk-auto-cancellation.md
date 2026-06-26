---
title: Understand and Control Auto-Cancellation
impact: MEDIUM
impactDescription: Prevents race conditions, improves UX for search/typeahead
tags: sdk, cancellation, requests, performance
---

## Understand and Control Auto-Cancellation

The SDK automatically cancels duplicate pending requests. This prevents race conditions but requires understanding for proper use in concurrent scenarios.

**Incorrect (confused by auto-cancellation):**

```javascript
// These requests will interfere with each other!
async function loadDashboard() {
  // Only the last one executes, others cancelled
  const posts = pb.collection('posts').getList(1, 20);
  const users = pb.collection('posts').getList(1, 10);  // Different params but same path
  const comments = pb.collection('posts').getList(1, 5);

  // posts and users are cancelled, only comments executes
  return Promise.all([posts, users, comments]);  // First two fail!
}

// Realtime combined with polling causes cancellation
pb.collection('posts').subscribe('*', callback);
setInterval(() => {
  pb.collection('posts').getList();  // May cancel realtime!
}, 5000);
```

**Correct (controlling auto-cancellation):**

```javascript
// Disable auto-cancellation for parallel requests
async function loadDashboard() {
  const [posts, users, recent] = await Promise.all([
    pb.collection('posts').getList(1, 20, { requestKey: null }),
    pb.collection('users').getList(1, 10, { requestKey: null }),
    pb.collection('posts').getList(1, 5, { requestKey: 'recent' })
  ]);
  // All requests complete independently
  return { posts, users, recent };
}

// Use unique request keys for different purposes
async function searchPosts(query) {
  return pb.collection('posts').getList(1, 20, {
    filter: pb.filter('title ~ {:q}', { q: query }),
    requestKey: 'post-search'  // Cancels previous searches only
  });
}

async function loadPostDetails(postId) {
  return pb.collection('posts').getOne(postId, {
    requestKey: `post-${postId}`  // Unique per post
  });
}

// Typeahead search - auto-cancellation is helpful here
async function typeaheadSearch(query) {
  // Previous search automatically cancelled when user types more
  return pb.collection('products').getList(1, 10, {
    filter: pb.filter('name ~ {:q}', { q: query })
    // No requestKey = uses default (path-based), previous cancelled
  });
}

// Globally disable auto-cancellation (use carefully)
pb.autoCancellation(false);

// Now all requests are independent
await Promise.all([
  pb.collection('posts').getList(1, 20),
  pb.collection('posts').getList(1, 10),
  pb.collection('posts').getList(1, 5)
]);

// Re-enable
pb.autoCancellation(true);
```

**Manual cancellation:**

```javascript
// Cancel all pending requests
pb.cancelAllRequests();

// Cancel specific request by key
pb.cancelRequest('post-search');

// Example: Cancel on component unmount
function PostList() {
  useEffect(() => {
    loadPosts();

    return () => {
      // Cleanup: cancel pending requests
      pb.cancelRequest('post-list');
    };
  }, []);

  async function loadPosts() {
    const result = await pb.collection('posts').getList(1, 20, {
      requestKey: 'post-list'
    });
    setPosts(result.items);
  }
}

// Handle cancellation in catch
async function fetchWithCancellation() {
  try {
    return await pb.collection('posts').getList();
  } catch (error) {
    if (error.isAbort) {
      // Request was cancelled - this is expected
      console.log('Request cancelled');
      return null;
    }
    throw error;
  }
}
```

**When to use each approach:**

| Scenario | Approach |
|----------|----------|
| Search/typeahead | Default (let it cancel) |
| Parallel data loading | `requestKey: null` |
| Grouped requests | Custom `requestKey` |
| Component cleanup | `cancelRequest(key)` |
| Testing/debugging | `autoCancellation(false)` |
| OAuth2 flow cancel | `cancelRequest(requestKey)` — properly rejects the `authWithOAuth2()` Promise (JS SDK v0.26.8+) |

> **Note (JS SDK v0.26.8):** Calling `pb.cancelRequest(requestKey)` while `authWithOAuth2()` is waiting now properly rejects the returned Promise. In earlier versions the manual cancellation did not account for the waiting realtime subscription, so the Promise could hang indefinitely.

Reference: [PocketBase Auto-Cancellation](https://github.com/pocketbase/js-sdk#auto-cancellation)
