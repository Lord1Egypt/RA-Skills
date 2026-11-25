# Hono Error Handling with @wthek

Guide for implementing `@wthek/hono-middleware`.

---

## Installation

```bash
npm install @wthek/hono-middleware http-error-kit http-response-status-code
```

**Peer dependency:** `hono >= 4.0.0`
**Multi-runtime:** Node.js, Cloudflare Workers, Deno, Bun

---

## 1. Global Setup (`KitHonoMiddleware`)

Attaches the error handler across the entire Hono application instance via `app.onError`:

```typescript
import { Hono } from "hono";
import { KitHonoMiddleware } from "@wthek/hono-middleware";
import { KitHttpError } from "http-error-kit";
import { NOT_FOUND } from "http-response-status-code";

const app = new Hono();

app.get("/users/:id", (c) => {
    throw new KitHttpError(NOT_FOUND, "User Not Found", { id: c.req.param("id") });
});

// Attach global error handler
KitHonoMiddleware(app, {
    log: true,
    handleUnknownErrors: true,
});

export default app;
```

---

## 2. Standalone Error Handler (`KitHonoErrorHandler`)

Returns a Hono-compatible `ErrorHandler` function for `app.onError()` or sub-routers:

```typescript
import { Hono } from "hono";
import { KitHonoErrorHandler } from "@wthek/hono-middleware";

const app = new Hono();

app.onError(
    KitHonoErrorHandler({
        log: (err, c) => console.error(`Error on ${c.req.method} ${c.req.path}:`, err),
        handleUnknownErrors: true,
    })
);
```

---

## With Zod Validation

```typescript
import { fromZodError } from "@wthek/zod-transformer";
import { z } from "zod";
import { UNPROCESSABLE_ENTITY } from "http-response-status-code";

app.post("/users", async (c) => {
    const body = await c.req.json();
    try {
        const user = UserSchema.parse(body);
        return c.json({ success: true, data: user }, 201);
    } catch (error) {
        const kitError = fromZodError(error, { statusCode: UNPROCESSABLE_ENTITY });
        if (kitError) throw kitError;
        throw error;
    }
});
```

## With Valibot Validation

```typescript
import { KitValibotTransformer } from "@wthek/valibot-transformer";
import * as v from "valibot";
import { UNPROCESSABLE_ENTITY } from "http-response-status-code";

app.post("/users", async (c) => {
    const body = await c.req.json();
    try {
        const user = v.parse(UserSchema, body);
        return c.json(user, 201);
    } catch (error) {
        KitValibotTransformer(error, { statusCode: UNPROCESSABLE_ENTITY });
    }
});
```

## With TypeBox Validation

```typescript
import { KitTypeBoxTransformer } from "@wthek/typebox-transformer";
import { Value } from "@sinclair/typebox/value";
import { Type } from "@sinclair/typebox";

const UserSchema = Type.Object({ name: Type.String(), age: Type.Number({ minimum: 18 }) });

app.post("/users", async (c) => {
    const body = await c.req.json();
    try {
        Value.Assert(UserSchema, body);
        return c.json(body, 201);
    } catch (error) {
        KitTypeBoxTransformer(error);
    }
});
```

---

## Options Reference

```typescript
interface IKitHonoMiddlewareOptions {
    // When true, logs via console.error.
    // When a callback is provided, receives (error: unknown, c: Context).
    log?: boolean | ((error: unknown, c: Context) => void);

    // When true, catches any uncaught non-KitHttpError and formats as a 500 response.
    handleUnknownErrors?: boolean;
}
```

---

## Error Handling Behavior

1. **KitHttpError / KitGeneralError**: Extracts `statusCode` via `error.getInputs()`, serializes via `error.toJSON()`, returns `c.json(payload, statusCode)`.
2. **Unknown errors + `handleUnknownErrors: true`**: Returns `c.json({ statusCode: 500, message: "Internal Server Error" }, 500)`.
3. **Unknown errors + `handleUnknownErrors: false`**: Returns `c.text(error.message, 500)`.
4. **Internal failure**: Returns `c.text("Internal Server Error", 500)` as ultimate fallback.

## Key Differences from Other Frameworks

- Uses `app.onError()` handler (not middleware chain or event)
- No Express-style pipeline ordering — error handler is a single registered function
- Uses `KitZodTransformer` / `KitValibotTransformer` / `KitTypeBoxTransformer` (manual), not interceptors
