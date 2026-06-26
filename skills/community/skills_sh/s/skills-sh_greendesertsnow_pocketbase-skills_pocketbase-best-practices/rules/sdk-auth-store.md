---
title: Use Appropriate Auth Store for Your Platform
impact: HIGH
impactDescription: Proper auth persistence across sessions and page reloads
tags: sdk, auth-store, persistence, storage
---

## Use Appropriate Auth Store for Your Platform

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
