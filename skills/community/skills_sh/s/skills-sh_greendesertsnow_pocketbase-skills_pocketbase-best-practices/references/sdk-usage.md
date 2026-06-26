# SDK Usage

**Impact: HIGH**

JavaScript SDK initialization, auth store patterns, error handling, request cancellation, and safe parameter binding.

---

## 1. Use Appropriate Auth Store for Your Platform

**Impact: HIGH (Proper auth persistence across sessions and page reloads)**

The auth store persists authentication state. Choose the right store type based on your platform: LocalAuthStore for browsers, AsyncAuthStore for React Native, or custom stores for specific needs.

**Incorrect (wrong store for platform):**

```javascript
// React Native: LocalAuthStore doesn't work correctly
import PocketBase from 'pocketbase';
const pb = new PocketBase('http://127.0.0.1:8090');
// Auth state lost on app restart!

// Deno server: LocalStorage shared between all clients
import PocketBase from 'pocketbase';
const pb = new PocketBase('http://127.0.0.1:8090');
// All clients share the same auth state!

// Server-side: Reusing single client for multiple users
const pb = new PocketBase('http://127.0.0.1:8090');
// User A logs in...
// User B's request uses User A's auth!
```

**Correct (platform-appropriate stores):**

```javascript
// Browser (default LocalAuthStore - works automatically)
import PocketBase from 'pocketbase';
const pb = new PocketBase('http://127.0.0.1:8090');
// Automatically persists to localStorage and syncs between tabs

// React Native (AsyncAuthStore)
import PocketBase, { AsyncAuthStore } from 'pocketbase';
import AsyncStorage from '@react-native-async-storage/async-storage';

const store = new AsyncAuthStore({
  save: async (serialized) => {
    await AsyncStorage.setItem('pb_auth', serialized);
  },
  initial: AsyncStorage.getItem('pb_auth'),
  clear: async () => {
    await AsyncStorage.removeItem('pb_auth');
  }
});

const pb = new PocketBase('http://127.0.0.1:8090', store);

// Server-side / SSR (create client per request)
import PocketBase from 'pocketbase';

export function createServerClient(cookieHeader) {
  const pb = new PocketBase('http://127.0.0.1:8090');
  pb.authStore.loadFromCookie(cookieHeader || '');
  return pb;
}

// Deno/Cloudflare Workers (memory-only store)
import PocketBase, { BaseAuthStore } from 'pocketbase';

class MemoryAuthStore extends BaseAuthStore {
  // Token only persists for request duration
  // Each request must include auth via cookie/header
}

const pb = new PocketBase('http://127.0.0.1:8090', new MemoryAuthStore());
```

**Custom auth store example:**

```javascript
import PocketBase, { BaseAuthStore } from 'pocketbase';

class SecureAuthStore extends BaseAuthStore {
  constructor() {
    super();
    // Load initial state from secure storage
    const data = secureStorage.get('pb_auth');
    if (data) {
      const { token, record } = JSON.parse(data);
      this.save(token, record);
    }
  }

  save(token, record) {
    super.save(token, record);
    // Persist to secure storage
    secureStorage.set('pb_auth', JSON.stringify({ token, record }));
  }

  clear() {
    super.clear();
    secureStorage.remove('pb_auth');
  }
}

const pb = new PocketBase('http://127.0.0.1:8090', new SecureAuthStore());
```

**Auth store methods:**

```javascript
// Available on all auth stores
pb.authStore.token;        // Current token
pb.authStore.record;       // Current auth record
pb.authStore.isValid;      // Token exists and not expired
pb.authStore.isSuperuser;  // Is superuser token

pb.authStore.save(token, record);  // Save auth state
pb.authStore.clear();              // Clear auth state

// Listen for changes
const unsubscribe = pb.authStore.onChange((token, record) => {
  console.log('Auth changed:', record?.email);
}, true);  // true = fire immediately

// Cookie helpers (for SSR)
pb.authStore.loadFromCookie(cookieString);
pb.authStore.exportToCookie({ httpOnly: false, secure: true });
```

Reference: [PocketBase Authentication](https://pocketbase.io/docs/authentication/)

## 2. Understand and Control Auto-Cancellation

**Impact: MEDIUM (Prevents race conditions, improves UX for search/typeahead)**

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

## 3. Handle SDK Errors Properly

**Impact: HIGH (Graceful error recovery, better UX, easier debugging)**

All SDK methods return Promises that may reject with `ClientResponseError`. Proper error handling improves user experience and simplifies debugging.

**Incorrect (ignoring or poorly handling errors):**

```javascript
// No error handling
const posts = await pb.collection('posts').getList();

// Generic catch that loses information
try {
  await pb.collection('posts').create({ title: '' });
} catch (e) {
  alert('Something went wrong');  // No useful info
}

// Not checking specific error types
try {
  await pb.collection('posts').getOne('nonexistent');
} catch (e) {
  console.log(e.message);  // Missing status, response details
}
```

**Correct (comprehensive error handling):**

```javascript
import PocketBase, { ClientResponseError } from 'pocketbase';

const pb = new PocketBase('http://127.0.0.1:8090');

// Basic error handling with ClientResponseError
async function createPost(data) {
  try {
    return await pb.collection('posts').create(data);
  } catch (error) {
    if (error instanceof ClientResponseError) {
      console.log('Status:', error.status);
      console.log('Response:', error.response);
      console.log('URL:', error.url);
      console.log('Is abort:', error.isAbort);

      // Handle specific status codes
      switch (error.status) {
        case 400:
          // Validation error - extract user-friendly messages only
          // IMPORTANT: Don't expose raw error.response.data to clients
          // as it may leak internal field names and validation rules
          const fieldErrors = {};
          if (error.response?.data) {
            for (const [field, details] of Object.entries(error.response.data)) {
              fieldErrors[field] = details.message;
            }
          }
          return { error: 'validation', fields: fieldErrors };
        case 401:
          // Unauthorized - need to login
          return { error: 'unauthorized' };
        case 403:
          // Forbidden - no permission
          return { error: 'forbidden' };
        case 404:
          // Not found
          return { error: 'not_found' };
        default:
          return { error: 'server_error' };
      }
    }
    throw error;  // Re-throw non-PocketBase errors
  }
}

// Handle validation errors with field details
async function updateProfile(userId, data) {
  try {
    return await pb.collection('users').update(userId, data);
  } catch (error) {
    if (error.status === 400 && error.response?.data) {
      // Extract field-specific errors
      const fieldErrors = {};
      for (const [field, details] of Object.entries(error.response.data)) {
        fieldErrors[field] = details.message;
      }
      return { success: false, errors: fieldErrors };
      // { errors: { email: "Invalid email format", name: "Required field" } }
    }
    throw error;
  }
}

// Handle request cancellation
async function searchWithCancel(query) {
  try {
    return await pb.collection('posts').getList(1, 20, {
      filter: pb.filter('title ~ {:query}', { query })
    });
  } catch (error) {
    if (error.isAbort) {
      // Request was cancelled (e.g., user typed again)
      console.log('Search cancelled');
      return null;
    }
    throw error;
  }
}

// Wrapper function for consistent error handling
async function pbRequest(fn) {
  try {
    return { data: await fn(), error: null };
  } catch (error) {
    if (error instanceof ClientResponseError) {
      return {
        data: null,
        error: {
          status: error.status,
          message: error.response?.message || 'Request failed',
          data: error.response?.data || null
        }
      };
    }
    return {
      data: null,
      error: { status: 0, message: error.message, data: null }
    };
  }
}

// Usage
const { data, error } = await pbRequest(() =>
  pb.collection('posts').getList(1, 20)
);

if (error) {
  console.log('Failed:', error.message);
} else {
  console.log('Posts:', data.items);
}
```

**ClientResponseError structure:**

```typescript
interface ClientResponseError {
  url: string;           // The request URL
  status: number;        // HTTP status code (0 if network error)
  response: {            // API response body
    code: number;
    message: string;
    data: { [field: string]: { code: string; message: string } };
  };
  isAbort: boolean;      // True if request was cancelled
  cause: Error | null;   // Original error (added in JS SDK v0.26.1)
}
```

Reference: [PocketBase Error Handling](https://github.com/pocketbase/js-sdk#error-handling)

## 4. Use Field Modifiers for Incremental Updates

**Impact: HIGH (Atomic updates, prevents race conditions, cleaner code)**

PocketBase supports `+` and `-` modifiers for incrementing numbers, appending/removing relation IDs, and managing file arrays without replacing the entire value.

**Incorrect (read-modify-write pattern):**

```javascript
// Race condition: two users adding tags simultaneously
async function addTag(postId, newTagId) {
  const post = await pb.collection('posts').getOne(postId);
  const currentTags = post.tags || [];

  // Another user might have added a tag in between!
  await pb.collection('posts').update(postId, {
    tags: [...currentTags, newTagId]  // Might overwrite the other user's tag
  });
}

// Inefficient for incrementing counters
async function incrementViews(postId) {
  const post = await pb.collection('posts').getOne(postId);
  await pb.collection('posts').update(postId, {
    views: post.views + 1  // Extra read, race condition
  });
}
```

**Correct (using field modifiers):**

```javascript
// Atomic relation append with + modifier
async function addTag(postId, newTagId) {
  await pb.collection('posts').update(postId, {
    'tags+': newTagId  // Appends to existing tags atomically
  });
}

// Append multiple relations
async function addTags(postId, tagIds) {
  await pb.collection('posts').update(postId, {
    'tags+': tagIds  // Appends array of IDs
  });
}

// Prepend relations (+ prefix)
async function prependTag(postId, tagId) {
  await pb.collection('posts').update(postId, {
    '+tags': tagId  // Prepends to start of array
  });
}

// Remove relations with - modifier
async function removeTag(postId, tagId) {
  await pb.collection('posts').update(postId, {
    'tags-': tagId  // Removes specific tag
  });
}

// Remove multiple relations
async function removeTags(postId, tagIds) {
  await pb.collection('posts').update(postId, {
    'tags-': tagIds  // Removes all specified tags
  });
}

// Atomic number increment
async function incrementViews(postId) {
  await pb.collection('posts').update(postId, {
    'views+': 1  // Atomic increment, no race condition
  });
}

// Atomic number decrement
async function decrementStock(productId, quantity) {
  await pb.collection('products').update(productId, {
    'stock-': quantity  // Atomic decrement
  });
}

// File append (for multi-file fields)
async function addImage(albumId, newImage) {
  await pb.collection('albums').update(albumId, {
    'images+': newImage  // Appends new file to existing
  });
}

// File removal
async function removeImage(albumId, filename) {
  await pb.collection('albums').update(albumId, {
    'images-': filename  // Removes specific file by name
  });
}

// Combined modifiers in single update
async function updatePost(postId, data) {
  await pb.collection('posts').update(postId, {
    title: data.title,        // Replace field
    'views+': 1,              // Increment number
    'tags+': data.newTagId,   // Append relation
    'tags-': data.oldTagId,   // Remove relation
    'images+': data.newImage  // Append file
  });
}
```

**Modifier reference:**

| Modifier | Field Types | Description |
|----------|-------------|-------------|
| `field+` or `+field` | relation, file | Append/prepend to array |
| `field-` | relation, file | Remove from array |
| `field+` | number | Increment by value |
| `field-` | number | Decrement by value |

**Benefits:**
- **Atomic**: No read-modify-write race conditions
- **Efficient**: Single request, no extra read needed
- **Clean**: Expresses intent clearly

**Note:** Modifiers only work with `update()`, not `create()`.

Reference: [PocketBase Relations](https://pocketbase.io/docs/working-with-relations/)

## 5. Use Safe Parameter Binding in Filters

**Impact: CRITICAL (Prevents injection attacks, handles special characters correctly)**

Always use `pb.filter()` with parameter binding when constructing filters with user input. String concatenation is vulnerable to injection attacks.

**Incorrect (string concatenation - DANGEROUS):**

```javascript
// SQL/filter injection vulnerability!
async function searchPosts(userInput) {
  // User input: `test" || id != "` breaks out of string
  const posts = await pb.collection('posts').getList(1, 20, {
    filter: `title ~ "${userInput}"`  // VULNERABLE!
  });
  return posts;
}

// Even with escaping, easy to get wrong
async function searchByEmail(email) {
  const escaped = email.replace(/"/g, '\\"');  // Incomplete escaping
  const users = await pb.collection('users').getList(1, 1, {
    filter: `email = "${escaped}"`  // Still potentially vulnerable
  });
  return users;
}

// Template literals are just as dangerous
const filter = `status = "${status}" && author = "${authorId}"`;
```

**Correct (using pb.filter with parameters):**

```javascript
// Safe parameter binding
async function searchPosts(userInput) {
  const posts = await pb.collection('posts').getList(1, 20, {
    filter: pb.filter('title ~ {:search}', { search: userInput })
  });
  return posts;
}

// Multiple parameters
async function filterPosts(status, authorId, minViews) {
  const posts = await pb.collection('posts').getList(1, 20, {
    filter: pb.filter(
      'status = {:status} && author = {:author} && views >= {:views}',
      { status, author: authorId, views: minViews }
    )
  });
  return posts;
}

// Reusing parameters
async function searchBothFields(query) {
  const results = await pb.collection('posts').getList(1, 20, {
    filter: pb.filter(
      'title ~ {:q} || content ~ {:q}',
      { q: query }  // Same parameter used twice
    )
  });
  return results;
}

// Different parameter types
async function complexFilter(options) {
  const filter = pb.filter(
    'created > {:date} && active = {:active} && category = {:cat}',
    {
      date: new Date('2024-01-01'),  // Date objects handled correctly
      active: true,                    // Booleans
      cat: options.category            // Strings auto-escaped
    }
  );

  return pb.collection('posts').getList(1, 20, { filter });
}

// Null handling
async function filterWithOptional(category) {
  // Only include filter if value provided
  const filter = category
    ? pb.filter('category = {:cat}', { cat: category })
    : '';

  return pb.collection('posts').getList(1, 20, { filter });
}

// Building dynamic filters
async function dynamicSearch(filters) {
  const conditions = [];
  const params = {};

  if (filters.title) {
    conditions.push('title ~ {:title}');
    params.title = filters.title;
  }

  if (filters.author) {
    conditions.push('author = {:author}');
    params.author = filters.author;
  }

  if (filters.minDate) {
    conditions.push('created >= {:minDate}');
    params.minDate = filters.minDate;
  }

  const filter = conditions.length > 0
    ? pb.filter(conditions.join(' && '), params)
    : '';

  return pb.collection('posts').getList(1, 20, { filter });
}
```

**Supported parameter types:**

| Type | Example | Notes |
|------|---------|-------|
| string | `'hello'` | Auto-escaped, quotes handled |
| number | `123`, `45.67` | No quotes added |
| boolean | `true`, `false` | Converted correctly |
| Date | `new Date()` | Formatted for PocketBase |
| null | `null` | For null comparisons |
| other | `{...}` | JSON.stringify() applied |

**Server-side is especially critical:**

```javascript
// Server-side code (Node.js, Deno, etc.) MUST use binding
// because malicious users control the input directly

export async function searchHandler(req) {
  const userQuery = req.query.q;  // Untrusted input!

  // ALWAYS use pb.filter() on server
  const results = await pb.collection('posts').getList(1, 20, {
    filter: pb.filter('title ~ {:q}', { q: userQuery })
  });

  return results;
}
```

Reference: [PocketBase Filters](https://pocketbase.io/docs/api-rules-and-filters/)

## 6. Initialize PocketBase Client Correctly

**Impact: HIGH (Proper setup enables auth persistence, SSR support, and optimal performance)**

Client initialization should consider the environment (browser, Node.js, SSR), auth store persistence, and any required polyfills.

**Incorrect (environment-agnostic initialization):**

```javascript
// Missing polyfills in Node.js
import PocketBase from 'pocketbase';
const pb = new PocketBase('http://127.0.0.1:8090');

// Node.js: EventSource not defined error on realtime
pb.collection('posts').subscribe('*', callback);  // Fails!

// Missing base URL
const pb = new PocketBase();  // Uses '/' - likely wrong
```

**Correct (environment-aware initialization):**

```javascript
// Browser setup (no polyfills needed)
// IMPORTANT: Use HTTPS in production (http is only for local development)
import PocketBase from 'pocketbase';

const pb = new PocketBase('http://127.0.0.1:8090');  // Use https:// in production

// Node.js setup (requires polyfills for realtime)
import PocketBase from 'pocketbase';
import { EventSource } from 'eventsource';

// Global polyfill for realtime
global.EventSource = EventSource;

const pb = new PocketBase('http://127.0.0.1:8090');

// React Native setup (async auth store)
import PocketBase, { AsyncAuthStore } from 'pocketbase';
import AsyncStorage from '@react-native-async-storage/async-storage';
import EventSource from 'react-native-sse';

global.EventSource = EventSource;

const store = new AsyncAuthStore({
  save: async (serialized) => AsyncStorage.setItem('pb_auth', serialized),
  initial: AsyncStorage.getItem('pb_auth'),
});

const pb = new PocketBase('http://127.0.0.1:8090', store);
```

**SSR initialization (per-request client):**

```javascript
// SvelteKit example
// src/hooks.server.js
import PocketBase from 'pocketbase';

export async function handle({ event, resolve }) {
  // Create fresh client for each request
  event.locals.pb = new PocketBase('http://127.0.0.1:8090');

  // Load auth from request cookie
  event.locals.pb.authStore.loadFromCookie(
    event.request.headers.get('cookie') || ''
  );

  // Validate token
  if (event.locals.pb.authStore.isValid) {
    try {
      await event.locals.pb.collection('users').authRefresh();
    } catch {
      event.locals.pb.authStore.clear();
    }
  }

  const response = await resolve(event);

  // Send updated auth cookie with secure options
  response.headers.append(
    'set-cookie',
    event.locals.pb.authStore.exportToCookie({
      httpOnly: true,   // Prevent XSS access to auth token
      secure: true,     // HTTPS only
      sameSite: 'Lax',  // CSRF protection
    })
  );

  return response;
}
```

**TypeScript with typed collections:**

```typescript
import PocketBase, { RecordService } from 'pocketbase';

// Define your record types
interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
}

interface Post {
  id: string;
  title: string;
  content: string;
  author: string;
  published: boolean;
}

// Create typed client interface
interface TypedPocketBase extends PocketBase {
  collection(idOrName: string): RecordService;
  collection(idOrName: 'users'): RecordService<User>;
  collection(idOrName: 'posts'): RecordService<Post>;
}

const pb = new PocketBase('http://127.0.0.1:8090') as TypedPocketBase;

// Now methods are typed
const post = await pb.collection('posts').getOne('abc');  // Returns Post
const users = await pb.collection('users').getList();      // Returns ListResult<User>
```

Reference: [PocketBase JS SDK](https://github.com/pocketbase/js-sdk)

## 7. Use Send Hooks for Request Customization

**Impact: MEDIUM (Custom headers, logging, response transformation)**

The SDK provides `beforeSend` and `afterSend` hooks for intercepting and modifying requests and responses globally.

**Incorrect (repeating logic in every request):**

```javascript
// Adding headers to every request manually
const posts = await pb.collection('posts').getList(1, 20, {
  headers: { 'X-Custom-Header': 'value' }
});

const users = await pb.collection('users').getList(1, 20, {
  headers: { 'X-Custom-Header': 'value' }  // Repeated!
});

// Logging each request manually
console.log('Fetching posts...');
const posts = await pb.collection('posts').getList();
console.log('Done');
```

**Correct (using send hooks):**

```javascript
import PocketBase from 'pocketbase';

const pb = new PocketBase('http://127.0.0.1:8090');

// beforeSend - modify requests before they're sent
pb.beforeSend = function(url, options) {
  // Add custom headers to all requests
  options.headers = Object.assign({}, options.headers, {
    'X-Custom-Header': 'value',
    'X-Request-ID': crypto.randomUUID()
  });

  // Log outgoing requests
  console.log(`[${options.method}] ${url}`);

  // Must return { url, options }
  return { url, options };
};

// afterSend - process responses
pb.afterSend = function(response, data) {
  // Log response status
  console.log(`Response: ${response.status}`);

  // Transform or extend response data
  if (data && typeof data === 'object') {
    data._fetchedAt = new Date().toISOString();
  }

  // Return the (possibly modified) data
  return data;
};

// All requests now automatically have headers and logging
const posts = await pb.collection('posts').getList();
const users = await pb.collection('users').getList();
```

**Practical examples:**

```javascript
// Request timing / performance monitoring
let requestStart;
pb.beforeSend = function(url, options) {
  requestStart = performance.now();
  return { url, options };
};

pb.afterSend = function(response, data) {
  const duration = performance.now() - requestStart;
  console.log(`${response.url}: ${duration.toFixed(2)}ms`);

  // Send to analytics
  trackApiPerformance(response.url, duration);

  return data;
};

// Add auth token from different source
pb.beforeSend = function(url, options) {
  const externalToken = getTokenFromExternalAuth();
  if (externalToken) {
    options.headers = Object.assign({}, options.headers, {
      'X-External-Auth': externalToken
    });
  }
  return { url, options };
};

// Handle specific response codes globally
pb.afterSend = function(response, data) {
  if (response.status === 401) {
    // Token expired - trigger re-auth
    handleAuthExpired();
  }

  if (response.status === 503) {
    // Service unavailable - show maintenance message
    showMaintenanceMode();
  }

  return data;
};

// Retry failed requests (simplified example)
const originalSend = pb.send.bind(pb);
pb.send = async function(path, options) {
  try {
    return await originalSend(path, options);
  } catch (error) {
    if (error.status === 429) {  // Rate limited
      await sleep(1000);
      return originalSend(path, options);  // Retry once
    }
    throw error;
  }
};

// Add request correlation for debugging
let requestId = 0;
pb.beforeSend = function(url, options) {
  requestId++;
  const correlationId = `req-${Date.now()}-${requestId}`;

  options.headers = Object.assign({}, options.headers, {
    'X-Correlation-ID': correlationId
  });

  console.log(`[${correlationId}] Starting: ${url}`);
  return { url, options };
};

pb.afterSend = function(response, data) {
  console.log(`Complete: ${response.status}`);
  return data;
};
```

**Hook signatures:**

```typescript
// beforeSend
beforeSend?: (
  url: string,
  options: SendOptions
) => { url: string; options: SendOptions } | Promise<{ url: string; options: SendOptions }>;

// afterSend
afterSend?: (
  response: Response,
  data: any
) => any | Promise<any>;
```

**Use cases:**
- Add custom headers (API keys, correlation IDs)
- Request/response logging
- Performance monitoring
- Global error handling
- Response transformation
- Authentication middleware

Reference: [PocketBase Send Hooks](https://github.com/pocketbase/js-sdk#send-hooks)

