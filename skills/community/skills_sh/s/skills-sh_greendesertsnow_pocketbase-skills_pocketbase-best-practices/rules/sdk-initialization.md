---
title: Initialize PocketBase Client Correctly
impact: HIGH
impactDescription: Proper setup enables auth persistence, SSR support, and optimal performance
tags: sdk, initialization, client, setup
---

## Initialize PocketBase Client Correctly

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
