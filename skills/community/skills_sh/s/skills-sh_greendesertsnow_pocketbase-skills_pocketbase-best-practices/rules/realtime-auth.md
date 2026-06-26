---
title: Authenticate Realtime Connections
impact: MEDIUM
impactDescription: Secure subscriptions respecting API rules
tags: realtime, authentication, security, subscriptions
---

## Authenticate Realtime Connections

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
