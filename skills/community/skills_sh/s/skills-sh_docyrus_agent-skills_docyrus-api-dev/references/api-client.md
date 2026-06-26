# @docyrus/api-client Reference

## Table of Contents

1. [RestApiClient](#restapiclient)
2. [HTTP Methods](#http-methods)
3. [Configuration](#configuration)
4. [Token Management](#token-management)
5. [OAuth2Client](#oauth2client)
6. [Interceptors](#interceptors)
7. [Error Handling](#error-handling)
8. [Streaming](#streaming)
9. [File Operations](#file-operations)
10. [Utilities](#utilities)

---

## RestApiClient

```typescript
import { RestApiClient, MemoryTokenManager } from '@docyrus/api-client'

const client = new RestApiClient({
  baseURL: 'https://api.docyrus.com',
  tokenManager: new MemoryTokenManager(),
  timeout: 5000,
  headers: { 'X-API-Version': '1.0' },
})
```

---

## HTTP Methods

```typescript
// GET with query params
const users = await client.get<User[]>('/v1/users', { params: { page: 1, limit: 10 } })

// POST with body
const newUser = await client.post<User>('/v1/users', { name: 'John', email: 'john@example.com' })

// PATCH (partial update)
const updated = await client.patch<User>('/v1/users/123', { name: 'Jane' })

// PUT (full replace)
await client.put('/v1/users/123', { name: 'Jane', email: 'jane@example.com' })

// DELETE
await client.delete('/v1/users/123')

// DELETE with body
await client.delete('/v1/items', { recordIds: ['id1', 'id2'] })
```

### Typed Responses

```typescript
interface ApiResponse<T> { data: T; meta: { page: number; total: number } }
const response = await client.get<ApiResponse<User[]>>('/v1/users')
const users: User[] = response.data.data
```

---

## Configuration

```typescript
interface ApiClientConfig {
  baseURL?: string                      // Base URL for all requests
  tokenManager?: TokenManager           // Token manager instance
  headers?: Record<string, string>      // Default headers
  timeout?: number                      // Request timeout in ms
  fetch?: typeof fetch                  // Custom fetch implementation
  FormData?: typeof FormData            // Custom FormData
  AbortController?: typeof AbortController
  storage?: Storage                     // Browser storage for persistence
}
```

---

## Token Management

### MemoryTokenManager (default)
```typescript
import { MemoryTokenManager } from '@docyrus/api-client'
const tokenManager = new MemoryTokenManager()
```

### StorageTokenManager (persistent)
```typescript
import { StorageTokenManager } from '@docyrus/api-client'
const tokenManager = new StorageTokenManager(localStorage, 'auth_token')
```

### AsyncTokenManager (custom)
```typescript
import { AsyncTokenManager } from '@docyrus/api-client'
const tokenManager = new AsyncTokenManager({
  async getToken() { return await secureStorage.get('token') },
  async setToken(token) { await secureStorage.set('token', token) },
  async clearToken() { await secureStorage.remove('token') },
})
```

### Set Token Directly
```typescript
await client.setAccessToken('your-auth-token')
```

---

## OAuth2Client

Full OAuth2 support with PKCE, Device Code, and Client Credentials flows.

### Setup
```typescript
import { OAuth2Client, BrowserOAuth2TokenStorage } from '@docyrus/api-client'

const oauth2 = new OAuth2Client({
  baseURL: 'https://api.docyrus.com',
  clientId: 'your-client-id',
  clientSecret: 'your-client-secret',    // optional for public clients
  redirectUri: 'http://localhost:3000/callback',
  defaultScopes: ['openid', 'offline_access'],
  usePKCE: true,                          // default: true
  tokenStorage: new BrowserOAuth2TokenStorage(localStorage),
})
```

### Authorization Code Flow (PKCE)
```typescript
// Step 1: Generate auth URL
const { url, state, codeVerifier } = await oauth2.getAuthorizationUrl({
  scope: 'openid offline_access Users.Read',
})

// Step 2: Redirect user
window.location.href = url

// Step 3: Handle callback
const tokens = await oauth2.handleCallback(window.location.href)
// tokens: { accessToken, refreshToken, ... }
```

### Client Credentials Flow (server-to-server)
```typescript
const tokens = await oauth2.getClientCredentialsToken({
  scope: 'Read.All',
  delegatedUserId: 'user-id-to-impersonate',
})
```

### Device Code Flow (CLI/headless)
```typescript
const deviceAuth = await oauth2.startDeviceAuthorization('openid offline_access')
console.log(`Go to: ${deviceAuth.verification_uri}`)
console.log(`Enter code: ${deviceAuth.user_code}`)

const tokens = await oauth2.pollDeviceAuthorization(
  deviceAuth.device_code, deviceAuth.interval, deviceAuth.expires_in,
  { onExpired: () => console.log('Code expired'), signal: abortController.signal },
)
```

### Token Operations
```typescript
const tokens = await oauth2.getTokens()
const isExpired = await oauth2.isTokenExpired()
const accessToken = await oauth2.getValidAccessToken()  // auto-refreshes
const newTokens = await oauth2.refreshAccessToken()
await oauth2.revokeToken(tokens.refreshToken)
const tokenInfo = await oauth2.introspectToken(tokens.accessToken)
await oauth2.logout()
```

### Integrate OAuth2 with RestApiClient
```typescript
import { RestApiClient, OAuth2Client, OAuth2TokenManagerAdapter, BrowserOAuth2TokenStorage } from '@docyrus/api-client'

const tokenStorage = new BrowserOAuth2TokenStorage(localStorage)
const oauth2 = new OAuth2Client({ baseURL: 'https://api.docyrus.com', clientId: 'id', tokenStorage })

const tokenManager = new OAuth2TokenManagerAdapter(tokenStorage, async () => {
  const tokens = await oauth2.refreshAccessToken()
  return tokens.accessToken
})

const apiClient = new RestApiClient({ baseURL: 'https://api.docyrus.com', tokenManager })
```

### Rate Limit Check
```typescript
const rateLimit = await oauth2.checkRateLimit()
// { remaining, limit, reset }
```

### PKCE Utilities
```typescript
import { generatePKCEChallenge, generateCodeVerifier, generateCodeChallenge, generateState, generateNonce } from '@docyrus/api-client'

const pkce = await generatePKCEChallenge()
// { codeVerifier, codeChallenge, codeChallengeMethod: 'S256' }
```

---

## Interceptors

```typescript
client.use({
  // Transform outgoing requests
  async request(config) {
    config.headers = { ...config.headers, 'X-Request-Time': new Date().toISOString() }
    return config
  },
  // Transform incoming responses
  async response(response, request) {
    console.log(`${request.url} took ${Date.now() - request.timestamp}ms`)
    return response
  },
  // Handle errors globally
  async error(error, request, response) {
    if (error.status === 401) { await refreshToken() }
    return { error, request, response }
  },
})
```

### Common Interceptor: Unwrap Response Data
```typescript
client.use({
  response: (response) => {
    if (response.data?.data && typeof response.data === 'object' && !Array.isArray(response.data)) {
      response.data = response.data.data
    }
    return response
  },
})
```

---

## Error Handling

```typescript
import {
  ApiError, NetworkError, TimeoutError,
  AuthenticationError,   // 401
  AuthorizationError,    // 403
  NotFoundError,         // 404
  RateLimitError,        // 429 — has error.retryAfter
  ValidationError,
  // OAuth2-specific
  OAuth2Error, InvalidGrantError, InvalidClientError,
  AccessDeniedError, ExpiredTokenError, AuthorizationPendingError,
} from '@docyrus/api-client'

try {
  await client.get('/resource')
} catch (error) {
  if (error instanceof AuthenticationError) { /* re-login */ }
  else if (error instanceof AuthorizationError) { /* forbidden */ }
  else if (error instanceof NotFoundError) { /* 404 */ }
  else if (error instanceof RateLimitError) { /* retry after error.retryAfter */ }
  else if (error instanceof NetworkError) { /* offline */ }
  else if (error instanceof TimeoutError) { /* timed out */ }
}
```

---

## Streaming

### Server-Sent Events (SSE)
```typescript
const eventSource = client.sse('/events', {
  onMessage(data) { console.log('Received:', data) },
  onError(error) { console.error(error) },
  onComplete() { console.log('Stream completed') },
})
eventSource.close()
```

### Chunked Streaming
```typescript
for await (const chunk of client.stream('/stream', {
  method: 'POST',
  body: { query: 'stream data' },
})) {
  console.log('Chunk:', chunk)
}
```

---

## File Operations

### Upload
```typescript
const formData = new FormData()
formData.append('file', fileInput.files[0])
formData.append('description', 'My file')
await client.post('/upload', formData)
```

### Download
```typescript
const response = await client.get('/download/file.pdf', { responseType: 'blob' })
const url = URL.createObjectURL(response.data)
const link = document.createElement('a')
link.href = url
link.download = 'file.pdf'
link.click()
```

### HTML to PDF
```typescript
await client.html2pdf({
  html: '<html><body>Content</body></html>',
  // or: url: 'https://example.com',
  options: { format: 'A4', margin: { top: 10, bottom: 10, left: 10, right: 10 }, landscape: false },
})
```

### Custom Query/Report
```typescript
const results = await client.runCustomQuery(customQueryId, options)
// PUT reports/runCustomQuery/:customQueryId
```

---

## Utilities

```typescript
import { buildUrl, isAbortError, parseContentDisposition, createAbortSignal, jsonToQueryString, withRetry } from '@docyrus/api-client'

const url = buildUrl('/api/users', { page: 1, limit: 10 })
// '/api/users?page=1&limit=10'

const signal = createAbortSignal(5000) // 5s timeout

const response = await withRetry(() => client.get('/flaky'), {
  retries: 3, retryDelay: 1000,
  retryCondition: (error) => error.status >= 500,
})
```
