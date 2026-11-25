# Zod Validation Integration with @wthek

Guide for `@wthek/zod-transformer` and `@wthek/zod-express-interceptor`.

---

## 1. When to Use Which Package

- **Express.js Applications:** Use `@wthek/zod-express-interceptor`. It automatically intercepts uncaught `ZodError`s thrown by route handlers and transforms them before reaching the error middleware.
- **Fastify, NestJS, Restify, or Custom Handlers:** Use `@wthek/zod-transformer`. It provides both throwing and non-throwing conversion functions.

---

## 2. Express Interceptor (`@wthek/zod-express-interceptor`)

Mount the interceptor **after** route declarations and **before** your final error handler:

```typescript
import express from "express";
import { z } from "zod";
import { KitZodExpressInterceptor } from "@wthek/zod-express-interceptor";
import { KitExpressMiddleware } from "@wthek/express-middleware";

const app = express();
app.use(express.json());

// 1. Routes (can throw raw ZodError)
app.post("/submit", (req, res) => {
    const schema = z.object({ title: z.string().min(3) });
    const data = schema.parse(req.body); // Throws ZodError on failure
    res.json({ success: true, data });
});

// 2. Intercept Zod errors (must be AFTER routes)
app.use(KitZodExpressInterceptor({
    message: "Validation failed on payload",
    statusCode: 422, // e.g. Unprocessable Entity
}));

// 3. Final Error Middleware
app.use(KitExpressMiddleware());
```

---

## 3. Framework-Agnostic Transformer (`@wthek/zod-transformer`)

The transformer exports two functions:

### A. `fromZodError(error, options?)` — Non-Throwing (Preferred)
Returns a `KitHttpError` if the input is a `ZodError`, or `null` if it is not:

```typescript
import { fromZodError } from "@wthek/zod-transformer";

try {
    schema.parse(input);
} catch (err: unknown) {
    const kitError = fromZodError(err, {
        message: "Invalid form input",
        statusCode: 422,
    });

    if (kitError) {
        // Handled as KitHttpError
        reply.status(kitError.statusCode ?? 400).send(kitError);
        return;
    }
    
    // Not a ZodError - rethrow or pass along
    throw err;
}
```

### B. `KitZodTransformer(error, options?)` — Throwing
Converts a `ZodError` to a `KitHttpError` and throws it. If the error is not a `ZodError`, it re-throws the error unchanged:

```typescript
import { KitZodTransformer } from "@wthek/zod-transformer";

try {
    schema.parse(input);
} catch (err) {
    KitZodTransformer(err, { statusCode: 400 });
}
```

---

## 4. Error Payload Structure

Both packages attach the native Zod issues array directly to `error.details.issues`:

```json
{
  "code": 400,
  "msg": "Zod Validation Failed",
  "extra": {
    "issues": [
      {
        "code": "too_small",
        "minimum": 18,
        "type": "number",
        "inclusive": true,
        "exact": false,
        "message": "Number must be greater than or equal to 18",
        "path": ["age"]
      }
    ]
  }
}
```

