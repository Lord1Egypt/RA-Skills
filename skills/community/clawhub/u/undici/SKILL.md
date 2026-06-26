---
name: undici
description: Use undici for HTTP requests, fetch, connection pooling, proxies, Mock testing, interceptors, caching. Note that undici's fetch differs from built-in fetch (no CORS, must consume body).
---

# undici

Node.js HTTP/1.1 client, written from scratch. The underlying engine for the built-in `fetch()` in Node.js v18+. Current version 8.x, ESM/CJS dual mode.

> Name meaning: Italian for "eleven" — 1.1 → 11 → Eleven → Undici (also a Stranger Things reference)

## Trigger Scenarios

Use when the user needs HTTP requests, undici, fetch, proxied requests, or HTTP mocking.

## Installation

```bash
npm i undici
```

## Performance Hierarchy

```
undici.dispatch()  >  undici.request()  >  undici.stream()
>  undici.pipeline()  >  undici.fetch()  >>  node:http
```

Approximately 3-4x faster than axios (50 TCP connections, pipelining depth 10).

## Core Usage

### `request()` — Highest-level API, best performance

```js
import { request } from 'undici';

const { statusCode, headers, body } = await request('http://localhost:3000/foo');
console.log(statusCode);               // 200
console.log(await body.json());        // Parse JSON

// body is a web ReadableStream, can also be read in chunks:
for await (const chunk of body) {
  console.log('chunk', chunk);
}

// ⚠️ Must consume body! Otherwise connection leaks
await body.dump(); // or .json() / .text() / for await
```

### `fetch()` — Standard Web API compatible

```js
import { fetch } from 'undici';

const res = await fetch('https://example.com');
const json = await res.json();

// With custom Agent
import { Agent } from 'undici';
const res = await fetch('https://example.com', {
  dispatcher: new Agent({ keepAliveTimeout: 10000 })
});
```

### `stream()` — Stream processing

```js
import { stream } from 'undici';
await stream('http://localhost:3000/foo', { method: 'GET' }, ({ statusCode, headers }) => {
  return new Writable({ write(chunk, _, cb) { console.log(chunk.toString()); cb(); } });
});
```

### `pipeline()` — Returns a Duplex stream

```js
import { pipeline } from 'undici';
import { Writable, Readable } from 'node:stream';

const duplex = pipeline('http://localhost:3000/foo', { method: 'POST' },
  ({ statusCode, headers }) => new Writable({ /* ... */ })
);
Readable.from(['data']).pipe(duplex);
```

## Agent — Connection Pool Management

Agent manages connections to multiple origins, automatically reusing them:

```js
import { Agent, setGlobalDispatcher, request } from 'undici';

const agent = new Agent({
  connections: 128,         // Max connections per origin
  pipelining: 10,           // Max pipelining depth per connection
  keepAliveTimeout: 4000,   // keep-alive timeout (ms)
  keepAliveMaxTimeout: 600000,
  bodyTimeout: 300000,
  headersTimeout: 300000,
});

setGlobalDispatcher(agent); // Set as global dispatcher
const data = await request('http://example.com');
```

## Built-in vs undici Module

| Aspect | Built-in `fetch()` (v18+) | `undici` Module |
|--------|---------------------------|-----------------|
| Dependencies | Zero dependencies | Requires installation |
| Version | Bundled with Node.js | Latest version |
| Performance | High (has Web Streams overhead) | `request()` is fastest |
| API | Only fetch | request/stream/pipeline/dispatch |
| Advanced features | ❌ | ✅ Agent/ProxyAgent/MockAgent/Interceptors |
| Error types | TypeError wrappers | More explicit error messages |

## FormData Consistency

⚠️ fetch and FormData must come from the same source:

```js
// ✅ Correct: Use undici exclusively
import { fetch, FormData } from 'undici';
const body = new FormData();
body.set('name', 'value');
await fetch(url, { method: 'POST', body });

// ✅ Or call install() to replace globals
import { install } from 'undici';
install(); // After this, global fetch/FormData/WebSocket/EventSource are from undici
```

## ProxyAgent — Proxy

```js
import { ProxyAgent, request, fetch } from 'undici';

const proxyAgent = new ProxyAgent('http://proxy:8080');
// Or with authentication:
const proxyAgent = new ProxyAgent({
  uri: 'http://proxy:8080',
  token: `Basic ${Buffer.from('user:pass').toString('base64')}`
});

// Set as global
setGlobalDispatcher(proxyAgent);
// Or use locally
await fetch('http://example.com', { dispatcher: proxyAgent });
```

## MockAgent — Testing Mock

```js
import { MockAgent, setGlobalDispatcher, request } from 'undici';

const mockAgent = new MockAgent();
setGlobalDispatcher(mockAgent);

const mockPool = mockAgent.get('http://localhost:3000');
mockPool.intercept({ path: '/foo', method: 'GET' }).reply(200, { ok: true });

const { body } = await request('http://localhost:3000/foo');
console.log(await body.json()); // { ok: true }
```

## Cache Interceptor

```js
import { Agent, interceptors, cacheStores, setGlobalDispatcher } from 'undici';

const client = new Agent().compose(interceptors.cache({
  store: new cacheStores.MemoryCacheStore({
    maxSize: 100 * 1024 * 1024, // 100MB
  }),
  methods: ['GET', 'HEAD']
}));
setGlobalDispatcher(client);
```

## Important Considerations

### Must Consume Response Body

```js
// ✅ Do
const { body } = await request(url);
await body.json(); // or .text() / .dump() / for await

// ❌ Don't — causes connection leaks
const { headers } = await request(url);

// ✅ Use HEAD method when only headers are needed
const headers = await fetch(url, { method: 'HEAD' }).then(r => r.headers);
```

### No CORS

undici does not implement browser CORS. No preflight is needed in server environments. If CORS protection is required, you must implement it yourself.

### body mixin can only be called once

Calling `.text()` after `.json()` will throw `TypeError: unusable`.

### Path Separators

Always use `/`. `\` is not supported as a path separator.

## Reference Documentation

- Low-level Dispatcher API (dispatch/handler) → `references/dispatcher.md`
- Agent/Pool/Client connection management → `references/connection.md`