# Fastify Error Handling with @wthek

Guide for implementing `@wthek/fastify-middleware`.

---

## Installation

```bash
npm install @wthek/fastify-middleware http-error-kit http-response-status-code
```

## Two Modes of Usage

`@wthek/fastify-middleware` supports two approaches depending on whether you are configuring the global application instance or a scoped plugin context:

### 1. Global Setup (`KitFastifyMiddleware`)

Attaches the error handler directly across the entire Fastify application instance:

```typescript
import Fastify from "fastify";
import { KitFastifyMiddleware } from "@wthek/fastify-middleware";

const app = Fastify({ logger: true });

// Setup routes
app.get("/items", async () => {
    // route logic
});

// Configure global error handler
KitFastifyMiddleware(app, {
    log: true,                 // Uses Fastify's built-in Pino logger (request.log.error)
    handleUnknownErrors: true, // Converts unexpected runtime crashes to 500 JSON
});

await app.listen({ port: 3000 });
```

### 2. Scoped Plugin Setup (`KitFastifyErrorHandler`)

Returns a pure error-handling function compatible with `fastify.setErrorHandler` or encapsulated plugins:

```typescript
import Fastify from "fastify";
import { KitFastifyErrorHandler } from "@wthek/fastify-middleware";

const app = Fastify();

// Use directly in setErrorHandler
app.setErrorHandler(
    KitFastifyErrorHandler({
        log: (err, req) => req.log.error({ err }, "Custom error message"),
        handleUnknownErrors: true,
    })
);

// Or inside a scoped Fastify plugin
app.register(async function apiV1(instance) {
    instance.setErrorHandler(KitFastifyErrorHandler());
    
    instance.get("/test", async () => {
        // ...
    });
}, { prefix: "/api/v1" });
```

## Options Reference

```typescript
interface IKitFastifyMiddlewareOptions {
    // When true, uses Fastify's built-in Pino logger (`request.log.error`).
    // When a callback is provided, receives (error: unknown, req: FastifyRequest).
    log?: boolean | ((error: unknown, req: FastifyRequest) => void);

    // When true, catches any uncaught non-KitHttpError and formats as a 500 response.
    handleUnknownErrors?: boolean;
}
```

