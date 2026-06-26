# Connection Management: Agent / Pool / Client

## Class Hierarchy

```
Dispatcher (abstract base class, extends EventEmitter)
├── Client        — Single origin, single connection
├── Pool          — Single origin, multiple connections + factory
├── Agent         — Multiple origins, automatic Pool factory
├── ProxyAgent    — Connect via proxy server
└── MockAgent     — Testing mock
```

## Client — Single Connection

```js
import { Client } from 'undici';
const client = new Client('http://localhost:3000', {
  // ClientOptions (no connections/pipelining)
  keepAliveTimeout: 4000,
  bodyTimeout: 300000,
  headersTimeout: 300000,
});
```

## Pool — Single Origin, Multiple Connections

```js
import { Pool } from 'undici';
const pool = new Pool('http://localhost:3000', {
  connections: 128,    // Maximum connections
  pipelining: 10,      // Pipelining depth per connection
  keepAliveTimeout: 4000,
  keepAliveMaxTimeout: 600000,
  factory: (origin, opts) => new Client(origin, opts), // Custom factory
});
```

## Agent — Multiple Origins

```js
import { Agent } from 'undici';
const agent = new Agent({
  connections: 128,
  pipelining: 10,
  maxOrigins: Infinity, // Maximum number of origins, throws MaxOriginsReachedError when exceeded
  factory: (origin, opts) => new Pool(origin, opts),
});
agent.stats(); // Returns Record<string, { connected, free, pending, queued }>
```

## Agent.compose() — Interceptor Composition

```js
const client = new Agent().compose(
  interceptors.redirect({ maxRedirections: 3 }),
  interceptors.retry({ maxRetries: 2 }),
  interceptors.cache({ store: new cacheStores.MemoryCacheStore() }),
);
```

## Lifecycle Methods

All Dispatcher subclasses support:

```js
await dispatcher.close();             // Graceful shutdown (waits for requests to complete)
await dispatcher.destroy();           // Immediate destruction
await dispatcher.destroy(new Error()); // Destroy with error, abort all ongoing requests
```

Properties:
- `dispatcher.closed` — Whether closed
- `dispatcher.destroyed` — Whether destroyed

## ProxyAgent — Proxy

```js
import { ProxyAgent } from 'undici';

new ProxyAgent('http://proxy:8080');
new ProxyAgent({
  uri: 'http://proxy:8080',
  token: 'Bearer xxx',       // Authentication token
  proxyTls: { /* TLS options */ },
  requestTls: { /* Request TLS options */ },
  proxyTunnel: false,        // Whether to tunnel non-secure connections
});
```

## MockAgent — Testing Mock

```js
import { MockAgent } from 'undici';

const mockAgent = new MockAgent({
  ignoreTrailingSlash: true,  // Ignore trailing slash matching
});
mockAgent.disableNetConnect(); // Disable real network (unmocked requests will error)
mockAgent.enableNetConnect();  // Re-enable
mockAgent.enableNetConnect('example.com'); // Allow only specific hosts

// Get mock for a specific origin:
const pool = mockAgent.get('http://localhost:3000');
// Matching methods: string (exact) / RegExp / (value) => boolean

pool.intercept({ path: '/api', method: 'GET' })
  .reply(200, { data: [] }, { headers: { 'x-custom': 'value' } })
  .delay(100); // Simulate delay (ms)

pool.intercept({ path: '/error' })
  .replyWithError(new Error('Network error'));
```