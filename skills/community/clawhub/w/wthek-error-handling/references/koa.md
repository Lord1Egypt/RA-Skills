# Koa Error Handling with @wthek

Guide for implementing `@wthek/koa-middleware`.

---

## Installation

```bash
npm install @wthek/koa-middleware http-error-kit http-response-status-code
```

---

## 1. Global Setup (`KitKoaMiddleware`)

In Koa's onion middleware architecture, error middleware sits at or near the **very top** of the middleware stack so that it wraps all downstream execution in `try ... catch`:

```typescript
import Koa from "koa";
import { KitKoaMiddleware } from "@wthek/koa-middleware";
import { KitHttpError } from "http-error-kit";
import { NOT_FOUND } from "http-response-status-code";

const app = new Koa();

// Register at the top of middleware stack
app.use(
  KitKoaMiddleware({
    log: true,
    handleUnknownErrors: true,
    emitAppError: true,
  }),
);

// Downstream routes / middleware
app.use(async (ctx) => {
  if (ctx.path === "/users/me") {
    throw new KitHttpError(NOT_FOUND, "User Not Found", { id: "me" });
  }
  ctx.body = { ok: true };
});

export default app;
```

---

## 2. Configuration Options

| Option | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `log` | `boolean \| ((error: unknown, ctx: Context) => void)` | `false` | When `true`, logs via `console.error`. When a function is provided, receives `(error, ctx)` for custom logging. |
| `handleUnknownErrors` | `boolean` | `false` | When `true`, unhandled non-Kit errors return a structured 500 JSON response instead of re-throwing. |
| `emitAppError` | `boolean` | `false` | When `true`, calls `ctx.app.emit("error", error, ctx)` to notify centralized app listeners (e.g. Sentry). |

---

## 3. Streaming and Headers Sent Guard

If headers have already been sent to the client (e.g., long-lived streams or partial responses), `KitKoaMiddleware` skips writing status or body to prevent ERR_HTTP_HEADERS_SENT exceptions.

