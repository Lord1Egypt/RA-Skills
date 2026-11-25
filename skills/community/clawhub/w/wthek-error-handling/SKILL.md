---
name: wthek-error-handling
description: >-
  Use this skill whenever adding, refactoring, configuring, or standardizing HTTP error handling, validation error pipelines (Zod, Valibot, TypeBox), HTTP status code usage, or MCP error formatting in Express, Fastify, Hono, Koa, NestJS, Restify, Node.js applications, or Model Context Protocol servers using @wthek packages, http-error-kit, and http-response-status-code.
---

# WTHek Error Handling Skill

This skill guides the implementation of standardized, production-safe HTTP error handling and validation error pipelines using the `@wthek` ("What The HEK") extension suite powered by [`http-error-kit`](https://www.npmjs.com/package/http-error-kit) and [`http-response-status-code`](https://www.npmjs.com/package/http-response-status-code).

---

## 1. Package Decision Matrix

Inspect the project's `package.json` to identify the framework and validation libraries in use, then select the appropriate packages:

| Framework / Need | Primary Package | Companion Validation Package |
| :--- | :--- | :--- |
| **Express.js** | `@wthek/express-middleware` | `@wthek/zod-express-interceptor` (if Zod) · `@wthek/zod-transformer` · `@wthek/valibot-transformer` · `@wthek/typebox-transformer` |
| **Fastify** | `@wthek/fastify-middleware` | `@wthek/zod-transformer` · `@wthek/valibot-transformer` · `@wthek/typebox-transformer` |
| **Hono** | `@wthek/hono-middleware` | `@wthek/zod-transformer` · `@wthek/valibot-transformer` · `@wthek/typebox-transformer` |
| **Koa** | `@wthek/koa-middleware` | `@wthek/zod-transformer` · `@wthek/valibot-transformer` · `@wthek/typebox-transformer` |
| **NestJS** | `@wthek/nestjs-middleware` | `@wthek/zod-transformer` · `@wthek/valibot-transformer` · `@wthek/typebox-transformer` |
| **Restify** | `@wthek/restify-middleware` | `@wthek/zod-transformer` · `@wthek/valibot-transformer` · `@wthek/typebox-transformer` |
| **Framework-Agnostic / Utils** | `http-error-kit` | `@wthek/zod-transformer` · `@wthek/valibot-transformer` · `@wthek/typebox-transformer` |

### Companion Packages (always install alongside)

| Package | Purpose |
| :--- | :--- |
| [`http-error-kit`](https://www.npmjs.com/package/http-error-kit) | Core error classes (`KitHttpError`, `KitGeneralError`, 42 named error classes) and formatter configuration (`KitHttpErrorConfig`) |
| [`http-response-status-code`](https://www.npmjs.com/package/http-response-status-code) | Type-safe, tree-shakeable HTTP status code constants and utilities |
| [`@wthek/mcp-error-formatter`](https://www.npmjs.com/package/@wthek/mcp-error-formatter) | Formats errors and `KitHttpError` instances into MCP tool results (`CallToolResult`), JSON-RPC 2.0 errors, and `KitHttpErrorConfig` formatters |
| [`@wthek/mcp`](https://www.npmjs.com/package/@wthek/mcp) | Standalone local MCP server providing AI agents with HTTP standards lookup, framework recipes, and code anti-pattern audits |

---

## 2. Core API: `http-error-kit`

### Three Import Paths

| Import Path | Base Class | Formatter Support | Use Case |
| :--- | :--- | :--- | :--- |
| `http-error-kit` (default) | Dynamic — delegates to `KitHttpError` or `KitGeneralError` | Yes (when configured) | Standard usage |
| `http-error-kit/http` | Always `KitHttpError` | Yes (global + instance) | When you always want formatter support |
| `http-error-kit/generic` | Always `KitGeneralError` | No (static format) | Lightweight, no formatter needed |

### KitHttpError Class

The primary error class. All `@wthek` middleware packages catch instances of this class (and `KitGeneralError`).

```typescript
import { KitHttpError } from "http-error-kit";
import { NOT_FOUND, BAD_REQUEST } from "http-response-status-code";

// Basic usage
throw new KitHttpError(NOT_FOUND, "User not found");

// With details
throw new KitHttpError(BAD_REQUEST, "Invalid input", { field: "email" });

// With additional args (spread onto instance or passed to formatter)
throw new KitHttpError(BAD_REQUEST, "Validation failed", { issues: [...] }, { requestId: "abc" });
```

#### Constructor

```typescript
new KitHttpError(statusCode: number, message: string, details?: unknown, ...args: unknown[])
```

#### Properties

| Property | Type | Description |
| :--- | :--- | :--- |
| `statusCode` | `number` | HTTP status code |
| `message` | `string` | Error message (inherited from `Error`) |
| `details` | `unknown` | Additional contextual information |
| `headers` | `Record<string, string> \| undefined` | HTTP response headers (e.g. WWW-Authenticate, Retry-After) |

#### Methods

| Method | Returns | Description |
| :--- | :--- | :--- |
| `getInputs()` | `IRawInput` | Returns `{ statusCode, message, details, args }` — original constructor arguments |
| `toJSON()` | `object` | Serializes using `instanceFormatter ?? defaultFormatter`, else `{ statusCode, message, details }` |
| `setFormatter(fn)` | `this` | Sets an instance-level formatter; returns `this` for chaining |
| `setHeader(name, value)` | `this` | Sets an individual response header; returns `this` for chaining |
| `setHeaders(headers)` | `this` | Sets multiple response headers; returns `this` for chaining |
| `toResponse(init?)` | `Response` | Converts error to a standard WHATWG Fetch `Response` (Next.js, Hono, Workers, Bun) |

### Type Guards

```typescript
import { isKitError, isKitHttpError, isKitGeneralError } from "http-error-kit";

try {
    // ...
} catch (err: unknown) {
    if (isKitError(err)) {
        // Safe access to statusCode, toJSON(), toResponse(), headers
        return err.toResponse();
    }
}
```

- **`isKitError(err)`**: True for any `KitHttpError`, `KitGeneralError`, or named error class
- **`isKitHttpError(err)`**: True for errors with configurable formatter support (`KitHttpError`)
- **`isKitGeneralError(err)`**: True for lightweight errors (`KitGeneralError`)

### KitGeneralError Class

Lightweight alternative — same constructor as `KitHttpError` but without formatter support. Always serializes to `{ statusCode, message, details }`.

### Named Error Classes (42 total)

`http-error-kit` exports pre-built error classes for every HTTP 4xx/5xx status code. Each class has the signature:

```typescript
constructor(message?: string, details?: unknown, ...args: unknown[])
```

The `message` defaults to the HTTP status description if omitted.

**4xx Client Errors:**
`BadRequestError` (400), `UnauthorizedError` (401), `PaymentRequiredError` (402), `ForbiddenError` (403), `NotFoundError` (404), `MethodNotAllowedError` (405), `NotAcceptableError` (406), `ProxyAuthenticationRequiredError` (407), `RequestTimeoutError` (408), `ConflictError` (409), `GoneError` (410), `LengthRequiredError` (411), `PreconditionFailedError` (412), `RequestTooLongError` (413), `RequestUriTooLongError` (414), `UnsupportedMediaTypeError` (415), `RequestedRangeNotSatisfiableError` (416), `ExpectationFailedError` (417), `ImATeapotError` (418), `InsufficientSpaceOnResourceError` (419), `MethodFailureError` (420), `MisdirectedRequestError` (421), `UnprocessableEntityError` (422), `LockedError` (423), `FailedDependencyError` (424), `TooEarlyError` (425), `UpgradeRequiredError` (426), `PreconditionRequiredError` (428), `TooManyRequestsError` (429), `RequestHeaderFieldsTooLargeError` (431), `UnavailableForLegalReasonsError` (451)

**5xx Server Errors:**
`InternalServerError` (500), `NotImplementedError` (501), `BadGatewayError` (502), `ServiceUnavailableError` (503), `GatewayTimeoutError` (504), `HttpVersionNotSupportedError` (505), `VariantAlsoNegotiatesError` (506), `InsufficientStorageError` (507), `LoopDetectedError` (508), `NotExtendedError` (510), `NetworkAuthenticationRequiredError` (511)

**Example usage:**

```typescript
import { NotFoundError, BadRequestError } from "http-error-kit";

// No need to pass status code — it's built in
throw new NotFoundError("User not found");
throw new NotFoundError(); // defaults to "Not Found"
throw new BadRequestError("Invalid email", { field: "email" });
```

### Formatter Configuration (`KitHttpErrorConfig`)

Formatters control the shape of serialized error output (`toJSON()` / `res.send(error)`). The middleware packages call `res.send(error)` or `c.json(error.toJSON())`, so the formatter determines the response body shape.

```typescript
import { KitHttpErrorConfig } from "http-error-kit";

// Configure once at server startup
KitHttpErrorConfig.configureFormatter((statusCode, message, details, ...args) => ({
    type: `https://httpstatuses.com/${statusCode}`,
    title: message,
    status: statusCode,
    detail: typeof details === "string" ? details : undefined,
    invalidParams: typeof details === "object" ? details : undefined,
}));

// Reset to defaults
KitHttpErrorConfig.resetFormatter();
```

**Instance-specific formatter** (overrides global):

```typescript
const error = new KitHttpError(BAD_REQUEST, "Payment failed", { code: "CARD_DECLINED" });
error.setFormatter((statusCode, message, details) => ({
    error_code: details?.code,
    error_description: message,
}));
throw error; // .setFormatter() returns this, so chaining works too
```

### Types Reference

```typescript
// Formatter function signature
type IFormatter = (statusCode: number, message: string, details: unknown, ...args: unknown[]) => unknown;

// Raw constructor inputs
interface IRawInput {
    statusCode: number;
    message: string;
    details: unknown;
    args: unknown[];
}
```

---

## 3. HTTP Status Codes: `http-response-status-code`

### Why Use It

- **Readability**: `NOT_FOUND` is self-documenting; `404` requires memorization
- **IDE discoverability**: Autocomplete surfaces all valid HTTP codes
- **Tree-shakeable**: Only imported codes are included in the bundle (`sideEffects: false`)
- **Zero dependencies**: Standalone, lightweight package
- **Utilities**: Helper functions for classification, description, and Fetch Response creation

### Installation

```bash
npm install http-response-status-code
```

### Import Patterns

```typescript
// ESM — named imports (tree-shaking friendly)
import { OK, NOT_FOUND, INTERNAL_SERVER_ERROR } from "http-response-status-code";

// CJS
const { OK, NOT_FOUND } = require("http-response-status-code");

// Enum access (alternative)
import { CODES } from "http-response-status-code";
CODES.HTTP_CODE_404; // 404
```

### Naming Convention

Named constants use **`SCREAMING_SNAKE_CASE`** matching the HTTP status name: `NOT_FOUND`, `BAD_REQUEST`, `OK`, `INTERNAL_SERVER_ERROR`, etc.

The `CODES` enum uses the pattern **`HTTP_CODE_{number}`**: `CODES.HTTP_CODE_200`, `CODES.HTTP_CODE_404`, etc.

### Complete Status Code Reference

#### 1xx Informational

| Constant | Code |
| :--- | :--- |
| `CONTINUE` | 100 |
| `SWITCHING_PROTOCOLS` | 101 |
| `PROCESSING` | 102 |
| `EARLY_HINTS` | 103 |
| `TOO_LONG` | 122 |

#### 2xx Success

| Constant | Code |
| :--- | :--- |
| `OK` | 200 |
| `CREATED` | 201 |
| `ACCEPTED` | 202 |
| `NON_AUTHORITATIVE_INFORMATION` | 203 |
| `NO_CONTENT` | 204 |
| `RESET_CONTENT` | 205 |
| `PARTIAL_CONTENT` | 206 |
| `MULTI_STATUS` | 207 |
| `ALREADY_REPORTED` | 208 |
| `IM_USED` | 226 |

#### 3xx Redirection

| Constant | Code |
| :--- | :--- |
| `MULTIPLE_CHOICES` | 300 |
| `MOVED_PERMANENTLY` | 301 |
| `MOVED_TEMPORARILY` | 302 |
| `SEE_OTHER` | 303 |
| `NOT_MODIFIED` | 304 |
| `USE_PROXY` | 305 |
| `SWITCH_PROXY` | 306 |
| `TEMPORARY_REDIRECT` | 307 |
| `PERMANENT_REDIRECT` | 308 |

#### 4xx Client Error

| Constant | Code |
| :--- | :--- |
| `BAD_REQUEST` | 400 |
| `UNAUTHORIZED` | 401 |
| `PAYMENT_REQUIRED` | 402 |
| `FORBIDDEN` | 403 |
| `NOT_FOUND` | 404 |
| `METHOD_NOT_ALLOWED` | 405 |
| `NOT_ACCEPTABLE` | 406 |
| `PROXY_AUTHENTICATION_REQUIRED` | 407 |
| `REQUEST_TIMEOUT` | 408 |
| `CONFLICT` | 409 |
| `GONE` | 410 |
| `LENGTH_REQUIRED` | 411 |
| `PRECONDITION_FAILED` | 412 |
| `REQUEST_TOO_LONG` | 413 |
| `REQUEST_URI_TOO_LONG` | 414 |
| `UNSUPPORTED_MEDIA_TYPE` | 415 |
| `REQUESTED_RANGE_NOT_SATISFIABLE` | 416 |
| `EXPECTATION_FAILED` | 417 |
| `IM_A_TEAPOT` | 418 |
| `INSUFFICIENT_SPACE_ON_RESOURCE` | 419 |
| `METHOD_FAILURE` | 420 |
| `MISDIRECTED_REQUEST` | 421 |
| `UNPROCESSABLE_ENTITY` | 422 |
| `LOCKED` | 423 |
| `FAILED_DEPENDENCY` | 424 |
| `TOO_EARLY` | 425 |
| `UPGRADE_REQUIRED` | 426 |
| `PRECONDITION_REQUIRED` | 428 |
| `TOO_MANY_REQUESTS` | 429 |
| `REQUEST_HEADER_FIELDS_TOO_LARGE` | 431 |
| `UNAVAILABLE_FOR_LEGAL_REASONS` | 451 |

#### 5xx Server Error

| Constant | Code |
| :--- | :--- |
| `INTERNAL_SERVER_ERROR` | 500 |
| `NOT_IMPLEMENTED` | 501 |
| `BAD_GATEWAY` | 502 |
| `SERVICE_UNAVAILABLE` | 503 |
| `GATEWAY_TIMEOUT` | 504 |
| `HTTP_VERSION_NOT_SUPPORTED` | 505 |
| `VARIANT_ALSO_NEGOTIATES` | 506 |
| `INSUFFICIENT_STORAGE` | 507 |
| `LOOP_DETECTED` | 508 |
| `NOT_EXTENDED` | 510 |
| `NETWORK_AUTHENTICATION_REQUIRED` | 511 |

### Utility Functions

| Function | Signature | Description |
| :--- | :--- | :--- |
| `getStatusCode(name)` | `(name: string) => number` | Get code from name: `getStatusCode("NOT_FOUND")` → `404` |
| `getStatusName(code)` | `(code: number) => string` | Get name from code: `getStatusName(404)` → `"NOT_FOUND"` |
| `getStatusDescription(code)` | `(code: number) => string` | Human-readable: `getStatusDescription(500)` → `"Internal Server Error"` |
| `toResponseInit(code, init?)` | `<T>(code: number \| string, init?: T) => IResponseInit & T` | Fetch API helper: `new Response(body, toResponseInit(OK))` |
| `isInformational(code)` | `(code: number) => boolean` | `true` if 1xx (throws for invalid codes) |
| `isSuccess(code)` | `(code: number) => boolean` | `true` if 2xx (throws for invalid codes) |
| `isRedirectional(code)` | `(code: number) => boolean` | `true` if 3xx (throws for invalid codes) |
| `isClientError(code)` | `(code: number) => boolean` | `true` if 4xx (throws for invalid codes) |
| `isServerError(code)` | `(code: number) => boolean` | `true` if 5xx (throws for invalid codes) |
| `isValidStatusCode(code)` | `(code: number) => boolean` | Safe check — returns `false` instead of throwing for invalid codes |
| `getInformationalCodes()` | `() => number[]` | All 1xx codes |
| `getSuccessCodes()` | `() => number[]` | All 2xx codes |
| `getRedirectionalCodes()` | `() => number[]` | All 3xx codes |
| `getClientErrorCodes()` | `() => number[]` | All 4xx codes |
| `getServerErrorCodes()` | `() => number[]` | All 5xx codes |

> **Warning:** All `is*` validators (except `isValidStatusCode`) **throw an Error** for unrecognized status codes. Use `isValidStatusCode(code)` first if you need a safe check.

### Integration with http-error-kit

**Always prefer named constants over magic numbers** when constructing errors:

```typescript
import { KitHttpError } from "http-error-kit";
import { NOT_FOUND, BAD_REQUEST } from "http-response-status-code";

// ❌ AVOID: Magic numbers
throw new KitHttpError(404, "User not found");

// ✅ PREFERRED: Named constants
throw new KitHttpError(NOT_FOUND, "User not found");
```

#### With Named Error Classes

```typescript
// Named error classes already have the status code baked in,
// so http-response-status-code is used for other purposes:
import { NotFoundError } from "http-error-kit";
import { CREATED, NO_CONTENT } from "http-response-status-code";

throw new NotFoundError("User not found"); // 404 is automatic

// For success responses:
res.status(CREATED).json({ user });
res.status(NO_CONTENT).send();
```

#### With Validation Transformers

```typescript
import { KitZodTransformer } from "@wthek/zod-transformer";
import { UNPROCESSABLE_ENTITY } from "http-response-status-code";

try {
    schema.parse(data);
} catch (error) {
    KitZodTransformer(error, { statusCode: UNPROCESSABLE_ENTITY });
}
```

#### With Fetch API / Web Standards

```typescript
import { toResponseInit, OK, NOT_FOUND } from "http-response-status-code";

// Hono, Next.js App Router, Cloudflare Workers, Deno, Bun
return Response.json({ data }, toResponseInit(OK));
return Response.json({ error: "Not found" }, toResponseInit(NOT_FOUND));

// With extra init options
return new Response(body, toResponseInit(OK, {
    headers: { "Content-Type": "application/json" },
}));
```

---

## 4. Mandatory Architectural Guardrails

When writing or refactoring error handling code with `@wthek`, you **must** enforce these rules:

### A. Framework Error Registration Patterns

Each framework registers the error handler differently. **Get this right first.**

| Framework | How to Register | Pattern |
| :--- | :--- | :--- |
| **Express** | `app.use(KitExpressMiddleware())` | Terminal error middleware (last `app.use`) |
| **Fastify** | `KitFastifyMiddleware(app, opts)` or `app.setErrorHandler(KitFastifyErrorHandler(opts))` | Error handler hook |
| **Hono** | `KitHonoMiddleware(app, opts)` or `app.onError(KitHonoErrorHandler(opts))` | `app.onError()` handler |
| **Koa** | `KitKoaMiddleware(app, opts)` or `app.use(KitKoaMiddleware(opts))` | Onion middleware (register at **top** of stack) |
| **NestJS** | `app.useGlobalFilters(new KitExceptionFilter(opts))` | Exception filter |
| **Restify** | `server.on("restifyError", KitRestifyMiddleware(opts))` | Error event listener |

### B. Middleware Execution Pipeline Ordering

- **Express** — Error middleware must be the **last** `app.use()`. Interceptors go after routes but before the error middleware.
- **Koa** — Error middleware must be at the **top** of the middleware stack (opposite of Express) because Koa uses an onion architecture where upstream middleware wraps downstream in `try/catch`.

```typescript
// ❌ WRONG (Express): Interceptor placed before routes
app.use(KitZodExpressInterceptor());
app.post("/users", userHandler);

// ✅ CORRECT (Express): Routes → Interceptors → Final Error Middleware
app.post("/users", userHandler);
app.use(KitZodExpressInterceptor());
app.use(KitExpressMiddleware());

// ✅ CORRECT (Koa): Error middleware at the TOP
app.use(KitKoaMiddleware({ handleUnknownErrors: true }));
app.use(router.routes());
```

### C. Streaming & Headers Sent Protection

- In Express / Restify: `if (res.headersSent) { next(error); return; }`
- In Fastify: `if (reply.sent) { return; }`
- In Koa: `if (ctx.headerSent) { return; }`

> **Note:** The `@wthek/express-middleware` and `@wthek/koa-middleware` have **built-in headers-sent checks**. This guardrail applies to **custom error handlers** you write manually.

### D. Type Safety Standards

- Never annotate caught errors as `error: any`. Always use `error: unknown`.
- Use nullish coalescing `??` instead of logical OR `||` when reading status codes (e.g., `statusCode ?? 400`).
- **Use `http-response-status-code` constants** instead of magic numbers for all status codes.

### E. Redundant Try/Catch Elimination

- Do not wrap code in `try { ... } catch (err) { throw err; }`. Only catch if handling, transforming, or logging.

### F. How Middlewares Serialize Errors

All `@wthek` middleware packages serialize errors through `error.toJSON()` (via `res.send(error)` in Express, or `c.json(error.toJSON())` in Hono). This means:

1. The **response body shape** is controlled by the formatter configured via `KitHttpErrorConfig.configureFormatter()` or `error.setFormatter()` — NOT by middleware options.
2. Middleware options control **logging** and **unknown error handling** only.
3. Without a formatter, the default output is: `{ statusCode, message, details }`.

---

## 5. Middleware Options Reference

All `@wthek` middleware packages have consistent options:

| Option | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `log` | `boolean \| ((error: unknown, req/c/ctx) => void)` | `false` | When `true`, logs via `console.error` (Fastify uses `request.log.error`). When a function, invokes custom logging. |
| `handleUnknownErrors` | `boolean` | `false` | If `true`, non-Kit errors return a structured `{ statusCode: 500, message: "Internal Server Error" }` JSON response instead of framework defaults. |

#### Koa-Specific Extra Option

| Option | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `emitAppError` | `boolean` | `false` | When `true`, calls `ctx.app.emit("error", error, ctx)` to notify centralized app listeners (e.g., Sentry, Datadog). |

### Fastify, Hono & Koa: Two Setup Approaches

Both Fastify, Hono, and Koa middleware packages export two setup approaches:

| Function | Description |
| :--- | :--- |
| `KitFastifyMiddleware(app, opts)` / `KitHonoMiddleware(app, opts)` / `KitKoaMiddleware(app, opts)` | Convenience wrapper — registers the handler globally on the app instance |
| `KitFastifyErrorHandler(opts)` / `KitHonoErrorHandler(opts)` / `app.use(KitKoaMiddleware(opts))` | Returns a handler/middleware for manual registration (scoped plugins, sub-routers) |

### Transformer Options

Available on: `IKitZodTransformerOptions`, `IKitZodExpressInterceptorOptions` (same type), `IKitValibotTransformerOptions`, `IKitTypeBoxTransformerOptions`

| Option | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `message` | `string` | `"Zod Validation Failed"` / `"Valibot Validation Failed"` / `"TypeBox Validation Failed"` | Custom error message for the validation failure. |
| `statusCode` | `number` | `400` (`BAD_REQUEST`) | Custom HTTP status code. Use `UNPROCESSABLE_ENTITY` from `http-response-status-code` for semantic correctness. |

---

## 6. Validation Library Integration

### Zod

Two packages are available:

| Package | Type | Use Case |
| :--- | :--- | :--- |
| `@wthek/zod-express-interceptor` | Express error middleware | Automatic — sits in the Express error pipeline, converts `ZodError` via `next()` |
| `@wthek/zod-transformer` | Pure functions | Manual — call in catch blocks for Fastify, Hono, NestJS, Restify, or any framework |

#### `@wthek/zod-transformer` exports two functions:

| Function | Returns | Behavior |
| :--- | :--- | :--- |
| `fromZodError(error, opts?)` | `KitHttpError \| null` | **Non-throwing.** Returns `KitHttpError` if input is `ZodError`, else `null`. |
| `KitZodTransformer(error, opts?)` | `never` | **Always throws.** Throws `KitHttpError` if `ZodError`, otherwise re-throws the original error unchanged. |

#### Error Payload Structure (Zod)

Zod issues are preserved in `error.details.issues`:

```json
{
    "statusCode": 400,
    "message": "Zod Validation Failed",
    "details": {
        "issues": [
            { "code": "too_small", "minimum": 18, "type": "number", "message": "...", "path": ["age"] }
        ]
    }
}
```

### Valibot

| Package | Type | Use Case |
| :--- | :--- | :--- |
| `@wthek/valibot-transformer` | Pure functions | Manual — call in catch blocks for any framework |

**Peer dependencies:** `valibot >= 1.0.0`, `http-error-kit >= 1.2.0`

#### `@wthek/valibot-transformer` exports two functions:

| Function | Returns | Behavior |
| :--- | :--- | :--- |
| `fromValiError(error, opts?)` | `KitHttpError \| null` | **Non-throwing.** Returns `KitHttpError` if input is `ValiError`, else `null`. |
| `KitValibotTransformer(error, opts?)` | `never` | **Always throws.** Throws `KitHttpError` if `ValiError`, otherwise re-throws unchanged. |

```typescript
import { KitValibotTransformer } from "@wthek/valibot-transformer";
import * as v from "valibot";
import { UNPROCESSABLE_ENTITY } from "http-response-status-code";

const schema = v.object({
    name: v.string(),
    age: v.pipe(v.number(), v.minValue(18)),
});

try {
    v.parse(schema, data);
} catch (err) {
    KitValibotTransformer(err, {
        message: "Validation Failed",
        statusCode: UNPROCESSABLE_ENTITY,
    });
}
```

#### Error Payload Structure (Valibot)

Valibot issues are preserved in `error.details.issues`:

```json
{
    "statusCode": 400,
    "message": "Valibot Validation Failed",
    "details": {
        "issues": [
            { "kind": "validation", "type": "min_value", "message": "...", "path": [...] }
        ]
    }
}
```

### TypeBox

| Package | Type | Use Case |
| :--- | :--- | :--- |
| `@wthek/typebox-transformer` | Pure functions | Manual — call in catch blocks for any framework |

**Peer dependencies:** `@sinclair/typebox >= 0.32.0`, `http-error-kit >= 1.2.0`

#### `@wthek/typebox-transformer` exports two functions:

| Function | Returns | Behavior |
| :--- | :--- | :--- |
| `fromTypeBoxError(error, opts?)` | `KitHttpError \| null` | **Non-throwing.** Returns `KitHttpError` if input is a TypeBox error, else `null`. |
| `KitTypeBoxTransformer(error, opts?)` | `never` | **Always throws.** Throws `KitHttpError` if TypeBox error, otherwise re-throws unchanged. |

#### Supported TypeBox Error Input Formats

Unlike Zod/Valibot which have a single error type, TypeBox has multiple error representations. The transformer handles **all** of them:

- `TypeBoxError` instances (including `AssertError` from `Value.Assert()`)
- `ValueError[]` arrays (e.g., `[...Value.Errors(schema, data)]`)
- `ValueErrorIterator` iterators directly (e.g., `Value.Errors(schema, data)`)
- Single `ValueError` objects
- Objects with an `.errors` property containing `ValueError[]`

```typescript
import { Type } from "@sinclair/typebox";
import { Value } from "@sinclair/typebox/value";
import { KitTypeBoxTransformer } from "@wthek/typebox-transformer";
import { UNPROCESSABLE_ENTITY } from "http-response-status-code";

const UserSchema = Type.Object({
    name: Type.String(),
    age: Type.Number({ minimum: 18 }),
});

// Pattern 1: With Value.Assert (throws TypeBoxError)
try {
    Value.Assert(UserSchema, data);
} catch (err) {
    KitTypeBoxTransformer(err, { statusCode: UNPROCESSABLE_ENTITY });
}

// Pattern 2: With Value.Errors (returns iterator)
import { fromTypeBoxError } from "@wthek/typebox-transformer";
const errors = [...Value.Errors(UserSchema, data)];
const kitError = fromTypeBoxError(errors);
if (kitError) throw kitError;
```

#### Error Payload Structure (TypeBox)

TypeBox issues are preserved in `error.details.issues`:

```json
{
    "statusCode": 400,
    "message": "TypeBox Validation Failed",
    "details": {
        "issues": [
            { "type": 38, "path": "/age", "value": 14, "message": "Expected number to be greater or equal to 18" }
        ]
    }
}
```

---

## 7. Progressive Guides & Recipes

Read the dedicated reference guide for your specific framework:

- [Express.js Implementation Guide](./references/express.md)
- [Fastify Implementation Guide](./references/fastify.md)
- [Hono Implementation Guide](./references/hono.md)
- [Koa Implementation Guide](./references/koa.md)
- [NestJS Implementation Guide](./references/nestjs.md)
- [Restify Implementation Guide](./references/restify.md)
- [Zod Validation Integration Guide](./references/zod.md)
- [Valibot Validation Integration Guide](./references/valibot.md)
- [TypeBox Validation Integration Guide](./references/typebox.md)
- [Custom Formatters, RFC-7807 & RFC-9457 Guide](./references/formatters.md)
- [http-response-status-code Usage Guide](./references/status-codes.md)
- [MCP & AI Agent Integration Guide](./references/mcp.md)

---

## 8. Default JSON Response Format

Without a custom formatter, all `@wthek` middlewares produce this structure (via `error.toJSON()`):

```json
{
    "statusCode": 400,
    "message": "Error description",
    "details": null
}
```

For unknown errors (when `handleUnknownErrors: true`):

```json
{
    "statusCode": 500,
    "message": "Internal Server Error"
}
```

With a formatter configured via `KitHttpErrorConfig.configureFormatter()`, the output shape is entirely controlled by your formatter function.

---

## 9. Verification Checklist

Before finalizing any error-handling task:

1. ✅ Verify error handler is registered correctly for the framework (see Section 4A).
2. ✅ Verify interceptors are registered **after** route definitions (Express only).
3. ✅ Test a synthetic 400 error (e.g., invalid Zod/Valibot schema payload) to confirm structured JSON output.
4. ✅ Test a synthetic 500 unhandled runtime error to confirm fallback behavior.
5. ✅ Ensure `http-response-status-code` constants are used instead of magic numbers.
6. ✅ Ensure `error: unknown` typing (never `error: any`).
7. ✅ Ensure nullish coalescing `??` for status code fallbacks (not `||`).
8. ✅ Verify no redundant `try/catch` blocks that only re-throw.
9. ✅ Confirm formatter configuration (if any) is set once at startup via `KitHttpErrorConfig.configureFormatter()`.
10. ✅ Ensure 100% test coverage if writing tests for custom adapters.
