# Custom Formatters, RFC-7807/RFC-9457 & MCP Alignment

Guide for formatting error responses into standardized formats using `http-error-kit` formatters.

---

## How Formatters Work

All `@wthek` middleware packages serialize errors by calling `error.toJSON()` (Express uses `res.send(error)` which triggers `toJSON()`; Hono/Koa use `c.json(error.toJSON())` / `ctx.body = error.toJSON()`). The **formatter** controls what `toJSON()` returns.

**Without a formatter**, the default output is:
```json
{ "statusCode": 400, "message": "Bad Request", "details": null }
```

**With a formatter**, you control the shape entirely.

### Formatter Function Signature

```typescript
type IFormatter = (
    statusCode: number,
    message: string,
    details: unknown,
    ...args: unknown[]
) => unknown;
```

The `args` are additional arguments passed to `new KitHttpError(statusCode, message, details, ...args)`.

---

## Global Formatter Configuration

Configure once at server startup. Applies to **all** `KitHttpError` instances:

```typescript
import { KitHttpErrorConfig } from "http-error-kit";

KitHttpErrorConfig.configureFormatter((statusCode, message, details, ...args) => {
    return {
        success: false,
        status: statusCode,
        error: {
            message,
            details: details ?? null,
            timestamp: new Date().toISOString(),
            traceId: args[0] ?? null,
        },
    };
});
```

### Resetting the Formatter

```typescript
KitHttpErrorConfig.resetFormatter();
```

This clears the global formatter **and** disables `KitHttpError`-based error mode (reverts to `KitGeneralError` for the default import path).

---

## Instance-Specific Formatter

Override the global format for a specific error. Returns `this` for chaining:

```typescript
import { KitHttpError } from "http-error-kit";
import { BAD_REQUEST } from "http-response-status-code";

const error = new KitHttpError(BAD_REQUEST, "Payment failed", { code: "CARD_DECLINED" });

error.setFormatter((statusCode, message, details) => ({
    error_code: (details as any)?.code,
    error_description: message,
}));

throw error;
```

---

## RFC-7807 Problem Details (application/problem+json)

[RFC 7807](https://datatracker.ietf.org/doc/html/rfc7807) defines a standard JSON format for HTTP error responses. Its successor [RFC 9457](https://datatracker.ietf.org/doc/html/rfc9457) refines and obsoletes it but maintains backward compatibility.

### Required Fields

| Field | Type | Description |
| :--- | :--- | :--- |
| `type` | `string` (URI) | A URI reference identifying the error type. Use `"about:blank"` when no specific type URI exists. |
| `title` | `string` | A short, human-readable summary. Should NOT change between occurrences. |
| `status` | `number` | The HTTP status code. |

### Optional Fields

| Field | Type | Description |
| :--- | :--- | :--- |
| `detail` | `string` | Human-readable explanation specific to this occurrence. |
| `instance` | `string` (URI) | A URI reference identifying the specific occurrence (e.g., request URL, trace ID). |

### Built-In RFC-7807 Formatter (Recommended)

`http-error-kit` provides a built-in RFC-7807 / RFC-9457 formatter and activation helper:

```typescript
import { KitHttpErrorConfig, rfcProblemDetailsFormatter } from "http-error-kit";

// One-liner activation:
KitHttpErrorConfig.useRfcProblemDetails();

// Or explicitly configure with the exported formatter function:
// KitHttpErrorConfig.configureFormatter(rfcProblemDetailsFormatter);
```

### Custom RFC Formatter Implementation

If you need a custom base URI or custom extension members:

```typescript
import { KitHttpErrorConfig } from "http-error-kit";

KitHttpErrorConfig.configureFormatter((statusCode, message, details, ...args) => {
    return {
        type: `https://httpstatuses.com/${statusCode}`,
        title: message,
        status: statusCode,
        detail: typeof details === "string" ? details : undefined,
        instance: typeof args[0] === "string" ? args[0] : undefined,
        ...(typeof details === "object" && details !== null ? { invalidParams: details } : {}),
    };
});
```

### RFC-9457 Enhancements

RFC 9457 (the successor to RFC 7807) adds:
- **`type` defaults to `"about:blank"`** when omitted (instead of being required)
- **Content-Type**: `application/problem+json` (same as RFC 7807)
- **Extension members**: Any additional JSON fields are allowed and encouraged

```typescript
KitHttpErrorConfig.configureFormatter((statusCode, message, details, ...args) => ({
    // RFC-9457 — type defaults to about:blank
    type: "about:blank",
    title: message,
    status: statusCode,
    detail: typeof details === "string" ? details : message,
    instance: typeof args[0] === "string" ? args[0] : undefined,
    // Extension: validation errors
    ...(details && typeof details === "object" && "issues" in (details as object)
        ? { errors: (details as { issues: unknown[] }).issues }
        : {}),
}));
```

### Setting Content-Type Header

The `@wthek` middleware packages set `application/json` by default. For strict RFC compliance, set the header in your framework:

```typescript
// Express — via a wrapper
app.use((err, req, res, next) => {
    res.type("application/problem+json");
    next(err);
});
app.use(KitExpressMiddleware());

// Hono — set in error handler
app.onError(KitHonoErrorHandler({ ... }));
// Or override with instance formatter that sets header
```

---

## MCP Error Formatter (Planned)

The `@wthek/mcp-error-formatter` package (not yet published) will format `KitHttpError` instances into [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) error responses.

### Planned Design

The MCP error format maps to JSON-RPC 2.0 error responses used by MCP:

```json
{
    "jsonrpc": "2.0",
    "error": {
        "code": -32603,
        "message": "Internal Server Error",
        "data": { "statusCode": 500, "details": null }
    },
    "id": 1
}
```

### Alignment Strategy

The MCP formatter will:
1. Map HTTP status codes to appropriate JSON-RPC error codes
2. Preserve `KitHttpError` details in the `data` field
3. Follow the same `KitHttpErrorConfig.configureFormatter()` pattern
4. Allow dual-output formatters that work for both HTTP and MCP transports

### Dual-Transport Formatter Pattern (Preview)

When the MCP formatter ships, you'll be able to write a single formatter that handles both:

```typescript
import { KitHttpErrorConfig } from "http-error-kit";

KitHttpErrorConfig.configureFormatter((statusCode, message, details, ...args) => {
    const transport = args[0]; // "http" | "mcp"

    if (transport === "mcp") {
        return {
            code: statusCode >= 500 ? -32603 : -32602,
            message,
            data: { statusCode, details },
        };
    }

    // Default: RFC-7807 for HTTP
    return {
        type: `https://httpstatuses.com/${statusCode}`,
        title: message,
        status: statusCode,
        detail: typeof details === "string" ? details : undefined,
    };
});
```

---

## Formatter Priority Chain

When `toJSON()` is called on a `KitHttpError`:

1. **Instance formatter** (set via `error.setFormatter(fn)`) — highest priority
2. **Global formatter** (set via `KitHttpErrorConfig.configureFormatter(fn)`)
3. **Default format** — `{ statusCode, message, details }`
