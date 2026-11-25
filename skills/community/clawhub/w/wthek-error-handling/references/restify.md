# Restify Error Handling with @wthek

Guide for implementing `@wthek/restify-middleware`.

---

## Installation

```bash
npm install @wthek/restify-middleware http-error-kit http-response-status-code
```

---

## Usage in Restify Server

In Restify, error handling is configured using server events (`restify.server.on("restifyError", ...)`):

```typescript
import restify from "restify";
import { KitRestifyMiddleware } from "@wthek/restify-middleware";
import { KitHttpError } from "http-error-kit";
import { NOT_FOUND } from "http-response-status-code";

const server = restify.createServer();
server.use(restify.plugins.bodyParser());

server.get("/user/:id", (req, res, next) => {
    // Throwing or returning a KitHttpError
    return next(new KitHttpError(NOT_FOUND, "User not found"));
});

// Attach KitRestifyMiddleware to the restifyError event
server.on(
    "restifyError",
    KitRestifyMiddleware({
        log: true,
        handleUnknownErrors: true,
    })
);

server.listen(8080, () => {
    console.log("Restify server running on port 8080");
});
```

---

## Options Reference

```typescript
interface IKitRestifyMiddlewareOptions {
    // When true, logs via console.error.
    // When a callback is provided, receives (error: unknown, req: restify.Request).
    log?: boolean | ((error: unknown, req: restify.Request) => void);

    // When true, catches any uncaught non-KitHttpError and formats as a structured 500 JSON response.
    handleUnknownErrors?: boolean;
}
```

---

## Key Differences from Express
- In Restify, errors are passed via `return next(error)` rather than `throw` in callback routes.
- Error handling is event-driven via `server.on("restifyError", ...)`.
- Built-in `res.headersSent` protection prevents double-reply crashes.

