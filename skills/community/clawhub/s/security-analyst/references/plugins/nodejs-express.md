---
name: Node.js + Express
detect:
  files: []
  dependencies: ["express", "koa", "fastify", "hapi"]
  keywords: ["Express", "Node.js"]
---

## attack-surface-http

**Middleware Ordering Vulnerabilities:**
1. Express middleware executes in registration order — auth middleware MUST come before route handlers
   - Read the main app setup file (typically `app.ts`, `index.ts`, `server.ts`)
   - Is auth middleware registered globally via `app.use()` BEFORE routes?
   - Are there routes registered before the auth middleware that should be protected?
   - Can route-specific middleware be bypassed by hitting a different path that maps to the same handler?

2. **Body Parser Configuration:**
   - Is `express.json()` configured with a `limit` option? (default is 100kb — may be too generous)
   - Is `express.urlencoded({ extended: true })` used? The `extended: true` option uses `qs` library which can be vulnerable to prototype pollution
   - Are there endpoints that accept `express.raw()` or `express.text()` without size limits?
   - Is body parsing applied globally or per-route? (global parsing wastes resources on routes that don't need it)

3. **Prototype Pollution:**
   - Does the app use `qs` for query string parsing (default with `extended: true`)?
   - Can an attacker send `?__proto__[isAdmin]=true` or `?constructor[prototype][isAdmin]=true`?
   - Are `Object.assign()`, spread operators, or deep merge utilities used on user input without prototype pollution protection?
   - Grep for `merge`, `extend`, `assign`, `defaults` with user-controlled objects

4. **`req.ip` Trust Proxy Misconfiguration:**
   - Is `trust proxy` configured? (`app.set('trust proxy', ...)`)
   - If `trust proxy` is `true` (trust all), an attacker behind ANY proxy can spoof IP via `X-Forwarded-For`
   - Are rate limiters or IP-based access controls using `req.ip`? (these are bypassable with spoofed headers if trust proxy is misconfigured)

5. **Path Traversal via `res.sendFile`:**
   - Grep for `res.sendFile`, `res.download`, `res.attachment`
   - Is the file path constructed from user input? (e.g., `res.sendFile(path.join(dir, req.params.filename))`)
   - Is `path.resolve()` or `path.join()` used without validating the result stays within the intended directory?
   - Is the `root` option set in `res.sendFile()` to restrict the base directory?

6. **Route Parameter Pollution:**
   - Express allows duplicate query parameters — `?id=1&id=2` results in `req.query.id` being an array `['1', '2']`
   - Can this break validation logic that expects a string? (e.g., `if (req.query.id === '1')` fails when id is an array)
   - Are there handlers that pass `req.query` or `req.body` directly to database queries without type checking?

## config-infrastructure

**Helmet.js Security Headers:**
1. Is Helmet.js installed and configured? (Grep for `helmet`, `require('helmet')`, `import helmet`)
   - If not installed: all security headers must be set manually — check for CSP, HSTS, X-Frame-Options, etc.
   - If installed: is it configured with defaults or customized? Check for:
     - `contentSecurityPolicy: false` (disables CSP entirely)
     - `crossOriginEmbedderPolicy: false` (weaker isolation)
     - Custom CSP with `unsafe-inline` or `unsafe-eval`

**Session Security:**
2. Which session library is used? (`express-session`, `cookie-session`, `connect-redis`, custom JWT)
   - `express-session`: Is `secret` strong and from environment? Is `cookie.secure` true in production? Is `cookie.httpOnly` true? Is `cookie.sameSite` set?
   - `cookie-session`: Is the session data small enough? (cookie-session stores ALL data in the cookie — large sessions can exceed cookie size limits)
   - Is session storage using a persistent store in production? (default `MemoryStore` leaks memory and doesn't scale)
   - Are session IDs regenerated after login? (`req.session.regenerate()`)

**CORS Configuration:**
3. Read CORS middleware configuration (Grep for `cors(`, `cors({`)
   - Is `origin` set to `*`? (allows any origin — bad for authenticated endpoints)
   - Is `origin` set to a function that validates against an allowlist?
   - Is `credentials: true` combined with a specific origin? (`credentials: true` with `origin: *` is rejected by browsers, but misconfigured patterns like reflecting the `Origin` header are dangerous)
   - Are CORS headers applied to all routes or only the ones that need cross-origin access?

**Error Handling:**
4. Is there a global error handler? (`app.use((err, req, res, next) => ...)`)
   - Does it leak stack traces in production? (check for `NODE_ENV` conditional)
   - Are unhandled promise rejections caught? (`process.on('unhandledRejection', ...)`)
   - Do error responses contain internal details (file paths, query strings, object structures)?
