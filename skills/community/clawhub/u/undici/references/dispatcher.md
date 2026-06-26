# Dispatcher — Low-Level API

Dispatcher is the underlying implementation for all higher-level APIs. All requests ultimately execute via `Dispatcher.dispatch(options, handler)`.

## dispatch(options, handler)

```js
client.dispatch({
  path: '/',
  method: 'GET',
  headers: { 'x-foo': 'bar' }
}, {
  onRequestStart: (controller) => {},
  onResponseStart: (controller, statusCode, headers, statusMessage) => {},
  onResponseData: (controller, chunk) => {},
  onResponseEnd: (controller, trailers) => {},
  onResponseError: (controller, error) => {},
  onRequestUpgrade: (controller, statusCode, headers, socket) => {} // For CONNECT/Upgrade
});
```

## DispatchOptions

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `origin` | `string\|URL` | - | Request origin |
| `path` | `string` | - | Request path |
| `method` | `string` | - | HTTP method |
| `body` | `string\|Buffer\|Readable\|Iterable\|AsyncIterable\|null` | `null` | Request body |
| `headers` | `UndiciHeaders` | `null` | Request headers |
| `query` | `Record<string,any>` | `null` | Query parameters (auto encodeURIComponent) |
| `reset` | `boolean` | `false` | `true` = close connection after request |
| `idempotent` | `boolean` | `true` (GET/HEAD) | Whether safe to retry |
| `blocking` | `boolean` | `method!=='HEAD'` | Whether it blocks pipeline |
| `upgrade` | `string\|null` | `null` | Upgrade protocol (e.g., `'websocket'`) |
| `bodyTimeout` | `number\|null` | `300000` | Body receive timeout (ms), `0` disables |
| `headersTimeout` | `number\|null` | `300000` | Headers receive timeout (ms) |
| `expectContinue` | `boolean` | `false` | H2: send `expect: 100-continue` |

## DispatchHandler Callbacks

- `onRequestStart(controller, context)` — Before request is sent, can call `controller.abort(reason)`
- `onRequestUpgrade(controller, statusCode, headers, socket)` — Upgrade request callback
- `onResponseStart(controller, statusCode, headers, statusMessage?)` — Headers received (may fire multiple times due to 1xx)
- `onResponseData(controller, chunk: Buffer)` — Data chunk received
- `onResponseEnd(controller, trailers)` — Request completed
- `onResponseError(controller, error)` — Error occurred

Controller methods: `pause()` / `resume()` / `abort(reason)`

Controller properties: `rawHeaders` / `rawTrailers` (raw header arrays)

## Migration from Legacy API

- `onConnect(abort)` → `onRequestStart(controller)` + `controller.abort(reason)`
- `onHeaders(status, rawHeaders, resume, statusText)` → `onResponseStart(controller, status, headers, statusText)`
- `onData(chunk)` → `onResponseData(controller, chunk)`
- `onComplete(trailers)` → `onResponseEnd(controller, trailers)`
- `onError(err)` → `onResponseError(controller, err)`
- `onUpgrade(status, rawHeaders, socket)` → `onRequestUpgrade(controller, status, headers, socket)`
- `return false` to pause → `controller.pause()` + `controller.resume()`

## Dispatcher Global Storage

v2 handler uses `Symbol.for('undici.globalDispatcher.2')` to avoid conflicts with Node.js built-in fetch.

v1 compatibility: `setGlobalDispatcher()` also writes to `Symbol.for('undici.globalDispatcher.1')` via `Dispatcher1Wrapper`.